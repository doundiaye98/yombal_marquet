# -*- coding: utf-8 -*-
from extensions import db
from models.coffret_model import Coffret
from models.faq_item import FaqItem
from models.recipe_model import Recipe
from models.coffrets import COFFRETS, get_coffret_by_slug as static_coffret
from models.faq import FAQ_ITEMS
from models.recipes import RECIPES, get_recipe_by_slug as static_recipe, recipes_for_product_slug as static_recipes_for_product


def all_recipe_defs():
    rows = Recipe.query.filter_by(is_active=True).order_by(Recipe.sort_order, Recipe.title).all()
    if rows:
        return [r.as_bundle_def() for r in rows]
    return list(RECIPES)


def recipe_def_by_slug(slug):
    row = Recipe.query.filter_by(slug=slug, is_active=True).first()
    if row:
        return row.as_bundle_def()
    return static_recipe(slug)


def recipes_for_product_slug(product_slug):
    defs = all_recipe_defs()
    out = []
    for recipe in defs:
        for ing in recipe.get("ingredients", []):
            if ing.get("product_slug") == product_slug:
                out.append(recipe)
                break
    if out:
        return out
    return static_recipes_for_product(product_slug)


def all_coffret_defs():
    rows = Coffret.query.filter_by(is_active=True).order_by(Coffret.sort_order, Coffret.title).all()
    if rows:
        return [c.as_bundle_def() for c in rows]
    return list(COFFRETS)


def coffret_def_by_slug(slug):
    row = Coffret.query.filter_by(slug=slug, is_active=True).first()
    if row:
        return row.as_bundle_def()
    return static_coffret(slug)


def all_faq_items():
    rows = FaqItem.query.filter_by(is_active=True).order_by(FaqItem.sort_order, FaqItem.id).all()
    if rows:
        return [r.as_dict() for r in rows]
    return list(FAQ_ITEMS)
