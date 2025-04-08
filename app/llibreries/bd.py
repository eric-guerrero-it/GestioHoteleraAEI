"""
Fitxer: bd.py

Conté les funcions per establir connexió amb la base de dades PostgreSQL.
Inclou mètodes per executar consultes, inserir dades i gestionar errors de connexió.
"""

# app/llibreries/bd.py
import sqlite3

def connectar_bd():
    conn = sqlite3.connect('base_dades.db')
    return conn
