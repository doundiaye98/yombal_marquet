# -*- coding: utf-8 -*-
"""Chemins des photos produits (static/img/products/)."""

import os
import shutil

from extensions import db
from models.product import Product

# slug → chemin relatif sous static/
PRODUCT_IMAGES = {
    # Catalogue initial
    "couscous-complet-1kg": "img/products/couscous-complet-1kg.png",
    "huile-argan-bio-100ml": "img/products/huile-argan-bio-100ml.jpg",
    "miel-thym-500g": "img/products/miel-thym-500g.jpg",
    "cafe-arabica-250g": "img/products/cafe-arabica-250g.jpg",
    "savon-noir-eucalyptus": "img/products/savon-noir-eucalyptus.jpg",
    "dates-medjool-400g": "img/products/dates-medjool-400g.jpg",
    "bissap-concentre-50cl": "img/products/bissap-concentre-50cl.jpg",
    "beurre-karite-brut-150g": "img/products/beurre-karite-brut-150g.jpg",
    "huile-palme-artisanale-1l": "img/products/huile-palme-artisanale-1l.jpg",
    # Extension sénégalaise — nouvelles photos
    "bissap-seche-200g": "img/products/bissap-seche-200g.jpg",
    "gingembre-poudre-100g": "img/products/gingembre-poudre-100g.jpg",
    "bouye-baobab-250g": "img/products/bouye-baobab-250g.jpg",
    "ditakh-300g": "img/products/ditakh-300g.jpg",
    "kinkeliba-80g": "img/products/kinkeliba-80g.jpg",
    "cafe-touba-250g": "img/products/cafe-touba-250g.jpg",
    "tamarin-pulpe-200g": "img/products/tamarin-pulpe-200g.jpg",
    "riz-brise-local-1kg": "img/products/riz-brise-local-1kg.jpg",
    "mil-millet-1kg": "img/products/mil-millet-1kg.jpg",
    "sorgho-1kg": "img/products/sorgho-1kg.jpg",
    "fonio-500g": "img/products/fonio-500g.jpg",
    "farine-niebe-500g": "img/products/farine-niebe-500g.jpg",
    "soumbala-100g": "img/products/soumbala-100g.jpg",
    "netetou-100g": "img/products/netetou-100g.jpg",
    "yett-coquillages-150g": "img/products/yett-coquillages-150g.jpg",
    "piment-sec-moulu-80g": "img/products/piment-sec-moulu-80g.jpg",
    "sel-kaolack-500g": "img/products/sel-kaolack-500g.jpg",
    "beurre-karite-alimentaire-250g": "img/products/beurre-karite-alimentaire-250g.jpg",
    "thiakry-400g": "img/products/thiakry-400g.jpg",
    "legumes-seches-thiebou-200g": "img/products/legumes-seches-thiebou-200g.jpg",
    "crevettes-sechees-100g": "img/products/crevettes-sechees-100g.jpg",
    "confiture-bissap-250g": "img/products/confiture-bissap-250g.jpg",
    "graine-sesame-250g": "img/products/graine-sesame-250g.jpg",
    "pastilles-tamarin-150g": "img/products/pastilles-tamarin-150g.jpg",
}

# Seuls ces slugs restent dans le catalogue boutique.
CATALOGUE_SLUGS = frozenset(PRODUCT_IMAGES.keys())

# Fichiers sources dans img/ (racine projet) → slug produit
IMAGE_SOURCES = {
    "BISAP S7CHE.jpg": "bissap-seche-200g",
    "Gijinbre.jpg": "gingembre-poudre-100g",
    "pain de singe.jpg": "bouye-baobab-250g",
    "DITAKH OU DETARIUM SENEGALENSE, UN CLASSIQUE DE LA MÉDECINE TRADITIONNELLE (TROUBLES DE LA DIGESTION, ANÉMIE, BRONCHITES ECT___.jpg": "ditakh-300g",
    "cinquéliba.jpg": "kinkeliba-80g",
    "Cafetera tuba.jpg": "cafe-touba-250g",
    "Tamarin.jpg": "tamarin-pulpe-200g",
    "riz.jpg": "riz-brise-local-1kg",
    "Pearl millet.jpg": "mil-millet-1kg",
    "#Sorgo.jpg": "sorgho-1kg",
    "Superfood Fonio – Glutenfreies Urgetreide aus Afrika _ Reich an Eisen, Magnesium & Calcium.jpg": "fonio-500g",
    "farine.jpg": "farine-niebe-500g",
    "Lost Recipes of Ancient Civilization People Really___.jpg": "soumbala-100g",
    "nétetu.jpg": "netetou-100g",
    "yéte.jpg": "yett-coquillages-150g",
    "pument.jpg": "piment-sec-moulu-80g",
    "Salt.jpg": "sel-kaolack-500g",
    "beure.jpg": "beurre-karite-alimentaire-250g",
    "Thiakry ou dégué.jpg": "thiakry-400g",
    "légume.jpg": "legumes-seches-thiebou-200g",
    "Recette de crevettes marinées délicatement.jpg": "crevettes-sechees-100g",
    "Sour Cherry and Chili Jam_ A sweet and spicy jam perfect for pairing with cheese or meat_.jpg": "confiture-bissap-250g",
    "😉 SEMILLAS DE LINO - 👉 Beneficios y Propiedades.jpg": "graine-sesame-250g",
    "téléchargement (5).jpg": "pastilles-tamarin-150g",
}


def install_product_images(app_root: str) -> int:
    """Copie img/ → static/img/products/ selon IMAGE_SOURCES. Retourne le nombre de fichiers copiés."""
    src_dir = os.path.join(app_root, "img")
    dest_dir = os.path.join(app_root, "static", "img", "products")
    os.makedirs(dest_dir, exist_ok=True)
    copied = 0
    for filename, slug in IMAGE_SOURCES.items():
        src = os.path.join(src_dir, filename)
        if not os.path.isfile(src):
            continue
        rel = PRODUCT_IMAGES.get(slug)
        if not rel:
            continue
        dest = os.path.join(app_root, "static", rel.replace("/", os.sep))
        if not os.path.isfile(dest) or os.path.getmtime(src) > os.path.getmtime(dest):
            shutil.copy2(src, dest)
            copied += 1
    return copied


def sync_product_images(app_root: str | None = None):
    """Copie les fichiers puis associe les photos aux produits (idempotent)."""
    from sqlalchemy import inspect

    if app_root:
        install_product_images(app_root)

    if not inspect(db.engine).has_table("products"):
        return
    cols = {c["name"] for c in inspect(db.engine).get_columns("products")}
    if "image" not in cols:
        return
    changed = False
    for slug, path in PRODUCT_IMAGES.items():
        product = Product.query.filter_by(slug=slug).first()
        if product and product.image != path:
            product.image = path
            changed = True
    if changed:
        db.session.commit()


def purge_products_without_images():
    """Supprime les produits sans photo (désactive s'ils sont liés à une commande)."""
    from sqlalchemy import or_

    from models.order import OrderItem

    if not Product.query.first():
        return
    changed = False
    for product in Product.query.filter(
        or_(Product.image.is_(None), Product.image == "", ~Product.slug.in_(CATALOGUE_SLUGS))
    ).all():
        has_orders = OrderItem.query.filter_by(product_id=product.id).first() is not None
        if has_orders:
            if product.is_active:
                product.is_active = False
                changed = True
        else:
            db.session.delete(product)
            changed = True
    if changed:
        db.session.commit()
