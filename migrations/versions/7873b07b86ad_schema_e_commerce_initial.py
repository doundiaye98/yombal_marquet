"""schema e-commerce initial

Revision ID: 7873b07b86ad
Revises:
Create Date: 2026-06-15 10:28:07.592684

"""
from alembic import op
import sqlalchemy as sa


revision = "7873b07b86ad"
down_revision = None
branch_labels = None
depends_on = None


def _has_table(name):
    bind = op.get_bind()
    return sa.inspect(bind).has_table(name)


def upgrade():
  if not _has_table("users"):
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=False),
        sa.Column("password_hash", sa.String(length=256), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=True),
        sa.Column("phone", sa.String(length=40), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("1"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

  if not _has_table("addresses"):
    op.create_table(
        "addresses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("label", sa.String(length=60), nullable=True),
        sa.Column("line1", sa.String(length=200), nullable=False),
        sa.Column("line2", sa.String(length=200), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=False),
        sa.Column("postal_code", sa.String(length=20), nullable=False),
        sa.Column("country", sa.String(length=2), server_default="FR", nullable=False),
        sa.Column("is_default", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_addresses_user_id"), "addresses", ["user_id"], unique=False)

  if not _has_table("products"):
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sku", sa.String(length=64), nullable=True),
        sa.Column("slug", sa.String(length=160), nullable=False),
        sa.Column("name", sa.String(length=220), nullable=False),
        sa.Column("summary", sa.String(length=600), nullable=True),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("price_cents", sa.Integer(), nullable=False),
        sa.Column("category", sa.String(length=80), nullable=False),
        sa.Column("origin", sa.String(length=160), nullable=True),
        sa.Column("weight_info", sa.String(length=120), nullable=True),
        sa.Column("ingredients", sa.Text(), nullable=True),
        sa.Column("allergens", sa.Text(), nullable=True),
        sa.Column("usage_tips", sa.Text(), nullable=True),
        sa.Column("conservation", sa.String(length=300), nullable=True),
        sa.Column("stock_qty", sa.Integer(), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("1"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_products_slug"), "products", ["slug"], unique=True)
    op.create_index(op.f("ix_products_sku"), "products", ["sku"], unique=True)
    op.create_index(op.f("ix_products_category"), "products", ["category"], unique=False)
    op.create_index("ix_products_category_active", "products", ["category", "is_active"], unique=False)

  if not _has_table("orders"):
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("public_ref", sa.String(length=32), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("guest_email", sa.String(length=120), nullable=True),
        sa.Column("guest_name", sa.String(length=100), nullable=True),
        sa.Column("guest_phone", sa.String(length=40), nullable=True),
        sa.Column("delivery_line1", sa.String(length=200), nullable=True),
        sa.Column("delivery_line2", sa.String(length=200), nullable=True),
        sa.Column("delivery_city", sa.String(length=100), nullable=True),
        sa.Column("delivery_postal_code", sa.String(length=20), nullable=True),
        sa.Column("delivery_country", sa.String(length=2), server_default="FR", nullable=True),
        sa.Column("customer_notes", sa.Text(), nullable=True),
        sa.Column("currency", sa.String(length=3), server_default="EUR", nullable=False),
        sa.Column("subtotal_cents", sa.Integer(), server_default="0", nullable=False),
        sa.Column("shipping_cents", sa.Integer(), server_default="0", nullable=False),
        sa.Column("total_cents", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=40), server_default="pending", nullable=False),
        sa.Column("payment_method", sa.String(length=40), nullable=True),
        sa.Column("stripe_session_id", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_orders_public_ref"), "orders", ["public_ref"], unique=True)
    op.create_index(op.f("ix_orders_user_id"), "orders", ["user_id"], unique=False)
    op.create_index(op.f("ix_orders_guest_email"), "orders", ["guest_email"], unique=False)
    op.create_index(op.f("ix_orders_status"), "orders", ["status"], unique=False)
    op.create_index("ix_orders_status_created", "orders", ["status", "created_at"], unique=False)
    op.create_index("ix_orders_user_created", "orders", ["user_id", "created_at"], unique=False)
    op.create_index(op.f("ix_orders_stripe_session_id"), "orders", ["stripe_session_id"], unique=False)

  if not _has_table("order_items"):
    op.create_table(
        "order_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("product_name", sa.String(length=220), nullable=False),
        sa.Column("quantity", sa.Integer(), server_default="1", nullable=False),
        sa.Column("unit_price_cents", sa.Integer(), nullable=False),
        sa.Column("line_total_cents", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_order_items_order_id"), "order_items", ["order_id"], unique=False)
    op.create_index(op.f("ix_order_items_product_id"), "order_items", ["product_id"], unique=False)
    op.create_index("ix_order_items_order_product", "order_items", ["order_id", "product_id"], unique=False)

  if not _has_table("order_status_events"):
    op.create_table(
        "order_status_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("from_status", sa.String(length=40), nullable=True),
        sa.Column("to_status", sa.String(length=40), nullable=False),
        sa.Column("note", sa.String(length=500), nullable=True),
        sa.Column("actor_user_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["actor_user_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_order_status_events_order_id"), "order_status_events", ["order_id"], unique=False)
    op.create_index(op.f("ix_order_status_events_created_at"), "order_status_events", ["created_at"], unique=False)


def downgrade():
    for table in (
        "order_status_events",
        "order_items",
        "orders",
        "addresses",
        "products",
        "users",
    ):
        if _has_table(table):
            op.drop_table(table)
