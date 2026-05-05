# Gestió Hotelera Espamus+

**Projecte intermodular ASIX M0372-M0370-MS003**  
**Curs 2024/2025**

---

## 📑 Índex

- [Nom del projecte](#gestió-hotelera-espamus)
- [Objectiu del Projecte](#objectiu-del-projecte)
- [Estructura de Carpetes](#-estructura-de-carpetes)
- [Requisits](#requisits)
- [Com executar el projecte](#com-executar-el-projecte)
  - [🔹 Amb entorn virtual](#-amb-entorn-virtual-recomanat)
  - [🔹 Sense entorn virtual](#-sense-entorn-virtual)
- [Exemple d'ús](#exemple-dús)
- [Seguretat i Alta Disponibilitat](#seguretat-i-alta-disponibilitat)
- [Exportació de dades i integració amb API](#exportació-de-dades-i-integració-amb-api)
- [Generació de Dummy Data](#generació-de-dummy-data)
- [Testing i Validacions](#testing-i-validacions)
- [Autors i Crèdits](#autors-i-crèdits)



## Objectiu del Projecte

Aquest projecte té com a objectiu desenvolupar una aplicació per a la gestió integrada d'una cadena hotelera.  
Inclou funcionalitats com:

- Gestió de clients  
- Reserves  
- Gestió del personal  
- Check-in / Check-out  
- Facturació  
- Exportació de dades a XML i Power BI  
- Connexió amb API externa (Mossos d'Esquadra)  
- Seguretat i alta disponibilitat de la base de dades  

L’aplicació està desenvolupada en **Python** i **PostgreSQL**, estructurada per funcionar amb programari lliure i adaptable a entorns amb pocs recursos — tot amb una estructura clara per al treball en equip.

---

## 📁 Estructura de Carpetes

```text
/app
├── main.py                     # Fitxer principal (menú, login, execució)
│  
├── llibreries/                 # Funcions per als mòduls de gestió hotelera
│   ├── bd.py                   # Connexió i execució de consultes SQL
│   ├── login.py                # Registre i validació d'usuaris
│   ├── client.py               # Registre i gestió de clients
│   ├── treballadors.py         # Gestió de personal
│   ├── manteniment.py          # Check-in, check-out, reserves
│   ├── facturacio.py           # Facturació i càlcul de serveis
│   ├── seguretat.py            # Permisos, enmascarament de dades, etc.
│   └── alta_disponibilitat.py  # Rèplica i còpies de seguretat
│
├── extract/                    # Bloc d’exportació i connexió amb API externa
│   ├── export_xml.py           # Exportació de reserves a XML + XSD
│   ├── powerbi.py              # Exportació a Power BI
│   └── api_mossos.py           # Enviament de dades a l’API dels Mossos
│
├── dummy_data/                 # Generació de dades de prova
│   ├── generar_dades.py
│   └── eliminar_dades.py
│
├── logs/
│   └── registre.log            # Registre d’accions i errors
│
├── requirements.txt            # Llista de llibreries Python requerides
└── README.md                   # Aquest document
```

--- 

## Requisits

Per tal d’executar correctament aquest projecte, cal complir amb els següents requisits a nivell de sistema i de programari:

### ✔️ Requisits del sistema
- Sistema operatiu: Linux (recomanat Ubuntu 22.04 o superior)
- Connexió a Internet per a clonar el repositori i instal·lar dependències
- Espai en disc mínim: 500MB
- Accés a terminal o consola per executar el projecte

### ✔️ Requisits de programari
- Python 3.10 o superior
- PostgreSQL 13 o superior
- Git instal·lat (per fer clonació i seguiment de canvis)
- Power BI (opcional, per quadres de comandament)
- Llibreries Python necessàries (veure requirements.txt)

### Llibreries Python utilitzades
Les llibreries requerides s’instal·len automàticament amb pip. Algunes de les més rellevants són:

- psycopg2-binary: connexió amb PostgreSQL
- faker: generació de dades de prova (dummy data)
- xml.etree.ElementTree: creació de fitxers XML
- requests: connexió amb l’API dels Mossos
- logging: registre d’errors i accions

Pots veure totes les dependències exactes al fitxer [requirements.txt](./requirements.txt).

### 🔐 Altres requisits especials
- La base de dades ha d’estar configurada amb suport per caràcters Unicode (UTF-8) per suportar idiomes asiàtics i ciríl·lics.
- És recomanable configurar accés SSL a la base de dades i aplicar data masking a camps sensibles (com targetes de crèdit).
- Per al desplegament en entorns reals, es recomana una arquitectura **Alta Disponibilitat** (amb rèplica Actiu-Actiu o Actiu-Passiu).

## Com executar el projecte

Pots executar l’aplicació de dues maneres:

### 🔹 Amb entorn virtual (recomanat)

```bash
# 1. Clona el repositori
git clone https://github.com/Marquesmarki/GestioHoteleraAEI.git
cd GestioHoteleraAEI

# 2. Crea i activa l’entorn virtual
python3 -m venv venv
source venv/bin/activate  # (Linux/macOS)
venv\Scripts\activate     # (Windows)

# 3. Instal·la les dependències
pip install -r requirements.txt

# 4. Executa el projecte
cd app
python3 main.py
```

### 🔹 Sense entorn virtual

> Només recomanat per entorns de prova temporal.

```bash
cd app
pip install -r ../requirements.txt
python3 main.py
```

## Exemple d'ús

Un cop accedeixes a l’aplicació, veuràs un menú com aquest (exemple bàsic inicial):

```
Benvingut a Gestió Hotelera Espamus+

1. Iniciar sessió
2. Registrar usuari
3. Sortir

Escull una opció:
```

> A mesura que es desenvolupin més funcionalitats, aquest menú s’anirà ampliant.

## Testing i Validacions

Totes les funcions s’han provat amb tests manuals per validar el seu comportament bàsic.

S’han verificat:
- Inici de sessió correcte i incorrecte
- Connexió a la base de dades
- Inserció i lectura de dades simulades (dummy data)
- Gestió d’errors bàsics (fitxers, connexió, entrada d’usuari)

## Autors i Crèdits

Aquest projecte ha estat desenvolupat per l’equip del grup **Grup12_AEI** dins del cicle formatiu de grau superior d’**Administració de Sistemes Informàtics i Xarxes (ASIX)**  
**INS Sa Palomera** – Curs 2024/2025

### Participació personal

He participat en el desenvolupament i implementació del projecte dins d’un entorn de treball en equip, col·laborant en la configuració del sistema, la gestió de la base de dades i la validació de les funcionalitats de l’aplicació.
