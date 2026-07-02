# -*- coding: utf-8 -*-
"""Tests panier — service et routes HTTP."""

from __future__ import annotations

from services import cart as cart_svc


def test_add_to_cart_increases_quantity(app, sample_product):
    with app.test_request_context():
        ok, err = cart_svc.add_to_cart(sample_product.id, 1)
        assert ok is True
        assert err is None
        assert cart_svc.cart_raw()[str(sample_product.id)] == 1

        ok, err = cart_svc.add_to_cart(sample_product.id, 2)
        assert ok is True
        assert cart_svc.cart_raw()[str(sample_product.id)] == 3


def test_set_cart_qty_zero_removes_item(app, sample_product):
    with app.test_request_context():
        cart_svc.add_to_cart(sample_product.id, 2)
        ok, err = cart_svc.set_cart_qty(sample_product.id, 0)
        assert ok is True
        assert err is None
        assert str(sample_product.id) not in cart_svc.cart_raw()


def test_stock_validation_blocks_oversell(app, sample_product):
    with app.app_context():
        sample_product.stock_qty = 5
        from extensions import db

        db.session.commit()

    with app.test_request_context():
        ok, err = cart_svc.add_to_cart(sample_product.id, 6)
        assert ok is False
        assert "Stock insuffisant" in (err or "")


def test_panier_ajouter_route(client, sample_product):
    response = client.post(
        "/panier/ajouter",
        data={"product_id": sample_product.id, "quantity": 1},
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert "Location" in response.headers

    with client.session_transaction() as sess:
        assert sess.get("cart", {}).get(str(sample_product.id)) == 1


def test_panier_page_lists_product(client, sample_product):
    client.post(
        "/panier/ajouter",
        data={"product_id": sample_product.id, "quantity": 1},
        follow_redirects=True,
    )
    response = client.get("/panier")
    assert response.status_code == 200
    assert sample_product.name.encode() in response.data
