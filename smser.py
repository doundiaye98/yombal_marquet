# -*- coding: utf-8 -*-
"""SMS transactionnels (Africa's Talking ou Twilio). Sans config : log console."""

import base64
import json
import logging
import os
import re
import urllib.error
import urllib.parse
import urllib.request

logger = logging.getLogger(__name__)


def _twilio_configured():
    return bool(
        (os.environ.get("TWILIO_ACCOUNT_SID") or "").strip()
        and (os.environ.get("TWILIO_AUTH_TOKEN") or "").strip()
        and (os.environ.get("TWILIO_PHONE_NUMBER") or "").strip()
    )


def _africastalking_configured():
    return bool((os.environ.get("AFRICASTALKING_API_KEY") or "").strip())


def _sms_provider():
    explicit = (os.environ.get("SMS_PROVIDER") or "auto").strip().lower()
    if explicit in ("twilio",):
        return "twilio" if _twilio_configured() else None
    if explicit in ("africastalking", "at", "africa"):
        return "africastalking" if _africastalking_configured() else None
    if explicit in ("none", "off", "disabled"):
        return None
    if _africastalking_configured():
        return "africastalking"
    if _twilio_configured():
        return "twilio"
    return None


def normalize_phone_e164(raw, default_country=None):
    """Convertit un numéro saisi en format E.164 (+33…, +221…)."""
    if not raw:
        return None
    default_country = (default_country or os.environ.get("SMS_DEFAULT_COUNTRY") or "FR").upper()
    cleaned = re.sub(r"[^\d+]", "", raw.strip())
    if not cleaned:
        return None
    if cleaned.startswith("00"):
        cleaned = "+" + cleaned[2:]
    if cleaned.startswith("+"):
        digits = re.sub(r"\D", "", cleaned)
        return f"+{digits}" if len(digits) >= 9 else None

    digits = re.sub(r"\D", "", cleaned)
    if default_country == "FR" and digits.startswith("0") and len(digits) == 10:
        return "+33" + digits[1:]
    if default_country == "FR" and len(digits) == 9:
        return "+33" + digits
    if default_country == "SN" and len(digits) == 9:
        return "+221" + digits
    if len(digits) >= 10:
        return "+" + digits
    return None


def _send_via_twilio(to_e164, body):
    sid = os.environ.get("TWILIO_ACCOUNT_SID", "").strip()
    token = os.environ.get("TWILIO_AUTH_TOKEN", "").strip()
    from_number = os.environ.get("TWILIO_PHONE_NUMBER", "").strip()
    url = f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json"
    payload = urllib.parse.urlencode({"To": to_e164, "From": from_number, "Body": body}).encode()
    auth = base64.b64encode(f"{sid}:{token}".encode()).decode()
    req = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return 200 <= resp.status < 300


def _africastalking_base_url(username):
    sandbox_flag = (os.environ.get("AFRICASTALKING_SANDBOX") or "").lower()
    if sandbox_flag in ("1", "true", "yes"):
        return "https://api.sandbox.africastalking.com"
    if sandbox_flag in ("0", "false", "no"):
        return "https://api.africastalking.com"
    if (username or "").lower() == "sandbox":
        return "https://api.sandbox.africastalking.com"
    return "https://api.africastalking.com"


def _parse_africastalking_response(raw):
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return False, raw[:300]
    recipients = (data.get("SMSMessageData") or {}).get("Recipients") or []
    if not recipients:
        message = (data.get("SMSMessageData") or {}).get("Message") or str(data)
        return False, message
    failed = [r for r in recipients if (r.get("status") or "").lower() not in ("success", "sent")]
    if failed:
        return False, str(failed[0])
    return True, str((data.get("SMSMessageData") or {}).get("Message") or "OK")


def _send_via_africastalking(to_e164, body):
    api_key = os.environ.get("AFRICASTALKING_API_KEY", "").strip()
    username = (os.environ.get("AFRICASTALKING_USERNAME") or "sandbox").strip()
    url = f"{_africastalking_base_url(username)}/version1/messaging"
    form = {"username": username, "to": to_e164, "message": body}
    sender = (os.environ.get("AFRICASTALKING_SENDER_ID") or "").strip()
    if sender:
        form["from"] = sender
    payload = urllib.parse.urlencode(form).encode()
    req = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={
            "Accept": "application/json",
            "apiKey": api_key,
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
        ok, detail = _parse_africastalking_response(raw)
        if not ok:
            raise RuntimeError(detail)
        logger.info("SMS Africa's Talking : %s", detail[:200])
        return True


def send_sms(to_e164, body):
    """Envoie un SMS. Retourne True si envoyé ou simulé sans erreur."""
    to_e164 = (to_e164 or "").strip()
    body = (body or "").strip()
    if not to_e164 or not body:
        return False

    suppress = os.environ.get("SMS_SUPPRESS_SEND", "").lower() in ("1", "true", "yes")
    provider = _sms_provider()
    if suppress or not provider:
        logger.info("[sms simulation] À: %s | %s", to_e164, body[:500])
        return True

    try:
        if provider == "africastalking":
            return _send_via_africastalking(to_e164, body)
        return _send_via_twilio(to_e164, body)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        logger.error("Échec envoi SMS %s (%s): %s", provider, exc.code, detail)
        return False
    except Exception as exc:
        logger.exception("Échec envoi SMS %s : %s", provider, exc)
        return False


def _order_phone_e164(order):
    phone = order.customer_phone()
    if not phone or phone == "—":
        return None
    return normalize_phone_e164(phone)


def notify_customer_order_created(order, *, suivi_url=""):
    """SMS de confirmation à la création de commande."""
    to = _order_phone_e164(order)
    if not to:
        return False
    total = order.total_cents / 100.0
    ref = order.public_ref or f"#{order.id}"
    lines = [
        f"Yombal Marche: commande {ref} enregistree ({total:.2f} EUR).",
    ]
    if suivi_url:
        lines.append(f"Suivi: {suivi_url}")
    else:
        lines.append("Finalisez le paiement depuis votre lien de commande.")
    return send_sms(to, " ".join(lines))


def notify_customer_payment_received(order, *, suivi_url=""):
    """SMS de validation après paiement confirmé."""
    to = _order_phone_e164(order)
    if not to:
        return False
    total = order.total_cents / 100.0
    ref = order.public_ref or f"#{order.id}"
    body = f"Yombal Marche: paiement confirme pour {ref} ({total:.2f} EUR). Merci!"
    if suivi_url:
        body += f" Suivi: {suivi_url}"
    return send_sms(to, body)
