# -*- coding: utf-8 -*-
"""Assistant boutique — retrieval + génération de réponse."""

from __future__ import annotations

import logging
import os
import re

from models.knowledge_chunk import KnowledgeChunk
from models.product import Product
from services import content as content_svc
from services import embeddings as embed_svc

logger = logging.getLogger(__name__)

DEFAULT_CHAT_MODEL = "gpt-4o-mini"
MAX_QUESTION_LEN = 500
DEFAULT_TOP_K = 5

ORDER_HINT_PATTERNS = (
    r"\bcommande\b",
    r"\bsuivi\b",
    r"\bcolis\b",
    r"\blivraison\b.*\b(où|quand|statut)\b",
    r"\bnuméro de commande\b",
    r"\btracking\b",
)

THANKS_REPLY = (
    "Je vous en prie, c'est un plaisir de vous accompagner. "
    "Toute l'équipe Yombal Marché reste à votre disposition pour vos questions "
    "sur nos produits, recettes ou services. "
    "Nous vous souhaitons une excellente journée."
)

THANKS_ONLY_PATTERNS = (
    r"^(?:un\s+)?(?:grand\s+)?merci(?:\s+(?:beaucoup|infiniment|bien|à\s+vous|pour\s+(?:tout|votre\s+aide|l'?info(?:rmation)?(?:rmations)?|votre\s+réponse|votre\s+message)))?[\s!.]*$",
    r"^je\s+vous\s+remercie(?:\s+(?:beaucoup|infiniment|bien))?[\s!.]*$",
    r"^(?:thanks?|thank\s+you)(?:\s+(?:a\s+lot|so\s+much))?[\s!.]*$",
    r"^(?:ok|d'accord|parfait|super|génial|très\s+bien)[\s,!.]+(?:merci|je\s+vous\s+remercie)(?:\s+(?:beaucoup|infiniment|pour\s+tout))?[\s!.]*$",
    r"^(?:merci|je\s+vous\s+remercie)[\s,!.]+(?:ok|d'accord|parfait|super|génial|très\s+bien)[\s!.]*$",
)

SYSTEM_PROMPT = """Tu es l'assistant de Yombal Marché, une épicerie sénégalaise en ligne.
Réponds en français, de façon chaleureuse et concise (3 à 6 phrases max sauf liste de produits).

Règles strictes :
- Utilise UNIQUEMENT les informations du contexte fourni ci-dessous.
- Ne invente jamais de prix, de stock, de délai de livraison ni de produit absent du contexte.
- Si la question concerne le suivi d'une commande précise (numéro, statut, colis), indique d'utiliser la page « Suivi de commande » avec le numéro et l'e-mail d'achat.
- Si tu ne sais pas, propose de contacter la boutique via la page Contact.
- Mentionne les noms de produits ou recettes pertinents quand c'est utile.
- Ne donne pas de conseils médicaux.
- Si le client vous remercie simplement, répondez avec professionnalisme et courtoisie, sans relancer une vente."""

REFUSAL_NO_KEY = (
    "L'assistant n'est pas disponible pour le moment. "
    "Consultez la FAQ sur la page Contact ou écrivez-nous directement."
)
REFUSAL_EMPTY_INDEX = (
    "L'assistant IA est presque prêt : le catalogue n'est pas encore indexé. "
    "En attendant, voici une recherche directe dans notre boutique."
)
REFUSAL_API_ERROR = (
    "L'assistant IA est temporairement indisponible. "
    "Voici une recherche dans notre catalogue, ou contactez-nous via la page Contact."
)
REFUSAL_ORDER = (
    "Pour suivre une commande, rendez-vous sur la page Suivi de commande "
    "avec votre numéro de commande et l'e-mail utilisé lors de l'achat."
)


def assistant_enabled() -> bool:
    flag = (os.environ.get("ASSISTANT_ENABLED") or "1").strip().lower()
    return flag not in ("0", "false", "no", "off")


def chat_model() -> str:
    return (os.environ.get("OPENAI_CHAT_MODEL") or DEFAULT_CHAT_MODEL).strip()


def top_k() -> int:
    try:
        return max(1, min(10, int(os.environ.get("ASSISTANT_TOP_K") or DEFAULT_TOP_K)))
    except ValueError:
        return DEFAULT_TOP_K


def _normalize_question(text: str) -> str:
    q = (text or "").strip()
    if len(q) > MAX_QUESTION_LEN:
        q = q[:MAX_QUESTION_LEN]
    return q


def _looks_like_order_tracking(question: str) -> bool:
    lower = question.lower()
    return any(re.search(pat, lower) for pat in ORDER_HINT_PATTERNS)


