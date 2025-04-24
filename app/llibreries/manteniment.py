"""
Fitxer: manteniment.py

Gestió de les operacions bàsiques de funcionament de l’hotel com el check-in, check-out, reserves,
consultes de dades i validació mitjançant triggers o funcions en PL/pgSQL.
"""

import tkinter as tk
from llibreries.bd import connectar_bd


def obrir_finestra_alta_modificacio_hotels():
    """
    Obre una finestra per donar d'alta o modificar dades d'un hotel.
    """
    finestra = tk.Toplevel()
    finestra.title("Alta / Modificació d'Hotels")
    finestra.geometry("500x500")

    camps = {
        "ID (per modificar)": tk.Entry(finestra),
        "Nom": tk.Entry(finestra),
        "Estrelles": tk.Entry(finestra),
        "Adreça": tk.Entry(finestra),
        "Població": tk.Entry(finestra),
        "Web": tk.Entry(finestra),
        "Telèfon": tk.Entry(finestra),
    }

    for etiqueta, entrada in camps.items():
        tk.Label(finestra, text=etiqueta + ":").pack()
        entrada.pack()

    def guardar_hotel():
        try:
            idhotel = camps["ID (per modificar)"].get().strip()
            nom = camps["Nom"].get().strip()
            estrelles = camps["Estrelles"].get().strip()
            adreca = camps["Adreça"].get().strip()
            poblacio = camps["Població"].get().strip()
            web = camps["Web"].get().strip()
            telefon = camps["Telèfon"].get().strip()

            if not nom:
                tk.messagebox.showerror("Error", "El camp 'Nom' és obligatori.")
                return

            conn = connectar_bd()
            cursor = conn.cursor()

            if idhotel:  # Modificació
                cursor.execute("""
                    UPDATE hotel SET nom = %s, estrelles = %s, adreca = %s,
                    poblacio = %s, web = %s, telefon = %s WHERE idhotel = %s
                """, (nom, estrelles or None, adreca, poblacio, web, telefon, idhotel))
                missatge = "Hotel modificat correctament."
            else:  # Alta
                cursor.execute("""
                    INSERT INTO hotel (idhotel, nom, estrelles, adreca, poblacio, web, telefon)
                    VALUES (DEFAULT, %s, %s, %s, %s, %s, %s)
                """, (nom, estrelles or None, adreca, poblacio, web, telefon))
                missatge = "Hotel donat d'alta correctament."

            conn.commit()
            conn.close()
            tk.messagebox.showinfo("Éxit", missatge)
            finestra.destroy()

        except Exception as e:
            tk.messagebox.showerror("Error", f"S'ha produït un error:\n{e}")

    tk.Button(finestra, text="Desar", command=guardar_hotel).pack(pady=15)

