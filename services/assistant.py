# -*- coding: utf-8 -*-
"""Assistant boutique — retrieval + génération de réponse."""

from __future__ import annotations

import logging
import os
import re

from models.knowledge_chunk import KnowledgeChunk
from models.product import Product
from services import content as content_svc
from services import ecosystem_nav as eco_nav
from services import embeddings as embed_svc

logger = logging.getLogger(__name__)

DEFAULT_CHAT_MODEL = "gpt-4o-mini"
MAX_QUESTION_LEN = 500
DEFAULT_TOP_K = 5

ORDER_HINT_PATTERNS = (
    r"\b(suivre|suivi)\s+(ma\s+|de\s+la\s+|d[' ]une?\s+)?commande\b",
    r"\bo[uù]\s+en\s+est\s+ma\s+commande\b",
    r"\bnuméro\s+de\s+commande\b",
    r"\btracking\b",
    r"\bstatut\s+(de\s+)?(ma\s+|la\s+)?commande\b",
    r"\b(mon|le)\s+colis\b.*\b(où|quand|statut|suivi)\b",
    r"\b(où|quand|statut|suivi)\b.*\b(mon|le)\s+colis\b",
)

# Vue d'ensemble du Groupe YOMBAL
GROUP_OVERVIEW_PATTERNS = (
    r"\bgroupe\s+yombal\b",
    r"\bunivers\s+yombal\b",
    r"\btous?\s+(vos|les)\s+services\b",
    r"\bquels?\s+services\b",
    r"\bque\s+proposez?[-\s]?vous\b",
    r"\bautres?\s+services?\b",
    r"\boffre\s+(du\s+)?groupe\b",
    r"\bliste\s+des\s+services\b",
)

# Intentions hors catalogue boutique → services Groupe YOMBAL
ECOSYSTEM_INTENTS: list[tuple[str, tuple[str, ...]]] = [
    (
        "voyages",
        (
            r"\bvoyag",
            r"\bvol\b",
            r"\bavion\b",
            r"\bbillet",
            r"\bs[eé]jour",
            r"\bcircuit",
            r"\bcroisi[eè]re",
            r"\bteranga",
            r"\breserver?\s+(un\s+)?vol",
            r"\balle[rz]\s+(au\s+)?s[eé]n[eé]gal",
        ),
    ),
    (
        "investissement",
        (
            r"\binvest",
            r"\bopportunit[eé]s?\s+d[' ]invest",
            r"\bplacement\b",
            r"\bbusiness\s+plan\b",
            r"\bfaisabilit[eé]\b",
        ),
    ),
    (
        "immobilier-btp",
        (
            r"\bimmobilier",
            r"\bterrain",
            r"\bparcelle",
            r"\bconstruction",
            r"\br[eé]novation",
            r"\bbtp\b",
            r"\bchantier",
            r"\bmaison\b.*\bs[eé]n[eé]gal",
            r"\bkeur\b",
            r"\bndayane\b",
            r"\bsangalcam\b",
            r"\byenne\b",
            r"\bndoukhoura\b",
        ),
    ),
    (
        "transport",
        (
            r"\btransport",
            r"\blocation\s+(de\s+)?voiture",
            r"\bvoiture\b",
            r"\bv[eé]hicule",
            r"\bd[eé]m[eé]nagement",
            r"\benvoi\s+de\s+colis",
            r"\bachat\s+(de\s+)?v[eé]hicule",
            r"\bvente\s+(de\s+)?v[eé]hicule",
        ),
    ),
    (
        "restaurant",
        (
            r"\brestaurant",
            r"\btraiteur",
            r"\br[eé]server?\s+(une?\s+)?table",
            r"\bmanger\b",
            r"\bcatering\b",
            r"\b[eé]v[eé]nement.*(traiteur|restaurant)",
        ),
    ),
    (
        "electronique",
        (
            r"\b[eé]lectronique",
            r"\bsmartphone",
            r"\bt[eé]l[eé]phone",
            r"\baccessoires?\s+(high[-\s]?tech|tech)",
            r"\b[eé]lectrom[eé]nager",
            r"\bcasque\b",
            r"\benceinte\b",
        ),
    ),
    (
        "coiffure",
        (
            r"\bcoiffure",
            r"\bcoiffeur",
            r"\bcoiffeuse",
            r"\btresse",
            r"\bsalon\s+(de\s+)?coiffure",
            r"\bsoins?\s+capillaires?",
            r"\bbeaut[eé]\b",
        ),
    ),
]

LANG_NAMES = {
    "fr": "français",
    "en": "anglais",
    "wo": "wolof",
    "es": "espagnol",
    "pt": "portugais",
    "de": "allemand",
    "it": "italien",
    "ar": "arabe",
    "nl": "néerlandais",
    "ru": "russe",
    "zh": "chinois",
    "ja": "japonais",
    "ko": "coréen",
    "auto": "la même langue que le message du client",
}

