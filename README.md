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

### Variables d’environnement

Elles sont **lues dans le code** via `os.environ` (`app.py`, `mailer.py`) — pas besoin d’autre mécanisme.

| Variable | Rôle |
|----------|------|
| `FLASK_SECRET_KEY` | Secret Flask (sessions) — **obligatoire en production** |
| `DATABASE_URL` | PostgreSQL (ex. Render) ; sinon SQLite local |
| `STRIPE_*` | Paiement carte + webhook |
| `BANK_*`, `CONTACT_EMAIL` | Virement, mentions contact |
| `PAYPAL_*` | Instructions PayPal |
| `ADMIN_EMAILS` | Accès `/admin/commandes` |
| `MAIL_*` | Envoi des e-mails transactionnels |

**Local :** copier `.env.example` vers `.env` et remplir les valeurs.

**Render (ou autre hôte) :** dans **Environment / Variables**, créez les **mêmes noms de clés** que dans `.env.example` et collez les valeurs (surtout les **secrets** : Stripe, SMTP, `FLASK_SECRET_KEY`). Ne commitez jamais `.env`.

La liste commentée et les détails sont dans **`.env.example`**.

Le fichier `.env` n’est pas versionné (voir `.gitignore`).

## Hébergement sur [Render](https://render.com)

### Important : base de données

Sur Render, le disque d’un **Web Service gratuit** est **réinitialisé** au redéploiement : avec **SQLite seul**, clients et commandes peuvent **disparaître**. Pour une boutique sérieuse, ajoutez **PostgreSQL** (Render → *New* → *PostgreSQL*), puis liez la base au service web : Render injecte automatiquement la variable **`DATABASE_URL`**. Le projet corrige déjà `postgres://…` au format SQLAlchemy.

Sans Postgres (tests uniquement), ne pas compter sur la persistance des données après un redeploy.

### Étapes (méthode manuelle, sans Blueprint)

1. Pousser le code sur **GitHub** (branche `main`).
2. Sur Render : **New +** → **Web Service** → connecter le dépôt `yombal_marquet`.
3. Réglages suggérés :
   - **Runtime** : Python  
   - **Build command** : `pip install -r requirements.txt`  
   - **Start command** : `gunicorn --bind 0.0.0.0:$PORT app:app`  
   - **Region** : *Frankfurt* (Europe) ou autre selon vous  
   - **Instance type** : *Free* (cold starts après inactivité)
4. **Environment** → ajouter les variables (repères dans `.env.example`) au minimum :
   - **`FLASK_SECRET_KEY`** — chaîne longue et aléatoire  
   - **`CONTACT_EMAIL`**, **`ADMIN_EMAILS`**, banque / PayPal / Stripe comme en local  
   - **`DATABASE_URL`** — automatique si vous créez une base Postgres Render et que vous la **liez** au Web Service  
5. Déployer. L’URL sera du type `https://yombal-marquet.onrender.com`.

Après le premier déploiement : Stripe webhook HTTPS vers  
`https://votre-service.onrender.com/webhooks/stripe` avec **`STRIPE_WEBHOOK_SECRET`** depuis le dashboard Stripe.

Les fichiers `runtime.txt`, `render.yaml` et **`gunicorn`** dans `requirements.txt` sont prévus pour Render.

### Alternative Blueprint

Dans Render : **New +** → **Blueprint** → sélectionner le dépôt et `render.yaml`, puis compléter les variables sensibles dans l’interface.

## Structure principale

- `app.py` — routes et logique
- `models.py` — utilisateurs, produits, commandes
- `mailer.py` — notifications e-mail
- `templates/` — pages HTML
- `static/` — CSS, JS
- `runtime.txt` / `render.yaml` — déploiement Render

---

© Groupe YOMBAL · Projet **Univers Diaspora**
