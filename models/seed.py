# -*- coding: utf-8 -*-
from extensions import db
from models.catalogue_extended import EXTENDED_CATALOGUE
from models.product import Product
from models.product_images import CATALOGUE_SLUGS, PRODUCT_IMAGES

CATALOGUE = [
    {
        "sku": "ALIM-COUSCOUS-1KG",
        "slug": "couscous-complet-1kg",
        "name": "Couscous complet précuit — 1 kg",
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
        "name": "Huile d’argan bio cosmétique — 100 ml",
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
        "name": "Miel de thym cru — 500 g",
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
        "name": "Café Arabica moulu — 250 g",
        "summary": "Torréfaction moyenne, notes chocolat et fruits rouges.",
        "description": (
            "Grain Arabica en altitude, torréfié par petits lots pour révéler acidité équilibrée et corps velouté.\n\n"
            "Mouture universelle adaptée à cafetière à piston, verseuse ou machine avec filtre papier. "
            "Pour espresso, préférer la version grains (demandez-nous la disponibilité).\n\n"
            "Date de torréfaction imprimée sur le sachet."
        ),
        "price_cents": 799,
        "category": "alimentaire",
        "origin": "Amérique centrale & Afrique — assemblage maison",
        "weight_info": "250 g — sachet avec valve",
        "ingredients": "Café 100 % Arabica.",
        "allergens": "",
        "usage_tips": "Ratio indicatif : 60 g pour 1 litre d’eau en cafetière à piston.",
        "conservation": "Refermer après ouverture ; consommer sous 3 semaines pour un arôme optimal.",
    },
    {
        "sku": "COSM-SAVON-200G",
        "slug": "savon-noir-eucalyptus",
        "name": "Savon noir traditionnel — eucalyptus — 200 g",
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
        "sku": "ALIM-DATES-400G",
        "slug": "dates-medjool-400g",
        "name": "Dates Medjool dénoyautées — 400 g",
        "summary": "Chair fondante, très peu sucrantes ajoutées — collation ou pâtisserie.",
        "description": (
            "Calibre premium, dénoyautées à la main. Texture caramel naturel.\n\n"
            "Parfaites pour smoothies, barres énergétiques maison, ou farçage de volailles sucré-salé.\n\n"
            "Contrôle qualité : fruits souples, non cristallisés."
        ),
        "price_cents": 649,
        "category": "alimentaire",
        "origin": "Jordanie / Israël selon saison",
        "weight_info": "400 g — barquette",
        "ingredients": "Dates.",
        "allergens": "Peut contenir des traces de FRUITS À COQUE.",
        "usage_tips": "Réhydrater 10 min dans du lait végétal pour un dessert express.",
        "conservation": "Au réfrigérateur après ouverture pour ralentir la cristallisation du sucre.",
    },
    {
        "sku": "ALIM-BISSAP-50CL",
        "slug": "bissap-concentre-50cl",
        "name": "Sirop de bissap (hibiscus) — 50 cl",
        "summary": "À diluer : une dosage floral acidulé, sans colorant artificiel.",
        "description": (
            "Réduction de fleurs d’hibiscus infusées avec sucre de canne équitable et une pointe de menthe verte.\n\n"
            "Diluer 1 volume de sirop pour 7 à 10 volumes d’eau gazeuse ou plate selon l’intensité désirée. "
            "Excellent en cocktail sans alcool avec citron vert.\n\n"
            "Stérilisé à chaud — conservation longue avant ouverture."
        ),
        "price_cents": 590,
        "category": "alimentaire",
        "origin": "Élaboré à partir de fleurs Sénégal / Burkina selon arrivages",
        "weight_info": "50 cl — bouteille verre",
        "ingredients": "Eau, sucre de canne, infusion hibiscus (minimum 18 %), jus de citron, extrait de menthe.",
        "allergens": "",
        "usage_tips": "Servez très frais avec glaçons et zestes d’orange.",
        "conservation": "Après ouverture : au frais et consommer sous 20 jours.",
    },
    {
        "sku": "COSM-KARITE-150G",
        "slug": "beurre-karite-brut-150g",
        "name": "Beurre de karité brut — 150 g",
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
    row for row in (CATALOGUE + EXTENDED_CATALOGUE) if row["slug"] in CATALOGUE_SLUGS
]


def _product_payload(row):
    data = dict(row)
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
    """Ajoute les nouvelles références sans toucher aux produits existants."""
    from sqlalchemy import inspect

    if not inspect(db.engine).has_table("products"):
        return
    changed = False
    for row in FULL_CATALOGUE:
        slug = row["slug"]
        product = Product.query.filter_by(slug=slug).first()
        if product:
            if row.get("icon") and not product.icon:
                product.icon = row["icon"]
                changed = True
            continue
        db.session.add(Product(**_product_payload(row)))
        changed = True
    if changed:
        db.session.commit()
