# -*- coding: utf-8 -*-
"""Restore PDF-missing products: images, admin unremove, sync."""

from __future__ import annotations

import io
import sys
from pathlib import Path

import fitz
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

PDF_LABEL = ROOT / "img" / "Catalogue LABEL (1).pdf"
DEST = ROOT / "static" / "img" / "products"

# page -> list of (slug, product-slot index among product photos top-to-bottom / L-R)
# Layout: 2x2 grid of products on pages 27, 52-56
EXTRACT_SLOTS = {
    27: [("huile-arachide-1l", 1)],  # TL=0 tournesol, TR=1 arachide, BL=2 tournesol5, BR=3 palme
    52: [("plantain-frais-1kg", 0)],
    53: [
        ("patate-douce-blanche-1kg", 1),
        ("patate-douce-rose-1kg", 2),
    ],
    54: [("gingembre-frais-1kg", 2)],
    55: [("poivron-rouge-1kg", 3)],
    56: [("citron-vert-1kg", 2)],
}

RESTORE_ADMIN = [
    "beurre-karite-alimentaire-250g",
    "fonio-500g",
    "mil-millet-1kg",
    "sel-kaolack-500g",
]


def product_bboxes(page) -> list:
    """Return product photo bboxes sorted reading-order (exclude logo / banner / bg)."""
    infos = []
    for info in page.get_image_info(xrefs=True):
        xref = info.get("xref") or 0
        w = info.get("width") or 0
        bbox = info["bbox"]
        if xref == 0:
            continue
        if w >= 1000:  # full-bleed background
            continue
        if w >= 190 and bbox[1] < 120:  # header logos
            continue
        if w < 70:
            continue
        # product photos typically y > 200
        if bbox[1] < 200:
            continue
        infos.append(info)
    infos.sort(key=lambda i: (round(i["bbox"][1] / 80), i["bbox"][0]))
    return infos


def save_clip(page, bbox, slug: str, zoom: float = 4.0) -> None:
    # pad clip a bit
    x0, y0, x1, y1 = bbox
    pad = 8
    clip = fitz.Rect(x0 - pad, y0 - pad, x1 + pad, y1 + pad) & page.rect
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, clip=clip, alpha=False)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left + side, top + side))
    if side > 900:
        img = img.resize((900, 900), Image.Resampling.LANCZOS)
    elif side < 400:
        img = img.resize((600, 600), Image.Resampling.LANCZOS)
    path = DEST / f"{slug}.jpg"
    img.save(path, "JPEG", quality=88, optimize=True)
    print("saved", path.name, img.size)


def extract_images() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(PDF_LABEL)
    for page_no, specs in EXTRACT_SLOTS.items():
        page = doc[page_no - 1]
        boxes = product_bboxes(page)
        print(f"page {page_no}: {len(boxes)} product photos")
        for slug, idx in specs:
            if idx >= len(boxes):
                print("MISSING slot", page_no, slug, "have", len(boxes))
                continue
            save_clip(page, boxes[idx]["bbox"], slug)


def main() -> None:
    extract_images()

    from app import app
    from extensions import db
    from models.constants import CATEGORY_FRUITS, CATEGORY_LEGUMES
    from models.product import Product
    from models.product_images import sync_product_images
    from models.seed import sync_catalogue
    from services.product_admin import unmark_slug_admin_removed

    new_slugs = [
        "huile-arachide-1l",
        "plantain-frais-1kg",
        "citron-vert-1kg",
        "poivron-rouge-1kg",
        "gingembre-frais-1kg",
        "patate-douce-blanche-1kg",
        "patate-douce-rose-1kg",
    ]

    with app.app_context():
        for slug in RESTORE_ADMIN:
            unmark_slug_admin_removed(slug)
            print("unremoved", slug)
        db.session.commit()

        sync_catalogue()
        sync_product_images(app.root_path)

        for slug in new_slugs + RESTORE_ADMIN:
            p = Product.query.filter_by(slug=slug).first()
            status = "OK" if p and p.is_active else "FAIL"
            detail = None if not p else f"{p.price_cents/100}€ img={bool(p.image)}"
            print(status, slug, detail)

        print(
            "fruits",
            Product.query.filter_by(category=CATEGORY_FRUITS, is_active=True).count(),
            "legumes",
            Product.query.filter_by(category=CATEGORY_LEGUMES, is_active=True).count(),
        )


if __name__ == "__main__":
    main()
