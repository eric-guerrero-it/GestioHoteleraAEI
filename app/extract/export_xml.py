"""
Fitxer: export_xml.py

Aquest fitxer permet exportar dades de reserves i clients en format XML.
També pot generar l'esquema XSD per validar l'estructura dels fitxers XML generats.

És útil per compartir dades amb altres sistemes o per integració amb eines externes.
"""
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import psycopg2
import xml.etree.ElementTree as ET
from datetime import date
from llibreries.bd import connectar_bd


def exportar_reserves_xml(nom_grup="AEI"):
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
            ORDER BY r.dataInici
        """)

        reserves = cursor.fetchall()
        print(f"Nombre de reserves trobades: {len(reserves)}")  

        if not reserves:
            print("No s'han trobat reserves a la base de dades.")
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

        print("Directori on s'escriu l'arxiu:", carpeta_export)
        print(f"S'escriurà el fitxer XML: {nom_fitxer}")
        arbre.write(nom_fitxer, encoding="utf-8", xml_declaration=True)
        print(f"Exportació completada: {nom_fitxer}")

    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()


if __name__ == "__main__":
    exportar_reserves_xml()
