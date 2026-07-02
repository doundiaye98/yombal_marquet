# -*- coding: utf-8 -*-
"""Embeddings OpenAI et similarité cosinus (sans dépendance numpy)."""

from __future__ import annotations

import logging
import math
import os
from typing import Sequence

logger = logging.getLogger(__name__)

DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIM = 1536


def is_configured() -> bool:
    return bool((os.environ.get("OPENAI_API_KEY") or "").strip())


def embedding_model() -> str:
    return (os.environ.get("OPENAI_EMBEDDING_MODEL") or DEFAULT_EMBEDDING_MODEL).strip()


def embed_texts(texts: Sequence[str]) -> list[list[float]]:
    """Génère des embeddings via l'API OpenAI."""
    if not texts:
        return []
    api_key = (os.environ.get("OPENAI_API_KEY") or "").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY manquant — impossible d'indexer ou d'interroger l'assistant.")

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("Package openai manquant — pip install openai") from exc

    client = OpenAI(api_key=api_key)
    cleaned = [(t or "").strip() or " " for t in texts]
    response = client.embeddings.create(model=embedding_model(), input=list(cleaned))
    ordered = sorted(response.data, key=lambda row: row.index)
    return [list(row.embedding) for row in ordered]


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = 0.0
    norm_a = 0.0
    norm_b = 0.0
    for x, y in zip(a, b, strict=False):
        dot += x * y
        norm_a += x * x
        norm_b += y * y
    if norm_a <= 0.0 or norm_b <= 0.0:
        return 0.0
    return dot / (math.sqrt(norm_a) * math.sqrt(norm_b))
