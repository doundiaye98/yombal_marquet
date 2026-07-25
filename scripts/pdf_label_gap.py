# -*- coding: utf-8 -*-
"""Full priced product list from Catalogue LABEL (1).pdf with site match."""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def unspace(s: str) -> str:
    parts = s.split()
    out, buf = [], []
    for part in parts:
        if len(part) == 1:
            buf.append(part)
        else:
            if buf:
                out.append("".join(buf))
                buf = []
            out.append(part)
    if buf:
        out.append("".join(buf))
    return " ".join(out)


def parse_price(text: str) -> float | None:
    m = re.search(r"(\d+)\s*,\s*(\d+)\s*€", text)
    if m:
        return float(f"{m.group(1)}.{m.group(2)}")
    m = re.search(r"(?<!\d)(\d{1,3})\s*€", text)
    if m:
        return float(m.group(1))
    return None


def extract() -> list[dict]:
    from pypdf import PdfReader

    reader = PdfReader(str(ROOT / "img" / "Catalogue LABEL (1).pdf"))
    items = []
    for page_no, page in enumerate(reader.pages, start=1):
        raw = page.extract_text() or ""
        # Prefer normal text; also try unspaced for spaced pages
        for text in (raw, unspace(raw)):
            parts = re.split(r"((?:\d+\s*,\s*\d+|\d{1,3})\s*€)", text)
            i = 0
            while i + 1 < len(parts):
                block, price_s = parts[i], parts[i + 1]
                i += 2
                price = parse_price(price_s)
                if price is None or price <= 0 or price >= 500:
                    continue
                lines = [ln.strip() for ln in block.replace("\r", "").split("\n") if ln.strip()]
                title = None
                for ln in reversed(lines[-12:]):
                    up = ln.upper()
                    if up in {
                        "UNIVERS DIASPORA",
                        "FAIRE DE VOS REVES UNE REALITE!",
                        "FAIRE DE VOS RÊVES UNE RÉALITÉ!",
                        "PRIX",
                        "RIZ",
                        "PATES ET FARINES",
                        "PÂTES ET FARINES",
                        "HUILES ET GRAISSES",
                        "SNACKS ET PATISSERIES",
                        "SNACKS ET PÂTISSERIES",
                        "LEGUMINEUSES",
                        "LÉGUMINEUSES",
                        "CONDIMENTS",
                        "FRUITS SECS",
                        "BOISSONS",
                        "BOISSONS ET SIROPS",
                        "CONSERVES",
                        "POISSONS",
                        "VIANDES",
                        "SURGELES",
                        "SURGELÉS",
                        "LES ALIMENTS",
                        "EPICES ET",
                        "ÉPICES ET",
                        "ASSAISONNEMENTS",
                        "LEGUMES ET",
                        "LÉGUMES ET",
                        "TUBERCULES",
                        "PRODUITS DE LA MER",
                    }:
                        continue
                    if "FAIRE DE VOS" in up or "UNIVERS" in up.replace(" ", ""):
                        continue
                    # Prefer ALLCAPS short titles
                    if ln == ln.upper() and 3 <= len(ln) <= 70 and re.search(r"[A-ZÀ-Ÿ]", ln):
                        title = re.sub(r"\s+", " ", ln).strip().title()
                        break
                if not title:
                    continue
                nt = norm(title)
                if len(nt) < 3:
                    continue
                junk = ("better than", "pure african", "natural protein", "celebration", "at the heart", "tree of life")
                if any(j in nt for j in junk):
                    continue
                items.append({"page": page_no, "name": title, "price": price, "n": nt})
    dedup = {}
    for it in items:
        dedup[(it["n"], it["price"])] = it
    return list(dedup.values())


def main() -> None:
    from app import app
    from models.product import Product

    items = extract()
    with app.app_context():
        site = [
            {
                "slug": p.slug,
                "name": p.name,
                "price": (p.price_cents or 0) / 100,
                "n": norm(p.name + " " + p.slug),
            }
            for p in Product.query.filter_by(is_active=True).all()
        ]

    missing = []
    matched = []
    for it in items:
        pt = set(it["n"].split()) - {"de", "du", "des", "la", "le", "les", "et", "en", "kg", "g", "gr", "au", "aux", "carton"}
        best = None
        best_score = 0.0
        for s in site:
            if it["n"] in s["n"] or s["n"] in it["n"]:
                best, best_score = s, 1.0
                break
            st = set(s["n"].split())
            inter = len(pt & st)
            union = len(pt | st) or 1
            score = inter / union
            if abs(s["price"] - it["price"]) < 0.02:
                score += 0.15
            if score > best_score:
                best_score = score
                best = s
        row = {**it, "match": best["name"] if best else None, "slug": best["slug"] if best else None, "score": round(best_score, 2)}
        if best_score >= 0.45:
            matched.append(row)
        else:
            missing.append(row)

    out = ROOT / "data" / "pdf_label_gap.json"
    out.write_text(json.dumps({"missing": missing, "matched": matched, "total": len(items)}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"total={len(items)} matched={len(matched)} missing={len(missing)}")
    for m in sorted(missing, key=lambda x: x["page"]):
        print(f"p{m['page']:02d} {m['price']:>7.2f}€  {m['name']}  -> {m['match']} ({m['score']})")


if __name__ == "__main__":
    main()
