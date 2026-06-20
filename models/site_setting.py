# -*- coding: utf-8 -*-
from extensions import db


class SiteSetting(db.Model):
    __tablename__ = "site_settings"

    key = db.Column(db.String(80), primary_key=True)
    value = db.Column(db.Text, nullable=False, default="")


def get_setting(key, default=""):
    row = db.session.get(SiteSetting, key)
    return (row.value if row and row.value is not None else default) or default


def set_setting(key, value):
    row = db.session.get(SiteSetting, key)
    if not row:
        row = SiteSetting(key=key, value=value or "")
        db.session.add(row)
    else:
        row.value = value or ""
    db.session.commit()


def all_settings_dict():
    return {r.key: r.value for r in SiteSetting.query.all()}
