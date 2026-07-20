# -*- coding: utf-8 -*-
"""Champs prénom / nom des formulaires de contact."""

from __future__ import annotations


def parse_person_name(form: dict) -> tuple[str, str, str, list[str]]:
    """Retourne (prénom, nom, nom complet, erreurs)."""
    errors: list[str] = []
    first_name = (form.get("first_name") or "").strip()
    last_name = (form.get("last_name") or "").strip()

    if not first_name and not last_name:
        legacy = (form.get("name") or "").strip()
        if legacy:
            parts = legacy.split(None, 1)
            first_name = parts[0]
            last_name = parts[1] if len(parts) > 1 else ""

    if len(first_name) < 2:
        errors.append("Indiquez votre prénom.")
    if len(last_name) < 2:
        errors.append("Indiquez votre nom.")

    full_name = f"{first_name} {last_name}".strip()
    return first_name, last_name, full_name, errors
