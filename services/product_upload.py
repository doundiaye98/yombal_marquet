# -*- coding: utf-8 -*-
"""Upload et suppression des photos produits (admin)."""

import os
import re

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
MAX_IMAGE_BYTES = 5 * 1024 * 1024


def _extension(filename: str) -> str:
    return os.path.splitext(filename or "")[1].lower()


def _safe_slug(slug: str) -> str:
    return re.sub(r"[^a-z0-9-]", "", (slug or "").lower())


def save_product_image(
    file_storage,
    slug: str,
    static_folder: str,
    *,
    filename_suffix: str = "",
) -> tuple[str | None, str | None]:
    """Enregistre l'image sous static/img/products/{slug}{suffix}.ext."""
    if not file_storage or not file_storage.filename:
        return None, None

    ext = _extension(file_storage.filename)
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        return None, "Format non autorisé — utilisez JPG, PNG, WebP ou GIF."

    file_storage.stream.seek(0, os.SEEK_END)
    size = file_storage.stream.tell()
    file_storage.stream.seek(0)
    if size > MAX_IMAGE_BYTES:
        return None, "Image trop lourde (maximum 5 Mo)."

    safe = _safe_slug(slug)
    if not safe:
        return None, "Slug invalide pour enregistrer l'image."

    rel_dir = os.path.join("img", "products")
    dest_dir = os.path.join(static_folder, rel_dir)
    os.makedirs(dest_dir, exist_ok=True)

    suffix = re.sub(r"[^a-z0-9-]", "", (filename_suffix or "").lower())
    rel_path = f"{rel_dir}/{safe}{suffix}{ext}".replace("\\", "/")
    abs_path = os.path.join(static_folder, rel_path)
    file_storage.save(abs_path)
    return rel_path, None


def remove_product_image_file(static_folder: str, rel_path: str | None) -> None:
    if not rel_path:
        return
    abs_path = os.path.join(static_folder, rel_path.replace("/", os.sep))
    if os.path.isfile(abs_path):
        try:
            os.remove(abs_path)
        except OSError:
            pass
