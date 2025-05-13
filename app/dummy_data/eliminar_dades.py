"""
Fitxer: eliminar_dades.py

Aquest fitxer s'encarrega d'eliminar les dades simulades generades per a proves 
(de la base de dades o fitxers temporals), deixant l’entorn net per a nous tests.

És útil per repetir proves múltiples vegades o fer demostracions amb base de dades buida.
"""
from faker import Faker
import random
from datetime import datetime, timedelta
from llibreries.bd import connectar_bd

# Faker amb idiomes especials
faker_default = Faker()
faker_ru = Faker('ru_RU')
faker_ja = Faker('ja_JP')
faker_zh = Faker('zh_CN')

def eliminar_dummy_data():
    conn = connectar_bd()
    cur = conn.cursor()
    # Eliminem tot el relacionat amb clients i hotels amb telèfon que comença per 999
    cur.execute("DELETE FROM FACTURA_SERVEI")
    cur.execute("DELETE FROM FACTURA")
    cur.execute("DELETE FROM SOLLICITUD")
    cur.execute("DELETE FROM RESERVA_HABITACIO")
    cur.execute("DELETE FROM RESERVA")
    cur.execute("DELETE FROM CLIENT WHERE dni IN (SELECT dni FROM PERSONA WHERE telefon LIKE '999%')")
    cur.execute("DELETE FROM PERSONA WHERE telefon LIKE '999%'")
    cur.execute("DELETE FROM HOTEL WHERE telefon LIKE '999%'")
    conn.commit()
    cur.close()
    conn.close()