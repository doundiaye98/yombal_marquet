# -*- coding: utf-8 -*-
"""Agences Univers Diaspora — page Contact (affiche officielle)."""

from __future__ import annotations

from urllib.parse import quote

# E-mail affiché sur l'affiche agences
AGENCIES_EMAIL = "contact@universdiaspora.com"

AGENCIES = (
    {
        "id": "paris-18",
        "label": "Paris 18ᵉ",
        "title": "Agence Paris 18ᵉ",
        "address_line1": "19 Rue Richomme",
        "address_line2": "75018 Paris",
        "phone_fixe": "09 70 70 70 59",
        "phone_mobile": "06 31 27 33 76",
        "transit": (
            {"mode": "Métro", "lines": "4", "stops": "Château Rouge"},
            {"mode": "Métro", "lines": "4 · 12", "stops": "Marcadet – Poissonniers"},
            {"mode": "Métro", "lines": "2 · 4", "stops": "Barbès – Rochechouart"},
            {"mode": "Métro", "lines": "2", "stops": "La Chapelle"},
        ),
        "map_query": "19 Rue Richomme, 75018 Paris, France",
        "lat": 48.8906,
        "lon": 2.3495,
    },
    {
        "id": "paris-17",
        "label": "Paris 17ᵉ",
        "title": "Agence Paris 17ᵉ",
        "address_line1": "75 Rue des Moines",
        "address_line2": "75017 Paris",
        "phone_fixe": "01 42 29 41 44",
        "phone_mobile": "06 59 40 89 56",
        "transit": (
            {"mode": "Métro", "lines": "13", "stops": "Brochant · Guy Môquet · La Fourche"},
            {"mode": "Métro", "lines": "14", "stops": "Pont Cardinet"},
        ),
        "map_query": "75 Rue des Moines, 75017 Paris, France",
        "lat": 48.8902,
        "lon": 2.3205,
    },
    {
        "id": "colombes",
        "label": "Colombes",
        "title": "Agence Colombes",
        "address_line1": "21 Rue M. Berteaux",
        "address_line2": "92700 Colombes",
        "phone_fixe": None,
        "phone_mobile": None,
        "transit": (
            {"mode": "Transilien", "lines": "J", "stops": "Gare de Colombes"},
            {"mode": "Métro", "lines": "13", "stops": "Les Agnettes"},
            {"mode": "Bus", "lines": "140 · 235 · 276 · 340 · 366", "stops": "Arrêts à proximité"},
        ),
        "map_query": "21 Rue Maurice Berteaux, 92700 Colombes, France",
        "lat": 48.9224,
        "lon": 2.2531,
    },
)


def agencies_for_contact() -> list[dict]:
    """Enrichit les agences avec URLs carte / itinéraire."""
    out = []
    for a in AGENCIES:
        q = a["map_query"]
        enc = quote(q)
        item = dict(a)
        item["maps_embed"] = f"https://maps.google.com/maps?q={enc}&z=16&output=embed"
        item["maps_link"] = f"https://www.google.com/maps/search/?api=1&query={enc}"
        item["phone_fixe_href"] = (
            f"tel:+33{a['phone_fixe'].replace(' ', '')[1:]}" if a.get("phone_fixe") else None
        )
        item["phone_mobile_href"] = (
            f"tel:+33{a['phone_mobile'].replace(' ', '')[1:]}" if a.get("phone_mobile") else None
        )
        out.append(item)
    return out
