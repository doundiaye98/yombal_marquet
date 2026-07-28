# -*- coding: utf-8 -*-
"""Installe les photos produits agneau depuis img/."""
from __future__ import annotations

import re
import shutil
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Exact filename → slug (filenames as on disk under img/)
MAPPINGS = {
    "Agneau côte première — 400–500 g.jpg": "agneau-cote-premiere",
    "Agneau navarin — 900 g–1,1 kg.jpg": "agneau-navarin",
    "Carré 5 côtes d'agneau français — 1–1,2 kg.jpg": "carre-5-cotes-agneau-francais",
    "Carré 8 côtes d'agneau français — 1,2–1,6 kg.jpg": "carre-8-cotes-agneau-francais",
    "Carré 8 côtes d'agneau — 800 g–1,2 kg.jpg": "carre-8-cotes-agneau",
    "Carré Box Agneau de Pâques premium —.jpg": "carre-box-agneau-paques-premium",
    "Carré Box Agneau de Pâques — 2,75–3,05 kg.jpg": "carre-box-agneau-paques",
    "Carré d'agneau 4 côtes premières — 400–500.jpg": "carre-agneau-4-cotes-premieres",
    "Côtes découvertes d'agneau français —.jpg": "cotes-decouvertes-agneau-francais",
    "Côtes découvertes d'agneau — 400–500 g.jpg": "cotes-decouvertes-agneau",
    "Gigot d'agneau entier — 2,3–2,7 kg.jpg": "gigot-agneau-entier",
    "Gigot d'agneau français — 2,3–2,7 kg.jpg": "gigot-agneau-francais",
    "Navarin d'agneau français — 900 g–1,1 kg.jpg": "navarin-agneau-francais",
    "Rôti d'épaule d'agneau ficelle — 900 g–1,2 kg.jpg": "roti-epaule-agneau-ficelle",
    "Rôti d'épaule d'agneau français — 1,3–1,7 kg.jpg": "roti-epaule-agneau-francais",
    "Rôti Gigotin d'épaule d'agneau — 1,2–1,5 kg.jpg": "roti-gigotin-epaule-agneau",
    "Rôti Noisette d'agneau — 1–1,5 kg.jpg": "roti-noisette-agneau",
    "Sauté d'épaule d'agneau — 800–900 g.jpg": "saute-epaule-agneau",
    "Sauté de gigot d'agneau — 800–900 g.jpg": "saute-gigot-agneau",
    "Épaule d'agneau français — 1,3–1,6 kg.jpg": "epaule-agneau-francais",
    "Épaule d'agneau sans palette — 1,5–1,8 kg.jpg": "epaule-agneau-sans-palette",
}


def patch_product_images() -> None:
    path = ROOT / "models" / "product_images.py"
    text = path.read_text(encoding="utf-8")
    changed = False

    # PRODUCT_IMAGES paths
    for fname, slug in MAPPINGS.items():
        line = f'    "{slug}": "img/products/{slug}.jpg",\n'
        if f'"{slug}":' not in text.split("PRODUCT_IMAGES")[0] if False else True:
            # Insert into _RAW_PRODUCT_IMAGES if missing
            key = f'    "{slug}":'
            if key not in text:
                anchor = '    "biscuits-gem": "img/products/biscuits-gem.jpg",\n'
                if "fataya-poisson-10" in text:
                    anchor = '    "fataya-viande-10": "img/products/fataya-viande-10.jpg",\n'
                if anchor in text and key not in text:
                    text = text.replace(anchor, anchor + line, 1)
                    changed = True
                    print("PRODUCT_IMAGES +", slug)

    # IMAGE_SOURCES
    for fname, slug in MAPPINGS.items():
        src_line = f'    "{fname}": "{slug}",\n'
        if fname in text and f'"{fname}"' in text:
            continue
        if src_line not in text:
            # insert near fataya or biscuits
            for anchor in (
                '    "Fataya viande.jpg": "fataya-viande-10",\n',
                '    "Biscuits Gem.jpg": "biscuits-gem",\n',
            ):
                if anchor in text:
                    text = text.replace(anchor, anchor + src_line, 1)
                    changed = True
                    print("IMAGE_SOURCES +", fname)
                    break

    if changed:
        path.write_text(text, encoding="utf-8")
        print("product_images.py mis à jour")
    else:
        print("product_images.py déjà à jour (ou patch manuel)")


def install_files() -> int:
    src_dir = ROOT / "img"
    dest_dir = ROOT / "static" / "img" / "products"
    dest_dir.mkdir(parents=True, exist_ok=True)
    # Build case/normalize tolerant lookup of files on disk
    on_disk = {p.name: p for p in src_dir.iterdir() if p.is_file()}
    copied = 0
    missing = []
    for fname, slug in MAPPINGS.items():
        src = on_disk.get(fname)
        if not src:
            # try normalize dashes
            missing.append(fname)
            continue
        dest = dest_dir / f"{slug}.jpg"
        shutil.copy2(src, dest)
        copied += 1
        print("copied", fname, "->", dest.name)
    if missing:
        print("MANQUANTS:")
        for m in missing:
            print(" -", repr(m))
            # show close matches
            key = m[:20]
            for name in on_disk:
                if name.startswith(key[:8]) or key[:8] in name:
                    print("   proche:", repr(name))
    return copied


def main():
    # Discover actual filenames for fuzzy fix
    img_dir = ROOT / "img"
    print("=== fichiers img/ candidats ===")
    for p in sorted(img_dir.iterdir()):
        if not p.is_file():
            continue
        n = p.name
        if any(
            x in n
            for x in (
                "Agneau",
                "Carré",
                "Gigot",
                "Épaule",
                "Navarin",
                "Rôti",
                "Sauté",
                "Côtes",
            )
        ):
            print(repr(n))

    n = install_files()
    print("fichiers copiés:", n)
    patch_product_images()

    from app import app
    from models.product_images import sync_product_images
    from models.product import Product

    with app.app_context():
        sync_product_images(str(ROOT))
        slugs = list(MAPPINGS.values())
        for slug in slugs:
            p = Product.query.filter_by(slug=slug).first()
            ok = bool(p and p.image and (ROOT / "static" / p.image.replace("/", "\\")).is_file())
            print(slug, "->", getattr(p, "image", None), "file_ok" if ok else "MISSING")


if __name__ == "__main__":
    main()
