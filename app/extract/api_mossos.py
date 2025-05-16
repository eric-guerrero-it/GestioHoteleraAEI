import sys
import os
import json
import requests
import tkinter as tk
from tkinter import messagebox
from datetime import date

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from llibreries.bd import connectar_bd


def exportar_reserves_format_mossos(data_inici, data_final):
    try:
        conn = connectar_bd()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                p.dni, p.nom, p.cognoms,
                r.dataInici, r.dataFinal,
                hab.numero, p.nacionalitat
            FROM reserva r
            JOIN reserva_habitacio rh ON r.idReserva = rh.idReserva
            JOIN habitacio hab ON rh.idHabitacio = hab.idHabitacio
            JOIN client c ON r.dniClient = c.dni
            JOIN persona p ON c.dni = p.dni
            WHERE r.dataInici BETWEEN %s AND %s
        """, (data_inici, data_final))

        registres = cur.fetchall()
        if not registres:
            return None, None, "No s'han trobat reserves en aquest període."

        dades = []
        for r in registres:
            dades.append({
                "dni": r[0],
                "nombre": r[1],
                "apellidos": r[2],
                "fecha_llegada": str(r[3]),
                "fecha_salida": str(r[4]),
                "habitación": str(r[5]),
                "nacionalidad": r[6]
            })

        carpeta_export = os.path.join(os.path.dirname(__file__), "..", "..", "export")
        os.makedirs(carpeta_export, exist_ok=True)

        nom_fitxer = f"mossos_{date.today()}.json"
        fitxer_json = os.path.join(carpeta_export, nom_fitxer)
        with open(fitxer_json, "w", encoding="utf-8") as f:
            json.dump(dades, f, indent=4, ensure_ascii=False)

        return fitxer_json, dades, f"Fitxer generat: {nom_fitxer}"
    except Exception as e:
        return None, None, f"Error: {str(e)}"
    finally:
        conn.close()


def enviar_a_api_local(fitxer_json):
    url = "http://apihotels.codeworks.es:7777/subir-json/"
    usuari = "usuario1"
    contrasenya = "contrasenya1"

    try:
        with open(fitxer_json, 'rb') as f:
            files = {'file': (os.path.basename(fitxer_json), f, 'application/json')}
            resposta = requests.post(url, files=files, auth=(usuari, contrasenya))

        if resposta.status_code == 200:
            return "OK", resposta.text
        else:   
            return f"ERROR {resposta.status_code}", resposta.text
    except Exception as e:
        return "ERROR", str(e)


def guardar_enviament(estat, dades_json):
    try:
        conn = connectar_bd()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO enviaments_api (estat, json_enviat)
            VALUES (%s, %s)
        """, (estat, json.dumps(dades_json, ensure_ascii=False)))
        conn.commit()
    except Exception as e:
        print("No s'ha pogut registrar a BD:", e)
    finally:
        conn.close()


def crear_interficie():
    finestra = tk.Tk()
    finestra.title("Enviar reserves a Mossos (format validat)")

    tk.Label(finestra, text="Data inici (YYYY-MM-DD):").pack()
    entry_inici = tk.Entry(finestra, width=20)
    entry_inici.pack(pady=2)

    tk.Label(finestra, text="Data final (YYYY-MM-DD):").pack()
    entry_final = tk.Entry(finestra, width=20)
    entry_final.pack(pady=2)

    def executar():
        data_inici = entry_inici.get().strip()
        data_final = entry_final.get().strip()

        if not data_inici or not data_final:
            messagebox.showwarning("Dates buides", "Has d’introduir dues dates.")
            return

        fitxer, dades, msg = exportar_reserves_format_mossos(data_inici, data_final)
        if not fitxer:
            messagebox.showinfo("Resultat", msg)
            return

        estat, resposta = enviar_a_api_local(fitxer)
        guardar_enviament(estat, dades)

        if estat == "OK":
            messagebox.showinfo("Enviament OK", "Fitxer enviat correctament.")
        else:
            messagebox.showerror("Error", f"{estat}\n{resposta}")

    tk.Button(finestra, text="Enviar reserves", command=executar, width=40).pack(pady=10)
    finestra.mainloop()


if __name__ == "__main__":
    crear_interficie()
