# -*- coding: utf-8 -*-
"""Paiement et livraison simulés (tests locaux)."""

import os

from models.constants import ORDER_STATUS_PAID_DEMO, ORDER_STATUS_SHIPPED, PAYMENT_DEMO
from models.order import Order


def payment_simulation_enabled() -> bool:
    """Actif par défaut en local ; désactiver en prod avec PAYMENT_SIMULATION=0."""
    val = os.environ.get("PAYMENT_SIMULATION", "1").strip().lower()
    return val not in ("0", "false", "no")


def simulate_payment(order: Order, *, actor_user_id=None) -> str:
    """Marque la commande comme payée (démo). Retourne l'ancien statut."""
    old = order.status
    order.set_status(ORDER_STATUS_PAID_DEMO, note="Paiement simulation", actor_user_id=actor_user_id)
    order.payment_method = PAYMENT_DEMO
    return old


def simulate_shipment(order: Order, *, actor_user_id=None) -> str:
    """Passe la commande en expédiée. Retourne l'ancien statut."""
    old = order.status
    order.set_status(ORDER_STATUS_SHIPPED, note="Livraison simulée (test)", actor_user_id=actor_user_id)
    return old


def simulate_full_flow(order: Order, *, actor_user_id=None) -> tuple[str, str]:
    """Paiement simulé puis expédition — pour tester les 4 étapes du suivi."""
    old_pay = simulate_payment(order, actor_user_id=actor_user_id)
    old_ship = simulate_shipment(order, actor_user_id=actor_user_id)
    return old_pay, old_ship
