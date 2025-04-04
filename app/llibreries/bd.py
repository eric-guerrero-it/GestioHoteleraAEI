# app/llibreries/bd.py

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../../usuaris.db")

def connectar():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuaris (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT UNIQUE NOT NULL,
            contrasenya_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
