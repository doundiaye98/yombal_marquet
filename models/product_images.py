# -*- coding: utf-8 -*-
"""Chemins des photos produits (static/img/products/)."""

import os
import shutil

from extensions import db
from models.catalogue_retired import RETIRED_IMAGE_MIGRATION, RETIRED_PRODUCT_SLUGS
from models.product import Product

# slug → chemin relatif sous static/
_RAW_PRODUCT_IMAGES = {
    # Catalogue initial
    "couscous-complet-1kg": "img/products/couscous-complet-1kg.png",
    "huile-argan-bio-100ml": "img/products/huile-argan-bio-100ml.jpg",
    "miel-thym-500g": "img/products/miel-thym-500g.jpg",
    "cafe-arabica-250g": "img/products/cafe-arabica-250g.jpg",
    "savon-noir-eucalyptus": "img/products/savon-noir-eucalyptus.jpg",
    "dates-medjool-400g": "img/products/dates-medjool-400g.jpg",
    "bissap-concentre-50cl": "img/products/bissap-concentre-50cl.jpg",
    "beurre-karite-brut-150g": "img/products/beurre-karite-brut-150g.jpg",
    "huile-palme-artisanale-1l": "img/products/huile-palme-artisanale-1l.jpg",
    # Extension sénégalaise — nouvelles photos
    "bissap-seche-200g": "img/products/bissap-seche-200g.jpg",
    "gingembre-poudre-100g": "img/products/gingembre-poudre-100g.jpg",
    "bouye-baobab-250g": "img/products/bouye-baobab-250g.jpg",
    "ditakh-300g": "img/products/ditakh-300g.jpg",
    "kinkeliba-80g": "img/products/kinkeliba-80g.jpg",
    "cafe-touba-250g": "img/products/cafe-touba-250g.jpg",
    "tamarin-pulpe-200g": "img/products/tamarin-pulpe-200g.jpg",
    "riz-brise-local-1kg": "img/products/riz-brise-local-1kg.jpg",
    "mil-millet-1kg": "img/products/mil-millet-1kg.jpg",
    "sorgho-1kg": "img/products/sorgho-1kg.jpg",
    "fonio-500g": "img/products/fonio-500g.jpg",
    "farine-niebe-500g": "img/products/farine-niebe-500g.jpg",
    "soumbala-100g": "img/products/soumbala-100g.jpg",
    "netetou-100g": "img/products/netetou-100g.jpg",
    "yett-coquillages-150g": "img/products/yett-coquillages-150g.jpg",
    "piment-sec-moulu-80g": "img/products/piment-sec-moulu-80g.jpg",
    "sel-kaolack-500g": "img/products/sel-kaolack-500g.jpg",
    "beurre-karite-alimentaire-250g": "img/products/beurre-karite-alimentaire-250g.jpg",
    "thiakry-400g": "img/products/thiakry-400g.jpg",
    "legumes-seches-thiebou-200g": "img/products/legumes-seches-thiebou-200g.jpg",
    "crevettes-sechees-100g": "img/products/crevettes-sechees-100g.jpg",
    "confiture-bissap-250g": "img/products/confiture-bissap-250g.jpg",
    "graine-sesame-250g": "img/products/graine-sesame-250g.jpg",
    "pastilles-tamarin-150g": "img/products/pastilles-tamarin-150g.jpg",
    # LabelAfrik — poisson, fruits de mer, moringa (sources img/)
    "moringa-feuilles-poudre-100g": "img/products/moringa-feuilles-poudre-100g.jpg",
    "barracuda-seud-10kg": "img/products/barracuda-seud-10kg.jpg",
    "barracuda-seud-5kg": "img/products/barracuda-seud-5kg.jpg",
    "capitaine-bar-600-800-10kg": "img/products/capitaine-bar-600-800-10kg.jpg",
    "capitaine-bar-400-600-5kg": "img/products/capitaine-bar-400-600-5kg.jpg",
    "crabe-mangrove": "img/products/crabe-mangrove.jpg",
    "crevettes-crues-decortiquees": "img/products/crevettes-crues-decortiquees.jpg",
    "dorade-diaregne-tete-10kg": "img/products/dorade-diaregne-tete-10kg.jpg",
    "dorade-diaregne-tete-5kg": "img/products/dorade-diaregne-tete-5kg.jpg",
    "dorade-diaregne-sans-tete-5kg": "img/products/dorade-diaregne-sans-tete-5kg.jpg",
    "dorade-vivaneau-10kg": "img/products/dorade-vivaneau-10kg.jpg",
    "dorade-500-800-5kg": "img/products/dorade-500-800-5kg.jpg",
    "dorade-400-600-5kg": "img/products/dorade-400-600-5kg.jpg",
    "gros-machoiron": "img/products/gros-machoiron.jpg",
    "gambas-geantes-sauvages": "img/products/gambas-geantes-sauvages.jpg",
    "merou-thiof-entier-5kg": "img/products/merou-thiof-entier-5kg.jpg",
    "merou-thiof-entier-10kg": "img/products/merou-thiof-entier-10kg.jpg",
    "merou-thiof-sans-tete-5kg": "img/products/merou-thiof-sans-tete-5kg.jpg",
    "merou-thiof-sans-tete-10kg": "img/products/merou-thiof-sans-tete-10kg.jpg",
    "petits-merous-thiof": "img/products/petits-merous-thiof.jpg",
    "sole-karabot": "img/products/sole-karabot.jpg",
    "tilapia-moyen-senegal": "img/products/tilapia-moyen-senegal.jpg",
    "queues-langoustes-blanches": "img/products/queues-langoustes-blanches.jpg",
    "sardinelle-yaboye": "img/products/sardinelle-yaboye.jpg",
    "tilapia-gros-xxl-10kg": "img/products/tilapia-gros-xxl-10kg.jpg",
    "ailes-poulet-texmex-halal": "img/products/ailes-poulet-texmex-halal.jpg",
    "chinchard-600-900-10kg": "img/products/chinchard-600-900-10kg.jpg",
    "dorade-1000-plus-5kg": "img/products/dorade-1000-plus-5kg.jpg",
    "biscuits-gem": "img/products/biscuits-gem.jpg",
    # Photos produits réelles (épicerie)
    "dakhar-sachet-150g": "img/products/dakhar-sachet-150g.jpg",
    "dakhar-sachet-375g": "img/products/dakhar-sachet-375g.webp",
    "miel-fleurs-500g": "img/products/miel-fleurs-500g.jpg",
    "pate-arachide-labelafrik": "img/products/pate-arachide-labelafrik.jpg",
    "pate-arachide-dakatine": "img/products/pate-arachide-dakatine.jpg",
    "pate-arachide-pcd-500g": "img/products/pate-arachide-pcd-500g.jpg",
}

