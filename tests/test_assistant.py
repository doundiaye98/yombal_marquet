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
