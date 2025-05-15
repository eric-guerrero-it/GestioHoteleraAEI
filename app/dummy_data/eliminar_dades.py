"""
Fitxer: eliminar_dades.py

Aquest script elimina totes les dades dummy generades per proves dins el projecte 
de gestió hotelera Espamus+. L'objectiu és deixar la base de dades neta per repetir 
proves, validar rendiment o fer demostracions amb dades regenerades.

Característiques:
- Elimina les dades seguint l'ordre correcte per evitar errors per dependències entre taules.
- Neteja més de 10 taules relacionades (reserves, clients, treballadors, activitats...).
- Pensat per funcionar després d'executar el script `generar_dades.py`.
- Mostra informació visual pas a pas del procés.
- Inclou confirmació per evitar eliminacions accidentals.

Requereix la connexió definida al mòdul `connectar_bd()` del paquet `llibreries`.
Recomanat utilitzar només en entorns de desenvolupament o proves.
"""

from llibreries.bd import connectar_bd

def eliminar_dades_dummy():
    conn = connectar_bd()
    cur = conn.cursor()
    try:
        print("Eliminant dades dummy de la base de dades...")

        taules = [
            "FACTURA_SERVEI",
            "FACTURA",
            "SOLLICITUD",
            "RESERVA_HABITACIO",
            "RESERVA",
            "ACTIVITAT",
            "TREBALLA",
            "TREBALLADOR",
            "CLIENT",
            "PERSONA",
            "HABITACIO",
            "HOTEL"
        ]

        for taula in taules:
            cur.execute(f"DELETE FROM {taula};")
            print(f"Taula {taula} netejada.")

        conn.commit()
        print("Totes les dades dummy s'han eliminat correctament.")

    except Exception as e:
        conn.rollback()
        print(f"Error durant l'eliminació: {e}")

    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    resposta = input("Estàs segur que vols eliminar totes les dades dummy? (sí/no): ")
    if resposta.lower() == "sí":
        eliminar_dades_dummy()
    else:
        print("Eliminació cancel·lada.")
        
