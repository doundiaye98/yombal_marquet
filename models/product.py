# -*- coding: utf-8 -*-
from extensions import db
from models.mixins import TimestampMixin


class Product(TimestampMixin, db.Model):
    __tablename__ = "products"
    __table_args__ = (db.Index("ix_products_category_active", "category", "is_active"),)

    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(64), unique=True, index=True)
    slug = db.Column(db.String(160), unique=True, nullable=False, index=True)
    name = db.Column(db.String(220), nullable=False)
    summary = db.Column(db.String(600))
    description = db.Column(db.Text, nullable=False)
    price_cents = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(80), nullable=False, index=True)
    origin = db.Column(db.String(160))
    weight_info = db.Column(db.String(120))
    ingredients = db.Column(db.Text)
    allergens = db.Column(db.Text)
    usage_tips = db.Column(db.Text)
    conservation = db.Column(db.String(300))
    stock_qty = db.Column(db.Integer)  # None = stock non suivi
    is_active = db.Column(db.Boolean, nullable=False, default=True, server_default="1")

    order_items = db.relationship("OrderItem", back_populates="product", lazy="dynamic")

    def price_euros(self):
        return self.price_cents / 100.0

    def in_stock(self, quantity=1):
        if self.stock_qty is None:
            return True
        return self.stock_qty >= quantity
