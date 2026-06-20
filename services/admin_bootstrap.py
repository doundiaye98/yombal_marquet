# -*- coding: utf-8 -*-
"""Création des comptes admin au déploiement (Render, etc.)."""

import logging
import os

from extensions import db
from models.user import User
from shop_auth import admin_emails_set

logger = logging.getLogger(__name__)


def upsert_admin_user(email, password, *, force_password=False):
    email = email.strip().lower()
    user = User.query.filter_by(email=email).first()
    if user:
        if force_password:
            user.set_password(password)
            user.is_active = True
            logger.info("Mot de passe admin mis à jour pour %s", email)
        return user, False
    user = User(email=email, name="Administrateur", is_active=True)
    user.set_password(password)
    db.session.add(user)
    logger.info("Compte admin créé pour %s", email)
    return user, True


def bootstrap_admin_users():
    """
    Crée les comptes listés dans ADMIN_EMAILS si BOOTSTRAP_ADMIN_PASSWORD est défini.
    Sur Render : ajoutez ces variables d'environnement puis redéployez.
    """
    password = (os.environ.get("BOOTSTRAP_ADMIN_PASSWORD") or "").strip()
    emails = admin_emails_set()
    if not emails:
        logger.warning("Aucun e-mail admin (ADMIN_EMAILS / CONTACT_EMAIL).")
        return []
    if not password:
        logger.info(
            "BOOTSTRAP_ADMIN_PASSWORD absent — création auto des admins ignorée "
            "(normal en local si compte déjà créé via scripts/create_admin.py)."
        )
        return []

    if len(password) < 6:
        logger.error("BOOTSTRAP_ADMIN_PASSWORD trop court (min. 6 caractères).")
        return []

    force = os.environ.get("FORCE_BOOTSTRAP_ADMIN", "").lower() in ("1", "true", "yes")
    created = []
    for email in sorted(emails):
        _, is_new = upsert_admin_user(email, password, force_password=force)
        if is_new:
            created.append(email)

    db.session.commit()
    if created:
        logger.info("Comptes admin créés : %s", ", ".join(created))
    return created
