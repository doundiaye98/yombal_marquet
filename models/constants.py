# -*- coding: utf-8 -*-
"""Valeurs métier centralisées — évite les chaînes magiques dans le code."""

ORDER_STATUS_PENDING = "pending"
ORDER_STATUS_AWAITING_WIRE = "awaiting_wire"
ORDER_STATUS_AWAITING_PAYPAL = "awaiting_paypal"
ORDER_STATUS_COD_CONFIRMED = "cod_confirmed"
ORDER_STATUS_PAID_STRIPE = "paid_stripe"
ORDER_STATUS_PAID_DEMO = "paid_demo"
ORDER_STATUS_PAID_MANUAL = "paid_manual"
ORDER_STATUS_SHIPPED = "shipped"
ORDER_STATUS_CANCELLED = "cancelled"

# Statuts annulables par le client (avant préparation / expédition)
ORDER_STATUS_CANCELLABLE = frozenset(
    {
        ORDER_STATUS_PENDING,
        ORDER_STATUS_AWAITING_WIRE,
        ORDER_STATUS_AWAITING_PAYPAL,
        ORDER_STATUS_COD_CONFIRMED,
    }
)

ORDER_STATUS_LABELS = {
    ORDER_STATUS_PENDING: "En attente de paiement",
    ORDER_STATUS_AWAITING_WIRE: "Virement en cours",
    ORDER_STATUS_AWAITING_PAYPAL: "PayPal en attente",
    ORDER_STATUS_COD_CONFIRMED: "Paiement à la livraison",
    ORDER_STATUS_PAID_STRIPE: "Payée — en préparation",
    ORDER_STATUS_PAID_DEMO: "Payée — en préparation",
    ORDER_STATUS_PAID_MANUAL: "Payée — en préparation",
    ORDER_STATUS_SHIPPED: "Expédiée",
    ORDER_STATUS_CANCELLED: "Annulée",
}

# Pastille courte (hub commandes type marketplace)
ORDER_STATUS_PILL = {
    ORDER_STATUS_PENDING: ("À payer", "pill-warning"),
    ORDER_STATUS_AWAITING_WIRE: ("Virement", "pill-info"),
    ORDER_STATUS_AWAITING_PAYPAL: ("PayPal", "pill-info"),
    ORDER_STATUS_COD_CONFIRMED: ("À la livraison", "pill-info"),
    ORDER_STATUS_PAID_STRIPE: ("Préparation", "pill-success"),
    ORDER_STATUS_PAID_DEMO: ("Préparation", "pill-success"),
    ORDER_STATUS_PAID_MANUAL: ("Préparation", "pill-success"),
    ORDER_STATUS_SHIPPED: ("En livraison", "pill-shipped"),
    ORDER_STATUS_CANCELLED: ("Annulée", "pill-muted"),
}

ORDER_STATUS_HINTS = {
    ORDER_STATUS_PENDING: "Finalisez le paiement pour lancer la préparation.",
    ORDER_STATUS_AWAITING_WIRE: "Effectuez le virement avec la référence indiquée.",
    ORDER_STATUS_AWAITING_PAYPAL: "Envoyez le paiement PayPal avec la référence commande.",
    ORDER_STATUS_COD_CONFIRMED: "Vous réglerez le montant à la livraison.",
    ORDER_STATUS_PAID_STRIPE: "Votre paiement est confirmé. Préparation en cours.",
    ORDER_STATUS_PAID_DEMO: "Paiement simulé enregistré.",
    ORDER_STATUS_PAID_MANUAL: "Paiement validé par notre équipe.",
    ORDER_STATUS_SHIPPED: "Votre colis est en route ou a été livré.",
    ORDER_STATUS_CANCELLED: "Cette commande a été annulée.",
}

# Étape courante (1–4) pour la barre de progression client
ORDER_STATUS_STEP = {
    ORDER_STATUS_PENDING: 1,
    ORDER_STATUS_AWAITING_WIRE: 2,
    ORDER_STATUS_AWAITING_PAYPAL: 2,
    ORDER_STATUS_COD_CONFIRMED: 2,
    ORDER_STATUS_PAID_STRIPE: 3,
    ORDER_STATUS_PAID_DEMO: 3,
    ORDER_STATUS_PAID_MANUAL: 3,
    ORDER_STATUS_SHIPPED: 4,
    ORDER_STATUS_CANCELLED: 0,
}

ORDER_TRACKING_STEPS = (
    {"id": 1, "title": "Commande", "desc": "Confirmée", "icon": "📋"},
    {"id": 2, "title": "Paiement", "desc": "Validé", "icon": "💳"},
    {"id": 3, "title": "Préparation", "desc": "En cours", "icon": "📦"},
    {"id": 4, "title": "Livraison", "desc": "En route", "icon": "🚚"},
)

ORDER_STATUSES = frozenset(
    {
        ORDER_STATUS_PENDING,
        ORDER_STATUS_AWAITING_WIRE,
        ORDER_STATUS_AWAITING_PAYPAL,
        ORDER_STATUS_COD_CONFIRMED,
        ORDER_STATUS_PAID_STRIPE,
        ORDER_STATUS_PAID_DEMO,
        ORDER_STATUS_PAID_MANUAL,
        ORDER_STATUS_SHIPPED,
        ORDER_STATUS_CANCELLED,
    }
)

