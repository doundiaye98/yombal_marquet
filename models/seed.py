# -*- coding: utf-8 -*-
from extensions import db
from models.catalogue_extended import EXTENDED_CATALOGUE
from models.catalogue_labelafrik import (
    LABELAFRIK_CATALOGUE,
    LABELAFRIK_SLUGS,
    LABELAFRIK_UPDATES,
)
from models.product import Product
from models.catalogue_retired import RETIRED_PRODUCT_SLUGS
from models.product_names import apply_display_name, display_name_for_product
from models.product_images import CATALOGUE_SLUGS, PRODUCT_IMAGES

CATALOGUE = [
    {
        "sku": "ALIM-COUSCOUS-1KG",
        "slug": "couscous-complet-1kg",
        "name": "Couscous complet — 1 kg",
        "summary": "Semoule complète, texture légère, idéale pour tajines et salades.",
        "description": (
            "Notre couscous complet est préparé à partir de blé dur soigneusement sélectionné, "
            "avec enveloppe du grain conservée pour plus de fibres et de goût.\n\n"
            "Il se réhydrate en quelques minutes à la vapeur ou au micro-ondes selon vos habitudes. "
            "Convient aux plats en sauce, aux légumes grillés et aux poissons.\n\n"
            "Conditionné sous atmosphère protectrice pour garder fraîcheur et arôme jusqu’à chez vous."
        ),
        "price_cents": 389,
        "category": "alimentaire",
        "origin": "Origine UE / Afrique du Nord (lot indiqué sur emballage)",
        "weight_info": "1 kg — pochette refermable",
        "ingredients": "Semoule de BLÉ dur complet (gluten). Peut contenir des traces de SESAME.",
        "allergens": "Gluten.",
        "usage_tips": "Pour 4 personnes : environ 250 g de couscous sec pour 300 ml d’eau bouillante salée, "
        "laisser gonfler hors du feu couvert 5 min, aerer à la fourchette.",
        "conservation": "À conserver à l’abri de la chaleur et de l’humidité. Après ouverture, refermer hermétiquement.",
    },
    {
        "sku": "COSM-ARGAN-100ML",
        "slug": "huile-argan-bio-100ml",
        "name": "Huile d'argan bio — 100 ml",
        "summary": "Pure, vierge pressée à froid — visage, corps et pointes.",
        "description": (
            "Huile d’argan du Maroc, certifiée biologique, obtenue par première pression à froid. "
            "Riche en vitamine E et en acides gras insaturés.\n\n"
            "Texture sèche, parfum léger de noisette : elle pénètre sans film gras. "
            "Appliquer quelques gouttes sur une peau légèrement humide pour un effet seconde peau.\n\n"
            "Flacon verre ambré avec compte-gouttes pour doser précisément."
        ),
        "price_cents": 2490,
        "category": "cosmetique",
        "origin": "Coopérative — Sud Maroc",
        "weight_info": "100 ml",
        "ingredients": "100 % huile d’Argania spinosa kernel oil.",
        "allergens": "",
        "usage_tips": "Visage : 2–3 gouttes le soir après nettoyage. Cheveux : bain d’huile 20 min avant shampoing sur longueurs.",
        "conservation": "À l’abri de la lumière, à température ambiante.",
    },
    {
        "sku": "ALIM-MIEL-500G",
        "slug": "miel-thym-500g",
        "name": "Miel d'acacia — 500 g",
        "summary": "Goût corsé, notes boisées — idéal au yaourt et dans les tisanes.",
        "description": (
            "Miellée de thym récoltée sur plateaux méditerranéens. Miel non chauffé pour préserver enzymes et arômes.\n\n"
            "Couleur ambrée, cristallisation naturelle possible avec le temps : placer le pot au bain-marie tiède "
            "pour retrouver une texture fluide sans altérer la qualité.\n\n"
            "Chaque pot porte un numéro de lot traçable."
        ),
        "price_cents": 895,
        "category": "alimentaire",
        "origin": "France / Espagne selon récolte",
        "weight_info": "500 g — pot verre",
        "ingredients": "100 % miel.",
        "allergens": "Peut ne pas convenir aux personnes allergiques aux pollens.",
        "usage_tips": "Une cuillère à café dans une tisane tiède ou sur un fromage frais.",
        "conservation": "Au sec, à température ambiante.",
    },
    {
        "sku": "ALIM-CAFE-250G",
        "slug": "cafe-arabica-250g",
        "name": "Café — 250 g",
        "summary": "Torréfaction moyenne, notes chocolat et fruits rouges.",
        "description": (
            "Grain torréfié par petits lots pour révéler acidité équilibrée et corps velouté.\n\n"
            "Mouture universelle adaptée à cafetière à piston, verseuse ou machine avec filtre papier. "
            "Pour espresso, préférer la version grains (demandez-nous la disponibilité).\n\n"
            "Date de torréfaction imprimée sur le sachet."
        ),
        "price_cents": 799,
        "category": "alimentaire",
        "origin": "Amérique centrale & Afrique — assemblage maison",
        "weight_info": "250 g — sachet avec valve",
        "ingredients": "Café 100 %.",
        "allergens": "",
        "usage_tips": "Ratio indicatif : 60 g pour 1 litre d’eau en cafetière à piston.",
        "conservation": "Refermer après ouverture ; consommer sous 3 semaines pour un arôme optimal.",
    },
    {
        "sku": "COSM-SAVON-200G",
        "slug": "savon-noir-eucalyptus",
        "name": "Savon noir eucalyptus — 200 g",
        "summary": "Pâte noire adoucissante pour le hammam et le soin du corps.",
        "description": (
            "Savon noir à base d’huile d’olive noircie au potasse végétale, enrichi en huile essentielle d’eucalyptus.\n\n"
            "Appliquer sur peau humide en massage circulaire avant de rincer abondamment. "
            "Effet gommage doux si utilisé avec un gant kessa.\n\n"
            "Évitez le contour des yeux."
        ),
        "price_cents": 690,
        "category": "cosmetique",
        "origin": "Fabrication Provence / Maghreb selon lot",
        "weight_info": "200 g — pot PEHD",
        "ingredients": "Huile d’olive, eau, potasse, glycérine végétale, huile essentielle d’eucalyptus globulus.",
        "allergens": "",
        "usage_tips": "Une noix suffit pour tout le corps. Compléter avec huile d’argan après la douche.",
        "conservation": "Bien refermer ; garder au sec.",
    },
    {
        "sku": "COSM-KARITE-150G",
        "slug": "beurre-karite-brut-150g",
        "name": "Beurre de karité — 150 g",
        "summary": "Non raffiné : odeur noisette naturelle, baume universel.",
        "description": (
            "Beurre de karité extrait à l’ancienne, non déodoré. Couleur ivoire à beige selon la récolte.\n\n"
            "Fond entre les mains puis application sur zones très sèches (coudes, talons, lèvres). "
            "Peut servir de base DIY baumes (avec huiles essentielles dosées par un aromathérapeute).\n\n"
            "Texture qui durcit par temps froid : réchauffer un peu au bain-marie."
        ),
        "price_cents": 1190,
        "category": "cosmetique",
        "origin": "Ghana / Burkina Faso — commerce équitable partenaire",
        "weight_info": "150 g — boîte métal ou pot selon arrivage",
        "ingredients": "Butyrospermum parkii (shea) butter.",
        "allergens": "",
        "usage_tips": "Le soir en couche épaisse sur les mains avec des gants coton.",
        "conservation": "Température stable ; éviter les variations extrêmes.",
    },
]


