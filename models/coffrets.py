# -*- coding: utf-8 -*-
"""Coffrets cadeaux diaspora — bundles produits Yombal Marché."""

COFFRETS = [
    {
        "slug": "goutiers-enfance",
        "title": "Goûters d'enfance",
        "emoji": "🍯",
        "theme": "diaspora",
        "theme_label": "Diaspora & souvenirs",
        "summary": "Miel, dattes et douceurs — le goût des dimanches et des retrouvailles en famille.",
        "gift_message": "Pour retrouver les saveurs du quartier, là où que vous soyez.",
        "ingredients": [
            {"product_slug": "miel-thym-500g", "quantity": 1},
            {"product_slug": "dates-medjool-400g", "quantity": 1},
            {"product_slug": "pastilles-tamarin-150g", "quantity": 1},
        ],
    },
    {
        "slug": "soins-naturels-maman",
        "title": "Soins naturels maman",
        "emoji": "🌿",
        "theme": "soin",
        "theme_label": "Beauté & bien-être",
        "summary": "Karité, argan et savon noir — un rituel hammam à offrir ou à s'offrir.",
        "gift_message": "Prenez soin de vous avec les trésors du terroir africain.",
        "ingredients": [
            {"product_slug": "beurre-karite-brut-150g", "quantity": 1},
            {"product_slug": "huile-argan-bio-100ml", "quantity": 1},
            {"product_slug": "savon-noir-eucalyptus", "quantity": 1},
        ],
    },
    {
        "slug": "premier-appart",
        "title": "Premier appart'",
        "emoji": "🏠",
        "theme": "quotidien",
        "theme_label": "Quotidien diaspora",
        "summary": "Café, couscous, bissap et sel — l'essentiel pour bien s'installer.",
        "gift_message": "Bienvenue chez vous — les bases du placard, version terroir.",
        "ingredients": [
            {"product_slug": "cafe-arabica-250g", "quantity": 1},
            {"product_slug": "couscous-complet-1kg", "quantity": 1},
            {"product_slug": "bissap-concentre-50cl", "quantity": 1},
            {"product_slug": "sel-kaolack-500g", "quantity": 1},
        ],
    },
    {
        "slug": "terroir-senegalais",
        "title": "Terroir sénégalais",
        "emoji": "🇸🇳",
        "theme": "terroir",
        "theme_label": "Saveurs du Sénégal",
        "summary": "Huile de palme, riz, bissap et piment — un voyage culinaire en coffret.",
        "gift_message": "Du marché de Dakar à votre table, sans prendre l'avion.",
        "ingredients": [
            {"product_slug": "huile-palme-artisanale-1l", "quantity": 1},
            {"product_slug": "riz-brise-local-1kg", "quantity": 1},
            {"product_slug": "bissap-seche-200g", "quantity": 1},
            {"product_slug": "piment-sec-moulu-80g", "quantity": 1},
        ],
    },
]


def get_coffret_by_slug(slug):
    for coffret in COFFRETS:
        if coffret["slug"] == slug:
            return coffret
    return None
