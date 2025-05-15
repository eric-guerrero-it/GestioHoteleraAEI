from faker import Faker
import random
from datetime import datetime
import sys
import os

# afegir la ruta a llibreries per importar connectar_bd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'llibreries')))
from bd import connectar_bd

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
    try:
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
        print(f"✅ {n} hotels generats correctament.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error generant hotels: {e}")
    finally:
        cur.close()
        conn.close()

def generar_clients(n=50000):
    conn = connectar_bd()
    cur = conn.cursor()
    try:
        batch_persona = []
        batch_client = []
        for i in range(1, n + 1):
            dni = faker_default.unique.bothify(text='########A')
            nom = nom_mixed()
            cognoms = faker_default.last_name() + " " + faker_default.last_name()
            telefon = '999' + faker_default.msisdn()[:7]
            adreca = faker_default.address()
            data_naixement = faker_default.date_of_birth(minimum_age=18, maximum_age=90)

            batch_persona.append((dni, nom, cognoms, telefon, adreca, data_naixement))
            batch_client.append((dni,))

            if i % 500 == 0 or i == n:
                cur.executemany("""
                    INSERT INTO PERSONA (dni, nom, cognoms, telefon, adreca, dataNaixement)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, batch_persona)

                cur.executemany("""
                    INSERT INTO CLIENT (dni)
                    VALUES (%s)
                """, batch_client)

                conn.commit()
                batch_persona.clear()
                batch_client.clear()
                print(f"{i}/{n} clients generats...")

        print("✅ Tots els clients generats correctament.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error generant clients: {e}")
    finally:
        cur.close()
        conn.close()

def generar_treballadors(n=10000):
    conn = connectar_bd()
    cur = conn.cursor()
    try:
        tipus_treballador = ['cuina', 'recepcio', 'neteja', 'manteniment', 'direccio']
        id_hotels = []

        # Recuperar ID d'hotels existents per assignar-los aleatòriament
        cur.execute("SELECT idHotel FROM HOTEL")
        rows = cur.fetchall()
        id_hotels = [r[0] for r in rows]

        if not id_hotels:
            print("❌ No hi ha hotels a la base de dades. Primer executa generar_hotels().")
            return

        batch_persona = []
        batch_treballador = []
        batch_treballa = []

        for i in range(1, n + 1):
            dni = faker_default.unique.bothify(text='########B')
            nom = nom_mixed()
            cognoms = faker_default.last_name() + " " + faker_default.last_name()
            telefon = '999' + faker_default.msisdn()[:7]
            adreca = faker_default.address()
            data_naixement = faker_default.date_of_birth(minimum_age=18, maximum_age=65)

            tipus = random.choice(tipus_treballador)
            hotel_id = random.choice(id_hotels)

            batch_persona.append((dni, nom, cognoms, telefon, adreca, data_naixement))
            batch_treballador.append((dni, tipus))
            batch_treballa.append((dni, hotel_id))

            if i % 500 == 0 or i == n:
                cur.executemany("""
                    INSERT INTO PERSONA (dni, nom, cognoms, telefon, adreca, dataNaixement)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, batch_persona)

                cur.executemany("""
                    INSERT INTO TREBALLADOR (dni, tipusTreballador)
                    VALUES (%s, %s)
                """, batch_treballador)

                cur.executemany("""
                    INSERT INTO TREBALLA (dniTreballador, idHotel)
                    VALUES (%s, %s)
                """, batch_treballa)

                conn.commit()
                batch_persona.clear()
                batch_treballador.clear()
                batch_treballa.clear()
                print(f"{i}/{n} treballadors generats...")

        print("✅ Tots els treballadors generats correctament.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error generant treballadors: {e}")
    finally:
        cur.close()
        conn.close()

def generar_activitats(n=150000):
    conn = connectar_bd()
    cur = conn.cursor()
    try:
        # Recuperar ID dels hotels
        cur.execute("SELECT idHotel FROM HOTEL")
        hotels = [r[0] for r in cur.fetchall()]

        if not hotels:
            print("❌ No hi ha hotels a la base de dades.")
            return

        noms_activitats = [
            "Visita guiada", "Spa", "Taller de cuina", "Excursió", "Piscina nocturna",
            "Cata de vins", "Massatge relaxant", "Ioga matinal", "Cinema a la fresca", "Karaoke"
        ]

        batch = []
        for i in range(1, n + 1):
            id_hotel = random.choice(hotels)
            nom = random.choice(noms_activitats)
            descripcio = faker_default.text(max_nb_chars=100)
            data = faker_default.date_between(start_date='-1y', end_date='+6m')
            preu = round(random.uniform(10.0, 100.0), 2)

            batch.append((id_hotel, nom, descripcio, data, preu))

            if i % 1000 == 0 or i == n:
                cur.executemany("""
                    INSERT INTO ACTIVITAT (idHotel, nom, descripcio, data, preu)
                    VALUES (%s, %s, %s, %s, %s)
                """, batch)
                conn.commit()
                batch.clear()
                print(f"{i}/{n} activitats generades...")

        print("✅ Totes les activitats generades correctament.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error generant activitats: {e}")
    finally:
        cur.close()
        conn.close()

