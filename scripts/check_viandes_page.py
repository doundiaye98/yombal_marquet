# -*- coding: utf-8 -*-
from app import app
import re
from collections import Counter

c = app.test_client()
for url in (
    "/boutique?categorie=viandes",
    "/boutique?categorie=viandes&famille=boeuf",
    "/boutique?categorie=viandes&type=alimentaire",
    "/boutique?type=alimentaire",
):
    r = c.get(url)
    html = r.data.decode("utf-8", errors="replace")
    titles = re.findall(
        r'class="boutique-card__title"[\s\S]*?<a[^>]*>\s*([^<]+?)\s*</a>',
        html,
    )
    bad = [
        t
        for t in titles
        if any(
            k in t.lower()
            for k in (
                "mixeur",
                "bouilloire",
                "aspirateur",
                "iphone",
                "lampe",
                "ampoule",
                "batterie",
                "casque",
                "valise",
                "enceinte",
                "micro-ondes",
                "friteuse",
                "fer à",
                "clavier",
                "samsung",
                "chargeur",
                "tablette",
                "t-shirt",
                "baskets",
            )
        )
    ]
    cats = re.findall(r'class="boutique-card__cat"[^>]*>\s*([^<]+?)\s*<', html)
    cat_counts = Counter([re.sub(r"\s+", " ", x.strip()) for x in cats])
    print("URL", url, "status", r.status_code, "cards", len(titles), "bad", len(bad))
    if bad:
        for b in bad[:10]:
            print("  BAD", b)
    print("  cats", cat_counts.most_common(5))
