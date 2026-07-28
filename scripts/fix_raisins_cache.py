# -*- coding: utf-8 -*-
"""Force une nouvelle URL photo pour Raisins secs golden (casse le cache navigateur)."""
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

OLD_SLUG_FILE = "raisins-secs-golden.jpg"
NEW_FILE = "raisins-secs-golden-v2.jpg"
SLUG = "raisins-secs-golden"
SRC_NAME = "Raisins secs golden.jpg"
REL = f"img/products/{NEW_FILE}"


def patch_product_images_py() -> None:
    path = ROOT / "models" / "product_images.py"
    text = path.read_text(encoding="utf-8")
    text2 = text.replace(
        f'"{SLUG}": "img/products/{OLD_SLUG_FILE}"',
        f'"{SLUG}": "{REL}"',
    )
    if f'"{SRC_NAME}":' not in text2:
        marker = '    "Bavette d\'aloyau x10 — 1,6–1,7 kg.jpg": "bavette-aloyau-x10",'
        text2 = text2.replace(
            marker,
            marker + f'\n    "{SRC_NAME}": "{SLUG}",',
            1,
        )
    if text2 != text:
        path.write_text(text2, encoding="utf-8")
        print("patched product_images.py")


def main() -> None:
    src = ROOT / "img" / SRC_NAME
    out_dir = ROOT / "static" / "img" / "products"
    dest = out_dir / NEW_FILE
    old = out_dir / OLD_SLUG_FILE
    if not src.is_file():
        raise SystemExit(f"missing {src}")
    shutil.copy2(src, dest)
    if old.is_file():
        old.unlink()
        print("removed old", OLD_SLUG_FILE)
    pi.PRODUCT_IMAGES[SLUG] = REL
    pi.IMAGE_SOURCES[SRC_NAME] = SLUG
    patch_product_images_py()
    with app.app_context():
        product = Product.query.filter_by(slug=SLUG).first()
        if not product:
            raise SystemExit("product missing")
        product.image = REL
        db.session.commit()
        print("OK", product.image, dest.stat().st_size)


if __name__ == "__main__":
    main()
