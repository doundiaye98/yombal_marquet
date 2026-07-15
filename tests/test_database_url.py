# -*- coding: utf-8 -*-
"""Tests normalisation DATABASE_URL Render."""

from services.database_url import normalize_database_url


def test_postgres_scheme_normalized():
    url = "postgres://user:pass@localhost/db"
    assert normalize_database_url(url).startswith("postgresql://")


def test_render_internal_host_expanded_with_ssl(monkeypatch):
    monkeypatch.delenv("DATABASE_EXTERNAL_URL", raising=False)
    monkeypatch.setenv("RENDER_REGION", "frankfurt")
    url = "postgresql://u:p@dpg-d8nrk3pkh4rs73fgs440-a/yombal"
    fixed = normalize_database_url(url)
    assert "dpg-d8nrk3pkh4rs73fgs440-a.frankfurt-postgres.render.com" in fixed
    assert "sslmode=require" in fixed


def test_external_override_gets_ssl(monkeypatch):
    monkeypatch.setenv(
        "DATABASE_EXTERNAL_URL",
        "postgresql://u:p@dpg-abc-a.frankfurt-postgres.render.com/yombal",
    )
    url = "postgresql://u:p@dpg-abc-a/yombal"
    fixed = normalize_database_url(url)
    assert "frankfurt-postgres.render.com" in fixed
    assert "sslmode=require" in fixed


def test_full_host_adds_sslmode():
    url = "postgresql://u:p@dpg-abc-a.frankfurt-postgres.render.com/yombal"
    fixed = normalize_database_url(url)
    assert "sslmode=require" in fixed
