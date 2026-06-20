# -*- coding: utf-8 -*-
from datetime import datetime

from extensions import db
from models.mixins import TimestampMixin


class PromoCode(TimestampMixin, db.Model):
    __tablename__ = "promo_codes"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(40), unique=True, nullable=False, index=True)
    discount_percent = db.Column(db.Integer)  # ex. 10 = 10 %
    discount_cents = db.Column(db.Integer)  # prioritaire si les deux définis
    min_order_cents = db.Column(db.Integer, nullable=False, default=0)
    max_uses = db.Column(db.Integer)
    used_count = db.Column(db.Integer, nullable=False, default=0)
    valid_until = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, nullable=False, default=True, server_default="1")

    def is_valid_now(self):
        if not self.is_active:
            return False
        if self.max_uses is not None and self.used_count >= self.max_uses:
            return False
        if self.valid_until and datetime.utcnow() > self.valid_until:
            return False
        return True

    def discount_for_subtotal(self, subtotal_cents):
        if subtotal_cents < self.min_order_cents:
            return 0
        if self.discount_cents:
            return min(subtotal_cents, self.discount_cents)
        if self.discount_percent:
            return min(subtotal_cents, subtotal_cents * self.discount_percent // 100)
        return 0
