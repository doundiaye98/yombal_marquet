# -*- coding: utf-8 -*-
"""Catalogue Univers Diaspora / LabelAfrik — prix et fiches produits."""

from models.constants import (
    CATEGORY_ALIMENTAIRE,
    CATEGORY_BOISSONS,
    CATEGORY_CEREALES,
    CATEGORY_CONDIMENTS,
    CATEGORY_CONSERVES,
    CATEGORY_COSMETIQUE,
    CATEGORY_FRUITS_SECS,
    CATEGORY_HUILES,
    CATEGORY_LEGUMINEUSES,
    CATEGORY_POISSON,
    CATEGORY_SNACKS,
    CATEGORY_VIANDES,
)

_BRAND = "LabelAfrik · Univers Diaspora"
_ORIGIN = "Sénégal & Afrique de l'Ouest — LabelAfrik"


def _euros(v):
    return int(round(float(v) * 100))


def _lf(
    sku,
    slug,
    name,
    summary,
    category,
    icon,
    price_euros,
    weight_info,
    *,
    description_extra="",
    ingredients="",
    usage_tips="",
):
    desc = (
        f"{summary}\n\n"
        f"Produit {_BRAND} — L'Afrique, dans chaque grain.\n\n"
        f"{description_extra}"
    ).strip()
    return {
        "sku": sku,
        "slug": slug,
        "name": name,
        "summary": summary,
        "description": desc,
        "price_cents": _euros(price_euros),
        "category": category,
        "icon": icon,
        "origin": _ORIGIN,
        "weight_info": weight_info,
        "ingredients": ingredients,
        "usage_tips": usage_tips,
        "conservation": "À l'abri de la lumière et de l'humidité.",
    }


# Mises à jour des produits déjà en boutique (photos existantes)
LABELAFRIK_UPDATES = {
    "thiakry-400g": _lf(
        "LF-THIAKRY",
        "thiakry-400g",
        "Thiakhry",
        "Dessert africain onctueux à base d'arraw de mil — sans gluten.",
        CATEGORY_SNACKS,
        "🍮",
        3,
        "400 g",
        description_extra=(
            "Délicieux avec du lait, du yaourt ou des fruits. "
            "Tradition gourmande et nutritive de nos terroirs."
        ),
    ),
    "fonio-500g": _lf(
        "LF-FONIO",
        "fonio-500g",
        "Fonio",
        "Céréale ancestrale sans gluten — graine du passé, saveur d'avenir.",
        CATEGORY_CEREALES,
        "✨",
        4,
        "500 g",
        description_extra="Léger, nutritif, cuisson rapide (~5 min). Meilleur que le quinoa.",
    ),
    "bouye-baobab-250g": _lf(
        "LF-BAOBAB",
        "bouye-baobab-250g",
        "Baobab",
        "Poudre de fruit de baobab — superaliment riche en vitamine C.",
        CATEGORY_BOISSONS,
        "🌳",
        3.9,
        "250 g",
        description_extra="L'arbre de vie africain. Idéal en jus, smoothies, yaourts et pâtisseries.",
    ),
    "farine-niebe-500g": _lf(
        "LF-NIEBE",
        "farine-niebe-500g",
        "Niébé",
        "Légumineuse africaine riche en protéines végétales.",
        CATEGORY_LEGUMINEUSES,
        "🫘",
        4,
        "500 g",
        description_extra="Couscous, beignets akara, soupes et plats mijotés. Sans gluten.",
    ),
    "kinkeliba-80g": _lf(
        "LF-KINKELIBA",
        "kinkeliba-80g",
        "Kinkeliba",
        "Infusion bien-être d'Afrique — digestive et tonifiante.",
        CATEGORY_BOISSONS,
        "🍃",
        2.5,
        "80 g",
        description_extra="Sans caféine. Infusion 5–8 min, chaude ou froide.",
    ),
    "bissap-seche-200g": _lf(
        "LF-BISSAP",
        "bissap-seche-200g",
        "Bissap",
        "Fleurs d'hibiscus — rouge & blanc, infusion bien-être.",
        CATEGORY_BOISSONS,
        "🌺",
        2.5,
        "200 g",
        description_extra="Rouge : vitalité acidulée. Blanc : douceur et fraîcheur.",
    ),
    "gingembre-poudre-100g": _lf(
        "LF-GINGEMBRE",
        "gingembre-poudre-100g",
        "Gingembre",
        "Épice africaine 100 % naturelle — énergie et digestion.",
        CATEGORY_CONDIMENTS,
        "🫚",
        2,
        "100 g",
        description_extra="Plats, infusions, pâtisseries et smoothies.",
    ),
    "miel-thym-500g": _lf(
        "LF-MIEL",
        "miel-thym-500g",
        "Miel",
        "Miel d'acacia du Sénégal — douceur délicate et énergisante.",
        CATEGORY_ALIMENTAIRE,
        "🍯",
        5,
        "500 g",
        description_extra="Récolté au cœur des acacias. Boissons, desserts et bien-être.",
    ),
    "beurre-karite-brut-150g": _lf(
        "LF-KARITE",
        "beurre-karite-brut-150g",
        "Karité pur",
        "Beurre de karité biologique — soin peau et cheveux.",
        CATEGORY_COSMETIQUE,
        "✨",
        3,
        "150 g",
        description_extra="100 % naturel, vitamines A, D, E et F. Biosene / LabelAfrik.",
    ),
    "mil-millet-1kg": _lf(
        "LF-MIL",
        "mil-millet-1kg",
        "Mil (dougoupe)",
        "Céréale de base — bouillies, thiéré et fondé.",
        CATEGORY_CEREALES,
        "🌿",
        2.5,
        "1 kg",
    ),
    "tamarin-pulpe-200g": _lf(
        "LF-DAKHAR",
        "tamarin-pulpe-200g",
        "Dakhar (Tamarin)",
        "Pulpe acidulée pour jus et sauces traditionnelles.",
        CATEGORY_BOISSONS,
        "🍫",
        2.9,
        "200 g",
    ),
    "cafe-touba-250g": _lf(
        "LF-CAFE-TOUBA",
        "cafe-touba-250g",
        "Café Touba",
        "Café épicé au diar — spécialité sénégalaise.",
        CATEGORY_BOISSONS,
        "☕",
        3.5,
        "250 g",
    ),
}

