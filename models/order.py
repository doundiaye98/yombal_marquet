# -*- coding: utf-8 -*-
import secrets
from datetime import datetime

from sqlalchemy import event

from extensions import db
from models.mixins import TimestampMixin


def _new_public_ref():
    return f"YM-{datetime.utcnow().strftime('%Y%m%d')}-{secrets.token_hex(3).upper()}"


class Order(TimestampMixin, db.Model):
    __tablename__ = "orders"
    __table_args__ = (
        db.Index("ix_orders_status_created", "status", "created_at"),
        db.Index("ix_orders_user_created", "user_id", "created_at"),
    )

    id = db.Column(db.Integer, primary_key=True)
    public_ref = db.Column(db.String(32), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    guest_email = db.Column(db.String(120), index=True)
    guest_name = db.Column(db.String(100))
    guest_phone = db.Column(db.String(40))

    delivery_line1 = db.Column(db.String(200))
    delivery_line2 = db.Column(db.String(200))
    delivery_city = db.Column(db.String(100))
    delivery_postal_code = db.Column(db.String(20))
    delivery_country = db.Column(db.String(2), default="FR", server_default="FR")
    customer_notes = db.Column(db.Text)

    currency = db.Column(db.String(3), nullable=False, default="EUR", server_default="EUR")
    subtotal_cents = db.Column(db.Integer, nullable=False, default=0)
    shipping_cents = db.Column(db.Integer, nullable=False, default=0)
    total_cents = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(40), nullable=False, default="pending", index=True)
    payment_method = db.Column(db.String(40))
    stripe_session_id = db.Column(db.String(255), index=True)

    user = db.relationship("User", back_populates="orders")
    items = db.relationship(
        "OrderItem",
        back_populates="order",
        lazy="joined",
        cascade="all, delete-orphan",
    )
    status_events = db.relationship(
        "OrderStatusEvent",
        back_populates="order",
        lazy="dynamic",
        cascade="all, delete-orphan",
        order_by="OrderStatusEvent.created_at",
    )

    def customer_email(self):
        if self.user_id and self.user:
            return self.user.email
        return self.guest_email or "—"

    def customer_name(self):
        if self.user_id and self.user:
            return self.user.name or "—"
        return self.guest_name or "—"

    def customer_phone(self):
        if self.guest_phone:
            return self.guest_phone
        if self.user_id and self.user:
            return self.user.phone or "—"
        return "—"

    def delivery_formatted(self):
        parts = []
        if self.delivery_line1:
            parts.append(self.delivery_line1)
        if self.delivery_line2:
            parts.append(self.delivery_line2)
        if self.delivery_postal_code or self.delivery_city:
            parts.append(f"{self.delivery_postal_code or ''} {self.delivery_city or ''}".strip())
        return ", ".join(parts) if parts else "—"

    def set_status(self, new_status, *, note=None, actor_user_id=None):
        old = self.status
        if old == new_status:
            return
        self.status = new_status
        self.status_events.append(
            OrderStatusEvent(
                from_status=old,
                to_status=new_status,
                note=note,
                actor_user_id=actor_user_id,
            )
        )

    def is_paid(self):
        return self.status.startswith("paid") or self.status == "cod_confirmed"


@event.listens_for(Order, "before_insert")
def _order_public_ref(mapper, connection, target):
    if not target.public_ref:
        target.public_ref = _new_public_ref()


class OrderItem(db.Model):
    __tablename__ = "order_items"
    __table_args__ = (db.Index("ix_order_items_order_product", "order_id", "product_id"),)

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    product_name = db.Column(db.String(220), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price_cents = db.Column(db.Integer, nullable=False)
    line_total_cents = db.Column(db.Integer, nullable=False)

    order = db.relationship("Order", back_populates="items")
    product = db.relationship("Product", back_populates="order_items", lazy="joined")

    @staticmethod
    def from_product(product, quantity, order_id):
        qty = max(1, int(quantity))
        unit = product.price_cents
        return OrderItem(
            order_id=order_id,
            product_id=product.id,
            product_name=product.name,
            quantity=qty,
            unit_price_cents=unit,
            line_total_cents=unit * qty,
        )


class OrderStatusEvent(db.Model):
    """Historique des changements de statut (audit, SAV, admin)."""

    __tablename__ = "order_status_events"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    from_status = db.Column(db.String(40))
    to_status = db.Column(db.String(40), nullable=False)
    note = db.Column(db.String(500))
    actor_user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)

    order = db.relationship("Order", back_populates="status_events")
    actor = db.relationship("User", foreign_keys=[actor_user_id])
