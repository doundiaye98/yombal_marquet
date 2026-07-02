"""knowledge_chunks RAG

Revision ID: e5f6a7b8c9d0
Revises: d4e5f6a7b8c9
Create Date: 2026-07-02 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "e5f6a7b8c9d0"
down_revision = "d4e5f6a7b8c9"
branch_labels = None
depends_on = None


def _has_table(name):
    bind = op.get_bind()
    return sa.inspect(bind).has_table(name)


def upgrade():
    if _has_table("knowledge_chunks"):
        return
    op.create_table(
        "knowledge_chunks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("source_type", sa.String(length=40), nullable=False),
        sa.Column("source_id", sa.String(length=160), nullable=False),
        sa.Column("title", sa.String(length=220), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("url_path", sa.String(length=255), nullable=True),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("embedding_json", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("source_type", "source_id", name="uq_knowledge_source"),
    )
    op.create_index("ix_knowledge_source_type", "knowledge_chunks", ["source_type"])
    op.create_index(op.f("ix_knowledge_chunks_content_hash"), "knowledge_chunks", ["content_hash"])


def downgrade():
    if not _has_table("knowledge_chunks"):
        return
    op.drop_index(op.f("ix_knowledge_chunks_content_hash"), table_name="knowledge_chunks")
    op.drop_index("ix_knowledge_source_type", table_name="knowledge_chunks")
    op.drop_table("knowledge_chunks")