# Nouveaux produits phares LabelAfrik (sans photo — emoji vitrine)
LABELAFRIK_PHARES = [
    _lf(
        "LF-ARRAW",
        "arraw-mil-labelafrik",
        "Arraw",
        "Porridge africain sain sans gluten — à base de mil.",
        CATEGORY_CEREALES,
        "🌾",
        3,
        "500 g",
        description_extra="Naturel, nutritif et savoureux pour toute la famille.",
    ),
    _lf(
        "LF-SANKHAL",
        "sankhal-labelafrik",
        "Sankhal",
        "Classique à base de mil — bouillies nourrissantes.",
        CATEGORY_CEREALES,
        "🥣",
        3,
        "500 g",
        description_extra="100 % naturel, sans gluten. Tradition en fête.",
    ),
    _lf(
        "LF-THIERE-LALO",
        "thiere-lalo-labelafrik",
        "Thiéré Lalo",
        "Couscous de mil traditionnel — riche en fibres.",
        CATEGORY_CEREALES,
        "🍲",
        3,
        "500 g",
        description_extra="Plat principal ou version sucrée. Sans gluten.",
    ),
    _lf(
        "LF-SOUNGOUF",
        "soungouf-labelafrik",
        "Soungouf",
        "Farine de mil — base de l'alimentation africaine.",
        CATEGORY_CEREALES,
        "🌾",
        3,
        "500 g",
        description_extra="Bouillies, galettes, pâtes. Énergie quotidienne.",
    ),
    _lf(
        "LF-MORINGA",
        "moringa-poudre-labelafrik",
        "Moringa",
        "Poudre de feuilles — superaliment riche en nutriments.",
        CATEGORY_CONDIMENTS,
        "🌿",
        5,
        "100 g",
        description_extra="Boissons, compléments et cuisine santé.",
    ),
    _lf(
        "LF-GOMBO",
        "gombo-poudre-labelafrik",
        "Gombo",
        "Poudre de gombo 100 % naturelle.",
        CATEGORY_CONDIMENTS,
        "🥬",
        2,
        "100 g",
        description_extra="Épaissit sauces et soupes traditionnelles.",
    ),
    _lf(
        "LF-PATE-ARACHIDE",
        "pate-arachide-labelafrik",
        "Pâte d'arachide",
        "Pâte onctueuse 100 % naturelle — protéines et fibres.",
        CATEGORY_CONDIMENTS,
        "🥜",
        2.5,
        "500 g",
        description_extra="Sauces traditionnelles, tartines et petit-déjeuner.",
    ),
]

