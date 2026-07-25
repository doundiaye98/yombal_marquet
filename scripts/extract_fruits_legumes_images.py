# -*- coding: utf-8 -*-
"""Extract fruits & légumes product photos from PDF into static/img/products/."""

from __future__ import annotations

import io
from pathlib import Path

import fitz
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "img" / "fruits et legumess.pdf"
DEST = ROOT / "static" / "img" / "products"

FRUIT_PAGES = {
    3: "mangue-frais-1kg",
    4: "pasteque-frais-1kg",
    5: "ditakh-frais-1kg",
    6: "bouye-frais-1kg",
    7: "madd-frais-1kg",
    8: "papaye-frais-1kg",
    9: "goyave-frais-1kg",
    10: "banane-frais-1kg",
    11: "orange-locale-1kg",
    12: "mandarine-frais-1kg",
    13: "corossol-frais-1kg",
    14: "noix-coco-frais-1kg",
    15: "ananas-frais-1kg",
    16: "jujube-sidem-1kg",
    17: "pomme-cajou-frais-1kg",
}

VEG_PAGES = {
    19: ["oignon-frais-1kg", "tomate-frais-1kg", "gombo-frais-1kg"],
    20: ["carotte-frais-1kg", "chou-pomme-frais-1kg", "chou-fleur-frais-1kg"],
    21: ["aubergine-noire-1kg", "aubergine-amere-djakhato-1kg", "pomme-terre-frais-1kg"],
    22: ["patate-douce-1kg", "manioc-frais-1kg", "poivron-vert-1kg"],
    23: ["piment-frais-1kg", "concombre-frais-1kg", "courgette-frais-1kg"],
    24: ["laitue-frais-1kg", "haricot-vert-1kg", "niebe-frais-1kg"],
    25: ["betterave-frais-1kg", "igname-frais-1kg", "navet-frais-1kg"],
}


def save_jpeg(data: bytes, slug: str) -> None:
    img = Image.open(io.BytesIO(data))
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left + side, top + side))
    if side > 900:
        img = img.resize((900, 900), Image.Resampling.LANCZOS)
    path = DEST / f"{slug}.jpg"
    img.save(path, "JPEG", quality=88, optimize=True)
    print("saved", path.name, img.size)


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(PDF)

    for page_no, slug in FRUIT_PAGES.items():
        page = doc[page_no - 1]
        infos = [i for i in page.get_image_info(xrefs=True) if i.get("width", 0) > 160]
        infos.sort(key=lambda i: -(i["width"] * i["height"]))
        if not infos:
            print("MISSING fruit page", page_no)
            continue
        raw = doc.extract_image(infos[0]["xref"])["image"]
        save_jpeg(raw, slug)

    for page_no, slugs in VEG_PAGES.items():
        page = doc[page_no - 1]
        infos = [i for i in page.get_image_info(xrefs=True) if i.get("width", 0) > 160]
        infos.sort(key=lambda i: (i["bbox"][1], i["bbox"][0]))
        if len(infos) < len(slugs):
            print("WARN page", page_no, "imgs", len(infos), "need", len(slugs))
        for slug, info in zip(slugs, infos):
            raw = doc.extract_image(info["xref"])["image"]
            save_jpeg(raw, slug)

    total = len(FRUIT_PAGES) + sum(len(v) for v in VEG_PAGES.values())
    print("done", total, "products")


if __name__ == "__main__":
    main()