THANKS_REPLY = {
    "fr": (
        "Je vous en prie. "
        "L'équipe Yombal Market reste à votre disposition pour toute autre question "
        "concernant le catalogue, les livraisons ou les services du Groupe YOMBAL. "
        "Nous vous souhaitons une excellente journée."
    ),
    "en": (
        "You're welcome. "
        "The Yombal Market team remains available for any question about the catalogue, "
        "delivery or Groupe YOMBAL services. Have a wonderful day."
    ),
    "wo": (
        "Amul solo. "
        "Équipe Yombal Market mooy lekk sa laaj yu aju ci boutique, livraison walla "
        "services yu Groupe YOMBAL. Ba beneen yoon — jamm ak jàmm."
    ),
    "es": (
        "De nada. "
        "El equipo de Yombal Market sigue a su disposición para cualquier pregunta "
        "sobre el catálogo, las entregas o los servicios del Groupe YOMBAL. "
        "Que tenga un excelente día."
    ),
    "pt": (
        "De nada. "
        "A equipe Yombal Market permanece à disposição para qualquer pergunta "
        "sobre o catálogo, entregas ou serviços do Groupe YOMBAL. "
        "Tenha um excelente dia."
    ),
    "de": (
        "Gern geschehen. "
        "Das Yombal Market Team steht Ihnen weiterhin für Fragen zu Katalog, "
        "Lieferung oder Groupe YOMBAL Services zur Verfügung. Einen schönen Tag."
    ),
    "it": (
        "Prego. "
        "Il team Yombal Market resta a disposizione per ogni domanda su catalogo, "
        "consegne o servizi del Groupe YOMBAL. Buona giornata."
    ),
    "ar": (
        "عفوًا. "
        "فريق Yombal Market جاهز لأي سؤال حول الكتالوج أو التوصيل أو خدمات Groupe YOMBAL. "
        "يومًا سعيدًا."
    ),
}

GREETING_REPLY = {
    "fr": (
        "Bonjour, bienvenue chez Yombal Market.\n\n"
        "Je suis le conseiller du Groupe YOMBAL. "
        "Je peux vous aider pour la boutique (produits, commandes, livraisons) "
        "ou vous orienter vers Voyages, Immobilier & BTP, Transports, "
        "Restaurant, Électronique et Coiffure.\n\n"
        "Vous pouvez m'écrire dans votre langue "
        "(français, anglais, wolof, espagnol, etc.).\n\n"
        "Comment puis-je vous accompagner ?"
    ),
    "en": (
        "Hello, welcome to Yombal Market.\n\n"
        "I am the Groupe YOMBAL advisor. "
        "I can help with the shop (products, orders, delivery) "
        "or guide you to Travel, Real Estate & Construction, Transport, "
        "Restaurant, Electronics and Haircare.\n\n"
        "You can write in your language "
        "(French, English, Wolof, Spanish, and more).\n\n"
        "How can I help you?"
    ),
    "wo": (
        "Asalaa maalekum, dalal ak jàmm ci Yombal Market.\n\n"
        "Man maay conseiller bu Groupe YOMBAL. "
        "Maa la mën a dimbali ci boutique (produits, commande, livraison) "
        "walla yóbbu la ci Voyages, Immobilier & BTP, Transports, "
        "Restaurant, Électronique ak Coiffure.\n\n"
        "Mën nga wax ci sa làkk (wolof, français, anglais, ak yeneen).\n\n"
        "Lan laa la mën a dimbali?"
    ),
    "es": (
        "Hola, bienvenido/a a Yombal Market.\n\n"
        "Soy el asesor del Groupe YOMBAL. "
        "Puedo ayudarle con la tienda (productos, pedidos, entregas) "
        "o orientarle hacia Viajes, Inmobiliaria & BTP, Transportes, "
        "Restaurante, Electrónica y Peluquería.\n\n"
        "Puede escribirme en su idioma.\n\n"
        "¿En qué puedo ayudarle?"
    ),
    "pt": (
        "Olá, bem-vindo(a) à Yombal Market.\n\n"
        "Sou o consultor do Groupe YOMBAL. "
        "Posso ajudar com a loja (produtos, encomendas, entregas) "
        "ou orientar para Viagens, Imobiliário & BTP, Transportes, "
        "Restaurante, Eletrónica e Cabeleireiro.\n\n"
        "Pode escrever no seu idioma.\n\n"
        "Como posso ajudar?"
    ),
    "de": (
        "Hallo, willkommen bei Yombal Market.\n\n"
        "Ich bin der Berater der Groupe YOMBAL. "
        "Ich helfe Ihnen im Shop (Produkte, Bestellungen, Lieferung) "
        "oder leite Sie zu Reisen, Immobilien & Bau, Transport, "
        "Restaurant, Elektronik und Friseur weiter.\n\n"
        "Sie können in Ihrer Sprache schreiben.\n\n"
        "Wie kann ich Ihnen helfen?"
    ),
    "it": (
        "Ciao, benvenuto/a su Yombal Market.\n\n"
        "Sono il consulente del Groupe YOMBAL. "
        "Posso aiutarla con il negozio (prodotti, ordini, consegne) "
        "o indirizzarla verso Viaggi, Immobiliare & BTP, Trasporti, "
        "Ristorante, Elettronica e Parrucchieri.\n\n"
        "Può scrivermi nella sua lingua.\n\n"
        "Come posso aiutarla?"
    ),
    "ar": (
        "مرحبًا، أهلاً بك في Yombal Market.\n\n"
        "أنا مستشار Groupe YOMBAL. "
        "يمكنني مساعدتك في المتجر (منتجات، طلبات، توصيل) "
        "أو توجيهك إلى السفر والعقار والنقل والمطعم والإلكترونيات وتصفيف الشعر.\n\n"
        "يمكنك الكتابة بلغتك.\n\n"
        "كيف يمكنني مساعدتك؟"
    ),
}

