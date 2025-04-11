"""
Fitxer: generar_dades.py

Aquest fitxer conté funcions per generar dades simulades (dummy data) 
per fer proves i validar el funcionament del sistema hoteler.
Les dades poden incloure clients, reserves, treballadors i activitats.

Aquestes dades ajuden a comprovar el rendiment i els fluxos del programa sense necessitat de dades reals.
"""
from faker import Faker
import psycopg2
from llibreries import bd  # fitxer bd.py per connectar 

# Inicialitzem Faker
fake = Faker('es_ES')  # Idioma espanyol/català

# Connectem a la base de dades
conn = bd.onnectar_bd()
cursor = conn.cursor()

# Inserim 100 registres
for _ in range(100):
    dni = fake.unique.bothify(text='########?')[:15]  # DNI estil 12345678A
    nom = fake.first_name()
    cognoms = f"{fake.last_name()} {fake.last_name()}"
    telefon = fake.phone_number()[:20]
    adreca = fake.address().replace("\n", ", ")[:150]
    datanaixement = fake.date_of_birth(minimum_age=18, maximum_age=65)  # format: YYYY-MM-DD

    cursor.execute("""
        INSERT INTO usuaris (dni, nom, cognoms, telefon, adreca, datanaixement)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (dni, nom, cognoms, telefon, adreca, datanaixement))

conn.commit()
conn.close()
print("100 usuaris falsos afegits correctament.")
