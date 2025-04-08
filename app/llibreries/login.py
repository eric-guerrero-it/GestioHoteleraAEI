"""
Fitxer: login.py

Conté el sistema de registre i autenticació d’usuaris.
Inclou validació de credencials i gestió de sessions.
"""

import hashlib
import sqlite3
from llibreries.bd import connectar_bd
import os


def crear_taula_usuaris():
    conn = connectar_bd()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuaris (
            usuari TEXT PRIMARY KEY,
            contrasenya TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def encriptar_contrasenya(contrasenya):
    return hashlib.sha256(contrasenya.encode()).hexdigest()

def registrar_usuari(usuari, contrasenya):
    conn = connectar_bd()
    cursor = conn.cursor()

    contrasenya_encriptada = encriptar_contrasenya(contrasenya)
    try:
        cursor.execute("INSERT INTO usuaris (usuari, contrasenya) VALUES (?, ?)", (usuari, contrasenya_encriptada))
        conn.commit()
        print("Usuari registrat correctament.")
        guardar_a_fitxer(usuari, contrasenya_encriptada)
    except sqlite3.IntegrityError:
        print("Aquest usuari ja existeix.")
    conn.close()

def iniciar_sessio(usuari, contrasenya):
    conn = connectar_bd()
    cursor = conn.cursor()
    contrasenya_encriptada = encriptar_contrasenya(contrasenya)

    cursor.execute("SELECT * FROM usuaris WHERE usuari = ? AND contrasenya = ?", (usuari, contrasenya_encriptada))
    usuari_trobat = cursor.fetchone()

    conn.close()

    if usuari_trobat:
        print("Sessió iniciada correctament!")
        return True
    else:
        print("Usuari o contrasenya incorrectes.")
        return False

def guardar_a_fitxer(usuari, contrasenya_encriptada):

    with open("app/logs/usuaris.txt", "a") as f:
        f.write(f"{usuari},{contrasenya_encriptada}\n")

"""
Fitxer: login.py

Conté el sistema de registre i autenticació d’usuaris.
Inclou validació de credencials i gestió de sessions.
"""
