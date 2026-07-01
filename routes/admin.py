# -*- coding: utf-8 -*-
"""Routes administration boutique."""

from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from extensions import db
from models.coffret_model import Coffret, CoffretLine
from models.contact_message import ContactMessage
from models.constants import PRODUCT_CATEGORIES, SHOP_CATEGORY_ORDER
from models.delivery_zone import DeliveryZone
from models.faq_item import FaqItem
from models.producer import Producer
from models.product import Product
from models.product_image import ProductImage
from models.promo_code import PromoCode
from models.recipe_model import Recipe, RecipeLine
from models.site_setting import SiteSetting, set_setting
from models.order import Order
from models.user import User
from shop_auth import admin_emails_set, admin_required, is_shop_admin
from services.product_admin import delete_product
from services.image_storage import remove_product_image, save_product_image

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/connexion", methods=["GET", "POST"])
def admin_login():
    if current_user.is_authenticated and is_shop_admin():
        return redirect(url_for("admin.admin_dashboard"))
    admins = admin_emails_set()
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = (request.form.get("password") or "").strip()
        user = User.query.filter_by(email=email).first()
        if email not in admins:
            if user and user.check_password(password):
                flash(
                    f"Compte valide, mais {email} n’est pas dans ADMIN_EMAILS. "
                    f"Autorisés : {', '.join(sorted(admins))}",
                    "danger",
                )
            else:
                flash(
                    f"E-mail non autorisé. Comptes admin : {', '.join(sorted(admins))}",
                    "danger",
                )
        elif not user:
            flash(
                f"Aucun compte pour {email}. Lancez : "
                f"python scripts/create_admin.py {email} VotreMotDePasse",
                "danger",
            )
        elif user.check_password(password):
            login_user(user)
            return redirect(url_for("admin.admin_dashboard"))
        else:
            flash("Mot de passe incorrect. Réinitialisez avec scripts/create_admin.py", "danger")
    return render_template("admin/login.html", allowed_admins=sorted(admins))


@admin_bp.route("/deconnexion")
def admin_logout():
    logout_user()
    flash("Session administrateur fermée.", "info")
    return redirect(url_for("admin.admin_login"))


@admin_bp.route("/")
@admin_required
def admin_dashboard():
    stats = {
        "orders": Order.query.count(),
        "products": Product.query.filter_by(is_active=True).count(),
        "messages_unread": ContactMessage.query.filter_by(is_read=False).count(),
    }
    return render_template("admin/dashboard.html", stats=stats)


@admin_bp.route("/produits")
@admin_required
def admin_products():
    products = Product.query.order_by(Product.category, Product.name).all()
    return render_template("admin/products.html", products=products)


@admin_bp.route("/produit/<int:product_id>", methods=["GET", "POST"])
@admin_bp.route("/produit/nouveau", methods=["GET", "POST"], defaults={"product_id": None})
@admin_required
def admin_product_edit(product_id):
    product = db.session.get(Product, product_id) if product_id else Product(is_active=True, price_cents=0, category="alimentaire", description="")
    producers = Producer.query.filter_by(is_active=True).order_by(Producer.name).all()
    if request.method == "POST":
        product.slug = (request.form.get("slug") or "").strip()
        product.name = (request.form.get("name") or "").strip()
        product.summary = (request.form.get("summary") or "").strip() or None
        product.description = (request.form.get("description") or "").strip()
        product.category = (request.form.get("category") or "alimentaire").strip()
        product.origin = (request.form.get("origin") or "").strip() or None
        product.price_cents = max(0, int(float(request.form.get("price_euros") or 0) * 100))
        stock_raw = request.form.get("stock_qty")
        if stock_raw in (None, ""):
            product.stock_qty = None
        else:
            product.stock_qty = max(0, int(stock_raw))
        product.icon = (request.form.get("icon") or "🛒")[:8]
        product.is_active = request.form.get("is_active") == "1"
        pid = request.form.get("producer_id", type=int)
        product.producer_id = pid or None
        if not product.slug or not product.name or not product.description:
            flash("Slug, nom et description obligatoires.", "danger")
        else:
            if not product_id:
                db.session.add(product)
                db.session.flush()

            static_folder = current_app.static_folder
            remove_image = request.form.get("remove_image") == "1"
            upload = request.files.get("image")

            if remove_image and product.image:
                remove_product_image(product.image, static_folder)
                product.image = None

            if upload and upload.filename:
                old_path = product.image
                rel_path, err = save_product_image(upload, product.slug, static_folder)
                if err:
                    flash(err, "danger")
                else:
                    if old_path and old_path != rel_path:
                        remove_product_image(old_path, static_folder)
                    product.image = rel_path

            remove_gallery = request.form.getlist("remove_gallery")
            for gid in remove_gallery:
                try:
                    gid_int = int(gid)
                except (TypeError, ValueError):
                    continue
                row = db.session.get(ProductImage, gid_int)
                if row and row.product_id == product.id:
                    remove_product_image(row.image, static_folder)
                    db.session.delete(row)

            gallery_uploads = request.files.getlist("gallery_uploads")
            existing = ProductImage.query.filter_by(product_id=product.id).count()
            sort_base = existing + 1
            added = 0
            for upload in gallery_uploads:
                if not upload or not upload.filename:
                    continue
                suffix = f"-g{sort_base + added}"
                rel_path, err = save_product_image(
                    upload, product.slug, static_folder, filename_suffix=suffix
                )
                if err:
                    flash(err, "warning")
                    continue
                db.session.add(
                    ProductImage(
                        product_id=product.id,
                        image=rel_path,
                        sort_order=sort_base + added,
                    )
                )
                added += 1

            db.session.commit()
            flash("Produit enregistré.", "success")
            return redirect(url_for("admin.admin_products"))
    return render_template(
        "admin/product_form.html",
        product=product,
        producers=producers,
        categories=PRODUCT_CATEGORIES,
        is_new=not product_id,
    )


