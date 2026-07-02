# -*- coding: utf-8 -*-
"""Tests webhook Stripe — signature, idempotence, mise à jour commande."""

from __future__ import annotations

import json
from types import SimpleNamespace
from unittest.mock import patch

from models.constants import ORDER_STATUS_PAID_STRIPE, ORDER_STATUS_PENDING, PAYMENT_STRIPE

import app as app_module


def test_webhook_get_is_active(client):
    response = client.get("/webhooks/stripe")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["ok"] is True
    assert payload["endpoint"] == "stripe_webhook"


def test_webhook_without_secret_is_ignored(client, guest_order):
    with patch.dict("os.environ", {"STRIPE_WEBHOOK_SECRET": ""}, clear=False):
        response = client.post(
            "/webhooks/stripe",
            data=json.dumps({"type": "payment_intent.succeeded"}),
            content_type="application/json",
        )
    assert response.status_code == 200
    assert response.data == b""

    with client.application.app_context():
        from extensions import db

        order = db.session.get(type(guest_order), guest_order.id)
        assert order.status == ORDER_STATUS_PENDING


def test_webhook_payment_intent_succeeded_marks_order_paid(client, guest_order):
    event = {
        "type": "payment_intent.succeeded",
        "data": {
            "object": {
                "id": "pi_test_123",
                "amount": guest_order.total_cents,
                "status": "succeeded",
                "metadata": {"order_id": str(guest_order.id)},
            }
        },
    }

    with patch.object(app_module.stripe_sdk.Webhook, "construct_event", return_value=event):
        response = client.post(
            "/webhooks/stripe",
            data=json.dumps(event),
            headers={"Stripe-Signature": "t=1,v1=test"},
            content_type="application/json",
        )

    assert response.status_code == 200

    with client.application.app_context():
        from extensions import db

        order = db.session.get(type(guest_order), guest_order.id)
        assert order.status == ORDER_STATUS_PAID_STRIPE
        assert order.payment_method == PAYMENT_STRIPE
        assert order.stripe_session_id == "pi_test_123"


def test_webhook_invalid_signature_returns_400(client):
    with patch.object(
        app_module.stripe_sdk.Webhook,
        "construct_event",
        side_effect=ValueError("bad signature"),
    ):
        response = client.post(
            "/webhooks/stripe",
            data="{}",
            headers={"Stripe-Signature": "invalid"},
            content_type="application/json",
        )
    assert response.status_code == 400


def test_apply_stripe_pi_wrong_amount_is_rejected(app, guest_order):
    with app.app_context():
        from extensions import db

        order = db.session.get(type(guest_order), guest_order.id)
        pi = SimpleNamespace(
            id="pi_bad_amount",
            amount=order.total_cents + 100,
            status="succeeded",
            metadata={"order_id": str(order.id)},
        )
        result = app_module._apply_stripe_pi_to_order(order, pi)
        assert result == "amount_bad"
        assert order.status == ORDER_STATUS_PENDING


def test_apply_stripe_pi_is_idempotent(app, guest_order):
    with app.app_context():
        from extensions import db

        order = db.session.get(type(guest_order), guest_order.id)
        pi = SimpleNamespace(
            id="pi_ok",
            amount=order.total_cents,
            status="succeeded",
            metadata={"order_id": str(order.id)},
        )
        assert app_module._apply_stripe_pi_to_order(order, pi) == "ok"
        assert app_module._apply_stripe_pi_to_order(order, pi) == "already_paid"
