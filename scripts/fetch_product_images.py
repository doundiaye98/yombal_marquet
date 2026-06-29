# -*- coding: utf-8 -*-
"""Télécharge des images produits (Biosene LabelAfrik) et assigne les photos locales."""

import os
import re
import shutil
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# Biosene (LabelAfrik) — slug → page produit
BIOSENE_PAGES = {
    "arraw-mil-labelafrik": "https://biosene.net/index.php/produit/arraw/",
    "sankhal-labelafrik": "https://biosene.net/index.php/produit/aliquam-tempus/",
    "thiere-lalo-labelafrik": "https://biosene.net/index.php/produit/cras-in-dictum/",
    "moringa-poudre-labelafrik": "https://biosene.net/index.php/produit/moringa/",
    "gombo-poudre-labelafrik": "https://biosene.net/index.php/produit/poudre-de-gombo/",
    "maad-labelafrik": "https://biosene.net/index.php/produit/maad-caramelise/",
    "soungouf-labelafrik": "https://biosene.net/index.php/produit/lalo/",
}

# Photos locales img/ → slug (fichiers pas encore mappés)
LOCAL_IMAGE_MAP = {
    "datte.jpg": [
        "dattes-branchees-ud",
        "dattes-demi-seches-ud",
        "raisins-secs-golden",
    ],
    "bissap.jpg": ["bissap-rouge-zena"],
    "Red palm oil Thailand_.jpg": ["huile-palme-1l"],
    "miel.jpg": ["miel-fleurs-1kg"],
    "cafe.jpg": [],  # déjà café touba / arabica
}

# Réutiliser une photo catalogue existante pour produits proches
COPY_FROM_EXISTING = {
    "farine-mil-1kg": "mil-millet-1kg",
    "fiono-guinee": "fonio-500g",
    "soungouf-labelafrik": "mil-millet-1kg",
    "thiacry-de-mil": "thiakry-400g",
    "dakhar-sachet-375g": "dakhar-sachet-150g",
    "poudre-arachide-ud": "pate-arachide-labelafrik",
    "pate-arachide-labelafrik": "farine-niebe-500g",
    "pate-arachide-dakatine": "pate-arachide-labelafrik",
    "pate-arachide-bonmafe": "pate-arachide-labelafrik",
    "pate-arachide-pcd-500g": "pate-arachide-labelafrik",
    "pate-arachide-25kg": "pate-arachide-labelafrik",
    "arachides-crues-blanches-1kg": "pate-arachide-labelafrik",
    "riz-long-parfume-1kg": "riz-casse-1x-1kg",
    "riz-long-parfume-45kg": "riz-casse-1x-1kg",
    "riz-casse-2x-1kg": "riz-casse-1x-1kg",
    "cornilles-haricots-blancs": "farine-niebe-500g",
    "haricots-noirs-tersol": "farine-niebe-500g",
    "maad-230g": "maad-labelafrik",
    "maad-400g": "maad-labelafrik",
    "huile-tournesol-1l": "huile-palme-artisanale-1l",
    "huile-tournesol-5l": "huile-palme-artisanale-1l",
    "butter-ghee": "beurre-karite-alimentaire-250g",
    "jus-citron-sicile-1l": "ditakh-300g",
    "concentre-tomates-rolli": "legumes-seches-thiebou-200g",
    "concentre-tomates-2kg": "legumes-seches-thiebou-200g",
    "lait-concentre-bonnet-rouge": "miel-thym-500g",
    "pate-sardinelle-pinton": "crevettes-sechees-100g",
    "sardinelle-pilchards-tomate": "crevettes-sechees-100g",
    "poisson-fume-ud": "crevettes-sechees-100g",
    "corned-beef-halal": "soumbala-100g",
    "sauce-trofai-palmier-350": "netetou-100g",
    "sauce-trofai-palmier-410": "netetou-100g",
    "bouillon-adjia": "piment-sec-moulu-80g",
    "jumbo-ramadan": "piment-sec-moulu-80g",
    "piment-rouge-antillais": "piment-sec-moulu-80g",
    "chips-plantain-doux": "bouye-baobab-250g",
    "chips-plantain-sale": "chips-plantain-doux",
    "chips-plantain-epice": "chips-plantain-doux",
    "samoussas-legumes-halal": "legumes-seches-thiebou-200g",
    "samoussas-poulet-20": "samoussas-legumes-halal",
    "samoussas-mouton-halal": "samoussas-legumes-halal",
    "nems-poulet-halal-50": "samoussas-legumes-halal",
    "nems-crevettes-poulet-halal": "samoussas-legumes-halal",
    "accras-morue": "crevettes-sechees-100g",
    "biscuits-gem": "thiakry-400g",
}