PRODUCT_IMAGES = dict(_RAW_PRODUCT_IMAGES)
for _old, _new in RETIRED_IMAGE_MIGRATION.items():
    if _old in PRODUCT_IMAGES and _new not in PRODUCT_IMAGES:
        PRODUCT_IMAGES[_new] = PRODUCT_IMAGES[_old]
for _old in RETIRED_PRODUCT_SLUGS:
    PRODUCT_IMAGES.pop(_old, None)

# Photos extraites des captures catalogue Univers Diaspora (prioritaires)
CATALOG_SCREENSHOT_IMAGES = {
    "poudre-lait-nido-400g": "img/products/poudre-lait-nido-400g.jpg",
    "poudre-lait-nido-900g": "img/products/poudre-lait-nido-900g.jpg",
    "poudre-lait-nido-1800g": "img/products/poudre-lait-nido-1800g.jpg",
    "poudre-lait-nido-2500g": "img/products/poudre-lait-nido-2500g.jpg",
    "sauce-trofai-palmier-350": "img/products/sauce-trofai-palmier-350.jpg",
    "sauce-trofai-palmier-410": "img/products/sauce-trofai-palmier-410.jpg",
    "concentre-tomates-rolli": "img/products/concentre-tomates-rolli.jpg",
    "maad-230g": "img/products/maad-230g.jpg",
    "maad-400g": "img/products/maad-400g.jpg",
    "sirop-bissap-ud": "img/products/sirop-bissap-ud.jpg",
    "sirop-gingembre-ud": "img/products/sirop-gingembre-ud.jpg",
    "concentre-tomates-2kg": "img/products/concentre-tomates-2kg.jpg",
    "pate-sardinelle-pinton": "img/products/pate-sardinelle-pinton.jpg",
    "sardinelle-pilchards-tomate": "img/products/sardinelle-pilchards-tomate.jpg",
    # Yombal Électronique
    "ecouteurs-bluetooth-yombal": "img/products/ecouteurs-bluetooth-yombal.jpg",
    "batterie-externe-20000mah": "img/products/batterie-externe-20000mah.jpg",
    "chargeur-solaire-portable": "img/products/chargeur-solaire-portable.jpg",
    "enceinte-bluetooth-portable": "img/products/enceinte-bluetooth-portable.jpg",
    "montre-connectee-yombal": "img/products/montre-connectee-yombal.jpg",
    "ampoules-led-pack-4": "img/products/ampoules-led-pack-4.jpg",
    "lampe-led-rechargeable": "img/products/lampe-led-rechargeable.jpg",
    "adaptateur-voyage-multiprise": "img/products/adaptateur-voyage-multiprise.jpg",
    "cable-usb-c-pack-2": "img/products/cable-usb-c-pack-2.jpg",
    "tablette-android-10": "img/products/tablette-android-10.jpg",
    "clavier-bluetooth-compact": "img/products/clavier-bluetooth-compact.jpg",
    "souris-sans-fil-ergonomique": "img/products/souris-sans-fil-ergonomique.jpg",
    "webcam-hd-1080p": "img/products/webcam-hd-1080p.jpg",
    "casque-audio-confort": "img/products/casque-audio-confort.jpg",
    "coque-smartphone-protection": "img/products/coque-smartphone-protection.jpg",
    "support-telephone-voiture": "img/products/support-telephone-voiture.jpg",
    "multiprise-parasurtenseur": "img/products/multiprise-parasurtenseur.jpg",
    "ventilateur-usb-portable": "img/products/ventilateur-usb-portable.jpg",
    "radio-fm-rechargeable": "img/products/radio-fm-rechargeable.jpg",
    "anneau-lumineux-led": "img/products/anneau-lumineux-led.jpg",
    # Marketplace — smartphones, électroménager, mode, chaussures, sacs
    "iphone-13-128go": "img/products/iphone-13-128go.jpg",
    "iphone-14-128go": "img/products/iphone-14-128go.jpg",
    "samsung-galaxy-a54": "img/products/samsung-galaxy-a54.jpg",
    "samsung-galaxy-s23": "img/products/samsung-galaxy-s23.jpg",
    "xiaomi-13t": "img/products/xiaomi-13t.jpg",
    "tecno-camon-20": "img/products/tecno-camon-20.jpg",
    "mixeur-plongeant-inox": "img/products/mixeur-plongeant-inox.jpg",
    "bouilloire-electrique-17l": "img/products/bouilloire-electrique-17l.jpg",
    "fer-repasser-vapeur": "img/products/fer-repasser-vapeur.jpg",
    "aspirateur-balai-sans-fil": "img/products/aspirateur-balai-sans-fil.jpg",
    "micro-ondes-20l": "img/products/micro-ondes-20l.jpg",
    "friteuse-air-5l": "img/products/friteuse-air-5l.jpg",
    "ventilateur-colonne-oscillant": "img/products/ventilateur-colonne-oscillant.jpg",
    "machine-cafe-filtre": "img/products/machine-cafe-filtre.jpg",
    "tshirt-coton-uni": "img/products/tshirt-coton-uni.jpg",
    "chemise-oxford-homme": "img/products/chemise-oxford-homme.jpg",
    "robe-legere-ete": "img/products/robe-legere-ete.jpg",
    "jean-slim-stretch": "img/products/jean-slim-stretch.jpg",
    "hoodie-molleton": "img/products/hoodie-molleton.jpg",
    "ensemble-sport-legging": "img/products/ensemble-sport-legging.jpg",
    "boubou-pagne-unisexe": "img/products/boubou-pagne-unisexe.jpg",
    "baskets-urbain-unisexe": "img/products/baskets-urbain-unisexe.jpg",
    "chaussures-running-legeres": "img/products/chaussures-running-legeres.jpg",
    "sandales-cuir-ete": "img/products/sandales-cuir-ete.jpg",
    "chaussures-ville-homme": "img/products/chaussures-ville-homme.jpg",
    "bottes-femme-mi-mollet": "img/products/bottes-femme-mi-mollet.jpg",
    "baskets-enfant-coloris": "img/products/baskets-enfant-coloris.jpg",
    "sac-a-dos-quotidien-25l": "img/products/sac-a-dos-quotidien-25l.jpg",
    "valise-cabine-rigide": "img/products/valise-cabine-rigide.jpg",
    "sac-bandouliere-urbain": "img/products/sac-bandouliere-urbain.jpg",
    "sac-weekend-50l": "img/products/sac-weekend-50l.jpg",
    "cartable-ecole-renforce": "img/products/cartable-ecole-renforce.jpg",
    "pochette-voyage-documents": "img/products/pochette-voyage-documents.jpg",
}
PRODUCT_IMAGES.update(CATALOG_SCREENSHOT_IMAGES)

