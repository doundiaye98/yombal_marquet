# -*- coding: utf-8 -*-
"""Catalogue Fruits et Légumes — Univers Diaspora (PDF fruits et légumes)."""

from models.constants import CATEGORY_FRUITS, CATEGORY_LEGUMES

_BRAND = "Univers Diaspora"
_ORIGIN = "Sénégal — Univers Diaspora"
_CONSERVATION = "Produit frais : à conserver au frais et consommer rapidement après réception."


def _euros(v):
    return int(round(float(v) * 100))


def _fl(
    sku,
    slug,
    name,
    summary,
    icon,
    price_euros,
    category,
    *,
    kind_label="Produit",
    description_extra="",
    usage_tips="",
):
    desc = (
        f"{summary}\n\n"
        f"Produit {_BRAND} — {kind_label} du Sénégal.\n\n"
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
        "weight_info": "1 kg",
        "ingredients": "",
        "usage_tips": usage_tips,
        "conservation": _CONSERVATION,
    }


def _fruit(*args, **kwargs):
    return _fl(*args, category=CATEGORY_FRUITS, kind_label="Fruits", **kwargs)


def _legume(*args, **kwargs):
    return _fl(*args, category=CATEGORY_LEGUMES, kind_label="Légumes", **kwargs)


# —— Fruits (prix au kilo, catalogue PDF) ——
_FRUITS = [
    _fruit(
        "UD-FL-MANGUE",
        "mangue-frais-1kg",
        "Mangue",
        "Juteuse, sucrée et parfumée — variétés Kent, Keitt et locales.",
        "🥭",
        3.0,
        description_extra=(
            "Cultivée principalement en Casamance, dans les Niayes et autour de Thiès. "
            "Chair jaune-orange, douce, idéale fraîche ou en jus."
        ),
        usage_tips="À manger mûre à point, en salade de fruits ou en jus.",
    ),
    _fruit(
        "UD-FL-PASTEQUE",
        "pasteque-frais-1kg",
        "Pastèque",
        "Chair rouge juteuse — hydratante et rafraîchissante.",
        "🍉",
        9.15,
        description_extra=(
            "Largement cultivée dans les Niayes. Riche en vitamines A et C et en lycopène."
        ),
        usage_tips="Servir bien fraîche, entière ou en tranches.",
    ),
    _fruit(
        "UD-FL-DITAKH",
        "ditakh-frais-1kg",
        "Ditakh",
        "Fruit tropical acidulé du Detarium senegalense — riche en vitamine C.",
        "🟢",
        6.10,
        description_extra=(
            "Pulpe fibreuse vert foncé autour d’un gros noyau. Saveur rappelant le citron ou le tamarin."
        ),
        usage_tips="Frais, en jus, nectar, marmelade ou sorbet.",
    ),
    _fruit(
        "UD-FL-BOUYE",
        "bouye-frais-1kg",
        "Bouye (fruit du baobab)",
        "Pulpe blanche acidulée du baobab — superaliment riche en vitamine C.",
        "🌳",
        3.66,
        description_extra=(
            "Aussi appelé pain de singe. Contient calcium, potassium, magnésium et fibres."
        ),
        usage_tips="Jus de bouye, sirop, confiture, sorbet ou poudre pour boissons.",
    ),
    _fruit(
        "UD-FL-MADD",
        "madd-frais-1kg",
        "Madd",
        "Fruit sauvage acidulé du Sahel — très populaire en Casamance.",
        "🟡",
        12.20,
        description_extra=(
            "Peau jaune-orange à maturité, pulpe juteuse douce-aigre. Riche en vitamine C."
        ),
        usage_tips="Frais avec sucre, sel ou piment ; en jus, sirop ou confiture.",
    ),
    _fruit(
        "UD-FL-PAPAYE",
        "papaye-frais-1kg",
        "Papaye",
        "Chair orange juteuse et douce — digeste grâce à la papaïne.",
        "🧡",
        41.16,
        description_extra=(
            "Fruit tropical à graines noires. Riche en vitamines C et A et en fibres."
        ),
        usage_tips="Frais, en salade de fruits, jus ou smoothie.",
    ),
    _fruit(
        "UD-FL-GOYAVE",
        "goyave-frais-1kg",
        "Goyave",
        "Sucrée-acidulée et très aromatique — exceptionnelle en vitamine C.",
        "🍈",
        0.91,
        description_extra=(
            "Chair blanche, rose ou rouge selon la variété, parsemée de petites graines."
        ),
        usage_tips="Frais, en jus, smoothie, confiture ou sorbet.",
    ),
    _fruit(
        "UD-FL-BANANE",
        "banane-frais-1kg",
        "Banane",
        "Douce et énergétique — riche en potassium et vitamine B6.",
        "🍌",
        1.86,
        description_extra="En-cas idéal, smoothie, salade de fruits ou cuite selon les recettes.",
        usage_tips="Consommer à maturité selon le degré de jaune souhaité.",
    ),
    _fruit(
        "UD-FL-ORANGE",
        "orange-locale-1kg",
        "Oranges locales",
        "Oranges du Sénégal — juteuses, sucrées, riches en vitamine C.",
        "🍊",
        4.85,
        description_extra="Cultivées notamment autour des Niayes et en Casamance.",
        usage_tips="Frais ou pressées en jus.",
    ),
    _fruit(
        "UD-FL-MANDARINE",
        "mandarine-frais-1kg",
        "Mandarine",
        "Petite, facile à éplucher — sucrée, juteuse et parfumée.",
        "🍊",
        3.15,
        description_extra="Idéale en saison sèche pour un encas rapide et vitaminé.",
        usage_tips="Frais, en jus ou en salade de fruits.",
    ),
    _fruit(
        "UD-FL-COROSSOL",
        "corossol-frais-1kg",
        "Corossol (graviola)",
        "Chair blanche crémeuse, douce et acidulée — énergisante.",
        "🤍",
        15.50,
        description_extra="Riche en vitamines C et B, fibres et antioxydants.",
        usage_tips="Frais, en jus, smoothie, sorbet ou dessert.",
    ),
    _fruit(
        "UD-FL-COCO",
        "noix-coco-frais-1kg",
        "Noix de coco",
        "Eau rafraîchissante et chair blanche — hydratante et nutritive.",
        "🥥",
        3.95,
        description_extra=(
            "Jeune (verte) pour l’eau ; mûre (brune) pour la chair, le râpé ou le lait de coco."
        ),
        usage_tips="Boire l’eau ; râper ou presser la chair pour cuisine et desserts.",
    ),
    _fruit(
        "UD-FL-ANANAS",
        "ananas-frais-1kg",
        "Ananas",
        "Sucré-acidulé et parfumé — digeste grâce à la bromélaïne.",
        "🍍",
        2.95,
        description_extra="Riche en vitamine C et en fibres. Goût tropical éclatant.",
        usage_tips="Frais, en jus, smoothie, salade ou plats sucrés-salés.",
    ),
    _fruit(
        "UD-FL-JUJUBE",
        "jujube-sidem-1kg",
        "Jujube (Sidem / Délem)",
        "Petit fruit croquant type pomme, plus sucré une fois séché.",
        "🟤",
        13.50,
        description_extra="Riche en vitamine C, fibres et minéraux — snack local nutritif.",
        usage_tips="Frais, séché, en jus ou en confiseries locales.",
    ),
    _fruit(
        "UD-FL-CAJOU",
        "pomme-cajou-frais-1kg",
        "Pomme de cajou",
        "Faux-fruit juteux sous la noix de cajou — très riche en vitamine C.",
        "🍎",
        22.95,
        description_extra="Jaune ou rouge à maturité. Goût exotique sucré-acidulé.",
        usage_tips="Frais, en jus, confiture ou recettes locales.",
    ),
    _fruit(
        "UD-FL-PLANTAIN",
        "plantain-frais-1kg",
        "Plantain",
        "Fruit polyvalent — frire, vapeur ou plats traditionnels.",
        "🍌",
        2.50,
        description_extra="Idéal pour alloco, bouillir ou accompagner les sauces.",
        usage_tips="Jaune mûr pour frire ; plus vert pour cuisson longue.",
    ),
    _fruit(
        "UD-FL-CITRON-VERT",
        "citron-vert-1kg",
        "Citron vert",
        "Acidulé et parfumé — assaisonnements, boissons et desserts.",
        "🍋",
        3.50,
        description_extra="Parfait pour marinades, jus et sauces.",
        usage_tips="Presser frais au dernier moment.",
    ),
]

