# -*- coding: utf-8 -*-
"""Navigation écosystème Groupe YOMBAL — style marketplace."""

from __future__ import annotations

from models.constants import (
    CATEGORY_ALIMENTAIRE,
    CATEGORY_BAGAGERIE,
    CATEGORY_BOISSONS,
    CATEGORY_CEREALES,
    CATEGORY_CHAUSSURES,
    CATEGORY_CONDIMENTS,
    CATEGORY_CONSERVES,
    CATEGORY_COSMETIQUE,
    CATEGORY_ELECTROMENAGER,
    CATEGORY_ELECTRONIQUE,
    CATEGORY_FRUITS_SECS,
    CATEGORY_HUILES,
    CATEGORY_LEGUMINEUSES,
    CATEGORY_MODE,
    CATEGORY_POISSON,
    CATEGORY_SNACKS,
    CATEGORY_VIANDES,
    SHOP_CATEGORY_ORDER,
)

SHOP_TYPE_ALIMENTAIRE = "alimentaire"
SHOP_TYPE_NON_ALIMENTAIRE = "non_alimentaire"

SHOP_UNIVERSE_ALIMENTAIRE = (
    CATEGORY_ALIMENTAIRE,
    CATEGORY_BOISSONS,
    CATEGORY_CEREALES,
    CATEGORY_HUILES,
    CATEGORY_CONDIMENTS,
    CATEGORY_LEGUMINEUSES,
    CATEGORY_FRUITS_SECS,
    CATEGORY_SNACKS,
    CATEGORY_CONSERVES,
    CATEGORY_POISSON,
    CATEGORY_VIANDES,
)

SHOP_UNIVERSE_NON_ALIMENTAIRE = (
    CATEGORY_COSMETIQUE,
    CATEGORY_ELECTRONIQUE,
    CATEGORY_ELECTROMENAGER,
    CATEGORY_MODE,
    CATEGORY_CHAUSSURES,
    CATEGORY_BAGAGERIE,
)

SHOP_UNIVERSE_LABELS = {
    SHOP_TYPE_ALIMENTAIRE: {
        "label": "Alimentaires",
        "emoji": "🛒",
        "description": "Riz, épices, boissons, produits de la mer et épicerie fine.",
    },
    SHOP_TYPE_NON_ALIMENTAIRE: {
        "label": "Non alimentaires",
        "emoji": "✨",
        "description": "Électronique, électroménager, mode, chaussures, sacs et cosmétique.",
    },
}

