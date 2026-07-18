# -*- coding: utf-8 -*-
"""Chemins des photos produits (static/img/products/)."""

import os
import shutil

from extensions import db
from models.catalogue_retired import RETIRED_IMAGE_MIGRATION, RETIRED_PRODUCT_SLUGS
from models.product import Product

# slug → chemin relatif sous static/
_RAW_PRODUCT_IMAGES = {
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
    # LabelAfrik — poisson, fruits de mer, moringa (sources img/)
    "moringa-feuilles-poudre-100g": "img/products/moringa-feuilles-poudre-100g.jpg",
    "barracuda-seud-10kg": "img/products/barracuda-seud-10kg.jpg",
    "barracuda-seud-5kg": "img/products/barracuda-seud-5kg.jpg",
    "capitaine-bar-600-800-10kg": "img/products/capitaine-bar-600-800-10kg.jpg",
    "capitaine-bar-400-600-5kg": "img/products/capitaine-bar-400-600-5kg.jpg",
    "crabe-mangrove": "img/products/crabe-mangrove.jpg",
    "crevettes-crues-decortiquees": "img/products/crevettes-crues-decortiquees.jpg",
    "dorade-diaregne-tete-10kg": "img/products/dorade-diaregne-tete-10kg.jpg",
    "dorade-diaregne-tete-5kg": "img/products/dorade-diaregne-tete-5kg.jpg",
    "dorade-diaregne-sans-tete-5kg": "img/products/dorade-diaregne-sans-tete-5kg.jpg",
    "dorade-vivaneau-10kg": "img/products/dorade-vivaneau-10kg.jpg",
    "dorade-500-800-5kg": "img/products/dorade-500-800-5kg.jpg",
    "dorade-400-600-5kg": "img/products/dorade-400-600-5kg.jpg",
    "gros-machoiron": "img/products/gros-machoiron.jpg",
    "gambas-geantes-sauvages": "img/products/gambas-geantes-sauvages.jpg",
    "merou-thiof-entier-5kg": "img/products/merou-thiof-entier-5kg.jpg",
    "merou-thiof-entier-10kg": "img/products/merou-thiof-entier-10kg.jpg",
    "merou-thiof-sans-tete-5kg": "img/products/merou-thiof-sans-tete-5kg.jpg",
    "merou-thiof-sans-tete-10kg": "img/products/merou-thiof-sans-tete-10kg.jpg",
    "petits-merous-thiof": "img/products/petits-merous-thiof.jpg",
    "sole-karabot": "img/products/sole-karabot.jpg",
    "tilapia-moyen-senegal": "img/products/tilapia-moyen-senegal.jpg",
    "queues-langoustes-blanches": "img/products/queues-langoustes-blanches.jpg",
    "sardinelle-yaboye": "img/products/sardinelle-yaboye.jpg",
    "tilapia-gros-xxl-10kg": "img/products/tilapia-gros-xxl-10kg.jpg",
    "ailes-poulet-texmex-halal": "img/products/ailes-poulet-texmex-halal.jpg",
    "chinchard-600-900-10kg": "img/products/chinchard-600-900-10kg.jpg",
    "dorade-1000-plus-5kg": "img/products/dorade-1000-plus-5kg.jpg",
    # Photos produits réelles (épicerie)
    "dakhar-sachet-150g": "img/products/dakhar-sachet-150g.jpg",
    "dakhar-sachet-375g": "img/products/dakhar-sachet-375g.webp",
    "miel-fleurs-500g": "img/products/miel-fleurs-500g.jpg",
    "pate-arachide-labelafrik": "img/products/pate-arachide-labelafrik.jpg",
    "pate-arachide-dakatine": "img/products/pate-arachide-dakatine.jpg",
    "pate-arachide-pcd-500g": "img/products/pate-arachide-pcd-500g.jpg",
}

PRODUCT_IMAGES = dict(_RAW_PRODUCT_IMAGES)
for _old, _new in RETIRED_IMAGE_MIGRATION.items():
    if _old in PRODUCT_IMAGES and _new not in PRODUCT_IMAGES:
        PRODUCT_IMAGES[_new] = PRODUCT_IMAGES[_old]