# —— Légumes (prix au kilo, catalogue PDF) ——
_LEGUMES = [
    _legume(
        "UD-FL-OIGNON",
        "oignon-frais-1kg",
        "Oignon",
        "Base de la cuisine sénégalaise — vallée du fleuve Sénégal.",
        "🧅",
        0.50,
        description_extra="Indispensable pour thiéboudienne, sauces et marinades.",
        usage_tips="Émincer pour sauces, ragoûts et marinades.",
    ),
    _legume(
        "UD-FL-TOMATE",
        "tomate-frais-1kg",
        "Tomate",
        "Légèrement acidulée — base des sauces du thiéboudienne.",
        "🍅",
        2.55,
        description_extra="Riche en vitamine C et antioxydants.",
        usage_tips="Sauces, salades, ragoûts.",
    ),
    _legume(
        "UD-FL-GOMBO",
        "gombo-frais-1kg",
        "Gombo",
        "Texture caractéristique — central dans le soupou kandja.",
        "🌿",
        6.60,
        description_extra="Riche en fibres et vitamines A et C.",
        usage_tips="Couper et cuire dans les sauces et soupes traditionnelles.",
    ),
    _legume(
        "UD-FL-CAROTTE",
        "carotte-frais-1kg",
        "Carotte",
        "Douce et orangée — source de bêta-carotène.",
        "🥕",
        1.75,
        description_extra="Ragoûts, salades et accompagnements.",
        usage_tips="Crue en salade ou mijotée.",
    ),
    _legume(
        "UD-FL-CHOU",
        "chou-pomme-frais-1kg",
        "Chou pommé",
        "Croquant et polyvalent — plats mijotés et salades.",
        "🥬",
        0.95,
        description_extra="Riche en fibres, vitamine K et antioxydants.",
        usage_tips="Émincer pour salades ou cuire dans les sauces.",
    ),
    _legume(
        "UD-FL-CHOUFLEUR",
        "chou-fleur-frais-1kg",
        "Chou-fleur",
        "Texture tendre et goût doux — faible en calories.",
        "🥦",
        2.15,
        description_extra="Riche en vitamine C. Sauces, couscous et ragoûts.",
        usage_tips="À vapeur, en gratin ou en sauce.",
    ),
    _legume(
        "UD-FL-AUBERGINE",
        "aubergine-noire-1kg",
        "Aubergine noire",
        "Chair fondante — ragoûts, grillades et sauces.",
        "🍆",
        3.50,
        description_extra="Légume polyvalent de la cuisine sénégalaise et méditerranéenne.",
        usage_tips="Griller, mijoter ou farcir.",
    ),
    _legume(
        "UD-FL-DJAKHATO",
        "aubergine-amere-djakhato-1kg",
        "Aubergine amère (Djakhato)",
        "Aubergine amère locale — goût typique des sauces sénégalaises.",
        "🟢",
        5.10,
        description_extra="Appelée djakhato, très utilisée dans les préparations traditionnelles.",
        usage_tips="Cuire en sauce pour adoucir l’amertume.",
    ),
    _legume(
        "UD-FL-PDT",
        "pomme-terre-frais-1kg",
        "Pomme de terre",
        "Tubercule polyvalent — accompagnements et ragoûts.",
        "🥔",
        0.95,
        description_extra="Bouillie, frite, en purée ou dans les plats mijotés.",
        usage_tips="Éplucher et cuire selon la recette.",
    ),
    _legume(
        "UD-FL-PATATE",
        "patate-douce-1kg",
        "Patate douce",
        "Douce et nourrissante — riche en bêta-carotène.",
        "🍠",
        2.50,
        description_extra="Bouillie, frite ou en purée.",
        usage_tips="Cuire à l’eau ou au four.",
    ),
    _legume(
        "UD-FL-MANIOC",
        "manioc-frais-1kg",
        "Manioc",
        "Tubercule traditionnel — énergie et cuisine locale.",
        "🌾",
        1.80,
        description_extra="À bien cuire. Base de nombreuses préparations africaines.",
        usage_tips="Éplucher, faire bouillir ou fritter après cuisson complète.",
    ),
    _legume(
        "UD-FL-POIVRON",
        "poivron-vert-1kg",
        "Poivron vert",
        "Croquant et parfumé — sauces et accompagnements.",
        "🫑",
        2.05,
        description_extra="Apporte fraîcheur et couleur aux plats.",
        usage_tips="Émincer pour sauces, salades ou grillades.",
    ),
    _legume(
        "UD-FL-POIVRON-R",
        "poivron-rouge-1kg",
        "Poivron rouge",
        "Sucré et savoureux — salades, sautés et sauces.",
        "🌶️",
        2.50,
        description_extra="Plus doux que le poivron vert à maturité.",
        usage_tips="Idéal grillé, en salade ou en sauce.",
    ),
    _legume(
        "UD-FL-GINGEMBRE-F",
        "gingembre-frais-1kg",
        "Gingembre frais",
        "Racine aromatique et piquante — sauces, boissons, marinades.",
        "🫚",
        4.50,
        description_extra="Frais du marché — plus parfumé que la poudre.",
        usage_tips="Râper ou émincer selon la recette.",
    ),
    _legume(
        "UD-FL-PATATE-BL",
        "patate-douce-blanche-1kg",
        "Patate douce blanche",
        "Tubercule doux — plats cuits, rôtis ou en purée.",
        "🤍",
        2.50,
        description_extra="Chair claire, goût doux.",
        usage_tips="Bouillir, rôtir ou écraser en purée.",
    ),
    _legume(
        "UD-FL-PATATE-RO",
        "patate-douce-rose-1kg",
        "Patate douce rose",
        "Tubercule sucré — plats cuits, rôtis ou en purée.",
        "🩷",
        2.50,
        description_extra="Chair rosée, légèrement sucrée.",
        usage_tips="Bouillir, rôtir ou en purée.",
    ),
    _legume(
        "UD-FL-PIMENT",
        "piment-frais-1kg",
        "Piment",
        "Piquant caractéristique de la cuisine sénégalaise.",
        "🌶️",
        3.19,
        description_extra="Variétés rouges ou vertes. Riche en vitamine C.",
        usage_tips="Dosé selon le goût dans sauces et marinades.",
    ),
    _legume(
        "UD-FL-CONCOMBRE",
        "concombre-frais-1kg",
        "Concombre",
        "Hydratant et léger — idéal en salade.",
        "🥒",
        1.90,
        description_extra="Principalement composé d’eau, riche en minéraux.",
        usage_tips="Tranches froides ou salades.",
    ),
    _legume(
        "UD-FL-COURGETTE",
        "courgette-frais-1kg",
        "Courgette",
        "Tendre et douce — ragoûts, couscous et mijotés.",
        "🥒",
        2.15,
        description_extra="Faible en calories, vitamines du groupe B.",
        usage_tips="Sauter, mijoter ou griller.",
    ),
    _legume(
        "UD-FL-LAITUE",
        "laitue-frais-1kg",
        "Laitue",
        "Fraîche et croquante — salades légères.",
        "🥬",
        1.10,
        description_extra="Faible en calories, riche en eau, fibres et vitamine K.",
        usage_tips="Laver et consommer cru.",
    ),
    _legume(
        "UD-FL-HARICOT",
        "haricot-vert-1kg",
        "Haricot vert",
        "Croquant — accompagnement riche en fibres.",
        "🫛",
        2.50,
        description_extra="Apprécié pour sa texture et ses vitamines.",
        usage_tips="À la vapeur ou sauté en accompagnement.",
    ),
    _legume(
        "UD-FL-NIEBE",
        "niebe-frais-1kg",
        "Niébé",
        "Légumineuse populaire — protéines végétales et fibres.",
        "🫘",
        3.15,
        description_extra="Utilisé dans sauces, couscous ou bouillies au Sénégal.",
        usage_tips="Cuire jusqu’à tendreté dans sauces et plats.",
    ),
    _legume(
        "UD-FL-BETTERAVE",
        "betterave-frais-1kg",
        "Betterave",
        "Racine sucrée rouge vif — fer et antioxydants.",
        "🟣",
        2.15,
        description_extra="Salade ou jus. Vitamines du groupe B.",
        usage_tips="Cuire puis éplucher pour salades ; ou presser en jus.",
    ),
    _legume(
        "UD-FL-IGNAME",
        "igname-frais-1kg",
        "Igname",
        "Tubercule nourrissant — source d’énergie.",
        "🌰",
        4.95,
        description_extra="Chair blanche ou jaune, bouillie, frite ou en purée.",
        usage_tips="Éplucher et bien cuire avant consommation.",
    ),
    _legume(
        "UD-FL-NAVET",
        "navet-frais-1kg",
        "Navet",
        "Racine douce légèrement sucrée — ragoûts et soupes.",
        "🤍",
        3.15,
        description_extra="Faible en calories, fibres, minéraux et vitamines.",
        usage_tips="Mijoter dans soupes et plats en sauce.",
    ),
]

FRUITS_LEGUMES_CATALOGUE = _FRUITS + _LEGUMES
FRUITS_LEGUMES_SLUGS = frozenset(p["slug"] for p in FRUITS_LEGUMES_CATALOGUE)
