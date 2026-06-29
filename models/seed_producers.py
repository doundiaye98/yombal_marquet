# -*- coding: utf-8 -*-
"""Producteurs locaux — vitrine traçabilité."""

from extensions import db
from models.producer import Producer
from models.product import Product

PRODUCERS = [
    {
        "slug": "aminata-diallo",
        "name": "Aminata Diallo",
        "region": "Casamance, Ziguinchor",
        "flagship_product": "Huile de palme artisanale",
        "experience": "20 ans de savoir-faire familial",
        "method": "Extraction traditionnelle, sans additifs ni raffinage industriel",
        "monthly_production": "50 litres",
        "avatar_emoji": "👩🏾‍🌾",
        "story": (
            "Aminata perpétue l’art de l’huile de palme rouge dans son village de Bignona. "
            "Les régimes sont cueillis à la main, pressés dans une mare traditionnelle, puis reposés "
            "pour obtenir une huile dense, parfumée et riche en vitamine A.\n\n"
            "« Chaque litre raconte notre terre et le travail des femmes de ma famille. "
            "Vendre sur Yombal Marché, c’est faire connaître la Casamance au-delà des frontières. »"
        ),
        "product_slugs": ["huile-palme-artisanale-1l"],
    },
    {
        "slug": "fatou-ndiaye",
        "name": "Fatou Ndiaye",
        "region": "Thiès, Sénégal",
        "flagship_product": "Sirop de bissap (hibiscus)",
        "experience": "15 ans dans la transformation florale",
        "method": "Infusion lente des fleurs, sucre de canne équitable, sans colorant",
        "monthly_production": "120 bouteilles de 50 cl",
        "avatar_emoji": "👩🏾‍🌾",
        "story": (
            "Fatou collecte les fleurs d’hibiscus auprès de petits exploitants du bassin arachidier. "
            "Elle maîtrise chaque étape : séchage à l’ombre, macération, filtration et embouteillage.\n\n"
            "Son sirop est devenu l’indispensable des fêtes de quartier — désormais disponible "
            "chez vous grâce à Yombal Marché."
        ),
        "product_slugs": ["sirop-bissap-ud", "bissap-seche-200g", "bissap-rouge-zena"],
    },
    {
        "slug": "cooperative-tafraout",
        "name": "Coopérative Tafraout",
        "region": "Souss-Massa, Maroc",
        "flagship_product": "Huile d’argan cosmétique",
        "experience": "Coopérative fondée en 2008 — 40 femmes",
        "method": "Première pression à froid, amandes décortiquées à la main",
        "monthly_production": "80 litres d’huile vierge",
        "avatar_emoji": "🌿",
        "story": (
            "Nichée entre arganiers centenaires, la coopérative valorise le savoir-faire berbère "
            "tout en garantissant des revenus directs aux productrices.\n\n"
            "Chaque flacon d’huile d’argan Yombal Marché est tracé jusqu’au lot de pression "
            "et soutient l’éducation des enfants des villages partenaires."
        ),
        "product_slugs": ["huile-argan-bio-100ml"],
    },
    {
        "slug": "moussa-kone",
        "name": "Moussa Koné",
        "region": "Banfora, Burkina Faso",
        "flagship_product": "Beurre de karité brut",
        "experience": "3ᵉ génération de collecteurs",
        "method": "Noix séchées, broyées et battues — beurre non raffiné",
        "monthly_production": "200 kg de beurre",
        "avatar_emoji": "👨🏾‍🌾",
        "story": (
            "Moussa coordonne un réseau de 25 familles qui récoltent les noix de karité dans les parcs "
            "naturels du sud-ouest burkinabè.\n\n"
            "Le beurre est transformé sur place pour éviter les intermédiaires et préserver "
            "l’odeur noisette caractéristique tant appréciée en cosmétique artisanale."
        ),
        "product_slugs": ["beurre-karite-brut-150g", "beurre-karite-alimentaire-250g"],
    },
    {
        "slug": "rucher-alpilles",
        "name": "Sophie & Marc — Rucher des Alpilles",
        "region": "Bouches-du-Rhône, France",
        "flagship_product": "Miel de thym cru",
        "experience": "12 ruches transhumantes",
        "method": "Miellée sauvage, extraction à froid, non chauffé",
        "monthly_production": "Variable selon floraison — 40 à 80 kg",
        "avatar_emoji": "🍯",
        "story": (
            "Le couple parcourt les garrigues provençales au rythme des floraisons. "
            "Le miel de thym est récolté lorsque les plants sont en pleine floraison, "
            "pour un goût corsé et une texture crémeuse.\n\n"
            "Transparence totale : numéro de rucher et date de récolte sur chaque pot."
        ),
        "product_slugs": ["miel-thym-500g"],
    },
    {
        "slug": "atelier-sahel",
        "name": "Atelier Sahel",
        "region": "Fès-Meknès & Provence",
        "flagship_product": "Savon noir traditionnel",
        "experience": "Artisanat du hammam depuis 1995",
        "method": "Saponification à l’huile d’olive, enrichi eucalyptus",
        "monthly_production": "300 pots de 200 g",
        "avatar_emoji": "🧼",
        "story": (
            "L’atelier réunit des savonniers marocains et français autour du savon noir, "
            "pilier du rituel du hammam.\n\n"
            "La pâte noire est malaxée à la main puis reposée avant conditionnement — "
            "un geste simple, efficace, transmis de maître à apprenti."
        ),
        "product_slugs": ["savon-noir-eucalyptus"],
    },
    {
        "slug": "oasis-jericho",
        "name": "Famille Al-Hadid",
        "region": "Vallée du Jourdain",
        "flagship_product": "Dates Medjool",
        "experience": "Palmeraie familiale — 4 générations",
        "method": "Cueillette à maturité, tri manuel, dénoyautage",
        "monthly_production": "2 tonnes en saison",
        "avatar_emoji": "🌴",
        "story": (
            "Sous les palmiers, chaque régime est inspecté avant récolte pour garantir "
            "une chair fondante et caramel naturel.\n\n"
            "La famille exporte une petite partie de sa production via Yombal Marché "
            "pour toucher une clientèle sensible à la qualité premium."
        ),
        "product_slugs": ["dattes-seches-ud", "dattes-branchees-ud"],
    },
    {
        "slug": "plantation-las-flores",
        "name": "Plantation Las Flores",
        "region": "Huehuetenango, Guatemala",
        "flagship_product": "Café",
        "experience": "Culture en altitude depuis 1982",
        "method": "Torréfaction moyenne par petits lots, commerce direct",
        "monthly_production": "600 kg de café vert",
        "avatar_emoji": "☕",
        "story": (
            "À plus de 1 600 m d’altitude, les cerises de café mûrissent lentement "
            "et développent des notes de fruits rouges.\n\n"
            "La plantation pratique l’agroforesterie et réinvestit une partie des ventes "
            "dans une école du village voisin."
        ),
        "product_slugs": ["cafe-arabica-250g"],
    },
    {
        "slug": "famille-bencherif",
        "name": "Famille Bencherif",
        "region": "Constantine, Algérie",
        "flagship_product": "Couscous complet",
        "experience": "Meunerie artisanale — 30 ans",
        "method": "Blé dur complet, précuit vapeur, sans blanchiment",
        "monthly_production": "1,5 tonne de semoule",
        "avatar_emoji": "🌾",
        "story": (
            "La famille Bencherif perpétue la semoulerie traditionnelle : le grain garde son enveloppe "
            "pour plus de fibres et de goût.\n\n"
            "Leur couscous accompagne les tables du Maghreb et arrive désormais directement "
            "dans vos placards via Yombal Marché."
        ),
        "product_slugs": ["couscous-complet-1kg"],
    },
    {
        "slug": "univers-diaspora",
        "name": "Univers Diaspora — LabelAfrik",
        "region": "Paris & Afrique de l'Ouest",
        "flagship_product": "Arraw, Thiakhry, Fonio, Baobab",
        "experience": "Partenariat LabelAfrik — du champ à la table",
        "method": "Produits 100 % locaux, sans gluten, savoir-faire traditionnel",
        "monthly_production": "Catalogue épicerie africaine",
        "avatar_emoji": "🌍",
        "story": (
            "Univers Diaspora valorise la richesse du patrimoine africain à travers des produits "
            "authentiques, issus du savoir-faire local et du respect de la nature.\n\n"
            "Ce partenariat est né d'une vision commune : promouvoir l'excellence africaine, "
            "du champ à la table, en alliant tradition, innovation et durabilité.\n\n"
            "Chaque grain, chaque saveur, chaque création raconte une histoire — celle d'un "
            "continent vibrant, fier et tourné vers l'avenir."
        ),
        "product_slugs": [],  # lié dynamiquement aux slugs LabelAfrik
    },
]

