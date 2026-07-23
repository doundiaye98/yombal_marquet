# -*- coding: utf-8 -*-
"""Copie les photos produits électronique depuis img/ vers static/img/products/."""
from __future__ import annotations

import re
import shutil
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "img"
OUT_DIR = ROOT / "static" / "img" / "products"

# slug → mots-clés ASCII attendus dans le nom de fichier (ordre de priorité)
MAPPINGS: list[tuple[str, tuple[str, ...]]] = [
    ("ecouteurs-bluetooth-yombal", ("ecouteurs bluetooth", "ecouteurs")),
    ("batterie-externe-20000mah", ("batterie externe",)),
    ("chargeur-solaire-portable", ("chargeur solaire",)),
    ("enceinte-bluetooth-portable", ("enceinte bluetooth",)),
    ("montre-connectee-yombal", ("montre connect",)),
    ("ampoules-led-pack-4", ("ampoules led",)),
    ("lampe-led-rechargeable", ("lampe led",)),
    ("adaptateur-voyage-multiprise", ("adaptateur voyage",)),
    ("cable-usb-c-pack-2", ("cables usb-c", "cable usb-c", "cables usb", "usb-c")),
    ("tablette-android-10", ("tablette android",)),
    ("clavier-bluetooth-compact", ("clavier bluetooth",)),
    ("souris-sans-fil-ergonomique", ("souris sans fil",)),
    ("webcam-hd-1080p", ("webcam",)),
    ("casque-audio-confort", ("casque audio",)),
    ("coque-smartphone-protection", ("coque smartphone",)),
    ("support-telephone-voiture", ("support telephone", "support tel")),
    ("multiprise-parasurtenseur", ("multiprise parasurtenseur",)),
    ("ventilateur-usb-portable", ("ventilateur usb", "ventilateur")),
    ("radio-fm-rechargeable", ("radio fm",)),
    ("anneau-lumineux-led", ("anneau lumineux",)),
]


def fold(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower().replace("œ", "oe")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    candidates = [
        p
        for p in SRC_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
    ]
    folded = [(p, fold(p.name)) for p in candidates]
    used: set[Path] = set()

    for slug, keys in MAPPINGS:
        match = None
        for key in keys:
            key_f = fold(key)
            for path, name_f in folded:
                if path in used:
                    continue
                if key_f in name_f:
                    match = path
                    break
            if match:
                break
        if not match:
            print(f"MISSING {slug} keys={keys}")
            continue
        dest = OUT_DIR / f"{slug}.jpg"
        # convert/normalize to jpg if needed
        if match.suffix.lower() in {".jpg", ".jpeg"}:
            shutil.copy2(match, dest)
        else:
            from PIL import Image

            img = Image.open(match).convert("RGB")
            img.save(dest, "JPEG", quality=90, optimize=True)
        used.add(match)
        print(f"OK {slug} <- {match.name}")

    print(f"done mapped={len(used)}")


if __name__ == "__main__":
    main()
