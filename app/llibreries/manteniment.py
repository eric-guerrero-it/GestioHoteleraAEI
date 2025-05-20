"""
Fitxer: manteniment.py

Gestió de les operacions bàsiques de funcionament de l’hotel com el check-in, check-out, reserves,
consultes de dades i validació mitjançant triggers o funcions en PL/pgSQL.
"""

import tkinter as tk
from tkinter import messagebox
import threading

from dummy_data.generar_dades import generar_hotels, generar_clients, generar_treballadors, generar_activitats, generar_reserves, crear_indexos, generar_habitacions
from dummy_data.eliminar_dades import eliminar_dades_dummy
from llibreries.bd import connectar_bd

import subprocess
import os


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

# ───────────────────────────────
# BLOQUEIG PER EVITAR DUES EXECUCIONS EN PARAL·LEL
# Variables globals per bloquejar accions concurrents
generant_dades = False
eliminant_dades = False

def executar_generar_dades_dummy():
    global generant_dades, eliminant_dades
    if generant_dades:
        messagebox.showwarning("Atenció", "Ja s'estan generant dades dummy.")
        return
    if eliminant_dades:
        messagebox.showwarning("Atenció", "No es poden generar dades mentre s'estan eliminant.")
        return

    def executar():
        global generant_dades
        generant_dades = True
        try:
            messagebox.showinfo("Generació", "S'estan generant les dades dummy. Pot trigar uns minuts.")
            generar_hotels(100)
            generar_clients(50000)
            generar_treballadors(10000)
            generar_activitats(150000)
            generar_habitacions(15)
            generar_reserves(100000)
            crear_indexos()
            messagebox.showinfo("Finalitzat", "Dades dummy generades correctament.")
        except Exception as e:
            messagebox.showerror("Error", f"Error en generar les dades:\n{e}")
        finally:
            generant_dades = False

    threading.Thread(target=executar, daemon=True).start()

def executar_eliminar_dades_dummy():
    global generant_dades, eliminant_dades
    if eliminant_dades:
        messagebox.showwarning("Atenció", "Ja s'estan eliminant dades.")
        return
    if generant_dades:
        messagebox.showwarning("Atenció", "No es poden eliminar dades mentre s'estan generant.")
        return

    resposta = messagebox.askyesno("Confirmació", "Estàs segur que vols eliminar totes les dades dummy?")
    if resposta:
        def executar():
            global eliminant_dades
            eliminant_dades = True
            try:
                messagebox.showinfo("Eliminació", "S'estan eliminant les dades dummy...")
                eliminar_dades_dummy()
                messagebox.showinfo("Eliminació finalitzada", "Dades dummy eliminades correctament.")
            except Exception as e:
                messagebox.showerror("Error", f"Error eliminant les dades:\n{e}")
            finally:
                eliminant_dades = False

        threading.Thread(target=executar, daemon=True).start()
    else:
        messagebox.showinfo("Cancel·lat", "Eliminació cancel·lada.")


