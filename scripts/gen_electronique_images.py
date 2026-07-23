# -*- coding: utf-8 -*-
"""Génère des visuels produits pour le catalogue électronique."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "static" / "img" / "yombal-electronique.jpg"
OUT = ROOT / "static" / "img" / "products"
OUT.mkdir(parents=True, exist_ok=True)

PRODUCTS = [
    ("ecouteurs-bluetooth-yombal", "Ecouteurs Bluetooth", "BT"),
    ("batterie-externe-20000mah", "Batterie 20000 mAh", "20K"),
    ("chargeur-solaire-portable", "Chargeur solaire", "SOL"),
    ("enceinte-bluetooth-portable", "Enceinte Bluetooth", "SON"),
    ("montre-connectee-yombal", "Montre connectee", "WATCH"),
    ("ampoules-led-pack-4", "Ampoules LED x4", "LED"),
    ("lampe-led-rechargeable", "Lampe LED", "LAMP"),
    ("adaptateur-voyage-multiprise", "Adaptateur voyage", "USB"),
    ("cable-usb-c-pack-2", "Cables USB-C x2", "CABLE"),
    ("tablette-android-10", "Tablette Android 10", "TAB"),
    ("clavier-bluetooth-compact", "Clavier Bluetooth", "KB"),
    ("souris-sans-fil-ergonomique", "Souris sans fil", "MOUSE"),
    ("webcam-hd-1080p", "Webcam HD 1080p", "CAM"),
    ("casque-audio-confort", "Casque audio", "HEAD"),
    ("coque-smartphone-protection", "Coque smartphone", "CASE"),
    ("support-telephone-voiture", "Support voiture", "CAR"),
    ("multiprise-parasurtenseur", "Multiprise USB", "POWER"),
    ("ventilateur-usb-portable", "Ventilateur USB", "FAN"),
    ("radio-fm-rechargeable", "Radio FM", "FM"),
    ("anneau-lumineux-led", "Anneau lumineux", "RING"),
]

NAVY = (0, 24, 88)
GOLD = (248, 192, 0)


def main():
    base = Image.open(SRC).convert("RGB")
    w, h = base.size
    side = min(w, h)
    left = (w - side) // 2
    top = max(0, (h - side) // 2 - side // 10)
    base = base.crop((left, top, left + side, top + side)).resize(
        (900, 900), Image.Resampling.LANCZOS
    )

    try:
        font_title = ImageFont.truetype("arial.ttf", 48)
        font_brand = ImageFont.truetype("arialbd.ttf", 22)
        font_badge = ImageFont.truetype("arialbd.ttf", 36)
    except OSError:
        font_title = ImageFont.load_default()
        font_brand = font_title
        font_badge = font_title

    for slug, label, badge in PRODUCTS:
        img = base.copy()
        img = ImageEnhance.Brightness(img).enhance(0.52)
        img = ImageEnhance.Color(img).enhance(0.8)
        overlay = Image.new("RGBA", img.size, (0, 24, 88, 120))
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
        draw = ImageDraw.Draw(img)

        draw.rectangle((0, 720, 900, 900), fill=NAVY)
        draw.rectangle((0, 712, 900, 720), fill=GOLD)

        brand = "YOMBAL ELECTRONIQUE"
        bbox = draw.textbbox((0, 0), brand, font=font_brand)
        tw = bbox[2] - bbox[0]
        draw.text(((900 - tw) / 2, 40), brand, fill=GOLD, font=font_brand)

        draw.ellipse((350, 300, 550, 500), fill=GOLD)
        bbox = draw.textbbox((0, 0), badge, font=font_badge)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((450 - tw / 2, 400 - th / 2), badge, fill=NAVY, font=font_badge)

        words = label.split()
        lines = []
        if len(words) <= 2:
            lines = [label]
        else:
            mid = len(words) // 2
            lines = [" ".join(words[:mid]), " ".join(words[mid:])]
        y = 760 if len(lines) == 1 else 745
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font_title)
            tw = bbox[2] - bbox[0]
            draw.text(((900 - tw) / 2, y), line, fill=(255, 255, 255), font=font_title)
            y += 52

        path = OUT / f"{slug}.jpg"
        img.save(path, "JPEG", quality=88, optimize=True)
        print(f"wrote {path.name} ({path.stat().st_size})")

    print(f"done {len(PRODUCTS)}")


if __name__ == "__main__":
    main()
