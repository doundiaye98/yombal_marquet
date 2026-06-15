# -*- coding: utf-8 -*-
"""Yombal Marché — boutique en ligne, comptes clients, panier et paiement."""

import logging
import os
from datetime import datetime
from functools import wraps

from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user

from extensions import db, login_manager, migrate
import mailer
from database import ensure_database
from models import (
    ORDER_STATUSES,
    ORDER_STATUS_AWAITING_PAYPAL,
    ORDER_STATUS_AWAITING_WIRE,
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
    ORDER_STATUS_STEP,
    ORDER_TRACKING_STEPS,
)
from models.order_tracking import find_order_by_reference_and_email

load_dotenv()

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
app.jinja_env.globals["product_categories"] = PRODUCT_CATEGORIES
app.jinja_env.globals["shop_category_order"] = SHOP_CATEGORY_ORDER
app.jinja_env.globals["order_status_labels"] = ORDER_STATUS_LABELS
app.jinja_env.globals["order_status_hints"] = ORDER_STATUS_HINTS
app.jinja_env.globals["order_status_step"] = ORDER_STATUS_STEP
app.jinja_env.globals["order_tracking_steps"] = ORDER_TRACKING_STEPS

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
    return session.get("cart") or {}


def _cart_items():
    raw = _cart_raw()
    rows = []
    total = 0
    for pid, qty in raw.items():
        try:
            q = max(1, min(99, int(qty)))
        except (TypeError, ValueError):
            continue
        p = db.session.get(Product, int(pid))
        if p and p.is_active:
            rows.append({"product": p, "quantity": q})
            total += p.price_cents * q
    return rows, total


def _cart_count():
    return sum(int(q) for q in _cart_raw().values() if str(q).isdigit())


def _admin_emails_set():
    return {e.strip().lower() for e in os.environ.get("ADMIN_EMAILS", "").split(",") if e.strip()}


def _is_shop_admin():
    if not current_user.is_authenticated:
        return False
    return current_user.email.lower() in _admin_emails_set()


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Connexion requise.", "warning")
            return redirect(url_for("login", next=request.path))
        if not _is_shop_admin():
            abort(403)
        return view(*args, **kwargs)

    return wrapped


def _order_contact(order):
    """Utilisateur enregistré ou coordonnées invité pour les e-mails."""
    if order.user_id:
        return db.session.get(User, order.user_id)
    contact = type("GuestContact", (), {})()
    contact.email = (order.guest_email or "").strip()
    contact.name = (order.guest_name or "").strip() or None
    return contact


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
    contact = _order_contact(order)
    if contact and contact.email:
        mailer.notify_customer_payment_received(order, contact)
        mailer.notify_admin_payment_received(order, contact)
    return "ok"