ECOSYSTEM_SERVICES = {
    "voyages": {
        "title": "Yombal Voyages",
        "short_label": "Voyages",
        "icon": "✈️",
        "external_url": "https://www.terangavoyages.com/",
        "tagline": "Agence de voyages TourCom — séjours, circuits et vols",
        "lead": (
            "Yombal Voyages (Teranga Voyages) organise vos départs vers l'Afrique, la Méditerranée "
            "et le monde entier : vols, séjours balnéaires, circuits et croisières."
        ),
        "bullets": [
            "Réservation en ligne sur terangavoyages.com",
            "Séjours, circuits et vols vers le Sénégal et l'Afrique",
            "Agence à Paris — 75 rue des Moines, 75017",
        ],
        "cta_label": "Voir les offres voyage",
    },
    "investissement": {
        "title": "Yombal Investissement Opportunités",
        "short_label": "Investissement",
        "icon": "📈",
        "tagline": "Opportunités d'investissement et projets",
        "lead": (
            "Identification d'opportunités d'investissement en Afrique et en Europe : "
            "commerce, agriculture, distribution et projets structurés pour la diaspora."
        ),
        "bullets": [
            "Étude de faisabilité et mise en relation",
            "Projets agro-alimentaires et distribution",
            "Accompagnement diaspora investisseurs",
            "Confidentialité et suivi personnalisé",
        ],
        "cta_label": "Explorer les opportunités",
    },
    "immobilier-btp": {
        "title": "Yombal Immobilier & BTP",
        "short_label": "Immobilier & BTP",
        "icon": "🏗️",
        "tagline": "Programme YOMBAL KEUR — terrains diaspora & construction",
        "lead": (
            "Terrains à céder au Sénégal (Yenne Ndoukhoura Peulh, Sangalcam, Ndayane) "
            "avec paiement échelonné sans apport initial, et accompagnement BTP "
            "pour vos projets de construction."
        ),
        "bullets": [
            "Programme YOMBAL KEUR — cité dédiée à la diaspora",
            "Parcelles de 150 m² — paiement échelonné, apport initial 0 €",
            "Titre foncier, acte administratif ou notification de bail selon le site",
            "Visite de site, protocole d'accord et représentant légal",
            "Construction, rénovation et suivi de chantier (BTP)",
        ],
        "cta_label": "Demander un projet",
        "demande_url": "immo_demande_projet",
        "custom_template": "ecosysteme/immobilier_btp.html",
    },
    "transport": {
        "title": "Yombal Transports",
        "short_label": "Transports",
        "icon": "🚗",
        "tagline": "Véhicules, location, déménagement et envoi de colis",
        "lead": (
            "Achat et vente de véhicules, location de voiture, déménagement professionnel "
            "et envoi de colis — une offre complète du Groupe YOMBAL pour vos déplacements "
            "et vos livraisons."
        ),
        "bullets": [
            "Achats véhicules",
            "Vente véhicules",
            "Location voiture",
            "Déménagement pro",
            "Envoi de colis",
        ],
        "cta_label": "Faire une demande",
    },
    "restaurant": {
        "title": "Yombal Restaurant",
        "short_label": "Restaurant",
        "icon": "🍽️",
        "tagline": "Restauration et saveurs africaines",
        "lead": (
            "Restauration authentique, traiteur et événements autour des saveurs "
            "que vous retrouvez aussi dans notre épicerie."
        ),
        "bullets": [
            "Plats traditionnels et cuisine du marché",
            "Traiteur pour événements et fêtes",
            "Carte évolutive selon les saisons",
            "Réservations et commandes groupe",
        ],
        "cta_label": "Réserver / commander",
    },
    "electronique": {
        "title": "Yombal Électronique",
        "short_label": "Électronique",
        "icon": "📱",
        "tagline": "Smartphones, high-tech et accessoires",
        "lead": (
            "Smartphones (iPhone, Samsung et autres marques), multimédia, accessoires "
            "et petit high-tech — une offre Yombal Market disponible en boutique en ligne."
        ),
        "bullets": [
            "Smartphones iPhone, Samsung et Android",
            "Audio, casques, enceintes et accessoires",
            "Tablettes, montres connectées et charge",
            "Commande en ligne avec livraison",
        ],
        "cta_label": "Voir l'électronique",
        "boutique_category": CATEGORY_ELECTRONIQUE,
    },
    "electromenager": {
        "title": "Yombal Électroménager",
        "short_label": "Électroménager",
        "icon": "🏠",
        "tagline": "Maison, cuisine et petit électroménager",
        "lead": (
            "Équipez votre cuisine et votre intérieur : mixeurs, bouilloires, fers, "
            "aspirateurs, micro-ondes et plus — sélection Yombal Market livrée chez vous."
        ),
        "bullets": [
            "Petit électroménager cuisine",
            "Entretien de la maison",
            "Appareils du quotidien à prix accessibles",
            "Commande en ligne avec livraison",
        ],
        "cta_label": "Voir l'électroménager",
        "boutique_category": CATEGORY_ELECTROMENAGER,
    },
    "mode": {
        "title": "Yombal Habillement",
        "short_label": "Habillement",
        "icon": "👕",
        "tagline": "Mode, vêtements et style au quotidien",
        "lead": (
            "T-shirts, chemises, robes, jeans, sport et ensembles pagne — "
            "une sélection habillement pour toute la famille sur Yombal Market."
        ),
        "bullets": [
            "Homme, femme et sport",
            "Basiques et pièces saisonnières",
            "Sélection diaspora (pagne, boubou)",
            "Commande en ligne avec livraison",
        ],
        "cta_label": "Voir l'habillement",
        "boutique_category": CATEGORY_MODE,
    },
    "chaussures": {
        "title": "Yombal Chaussures",
        "short_label": "Chaussures",
        "icon": "👟",
        "tagline": "Baskets, ville, sandales et plus",
        "lead": (
            "Baskets urbaines, running, sandales, chaussures de ville et bottes — "
            "trouvez la paire adaptée à chaque occasion sur Yombal Market."
        ),
        "bullets": [
            "Baskets et running",
            "Chaussures de ville et sandales",
            "Modèles enfant et adulte",
            "Commande en ligne avec livraison",
        ],
        "cta_label": "Voir les chaussures",
        "boutique_category": CATEGORY_CHAUSSURES,
    },
    "bagagerie": {
        "title": "Yombal Sacs & bagagerie",
        "short_label": "Sacs & bagagerie",
        "icon": "🎒",
        "tagline": "Sacs à dos, valises et accessoires voyage",
        "lead": (
            "Sacs à dos, valises cabine, bandoulières, sacs week-end et pochettes voyage — "
            "tout pour vos trajets et votre quotidien."
        ),
        "bullets": [
            "Sacs à dos et cartables",
            "Valises et sacs de voyage",
            "Bandoulières et pochettes documents",
            "Commande en ligne avec livraison",
        ],
        "cta_label": "Voir les sacs",
        "boutique_category": CATEGORY_BAGAGERIE,
    },
    "coiffure": {
        "title": "Yombal Coiffure",
        "short_label": "Coiffure",
        "icon": "💇🏾",
        "tagline": "Coiffure, soins et beauté",
        "lead": (
            "Salon et prestations capillaires : tresses, soins, coupes et beauté "
            "dans l'esprit Yombal — authenticité et qualité."
        ),
        "bullets": [
            "Coiffure afro et soins capillaires",
            "Produits naturels (karité, huiles)",
            "Rendez-vous sur place ou à domicile (selon zone)",
            "Tarifs affichés sur demande",
        ],
        "cta_label": "Prendre rendez-vous",
    },
    "autres-services": {
        "title": "Autres services",
        "short_label": "Autres",
        "icon": "✦",
        "tagline": "Toute l'offre du Groupe YOMBAL",
        "lead": (
            "Découvrez l'ensemble des prestations du Groupe YOMBAL : boutique en ligne, "
            "livraison, conseil et services sur mesure."
        ),
        "bullets": [
            "Boutique alimentaire, cosmétique, électronique et mode",
            "Électroménager, chaussures et bagagerie",
            "Immobilier & BTP et investissement",
            "Livraison à domicile",
            "Contact unique pour toutes vos demandes",
        ],
        "cta_label": "Nous contacter",
    },
}