GREETING_ONLY_PATTERNS = (
    r"^(?:bonjour|bonsoir|bonne\s+journ[eé]e|salut|hello|hi|hey|coucou)(?:\s+[!.…]*)?$",
    r"^(?:bonjour|bonsoir|salut|hello)(?:\s+(?:à\s+vous|messieurs?|mesdames?))?[\s!.]*$",
    r"^(?:bonjour|bonsoir)[\s,]+(?:je\s+vous\s+)?(?:salue|salut)[\s!.]*$",
    # Wolof
    r"^(?:asalaa?\s*maalekum|salaam\s*aleekum|salam\s*aleikum|assalamu?\s*alaikum)[\s!.]*$",
    r"^(?:nanga\s+def|nanu\s+def|na\s+ngi\s+fi|naka\s+nga\s+def)[\s!.]*$",
    # Autres langues
    r"^(?:hola|buenos?\s+d[ií]as|buenas?\s+(?:tardes|noches))[\s!.]*$",
    r"^(?:ol[aá]|bom\s+dia|boa\s+(?:tarde|noite))[\s!.]*$",
    r"^(?:hallo|guten\s+(?:tag|morgen|abend)|gr[uü][sß]?\s*gott)[\s!.]*$",
    r"^(?:ciao|buongiorno|buonasera|salve)[\s!.]*$",
    r"^(?:marhaba|ahlan|as[- ]?sal[aā]mu?\s*['`]?alaykum)[\s!.]*$",
)

THANKS_ONLY_PATTERNS = (
    r"^(?:un\s+)?(?:grand\s+)?merci(?:\s+(?:beaucoup|infiniment|bien|à\s+vous|pour\s+(?:tout|votre\s+aide|l'?info(?:rmation)?(?:rmations)?|votre\s+réponse|votre\s+message)))?[\s!.]*$",
    r"^je\s+vous\s+remercie(?:\s+(?:beaucoup|infiniment|bien))?[\s!.]*$",
    r"^(?:thanks?|thank\s+you)(?:\s+(?:a\s+lot|so\s+much))?[\s!.]*$",
    r"^(?:ok|d'accord|parfait|super|génial|très\s+bien)[\s,!.]+(?:merci|je\s+vous\s+remercie)(?:\s+(?:beaucoup|infiniment|pour\s+tout))?[\s!.]*$",
    r"^(?:merci|je\s+vous\s+remercie)[\s,!.]+(?:ok|d'accord|parfait|super|génial|très\s+bien)[\s!.]*$",
    # Wolof
    r"^(?:j[eë]r[eë]j[eë]f|jerejef|jerrejef)(?:\s+(?:bu\s+baax|lool))?[\s!.]*$",
    # Autres langues
    r"^(?:gracias|muchas\s+gracias)[\s!.]*$",
    r"^(?:obrigad[oa]|muito\s+obrigad[oa])[\s!.]*$",
    r"^(?:danke(?:\s+sch[oö]n)?|vielen\s+dank)[\s!.]*$",
    r"^(?:grazie(?:\s+mille)?)[\s!.]*$",
    r"^(?:shukran|choukran|شكرا(?:ً)?)[\s!.]*$",
)

SYSTEM_PROMPT = """Tu es le conseiller client officiel de Yombal Market,
enseigne e-commerce du Groupe YOMBAL (« votre marché en poche »).

Langues :
- Réponds TOUJOURS dans la langue utilisée par le client (toutes langues étrangères incluses).
- Priorité locale : français, anglais, wolof (orthographe latine courante).
- Autres langues courantes aussi prises en charge : espagnol, portugais, allemand, italien, arabe, etc.
- Si le message mélange plusieurs langues, privilégie la langue dominante du message.
- Si la langue détectée est incertaine, suis fidèlement la langue du message client.
- Les noms de marques/services (Yombal Market, Yombal Voyages, etc.) restent inchangés.
- Les prix et unités monétaires restent en euros (€), quelle que soit la langue.

Ton : professionnel, précis, courtois. Réponses structurées, 2 à 5 phrases max (sauf listes).

Périmètre Yombal Market (boutique) :
- Catalogue alimentaire, cosmétiques, électronique, recettes, coffrets, livraison, paiement.

Périmètre Groupe YOMBAL (Univers YOMBAL) — oriente vers la fiche dédiée :
- Yombal Voyages (vols, séjours, circuits)
- Yombal Investissement Opportunités
- Yombal Immobilier & BTP (terrains, construction)
- Yombal Transports (véhicules, location, déménagement, colis)
- Yombal Restaurant (restauration, traiteur)
- Yombal Électronique (aussi disponible en boutique)
- Yombal Coiffure (salon, soins)
- Autres services / contact transversal

Règles :
- Utilise UNIQUEMENT le contexte fourni. N'invente jamais prix, stock, délais ou produits.
- Suivi de commande : renvoyer vers la page « Suivi de commande » (numéro + e-mail d'achat).
- Services hors boutique : indiquer le service concerné et la page / formulaire dédié, sans inventer de tarifs.
- Si la question porte sur l'ensemble du Groupe, énumérer les services ci-dessus et renvoyer vers Univers YOMBAL.
- En cas d'incertitude : proposer la page Contact.
- Pas de conseils médicaux.
- Remerciements : réponse courte et courtoise, sans argumentaire commercial.
- Évite le langage familier et les emojis."""