LABELAFRIK_RIZ = [
    _lf("UD-RIZ-LP20", "riz-long-parfume-20kg", "Riz long parfumé", "Riz long parfumé — sac 20 kg.", CATEGORY_CEREALES, "🌾", 40, "20 kg"),
    _lf("UD-RIZ-B2-20", "riz-brise-2x-20kg", "Riz brisé 2 fois", "Riz brisé deux fois — sac 20 kg.", CATEGORY_CEREALES, "🌾", 28, "20 kg"),
    _lf("UD-RIZ-B1-20", "riz-brise-1x-20kg", "Riz brisé 1 fois", "Riz brisé une fois — sac 20 kg.", CATEGORY_CEREALES, "🌾", 28.9, "20 kg"),
    _lf("UD-RIZ-LP-45", "riz-long-parfume-45kg", "Riz long parfumé", "Riz long parfumé — sac 4,5 kg.", CATEGORY_CEREALES, "🌾", 12.5, "4,5 kg"),
    _lf("UD-RIZ-B1-5", "riz-brise-1x-5kg", "Riz brisé 1 fois", "Riz brisé une fois — sac 5 kg.", CATEGORY_CEREALES, "🌾", 8.9, "5 kg"),
    _lf("UD-RIZ-B2-5", "riz-brise-2x-5kg", "Riz brisé 2 fois", "Riz brisé deux fois — sac 5 kg.", CATEGORY_CEREALES, "🌾", 7.9, "5 kg"),
    _lf("UD-RIZ-LP-THAI", "riz-long-parfume-thai-1kg", "Riz long parfumé thaï", "Arôme délicat — sac 1 kg.", CATEGORY_CEREALES, "🌾", 2.5, "1 kg"),
    _lf("UD-RIZ-LP-1", "riz-long-parfume-1kg", "Riz long parfumé", "Riz long parfumé — sac 1 kg.", CATEGORY_CEREALES, "🌾", 2.5, "1 kg"),
    _lf("UD-RIZ-B2-1", "riz-brise-2x-1kg", "Riz brisé 2 fois", "Riz brisé deux fois — sac 1 kg.", CATEGORY_CEREALES, "🌾", 1.6, "1 kg"),
    _lf("UD-RIZ-C1-1", "riz-casse-1x-1kg", "Riz cassé 1 fois", "Riz cassé une fois — sac 1 kg.", CATEGORY_CEREALES, "🌾", 1.8, "1 kg"),
]

LABELAFRIK_FARINES = [
    _lf("UD-FR-RIZ", "farine-riz-1kg", "Farine de riz", "Fine et légère — sans gluten.", CATEGORY_CEREALES, "🌾", 1.5, "1 kg"),
    _lf("UD-FR-MIL", "farine-mil-1kg", "Farine de mil", "Riche et nutritive.", CATEGORY_CEREALES, "🌾", 2.9, "1 kg"),
    _lf("UD-FR-MANIOC", "farine-manioc-1kg", "Farine de manioc", "Traditionnelle et polyvalente.", CATEGORY_CEREALES, "🌾", 2.9, "1 kg"),
    _lf("UD-FECULE-PT", "fecule-pomme-de-terre-1kg", "Fécule de pomme de terre", "Épaississant pour sauces et pâtisserie.", CATEGORY_CEREALES, "🥔", 1.2, "1 kg"),
    _lf("UD-FR-MAIS-J", "farine-mais-jaune", "Farine de maïs jaune", "Fine et polyvalente.", CATEGORY_CEREALES, "🌽", 2.2, "1 kg"),
    _lf("UD-FR-MAIS-B", "farine-mais-blanc", "Farine de maïs blanc", "Bouillies et galettes.", CATEGORY_CEREALES, "🌽", 2.25, "1 kg"),
    _lf("UD-GRAIN-MIL", "grain-de-mil", "Grain de mil", "Grains entiers pour bouillies.", CATEGORY_CEREALES, "🌿", 2.5, "1 kg"),
]

LABELAFRIK_HUILES = [
    _lf("UD-HL-TOUR-1", "huile-tournesol-1l", "Huile de tournesol", "Légère — cuisson et assaisonnement.", CATEGORY_HUILES, "🫒", 3.9, "1 L"),
    _lf("UD-HL-ARACH-1", "huile-arachide-1l", "Huile d'arachide", "Riche et savoureuse.", CATEGORY_HUILES, "🥜", 2.9, "1 L"),
    _lf("UD-HL-TOUR-5", "huile-tournesol-5l", "Huile de tournesol", "Format familial 5 L.", CATEGORY_HUILES, "🫒", 17.9, "5 L"),
    _lf("UD-HL-PALME-1", "huile-palme-1l", "Huile de palme", "Parfumée — plats traditionnels.", CATEGORY_HUILES, "🫒", 5, "1 L"),
]

