# -*- coding: utf-8 -*-
"""Initialisation et migrations de la base de données."""

import logging
import os

from flask import Flask
from flask_migrate import upgrade

from extensions import db

logger = logging.getLogger(__name__)


def ensure_database(app: Flask) -> None:
    """Applique les migrations Alembic puis le catalogue de démo si besoin."""
    os.makedirs(app.instance_path, exist_ok=True)
    migrations_dir = os.path.join(app.root_path, "migrations")
    with app.app_context():
        if os.path.isdir(migrations_dir):
            try:
                upgrade()
                logger.info("Migrations Alembic appliquées.")
            except Exception as exc:
                logger.warning("Alembic upgrade (%s) — repli create_all.", exc)
                db.create_all()
        else:
            db.create_all()

        db.create_all()
        _legacy_patch_schema()

        from models import seed_products_if_empty, seed_producers
        from models.product_images import purge_products_without_images, sync_product_images
        from models.seed import sync_catalogue

        from models.seed_content import seed_content_if_empty

        seed_products_if_empty()
        sync_catalogue()
        seed_producers()
        seed_content_if_empty()
        sync_product_images(app.root_path)
        purge_products_without_images()

        from services.admin_bootstrap import bootstrap_admin_users

        bootstrap_admin_users()


def _add_columns(table, patches):
    from sqlalchemy import inspect, text

    insp = inspect(db.engine)
    if not insp.has_table(table):
        return
    cols = {c["name"] for c in insp.get_columns(table)}
    for name, typ in patches:
        if name in cols:
            continue
        try:
            with db.engine.begin() as conn:
                conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {name} {typ}"))
        except Exception as exc:
            logger.warning("ALTER TABLE %s ADD %s ignoré : %s", table, name, exc)


def _backfill_timestamps():
    from sqlalchemy import inspect, text

    insp = inspect(db.engine)
    for table in ("users", "products", "orders", "addresses", "order_items", "order_status_events"):
        if not insp.has_table(table):
            continue
        cols = {c["name"] for c in insp.get_columns(table)}
        for col in ("created_at", "updated_at"):
            if col not in cols:
                continue
            try:
                with db.engine.begin() as conn:
                    conn.execute(
                        text(f"UPDATE {table} SET {col} = CURRENT_TIMESTAMP WHERE {col} IS NULL")
                    )
            except Exception as exc:
                logger.warning("Backfill %s.%s ignoré : %s", table, col, exc)


def _legacy_patch_schema():
    """Pont pour bases locales créées avant le schéma actuel."""
    # SQLite n'accepte pas DEFAULT CURRENT_TIMESTAMP dans ALTER TABLE — colonnes nulles puis backfill.
    dt = "DATETIME"
    _add_columns(
        "users",
        [
            ("phone", "VARCHAR(40)"),
            ("is_active", "BOOLEAN"),
            ("created_at", dt),
            ("updated_at", dt),
        ],
    )
    _add_columns(
        "products",
        [
            ("sku", "VARCHAR(64)"),
            ("stock_qty", "INTEGER"),
            ("is_active", "BOOLEAN"),
            ("producer_id", "INTEGER"),
            ("image", "VARCHAR(255)"),
            ("icon", "VARCHAR(8)"),
            ("created_at", dt),
            ("updated_at", dt),
        ],
    )
    _add_columns(
        "orders",
        [
            ("payment_method", "VARCHAR(40)"),
            ("guest_email", "VARCHAR(120)"),
            ("guest_name", "VARCHAR(100)"),
            ("guest_phone", "VARCHAR(40)"),
            ("public_ref", "VARCHAR(32)"),
            ("delivery_line1", "VARCHAR(200)"),
            ("delivery_line2", "VARCHAR(200)"),
            ("delivery_city", "VARCHAR(100)"),
            ("delivery_postal_code", "VARCHAR(20)"),
            ("delivery_country", "VARCHAR(2)"),
            ("customer_notes", "TEXT"),
            ("currency", "VARCHAR(3)"),
            ("subtotal_cents", "INTEGER"),
            ("shipping_cents", "INTEGER"),
            ("created_at", dt),
            ("updated_at", dt),
        ],
    )
    _add_columns(
        "order_items",
        [
            ("product_name", "VARCHAR(220)"),
            ("line_total_cents", "INTEGER"),
        ],
    )

    _add_columns(
        "producers",
        [
            ("audio_url", "VARCHAR(500)"),
            ("map_x", "INTEGER"),
            ("map_y", "INTEGER"),
            ("map_label", "VARCHAR(120)"),
        ],
    )
    _add_columns(
        "orders",
        [
            ("gift_message", "TEXT"),
            ("is_gift", "BOOLEAN"),
            ("promo_code", "VARCHAR(40)"),
            ("discount_cents", "INTEGER"),
            ("notify_status_updates", "BOOLEAN"),
        ],
    )
    _add_columns(
        "order_items",
        [
            ("bundle_type", "VARCHAR(20)"),
            ("bundle_slug", "VARCHAR(120)"),
        ],
    )

    _backfill_timestamps()

    try:
        from sqlalchemy import inspect, text

        if not inspect(db.engine).has_table("orders"):
            pass
        else:
            db.session.execute(
                text(
                    "UPDATE order_items SET product_name = "
                    "(SELECT name FROM products WHERE products.id = order_items.product_id) "
                    "WHERE product_name IS NULL OR product_name = ''"
                )
            )
            db.session.execute(
                text(
                    "UPDATE order_items SET line_total_cents = unit_price_cents * quantity "
                    "WHERE line_total_cents IS NULL"
                )
            )
            db.session.execute(
                text("UPDATE products SET is_active = 1 WHERE is_active IS NULL")
            )
            db.session.execute(
                text("UPDATE orders SET subtotal_cents = total_cents WHERE subtotal_cents IS NULL")
            )
            db.session.execute(
                text("UPDATE orders SET shipping_cents = 0 WHERE shipping_cents IS NULL")
            )
            db.session.commit()
    except Exception:
        db.session.rollback()

    try:
        from models.order import Order, _new_public_ref

        for order in Order.query.filter(
            (Order.public_ref == None) | (Order.public_ref == "")  # noqa: E711
        ).all():
            order.public_ref = _new_public_ref()
        db.session.commit()
    except Exception:
        db.session.rollback()
