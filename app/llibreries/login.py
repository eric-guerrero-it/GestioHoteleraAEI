"""
Fitxer: login.py

Conté el sistema de registre i autenticació d’usuaris.
Inclou validació de credencials, gestió de sessions i interfície gràfica amb Tkinter.
"""

import hashlib
import sqlite3
import os
import tkinter as tk
from tkinter import simpledialog, messagebox
from llibreries.bd import connectar_bd  # Importem la connexió amb SQLite

# ───────────────────────────────────────────────
# Crea la taula d’usuaris si no existeix
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

# ───────────────────────────────────────────────
# Encripta la contrasenya amb SHA-256
def encriptar_contrasenya(contrasenya):
    return hashlib.sha256(contrasenya.encode()).hexdigest()

# ───────────────────────────────────────────────
# Registra un nou usuari (si no existeix ja)
def registrar_usuari(usuari, contrasenya):
    conn = connectar_bd()
    cursor = conn.cursor()
    contrasenya_encriptada = encriptar_contrasenya(contrasenya)

    try:
        cursor.execute("INSERT INTO usuaris (usuari, contrasenya) VALUES (?, ?)",
                       (usuari, contrasenya_encriptada))
        conn.commit()
        print("Usuari registrat correctament.")
        guardar_a_fitxer(usuari, contrasenya_encriptada)  # Guardem també al fitxer local
    except sqlite3.IntegrityError:
        print("Aquest usuari ja existeix.")
    conn.close()

# ───────────────────────────────────────────────
# Inicia sessió verificant les credencials.
def iniciar_sessio(usuari, contrasenya):
    conn = connectar_bd()
    cursor = conn.cursor()
    contrasenya_encriptada = encriptar_contrasenya(contrasenya)

    cursor.execute("SELECT * FROM usuaris WHERE usuari = ? AND contrasenya = ?",
                   (usuari, contrasenya_encriptada))
    usuari_trobat = cursor.fetchone()
    conn.close()

    if usuari_trobat:
        print("Sessió iniciada correctament!")
        return True
    else:
        print("Usuari o contrasenya incorrectes.")
        return False

# ───────────────────────────────────────────────
# Desa les credencials (encriptades) a un fitxer local
def guardar_a_fitxer(usuari, contrasenya_encriptada):
    os.makedirs("app/logs", exist_ok=True)
    with open("app/logs/usuaris.txt", "a") as f:
        f.write(f"{usuari},{contrasenya_encriptada}\n")

# ───────────────────────────────────────────────
# INTERFÍCIE GRÀFICA AMB TKINTER
def iniciar_gui():
    # Demana dades per registrar un usuari des d’una finestra
    def registrar_gui():
        usuari = simpledialog.askstring("Registrar-se", "Usuari:")
        if usuari is None: return
        contrasenya = simpledialog.askstring("Registrar-se", "Contrasenya:", show="*")
        if contrasenya is None: return
        registrar_usuari(usuari, contrasenya)
        messagebox.showinfo("Info", "Usuari registrat correctament.")

    # Demana dades per iniciar sessió des d’una finestra
    def login_gui():
        usuari = simpledialog.askstring("Login", "Usuari:")
        if usuari is None: return
        contrasenya = simpledialog.askstring("Login", "Contrasenya:", show="*")
        if contrasenya is None: return
        if iniciar_sessio(usuari, contrasenya):
            messagebox.showinfo("Benvingut", "Sessió iniciada correctament!")
        else:
            messagebox.showerror("Error", "Usuari o contrasenya incorrectes.")

    crear_taula_usuaris()  # Ens assegurem que la taula existeixi

    # Disseny de la finestra
    root = tk.Tk()
    root.title("Gestor d'Hotels")
    root.geometry("300x150")

    tk.Label(root, text="Benvingut/da al gestor d'hotels", font=("Arial", 12)).pack(pady=10)
    tk.Button(root, text="Iniciar Sessió", width=20, command=login_gui).pack(pady=5)
    tk.Button(root, text="Registrar-se", width=20, command=registrar_gui).pack(pady=5)

    root.mainloop()
