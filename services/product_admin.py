# -*- coding: utf-8 -*-
"""Actions admin sur les produits."""

import json

from extensions import db
from models.order import OrderItem
from models.site_setting import SiteSetting
from services.product_upload import remove_product_image_file

ADMIN_REMOVED_KEY = "admin_removed_slugs"


def admin_removed_slugs() -> frozenset[str]:
    row = db.session.get(SiteSetting, ADMIN_REMOVED_KEY)
    if not row or not row.value:
        return frozenset()
    try:
        data = json.loads(row.value)
        if isinstance(data, list):
            return frozenset(str(s) for s in data if s)
    except (json.JSONDecodeError, TypeError):
        pass
    return frozenset()


def mark_slug_admin_removed(slug: str) -> None:
    if not slug:
        return
    slugs = set(admin_removed_slugs())
    slugs.add(slug)
    row = db.session.get(SiteSetting, ADMIN_REMOVED_KEY)
    payload = json.dumps(sorted(slugs))
    if row:
        row.value = payload
    else:
        db.session.add(SiteSetting(key=ADMIN_REMOVED_KEY, value=payload))


def delete_product(product, static_folder: str) -> tuple[str, str]:
    """
    Supprime un produit ou le désactive s'il figure dans une commande.
    Retourne (niveau_flash, message).
    """
    has_orders = (
        OrderItem.query.filter_by(product_id=product.id).first() is not None
    )
    if has_orders:
        product.is_active = False
        return (
            "warning",
            f"« {product.name} » a déjà été commandé : il a été désactivé "
            "(retrait de la boutique) mais conservé dans l'historique.",
        )

    slug = product.slug
    name = product.name
    if product.image:
        remove_product_image_file(static_folder, product.image)
    for row in list(product.gallery_images or []):
        remove_product_image_file(static_folder, row.image)
    mark_slug_admin_removed(slug)
    db.session.delete(product)
    return ("success", f"« {name} » a été supprimé définitivement.")
