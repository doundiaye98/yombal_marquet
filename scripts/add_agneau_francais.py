# -*- coding: utf-8 -*-
"""Ajoute la gamme agneau français / Pâques dans Viandes."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

PRODUCTS = [
    # sku, slug, name, summary, price_euros, weight_info, description_extra, origin_note
    (
        "UD-AGN-BOX-P",
        "carre-box-agneau-paques-premium",
        "Carré Box Agneau de Pâques premium",
        "Box premium 3,95–4,35 kg — pièce festive.",
        111.92,
        "3,95–4,35 kg",
        "Carré Box Agneau de Pâques premium. Prix à la pièce.",
        "",
    ),
    (
        "UD-AGN-BOX",
        "carre-box-agneau-paques",
        "Carré Box Agneau de Pâques",
        "Box 2,75–3,05 kg — pour les fêtes.",
        69.03,
        "2,75–3,05 kg",
        "Carré Box Agneau de Pâques. Prix à la pièce.",
        "",
    ),
    (
        "UD-AGN-GIG-FR",
        "gigot-agneau-francais",
        "Gigot d'agneau français",
        "2,3–2,7 kg — origine France. 38,61 €/kg.",
        104.25,
        "2,3–2,7 kg",
        "Gigot d'agneau français. Tarif 38,61 €/kg (max. 104,25 €/pièce).",
        "Origine nationale France.",
    ),
    (
        "UD-AGN-EPA-FR",
        "epaule-agneau-francais",
        "Épaule d'agneau français",
        "1,3–1,6 kg — origine France. 31,19 €/kg.",
        49.90,
        "1,3–1,6 kg",
        "Épaule d'agneau français. Tarif 31,19 €/kg (max. 49,90 €/pièce).",
        "Origine nationale France.",
    ),
    (
        "UD-AGN-C5-FR",
        "carre-5-cotes-agneau-francais",
        "Carré 5 côtes d'agneau français",
        "1–1,2 kg — origine France. 44,92 €/kg.",
        53.90,
        "1–1,2 kg",
        "Carré 5 côtes d'agneau français. Tarif 44,92 €/kg (max. 53,90 €/pièce).",
        "Origine nationale France.",
    ),
    (
        "UD-AGN-C8-FR",
        "carre-8-cotes-agneau-francais",
        "Carré 8 côtes d'agneau français",
        "1,2–1,6 kg — origine France. 50,00 €/kg.",
        80.00,
        "1,2–1,6 kg",
        "Carré 8 côtes d'agneau français. Tarif 50,00 €/kg (max. 80,00 €/pièce).",
        "Origine nationale France.",
    ),
    (
        "UD-AGN-ROT-FIC",
        "roti-epaule-agneau-ficelle",
        "Rôti d'épaule d'agneau ficelle",
        "900 g–1,2 kg — prêt à rôtir. 39,75 €/kg.",
        47.70,
        "900 g–1,2 kg",
        "Rôti d'épaule d'agneau ficelle. Tarif 39,75 €/kg (max. 47,70 €/pièce).",
        "",
    ),
    (
        "UD-AGN-ROT-NOI",
        "roti-noisette-agneau",
        "Rôti Noisette d'agneau",
        "1–1,5 kg — pièce tendre. 64,00 €/kg.",
        96.00,
        "1–1,5 kg",
        "Rôti Noisette d'agneau. Tarif 64,00 €/kg (max. 96,00 €/pièce).",
        "",
    ),
    (
        "UD-AGN-COTE-1",
        "agneau-cote-premiere",
        "Agneau côte première",
        "400–500 g — 42,24 €/kg (−20 %).",
        21.12,
        "400–500 g",
        "Agneau côte première. Tarif promo 42,24 €/kg (max. 21,12 €/pièce).",
        "",
    ),
    (
        "UD-AGN-C4",
        "carre-agneau-4-cotes-premieres",
        "Carré d'agneau 4 côtes premières",
        "400–500 g — 65,00 €/kg.",
        32.50,
        "400–500 g",
        "Carré d'agneau 4 côtes premières. Tarif 65,00 €/kg (max. 32,50 €/pièce).",
        "",
    ),
    (
        "UD-AGN-GIG-ENT",
        "gigot-agneau-entier",
        "Gigot d'agneau entier",
        "2,3–2,7 kg — 33,30 €/kg.",
        89.90,
        "2,3–2,7 kg",
        "Gigot d'agneau entier. Tarif 33,30 €/kg (max. 89,90 €/pièce).",
        "",
    ),
    (
        "UD-AGN-EPA-SP",
        "epaule-agneau-sans-palette",
        "Épaule d'agneau sans palette",
        "1,5–1,8 kg — 36,11 €/kg.",
        65.00,
        "1,5–1,8 kg",
        "Épaule d'agneau sans palette. Tarif 36,11 €/kg (max. 65,00 €/pièce).",
        "",
    ),
    (
        "UD-AGN-COT-DEC",
        "cotes-decouvertes-agneau",
        "Côtes découvertes d'agneau",
        "400–500 g — 64,00 €/kg.",
        32.00,
        "400–500 g",
        "Côtes découvertes d'agneau. Tarif 64,00 €/kg (max. 32,00 €/pièce).",
        "",
    ),
    (
        "UD-AGN-C8",
        "carre-8-cotes-agneau",
        "Carré 8 côtes d'agneau",
        "800 g–1,2 kg — 54,35 €/kg.",
        65.22,
        "800 g–1,2 kg",
        "Carré 8 côtes d'agneau. Tarif 54,35 €/kg (max. 65,22 €/pièce).",
        "",
    ),
    (
        "UD-AGN-SAU-GIG",
        "saute-gigot-agneau",
        "Sauté de gigot d'agneau",
        "800–900 g — 37,50 €/kg.",
        33.75,
        "800–900 g",
        "Sauté de gigot d'agneau. Tarif 37,50 €/kg (max. 33,75 €/pièce).",
        "",
    ),
    (
        "UD-AGN-SAU-EPA",
        "saute-epaule-agneau",
        "Sauté d'épaule d'agneau",
        "800–900 g — 35,72 €/kg.",
        32.15,
        "800–900 g",
        "Sauté d'épaule d'agneau. Tarif 35,72 €/kg (max. 32,15 €/pièce).",
        "",
    ),
    (
        "UD-AGN-NAV",
        "agneau-navarin",
        "Agneau navarin",
        "900 g–1,1 kg — 35,90 €/kg.",
        39.49,
        "900 g–1,1 kg",
        "Agneau navarin. Tarif 35,90 €/kg (max. 39,49 €/pièce).",
        "",
    ),
    (
        "UD-AGN-ROT-SEL",
        "roti-selle-agneau",
        "Rôti de selle d'agneau",
        "800 g–1 kg — 50,00 €/kg.",
        50.00,
        "800 g–1 kg",
        "Rôti de selle d'agneau. Tarif 50,00 €/kg (max. 50,00 €/pièce).",
        "",
    ),
    (
        "UD-AGN-GIGOTIN",
        "roti-gigotin-epaule-agneau",
        "Rôti Gigotin d'épaule d'agneau",
        "1,2–1,5 kg — 36,67 €/kg.",
        55.00,
        "1,2–1,5 kg",
        "Rôti Gigotin d'épaule d'agneau. Tarif 36,67 €/kg (max. 55,00 €/pièce).",
        "",
    ),
    (
        "UD-AGN-ROT-EPA-FR",
        "roti-epaule-agneau-francais",
        "Rôti d'épaule d'agneau français",
        "1,3–1,7 kg — origine France. 34,41 €/kg.",
        58.50,
        "1,3–1,7 kg",
        "Rôti d'épaule d'agneau français. Tarif 34,41 €/kg (max. 58,50 €/pièce).",
        "Origine nationale France.",
    ),
    (
        "UD-AGN-ROT-SEL-FR",
        "roti-selle-agneau-francais",
        "Rôti de selle d'agneau français",
        "1,2–1,6 kg — origine France. 30,94 €/kg.",
        49.50,
        "1,2–1,6 kg",
        "Rôti de selle d'agneau français. Tarif 30,94 €/kg (max. 49,50 €/pièce).",
        "Origine nationale France.",
    ),
    (
        "UD-AGN-NAV-FR",
        "navarin-agneau-francais",
        "Navarin d'agneau français",
        "900 g–1,1 kg — origine France. 34,91 €/kg.",
        38.40,
        "900 g–1,1 kg",
        "Navarin d'agneau français. Tarif 34,91 €/kg (max. 38,40 €/pièce).",
        "Origine nationale France.",
    ),
    (
        "UD-AGN-COT-DEC-FR",
        "cotes-decouvertes-agneau-francais",
        "Côtes découvertes d'agneau français",
        "450–650 g — origine France. 44,00 €/kg.",
        28.60,
        "450–650 g",
        "Côtes découvertes d'agneau français. Tarif 44,00 €/kg (max. 28,60 €/pièce).",
        "Origine nationale France.",
    ),
]


def _lf_block(sku, slug, name, summary, price, weight, extra, origin):
    origin_line = f" {origin}" if origin else ""
    # Escape quotes in name for Python source
    name_src = name.replace("\\", "\\\\").replace('"', '\\"')
    return f'''    _lf(
        "{sku}",
        "{slug}",
        "{name_src}",
        "{summary}",
        CATEGORY_VIANDES,
        "🐑",
        {price},
        "{weight}",
        description_extra="{extra}{origin_line}",
        ingredients="Viande d'agneau.",
        usage_tips="Décongeler au frais si surgelé. Cuisson four, mijoté ou grillade selon la coupe.",
        conservation="Au frais ou surgelé selon lot — respecter la DLC / DDM.",
    ),
'''


def patch_catalogue():
    path = ROOT / "models" / "catalogue_labelafrik.py"
    text = path.read_text(encoding="utf-8")
    if "carre-box-agneau-paques-premium" in text:
        print("catalogue déjà à jour")
        return
    blocks = "".join(_lf_block(*p) for p in PRODUCTS)
    section = (
        "    # —— Agneau français / Pâques ——\n"
        + blocks
    )
    anchor = '        conservation="Surgelé — conserver à -18 °C.",\n    ),\n]\n\nLABELAFRIK_EXTRA = ['
    # Find the last viande block ending (escargot)
    needle = (
        '        "UD-ESCAR",\n'
        '        "viande-escargot-500g",'
    )
    if needle not in text:
        raise SystemExit("ancre viande-escargot introuvable")
    # Insert before closing of LABELAFRIK_VIANDES
    end = text.find("]\n\nLABELAFRIK_EXTRA = [")
    if end < 0:
        raise SystemExit("fin LABELAFRIK_VIANDES introuvable")
    # Find the closing ], of VIANDES — the last ), before ]
    insert_at = end
    text = text[:insert_at] + section + text[insert_at:]
    path.write_text(text, encoding="utf-8")
    print("catalogue patché:", len(PRODUCTS), "produits")


def patch_names():
    path = ROOT / "models" / "product_names.py"
    text = path.read_text(encoding="utf-8")
    if "carre-box-agneau-paques-premium" in text:
        print("names déjà à jour")
        return
    lines = []
    for _, slug, name, _, _, weight, *_ in PRODUCTS:
        display = f"{name} — {weight}"
        lines.append(f'    "{slug}": "{display}",\n')
    block = "    # —— Agneau français / Pâques ——\n" + "".join(lines)
    anchor = '    "viande-escargot-500g": "Viande d\'escargot — 500–600 g",\n'
    if anchor not in text:
        raise SystemExit("ancre product_names introuvable")
    text = text.replace(anchor, anchor + block, 1)
    path.write_text(text, encoding="utf-8")
    print("names patchés")


def main():
    patch_catalogue()
    patch_names()
    from app import app
    from models.seed import sync_catalogue
    from models.product import Product

    with app.app_context():
        sync_catalogue()
        slugs = [p[1] for p in PRODUCTS]
        found = Product.query.filter(Product.slug.in_(slugs)).count()
        print(f"en base: {found}/{len(slugs)}")
        for p in Product.query.filter(Product.slug.in_(slugs)).order_by(Product.name).all():
            print(f"  - {p.name} | {p.price_cents/100:.2f} € | {p.category}")


if __name__ == "__main__":
    main()
