# -*- coding: utf-8 -*-
"""Construction et indexation des chunks RAG depuis le catalogue."""

from __future__ import annotations

import hashlib
import logging

from extensions import db
from models.coffret_model import Coffret
from models.faq_item import FaqItem
from models.knowledge_chunk import KnowledgeChunk
from models.producer import Producer
from models.product import Product
from models.recipe_model import Recipe
from services import content as content_svc
from services import embeddings as embed_svc

logger = logging.getLogger(__name__)

BATCH_SIZE = 32


def _hash_content(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _join(*parts):
    return "\n".join(p for p in parts if p and str(p).strip())


def _product_chunk(product: Product) -> dict:
    producer_name = product.producer.name if product.producer else ""
    stock = "en stock" if product.in_stock() else "rupture ou stock limité"
    if product.stock_qty is not None:
        stock = f"stock: {product.stock_qty} unité(s)"

    content = _join(
        f"Type: produit",
        f"Nom: {product.name}",
        f"Prix: {product.price_euros():.2f} €",
        f"Catégorie: {product.category}",
        f"Référence (slug): {product.slug}",
        f"Disponibilité: {stock}",
        f"Origine: {product.origin}" if product.origin else "",
        f"Poids/format: {product.weight_info}" if product.weight_info else "",
        f"Producteur: {producer_name}" if producer_name else "",
        f"Résumé: {product.summary}" if product.summary else "",
        f"Description: {product.description}" if product.description else "",
        f"Ingrédients: {product.ingredients}" if product.ingredients else "",
        f"Allergènes: {product.allergens}" if product.allergens else "",
        f"Conservation: {product.conservation}" if product.conservation else "",
        f"Conseils: {product.usage_tips}" if product.usage_tips else "",
    )
    return {
        "source_type": "product",
        "source_id": product.slug,
        "title": product.name,
        "content": content,
        "url_path": f"/produit/{product.slug}",
    }


def _faq_chunk(item: dict, index: int) -> dict:
    content = _join(
        "Type: FAQ",
        f"Question: {item['q']}",
        f"Réponse: {item['a']}",
    )
    source_id = f"faq-{index}"
    return {
        "source_type": "faq",
        "source_id": source_id,
        "title": item["q"],
        "content": content,
        "url_path": "/contact",
    }


def _recipe_chunk(recipe: dict) -> dict:
    ingredients = []
    for ing in recipe.get("ingredients", []):
        slug = ing.get("product_slug") or ""
        qty = ing.get("quantity") or 1
        note = ing.get("note") or ""
        line = f"- {slug} x{qty}"
        if note:
            line += f" ({note})"
        ingredients.append(line)

    steps = recipe.get("steps") or []
    content = _join(
        "Type: recette",
        f"Titre: {recipe.get('title', '')}",
        f"Catégorie: {recipe.get('kind_label') or recipe.get('kind', '')}",
        f"Durée: {recipe.get('time_minutes')} min" if recipe.get("time_minutes") else "",
        f"Portions: {recipe.get('servings')}" if recipe.get("servings") else "",
        f"Résumé: {recipe.get('summary')}" if recipe.get("summary") else "",
        "Ingrédients:",
        "\n".join(ingredients) if ingredients else "",
        "Étapes:",
        "\n".join(f"{i + 1}. {s}" for i, s in enumerate(steps)) if steps else "",
    )
    slug = recipe["slug"]
    return {
        "source_type": "recipe",
        "source_id": slug,
        "title": recipe.get("title") or slug,
        "content": content,
        "url_path": f"/recette/{slug}",
    }


def _coffret_chunk(coffret: dict) -> dict:
    items = []
    for ing in coffret.get("ingredients", []):
        slug = ing.get("product_slug") or ""
        qty = ing.get("quantity") or 1
        items.append(f"- {slug} x{qty}")

    content = _join(
        "Type: coffret cadeau",
        f"Titre: {coffret.get('title', '')}",
        f"Thème: {coffret.get('theme_label') or coffret.get('theme', '')}",
        f"Résumé: {coffret.get('summary')}" if coffret.get("summary") else "",
        f"Message cadeau: {coffret.get('gift_message')}" if coffret.get("gift_message") else "",
        "Contenu:",
        "\n".join(items) if items else "",
    )
    slug = coffret["slug"]
    return {
        "source_type": "coffret",
        "source_id": slug,
        "title": coffret.get("title") or slug,
        "content": content,
        "url_path": f"/coffret/{slug}",
    }


def _producer_chunk(producer: Producer) -> dict:
    products = [p.name for p in producer.active_products().limit(12)]
    content = _join(
        "Type: producteur",
        f"Nom: {producer.name}",
        f"Région: {producer.region}",
        f"Produit phare: {producer.flagship_product}",
        f"Expérience: {producer.experience}" if producer.experience else "",
        f"Méthode: {producer.method}" if producer.method else "",
        f"Production: {producer.monthly_production}" if producer.monthly_production else "",
        f"Histoire: {producer.story}",
        "Produits associés: " + ", ".join(products) if products else "",
    )
    return {
        "source_type": "producer",
        "source_id": producer.slug,
        "title": producer.name,
        "content": content,
        "url_path": f"/producteur/{producer.slug}",
    }


def collect_chunk_defs() -> list[dict]:
    """Rassemble tous les documents à indexer depuis la base."""
    defs: list[dict] = []

    products = Product.query.filter_by(is_active=True).order_by(Product.name).all()
    defs.extend(_product_chunk(p) for p in products)

    for i, item in enumerate(content_svc.all_faq_items()):
        defs.append(_faq_chunk(item, i))

    for recipe in content_svc.all_recipe_defs():
        defs.append(_recipe_chunk(recipe))

    for coffret in content_svc.all_coffret_defs():
        defs.append(_coffret_chunk(coffret))

    producers = Producer.query.filter_by(is_active=True).order_by(Producer.name).all()
    defs.extend(_producer_chunk(p) for p in producers)

    return defs


def _upsert_chunk(defn: dict, vector: list[float] | None = None) -> str:
    content_hash = _hash_content(defn["content"])
    row = KnowledgeChunk.query.filter_by(
        source_type=defn["source_type"],
        source_id=defn["source_id"],
    ).first()

    if row and row.content_hash == content_hash:
        if vector is None and not row.embedding():
            return "skipped"
        if vector is not None and row.embedding() and row.content_hash == content_hash:
            return "skipped"

    if not row:
        row = KnowledgeChunk(
            source_type=defn["source_type"],
            source_id=defn["source_id"],
        )
        db.session.add(row)

    row.title = defn["title"]
    row.content = defn["content"]
    row.url_path = defn.get("url_path")
    row.content_hash = content_hash
    if vector is not None:
        row.set_embedding(vector)
    elif not row.embedding_json:
        row.embedding_json = None
    return "updated"


def _is_openai_quota_error(exc: Exception) -> bool:
    message = str(exc).lower()
    return "insufficient_quota" in message or "exceeded your current quota" in message


def _index_local(defs: list[dict], stats: dict) -> None:
    for defn in defs:
        try:
            action = _upsert_chunk(defn, vector=None)
            if action == "skipped":
                stats["skipped"] += 1
            else:
                stats["updated"] += 1
        except Exception as exc:
            logger.warning("Upsert local %s/%s: %s", defn["source_type"], defn["source_id"], exc)
            stats["errors"] += 1
    db.session.commit()


def index_all(*, force: bool = False, local_only: bool = False) -> dict:
    """
    Indexe le catalogue dans knowledge_chunks.
    - local_only=True : sans OpenAI (texte seul, recherche locale)
    - local_only=False : embeddings OpenAI si disponibles
    Retourne des statistiques {total, updated, skipped, errors, mode}.
    """
    defs = collect_chunk_defs()
    stats = {
        "total": len(defs),
        "updated": 0,
        "skipped": 0,
        "errors": 0,
        "mode": "local" if local_only else "ai",
    }

    if force:
        KnowledgeChunk.query.delete()
        db.session.commit()

    if local_only or not embed_svc.is_configured():
        if not local_only and not embed_svc.is_configured():
            logger.warning("OPENAI_API_KEY absent — indexation locale.")
        stats["mode"] = "local"
        _index_local(defs, stats)
    else:
        quota_exhausted = False
        for start in range(0, len(defs), BATCH_SIZE):
            if quota_exhausted:
                break
            batch = defs[start : start + BATCH_SIZE]
            try:
                vectors = embed_svc.embed_texts([d["content"] for d in batch])
            except Exception as exc:
                if _is_openai_quota_error(exc):
                    logger.warning("Quota OpenAI épuisé — bascule indexation locale.")
                    quota_exhausted = True
                    stats["mode"] = "local"
                    stats["quota_fallback"] = True
                    break
                logger.exception("Embeddings batch %s: %s", start, exc)
                stats["errors"] += len(batch)
                continue

            for defn, vector in zip(batch, vectors, strict=False):
                try:
                    action = _upsert_chunk(defn, vector)
                    if action == "skipped":
                        stats["skipped"] += 1
                    else:
                        stats["updated"] += 1
                except Exception as exc:
                    logger.warning("Upsert %s/%s: %s", defn["source_type"], defn["source_id"], exc)
                    stats["errors"] += 1

            db.session.commit()

        if quota_exhausted:
            _index_local(defs, stats)

    # Supprimer les chunks orphelins (produit retiré du catalogue)
    live_keys = {(d["source_type"], d["source_id"]) for d in defs}
    stale = KnowledgeChunk.query.all()
    removed = 0
    for row in stale:
        if (row.source_type, row.source_id) not in live_keys:
            db.session.delete(row)
            removed += 1
    if removed:
        db.session.commit()
    stats["removed"] = removed
    return stats


def chunk_count() -> int:
    return KnowledgeChunk.query.count()


def embedded_chunk_count() -> int:
    return KnowledgeChunk.query.filter(KnowledgeChunk.embedding_json.isnot(None)).count()
