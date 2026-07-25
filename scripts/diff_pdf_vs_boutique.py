# -*- coding: utf-8 -*-
"""Compare Catalogue LABEL + Catalogue UD PDFs against the live boutique catalogue."""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

OUT = ROOT / "data" / "pdf_missing_products.json"

SKIP = {
    "univers diaspora",
    "labelafrik",
    "prix",
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
    "faire de vos reves une realite",
}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = s.replace("œ", "oe").replace("æ", "ae")
    s = re.sub(r"[^a-z0-9]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    # drop packaging noise
    for noise in (
        " carton de ",
        " carton ",
        " sachet ",
        " piece ",
        " pieces ",
        " au kg ",
        " par kilo ",
        " par kg ",
    ):
        s = s.replace(noise, " ")
    return re.sub(r"\s+", " ", s).strip()


def tokens(s: str) -> set[str]:
    stop = {"de", "du", "des", "la", "le", "les", "et", "en", "au", "aux", "kg", "g", "l", "cl", "ml", "ud", "labelafrik"}
    return {t for t in norm(s).split() if len(t) > 1 and t not in stop}


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


CATEGORY_MARKERS = {
    "RIZ": "cereales",
    "PÂTES ET FARINES": "cereales",
    "PATES ET FARINES": "cereales",
    "HUILES ET GRAISSES": "huiles",
    "SNACKS ET PÂTISSERIES": "snacks",
    "SNACKS ET PATISSERIES": "snacks",
    "LÉGUMINEUSES": "cereales",
    "LEGUMINEUSES": "cereales",
    "CONDIMENTS": "condiments",
    "FRUITS SECS": "fruits",
    "BOISSONS": "boissons",
    "CONSERVES": "conserves",
    "POISSONS": "poisson",
    "VIANDES": "viandes",
    "SURGELÉS": "snacks",
    "SURGELES": "snacks",
}


def extract_label_pdf(path: Path) -> list[dict]:
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    items: list[dict] = []
    current_cat = ""

    for page_no, page in enumerate(reader.pages, start=1):
        raw = page.extract_text() or ""
        lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]

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
                        "pdf": path.name,
                        "page": page_no,
                        "category": current_cat or "alimentaire",
                        "name": title,
                        "price_euros": price,
                        "description": "",
                        "source": "fiche",
                    }
                )
            continue

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
                        if bl.lower().startswith(("c'est", "ce sont", "c est")):
                            desc = bl
                            break
                    for bl in block_lines:
                        if bl != desc and len(bl) > 8 and not bl.startswith("U N"):
                            if parse_price(bl) is None and "€" not in bl:
                                name = normalize_name(bl)
                                break
                if name and norm(name) not in SKIP and 0 < price < 500:
                    # filter junk packaging titles
                    junk = ("carton", "vidée", "ecaillee", "avec tete", "sans tete", "gr-", "kg-")
                    nn = norm(name)
                    if any(j in nn for j in junk) and len(nn.split()) <= 5:
                        block_lines = []
                        continue
                    if not desc:
                        desc = next(
                            (bl for bl in block_lines if bl.lower().startswith(("c'est", "ce sont"))),
                            "",
                        )
                    items.append(
                        {
                            "pdf": path.name,
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
        key = (norm(row["name"]), row["price_euros"])
        dedup[key] = row
    return list(dedup.values())


def extract_ud_pdf(path: Path) -> list[dict]:
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    items = []
    for page_no, page in enumerate(reader.pages, start=1):
        raw = page.extract_text() or ""
        # Product lines like "Arraw de Mil–LabelAfrik 3€"
        for m in re.finditer(
            r"([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ0-9\s'\-]{2,60})(?:–|-)?\s*LabelAfrik[^\d]{0,20}(\d+)\s*€",
            raw,
            flags=re.I,
        ):
            name = normalize_name(m.group(1).strip(" –-"))
            price = float(m.group(2))
            if norm(name) in SKIP:
                continue
            items.append(
                {
                    "pdf": path.name,
                    "page": page_no,
                    "category": "alimentaire",
                    "name": name,
                    "price_euros": price,
                    "description": "",
                    "source": "ud",
                }
            )
        # Also "Name 3€ Prix" patterns
        price = parse_price(raw)
        if price and "LabelAfrik" in raw:
            # try to find French title before LabelAfrik
            m = re.search(
                r"([A-ZÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ][A-Za-zÀ-ÿ\s'\-]{2,40})\s*[–-]?\s*LabelAfrik",
                raw,
            )
            if m:
                name = normalize_name(m.group(1).strip(" –-"))
                if norm(name) not in SKIP and 0 < price < 100:
                    items.append(
                        {
                            "pdf": path.name,
                            "page": page_no,
                            "category": "alimentaire",
                            "name": name,
                            "price_euros": price,
                            "description": "",
                            "source": "ud",
                        }
                    )
    dedup: dict[tuple, dict] = {}
    for row in items:
        key = (norm(row["name"]), row["price_euros"])
        dedup[key] = row
    return list(dedup.values())


def load_site_products() -> list[dict]:
    from app import app
    from models.product import Product
    from models.seed import FULL_CATALOGUE

    rows = []
    with app.app_context():
        for p in Product.query.filter_by(is_active=True).all():
            rows.append(
                {
                    "slug": p.slug,
                    "name": p.name,
                    "price_euros": (p.price_cents or 0) / 100,
                    "category": p.category,
                    "source": "db",
                }
            )
    # also seed catalogue (in case DB lag)
    for r in FULL_CATALOGUE:
        rows.append(
            {
                "slug": r["slug"],
                "name": r["name"],
                "price_euros": r["price_cents"] / 100,
                "category": r["category"],
                "source": "seed",
            }
        )
    return rows


def best_match(pdf_name: str, site_rows: list[dict]) -> tuple[dict | None, float]:
    pt = tokens(pdf_name)
    if not pt:
        return None, 0.0
    best = None
    best_score = 0.0
    pn = norm(pdf_name)
    for r in site_rows:
        sn = norm(r["name"])
        st = tokens(r["name"] + " " + r.get("slug", ""))
        if not st:
            continue
        if pn == sn or pn in sn or sn in pn:
            return r, 1.0
        inter = len(pt & st)
        union = len(pt | st) or 1
        score = inter / union
        # boost if slug shares key tokens
        if inter >= 2 and score > best_score:
            best_score = score
            best = r
        elif score > best_score:
            best_score = score
            best = r
    return best, best_score


def main() -> int:
    label = ROOT / "img" / "Catalogue LABEL (1).pdf"
    ud = ROOT / "img" / "Catalogue UD.pdf"

    pdf_rows = []
    if label.exists():
        print("Parsing", label.name, "...")
        pdf_rows.extend(extract_label_pdf(label))
    if ud.exists():
        print("Parsing", ud.name, "...")
        pdf_rows.extend(extract_ud_pdf(ud))

    # dedup across pdfs
    dedup: dict[tuple, dict] = {}
    for row in pdf_rows:
        dedup[(norm(row["name"]), row["price_euros"])] = row
    pdf_rows = sorted(dedup.values(), key=lambda r: r["name"].lower())

    print("Loading site catalogue...")
    site = load_site_products()
    # unique by slug
    by_slug = {}
    for r in site:
        by_slug[r["slug"]] = r
    site_unique = list(by_slug.values())

    missing = []
    matched = []
    for row in pdf_rows:
        hit, score = best_match(row["name"], site_unique)
        if score >= 0.55:
            matched.append({**row, "match_slug": hit["slug"], "match_name": hit["name"], "score": round(score, 2)})
        else:
            missing.append({**row, "best_guess": (hit or {}).get("name"), "score": round(score, 2)})

    OUT.write_text(
        json.dumps({"missing": missing, "matched": matched}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"PDF products: {len(pdf_rows)}")
    print(f"Site unique: {len(site_unique)}")
    print(f"Matched: {len(matched)}")
    print(f"Missing: {len(missing)}")
    print("\n--- MISSING ---")
    for r in missing:
        print(f"  p{r['page']:02d} {r['price_euros']:>7.2f}€  [{r['category']}] {r['name']}  (best={r.get('best_guess')} {r.get('score')})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
