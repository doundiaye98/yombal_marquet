# -*- coding: utf-8 -*-
import os
from functools import wraps

from flask import abort, redirect, request, url_for
from flask_login import current_user

_DEFAULT_ADMIN_EMAIL = "compta@universdiasporas.com"


def _emails_from_db():
    try:
        from flask import has_app_context

        if not has_app_context():
            return set()
        from services.settings import shop_settings

        contact = (shop_settings().get("shop_contact_email") or "").strip().lower()
        return {contact} if contact else set()
    except Exception:
        return set()


def admin_emails_set():
    emails = {e.strip().lower() for e in os.environ.get("ADMIN_EMAILS", "").split(",") if e.strip()}
    if not emails:
        fallback = (os.environ.get("CONTACT_EMAIL") or "").strip().lower()
        if fallback:
            emails.add(fallback)
    if not emails:
        emails |= _emails_from_db()
    if not emails:
        emails.add(_DEFAULT_ADMIN_EMAIL.lower())
    return emails


def is_shop_admin():
    if not current_user.is_authenticated:
        return False
    return current_user.email.lower() in admin_emails_set()


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("admin.admin_login"))
        if not is_shop_admin():
            abort(403)
        return view(*args, **kwargs)

    return wrapped
