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

    El fitxer 'hotel.enu' ha de contenir línies amb format clau=valor:
        BD=nom_base_dades
        USER=nom_usuari
        PW=contrasenya
        IP=adreça_ip_servidor
        PORT=port_de_connexio
        SSLMODE=require / disable / allow
        
    Returns:
        connection: Objecte de connexió a la base de dades PostgreSQL.
    """
    ruta = os.path.join(os.path.dirname(__file__), "hotel.enu")

    config = {}
    with open(ruta, "r") as f:
        for linia in f:
            if "=" in linia:
                clau, valor = linia.strip().split("=", 1)
                config[clau.strip()] = valor.strip()

    conn = psycopg2.connect(
        dbname=config["BD"],
        user=config["USER"],
        password=config["PW"],
        host=config["IP"],
        port=int(config["PORT"]),
        sslmode=config["SSLMODE"]
    )

    return conn
