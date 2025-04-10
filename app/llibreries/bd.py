"""
Fitxer: bd.py

Conté les funcions per establir connexió amb la base de dades PostgreSQL.
Inclou mètodes per executar consultes, inserir dades i gestionar errors de connexió.
"""

"""
Fitxer: bd.py

Conté la funció per connectar-se a la base de dades PostgreSQL.
Llegeix les credencials des d’un fitxer 'hotel.enu' (afegit al .gitignore).
"""

import psycopg2
import os


# ───────────────────────────────────────────────
# Connecta a la base de dades PostgreSQL utilitzant les credencials del fitxer
def connectar_bd():
    # Llegim les 4 línies del fitxer amb BD, USER, PW, IP
    ruta = os.path.join(os.path.dirname(__file__), "hotel.enu")
    with open(ruta, "r") as f:
            linies = f.read().splitlines()

    # Assignem cada línia a la variable corresponent
    bd = linies[0].split("=")[1].strip()
    user = linies[1].split("=")[1].strip()
    pw = linies[2].split("=")[1].strip()
    ip = linies[3].split("=")[1].strip()

    # Connectem a PostgreSQL
    conn = psycopg2.connect(
        dbname=bd,
        user=user,
        password=pw,
        host=ip
    )
    return conn