PALM_OIL_PRODUCT = {
    "sku": "ALIM-PALME-1L",
    "slug": "huile-palme-artisanale-1l",
    "name": "Huile de palme rouge artisanale — 1 L",
    "summary": "Pressée à froid par Aminata Diallo — Casamance, sans additifs.",
    "description": (
        "Huile de palme rouge traditionnelle, issue de régimes mûrs cueillis à la main "
        "dans les palmeraies de Basse-Casamance.\n\n"
        "Extraction par broyage et décantation lente : couleur rouge intense, "
        "arôme fruité, riche en caroténoïdes. Idéale pour mijoter sauces, riz gras "
        "et plats ouest-africains authentiques.\n\n"
        "Chaque litre soutient directement le travail d’Aminata Diallo et des femmes de son collectif."
    ),
    "price_cents": 1290,
    "category": "huiles",
    "origin": "Casamance, Sénégal — productrice Aminata Diallo",
    "weight_info": "1 L — bouteille verre ambré",
    "ingredients": "100 % huile de palme rouge brute.",
    "allergens": "",
    "usage_tips": "Une cuillère à soupe suffit pour parfumer un plat pour 4 personnes. Ne pas surchauffer.",
    "conservation": "À l’abri de la lumière ; consommer sous 6 mois après ouverture.",
    "producer_slug": "aminata-diallo",
    "icon": "🟠",
}


