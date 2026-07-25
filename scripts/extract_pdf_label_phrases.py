# -*- coding: utf-8 -*-
"""Extract 'Ce sont...' product lines from Catalogue LABEL PDF."""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
PDF = ROOT / "img" / "Catalogue LABEL (1).pdf"
OUT = ROOT / "data" / "pdf_label_phrases.json"


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def main() -> None:
    from pypdf import PdfReader

    from app import app
    from models.product import Product

    reader = PdfReader(str(PDF))
    phrases = []
    for i, page in enumerate(reader.pages, 1):
        raw = page.extract_text() or ""
        for m in re.finditer(r"Ce sont des? ([^.]{8,140})", raw, flags=re.I):
            phrase = m.group(1).strip()
            tail = raw[m.end() : m.end() + 220]
            pm = re.search(r"(\d+)\s*,\s*(\d+)\s*€|(\d{1,3})\s*€", tail)
            price = None
            if pm:
                if pm.group(1) is not None:
                    price = float(f"{pm.group(1)}.{pm.group(2)}")
                else:
                    price = float(pm.group(3))
            phrases.append({"page": i, "phrase": phrase, "price": price})

    with app.app_context():
        site = [
            {"slug": p.slug, "name": p.name, "n": norm(p.name + " " + p.slug)}
            for p in Product.query.filter_by(is_active=True).all()
        ]

    missing = []
    matched = []
    for row in phrases:
        pn = norm(row["phrase"])
        hit = None
        score = 0
        pt = set(pn.split()) - {"de", "du", "des", "la", "le", "les", "et", "en", "kg", "g"}
        for s in site:
            st = set(s["n"].split())
            if pn in s["n"] or s["n"] in pn:
                hit, score = s, 100
                break
            inter = len(pt & st)
            if inter > score:
                score = inter
                hit = s
        entry = {**row, "match": (hit or {}).get("name"), "slug": (hit or {}).get("slug"), "score": score}
        if score >= 2:
            matched.append(entry)
        else:
            missing.append(entry)

    # dedup missing by norm phrase
    seen = set()
    uniq_missing = []
    for m in missing:
        k = norm(m["phrase"])
        if k in seen:
            continue
        seen.add(k)
        uniq_missing.append(m)

    OUT.write_text(
        json.dumps({"phrases": phrases, "missing": uniq_missing, "matched": matched}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"phrases={len(phrases)} matched={len(matched)} missing_unique={len(uniq_missing)}")
    for m in uniq_missing:
        print(f"p{m['page']:02d} {m['price']:>7}  {m['phrase'][:100]}")
        print(f"         best={m['match']} score={m['score']}")


if __name__ == "__main__":
    main()
