# -*- coding: utf-8 -*-
"""Yombal Marché — boutique en ligne, comptes clients, panier et paiement."""

import logging
import os
from datetime import datetime

from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user

from extensions import db, login_manager, migrate
import mailer
import smser
from database import ensure_database
from models import (
    ORDER_STATUSES,
    ORDER_STATUS_AWAITING_PAYPAL,
    ORDER_STATUS_AWAITING_WIRE,
    ORDER_STATUS_CANCELLED,
    ORDER_STATUS_COD_CONFIRMED,
    ORDER_STATUS_PAID_DEMO,
    ORDER_STATUS_PAID_MANUAL,
    ORDER_STATUS_PAID_STRIPE,
    ORDER_STATUS_PENDING,
    ORDER_STATUS_SHIPPED,
    PAYMENT_CASH_DELIVERY,
    PAYMENT_DEMO,
    PAYMENT_PAYPAL,
    PAYMENT_STRIPE,
    PAYMENT_WIRE,
    Order,
    OrderItem,
    OrderStatusEvent,
    Producer,
    Product,
    User,
)
from models.constants import PRODUCT_CATEGORIES, SHOP_CATEGORY_ORDER
from models.constants import (
    ORDER_STATUS_HINTS,
    ORDER_STATUS_LABELS,
    ORDER_STATUS_PILL,
    ORDER_STATUS_STEP,
    ORDER_TRACKING_STEPS,
)
from models.order_tracking import find_order_by_reference_and_email
from routes.admin import admin_bp
from services import cart as cart_svc
from services import content as content_svc
from services import promo as promo_svc
from services import settings as settings_svc
from services import delivery_estimate as delivery_est_svc
from services import order_ui as order_ui_svc
from services import shipping as shipping_svc
from shop_auth import admin_required, is_shop_admin
from models.contact_message import ContactMessage

_APP_ROOT = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(_APP_ROOT, ".env"))

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY") or "dev-secret-change-me"
_sqlite_path = os.path.join(app.instance_path, "yombal.sqlite").replace("\\", "/")
_db_url = (os.environ.get("DATABASE_URL") or "").strip()
if _db_url.startswith("postgres://"):
    _db_url = _db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = _db_url or ("sqlite:///" + _sqlite_path)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
app.register_blueprint(admin_bp)
app.jinja_env.globals["product_categories"] = PRODUCT_CATEGORIES
app.jinja_env.globals["shop_category_order"] = SHOP_CATEGORY_ORDER
app.jinja_env.globals["order_status_labels"] = ORDER_STATUS_LABELS
app.jinja_env.globals["order_status_hints"] = ORDER_STATUS_HINTS
app.jinja_env.globals["order_status_step"] = ORDER_STATUS_STEP
app.jinja_env.globals["order_delivery_estimate"] = delivery_est_svc.estimate_for_order
app.jinja_env.globals["checkout_delivery_estimate"] = delivery_est_svc.estimate_checkout_preview
app.jinja_env.globals["order_status_pills"] = ORDER_STATUS_PILL

try:
    import stripe as stripe_sdk
except ImportError:
    stripe_sdk = None


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


SERVICE_CATEGORIES = [
    {
        "id": "boutique",
        "title": "Boutique Yombal Marché",
        "prestations": [
            "Produits alimentaires",
            "Produits cosmétiques",
            "Livraison à domicile",
            "Prix abordables",
            "Boutique en ligne",
        ],
    },
]

PRESTATION_CATEGORY = {
    "Produits alimentaires": "alimentaire",
    "Produits cosmétiques": "cosmetique",
}


def _cart_raw():
    return cart_svc.cart_raw()


def _cart_items():
    return cart_svc.cart_items()


def _cart_count():
    return cart_svc.cart_count()


def _admin_emails_set():
    from shop_auth import admin_emails_set
    return admin_emails_set()


def _is_shop_admin():
    return is_shop_admin()


def _order_contact(order):
    """Utilisateur enregistré ou coordonnées invité pour les e-mails."""
    if order.user_id:
        return db.session.get(User, order.user_id)
    contact = type("GuestContact", (), {})()
    contact.email = (order.guest_email or "").strip()
    contact.name = (order.guest_name or "").strip() or None
    return contact


def _phone_from_form():
    return (request.form.get("customer_phone") or request.form.get("guest_phone") or "").strip()


def _order_suivi_url(order):
    return url_for("suivi_commande_detail", order_id=order.id, _external=True)


def _notify_order_created(order):
    contact = _order_contact(order)
    suivi = _order_suivi_url(order)
    try:
        if contact and contact.email:
            mailer.notify_customer_order_created(order, contact)
            mailer.notify_admin_new_order(order, contact)
    except Exception:
        pass
    try:
        smser.notify_customer_order_created(order, suivi_url=suivi)
    except Exception:
        pass


def _notify_payment_received(order):
    contact = _order_contact(order)
    suivi = _order_suivi_url(order)
    try:
        if contact and contact.email:
            mailer.notify_customer_payment_received(order, contact, suivi_url=suivi)
            mailer.notify_admin_payment_received(order, contact)
    except Exception:
        pass
    try:
        smser.notify_customer_payment_received(order, suivi_url=suivi)
    except Exception:
        pass


