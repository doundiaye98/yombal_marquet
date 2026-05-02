# -*- coding: utf-8 -*-
"""Point d’entrée WSGI pour Waitress, Gunicorn, mod_wsgi, etc."""

from app import app as application

__all__ = ["application"]