@admin_bp.route("/produit/<int:product_id>/supprimer", methods=["POST"])
@admin_required
def admin_product_delete(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        abort(404)
    level, message = delete_product(product, current_app.static_folder)
    db.session.commit()
    flash(message, level)
    return redirect(url_for("admin.admin_products"))


@admin_bp.route("/producteurs")
@admin_required
def admin_producers():
    producers = Producer.query.order_by(Producer.name).all()
    return render_template("admin/producers.html", producers=producers)


@admin_bp.route("/producteur/<int:producer_id>", methods=["GET", "POST"])
@admin_required
def admin_producer_edit(producer_id):
    producer = db.session.get(Producer, producer_id)
    if not producer:
        abort(404)
    if request.method == "POST":
        producer.name = (request.form.get("name") or "").strip()
        producer.region = (request.form.get("region") or "").strip()
        producer.flagship_product = (request.form.get("flagship_product") or "").strip()
        producer.story = (request.form.get("story") or "").strip()
        producer.avatar_emoji = (request.form.get("avatar_emoji") or "👤")[:8]
        producer.audio_url = (request.form.get("audio_url") or "").strip() or None
        producer.map_x = request.form.get("map_x", type=int)
        producer.map_y = request.form.get("map_y", type=int)
        producer.map_label = (request.form.get("map_label") or "").strip() or None
        producer.is_active = request.form.get("is_active") == "1"
        db.session.commit()
        flash("Producteur mis à jour.", "success")
        return redirect(url_for("admin.admin_producers"))
    return render_template("admin/producer_form.html", producer=producer)


@admin_bp.route("/recettes")
@admin_required
def admin_recipes():
    recipes = Recipe.query.order_by(Recipe.sort_order, Recipe.title).all()
    return render_template("admin/recipes.html", recipes=recipes)


@admin_bp.route("/coffrets")
@admin_required
def admin_coffrets():
    coffrets = Coffret.query.order_by(Coffret.sort_order, Coffret.title).all()
    return render_template("admin/coffrets.html", coffrets=coffrets)


@admin_bp.route("/faq")
@admin_required
def admin_faq():
    items = FaqItem.query.order_by(FaqItem.sort_order, FaqItem.id).all()
    return render_template("admin/faq.html", items=items)


@admin_bp.route("/faq/<int:item_id>", methods=["GET", "POST"])
@admin_bp.route("/faq/nouveau", methods=["GET", "POST"], defaults={"item_id": None})
@admin_required
def admin_faq_edit(item_id):
    item = db.session.get(FaqItem, item_id) if item_id else FaqItem(is_active=True, sort_order=0)
    if request.method == "POST":
        item.question = (request.form.get("question") or "").strip()
        item.answer = (request.form.get("answer") or "").strip()
        item.sort_order = request.form.get("sort_order", type=int) or 0
        item.is_active = request.form.get("is_active") == "1"
        if not item.question or not item.answer:
            flash("Question et réponse obligatoires.", "danger")
        else:
            if not item_id:
                db.session.add(item)
            db.session.commit()
            flash("FAQ enregistrée.", "success")
            return redirect(url_for("admin.admin_faq"))
    return render_template("admin/faq_form.html", item=item, is_new=not item_id)


@admin_bp.route("/zones-livraison")
@admin_required
def admin_zones():
    zones = DeliveryZone.query.order_by(DeliveryZone.sort_order).all()
    return render_template("admin/zones.html", zones=zones)


@admin_bp.route("/zone/<int:zone_id>", methods=["GET", "POST"])
@admin_bp.route("/zone/nouvelle", methods=["GET", "POST"], defaults={"zone_id": None})
@admin_required
def admin_zone_edit(zone_id):
    zone = db.session.get(DeliveryZone, zone_id) if zone_id else DeliveryZone(is_active=True, price_cents=590)
    if request.method == "POST":
        zone.name = (request.form.get("name") or "").strip()
        zone.postal_prefix = (request.form.get("postal_prefix") or "").strip()
        zone.price_cents = max(0, int(float(request.form.get("price_euros") or 0) * 100))
        free = request.form.get("free_over_euros")
        zone.free_over_cents = int(float(free) * 100) if free else None
        zone.sort_order = request.form.get("sort_order", type=int) or 0
        zone.is_active = request.form.get("is_active") == "1"
        if not zone.name:
            flash("Nom obligatoire.", "danger")
        else:
            if not zone_id:
                db.session.add(zone)
            db.session.commit()
            flash("Zone enregistrée.", "success")
            return redirect(url_for("admin.admin_zones"))
    return render_template("admin/zone_form.html", zone=zone, is_new=not zone_id)


@admin_bp.route("/promos")
@admin_required
def admin_promos():
    promos = PromoCode.query.order_by(PromoCode.code).all()
    return render_template("admin/promos.html", promos=promos)


@admin_bp.route("/promo/<int:promo_id>", methods=["GET", "POST"])
@admin_bp.route("/promo/nouvelle", methods=["GET", "POST"], defaults={"promo_id": None})
@admin_required
def admin_promo_edit(promo_id):
    promo = db.session.get(PromoCode, promo_id) if promo_id else PromoCode(is_active=True, min_order_cents=0)
    if request.method == "POST":
        promo.code = (request.form.get("code") or "").strip().upper()
        promo.discount_percent = request.form.get("discount_percent", type=int)
        dc = request.form.get("discount_euros")
        promo.discount_cents = int(float(dc) * 100) if dc else None
        promo.min_order_cents = max(0, int(float(request.form.get("min_order_euros") or 0) * 100))
        promo.max_uses = request.form.get("max_uses", type=int)
        promo.is_active = request.form.get("is_active") == "1"
        if not promo.code:
            flash("Code obligatoire.", "danger")
        else:
            if not promo_id:
                db.session.add(promo)
            db.session.commit()
            flash("Code promo enregistré.", "success")
            return redirect(url_for("admin.admin_promos"))
    return render_template("admin/promo_form.html", promo=promo, is_new=not promo_id)


@admin_bp.route("/parametres", methods=["GET", "POST"])
@admin_required
def admin_settings():
    keys = [
        "shop_name",
        "shop_contact_email",
        "shop_address_line1",
        "shop_address_line2",
        "shop_hours_weekday",
        "shop_hours_saturday",
        "shop_hours_sunday",
        "shop_phone",
        "shop_delivery_days_min",
        "shop_delivery_days_max",
    ]
    if request.method == "POST":
        for key in keys:
            set_setting(key, request.form.get(key, ""))
        flash("Paramètres enregistrés.", "success")
        return redirect(url_for("admin.admin_settings"))
    from services.settings import shop_settings

    return render_template("admin/settings.html", settings=shop_settings(), keys=keys)


@admin_bp.route("/messages")
@admin_required
def admin_messages():
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(200).all()
    return render_template("admin/messages.html", messages=messages)


@admin_bp.route("/message/<int:msg_id>", methods=["POST"])
@admin_required
def admin_message_read(msg_id):
    msg = db.session.get(ContactMessage, msg_id)
    if msg:
        msg.is_read = True
        db.session.commit()
    return redirect(url_for("admin.admin_messages"))