# Seuls ces slugs restent dans le catalogue boutique (avec photo).
CATALOGUE_SLUGS = frozenset(PRODUCT_IMAGES.keys())

try:
    from models.catalogue_labelafrik import LABELAFRIK_SLUGS
except ImportError:
    LABELAFRIK_SLUGS = frozenset()

# Fichiers sources dans img/ (racine projet) → slug produit
IMAGE_SOURCES = {
    "BISAP S7CHE.jpg": "bissap-seche-200g",
    "Gijinbre.jpg": "gingembre-poudre-100g",
    "pain de singe.jpg": "bouye-baobab-250g",
    "DITAKH OU DETARIUM SENEGALENSE, UN CLASSIQUE DE LA MÉDECINE TRADITIONNELLE (TROUBLES DE LA DIGESTION, ANÉMIE, BRONCHITES ECT___.jpg": "ditakh-300g",
    "cinquéliba.jpg": "kinkeliba-80g",
    "Cafetera tuba.jpg": "cafe-touba-250g",
    "Tamarin.jpg": "tamarin-pulpe-200g",
    "riz.jpg": "riz-casse-1x-1kg",
    "Pearl millet.jpg": "mil-millet-1kg",
    "#Sorgo.jpg": "sorgho-1kg",
    "Superfood Fonio – Glutenfreies Urgetreide aus Afrika _ Reich an Eisen, Magnesium & Calcium.jpg": "fonio-500g",
    "farine.jpg": "farine-niebe-500g",
    "Lost Recipes of Ancient Civilization People Really___.jpg": "soumbala-100g",
    "nétetu.jpg": "netetou-100g",
    "yéte.jpg": "yett-coquillages-150g",
    "pument.jpg": "piment-sec-moulu-80g",
    "Salt.jpg": "sel-kaolack-500g",
    "beure.jpg": "beurre-karite-alimentaire-250g",
    "Thiakry ou dégué.jpg": "thiakry-400g",
    "légume.jpg": "legumes-seches-thiebou-200g",
    "Recette de crevettes marinées délicatement.jpg": "crevettes-sechees-100g",
    "Sour Cherry and Chili Jam_ A sweet and spicy jam perfect for pairing with cheese or meat_.jpg": "confiture-bissap-250g",
    "😉 SEMILLAS DE LINO - 👉 Beneficios y Propiedades.jpg": "graine-sesame-250g",
    "téléchargement (5).jpg": "pastilles-tamarin-150g",
    # Poisson & mer — photos récentes (dossier img/)
    "Poudre de feuilles de moringa — 100 g.jpg": "moringa-feuilles-poudre-100g",
    "Barracuda Seud — carton 10 kg.jpg": "barracuda-seud-10kg",
    "Barracuda_ameliore.jpg": "barracuda-seud-5kg",
    "Capitaine Bar (Ombrine) — carton 10 kg.jpg": "capitaine-bar-600-800-10kg",
    "Capitaine_Bar_Ombrine_5kg_ameliore.jpg": "capitaine-bar-400-600-5kg",
    "Crabe de mangrove — pièce.jpg": "crabe-mangrove",
    "Crevettes crues décortiquées — sachet.jpg": "crevettes-crues-decortiquees",
    "Dorade Diaregne avec tête — carton 10 kg.jpg": "dorade-diaregne-tete-10kg",
    "Dorade Diaregne avec tête — carton 5 kg.jpg": "dorade-diaregne-tete-5kg",
    "Dorade Diaregne sans tête — carton 5 kg.jpg": "dorade-diaregne-sans-tete-5kg",
    "Dorade plate Vivaneau — carton 10 kg.jpg": "dorade-vivaneau-10kg",
    "Dorade 500–800 g — carton 5 kg.jpg": "dorade-500-800-5kg",
    "Dorade.jpg": "dorade-400-600-5kg",
    "Gros machoiron — pièce.jpg": "gros-machoiron",
    "Gambas géantes sauvages — sachet.jpg": "gambas-geantes-sauvages",
    "Mérou Thiof entier — carton 5 kg.jpg": "merou-thiof-entier-5kg",
    "Mérou Thiof entier — carton 10 kg.jpg": "merou-thiof-entier-10kg",
    "Mérou Thiof sans tête — carton 5 kg.jpg": "merou-thiof-sans-tete-5kg",
    "Mérou Thiof sans tête — carton 10 kg.jpg": "merou-thiof-sans-tete-10kg",
    "Petits mérous Thiof — au kg.jpg": "petits-merous-thiof",
    "Grosse sole Karabot — pièce.jpg": "sole-karabot",
    "Tilapia moyen Sénégal — carton.jpg": "tilapia-moyen-senegal",
    "Queues de langoustes blanches — sachet.jpg": "queues-langoustes-blanches",
    "Sardinelle Yaboye — sachet.jpg": "sardinelle-yaboye",
    "Tilapia gros XXL — carton 10 kg.jpg": "tilapia-gros-xxl-10kg",
    "Ailes de poulet Tex-Mex halal — 2.jpg": "ailes-poulet-texmex-halal",
    "Chinchard entier— carton 10 kg.jpg": "chinchard-600-900-10kg",
    "Dorade 1000 g+ — carton 5 kg.jpg": "dorade-1000-plus-5kg",
    "Sauce graine de palme Trofai — 350 g.jpg": "sauce-trofai-palmier-350",
    "Sauce graine de palme Trofai — 410 g.jpg": "sauce-trofai-palmier-410",
    "Biscuits Gem.jpg": "biscuits-gem",
    # Épicerie — photos produits réelles
    "Dakhar — 150 g.jpg": "dakhar-sachet-150g",
    "Dakhar — 375 g.webp": "dakhar-sachet-375g",
    "Miel de fleurs — 500 g.jpg": "miel-fleurs-500g",
    "Sirop de bissap — 50 cl.jpg": "sirop-bissap-ud",
    "Sirop de gingembre — 50 cl.jpg": "sirop-gingembre-ud",
    "Pâte d'arachide — 500 g.jpg": "pate-arachide-labelafrik",
    "Pâte d'arachide PCD — 500 g.jpg": "pate-arachide-pcd-500g",
    "âte d'arachide Dakatine.jpg": "pate-arachide-dakatine",
    # Yombal Électronique — photos produits
    "Écouteurs Bluetooth — 1 paire.jpg": "ecouteurs-bluetooth-yombal",
    "Batterie externe 20 000 mAh — 1 unité.jpg": "batterie-externe-20000mah",
    "Chargeur solaire portable — 1 kit pliable.jpg": "chargeur-solaire-portable",
    "Enceinte Bluetooth portable — 1 enceinte.jpg": "enceinte-bluetooth-portable",
    "Montre connectée — 1 montre + bracelet + chargeur.jpg": "montre-connectee-yombal",
    "Ampoules LED — pack de 4 — Pack de 4 ampoules E27.jpg": "ampoules-led-pack-4",
    "Lampe LED rechargeable — 1 lampe + câble USB.jpg": "lampe-led-rechargeable",
    "Adaptateur voyage multiprise — 1 adaptateur multi-normes.jpg": "adaptateur-voyage-multiprise",
    "Câbles USB-C — pack de 2 — 2 câbles USB-C.jpg": "cable-usb-c-pack-2",
    "Tablette Android 10 pouces — 1 tablette 10 + charge + câble.jpg": "tablette-android-10",
    "Clavier Bluetooth compact — 1 clavier + piles _charge.jpg": "clavier-bluetooth-compact",
    "Souris sans fil ergonomique — 1 souris + dongle USB.jpg": "souris-sans-fil-ergonomique",
    "Webcam HD 1080p — 1 webcam USB.jpg": "webcam-hd-1080p",
    "Casque audio confort — 1 casque + câble jack.jpg": "casque-audio-confort",
    "Coque smartphone protection — 1 coque.jpg": "coque-smartphone-protection",
    "Support téléphone voiture — 1 support magnétique_pince.jpg": "support-telephone-voiture",
    "Multiprise parasurtenseur — 1 multiprise 1.jpg": "multiprise-parasurtenseur",
    "Ventilateur USB portable — 1 ventilateur portable.jpg": "ventilateur-usb-portable",
    "Radio FM rechargeable — 1 radio + câble USB.jpg": "radio-fm-rechargeable",
    "Anneau lumineux LED — 1 ring light + trépied.jpg": "anneau-lumineux-led",
    # Smartphones
    "iPhone 13 — 128 Go.jpg": "iphone-13-128go",
    "iPhone 14 — 128 Go.jpg": "iphone-14-128go",
    "Samsung Galaxy A54 — 128 Go.jpg": "samsung-galaxy-a54",
    "Samsung Galaxy S23 — 128 Go_256 Go selon stock.jpg": "samsung-galaxy-s23",
    "Xiaomi 13T — 256 Go.jpg": "xiaomi-13t",
    "Tecno Camon 20 — 128 Go.jpg": "tecno-camon-20",
    # Électroménager
    "Mixeur plongeant inox — 1 mixeur + accessoires.jpg": "mixeur-plongeant-inox",
    "Bouilloire électrique 1,7 L.jpg": "bouilloire-electrique-17l",
    "Fer à repasser vapeur — 1 fer + réservoir.jpg": "fer-repasser-vapeur",
    "Aspirateur balai sans fil — 1 aspirateur + 2 embouts.jpg": "aspirateur-balai-sans-fil",
    "Micro-ondes 20 L.jpg": "micro-ondes-20l",
    "Friteuse à air 5 L.jpg": "friteuse-air-5l",
    "Ventilateur colonne oscillant — 1 colonne.jpg": "ventilateur-colonne-oscillant",
    "Machine à café filtre — 1 machine + filtre permanent.jpg": "machine-cafe-filtre",
    # Habillement
    "T-shirt coton uni — Tailles S–XXL.jpg": "tshirt-coton-uni",
    "Chemise Oxford homme — Tailles S–XXL.jpg": "chemise-oxford-homme",
    "Robe légère d'été — Tailles S–XL.jpg": "robe-legere-ete",
    "Jean slim stretch — Tailles 28–42.jpg": "jean-slim-stretch",
    "Hoodie molleton — Tailles S–XXL.jpg": "hoodie-molleton",
    "Ensemble sport legging + top — Tailles S–XL.jpg": "ensemble-sport-legging",
    "Boubou ensemble pagne — Taille unique_sur mesure léger.jpg": "boubou-pagne-unisexe",
    # Chaussures
    "Baskets urbain unisexe — Pointures 36–45.jpg": "baskets-urbain-unisexe",
    "Chaussures running légères — Pointures 36–45.jpg": "chaussures-running-legeres",
    "Sandales cuir d'été — Pointures 36–44.jpg": "sandales-cuir-ete",
    "Chaussures de ville homme — Pointures 39–45.jpg": "chaussures-ville-homme",
    "Bottes femme mi-mollet — Pointures 36–41.jpg": "bottes-femme-mi-mollet",
    "Baskets enfant — Pointures 28–35.jpg": "baskets-enfant-coloris",
    # Sacs & bagagerie
    "Sac à dos quotidien 25 L.jpg": "sac-a-dos-quotidien-25l",
    "Valise cabine rigide — Cabine ~55 cm.jpg": "valise-cabine-rigide",
    "Sac bandoulière urbain — 1 sac.jpg": "sac-bandouliere-urbain",
    "Sac week-end 50 L.jpg": "sac-weekend-50l",
    "Pochette voyage documents — 1 pochette RFID selon lot.jpg": "pochette-voyage-documents",
}


_IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".gif")


def discover_image_for_slug(app_root: str | None, slug: str) -> str | None:
    """Cherche static/img/products/{slug}.ext — utile pour Render après déploiement Git."""
    if not app_root or not slug:
        return None
    products_dir = os.path.join(app_root, "static", "img", "products")
    if not os.path.isdir(products_dir):
        return None
    safe = slug.strip().lower()
    for ext in _IMAGE_EXTENSIONS:
        filename = f"{safe}{ext}"
        if os.path.isfile(os.path.join(products_dir, filename)):
            return f"img/products/{filename}"
    return None


def image_file_exists(app_root: str | None, rel_path: str | None) -> bool:
    if not app_root or not rel_path:
        return False
    return os.path.isfile(os.path.join(app_root, "static", rel_path.replace("/", os.sep)))


def install_product_images(app_root: str) -> int:
    """Copie img/ → static/img/products/ selon IMAGE_SOURCES. Retourne le nombre de fichiers copiés."""
    src_dir = os.path.join(app_root, "img")
    dest_dir = os.path.join(app_root, "static", "img", "products")
    os.makedirs(dest_dir, exist_ok=True)
    copied = 0
    for filename, slug in IMAGE_SOURCES.items():
        src = os.path.join(src_dir, filename)
        if not os.path.isfile(src):
            continue
        rel = PRODUCT_IMAGES.get(slug)
        if not rel:
            continue
        dest = os.path.join(app_root, "static", rel.replace("/", os.sep))
        if not os.path.isfile(dest) or os.path.getmtime(src) > os.path.getmtime(dest):
            shutil.copy2(src, dest)
            copied += 1
    return copied