def _notify_status_change(order, old_status, new_status):
    if old_status == new_status:
        return
    if not getattr(order, "notify_status_updates", True):
        return
    if new_status == ORDER_STATUS_CANCELLED:
        _notify_order_cancelled(order, by_customer=False)
        return
    if new_status in (
        ORDER_STATUS_PAID_STRIPE,
        ORDER_STATUS_PAID_DEMO,
        ORDER_STATUS_PAID_MANUAL,
    ):
        return
    contact = _order_contact(order)
    suivi = _order_suivi_url(order)
    try:
        if contact and contact.email:
            mailer.notify_customer_status_update(order, contact, old_status, new_status, suivi_url=suivi)
    except Exception:
        pass
    try:
        smser.notify_customer_status_update(order, old_status, new_status, suivi_url=suivi)
    except Exception:
        pass


def _notify_order_cancelled(order, *, by_customer=False):
    if not getattr(order, "notify_status_updates", True):
        return
    contact = _order_contact(order)
    suivi = _order_suivi_url(order)
    try:
        if contact and contact.email:
            mailer.notify_customer_order_cancelled(
                order, contact, suivi_url=suivi, by_customer=by_customer
            )
            mailer.notify_admin_order_cancelled(order, contact, by_customer=by_customer)
    except Exception:
        pass
    try:
        smser.notify_customer_status_update(
            order, order.status, ORDER_STATUS_CANCELLED, suivi_url=suivi
        )
    except Exception:
        pass


def _guest_order_ids():
    return [int(x) for x in (session.get("guest_orders") or []) if str(x).isdigit()]


def _remember_guest_order(order_id):
    ids = _guest_order_ids()
    if order_id not in ids:
        ids.append(order_id)
        session["guest_orders"] = ids[-20:]
        session.modified = True


def _can_access_order(order):
    if not order:
        return False
    if current_user.is_authenticated and order.user_id == current_user.id:
        return True
    if not order.user_id and order.id in _guest_order_ids():
        return True
    return False


def _apply_stripe_pi_to_order(order, pi):
    """Marque la commande payée Stripe et envoie les mails (idempotent si déjà payée)."""
    if order.is_paid():
        return "already_paid"
    amt = int(getattr(pi, "amount", 0) or 0)
    if amt != int(order.total_cents):
        return "amount_bad"
    if getattr(pi, "status", "") != "succeeded":
        return "not_success"
    order.set_status(ORDER_STATUS_PAID_STRIPE, note="Paiement Stripe confirmé")
    order.payment_method = PAYMENT_STRIPE
    order.stripe_session_id = getattr(pi, "id", "") or ""
    db.session.commit()
    _notify_payment_received(order)
    return "ok"


@app.context_processor
def inject_globals():
    shop = settings_svc.shop_settings()
    return {
        "current_year": datetime.now().year,
        "service_categories": SERVICE_CATEGORIES,
        "cart_count": _cart_count(),
        "shop_contact_email": shop.get("shop_contact_email"),
        "shop_settings": shop,
        "is_shop_admin": _is_shop_admin(),
        "product_categories": PRODUCT_CATEGORIES,
        "shop_category_order": SHOP_CATEGORY_ORDER,
        "order_status_labels": ORDER_STATUS_LABELS,
        "order_status_hints": ORDER_STATUS_HINTS,
        "order_status_step": ORDER_STATUS_STEP,
        "order_tracking_steps": ORDER_TRACKING_STEPS,
        "order_status_pills": ORDER_STATUS_PILL,
    }


@app.before_request
def ensure_session_cart():
    session.setdefault("cart", {})


@app.route("/healthz")
def healthz():
    """Réponse minimale pour les health checks Render (sans accès DB)."""
    return "ok", 200, {"Cache-Control": "no-store"}


def _bank_env():
    return {
        "name": (os.environ.get("BANK_NAME") or "").strip(),
        "iban": (os.environ.get("BANK_IBAN") or "").strip(),
        "bic": (os.environ.get("BANK_BIC") or "").strip(),
        "holder": (os.environ.get("BANK_HOLDER") or "").strip(),
    }


def _paypal_env():
    return {
        "email": (os.environ.get("PAYPAL_EMAIL") or "").strip(),
        "me_url": (os.environ.get("PAYPAL_ME_URL") or "").strip(),
    }


with app.app_context():
    ensure_database(app)


def _product_query_active():
    return Product.query.filter_by(is_active=True)


def _producer_query_active():
    return Producer.query.filter_by(is_active=True)


def _delivery_from_form():
    is_gift = request.form.get("is_gift") == "1"
    gift_message = (request.form.get("gift_message") or "").strip() or None
    notes = (request.form.get("customer_notes") or "").strip() or None
    if is_gift and gift_message and not notes:
        notes = gift_message
    return {
        "delivery_line1": (request.form.get("delivery_line1") or "").strip(),
        "delivery_line2": (request.form.get("delivery_line2") or "").strip() or None,
        "delivery_city": (request.form.get("delivery_city") or "").strip(),
        "delivery_postal_code": (request.form.get("delivery_postal_code") or "").strip(),
        "delivery_country": (request.form.get("delivery_country") or "FR").strip().upper()[:2],
        "customer_notes": notes,
        "is_gift": is_gift,
        "gift_message": gift_message,
    }


def _checkout_preview(items, subtotal_cents, form=None):
    form = form or {}
    postal = (form.get("delivery_postal_code") or request.form.get("delivery_postal_code") or "").strip()
    promo_code = (form.get("promo_code") or request.form.get("promo_code") or "").strip()
    shipping = shipping_svc.shipping_cents_for_postal(postal, subtotal_cents) if postal else 0
    promo, discount, promo_err = promo_svc.validate_promo(promo_code, subtotal_cents)
    total = max(0, subtotal_cents + shipping - discount)
    return {
        "shipping_cents": shipping,
        "discount_cents": discount,
        "promo_code": promo.code if promo else None,
        "promo_error": promo_err,
        "total_cents": total,
        "subtotal_cents": subtotal_cents,
    }


