# -*- coding: utf-8 -*-
"""Normalisation DATABASE_URL (Render PostgreSQL)."""

from __future__ import annotations

import logging
import os
from urllib.parse import quote, urlparse, urlunparse

logger = logging.getLogger(__name__)


def normalize_database_url(url: str) -> str:
    """Corrige postgres:// → postgresql:// et hostname Render incomplet."""
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
    if not host.startswith("dpg-") or not host.endswith("-a") or "." in host:
        return url

    region = (os.environ.get("RENDER_REGION") or "frankfurt").strip().lower()
    new_host = f"{host}.{region}-postgres.render.com"

    auth = ""
    if parsed.username:
        user = quote(parsed.username, safe="")
        if parsed.password is not None:
            auth = f"{user}:{quote(parsed.password, safe='')}"
        else:
            auth = user

    hostpart = new_host if not parsed.port else f"{new_host}:{parsed.port}"
    netloc = f"{auth}@{hostpart}" if auth else hostpart
    fixed = urlunparse(parsed._replace(netloc=netloc))

    logger.warning(
        "DATABASE_URL : hostname Render interne %s non résolu — utilisation de %s",
        host,
        new_host,
    )
    return fixed