for _old in RETIRED_PRODUCT_SLUGS:
    PRODUCT_IMAGES.pop(_old, None)

# Photos extraites des captures catalogue Univers Diaspora (prioritaires)
CATALOG_SCREENSHOT_IMAGES = {
    "poudre-lait-nido-400g": "img/products/poudre-lait-nido-400g.jpg",
    "poudre-lait-nido-900g": "img/products/poudre-lait-nido-900g.jpg",
    "poudre-lait-nido-1800g": "img/products/poudre-lait-nido-1800g.jpg",
    "poudre-lait-nido-2500g": "img/products/poudre-lait-nido-2500g.jpg",
    "sauce-trofai-palmier-350": "img/products/sauce-trofai-palmier-350.jpg",
    "sauce-trofai-palmier-410": "img/products/sauce-trofai-palmier-410.jpg",
    "concentre-tomates-rolli": "img/products/concentre-tomates-rolli.jpg",
    "maad-230g": "img/products/maad-230g.jpg",
    "maad-400g": "img/products/maad-400g.jpg",
    "sirop-bissap-ud": "img/products/sirop-bissap-ud.jpg",
    "sirop-gingembre-ud": "img/products/sirop-gingembre-ud.jpg",
    "concentre-tomates-2kg": "img/products/concentre-tomates-2kg.jpg",
    "pate-sardinelle-pinton": "img/products/pate-sardinelle-pinton.jpg",
    "sardinelle-pilchards-tomate": "img/products/sardinelle-pilchards-tomate.jpg",
}
PRODUCT_IMAGES.update(CATALOG_SCREENSHOT_IMAGES)

# Seuls ces slugs restent dans le catalogue boutique (avec photo).
CATALOGUE_SLUGS = frozenset(PRODUCT_IMAGES.keys())

try:
    from models.catalogue_labelafrik import LABELAFRIK_SLUGS
except ImportError:
    LABELAFRIK_SLUGS = frozenset()

