# -*- coding: utf-8 -*-
"""Demandes simples — services écosystème (hors immobilier dédié)."""

from __future__ import annotations

from services import ecosystem_nav as nav_svc
from services.contact_form import parse_person_name

FORM_PAGE_SLUGS = frozenset({
    "investissement",
    "transport",
    "restaurant",
    "coiffure",
    "electronique",
    "electromenager",
    "mode",
    "chaussures",
    "bagagerie",
    "autres-services",
})

TOPIC_CHOICES = {
    "investissement": "Investissement",
    "transport": "Yombal Transports",
    "restaurant": "Restaurant & traiteur",
    "coiffure": "Coiffure & beauté",
    "electronique": "Électronique",
    "electromenager": "Électroménager",
    "mode": "Habillement",
    "chaussures": "Chaussures",
    "bagagerie": "Sacs & bagagerie",
    "boutique": "Boutique en ligne",
    "autre": "Autre demande",
}

TRANSPORT_TOPIC_CHOICES = {
    "achat_vehicule": "Achats véhicules",
    "vente_vehicule": "Vente véhicules",
    "location_voiture": "Location voiture",
    "demenagement": "Déménagement pro",
    "envoi_colis": "Envoi de colis",
}


def service_label(slug: str) -> str | None:
    service = nav_svc.get_ecosystem_service(slug)
    if not service:
        return None
    return service["title"]


def topic_choices() -> list[tuple[str, str]]:
    return list(TOPIC_CHOICES.items())


def transport_topic_choices() -> list[tuple[str, str]]:
    return list(TRANSPORT_TOPIC_CHOICES.items())


def validate_form(form: dict, page_slug: str) -> tuple[dict | None, list[str]]:
    errors: list[str] = []
    if page_slug not in FORM_PAGE_SLUGS:
        return None, ["Service invalide."]

    first_name, last_name, name, name_errors = parse_person_name(form)
    email = (form.get("email") or "").strip().lower()
    phone = (form.get("phone") or "").strip()
    message = (form.get("message") or "").strip()
    consent = form.get("consent") == "1"
    topic_slug = (form.get("topic_slug") or "").strip()

    if page_slug == "autres-services":
        if topic_slug not in TOPIC_CHOICES:
            errors.append("Choisissez le service concerné.")
        service_slug = topic_slug if topic_slug != "autre" else "autres-services"
        topic_label = TOPIC_CHOICES[topic_slug]
    elif page_slug == "transport":
        if topic_slug not in TRANSPORT_TOPIC_CHOICES:
            errors.append("Choisissez le type de demande.")
        service_slug = page_slug
        topic_label = (
            f"{service_label(page_slug)} — {TRANSPORT_TOPIC_CHOICES[topic_slug]}"
            if topic_slug in TRANSPORT_TOPIC_CHOICES
            else service_label(page_slug) or page_slug
        )
    else:
        service_slug = page_slug
        topic_slug = page_slug
        topic_label = service_label(page_slug) or page_slug

    if name_errors:
        errors.extend(name_errors)
    if not email or "@" not in email:
        errors.append("Indiquez une adresse e-mail valide.")
    if len(phone) < 8:
        errors.append("Indiquez un numéro de téléphone joignable.")
    if len(message) < 10:
        errors.append("Décrivez votre demande (au moins 10 caractères).")
    if not consent:
        errors.append("Veuillez accepter le traitement de vos données.")

    if errors:
        return None, errors

    return {
        "first_name": first_name,
        "last_name": last_name,
        "name": name,
        "email": email,
        "phone": phone,
        "message": message,
        "page_slug": page_slug,
        "service_slug": service_slug,
        "service_label": service_label(service_slug) or topic_label,
        "topic_slug": topic_slug,
        "topic_label": topic_label,
    }, []


def build_subject(data: dict) -> str:
    return f"[Yombal {data['topic_label']}] {data['name']}"


def build_message_body(data: dict) -> str:
    lines = [
        f"=== Demande — {data['topic_label']} ===",
        "",
        f"Prénom : {data['first_name']}",
        f"Nom : {data['last_name']}",
        f"E-mail : {data['email']}",
        f"Téléphone : {data['phone']}",
        f"Service : {data['topic_label']}",
        "",
        "--- Message ---",
        data["message"],
    ]
    return "\n".join(lines)
