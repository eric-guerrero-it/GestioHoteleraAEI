"""
Fitxer: export_xml.py

Exporta reserves en format XML i mostra un rànquing d'hotels amb més reserves.
Inclou una interfície gràfica amb Tkinter i filtres per dates.
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import psycopg2
import xml.etree.ElementTree as ET
from datetime import date
from llibreries.bd import connectar_bd


def exportar_reserves_xml(data_inici, data_final, nom_grup="AEI"):
    try:
        conn = connectar_bd()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                r.idReserva,
                h.idHotel,  
                r.dataInici,
                r.dataFinal,
                p.dni,
                p.nom,
                p.cognoms
            FROM
                reserva r
            JOIN hotel h ON r.idHotel = h.idHotel
            JOIN client c ON r.dniClient = c.dni
            JOIN persona p ON c.dni = p.dni
            WHERE r.dataInici >= %s AND r.dataFinal <= %s
            ORDER BY r.dataInici
        """, (data_inici, data_final))

        reserves = cursor.fetchall()

        if not reserves:
            messagebox.showinfo("Exportació", "No s'han trobat reserves dins del rang indicat.")
            return

        arrel = ET.Element("reserves")

        for r in reserves:
            reserva = ET.SubElement(arrel, "reserva", id=str(r[0]))
            ET.SubElement(reserva, "hotel").text = str(r[1])
            ET.SubElement(reserva, "dataInici").text = str(r[2])
            ET.SubElement(reserva, "dataFinal").text = str(r[3])

            client = ET.SubElement(reserva, "client")
            ET.SubElement(client, "dni").text = r[4]
            ET.SubElement(client, "nom").text = r[5]
            ET.SubElement(client, "cognoms").text = r[6]

        arbre = ET.ElementTree(arrel)
        carpeta_export = os.path.join(os.path.dirname(__file__), "..", "..", "export")
        os.makedirs(carpeta_export, exist_ok=True)

        nom_fitxer = os.path.join(carpeta_export, f"{nom_grup}_{date.today()}.xml")
        ET.indent(arbre, space="\t", level=0)
        arbre.write(nom_fitxer, encoding="utf-8", xml_declaration=True)

        messagebox.showinfo("Exportació completada", f"Fitxer guardat a:\n{nom_fitxer}")

    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()


def mostrar_ranking_hotels():
    try:
        conn = connectar_bd()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT h.nom, COUNT(*) AS total_reserves
            FROM reserva r
            JOIN hotel h ON r.idHotel = h.idHotel
            GROUP BY h.nom
            ORDER BY total_reserves DESC
        """)

        resultats = cursor.fetchall()
        finestra_ranking = tk.Toplevel()
        finestra_ranking.title("Rànquing d'Hotels amb més visites")

        tree = ttk.Treeview(finestra_ranking, columns=("Hotel", "Reserves"), show="headings")
        tree.heading("Hotel", text="Nom de l'Hotel")
        tree.heading("Reserves", text="Nombre de Reserves")
        tree.pack(fill="both", expand=True)

        for fila in resultats:
            tree.insert("", "end", values=fila)

    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()


def crear_interficie():
    finestra = tk.Tk()
    finestra.title("Gestió de Reserves - Espamus+")

    tk.Label(finestra, text="Data inici (YYYY-MM-DD):").pack()
    entry_inici = tk.Entry(finestra, width=20)
    entry_inici.pack(pady=2)

    tk.Label(finestra, text="Data final (YYYY-MM-DD):").pack()
    entry_final = tk.Entry(finestra, width=20)
    entry_final.pack(pady=2)

    def exportar_amb_dates():
        data_inici = entry_inici.get().strip()
        data_final = entry_final.get().strip()

        if not data_inici or not data_final:
            messagebox.showwarning("Camp buit", "Has d'introduir les dues dates.")
            return

        exportar_reserves_xml(data_inici, data_final)

    boto_exportar = tk.Button(finestra, text="Exportar reserves entre dates", command=exportar_amb_dates, width=40)
    boto_exportar.pack(pady=10)

    boto_ranking = tk.Button(finestra, text="Mostrar rànquing d'hotels amb més visites", command=mostrar_ranking_hotels, width=40)
    boto_ranking.pack(pady=10)

    finestra.mainloop()


if __name__ == "__main__":
    crear_interficie()