def obrir_finestra_reserves_per_dia():
    """
    Obre una finestra per consultar les reserves per dia, amb l'hora, client i habitació.
    """
    finestra = tk.Toplevel()
    finestra.title("Reserves per Dia")
    finestra.geometry("500x400")

    tk.Label(finestra, text="Data (YYYY-MM-DD):").pack(pady=10)
    entrada_data = tk.Entry(finestra)
    entrada_data.pack(pady=10)

    def consultar_reserves():
        dia = entrada_data.get().strip()
        if not dia:
            tk.messagebox.showerror("Error", "Has d'introduir una data.")
            return
        try:
            conn = connectar_bd()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    r.idReserva,
                    r.dataInici,
                    r.dataFinal,
                    p.dni AS client_dni,
                    p.nom AS client_nom,
                    h.numero AS habitacio_numero
                FROM
                    reserva r
                JOIN reserva_habitacio rh ON r.idReserva = rh.idReserva
                JOIN habitacio h ON rh.idHabitacio = h.idHabitacio
                JOIN client c ON r.dniClient = c.dni
                JOIN persona p ON c.dni = p.dni
                WHERE
                    %s BETWEEN r.dataInici AND r.dataFinal 
                ORDER BY
                    r.dataInici;
            """, (dia,))

            reserves = cursor.fetchall()
            if not reserves:
                tk.messagebox.showinfo("Resultat", "No hi ha reserves per aquest dia.")
            else:
                resultats = "\n".join([f"Reserva ID: {r[0]} | Data Inici: {r[1]} | Data Final: {r[2]} | Client: {r[3]} - {r[4]} | Habitació: {r[5]}" for r in reserves])
                tk.messagebox.showinfo("Reserves per Dia", resultats)

            conn.close()

        except Exception as e:
            tk.messagebox.showerror("Error", f"No s'ha pogut recuperar la informació:\n{e}")

    tk.Button(finestra, text="Consultar Reserves", command=consultar_reserves).pack(pady=20)

def obrir_finestra_empleats_per_hotel():
    """
    Obre una finestra per consultar els empleats per hotel, incloent el director, el gerent i la seva funció.
    """
    finestra = tk.Toplevel()
    finestra.title("Empleats per Hotel")
    finestra.geometry("500x400")

    tk.Label(finestra, text="ID de l'Hotel:").pack(pady=10)
    entrada_idhotel = tk.Entry(finestra)
    entrada_idhotel.pack(pady=10)

    def consultar_empleats():
        idhotel = entrada_idhotel.get().strip()
        if not idhotel:
            tk.messagebox.showerror("Error", "Has d'introduir un ID d'hotel.")
            return
        try:
            conn = connectar_bd()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    t.dni,
                    p.nom || ' ' || p.cognoms AS treballador_nom,
                    t.tipusTreballador,
                    r.anysExperiencia AS recepcio_experience
                FROM
                    treballador t
                JOIN persona p ON t.dni = p.dni
                LEFT JOIN recepcio r ON t.dni = r.dni
                WHERE
                    t.dni IN (
                        SELECT dniTreballador FROM treballa WHERE idHotel = %s
                    )
                ORDER BY
                    t.tipusTreballador;
            """, (idhotel,))

            empleats = cursor.fetchall()
            if not empleats:
                tk.messagebox.showinfo("Resultat", "No hi ha empleats registrats per aquest hotel.")
            else:
                resultats = "\n".join([f"DNI: {e[0]} | Nom: {e[1]} | Funció: {e[2]} | Experiència Recepció: {e[3] if e[3] else 'N/A'}" for e in empleats])
                tk.messagebox.showinfo("Empleats per Hotel", resultats)

            conn.close()

        except Exception as e:
            tk.messagebox.showerror("Error", f"No s'ha pogut recuperar la informació:\n{e}")

    tk.Button(finestra, text="Consultar Empleats", command=consultar_empleats).pack(pady=20)

import tkinter as tk
from llibreries.bd import connectar_bd

