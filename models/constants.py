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

ORDER_STATUS_LABELS = {
    ORDER_STATUS_PENDING: "Commande enregistrée",
    ORDER_STATUS_AWAITING_WIRE: "En attente de virement",
    ORDER_STATUS_AWAITING_PAYPAL: "En attente PayPal",
    ORDER_STATUS_COD_CONFIRMED: "Paiement à la livraison confirmé",
    ORDER_STATUS_PAID_STRIPE: "Payée par carte",
    ORDER_STATUS_PAID_DEMO: "Payée (démo)",
    ORDER_STATUS_PAID_MANUAL: "Paiement reçu",
    ORDER_STATUS_SHIPPED: "Expédiée / en livraison",
    ORDER_STATUS_CANCELLED: "Annulée",
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
    {"id": 1, "title": "Commande", "desc": "Reçue"},
    {"id": 2, "title": "Paiement", "desc": "Validé"},
    {"id": 3, "title": "Préparation", "desc": "En cours"},
    {"id": 4, "title": "Livraison", "desc": "Expédiée"},
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
CATEGORY_BOISSONS = "boissons"
CATEGORY_CEREALES = "cereales"
CATEGORY_CONDIMENTS = "condiments"
CATEGORY_HUILES = "huiles"
CATEGORY_SNACKS = "snacks"
CATEGORY_CONSERVES = "conserves"
CATEGORY_LEGUMINEUSES = "legumineuses"
CATEGORY_FRUITS_SECS = "fruits_secs"

PRODUCT_CATEGORIES = {
    CATEGORY_ALIMENTAIRE: {"label": "Alimentaire", "emoji": "🛒"},
    CATEGORY_COSMETIQUE: {"label": "Cosmétique", "emoji": "✨"},
    CATEGORY_BOISSONS: {"label": "Boissons", "emoji": "🥤"},
    CATEGORY_CEREALES: {"label": "Céréales", "emoji": "🌾"},
    CATEGORY_CONDIMENTS: {"label": "Condiments", "emoji": "🧂"},
    CATEGORY_HUILES: {"label": "Huiles", "emoji": "🫒"},
    CATEGORY_SNACKS: {"label": "Snacks & Desserts", "emoji": "🍮"},
    CATEGORY_CONSERVES: {"label": "Conserves", "emoji": "🫙"},
    CATEGORY_LEGUMINEUSES: {"label": "Légumineuses", "emoji": "🫘"},
    CATEGORY_FRUITS_SECS: {"label": "Fruits séchés", "emoji": "🥭"},
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
    CATEGORY_COSMETIQUE,
)