from datetime import timedelta

def generar_reserves(n=100000):
    conn = connectar_bd()
    cur = conn.cursor()
    try:
        # Obtenir DNI de clients
        cur.execute("SELECT dni FROM CLIENT")
        clients = [r[0] for r in cur.fetchall()]
        
        # Obtenir ID dels hotels
        cur.execute("SELECT idHotel FROM HOTEL")
        hotels = [r[0] for r in cur.fetchall()]

        # Obtenir habitacions i associar-les al seu hotel
        cur.execute("SELECT idHabitacio, idHotel FROM HABITACIO")
        habitacions = cur.fetchall()
        habitacions_per_hotel = {}
        for idHab, idHot in habitacions:
            habitacions_per_hotel.setdefault(idHot, []).append(idHab)

        if not clients or not hotels or not habitacions:
            print("❌ Falten clients, hotels o habitacions.")
            return

        for i in range(1, n + 1):
            dni_client = random.choice(clients)
            id_hotel = random.choice(hotels)

            data_inici = faker_default.date_between(start_date='-30d', end_date='+90d')
            durada = random.randint(1, 14)
            data_final = data_inici + timedelta(days=durada)

            # Inserir RESERVA i recuperar ID
            cur.execute("""
                INSERT INTO RESERVA (dniClient, idHotel, dataInici, dataFinal)
                VALUES (%s, %s, %s, %s)
                RETURNING idReserva
            """, (dni_client, id_hotel, data_inici, data_final))
            id_reserva = cur.fetchone()[0]

            # Triar entre 1 i 2 habitacions del mateix hotel
            habitacions_hotel = habitacions_per_hotel.get(id_hotel, [])
            seleccionades = random.sample(habitacions_hotel, k=min(len(habitacions_hotel), random.choice([1, 2])))

            for id_hab in seleccionades:
                preu_alta = round(random.uniform(80.0, 200.0), 2)
                preu_baixa = round(preu_alta * 0.7, 2)
                cur.execute("""
                    INSERT INTO RESERVA_HABITACIO (idReserva, idHabitacio, preuTemporadaAlta, preuTemporadaBaixa)
                    VALUES (%s, %s, %s, %s)
                """, (id_reserva, id_hab, preu_alta, preu_baixa))

            if i % 1000 == 0:
                conn.commit()
                print(f"{i}/{n} reserves generades...")

        conn.commit()
        print("✅ Totes les reserves (i habitacions) generades correctament.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error generant reserves: {e}")
    finally:
        cur.close()
        conn.close()

def crear_indexos():
    conn = connectar_bd()
    cur = conn.cursor()
    try:
        print("⚙️ Creant índexs útils per a consultes...")

        indexos = [
            "CREATE INDEX IF NOT EXISTS idx_reserva_dni ON RESERVA(dniClient);",
            "CREATE INDEX IF NOT EXISTS idx_reserva_hotel ON RESERVA(idHotel);",
            "CREATE INDEX IF NOT EXISTS idx_reserva_dates ON RESERVA(dataInici, dataFinal);",
            "CREATE INDEX IF NOT EXISTS idx_activitat_hotel ON ACTIVITAT(idHotel);",
            "CREATE INDEX IF NOT EXISTS idx_reserva_habitacio ON RESERVA_HABITACIO(idReserva);"
        ]

        for idx in indexos:
            cur.execute(idx)

        conn.commit()
        print("✅ Índexs creats correctament.")

    except Exception as e:
        conn.rollback()
        print(f"❌ Error creant índexs: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    print("🔄 Generant dades dummy...")
    generar_hotels(100)
    generar_clients(50000)
    generar_treballadors(10000)
    generar_activitats(150000)
    generar_reserves(100000)
    crear_indexos()
    print("🎉 Totes les dades generades correctament.")