def obrir_finestra_recepcio_idiomes_nivell():
    """
    Obre una finestra per consultar els idiomes i el nivell dels treballadors de recepció.
    """
    finestra = tk.Toplevel()
    finestra.title("Recepció: Idiomes i Nivell")
    finestra.geometry("500x400")

    tk.Label(finestra, text="ID de l'Hotel:").pack(pady=10)
    entrada_idhotel = tk.Entry(finestra)
    entrada_idhotel.pack(pady=10)

    def consultar_recepcio_idiomes_nivell():
        idhotel = entrada_idhotel.get().strip()
        if not idhotel:
            tk.messagebox.showerror("Error", "Has d'introduir un ID d'hotel.")
            return
        try:
            conn = connectar_bd()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    r.dni AS recepcio_dni,
                    p.nom || ' ' || p.cognoms AS recepcio_nom,
                    i.nom AS idioma,
                    c.parla AS nivell_parla,
                    c.enten AS nivell_enten,
                    c.escriu AS nivell_escriu
                FROM
                    recepcio r
                JOIN persona p ON r.dni = p.dni
                JOIN coneixement c ON r.dni = c.dni
                JOIN idioma i ON c.nomIdioma = i.nom
                WHERE
                    r.dni IN (
                        SELECT dniTreballador FROM treballa WHERE idHotel = %s
                    )
                ORDER BY
                    p.nom, p.cognoms, i.nom;
            """, (idhotel,))

            recepcio_idiomes = cursor.fetchall()
            if not recepcio_idiomes:
                tk.messagebox.showinfo("Resultat", "No hi ha treballadors de recepció registrats per aquest hotel.")
            else:
                resultats = "\n".join([f"DNI: {e[0]} | Nom: {e[1]} | Idioma: {e[2]} | Nivell de parla: {e[3]} | Nivell d'entendre: {e[4]} | Nivell d'escriure: {e[5]}" for e in recepcio_idiomes])
                tk.messagebox.showinfo("Recepció: Idiomes i Nivell", resultats)

            conn.close()

        except Exception as e:
            tk.messagebox.showerror("Error", f"No s'ha pogut recuperar la informació:\n{e}")

    tk.Button(finestra, text="Consultar Idiomes i Nivell", command=consultar_recepcio_idiomes_nivell).pack(pady=20)

def obrir_finestra_recepcio_idiomes_nivell():
    """
    Obre una finestra per consultar els idiomes i el nivell dels treballadors de recepció.
    """
    finestra = tk.Toplevel()
    finestra.title("Recepció: Idiomes i Nivell")
    finestra.geometry("500x400")

    tk.Label(finestra, text="ID de l'Hotel:").pack(pady=10)
    entrada_idhotel = tk.Entry(finestra)
    entrada_idhotel.pack(pady=10)

    def consultar_recepcio_idiomes_nivell():
        idhotel = entrada_idhotel.get().strip()
        if not idhotel:
            tk.messagebox.showerror("Error", "Has d'introduir un ID d'hotel.")
            return
        try:
            conn = connectar_bd()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    r.dni AS recepcio_dni,
                    p.nom || ' ' || p.cognoms AS recepcio_nom,
                    i.nom AS idioma,
                    c.parla AS nivell_parla,
                    c.enten AS nivell_enten,
                    c.escriu AS nivell_escriu
                FROM
                    recepcio r
                JOIN persona p ON r.dni = p.dni
                JOIN coneixement c ON r.dni = c.dni
                JOIN idioma i ON c.nomIdioma = i.nom
                WHERE
                    r.dni IN (
                        SELECT dniTreballador FROM treballa WHERE idHotel = %s
                    )
                ORDER BY
                    p.nom, p.cognoms, i.nom;
            """, (idhotel,))

            recepcio_idiomes = cursor.fetchall()
            if not recepcio_idiomes:
                tk.messagebox.showinfo("Resultat", "No hi ha treballadors de recepció registrats per aquest hotel.")
            else:
                resultats = "\n".join([f"DNI: {e[0]} | Nom: {e[1]} | Idioma: {e[2]} | Nivell de parla: {e[3]} | Nivell d'entendre: {e[4]} | Nivell d'escriure: {e[5]}" for e in recepcio_idiomes])
                tk.messagebox.showinfo("Recepció: Idiomes i Nivell", resultats)

            conn.close()

        except Exception as e:
            tk.messagebox.showerror("Error", f"No s'ha pogut recuperar la informació:\n{e}")

    tk.Button(finestra, text="Consultar Idiomes i Nivell", command=consultar_recepcio_idiomes_nivell).pack(pady=20)

