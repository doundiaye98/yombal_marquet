# -*- coding: utf-8 -*-
"""Recettes Yombal Marché — paniers intelligents liés au catalogue."""

RECIPES = [
    {
        "slug": "jus-bissap-maison",
        "title": "Jus de bissap maison",
        "emoji": "🌺",
        "kind": "boisson",
        "kind_label": "Boisson fraîche",
        "time_minutes": 15,
        "servings": 6,
        "summary": "Le classique rouge éclatant — fleurs d'hibiscus, gingembre et sucre au goût.",
        "steps": [
            "Portez 1 L d'eau à frémissement et retirez du feu.",
            "Ajoutez 2 c. à soupe de bissap séché et une pincée de gingembre en poudre.",
            "Laissez infuser 10 minutes puis filtrez.",
            "Sucrez, ajoutez menthe ou citron si vous le souhaitez, servez bien frais.",
        ],
        "ingredients": [
            {"product_slug": "bissap-seche-200g", "quantity": 1, "note": "2 c. à soupe pour 1 L"},
            {"product_slug": "gingembre-poudre-100g", "quantity": 1, "note": "1 pincée"},
        ],
    },
    {
        "slug": "riz-gras-terroir",
        "title": "Riz gras du terroir",
        "emoji": "🍚",
        "kind": "plat",
        "kind_label": "Plat mijoté",
        "time_minutes": 55,
        "servings": 4,
        "summary": "Riz parfumé à l'huile de palme rouge, légumes séchés et piment — l'esprit du marché.",
        "steps": [
            "Faites revenir oignon et tomate dans 2 c. à soupe d'huile de palme.",
            "Ajoutez les légumes séchés réhydratés, le piment et 600 ml d'eau.",
            "Lorsque l'eau bout, incorporez le riz, baissez le feu et couvrez 25 min.",
            "Laissez reposer 5 min hors du feu avant de servir.",
        ],
        "ingredients": [
            {"product_slug": "huile-palme-artisanale-1l", "quantity": 1, "note": "2 c. à soupe"},
            {"product_slug": "riz-casse-1x-1kg", "quantity": 1, "note": "400 g"},
            {"product_slug": "legumes-seches-thiebou-200g", "quantity": 1, "note": "1 sachet"},
            {"product_slug": "piment-sec-moulu-80g", "quantity": 1, "note": "1/2 c. à café"},
        ],
    },
    {
        "slug": "petit-dejeuner-douceur",
        "title": "Petit-déjeuner douceur",
        "emoji": "☀️",
        "kind": "petit-dejeuner",
        "kind_label": "Petit-déjeuner",
        "time_minutes": 10,
        "servings": 2,
        "summary": "Café arabica, dattes Medjool et miel de thym — un réveil gourmand et naturel.",
        "steps": [
            "Préparez le café arabica selon votre méthode habituelle.",
            "Disposez 4 à 6 dattes Medjool dans une assiette.",
            "Arrosez d'une cuillère de miel de thym ou servez à côté.",
        ],
        "ingredients": [
            {"product_slug": "cafe-arabica-250g", "quantity": 1, "note": "2 c. à soupe moulu"},
            {"product_slug": "dattes-seches-ud", "quantity": 1, "note": "4 à 6 dattes"},
            {"product_slug": "miel-thym-500g", "quantity": 1, "note": "1 c. à soupe"},
        ],
    },
    {
        "slug": "rituel-hammam-karite",
        "title": "Rituel hammam karité & argan",
        "emoji": "🧖🏾‍♀️",
        "kind": "soin",
        "kind_label": "Soin naturel",
        "time_minutes": 25,
        "servings": 1,
        "summary": "Savon noir, gommage doux et nutrition à l'argan et au karité — peau satinée.",
        "steps": [
            "Sous la douche chaude, appliquez le savon noir sur peau humide et massez.",
            "Rincez, puis appliquez une noisette de beurre de karité sur zones sèches.",
            "Terminez par quelques gouttes d'huile d'argan sur le visage et les mains.",
        ],
        "ingredients": [
            {"product_slug": "savon-noir-eucalyptus", "quantity": 1, "note": "1 noisette"},
            {"product_slug": "beurre-karite-brut-150g", "quantity": 1, "note": "1 noisette"},
            {"product_slug": "huile-argan-bio-100ml", "quantity": 1, "note": "3 à 5 gouttes"},
        ],
    },
    {
        "slug": "smoothie-bouye-energie",
        "title": "Smoothie bouye énergie",
        "emoji": "🌳",
        "kind": "boisson",
        "kind_label": "Boisson fraîche",
        "time_minutes": 5,
        "servings": 2,
        "summary": "Pulpe de baobab et miel — boisson nutritive en un clin d'œil.",
        "steps": [
            "Mélangez 2 c. à soupe de bouye dans 400 ml d'eau froide ou de lait végétal.",
            "Ajoutez 1 c. à soupe de miel et mixez 30 secondes.",
            "Servez immédiatement avec des glaçons.",
        ],
        "ingredients": [
            {"product_slug": "bouye-baobab-250g", "quantity": 1, "note": "2 c. à soupe"},
            {"product_slug": "miel-thym-500g", "quantity": 1, "note": "1 c. à soupe"},
        ],
    },
    {
        "slug": "couscous-express",
        "title": "Couscous complet express",
        "emoji": "🌾",
        "kind": "plat",
        "kind_label": "Plat mijoté",
        "time_minutes": 35,
        "servings": 4,
        "summary": "Semoule complète, légumes et épices — un plat réconfortant en moins d'une heure.",
        "steps": [
            "Réhydratez la semoule selon les indications du paquet (vapeur ou eau bouillante).",
            "Faites revenir légumes et épices yassa dans un peu d'huile.",
            "Mélangez semoule et garniture, servez chaud.",
        ],
        "ingredients": [
            {"product_slug": "couscous-complet-1kg", "quantity": 1, "note": "500 g"},
            {"product_slug": "epices-yassa-60g", "quantity": 1, "note": "1 c. à soupe"},
            {"product_slug": "huile-arachide-1l", "quantity": 1, "note": "2 c. à soupe"},
        ],
    },
]


def get_recipe_by_slug(slug):
    for recipe in RECIPES:
        if recipe["slug"] == slug:
            return recipe
    return None


def recipes_for_product_slug(product_slug):
    """Recettes contenant ce produit dans leurs ingrédients."""
    out = []
    for recipe in RECIPES:
        for ing in recipe.get("ingredients", []):
            if ing.get("product_slug") == product_slug:
                out.append(recipe)
                break
    return out


def recipes_by_kind(kind=None):
    if not kind:
        return list(RECIPES)
    return [r for r in RECIPES if r.get("kind") == kind]