ECOSYSTEM_NAV_ORDER = (
    "voyages",
    "investissement",
    "immobilier-btp",
    "transport",
    "restaurant",
    "electronique",
    "electromenager",
    "mode",
    "chaussures",
    "bagagerie",
    "coiffure",
    "autres-services",
)


def ecosystem_nav_items() -> list[dict]:
    return [
        {"slug": slug, **ECOSYSTEM_SERVICES[slug]}
        for slug in ECOSYSTEM_NAV_ORDER
    ]


ECOSYSTEM_SLUG_ALIASES = {
    "immobilier": "immobilier-btp",
    "btp": "immobilier-btp",
}


def hub_services() -> list[dict]:
    """Services affichés sur la page Autres services."""
    skip = frozenset({"autres-services"})
    return [
        item for item in ecosystem_nav_items()
        if item["slug"] not in skip
    ]


def get_ecosystem_service(slug: str) -> dict | None:
    data = ECOSYSTEM_SERVICES.get(slug)
    if not data:
        return None
    return {"slug": slug, **data}


def categories_for_shop_type(shop_type: str | None) -> tuple[str, ...]:
    if shop_type == SHOP_TYPE_ALIMENTAIRE:
        return SHOP_UNIVERSE_ALIMENTAIRE
    if shop_type == SHOP_TYPE_NON_ALIMENTAIRE:
        return SHOP_UNIVERSE_NON_ALIMENTAIRE
    return SHOP_CATEGORY_ORDER


def boutique_rayons_for_type(shop_type: str | None) -> tuple[str, ...]:
    allowed = set(categories_for_shop_type(shop_type))
    return tuple(k for k in SHOP_CATEGORY_ORDER if k in allowed)
