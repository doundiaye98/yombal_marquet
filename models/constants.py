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