def obrir_finestra_alta_personal():
    """
    Obre una finestra per donar d'alta nou personal de qualsevol classe.
    """
    finestra = tk.Toplevel()
    finestra.title("Alta de Personal")
    finestra.geometry("400x500")

    labels = ["DNI", "Nom", "Cognoms", "Telèfon", "Adreça", "Data Naixement (YYYY-MM-DD)"]
    entrades = {}

    for label in labels:
        tk.Label(finestra, text=label).pack()
        entry = tk.Entry(finestra)
        entry.pack()
        entrades[label] = entry

    tk.Label(finestra, text="Tipus Treballador").pack()
    tipus_var = tk.StringVar(value="recepció")
    tipus_menu = tk.OptionMenu(finestra, tipus_var, "recepció", "cuina", "altres")
    tipus_menu.pack()

    def guardar_personal():
        dni = entrades["DNI"].get().strip()
        nom = entrades["Nom"].get().strip()
        cognoms = entrades["Cognoms"].get().strip()
        telefon = entrades["Telèfon"].get().strip()
        adreca = entrades["Adreça"].get().strip()
        naixement = entrades["Data Naixement (YYYY-MM-DD)"].get().strip()
        tipus = tipus_var.get()

        try:
            conn = connectar_bd()
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO persona (dni, nom, cognoms, telefon, adreca, dataNaixement)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (dni, nom, cognoms, telefon, adreca, naixement))

            cursor.execute('''
                INSERT INTO treballador (dni, tipusTreballador)
                VALUES (%s, %s)
            ''', (dni, tipus))

            if tipus == "recepció":
                cursor.execute("INSERT INTO recepcio (dni, anysExperiencia) VALUES (%s, %s)", (dni, 0))
            elif tipus == "cuina":
                cursor.execute("INSERT INTO cuina (dni, categoria) VALUES (%s, 'ajudant de cuina')", (dni,))
            elif tipus == "altres":
                cursor.execute("INSERT INTO restapersonal (dni) VALUES (%s)", (dni,))

            conn.commit()
            tk.messagebox.showinfo("Èxit", "Treballador donat d’alta correctament.")
            finestra.destroy()
        except Exception as e:
            conn.rollback()
            tk.messagebox.showerror("Error", f"Error en registrar el treballador: {e}")
        finally:
            conn.close()

    tk.Button(finestra, text="Desar", command=guardar_personal).pack(pady=10)    

