"""
Fitxer: eliminar_dades.py

Aquest script elimina totes les dades dummy generades per proves dins el projecte 
de gestió hotelera Espamus+. L'objectiu és deixar la base de dades neta per repetir 
proves, validar rendiment o fer demostracions amb dades regenerades.

Característiques:
- Elimina les dades seguint l'ordre correcte per evitar errors de dependència.
- Inclou filtre específic per només eliminar les dades generades per scripts (telèfons '999%').
- Pensat per funcionar després de `generar_dades.py`.
- Mostra informació clara del procés amb confirmació prèvia.

Requereix la connexió definida al mòdul `connectar_bd()` dins `llibreries`.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'llibreries')))
from bd import connectar_bd

def eliminar_dades_dummy():
    conn = connectar_bd()
    cur = conn.cursor()
    try:
        print("🗑️ Iniciant eliminació de dades dummy...")

        # Eliminar registres en ordre de dependència
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
