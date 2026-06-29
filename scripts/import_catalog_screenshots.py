# -*- coding: utf-8 -*-
"""Découpe les captures catalogue Univers Diaspora et assigne les photos produits."""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ASSETS = os.environ.get(
    "CURSOR_ASSETS",
    os.path.normpath(
        os.path.join(
            ROOT,
            "..",
            "..",
            "..",
            "Users",
            "group",
            ".cursor",
            "projects",
            "c-wamp64-www-yombal-marquet",
            "assets",
        )
    ),
)
if not os.path.isdir(ASSETS):
    ASSETS = os.path.join(ROOT, "img", "catalog")

sys.path.insert(0, ROOT)

# fragment du nom de fichier → [(slug, row, col), ...]  grille 2×2
CATALOG_CROPS = {
    "153519": [
        ("poudre-lait-nido-400g", 0, 0),
        ("poudre-lait-nido-900g", 0, 1),
        ("poudre-lait-nido-1800g", 1, 0),
        ("poudre-lait-nido-2500g", 1, 1),
    ],
    "153536": [
        ("lait-concentre-bonnet-rouge", 0, 0),
        ("sauce-trofai-palmier-350", 0, 1),
        ("sauce-trofai-palmier-410", 1, 0),
        ("concentre-tomates-rolli", 1, 1),
    ],
    "153611": [
        ("maad-230g", 0, 0),
        ("maad-400g", 0, 1),
        ("sirop-bissap-ud", 1, 0),
        ("sirop-gingembre-ud", 1, 1),
    ],
    "153558": [
        ("concentre-tomates-2kg", 0, 1),
        ("pate-sardinelle-pinton", 1, 0),
        ("sardinelle-pilchards-tomate", 1, 1),
    ],
}


def _find_screenshot(fragment: str) -> str | None:
    if not os.path.isdir(ASSETS):
        return None
    for name in os.listdir(ASSETS):
        if fragment in name and name.lower().endswith(".png"):
            return os.path.join(ASSETS, name)
    return None


def _crop_product(img, row: int, col: int):
    w, h = img.size
    top = int(h * 0.17)
    body_h = h - top
    cell_w = w // 2
    cell_h = body_h // 2
    x0 = col * cell_w + int(cell_w * 0.02)
    y0 = top + row * cell_h + int(cell_h * 0.05)
    x1 = (col + 1) * cell_w - int(cell_w * 0.35)
    y1 = top + (row + 1) * cell_h - int(cell_h * 0.45)
    return img.crop((x0, y0, x1, y1))


def main():
    try:
        from PIL import Image
    except ImportError:
        print("Installez Pillow : pip install Pillow")
        return

    from app import app
    from extensions import db
    from models.product import Product

    dest_dir = os.path.join(ROOT, "static", "img", "products")
    os.makedirs(dest_dir, exist_ok=True)
    updated = 0

    with app.app_context():
        for fragment, items in CATALOG_CROPS.items():
            path = _find_screenshot(fragment)
            if not path:
                print(f"Capture introuvable: {fragment}")
                continue
            img = Image.open(path).convert("RGB")
            for slug, row, col in items:
                product = Product.query.filter_by(slug=slug).first()
                if not product:
                    print(f"Produit absent: {slug}")
                    continue
                crop = _crop_product(img, row, col)
                rel = f"img/products/{slug}.jpg"
                out = os.path.join(ROOT, "static", rel.replace("/", os.sep))
                crop.save(out, "JPEG", quality=88)
                product.image = rel
                updated += 1
                print(f"OK {slug}")
        db.session.commit()
        print(f"\nPhotos mises à jour: {updated}")


if __name__ == "__main__":
    main()
