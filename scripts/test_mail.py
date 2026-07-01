# -*- coding: utf-8 -*-
"""Test d'envoi e-mail SMTP (commandes, contact).

Usage :
    python scripts/test_mail.py votre@email.com
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))


def main():
    if len(sys.argv) < 2:
        print("Usage : python scripts/test_mail.py destinataire@example.com")
        return 1

    to = sys.argv[1].strip()
    if "@" not in to:
        print("Adresse e-mail invalide.")
        return 1

    from mailer import send_mail, _smtp_configured

    if not _smtp_configured():
        print("[MANQUE] MAIL_SERVER non défini — configurez MAIL_* dans .env ou Render.")
        print("Sans SMTP, les e-mails sont seulement journalisés en console.")
        return 1

    body = (
        "Ceci est un e-mail de test depuis Yombal Marché.\n\n"
        "Si vous recevez ce message, la configuration SMTP est opérationnelle.\n\n"
        "— scripts/test_mail.py"
    )
    ok = send_mail(to, "[Yombal Marché] Test SMTP", body)
    if ok:
        print(f"[OK] E-mail de test envoyé à {to}")
        return 0
    print("[ERREUR] Échec envoi — vérifiez MAIL_USERNAME, MAIL_PASSWORD, MAIL_PORT, MAIL_USE_TLS.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
