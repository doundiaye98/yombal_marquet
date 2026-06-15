"""photos produits

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-06-15 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "b2c3d4e5f6a7"
down_revision = "a1b2c3d4e5f6"
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
    if _has_table("products") and not _has_column("products", "image"):
        op.add_column("products", sa.Column("image", sa.String(length=255), nullable=True))


def downgrade():
    if _has_table("products") and _has_column("products", "image"):
        op.drop_column("products", "image")
