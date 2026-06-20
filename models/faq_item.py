# -*- coding: utf-8 -*-
from extensions import db


class FaqItem(db.Model):
    __tablename__ = "faq_items"

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    sort_order = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=True, server_default="1")

    def as_dict(self):
        return {"q": self.question, "a": self.answer}
