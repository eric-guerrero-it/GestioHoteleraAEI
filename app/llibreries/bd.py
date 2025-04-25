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
        SSL=sslmode (enable per a SSL)
        SSLCERT=ruta_certificat
        SSLKEY=ruta_clau_privada
        
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
    ssl = linies[4].split("=")[1].strip()  # SSL activat/desactivat
    sslcert = linies[5].split("=")[1].strip()  # Ruta al certificat
    sslkey = linies[6].split("=")[1].strip()  # Ruta a la clau privada

     # Comprovar si els fitxers SSL existeixen
    if not os.path.isfile(sslcert):
        raise FileNotFoundError(f"El certificat SSL no es troba: {sslcert}")
    if not os.path.isfile(sslkey):
        raise FileNotFoundError(f"La clau privada SSL no es troba: {sslkey}")

    # Connexió amb SSL (sense certificat CA, només amb clau i certificat del servidor)
    conn = psycopg2.connect(
        dbname=bd,
        user=user,
        password=pw,
        host=ip,
        sslmode=ssl,  # Activa l'SSL
        sslcert=sslcert,
        sslkey=sslkey
    )

    return conn
