# Gestió Hotelera Espamus+

**Projecte intermodular ASIX M0372-M0370-MS003**  
**Curs 2024/2025**

---
## 📑 Índex

- [Nom del projecte](#gestió-hotelera-espamus)
- [Objectiu del Projecte](#objectiu-del-projecte)
- [Estructura de Carpetes](#estructura-de-carpetes)
- [Requisits](#requisits)
- [Com executar el projecte](#com-executar-el-projecte)
  - [🔹 Amb entorn virtual](#amb-entorn-virtual-recomanat)
  - [🔹 Sense entorn virtual](#sense-entorn-virtual)
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
