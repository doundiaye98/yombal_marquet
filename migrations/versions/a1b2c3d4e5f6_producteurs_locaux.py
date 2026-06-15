"""producteurs locaux

Revision ID: a1b2c3d4e5f6
Revises: 7873b07b86ad
Create Date: 2026-06-15 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "a1b2c3d4e5f6"
down_revision = "7873b07b86ad"
branch_labels = None
depends_on = None


def _has_table(name):
    bind = op.get_bind()
    return sa.inspect(bind).has_table(name)


def _has_column(table, column):
    bind = op.get_bind()
    if not _has_table(table):
        return False
    return column in {c["name"] for c in sa.inspect(bind).get_columns(table)}


def upgrade():
    if not _has_table("producers"):
        op.create_table(
            "producers",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("slug", sa.String(length=120), nullable=False),
            sa.Column("name", sa.String(length=120), nullable=False),
            sa.Column("region", sa.String(length=160), nullable=False),
            sa.Column("flagship_product", sa.String(length=220), nullable=False),
            sa.Column("experience", sa.String(length=200), nullable=True),
            sa.Column("method", sa.String(length=300), nullable=True),
            sa.Column("monthly_production", sa.String(length=120), nullable=True),
            sa.Column("story", sa.Text(), nullable=False),
            sa.Column("avatar_emoji", sa.String(length=8), server_default="👤", nullable=False),
            sa.Column("is_active", sa.Boolean(), server_default=sa.text("1"), nullable=False),
            sa.Column("created_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
            sa.Column("updated_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_producers_slug"), "producers", ["slug"], unique=True)

    if _has_table("products") and not _has_column("products", "producer_id"):
        with op.batch_alter_table("products", schema=None) as batch_op:
            batch_op.add_column(sa.Column("producer_id", sa.Integer(), nullable=True))
            batch_op.create_foreign_key(
                "fk_products_producer_id",
                "producers",
                ["producer_id"],
                ["id"],
                ondelete="SET NULL",
            )
            batch_op.create_index(op.f("ix_products_producer_id"), ["producer_id"], unique=False)


def downgrade():
    if _has_table("products") and _has_column("products", "producer_id"):
        with op.batch_alter_table("products", schema=None) as batch_op:
            batch_op.drop_index(op.f("ix_products_producer_id"))
            batch_op.drop_constraint("fk_products_producer_id", type_="foreignkey")
            batch_op.drop_column("producer_id")
    if _has_table("producers"):
        op.drop_table("producers")
