# -*- coding: utf-8 -*-
"""Ajoute sombi, thiakhri au lait et ngalakh au catalogue."""
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

BLOCK = r'''
    _lf(
        "UD-SOMBI",
        "sombi-riz-au-lait",
        "Riz au lait (sombi)",
        "Dessert sénégalais crémeux — riz cuit dans le lait sucré.",
        CATEGORY_DESSERTS,
        "🍚",
        3.5,
        "400 g",
        description_extra=(
            "Le sombi (riz au lait) est un classique du goûter et des fêtes : "
            "onctueux, parfumé à la vanille ou à la cannelle selon la préparation."
        ),
        ingredients="Riz, lait, sucre, arômes (selon lot).",
        allergens="Lait.",
        usage_tips="Servir frais. Réchauffer doucement si besoin.",
        conservation="Au frais après ouverture. Consommer rapidement.",
    ),
    _lf(
        "UD-THIAK-LAIT",
        "thiakhri-au-lait",
        "Thiakhri au lait",
        "Arraw de mil au lait — dessert onctueux et nourrissant.",
        CATEGORY_DESSERTS,
        "🍮",
        3.5,
        "400 g",
        description_extra=(
            "Thiakhri (dégué) préparé au lait : texture légère, goût doux du mil. "
            "Idéal au petit-déjeuner ou en dessert."
        ),
        ingredients="Arraw de mil, lait, sucre (selon lot).",
        allergens="Lait. Peut contenir des traces de gluten selon préparation.",
        usage_tips="Servir bien frais. Ajouter raisins ou fruits secs selon goût.",
        conservation="Au frais après ouverture.",
    ),
    _lf(
        "UD-NGALAKH",
        "thiakhri-ngalakh",
        "Thiakhri pâte d'arachide (ngalakh)",
        "Dessert de mil à la pâte d'arachide — ngalakh traditionnel.",
        CATEGORY_DESSERTS,
        "🥜",
        4.5,
        "400 g",
        description_extra=(
            "Le ngalakh marie thiakhri (arraw de mil), pâte d'arachide et souvent baobab : "
            "riche, sucré-salé subtil, incontournable des tables sénégalaises."
        ),
        ingredients="Arraw de mil, pâte d'arachide, sucre, baobab (selon lot).",
        allergens="Arachides. Lait possible selon préparation.",
        usage_tips="Servir frais. Remuer avant dégustation si la pâte se dépose.",
        conservation="Au frais après ouverture.",
    ),
'''


def patch_catalogue():
    path = ROOT / "models" / "catalogue_labelafrik.py"
    text = path.read_text(encoding="utf-8")
    if "sombi-riz-au-lait" in text:
        print("catalogue already patched")
        return
    needle = '    _lf("UD-RIZ-C2", "riz-casse-2x-1kg", "Riz cassé 2 fois", "Sac 1 kg — absorption des sauces.", CATEGORY_CEREALES, "🌾", 1.6, "1 kg"),\n]'
    if needle not in text:
        raise SystemExit("needle not found")
    text = text.replace(
        needle,
        '    _lf("UD-RIZ-C2", "riz-casse-2x-1kg", "Riz cassé 2 fois", "Sac 1 kg — absorption des sauces.", CATEGORY_CEREALES, "🌾", 1.6, "1 kg"),'
        + BLOCK
        + "]",
        1,
    )
    path.write_text(text, encoding="utf-8")
    print("catalogue patched")


def patch_names():
    path = ROOT / "models" / "product_names.py"
    text = path.read_text(encoding="utf-8")
    if "sombi-riz-au-lait" in text:
        print("names already patched")
        return
    anchor = '    "thiakry-400g": "Thiakhry — 400 g",\n'
    extra = (
        '    "sombi-riz-au-lait": "Riz au lait (sombi) — 400 g",\n'
        '    "thiakhri-au-lait": "Thiakhri au lait — 400 g",\n'
        '    "thiakhri-ngalakh": "Thiakhri pâte d\'arachide (ngalakh) — 400 g",\n'
    )
    if anchor not in text:
        raise SystemExit("names anchor not found")
    path.write_text(text.replace(anchor, anchor + extra, 1), encoding="utf-8")
    print("names patched")


def patch_images():
    path = ROOT / "models" / "product_images.py"
    text = path.read_text(encoding="utf-8")
    if "sombi-riz-au-lait" in text:
        print("images already patched")
        return
    anchor = '    "thiakry-400g": "img/products/thiakry-400g.jpg",\n'
    extra = (
        '    "sombi-riz-au-lait": "img/products/sombi-riz-au-lait.jpg",\n'
        '    "thiakhri-au-lait": "img/products/thiakhri-au-lait.jpg",\n'
        '    "thiakhri-ngalakh": "img/products/thiakhri-ngalakh.jpg",\n'
    )
    if anchor not in text:
        raise SystemExit("images anchor not found")
    path.write_text(text.replace(anchor, anchor + extra, 1), encoding="utf-8")
    print("images map patched")


def make_placeholders():
    from PIL import Image, ImageDraw, ImageFont

    out = ROOT / "static" / "img" / "products"
    out.mkdir(parents=True, exist_ok=True)
    # Prefer existing thiakry photo as visual base for related desserts
    base = out / "thiakry-400g.jpg"
    products = [
        ("sombi-riz-au-lait", "Sombi", "🍚"),
        ("thiakhri-au-lait", "Thiakhri lait", "🍮"),
        ("thiakhri-ngalakh", "Ngalakh", "🥜"),
    ]
    for slug, label, icon in products:
        dest = out / f"{slug}.jpg"
        if base.is_file() and slug != "sombi-riz-au-lait":
            shutil.copy2(base, dest)
            print("copied thiakry ->", dest.name)
            continue
        # simple branded placeholder
        img = Image.new("RGB", (900, 900), (247, 244, 236))
        draw = ImageDraw.Draw(img)
        draw.rectangle((0, 0, 900, 120), fill=(0, 24, 88))
        draw.rectangle((0, 760, 900, 900), fill=(0, 24, 88))
        draw.rectangle((0, 112, 900, 120), fill=(248, 192, 0))
        draw.rectangle((0, 752, 900, 760), fill=(248, 192, 0))
        try:
            font = ImageFont.truetype("arial.ttf", 36)
            font_b = ImageFont.truetype("seguiemj.ttf", 72)
        except OSError:
            font = font_b = ImageFont.load_default()
        draw.ellipse((300, 280, 600, 580), fill=(248, 192, 0))
        bbox = draw.textbbox((0, 0), icon, font=font_b)
        draw.text((450 - (bbox[2] - bbox[0]) / 2, 400 - (bbox[3] - bbox[1]) / 2), icon, fill=(0, 24, 88), font=font_b)
        bbox = draw.textbbox((0, 0), label, font=font)
        draw.text((450 - (bbox[2] - bbox[0]) / 2, 820), label, fill=(255, 255, 255), font=font)
        img.save(dest, quality=88)
        print("placeholder", dest.name)


def main():
    patch_catalogue()
    patch_names()
    patch_images()
    make_placeholders()
    from app import app
    from models.seed import sync_catalogue
    from models.product_images import sync_product_images
    from models.product import Product

    with app.app_context():
        sync_catalogue()
        sync_product_images(str(ROOT))
        for slug in ("sombi-riz-au-lait", "thiakhri-au-lait", "thiakhri-ngalakh"):
            p = Product.query.filter_by(slug=slug).first()
            print(slug, "->", p.name if p else None, p.price_cents if p else None, p.category if p else None)


if __name__ == "__main__":
    main()
