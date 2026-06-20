# -*- coding: utf-8 -*-
import json

from extensions import db
from models.mixins import TimestampMixin


class Recipe(TimestampMixin, db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120), unique=True, nullable=False, index=True)
    title = db.Column(db.String(220), nullable=False)
    emoji = db.Column(db.String(8), default="🍲")
    kind = db.Column(db.String(40), nullable=False, index=True)
    kind_label = db.Column(db.String(80))
    time_minutes = db.Column(db.Integer)
    servings = db.Column(db.Integer)
    summary = db.Column(db.Text)
    steps_json = db.Column(db.Text, nullable=False, default="[]")
    is_active = db.Column(db.Boolean, nullable=False, default=True, server_default="1")
    sort_order = db.Column(db.Integer, nullable=False, default=0)

    lines = db.relationship(
        "RecipeLine",
        back_populates="recipe",
        cascade="all, delete-orphan",
        lazy="joined",
        order_by="RecipeLine.sort_order",
    )

    @property
    def steps(self):
        try:
            return json.loads(self.steps_json or "[]")
        except (TypeError, ValueError):
            return []

    @steps.setter
    def steps(self, value):
        self.steps_json = json.dumps(list(value or []), ensure_ascii=False)

    def as_bundle_def(self):
        return {
            "slug": self.slug,
            "title": self.title,
            "emoji": self.emoji,
            "kind": self.kind,
            "kind_label": self.kind_label,
            "time_minutes": self.time_minutes,
            "servings": self.servings,
            "summary": self.summary,
            "steps": self.steps,
            "ingredients": [
                {
                    "product_slug": line.product.slug if line.product else "",
                    "quantity": line.quantity,
                    "note": line.note or "",
                }
                for line in self.lines
                if line.product
            ],
        }


class RecipeLine(db.Model):
    __tablename__ = "recipe_lines"

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    note = db.Column(db.String(200))
    sort_order = db.Column(db.Integer, nullable=False, default=0)

    recipe = db.relationship("Recipe", back_populates="lines")
    product = db.relationship("Product", lazy="joined")
