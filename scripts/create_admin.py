#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Crée ou met à jour un compte admin : python scripts/create_admin.py email@exemple.com MonMotDePasse"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import app
from extensions import db
from models.user import User


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
        user = User.query.filter_by(email=email).first()
        if user:
            user.set_password(password)
            user.is_active = True
            print(f"Mot de passe mis à jour pour {email}")
        else:
            user = User(email=email, name="Administrateur", is_active=True)
            user.set_password(password)
            db.session.add(user)
            print(f"Compte créé : {email}")
        db.session.commit()
        admins = os.environ.get("ADMIN_EMAILS", "")
        if email not in {e.strip().lower() for e in admins.split(",") if e.strip()}:
            print(
                f"\nAjoutez aussi dans .env :\nADMIN_EMAILS={email}\n"
                "Puis redemarrez l'application Flask."
            )
        else:
            print(f"\nConnectez-vous sur /admin/connexion")


if __name__ == "__main__":
    main()
