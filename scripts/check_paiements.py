# -*- coding: utf-8 -*-
"""Diagnostic des moyens de paiement (Stripe, PayPal, virement).

Usage :
    python scripts/check_paiements.py

Ne modifie rien : lit le .env, teste la connexion Stripe et verifie
l'affichage des instructions PayPal / virement sur la page paiement.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))


def _tag(ok):
    return "[OK]   " if ok else "[MANQUE]"


def section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def check_env():
    section("1. Variables .env")
    keys = {
        "FLASK_SECRET_KEY": True,
        "STRIPE_SECRET_KEY": True,
        "STRIPE_PUBLISHABLE_KEY": True,
        "STRIPE_WEBHOOK_SECRET": False,
        "PAYPAL_EMAIL": False,
        "PAYPAL_ME_URL": False,
        "BANK_IBAN": True,
        "BANK_HOLDER": False,
        "MAIL_SERVER": False,
    }
    for key, important in keys.items():
        val = (os.environ.get(key) or "").strip()
        note = "" if val else ("  <- a remplir" if important else "  (optionnel)")
        print(f"  {_tag(bool(val))} {key}{note}")

    sim = os.environ.get("PAYMENT_SIMULATION", "1").strip()
    print(f"\n  PAYMENT_SIMULATION = {sim}  "
          f"({'simulation ACTIVE (paiements factices)' if sim != '0' else 'vrai flux Stripe'})")


def check_stripe():
    section("2. Connexion API Stripe")
    sk = (os.environ.get("STRIPE_SECRET_KEY") or "").strip()
    if not sk:
        print("  [MANQUE] Pas de STRIPE_SECRET_KEY : rien a tester.")
        return
    mode = "test" if "_test_" in sk else ("live" if "_live_" in sk else "inconnu")
    print(f"  Mode detecte : {mode}")
    try:
        import stripe
    except ImportError:
        print("  [ERREUR] module 'stripe' absent -> pip install stripe")
        return
    stripe.api_key = sk
    try:
        stripe.Balance.retrieve()
        print("  [OK]   Connexion au compte Stripe reussie")
    except Exception as exc:  # noqa: BLE001
        print(f"  [ERREUR] Connexion refusee : {type(exc).__name__} - {str(exc)[:120]}")
        return
    try:
        pi = stripe.PaymentIntent.create(
            amount=100,
            currency="eur",
            automatic_payment_methods={"enabled": True},
            metadata={"diagnostic": "1"},
        )
        print(f"  [OK]   PaymentIntent de test cree : {pi.id} ({pi.status})")
        stripe.PaymentIntent.cancel(pi.id)
        print("  [OK]   PaymentIntent de test annule (aucun debit)")
    except Exception as exc:  # noqa: BLE001
        print(f"  [ERREUR] Creation PaymentIntent : {type(exc).__name__} - {str(exc)[:120]}")


def check_pages():
    section("3. Rendu des pages paiement (par statut)")
    from app import app
    from extensions import db
    from models.order import Order, OrderItem
    from models.product import Product

    client = app.test_client()

    # --- Commande invitee temporaire en statut 'pending' pour tester Stripe ---
    temp_id = None
    with app.app_context():
        product = Product.query.filter_by(is_active=True).first()
        if product:
            order = Order(
                status="pending",
                guest_email="diagnostic@example.com",
                guest_name="Test Diagnostic",
                guest_phone="0600000000",
                delivery_line1="1 rue du Test",
                delivery_city="Paris",
                delivery_postal_code="75001",
                delivery_country="FR",
                subtotal_cents=product.price_cents,
                shipping_cents=0,
                discount_cents=0,
                total_cents=product.price_cents,
            )
            order.items.append(
                OrderItem(
                    product_id=product.id,
                    product_name=product.name,
                    quantity=1,
                    unit_price_cents=product.price_cents,
                    line_total_cents=product.price_cents,
                )
            )
            db.session.add(order)
            db.session.commit()
            temp_id = order.id

    if temp_id:
        with client.session_transaction() as sess:
            sess["guest_orders"] = [temp_id]
        resp = client.get(f"/paiement/{temp_id}")
        html = resp.get_data(as_text=True)
        print(f"\n  Commande TEST invitee #{temp_id} (pending) -> HTTP {resp.status_code}")
        print(f"    {_tag('Visa, Mastercard' in html)} Carte bancaire Stripe proposee")
        print(f"    {_tag('clientSecret' in html)} client_secret Stripe injecte")
        # nettoyage : on supprime la commande de diagnostic
        with app.app_context():
            o = db.session.get(Order, temp_id)
            if o:
                db.session.delete(o)
                db.session.commit()
        print(f"    (commande de test #{temp_id} supprimee)")
    else:
        print("  Aucun produit actif : impossible de creer une commande de test.")

    # --- Commandes reelles existantes pour PayPal / virement ---
    with app.app_context():
        by_status = {}
        for status in ("awaiting_paypal", "awaiting_wire"):
            o = Order.query.filter_by(status=status).order_by(Order.id.desc()).first()
            if o:
                by_status[status] = o.id

    for status, oid in by_status.items():
        with client.session_transaction() as sess:
            sess["guest_orders"] = [oid]
        resp = client.get(f"/paiement/{oid}")
        html = resp.get_data(as_text=True)
        print(f"\n  Commande #{oid} (statut '{status}') -> HTTP {resp.status_code}")
        if status == "awaiting_paypal":
            print(f"    {_tag('paypal.me' in html or '@' in html)} Instructions PayPal affichees")
        if status == "awaiting_wire":
            print(f"    {_tag('FR' in html and 'IBAN' in html)} IBAN / virement affiche")


def main():
    print("DIAGNOSTIC PAIEMENTS - Yombal Marche")
    check_env()
    check_stripe()
    try:
        check_pages()
    except Exception as exc:  # noqa: BLE001
        section("3. Rendu des pages paiement")
        print(f"  [ERREUR] {type(exc).__name__} : {str(exc)[:160]}")
    section("Termine")
    print("  Astuce : apres toute modif du .env, redemarrez Flask.")


if __name__ == "__main__":
    main()
