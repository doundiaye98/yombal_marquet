# -*- coding: utf-8 -*-
"""Re-diff data/pdf_catalogue_full.json against live boutique with smarter matching."""

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
    s = s.replace("œ", "oe")
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


ALIASES = {
    "thiakhry": "thiakry",
    "thiacry": "thiakry",
    "bouye": "baobab",
    "dakhar": "tamarin",
    "tamarind": "tamarin",
    "madd": "maad",
    "nodo": "nido",
    "niebe": "niebe",
    "kinkeliba": "kinkeliba",
    "kinkeliba sechees": "kinkeliba",
    "feuille de kinkeliba sechees": "kinkeliba",
}


def key_tokens(s: str) -> set[str]:
    stop = {
        "de", "du", "des", "la", "le", "les", "et", "en", "au", "aux", "un", "une",
        "kg", "g", "gr", "ml", "cl", "l", "carton", "sachet", "piece", "pieces",
        "fois", "avec", "sans", "tete", "videe", "ecaillee", "halal", "ud",
        "labelafrik", "pour", "par", "kilo",
    }
    n = norm(s)
    for a, b in ALIASES.items():
        n = n.replace(a, b)
    return {t for t in n.split() if len(t) > 1 and t not in stop}


def main() -> None:
    from app import app
    from models.product import Product
    from pypdf import PdfReader

    # refresh PDF extract using existing script logic + UD
    from scripts.diff_pdf_vs_boutique import extract_label_pdf, extract_ud_pdf, norm as n2

    rows = extract_label_pdf(ROOT / "img" / "Catalogue LABEL (1).pdf")
    rows += extract_ud_pdf(ROOT / "img" / "Catalogue UD.pdf")
    # also include old json
    old = json.loads((ROOT / "data" / "pdf_catalogue_full.json").read_text(encoding="utf-8"))
    for r in old:
        rows.append(
            {
                "pdf": "Catalogue LABEL (1).pdf",
                "page": r.get("page"),
                "category": r.get("category"),
                "name": r["name"],
                "price_euros": r["price_euros"],
                "description": r.get("description", ""),
                "source": "json",
            }
        )

    dedup = {}
    for r in rows:
        dedup[(norm(r["name"]), float(r["price_euros"]))] = r
    rows = list(dedup.values())

    with app.app_context():
        site = list(Product.query.filter_by(is_active=True).all())
        site_data = [
            {
                "slug": p.slug,
                "name": p.name,
                "price": (p.price_cents or 0) / 100,
                "tok": key_tokens(p.name + " " + p.slug + " " + (p.summary or "")),
                "n": norm(p.name + " " + p.slug),
            }
            for p in site
        ]

    missing = []
    matched = []
    for r in rows:
        name = r["name"]
        # skip obvious junk
        nn = norm(name)
        if any(
            j in nn
            for j in (
                "better than",
                "pure african",
                "natural protein",
                "celebration",
                "at the heart",
                "tree of life",
                "comme les cheveux",
                "digestion",
                "vitalite quotidienne",
                "filling intense",
                "s natural energy",
            )
        ):
            continue
        if re.match(r"^\d", nn) and "carton" in nn:
            continue
        if nn in {"carton de 5 kg", "avec tete carton de 10 kg", "videe ecaillee", "5 kg videe ecaillee"}:
            continue

        pt = key_tokens(name + " " + r.get("description", ""))
        if len(pt) < 1:
            continue
        best = None
        best_score = 0.0
        for s in site_data:
            if nn in s["n"] or s["n"] in nn:
                best, best_score = s, 1.0
                break
            inter = len(pt & s["tok"])
            union = len(pt | s["tok"]) or 1
            score = inter / max(len(pt), 1)
            # require at least 1 shared meaningful token
            if inter == 0:
                score = 0
            if abs(s["price"] - float(r["price_euros"])) < 0.02 and inter >= 1:
                score = max(score, 0.7)
            if score > best_score:
                best_score = score
                best = s
        entry = {
            "name": name,
            "price": r["price_euros"],
            "page": r.get("page"),
            "category": r.get("category"),
            "desc": (r.get("description") or "")[:160],
            "match": best["name"] if best else None,
            "slug": best["slug"] if best else None,
            "score": round(best_score, 2),
        }
        if best_score >= 0.5:
            matched.append(entry)
        else:
            missing.append(entry)

    # dedup missing by name+price
    uniq = {}
    for m in missing:
        uniq[(norm(m["name"]), m["price"])] = m
    missing = sorted(uniq.values(), key=lambda x: (x.get("page") or 0, x["name"]))

    Path("data/pdf_true_missing.json").write_text(
        json.dumps({"missing": missing, "matched_count": len(matched)}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"matched~{len(matched)} missing={len(missing)}")
    for m in missing:
        print(f"p{m['page'] or '?':>3} {m['price']:>7.2f}€ [{m.get('category')}] {m['name']}")
        print(f"      desc={m['desc'][:90]}")
        print(f"      best={m['match']} ({m['score']})")


if __name__ == "__main__":
    main()
