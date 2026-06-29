# -*- coding: utf-8 -*-
"""Anciens produits remplacés par le catalogue Univers Diaspora / LabelAfrik."""

# slug retiré → slug LabelAfrik qui reprend la photo (optionnel)
RETIRED_PRODUCT_SLUGS = frozenset(
    {
        # Catalogue initial — doublons LabelAfrik
        "dates-medjool-400g",
        "bissap-concentre-50cl",
        # Extension — doublons LabelAfrik
        "riz-brise-local-1kg",
        "pastilles-tamarin-150g",
        "puree-arachide-350g",
        "moringa-poudre-100g",
        "confiture-bissap-250g",
        "banane-plantain-sechee-120g",
        "arachides-grillees-300g",
        "tomate-concentree-400g",
        "niebe-haricot-1kg",
        "huile-arachide-1l",
        # Doublon Maad (captures catalogue : maad-230g / maad-400g)
        "maad-labelafrik",
    }
)

# Transfert des photos vers le produit LabelAfrik de remplacement
RETIRED_IMAGE_MIGRATION = {
    "dates-medjool-400g": "dattes-seches-ud",
    "bissap-concentre-50cl": "sirop-bissap-ud",
    "riz-brise-local-1kg": "riz-casse-1x-1kg",
    "pastilles-tamarin-150g": "dakhar-sachet-150g",
    "puree-arachide-350g": "pate-arachide-labelafrik",
    "moringa-poudre-100g": "moringa-poudre-labelafrik",
    "banane-plantain-sechee-120g": "chips-plantain-doux",
    "arachides-grillees-300g": "arachides-crues-blanches-1kg",
    "tomate-concentree-400g": "concentre-tomates-rolli",
    "maad-labelafrik": "maad-230g",
}
