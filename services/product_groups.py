# -*- coding: utf-8 -*-
"""Regroupement catalogue : une carte « gamme » → plusieurs formats/variantes."""

from __future__ import annotations

from models.constants import CATEGORY_CEREALES

# Libellés des filtres affichés sur la page gamme
RIZ_TYPE_LABELS = {
    "long-parfume": "Long parfumé",
    "long-parfume-thai": "Long parfumé thaï",
    "brise-1x": "Brisé 1×",
    "brise-2x": "Brisé 2×",
    "casse-1x": "Cassé 1×",
    "casse-2x": "Cassé 2×",
}

RIZ_FORMAT_LABELS = {
    "1kg": "1 kg",
    "45kg": "4,5 kg",
    "5kg": "5 kg",
    "20kg": "20 kg",
}

RIZ_MEMBER_SLUGS = (
    "riz-long-parfume-20kg",
    "riz-brise-2x-20kg",
    "riz-brise-1x-20kg",
    "riz-long-parfume-45kg",
    "riz-brise-1x-5kg",
    "riz-brise-2x-5kg",
    "riz-long-parfume-thai-1kg",
    "riz-long-parfume-1kg",
    "riz-brise-2x-1kg",
    "riz-casse-1x-1kg",
    "riz-casse-2x-1kg",
)

PRODUCT_GROUP_DEFS = {
    "riz": {
        "slug": "riz",
        "title": "Riz",
        "summary": (
            "Long parfumé, brisé ou cassé — du format familial au sac de 20 kg. "
            "Choisissez le type et le conditionnement adaptés à vos plats."
        ),
        "emoji": "🌾",
        "category": CATEGORY_CEREALES,
        "member_slugs": RIZ_MEMBER_SLUGS,
        "type_labels": RIZ_TYPE_LABELS,
        "format_labels": RIZ_FORMAT_LABELS,
        "hero_slug": "riz-casse-1x-1kg",
    },
}


def _riz_variant_tags(slug: str) -> tuple[str, str]:
    type_key = ""
    if "long-parfume-thai" in slug:
        type_key = "long-parfume-thai"
    elif "long-parfume" in slug:
        type_key = "long-parfume"
    elif "brise-2x" in slug:
        type_key = "brise-2x"
    elif "brise-1x" in slug:
        type_key = "brise-1x"
    elif "casse-2x" in slug:
        type_key = "casse-2x"
    elif "casse-1x" in slug:
        type_key = "casse-1x"

    format_key = ""
    if slug.endswith("-20kg"):
        format_key = "20kg"
    elif slug.endswith("-45kg"):
        format_key = "45kg"
    elif slug.endswith("-5kg"):
        format_key = "5kg"
    elif slug.endswith("-1kg"):
        format_key = "1kg"
    return type_key, format_key


def variant_tags_for_slug(group_slug: str, product_slug: str) -> dict[str, str]:
    if group_slug == "riz":
        type_key, format_key = _riz_variant_tags(product_slug)
        return {"type": type_key, "format": format_key}
    return {"type": "", "format": ""}


def all_grouped_slugs() -> set[str]:
    slugs: set[str] = set()
    for group in PRODUCT_GROUP_DEFS.values():
        slugs.update(group["member_slugs"])
    return slugs


def group_for_product_slug(product_slug: str) -> dict | None:
    for group in PRODUCT_GROUP_DEFS.values():
        if product_slug in group["member_slugs"]:
            return group
    return None


def get_group_def(group_slug: str) -> dict | None:
    return PRODUCT_GROUP_DEFS.get(group_slug)


def load_group_products(group_slug: str, active_query):
    """Produits actifs de la gamme, triés selon l'ordre catalogue."""
    from models.product import Product

    group = get_group_def(group_slug)
    if not group:
        return []
    slugs = group["member_slugs"]
    rows = (
        active_query.filter(Product.slug.in_(slugs))
        .order_by(Product.price_cents.asc(), Product.name.asc())
        .all()
    )
    slug_order = {slug: idx for idx, slug in enumerate(slugs)}
    rows.sort(key=lambda p: (slug_order.get(p.slug, 999), p.price_cents))
    return rows


