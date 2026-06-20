# -*- coding: utf-8 -*-
"""Importe FAQ, recettes, coffrets, zones livraison et réglages site depuis les données statiques."""

from extensions import db
from models.coffret_model import Coffret, CoffretLine
from models.coffrets import COFFRETS
from models.delivery_zone import DeliveryZone
from models.faq import FAQ_ITEMS
from models.faq_item import FaqItem
from models.product import Product
from models.producer import Producer
from models.recipe_model import Recipe, RecipeLine
from models.recipes import RECIPES
from models.site_setting import SiteSetting
from models.promo_code import PromoCode

MAP_COORDS = {
    "aminata-diallo": (260, 330, "Casamance"),
    "fatou-ndiaye": (420, 300, "Thiès"),
    "moussa-kone": (480, 345, "Burkina Faso"),
    "cooperative-tafraout": (420, 165, "Maroc"),
    "atelier-sahel": (390, 205, "Savon noir"),
    "famille-bencherif": (360, 210, "Algérie"),
    "oasis-jericho": (650, 235, "Vallée du Jourdain"),
    "rucher-alpilles": (160, 150, "Alpilles"),
}

DEFAULT_SETTINGS = {
    "shop_name": "Yombal Marché",
    "shop_contact_email": "compta@universdiasporas.com",
    "shop_address_line1": "Place du marché",
    "shop_address_line2": "Code postal · Ville",
    "shop_hours_weekday": "Lun – ven · 8h30 – 13h30 · 15h30 – 19h30",
    "shop_hours_saturday": "Samedi · 8h – 19h30",
    "shop_hours_sunday": "Dimanche · 9h – 13h",
    "shop_delivery_days_min": "3",
    "shop_delivery_days_max": "7",
}


def seed_content_if_empty():
    _seed_settings()
    _seed_delivery_zones()
    _seed_faq()
    _seed_recipes()
    _seed_coffrets()
    _seed_producer_map()
    _seed_demo_promo()
    db.session.commit()


def _seed_settings():
    for key, value in DEFAULT_SETTINGS.items():
        existing = db.session.get(SiteSetting, key)
        if not existing:
            db.session.add(SiteSetting(key=key, value=value))
        elif key == "shop_contact_email" and existing.value in ("", "contact@yombal-marche.local", "contact@exemple.com"):
            existing.value = value


def _seed_delivery_zones():
    if DeliveryZone.query.count():
        return
    zones = [
        ("France — défaut", "", 590, 5000, 0),
        ("Paris & petite couronne", "75", 390, 5000, 1),
        ("Petite couronne", "92", 490, 5000, 2),
        ("Petite couronne", "93", 490, 5000, 3),
        ("Petite couronne", "94", 490, 5000, 4),
    ]
    for name, prefix, price, free_over, order in zones:
        db.session.add(
            DeliveryZone(
                name=name,
                postal_prefix=prefix,
                price_cents=price,
                free_over_cents=free_over,
                sort_order=order,
            )
        )


def _seed_faq():
    if FaqItem.query.count():
        return
    for i, item in enumerate(FAQ_ITEMS):
        db.session.add(
            FaqItem(question=item["q"], answer=item["a"], sort_order=i, is_active=True)
        )


def _seed_recipes():
    if Recipe.query.count():
        return
    for i, r in enumerate(RECIPES):
        recipe = Recipe(
            slug=r["slug"],
            title=r["title"],
            emoji=r.get("emoji", "🍲"),
            kind=r.get("kind", "plat"),
            kind_label=r.get("kind_label"),
            time_minutes=r.get("time_minutes"),
            servings=r.get("servings"),
            summary=r.get("summary"),
            sort_order=i,
            is_active=True,
        )
        recipe.steps = r.get("steps", [])
        db.session.add(recipe)
        db.session.flush()
        for j, ing in enumerate(r.get("ingredients", [])):
            product = Product.query.filter_by(slug=ing["product_slug"]).first()
            if product:
                db.session.add(
                    RecipeLine(
                        recipe_id=recipe.id,
                        product_id=product.id,
                        quantity=max(1, int(ing.get("quantity", 1))),
                        note=ing.get("note"),
                        sort_order=j,
                    )
                )


def _seed_coffrets():
    if Coffret.query.count():
        return
    for i, c in enumerate(COFFRETS):
        coffret = Coffret(
            slug=c["slug"],
            title=c["title"],
            emoji=c.get("emoji", "🎁"),
            theme=c.get("theme", "diaspora"),
            theme_label=c.get("theme_label"),
            summary=c.get("summary"),
            gift_message=c.get("gift_message"),
            sort_order=i,
            is_active=True,
        )
        db.session.add(coffret)
        db.session.flush()
        for j, ing in enumerate(c.get("ingredients", [])):
            product = Product.query.filter_by(slug=ing["product_slug"]).first()
            if product:
                db.session.add(
                    CoffretLine(
                        coffret_id=coffret.id,
                        product_id=product.id,
                        quantity=max(1, int(ing.get("quantity", 1))),
                        sort_order=j,
                    )
                )


def _seed_producer_map():
    for slug, (x, y, label) in MAP_COORDS.items():
        producer = Producer.query.filter_by(slug=slug).first()
        if producer and producer.map_x is None:
            producer.map_x = x
            producer.map_y = y
            producer.map_label = label


def _seed_demo_promo():
    if PromoCode.query.filter_by(code="BIENVENUE10").first():
        return
    db.session.add(
        PromoCode(
            code="BIENVENUE10",
            discount_percent=10,
            min_order_cents=2000,
            max_uses=1000,
            is_active=True,
        )
    )
