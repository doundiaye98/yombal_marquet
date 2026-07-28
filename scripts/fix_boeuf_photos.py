# -*- coding: utf-8 -*-
"""Corrige les mauvaises associations photos + installe les vraies photos bœuf."""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Uniquement les nouvelles photos bœuf fournies (fichiers exacts)
GOOD = {
    "Bavette d'aloyau x10 — 1,6–1,7 kg.jpg": "bavette-aloyau-x10",
    "Bavette d'aloyau x2 — 300–400 g.jpg": "bavette-aloyau-x2",
    "Carré Box 100% bœuf — 3,85–4,85 kg.jpg": "carre-box-boeuf-100",
    "Carré Box régime protéiné avec rôtis — 4.jpg": "carre-box-regime-proteine-rotis",
    "Carré Box régime.jpg": "carre-box-regime-proteine",
    "Carré Box viande familial authentique —.jpg": "carre-box-viande-familial-authentique",
}

# Slugs beef récemment ajoutés : retirer les mauvaises entrées IMAGE_SOURCES
# sauf les GOOD ci-dessus et les anciennes photos hali déjà correctes
BEEF_NEW_SLUGS = {
    "bavette-aloyau-x10",
    "bavette-aloyau-x2",
    "carre-box-boeuf-100",
    "carre-box-regime-proteine-rotis",
    "carre-box-regime-proteine",
    "carre-box-viande-familial-authentique",
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


def clean_product_images_py():
    path = ROOT / "models" / "product_images.py"
    text = path.read_text(encoding="utf-8")

    # Remove IMAGE_SOURCES lines that point to BEEF_NEW_SLUGS but are not in GOOD
    # Pattern: "filename": "slug",
    def keep_source_line(line: str) -> bool:
        m = re.match(r'\s+"(.+?)": "([a-z0-9-]+)",\s*$', line)
        if not m:
            return True
        fname, slug = m.group(1), m.group(2)
        if slug not in BEEF_NEW_SLUGS:
            return True
        # keep only if this filename is the good one for that slug
        for good_fname, good_slug in GOOD.items():
            if slug == good_slug and fname == good_fname:
                return True
        # Also keep if filename clearly names the product (contains key tokens)
        # Drop clearly wrong mappings (electronics, wrong meats, etc.)
        bad_hints = (
            "Ampoules",
            "Adaptateur",
            "Clavier",
            "Enceinte",
            "Fer à",
            "Mixeur",
            "Bouilloire",
            "Aspirateur",
            "Batterie",
            "Chargeur",
            "Casque",
            "Anneau",
            "Baskets",
            "Coque",
            "Lampe",
            "Machine à café",
            "Gemini_",
            "Dorade",
            "Chinchard",
            "Ailes de poulet",
            "Ailerons",
            "Filets de poulet",
            "Thiakhri",
            "Miel de fleurs",
            "Agneau",
            "Carré 5",
            "Carré 8",
            "Carré d'agneau",
            "Navarin",
            "Côtes découvertes",
            "Brochettes",
            "Queue de bœuf",
            "Pieds de bœuf",
            "Morceaux de bœuf",
            "Foie de bœuf",
            "Tripes",
            "Steak haché",
            "Carré Box Agneau",
        )
        if any(h in fname for h in bad_hints):
            return False
        # For beef new slugs without GOOD filename, drop unknown auto mappings
        if slug in BEEF_NEW_SLUGS and fname not in GOOD:
            # keep only if fname looks related
            low = fname.lower()
            slug_bits = slug.replace("-", " ").split()
            if not any(bit in low for bit in slug_bits if len(bit) > 3):
                return False
        return True

    lines = text.splitlines(keepends=True)
    new_lines = []
    removed = 0
    in_sources = False
    for line in lines:
        if line.startswith("IMAGE_SOURCES"):
            in_sources = True
        if in_sources and line.strip() == "}":
            in_sources = False
        if in_sources and '": "' in line and not keep_source_line(line):
            removed += 1
            continue
        new_lines.append(line)
    text = "".join(new_lines)

    # Ensure GOOD entries exist in IMAGE_SOURCES and PRODUCT_IMAGES
    for fname, slug in GOOD.items():
        img_line = f'    "{slug}": "img/products/{slug}.jpg",\n'
        if f'"{slug}": "img/products/{slug}.jpg"' not in text:
            anchor = '    "fataya-viande-10": "img/products/fataya-viande-10.jpg",\n'
            if anchor in text:
                text = text.replace(anchor, anchor + img_line, 1)
        src_line = f'    "{fname}": "{slug}",\n'
        if f'"{fname}"' not in text:
            anchor = '    "Fataya viande.jpg": "fataya-viande-10",\n'
            if anchor in text:
                text = text.replace(anchor, anchor + src_line, 1)

    # Clear DB image for beef new slugs that are NOT in GOOD (wrong photos)
    path.write_text(text, encoding="utf-8")
    print(f"removed {removed} bad IMAGE_SOURCES lines")


def install_good():
    dest_dir = ROOT / "static" / "img" / "products"
    dest_dir.mkdir(parents=True, exist_ok=True)
    img = ROOT / "img"
    for fname, slug in GOOD.items():
        src = img / fname
        if not src.is_file():
            print("MISSING src", fname)
            continue
        shutil.copy2(src, dest_dir / f"{slug}.jpg")
        print("installed", slug)


def restore_all_from_sources():
    from models.product_images import install_product_images, sync_product_images
    from app import app
    from models.product import Product
    from models import db

    n = install_product_images(str(ROOT))
    print("reinstalled from IMAGE_SOURCES:", n)

    with app.app_context():
        # Clear wrong images on beef new products without a good photo
        good_slugs = set(GOOD.values())
        for p in Product.query.filter(Product.slug.in_(BEEF_NEW_SLUGS)).all():
            if p.slug in good_slugs:
                p.image = f"img/products/{p.slug}.jpg"
            else:
                # if mapped image file doesn't look like a real meat product path, clear
                # keep image only if file exists AND was restored from a sensible source
                # For now: clear unless in GOOD
                rel = p.image or ""
                path = ROOT / "static" / rel.replace("/", "\\")
                # If no dedicated source in IMAGE_SOURCES for this slug, clear
                from models.product_images import IMAGE_SOURCES

                has_source = any(s == p.slug for s in IMAGE_SOURCES.values())
                if not has_source:
                    p.image = None
                    if path.is_file() and p.slug not in good_slugs:
                        # remove wrongly copied file for this slug if it was a bad match
                        # only delete if slug is new beef without good photo
                        try:
                            path.unlink()
                            print("deleted bad file", path.name)
                        except OSError:
                            pass
        db.session.commit()
        sync_product_images(str(ROOT))
        for slug in sorted(GOOD.values()):
            p = Product.query.filter_by(slug=slug).first()
            print("OK" if p and p.image else "NO", slug, "->", getattr(p, "image", None))


def main():
    clean_product_images_py()
    install_good()
    restore_all_from_sources()


if __name__ == "__main__":
    main()
