#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Indexe le catalogue pour l'assistant RAG.

Usage :
  python scripts/index_rag.py              # tente OpenAI, sinon mode local
  python scripts/index_rag.py --local      # sans OpenAI (quota épuisé OK)
  python scripts/index_rag.py --force
"""

from __future__ import annotations

import argparse
import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from dotenv import load_dotenv

load_dotenv(os.path.join(_ROOT, ".env"))

from app import app  # noqa: E402
from services import embeddings as embed_svc  # noqa: E402
from services import rag_index  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Indexe produits, FAQ, recettes pour l'assistant RAG.")
    parser.add_argument("--force", action="store_true", help="Supprime l'index existant avant réindexation.")
    parser.add_argument(
        "--local",
        action="store_true",
        help="Indexation sans OpenAI (recherche par mots-clés dans l'assistant).",
    )
    args = parser.parse_args()

    if not args.local and not embed_svc.is_configured():
        print("OPENAI_API_KEY absent — indexation en mode local.")
        args.local = True

    with app.app_context():
        before = rag_index.chunk_count()
        embedded_before = rag_index.embedded_chunk_count()
        print(f"Chunks en base avant : {before} (dont {embedded_before} avec embeddings IA)")

        stats = rag_index.index_all(force=args.force, local_only=args.local)
        after = rag_index.chunk_count()
        embedded_after = rag_index.embedded_chunk_count()

    mode = stats.get("mode", "ai")
    print(
        f"Terminé [{mode}] — sources: {stats['total']}, "
        f"mis à jour: {stats['updated']}, ignorés: {stats['skipped']}, "
        f"erreurs: {stats['errors']}, supprimés: {stats.get('removed', 0)}"
    )
    print(f"Chunks en base après : {after} (dont {embedded_after} avec embeddings IA)")

    if stats.get("quota_fallback"):
        print()
        print("Quota OpenAI épuisé : catalogue indexé en mode LOCAL.")
        print("L'assistant fonctionne par recherche mots-clés. Rechargez OpenAI puis relancez sans --local.")

    if mode == "local" and embedded_after == 0:
        print()
        print("Mode local actif — l'assistant répond sans appeler OpenAI.")

    return 0 if stats["errors"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