def obrir_finestra_cuina_categoria_revisor():
    """
    Obre una finestra per consultar les categories i revisors del personal de cuina.
    """
    finestra = tk.Toplevel()
    finestra.title("Cuina: Categoria i Revisor")
    finestra.geometry("500x400")

    tk.Label(finestra, text="ID de l'Hotel:").pack(pady=10)
    entrada_idhotel = tk.Entry(finestra)
    entrada_idhotel.pack(pady=10)

    def consultar_cuina():
        idhotel = entrada_idhotel.get().strip()
        if not idhotel:
            tk.messagebox.showerror("Error", "Has d'introduir un ID d'hotel.")
            return
        try:
            conn = connectar_bd()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    c.dni,
                    p.nom || ' ' || p.cognoms AS cuiner_nom,
                    c.categoria,
                    c.revisatPer AS cuiner_revisor
                FROM
                    cuina c
                JOIN persona p ON c.dni = p.dni
                WHERE
                    c.dni IN (
                        SELECT dniTreballador FROM treballa WHERE idHotel = %s
                    )
                ORDER BY
                    c.categoria;
            """, (idhotel,))

            cuiners = cursor.fetchall()
            if not cuiners:
                tk.messagebox.showinfo("Resultat", "No hi ha treballadors de cuina registrats per aquest hotel.")
            else:
                resultats = "\n".join([f"DNI: {e[0]} | Nom: {e[1]} | Categoria: {e[2]} | Revisor: {e[3]}" for e in cuiners])
                tk.messagebox.showinfo("Cuina: Categoria i Revisor", resultats)

            conn.close()

        except Exception as e:
            tk.messagebox.showerror("Error", f"No s'ha pogut recuperar la informació:\n{e}")

    tk.Button(finestra, text="Consultar Cuina", command=consultar_cuina).pack(pady=20)

def obrir_finestra_habitacions_per_hotel():
    """
    Obre una finestra per consultar les habitacions per hotel, incloent el número de l'habitació,
    el nombre de llits, la superfície, i les característiques com la nevera i la televisió.
    """
    finestra = tk.Toplevel()
    finestra.title("Habitacions per Hotel i Característiques")
    finestra.geometry("500x400")

    tk.Label(finestra, text="ID de l'Hotel:").pack(pady=10)
    entrada_idhotel = tk.Entry(finestra)
    entrada_idhotel.pack(pady=10)

    def consultar_habitacions():
        idhotel = entrada_idhotel.get().strip()
        if not idhotel:
            tk.messagebox.showerror("Error", "Has d'introduir un ID d'hotel.")
            return
        try:
            conn = connectar_bd()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    h.numero AS habitacio_numero,
                    h.llits AS habitacio_llits,
                    h.m2 AS habitacio_m2,
                    h.teNevera AS habitacio_nevera,
                    h.teTelevisio AS habitacio_televisio
                FROM
                    habitacio h
                WHERE
                    h.idHotel = %s
                ORDER BY
                    h.numero;
            """, (idhotel,))

            habitacions = cursor.fetchall()
            if not habitacions:
                tk.messagebox.showinfo("Resultat", "No hi ha habitacions registrades per aquest hotel.")
            else:
                resultats = "\n".join([f"Habitació {e[0]} | Llits: {e[1]} | M2: {e[2]} | Nevera: {e[3]} | Televisió: {e[4]}" for e in habitacions])
                tk.messagebox.showinfo("Habitacions per Hotel", resultats)

            conn.close()

        except Exception as e:
            tk.messagebox.showerror("Error", f"No s'ha pogut recuperar la informació:\n{e}")

    tk.Button(finestra, text="Consultar Habitacions", command=consultar_habitacions).pack(pady=20)

