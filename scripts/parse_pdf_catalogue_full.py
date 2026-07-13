#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Parse complet du PDF catalogue → JSON + comparaison avec catalogue_labelafrik."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "img" / "Catalogue LABEL (1).pdf"
OUT = ROOT / "data" / "pdf_catalogue_full.json"

SKIP_NAMES = {
    "u n i v e r s  d i a s p o r a",
    "univers diaspora",
    "riz",
    "pates et farines",
    "huiles et graisses",
    "snacks et patisseries",
    "legumineuses",
    "condiments",
    "fruits secs",
    "boissons",
    "conserves",
    "poissons",
    "viandes",
    "surgeles",
    "prix",
}

CATEGORY_MARKERS = {
    "RIZ": "cereales",
    "PÂTES ET FARINES": "cereales",
    "PATES ET FARINES": "cereales",
    "HUILES ET GRAISSES": "huiles",
    "SNACKS ET PÂTISSERIES": "snacks",
    "SNACKS ET PATISSERIES": "snacks",
    "LÉGUMINEUSES": "legumineuses",
    "LEGUMINEUSES": "legumineuses",
    "CONDIMENTS": "condiments",
    "FRUITS SECS": "fruits_secs",
    "BOISSONS": "boissons",
    "CONSERVES": "conserves",
    "POISSONS": "conserves",
    "VIANDES": "alimentaire",
    "SURGELÉS": "alimentaire",
    "SURGELES": "alimentaire",
}


def slugify(name: str) -> str:
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def parse_price(text: str) -> float | None:
    m = re.search(r"(\d(?:\s*\d)*)\s*,\s*(\d(?:\s*\d)*)\s*€", text)
    if m:
        return round(float(f"{m.group(1).replace(' ', '')}.{m.group(2).replace(' ', '')}"), 2)
    m = re.search(r"(?<!\d)(\d{1,3})\s*€", text)
    if m:
        return float(m.group(1))
    return None


def normalize_name(name: str) -> str:
    name = re.sub(r"\s+", " ", name).strip()
    if name.isupper():
        return name.title()
    return name


def extract_from_pdf() -> list[dict]:
    from pypdf import PdfReader

    reader = PdfReader(str(PDF))
    items: list[dict] = []
    current_cat = ""

    for page_no, page in enumerate(reader.pages, start=1):
        raw = page.extract_text() or ""
        lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]

        # Pages fiches produit (un seul gros titre + un prix)
        if page_no <= 21 and "LabelAfrik" in raw and raw.count("€") <= 2:
            price = parse_price(raw)
            title = None
            for ln in lines:
                clean = ln.replace(" ", "")
                if len(ln) >= 4 and ln.upper() == ln and "UNIVERS" not in clean and "PRIX" not in ln:
                    if re.match(r"^[A-ZÉÈÊÀÂÄÙÛÜÎÏÔÖÇ\s\-']+$", ln):
                        title = normalize_name(ln)
                        break
            if title and price and 0 < price < 200:
                items.append(
                    {
                        "page": page_no,
                        "category": current_cat or "phares",
                        "name": title,
                        "price_euros": price,
                        "description": "",
                        "source": "fiche",
                    }
                )
            continue

        # Pages liste multi-produits
        block_lines: list[str] = []
        for ln in lines:
            upper = ln.upper().replace("  ", " ")
            if upper in CATEGORY_MARKERS:
                current_cat = CATEGORY_MARKERS[upper]
                continue
            if ln.startswith("U N I") or "FAIRE DE VOS" in upper:
                continue

            price = parse_price(ln)
            if price is not None and block_lines:
                name = None
                desc = ""
                for bl in reversed(block_lines):
                    bl_up = bl.upper()
                    if bl_up in CATEGORY_MARKERS or bl.startswith("U N I"):
                        continue
                    if len(bl) >= 5 and bl_up == bl and re.match(r"^[A-ZÉÈÊÀÂÄÙÛÜÎÏÔÖÇ0-9\s\-'/&]+$", bl):
                        name = normalize_name(bl)
                        break
                if not name:
                    for bl in block_lines:
                        if bl.lower().startswith(("c'est", "ce sont", "c est", "c'est")):
                            desc = bl
                            break
                    for bl in block_lines:
                        if bl != desc and len(bl) > 8 and not bl.startswith("U N"):
                            if parse_price(bl) is None and "€" not in bl:
                                name = normalize_name(bl)
                                break
                if name and name.lower() not in SKIP_NAMES and 0 < price < 500:
                    if not desc:
                        desc = next(
                            (bl for bl in block_lines if bl.lower().startswith(("c'est", "ce sont"))),
                            "",
                        )
                    items.append(
                        {
                            "page": page_no,
                            "category": current_cat or "alimentaire",
                            "name": name,
                            "price_euros": price,
                            "description": desc[:240],
                            "source": "liste",
                        }
                    )
                block_lines = []
            else:
                if "€" not in ln and "Prix" not in ln:
                    block_lines.append(ln)
                    if len(block_lines) > 8:
                        block_lines = block_lines[-8:]

    dedup: dict[tuple, dict] = {}
    for row in items:
        key = (row["name"].lower(), row["price_euros"])
        dedup[key] = row
    return sorted(dedup.values(), key=lambda r: r["name"].lower())


def load_site_catalogue() -> list[dict]:
    sys.path.insert(0, str(ROOT))
    from models.catalogue_labelafrik import LABELAFRIK_CATALOGUE, LABELAFRIK_UPDATES

    rows = list(LABELAFRIK_CATALOGUE)
    for slug, row in LABELAFRIK_UPDATES.items():
        rows.append({**row, "slug": slug})
    return [
        {
            "slug": r["slug"],
            "name": r["name"],
            "price_euros": r["price_cents"] / 100,
            "category": r["category"],
        }
        for r in rows
    ]


def main() -> int:
    if not PDF.exists():
        print(f"PDF manquant: {PDF}", file=sys.stderr)
        return 1

    pdf_rows = extract_from_pdf()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(pdf_rows, ensure_ascii=False, indent=2), encoding="utf-8")

    site_rows = load_site_catalogue()
    site_by_price: dict[float, list] = {}
    for r in site_rows:
        site_by_price.setdefault(r["price_euros"], []).append(r)

    pdf_names = {r["name"].lower() for r in pdf_rows}
    site_names = {r["name"].lower() for r in site_rows}

    missing_in_site = [r for r in pdf_rows if r["name"].lower() not in site_names]
    extra_on_site = [r for r in site_rows if r["name"].lower() not in pdf_names]

    print(f"PDF: {len(pdf_rows)} produits uniques")
    print(f"Site LabelAfrik: {len(site_rows)} produits")
    print(f"Manquants sur le site: {len(missing_in_site)}")
    print(f"Sur le site mais pas clairement dans PDF: {len(extra_on_site)}")
    print("\n--- Manquants (extrait) ---")
    for r in missing_in_site[:40]:
        print(f"  {r['price_euros']:>7.2f} €  {r['name']}")
    if len(missing_in_site) > 40:
        print(f"  ... +{len(missing_in_site)-40}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
