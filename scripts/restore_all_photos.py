# -*- coding: utf-8 -*-
"""Force la restauration des photos depuis IMAGE_SOURCES + photos bœuf correctes."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

GOOD = {
    "Bavette d'aloyau x10 — 1,6–1,7 kg.jpg": "bavette-aloyau-x10",
    "Bavette d'aloyau x2 — 300–400 g.jpg": "bavette-aloyau-x2",
    "Carré Box 100% bœuf — 3,85–4,85 kg.jpg": "carre-box-boeuf-100",
    "Carré Box régime protéiné avec rôtis — 4.jpg": "carre-box-regime-proteine-rotis",
    "Carré Box régime.jpg": "carre-box-regime-proteine",
    "Carré Box viande familial authentique —.jpg": "carre-box-viande-familial-authentique",
}

# Produits bœuf nouveaux sans vraie photo (hors GOOD)
BEEF_NO_PHOTO = {
    "carre-box-viande-famille-nombreuse",
    "carre-box-degustation-plaisir",
    "entrecote-xxl-boeuf-montbeliarde",
    "cote-boeuf-france-800g-1kg",
    "faux-filet-boeuf-salers",
    "entrecote-boeuf-charolais",
    "pave-rumsteck-boeuf-salers-x2",
    "entrecote-boeuf-selection-boucher-x2",
    "entrecote-boeuf-xxl-selection-boucher",
    "paleron-boeuf-bourguignon",
    "tomahawk-boeuf-blonde-galice",
    "cote-boeuf-france-1-15kg",
    "cote-boeuf-selection-boucher-115-14",
    "cote-boeuf-selection-boucher-950-115",
    "tournedos-rumsteck-boeuf-salers-x2",
    "tournedos-filet-boeuf-salers-x2",
    "gite-boeuf-pot-au-feu",
    "viande-fondue-boeuf-salers",
    "roti-boeuf-salers-800g-1kg",
    "roti-boeuf-salers-115-135",
    "roti-filet-boeuf-francais-115-135",
    "roti-filet-boeuf-francais-800-900",
    "roti-boeuf-tende-tranche-2-22",
    "roti-boeuf-tende-tranche-115-135",
    "roti-boeuf-tende-tranche-800g-1kg",
    "steak-tartare-boeuf-francais-180g",
    "onglet-boeuf-x2",
    "steak-poire-boeuf-x2",
    "emince-boeuf-500g",
    "entrecote-boeuf-francaise-xxl",
    "entrecote-boeuf-francaise",
    "filet-boeuf-entier",
    "filet-boeuf-francais-entier",
    "cote-boeuf-angus",
    "picanha-boeuf-angus",
    "filet-boeuf-angus-entier",
    "entrecote-boeuf-wagyu-japonais",
    "onglet-boeuf-angus-x2",
    "entrecote-xxl-boeuf-salers",
    "entrecote-boeuf-salers",
}


def patch_py():
    path = ROOT / "models" / "product_images.py"
    text = path.read_text(encoding="utf-8")
    # remove truncated Bavette d'.jpg mapping
    text = text.replace('    "Bavette d\'.jpg": "bavette-aloyau-x2",\n', "")
    # remove PRODUCT_IMAGES lines for BEEF_NO_PHOTO (bad placeholders)
    for slug in BEEF_NO_PHOTO:
        text = text.replace(f'    "{slug}": "img/products/{slug}.jpg",\n', "")
    # ensure GOOD in PRODUCT_IMAGES
    for slug in GOOD.values():
        line = f'    "{slug}": "img/products/{slug}.jpg",\n'
        if line not in text:
            anchor = '    "fataya-viande-10": "img/products/fataya-viande-10.jpg",\n'
            text = text.replace(anchor, anchor + line, 1)
    for fname, slug in GOOD.items():
        line = f'    "{fname}": "{slug}",\n'
        if f'"{fname}"' not in text:
            anchor = '    "Fataya viande.jpg": "fataya-viande-10",\n'
            text = text.replace(anchor, anchor + line, 1)
    path.write_text(text, encoding="utf-8")
    print("product_images.py cleaned")


def force_install_all_sources():
    from models.product_images import IMAGE_SOURCES, PRODUCT_IMAGES

    src_dir = ROOT / "img"
    dest_dir = ROOT / "static" / "img" / "products"
    dest_dir.mkdir(parents=True, exist_ok=True)
    # delete corrupted beef-no-photo files
    for slug in BEEF_NO_PHOTO:
        f = dest_dir / f"{slug}.jpg"
        if f.is_file():
            f.unlink()
            print("deleted", f.name)

    copied = 0
    for filename, slug in IMAGE_SOURCES.items():
        src = src_dir / filename
        if not src.is_file():
            continue
        rel = PRODUCT_IMAGES.get(slug)
        if not rel:
            # still copy to standard path
            dest = dest_dir / f"{slug}.jpg"
        else:
            dest = ROOT / "static" / rel.replace("/", "\\")
        shutil.copy2(src, dest)
        copied += 1
    print("force-copied", copied, "from IMAGE_SOURCES")

    # GOOD explicitly
    for fname, slug in GOOD.items():
        src = src_dir / fname
        if src.is_file():
            shutil.copy2(src, dest_dir / f"{slug}.jpg")
            print("good", slug, src.stat().st_size)


def sync_db():
    from extensions import db
    from app import app
    from models.product import Product
    from models.product_images import sync_product_images, PRODUCT_IMAGES

    with app.app_context():
        for slug in BEEF_NO_PHOTO:
            p = Product.query.filter_by(slug=slug).first()
            if p:
                p.image = None
        for slug in GOOD.values():
            p = Product.query.filter_by(slug=slug).first()
            if p:
                p.image = f"img/products/{slug}.jpg"
        db.session.commit()
        sync_product_images(str(ROOT))
        # verify a few known good
        samples = [
            "bavette-aloyau-x10",
            "carre-box-boeuf-100",
            "foie-boeuf-halal-1kg",
            "cotes-boeuf-halal-1kg",
            "agneau-cote-premiere",
            "carre-box-agneau-paques-premium",
            "merguez-boeuf-halal-1kg",
            "batterie-externe-20000mah",
        ]
        for slug in samples:
            p = Product.query.filter_by(slug=slug).first()
            path = ROOT / "static" / (p.image or "").replace("/", "\\") if p and p.image else None
            ok = bool(path and path.is_file())
            print(("OK" if ok else "BAD"), slug, "->", getattr(p, "image", None))


def main():
    patch_py()
    force_install_all_sources()
    sync_db()


if __name__ == "__main__":
    main()
