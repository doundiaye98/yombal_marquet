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
        name = line.product_name or (line.product.name if line.product else "Article")
        lines.append(f"  - {name} × {line.quantity} : {sub:.2f} €")
    return "\n".join(lines)


def _status_label(status):
    from models.constants import ORDER_STATUS_LABELS

    return ORDER_STATUS_LABELS.get(status, status)


def notify_customer_order_created(order, user):
    total = order.total_cents / 100.0
    ref = order.public_ref or f"#{order.id}"
    body = (
        f"Bonjour,\n\n"
        f"Votre commande {ref} a bien été enregistrée chez Yombal Marché.\n"
        f"Montant : {total:.2f} €\n\n"
        f"Détail :\n{_format_order_lines(order)}\n\n"
        f"Finalisez le paiement depuis votre espace si ce n’est pas déjà fait.\n\n"
        f"— Yombal Marché"
    )
    send_mail(user.email, f"[Yombal Marché] Commande {ref} enregistrée", body)


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


def notify_customer_payment_received(order, user, *, suivi_url=""):
    total = order.total_cents / 100.0
    ref = order.public_ref or f"#{order.id}"
    body = (
        f"Bonjour,\n\n"
        f"Nous avons bien enregistré le paiement pour votre commande {ref} "
        f"(montant {total:.2f} €).\n\n"
    )
    if suivi_url:
        body += f"Suivre votre commande : {suivi_url}\n\n"
    body += "Merci pour votre confiance.\n\n— Yombal Marché"
    send_mail(user.email, f"[Yombal Marché] Paiement reçu — {ref}", body)


def notify_customer_status_update(order, user, old_status, new_status, *, suivi_url=""):
    if not getattr(user, "email", None):
        return
    ref = order.public_ref or f"#{order.id}"
    label = _status_label(new_status)
    body = (
        f"Bonjour,\n\n"
        f"Mise à jour de votre commande {ref} :\n"
        f"→ {_status_label(old_status)} → {label}\n\n"
    )
    from models.constants import ORDER_STATUS_SHIPPED

    if new_status == ORDER_STATUS_SHIPPED:
        body += "Votre colis est en route. Préparez-vous à le recevoir prochainement.\n\n"
    if suivi_url:
        body += f"Détail et suivi : {suivi_url}\n\n"
    body += "— Yombal Marché"
    send_mail(user.email, f"[Yombal Marché] Commande {ref} — {label}", body)


def notify_customer_order_cancelled(order, user, *, suivi_url="", by_customer=False):
    if not getattr(user, "email", None):
        return
    ref = order.public_ref or f"#{order.id}"
    who = "Vous avez annulé" if by_customer else "Nous avons annulé"
    body = (
        f"Bonjour,\n\n"
        f"{who} la commande {ref}.\n"
        f"Montant : {order.total_cents / 100.0:.2f} €\n\n"
    )
    if suivi_url:
        body += f"Historique : {suivi_url}\n\n"
    body += "Pour toute question, répondez à cet e-mail ou contactez-nous.\n\n— Yombal Marché"
    send_mail(user.email, f"[Yombal Marché] Commande {ref} annulée", body)


def notify_admin_order_cancelled(order, user, *, by_customer=False):
    admins = _admin_recipients()
    if not admins:
        return
    ref = order.public_ref or f"#{order.id}"
    body = (
        f"Commande annulée : {ref}\n"
        f"Par : {'client' if by_customer else 'admin'}\n"
        f"Client : {getattr(user, 'email', '—')}\n"
        f"Montant : {order.total_cents / 100.0:.2f} €\n"
    )
    send_mail(admins, f"[Admin Yombal] Annulation — {ref}", body)


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


def notify_contact_message(msg):
    """Alerte admin + accusé réception client."""
    admins = _admin_recipients()
    contact = (os.environ.get("CONTACT_EMAIL") or "").strip()
    if not contact:
        try:
            from flask import has_app_context

            if has_app_context():
                from services.settings import shop_settings

                contact = (shop_settings().get("shop_contact_email") or "").strip()
        except Exception:
            pass
    if not contact:
        contact = "compta@universdiasporas.com"
    targets = admins or ([contact] if contact else [])
    body_admin = (
        f"Message contact Yombal Marché\n\n"
        f"De : {msg.name} <{msg.email}>\n"
        f"Sujet : {msg.subject}\n\n"
        f"{msg.message}\n"
    )
    if targets:
        send_mail(targets, f"[Yombal] Contact — {msg.subject}", body_admin, reply_to=msg.email)
    send_mail(
        msg.email,
        "[Yombal Marché] Nous avons bien reçu votre message",
        f"Bonjour {msg.name},\n\nNous avons bien reçu votre message. "
        f"Notre équipe vous répondra sous 24 h en semaine.\n\n— Yombal Marché",
    )