@app.context_processor
def inject_globals():
    return {
        "current_year": datetime.now().year,
        "service_categories": SERVICE_CATEGORIES,
        "cart_count": _cart_count(),
        "shop_contact_email": (os.environ.get("CONTACT_EMAIL") or "contact@yombal-marche.local").strip(),
        "is_shop_admin": _is_shop_admin(),
        "product_categories": PRODUCT_CATEGORIES,
        "shop_category_order": SHOP_CATEGORY_ORDER,
        "order_status_labels": ORDER_STATUS_LABELS,
        "order_status_hints": ORDER_STATUS_HINTS,
        "order_status_step": ORDER_STATUS_STEP,
        "order_tracking_steps": ORDER_TRACKING_STEPS,
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
    return {
        "delivery_line1": (request.form.get("delivery_line1") or "").strip(),
        "delivery_line2": (request.form.get("delivery_line2") or "").strip() or None,
        "delivery_city": (request.form.get("delivery_city") or "").strip(),
        "delivery_postal_code": (request.form.get("delivery_postal_code") or "").strip(),
        "delivery_country": (request.form.get("delivery_country") or "FR").strip().upper()[:2],
        "customer_notes": (request.form.get("customer_notes") or "").strip() or None,
    }


def _apply_delivery_to_order(order, delivery):
    for key, value in delivery.items():
        setattr(order, key, value)


@app.route("/")
def index():
    featured = _product_query_active().order_by(Product.id).limit(6).all()
    featured_producers = _producer_query_active().order_by(Producer.id).limit(4).all()
    return render_template(
        "index.html",
        featured_products=featured,
        featured_producers=featured_producers,
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
    return render_template("boutique/detail.html", product=product, related=related)


@app.route("/producteurs")
def producteurs():
    producers = _producer_query_active().order_by(Producer.name).all()
    return render_template("producteurs/index.html", producers=producers)


@app.route("/producteur/<slug>")
def producteur_detail(slug):
    producer = _producer_query_active().filter_by(slug=slug).first_or_404()
    products = producer.active_products().all()
    return render_template("producteurs/detail.html", producer=producer, products=products)


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
    qty = max(1, min(20, qty))
    cart = dict(session.get("cart") or {})
    cart[str(pid)] = cart.get(str(pid), 0) + qty
    if cart[str(pid)] > 99:
        cart[str(pid)] = 99
    session["cart"] = cart
    session.modified = True
    flash("Produit ajouté au panier.", "success")
    next_url = request.form.get("next") or request.referrer
    return redirect(next_url or url_for("panier"))


@app.route("/panier")
def panier():
    items, total = _cart_items()
    return render_template("panier.html", items=items, total_cents=total)


@app.route("/panier/modifier", methods=["POST"])
def panier_modifier():
    pid = str(request.form.get("product_id", ""))
    qty = request.form.get("quantity", type=int)
    cart = dict(session.get("cart") or {})
    if pid not in cart:
        return redirect(url_for("panier"))
    if qty is None or qty < 1:
        cart.pop(pid, None)
    else:
        cart[pid] = max(1, min(99, qty))
    session["cart"] = cart
    session.modified = True
    return redirect(url_for("panier"))


@app.route("/auth/inscription", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("boutique"))
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        name = (request.form.get("name") or "").strip()
        if not email or "@" not in email:
            flash("Adresse e-mail invalide.", "danger")
        elif len(password) < 6:
            flash("Mot de passe : au moins 6 caractères.", "danger")
        elif User.query.filter_by(email=email).first():
            flash("Un compte existe déjà avec cet e-mail.", "danger")
        else:
            u = User(email=email, name=name or None)
            u.set_password(password)
            db.session.add(u)
            db.session.commit()
            login_user(u)
            flash("Compte créé. Vous pouvez finaliser votre commande.", "success")
            return redirect(url_for("boutique"))
    return render_template("auth/register.html")


@app.route("/auth/connexion", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("boutique"))
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        u = User.query.filter_by(email=email).first()
        if u and u.check_password(password):
            login_user(u, remember=bool(request.form.get("remember")))
            flash("Bon retour parmi nous.", "success")
            nxt = request.form.get("next") or request.args.get("next") or ""
            if nxt.startswith("/") and not nxt.startswith("//"):
                return redirect(nxt)
            return redirect(url_for("boutique"))
        flash("E-mail ou mot de passe incorrect.", "danger")
    return render_template("auth/login.html")


@app.route("/auth/deconnexion")
@login_required
def logout():
    logout_user()
    flash("Vous êtes déconnecté.", "info")
    return redirect(url_for("index"))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    items, total = _cart_items()
    if not items:
        flash("Votre panier est vide.", "warning")
        return redirect(url_for("boutique"))
    if request.method == "POST":
        delivery = _delivery_from_form()
        if len(delivery["delivery_line1"]) < 5:
            flash("Indiquez une adresse de livraison complète.", "danger")
            return render_template("checkout.html", items=items, total_cents=total, guest_form=request.form)
        if len(delivery["delivery_city"]) < 2 or len(delivery["delivery_postal_code"]) < 4:
            flash("Indiquez la ville et le code postal.", "danger")
            return render_template("checkout.html", items=items, total_cents=total, guest_form=request.form)

        if current_user.is_authenticated:
            order = Order(
                user_id=current_user.id,
                subtotal_cents=total,
                shipping_cents=0,
                total_cents=total,
                status=ORDER_STATUS_PENDING,
            )
            _apply_delivery_to_order(order, delivery)
        else:
            email = (request.form.get("guest_email") or "").strip().lower()
            name = (request.form.get("guest_name") or "").strip()
            phone = (request.form.get("guest_phone") or "").strip()
            if not email or "@" not in email:
                flash("Indiquez une adresse e-mail valide pour la commande.", "danger")
                return render_template("checkout.html", items=items, total_cents=total, guest_form=request.form)
            if len(name) < 2:
                flash("Indiquez votre nom pour la livraison.", "danger")
                return render_template("checkout.html", items=items, total_cents=total, guest_form=request.form)
            if len(phone) < 6:
                flash("Indiquez un numéro de téléphone pour la livraison.", "danger")
                return render_template("checkout.html", items=items, total_cents=total, guest_form=request.form)
            order = Order(
                user_id=None,
                guest_email=email,
                guest_name=name,
                guest_phone=phone,
                subtotal_cents=total,
                shipping_cents=0,
                total_cents=total,
                status=ORDER_STATUS_PENDING,
            )
            _apply_delivery_to_order(order, delivery)

        order.status_events.append(
            OrderStatusEvent(to_status=ORDER_STATUS_PENDING, note="Commande créée")
        )
        db.session.add(order)
        db.session.flush()
        for row in items:
            db.session.add(OrderItem.from_product(row["product"], row["quantity"], order.id))
        db.session.commit()
        if not order.user_id:
            _remember_guest_order(order.id)
        session["cart"] = {}
        session.modified = True
        contact = _order_contact(order)
        if contact and contact.email:
            try:
                mailer.notify_customer_order_created(order, contact)
                mailer.notify_admin_new_order(order, contact)
            except Exception:
                pass
        return redirect(url_for("paiement", order_id=order.id))
    return render_template("checkout.html", items=items, total_cents=total, guest_form=None)


@app.route("/paiement/<int:order_id>")
def paiement(order_id):
    order = db.session.get(Order, order_id)
    if not _can_access_order(order):
        if not current_user.is_authenticated:
            flash("Connectez-vous ou finalisez une commande invité depuis ce navigateur.", "warning")
            return redirect(url_for("login", next=request.path))
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
        contact = _order_contact(order)
        if contact and contact.email:
            try:
                mailer.notify_customer_payment_received(order, contact)
                mailer.notify_admin_payment_received(order, contact)
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
    contact = _order_contact(order)
    if contact and contact.email:
        try:
            mailer.notify_customer_payment_received(order, contact)
            mailer.notify_admin_payment_received(order, contact)
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
                contact = _order_contact(order)
                if contact and contact.email:
                    try:
                        mailer.notify_customer_payment_received(order, contact)
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
    return render_template("apropos.html")


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
    return redirect(url_for("suivi_commande_detail", order_id=order_id))


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
    return render_template("commandes/suivi.html", recent_orders=recent_orders)


@app.route("/suivi-commande/<int:order_id>")
def suivi_commande_detail(order_id):
    order = db.session.get(Order, order_id)
    if not _can_access_order(order):
        flash("Accès refusé. Utilisez le formulaire de suivi avec votre e-mail de commande.", "warning")
        return redirect(url_for("suivi_commande"))
    events = order.status_events.order_by(OrderStatusEvent.created_at.desc()).all()
    current_step = ORDER_STATUS_STEP.get(order.status, 1)
    return render_template(
        "commandes/detail.html",
        order=order,
        events=events,
        current_step=current_step,
    )


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
