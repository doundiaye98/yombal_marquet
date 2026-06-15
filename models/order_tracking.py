# -*- coding: utf-8 -*-
"""Recherche et affichage du suivi commande client."""

import re

from extensions import db
from models.order import Order


def parse_order_reference(raw: str):
    """Retourne (order_id, public_ref) — l'un des deux est renseigné."""
    text = (raw or "").strip()
    if not text:
        return None, None
    upper = text.upper()
    m = re.match(r"^YOMBAL-CMD-(\d+)$", upper)
    if m:
        return int(m.group(1)), None
    m = re.match(r"^YM-\d{8}-[A-F0-9]{6}$", upper)
    if m:
        return None, upper
    if text.isdigit():
        return int(text), None
    if upper.startswith("YM-"):
        return None, upper
    return None, None


def find_order_by_reference_and_email(ref: str, email: str):
    order_id, public_ref = parse_order_reference(ref)
    email_norm = (email or "").strip().lower()
    if not email_norm:
        return None
    if order_id:
        order = db.session.get(Order, order_id)
    elif public_ref:
        order = Order.query.filter_by(public_ref=public_ref).first()
    else:
        return None
    if not order:
        return None
    if (order.customer_email() or "").strip().lower() != email_norm:
        return None
    return order
