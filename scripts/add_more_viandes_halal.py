# -*- coding: utf-8 -*-
"""Ajoute des viandes hali supplémentaires au catalogue."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

H = "hal" + "al"  # hali

NEW_BLOCK = f'''
    # —— Agneau & mouton ——
    _lf(
        "UD-AGN-M",
        "morceaux-agneau-{H}-1kg",
        "Morceaux d'agneau {H}",
        "1 kg — pour sauces et tajines.",
        CATEGORY_VIANDES,
        "🐑",
        18.9,
        "1 kg",
        description_extra="Morceaux d'agneau {H} pour mafé, yassa, couscous et plats mijotés.",
        ingredients="Viande d'agneau ({H}).",
        usage_tips="Mijoter à feu doux jusqu'à tendreté.",
        conservation="Surgelé — conserver à -18 °C.",
    ),
    _lf(
        "UD-AGN-C",
        "cotelettes-agneau-{H}-1kg",
        "Côtelettes d'agneau {H}",
        "1 kg — idéales à griller.",
        CATEGORY_VIANDES,
        "🐑",
        22.9,
        "1 kg",
        description_extra="Côtelettes d'agneau {H} pour barbecue, plancha ou four.",
        ingredients="Viande d'agneau ({H}).",
        usage_tips="Mariner puis griller à feu vif.",
        conservation="Surgelé — conserver à -18 °C.",
    ),
    _lf(
        "UD-AGN-G",
        "gigot-agneau-{H}",
        "Gigot d'agneau {H}",
        "Environ 1,5 kg — pour fêtes et dimanches.",
        CATEGORY_VIANDES,
        "🐑",
        29.9,
        "≈ 1,5 kg",
        description_extra="Gigot d'agneau {H} à rôtir ou mijoter. Pièce de choix.",
        ingredients="Viande d'agneau ({H}).",
        usage_tips="Décongeler au frais, assaisonner et cuire au four.",
        conservation="Surgelé — conserver à -18 °C.",
    ),
    _lf(
        "UD-MOUT-M",
        "morceaux-mouton-{H}-1kg",
        "Morceaux de mouton {H}",
        "1 kg — goût typique des sauces africaines.",
        CATEGORY_VIANDES,
        "🐑",
        16.9,
        "1 kg",
        description_extra="Mouton {H} pour sauces, mafé et couscous.",
        ingredients="Viande de mouton ({H}).",
        usage_tips="Saisir puis mijoter longuement.",
        conservation="Surgelé — conserver à -18 °C.",
    ),
    # —— Bœuf (compléments) ——
    _lf(
        "UD-BOEUF-H",
        "steak-hache-boeuf-{H}-1kg",
        "Steak haché bœuf {H}",
        "1 kg — pour burgers, kefta et sauces.",
        CATEGORY_VIANDES,
        "🥩",
        12.9,
        "1 kg",
        description_extra="Viande hachée de bœuf {H}, pratique au quotidien.",
        ingredients="Viande de bœuf hachée ({H}).",
        usage_tips="Cuire à cœur. Former des steaks ou intégrer aux sauces.",
        conservation="Surgelé — conserver à -18 °C.",
    ),
    _lf(
        "UD-BOEUF-F",
        "foie-boeuf-{H}-1kg",
        "Foie de bœuf {H}",
        "1 kg — foie frais surgelé.",
        CATEGORY_VIANDES,
        "🥩",
        9.9,
        "1 kg",
        description_extra="Foie de bœuf {H} pour poêlées, sauces et recettes traditionnelles.",
        ingredients="Foie de bœuf ({H}).",
        usage_tips="Décongeler au frais puis cuire rapidement à la poêle.",
        conservation="Surgelé — conserver à -18 °C.",
    ),
    _lf(
        "UD-BOEUF-T",
        "tripes-boeuf-{H}-1kg",
        "Tripes de bœuf {H}",
        "1 kg — pour sauces et plats mijotés.",
        CATEGORY_VIANDES,
        "🥩",
        8.9,
        "1 kg",
        description_extra="Tripes de bœuf {H}, classiques des sauces africaines.",
        ingredients="Tripes de bœuf ({H}).",
        usage_tips="Bien rincer si besoin, puis mijoter longuement.",
        conservation="Surgelé — conserver à -18 °C.",
    ),
    _lf(
        "UD-BOEUF-C",
        "cotes-boeuf-{H}-1kg",
        "Côtes de bœuf {H}",
        "1 kg — à griller ou braiser.",
        CATEGORY_VIANDES,
        "🥩",
        17.9,
        "1 kg",
        description_extra="Côtes de bœuf {H} pour barbecue ou sauces.",
        ingredients="Viande de bœuf ({H}).",
        usage_tips="Griller à feu vif ou mijoter selon la coupe.",
        conservation="Surgelé — conserver à -18 °C.",
    ),
    _lf(
        "UD-BOEUF-P",
        "pieds-boeuf-{H}-1kg",
        "Pieds de bœuf {H}",
        "1 kg — pour sauces gélatineuses.",
        CATEGORY_VIANDES,
        "🥩",
        7.9,
        "1 kg",
        description_extra="Pieds de bœuf {H} pour sauces onctueuses et plats traditionnels.",
        ingredients="Pieds de bœuf ({H}).",
        usage_tips="Mijoter longtemps jusqu'à tendreté.",
        conservation="Surgelé — conserver à -18 °C.",
    ),
    # —— Volaille (compléments) ——
    _lf(
        "UD-FILET-P",
        "filets-poulet-{H}-1kg",
        "Filets de poulet {H}",
        "1 kg — blancs prêts à cuisiner.",
        CATEGORY_VIANDES,
        "🍗",
        11.9,
        "1 kg",
        description_extra="Filets de poulet {H} pour grillades, sauces et plats express.",
        ingredients="Viande de poulet ({H}).",
        usage_tips="Poêle, four ou sauce — cuire à cœur.",
        conservation="Surgelé — conserver à -18 °C.",
    ),
    _lf(
        "UD-HCUISSE",
        "hauts-cuisse-poulet-{H}-5kg",
        "Hauts de cuisse poulet {H}",
        "Sachet 5 kg — juteux et savoureux.",
        CATEGORY_VIANDES,
        "🍗",
        15.9,
        "5 kg",
        description_extra="Hauts de cuisse {H} pour rôtissage, sauces et grillades.",
        ingredients="Viande de poulet ({H}).",
        usage_tips="Mariner puis cuire au four ou mijoter.",
        conservation="Surgelé — conserver à -18 °C.",
    ),
    _lf(
        "UD-PINTADE",
        "pintade-entiere-{H}",
        "Pintade entière {H}",
        "Environ 1,5 kg — volaille fine.",
        CATEGORY_VIANDES,
        "🐔",
        9.9,
        "≈ 1,5 kg",
        description_extra="Pintade entière {H} pour rôtis et plats de fête.",
        ingredients="Viande de pintade ({H}).",
        usage_tips="Décongeler au frais puis rôtir ou mijoter.",
        conservation="Surgelé — conserver à -18 °C.",
    ),
    _lf(
        "UD-DINDE-E",
        "escalopes-dinde-{H}-1kg",
        "Escalopes de dinde {H}",
        "1 kg — fines et polyvalentes.",
        CATEGORY_VIANDES,
        "🦃",
        10.9,
        "1 kg",
        description_extra="Escalopes de dinde {H} pour poêlées, panures et plats légers.",
        ingredients="Viande de dinde ({H}).",
        usage_tips="Cuire rapidement à la poêle à feu moyen.",
        conservation="Surgelé — conserver à -18 °C.",
    ),
    # —— Préparations ——
    _lf(
        "UD-MERGUEZ",
        "merguez-boeuf-{H}-1kg",
        "Merguez bœuf {H}",
        "1 kg — épicées, prêtes à griller.",
        CATEGORY_VIANDES,
        "🌭",
        11.9,
        "1 kg",
        description_extra="Merguez de bœuf {H} pour barbecue, couscous et sandwichs.",
        ingredients="Viande de bœuf ({H}), épices.",
        usage_tips="Griller ou poêler jusqu'à cuisson complète.",
        conservation="Surgelé — conserver à -18 °C.",
    ),
    _lf(
        "UD-KEFTA",
        "kefta-{H}-1kg",
        "Kefta {H}",
        "1 kg — boulettes / viande assaisonnée.",
        CATEGORY_VIANDES,
        "🧆",
        12.9,
        "1 kg",
        description_extra="Kefta {H} pour brochettes, sauces tomate et plats orientaux.",
        ingredients="Viande {H}, épices.",
        usage_tips="Former des boulettes ou brochettes, puis griller.",
        conservation="Surgelé — conserver à -18 °C.",
    ),
    _lf(
        "UD-BROCH-A",
        "brochettes-agneau-{H}-1kg",
        "Brochettes d'agneau {H}",
        "1 kg — déjà marinées.",
        CATEGORY_VIANDES,
        "🍢",
        19.9,
        "1 kg",
        description_extra="Brochettes d'agneau {H} prêtes pour le barbecue.",
        ingredients="Viande d'agneau ({H}), marinade.",
        usage_tips="Griller à feu vif en retournant régulièrement.",
        conservation="Surgelé — conserver à -18 °C.",
    ),
    _lf(
        "UD-BROCH-P",
        "brochettes-poulet-{H}-1kg",
        "Brochettes de poulet {H}",
        "1 kg — marinées, prêtes à cuire.",
        CATEGORY_VIANDES,
        "🍢",
        13.9,
        "1 kg",
        description_extra="Brochettes de poulet {H} pour plancha et apéritifs.",
        ingredients="Viande de poulet ({H}), marinade.",
        usage_tips="Griller ou cuire au four jusqu'à cœur.",
        conservation="Surgelé — conserver à -18 °C.",
    ),
    _lf(
        "UD-ESCAR",
        "viande-escargot-500g",
        "Viande d'escargot",
        "500–600 g — sans coque.",
        CATEGORY_VIANDES,
        "🐌",
        24.0,
        "500–600 g",
        description_extra="Viande d'escargot pour sauces et plats africains.",
        ingredients="Viande d'escargot.",
        usage_tips="Mijoter dans une sauce épicée selon la recette.",
        conservation="Surgelé — conserver à -18 °C.",
    ),
'''

DISPLAY = {
    f"morceaux-agneau-{H}-1kg": f"Morceaux d'agneau {H} — 1 kg",
    f"cotelettes-agneau-{H}-1kg": f"Côtelettes d'agneau {H} — 1 kg",
    f"gigot-agneau-{H}": f"Gigot d'agneau {H} — ≈ 1,5 kg",
    f"morceaux-mouton-{H}-1kg": f"Morceaux de mouton {H} — 1 kg",
    f"steak-hache-boeuf-{H}-1kg": f"Steak haché bœuf {H} — 1 kg",
    f"foie-boeuf-{H}-1kg": f"Foie de bœuf {H} — 1 kg",
    f"tripes-boeuf-{H}-1kg": f"Tripes de bœuf {H} — 1 kg",
    f"cotes-boeuf-{H}-1kg": f"Côtes de bœuf {H} — 1 kg",
    f"pieds-boeuf-{H}-1kg": f"Pieds de bœuf {H} — 1 kg",
    f"filets-poulet-{H}-1kg": f"Filets de poulet {H} — 1 kg",
    f"hauts-cuisse-poulet-{H}-5kg": f"Hauts de cuisse poulet {H} — 5 kg",
    f"pintade-entiere-{H}": f"Pintade entière {H} — ≈ 1,5 kg",
    f"escalopes-dinde-{H}-1kg": f"Escalopes de dinde {H} — 1 kg",
    f"merguez-boeuf-{H}-1kg": f"Merguez bœuf {H} — 1 kg",
    f"kefta-{H}-1kg": f"Kefta {H} — 1 kg",
    f"brochettes-agneau-{H}-1kg": f"Brochettes d'agneau {H} — 1 kg",
    f"brochettes-poulet-{H}-1kg": f"Brochettes de poulet {H} — 1 kg",
    "viande-escargot-500g": "Viande d'escargot — 500–600 g",
}


def patch_catalogue() -> None:
    path = ROOT / "models" / "catalogue_labelafrik.py"
    text = path.read_text(encoding="utf-8")
    if f"morceaux-agneau-{H}-1kg" in text:
        print("catalogue already has new meats")
        return
    marker = "LABELAFRIK_VIANDES = ["
    start = text.find(marker)
    if start < 0:
        raise SystemExit("LABELAFRIK_VIANDES not found")
    # Closing ] of the list: first \n]\n after start that is at indent 0
    end = text.find("\n]\n\nLABELAFRIK_EXTRA", start)
    if end < 0:
        end = text.find("\n]\n\nLABELAFRIK", start)
    if end < 0:
        raise SystemExit("end of LABELAFRIK_VIANDES not found")
    # Ensure previous entry has a trailing comma before insert
    before = text[:end].rstrip()
    if not before.endswith(","):
        # last entry ends with ),
        if before.endswith(")"):
            before += ","
    text = before + "\n" + NEW_BLOCK.rstrip() + "\n]" + text[end + 2 :]
    path.write_text(text, encoding="utf-8")
    print("catalogue patched")


def patch_names() -> None:
    path = ROOT / "models" / "product_names.py"
    text = path.read_text(encoding="utf-8")
    if f"morceaux-agneau-{H}-1kg" in text:
        print("names already patched")
        return
    anchor = f'    "morceaux-boeuf-1kg": "Morceaux de bœuf {H} — 1 kg",\n'
    if anchor not in text:
        raise SystemExit("names anchor not found")
    extra = "".join(f'    "{slug}": "{name}",\n' for slug, name in DISPLAY.items())
    text = text.replace(anchor, anchor + extra, 1)
    path.write_text(text, encoding="utf-8")
    print("names patched")


def patch_images_map() -> None:
    path = ROOT / "models" / "product_images.py"
    text = path.read_text(encoding="utf-8")
    if f"morceaux-agneau-{H}-1kg" in text:
        print("images map already patched")
        return
    anchor = '    "morceaux-boeuf-1kg": "img/products/morceaux-boeuf-1kg.jpg",\n'
    if anchor not in text:
        raise SystemExit("images anchor not found")
    extra = "".join(
        f'    "{slug}": "img/products/{slug}.jpg",\n' for slug in DISPLAY
    )
    text = text.replace(anchor, anchor + extra, 1)
    path.write_text(text, encoding="utf-8")
    print("images map patched")


def main() -> None:
    patch_catalogue()
    patch_names()
    patch_images_map()

    # Validate syntax by importing
    from models.catalogue_labelafrik import LABELAFRIK_VIANDES

    slugs = [p["slug"] for p in LABELAFRIK_VIANDES]
    print("viandes count", len(slugs))
    missing = [s for s in DISPLAY if s not in slugs]
    if missing:
        print("MISSING from catalogue", missing)

    # Generate placeholders for products without real photos yet
    from scripts.gen_viandes_images import main as gen_images

    # Expand SKIP in gen to keep existing real photos
    gen_images()

    from app import app
    from models.seed import sync_catalogue
    from models.product_images import sync_product_images

    with app.app_context():
        sync_catalogue()
        sync_product_images(str(ROOT))
        from models.product import Product

        n = Product.query.filter_by(category="viandes", is_active=True).count()
        print("active viandes in DB", n)


if __name__ == "__main__":
    main()
