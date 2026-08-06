# -*- coding: utf-8 -*-
"""Exporte products (+ producers) depuis SQLite Flask vers SQL MySQL.
Usage: python php/scripts/export_sqlite_to_mysql.py > php/sql/products_seed.sql
"""
from __future__ import annotations

import os
import sqlite3
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DB = os.path.join(ROOT, "instance", "yombal.sqlite")


def esc(v):
    if v is None:
        return "NULL"
    if isinstance(v, (int, float)):
        return str(int(v) if isinstance(v, bool) else v)
    if isinstance(v, bytes):
        v = v.decode("utf-8", "replace")
    s = str(v).replace("\\", "\\\\").replace("'", "''")
    return "'" + s + "'"


def main():
    out_path = os.path.join(ROOT, "php", "sql", "products_seed.sql")
    if not os.path.isfile(DB):
        print(f"-- DB introuvable: {DB}", file=sys.stderr)
        sys.exit(1)
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    lines: list[str] = ["SET NAMES utf8mb4;", "SET FOREIGN_KEY_CHECKS=0;"]

    try:
        prod_rows = cur.execute("SELECT * FROM producers").fetchall()
        for r in prod_rows:
            cols = list(r.keys())
            vals = ", ".join(esc(r[c]) for c in cols)
            lines.append(
                f"INSERT INTO producers ({', '.join('`'+c+'`' for c in cols)}) VALUES ({vals}) "
                f"ON DUPLICATE KEY UPDATE name=VALUES(name);"
            )
    except sqlite3.OperationalError:
        lines.append("-- table producers absente")

    rows = cur.execute("SELECT * FROM products").fetchall()
    for r in rows:
        cols = list(r.keys())
        vals = ", ".join(esc(r[c]) for c in cols)
        lines.append(
            f"INSERT INTO products ({', '.join('`'+c+'`' for c in cols)}) VALUES ({vals}) "
            f"ON DUPLICATE KEY UPDATE name=VALUES(name), price_cents=VALUES(price_cents), "
            f"is_active=VALUES(is_active), image=VALUES(image);"
        )

    try:
        img_rows = cur.execute("SELECT * FROM product_images").fetchall()
        for r in img_rows:
            cols = list(r.keys())
            vals = ", ".join(esc(r[c]) for c in cols)
            lines.append(
                f"INSERT INTO product_images ({', '.join('`'+c+'`' for c in cols)}) VALUES ({vals});"
            )
    except sqlite3.OperationalError:
        pass

    lines.append("SET FOREIGN_KEY_CHECKS=1;")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"OK → {out_path} ({len(rows)} produits)", file=sys.stderr)


if __name__ == "__main__":
    main()
