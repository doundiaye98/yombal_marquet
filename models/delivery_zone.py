# -*- coding: utf-8 -*-
from extensions import db
from models.mixins import TimestampMixin


class DeliveryZone(TimestampMixin, db.Model):
    __tablename__ = "delivery_zones"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    postal_prefix = db.Column(db.String(10), nullable=False, index=True)
    price_cents = db.Column(db.Integer, nullable=False, default=590)
    free_over_cents = db.Column(db.Integer)  # livraison offerte au-dessus de ce montant
    is_active = db.Column(db.Boolean, nullable=False, default=True, server_default="1")
    sort_order = db.Column(db.Integer, nullable=False, default=0)

    def price_for_subtotal(self, subtotal_cents):
        if self.free_over_cents and subtotal_cents >= self.free_over_cents:
            return 0
        return self.price_cents