LABELAFRIK_BOISSONS = [
    _lf("UD-SIR-BISSAP", "sirop-bissap-ud", "Sirop de bissap", "Sucré et fruité — boissons rafraîchissantes.", CATEGORY_BOISSONS, "🌺", 5, "50 cl"),
    _lf("UD-SIR-GING", "sirop-gingembre-ud", "Sirop de gingembre", "Épicé et tonifiant.", CATEGORY_BOISSONS, "🫚", 5, "50 cl"),
    _lf("UD-BOIS-GING", "boisson-gingembre-ud", "Boisson de gingembre", "Rafraîchissante et énergisante.", CATEGORY_BOISSONS, "🫚", 5, "1 L"),
    _lf("UD-BISSAP-VRAC", "bissap-rouge-vrac-1kg", "Bissap rouge vrac", "Fleurs d'hibiscus — sac 1 kg.", CATEGORY_BOISSONS, "🌺", 10, "1 kg"),
    _lf("UD-POUD-ARACH", "poudre-arachide-ud", "Poudre d'arachide", "Fine et savoureuse.", CATEGORY_CONDIMENTS, "🥜", 2.9, "500 g"),
    _lf("UD-BOUYE-ZENA", "poudre-baobab-zena-200g", "Poudre de baobab Zena", "Vitamines et fibres — 200 g.", CATEGORY_BOISSONS, "🌳", 3, "200 g"),
    _lf("UD-MIEL-1KG", "miel-fleurs-1kg", "Miel", "Miel de fleurs — pot 1 kg.", CATEGORY_ALIMENTAIRE, "🍯", 9, "1 kg"),
    _lf("UD-LAIT-COCO", "lait-coco-ud", "Lait de coco", "Crémeux — sauces et desserts.", CATEGORY_BOISSONS, "🥥", 2.5, "400 ml"),
]

LABELAFRIK_SNACKS = [
    _lf("UD-CHIPS-PLT-D", "chips-plantain-doux", "Chips de plantain doux", "Croustillantes et légèrement sucrées.", CATEGORY_SNACKS, "🍌", 1, "sachet"),
    _lf("UD-CHIPS-PLT-E", "chips-plantain-epice", "Chips de plantain épicé", "Sucré et relevé.", CATEGORY_SNACKS, "🍌", 1, "sachet"),
    _lf("UD-CHIPS-PLT-S", "chips-plantain-sale", "Chips de plantain salé", "Croustillantes et savoureuses.", CATEGORY_SNACKS, "🍌", 1, "sachet"),
    _lf("UD-BISC-GEM", "biscuits-gem", "Biscuits sucrés Gem", "Croustillants — goûter.", CATEGORY_SNACKS, "🍪", 1.5, "sachet"),
    _lf("UD-SAM-LEG", "samoussas-legumes-halal", "Samoussas légumes halal", "Lot de 20 pièces.", CATEGORY_SNACKS, "🥟", 7.9, "20 pièces"),
    _lf("UD-SAM-POU", "samoussas-poulet-20", "Samoussas poulet", "Lot de 20 pièces.", CATEGORY_SNACKS, "🥟", 5.5, "20 pièces"),
    _lf("UD-ACCRAS", "accras-morue", "Accras de morue", "Beignets savoureux.", CATEGORY_SNACKS, "🐟", 7.9, "sachet"),
]

LABELAFRIK_LEGUMES = [
    _lf("UD-CORNILLES", "cornilles-haricots-blancs", "Cornilles", "Haricots blancs — soupes et ragoûts.", CATEGORY_LEGUMINEUSES, "🫘", 2.5, "500 g"),
    _lf("UD-HAR-NOIR", "haricots-noirs-tersol", "Haricots noirs", "Tersol — protéines et fibres.", CATEGORY_LEGUMINEUSES, "🫘", 1.99, "500 g"),
    _lf("UD-ARACH-CRU", "arachides-crues-blanches-1kg", "Arachides crues", "Blanches — 1 kg.", CATEGORY_LEGUMINEUSES, "🥜", 4.75, "1 kg"),
]

