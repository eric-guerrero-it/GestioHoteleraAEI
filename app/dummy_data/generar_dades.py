from faker import Faker
import random
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'llibreries')))

from llibreries.bd import connectar_bd

# Faker amb idiomes especials
faker_default = Faker()
faker_ru = Faker('ru_RU')
faker_ja = Faker('ja_JP')
faker_zh = Faker('zh_CN')

def nom_mixed():
    idioma = random.choices(['default', 'ru', 'ja', 'zh'], weights=[85, 5, 5, 5])[0]
    if idioma == 'ru':
        return faker_ru.name()
    elif idioma == 'ja':
        return faker_ja.name()
    elif idioma == 'zh':
        return faker_zh.name()
    else:
        return faker_default.name()

def generar_hotels(n=100):
    conn = connectar_bd()
    cur = conn.cursor()
    for _ in range(n):
        cur.execute("""
            INSERT INTO HOTEL (nom, estrelles, adreca, poblacio, web, telefon)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            nom_mixed(),
            random.randint(1, 5),
            faker_default.address(),
            faker_default.city(),
            faker_default.url(),
            '999' + faker_default.msisdn()[:7]
        ))
    conn.commit()
    cur.close()
    conn.close()

def generar_clients(n=100):
    conn = connectar_bd()
    cur = conn.cursor()
    for _ in range(n):
        dni = faker_default.unique.bothify(text='########A')
        nom = nom_mixed()
        cognoms = faker_default.last_name() + " " + faker_default.last_name()
        telefon = '999' + faker_default.msisdn()[:7]
        adreca = faker_default.address()
        data_naixement = faker_default.date_of_birth(minimum_age=18, maximum_age=90)

        cur.execute("""
            INSERT INTO PERSONA (dni, nom, cognoms, telefon, adreca, dataNaixement)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (dni, nom, cognoms, telefon, adreca, data_naixement))
        
        cur.execute("""
            INSERT INTO CLIENT (dni)
            VALUES (%s)
        """, (dni,))
    conn.commit()
    cur.close()
    conn.close()



if __name__ == "__main__":
    print("Generant dades dummy...")
    generar_hotels()
    generar_clients()
    print("Dades generades correctament. Pots consultar la base de dades.")