def _apply_delivery_to_order(order, delivery):
    for key in (
        "delivery_line1",
        "delivery_line2",
        "delivery_city",
        "delivery_postal_code",
        "delivery_country",
        "customer_notes",
        "is_gift",
        "gift_message",
    ):
        if key in delivery:
            setattr(order, key, delivery[key])


@app.route("/")
def index():
    featured = _product_query_active().order_by(Product.id).limit(6).all()
    featured_producers = _producer_query_active().order_by(Producer.id).limit(4).all()
    featured_recipes = [_build_recipe_view(r) for r in content_svc.all_recipe_defs()[:3]]
    featured_coffrets = [_build_product_bundle(c) for c in content_svc.all_coffret_defs()[:2]]
    return render_template(
        "index.html",
        featured_products=featured,
        featured_producers=featured_producers,
        featured_recipes=featured_recipes,
        featured_coffrets=featured_coffrets,
    )


@app.route("/services")
def services():
    sections = []
    for label in SERVICE_CATEGORIES[0]["prestations"]:
        cat = PRESTATION_CATEGORY.get(label)
        products = (
            _product_query_active().filter_by(category=cat).order_by(Product.name).all()
            if cat
            else []
        )
        sections.append({"title": label, "products": products, "has_products": bool(products)})
    return render_template("services.html", sections=sections)


@app.route("/boutique")
def boutique():
    cat = request.args.get("categorie")
    q = _product_query_active()
    if cat:
        q = q.filter_by(category=cat)
    products = q.order_by(Product.category, Product.name).all()
    shop_counts = {
        key: _product_query_active().filter_by(category=key).count()
        for key in SHOP_CATEGORY_ORDER
    }
    total_products = _product_query_active().count()
    return render_template(
        "boutique/index.html",
        products=products,
        filter_cat=cat,
        shop_counts=shop_counts,
        total_products=total_products,
    )


@app.route("/produit/<slug>")
def product_detail(slug):
    product = _product_query_active().filter_by(slug=slug).first_or_404()
    related = (
        _product_query_active()
        .filter(Product.category == product.category, Product.id != product.id)
        .limit(4)
        .all()
    )
    related_recipes = [
        _build_recipe_view(r) for r in content_svc.recipes_for_product_slug(slug)[:3]
    ]
    return render_template(
        "boutique/detail.html",
        product=product,
        related=related,
        related_recipes=related_recipes,
    )


@app.route("/producteurs")
def producteurs():
    producers = _producer_query_active().order_by(Producer.name).all()
    return render_template("producteurs/index.html", producers=producers)


@app.route("/producteur/<slug>")
def producteur_detail(slug):
    producer = _producer_query_active().filter_by(slug=slug).first_or_404()
    products = producer.active_products().all()
    return render_template("producteurs/detail.html", producer=producer, products=products)


# --- Carte des saveurs (expérience traçabilité) ---
SAVEURS_PIN_DEFS = (
    # x, y dans un repère 1000x500 (puis converti en % dans la route)
    {"producer_slug": "aminata-diallo", "x": 260, "y": 330, "label": "Casamance"},
    {"producer_slug": "fatou-ndiaye", "x": 420, "y": 300, "label": "Thiès"},
    {"producer_slug": "moussa-kone", "x": 480, "y": 345, "label": "Burkina Faso"},
    {"producer_slug": "cooperative-tafraout", "x": 420, "y": 165, "label": "Maroc"},
    {"producer_slug": "atelier-sahel", "x": 390, "y": 205, "label": "Savon noir"},
    {"producer_slug": "famille-bencherif", "x": 360, "y": 210, "label": "Algérie"},
    {"producer_slug": "oasis-jericho", "x": 650, "y": 235, "label": "Vallée du Jourdain"},
    {"producer_slug": "rucher-alpilles", "x": 160, "y": 150, "label": "Alpilles"},
)


def _saveurs_pins():
    pins = []
    producers = _producer_query_active().filter(
        Producer.map_x.isnot(None),
        Producer.map_y.isnot(None),
    ).order_by(Producer.name)
    for producer in producers:
        pins.append(
            {
                "producer": producer,
                "x_pct": round(producer.map_x / 1000 * 100, 2),
                "y_pct": round(producer.map_y / 500 * 100, 2),
                "label": producer.map_label or producer.region,
                "products": producer.active_products().limit(3).all(),
            }
        )
    if pins:
        return pins
    for d in SAVEURS_PIN_DEFS:
        producer = _producer_query_active().filter_by(slug=d["producer_slug"]).first()
        if not producer:
            continue
        pins.append(
            {
                "producer": producer,
                "x_pct": round(d["x"] / 1000 * 100, 2),
                "y_pct": round(d["y"] / 500 * 100, 2),
                "label": d.get("label") or producer.region,
                "products": producer.active_products().limit(3).all(),
            }
        )
    return pins


@app.route("/decouvrir")
def decouvrir():
    return render_template("decouvrir.html")


@app.route("/saveurs")
def saveurs():
    pins = _saveurs_pins()
    return render_template("saveurs.html", pins=pins)


