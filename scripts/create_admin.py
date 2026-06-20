#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Crée ou met à jour un compte admin : python scripts/create_admin.py email@exemple.com MonMotDePasse"""

import sys

ROOT = __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import app
from extensions import db
from services.admin_bootstrap import upsert_admin_user
from shop_auth import admin_emails_set


def main():
    if len(sys.argv) != 3:
        print("Usage: python scripts/create_admin.py email@exemple.com MotDePasse")
        sys.exit(1)
    email = sys.argv[1].strip().lower()
    password = sys.argv[2]
    if not email or "@" not in email or len(password) < 6:
        print("E-mail invalide ou mot de passe trop court (min. 6 caractères).")
        sys.exit(1)

    with app.app_context():
        upsert_admin_user(email, password, force_password=True)
        db.session.commit()
        print(f"Compte enregistré pour {email}")
        if email not in admin_emails_set():
            print(f"\nAjoutez aussi dans .env / Render :\nADMIN_EMAILS={email}")
        else:
            print("\nConnectez-vous sur /admin/connexion")


if __name__ == "__main__":
    main()
