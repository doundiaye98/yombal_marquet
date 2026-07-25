# -*- coding: utf-8 -*-
"""Applique les corrections de rayons + sync catalogue."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.category_fixes import CATEGORY_FIXES


def main() -> None:
    from app import app
    from extensions import db
    from models.product import Product
    from models.seed import sync_catalogue
    from services import rag_index

    with app.app_context():
        sync_catalogue()
        changed = 0
        for slug, cat in CATEGORY_FIXES.items():
            p = Product.query.filter_by(slug=slug).first()
            if not p:
                continue
            if p.category != cat:
                print(f"{slug}: {p.category} -> {cat}")
                p.category = cat
                changed += 1
        if changed:
            db.session.commit()
        print("updated", changed)

        # sanity: no seafood left in conserves/condiments
        bad = (
            Product.query.filter(Product.is_active.is_(True))
            .filter(Product.category.in_(["conserves", "condiments"]))
            .filter(
                Product.slug.contains("sardine")
                | Product.slug.contains("crevette")
                | Product.slug.contains("yett")
                | Product.slug.contains("poisson")
                | Product.slug.contains("guedj")
                | Product.slug.contains("ketiakh")
            )
            .all()
        )
        print("seafood still misfiled", [(p.slug, p.category) for p in bad])
        rag_index.index_all(force=False, local_only=True)


if __name__ == "__main__":
    main()
