# -*- coding: utf-8 -*-
from extensions import db
from models.mixins import TimestampMixin


class Coffret(TimestampMixin, db.Model):
    __tablename__ = "coffrets"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120), unique=True, nullable=False, index=True)
    title = db.Column(db.String(220), nullable=False)
    emoji = db.Column(db.String(8), default="🎁")
    theme = db.Column(db.String(40), nullable=False, index=True)
    theme_label = db.Column(db.String(80))
    summary = db.Column(db.Text)
    gift_message = db.Column(db.Text)
    is_active = db.Column(db.Boolean, nullable=False, default=True, server_default="1")
    sort_order = db.Column(db.Integer, nullable=False, default=0)

    lines = db.relationship(
        "CoffretLine",
        back_populates="coffret",
        cascade="all, delete-orphan",
        lazy="joined",
        order_by="CoffretLine.sort_order",
    )

    def as_bundle_def(self):
        return {
            "slug": self.slug,
            "title": self.title,
            "emoji": self.emoji,
            "theme": self.theme,
            "theme_label": self.theme_label,
            "summary": self.summary,
            "gift_message": self.gift_message,
            "ingredients": [
                {
                    "product_slug": line.product.slug if line.product else "",
                    "quantity": line.quantity,
                }
                for line in self.lines
                if line.product
            ],
        }


class CoffretLine(db.Model):
    __tablename__ = "coffret_lines"

    id = db.Column(db.Integer, primary_key=True)
    coffret_id = db.Column(db.Integer, db.ForeignKey("coffrets.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    sort_order = db.Column(db.Integer, nullable=False, default=0)

    coffret = db.relationship("Coffret", back_populates="lines")
    product = db.relationship("Product", lazy="joined")
