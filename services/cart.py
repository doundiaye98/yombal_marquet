# -*- coding: utf-8 -*-
from flask import session

from extensions import db
from models.product import Product


def cart_raw():
    return session.get("cart") or {}


def cart_meta():
    return session.get("cart_meta") or {}


def cart_count():
    return sum(int(q) for q in cart_raw().values() if str(q).isdigit())


def _validate_stock(product, qty_needed):
    if not product.in_stock(qty_needed):
        avail = product.stock_qty if product.stock_qty is not None else "∞"
        return False, f"Stock insuffisant pour « {product.name} » (dispo : {avail})."
    return True, None


def add_to_cart(product_id, quantity=1, bundle_type=None, bundle_slug=None):
    product = db.session.get(Product, int(product_id))
    if not product or not product.is_active:
        return False, "Produit introuvable."
    qty = max(1, min(20, int(quantity or 1)))
    cart = dict(cart_raw())
    pid = str(product.id)
    new_total = cart.get(pid, 0) + qty
    if new_total > 99:
        new_total = 99
    ok, err = _validate_stock(product, new_total)
    if not ok:
        return False, err
    cart[pid] = new_total
    session["cart"] = cart
    if bundle_type and bundle_slug:
        meta = dict(cart_meta())
        meta[pid] = {"bundle_type": bundle_type, "bundle_slug": bundle_slug}
        session["cart_meta"] = meta
    session.modified = True
    return True, None


def set_cart_qty(product_id, quantity):
    cart = dict(cart_raw())
    pid = str(product_id)
    if pid not in cart:
        return False, "Article absent du panier."
    if quantity is None or quantity < 1:
        cart.pop(pid, None)
        meta = dict(cart_meta())
        meta.pop(pid, None)
        session["cart_meta"] = meta
    else:
        qty = max(1, min(99, int(quantity)))
        product = db.session.get(Product, int(pid))
        if not product:
            cart.pop(pid, None)
        else:
            ok, err = _validate_stock(product, qty)
            if not ok:
                return False, err
            cart[pid] = qty
    session["cart"] = cart
    session.modified = True
    return True, None


def cart_items():
    raw = cart_raw()
    meta = cart_meta()
    rows = []
    total = 0
    for pid, qty in raw.items():
        try:
            q = max(1, min(99, int(qty)))
        except (TypeError, ValueError):
            continue
        p = db.session.get(Product, int(pid))
        if p and p.is_active:
            line = {"product": p, "quantity": q}
            if pid in meta:
                line["bundle_type"] = meta[pid].get("bundle_type")
                line["bundle_slug"] = meta[pid].get("bundle_slug")
            rows.append(line)
            total += p.price_cents * q
    return rows, total


def clear_cart():
    session["cart"] = {}
    session["cart_meta"] = {}
    session.modified = True


def decrement_stock_for_order(items):
    for row in items:
        product = row["product"]
        qty = row["quantity"]
        if product.stock_qty is not None:
            product.stock_qty = max(0, product.stock_qty - qty)


def restore_stock_for_order(order):
    for line in order.items:
        product = line.product
        if product and product.stock_qty is not None:
            product.stock_qty += line.quantity
