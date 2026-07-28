# -*- coding: utf-8 -*-
"""Associe la vraie photo Raisins secs golden."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import app
from extensions import db
from models.product import Product
from models import product_images as pi

SLUG = "raisins-secs-golden"
SRC_NAME = "Raisins secs golden.jpg"
REL = f"img/products/{SLUG}.jpg"


def ensure_py_entries() -> None:
    path = ROOT / "models" / "product_images.py"
    text = path.read_text(encoding="utf-8")
    changed = False
    raw_section = text.split("PRODUCT_IMAGES = dict")[0]
    raw_line = f'    "{SLUG}": "{REL}",'
    if f'"{SLUG}":' not in raw_section:
        marker = '    "bavette-aloyau-x2": "img/products/bavette-aloyau-x2.jpg",'
        if marker not in text:
            raise SystemExit("marker RAW introuvable")
        text = text.replace(marker, marker + "\n" + raw_line, 1)
        changed = True
    src_line = f'    "{SRC_NAME}": "{SLUG}",'
    if f'"{SRC_NAME}":' not in text:
        marker2 = '    "Bavette d\'aloyau x10 — 1,6–1,7 kg.jpg": "bavette-aloyau-x10",'
        if marker2 not in text:
            raise SystemExit("marker IMAGE_SOURCES introuvable")
        text = text.replace(marker2, marker2 + "\n" + src_line, 1)
        changed = True
    if changed:
        path.write_text(text, encoding="utf-8")
        print("updated product_images.py")


def main() -> None:
    src = ROOT / "img" / SRC_NAME
    dest = ROOT / "static" / "img" / "products" / f"{SLUG}.jpg"
    if not src.is_file():
        raise SystemExit(f"missing {src}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    pi.PRODUCT_IMAGES[SLUG] = REL
    pi.IMAGE_SOURCES[SRC_NAME] = SLUG
    ensure_py_entries()
    with app.app_context():
        product = Product.query.filter_by(slug=SLUG).first()
        if not product:
            raise SystemExit("product missing")
        product.image = REL
        db.session.commit()
        print(f"OK {product.name} -> {product.image} ({dest.stat().st_size} o)")


if __name__ == "__main__":
    main()