def obrir_finestra_nova_reserva():
    """
    Obre una finestra per donar d'alta una nova reserva.
    """
    finestra = tk.Toplevel()
    finestra.title("Nova Reserva")
    finestra.geometry("400x400")

    # Camps
    labels = {
        "Data Inici (YYYY-MM-DD)": tk.Entry(finestra),
        "Data Final (YYYY-MM-DD)": tk.Entry(finestra),
        "ID Hotel": tk.Entry(finestra),
        "DNI Client": tk.Entry(finestra),
    }

    for text, entrada in labels.items():
        tk.Label(finestra, text=text).pack()
        entrada.pack()

    def guardar_reserva():
        data_inici = labels["Data Inici (YYYY-MM-DD)"].get().strip()
        data_final = labels["Data Final (YYYY-MM-DD)"].get().strip()
        idhotel = labels["ID Hotel"].get().strip()
        dni = labels["DNI Client"].get().strip()

        try:
            conn = connectar_bd()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO reserva (dataInici, dataFinal, idHotel, dniClient)
                VALUES (%s, %s, %s, %s)
            """, (data_inici, data_final, idhotel, dni))

            conn.commit()
            tk.messagebox.showinfo("Èxit", "Reserva creada correctament.")
            finestra.destroy()
        except Exception as e:
            conn.rollback()
            tk.messagebox.showerror("Error", f"No s'ha pogut crear la reserva:\n{e}")
        finally:
            conn.close()

    tk.Button(finestra, text="Confirmar Reserva", command=guardar_reserva).pack(pady=20)

def obrir_finestra_checkin():
    """
    Obre una finestra per fer el check-in d’una reserva (canvia dataInici a la data actual).
    """
    finestra = tk.Toplevel()
    finestra.title("Check-in")
    finestra.geometry("350x200")

    tk.Label(finestra, text="ID de la reserva:").pack(pady=5)
    entrada = tk.Entry(finestra)
    entrada.pack()

    def fer_checkin():
        idreserva = entrada.get().strip()
        if not idreserva:
            tk.messagebox.showerror("Error", "Has d'introduir un ID de reserva.")
            return
        try:
            conn = connectar_bd()
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM reserva WHERE idreserva = %s", (idreserva,))
            if cursor.fetchone() is None:
                tk.messagebox.showerror("Error", "No existeix cap reserva amb aquest ID.")
                conn.close()
                return

            cursor.execute("UPDATE reserva SET dataInici = CURRENT_DATE WHERE idreserva = %s", (idreserva,))
            conn.commit()
            conn.close()
            tk.messagebox.showinfo("Èxit", "Check-in fet correctament.")
            finestra.destroy()
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error en fer el check-in:\n{e}")

    tk.Button(finestra, text="Confirmar Check-in", command=fer_checkin).pack(pady=15)

def obrir_finestra_checkout():
    """
    Obre una finestra per fer el check-out d’una reserva (actualitza dataFinal a la data actual).
    """
    finestra = tk.Toplevel()
    finestra.title("Check-out")
    finestra.geometry("350x200")

    tk.Label(finestra, text="ID de la reserva:").pack(pady=5)
    entrada = tk.Entry(finestra)
    entrada.pack()

    def fer_checkout():
        idreserva = entrada.get().strip()
        if not idreserva:
            tk.messagebox.showerror("Error", "Has d'introduir un ID de reserva.")
            return
        try:
            conn = connectar_bd()
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM reserva WHERE idreserva = %s", (idreserva,))
            if cursor.fetchone() is None:
                tk.messagebox.showerror("Error", "No existeix cap reserva amb aquest ID.")
                conn.close()
                return

            cursor.execute("UPDATE reserva SET dataFinal = CURRENT_DATE WHERE idreserva = %s", (idreserva,))
            conn.commit()
            conn.close()
            tk.messagebox.showinfo("Èxit", "Check-out fet correctament.")
            finestra.destroy()
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error en fer el check-out:\n{e}")

    tk.Button(finestra, text="Confirmar Check-out", command=fer_checkout).pack(pady=15)


def obrir_finestra_manteniment():
    """
    Obre la finestra principal de manteniment amb les opcions de gestió i consultes.
    """
    root = tk.Tk()
    root.title("Gestió de Manteniment")
    root.geometry("500x700")

    tk.Label(root, text="Mòdul de Manteniment", font=("Arial", 16)).pack(pady=10)

    # ───────────────────────────────
    # GESTIÓ DE DADES
    tk.Label(root, text="Gestió bàsica", font=("Arial", 12, "bold")).pack(pady=5)

    tk.Button(root, text="Alta / Modificació d'Hotels", width=40, command=obrir_finestra_alta_modificacio_hotels).pack(pady=3)
    tk.Button(root, text="Alta de Personal", width=40, command=obrir_finestra_alta_personal).pack(pady=3)
    tk.Button(root, text="Nova Reserva", width=40, command=obrir_finestra_nova_reserva).pack(pady=3)
    tk.Button(root, text="Check-in", width=40, command=obrir_finestra_checkin).pack(pady=3)
    tk.Button(root, text="Check-out", width=40, command=obrir_finestra_checkout).pack(pady=3)

    # ───────────────────────────────
    # CONSULTES DADES
    tk.Label(root, text="Consultes d'informació", font=("Arial", 12, "bold")).pack(pady=10)

    tk.Button(root, text="Reserves per dia (hora, client, habitació)", width=50).pack(pady=2)
    tk.Button(root, text="Empleats per hotel (director, gerent, funció)", width=50).pack(pady=2)
    tk.Button(root, text="Recepció: idiomes i nivell", width=50).pack(pady=2)
    tk.Button(root, text="Cuina: categoria i revisor", width=50).pack(pady=2)
    tk.Button(root, text="Habitacions per hotel i característiques", width=50).pack(pady=2)
    tk.Button(root, text="Reserves per hotel (dates, clients)", width=50).pack(pady=2)
    tk.Button(root, text="Serveis que ofereix l'hotel", width=50).pack(pady=2)
    tk.Button(root, text="Sol·licituds de serveis per client", width=50).pack(pady=2)

    # ───────────────────────────────
    # TRIGGERS I VALIDACIONS (PLPGSQL)
    tk.Label(root, text="Gestió i validació amb PL/pgSQL", font=("Arial", 12, "bold")).pack(pady=10)

    tk.Button(root, text="Executar procediments de validació", width=40).pack(pady=2)
    tk.Button(root, text="Simular trigger de control", width=40).pack(pady=2)

    root.mainloop()
