# Yombal Market — version PHP + MySQL (Hostinger)

Boutique e-commerce **identique en design** (mêmes CSS/JS/images que le site Flask) avec backend **PHP 8 + MySQL**.

## Contenu du dossier `php/`

| Élément | Rôle |
|---------|------|
| `public/` | **Racine web** Hostinger (pointer le domaine ici) |
| `public/static/` | Jonction vers `../static` (CSS, JS, images) |
| `app/` | Config, DB, auth, panier, router |
| `controllers/` | Logique métier |
| `views/` | Templates PHP (même charte visuelle) |
| `sql/schema.sql` | Schéma MySQL complet |
| `scripts/` | Admin bootstrap + export catalogue SQLite |

## Déploiement Hostinger (mutualisé)

1. **Créer une base MySQL** dans hPanel (noter host, nom, user, mot de passe).
2. **Importer** `sql/schema.sql` via phpMyAdmin.
3. **Exporter le catalogue** depuis votre machine (si vous avez déjà des produits en local Flask) :
   ```bash
   python php/scripts/export_sqlite_to_mysql.py > php/sql/products_seed.sql
   ```
   Puis importer `products_seed.sql` dans phpMyAdmin.
4. **Uploader** le contenu de `php/` sur Hostinger :
   - Soit tout le dossier `php/` et définir la racine du site sur `public/`
   - Soit uploader le contenu de `public/` dans `public_html/` **et** les dossiers `app`, `controllers`, `views`, `sql` **au-dessus** de `public_html` (ajuster les chemins) — structure recommandée :

   ```
   /home/uXXXX/domains/votredomaine.com/
     app/
     controllers/
     views/
     sql/
     .env
     public_html/          ← contenu de php/public/
       index.php
       .htaccess
       static/             ← copier tout le dossier static du projet Flask
   ```

5. **Copier les assets** : le dossier `static/` du projet Flask doit être dans `public/static/` (ou `public_html/static/`). Sur Windows, une jonction a déjà été créée ; sur Hostinger, **copiez** physiquement `static/`.
6. **Créer `.env`** à partir de `.env.example` (à côté de `app/`, pas dans public) :
   ```
   APP_URL=https://votredomaine.com
   APP_SECRET=...longue-chaine-aleatoire...
   DB_HOST=localhost
   DB_NAME=yombal_market
   DB_USER=root
   DB_PASS=...
   ADMIN_EMAILS=vous@exemple.com
   BOOTSTRAP_ADMIN_PASSWORD=MotDePasseTemporaire123
   CONTACT_EMAIL=...
   PAYMENT_SIMULATION=0
   ```
7. **Créer l’admin** en SSH ou localement avec les mêmes identifiants DB :
   ```bash
   php scripts/bootstrap_admin.php
   ```
   Puis supprimer `BOOTSTRAP_ADMIN_PASSWORD` du `.env`.
8. Connexion admin : `https://votredomaine.com/admin/connexion`

## Test local (WAMP)

1. Créer une base MySQL `yombal_market` et importer `sql/schema.sql`.
2. Copier `.env.example` → `.env` (user `root`, pass WAMP).
3. Ouvrir : `http://localhost/yombal_marquet/index.php`
4. Vérifier que `mod_rewrite` est actif sous Apache.

## Fonctionnalités incluses

- Accueil, boutique (filtres), fiche produit  
- Panier, checkout, paiement (virement / PayPal / COD + simulation)  
- Inscription / connexion / compte  
- Suivi commande, annulation, recommander  
- Contact + FAQ  
- Pages : à propos, services, découvrir, saveurs, recettes, coffrets, écosystème, CGV, mentions  
- Admin : dashboard, produits CRUD, commandes + statuts, messages  
- SEO : robots.txt, sitemap.xml, PWA manifest/sw  
- Mots de passe compatibles **Flask Werkzeug pbkdf2** (re-hash auto à la connexion)

## Non inclus (phase 2)

- Stripe PaymentIntent complet (clés prévues dans `.env` ; brancher le SDK Stripe PHP)  
- SMS, PDF facture, assistant RAG OpenAI  
- Upload Cloudinary / galerie avancée  
- Parité pixel-perfect de **toutes** les sections Jinja complexes (accueil sticky slideshow, méga-menus) — le **design system CSS** est le même ; certaines pages sont simplifiées en structure HTML tout en gardant les mêmes feuilles de style.

Pour coller encore plus au HTML Flask d’une page précise (ex. `index.html` sticky), on peut porter page par page les templates Jinja → PHP.

## Sécurité

- Ne jamais committer le `.env`
- Document root = `public/` uniquement
- HTTPS obligatoire en production
- Désactiver `APP_DEBUG` et `PAYMENT_SIMULATION` en prod
