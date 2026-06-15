"""emoji produits

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-06-15 16:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "c3d4e5f6a7b8"
down_revision = "b2c3d4e5f6a7"
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
    if _has_table("products") and not _has_column("products", "icon"):
        op.add_column("products", sa.Column("icon", sa.String(length=8), nullable=True))


def downgrade():
    if _has_table("products") and _has_column("products", "icon"):
        op.drop_column("products", "icon")
