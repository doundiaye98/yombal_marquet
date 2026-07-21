# -*- coding: utf-8 -*-
"""Tests de l'assistant RAG (mocks OpenAI, pas d'appel réseau)."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from extensions import db
from models.knowledge_chunk import KnowledgeChunk
from services import assistant as assistant_svc
from services import rag_index


@pytest.fixture
def indexed_chunks(app):
    with app.app_context():
        rows = [
            KnowledgeChunk(
                source_type="faq",
                source_id="faq-0",
                title="Paiement",
                content="Type: FAQ\nQuestion: Quels paiements ?\nRéponse: Stripe, PayPal, virement.",
                url_path="/contact",
                content_hash="abc",
            ),
            KnowledgeChunk(
                source_type="product",
                source_id="fonio-blanc",
                title="Fonio blanc",
                content="Type: produit\nNom: Fonio blanc\nPrix: 4.50 €\nSans gluten.",
                url_path="/produit/fonio-blanc",
                content_hash="def",
            ),
        ]
        vec_a = [1.0, 0.0, 0.0]
        vec_b = [0.9, 0.1, 0.0]
        rows[0].set_embedding(vec_a)
        rows[1].set_embedding(vec_b)
        for row in rows:
            db.session.add(row)
        db.session.commit()
        yield rows
        KnowledgeChunk.query.delete()
        db.session.commit()


def test_assistant_disabled(client, monkeypatch):
    monkeypatch.setenv("ASSISTANT_ENABLED", "0")
    rv = client.post("/api/assistant", json={"question": "Bonjour"})
    assert rv.status_code == 503


def test_assistant_empty_question(client, monkeypatch):
    monkeypatch.setenv("ASSISTANT_ENABLED", "1")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    rv = client.post("/api/assistant", json={"question": "   "})
    assert rv.status_code == 400


def test_assistant_order_hint(client, monkeypatch):
    monkeypatch.setenv("ASSISTANT_ENABLED", "1")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    rv = client.post("/api/assistant", json={"question": "Où en est ma commande ?"})
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["hint"] == "order_tracking"
    assert "Suivi de commande" in data["answer"]


@pytest.mark.parametrize(
    ("question", "lang", "needle"),
    [
        ("bonjour", "fr", "Bienvenue"),
        ("Bonjour !", "fr", "Bienvenue"),
        ("bonsoir", "fr", "Bienvenue"),
        ("Salut", "fr", "Bienvenue"),
        ("Hello", "en", "welcome"),
        ("nanga def", "wo", "Yombal Market"),
        ("Asalaa maalekum", "wo", "dalal"),
        ("Hola", "es", "bienvenido"),
        ("Ciao", "it", "benvenuto"),
        ("Olá", "pt", "bem-vindo"),
        ("Hallo", "de", "willkommen"),
    ],
)
def test_assistant_greeting(client, monkeypatch, question, lang, needle):
    monkeypatch.setenv("ASSISTANT_ENABLED", "1")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    rv = client.post("/api/assistant", json={"question": question})
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["hint"] == "greeting"
    assert data.get("lang") == lang
    assert needle.lower() in data["answer"].lower()
    assert "Yombal Market" in data["answer"]


def test_detect_language_multilingual():
    assert assistant_svc._detect_language("nanga def") == "wo"
    assert assistant_svc._detect_language("jërëjëf") == "wo"
    assert assistant_svc._detect_language("Where is my order?") == "en"
    assert assistant_svc._detect_language("Bonjour, avez-vous du fonio ?") == "fr"
    assert assistant_svc._detect_language("¿Tienen fonio en la tienda?") == "es"
    assert assistant_svc._detect_language("Haben Sie Fonio?") == "de"
    assert assistant_svc._detect_language("Vorrei un prodotto") == "it"
    assert assistant_svc._detect_language("شكرا") == "ar"


@pytest.mark.parametrize(
    "question",
    [
        "je voudrais voyager ?",
        "Je veux un vol pour le Sénégal",
        "Avez-vous des séjours ?",
    ],
)
def test_assistant_voyages_intent(client, monkeypatch, question):
    monkeypatch.setenv("ASSISTANT_ENABLED", "1")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    rv = client.post("/api/assistant", json={"question": question})
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["hint"] == "ecosystem"
    assert data["ecosystem_slug"] == "voyages"
    assert "Yombal Voyages" in data["answer"]
    assert any(s.get("url", "").startswith("/ecosysteme/voyages") or "teranga" in s.get("url", "") for s in data["sources"])


def test_assistant_immobilier_intent(client, monkeypatch):
    monkeypatch.setenv("ASSISTANT_ENABLED", "1")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    rv = client.post("/api/assistant", json={"question": "Je cherche un terrain au Sénégal"})
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["hint"] == "ecosystem"
    assert data["ecosystem_slug"] == "immobilier-btp"
    assert "Immobilier" in data["answer"]


@pytest.mark.parametrize(
    ("question", "slug"),
    [
        ("Je veux investir en Afrique", "investissement"),
        ("Besoin d'un déménagement", "transport"),
        ("Je cherche un traiteur", "restaurant"),
        ("Prendre rendez-vous coiffure", "coiffure"),
        ("Avez-vous des smartphones ?", "electronique"),
    ],
)
def test_assistant_all_group_services(client, monkeypatch, question, slug):
    monkeypatch.setenv("ASSISTANT_ENABLED", "1")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    rv = client.post("/api/assistant", json={"question": question})
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["hint"] == "ecosystem"
    assert data["ecosystem_slug"] == slug


def test_assistant_group_overview(client, monkeypatch):
    monkeypatch.setenv("ASSISTANT_ENABLED", "1")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    rv = client.post(
        "/api/assistant",
        json={"question": "Quels sont les services du Groupe YOMBAL ?"},
    )
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["hint"] == "ecosystem"
    assert "Yombal Voyages" in data["answer"]
    assert "Yombal Immobilier" in data["answer"]
    assert "Yombal Transports" in data["answer"]
    assert "Yombal Restaurant" in data["answer"]
    assert "Yombal Coiffure" in data["answer"]
    assert len(data["sources"]) >= 7


def test_rag_includes_ecosystem_chunks(app):
    with app.app_context():
        defs = rag_index.collect_chunk_defs()
        eco_ids = {d["source_id"] for d in defs if d["source_type"] == "ecosystem"}
        assert "voyages" in eco_ids
        assert "immobilier-btp" in eco_ids
        assert "transport" in eco_ids
        assert "investissement" in eco_ids
        assert "restaurant" in eco_ids
        assert "coiffure" in eco_ids
        assert "electronique" in eco_ids
        assert "autres-services" in eco_ids

@pytest.mark.parametrize(
    ("question", "lang", "needle"),
    [
        ("merci", "fr", "Je vous en prie"),
        ("Merci beaucoup !", "fr", "excellente journée"),
        ("Je vous remercie", "fr", "Je vous en prie"),
        ("Ok merci", "fr", "Je vous en prie"),
        ("Parfait, merci pour tout", "fr", "Je vous en prie"),
        ("thank you", "en", "You're welcome"),
        ("jërëjëf", "wo", "Amul solo"),
        ("gracias", "es", "De nada"),
        ("grazie", "it", "Prego"),
        ("danke", "de", "Gern geschehen"),
    ],
)
def test_assistant_thanks_reply(client, monkeypatch, question, lang, needle):
    monkeypatch.setenv("ASSISTANT_ENABLED", "1")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    rv = client.post("/api/assistant", json={"question": question})
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["hint"] == "thanks"
    assert data["mode"] == "courtesy"
    assert data.get("lang") == lang
    assert needle.lower() in data["answer"].lower()


def test_assistant_merci_de_not_treated_as_thanks(client, monkeypatch):
    monkeypatch.setenv("ASSISTANT_ENABLED", "1")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    rv = client.post("/api/assistant", json={"question": "Merci de me dire si vous avez du fonio"})
    assert rv.status_code == 200
    data = rv.get_json()
    assert data.get("hint") != "thanks"


@patch("services.assistant._call_chat", return_value="Le fonio est sans gluten et coûte 4,50 €.")
@patch("services.embeddings.embed_texts", return_value=[[0.95, 0.05, 0.0]])
def test_assistant_rag_answer(mock_embed, mock_chat, client, monkeypatch, indexed_chunks):
    monkeypatch.setenv("ASSISTANT_ENABLED", "1")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    rv = client.post("/api/assistant", json={"question": "Avez-vous du fonio sans gluten ?"})
    assert rv.status_code == 200
    data = rv.get_json()
    assert "fonio" in data["answer"].lower()
    assert any(s["type"] == "product" for s in data["sources"])
    mock_chat.assert_called_once()
    mock_embed.assert_called()


def test_assistant_local_without_api_key(client, monkeypatch, sample_product):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("ASSISTANT_ENABLED", "1")
    rv = client.post("/api/assistant", json={"question": "produit test"})
    assert rv.status_code == 200
    data = rv.get_json()
    assert data.get("mode") == "local"
    assert "Produit test" in data["answer"] or data["sources"]


def test_cosine_similarity():
    from services.embeddings import cosine_similarity

    assert cosine_similarity([1, 0], [1, 0]) == pytest.approx(1.0)
    assert cosine_similarity([1, 0], [0, 1]) == pytest.approx(0.0)


def test_collect_chunk_defs(app, sample_product):
    with app.app_context():
        defs = rag_index.collect_chunk_defs()
        slugs = {d["source_id"] for d in defs if d["source_type"] == "product"}
        assert sample_product.slug in slugs


def test_index_all_local(app, sample_product):
    with app.app_context():
        KnowledgeChunk.query.delete()
        db.session.commit()
        stats = rag_index.index_all(local_only=True)
        assert stats["errors"] == 0
        assert stats["mode"] == "local"
        assert rag_index.chunk_count() > 0
        assert rag_index.embedded_chunk_count() == 0
        KnowledgeChunk.query.delete()
        db.session.commit()
