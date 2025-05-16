"""
Fitxer: inform.py

Aquest script implementa la interfície gràfica d’Espamus+ amb Tkinter per consultar 
i mostrar informes de gestió hotelera, utilitzant dades emmagatzemades en PostgreSQL.

Funcionalitats principals:
- Connexió segura a la base de dades amb psycopg2.
- Visualització en format taula (ASCII) mitjançant `tabulate`.
- 4 informes disponibles:
  1. Nombre d’habitacions i personal per hotel.
  2. Personal assignat a un hotel.
  3. Check-in / check-out en una data concreta.
  4. Rànquing d’hotels per nombre de reserves.

Llibreries requerides:
- tkinter → Interfície d’usuari
- tabulate → pip install tabulate
- psycopg2 → pip install psycopg2-binary

Pensat per facilitar el manteniment futur i la col·laboració entre desenvolupadors.
Inclou tota la configuració de la GUI: camps d’entrada, botons i àrea de resultats.
"""

import tkinter as tk
from tabulate import tabulate
import psycopg2
from tkinter import messagebox

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from llibreries.bd import connectar_bd

def mostrar_informe_simulat():
    conn = connectar_bd()
    if conn is None:
        return

    result_display.delete(1.0, tk.END)
    result_display.insert(tk.END, "=== Informes ===\n")

    hotel_id = entry_hotel_id.get().strip()
    data_inici = entry_data.get().strip()

    if informe_var.get() == 4:
        hotel_id = ""
        data_inici = ""

    try:
        cursor = conn.cursor()

        if informe_var.get() == 1:
            query = """
            SELECT h.nom AS hotel,
                    COUNT(DISTINCT hab.idHabitacio) AS num_habitacions,
                    COUNT(DISTINCT t.dnitreballador) AS num_personal
            FROM HOTEL h
            LEFT JOIN HABITACIO hab ON h.idHotel = hab.idHotel
            LEFT JOIN TREBALLA t ON h.idHotel = t.idHotel
            WHERE h.idHotel = %s
            GROUP BY h.nom;
            """
            cursor.execute(query, (hotel_id,))
            headers = ["Hotel", "Nº Habitacions", "Nº Personal"]

        elif informe_var.get() == 2:
            query = """
            SELECT p.nom || ' ' || p.cognoms AS treballador,
                    h.nom AS hotel,
                    tr.tipusTreballador
            FROM HOTEL h
            JOIN TREBALLA t ON h.idHotel = t.idHotel
            JOIN TREBALLADOR tr ON t.dnitreballador = tr.DNI
            JOIN PERSONA p ON p.DNI = tr.DNI
            WHERE h.idHotel = %s
            ORDER BY t.dnitreballador;
            """
            cursor.execute(query, (hotel_id,))
            headers = ["Treballador", "Hotel", "Tipus"]

        elif informe_var.get() == 3:
            if hotel_id == "" or data_inici == "":
                messagebox.showwarning("Atenció", "Cal introduir ID de l'hotel i data.")
                return
            query = """
            SELECT r.idReserva,
                    p.nom || ' ' || p.cognoms AS client,
                    r.dataInici AS arribada,
                    r.dataFinal AS sortida
            FROM RESERVA r
            JOIN CLIENT c ON r.dniclient = c.DNI
            JOIN PERSONA p ON c.DNI = p.DNI
            WHERE r.idHotel = %s
            AND r.dataInici = %s
            ORDER BY r.dataInici;
            """
            cursor.execute(query, (hotel_id, data_inici))
            headers = ["ID Reserva", "Client", "Arribada", "Sortida"]

        elif informe_var.get() == 4:
            query = """
            SELECT h.nom AS hotel,
                   COUNT(r.idReserva) AS visites
            FROM HOTEL h
            LEFT JOIN RESERVA r ON h.idHotel = r.idHotel
            GROUP BY h.nom
            ORDER BY visites DESC;
            """
            cursor.execute(query)
            headers = ["Hotel", "Nº Visites"]

        else:
            result_display.insert(tk.END, "Cap informe seleccionat.")
            return

        result = cursor.fetchall()
        if not result:
            result_display.insert(tk.END, "No hi ha dades per mostrar.")
        else:
            taula = tabulate(result, headers=headers, tablefmt="grid")
            result_display.insert(tk.END, taula)

        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"Error en executar la consulta: {e}")

# Tkinter
root = tk.Tk()
root.title("Espamus+ | Consultes i Informes")
root.geometry("750x620")
root.configure(bg="white")

frame_informe = tk.LabelFrame(root, text="Selecciona l'informe", font=("Arial", 10, "bold"), bg="white", padx=10, pady=10)
frame_informe.grid(row=0, column=0, padx=15, pady=10, sticky="we")

informe_var = tk.IntVar(value=1)
tk.Radiobutton(frame_informe, text="1. Habitacions i personal", variable=informe_var, value=1, bg="white", anchor="w").grid(row=0, column=0, sticky="w")
tk.Radiobutton(frame_informe, text="2. Personal per hotel", variable=informe_var, value=2, bg="white", anchor="w").grid(row=1, column=0, sticky="w")
tk.Radiobutton(frame_informe, text="3. Arribades i sortides", variable=informe_var, value=3, bg="white", anchor="w").grid(row=2, column=0, sticky="w")
tk.Radiobutton(frame_informe, text="4. Rànquing d'hotels amb més visites", variable=informe_var, value=4, bg="white", anchor="w").grid(row=3, column=0, sticky="w")

frame_dades = tk.LabelFrame(root, text="Dades d'entrada", font=("Arial", 10, "bold"), bg="white", padx=10, pady=10)
frame_dades.grid(row=1, column=0, padx=15, pady=5, sticky="we")

tk.Label(frame_dades, text="ID de l'hotel:", bg="white").grid(row=0, column=0, sticky="e", padx=5, pady=5)
entry_hotel_id = tk.Entry(frame_dades, width=25)
entry_hotel_id.grid(row=0, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_dades, text="Data (YYYY-MM-DD):", bg="white").grid(row=1, column=0, sticky="e", padx=5, pady=5)
entry_data = tk.Entry(frame_dades, width=25)
entry_data.grid(row=1, column=1, padx=5, pady=5, sticky="w")

btn_mostrar = tk.Button(root, text="Mostrar informe", command=mostrar_informe_simulat, bg="#d6eaff", font=("Arial", 10, "bold"), width=20)
btn_mostrar.grid(row=2, column=0, pady=10)

frame_resultats = tk.LabelFrame(root, text="Resultat", font=("Arial", 10, "bold"), bg="white", padx=10, pady=10)
frame_resultats.grid(row=3, column=0, padx=15, pady=5, sticky="we")

result_display = tk.Text(frame_resultats, height=15, width=85, font=("Courier", 10))
result_display.pack()

root.mainloop()
