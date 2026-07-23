# -*- coding: utf-8 -*-
"""Génère des visuels placeholder pour le catalogue marketplace."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from PIL import Image, ImageDraw, ImageFont

from models.catalogue_marketplace import MARKETPLACE_CATALOGUE
from models.constants import PRODUCT_CATEGORIES

OUT = ROOT / "static" / "img" / "products"
OUT.mkdir(parents=True, exist_ok=True)

NAVY = (0, 24, 88)
GOLD = (248, 192, 0)
CREAM = (247, 244, 236)


def main():
    try:
        font_title = ImageFont.truetype("arial.ttf", 36)
        font_brand = ImageFont.truetype("arialbd.ttf", 20)
        font_cat = ImageFont.truetype("arial.ttf", 18)
    except OSError:
        font_title = ImageFont.load_default()
        font_brand = font_title
        font_cat = font_title

    for product in MARKETPLACE_CATALOGUE:
        slug = product["slug"]
        name = product["name"]
        cat = PRODUCT_CATEGORIES.get(product["category"], {})
        label = cat.get("label", product["category"])
        emoji = cat.get("emoji", "")

        img = Image.new("RGB", (900, 900), CREAM)
        draw = ImageDraw.Draw(img)
        draw.rectangle((0, 0, 900, 120), fill=NAVY)
        draw.rectangle((0, 112, 900, 120), fill=GOLD)
        draw.rectangle((0, 760, 900, 900), fill=NAVY)
        draw.rectangle((0, 752, 900, 760), fill=GOLD)

        brand = "YOMBAL MARKET"
        bbox = draw.textbbox((0, 0), brand, font=font_brand)
        draw.text(((900 - (bbox[2] - bbox[0])) / 2, 28), brand, fill=GOLD, font=font_brand)

        cat_line = f"{emoji}  {label}".strip()
        bbox = draw.textbbox((0, 0), cat_line, font=font_cat)
        draw.text(((900 - (bbox[2] - bbox[0])) / 2, 70), cat_line, fill=(255, 255, 255), font=font_cat)

        draw.ellipse((300, 280, 600, 580), fill=GOLD)
        badge = (product.get("icon") or "•")[:2]
        try:
            font_badge = ImageFont.truetype("seguiemj.ttf", 72)
        except OSError:
            font_badge = ImageFont.truetype("arialbd.ttf", 48) if hasattr(ImageFont, "truetype") else font_title
            try:
                font_badge = ImageFont.truetype("arialbd.ttf", 48)
            except OSError:
                font_badge = font_title
        bbox = draw.textbbox((0, 0), badge, font=font_badge)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((450 - tw / 2, 430 - th / 2), badge, fill=NAVY, font=font_badge)

        # wrap name
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
            tw = bbox[2] - bbox[0]
            draw.text(((900 - tw) / 2, y), line, fill=(255, 255, 255), font=font_title)
            y += 44

        path = OUT / f"{slug}.jpg"
        img.save(path, "JPEG", quality=88, optimize=True)
        print("wrote", path.name)

    print("done", len(MARKETPLACE_CATALOGUE))


if __name__ == "__main__":
    main()