def _looks_like_thanks(question: str) -> bool:
    """Remerciement simple (pas « merci de… » = formule de politesse / demande)."""
    q = (question or "").strip().lower()
    if not q or len(q) > 120:
        return False
    if re.match(r"^merci\s+d[e']", q):
        return False
    return any(re.search(pat, q) for pat in THANKS_ONLY_PATTERNS)


def _question_tokens(question: str) -> list[str]:
    stop = {
        "avez", "vous", "des", "les", "une", "est", "pour", "dans", "avec", "sans",
        "comment", "quels", "quel", "quelle", "que", "qui", "sur", "pas", "plus",
        "tout", "tous", "notre", "nos", "votre", "mes", "the", "and", "are",
    }
    tokens = [t.lower() for t in re.findall(r"[a-zàâäéèêëïîôùûüç0-9]+", question.lower())]
    return [t for t in tokens if len(t) >= 3 and t not in stop]


def _score_text(haystack: str, tokens: list[str]) -> float:
    if not haystack or not tokens:
        return 0.0
    text = haystack.lower()
    return float(sum(1 for token in tokens if token in text))


def _local_hits(question: str, limit: int = 5) -> list[dict]:
    tokens = _question_tokens(question)
    if not tokens:
        tokens = [question.lower()[:40]]

    hits: list[dict] = []

    for product in Product.query.filter_by(is_active=True).all():
        hay = " ".join(
            filter(
                None,
                [
                    product.name,
                    product.summary,
                    product.description,
                    product.ingredients,
                    product.category,
                    product.origin,
                    product.slug,
                ],
            )
        )
        score = _score_text(hay, tokens)
        if score <= 0:
            continue
        snippet = (product.summary or product.description or "")[:160]
        hits.append(
            {
                "score": score,
                "type": "product",
                "id": product.slug,
                "title": product.name,
                "url": f"/produit/{product.slug}",
                "line": f"{product.name} — {product.price_euros():.2f} € — {snippet}",
            }
        )

    for i, item in enumerate(content_svc.all_faq_items()):
        hay = f"{item.get('q', '')} {item.get('a', '')}"
        score = _score_text(hay, tokens)
        if score <= 0:
            continue
        hits.append(
            {
                "score": score + 0.5,
                "type": "faq",
                "id": f"faq-{i}",
                "title": item.get("q", "FAQ"),
                "url": "/contact#faq",
                "line": f"{item.get('q', '')} — {item.get('a', '')}",
            }
        )

    for recipe in content_svc.all_recipe_defs():
        hay = " ".join(
            filter(
                None,
                [
                    recipe.get("title"),
                    recipe.get("summary"),
                    recipe.get("kind_label"),
                    " ".join(
                        ing.get("product_slug", "")
                        for ing in recipe.get("ingredients", [])
                    ),
                ],
            )
        )
        score = _score_text(hay, tokens)
        if score <= 0:
            continue
        hits.append(
            {
                "score": score,
                "type": "recipe",
                "id": recipe["slug"],
                "title": recipe.get("title", recipe["slug"]),
                "url": f"/recette/{recipe['slug']}",
                "line": f"Recette : {recipe.get('title', '')} — {recipe.get('summary', '')}",
            }
        )

    for coffret in content_svc.all_coffret_defs():
        hay = " ".join(
            filter(
                None,
                [
                    coffret.get("title"),
                    coffret.get("summary"),
                    coffret.get("theme_label"),
                    " ".join(
                        ing.get("product_slug", "")
                        for ing in coffret.get("ingredients", [])
                    ),
                ],
            )
        )
        score = _score_text(hay, tokens)
        if score <= 0:
            continue
        hits.append(
            {
                "score": score,
                "type": "coffret",
                "id": coffret["slug"],
                "title": coffret.get("title", coffret["slug"]),
                "url": f"/coffret/{coffret['slug']}",
                "line": f"Coffret : {coffret.get('title', '')} — {coffret.get('summary', '')}",
            }
        )

    for chunk in KnowledgeChunk.query.all():
        score = _score_text(chunk.content, tokens)
        if score <= 0:
            continue
        if any(h["type"] == chunk.source_type and h["id"] == chunk.source_id for h in hits):
            continue
        hits.append(
            {
                "score": score,
                "type": chunk.source_type,
                "id": chunk.source_id,
                "title": chunk.title,
                "url": chunk.url_path or "/",
                "line": f"{chunk.title} — {(chunk.content or '')[:140]}",
            }
        )

    hits.sort(key=lambda item: item["score"], reverse=True)
    return hits[:limit]


