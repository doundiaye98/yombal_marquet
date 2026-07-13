# -*- coding: utf-8 -*-
"""Demandes de projet immobilier & BTP — YOMBAL KEUR."""

from __future__ import annotations

from services import immobilier_programmes as immo_svc

PROJECT_TYPES = {
    "achat_terrain": "Achat de terrain (YOMBAL KEUR)",
    "terrain_et_construction": "Terrain + construction (BTP)",
    "btp_seul": "Construction / rénovation (j'ai déjà un terrain)",
    "renseignement": "Demande d'information",
}

TERRAIN_CHOICES = {t["slug"]: t for t in immo_svc.YOMBAL_KEUR_TERRAINS}


def terrain_by_slug(slug: str | None) -> dict | None:
    if not slug:
        return None
    return TERRAIN_CHOICES.get(slug)


def validate_form(form: dict) -> tuple[dict | None, list[str]]:
    errors: list[str] = []
    name = (form.get("name") or "").strip()
    email = (form.get("email") or "").strip().lower()
    phone = (form.get("phone") or "").strip()
    country = (form.get("country") or "").strip()
    project_type = (form.get("project_type") or "").strip()
    terrain_slug = (form.get("terrain_slug") or "").strip() or None
    message = (form.get("message") or "").strip()
    consent = form.get("consent") == "1"

    if len(name) < 2:
        errors.append("Indiquez votre nom complet.")
    if not email or "@" not in email:
        errors.append("Indiquez une adresse e-mail valide.")
    if len(phone) < 8:
        errors.append("Indiquez un numéro de téléphone joignable.")
    if len(country) < 2:
        errors.append("Indiquez votre pays de résidence.")
    if project_type not in PROJECT_TYPES:
        errors.append("Choisissez le type de projet.")
    if terrain_slug and terrain_slug not in TERRAIN_CHOICES:
        errors.append("Terrain sélectionné invalide.")
    if message and len(message) < 10:
        errors.append("Le message doit contenir au moins 10 caractères.")
    if not consent:
        errors.append("Veuillez accepter le traitement de vos données.")

    if errors:
        return None, errors

    terrain = terrain_by_slug(terrain_slug)
    return {
        "name": name,
        "email": email,
        "phone": phone,
        "country": country,
        "project_type": project_type,
        "project_type_label": PROJECT_TYPES[project_type],
        "terrain_slug": terrain_slug,
        "terrain_label": terrain["location"] if terrain else None,
        "message": message,
    }, []


def build_subject(data: dict) -> str:
    terrain_part = data["terrain_label"] or "Projet immobilier"
    return f"[YOMBAL KEUR] {terrain_part} — {data['name']}"


def build_message_body(data: dict) -> str:
    lines = [
        "=== Demande de projet — YOMBAL KEUR ===",
        "",
        f"Nom : {data['name']}",
        f"E-mail : {data['email']}",
        f"Téléphone : {data['phone']}",
        f"Pays de résidence : {data['country']}",
        f"Type de projet : {data['project_type_label']}",
    ]
    if data["terrain_label"]:
        lines.append(f"Terrain visé : {data['terrain_label']}")
    lines.extend(["", "--- Message ---", data["message"] or "(aucun message complémentaire)"])
    return "\n".join(lines)
