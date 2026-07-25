# -*- coding: utf-8 -*-
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

SOURCES = {
    "Riz au lait (sombi).jpg": "sombi-riz-au-lait",
    "Thiakhri au lait — 400 g.jpg": "thiakhri-au-lait",
    "Thiakhri pâte d'arachide (ngalakh).jpg": "thiakhri-ngalakh",
}


def patch_image_sources() -> None:
    path = ROOT / "models" / "product_images.py"
    text = path.read_text(encoding="utf-8")
    if "Riz au lait (sombi).jpg" in text:
        print("IMAGE_SOURCES already patched")
        return
    anchor = '    "Maad en boîte.png": "maad-230g",\n'
    if anchor not in text:
        anchor = '    "Miel de fleurs — 500 g.jpg": "miel-fleurs-500g",\n'
    block = "\n".join(f'    "{fn}": "{slug}",' for fn, slug in SOURCES.items()) + "\n"
    if anchor not in text:
        raise SystemExit("anchor not found")
    path.write_text(text.replace(anchor, anchor + block, 1), encoding="utf-8")
    print("patched IMAGE_SOURCES")


def install() -> None:
    dest_dir = ROOT / "static" / "img" / "products"
    dest_dir.mkdir(parents=True, exist_ok=True)
    for filename, slug in SOURCES.items():
        src = ROOT / "img" / filename
        if not src.is_file():
            print("MISSING", repr(filename))
            continue
        dest = dest_dir / f"{slug}.jpg"
        shutil.copy2(src, dest)
        print("copied", filename, "->", dest.name)


def main() -> None:
    patch_image_sources()
    install()
    from app import app
    from models.product_images import sync_product_images
    from models.product import Product

    with app.app_context():
        sync_product_images(str(ROOT))
        for slug in SOURCES.values():
            p = Product.query.filter_by(slug=slug).first()
            print(slug, bool(p and p.image), p.image if p else None)


if __name__ == "__main__":
    main()
