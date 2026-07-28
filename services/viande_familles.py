# -*- coding: utf-8 -*-
"""Sous-filtres du rayon Viandes & volailles (bœuf, agneau, volaille…)."""

from __future__ import annotations

from models.constants import CATEGORY_VIANDES

VIANDE_FAMILLE_ORDER = (
    "boeuf",
    "agneau",
    "mouton",
    "volaille",
    "preparations",
    "autres",
)

VIANDE_FAMILLES = {
    "boeuf": {"label": "Bœuf", "emoji": "🥩"},
    "agneau": {"label": "Agneau", "emoji": "🐑"},
    "mouton": {"label": "Mouton", "emoji": "🐏"},
    "volaille": {"label": "Volailles", "emoji": "🍗"},
    "preparations": {"label": "Préparations", "emoji": "🌭"},
    "autres": {"label": "Autres", "emoji": "✦"},
}


def viande_famille_for_product(slug: str | None, name: str | None = None) -> str:
    """Classe un produit viande dans une sous-famille (par slug puis nom)."""
    text = f"{slug or ''} {name or ''}".lower()
    text = (
        text.replace("œ", "oe")
        .replace("é", "e")
        .replace("è", "e")
        .replace("ê", "e")
        .replace("à", "a")
        .replace("ù", "u")
        .replace("î", "i")
        .replace("ô", "o")
    )

    # Préparations d'abord (sauf brochettes déjà typées viande)
    if any(k in text for k in ("merguez", "kefta", "steak-hache", "steak hache")):
        return "preparations"

    if "mouton" in text:
        return "mouton"

    if "agneau" in text or "navarin" in text:
        return "agneau"

    if any(
        k in text
        for k in (
            "poulet",
            "poule",
            "dinde",
            "pintade",
            "volaille",
        )
    ):
        return "volaille"

    if any(
        k in text
        for k in (
            "boeuf",
            "boef",  # typo safety
            "entrecote",
            "faux-filet",
            "faux filet",
            "rumsteck",
            "bavette",
            "onglet",
            "picanha",
            "tomahawk",
            "paleron",
            "gite",
            "gîte",
            "filet-boeuf",
            "filet de boeuf",
            "cote-boeuf",
            "cote de boeuf",
            "roti-boeuf",
            "roti de boeuf",
            "emince",
            "tartare",
            "wagyu",
            "angus",
            "salers",
            "charolais",
            "montbeliarde",
            "aloyau",
            "poire de boeuf",
            "fondue",
            "bourguignon",
        )
    ):
        return "boeuf"

    # Boxes mixtes / escargot / reste
    if "carre-box" in text or "box" in text:
        if "agneau" in text:
            return "agneau"
        if "boeuf" in text or "boef" in text:
            return "boeuf"
        return "autres"

    return "autres"


def filter_products_by_famille(products: list, famille: str | None) -> list:
    if not famille or famille not in VIANDE_FAMILLES:
        return products
    return [
        p
        for p in products
        if viande_famille_for_product(getattr(p, "slug", None), getattr(p, "name", None))
        == famille
    ]


def famille_counts(products: list) -> dict[str, int]:
    counts = {key: 0 for key in VIANDE_FAMILLE_ORDER}
    for p in products:
        key = viande_famille_for_product(getattr(p, "slug", None), getattr(p, "name", None))
        counts[key] = counts.get(key, 0) + 1
    return counts


def familles_nav(products: list) -> list[dict]:
    """Liste des sous-filtres avec compteurs (masque les familles vides)."""
    counts = famille_counts(products)
    items = []
    for key in VIANDE_FAMILLE_ORDER:
        n = counts.get(key, 0)
        if n <= 0:
            continue
        meta = VIANDE_FAMILLES[key]
        items.append(
            {
                "key": key,
                "label": meta["label"],
                "emoji": meta["emoji"],
                "count": n,
            }
        )
    return items


def is_viandes_category(cat: str | None) -> bool:
    return cat == CATEGORY_VIANDES