PAYMENT_STRIPE = "stripe"
PAYMENT_PAYPAL = "paypal"
PAYMENT_WIRE = "wire"
PAYMENT_CASH_DELIVERY = "cash_delivery"
PAYMENT_DEMO = "demo"

CATEGORY_ALIMENTAIRE = "alimentaire"
CATEGORY_COSMETIQUE = "cosmetique"
CATEGORY_ELECTRONIQUE = "electronique"
CATEGORY_ELECTROMENAGER = "electromenager"
CATEGORY_MODE = "mode"
CATEGORY_CHAUSSURES = "chaussures"
CATEGORY_BAGAGERIE = "bagagerie"
CATEGORY_BOISSONS = "boissons"
CATEGORY_CEREALES = "cereales"
CATEGORY_CONDIMENTS = "condiments"
CATEGORY_HUILES = "huiles"
CATEGORY_SNACKS = "snacks"
CATEGORY_CONSERVES = "conserves"
CATEGORY_LEGUMINEUSES = "legumineuses"
CATEGORY_FRUITS_SECS = "fruits_secs"
CATEGORY_POISSON = "poisson"
CATEGORY_VIANDES = "viandes"

PRODUCT_CATEGORIES = {
    CATEGORY_ALIMENTAIRE: {"label": "Alimentaire", "emoji": "🛒"},
    CATEGORY_COSMETIQUE: {"label": "Cosmétique", "emoji": "✨"},
    CATEGORY_ELECTRONIQUE: {"label": "Électronique", "emoji": "📱"},
    CATEGORY_ELECTROMENAGER: {"label": "Électroménager", "emoji": "🏠"},
    CATEGORY_MODE: {"label": "Habillement", "emoji": "👕"},
    CATEGORY_CHAUSSURES: {"label": "Chaussures", "emoji": "👟"},
    CATEGORY_BAGAGERIE: {"label": "Sacs & bagagerie", "emoji": "🎒"},
    CATEGORY_BOISSONS: {"label": "Boissons", "emoji": "🥤"},
    CATEGORY_CEREALES: {"label": "Céréales", "emoji": "🌾"},
    CATEGORY_CONDIMENTS: {"label": "Condiments", "emoji": "🧂"},
    CATEGORY_HUILES: {"label": "Huiles", "emoji": "🫒"},
    CATEGORY_SNACKS: {"label": "Snacks & Desserts", "emoji": "🍮"},
    CATEGORY_CONSERVES: {"label": "Conserves", "emoji": "🫙"},
    CATEGORY_LEGUMINEUSES: {"label": "Légumineuses", "emoji": "🫘"},
    CATEGORY_FRUITS_SECS: {"label": "Fruits séchés", "emoji": "🥭"},
    CATEGORY_POISSON: {"label": "Produits de la mer", "emoji": "🐟"},
    CATEGORY_VIANDES: {"label": "Viandes & volailles", "emoji": "🍗"},
}

SHOP_CATEGORY_ORDER = (
    CATEGORY_ALIMENTAIRE,
    CATEGORY_BOISSONS,
    CATEGORY_CEREALES,
    CATEGORY_HUILES,
    CATEGORY_CONDIMENTS,
    CATEGORY_LEGUMINEUSES,
    CATEGORY_FRUITS_SECS,
    CATEGORY_SNACKS,
    CATEGORY_CONSERVES,
    CATEGORY_POISSON,
    CATEGORY_VIANDES,
    CATEGORY_COSMETIQUE,
    CATEGORY_ELECTRONIQUE,
    CATEGORY_ELECTROMENAGER,
    CATEGORY_MODE,
    CATEGORY_CHAUSSURES,
    CATEGORY_BAGAGERIE,
)

# Pays de livraison (code ISO → libellé)
DELIVERY_COUNTRIES = {
    "FR": "France",
    "BE": "Belgique",
    "LU": "Luxembourg",
    "CH": "Suisse",
    "DE": "Allemagne",
    "ES": "Espagne",
    "IT": "Italie",
    "GB": "Royaume-Uni",
    "SN": "Sénégal",
    "CI": "Côte d'Ivoire",
    "ML": "Mali",
    "GN": "Guinée",
    "MA": "Maroc",
    "TN": "Tunisie",
    "DZ": "Algérie",
    "CM": "Cameroun",
    "GA": "Gabon",
}

# Frais livraison internationale forfaitaires (centimes EUR), hors France
INTERNATIONAL_SHIPPING_CENTS = {
    "BE": 890,
    "LU": 790,
    "DE": 990,
    "ES": 1190,
    "IT": 1190,
    "CH": 1490,
    "GB": 1290,
    "SN": 1490,
    "CI": 1490,
    "ML": 1490,
    "GN": 1490,
    "MA": 1290,
    "TN": 1290,
    "DZ": 1290,
    "CM": 1690,
    "GA": 1690,
}
DEFAULT_INTERNATIONAL_SHIPPING_CENTS = 1490