def obrir_finestra_reserves_per_hotel():
    """
    Obre una finestra per consultar les reserves per hotel, incloent les dates d'inici i final de la reserva,
    així com el client associat a cada reserva.
    """
    finestra = tk.Toplevel()
    finestra.title("Reserves per Hotel (Dates, Clients)")
    finestra.geometry("500x400")

    tk.Label(finestra, text="ID de l'Hotel:").pack(pady=10)
    entrada_idhotel = tk.Entry(finestra)
    entrada_idhotel.pack(pady=10)

    def consultar_reserves():
        idhotel = entrada_idhotel.get().strip()
        if not idhotel:
            tk.messagebox.showerror("Error", "Has d'introduir un ID d'hotel.")
            return
        try:
            conn = connectar_bd()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    r.idReserva,
                    r.dataInici,
                    r.dataFinal,
                    p.dni AS client_dni,
                    p.nom || ' ' || p.cognoms AS client_nom
                FROM
                    reserva r
                JOIN client c ON r.dniClient = c.dni
                JOIN persona p ON c.dni = p.dni
                WHERE
                    r.idHotel = %s
                ORDER BY
                    r.dataInici;
            """, (idhotel,))

            reserves = cursor.fetchall()
            if not reserves:
                tk.messagebox.showinfo("Resultat", "No hi ha reserves registrades per aquest hotel.")
            else:
                resultats = "\n".join([f"Reserva ID: {r[0]} | Data Inici: {r[1]} | Data Final: {r[2]} | Client: {r[3]} - {r[4]}" for r in reserves])
                tk.messagebox.showinfo("Reserves per Hotel", resultats)

            conn.close()

        except Exception as e:
            tk.messagebox.showerror("Error", f"No s'ha pogut recuperar la informació:\n{e}")

    tk.Button(finestra, text="Consultar Reserves", command=consultar_reserves).pack(pady=20)

def obrir_finestra_serveis_per_hotel():
    """
    Obre una finestra per consultar els serveis que ofereix un hotel específic.
    """
    finestra = tk.Toplevel()
    finestra.title("Serveis que ofereix l'Hotel")
    finestra.geometry("500x400")

    tk.Label(finestra, text="ID de l'Hotel:").pack(pady=10)
    entrada_idhotel = tk.Entry(finestra)
    entrada_idhotel.pack(pady=10)

    def consultar_serveis():
        idhotel = entrada_idhotel.get().strip()
        if not idhotel:
            tk.messagebox.showerror("Error", "Has d'introduir un ID d'hotel.")
            return
        try:
            conn = connectar_bd()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    s.nom AS servei_nom,
                    s.cost AS servei_cost
                FROM
                    servei s
                JOIN hotel_servei hs ON s.idServei = hs.idServei
                WHERE
                    hs.idHotel = %s
                ORDER BY
                    s.nom;
            """, (idhotel,))

            serveis = cursor.fetchall()
            if not serveis:
                tk.messagebox.showinfo("Resultat", "No hi ha serveis disponibles per aquest hotel.")
            else:
                resultats = "\n".join([f"Servei: {s[0]} | Cost: {s[1]}" for s in serveis])
                tk.messagebox.showinfo("Serveis per Hotel", resultats)

            conn.close()

        except Exception as e:
            tk.messagebox.showerror("Error", f"No s'ha pogut recuperar la informació:\n{e}")

    tk.Button(finestra, text="Consultar Serveis", command=consultar_serveis).pack(pady=20)

