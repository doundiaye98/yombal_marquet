# -*- coding: utf-8 -*-
"""Chunks indexés pour l'assistant RAG (produits, FAQ, recettes…)."""

import json

from extensions import db
from models.mixins import TimestampMixin


class KnowledgeChunk(TimestampMixin, db.Model):
    __tablename__ = "knowledge_chunks"
    __table_args__ = (
        db.UniqueConstraint("source_type", "source_id", name="uq_knowledge_source"),
        db.Index("ix_knowledge_source_type", "source_type"),
    )

    id = db.Column(db.Integer, primary_key=True)
    source_type = db.Column(db.String(40), nullable=False)
    source_id = db.Column(db.String(160), nullable=False)
    title = db.Column(db.String(220), nullable=False)
    content = db.Column(db.Text, nullable=False)
    url_path = db.Column(db.String(255))
    content_hash = db.Column(db.String(64), nullable=False, index=True)
    embedding_json = db.Column(db.Text)

    def embedding(self):
        if not self.embedding_json:
            return None
        try:
            return json.loads(self.embedding_json)
        except (TypeError, ValueError):
            return None

    def set_embedding(self, vector):
        self.embedding_json = json.dumps(vector, ensure_ascii=False) if vector else None

    def as_source_dict(self):
        return {
            "type": self.source_type,
            "id": self.source_id,
            "title": self.title,
            "url": self.url_path,
        }
