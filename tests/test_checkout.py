# -*- coding: utf-8 -*-
"""Tests checkout — validation et création de commande invité."""

from __future__ import annotations

from models import Order
from models.constants import ORDER_STATUS_PENDING


def test_checkout_empty_cart_redirects(client):
    with client.session_transaction() as sess:
        sess["cart"] = {}

    response = client.get("/checkout", follow_redirects=False)
    assert response.status_code == 302
    assert "/boutique" in response.headers["Location"]


def test_checkout_guest_creates_order(client, sample_product, guest_checkout_form):
    client.post(
        "/panier/ajouter",
        data={"product_id": sample_product.id, "quantity": 1},
        follow_redirects=True,
    )

    response = client.post("/checkout", data=guest_checkout_form, follow_redirects=False)
    assert response.status_code == 302
    assert "/paiement/" in response.headers["Location"]

    with client.application.app_context():
        order = Order.query.order_by(Order.id.desc()).first()
        assert order is not None
        assert order.guest_email == guest_checkout_form["guest_email"]
        assert order.status == ORDER_STATUS_PENDING
        assert order.total_cents > sample_product.price_cents

    with client.session_transaction() as sess:
        assert sess.get("cart") == {}


def test_checkout_rejects_invalid_email(client, sample_product, guest_checkout_form):
    client.post(
        "/panier/ajouter",
        data={"product_id": sample_product.id, "quantity": 1},
        follow_redirects=True,
    )

    bad_form = dict(guest_checkout_form)
    bad_form["guest_email"] = "pas-un-email"
    response = client.post("/checkout", data=bad_form)
    assert response.status_code == 200
    assert b"e-mail valide" in response.data
