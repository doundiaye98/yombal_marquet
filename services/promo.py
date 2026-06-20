# -*- coding: utf-8 -*-
from models.promo_code import PromoCode


def normalize_code(code):
    return (code or "").strip().upper()


def validate_promo(code, subtotal_cents):
    norm = normalize_code(code)
    if not norm:
        return None, 0, None
    promo = PromoCode.query.filter_by(code=norm).first()
    if not promo or not promo.is_valid_now():
        return None, 0, "Code promo invalide ou expiré."
    discount = promo.discount_for_subtotal(subtotal_cents)
    if discount <= 0:
        return None, 0, "Ce code ne s'applique pas à ce montant de commande."
    return promo, discount, None


def apply_promo_use(promo):
    if promo:
        promo.used_count = (promo.used_count or 0) + 1
