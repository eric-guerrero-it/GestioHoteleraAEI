"""
Fitxer: eliminar_dades.py

Aquest fitxer s'encarrega d'eliminar les dades simulades generades per a proves 
(de la base de dades o fitxers temporals), deixant l’entorn net per a nous tests.

És útil per repetir proves múltiples vegades o fer demostracions amb base de dades buida.
"""
from llibreries.bd import connectar_bd

def eliminar_dades_dummy():
    conn = connectar_bd()
    cur = conn.cursor()
    try:
        print("🗑️ Eliminant dades dummy de la base de dades...")

        # Ordre segur per evitar errors per claus foranes
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
            print(f"✔️ Taula {taula} netejada.")

        conn.commit()
        print("✅ Totes les dades dummy s'han eliminat correctament.")

    except Exception as e:
        conn.rollback()
        print(f"❌ Error durant l'eliminació: {e}")

    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    resposta = input("Estàs segur que vols eliminar totes les dades dummy? (sí/no): ")
    if resposta.lower() == "sí":
        eliminar_dades_dummy()
    else:
        print("❌ Eliminació cancel·lada.")
