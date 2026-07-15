# -*- coding: utf-8 -*-
"""Normalisation DATABASE_URL (Render PostgreSQL)."""

from __future__ import annotations

import logging
import os
from urllib.parse import parse_qs, quote, urlparse, urlencode, urlunparse

logger = logging.getLogger(__name__)


def _is_render_postgres_host(host: str) -> bool:
    host = (host or "").strip().lower()
    return host.startswith("dpg-") and (
        host.endswith("-a") or host.endswith("-postgres.render.com")
    )


def _needs_host_expansion(host: str) -> bool:
    host = (host or "").strip()
    return host.startswith("dpg-") and host.endswith("-a") and "." not in host


def _rebuild_netloc(parsed, hostname: str) -> str:
    auth = ""
    if parsed.username:
        user = quote(parsed.username, safe="")
        if parsed.password is not None:
            auth = f"{user}:{quote(parsed.password, safe='')}"
        else:
            auth = user
    hostpart = hostname if not parsed.port else f"{hostname}:{parsed.port}"
    return f"{auth}@{hostpart}" if auth else hostpart


def _ensure_sslmode(url: str, mode: str = "require") -> str:
    parsed = urlparse(url)
    host = (parsed.hostname or "").strip()
    if not _is_render_postgres_host(host) or "." not in host:
        return url
    qs = parse_qs(parsed.query, keep_blank_values=True)
    if "sslmode" in qs:
        return url
    qs["sslmode"] = [mode]
    return urlunparse(parsed._replace(query=urlencode(qs, doseq=True)))


def normalize_database_url(url: str) -> str:
    """Corrige postgres://, hostname Render incomplet et SSL externe."""
    url = (url or "").strip()
    if not url:
        return ""

    override = (
        os.environ.get("DATABASE_EXTERNAL_URL")
        or os.environ.get("EXTERNAL_DATABASE_URL")
        or ""
    ).strip()
    if override:
        url = override

    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)

    if not url.startswith("postgresql://"):
        return url

    parsed = urlparse(url)
    host = (parsed.hostname or "").strip()

    if _needs_host_expansion(host):
        region = (os.environ.get("RENDER_REGION") or "frankfurt").strip().lower()
        new_host = f"{host}.{region}-postgres.render.com"
        url = urlunparse(parsed._replace(netloc=_rebuild_netloc(parsed, new_host)))
        logger.warning(
            "DATABASE_URL : hostname Render interne %s — utilisation de %s (SSL requis)",
            host,
            new_host,
        )

    return _ensure_sslmode(url)