def _fetch_biosene_image(page_url: str) -> str | None:
    req = urllib.request.Request(page_url, headers={"User-Agent": "YombalMarché/1.0"})
    html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")
    patterns = [
        r'property="og:image"\s+content="([^"]+)"',
        r'class="wp-post-image[^"]*"\s[^>]*src="([^"]+)"',
        r'data-large_image="([^"]+)"',
        r'data-src="(https://biosene\.net/wp-content/uploads/[^"]+)"',
        r'src="(https://biosene\.net/wp-content/uploads/[^"]+\.(?:jpg|jpeg|png|webp))"',
    ]
    for pat in patterns:
        m = re.search(pat, html, re.I)
        if m:
            return m.group(1).replace("&amp;", "&")
    return None


def _download(url: str, dest: str) -> bool:
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "YombalMarché/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp, open(dest, "wb") as out:
        out.write(resp.read())
    return os.path.getsize(dest) > 1000


def _ext_from_url(url: str) -> str:
    path = url.split("?")[0].lower()
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        if ext in path:
            return ext if ext != ".jpeg" else ".jpg"
    return ".jpg"


def main():
    from app import app
    from extensions import db
    from models.product import Product
    from models.product_images import PRODUCT_IMAGES

    static_products = os.path.join(ROOT, "static", "img", "products")
    img_src = os.path.join(ROOT, "img")
    updated = 0

    with app.app_context():
        # 1) Biosene LabelAfrik
        for slug, page in BIOSENE_PAGES.items():
            product = Product.query.filter_by(slug=slug).first()
            if not product or product.image:
                continue
            img_url = _fetch_biosene_image(page)
            if not img_url:
                print(f"SKIP biosene (pas d'URL): {slug}")
                continue
            ext = _ext_from_url(img_url)
            rel = f"img/products/{slug}{ext}"
            dest = os.path.join(ROOT, "static", rel.replace("/", os.sep))
            try:
                _download(img_url, dest)
                product.image = rel.replace("\\", "/")
                PRODUCT_IMAGES[slug] = product.image
                updated += 1
                print(f"OK biosene: {slug}")
            except Exception as exc:
                print(f"ERR biosene {slug}: {exc}")

        # 2) Copies locales img/
        for filename, slugs in LOCAL_IMAGE_MAP.items():
            src = os.path.join(img_src, filename)
            if not os.path.isfile(src):
                continue
            ext = os.path.splitext(filename)[1].lower()
            for slug in slugs:
                product = Product.query.filter_by(slug=slug).first()
                if not product or product.image:
                    continue
                rel = f"img/products/{slug}{ext}"
                dest = os.path.join(ROOT, "static", rel.replace("/", os.sep))
                shutil.copy2(src, dest)
                product.image = rel.replace("\\", "/")
                PRODUCT_IMAGES[slug] = product.image
                updated += 1
                print(f"OK local: {slug} <- {filename}")

        # 3) Copie depuis produit similaire déjà illustré
        for slug, source_slug in COPY_FROM_EXISTING.items():
            if not source_slug:
                continue
            product = Product.query.filter_by(slug=slug).first()
            if not product or product.image:
                continue
            source = Product.query.filter_by(slug=source_slug).first()
            if not source or not source.image:
                continue
            src_path = os.path.join(ROOT, "static", source.image.replace("/", os.sep))
            if not os.path.isfile(src_path):
                continue
            ext = os.path.splitext(source.image)[1] or ".jpg"
            rel = f"img/products/{slug}{ext}"
            dest = os.path.join(ROOT, "static", rel.replace("/", os.sep))
            if not os.path.isfile(dest):
                shutil.copy2(src_path, dest)
            product.image = rel.replace("\\", "/")
            PRODUCT_IMAGES[slug] = product.image
            updated += 1
            print(f"OK copy: {slug} <- {source_slug}")

        db.session.commit()

        remaining = Product.query.filter_by(is_active=True).filter(
            (Product.image.is_(None)) | (Product.image == "")
        ).count()
        print(f"\nMis à jour: {updated} | Sans image restants: {remaining}")


if __name__ == "__main__":
    main()