LABELAFRIK_CONDIMENTS = [
    _lf("UD-DAKATINE", "pate-arachide-dakatine", "Pâte d'arachide Dakatine", "Onctueuse — sauces et tartines.", CATEGORY_CONDIMENTS, "🥜", 5.9, "pot"),
    _lf("UD-PIM-ANT", "piment-rouge-antillais", "Piment rouge antillais", "Très piquant — arôme antillais.", CATEGORY_CONDIMENTS, "🌶️", 5.9, "pot"),
    _lf("UD-ADJIA", "bouillon-adjia", "Bouillon Adjia", "Épices en poudre — saveur rapide.", CATEGORY_CONDIMENTS, "🧂", 5.9, "sachet"),
    _lf("UD-JUMBO-RAM", "jumbo-ramadan", "Jumbo Ramadan", "Bouillon spécial Ramadan.", CATEGORY_CONDIMENTS, "🧂", 5.9, "sachet"),
    _lf("UD-PATE-25", "pate-arachide-25kg", "Pâte d'arachide", "Pot 2,5 kg.", CATEGORY_CONDIMENTS, "🥜", 15, "2,5 kg"),
    _lf("UD-PATE-BON", "pate-arachide-bonmafe", "Pâte d'arachide Bonmafe", "Pot 850 g.", CATEGORY_CONDIMENTS, "🥜", 7.9, "850 g"),
    _lf("UD-PATE-PCD", "pate-arachide-pcd-500g", "Pâte d'arachide PCD", "Pot 500 g.", CATEGORY_CONDIMENTS, "🥜", 2.5, "500 g"),
]

LABELAFRIK_FRUITS = [
    _lf("UD-DATTES-SEC", "dattes-seches-ud", "Dattes sèches", "Sucrées et nutritives.", CATEGORY_FRUITS_SECS, "🌴", 3.9, "500 g"),
    _lf("UD-DATTES-BR", "dattes-branchees-ud", "Dattes branchées", "Fraîches et savoureuses.", CATEGORY_FRUITS_SECS, "🌴", 5.9, "500 g"),
    _lf("UD-DATTES-DEM", "dattes-demi-seches-ud", "Dattes demi-sèches", "Moelleuses et naturellement sucrées.", CATEGORY_FRUITS_SECS, "🌴", 3.9, "500 g"),
    _lf("UD-RAISIN-SEC", "raisins-secs-golden", "Raisins secs golden", "Moelleux — collations.", CATEGORY_FRUITS_SECS, "🍇", 3.9, "500 g"),
    _lf("UD-TAM-150", "dakhar-sachet-150g", "Dakhar (Tamarin)", "Sachet 150 g.", CATEGORY_FRUITS_SECS, "🍫", 2, "150 g"),
    _lf("UD-TAM-375", "dakhar-sachet-375g", "Dakhar (Tamarin)", "Sachet 375 g.", CATEGORY_FRUITS_SECS, "🍫", 3.9, "375 g"),
]

LABELAFRIK_ALIMENTS = [
    _lf("UD-FOUFOU", "foufou-farine-manioc", "Foufou", "Farine de manioc prête à cuire.", CATEGORY_CEREALES, "🌾", 2.9, "500 g"),
    _lf("UD-FUFU", "fufu-farine-plantain", "Fufu plantain", "Farine de plantain — texture moelleuse.", CATEGORY_CEREALES, "🍌", 4.95, "600 g"),
    _lf("UD-FIONO", "fiono-guinee", "Fiono Guinée", "Préparation traditionnelle manioc/céréales.", CATEGORY_CEREALES, "🌾", 3.9, "500 g"),
    _lf("UD-THIACRY", "thiacry-de-mil", "Thiacry de mil", "Dessert traditionnel au mil et lait.", CATEGORY_SNACKS, "🍮", 1.8, "400 g"),
    _lf("UD-CORNED", "corned-beef-halal", "Corned beef halal", "Prêt à consommer — repas rapides.", CATEGORY_CONSERVES, "🥫", 2.5, "340 g"),
    _lf("UD-CITRON", "jus-citron-sicile-1l", "Jus de citron", "Citron jaune de Sicile — 1 L.", CATEGORY_CONDIMENTS, "🍋", 3.9, "1 L"),
    _lf("UD-GHEE", "butter-ghee", "Beurre ghee", "Beurre clarifié — cuisson et friture.", CATEGORY_HUILES, "🧈", 7.9, "500 g"),
    _lf("UD-MADD-230", "maad-230g", "Maad", "Boîte 230 g — fruit acidulé.", CATEGORY_CONSERVES, "🍋", 4.9, "230 g"),
    _lf("UD-MADD-400", "maad-400g", "Maad", "Boîte 400 g — fruit acidulé.", CATEGORY_CONSERVES, "🍋", 7.9, "400 g"),
    _lf("UD-BISSAP-Z", "bissap-rouge-zena", "Bissap blanc Zena", "Infusion douce et rafraîchissante.", CATEGORY_BOISSONS, "🌺", 2.5, "125 g"),
    _lf("UD-POISS-F", "poisson-fume-ud", "Poisson fumé", "Séché et fumé — soupes, sauces, thiéb.", CATEGORY_POISSON, "🐟", 18, "500 g"),
    _lf("UD-BARBET", "rouge-barbet-ud", "Rouge barbet", "Poisson frais — friture ou grillade.", CATEGORY_POISSON, "🐟", 7.5, "1 kg"),
]