def _build_product_bundle(bundle_def):
    """Enrichit un bundle (recette ou coffret) avec les produits du catalogue."""
    items = []
    total_cents = 0
    for ing in bundle_def.get("ingredients", []):
        product = _product_query_active().filter_by(slug=ing["product_slug"]).first()
        qty = max(1, min(20, int(ing.get("quantity", 1))))
        if product:
            line_cents = product.price_cents * qty
            items.append({**ing, "product": product, "quantity": qty, "line_cents": line_cents})
            total_cents += line_cents
    return {
        **bundle_def,
        "cart_items": items,
        "total_cents": total_cents,
        "ingredient_count": len(bundle_def.get("ingredients", [])),
        "available_count": len(items),
        "is_complete": len(items) == len(bundle_def.get("ingredients", [])),
    }


def _build_recipe_view(recipe_def):
    return _build_product_bundle(recipe_def)


@app.route("/recettes")
def recettes():
    kind = request.args.get("type")
    recipes = [_build_recipe_view(r) for r in content_svc.all_recipe_defs() if not kind or r.get("kind") == kind]
    kinds = sorted({r.get("kind") for r in content_svc.all_recipe_defs() if r.get("kind")})
    return render_template("recettes/index.html", recipes=recipes, kinds=kinds, filter_kind=kind)


@app.route("/recette/<slug>")
def recette_detail(slug):
    recipe_def = content_svc.recipe_def_by_slug(slug)
    if not recipe_def:
        abort(404)
    recipe = _build_recipe_view(recipe_def)
    return render_template("recettes/detail.html", recipe=recipe)


@app.route("/recette/<slug>/panier", methods=["POST"])
def recette_panier(slug):
    recipe_def = content_svc.recipe_def_by_slug(slug)
    if not recipe_def:
        abort(404)
    recipe = _build_recipe_view(recipe_def)
    if not recipe["cart_items"]:
        flash("Aucun ingrédient disponible pour cette recette.", "warning")
        return redirect(url_for("recette_detail", slug=slug))

    cart = dict(session.get("cart") or {})
    for ing in recipe["cart_items"]:
        ok, err = cart_svc.add_to_cart(ing["product"].id, ing["quantity"], "recipe", slug)
        if not ok:
            flash(err, "danger")
            return redirect(url_for("recette_detail", slug=slug))

    added = len(recipe["cart_items"])
    if recipe["is_complete"]:
        flash(f"Panier recette prêt : {added} ingrédient(s) ajouté(s) pour « {recipe['title']} ».", "success")
    else:
        flash(
            f"{added} ingrédient(s) ajouté(s) — certains produits sont indisponibles pour le moment.",
            "warning",
        )
    nxt = request.form.get("next") or url_for("panier")
    if nxt.startswith("/") and not nxt.startswith("//"):
        return redirect(nxt)
    return redirect(url_for("panier"))


@app.route("/coffrets")
def coffrets():
    theme = request.args.get("theme")
    items = [_build_product_bundle(c) for c in content_svc.all_coffret_defs() if not theme or c.get("theme") == theme]
    themes = sorted({c.get("theme") for c in content_svc.all_coffret_defs() if c.get("theme")})
    return render_template("coffrets/index.html", coffrets=items, themes=themes, filter_theme=theme)


@app.route("/coffret/<slug>")
def coffret_detail(slug):
    coffret_def = content_svc.coffret_def_by_slug(slug)
    if not coffret_def:
        abort(404)
    coffret = _build_product_bundle(coffret_def)
    return render_template("coffrets/detail.html", coffret=coffret)


@app.route("/coffret/<slug>/panier", methods=["POST"])
def coffret_panier(slug):
    coffret_def = content_svc.coffret_def_by_slug(slug)
    if not coffret_def:
        abort(404)
    coffret = _build_product_bundle(coffret_def)
    if not coffret["cart_items"]:
        flash("Aucun produit disponible pour ce coffret.", "warning")
        return redirect(url_for("coffret_detail", slug=slug))

    for ing in coffret["cart_items"]:
        ok, err = cart_svc.add_to_cart(ing["product"].id, ing["quantity"], "coffret", slug)
        if not ok:
            flash(err, "danger")
            return redirect(url_for("coffret_detail", slug=slug))

    added = len(coffret["cart_items"])
    if coffret["is_complete"]:
        flash(f"Coffret ajouté au panier : {added} produit(s) pour « {coffret['title']} ».", "success")
    else:
        flash(
            f"{added} produit(s) ajouté(s) — certains articles sont indisponibles pour le moment.",
            "warning",
        )
    nxt = request.form.get("next") or url_for("panier")
    if nxt.startswith("/") and not nxt.startswith("//"):
        return redirect(nxt)
    return redirect(url_for("panier"))


@app.route("/panier/ajouter", methods=["POST"])
def panier_ajouter():
    pid = request.form.get("product_id", type=int)
    qty = request.form.get("quantity", default=1, type=int) or 1
    if not pid:
        flash("Produit introuvable.", "danger")
        return redirect(request.referrer or url_for("boutique"))
    product = db.session.get(Product, pid)
    if not product or not product.is_active:
        flash("Produit introuvable.", "danger")
        return redirect(request.referrer or url_for("boutique"))
    ok, err = cart_svc.add_to_cart(pid, qty)
    if not ok:
        flash(err or "Produit introuvable.", "danger")
        return redirect(request.referrer or url_for("boutique"))
    flash("Produit ajouté au panier.", "success")
    next_url = request.form.get("next") or request.referrer
    return redirect(next_url or url_for("panier"))


@app.route("/panier")
def panier():
    items, total = _cart_items()
    item_count = sum(row["quantity"] for row in items)
    return render_template("panier.html", items=items, total_cents=total, cart_item_count=item_count)


