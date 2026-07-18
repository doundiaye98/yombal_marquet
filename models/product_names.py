# -*- coding: utf-8 -*-
"""
Noms d'affichage boutique — convention : « Produit — conditionnement ».
Le conditionnement reprend weight_info (sans texte emballage).
"""

# Noms complets par slug (prioritaires)
PRODUCT_DISPLAY_NAMES = {
    # —— Catalogue initial ——
    "couscous-complet-1kg": "Couscous complet — 1 kg",
    "huile-argan-bio-100ml": "Huile d'argan bio — 100 ml",
    "miel-thym-500g": "Miel d'acacia — 500 g",
    "cafe-arabica-250g": "Café arabica — 250 g",
    "savon-noir-eucalyptus": "Savon noir eucalyptus — 200 g",
    "beurre-karite-brut-150g": "Beurre de karité — 150 g",
    "huile-palme-artisanale-1l": "Huile de palme artisanale — 1 L",
    # —— Extension terroir ——
    "bissap-seche-200g": "Bissap séché — 200 g",
    "gingembre-poudre-100g": "Gingembre — 100 g",
    "bouye-baobab-250g": "Baobab — 250 g",
    "ditakh-300g": "Ditakh — 300 g",
    "kinkeliba-80g": "Kinkeliba — 80 g",
    "cafe-touba-250g": "Café Touba — 250 g",
    "tamarin-pulpe-200g": "Dakhar — 200 g",
    "mil-millet-1kg": "Mil — 1 kg",
    "sorgho-1kg": "Sorgho — 1 kg",
    "fonio-500g": "Fonio — 500 g",
    "farine-niebe-500g": "Farine de niébé — 500 g",
    "soumbala-100g": "Soumbala — 100 g",
    "netetou-100g": "Nététou — 100 g",
    "yett-coquillages-150g": "Yett — 150 g",
    "piment-sec-moulu-80g": "Piment moulu — 80 g",
    "sel-kaolack-500g": "Sel de Kaolack — 500 g",
    "beurre-karite-alimentaire-250g": "Beurre de karité alimentaire — 250 g",
    "thiakry-400g": "Thiakhry — 400 g",
    "legumes-seches-thiebou-200g": "Légumes séchés thiéb — 200 g",
    "crevettes-sechees-100g": "Crevettes séchées — 100 g",
    "graine-sesame-250g": "Graines de sésame — 250 g",
    # —— LabelAfrik phares ——
    "arraw-mil-labelafrik": "Arraw — 500 g",
    "sankhal-labelafrik": "Sankhal — 500 g",
    "thiere-lalo-labelafrik": "Thiéré lalo — 500 g",
    "soungouf-labelafrik": "Soungouf — 500 g",
    "moringa-poudre-labelafrik": "Moringa — 100 g",
    "gombo-poudre-labelafrik": "Gombo — 100 g",
    "pate-arachide-labelafrik": "Pâte d'arachide — 500 g",
    # —— Riz ——
    "riz-long-parfume-20kg": "Riz long parfumé — 20 kg",
    "riz-brise-2x-20kg": "Riz brisé (2×) — 20 kg",
    "riz-brise-1x-20kg": "Riz brisé (1×) — 20 kg",
    "riz-long-parfume-45kg": "Riz long parfumé — 4,5 kg",
    "riz-brise-1x-5kg": "Riz brisé (1×) — 5 kg",
    "riz-brise-2x-5kg": "Riz brisé (2×) — 5 kg",
    "riz-long-parfume-thai-1kg": "Riz long parfumé thaï — 1 kg",
    "riz-long-parfume-1kg": "Riz long parfumé — 1 kg",
    "riz-brise-2x-1kg": "Riz brisé (2×) — 1 kg",
    "riz-casse-1x-1kg": "Riz cassé (1×) — 1 kg",
    "riz-casse-2x-1kg": "Riz cassé (2×) — 1 kg",
    # —— Farines & céréales ——
    "farine-riz-1kg": "Farine de riz — 1 kg",
    "farine-mil-1kg": "Farine de mil — 1 kg",
    "farine-manioc-1kg": "Farine de manioc — 1 kg",
    "fecule-pomme-de-terre-1kg": "Fécule de pomme de terre — 1 kg",
    "farine-mais-jaune": "Farine de maïs jaune — 1 kg",
    "farine-mais-blanc": "Farine de maïs blanc — 1 kg",
    "grain-de-mil": "Grains de mil — 1 kg",
    "foufou-farine-manioc": "Foufou — 500 g",
    "fufu-farine-plantain": "Fufu plantain — 600 g",
    "fiono-guinee": "Fiono — 500 g",
    # —— Huiles ——
    "huile-tournesol-1l": "Huile de tournesol — 1 L",
    "huile-arachide-1l": "Huile d'arachide — 1 L",
    "huile-tournesol-5l": "Huile de tournesol — 5 L",
    "huile-palme-1l": "Huile de palme — 1 L",
    "butter-ghee": "Beurre ghee — 500 g",
    # —— Boissons ——
    "sirop-bissap-ud": "Sirop de bissap — 50 cl",
    "sirop-gingembre-ud": "Sirop de gingembre — 50 cl",
    "boisson-gingembre-ud": "Boisson au gingembre — 1 L",
    "bissap-rouge-vrac-1kg": "Bissap rouge — 1 kg",
    "poudre-baobab-zena-200g": "Baobab Zena — 200 g",
    "miel-fleurs-1kg": "Miel de fleurs — 1 kg",
    "lait-coco-ud": "Lait de coco — 400 ml",
    "bissap-rouge-zena": "Bissap blanc Zena — 125 g",
    "poudre-lait-nido-400g": "Lait en poudre Nido — 400 g",
    "poudre-lait-nido-900g": "Lait en poudre Nido — 900 g",
    "poudre-lait-nido-1800g": "Lait en poudre Nido — 1,8 kg",
    "poudre-lait-nido-2500g": "Lait en poudre Nido — 2,5 kg",
    "the-instantane-starling": "Thé instantané Starling",
    "boisson-instantanee-foster": "Boisson instantanée Foster",
    # —— Snacks ——
    "chips-plantain-doux": "Chips de plantain — doux",
    "chips-plantain-epice": "Chips de plantain — épicé",
    "chips-plantain-sale": "Chips de plantain — salé",
    "biscuits-gem": "Biscuits Gem",
    "samoussas-legumes-halal": "Samoussas légumes — 20 pièces",
    "samoussas-poulet-20": "Samoussas poulet — 20 pièces",
    "samoussas-mouton-halal": "Samoussas mouton — 20 pièces",
    "accras-morue": "Accras de morue",
    "nems-poulet-halal-50": "Nems poulet — 50 pièces",
    "nems-crevettes-poulet-halal": "Nems crevettes & poulet — 50 pièces",
    "thiacry-de-mil": "Thiakhry (préparation) — 400 g",
    # —— Légumineuses ——
    "cornilles-haricots-blancs": "Cornilles — 500 g",
    "haricots-noirs-tersol": "Haricots noirs Tersol — 500 g",
    "arachides-crues-blanches-1kg": "Arachides crues — 1 kg",
    # —— Condiments ——
    "poudre-arachide-ud": "Poudre d'arachide — 500 g",
    "pate-arachide-dakatine": "Pâte d'arachide Dakatine",
    "piment-rouge-antillais": "Piment antillais fort",
    "bouillon-adjia": "Bouillon Adjia",
    "jumbo-ramadan": "Bouillon Jumbo Ramadan",
    "pate-arachide-25kg": "Pâte d'arachide — 2,5 kg",
    "pate-arachide-bonmafe": "Pâte d'arachide Bonmafe — 850 g",
    "pate-arachide-pcd-500g": "Pâte d'arachide PCD — 500 g",
    "sauce-trofai-palmier-350": "Sauce graine de palme Trofai — 350 g",
    "sauce-trofai-palmier-410": "Sauce graine de palme Trofai — 410 g",
    "concentre-tomates-rolli": "Concentré de tomates Rolli — 880 g",
    "concentre-tomates-2kg": "Concentré de tomates — 2 kg",
    "jus-citron-sicile-1l": "Jus de citron — 1 L",
    # —— Fruits séchés ——
    "dattes-seches-ud": "Dattes sèches — 500 g",
    "dattes-branchees-ud": "Dattes branchées — 500 g",
    "dattes-demi-seches-ud": "Dattes demi-sèches — 500 g",
    "raisins-secs-golden": "Raisins secs golden — 500 g",
    "dakhar-sachet-150g": "Dakhar — 150 g",
    "dakhar-sachet-375g": "Dakhar — 375 g",
    # —— Conserves & aliments ——
    "corned-beef-halal": "Corned beef halal — 340 g",
    "maad-230g": "Maad en boîte — 230 g",
    "maad-400g": "Maad en boîte — 400 g",
    "poisson-fume-ud": "Poisson fumé — 500 g",
    "rouge-barbet-ud": "Poisson rouge barbet — 1 kg",
    "pate-sardinelle-pinton": "Pâte de sardinelle Pinton",
    "sardinelle-pilchards-tomate": "Sardinelles à la tomate",
}


def _normalize_weight(weight_info: str | None) -> str | None:
    if not weight_info:
        return None
    part = weight_info.split("—")[0].split(",")[0].strip()
    return part or None


def display_name_for_product(slug: str, weight_info: str | None = None, fallback: str = "") -> str:
    """Retourne le nom boutique cohérent pour un slug."""
    if slug in PRODUCT_DISPLAY_NAMES:
        return PRODUCT_DISPLAY_NAMES[slug]
    base = fallback.strip() or slug.replace("-", " ").title()
    w = _normalize_weight(weight_info)
    if w and w.lower() not in base.lower():
        return f"{base} — {w}"
    return base


def apply_display_name(row: dict) -> dict:
    """Enrichit une ligne catalogue avec le nom d'affichage."""
    slug = row.get("slug", "")
    row = dict(row)
    row["name"] = display_name_for_product(slug, row.get("weight_info"), row.get("name", ""))
    return row
