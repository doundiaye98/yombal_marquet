# -*- coding: utf-8 -*-
"""Score de maturité production (6 axes, objectif ≥ 95 %).

Usage :
    python scripts/check_production.py
    python scripts/check_production.py --json
"""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

TARGET = 95
# Caractères ASCII pour compatibilité console Windows
CHECK = "[OK]"
CROSS = "[--]"


def _bar(pct: float, width: int = 10) -> str:
    filled = round(width * pct / 100)
    return "#" * filled + "." * (width - filled)


def _env(key: str) -> str:
    return (os.environ.get(key) or "").strip()


def _has(key: str) -> bool:
    return bool(_env(key))


def _path_exists(rel: str) -> bool:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.exists(os.path.join(root, rel))


def score_catalogue() -> tuple[float, list[str]]:
    notes: list[str] = []
    checks = 0
    ok = 0

    def add(cond: bool, msg_ok: str, msg_ko: str):
        nonlocal checks, ok
        checks += 1
        if cond:
            ok += 1
            notes.append(f"  {CHECK} {msg_ok}")
        else:
            notes.append(f"  {CROSS} {msg_ko}")

    try:
        from app import app
        from models.product import Product

        with app.app_context():
            active = Product.query.filter_by(is_active=True).count()
            with_img = (
                Product.query.filter(Product.is_active.is_(True))
                .filter(Product.image.isnot(None), Product.image != "")
                .count()
            )
            ratio = (with_img / active * 100) if active else 0
            add(
                ratio >= 95,
                f"Photos catalogue {with_img}/{active} ({ratio:.0f} %)",
                f"Photos catalogue {with_img}/{active} ({ratio:.0f} %) - lancer sync_product_images ou ajouter images",
            )
            add(active >= 50, f"{active} produits actifs", f"Peu de produits actifs ({active})")
    except Exception as exc:
        add(False, "", f"Base inaccessible : {exc}")

    add(_path_exists("models/product_images.py"), "Module images catalogue", "models/product_images.py manquant")
    add(_path_exists("static/img/products"), "Dossier static/img/products", "Dossier images produits absent")
    return (ok / checks * 100) if checks else 0, notes


def score_design() -> tuple[float, list[str]]:
    notes: list[str] = []
    checks = 0
    ok = 0

    def add(cond: bool, msg_ok: str, msg_ko: str):
        nonlocal checks, ok
        checks += 1
        if cond:
            ok += 1
            notes.append(f"  {CHECK} {msg_ok}")
        else:
            notes.append(f"  {CROSS} {msg_ko}")

    templates = {
        "templates/boutique/index.html": "boutique-page",
        "templates/boutique/gamme.html": "boutique-page",
        "templates/index.html": "home-hero",
        "templates/panier.html": "order-flow-page",
        "templates/checkout.html": "order-flow-page",
        "templates/paiement.html": "order-flow-page",
    }
    for path, marker in templates.items():
        full = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), path)
        if os.path.isfile(full):
            text = open(full, encoding="utf-8").read()
            add(marker in text, f"{path} -> {marker}", f"{path} sans classe {marker}")
        else:
            add(False, "", f"{path} manquant")

    add(_path_exists("static/css/modern.css"), "Feuille modern.css", "modern.css manquant")
    add(_path_exists("templates/macros/product_image.html"), "Macro product_image", "Macro images manquante")
    return (ok / checks * 100) if checks else 0, notes


def score_checkout() -> tuple[float, list[str]]:
    notes: list[str] = []
    checks = 0
    ok = 0

    def add(cond: bool, msg_ok: str, msg_ko: str):
        nonlocal checks, ok
        checks += 1
        if cond:
            ok += 1
            notes.append(f"  {CHECK} {msg_ok}")
        else:
            notes.append(f"  {CROSS} {msg_ko}")

    sim_off = _env("PAYMENT_SIMULATION") == "0"
    add(sim_off, "PAYMENT_SIMULATION=0 (vrais paiements)", "PAYMENT_SIMULATION!=0 - desactiver en production")

    stripe_ok = _has("STRIPE_SECRET_KEY") and _has("STRIPE_PUBLISHABLE_KEY")
    add(stripe_ok, "Clés Stripe configurées", "STRIPE_SECRET_KEY / STRIPE_PUBLISHABLE_KEY manquants")
    add(_has("STRIPE_WEBHOOK_SECRET"), "STRIPE_WEBHOOK_SECRET (webhook /webhooks/stripe)", "STRIPE_WEBHOOK_SECRET manquant - paiements sans confirmation serveur")

    wire_ok = _has("BANK_IBAN") and _has("BANK_NAME")
    add(wire_ok, "Coordonnées virement", "BANK_IBAN ou BANK_NAME manquant")

    paypal_ok = _has("PAYPAL_EMAIL") or _has("PAYPAL_ME_URL")
    add(paypal_ok, "PayPal configuré", "PAYPAL_EMAIL ou PAYPAL_ME_URL manquant")

    add(_has("CONTACT_EMAIL"), "CONTACT_EMAIL défini", "CONTACT_EMAIL manquant")
    add(_path_exists("templates/checkout.html"), "Page checkout", "checkout.html manquant")
    add(_path_exists("templates/paiement.html"), "Page paiement", "paiement.html manquant")
    return (ok / checks * 100) if checks else 0, notes


