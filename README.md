# Yombal Marché

Boutique en ligne **Flask** (produits alimentaires et cosmétiques) : catalogue, panier, comptes clients, commandes et paiements (Stripe, PayPal, virement, espèces à la livraison).

## Démarrage rapide

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python app.py
```

Puis ouvrir http://127.0.0.1:5000/

Production locale avec Waitress : `run_waitress.bat` ou voir `wsgi.py`.

## Configuration

Copier `.env.example` vers `.env` et renseigner au minimum `FLASK_SECRET_KEY`, coordonnées banque / PayPal si besoin, clés Stripe pour la carte, `ADMIN_EMAILS` pour l’espace admin, SMTP pour les e-mails transactionnels.

Le fichier `.env` n’est pas versionné (voir `.gitignore`).

## Structure principale

- `app.py` — routes et logique
- `models.py` — utilisateurs, produits, commandes
- `mailer.py` — notifications e-mail
- `templates/` — pages HTML
- `static/` — CSS, JS

---

© Groupe YOMBAL · Projet **Univers Diaspora**
