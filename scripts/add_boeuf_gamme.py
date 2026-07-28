# -*- coding: utf-8 -*-
"""Ajoute la gamme bœuf (entrecôtes, côtes, rôtis, boxes…) dans Viandes."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# sku, slug, name, summary, price_euros, weight_info, description_extra, category
# category: "viandes" | "huiles"
PRODUCTS = [
    (
        "UD-BOE-ENT-XXL-M",
        "entrecote-xxl-boeuf-montbeliarde",
        "Entrecôte XXL de bœuf Montbéliarde",
        "350–450 g — origine France. 48,00 €/kg (−20 %).",
        21.60,
        "350–450 g",
        "Entrecôte XXL Montbéliarde. Tarif promo 48,00 €/kg (max. 21,60 €/pièce). Origine France.",
        "viandes",
    ),
    (
        "UD-BOE-COTE-FR-1",
        "cote-boeuf-france-800g-1kg",
        "Côte de bœuf origine France",
        "800 g–1 kg — origine France. 39,50 €/kg.",
        39.50,
        "800 g–1 kg",
        "Côte de bœuf origine France. Tarif 39,50 €/kg (max. 39,50 €/pièce).",
        "viandes",
    ),
    (
        "UD-BOE-FAUX-SAL",
        "faux-filet-boeuf-salers",
        "Faux-filet de bœuf Salers",
        "300–400 g — bœuf français. 38,75 €/kg.",
        15.50,
        "300–400 g",
        "Faux-filet de bœuf Salers. Tarif 38,75 €/kg (max. 15,50 €/pièce).",
        "viandes",
    ),
    (
        "UD-BOE-ENT-CHA",
        "entrecote-boeuf-charolais",
        "Entrecôte de bœuf Charolais",
        "350–450 g — bœuf français. 43,55 €/kg (−20 %).",
        19.60,
        "350–450 g",
        "Entrecôte de bœuf Charolais. Tarif promo 43,55 €/kg (max. 19,60 €/pièce).",
        "viandes",
    ),
    (
        "UD-BOE-BAV-X10",
        "bavette-aloyau-x10",
        "Bavette d'aloyau x10",
        "1,6–1,7 kg — lot de 10. 29,75 €/kg (−15 %).",
        50.58,
        "1,6–1,7 kg",
        "Bavette d'aloyau x10. Tarif promo 29,75 €/kg (max. 50,58 €/pièce).",
        "viandes",
    ),
    (
        "UD-BOE-PAVE-RUM",
        "pave-rumsteck-boeuf-salers-x2",
        "Pavé de rumsteck de bœuf Salers x2",
        "300–400 g — bœuf français. 40,00 €/kg.",
        16.00,
        "300–400 g",
        "Pavé de rumsteck Salers x2. Tarif 40,00 €/kg (max. 16,00 €/pièce).",
        "viandes",
    ),
    (
        "UD-BOE-ENT-SEL-X2",
        "entrecote-boeuf-selection-boucher-x2",
        "Entrecôte de bœuf Sélection du Boucher x2",
        "400–600 g — 45,58 €/kg.",
        27.35,
        "400–600 g",
        "Entrecôte Sélection du Boucher x2. Tarif 45,58 €/kg (max. 27,35 €/pièce).",
        "viandes",
    ),
    (
        "UD-BOE-ENT-XXL-SEL",
        "entrecote-boeuf-xxl-selection-boucher",
        "Entrecôte de bœuf XXL Sélection du Boucher",
        "350–450 g — 40,00 €/kg.",
        18.00,
        "350–450 g",
        "Entrecôte XXL Sélection du Boucher. Tarif 40,00 €/kg (max. 18,00 €/pièce).",
        "viandes",
    ),
    (
        "UD-BOE-PAL",
        "paleron-boeuf-bourguignon",
        "Paleron de bœuf pour bourguignon",
        "800–900 g — 28,44 €/kg.",
        25.60,
        "800–900 g",
        "Paleron de bœuf pour bourguignon. Tarif 28,44 €/kg (max. 25,60 €/pièce).",
        "viandes",
    ),
    (
        "UD-BOE-TOM",
        "tomahawk-boeuf-blonde-galice",
        "Tomahawk de bœuf Blonde de Galice",
        "1–1,5 kg — origine Espagne. 79,95 €/kg.",
        119.93,
        "1–1,5 kg",
        "Tomahawk Blonde de Galice. Tarif 79,95 €/kg (max. 119,93 €/pièce). Origine Espagne.",
        "viandes",
    ),
    (
        "UD-HUILE-FONDUE",
        "huile-speciale-fondue-1l",
        "Huile spéciale fondue",
        "Bouteille verre 1 L — origine France.",
        9.90,
        "1 L",
        "Huile spéciale fondue. Prix 9,90 €/pièce (9,00 €/kg). Origine nationale France.",
        "huiles",
    ),
    (
        "UD-BOE-COTE-FR-15",
        "cote-boeuf-france-1-15kg",
        "Côte de bœuf origine France",
        "1–1,5 kg — origine France. 55,90 €/kg.",
        83.85,
        "1–1,5 kg",
        "Côte de bœuf origine France. Tarif 55,90 €/kg (max. 83,85 €/pièce).",
        "viandes",
    ),
    (
        "UD-BOE-COTE-SEL-L",
        "cote-boeuf-selection-boucher-115-14",
        "Côte de bœuf Sélection du Boucher",
        "1,15–1,4 kg — 39,90 €/kg.",
        55.86,
        "1,15–1,4 kg",
        "Côte de bœuf Sélection du Boucher. Tarif 39,90 €/kg (max. 55,86 €/pièce).",
        "viandes",
    ),
    (
        "UD-BOE-COTE-SEL-S",
        "cote-boeuf-selection-boucher-950-115",
        "Côte de bœuf Sélection du Boucher",
        "950 g–1,15 kg — 39,90 €/kg.",
        45.89,
        "950 g–1,15 kg",
        "Côte de bœuf Sélection du Boucher. Tarif 39,90 €/kg (max. 45,89 €/pièce).",
        "viandes",
    ),
    (
        "UD-BOE-TOUR-RUM",
        "tournedos-rumsteck-boeuf-salers-x2",
        "Tournedos de rumsteck de bœuf Salers x2",
        "300–400 g — viande de France. 44,70 €/kg.",
        17.88,
        "300–400 g",
        "Tournedos de rumsteck Salers x2. Tarif 44,70 €/kg (max. 17,88 €/pièce).",
        "viandes",
    ),
    (
        "UD-BOE-TOUR-FIL",
        "tournedos-filet-boeuf-salers-x2",
        "Tournedos de filet de bœuf Salers x2",
        "300–400 g — viande de France. 76,00 €/kg.",
        30.40,
        "300–400 g",
        "Tournedos de filet Salers x2. Tarif 76,00 €/kg (max. 30,40 €/pièce).",
        "viandes",
    ),
    (
        "UD-BOE-GITE",
        "gite-boeuf-pot-au-feu",
        "Gîte de bœuf pour pot-au-feu",
        "1,5–1,6 kg — 25,90 €/kg.",
        41.44,
        "1,5–1,6 kg",
        "Gîte de bœuf pour pot-au-feu. Tarif 25,90 €/kg (max. 41,44 €/pièce).",
        "viandes",
    ),
    (
        "UD-BOE-FONDUE",
        "viande-fondue-boeuf-salers",
        "Viande à fondue de bœuf Salers",
        "350–450 g — origine France. 35,00 €/kg.",
        15.75,
        "350–450 g",
        "Viande à fondue Salers. Tarif 35,00 €/kg (max. 15,75 €/pièce). Origine nationale France.",
        "viandes",
    ),
    (
        "UD-BOE-ROT-SAL-S",
        "roti-boeuf-salers-800g-1kg",
        "Rôti de bœuf Salers",
        "800 g–1 kg — bœuf français. 45,00 €/kg.",
        45.00,
        "800 g–1 kg",
        "Rôti de bœuf Salers. Tarif 45,00 €/kg (max. 45,00 €/pièce).",
        "viandes",
    ),
    (
        "UD-BOE-ROT-SAL-L",
        "roti-boeuf-salers-115-135",
        "Rôti de bœuf Salers",
        "1,15–1,35 kg — bœuf français. 45,00 €/kg.",
        60.75,
        "1,15–1,35 kg",
        "Rôti de bœuf Salers. Tarif 45,00 €/kg (max. 60,75 €/pièce).",
        "viandes",
    ),
    (
        "UD-BOE-ROT-FIL-L",
        "roti-filet-boeuf-francais-115-135",
        "Rôti de filet de bœuf français",
        "1,15–1,35 kg — origine France. 69,89 €/kg.",
        94.35,
        "1,15–1,35 kg",
        "Rôti de filet français. Tarif 69,89 €/kg (max. 94,35 €/pièce). Origine France.",
        "viandes",
    ),
    (
        "UD-BOE-ROT-FIL-S",
        "roti-filet-boeuf-francais-800-900",
        "Rôti de filet de bœuf français",
        "800–900 g — origine France. 69,89 €/kg.",
        62.90,
        "800–900 g",
        "Rôti de filet français. Tarif 69,89 €/kg (max. 62,90 €/pièce). Origine France.",
        "viandes",
    ),
    (
        "UD-BOE-ROT-TEN-XL",
        "roti-boeuf-tende-tranche-2-22",
        "Rôti de bœuf tende de tranche",
        "2–2,2 kg — 33,00 €/kg.",
        72.60,
        "2–2,2 kg",
        "Rôti tende de tranche. Tarif 33,00 €/kg (max. 72,60 €/pièce).",
        "viandes",
    ),
    (
        "UD-BOE-ROT-TEN-M",
        "roti-boeuf-tende-tranche-115-135",
        "Rôti de bœuf tende de tranche",
        "1,15–1,35 kg — 33,95 €/kg.",
        45.83,
        "1,15–1,35 kg",
        "Rôti tende de tranche. Tarif 33,95 €/kg (max. 45,83 €/pièce).",
        "viandes",
    ),
    (
        "UD-BOE-ROT-TEN-S",
        "roti-boeuf-tende-tranche-800g-1kg",
        "Rôti de bœuf tende de tranche",
        "800 g–1 kg — 29,90 €/kg.",
        29.90,
        "800 g–1 kg",
        "Rôti tende de tranche. Tarif 29,90 €/kg (max. 29,90 €/pièce).",
        "viandes",
    ),
    (
        "UD-BOE-TART",
        "steak-tartare-boeuf-francais-180g",
        "Steak tartare de bœuf français 5% MG",
        "180 g — bœuf français. 5,76 €/pièce.",
        5.76,
        "180 g",
        "Steak tartare français 5 % MG. Prix 5,76 €/pièce (32,00 €/kg).",
        "viandes",
    ),
    (
        "UD-BOE-ONG",
        "onglet-boeuf-x2",
        "Onglet de bœuf x2",
        "300–400 g — 41,50 €/kg.",
        16.60,
        "300–400 g",
        "Onglet de bœuf x2. Tarif 41,50 €/kg (max. 16,60 €/pièce).",
        "viandes",
    ),
    (
        "UD-BOE-POIRE",
        "steak-poire-boeuf-x2",
        "Steak de poire de bœuf x2",
        "300–400 g — 29,75 €/kg.",
        11.90,
        "300–400 g",
        "Steak de poire x2. Tarif 29,75 €/kg (max. 11,90 €/pièce).",
        "viandes",
    ),
    (
        "UD-BOE-BAV-X2",
        "bavette-aloyau-x2",
        "Bavette d'aloyau x2",
        "300–400 g — 35,00 €/kg.",
        14.00,
        "300–400 g",
        "Bavette d'aloyau x2. Tarif 35,00 €/kg (max. 14,00 €/pièce).",
        "viandes",
    ),
    (
        "UD-BOE-EMIN",
        "emince-boeuf-500g",
        "Émincé de bœuf",
        "±500 g — 24,22 €/kg (−10 %).",
        13.32,
        "±500 g",
        "Émincé de bœuf. Tarif promo 24,22 €/kg (max. 13,32 €/pièce).",
        "viandes",
    ),
    (
        "UD-BOE-BOX-100",
        "carre-box-boeuf-100",
        "Carré Box 100% bœuf",
        "3,85–4,85 kg — box familiale (−10 %).",
        169.05,
        "3,85–4,85 kg",
        "Carré Box 100 % bœuf. Prix 169,05 €/pièce (−10 %).",
        "viandes",
    ),
    (
        "UD-BOE-BOX-PROT-R",
        "carre-box-regime-proteine-rotis",
        "Carré Box régime protéiné avec rôtis",
        "4–5,1 kg — box protéinée (−10 %).",
        164.21,
        "4–5,1 kg",
        "Carré Box régime protéiné avec rôtis. Prix 164,21 €/pièce (−10 %).",
        "viandes",
    ),
    (
        "UD-BOE-BOX-FAM",
        "carre-box-viande-famille-nombreuse",
        "Carré Box viande famille nombreuse",
        "6,2–6,9 kg — grande famille (−10 %).",
        158.49,
        "6,2–6,9 kg",
        "Carré Box viande famille nombreuse. Prix 158,49 €/pièce (−10 %).",
        "viandes",
    ),
    (
        "UD-BOE-BOX-DEG",
        "carre-box-degustation-plaisir",
        "Carré Box dégustation plaisir",
        "3–4 kg — dégustation (−10 %).",
        127.16,
        "3–4 kg",
        "Carré Box dégustation plaisir. Prix 127,16 €/pièce (−10 %).",
        "viandes",
    ),
    (
        "UD-BOE-BOX-AUTH",
        "carre-box-viande-familial-authentique",
        "Carré Box viande familial authentique",
        "4,8–7 kg — box familiale (−10 %).",
        113.86,
        "4,8–7 kg",
        "Carré Box viande familial authentique. Prix 113,86 €/pièce (−10 %).",
        "viandes",
    ),
    (
        "UD-BOE-BOX-PROT",
        "carre-box-regime-proteine",
        "Carré Box régime protéiné",
        "3,7–5 kg — box protéinée (−10 %).",
        138.38,
        "3,7–5 kg",
        "Carré Box régime protéiné. Prix 138,38 €/pièce (−10 %).",
        "viandes",
    ),
    (
        "UD-BOE-ENT-FR-XXL",
        "entrecote-boeuf-francaise-xxl",
        "Entrecôte de bœuf française XXL",
        "350–450 g — origine France. 50,00 €/kg.",
        22.50,
        "350–450 g",
        "Entrecôte française XXL. Tarif 50,00 €/kg (max. 22,50 €/pièce). Origine France.",
        "viandes",
    ),
    (
        "UD-BOE-ENT-FR",
        "entrecote-boeuf-francaise",
        "Entrecôte de bœuf française",
        "250–350 g — origine France. 50,00 €/kg.",
        17.50,
        "250–350 g",
        "Entrecôte française. Tarif 50,00 €/kg (max. 17,50 €/pièce). Origine France.",
        "viandes",
    ),
    (
        "UD-BOE-FIL-ENT",
        "filet-boeuf-entier",
        "Filet de bœuf entier",
        "1,5–2,5 kg — 63,96 €/kg.",
        159.90,
        "1,5–2,5 kg",
        "Filet de bœuf entier. Tarif 63,96 €/kg (max. 159,90 €/pièce).",
        "viandes",
    ),
    (
        "UD-BOE-FIL-FR",
        "filet-boeuf-francais-entier",
        "Filet de bœuf français entier",
        "1,6–2 kg — origine France. 61,00 €/kg.",
        122.00,
        "1,6–2 kg",
        "Filet de bœuf français entier. Tarif 61,00 €/kg (max. 122,00 €/pièce). Origine France.",
        "viandes",
    ),
    (
        "UD-BOE-COTE-ANG",
        "cote-boeuf-angus",
        "Côte de bœuf Angus",
        "950 g–1,15 kg — 60,00 €/kg.",
        69.00,
        "950 g–1,15 kg",
        "Côte de bœuf Angus. Tarif 60,00 €/kg (max. 69,00 €/pièce).",
        "viandes",
    ),
    (
        "UD-BOE-PIC",
        "picanha-boeuf-angus",
        "Picanha de bœuf Angus",
        "1,5–2,5 kg — 39,90 €/kg.",
        99.75,
        "1,5–2,5 kg",
        "Picanha de bœuf Angus. Tarif 39,90 €/kg (max. 99,75 €/pièce).",
        "viandes",
    ),
    (
        "UD-BOE-FIL-ANG",
        "filet-boeuf-angus-entier",
        "Filet de bœuf Angus entier",
        "1,5–2,5 kg — 72,90 €/kg.",
        182.25,
        "1,5–2,5 kg",
        "Filet de bœuf Angus entier. Tarif 72,90 €/kg (max. 182,25 €/pièce).",
        "viandes",
    ),
    (
        "UD-BOE-ENT-WAG",
        "entrecote-boeuf-wagyu-japonais",
        "Entrecôte de bœuf Wagyu japonais",
        "200–250 g — origine Japon. 239,60 €/kg.",
        59.90,
        "200–250 g",
        "Entrecôte Wagyu japonais. Tarif 239,60 €/kg (max. 59,90 €/pièce). Origine Japon.",
        "viandes",
    ),
    (
        "UD-BOE-ONG-ANG",
        "onglet-boeuf-angus-x2",
        "Onglet de bœuf Angus x2",
        "300–400 g — 46,25 €/kg.",
        18.50,
        "300–400 g",
        "Onglet de bœuf Angus x2. Tarif 46,25 €/kg (max. 18,50 €/pièce).",
        "viandes",
    ),
    (
        "UD-BOE-ENT-XXL-SAL",
        "entrecote-xxl-boeuf-salers",
        "Entrecôte XXL de bœuf Salers",
        "350–450 g — bœuf français. 59,00 €/kg.",
        26.55,
        "350–450 g",
        "Entrecôte XXL Salers. Tarif 59,00 €/kg (max. 26,55 €/pièce).",
        "viandes",
    ),
    (
        "UD-BOE-ENT-SAL",
        "entrecote-boeuf-salers",
        "Entrecôte de bœuf Salers",
        "250–350 g — bœuf français. 59,00 €/kg.",
        20.65,
        "250–350 g",
        "Entrecôte Salers. Tarif 59,00 €/kg (max. 20,65 €/pièce).",
        "viandes",
    ),
]


def _cat_const(cat: str) -> str:
    return "CATEGORY_HUILES" if cat == "huiles" else "CATEGORY_VIANDES"


def _icon(cat: str) -> str:
    return "🫒" if cat == "huiles" else "🥩"


def _lf_block(sku, slug, name, summary, price, weight, extra, cat):
    name_src = name.replace("\\", "\\\\").replace('"', '\\"')
    ingredients = "Huile végétale." if cat == "huiles" else "Viande de bœuf."
    tips = (
        "Utiliser pour fondue bourguignonne selon notice."
        if cat == "huiles"
        else "Décongeler au frais si surgelé. Grillade, poêle ou four selon la coupe."
    )
    return f'''    _lf(
        "{sku}",
        "{slug}",
        "{name_src}",
        "{summary}",
        {_cat_const(cat)},
        "{_icon(cat)}",
        {price},
        "{weight}",
        description_extra="{extra}",
        ingredients="{ingredients}",
        usage_tips="{tips}",
        conservation="Au frais ou surgelé selon lot — respecter la DLC / DDM.",
    ),
'''


def patch_catalogue():
    path = ROOT / "models" / "catalogue_labelafrik.py"
    text = path.read_text(encoding="utf-8")
    if "entrecote-xxl-boeuf-montbeliarde" in text:
        print("catalogue déjà à jour")
        return
    # Ensure CATEGORY_HUILES is imported
    if "CATEGORY_HUILES" not in text.split("from models.constants import")[1].split(")")[0]:
        text = text.replace(
            "    CATEGORY_HUILES,\n" if "CATEGORY_HUILES" in text else "    CATEGORY_FRUITS,\n",
            "    CATEGORY_FRUITS,\n" if "CATEGORY_HUILES" in text else "    CATEGORY_FRUITS,\n",
        )
        if "CATEGORY_HUILES," not in text[:800]:
            text = text.replace(
                "    CATEGORY_FRUITS,\n",
                "    CATEGORY_FRUITS,\n    CATEGORY_HUILES,\n",
                1,
            )
    viande = [p for p in PRODUCTS if p[7] == "viandes"]
    huile = [p for p in PRODUCTS if p[7] == "huiles"]
    section_v = "    # —— Bœuf français / boxes / races ——\n" + "".join(_lf_block(*p) for p in viande)
    section_h = "".join(_lf_block(*p) for p in huile)

    # Insert viande products before end of LABELAFRIK_VIANDES
    end = text.find("]\n\nLABELAFRIK_EXTRA = [")
    if end < 0:
        raise SystemExit("fin LABELAFRIK_VIANDES introuvable")
    text = text[:end] + section_v + text[end:]

    # Append huile to LABELAFRIK_EXTRA if any
    if section_h:
        extra_end = text.rfind("]\n\nLABELAFRIK_CATALOGUE = (")
        if extra_end < 0:
            raise SystemExit("fin LABELAFRIK_EXTRA introuvable")
        text = text[:extra_end] + "    # —— Huile fondue ——\n" + section_h + text[extra_end:]

    path.write_text(text, encoding="utf-8")
    print("catalogue patché:", len(PRODUCTS), "produits")


def patch_names():
    path = ROOT / "models" / "product_names.py"
    text = path.read_text(encoding="utf-8")
    if "entrecote-xxl-boeuf-montbeliarde" in text:
        print("names déjà à jour")
        return
    lines = []
    for _, slug, name, _, _, weight, *_ in PRODUCTS:
        lines.append(f'    "{slug}": "{name} — {weight}",\n')
    block = "    # —— Bœuf / boxes ——\n" + "".join(lines)
    # Insert after agneau section or after viande-escargot
    markers = [
        '    "cotes-decouvertes-agneau-francais": "Côtes découvertes d\'agneau français — 450–650 g",\n',
        '    "viande-escargot-500g": "Viande d\'escargot — 500–600 g",\n',
    ]
    for anchor in markers:
        if anchor in text:
            text = text.replace(anchor, anchor + block, 1)
            path.write_text(text, encoding="utf-8")
            print("names patchés")
            return
    raise SystemExit("ancre product_names introuvable")


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
