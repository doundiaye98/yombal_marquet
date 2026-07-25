# -*- coding: utf-8 -*-
"""Dump cleaned LABEL PDF product candidates with prices."""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
PDF = ROOT / "img" / "Catalogue LABEL (1).pdf"
OUT = ROOT / "data" / "pdf_label_candidates.json"


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def parse_price(text: str) -> float | None:
    m = re.search(r"(\d+)\s*,\s*(\d+)\s*€", text)
    if m:
        return float(f"{m.group(1)}.{m.group(2)}")
    m = re.search(r"(?<!\d)(\d{1,3})\s*€", text)
    if m:
        return float(m.group(1))
    return None


def main() -> None:
    from pypdf import PdfReader

    from app import app
    from models.product import Product

    reader = PdfReader(str(PDF))
    items = []
    for page_no, page in enumerate(reader.pages, start=1):
        raw = page.extract_text() or ""
        # Split by euro prices
        parts = re.split(r"(\d+\s*,\s*\d+\s*€|\d{1,3}\s*€)", raw)
        # parts: text, price, text, price...
        i = 0
        while i + 1 < len(parts):
            block = parts[i]
            price_raw = parts[i + 1]
            price = parse_price(price_raw)
            i += 2
            if price is None or not (0 < price < 500):
                continue
            # find uppercase title lines in block
            lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
            title = None
            for ln in reversed(lines):
                if ln.upper() == ln and len(ln) >= 4 and re.match(r"^[A-ZÉÈÊÀÂÄÙÛÜÎÏÔÖÇ0-9\s\-'/&]+$", ln):
                    if "UNIVERS" in ln.replace(" ", "") or ln in ("PRIX",):
                        continue
                    title = re.sub(r"\s+", " ", ln).strip().title()
                    break
            desc = next((ln for ln in lines if ln.lower().startswith(("c'est", "ce sont"))), "")
            if not title and desc:
                # derive short name from desc
                m = re.match(r"Ce sont des? (.+)", desc, re.I)
                if m:
                    title = m.group(1).split(",")[0].strip()
                    if len(title) > 60:
                        title = title[:60]
            if not title:
                continue
            nt = norm(title)
            if any(
                x in nt
                for x in (
                    "faire de vos",
                    "univers",
                    "labelafrik",
                    "carton de",
                    "avec tete",
                    "sans tete",
                    "videe",
                )
            ):
                continue
            items.append(
                {
                    "page": page_no,
                    "name": title,
                    "price": price,
                    "desc": desc[:200],
                    "n": nt,
                }
            )

    # dedup
    dedup = {}
    for it in items:
        key = (it["n"], it["price"])
        dedup[key] = it
    items = sorted(dedup.values(), key=lambda x: (x["page"], x["name"]))

    with app.app_context():
        site = list(Product.query.filter_by(is_active=True).all())
        site_n = [(p, norm(p.name + " " + p.slug + " " + (p.summary or ""))) for p in site]

    missing = []
    matched = []
    for it in items:
        pt = set(it["n"].split()) - {"de", "du", "des", "la", "le", "les", "et", "en", "kg", "g", "gr", "ml", "cl", "l"}
        best = None
        best_score = 0
        for p, sn in site_n:
            if it["n"] in sn or sn in it["n"]:
                best, best_score = p, 99
                break
            st = set(sn.split())
            score = len(pt & st)
            # price proximity bonus
            if abs((p.price_cents or 0) / 100 - it["price"]) < 0.05 and score >= 1:
                score += 2
            if score > best_score:
                best_score = score
                best = p
        row = {
            **{k: v for k, v in it.items() if k != "n"},
            "match_slug": best.slug if best else None,
            "match_name": best.name if best else None,
            "score": best_score,
        }
        if best_score >= 2:
            matched.append(row)
        else:
            missing.append(row)

    OUT.write_text(json.dumps({"all": items, "missing": missing, "matched": matched}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"candidates={len(items)} matched={len(matched)} missing={len(missing)}")
    print("\nMISSING:")
    for m in missing:
        print(f"p{m['page']:02d} {m['price']:>7.2f}€  {m['name']}")
        if m["desc"]:
            print(f"         {m['desc'][:110]}")
        print(f"         best={m['match_name']} ({m['score']})")


if __name__ == "__main__":
    main()
