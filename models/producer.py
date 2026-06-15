# -*- coding: utf-8 -*-
from extensions import db
from models.mixins import TimestampMixin


class Producer(TimestampMixin, db.Model):
    """Producteur local — vitrine traçabilité et savoir-faire."""

    __tablename__ = "producers"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120), unique=True, nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    region = db.Column(db.String(160), nullable=False)
    flagship_product = db.Column(db.String(220), nullable=False)
    experience = db.Column(db.String(200))
    method = db.Column(db.String(300))
    monthly_production = db.Column(db.String(120))
    story = db.Column(db.Text, nullable=False)
    avatar_emoji = db.Column(db.String(8), nullable=False, default="👤", server_default="👤")
    is_active = db.Column(db.Boolean, nullable=False, default=True, server_default="1")

    products = db.relationship("Product", back_populates="producer", lazy="dynamic")

    def active_products(self):
        return self.products.filter_by(is_active=True).order_by("name")