FULL_CATALOGUE = [
    apply_display_name(row)
    for row in (CATALOGUE + EXTENDED_CATALOGUE)
    if row["slug"] in CATALOGUE_SLUGS and row["slug"] not in RETIRED_PRODUCT_SLUGS
] + [apply_display_name(row) for row in LABELAFRIK_CATALOGUE]


def _sync_row_to_product(product, row):
    """Applique nom, prix, textes depuis une ligne catalogue."""
    changed = False
    for field in (
        "name",
        "summary",
        "description",
        "price_cents",
        "weight_info",
        "category",
        "origin",
        "ingredients",
        "usage_tips",
        "conservation",
    ):
        if field in row and row[field] is not None and getattr(product, field) != row[field]:
            setattr(product, field, row[field])
            changed = True
    if row.get("icon") and not product.icon:
        product.icon = row["icon"]
        changed = True
    return changed


def _product_payload(row):
    data = apply_display_name(dict(row))
    img = PRODUCT_IMAGES.get(data["slug"])
    if img:
        data["image"] = img
    return data


def seed_products_if_empty():
    """Charge le catalogue vitrine une seule fois."""
    from sqlalchemy import inspect, text

    if not inspect(db.engine).has_table("products"):
        return
    try:
        count = db.session.execute(text("SELECT COUNT(*) FROM products")).scalar() or 0
    except Exception:
        return
    if count > 0:
        return
    for row in FULL_CATALOGUE:
        db.session.add(Product(**_product_payload(row)))
    db.session.commit()


def sync_catalogue():
    """Ajoute ou met à jour le catalogue (dont LabelAfrik / Univers Diaspora)."""
    from sqlalchemy import inspect

    from services.product_admin import admin_removed_slugs

    if not inspect(db.engine).has_table("products"):
        return
    removed = admin_removed_slugs()
    changed = False
    for row in FULL_CATALOGUE:
        slug = row["slug"]
        if slug in removed:
            continue
        product = Product.query.filter_by(slug=slug).first()
        if product:
            if _sync_row_to_product(product, row):
                changed = True
            continue
        db.session.add(Product(**_product_payload(row)))
        changed = True
    for slug, row in LABELAFRIK_UPDATES.items():
        if slug in RETIRED_PRODUCT_SLUGS or slug in removed:
            continue
        product = Product.query.filter_by(slug=slug).first()
        if product and _sync_row_to_product(product, apply_display_name(row)):
            changed = True
    names_changed = sync_all_product_names()
    if changed or names_changed:
        db.session.commit()


def sync_all_product_names():
    """Harmonise les noms affichés pour tous les produits."""
    from sqlalchemy import inspect

    if not inspect(db.engine).has_table("products"):
        return False
    changed = False
    for product in Product.query.all():
        new_name = display_name_for_product(product.slug, product.weight_info, product.name)
        if new_name and product.name != new_name:
            product.name = new_name
            changed = True
    return changed


def retire_superseded_products():
    """Supprime ou désactive les anciens produits remplacés par LabelAfrik."""
    from sqlalchemy import inspect

    from models.order import OrderItem

    if not inspect(db.engine).has_table("products"):
        return
    changed = False
    for slug in RETIRED_PRODUCT_SLUGS:
        product = Product.query.filter_by(slug=slug).first()
        if not product:
            continue
        has_orders = OrderItem.query.filter_by(product_id=product.id).first() is not None
        if has_orders:
            if product.is_active:
                product.is_active = False
                changed = True
        else:
            db.session.delete(product)
            changed = True
    if changed:
        db.session.commit()
