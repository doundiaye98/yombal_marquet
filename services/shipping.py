# -*- coding: utf-8 -*-
from models.constants import (
    DEFAULT_INTERNATIONAL_SHIPPING_CENTS,
    INTERNATIONAL_SHIPPING_CENTS,
)
from models.delivery_zone import DeliveryZone


def shipping_cents_for_postal(postal_code, subtotal_cents):
    code = (postal_code or "").strip().replace(" ", "")
    if not code:
        return 590
    zones = (
        DeliveryZone.query.filter_by(is_active=True)
        .order_by(DeliveryZone.sort_order, DeliveryZone.postal_prefix.desc())
        .all()
    )
    best = None
    best_len = -1
    for zone in zones:
        prefix = (zone.postal_prefix or "").strip()
        if prefix and code.startswith(prefix) and len(prefix) > best_len:
            best = zone
            best_len = len(prefix)
    if best:
        return best.price_for_subtotal(subtotal_cents)
    return 590


def shipping_cents_for_address(country_code, postal_code, subtotal_cents):
    country = (country_code or "FR").strip().upper()[:2]
    if country == "FR":
        return shipping_cents_for_postal(postal_code, subtotal_cents)
    return INTERNATIONAL_SHIPPING_CENTS.get(country, DEFAULT_INTERNATIONAL_SHIPPING_CENTS)
