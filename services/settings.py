# -*- coding: utf-8 -*-
import os

from models.site_setting import all_settings_dict

DEFAULTS = {
    "shop_name": "Yombal Marché",
    "shop_contact_email": "compta@universdiasporas.com",
    "shop_address_line1": "Place du marché",
    "shop_address_line2": "Code postal · Ville",
    "shop_hours_weekday": "Lun – ven · 8h30 – 13h30 · 15h30 – 19h30",
    "shop_hours_saturday": "Samedi · 8h – 19h30",
    "shop_hours_sunday": "Dimanche · 9h – 13h",
    "shop_phone": "",
    "shop_delivery_days_min": "3",
    "shop_delivery_days_max": "7",
}


def shop_settings():
    stored = all_settings_dict()
    out = dict(DEFAULTS)
    out.update(stored)
    out["shop_contact_email"] = (
        stored.get("shop_contact_email")
        or (os.environ.get("CONTACT_EMAIL") or "").strip()
        or "compta@universdiasporas.com"
    )
    return out