REFUSAL_NO_KEY = {
    "fr": (
        "Notre assistant est momentanément indisponible. "
        "Vous pouvez consulter la FAQ sur la page Contact ou nous écrire directement."
    ),
    "en": (
        "Our advisor is temporarily unavailable. "
        "Please check the FAQ on the Contact page or email us directly."
    ),
    "wo": (
        "Conseiller bi amul ci jamono jii. "
        "Mën nga xool FAQ ci page Contact walla bind nu."
    ),
    "es": (
        "Nuestro asesor no está disponible temporalmente. "
        "Consulte la FAQ en la página Contacto o escríbanos directamente."
    ),
    "pt": (
        "O nosso consultor está temporariamente indisponível. "
        "Consulte a FAQ na página Contacto ou escreva-nos diretamente."
    ),
    "de": (
        "Unser Berater ist vorübergehend nicht verfügbar. "
        "Bitte prüfen Sie die FAQ auf der Kontaktseite oder schreiben Sie uns."
    ),
    "it": (
        "Il nostro consulente è temporaneamente non disponibile. "
        "Consulti la FAQ nella pagina Contatti o ci scriva direttamente."
    ),
    "ar": (
        "المستشار غير متاح مؤقتًا. "
        "يمكنك مراجعة الأسئلة الشائعة في صفحة الاتصال أو مراسلتنا مباشرة."
    ),
}
REFUSAL_EMPTY_INDEX = (
    "L'index catalogue est en cours de mise à jour. "
    "Voici néanmoins les résultats d'une recherche directe dans Yombal Market."
)
REFUSAL_API_ERROR = (
    "Le service de conseil intelligent est temporairement indisponible. "
    "Voici une recherche dans le catalogue, ou contactez-nous via la page Contact."
)
REFUSAL_ORDER = {
    "fr": (
        "Pour consulter le statut d'une commande, utilisez la page Suivi de commande "
        "avec votre numéro de commande et l'adresse e-mail renseignée lors de l'achat."
    ),
    "en": (
        "To check an order status, open the Order tracking page "
        "with your order number and the email used at checkout."
    ),
    "wo": (
        "Ngir xool sa commande, demal ci page Suivi de commande "
        "ak numéro commande bi ak email bi nga jëfandikoo."
    ),
    "es": (
        "Para consultar el estado de un pedido, use la página Seguimiento de pedido "
        "con su número de pedido y el correo electrónico usado en la compra."
    ),
    "pt": (
        "Para consultar o estado de uma encomenda, use a página Seguimento de encomenda "
        "com o número da encomenda e o e-mail usado na compra."
    ),
    "de": (
        "Um den Status einer Bestellung zu prüfen, öffnen Sie die Seite Bestellverfolgung "
        "mit Ihrer Bestellnummer und der beim Kauf angegebenen E-Mail-Adresse."
    ),
    "it": (
        "Per verificare lo stato di un ordine, usi la pagina Tracciamento ordine "
        "con il numero d'ordine e l'e-mail usata all'acquisto."
    ),
    "ar": (
        "لمتابعة حالة الطلب، استخدم صفحة تتبع الطلب "
        "مع رقم الطلب والبريد الإلكتروني المستخدم عند الشراء."
    ),
}

EMPTY_CATALOGUE_REPLY = {
    "fr": (
        "Je n'ai pas identifié d'élément correspondant dans le catalogue. "
        "Vous pouvez parcourir la boutique, consulter la FAQ (page Contact) "
        "ou nous adresser votre demande via le formulaire de contact."
    ),
    "en": (
        "I could not find a matching item in the catalogue. "
        "You can browse the shop, check the FAQ (Contact page), "
        "or send us a message via the contact form."
    ),
    "wo": (
        "Gisuma dara bu mel ni loolu ci catalogue bi. "
        "Mën nga xool boutique bi, FAQ (page Contact), "
        "walla yonnee nu laaj ci formulaire contact."
    ),
    "es": (
        "No he encontrado un elemento correspondiente en el catálogo. "
        "Puede explorar la tienda, consultar la FAQ (página Contacto) "
        "o enviarnos su solicitud mediante el formulario de contacto."
    ),
    "pt": (
        "Não encontrei um item correspondente no catálogo. "
        "Pode explorar a loja, consultar a FAQ (página Contacto) "
        "ou enviar-nos o pedido através do formulário de contacto."
    ),
    "de": (
        "Ich habe keinen passenden Eintrag im Katalog gefunden. "
        "Sie können den Shop durchsuchen, die FAQ (Kontaktseite) prüfen "
        "oder uns über das Kontaktformular schreiben."
    ),
    "it": (
        "Non ho trovato un elemento corrispondente nel catalogo. "
        "Può sfogliare il negozio, consultare la FAQ (pagina Contatti) "
        "o inviarci la richiesta tramite il modulo di contatto."
    ),
    "ar": (
        "لم أجد عنصرًا مطابقًا في الكتالوج. "
        "يمكنك تصفح المتجر أو مراجعة الأسئلة الشائعة (صفحة الاتصال) "
        "أو مراسلتنا عبر نموذج الاتصال."
    ),
}


def assistant_enabled() -> bool:
    flag = (os.environ.get("ASSISTANT_ENABLED") or "1").strip().lower()
    return flag not in ("0", "false", "no", "off")


def chat_model() -> str:
    return (os.environ.get("OPENAI_CHAT_MODEL") or DEFAULT_CHAT_MODEL).strip()


def top_k() -> int:
    try:
        return max(1, min(10, int(os.environ.get("ASSISTANT_TOP_K") or DEFAULT_TOP_K)))
    except ValueError:
        return DEFAULT_TOP_K


def _normalize_question(text: str) -> str:
    q = (text or "").strip()
    if len(q) > MAX_QUESTION_LEN:
        q = q[:MAX_QUESTION_LEN]
    return q


