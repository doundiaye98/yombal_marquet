# -*- coding: utf-8 -*-
"""Estimation de livraison (délai configurable en admin)."""

from datetime import datetime, timedelta

from services.settings import shop_settings

_FR_MONTHS = (
    "janvier",
    "février",
    "mars",
    "avril",
    "mai",
    "juin",
    "juillet",
    "août",
    "septembre",
    "octobre",
    "novembre",
    "décembre",
)


def _parse_days(value, default):
    try:
        return max(1, int(value))
    except (TypeError, ValueError):
        return default


def delivery_day_range(shop=None):
    shop = shop or shop_settings()
    min_d = _parse_days(shop.get("shop_delivery_days_min"), 3)
    max_d = _parse_days(shop.get("shop_delivery_days_max"), 7)
    if max_d < min_d:
        max_d = min_d
    return min_d, max_d


def _fr_date(d):
    return f"{d.day} {_FR_MONTHS[d.month - 1]}"


def format_date_range(min_date, max_date):
    if min_date == max_date:
        return _fr_date(min_date)
    if min_date.year == max_date.year and min_date.month == max_date.month:
        return f"{min_date.day} – {max_date.day} {_FR_MONTHS[min_date.month - 1]}"
    return f"{_fr_date(min_date)} – {_fr_date(max_date)}"


def estimate_from_datetime(from_dt=None, shop=None):
    from_dt = from_dt or datetime.utcnow()
    min_d, max_d = delivery_day_range(shop)
    base = from_dt.date() if hasattr(from_dt, "date") else from_dt
    min_date = base + timedelta(days=min_d)
    max_date = base + timedelta(days=max_d)
    return {
        "min_date": min_date,
        "max_date": max_date,
        "days_min": min_d,
        "days_max": max_d,
        "label": format_date_range(min_date, max_date),
        "short": f"{min_d}–{max_d} j. ouvrés",
    }


def estimate_for_order(order, shop=None):
    return estimate_from_datetime(order.created_at if order else None, shop=shop)


def estimate_checkout_preview(shop=None):
    """Estimation affichée au checkout avant création de commande."""
    return estimate_from_datetime(shop=shop)