@app.route("/panier/modifier", methods=["POST"])
def panier_modifier():
    pid = str(request.form.get("product_id", ""))
    qty = request.form.get("quantity", type=int)
    ok, err = cart_svc.set_cart_qty(pid, qty)
    if not ok:
        flash(err, "warning")
    return redirect(url_for("panier"))


@app.route("/auth/inscription", methods=["GET", "POST"])
def register():
    abort(404)


@app.route("/auth/connexion", methods=["GET", "POST"])
def login():
    abort(404)


@app.route("/auth/deconnexion")
@login_required
def logout():
    logout_user()
    flash("Vous êtes déconnecté.", "info")
    return redirect(url_for("index"))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    items, subtotal = _cart_items()
    if not items:
        flash("Votre panier est vide.", "warning")
        return redirect(url_for("boutique"))
    preview = _checkout_preview(items, subtotal, request.form if request.method == "POST" else None)

    def _render_checkout(form=None, preview_override=None):
        p = preview_override or preview
        return render_template(
            "checkout.html",
            items=items,
            subtotal_cents=subtotal,
            shipping_cents=p["shipping_cents"],
            discount_cents=p["discount_cents"],
            total_cents=p["total_cents"],
            promo_code=p.get("promo_code") or ((form or {}).get("promo_code") or ""),
            promo_error=p.get("promo_error"),
            guest_form=form,
        )

    if request.method == "POST":
        delivery = _delivery_from_form()
        preview = _checkout_preview(items, subtotal, request.form)
        if preview.get("promo_error") and (request.form.get("promo_code") or "").strip():
            flash(preview["promo_error"], "danger")
            return _render_checkout(request.form, preview)
        if len(delivery["delivery_line1"]) < 5:
            flash("Indiquez une adresse de livraison complète.", "danger")
            return _render_checkout(request.form, preview)
        if len(delivery["delivery_city"]) < 2 or len(delivery["delivery_postal_code"]) < 4:
            flash("Indiquez la ville et le code postal.", "danger")
            return _render_checkout(request.form, preview)

        if current_user.is_authenticated:
            phone = _phone_from_form()
            if len(phone) < 6:
                flash("Indiquez un numéro de téléphone pour la livraison et les confirmations SMS.", "danger")
                return _render_checkout(request.form, preview)
            order = Order(
                user_id=current_user.id,
                guest_phone=phone,
                subtotal_cents=subtotal,
                shipping_cents=preview["shipping_cents"],
                discount_cents=preview["discount_cents"],
                total_cents=preview["total_cents"],
                promo_code=preview.get("promo_code"),
                status=ORDER_STATUS_PENDING,
                notify_status_updates=request.form.get("notify_status_updates") == "1",
            )
            _apply_delivery_to_order(order, delivery)
        else:
            email = (request.form.get("guest_email") or "").strip().lower()
            name = (request.form.get("guest_name") or "").strip()
            phone = _phone_from_form()
            if not email or "@" not in email:
                flash("Indiquez une adresse e-mail valide pour la commande.", "danger")
                return _render_checkout(request.form, preview)
            if len(name) < 2:
                flash("Indiquez votre nom pour la livraison.", "danger")
                return _render_checkout(request.form, preview)
            if len(phone) < 6:
                flash("Indiquez un numéro de téléphone valide (confirmation SMS).", "danger")
                return _render_checkout(request.form, preview)
            order = Order(
                user_id=None,
                guest_email=email,
                guest_name=name,
                guest_phone=phone,
                subtotal_cents=subtotal,
                shipping_cents=preview["shipping_cents"],
                discount_cents=preview["discount_cents"],
                total_cents=preview["total_cents"],
                promo_code=preview.get("promo_code"),
                status=ORDER_STATUS_PENDING,
                notify_status_updates=request.form.get("notify_status_updates") == "1",
            )
            _apply_delivery_to_order(order, delivery)

        order.status_events.append(
            OrderStatusEvent(to_status=ORDER_STATUS_PENDING, note="Commande créée")
        )
        db.session.add(order)
        db.session.flush()
        for row in items:
            db.session.add(
                OrderItem.from_product(
                    row["product"],
                    row["quantity"],
                    order.id,
                    bundle_type=row.get("bundle_type"),
                    bundle_slug=row.get("bundle_slug"),
                )
            )
        cart_svc.decrement_stock_for_order(items)
        promo_obj = None
        if preview.get("promo_code"):
            promo_obj = promo_svc.validate_promo(preview["promo_code"], subtotal)[0]
        promo_svc.apply_promo_use(promo_obj)
        db.session.commit()
        if not order.user_id:
            _remember_guest_order(order.id)
        cart_svc.clear_cart()
        try:
            _notify_order_created(order)
        except Exception:
            pass
        return redirect(url_for("paiement", order_id=order.id))
    return _render_checkout()