def _detect_language(question: str) -> str:
    """Détecte la langue du message (fr/en/wo + langues étrangères courantes)."""
    q = (question or "").strip().lower()
    if not q:
        return "fr"

    # Écritures non latines
    if re.search(r"[\u0600-\u06FF]", question or ""):
        return "ar"
    if re.search(r"[\u0400-\u04FF]", question or ""):
        return "ru"
    if re.search(r"[\u3040-\u30ff]", question or ""):
        return "ja"
    if re.search(r"[\uac00-\ud7af]", question or ""):
        return "ko"
    if re.search(r"[\u4e00-\u9fff]", question or ""):
        return "zh"

    markers = {
        "wo": (
            "nanga", "nanu", "asalaa", "salaam", "salam", "jërëjëf", "jerejef",
            "jerrejef", "ndax", "lool", "baax", "jàmm", "jamm", "waaw", "déedéet",
            "deedeet", "fan la", "lan la", "maa ngi", "maangi", "yow", "leen",
            "defara", "dimbali", "bëgg", "begg", "xam", "gis", "jënd", "jend",
        ),
        "en": (
            " the ", " you ", " your ", " please", " order", " delivery", " shipping",
            " how ", " what ", " where ", " want", " need", " have you", " can i",
            "hello", "thanks", "thank you", "price", "product",
        ),
        "fr": (
            " je ", " vous ", " nous ", " les ", " des ", " une ", " est ", " pour ",
            " comment ", " avez", " voulez", " souhait", " commande", " livraison",
            "bonjour", "bonsoir", "salut", "coucou", "merci", "produit", "prix",
        ),
        "es": (
            " el ", " los ", " las ", " una ", " qué ", " como ", " quiero", "tiene",
            "hola", "gracias", "precio", "producto", "pedido", "entrega", "ustedes",
            "buenos dias", "buenas",
        ),
        "pt": (
            " você", "voce", "obrigad", "olá", "ola ", "preço", "preco", "quero",
            "tem ", "produto", "encomenda", "entrega", "por favor", "bom dia",
        ),
        "de": (
            " der ", " die ", " das ", " und ", " ich ", " bitte", "danke", "hallo",
            "preis", "produkt", "bestellung", "lieferung", "haben sie", "guten",
        ),
        "it": (
            " il ", " gli ", " una ", " che ", "sono", "vorrei", "grazie", "ciao",
            "prezzo", "prodotto", "ordine", "consegna", "buongiorno", "per favore",
        ),
        "ar": ("shukran", "choukran", "marhaba", "ahlan", "min fadlik", "kayfa"),
        "nl": (
            " de ", " het ", " een ", " ik ", "u ", "alstublieft", "dank", "hallo",
            "prijs", "product", "bestelling", "levering", "goedemorgen",
        ),
    }

    padded = f" {q} "
    scores = {
        code: sum(1 for m in words if m in padded or q.startswith(m.strip()))
        for code, words in markers.items()
    }

    if re.search(
        r"\b(asalaa|salaam|nanga\s+def|nanu\s+def|j[eë]r[eë]j[eë]f|jerejef)\b",
        q,
    ):
        scores["wo"] += 3
    if re.search(r"\b(hola|gracias|buenos?\s+d[ií]as)\b", q):
        scores["es"] += 3
    if re.search(r"\b(ol[aá]|obrigad[oa]|bom\s+dia)\b", q):
        scores["pt"] += 3
    if re.search(r"\b(hallo|danke|guten\s+tag)\b", q):
        scores["de"] += 2
    if re.search(r"\b(ciao|grazie|buongiorno)\b", q):
        scores["it"] += 3
    if re.search(r"\b(bonjour|bonsoir|salut|merci)\b", q):
        scores["fr"] += 2
    if re.search(r"\b(hello|hi|hey|thanks?|thank\s+you)\b", q):
        scores["en"] += 2

    best_lang, best_score = max(scores.items(), key=lambda item: item[1])
    if best_score >= 1:
        return best_lang
    # Latin sans indice clair : laisser l'IA suivre la langue du message
    if len(q) >= 12 and re.search(r"[a-zàâäáãåæçéèêëíìîïñóòôöõøœúùûüýÿ]", q):
        return "auto"
    return "fr"


def _language_label(lang: str) -> str:
    return LANG_NAMES.get(lang) or LANG_NAMES["auto"]


def _localized(mapping, lang: str, fallback: str | None = None) -> str:
    if isinstance(mapping, str):
        return mapping
    if lang in mapping:
        return mapping[lang]
    # Langues étrangères sans gabarit dédié → anglais international
    if lang not in ("fr", "wo") and "en" in mapping:
        return mapping["en"]
    if fallback and fallback in mapping:
        return mapping[fallback]
    return mapping.get("fr") or next(iter(mapping.values()))

def _looks_like_order_tracking(question: str) -> bool:
    lower = question.lower()
    return any(re.search(pat, lower) for pat in ORDER_HINT_PATTERNS)


def _looks_like_group_overview(question: str) -> bool:
    lower = question.lower()
    return any(re.search(pat, lower) for pat in GROUP_OVERVIEW_PATTERNS)