def _answer_from_local_hits(question: str, hits: list[dict], *, prefix: str = "") -> dict:
    if not hits:
        return {
            "answer": (
                "Je n'ai pas trouvé de réponse précise dans le catalogue. "
                "Parcourez la boutique, la FAQ (page Contact) ou écrivez-nous."
            ),
            "sources": [],
            "mode": "local",
        }

    lines = [prefix] if prefix else []
    lines.append("Voici ce que j'ai trouvé :")
    lines.extend(f"• {hit['line']}" for hit in hits)
    lines.append("")
    lines.append("Cliquez sur les liens ci-dessous pour plus de détails.")

    sources = [
        {
            "type": hit["type"],
            "id": hit["id"],
            "title": hit["title"],
            "url": hit["url"],
            "score": round(hit["score"], 2),
        }
        for hit in hits
    ]
    return {"answer": "\n".join(line for line in lines if line is not None), "sources": sources, "mode": "local"}


def answer_local(question: str) -> dict:
    return _answer_from_local_hits(question, _local_hits(question))


def ai_mode_available() -> bool:
    return embed_svc.is_configured()


def _refresh_product_facts(chunks: list[KnowledgeChunk]) -> list[str]:
    """Réinjecte prix/stock à jour pour les produits cités."""
    lines = []
    for chunk in chunks:
        if chunk.source_type != "product":
            lines.append(chunk.content)
            continue
        product = Product.query.filter_by(slug=chunk.source_id, is_active=True).first()
        if not product:
            lines.append(chunk.content)
            continue
        stock = "en stock" if product.in_stock() else "indisponible ou stock limité"
        if product.stock_qty is not None:
            stock = f"stock actuel: {product.stock_qty}"
        lines.append(
            f"{chunk.content}\n"
            f"[Prix actuel vérifié: {product.price_euros():.2f} € | {stock}]"
        )
    return lines


def retrieve(question: str, k: int | None = None) -> list[tuple[KnowledgeChunk, float]]:
    k = k or top_k()
    query_vec = embed_svc.embed_texts([question])[0]
    rows = KnowledgeChunk.query.filter(KnowledgeChunk.embedding_json.isnot(None)).all()
    scored: list[tuple[KnowledgeChunk, float]] = []
    for row in rows:
        vec = row.embedding()
        if not vec:
            continue
        score = embed_svc.cosine_similarity(query_vec, vec)
        scored.append((row, score))
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]


def _call_chat(messages: list[dict]) -> str:
    api_key = (os.environ.get("OPENAI_API_KEY") or "").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY manquant")

    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=chat_model(),
        messages=messages,
        temperature=0.3,
        max_tokens=600,
    )
    return (response.choices[0].message.content or "").strip()


def answer(question: str) -> dict:
    """
    Répond à une question client.
    Retourne {answer, sources, hint?}.
    """
    q = _normalize_question(question)
    if not q:
        return {"answer": "Posez une question sur nos produits, recettes ou services.", "sources": []}

    if not assistant_enabled():
        return {"answer": REFUSAL_NO_KEY, "sources": []}

    if _looks_like_order_tracking(q):
        return {"answer": REFUSAL_ORDER, "sources": [], "hint": "order_tracking"}

    if _looks_like_thanks(q):
        return {"answer": THANKS_REPLY, "sources": [], "hint": "thanks", "mode": "courtesy"}

    if not embed_svc.is_configured():
        return answer_local(q)

    indexed = KnowledgeChunk.query.filter(KnowledgeChunk.embedding_json.isnot(None)).count()
    if indexed == 0:
        return answer_local(q)

    try:
        hits = retrieve(q)
    except Exception as exc:
        logger.exception("RAG retrieve: %s", exc)
        local = _local_hits(q)
        if local:
            return _answer_from_local_hits(q, local)
        return _answer_from_local_hits(q, [], prefix=REFUSAL_API_ERROR)

    if not hits:
        local = _local_hits(q)
        if local:
            return _answer_from_local_hits(q, local)
        return {
            "answer": "Je n'ai pas trouvé d'information précise. Consultez la boutique ou contactez-nous.",
            "sources": [],
        }

    context_blocks = _refresh_product_facts([chunk for chunk, _ in hits])
    context = "\n\n---\n\n".join(context_blocks)
    user_prompt = f"Contexte boutique :\n\n{context}\n\nQuestion client : {q}"

    try:
        reply = _call_chat(
            [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ]
        )
    except Exception as exc:
        logger.exception("RAG chat: %s", exc)
        local = _local_hits(q)
        if local:
            return _answer_from_local_hits(q, local)
        return _answer_from_local_hits(q, [], prefix=REFUSAL_API_ERROR)

    sources = []
    seen = set()
    for chunk, score in hits:
        key = (chunk.source_type, chunk.source_id)
        if key in seen:
            continue
        seen.add(key)
        src = chunk.as_source_dict()
        src["score"] = round(score, 4)
        sources.append(src)

    return {"answer": reply, "sources": sources, "mode": "ai"}
