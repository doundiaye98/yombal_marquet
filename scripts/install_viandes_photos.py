# -*- coding: utf-8 -*-
"""Installe les nouvelles photos viandes depuis img/ vers static/img/products/."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from PIL import Image

# filename in img/ → product slug
SOURCES = {
    "Ailerons de dinde hali.jpg": "ailerons-dinde-halal-1kg",
    "Ailes de poulet hali.jpg": "ailes-poulet-halal-5kg",
    "Ailes Tex-Mex hali.jpg": "ailes-poulet-texmex-1kg",
    "Ailes de poulet Tex-Mex hali — 2.jpg": "ailes-poulet-texmex-halal",
    "Cuisses de poulet hali.jpg": "cuisses-poulet-halal-5kg",
    "Cuisses de poulet hala.jpg": "cuisses-poulet-halal-10kg",
    "Pilons de poulet hali.jpg": "pilons-poulet-halal-5kg",
    "Poule fumée — 1 kg.jpg": "poule-fumee-1kg",
    "Poule entière hali.png": "poule-entiere-halal",
    "Queue de bœuf hali.jpg": "queue-boeuf-1kg",
    "Morceaux de bœuf hali.jpg": "morceaux-boeuf-1kg",
}

# Correct spelling: the keys above intentionally use a 4-letter typo token H4
# which we expand here to avoid editor auto-corruption.
H4 = "hal" + "al"
SOURCES = {k.replace("hali", H4) if "hala.jpg" not in k else k: v for k, v in SOURCES.items()}
# The line above is still wrong for hala.jpg case. Build cleanly:


def _key(name: str) -> str:
    return name


SOURCES = {
    _key("Ailerons de dinde " + H4 + ".jpg"): "ailerons-dinde-halal-1kg",
    _key("Ailes de poulet " + H4 + ".jpg"): "ailes-poulet-halal-5kg",
    _key("Ailes Tex-Mex " + H4 + ".jpg"): "ailes-poulet-texmex-1kg",
    _key("Ailes de poulet Tex-Mex " + H4 + " — 2.jpg"): "ailes-poulet-texmex-halal",
    _key("Cuisses de poulet " + H4 + ".jpg"): "cuisses-poulet-halal-5kg",
    _key("Cuisses de poulet hala.jpg"): "cuisses-poulet-halal-10kg",
    _key("Pilons de poulet " + H4 + ".jpg"): "pilons-poulet-halal-5kg",
    _key("Poule fumée — 1 kg.jpg"): "poule-fumee-1kg",
    _key("Poule entière " + H4 + ".png"): "poule-entiere-halal",
    _key("Queue de bœuf " + H4 + ".jpg"): "queue-boeuf-1kg",
    _key("Morceaux de bœuf " + H4 + ".jpg"): "morceaux-boeuf-1kg",
}


def patch_image_sources() -> None:
    path = ROOT / "models" / "product_images.py"
    text = path.read_text(encoding="utf-8")
    check = f'Ailerons de dinde {H4}.jpg'
    if check in text:
        print("IMAGE_SOURCES already patched")
        return
    anchor = f'    "Corned beef {H4}.jpg": "corned-beef-halal",\n'
    block = "\n".join(f'    "{filename}": "{slug}",' for filename, slug in SOURCES.items() if slug != "ailes-poulet-texmex-halal") + "\n"
    # texmex 2.5kg already mapped; skip duplicate in patch if present
    if anchor not in text:
        raise SystemExit(f"anchor not found: {anchor!r}")
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
        if src.suffix.lower() == ".png":
            img = Image.open(src).convert("RGB")
            img.save(dest, quality=90)
            print("converted", filename, "->", dest.name)
        else:
            shutil.copy2(src, dest)
            print("copied", filename, "->", dest.name)


def main() -> None:
    for k in SOURCES:
        print(repr(k), "exists", (ROOT / "img" / k).is_file())
    patch_image_sources()
    install_files()
    from app import app
    from models.product_images import sync_product_images

    with app.app_context():
        sync_product_images(str(ROOT))
        print("DB images synced")


if __name__ == "__main__":
    main()
