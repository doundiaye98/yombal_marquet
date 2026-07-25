# -*- coding: utf-8 -*-
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from PIL import Image, ImageDraw, ImageFont

from models.catalogue_marketplace import BAGAGERIE_CATALOGUE
from models.constants import PRODUCT_CATEGORIES

NEW_SLUGS = {
    "sac-a-dos-voyage-40l",
    "sac-a-dos-laptop-15",
    "valise-moyenne-65cm",
    "set-valises-3-pieces",
    "sac-trolley-cabine",
    "besace-cuir-urbain",
    "sacoche-ceinture-voyage",
    "organiseur-bagage-cubes",
    "trousse-toilette-voyage",
    "housse-valise-protection",
    "sac-sport-duffel-35l",
}

OUT = ROOT / "static" / "img" / "products"
OUT.mkdir(parents=True, exist_ok=True)
NAVY = (0, 24, 88)
GOLD = (248, 192, 0)
CREAM = (247, 244, 236)

try:
    font_title = ImageFont.truetype("arial.ttf", 34)
    font_brand = ImageFont.truetype("arialbd.ttf", 20)
    font_cat = ImageFont.truetype("arial.ttf", 18)
    font_badge = ImageFont.truetype("arialbd.ttf", 40)
except OSError:
    font_title = font_brand = font_cat = font_badge = ImageFont.load_default()


def main():
    for product in BAGAGERIE_CATALOGUE:
        slug = product["slug"]
        if slug not in NEW_SLUGS:
            continue
        name = product["name"]
        cat = PRODUCT_CATEGORIES.get(product["category"], {})
        label = cat.get("label", "Bagagerie")
        img = Image.new("RGB", (900, 900), CREAM)
        draw = ImageDraw.Draw(img)
        draw.rectangle((0, 0, 900, 120), fill=NAVY)
        draw.rectangle((0, 112, 900, 120), fill=GOLD)
        draw.rectangle((0, 760, 900, 900), fill=NAVY)
        draw.rectangle((0, 752, 900, 760), fill=GOLD)
        brand = "YOMBAL MARKET"
        bbox = draw.textbbox((0, 0), brand, font=font_brand)
        draw.text(((900 - (bbox[2] - bbox[0])) / 2, 28), brand, fill=GOLD, font=font_brand)
        cat_line = f"{cat.get('emoji', '')}  {label}".strip()
        bbox = draw.textbbox((0, 0), cat_line, font=font_cat)
        draw.text(((900 - (bbox[2] - bbox[0])) / 2, 70), cat_line, fill=(255, 255, 255), font=font_cat)
        draw.ellipse((300, 280, 600, 580), fill=GOLD)
        badge = (product.get("icon") or "BAG")[:3]
        bbox = draw.textbbox((0, 0), badge, font=font_badge)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((450 - tw / 2, 430 - th / 2), badge, fill=NAVY, font=font_badge)
        words = name.split()
        lines, cur = [], ""
        for w in words:
            trial = f"{cur} {w}".strip()
            if draw.textbbox((0, 0), trial, font=font_title)[2] > 820 and cur:
                lines.append(cur)
                cur = w
            else:
                cur = trial
        if cur:
            lines.append(cur)
        y = 790 if len(lines) == 1 else 775
        for line in lines[:2]:
            bbox = draw.textbbox((0, 0), line, font=font_title)
            draw.text(((900 - (bbox[2] - bbox[0])) / 2, y), line, fill=(255, 255, 255), font=font_title)
            y += 44
        path = OUT / f"{slug}.jpg"
        img.save(path, "JPEG", quality=88, optimize=True)
        print("wrote", path.name)

    from app import app
    from models.constants import CATEGORY_BAGAGERIE
    from models.product import Product
    from models.product_images import sync_product_images
    from models.seed import sync_catalogue
    from services import rag_index

    with app.app_context():
        sync_catalogue()
        sync_product_images(app.root_path)
        n = Product.query.filter_by(category=CATEGORY_BAGAGERIE, is_active=True).count()
        print("bagagerie count", n)
        rag_index.index_all(force=False, local_only=True)
        print("rag chunks", rag_index.chunk_count())


if __name__ == "__main__":
    main()