LABELAFRIK_CONSERVES = [
    _lf("UD-TROFAI-35", "sauce-trofai-palmier-350", "Sauce Trofai", "Graine de palmier — pot 350 g.", CATEGORY_CONDIMENTS, "🫙", 3.5, "350 g"),
    _lf("UD-TROFAI-41", "sauce-trofai-palmier-410", "Sauce Trofai", "Graine de palmier — pot 410 g.", CATEGORY_CONDIMENTS, "🫙", 4.1, "410 g"),
    _lf("UD-TOM-ROLLI", "concentre-tomates-rolli", "Concentré de tomates Rolli", "Tube 880 g.", CATEGORY_CONDIMENTS, "🍅", 4.25, "880 g"),
    _lf("UD-TOM-2KG", "concentre-tomates-2kg", "Concentré de tomates", "Pot 2 kg.", CATEGORY_CONDIMENTS, "🍅", 7.5, "2 kg"),
    _lf("UD-SARD-P", "pate-sardinelle-pinton", "Pâte de sardinelle Pinton", "Sauces et plats de riz.", CATEGORY_CONSERVES, "🐟", 2.9, "pot"),
    _lf("UD-SARD-T", "sardinelle-pilchards-tomate", "Sardinelles à la sauce tomate", "Prêtes à consommer.", CATEGORY_CONSERVES, "🐟", 2.5, "boîte"),
    _lf("UD-NIDO-400", "poudre-lait-nido-400g", "Lait en poudre Nido", "Poudre Nido en sachet — riche en calcium et nutriments.", CATEGORY_BOISSONS, "🥛", 8.9, "400 g"),
    _lf("UD-NIDO-900", "poudre-lait-nido-900g", "Lait en poudre Nido", "Poudre Nido en sachet — riche en calcium et nutriments.", CATEGORY_BOISSONS, "🥛", 15.9, "900 g"),
    _lf("UD-NIDO-18", "poudre-lait-nido-1800g", "Lait en poudre Nido", "Poudre Nido en sachet — riche en calcium et nutriments.", CATEGORY_BOISSONS, "🥛", 26.9, "1,8 kg"),
    _lf("UD-NIDO-25", "poudre-lait-nido-2500g", "Lait en poudre Nido", "Poudre Nido en sachet — riche en calcium et nutriments.", CATEGORY_BOISSONS, "🥛", 34.9, "2,5 kg"),
    _lf("UD-STAR", "the-instantane-starling", "Thé instantané Starling", "Préparation rapide aromatique.", CATEGORY_BOISSONS, "☕", 2.5, "sachet"),
    _lf("UD-FOSTER", "boisson-instantanee-foster", "Boisson instantanée Foster Clark's", "Rafraîchissante et facile.", CATEGORY_BOISSONS, "🥤", 5, "sachet"),
]

LABELAFRIK_SNACKS_EXTRA = [
    _lf("UD-SAM-MOUT", "samoussas-mouton-halal", "Samoussas mouton halal", "Lot de 20 pièces.", CATEGORY_SNACKS, "🥟", 7.9, "20 pièces"),
    _lf("UD-NEMS-P", "nems-poulet-halal-50", "Nems poulet halal", "Lot de 50 pièces.", CATEGORY_SNACKS, "🥟", 22.5, "50 pièces"),
    _lf("UD-NEMS-CP", "nems-crevettes-poulet-halal", "Nems crevettes & poulet", "Lot de 50 pièces halal.", CATEGORY_SNACKS, "🥟", 25.9, "50 pièces"),
    _lf("UD-RIZ-C2", "riz-casse-2x-1kg", "Riz cassé 2 fois", "Sac 1 kg — absorption des sauces.", CATEGORY_CEREALES, "🌾", 1.6, "1 kg"),
]