def _answer_group_overview() -> dict:
    """Présente l'ensemble des services du Groupe YOMBAL."""
    lines = [
        "Le Groupe YOMBAL regroupe plusieurs activités complémentaires. "
        "Yombal Market est la boutique en ligne (épicerie, cosmétiques, électronique, recettes, coffrets).",
        "",
        "Services Univers YOMBAL :",
    ]
    sources = [
        {
            "type": "ecosystem",
            "id": "boutique",
            "title": "Yombal Market — Boutique",
            "url": "/boutique",
        }
    ]
    for item in eco_nav.ecosystem_nav_items():
        slug = item["slug"]
        title = item.get("title") or item.get("short_label") or slug
        tagline = item.get("tagline") or ""
        lines.append(f"• {title} — {tagline}" if tagline else f"• {title}")
        sources.append(
            {
                "type": "ecosystem",
                "id": slug,
                "title": title,
                "url": f"/ecosysteme/{slug}",
            }
        )
    lines.append(
        "Indiquez le service qui vous intéresse, ou ouvrez le menu Univers YOMBAL "
        "pour accéder à chaque fiche."
    )
    return {
        "answer": "\n".join(lines),
        "sources": sources,
        "hint": "ecosystem",
        "ecosystem_slug": "autres-services",
        "mode": "ecosystem",
    }


def _detect_ecosystem_slug(question: str) -> str | None:
    """Repère une intention liée à un service Groupe YOMBAL (hors catalogue)."""
    lower = question.lower()
    for slug, patterns in ECOSYSTEM_INTENTS:
        if any(re.search(pat, lower) for pat in patterns):
            return slug
    return None


def _answer_ecosystem(slug: str) -> dict:
    service = eco_nav.ECOSYSTEM_SERVICES.get(slug) or {}
    title = service.get("title") or slug
    lead = service.get("lead") or ""
    bullets = service.get("bullets") or []
    cta = service.get("cta_label") or "Accéder au service"
    page_url = f"/ecosysteme/{slug}"
    external = (service.get("external_url") or "").strip()
    boutique_category = service.get("boutique_category")

    lines = [
        f"Votre demande concerne {title}, service du Groupe YOMBAL.",
    ]
    if slug != "autres-services":
        lines[0] = (
            f"Votre demande concerne {title}, service du Groupe YOMBAL "
            f"(complémentaire à la boutique Yombal Market)."
        )
    if lead:
        lines.append(lead)
    if bullets:
        lines.append("Points clés :")
        for bullet in bullets[:5]:
            lines.append(f"• {bullet}")
    if external:
        if slug == "voyages":
            lines.append(
                f"Pour poursuivre, consultez la fiche {title} ou le site officiel "
                "via les liens ci-dessous."
            )
        else:
            lines.append(f"Pour poursuivre, utilisez les liens ci-dessous ({cta}).")
    elif boutique_category:
        lines.append(
            f"Une partie de l'offre est aussi disponible dans la boutique en ligne. "
            f"Utilisez les liens ci-dessous ({cta})."
        )
    else:
        lines.append(
            f"Pour formuler une demande, ouvrez la page {title} "
            f"ou le menu Univers YOMBAL ({cta})."
        )

    sources = [
        {
            "type": "ecosystem",
            "id": slug,
            "title": f"Fiche {title}",
            "url": page_url,
        }
    ]
    if boutique_category:
        sources.append(
            {
                "type": "ecosystem",
                "id": f"{slug}-boutique",
                "title": "Voir en boutique",
                "url": f"/boutique?categorie={boutique_category}",
            }
        )
    if external:
        sources.append(
            {
                "type": "ecosystem",
                "id": f"{slug}-external",
                "title": "Site officiel",
                "url": external,
            }
        )

    return {
        "answer": "\n".join(lines),
        "sources": sources,
        "hint": "ecosystem",
        "ecosystem_slug": slug,
        "mode": "ecosystem",
    }


def _looks_like_thanks(question: str) -> bool:
    """Remerciement simple (pas « merci de… » = formule de politesse / demande)."""
    q = (question or "").strip().lower()
    if not q or len(q) > 120:
        return False
    if re.match(r"^merci\s+d[e']", q):
        return False
    return any(re.search(pat, q) for pat in THANKS_ONLY_PATTERNS)


def _looks_like_greeting(question: str) -> bool:
    """Salutation seule, sans demande associée."""
    q = (question or "").strip().lower()
    if not q or len(q) > 48:
        return False
    return any(re.search(pat, q) for pat in GREETING_ONLY_PATTERNS)


def _question_tokens(question: str) -> list[str]:
    stop = {
        "avez", "vous", "des", "les", "une", "est", "pour", "dans", "avec", "sans",
        "comment", "quels", "quel", "quelle", "que", "qui", "sur", "pas", "plus",
        "tout", "tous", "notre", "nos", "votre", "mes", "the", "and", "are",
    }
    tokens = [t.lower() for t in re.findall(r"[a-zàâäéèêëïîôùûüç0-9]+", question.lower())]
    return [t for t in tokens if len(t) >= 3 and t not in stop]


def _score_text(haystack: str, tokens: list[str]) -> float:
    if not haystack or not tokens:
        return 0.0
    text = haystack.lower()
    return float(sum(1 for token in tokens if token in text))