@app.route("/paiement/<int:order_id>")
def paiement(order_id):
    order = db.session.get(Order, order_id)
    if not _can_access_order(order):
        if not current_user.is_authenticated:
            flash("Finalisez une commande invité depuis ce navigateur pour accéder au paiement.", "warning")
            return redirect(url_for("checkout"))
        abort(403)
    if order.is_paid():
        return _redirect_suivi_commande(order.id, "Cette commande est déjà réglée.", "info")
    stripe_key = os.environ.get("STRIPE_SECRET_KEY")
    publishable = (os.environ.get("STRIPE_PUBLISHABLE_KEY") or "").strip()
    stripe_ok = bool(stripe_key and stripe_sdk and publishable)

    manual_states = (ORDER_STATUS_AWAITING_WIRE, ORDER_STATUS_AWAITING_PAYPAL, ORDER_STATUS_COD_CONFIRMED)
    payment_phase = "manual_instructions" if order.status in manual_states else "choose"

    stripe_client_secret = None
    stripe_pi_error = None
    if stripe_ok and payment_phase == "choose":
        try:
            stripe_sdk.api_key = stripe_key
            intent = stripe_sdk.PaymentIntent.create(
                amount=order.total_cents,
                currency="eur",
                automatic_payment_methods={"enabled": True},
                metadata={
                    "order_id": str(order.id),
                    "user_id": str(order.user_id or ""),
                },
            )
            stripe_client_secret = intent.client_secret
        except Exception as exc:
            stripe_pi_error = str(exc)

    return render_template(
        "paiement.html",
        order=order,
        stripe_ok=stripe_ok,
        stripe_publishable=publishable,
        stripe_client_secret=stripe_client_secret,
        stripe_pi_error=stripe_pi_error,
        payment_phase=payment_phase,
        bank=_bank_env(),
        paypal=_paypal_env(),
        stripe_return_url=url_for("paiement_stripe_retour", _external=True),
    )


@app.route("/paiement/<int:order_id>/manuel", methods=["POST"])
def paiement_valider_manuel(order_id):
    order = db.session.get(Order, order_id)
    if not _can_access_order(order):
        abort(403)
    if order.is_paid():
        return _redirect_suivi_commande(order.id, "Cette commande est déjà réglée.", "info")
    manual_states = (ORDER_STATUS_AWAITING_WIRE, ORDER_STATUS_AWAITING_PAYPAL, ORDER_STATUS_COD_CONFIRMED)
    if order.status in manual_states:
        flash("Ce mode de paiement est déjà enregistré pour cette commande.", "info")
        return redirect(url_for("paiement", order_id=order.id))

    methode = (request.form.get("methode") or "").strip()
    mapping = {
        "virement": (ORDER_STATUS_AWAITING_WIRE, PAYMENT_WIRE),
        "paypal": (ORDER_STATUS_AWAITING_PAYPAL, PAYMENT_PAYPAL),
        "especes_livraison": (ORDER_STATUS_COD_CONFIRMED, PAYMENT_CASH_DELIVERY),
    }
    if methode not in mapping:
        flash("Veuillez choisir un mode de paiement valide.", "danger")
        return redirect(url_for("paiement", order_id=order.id))

    new_status, pm = mapping[methode]
    order.set_status(new_status, note=f"Choix client : {pm}")
    order.payment_method = pm
    db.session.commit()
    try:
        mailer.notify_admin_manual_payment_choice(order, _order_contact(order))
    except Exception:
        pass
    flash(
        "Votre choix est enregistré. Suivez les instructions ci-dessous pour finaliser le règlement.",
        "success",
    )
    return redirect(url_for("paiement", order_id=order.id))


@app.route("/paiement/stripe/retour")
def paiement_stripe_retour():
    """Après saisie carte (3-D Secure inclus), Stripe renvoie ici avec payment_intent=…"""
    pi_id = request.args.get("payment_intent")
    redirect_status = request.args.get("redirect_status") or ""
    if not pi_id or not stripe_sdk:
        flash("Retour de paiement incomplet.", "warning")
        return redirect(url_for("boutique"))

    key = os.environ.get("STRIPE_SECRET_KEY")
    if not key:
        flash("Stripe n’est pas configuré.", "danger")
        return redirect(url_for("boutique"))

    stripe_sdk.api_key = key
    try:
        pi = stripe_sdk.PaymentIntent.retrieve(pi_id)
    except Exception:
        flash("Paiement introuvable ou invalide.", "danger")
        return redirect(url_for("boutique"))

    oid = int(pi.metadata.get("order_id") or 0)
    order = db.session.get(Order, oid)
    if not order or not _can_access_order(order):
        flash("Commande introuvable.", "danger")
        return redirect(url_for("boutique"))
    meta_uid = str(pi.metadata.get("user_id") or "")
    if meta_uid and order.user_id and meta_uid != str(order.user_id):
        flash("Commande introuvable.", "danger")
        return redirect(url_for("boutique"))

    result = _apply_stripe_pi_to_order(order, pi)
    if result == "already_paid":
        return _redirect_suivi_commande(order.id, "Cette commande est déjà réglée.", "info")
    if result == "amount_bad":
        flash("Montant du paiement incompatible avec la commande.", "danger")
        return redirect(url_for("paiement", order_id=order.id))
    if result == "ok":
        return _redirect_suivi_commande(order.id, "Paiement par carte confirmé. Merci pour votre commande !")

    if redirect_status == "failed":
        flash(
            "Le paiement par carte a été refusé ou annulé. Réessayez ou choisissez un autre mode.",
            "danger",
        )
        return redirect(url_for("paiement", order_id=order.id))

    flash(
        "Paiement en cours de traitement. Si un montant a été réservé, la confirmation peut prendre quelques instants.",
        "warning",
    )
    return redirect(url_for("paiement", order_id=order.id))