def _ensure_palm_oil_product():
    if Product.query.filter_by(slug=PALM_OIL_PRODUCT["slug"]).first():
        return
    row = dict(PALM_OIL_PRODUCT)
    row.pop("producer_slug", None)
    db.session.add(Product(**row))
    db.session.commit()


def seed_producers():
    """Crée les fiches producteurs et les lie aux produits du catalogue."""
    from sqlalchemy import inspect

    if not inspect(db.engine).has_table("producers"):
        return

    _ensure_palm_oil_product()

    for entry in PRODUCERS:
        data = dict(entry)
        slugs = data.pop("product_slugs", [])
        producer = Producer.query.filter_by(slug=data["slug"]).first()
        if not producer:
            producer = Producer(**data)
            db.session.add(producer)
            db.session.flush()
        else:
            for key, value in data.items():
                setattr(producer, key, value)

        for slug in slugs:
            product = Product.query.filter_by(slug=slug).first()
            if product and product.producer_id != producer.id:
                product.producer_id = producer.id

    palm = Product.query.filter_by(slug="huile-palme-artisanale-1l").first()
    if palm:
        if palm.category != "huiles":
            palm.category = "huiles"
        if not palm.icon:
            palm.icon = "🟠"
    sirop_bissap = Product.query.filter_by(slug="sirop-bissap-ud").first()
    if sirop_bissap and sirop_bissap.category != "boissons":
        sirop_bissap.category = "boissons"

    _link_univers_diaspora_products()

    db.session.commit()


def _link_univers_diaspora_products():
    """Associe le producteur Univers Diaspora aux produits LabelAfrik."""
    try:
        from models.catalogue_labelafrik import LABELAFRIK_SLUGS
    except ImportError:
        return
    producer = Producer.query.filter_by(slug="univers-diaspora").first()
    if not producer:
        return
    for slug in LABELAFRIK_SLUGS:
        product = Product.query.filter_by(slug=slug).first()
        if product and product.producer_id != producer.id:
            product.producer_id = producer.id
