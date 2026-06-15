#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Initialise ou met à jour la base : python scripts/init_db.py"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import app
from database import ensure_database


def main():
    with app.app_context():
        ensure_database(app)
    print("Base de données prête (migrations + catalogue si vide).")


if __name__ == "__main__":
    main()
