# -*- coding: utf-8 -*-
"""Catalogue Yombal Électronique — accessoires et tech pour le quotidien & la diaspora."""

from models.constants import CATEGORY_ELECTRONIQUE


def _item(
    sku,
    slug,
    name,
    summary,
    icon,
    price_cents,
    weight_info,
    *,
    origin="Sélection Yombal Électronique — Groupe YOMBAL",
    usage_tips="",
    conservation="À l'abri de l'humidité et des chocs. Température ambiante.",
    description_extra="",
):
    desc = (
        f"{summary}\n\n"
        f"Produit proposé par Yombal Électronique : qualité contrôlée, "
        f"garantie constructeur selon modèle, livraison via le réseau Groupe YOMBAL.\n\n"
        f"{description_extra}"
    ).strip()
    return {
        "sku": sku,
        "slug": slug,
        "name": name,
        "summary": summary,
        "description": desc,
        "price_cents": price_cents,
        "category": CATEGORY_ELECTRONIQUE,
        "icon": icon,
        "origin": origin,
        "weight_info": weight_info,
        "ingredients": "",
        "allergens": "",
        "usage_tips": usage_tips,
        "conservation": conservation,
        "stock_qty": 25,
    }


ELECTRONIQUE_CATALOGUE = [
    _item(
        "ELEC-ECOUT-BT-01",
        "ecouteurs-bluetooth-yombal",
        "Écouteurs Bluetooth",
        "Sans fil, autonomie confortable, micro intégré pour appels.",
        "🎧",
        2990,
        "1 paire — boîte + câble USB-C",
        usage_tips="Charger 2 h avant première utilisation. Appairer via Bluetooth des paramètres téléphone.",
        description_extra=(
            "Réduction du bruit ambiant en usage quotidien, commandes tactiles, "
            "étui de charge compact — idéal trajets et bureau."
        ),
    ),
    _item(
        "ELEC-POWER-20K",
        "batterie-externe-20000mah",
        "Batterie externe 20 000 mAh",
        "Recharge rapide pour smartphone et tablette, double port USB.",
        "🔋",
        3490,
        "1 unité — 20 000 mAh",
        usage_tips="Utiliser le câble fourni. Ne pas exposer au soleil direct pendant la charge.",
        description_extra=(
            "Capacité adaptée aux longs voyages. Indicateur LED de niveau de charge. "
            "Compatible la plupart des smartphones Android et iPhone (câble adapté)."
        ),
    ),
    _item(
        "ELEC-SOLAR-PWR",
        "chargeur-solaire-portable",
        "Chargeur solaire portable",
        "Panneau pliable + ports USB — autonomie hors réseau.",
        "☀️",
        4490,
        "1 kit pliable",
        usage_tips="Orienter le panneau face au soleil. Brancher l'appareil ou la batterie externe.",
        description_extra=(
            "Pensé pour chantiers, voyages et zones à coupures électriques. "
            "Résistant aux projections légères ; ranger à l'abri la nuit."
        ),
    ),
    _item(
        "ELEC-SPEAK-BT",
        "enceinte-bluetooth-portable",
        "Enceinte Bluetooth portable",
        "Son clair, autonomie longue, prise en main légère.",
        "🔊",
        3990,
        "1 enceinte — Bluetooth 5.x",
        usage_tips="Appairer en maintenant le bouton Bluetooth. Volume progressif pour préserver les haut-parleurs.",
        description_extra=(
            "Idéale pour réunions, fêtes familiales ou bureau. "
            "Connexion stable jusqu'à plusieurs mètres en intérieur."
        ),
    ),
    _item(
        "ELEC-WATCH-01",
        "montre-connectee-yombal",
        "Montre connectée",
        "Notifications, sport, fréquence cardiaque — écran tactile.",
        "⌚",
        5990,
        "1 montre + bracelet + chargeur",
        usage_tips="Installer l'app compagnon, activer Bluetooth et synchroniser le compte.",
        description_extra=(
            "Suivi d'activité, rappels, autonomie multi-jours selon usage. "
            "Bracelet interchangeables selon modèle."
        ),
    ),
    _item(
        "ELEC-LED-PACK",
        "ampoules-led-pack-4",
        "Ampoules LED — pack de 4",
        "Éclairage économe, lumière blanc chaud, culot E27.",
        "💡",
        1490,
        "Pack de 4 ampoules E27",
        usage_tips="Couper le courant avant remplacement. Ne pas utiliser avec variateur non compatible LED.",
        description_extra=(
            "Faible consommation, durée de vie longue. "
            "Adaptées maison, boutique et locaux professionnels."
        ),
    ),
    _item(
        "ELEC-LAMP-LED",
        "lampe-led-rechargeable",
        "Lampe LED rechargeable",
        "Éclairage puissant USB, modes nuit / travail.",
        "🔦",
        2490,
        "1 lampe + câble USB",
        usage_tips="Charger complètement avant première utilisation. Modes d'intensité via le bouton principal.",
        description_extra=(
            "Utile en cas de coupure, pour atelier ou déplacement. "
            "Base stable et poignée pour transport."
        ),
    ),
    _item(
        "ELEC-ADAPT-MULTI",
        "adaptateur-voyage-multiprise",
        "Adaptateur voyage multiprise",
        "Prises universelles + ports USB pour voyages Europe / Afrique.",
        "🔌",
        1990,
        "1 adaptateur multi-normes",
        usage_tips="Vérifier la tension locale. Ne pas dépasser la puissance indiquée sur le boîtier.",
        description_extra=(
            "Compact pour bagage cabine. Charge simultanément téléphone et petits appareils."
        ),
    ),
    _item(
        "ELEC-CABLE-USBC",
        "cable-usb-c-pack-2",
        "Câbles USB-C — pack de 2",
        "Charge et transfert rapides, longueur 1,5 m.",
        "📎",
        1290,
        "2 câbles USB-C — 1,5 m",
        usage_tips="Brancher côté chargeur puis appareil. Éviter de plier le câble à angle aigu.",
        description_extra=(
            "Renforcés aux extrémités. Compatibles chargeurs et power banks USB-C."
        ),
    ),
    _item(
        "ELEC-TABLET-STD",
        "tablette-android-10",
        "Tablette Android 10 pouces",
        "Écran HD, Wi-Fi, idéale lecture, vidéos et travail léger.",
        "📱",
        14990,
        "1 tablette 10\" + charge + câble",
        usage_tips="Mettre à jour le système au premier démarrage. Créer un compte pour le Play Store.",
        description_extra=(
            "Mémoire confortable pour apps courantes. "
            "Parfaite pour la famille, le suivi de projet ou la formation à distance."
        ),
    ),
    _item(
        "ELEC-CLAV-BT",
        "clavier-bluetooth-compact",
        "Clavier Bluetooth compact",
        "Frappe silencieuse, compatible téléphone, tablette et PC.",
        "⌨️",
        2490,
        "1 clavier + piles / charge",
        usage_tips="Activer le mode Bluetooth puis sélectionner le périphérique dans les réglages.",
        description_extra="Idéal télétravail et déplacements. Disposition AZERTY selon lot.",
    ),
    _item(
        "ELEC-SOURIS-SF",
        "souris-sans-fil-ergonomique",
        "Souris sans fil ergonomique",
        "Précise, légère, autonomie longue pour le quotidien.",
        "🖱️",
        1590,
        "1 souris + dongle USB",
        usage_tips="Insérer le récepteur USB. Vérifier que le commutateur ON/OFF est activé.",
        description_extra="Poignée confortable pour usage bureau prolongé.",
    ),
    _item(
        "ELEC-WEBCAM-HD",
        "webcam-hd-1080p",
        "Webcam HD 1080p",
        "Visio nette avec micro intégré — réunions et cours en ligne.",
        "🎥",
        3290,
        "1 webcam USB — 1080p",
        usage_tips="Brancher en USB, autoriser l'accès caméra dans l'application de visioconférence.",
        description_extra="Clip universel pour écran d'ordinateur ou trépied.",
    ),
    _item(
        "ELEC-CASQUE-FIL",
        "casque-audio-confort",
        "Casque audio confort",
        "Son équilibré, oreillettes rembourrées, prise jack 3,5 mm.",
        "🎧",
        2790,
        "1 casque + câble jack",
        usage_tips="Brancher sur la prise casque. Régler le volume progressivement.",
        description_extra="Adapté musique, podcasts et appels avec micro selon modèle.",
    ),
    _item(
        "ELEC-COQUE-UNI",
        "coque-smartphone-protection",
        "Coque smartphone protection",
        "Anti-choc fine, grip antidérapant — modèles courants.",
        "📱",
        1290,
        "1 coque — taille selon référence",
        usage_tips="Vérifier la compatibilité du modèle avant commande. Aligner les découpes caméra.",
        description_extra="Protection des angles et dos. Coloris assortis YOMBAL.",
    ),
    _item(
        "ELEC-SUPPORT-AUTO",
        "support-telephone-voiture",
        "Support téléphone voiture",
        "Fixation grille d'aération, rotation 360°, stable en route.",
        "🚗",
        1790,
        "1 support magnétique / pince",
        usage_tips="Clipser sur la aération, verrouiller le téléphone avant de démarrer.",
        description_extra="Compatible la plupart des smartphones avec ou sans coque fine.",
    ),
    _item(
        "ELEC-MULTI-PARA",
        "multiprise-parasurtenseur",
        "Multiprise parasurtenseur",
        "4 prises + 2 USB, protection contre les surtensions.",
        "⚡",
        2290,
        "1 multiprise 1,5 m",
        usage_tips="Ne pas dépasser la puissance max indiquée. Brancher d'abord la multiprise puis les appareils.",
        description_extra="Utile bureau, salon et boutique — charge USB intégrée.",
    ),
    _item(
        "ELEC-VENTIL-USB",
        "ventilateur-usb-portable",
        "Ventilateur USB portable",
        "Silencieux, 2 vitesses, alimentation USB ou batterie.",
        "🌀",
        1890,
        "1 ventilateur portable",
        usage_tips="Brancher en USB ou charger avant usage autonome.",
        description_extra="Compact pour bureau, voyage et pièces sans clim.",
    ),
    _item(
        "ELEC-RADIO-FM",
        "radio-fm-rechargeable",
        "Radio FM rechargeable",
        "Tuner FM clair, autonomie confortable, haut-parleur intégré.",
        "📻",
        2690,
        "1 radio + câble USB",
        usage_tips="Déployer l'antenne pour une meilleure réception. Charger régulièrement.",
        description_extra="Pratique à la maison comme en déplacement.",
    ),
    _item(
        "ELEC-RING-LED",
        "anneau-lumineux-led",
        "Anneau lumineux LED",
        "Éclairage selfie / visio, intensité réglable, trépied inclus.",
        "✨",
        3490,
        "1 ring light + trépied",
        usage_tips="Régler la température de couleur avant l'enregistrement. Fixer le téléphone au centre.",
        description_extra="Idéal contenus, réunions et maquillage.",
    ),
]

ELECTRONIQUE_SLUGS = frozenset(p["slug"] for p in ELECTRONIQUE_CATALOGUE)
