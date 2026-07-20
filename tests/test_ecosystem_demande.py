# -*- coding: utf-8 -*-
"""Tests formulaire demande services écosystème."""

from models.contact_message import ContactMessage


def test_ecosystem_page_has_inline_form_transport(client):
    r = client.get("/ecosysteme/transport")
    assert r.status_code == 200
    assert b"id=\"demande-form\"" in r.data
    assert b"Votre demande" in r.data
    assert b"Achats" in r.data
    assert b"Location voiture" in r.data
    assert b"Envoi de colis" in r.data
    assert b"Type de demande" in r.data


def test_ecosystem_demande_redirects_to_page(client):
    r = client.get("/ecosysteme/transport/demande", follow_redirects=False)
    assert r.status_code == 302
    assert "demande-form" in r.headers["Location"]


def test_autres_services_page_has_hub_and_topics(client):
    r = client.get("/ecosysteme/autres-services")
    assert r.status_code == 200
    assert b"Tous nos services" in r.data
    assert b"Service concern" in r.data
    assert b"Investissement" in r.data


def test_ecosystem_demande_unknown_service_404(client):
    r = client.get("/ecosysteme/voyages/demande")
    assert r.status_code == 404


def test_ecosystem_post_on_service_page_creates_message(client, app):
    r = client.post(
        "/ecosysteme/restaurant",
        data={
            "first_name": "Fatou",
            "last_name": "Ndiaye",
            "email": "fatou@example.com",
            "phone": "0611223344",
            "message": "Reservation traiteur pour 50 personnes en septembre.",
            "consent": "1",
        },
    )
    assert r.status_code == 200
    assert b"Demande envoy" in r.data

    with app.app_context():
        msg = ContactMessage.query.order_by(ContactMessage.id.desc()).first()
        assert msg is not None
        assert msg.email == "fatou@example.com"
        assert "Restaurant" in msg.subject


def test_ecosystem_post_transport_requires_topic(client):
    r = client.post(
        "/ecosysteme/transport",
        data={
            "first_name": "Fatou",
            "last_name": "Ndiaye",
            "email": "fatou@example.com",
            "phone": "0611223344",
            "message": "Besoin d une location pour une semaine en aout.",
            "consent": "1",
        },
    )
    assert r.status_code == 200
    assert b"Type de demande" in r.data


def test_ecosystem_post_transport_creates_message(client, app):
    r = client.post(
        "/ecosysteme/transport",
        data={
            "topic_slug": "location_voiture",
            "first_name": "Fatou",
            "last_name": "Ndiaye",
            "email": "fatou@example.com",
            "phone": "0611223344",
            "message": "Besoin d une location pour une semaine en aout.",
            "consent": "1",
        },
    )
    assert r.status_code == 200
    assert b"Demande envoy" in r.data

    with app.app_context():
        msg = ContactMessage.query.order_by(ContactMessage.id.desc()).first()
        assert msg is not None
        assert msg.email == "fatou@example.com"
        assert "Location voiture" in msg.subject or "Location voiture" in msg.message


def test_ecosystem_post_validation(client):
    r = client.post(
        "/ecosysteme/coiffure",
        data={"first_name": "A", "last_name": "", "email": "bad", "message": "court"},
    )
    assert r.status_code == 200
    assert b"field-input" in r.data
