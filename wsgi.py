# -*- coding: utf-8 -*-
"""Point d’entrée WSGI pour Waitress, Gunicorn, mod_wsgi, etc."""

import os

from dotenv import load_dotenv

_ROOT = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(_ROOT, ".env"))

from app import app as application

__all__ = ["application"]
