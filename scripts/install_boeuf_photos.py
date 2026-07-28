# -*- coding: utf-8 -*-
"""Installe les photos bœuf depuis img/ vers static/img/products/."""
from __future__ import annotations

import re
import shutil
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def norm(s: str) -> str:
    s = s.lower().replace("œ", "oe")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("—", "-").replace("–", "-").replace("'", "'").replace("'", "'")
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


# Explicit mappings for truncated / ambiguous filenames
EXPLICIT = {
    "Bavette d'.jpg": "bavette-aloyau-x2",  # may override if better match exists
    "Bavette d'aloyau x10 — 1,6–1,7 kg.jpg": "bavette-aloyau-x10",
    "Bavette d'aloyau x2 — 300–400 g.jpg": "bavette-aloyau-x2",
    "Carré Box 100% bœuf — 3,85–4,85 kg.jpg": "carre-box-boeuf-100",
    "Carré Box régime protéiné avec rôtis — 4.jpg": "carre-box-regime-proteine-rotis",
    "Carré Box régime.jpg": "carre-box-regime-proteine",
    "Carré Box viande familial authentique —.jpg": "carre-box-viande-familial-authentique",
}


def score_match(filename: str, slug: str, name: str) -> int:
    fn = norm(Path(filename).stem)
    sl = norm(slug.replace("-", " "))
    nm = norm(name)
    score = 0
    # token overlap with slug
    ftoks = set(fn.split())
    stoks = set(sl.split())
    ntoks = set(nm.split())
    score += 3 * len(ftoks & stoks)
    score += 2 * len(ftoks & ntoks)
    # bonus if weight fragment present in both
    for t in ftoks:
        if any(c.isdigit() for c in t) and t in stoks.union(ntoks):
            score += 4
    return score


def main():
    from app import app
    from models.product import Product
    from models.product_images import sync_product_images

    img_dir = ROOT / "img"
    dest_dir = ROOT / "static" / "img" / "products"
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Candidates: files that look like meat product photos (not gallery/resto/electronics)
    skip = (
        "gallery-",
        "resto-",
        "electronics-",
        "yombal-",
        "Fataya",
        "background",
    )
    files = []
    for p in img_dir.iterdir():
        if not p.is_file() or p.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        if any(p.name.startswith(s) or s in p.name for s in skip):
            continue
        files.append(p)

    with app.app_context():
        products = Product.query.filter_by(category="viandes", is_active=True).all()
        # Prefer beef + boxes + related
        beefy = []
        for p in products:
            s = p.slug or ""
            if any(
                k in s
                for k in (
                    "boeuf",
                    "bavette",
                    "entrecote",
                    "cote-boeuf",
                    "filet-boeuf",
                    "onglet",
                    "roti-boeuf",
                    "roti-filet",
                    "tomahawk",
                    "picanha",
                    "paleron",
                    "emince",
                    "gite",
                    "rumsteck",
                    "tournedos",
                    "faux-filet",
                    "tartare",
                    "fondue",
                    "angus",
                    "wagyu",
                    "poire",
                    "carre-box",
                    "queue-boeuf",
                    "morceaux-boeuf",
                    "foie-boeuf",
                    "tripes",
                    "pieds-boeuf",
                    "cotes-boeuf",
                    "steak-hache",
                )
            ):
                beefy.append(p)

        # Also include products that already have no image among all viandes if filename matches
        products_by_slug = {p.slug: p for p in products}

        mappings: dict[str, str] = {}  # filename -> slug

        # 1) Explicit
        on_disk = {p.name: p for p in files}
        for fname, slug in EXPLICIT.items():
            if fname in on_disk and slug in products_by_slug:
                mappings[fname] = slug

        # 2) Auto-match remaining files to products without image or all beefy
        used_slugs = set(mappings.values())
        for p in files:
            if p.name in mappings:
                continue
            best = None
            best_score = 0
            for prod in beefy:
                if prod.slug in used_slugs:
                    continue
                sc = score_match(p.name, prod.slug, prod.name or "")
                if sc > best_score:
                    best_score = sc
                    best = prod
            # threshold: need decent overlap
            if best and best_score >= 6:
                mappings[p.name] = best.slug
                used_slugs.add(best.slug)

        print(f"matches: {len(mappings)}")
        for fname, slug in sorted(mappings.items(), key=lambda x: x[1]):
            print(f"  {slug} <= {fname}")

        # Copy + patch product_images.py
        pi_path = ROOT / "models" / "product_images.py"
        text = pi_path.read_text(encoding="utf-8")
        changed = False

        for fname, slug in mappings.items():
            src = on_disk[fname]
            dest = dest_dir / f"{slug}.jpg"
            shutil.copy2(src, dest)
            print("copied", dest.name)

            img_line = f'    "{slug}": "img/products/{slug}.jpg",\n'
            if f'"{slug}": "img/products/' not in text:
                for anchor in (
                    '    "fataya-viande-10": "img/products/fataya-viande-10.jpg",\n',
                    '    "biscuits-gem": "img/products/biscuits-gem.jpg",\n',
                ):
                    if anchor in text:
                        text = text.replace(anchor, anchor + img_line, 1)
                        changed = True
                        break

            src_line = f'    "{fname}": "{slug}",\n'
            if f'"{fname}"' not in text:
                for anchor in (
                    '    "Fataya viande.jpg": "fataya-viande-10",\n',
                    '    "Biscuits Gem.jpg": "biscuits-gem",\n',
                ):
                    if anchor in text:
                        text = text.replace(anchor, anchor + src_line, 1)
                        changed = True
                        break

        if changed:
            pi_path.write_text(text, encoding="utf-8")
            print("product_images.py updated")

        sync_product_images(str(ROOT))

        ok = 0
        for slug in mappings.values():
            p = products_by_slug[slug]
            # refresh
            p = Product.query.filter_by(slug=slug).first()
            f = ROOT / "static" / (p.image or "").replace("/", "\\")
            status = "OK" if p and p.image and f.is_file() else "MISSING"
            if status == "OK":
                ok += 1
            print(status, slug, "->", getattr(p, "image", None))
        print(f"done {ok}/{len(mappings)}")

        unmatched = [p.name for p in files if p.name not in mappings and any(
            k in p.name.lower() for k in ("bavette", "box", "bœuf", "boeuf", "entrec", "côte de", "filet", "salers", "angus")
        )]
        if unmatched:
            print("UNMATCHED beef-ish files:")
            for n in unmatched:
                print(" ", repr(n))


if __name__ == "__main__":
    main()
