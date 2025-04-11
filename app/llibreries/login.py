"""
Fitxer: login.py

Conté el sistema de registre i autenticació d’usuaris.
Inclou validació de credencials, gestió de sessions i interfície gràfica amb Tkinter.
"""

import hashlib
import os
import tkinter as tk
from tkinter import simpledialog, messagebox
from llibreries.bd import connectar_bd


def crear_taula_usuaris():
    """
    Crea l'esquema i la taula 'usuaris' si no existeixen.
    """
    conn = connectar_bd()
    cursor = conn.cursor()

    cursor.execute("CREATE SCHEMA IF NOT EXISTS public;")
    cursor.execute("SET search_path TO public;")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuaris (
            usuari TEXT PRIMARY KEY,
            contrasenya TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


def encriptar_contrasenya(contrasenya):
    """
    Encripta una contrasenya en SHA-256.

    Args:
        contrasenya (str): Contrasenya en text pla

    Returns:
        str: Contrasenya encriptada
    """
    return hashlib.sha256(contrasenya.encode()).hexdigest()


def registrar_usuari(usuari, contrasenya):
    """
    Registra un nou usuari si no existeix prèviament.

    Args:
        usuari (str): Nom d'usuari
        contrasenya (str): Contrasenya
    """
    conn = connectar_bd()
    cursor = conn.cursor()
    contrasenya_encriptada = encriptar_contrasenya(contrasenya)

    try:
        cursor.execute("INSERT INTO usuaris (usuari, contrasenya) VALUES (%s, %s)",
                       (usuari, contrasenya_encriptada))
        conn.commit()
        print("Usuari registrat correctament.")
        guardar_a_fitxer(usuari, contrasenya_encriptada)
        conn.close()
        return True
    except Exception as e:
        print("Aquest usuari ja existeix.")
        conn.close()
        return False


def iniciar_sessio(usuari, contrasenya):
    """
    Valida les credencials d’un usuari.

    Args:
        usuari (str): Nom d'usuari
        contrasenya (str): Contrasenya

    Returns:
        bool: True si les credencials són vàlides, False altrament
    """
    conn = connectar_bd()
    cursor = conn.cursor()
    contrasenya_encriptada = encriptar_contrasenya(contrasenya)

    cursor.execute("SELECT * FROM usuaris WHERE usuari = %s AND contrasenya = %s",
                   (usuari, contrasenya_encriptada))
    usuari_trobat = cursor.fetchone()
    conn.close()

    return bool(usuari_trobat)


def guardar_a_fitxer(usuari, contrasenya_encriptada):
    """
    Desa l’usuari i la seva contrasenya encriptada al fitxer registre.log.

    Args:
        usuari (str): Nom d’usuari
        contrasenya_encriptada (str): Contrasenya SHA-256
    """
    os.makedirs("app/logs", exist_ok=True)
    with open("app/logs/registre.log", "a") as f:
        f.write(f"{usuari},{contrasenya_encriptada}\n")


def iniciar_gui():
    """
    Obre una interfície gràfica per registrar o iniciar sessió amb Tkinter.
    """

    def registrar_gui():
        usuari = simpledialog.askstring("Registrar-se", "Usuari:")
        if usuari is None:
            return
        contrasenya = simpledialog.askstring("Registrar-se", "Contrasenya:", show="*")
        if contrasenya is None:
            return

        if registrar_usuari(usuari, contrasenya):
            messagebox.showinfo("Info", "Usuari registrat correctament.")
        else:
            messagebox.showerror("Error", "Aquest usuari ja existeix.")

    def login_gui():
        usuari = simpledialog.askstring("Login", "Usuari:")
        if usuari is None:
            return
        contrasenya = simpledialog.askstring("Login", "Contrasenya:", show="*")
        if contrasenya is None:
            return

        if iniciar_sessio(usuari, contrasenya):
            messagebox.showinfo("Benvingut", "Sessió iniciada correctament!")
        else:
            messagebox.showerror("Error", "Usuari o contrasenya incorrectes.")

    crear_taula_usuaris()

    root = tk.Tk()
    root.title("Gestor d'Hotels")
    root.geometry("300x150")

    tk.Label(root, text="Benvingut/da al gestor d'hotels", font=("Arial", 12)).pack(pady=10)
    tk.Button(root, text="Iniciar Sessió", width=20, command=login_gui).pack(pady=5)
    tk.Button(root, text="Registrar-se", width=20, command=registrar_gui).pack(pady=5)

    root.mainloop() 
 