def build_group_view(group_slug: str, products) -> dict | None:
    group = get_group_def(group_slug)
    if not group or not products:
        return None

    hero = next((p for p in products if p.slug == group.get("hero_slug")), products[0])
    min_price = min(p.price_cents for p in products)

    type_keys: list[str] = []
    format_keys: list[str] = []
    variants = []
    for product in products:
        tags = variant_tags_for_slug(group_slug, product.slug)
        if tags["type"] and tags["type"] not in type_keys:
            type_keys.append(tags["type"])
        if tags["format"] and tags["format"] not in format_keys:
            format_keys.append(tags["format"])
        variants.append(
            {
                "product": product,
                "type": tags["type"],
                "format": tags["format"],
                "type_label": group["type_labels"].get(tags["type"], tags["type"]),
                "format_label": group["format_labels"].get(tags["format"], tags["format"]),
            }
        )

    type_filters = [
        {"key": key, "label": group["type_labels"][key]}
        for key in group["type_labels"]
        if key in type_keys
    ]
    format_filters = [
        {"key": key, "label": group["format_labels"][key]}
        for key in group["format_labels"]
        if key in format_keys
    ]

    return {
        "group": group,
        "hero_product": hero,
        "min_price_cents": min_price,
        "variant_count": len(variants),
        "variants": variants,
        "type_filters": type_filters,
        "format_filters": format_filters,
    }


def build_group_card(group_slug: str, products) -> dict | None:
    view = build_group_view(group_slug, products)
    if not view:
        return None
    group = view["group"]
    return {
        "kind": "group",
        "slug": group_slug,
        "title": group["title"],
        "summary": group["summary"],
        "emoji": group["emoji"],
        "category": group["category"],
        "hero_product": view["hero_product"],
        "min_price_cents": view["min_price_cents"],
        "variant_count": view["variant_count"],
    }


def catalog_entries(products, *, include_groups: bool = True) -> list[dict]:
    """Transforme une liste de produits en entrées catalogue (gammes + fiches seules)."""
    if not include_groups:
        return [{"kind": "product", "product": p} for p in products]

    grouped_slugs = all_grouped_slugs()
    by_slug = {p.slug: p for p in products}
    entries: list[dict] = []
    used_group_slugs: set[str] = set()

    for group_slug, group in PRODUCT_GROUP_DEFS.items():
        members = [by_slug[s] for s in group["member_slugs"] if s in by_slug]
        if not members:
            continue
        card = build_group_card(group_slug, members)
        if card:
            entries.append(card)
            used_group_slugs.add(group_slug)

    for product in products:
        if product.slug in grouped_slugs:
            continue
        entries.append({"kind": "product", "product": product})

    # Gammes en premier (tri alpha), puis produits
    entries.sort(
        key=lambda e: (
            0 if e["kind"] == "group" else 1,
            (e["title"] if e["kind"] == "group" else e["product"].name).lower(),
        )
    )
    return entries


def display_count(active_query) -> int:
    """Nombre d'entrées visibles dans le catalogue (gammes = 1 carte)."""
    from models.product import Product

    products = active_query.order_by(Product.id).all()
    return len(catalog_entries(products))


def display_count_for_category(active_query, category_key: str) -> int:
    from models.product import Product

    products = active_query.filter_by(category=category_key).order_by(Product.id).all()
    return len(catalog_entries(products))


def related_variants(active_query, product, *, limit: int = 4):
    """Variantes de la même gamme, ou None si le produit n'est pas regroupé."""
    group = group_for_product_slug(product.slug)
    if not group:
        return None
    from models.product import Product

    siblings = (
        active_query.filter(
            Product.slug.in_(group["member_slugs"]),
            Product.id != product.id,
        )
        .order_by(Product.price_cents.asc())
        .limit(limit)
        .all()
    )
    return siblings
