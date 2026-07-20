# -*- coding: utf-8 -*-
"""Tests champs prénom / nom des formulaires contact."""

from services.contact_form import parse_person_name


def test_parse_person_name_from_fields():
    first, last, full, errors = parse_person_name(
        {"first_name": "Fatou", "last_name": "Ndiaye"}
    )
    assert errors == []
    assert first == "Fatou"
    assert last == "Ndiaye"
    assert full == "Fatou Ndiaye"


def test_parse_person_name_legacy_single_field():
    first, last, full, errors = parse_person_name({"name": "Amadou Diop"})
    assert errors == []
    assert first == "Amadou"
    assert last == "Diop"
    assert full == "Amadou Diop"


def test_parse_person_name_validation():
    _, _, _, errors = parse_person_name({"first_name": "A", "last_name": ""})
    assert len(errors) == 2