# Fichiers sources dans img/ (racine projet) → slug produit
IMAGE_SOURCES = {
    "BISAP S7CHE.jpg": "bissap-seche-200g",
    "Gijinbre.jpg": "gingembre-poudre-100g",
    "pain de singe.jpg": "bouye-baobab-250g",
    "DITAKH OU DETARIUM SENEGALENSE, UN CLASSIQUE DE LA MÉDECINE TRADITIONNELLE (TROUBLES DE LA DIGESTION, ANÉMIE, BRONCHITES ECT___.jpg": "ditakh-300g",
    "cinquéliba.jpg": "kinkeliba-80g",
    "Cafetera tuba.jpg": "cafe-touba-250g",
    "Tamarin.jpg": "tamarin-pulpe-200g",
    "riz.jpg": "riz-casse-1x-1kg",
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
    # Poisson & mer — photos récentes (dossier img/)
    "Poudre de feuilles de moringa — 100 g.jpg": "moringa-feuilles-poudre-100g",
    "Barracuda Seud — carton 10 kg.jpg": "barracuda-seud-10kg",
    "Barracuda_ameliore.jpg": "barracuda-seud-5kg",
    "Capitaine Bar (Ombrine) — carton 10 kg.jpg": "capitaine-bar-600-800-10kg",
    "Capitaine_Bar_Ombrine_5kg_ameliore.jpg": "capitaine-bar-400-600-5kg",
    "Crabe de mangrove — pièce.jpg": "crabe-mangrove",
    "Crevettes crues décortiquées — sachet.jpg": "crevettes-crues-decortiquees",
    "Dorade Diaregne avec tête — carton 10 kg.jpg": "dorade-diaregne-tete-10kg",
    "Dorade Diaregne avec tête — carton 5 kg.jpg": "dorade-diaregne-tete-5kg",
    "Dorade Diaregne sans tête — carton 5 kg.jpg": "dorade-diaregne-sans-tete-5kg",
    "Dorade plate Vivaneau — carton 10 kg.jpg": "dorade-vivaneau-10kg",
    "Dorade 500–800 g — carton 5 kg.jpg": "dorade-500-800-5kg",
    "Dorade.jpg": "dorade-400-600-5kg",
    "Gros machoiron — pièce.jpg": "gros-machoiron",
    "Gambas géantes sauvages — sachet.jpg": "gambas-geantes-sauvages",
    "Mérou Thiof entier — carton 5 kg.jpg": "merou-thiof-entier-5kg",
    "Mérou Thiof entier — carton 10 kg.jpg": "merou-thiof-entier-10kg",
    "Mérou Thiof sans tête — carton 5 kg.jpg": "merou-thiof-sans-tete-5kg",
    "Mérou Thiof sans tête — carton 10 kg.jpg": "merou-thiof-sans-tete-10kg",
    "Petits mérous Thiof — au kg.jpg": "petits-merous-thiof",
    "Grosse sole Karabot — pièce.jpg": "sole-karabot",
    "Tilapia moyen Sénégal — carton.jpg": "tilapia-moyen-senegal",
    "Queues de langoustes blanches — sachet.jpg": "queues-langoustes-blanches",
    "Sardinelle Yaboye — sachet.jpg": "sardinelle-yaboye",
    "Tilapia gros XXL — carton 10 kg.jpg": "tilapia-gros-xxl-10kg",
    "Ailes de poulet Tex-Mex halal — 2.jpg": "ailes-poulet-texmex-halal",
    "Chinchard entier— carton 10 kg.jpg": "chinchard-600-900-10kg",
    "Dorade 1000 g+ — carton 5 kg.jpg": "dorade-1000-plus-5kg",
    "Sauce graine de palme Trofai — 350 g.jpg": "sauce-trofai-palmier-350",
    "Sauce graine de palme Trofai — 410 g.jpg": "sauce-trofai-palmier-410",
    # Épicerie — photos produits réelles
    "Dakhar — 150 g.jpg": "dakhar-sachet-150g",
    "Dakhar — 375 g.webp": "dakhar-sachet-375g",
    "Miel de fleurs — 500 g.jpg": "miel-fleurs-500g",
    "Sirop de bissap — 50 cl.jpg": "sirop-bissap-ud",
    "Sirop de gingembre — 50 cl.jpg": "sirop-gingembre-ud",
    "Pâte d'arachide — 500 g.jpg": "pate-arachide-labelafrik",
    "Pâte d'arachide PCD — 500 g.jpg": "pate-arachide-pcd-500g",
    "âte d'arachide Dakatine.jpg": "pate-arachide-dakatine",
}


_IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".gif")


def discover_image_for_slug(app_root: str | None, slug: str) -> str | None:
    """Cherche static/img/products/{slug}.ext — utile pour Render après déploiement Git."""
    if not app_root or not slug:
        return None
    products_dir = os.path.join(app_root, "static", "img", "products")
    if not os.path.isdir(products_dir):
        return None
    safe = slug.strip().lower()
    for ext in _IMAGE_EXTENSIONS:
        filename = f"{safe}{ext}"
        if os.path.isfile(os.path.join(products_dir, filename)):
            return f"img/products/{filename}"
    return None


def image_file_exists(app_root: str | None, rel_path: str | None) -> bool:
    if not app_root or not rel_path:
        return False
    return os.path.isfile(os.path.join(app_root, "static", rel_path.replace("/", os.sep)))


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

    # 1) Cartographie explicite (catalogue historique)
    for slug, path in PRODUCT_IMAGES.items():
        product = Product.query.filter_by(slug=slug).first()
        if product and product.image != path:
            product.image = path
            changed = True

    # 2) Fichiers déjà présents dans static/img/products/ (LabelAfrik, uploads commités Git)
    for product in Product.query.all():
        current = (product.image or "").strip()
        if current and image_file_exists(app_root, current):
            continue
        discovered = discover_image_for_slug(app_root, product.slug)
        if discovered and product.image != discovered:
            product.image = discovered
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
    keep_slugs = CATALOGUE_SLUGS | LABELAFRIK_SLUGS
    for product in Product.query.filter(
        or_(Product.image.is_(None), Product.image == "")
    ).filter(~Product.slug.in_(keep_slugs)).all():
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