def score_admin() -> tuple[float, list[str]]:
    notes: list[str] = []
    checks = 0
    ok = 0

    def add(cond: bool, msg_ok: str, msg_ko: str):
        nonlocal checks, ok
        checks += 1
        if cond:
            ok += 1
            notes.append(f"  {CHECK} {msg_ok}")
        else:
            notes.append(f"  {CROSS} {msg_ko}")

    admins = [e.strip().lower() for e in _env("ADMIN_EMAILS").split(",") if e.strip()]
    add(bool(admins), f"ADMIN_EMAILS ({len(admins)} e-mail(s))", "ADMIN_EMAILS vide")

    bootstrap_left = bool(_env("BOOTSTRAP_ADMIN_PASSWORD"))
    add(not bootstrap_left, "BOOTSTRAP_ADMIN_PASSWORD retiré (sécurité)", "Retirez BOOTSTRAP_ADMIN_PASSWORD après 1ère connexion")

    try:
        from app import app
        from models.user import User
        from shop_auth import admin_emails_set

        with app.app_context():
            for email in sorted(admin_emails_set()):
                user = User.query.filter_by(email=email).first()
                valid = user and user.is_active and user.has_valid_password_hash()
                add(valid, f"Compte admin {email}", f"Compte admin manquant ou mot de passe invalide : {email}")
    except Exception as exc:
        add(False, "", f"Vérification comptes admin impossible : {exc}")

    add(_path_exists("routes/admin.py"), "Routes admin", "routes/admin.py manquant")
    return (ok / checks * 100) if checks else 0, notes


def score_render() -> tuple[float, list[str]]:
    notes: list[str] = []
    checks = 0
    ok = 0

    def add(cond: bool, msg_ok: str, msg_ko: str):
        nonlocal checks, ok
        checks += 1
        if cond:
            ok += 1
            notes.append(f"  {CHECK} {msg_ok}")
        else:
            notes.append(f"  {CROSS} {msg_ko}")

    db_url = _env("DATABASE_URL")
    is_pg = db_url.startswith("postgres")
    add(is_pg, "DATABASE_URL PostgreSQL", "DATABASE_URL absent ou non-PostgreSQL (SQLite fragile sur Render)")

    add(_has("FLASK_SECRET_KEY"), "FLASK_SECRET_KEY", "FLASK_SECRET_KEY manquant")

    req_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "requirements.txt")
    if os.path.isfile(req_path):
        req = open(req_path, encoding="utf-8").read().lower()
        add("gunicorn" in req, "gunicorn dans requirements.txt", "gunicorn absent de requirements.txt")
        add("psycopg2" in req, "psycopg2-binary dans requirements.txt", "psycopg2-binary absent")
    else:
        add(False, "", "requirements.txt manquant")

    add(_path_exists("render.yaml"), "render.yaml present", "render.yaml manquant - blueprint Render")

    cloud = _has("CLOUDINARY_CLOUD_NAME") and _has("CLOUDINARY_API_KEY")
    add(cloud, "Cloudinary (images persistantes Render)", "Cloudinary non configure - uploads admin perdus au redeploiement")

    add(_path_exists("services/image_storage.py"), "Service image_storage", "image_storage.py manquant")
    return (ok / checks * 100) if checks else 0, notes


