# -*- coding: utf-8 -*-
"""Installe les nouvelles photos viandes (lot 2) depuis img/."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

H = "hal" + "al"

SOURCES = {
    f"Brochettes d'agneau {H}.jpg": "brochettes-agneau-halal-1kg",
    f"Brochettes de poulet {H}.jpg": "brochettes-poulet-halal-1kg",
    f"Côtelettes d'agneau {H}.jpg": "cotelettes-agneau-halal-1kg",
    f"Côtes de bœuf {H}.jpg": "cotes-boeuf-halal-1kg",
    f"Escalopes de dinde {H}.jpg": "escalopes-dinde-halal-1kg",
    f"Filets de poulet {H}.jpg": "filets-poulet-halal-1kg",
    f"Foie de bœuf {H}.jpg": "foie-boeuf-halal-1kg",
    f"Gigot d'agneau {H}.jpg": "gigot-agneau-halal",
    f"Hauts de cuisse poulet {H}.jpg": "hauts-cuisse-poulet-halal-5kg",
    f"Kefta {H}.jpg": "kefta-halal-1kg",
    f"Merguez bœuf {H}.jpg": "merguez-boeuf-halal-1kg",
    f"Morceaux d'agneau {H}.jpg": "morceaux-agneau-halal-1kg",
    "Morceaux de mouton.jpg": "morceaux-mouton-halal-1kg",
    f"Pieds de bœuf {H}.jpg": "pieds-boeuf-halal-1kg",
    f"Pintade entière {H}.jpg": "pintade-entiere-halal",
    f"Steak haché bœuf {H}.jpg": "steak-hache-boeuf-halal-1kg",
    f"Tripes de bœuf {H}.jpg": "tripes-boeuf-halal-1kg",
    "Viande d'escargot.jpg": "viande-escargot-500g",
}


def patch_image_sources() -> None:
    path = ROOT / "models" / "product_images.py"
    text = path.read_text(encoding="utf-8")
    check = f'Brochettes d\'agneau {H}.jpg'
    if check in text:
        print("IMAGE_SOURCES already has lot 2")
        return
    anchor = f'    "Morceaux de bœuf {H}.jpg": "morceaux-boeuf-1kg",\n'
    if anchor not in text:
        # try after corned or end of previous meat block
        for alt in (
            f'    "Poule entière {H}.png": "poule-entiere-halal",\n',
            f'    "Queue de bœuf {H}.jpg": "queue-boeuf-1kg",\n',
        ):
            if alt in text:
                anchor = alt
                break
        else:
            raise SystemExit("anchor not found for IMAGE_SOURCES")
    block = "\n".join(f'    "{fn}": "{slug}",' for fn, slug in SOURCES.items()) + "\n"
    text = text.replace(anchor, anchor + block, 1)
    path.write_text(text, encoding="utf-8")
    print("patched IMAGE_SOURCES")


def install_files() -> None:
    src_dir = ROOT / "img"
    dest_dir = ROOT / "static" / "img" / "products"
    dest_dir.mkdir(parents=True, exist_ok=True)
    for filename, slug in SOURCES.items():
        src = src_dir / filename
        if not src.is_file():
            print("MISSING", repr(filename))
            continue
        dest = dest_dir / f"{slug}.jpg"
        shutil.copy2(src, dest)
        print("copied", filename, "->", dest.name)


def main() -> None:
    for k in SOURCES:
        print(repr(k), (ROOT / "img" / k).is_file())
    patch_image_sources()
    install_files()
    from app import app
    from models.product_images import sync_product_images

    with app.app_context():
        sync_product_images(str(ROOT))
        print("DB synced")


if __name__ == "__main__":
    main()