LABELAFRIK_MER = [
    _lf(
        "UD-MER-T5",
        "merou-thiof-entier-5kg",
        "Mérou Thiof entier",
        "Frais et savoureux — carton de 5 kg.",
        CATEGORY_POISSON,
        "🐟",
        50,
        "carton 5 kg",
        description_extra="Idéal pour griller, cuire ou préparer des plats de poisson traditionnels.",
    ),
    _lf(
        "UD-MER-T5ST",
        "merou-thiof-sans-tete-5kg",
        "Mérou Thiof sans tête",
        "Gros mérou sans tête — carton de 5 kg.",
        CATEGORY_POISSON,
        "🐟",
        65,
        "carton 5 kg",
    ),
    _lf(
        "UD-MER-T10",
        "merou-thiof-entier-10kg",
        "Mérou Thiof entier",
        "Frais et savoureux — carton de 10 kg.",
        CATEGORY_POISSON,
        "🐟",
        90,
        "carton 10 kg",
    ),
    _lf(
        "UD-MER-T10ST",
        "merou-thiof-sans-tete-10kg",
        "Mérou Thiof sans tête",
        "Gros mérou sans tête — carton de 10 kg.",
        CATEGORY_POISSON,
        "🐟",
        125,
        "carton 10 kg",
    ),
    _lf(
        "UD-MER-PT",
        "petits-merous-thiof",
        "Petits mérous Thiof",
        "Frais et savoureux — parfaits pour griller ou frire.",
        CATEGORY_POISSON,
        "🐟",
        10,
        "au kg",
    ),
    _lf(
        "UD-MER-DD10",
        "dorade-diaregne-tete-10kg",
        "Dorade Diaregne avec tête",
        "Grosses dorades fraîches — carton de 10 kg.",
        CATEGORY_POISSON,
        "🐟",
        75,
        "carton 10 kg",
    ),
    _lf(
        "UD-MER-DD5",
        "dorade-diaregne-tete-5kg",
        "Dorade Diaregne avec tête",
        "Grosses dorades fraîches — carton de 5 kg.",
        CATEGORY_POISSON,
        "🐟",
        40,
        "carton 5 kg",
    ),
    _lf(
        "UD-MER-DD5ST",
        "dorade-diaregne-sans-tete-5kg",
        "Dorade Diaregne sans tête",
        "Grosses dorades sans tête — carton de 5 kg.",
        CATEGORY_POISSON,
        "🐟",
        80,
        "carton 5 kg",
    ),
    _lf(
        "UD-MER-DV10",
        "dorade-vivaneau-10kg",
        "Dorade plate Vivaneau",
        "Grosses dorades plates — carton de 10 kg.",
        CATEGORY_POISSON,
        "🐟",
        100,
        "carton 10 kg",
    ),
    _lf(
        "UD-MER-D58",
        "dorade-500-800-5kg",
        "Dorade 500–800 g",
        "Vidée, écaillée — carton de 5 kg.",
        CATEGORY_POISSON,
        "🐟",
        40,
        "carton 5 kg",
    ),
    _lf(
        "UD-MER-D46",
        "dorade-400-600-5kg",
        "Dorade 400–600 g",
        "Vidée, écaillée — carton de 5 kg.",
        CATEGORY_POISSON,
        "🐟",
        35,
        "carton 5 kg",
    ),
    _lf(
        "UD-MER-D10",
        "dorade-1000-plus-5kg",
        "Dorade 1000 g+",
        "Vidée, écaillée — carton de 5 kg.",
        CATEGORY_POISSON,
        "🐟",
        45,
        "carton 5 kg",
    ),
    _lf(
        "UD-MER-CB46",
        "capitaine-bar-400-600-5kg",
        "Capitaine Bar (Ombrine)",
        "400 à 600 g — carton de 5 kg.",
        CATEGORY_POISSON,
        "🐟",
        45,
        "carton 5 kg",
    ),
    _lf(
        "UD-MER-BAR5",
        "barracuda-seud-5kg",
        "Barracuda Seud",
        "Frais et savoureux — carton de 5 kg.",
        CATEGORY_POISSON,
        "🐟",
        40,
        "carton 5 kg",
    ),
    _lf(
        "UD-MER-CB68",
        "capitaine-bar-600-800-10kg",
        "Capitaine Bar (Ombrine)",
        "600 à 800 g — carton de 10 kg.",
        CATEGORY_POISSON,
        "🐟",
        90,
        "carton 10 kg",
    ),
    _lf(
        "UD-MER-BAR10",
        "barracuda-seud-10kg",
        "Barracuda Seud",
        "Conditionné en carton de 10 kg.",
        CATEGORY_POISSON,
        "🐟",
        70,
        "carton 10 kg",
        description_extra="Idéal pour grillades, fumé ou en sauce.",
    ),
    _lf(
        "UD-MER-SOLE",
        "sole-karabot",
        "Grosse sole Karabot",
        "Poisson plat à chair fine et délicate.",
        CATEGORY_POISSON,
        "🐟",
        22,
        "pièce",
    ),
    _lf(
        "UD-MER-SARD",
        "sardinelle-yaboye",
        "Sardinelle Yaboye",
        "Poisson savoureux pour plats traditionnels sénégalais.",
        CATEGORY_POISSON,
        "🐟",
        10,
        "sachet",
    ),
    _lf(
        "UD-MER-TILM",
        "tilapia-moyen-senegal",
        "Tilapia moyen Sénégal",
        "Chair tendre — four, poêle ou grill.",
        CATEGORY_POISSON,
        "🐟",
        20,
        "carton",
    ),
    _lf(
        "UD-MER-CHIN",
        "chinchard-600-900-10kg",
        "Chinchard entier 600/900",
        "Carton de 10 kg — chair ferme et goûteuse.",
        CATEGORY_POISSON,
        "🐟",
        35,
        "carton 10 kg",
    ),
    _lf(
        "UD-MER-TILX",
        "tilapia-gros-xxl-10kg",
        "Tilapia gros XXL",
        "Carton de 10 kg — grandes préparations.",
        CATEGORY_POISSON,
        "🐟",
        50,
        "carton 10 kg",
    ),
    _lf(
        "UD-MER-MACH",
        "gros-machoiron",
        "Gros machoiron",
        "Chair ferme — plats en sauce ou grillades.",
        CATEGORY_POISSON,
        "🐟",
        8,
        "pièce",
    ),
    _lf(
        "UD-CREV",
        "crevettes-crues-decortiquees",
        "Crevettes crues décortiquées",
        "Fraîches et prêtes à cuisiner.",
        CATEGORY_POISSON,
        "🦐",
        7,
        "sachet",
        description_extra="Sauces, plats sautés et recettes de fruits de mer.",
    ),
    _lf(
        "UD-GAMB",
        "gambas-geantes-sauvages",
        "Gambas géantes sauvages",
        "Fraîches et savoureuses.",
        CATEGORY_POISSON,
        "🦐",
        20,
        "sachet",
        description_extra="Grillées, sautées ou en plats de fruits de mer.",
    ),
    _lf(
        "UD-LANG",
        "queues-langoustes-blanches",
        "Queues de langoustes blanches",
        "Sauvages et fraîches.",
        CATEGORY_POISSON,
        "🦞",
        20,
        "sachet",
        description_extra="Plats raffinés et préparations de fruits de mer.",
    ),
    _lf(
        "UD-CRAB",
        "crabe-mangrove",
        "Crabe de mangrove",
        "Frais et savoureux.",
        CATEGORY_POISSON,
        "🦀",
        14.9,
        "pièce",
    ),
]