def _local_hits(question: str, limit: int = 5) -> list[dict]:
    tokens = _question_tokens(question)
    if not tokens:
        tokens = [question.lower()[:40]]

    hits: list[dict] = []

    for product in Product.query.filter_by(is_active=True).all():
        hay = " ".join(
            filter(
                None,
                [
                    product.name,
                    product.summary,
                    product.description,
                    product.ingredients,
                    product.category,
                    product.origin,
                    product.slug,
                ],
            )
        )
        score = _score_text(hay, tokens)
        if score <= 0:
            continue
        snippet = (product.summary or product.description or "")[:160]
        hits.append(
            {
                "score": score,
                "type": "product",
                "id": product.slug,
                "title": product.name,
                "url": f"/produit/{product.slug}",
                "line": f"{product.name} — {product.price_euros():.2f} € — {snippet}",
            }
        )

    for i, item in enumerate(content_svc.all_faq_items()):
        hay = f"{item.get('q', '')} {item.get('a', '')}"
        score = _score_text(hay, tokens)
        if score <= 0:
            continue
        hits.append(
            {
                "score": score + 0.5,
                "type": "faq",
                "id": f"faq-{i}",
                "title": item.get("q", "FAQ"),
                "url": "/contact#faq",
                "line": f"{item.get('q', '')} — {item.get('a', '')}",
            }
        )

    for recipe in content_svc.all_recipe_defs():
        hay = " ".join(
            filter(
                None,
                [
                    recipe.get("title"),
                    recipe.get("summary"),
                    recipe.get("kind_label"),
                    " ".join(
                        ing.get("product_slug", "")
                        for ing in recipe.get("ingredients", [])
                    ),
                ],
            )
        )
        score = _score_text(hay, tokens)
        if score <= 0:
            continue
        hits.append(
            {
                "score": score,
                "type": "recipe",
                "id": recipe["slug"],
                "title": recipe.get("title", recipe["slug"]),
                "url": f"/recette/{recipe['slug']}",
                "line": f"Recette : {recipe.get('title', '')} — {recipe.get('summary', '')}",
            }
        )

    for coffret in content_svc.all_coffret_defs():
        hay = " ".join(
            filter(
                None,
                [
                    coffret.get("title"),
                    coffret.get("summary"),
                    coffret.get("theme_label"),
                    " ".join(
                        ing.get("product_slug", "")
                        for ing in coffret.get("ingredients", [])
                    ),
                ],
            )
        )
        score = _score_text(hay, tokens)
        if score <= 0:
            continue
        hits.append(
            {
                "score": score,
                "type": "coffret",
                "id": coffret["slug"],
                "title": coffret.get("title", coffret["slug"]),
                "url": f"/coffret/{coffret['slug']}",
                "line": f"Coffret : {coffret.get('title', '')} — {coffret.get('summary', '')}",
            }
        )

    for chunk in KnowledgeChunk.query.all():
        score = _score_text(chunk.content, tokens)
        if score <= 0:
            continue
        if any(h["type"] == chunk.source_type and h["id"] == chunk.source_id for h in hits):
            continue
        hits.append(
            {
                "score": score,
                "type": chunk.source_type,
                "id": chunk.source_id,
                "title": chunk.title,
                "url": chunk.url_path or "/",
                "line": f"{chunk.title} — {(chunk.content or '')[:140]}",
            }
        )

    hits.sort(key=lambda item: item["score"], reverse=True)
    return hits[:limit]


def _answer_from_local_hits(
    question: str,
    hits: list[dict],
    *,
    prefix: str = "",
    lang: str = "fr",
) -> dict:
    if not hits:
        return {
            "answer": _localized(EMPTY_CATALOGUE_REPLY, lang),
            "sources": [],
            "mode": "local",
            "lang": lang,
        }

    intro = {
        "fr": "Éléments correspondants :",
        "en": "Matching items:",
        "wo": "Li ñu gis:",
        "es": "Elementos coincidentes:",
        "pt": "Itens correspondentes:",
        "de": "Passende Einträge:",
        "it": "Elementi corrispondenti:",
        "ar": "العناصر المطابقة:",
    }
    outro = {
        "fr": "Consultez les liens ci-dessous pour le détail.",
        "en": "Please use the links below for more details.",
        "wo": "Xoolal liens yi ci suuf ngir xibaar yu gëna bari.",
        "es": "Consulte los enlaces a continuación para más detalles.",
        "pt": "Consulte as ligações abaixo para mais detalhes.",
        "de": "Bitte nutzen Sie die Links unten für weitere Details.",
        "it": "Consulti i link qui sotto per i dettagli.",
        "ar": "يرجى استخدام الروابط أدناه للمزيد من التفاصيل.",
    }

    lines = [prefix] if prefix else []
    lines.append(_localized(intro, lang))
    lines.extend(f"• {hit['line']}" for hit in hits)
    lines.append(_localized(outro, lang))

    sources = [
        {
            "type": hit["type"],
            "id": hit["id"],
            "title": hit["title"],
            "url": hit["url"],
            "score": round(hit["score"], 2),
        }
        for hit in hits
    ]
    return {
        "answer": "\n".join(line for line in lines if line is not None),
        "sources": sources,
        "mode": "local",
        "lang": lang,
    }


def answer_local(question: str, lang: str = "fr") -> dict:
    return _answer_from_local_hits(question, _local_hits(question), lang=lang)


def ai_mode_available() -> bool:
    return embed_svc.is_configured()


def _refresh_product_facts(chunks: list[KnowledgeChunk]) -> list[str]:
    """Réinjecte prix/stock à jour pour les produits cités."""
    lines = []
    for chunk in chunks:
        if chunk.source_type != "product":
            lines.append(chunk.content)
            continue
        product = Product.query.filter_by(slug=chunk.source_id, is_active=True).first()
        if not product:
            lines.append(chunk.content)
            continue
        stock = "en stock" if product.in_stock() else "indisponible ou stock limité"
        if product.stock_qty is not None:
            stock = f"stock actuel: {product.stock_qty}"
        lines.append(
            f"{chunk.content}\n"
            f"[Prix actuel vérifié: {product.price_euros():.2f} € | {stock}]"
        )
    return lines


