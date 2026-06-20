# -*- coding: utf-8 -*-
"""Helpers UI commandes (style marketplace)."""

from models.constants import ORDER_STATUS_CANCELLABLE, ORDER_STATUS_CANCELLED, ORDER_STATUS_PILL


def order_status_pill(status):
    return ORDER_STATUS_PILL.get(status, ("En cours", "pill-neutral"))


def order_preview_lines(order, limit=3):
    lines = []
    for item in order.items[:limit]:
        product = item.product
        lines.append(
            {
                "item": item,
                "product": product,
                "name": item.product_name,
                "quantity": item.quantity,
                "image": product.image if product else None,
                "icon": (product.icon if product else None) or "🛒",
                "slug": product.slug if product else None,
            }
        )
    return lines


def order_extra_count(order, limit=3):
    total = len(order.items)
    return max(0, total - limit)


def order_can_pay(order):
    return order.status == "pending" and not order.is_paid()


def order_can_reorder(order):
    return order.status not in (ORDER_STATUS_CANCELLED,) and len(order.items) > 0


def order_can_cancel(order):
    return order.status in ORDER_STATUS_CANCELLABLE
