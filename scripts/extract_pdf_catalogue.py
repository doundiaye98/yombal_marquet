#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Extrait produits + prix du PDF catalogue LabelAfrik / Univers Diaspora."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "img" / "Catalogue LABEL (1).pdf"
OUT = ROOT / "data" / "catalogue_pdf_extracted.json"


def parse_euro_price(text: str) -> float | None:
    m = re.search(r"(\d(?:\s*\d)*)\s*,\s*(\d(?:\s*\d)*)\s*€", text)
    if m:
        euros = m.group(1).replace(" ", "")
        cents = m.group(2).replace(" ", "")
        return round(float(f"{euros}.{cents}"), 2)
    m = re.search(r"(?<!\d)(\d{1,3})\s*€", text)
    if m:
        return float(m.group(1))
    return None


def extract_items() -> list[dict]:
    from pypdf import PdfReader

    reader = PdfReader(str(PDF))
    items: list[dict] = []

    for page_no, page in enumerate(reader.pages, start=1):
        raw = page.extract_text() or ""
        if "UNIVERS" not in raw.upper().replace(" ", ""):
            continue

        # Pages liste (plusieurs produits)
        if re.search(r"\d\s*,\s*\d\s*€", raw):
            parts = re.split(r"(?=\n[A-ZÉÈÊÀÂÙ][A-ZÉÈÊÀÂÙ\s\-'/]{4,})", raw)
            for block in parts:
                price = parse_euro_price(block)
                if price is None:
                    continue
                lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
                name = next(
                    (
                        ln
                        for ln in lines
                        if len(ln) > 4
                        and ln.upper() == ln
                        and "UNIVERS" not in ln
                        and "PRIX" not in ln
                        and not ln.startswith("U N")
                    ),
                    None,
                )
                if not name:
                    continue
                desc = next((ln for ln in lines if ln.lower().startswith("c'est") or ln.lower().startswith("ce sont")), "")
                items.append(
                    {
                        "page": page_no,
                        "name": name.title() if name.isupper() else name,
                        "price_euros": price,
                        "description": desc,
                    }
                )
            continue

        # Pages fiches produit (un prix)
        price = parse_euro_price(raw)
        if price is None:
            continue
        title = None
        for ln in raw.splitlines():
            ln = ln.strip()
            if len(ln) >= 4 and ln.isupper() and "UNIVERS" not in ln and "PRIX" not in ln:
                if re.match(r"^[A-ZÉÈÊÀÂÄÙÛÜÎÏÔÖÇ\s\-']+$", ln):
                    title = ln.title()
                    break
        if title:
            items.append({"page": page_no, "name": title, "price_euros": price, "description": ""})

    dedup: dict[tuple, dict] = {}
    for row in items:
        key = (row["name"].lower(), row["price_euros"])
        dedup[key] = row
    return sorted(dedup.values(), key=lambda r: (r["name"].lower(), r["price_euros"]))


def main() -> int:
    if not PDF.exists():
        print(f"PDF introuvable: {PDF}", file=sys.stderr)
        return 1
    rows = extract_items()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(rows)} produits extraits -> {OUT}")
    for row in rows[:20]:
        print(f"  {row['price_euros']:>6.2f} €  {row['name']}")
    if len(rows) > 20:
        print(f"  ... +{len(rows) - 20} autres")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