def sync_product_images(app_root: str | None = None):
    """Copie les fichiers puis associe les photos aux produits (idempotent)."""
    from sqlalchemy import inspect

    if app_root:
        install_product_images(app_root)

    if not inspect(db.engine).has_table("products"):
        return
    cols = {c["name"] for c in inspect(db.engine).get_columns("products")}
    if "image" not in cols:
        return
    changed = False

    # 1) Cartographie explicite (catalogue historique)
    for slug, path in PRODUCT_IMAGES.items():
        product = Product.query.filter_by(slug=slug).first()
        if product and product.image != path:
            product.image = path
            changed = True

    # 2) Fichiers déjà présents dans static/img/products/ (LabelAfrik, uploads commités Git)
    for product in Product.query.all():
        current = (product.image or "").strip()
        if current and image_file_exists(app_root, current):
            continue
        discovered = discover_image_for_slug(app_root, product.slug)
        if discovered and product.image != discovered:
            product.image = discovered
            changed = True

    if changed:
        db.session.commit()


def purge_products_without_images():
    """Supprime les produits sans photo (désactive s'ils sont liés à une commande)."""
    from sqlalchemy import or_

    from models.order import OrderItem

    if not Product.query.first():
        return
    changed = False
    keep_slugs = CATALOGUE_SLUGS | LABELAFRIK_SLUGS
    for product in Product.query.filter(
        or_(Product.image.is_(None), Product.image == "")
    ).filter(~Product.slug.in_(keep_slugs)).all():
        has_orders = OrderItem.query.filter_by(product_id=product.id).first() is not None
        if has_orders:
            if product.is_active:
                product.is_active = False
                changed = True
        else:
            db.session.delete(product)
            changed = True
    if changed:
        db.session.commit()
