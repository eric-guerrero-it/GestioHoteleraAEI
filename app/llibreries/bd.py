"""
Fitxer: bd.py

Conté la funció per connectar-se a la base de dades PostgreSQL.
Llegeix les credencials des d’un fitxer 'hotel.enu' (afegit al .gitignore).
"""

import psycopg2
import os


def connectar_bd():
    """
    Estableix la connexió amb la base de dades PostgreSQL utilitzant
    les credencials definides en el fitxer 'hotel.enu'.

    El fitxer 'hotel.enu' ha de contenir 4 línies amb format clau=valor:
        BD=nom_base_dades
        USER=nom_usuari
        PW=contrasenya
        IP=adreça_ip_servidor

    Returns:
        connection: Objecte de connexió a la base de dades PostgreSQL.
    """
    ruta = os.path.join(os.path.dirname(__file__), "hotel.enu")

    with open(ruta, "r") as f:
        linies = f.read().splitlines()

    bd = linies[0].split("=")[1].strip()
    user = linies[1].split("=")[1].strip()
    pw = linies[2].split("=")[1].strip()
    ip = linies[3].split("=")[1].strip()

    conn = psycopg2.connect(
        dbname=bd,
        user=user,
        password=pw,
        host=ip
    )

    return conn
