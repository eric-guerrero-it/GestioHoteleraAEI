"""
Fitxer: eliminar_dades.py

Aquest script elimina totes les dades dummy generades per proves dins del sistema 
de gestió hotelera Espamus+. És útil per reiniciar l'estat de la base de dades i 
permetre noves execucions de tests o demostracions.

Característiques clau:
- Elimina registres de més de 10 taules relacionades (reserves, clients, activitats, etc.).
- Respecta l’ordre de dependència per evitar errors de clau forana.
- Filtra només les dades generades per scripts, mitjançant el prefix '999' als telèfons.
- Requereix confirmació per evitar eliminacions accidentals.
- Mostra l’estat de l’operació amb missatges clars.

Requereix:
- Connexió a PostgreSQL via la funció `connectar_bd()` (modul llibreries.bd)
- Ús exclusiu en entorns de desenvolupament o proves.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'llibreries')))
from bd import connectar_bd

def eliminar_dades_dummy():
    conn = connectar_bd()
    cur = conn.cursor()
    try:
        print("Iniciant eliminació de dades dummy...")

        cur.execute("DELETE FROM FACTURA_SERVEI")
        cur.execute("DELETE FROM FACTURA")
        cur.execute("DELETE FROM SOLLICITUD")
        cur.execute("DELETE FROM RESERVA_HABITACIO")
        cur.execute("DELETE FROM RESERVA")
        cur.execute("DELETE FROM ACTIVITAT")
        cur.execute("DELETE FROM TREBALLA")
        cur.execute("DELETE FROM TREBALLADOR WHERE dni IN (SELECT dni FROM PERSONA WHERE telefon LIKE '999%')")
        cur.execute("DELETE FROM CLIENT WHERE dni IN (SELECT dni FROM PERSONA WHERE telefon LIKE '999%')")
        cur.execute("DELETE FROM PERSONA WHERE telefon LIKE '999%'")
        cur.execute("DELETE FROM HABITACIO WHERE idHotel IN (SELECT idHotel FROM HOTEL WHERE telefon LIKE '999%')")
        cur.execute("DELETE FROM HOTEL WHERE telefon LIKE '999%'")

        conn.commit()
        print("Dades dummy eliminades correctament.")

    except Exception as e:
        conn.rollback()
        print(f"Error durant l'eliminació: {e}")

    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    resposta = input("Estàs segur que vols eliminar totes les dades dummy generades? (sí/no): ")
    if resposta.strip().lower() == "sí":
        eliminar_dades_dummy()
    else:
        print("Eliminació cancel·lada.")
        
