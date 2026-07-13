# -*- coding: utf-8 -*-
"""Programme YOMBAL KEUR — terrains diaspora (données des affiches)."""

from __future__ import annotations

IMMOBILIER_CONTACT = {
    "phone": "06 31 27 33 76",
    "phone_href": "tel:+33631273376",
    "email": "imo@universdiaspora.com",
    "address": "19 rue Richomme, 75018 Paris",
}

YOMBAL_KEUR_PROGRAM = {
    "name": "YOMBAL KEUR",
    "tagline": "Une cité entièrement dédiée à la diaspora",
    "intro": (
        "Le Groupe YOMBAL et Univers Diaspora proposent des terrains à céder au Sénégal, "
        "avec paiement échelonné sans apport initial, pour construire votre projet à distance."
    ),
}

YOMBAL_KEUR_TERRAINS = (
    {
        "slug": "yenne-ndoukhoura",
        "location": "Yenne Ndoukhoura Peulh",
        "country": "Sénégal",
        "headline": "Opportunité à Yenne Ndoukhoura Peulh",
        "poster": "img/immobilier/yenne-ndoukhoura.png",
        "cover": "img/immobilier/gemini-terrain.png",
        "cover_alt": "Vue du terrain à Yenne Ndoukhoura Peulh — programme YOMBAL KEUR",
        "surface_m2": 150,
        "price_euros": 4776,
        "initial_deposit_euros": 0,
        "monthly_payment_euros": 199,
        "duration_months": 24,
        "legal_nature": "Acte Administratif",
        "highlights": (),
        "services": (
            "Visite de site",
            "Élaboration d'un protocole d'accord",
            "Représentant légal pour régularisation",
        ),
    },
    {
        "slug": "sangalcam",
        "location": "Sangalcam",
        "country": "Sénégal",
        "headline": "Grande opportunité à Sangalcam",
        "poster": "img/immobilier/sangalcam.png",
        "cover": "img/immobilier/gemini-chantier-btp.png",
        "cover_alt": "Chantier et terrain à Sangalcam — programme YOMBAL KEUR",
        "surface_m2": 150,
        "price_euros": 19000,
        "initial_deposit_euros": 0,
        "monthly_payment_euros": 395.84,
        "duration_months": 48,
        "legal_nature": "Titre Foncier",
        "highlights": (
            "5 min de la Route Nationale",
            "Autorisation de lotir",
            "Certificat de conformité",
        ),
        "services": (
            "Visite de site",
            "Élaboration d'un protocole d'accord",
            "Représentant légal pour régularisation",
        ),
    },
    {
        "slug": "ndayane",
        "location": "Ndayane",
        "country": "Sénégal",
        "headline": "Grande opportunité à Ndayane",
        "poster": "img/immobilier/ndayane.png",
        "cover": "img/immobilier/gemini-terrain.png",
        "cover_alt": "Vue du terrain à Ndayane — programme YOMBAL KEUR",
        "surface_m2": 150,
        "price_euros": 11960,
        "initial_deposit_euros": 0,
        "monthly_payment_euros": 299,
        "duration_months": 40,
        "legal_nature": "Notification de Bail",
        "highlights": (),
        "services": (
            "Visite de site",
            "Élaboration d'un protocole d'accord",
            "Représentant légal pour régularisation",
        ),
    },
)

BTP_GALLERY = (
    {
        "src": "img/immobilier/gemini-terrain.png",
        "alt": "Terrain — programme YOMBAL KEUR",
    },
    {
        "src": "img/immobilier/gemini-chantier-btp.png",
        "alt": "Chantier BTP — construction en cours",
    },
)


def _format_eur(amount: float) -> str:
    if float(amount).is_integer():
        whole = f"{int(amount):,}".replace(",", "\u00a0")
        return f"{whole}\u00a0€"
    whole, frac = f"{amount:.2f}".split(".")
    whole = f"{int(whole):,}".replace(",", "\u00a0")
    return f"{whole},{frac}\u00a0€"


def enriched_terrains() -> list[dict]:
    cards = []
    for terrain in YOMBAL_KEUR_TERRAINS:
        cards.append(
            {
                **terrain,
                "price_label": _format_eur(terrain["price_euros"]),
                "monthly_label": _format_eur(terrain["monthly_payment_euros"]),
                "deposit_label": _format_eur(terrain["initial_deposit_euros"]),
            }
        )
    return cards
