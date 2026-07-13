# -*- coding: utf-8 -*-
"""Tests demande projet immobilier."""

from models.contact_message import ContactMessage


def test_immo_demande_get(client):
    r = client.get("/ecosysteme/immobilier-btp/demande")
    assert r.status_code == 200
    assert b"Demander" in r.data
    assert b"Yenne Ndoukhoura" in r.data


def test_immo_demande_get_with_terrain(client):
    r = client.get("/ecosysteme/immobilier-btp/demande?terrain=sangalcam")
    assert r.status_code == 200
    assert b"Sangalcam" in r.data


def test_immo_demande_post_creates_message(client, app):
    r = client.post(
        "/ecosysteme/immobilier-btp/demande",
        data={
            "name": "Amadou Diop",
            "email": "amadou@example.com",
            "phone": "0612345678",
            "country": "France",
            "project_type": "achat_terrain",
            "terrain_slug": "yenne-ndoukhoura",
            "message": "Je souhaite visiter le site en juillet.",
            "consent": "1",
        },
        follow_redirects=True,
    )
    assert r.status_code == 200
    assert b"Demande envoy" in r.data

    with app.app_context():
        msg = ContactMessage.query.order_by(ContactMessage.id.desc()).first()
        assert msg is not None
        assert msg.email == "amadou@example.com"
        assert "YOMBAL KEUR" in msg.subject
        assert "Yenne Ndoukhoura" in msg.message


def test_immo_demande_post_validation(client):
    r = client.post(
        "/ecosysteme/immobilier-btp/demande",
        data={"name": "A", "email": "bad", "consent": "0"},
    )
    assert r.status_code == 200
    assert b"field-input" in r.data
