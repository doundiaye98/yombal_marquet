# -*- coding: utf-8 -*-
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db
from models.mixins import TimestampMixin


class User(UserMixin, TimestampMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(40))
    is_active = db.Column(db.Boolean, nullable=False, default=True, server_default="1")

    orders = db.relationship("Order", back_populates="user", lazy="dynamic")
    addresses = db.relationship(
        "Address",
        back_populates="user",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def default_address(self):
        return self.addresses.filter_by(is_default=True).first() or self.addresses.first()


class Address(TimestampMixin, db.Model):
    """Adresses enregistrées des clients connectés (livraison réutilisable)."""

    __tablename__ = "addresses"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    label = db.Column(db.String(60), default="Domicile")
    line1 = db.Column(db.String(200), nullable=False)
    line2 = db.Column(db.String(200))
    city = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(2), nullable=False, default="FR", server_default="FR")
    is_default = db.Column(db.Boolean, nullable=False, default=False, server_default="0")

    user = db.relationship("User", back_populates="addresses")

    def formatted(self):
        parts = [self.line1]
        if self.line2:
            parts.append(self.line2)
        parts.append(f"{self.postal_code} {self.city}")
        return ", ".join(parts)
