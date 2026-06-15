# -*- coding: utf-8 -*-
"""E-mails transactionnels (SMTP). Sans MAIL_SERVER : journalisation console uniquement."""

import logging
import os
import smtplib
from email.message import EmailMessage

logger = logging.getLogger(__name__)


def _smtp_configured():
    return bool((os.environ.get("MAIL_SERVER") or "").strip())


def send_mail(to_addrs, subject, body, *, reply_to=None):
    """Envoie un e-mail texte brut. Retourne True si envoyé ou simulé sans erreur."""
    if isinstance(to_addrs, str):
        to_addrs = [to_addrs]
    to_addrs = [a.strip() for a in to_addrs if a and a.strip()]
    if not to_addrs:
        return False

    sender = (os.environ.get("MAIL_DEFAULT_SENDER") or os.environ.get("CONTACT_EMAIL") or "").strip()
    if not sender:
        sender = "noreply@localhost"

    suppress = os.environ.get("MAIL_SUPPRESS_SEND", "").lower() in ("1", "true", "yes")
    if suppress or not _smtp_configured():
        logger.info(
            "[mail simulation] De: %s | À: %s | %s\n%s",
            sender,
            ", ".join(to_addrs),
            subject,
            body[:2000],
        )
        return True

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(to_addrs)
    if reply_to:
        msg["Reply-To"] = reply_to
    msg.set_content(body)

    server = os.environ.get("MAIL_SERVER", "").strip()
    port = int(os.environ.get("MAIL_PORT") or "587")
    user = (os.environ.get("MAIL_USERNAME") or "").strip()
    password = (os.environ.get("MAIL_PASSWORD") or "").strip()
    use_tls = os.environ.get("MAIL_USE_TLS", "true").lower() in ("1", "true", "yes")

    try:
        with smtplib.SMTP(server, port, timeout=30) as smtp:
            if use_tls:
                smtp.starttls()
            if user:
                smtp.login(user, password)
            smtp.send_message(msg)
        return True
    except Exception as exc:
        logger.exception("Échec envoi mail : %s", exc)
        return False


def _format_order_lines(order):
    lines = []
    for line in order.items:
        sub = line.unit_price_cents * line.quantity / 100.0
        lines.append(f"  - {line.product.name} × {line.quantity} : {sub:.2f} €")
    return "\n".join(lines)


def notify_customer_order_created(order, user):
    total = order.total_cents / 100.0
    body = (
        f"Bonjour,\n\n"
        f"Votre commande #{order.id} a bien été enregistrée chez Yombal Marché.\n"
        f"Montant : {total:.2f} €\n\n"
        f"Détail :\n{_format_order_lines(order)}\n\n"
        f"Finalisez le paiement depuis votre espace si ce n’est pas déjà fait.\n\n"
        f"— Yombal Marché"
    )
    send_mail(user.email, f"[Yombal Marché] Commande #{order.id} enregistrée", body)


def notify_admin_new_order(order, user):
    admins = _admin_recipients()
    if not admins:
        return
    total = order.total_cents / 100.0
    phone = order.customer_phone()
    phone_line = f"\nTél. : {phone}" if phone and phone != "—" else ""
    body = (
        f"Nouvelle commande #{order.id}\n"
        f"Client : {user.email} ({user.name or '—'}){phone_line}\n"
        f"Statut : {order.status}\n"
        f"Montant : {total:.2f} €\n\n"
        f"{_format_order_lines(order)}\n"
    )
    send_mail(admins, f"[Admin Yombal] Commande #{order.id}", body)


def notify_customer_payment_received(order, user):
    total = order.total_cents / 100.0
    body = (
        f"Bonjour,\n\n"
        f"Nous avons bien enregistré le paiement pour votre commande #{order.id} "
        f"(montant {total:.2f} €).\n\n"
        f"Merci pour votre confiance.\n\n"
        f"— Yombal Marché"
    )
    send_mail(user.email, f"[Yombal Marché] Paiement reçu — commande #{order.id}", body)


def notify_admin_payment_received(order, user):
    admins = _admin_recipients()
    if not admins:
        return
    body = (
        f"Paiement confirmé pour la commande #{order.id}\n"
        f"Client : {user.email}\n"
        f"Statut : {order.status} | Mode : {order.payment_method or '—'}\n"
    )
    send_mail(admins, f"[Admin Yombal] Payé — commande #{order.id}", body)


def notify_admin_manual_payment_choice(order, user):
    admins = _admin_recipients()
    if not admins:
        return
    body = (
        f"Le client a choisi un mode de paiement à traiter manuellement.\n\n"
        f"Commande #{order.id}\n"
        f"Client : {user.email}\n"
        f"Statut : {order.status}\n"
        f"Mode : {order.payment_method or '—'}\n"
        f"Montant : {order.total_cents / 100.0:.2f} €\n"
    )
    send_mail(admins, f"[Admin Yombal] Mode paiement — commande #{order.id}", body)


def _admin_recipients():
    raw = os.environ.get("ADMIN_EMAILS", "")
    return [e.strip() for e in raw.split(",") if e.strip()]