def obrir_finestra_solicituds_per_client():
    """
    Obre una finestra per consultar les sol·licituds de serveis realitzades per un client específic.
    """
    finestra = tk.Toplevel()
    finestra.title("Sol·licituds de Serveis per Client")
    finestra.geometry("500x400")

    tk.Label(finestra, text="DNI del Client:").pack(pady=10)
    entrada_dni = tk.Entry(finestra)
    entrada_dni.pack(pady=10)

    def consultar_solicituds():
        dni_client = entrada_dni.get().strip()
        if not dni_client:
            tk.messagebox.showerror("Error", "Has d'introduir un DNI de client.")
            return
        try:
            conn = connectar_bd()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    s.nom AS servei_nom,
                    ss.dataHora AS sol_servei_data,
                    ss.pagarEnCheckOut AS pagar_en_checkout
                FROM
                    sollicitud ss
                JOIN servei s ON ss.idServei = s.idServei
                WHERE
                    ss.dniClient = %s
                ORDER BY
                    ss.dataHora;
            """, (dni_client,))

            sol_serveis = cursor.fetchall()
            if not sol_serveis:
                tk.messagebox.showinfo("Resultat", "No hi ha sol·licituds de serveis per aquest client.")
            else:
                resultats = "\n".join([f"Servei: {s[0]} | Data: {s[1]} | Pagar a Check-out: {'Sí' if s[2] else 'No'}" for s in sol_serveis])
                tk.messagebox.showinfo("Sol·licituds de Serveis per Client", resultats)

            conn.close()

        except Exception as e:
            tk.messagebox.showerror("Error", f"No s'ha pogut recuperar la informació:\n{e}")

    tk.Button(finestra, text="Consultar Sol·licituds", command=consultar_solicituds).pack(pady=20)

def executar_procediment_validacio():
    try:
        conn = connectar_bd()
        cursor = conn.cursor()
        cursor.execute("SET client_min_messages = WARNING;")  # Per no veure info interna
        cursor.execute("DROP TRIGGER IF EXISTS trg_validar_telefon ON persona CASCADE;")
        cursor.execute("""
            CREATE OR REPLACE FUNCTION validar_telefon()
            RETURNS TRIGGER AS $$
            BEGIN
                IF NEW.telefon IS NULL OR NEW.telefon !~ '^\d{9,}$' THEN
                    RAISE EXCEPTION 'El telèfon ha de contenir només dígits i tenir com a mínim 9 caràcters.';
                END IF;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """)
        cursor.execute("""
            CREATE TRIGGER trg_validar_telefon
            BEFORE INSERT OR UPDATE ON persona
            FOR EACH ROW
            EXECUTE FUNCTION validar_telefon();
        """)
        conn.commit()
        tk.messagebox.showinfo("Èxit", "Trigger de validació creat correctament.")
    except Exception as e:
        tk.messagebox.showerror("Error", f"No s'ha pogut crear el trigger:\n{e}")
    finally:
        conn.close()

def simular_trigger_control_reserva():
    try:
        conn = connectar_bd()
        cursor = conn.cursor()
        cursor.execute("DROP TRIGGER IF EXISTS trg_evitar_duplicacio_reserva ON reserva CASCADE;")
        cursor.execute("""
            CREATE OR REPLACE FUNCTION evitar_duplicacio_reserva()
            RETURNS TRIGGER AS $$
            BEGIN
                IF EXISTS (
                    SELECT 1 FROM reserva
                    WHERE dniClient = NEW.dniClient
                    AND idHotel = NEW.idHotel
                    AND NEW.dataInici BETWEEN dataInici AND dataFinal
                ) THEN
                    RAISE EXCEPTION 'Ja existeix una reserva activa per aquest client a l''hotel en aquest període.';
                END IF;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """)
        cursor.execute("""
            CREATE TRIGGER trg_evitar_duplicacio_reserva
            BEFORE INSERT ON reserva
            FOR EACH ROW
            EXECUTE FUNCTION evitar_duplicacio_reserva();
        """)
        conn.commit()
        tk.messagebox.showinfo("Èxit", "Trigger de control de duplicació activat.")
    except Exception as e:
        tk.messagebox.showerror("Error", f"No s'ha pogut crear el trigger:\n{e}")
    finally:
        conn.close()

def obrir_finestra_reserves_per_habitacio():
    """
    Obre una finestra per consultar les reserves futures d’una habitació.
    Mostra la data d’arribada, sortida i el client.
    """
    finestra = tk.Toplevel()
    finestra.title("Reserves futures per Habitació")
    finestra.geometry("500x400")

    tk.Label(finestra, text="ID de l'Habitació:").pack(pady=10)
    entrada_idhabitacio = tk.Entry(finestra)
    entrada_idhabitacio.pack(pady=10)

    def consultar_reserves():
        idhabitacio = entrada_idhabitacio.get().strip()
        if not idhabitacio:
            tk.messagebox.showerror("Error", "Has d'introduir un ID d'habitació.")
            return
        try:
            conn = connectar_bd()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT r.dataInici, r.dataFinal, p.nom || ' ' || p.cognoms AS client
                FROM reserva r
                JOIN client c ON r.dniClient = c.dni
                JOIN persona p ON c.dni = p.dni
                JOIN reserva_habitacio rh ON r.idReserva = rh.idReserva
                WHERE rh.idHabitacio = %s AND r.dataInici >= CURRENT_DATE
                ORDER BY r.dataInici;
            """, (idhabitacio,))

            reserves = cursor.fetchall()
            if not reserves:
                tk.messagebox.showinfo("Resultat", "No hi ha reserves futures per aquesta habitació.")
            else:
                resultats = "\n".join([f"Entrada: {r[0]} | Sortida: {r[1]} | Client: {r[2]}" for r in reserves])
                tk.messagebox.showinfo("Reserves futures", resultats)

            conn.close()
        except Exception as e:
            tk.messagebox.showerror("Error", f"No s'ha pogut consultar:\n{e}")

    tk.Button(finestra, text="Consultar Reserves", command=consultar_reserves).pack(pady=20)

