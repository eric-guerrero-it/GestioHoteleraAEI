from llibreries.bd import connectar_bd
from faker import Faker

# Inicialitzar Faker
fake = Faker()

def generar_persona(cursor, num_dades=10):
    for _ in range(num_dades):
        # Generació de dades falses per a la taula PERSONA
        dni = fake.unique.ssn()
        nom = fake.first_name()
        cognoms = fake.last_name()
        telefon = fake.phone_number()
        adreca = fake.address()
        data_naixement = fake.date_of_birth(minimum_age=18, maximum_age=70)

        try:
            # Establir connexió amb la base de dades
            conn = connectar_bd()  # Aquí utilitzes la connexió definida a bd.py
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO persona (dni, nom, cognoms, telefon, adreca, dataNaixement)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (dni, nom, cognoms, telefon, adreca, data_naixement))
            conn.commit()
        except Exception as e:
            print(f"Error en generar persona: {e}")
        finally:
            conn.close()