def retrieve(question: str, k: int | None = None) -> list[tuple[KnowledgeChunk, float]]:
    k = k or top_k()
    query_vec = embed_svc.embed_texts([question])[0]
    rows = KnowledgeChunk.query.filter(KnowledgeChunk.embedding_json.isnot(None)).all()
    scored: list[tuple[KnowledgeChunk, float]] = []
    for row in rows:
        vec = row.embedding()
        if not vec:
            continue
        score = embed_svc.cosine_similarity(query_vec, vec)
        scored.append((row, score))
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]


def _call_chat(messages: list[dict]) -> str:
    api_key = (os.environ.get("OPENAI_API_KEY") or "").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY manquant")

    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=chat_model(),
        messages=messages,
        temperature=0.3,
        max_tokens=600,
    )
    return (response.choices[0].message.content or "").strip()


def answer(question: str) -> dict:
    """
    Répond à une question client.
    Retourne {answer, sources, hint?, lang?}.
    """
    q = _normalize_question(question)
    lang = _detect_language(q)

    empty_prompt = {
        "fr": "Indiquez votre question concernant nos produits, livraisons ou services.",
        "en": "Please enter your question about our products, delivery or services.",
        "wo": "Bindal sa laaj ci produits, livraison walla services.",
    }
    if not q:
        return {"answer": _localized(empty_prompt, lang), "sources": [], "lang": lang}

    if not assistant_enabled():
        return {"answer": _localized(REFUSAL_NO_KEY, lang), "sources": [], "lang": lang}

    if _looks_like_order_tracking(q):
        return {
            "answer": _localized(REFUSAL_ORDER, lang),
            "sources": [],
            "hint": "order_tracking",
            "lang": lang,
        }

    if _looks_like_greeting(q):
        return {
            "answer": _localized(GREETING_REPLY, lang),
            "sources": [],
            "hint": "greeting",
            "mode": "courtesy",
            "lang": lang,
        }

    if _looks_like_thanks(q):
        return {
            "answer": _localized(THANKS_REPLY, lang),
            "sources": [],
            "hint": "thanks",
            "mode": "courtesy",
            "lang": lang,
        }

    if _looks_like_group_overview(q):
        result = _answer_group_overview()
        result["lang"] = lang
        if lang == "wo":
            result["answer"] = (
                "Groupe YOMBAL am na ay services yu bari. Yombal Market mooy boutique bi.\n\n"
                + result["answer"]
            )
        elif lang not in ("fr", "auto"):
            result["answer"] = (
                "Here is an overview of Groupe YOMBAL services. "
                "Yombal Market is the online shop.\n\n" + result["answer"]
            )
        return result

    ecosystem_slug = _detect_ecosystem_slug(q)
    if ecosystem_slug:
        result = _answer_ecosystem(ecosystem_slug)
        result["lang"] = lang
        if lang == "wo":
            result["answer"] = (
                "Sa laaj aju na ci service bii ci Groupe YOMBAL. "
                "Xoolal liens yi ngir kontine.\n\n" + result["answer"]
            )
        elif lang not in ("fr", "auto"):
            result["answer"] = (
                "Your request relates to this Groupe YOMBAL service. "
                "Please use the links below to continue.\n\n" + result["answer"]
            )
        return result

    if not embed_svc.is_configured():
        return answer_local(q, lang=lang)

    indexed = KnowledgeChunk.query.filter(KnowledgeChunk.embedding_json.isnot(None)).count()
    if indexed == 0:
        return answer_local(q, lang=lang)

    try:
        hits = retrieve(q)
    except Exception as exc:
        logger.exception("RAG retrieve: %s", exc)
        local = _local_hits(q)
        if local:
            return _answer_from_local_hits(q, local, lang=lang)
        return _answer_from_local_hits(q, [], prefix=REFUSAL_API_ERROR, lang=lang)

    if not hits:
        local = _local_hits(q)
        if local:
            return _answer_from_local_hits(q, local, lang=lang)
        return {
            "answer": _localized(EMPTY_CATALOGUE_REPLY, lang),
            "sources": [],
            "lang": lang,
        }

    context_blocks = _refresh_product_facts([chunk for chunk, _ in hits])
    context = "\n\n---\n\n".join(context_blocks)
    lang_name = _language_label(lang)
    user_prompt = (
        f"Langue détectée du client : {lang_name}. "
        f"Réponds obligatoirement en {lang_name}. "
        "Si la détection est incertaine, suis exactement la langue du message client.\n\n"
        f"Contexte boutique :\n\n{context}\n\nQuestion client : {q}"
    )

    try:
        reply = _call_chat(
            [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ]
        )
    except Exception as exc:
        logger.exception("RAG chat: %s", exc)
        local = _local_hits(q)
        if local:
            return _answer_from_local_hits(q, local, lang=lang)
        return _answer_from_local_hits(q, [], prefix=REFUSAL_API_ERROR, lang=lang)

    sources = []
    seen = set()
    for chunk, score in hits:
        key = (chunk.source_type, chunk.source_id)
        if key in seen:
            continue
        seen.add(key)
        src = chunk.as_source_dict()
        src["score"] = round(score, 4)
        sources.append(src)

    return {"answer": reply, "sources": sources, "mode": "ai", "lang": lang}