def obrir_finestra_historial_client():
    """
    Obre una finestra per consultar les visites i serveis utilitzats per un client.
    """
    finestra = tk.Toplevel()
    finestra.title("Historial del Client")
    finestra.geometry("500x400")

    tk.Label(finestra, text="DNI del Client:").pack(pady=10)
    entrada_dni = tk.Entry(finestra)
    entrada_dni.pack(pady=10)

    def consultar_historial():
        dni = entrada_dni.get().strip()
        if not dni:
            tk.messagebox.showerror("Error", "Has d'introduir un DNI.")
            return
        try:
            conn = connectar_bd()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT r.dataInici, r.dataFinal, s.nom AS servei
                FROM reserva r
                LEFT JOIN sollicitud ss ON r.idReserva = ss.idReserva
                LEFT JOIN servei s ON ss.idServei = s.idServei
                WHERE r.dniClient = %s
                ORDER BY r.dataInici;
            """, (dni,))

            resultats = cursor.fetchall()
            if not resultats:
                tk.messagebox.showinfo("Resultat", "No s'han trobat visites ni serveis per aquest client.")
            else:
                resposta = "\n".join([
                    f"Estada: {r[0]} → {r[1]} | Servei: {r[2] if r[2] else 'Cap'}"
                    for r in resultats
                ])
                tk.messagebox.showinfo("Historial del Client", resposta)

            conn.close()
        except Exception as e:
            tk.messagebox.showerror("Error", f"No s'ha pogut consultar:\n{e}")

    tk.Button(finestra, text="Consultar Historial", command=consultar_historial).pack(pady=20)

def executar_script(rel_path):
    try:
        base_dir = os.path.dirname(__file__)  # app/llibreries
        full_path = os.path.abspath(os.path.join(base_dir, rel_path))  # ../extract/...
        subprocess.Popen(["python", full_path])
    except Exception as e:
        tk.messagebox.showerror("Error", f"No s'ha pogut executar el script:\n{e}")

def obrir_finestra_manteniment():
    """
    Obre la finestra principal de manteniment amb les opcions de gestió i consultes.
    """
    root = tk.Tk()
    root.title("Gestió de Manteniment")
    root.geometry("480x600")

    tk.Label(root, text="Mòdul de Manteniment", font=("Arial", 14, "bold")).pack(pady=5)

    def bloc(titol, accions):
        tk.Label(root, text=titol, font=("Arial", 11, "bold")).pack(pady=(8, 2))
        for text, func in accions:
            tk.Button(root, text=text, width=45, font=("Arial", 9), command=func).pack(pady=1)

    bloc("Gestió bàsica", [
        ("Alta / Modificació d'Hotels", obrir_finestra_alta_modificacio_hotels),
        ("Alta de Personal", obrir_finestra_alta_personal),
        ("Nova Reserva", obrir_finestra_nova_reserva),
        ("Check-in", obrir_finestra_checkin),
        ("Check-out", obrir_finestra_checkout),
        ("Generar Dummy Data", executar_generar_dades_dummy),
        ("Eliminar Dummy Data", executar_eliminar_dades_dummy),
        ("Executar generar_dades.py", lambda: executar_script("../extract/export_xml.py")),
        ("Executar api_mossos.py", lambda: executar_script("../extract/api_mossos.py")),
        ("Executar bloc de consultes", lambda: executar_script("../llibreries/inform.py"))
    ])

    bloc("Consultes d'informació", [
        ("Reserves per dia", obrir_finestra_reserves_per_dia),
        ("Empleats per hotel", obrir_finestra_empleats_per_hotel),
        ("Recepció: idiomes i nivell", obrir_finestra_recepcio_idiomes_nivell),
        ("Cuina: categoria i revisor", obrir_finestra_cuina_categoria_revisor),
        ("Habitacions per hotel", obrir_finestra_habitacions_per_hotel),
        ("Reserves per hotel", obrir_finestra_reserves_per_hotel),
        ("Serveis de l'hotel", obrir_finestra_serveis_per_hotel),
        ("Sol·licituds de serveis", obrir_finestra_solicituds_per_client),
        ("Reserves futures per habitació", obrir_finestra_reserves_per_habitacio),
        ("Historial del client", obrir_finestra_historial_client)
    ])

    bloc("PL/pgSQL i Triggers", [
        ("Executar validació", executar_procediment_validacio),
        ("Simular trigger de reserva", simular_trigger_control_reserva)
    ])

    root.mainloop()