@app.route("/paiement/succes")
def paiement_succes():
    """Compatibilité : anciennes redirections Stripe Checkout (session_id)."""
    session_id = request.args.get("session_id")
    key = os.environ.get("STRIPE_SECRET_KEY")
    if not session_id or not stripe_sdk or not key:
        flash("Impossible de vérifier le paiement.", "warning")
        return redirect(url_for("boutique"))
    stripe_sdk.api_key = key
    try:
        checkout_session = stripe_sdk.checkout.Session.retrieve(session_id)
    except Exception:
        flash("Session de paiement invalide.", "danger")
        return redirect(url_for("boutique"))
    if checkout_session.payment_status != "paid":
        flash("Paiement non finalisé.", "warning")
        return redirect(url_for("boutique"))
    oid = int(checkout_session.metadata.get("order_id") or 0)
    order = db.session.get(Order, oid)
    if not order or not _can_access_order(order):
        flash("Commande introuvable.", "danger")
        return redirect(url_for("boutique"))
    if not order.is_paid():
        order.set_status(ORDER_STATUS_PAID_STRIPE, note="Stripe Checkout (legacy)")
        order.payment_method = PAYMENT_STRIPE
        db.session.commit()
        try:
            _notify_payment_received(order)
        except Exception:
            pass
    return _redirect_suivi_commande(order.id, "Paiement confirmé. Merci pour votre commande !")


@app.route("/webhooks/stripe", methods=["GET", "POST"])
def webhooks_stripe():
    """Confirmation automatique des paiements (évite de dépendre uniquement du navigateur)."""
    if request.method == "GET":
        return {
            "ok": True,
            "endpoint": "stripe_webhook",
            "message": "Endpoint actif. Stripe envoie des requêtes POST (pas GET depuis le navigateur).",
        }, 200

    if not stripe_sdk:
        abort(501)
    wh_secret = (os.environ.get("STRIPE_WEBHOOK_SECRET") or "").strip()
    if not wh_secret:
        logger.warning("Webhook Stripe ignoré : définissez STRIPE_WEBHOOK_SECRET dans .env")
        return "", 200
    payload = request.data
    sig = request.headers.get("Stripe-Signature") or ""
    try:
        event = stripe_sdk.Webhook.construct_event(payload, sig, wh_secret)
    except ValueError:
        abort(400)
    except Exception:
        abort(400)

    if event["type"] == "payment_intent.succeeded":
        obj = event["data"]["object"]
        from types import SimpleNamespace

        pi = SimpleNamespace(
            id=obj.get("id"),
            amount=obj.get("amount"),
            status=obj.get("status"),
            metadata=obj.get("metadata") or {},
        )
        oid = int(pi.metadata.get("order_id") or 0)
        order = db.session.get(Order, oid)
        if order:
            meta_uid = str(pi.metadata.get("user_id") or "")
            if meta_uid and order.user_id and meta_uid != str(order.user_id):
                return "", 200
            _apply_stripe_pi_to_order(order, pi)

    return "", 200


@app.route("/paiement/annule/<int:order_id>")
def paiement_annule(order_id):
    order = db.session.get(Order, order_id)
    if not _can_access_order(order):
        abort(403)
    flash("Paiement annulé. Vous pouvez réessayer quand vous voulez.", "info")
    return redirect(url_for("paiement", order_id=order_id))


@app.route("/paiement/demo/<int:order_id>", methods=["POST"])
def paiement_demo(order_id):
    order = db.session.get(Order, order_id)
    if not _can_access_order(order):
        abort(403)
    order.set_status(ORDER_STATUS_PAID_DEMO, note="Paiement démonstration")
    order.payment_method = PAYMENT_DEMO
    db.session.commit()
    try:
        _notify_payment_received(order)
    except Exception:
        pass
    return _redirect_suivi_commande(order.id, "Paiement simulé enregistré (mode démonstration).")


@app.route("/admin/commandes")
@admin_required
def admin_orders():
    status_filter = (request.args.get("status") or "").strip()
    q = Order.query
    if status_filter:
        q = q.filter(Order.status == status_filter)
    orders = q.order_by(Order.created_at.desc()).limit(250).all()
    return render_template(
        "admin/orders.html",
        orders=orders,
        status_filter=status_filter,
    )


@app.route("/admin/commande/<int:order_id>", methods=["GET", "POST"])
@admin_required
def admin_order_detail(order_id):
    order = db.session.get(Order, order_id)
    if not order:
        abort(404)
    allowed_status = ORDER_STATUSES
    if request.method == "POST":
        new_status = (request.form.get("new_status") or "").strip()
        if new_status in allowed_status:
            old = order.status
            order.set_status(
                new_status,
                note="Mise à jour admin",
                actor_user_id=current_user.id,
            )
            if new_status == ORDER_STATUS_PAID_MANUAL and not old.startswith("paid"):
                order.payment_method = order.payment_method or PAYMENT_WIRE
                try:
                    _notify_payment_received(order)
                except Exception:
                    pass
            else:
                try:
                    _notify_status_change(order, old, new_status)
                except Exception:
                    pass
            db.session.commit()
            flash("Statut de commande mis à jour.", "success")
        else:
            flash("Statut invalide.", "danger")
        return redirect(url_for("admin_order_detail", order_id=order.id))
    customer = db.session.get(User, order.user_id) if order.user_id else None
    return render_template(
        "admin/order_detail.html",
        order=order,
        customer=customer,
        allowed_status=sorted(allowed_status),
        status_events=order.status_events.all(),
    )


@app.route("/mentions-legales")
def mentions_legales():
    return render_template("legal/mentions.html")


@app.route("/cgv")
def cgv():
    return render_template("legal/cgv.html")


@app.route("/apropos")
def apropos():
    featured_producers = _producer_query_active().order_by(Producer.id).limit(3).all()
    return render_template(
        "apropos.html",
        featured_producers=featured_producers,
        stats={
            "products": _product_query_active().count(),
            "producers": _producer_query_active().count(),
        },
    )


