# -*- coding: utf-8 -*-
"""Sitemap et SEO."""

from flask import url_for

from models.producer import Producer
from models.product import Product


def sitemap_urls(app, base_url: str) -> list[dict]:
    base = (base_url or "").rstrip("/")
    urls = []

    def add(loc_path: str, changefreq: str = "weekly", priority: str = "0.6"):
        urls.append(
            {
                "loc": f"{base}{loc_path}",
                "changefreq": changefreq,
                "priority": priority,
            }
        )

    with app.app_context():
        static_pages = [
            (url_for("index"), "daily", "1.0"),
            (url_for("boutique"), "daily", "0.9"),
            (url_for("producteurs"), "weekly", "0.7"),
            (url_for("decouvrir"), "monthly", "0.6"),
            (url_for("saveurs"), "monthly", "0.6"),
            (url_for("recettes"), "weekly", "0.7"),
            (url_for("coffrets"), "weekly", "0.7"),
            (url_for("services"), "monthly", "0.5"),
            (url_for("apropos"), "monthly", "0.5"),
            (url_for("contact"), "monthly", "0.5"),
            (url_for("cgv"), "yearly", "0.3"),
            (url_for("mentions_legales"), "yearly", "0.3"),
        ]
        for path, freq, prio in static_pages:
            add(path, freq, prio)

        for product in Product.query.filter_by(is_active=True).order_by(Product.id):
            add(url_for("product_detail", slug=product.slug), "weekly", "0.8")

        for producer in Producer.query.filter_by(is_active=True).order_by(Producer.id):
            add(url_for("producteur_detail", slug=producer.slug), "monthly", "0.6")

    return urls


def render_sitemap_xml(urls: list[dict]) -> str:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for row in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{row['loc']}</loc>")
        lines.append(f"    <changefreq>{row['changefreq']}</changefreq>")
        lines.append(f"    <priority>{row['priority']}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines)
