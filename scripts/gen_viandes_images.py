# -*- coding: utf-8 -*-
"""Génère des visuels placeholder pour les nouvelles viandes halal."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from PIL import Image, ImageDraw, ImageFont

from models.catalogue_labelafrik import LABELAFRIK_VIANDES
from models.constants import PRODUCT_CATEGORIES

OUT = ROOT / "static" / "img" / "products"
OUT.mkdir(parents=True, exist_ok=True)

NAVY = (0, 24, 88)
GOLD = (248, 192, 0)
CREAM = (247, 244, 236)
SKIP = {
    "ailes-poulet-texmex-halal",
    "corned-beef-halal",
    "cuisses-poulet-halal-5kg",
    "cuisses-poulet-halal-10kg",
    "pilons-poulet-halal-5kg",
    "ailes-poulet-halal-5kg",
    "ailes-poulet-texmex-1kg",
    "poule-fumee-1kg",
    "poule-entiere-halal",
    "ailerons-dinde-halal-1kg",
    "queue-boeuf-1kg",
    "morceaux-boeuf-1kg",
}


def main():
    try:
        font_title = ImageFont.truetype("arial.ttf", 34)
        font_brand = ImageFont.truetype("arialbd.ttf", 20)
        font_cat = ImageFont.truetype("arial.ttf", 18)
    except OSError:
        font_title = font_brand = font_cat = ImageFont.load_default()

    maps = []
    for product in LABELAFRIK_VIANDES:
        slug = product["slug"]
        if slug in SKIP:
            continue
        path = OUT / f"{slug}.jpg"
        if path.is_file():
            continue
        name = product["name"]
        cat = PRODUCT_CATEGORIES.get(product["category"], {})
        img = Image.new("RGB", (900, 900), CREAM)
        draw = ImageDraw.Draw(img)
        draw.rectangle((0, 0, 900, 120), fill=NAVY)
        draw.rectangle((0, 112, 900, 120), fill=GOLD)
        draw.rectangle((0, 760, 900, 900), fill=NAVY)
        draw.rectangle((0, 752, 900, 760), fill=GOLD)
        brand = "YOMBAL MARKET"
        bbox = draw.textbbox((0, 0), brand, font=font_brand)
        draw.text(((900 - (bbox[2] - bbox[0])) / 2, 28), brand, fill=GOLD, font=font_brand)
        cat_line = f"{cat.get('emoji', '')}  {cat.get('label', '')}".strip()
        bbox = draw.textbbox((0, 0), cat_line, font=font_cat)
        draw.text(((900 - (bbox[2] - bbox[0])) / 2, 70), cat_line, fill=(255, 255, 255), font=font_cat)
        draw.ellipse((300, 280, 600, 580), fill=GOLD)
        badge = (product.get("icon") or "•")[:2]
        try:
            font_badge = ImageFont.truetype("seguiemj.ttf", 72)
        except OSError:
            font_badge = font_title
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
        y = 800
        for ln in lines[:3]:
            bbox = draw.textbbox((0, 0), ln, font=font_title)
            draw.text(((900 - (bbox[2] - bbox[0])) / 2, y), ln, fill=(255, 255, 255), font=font_title)
            y += 36
        img.save(path, quality=88)
        maps.append(slug)
        print("wrote", path.name)
    print("count", len(maps))
    return maps


if __name__ == "__main__":
    main()
