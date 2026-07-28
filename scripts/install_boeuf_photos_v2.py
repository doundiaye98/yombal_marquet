# -*- coding: utf-8 -*-
"""Installe les photos bœuf (mapping explicite préfixe → slug, sans fuzzy match)."""
from __future__ import annotations

import hashlib
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import app
from extensions import db
from models.product import Product
from models.product_images import PRODUCT_IMAGES, sync_product_images

IMG = ROOT / "img"
OUT = ROOT / "static" / "img" / "products"
PI_PATH = ROOT / "models" / "product_images.py"

# Lot courant uniquement (préfixes les plus spécifiques d'abord).
PREFIX_MAP: list[tuple[str, str]] = [
    ("Entrecôte de bœuf XXL Sélection du Boucher", "entrecote-boeuf-xxl-selection-boucher"),
    ("Entrecôte de bœuf Sélection du Boucher", "entrecote-boeuf-selection-boucher-x2"),
    ("Entrecôte de bœuf française XXL", "entrecote-boeuf-francaise-xxl"),
    ("Entrecôte de bœuf Charolais", "entrecote-boeuf-charolais"),
    ("Entrecôte XXL de bœuf Montbéliarde", "entrecote-xxl-boeuf-montbeliarde"),
    ("Faux-filet de bœuf Salers", "faux-filet-boeuf-salers"),
    ("Paleron de bœuf pour bourguignon", "paleron-boeuf-bourguignon"),
    ("Pavé de rumsteck de bœuf Salers x2", "pave-rumsteck-boeuf-salers-x2"),
    ("Picanha de bœuf Angus", "picanha-boeuf-angus"),
    ("Tournedos de rumsteck de bœuf Salers x2", "tournedos-rumsteck-boeuf-salers-x2"),
    ("Tournedos de filet de bœuf Salers x2", "tournedos-filet-boeuf-salers-x2"),
    ("Émincé de bœuf", "emince-boeuf-500g"),
    ("Steak de poire de bœuf x2", "steak-poire-boeuf-x2"),
    ("Steak tartare de bœuf français", "steak-tartare-boeuf-francais-180g"),
]

# Doublons connus (même octets qu'un autre produit) → ne pas installer
SKIP_SLUGS = {
    "filet-boeuf-francais-entier",  # = entrecôte française
    "roti-filet-boeuf-francais-800-900",  # = rôti Salers 1,15
}


def resolve_mappings() -> list[tuple[str, str, Path]]:
    files = [
        p
        for p in IMG.iterdir()
        if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
    ]
    used: set[Path] = set()
    resolved: list[tuple[str, str, Path]] = []
    for prefix, slug in PREFIX_MAP:
        if slug in SKIP_SLUGS:
            continue
        matches = [p for p in files if p.name.startswith(prefix) and p not in used]
        if len(matches) != 1:
            names = [m.name for m in matches]
            raise SystemExit(f"Ambigu/manquant pour {prefix!r} -> {slug}: {names}")
        used.add(matches[0])
        resolved.append((matches[0].name, slug, matches[0]))
    return resolved


def existing_static_hashes() -> dict[str, str]:
    hashes: dict[str, str] = {}
    for p in OUT.glob("*"):
        if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}:
            hashes[hashlib.md5(p.read_bytes()).hexdigest()] = p.name
    return hashes


def ensure_product_images_entries(pairs: list[tuple[str, str, str]]) -> None:
    """pairs: (filename, slug, rel_path under static/)"""
    text = PI_PATH.read_text(encoding="utf-8")
    changed = False

    raw_marker = '    "bavette-aloyau-x2": "img/products/bavette-aloyau-x2.jpg",'
    if raw_marker not in text:
        raise SystemExit("marker RAW introuvable")
    raw_inserts = []
    raw_section = text.split("PRODUCT_IMAGES = dict")[0]
    for _, slug, rel in pairs:
        line = f'    "{slug}": "{rel}",'
        if f'"{slug}":' not in raw_section:
            raw_inserts.append(line)
    if raw_inserts:
        text = text.replace(raw_marker, raw_marker + "\n" + "\n".join(raw_inserts), 1)
        changed = True

    src_marker = '    "Bavette d\'aloyau x10 — 1,6–1,7 kg.jpg": "bavette-aloyau-x10",'
    if src_marker not in text:
        raise SystemExit("marker IMAGE_SOURCES introuvable")
    src_inserts = []
    for fname, slug, _ in pairs:
        if f'"{fname}":' not in text:
            src_inserts.append(f'    "{fname}": "{slug}",')
    if src_inserts:
        text = text.replace(src_marker, src_marker + "\n" + "\n".join(src_inserts), 1)
        changed = True

    if changed:
        PI_PATH.write_text(text, encoding="utf-8")
        print(f"updated {PI_PATH.name}")
    else:
        print("product_images.py deja a jour")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    resolved = resolve_mappings()
    hashes = existing_static_hashes()
    log: list[str] = []
    installed: list[tuple[str, str, str]] = []

    for fname, slug, src in resolved:
        digest = hashlib.md5(src.read_bytes()).hexdigest()
        if digest in hashes and not hashes[digest].startswith(slug + "."):
            log.append(f"SKIP DUP {slug} <- {fname} (== {hashes[digest]})")
            continue
        ext = src.suffix.lower()
        if ext == ".jpeg":
            ext = ".jpg"
        dest = OUT / f"{slug}{ext}"
        shutil.copy2(src, dest)
        rel = f"img/products/{slug}{ext}"
        PRODUCT_IMAGES[slug] = rel
        installed.append((fname, slug, rel))
        hashes[digest] = dest.name
        log.append(f"OK {slug} <- {fname} ({src.stat().st_size} o)")

    if installed:
        ensure_product_images_entries(installed)

    with app.app_context():
        for _, slug, rel in installed:
            product = Product.query.filter_by(slug=slug).first()
            if not product:
                log.append(f"WARN produit absent: {slug}")
                continue
            if product.image != rel:
                product.image = rel
        db.session.commit()
        sync_product_images(str(ROOT))

    out = ROOT / "scripts" / "_install_boeuf_v2_log.txt"
    out.write_text("\n".join(log), encoding="utf-8")
    print(f"installed {len(installed)} photos")
    print("\n".join(log))


if __name__ == "__main__":
    main()
