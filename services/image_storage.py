# -*- coding: utf-8 -*-
"""Stockage images produits : disque local ou Cloudinary (persistant sur Render)."""

from __future__ import annotations

import os
import re

from services import product_upload as upload_svc

_IMAGE_URL_PREFIXES = ("http://", "https://")


def cloudinary_enabled() -> bool:
    return bool(
        (os.environ.get("CLOUDINARY_CLOUD_NAME") or "").strip()
        and (os.environ.get("CLOUDINARY_API_KEY") or "").strip()
        and (os.environ.get("CLOUDINARY_API_SECRET") or "").strip()
    )


def _cloudinary_folder() -> str:
    return (os.environ.get("CLOUDINARY_FOLDER") or "yombal/products").strip().strip("/")


def _configure_cloudinary():
    import cloudinary

    cloudinary.config(
        cloud_name=os.environ["CLOUDINARY_CLOUD_NAME"].strip(),
        api_key=os.environ["CLOUDINARY_API_KEY"].strip(),
        api_secret=os.environ["CLOUDINARY_API_SECRET"].strip(),
        secure=True,
    )


def _cloudinary_public_id(slug: str, suffix: str = "") -> str:
    safe = re.sub(r"[^a-z0-9-]", "", (slug or "").lower())
    suffix = re.sub(r"[^a-z0-9-]", "", (suffix or "").lower())
    base = f"{_cloudinary_folder()}/{safe}{suffix}"
    return base


def save_product_image(file_storage, slug: str, static_folder: str, *, filename_suffix: str = ""):
    """Retourne (chemin_ou_url, erreur)."""
    if cloudinary_enabled():
        return _save_cloudinary(file_storage, slug, filename_suffix=filename_suffix)
    return upload_svc.save_product_image(
        file_storage, slug, static_folder, filename_suffix=filename_suffix
    )


def _save_cloudinary(file_storage, slug: str, *, filename_suffix: str = ""):
    if not file_storage or not file_storage.filename:
        return None, None

    ext = upload_svc._extension(file_storage.filename)
    if ext not in upload_svc.ALLOWED_IMAGE_EXTENSIONS:
        return None, "Format non autorisé — utilisez JPG, PNG, WebP ou GIF."

    file_storage.stream.seek(0, os.SEEK_END)
    size = file_storage.stream.tell()
    file_storage.stream.seek(0)
    if size > upload_svc.MAX_IMAGE_BYTES:
        return None, "Image trop lourde (maximum 5 Mo)."

    try:
        _configure_cloudinary()
        import cloudinary.uploader

        result = cloudinary.uploader.upload(
            file_storage,
            public_id=_cloudinary_public_id(slug, filename_suffix),
            overwrite=True,
            resource_type="image",
        )
        return result.get("secure_url"), None
    except Exception as exc:
        return None, f"Échec upload Cloudinary : {exc}"


def remove_product_image(path_or_url: str | None, static_folder: str) -> None:
    if not path_or_url:
        return
    if path_or_url.startswith(_IMAGE_URL_PREFIXES) and "res.cloudinary.com" in path_or_url:
        if not cloudinary_enabled():
            return
        try:
            _configure_cloudinary()
            import cloudinary.uploader

            # public_id avec dossier : yombal/products/slug-g1
            marker = "/upload/"
            if marker in path_or_url:
                tail = path_or_url.split(marker, 1)[1]
                # v1234567890/yombal/products/foo.jpg → prendre après version
                parts = tail.split("/", 1)
                public_id = parts[1] if len(parts) == 2 and parts[0].startswith("v") else tail
                public_id = public_id.rsplit(".", 1)[0]
                cloudinary.uploader.destroy(public_id, resource_type="image")
        except Exception:
            pass
        return
    if not path_or_url.startswith(_IMAGE_URL_PREFIXES):
        upload_svc.remove_product_image_file(static_folder, path_or_url)


def image_display_url(path_or_url: str | None) -> str | None:
    """URL absolue ou chemin relatif static/ pour les templates."""
    if not path_or_url:
        return None
    if path_or_url.startswith(_IMAGE_URL_PREFIXES):
        return path_or_url
    return path_or_url.replace("\\", "/")


def is_remote_url(path_or_url: str | None) -> bool:
    return bool(path_or_url and path_or_url.startswith(_IMAGE_URL_PREFIXES))