def _recent_orders_for_user():
    if current_user.is_authenticated:
        return (
            Order.query.filter_by(user_id=current_user.id)
            .order_by(Order.created_at.desc())
            .limit(30)
            .all()
        )
    ids = _guest_order_ids()
    if not ids:
        return []
    return (
        Order.query.filter(Order.id.in_(ids))
        .order_by(Order.created_at.desc())
        .all()
    )


def _redirect_suivi_commande(order_id, message=None, category="success"):
    if message:
        flash(message, category)
    kwargs = {"order_id": order_id}
    if category == "success" and message:
        kwargs["confirmed"] = 1
    return redirect(url_for("suivi_commande_detail", **kwargs))


@app.route("/suivi-commande", methods=["GET", "POST"])
def suivi_commande():
    recent_orders = _recent_orders_for_user()
    if request.method == "POST":
        ref = (request.form.get("order_ref") or "").strip()
        email = (request.form.get("email") or "").strip()
        if not ref or not email:
            flash("Indiquez la référence de commande et votre e-mail.", "warning")
        else:
            order = find_order_by_reference_and_email(ref, email)
            if not order:
                flash("Aucune commande trouvée. Vérifiez la référence et l'e-mail utilisés à la commande.", "danger")
            else:
                if not order.user_id:
                    _remember_guest_order(order.id)
                return redirect(url_for("suivi_commande_detail", order_id=order.id))
    order_cards = []
    for o in recent_orders:
        pill = order_ui_svc.order_status_pill(o.status)
        order_cards.append(
            {
                "order": o,
                "preview_lines": order_ui_svc.order_preview_lines(o),
                "extra_item_count": order_ui_svc.order_extra_count(o),
                "pill_label": pill[0],
                "pill_class": pill[1],
                "can_pay": order_ui_svc.order_can_pay(o),
            }
        )
    return render_template("commandes/suivi.html", recent_orders=recent_orders, order_cards=order_cards)


@app.route("/suivi-commande/<int:order_id>")
def suivi_commande_detail(order_id):
    order = db.session.get(Order, order_id)
    if not _can_access_order(order):
        flash("Accès refusé. Utilisez le formulaire de suivi avec votre e-mail de commande.", "warning")
        return redirect(url_for("suivi_commande"))
    events = order.status_events.order_by(OrderStatusEvent.created_at.desc()).all()
    current_step = ORDER_STATUS_STEP.get(order.status, 1)
    pill = order_ui_svc.order_status_pill(order.status)
    return render_template(
        "commandes/detail.html",
        order=order,
        events=events,
        current_step=current_step,
        preview_lines=order_ui_svc.order_preview_lines(order),
        extra_item_count=order_ui_svc.order_extra_count(order),
        status_pill_label=pill[0],
        status_pill_class=pill[1],
        can_pay=order_ui_svc.order_can_pay(order),
        can_reorder=order_ui_svc.order_can_reorder(order),
        can_cancel=order_ui_svc.order_can_cancel(order),
        delivery_estimate=delivery_est_svc.estimate_for_order(order),
    )


@app.route("/commande/<int:order_id>/annuler", methods=["POST"])
def commande_annuler(order_id):
    order = db.session.get(Order, order_id)
    if not _can_access_order(order):
        abort(403)
    if not order_ui_svc.order_can_cancel(order):
        flash("Cette commande ne peut plus être annulée en ligne. Contactez-nous.", "warning")
        return redirect(url_for("suivi_commande_detail", order_id=order.id))
    cart_svc.restore_stock_for_order(order)
    order.set_status(ORDER_STATUS_CANCELLED, note="Annulation client")
    db.session.commit()
    try:
        _notify_order_cancelled(order, by_customer=True)
    except Exception:
        pass
    flash("Commande annulée. Un e-mail de confirmation vous sera envoyé.", "success")
    return redirect(url_for("suivi_commande_detail", order_id=order.id))


@app.route("/api/commande/<int:order_id>/statut")
def api_commande_statut(order_id):
    order = db.session.get(Order, order_id)
    if not _can_access_order(order):
        return jsonify({"error": "forbidden"}), 403
    est = delivery_est_svc.estimate_for_order(order)
    return jsonify(
        {
            "status": order.status,
            "status_label": ORDER_STATUS_LABELS.get(order.status, order.status),
            "step": ORDER_STATUS_STEP.get(order.status, 1),
            "delivery_estimate": est["label"],
        }
    )


@app.route("/commande/<int:order_id>/recommander", methods=["POST"])
def commande_recommander(order_id):
    order = db.session.get(Order, order_id)
    if not _can_access_order(order):
        abort(403)
    added = 0
    for line in order.items:
        if line.product and line.product.is_active:
            ok, _ = cart_svc.add_to_cart(line.product_id, line.quantity)
            if ok:
                added += 1
    if added:
        flash(f"{added} article(s) ajouté(s) au panier.", "success")
    else:
        flash("Impossible de recommander — produits indisponibles.", "warning")
    return redirect(url_for("panier"))


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        subject = (request.form.get("subject") or "").strip()
        message = (request.form.get("message") or "").strip()
        if len(name) < 2 or not email or "@" not in email or len(subject) < 3 or len(message) < 10:
            flash("Veuillez remplir tous les champs du formulaire.", "danger")
        else:
            msg = ContactMessage(name=name, email=email, subject=subject, message=message)
            db.session.add(msg)
            db.session.commit()
            try:
                mailer.notify_contact_message(msg)
            except Exception:
                pass
            flash("Message envoyé — nous vous répondrons rapidement.", "success")
            return redirect(url_for("contact"))
    return render_template("contact.html", faq_items=content_svc.all_faq_items())


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
