# -*- coding: utf-8 -*-
"""Création des comptes admin au déploiement (Render, etc.)."""

import logging
import os

from extensions import db
from models.user import User
from shop_auth import admin_emails_set

logger = logging.getLogger(__name__)


def upsert_admin_user(email, password, *, force_password=False):
    """
    Crée ou met à jour un compte admin.
    Retourne (user, created, password_updated).
    """
    email = email.strip().lower()
    password = (password or "").strip()
    if not email or "@" not in email:
        raise ValueError("E-mail admin invalide.")
    if len(password) < 6:
        raise ValueError("Mot de passe trop court (min. 6 caractères).")

    user = User.query.filter_by(email=email).first()
    if user:
        password_updated = False
        if force_password or not user.has_valid_password_hash():
            user.set_password(password)
            user.is_active = True
            password_updated = True
            logger.info("Mot de passe admin mis à jour pour %s", email)
        return user, False, password_updated

    user = User(email=email, name="Administrateur", is_active=True)
    user.set_password(password)
    db.session.add(user)
    logger.info("Compte admin créé pour %s", email)
    return user, True, True


def bootstrap_admin_users():
    """
    Crée les comptes listés dans ADMIN_EMAILS si BOOTSTRAP_ADMIN_PASSWORD est défini.

    Sur Render :
      ADMIN_EMAILS=compta@...,autre@...
      BOOTSTRAP_ADMIN_PASSWORD=VotreMotDePasse
      FORCE_BOOTSTRAP_ADMIN=1   (pour réinitialiser un mot de passe existant)
    """
    password = (os.environ.get("BOOTSTRAP_ADMIN_PASSWORD") or "").strip()
    emails = admin_emails_set()
    if not emails:
        logger.warning("Aucun e-mail admin (ADMIN_EMAILS / CONTACT_EMAIL).")
        return {"created": [], "updated": []}
    if not password:
        logger.info(
            "BOOTSTRAP_ADMIN_PASSWORD absent — bootstrap admin ignoré "
            "(utilisez scripts/create_admin.py en local ou Render Shell)."
        )
        return {"created": [], "updated": []}

    if len(password) < 6:
        logger.error("BOOTSTRAP_ADMIN_PASSWORD trop court (min. 6 caractères).")
        return {"created": [], "updated": []}

    force = os.environ.get("FORCE_BOOTSTRAP_ADMIN", "").lower() in ("1", "true", "yes")
    created = []
    updated = []

    for email in sorted(emails):
        user = User.query.filter_by(email=email).first()
        must_set = force or user is None or not user.has_valid_password_hash()
        _, is_new, password_updated = upsert_admin_user(
            email,
            password,
            force_password=must_set,
        )
        if is_new:
            created.append(email)
        elif password_updated:
            updated.append(email)

    db.session.commit()

    if created:
        logger.info("Comptes admin créés : %s", ", ".join(created))
    if updated:
        logger.info("Mots de passe admin mis à jour : %s", ", ".join(updated))
    return {"created": created, "updated": updated}