def score_mail() -> tuple[float, list[str]]:
    notes: list[str] = []
    checks = 0
    ok = 0

    def add(cond: bool, msg_ok: str, msg_ko: str):
        nonlocal checks, ok
        checks += 1
        if cond:
            ok += 1
            notes.append(f"  {CHECK} {msg_ok}")
        else:
            notes.append(f"  {CROSS} {msg_ko}")

    smtp = _has("MAIL_SERVER")
    add(smtp, f"MAIL_SERVER ({_env('MAIL_SERVER') or '-'})", "MAIL_SERVER manquant - e-mails en log console seulement")

    if smtp:
        add(_has("MAIL_USERNAME"), "MAIL_USERNAME", "MAIL_USERNAME manquant")
        add(_has("MAIL_PASSWORD"), "MAIL_PASSWORD", "MAIL_PASSWORD manquant")
        add(_has("MAIL_DEFAULT_SENDER") or _has("CONTACT_EMAIL"), "Expéditeur (MAIL_DEFAULT_SENDER ou CONTACT_EMAIL)", "Définir MAIL_DEFAULT_SENDER")
        suppress = _env("MAIL_SUPPRESS_SEND").lower() in ("1", "true", "yes")
        add(not suppress, "Envoi reel active (MAIL_SUPPRESS_SEND off)", "MAIL_SUPPRESS_SEND=true - aucun envoi reel")
    else:
        notes.append("  -> Completer MAIL_* puis : python scripts/test_mail.py votre@email.com")

    add(_path_exists("mailer.py"), "Module mailer.py", "mailer.py manquant")
    add(_path_exists("scripts/test_mail.py"), "Script test_mail.py", "scripts/test_mail.py manquant")
    return (ok / checks * 100) if checks else 0, notes


def score_tests() -> tuple[float, list[str]]:
    notes: list[str] = []
    checks = 0
    ok = 0

    def add(cond: bool, msg_ok: str, msg_ko: str):
        nonlocal checks, ok
        checks += 1
        if cond:
            ok += 1
            notes.append(f"  {CHECK} {msg_ok}")
        else:
            notes.append(f"  {CROSS} {msg_ko}")

    add(_path_exists("tests/conftest.py"), "Suite pytest (conftest)", "tests/conftest.py manquant")
    add(_path_exists("tests/test_cart.py"), "Tests panier", "tests/test_cart.py manquant")
    add(_path_exists("tests/test_checkout.py"), "Tests checkout", "tests/test_checkout.py manquant")
    add(_path_exists("tests/test_stripe_webhook.py"), "Tests webhook Stripe", "tests/test_stripe_webhook.py manquant")

    req_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "requirements.txt")
    if os.path.isfile(req_path):
        req = open(req_path, encoding="utf-8").read().lower()
        add("pytest" in req, "pytest dans requirements.txt", "pytest absent de requirements.txt")
    else:
        add(False, "", "requirements.txt manquant")

    notes.append("  -> Lancer : python -m pytest tests/")
    return (ok / checks * 100) if checks else 0, notes


AXES = [
    ("Contenu catalogue", score_catalogue),
    ("Design vitrine", score_design),
    ("Parcours commande", score_checkout),
    ("Tests automatisés", score_tests),
    ("Admin", score_admin),
    ("Production Render", score_render),
    ("Automatisation (mail)", score_mail),
]


def run_report() -> dict:
    results = {}
    for label, fn in AXES:
        pct, notes = fn()
        results[label] = {"score": round(pct, 1), "notes": notes, "ok": pct >= TARGET}
    overall = sum(r["score"] for r in results.values()) / len(results)
    results["__overall__"] = round(overall, 1)
    return results


def main():
    parser = argparse.ArgumentParser(description="Score maturité production Yombal Marché")
    parser.add_argument("--json", action="store_true", help="Sortie JSON")
    args = parser.parse_args()

    results = run_report()

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 0 if all(results[k]["ok"] for k in results if not k.startswith("__")) else 1

    print("\n" + "=" * 58)
    print("  YOMBAL MARCHE - Score production (objectif >= 95 %)")
    print("=" * 58)

    all_ok = True
    for label, fn in AXES:
        pct = results[label]["score"]
        ok = results[label]["ok"]
        all_ok = all_ok and ok
        status = "OK" if ok else "!!"
        print(f"\n{label:<22} {_bar(pct)}  {pct:5.1f} %  [{status}]")
        for line in results[label]["notes"]:
            print(line)

    overall = results["__overall__"]
    print("\n" + "-" * 58)
    print(f"Score global moyen : {overall:.1f} %")
    if all_ok:
        print("Tous les axes atteignent 95 % - pret pour la production.")
    else:
        print("Actions restantes : completer les [--] ci-dessus, puis relancer ce script.")
    print()
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