LABELAFRIK_VIANDES = [
    _lf(
        "UD-AILES",
        "ailes-poulet-texmex-halal",
        "Ailes de poulet Tex-Mex halal",
        "Lot de 2,5 kg — savoureuses et épicées.",
        CATEGORY_VIANDES,
        "🍗",
        17.5,
        "2,5 kg",
        description_extra="Parfaites pour griller ou cuire au four.",
    ),
]

LABELAFRIK_EXTRA = [
    _lf(
        "UD-MOR-F",
        "moringa-feuilles-poudre-100g",
        "Poudre de feuilles de moringa",
        "Riche en nutriments et antioxydants.",
        CATEGORY_CONDIMENTS,
        "🌿",
        3.5,
        "100 g",
        description_extra="Boissons, compléments et cuisine santé.",
    ),
    _lf(
        "UD-MIEL-5",
        "miel-fleurs-500g",
        "Miel de fleurs",
        "Naturel et savoureux — pot 500 g.",
        CATEGORY_ALIMENTAIRE,
        "🍯",
        5,
        "500 g",
    ),
]

LABELAFRIK_CATALOGUE = (
    LABELAFRIK_PHARES
    + LABELAFRIK_RIZ
    + LABELAFRIK_FARINES
    + LABELAFRIK_HUILES
    + LABELAFRIK_BOISSONS
    + LABELAFRIK_SNACKS
    + LABELAFRIK_SNACKS_EXTRA
    + LABELAFRIK_LEGUMES
    + LABELAFRIK_CONDIMENTS
    + LABELAFRIK_FRUITS
    + LABELAFRIK_ALIMENTS
    + LABELAFRIK_CONSERVES
    + LABELAFRIK_MER
    + LABELAFRIK_VIANDES
    + LABELAFRIK_EXTRA
)

LABELAFRIK_SLUGS = frozenset(
    list(LABELAFRIK_UPDATES.keys()) + [p["slug"] for p in LABELAFRIK_CATALOGUE]
)
