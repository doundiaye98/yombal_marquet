# -*- coding: utf-8 -*-
"""Configuration pytest — base SQLite isolée, sans envoi mail réel."""

from __future__ import annotations

import os
import tempfile
import uuid

import pytest

_test_db = tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False)
_test_db.close()

os.environ.setdefault("FLASK_SECRET_KEY", "pytest-secret-key")
os.environ["DATABASE_URL"] = f"sqlite:///{_test_db.name.replace(os.sep, '/')}"
os.environ["TESTING"] = "1"
os.environ["MAIL_SUPPRESS_SEND"] = "1"
os.environ["PAYMENT_SIMULATION"] = "1"
os.environ["STRIPE_WEBHOOK_SECRET"] = "whsec_pytest_secret"

from app import app as flask_app  # noqa: E402
from extensions import db  # noqa: E402
from models import Order, OrderItem  # noqa: E402
from models.constants import ORDER_STATUS_PENDING  # noqa: E402
from models.product import Product  # noqa: E402


@pytest.fixture
def app():
    flask_app.config.update(
        TESTING=True,
        SERVER_NAME="localhost.localdomain",
        PREFERRED_URL_SCHEME="https",
    )
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def sample_product(app):
    with app.app_context():
        slug = f"test-{uuid.uuid4().hex[:8]}"
        product = Product(
            slug=slug,
            name="Produit test",
            description="Description test",
            price_cents=160,
            category="cereales",
            stock_qty=20,
            is_active=True,
        )
        db.session.add(product)
        db.session.commit()
        product_id = product.id
        yield product
        db.session.query(OrderItem).filter_by(product_id=product_id).delete()
        db.session.query(Product).filter_by(id=product_id).delete()
        db.session.commit()


@pytest.fixture
def guest_checkout_form():
    return {
        "guest_email": "client@test.example",
        "guest_name": "Jean Test",
        "customer_phone": "+33601020304",
        "delivery_line1": "12 rue de la Paix",
        "delivery_city": "Paris",
        "delivery_postal_code": "75001",
        "delivery_country": "FR",
    }


@pytest.fixture
def guest_order(app, sample_product, guest_checkout_form):
    with app.app_context():
        shipping = 590
        total = sample_product.price_cents + shipping
        order = Order(
            guest_email=guest_checkout_form["guest_email"],
            guest_name=guest_checkout_form["guest_name"],
            guest_phone=guest_checkout_form["customer_phone"],
            delivery_line1=guest_checkout_form["delivery_line1"],
            delivery_city=guest_checkout_form["delivery_city"],
            delivery_postal_code=guest_checkout_form["delivery_postal_code"],
            delivery_country=guest_checkout_form["delivery_country"],
            subtotal_cents=sample_product.price_cents,
            shipping_cents=shipping,
            total_cents=total,
            status=ORDER_STATUS_PENDING,
        )
        db.session.add(order)
        db.session.flush()
        db.session.add(
            OrderItem.from_product(sample_product, 1, order.id),
        )
        db.session.commit()
        order_id = order.id
        yield order
        db.session.query(OrderItem).filter_by(order_id=order_id).delete()
        db.session.query(Order).filter_by(id=order_id).delete()
        db.session.commit()
