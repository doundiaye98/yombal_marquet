# -*- coding: utf-8 -*-
"""Recatégorisation boutique — corrige les rayons mal assignés."""

from __future__ import annotations

# slug → nouvelle catégorie
CATEGORY_FIXES = {
    # —— Dakhar / tamarin : tout en fruits (comme les fruits séchés) ——
    "tamarin-pulpe-200g": "fruits",
    "dakhar-sachet-150g": "fruits",
    "dakhar-sachet-375g": "fruits",
    # —— Fruits séchés / boîtes fruitées ——
    "maad-230g": "fruits",
    "maad-400g": "fruits",
    "ditakh-300g": "fruits",
    # —— Mer : hors conserves / condiments ——
    "yett-coquillages-150g": "poisson",
    "crevettes-sechees-100g": "poisson",
    "pate-sardinelle-pinton": "poisson",
    "sardinelle-pilchards-tomate": "poisson",
    # —— Viandes ——
    "corned-beef-halal": "viandes",
    # —— Conserves / sauces tomate ——
    "concentre-tomates-rolli": "conserves",
    "concentre-tomates-2kg": "conserves",
    # —— Boissons ——
    "jus-citron-sicile-1l": "boissons",
    "cafe-arabica-250g": "boissons",
    "lait-concentre": "boissons",
    # —— Légumes / cuisine ——
    "legumes-seches-thiebou-200g": "legumes",
    # —— Condiment (graines) ——
    "graine-sesame-250g": "condiments",
    # —— Miels (ex-rayon « Alimentaire ») ; couscous → céréales ——
    "miel-thym-500g": "miels",
    "miel-fleurs-500g": "miels",
    "miel-fleurs-1kg": "miels",
    "couscous-complet-1kg": "cereales",
    # —— Poissons séchés / fermentés ——
    "guedj-poisson-200g": "poisson",
    "ketiakh-poisson-100g": "poisson",
}
