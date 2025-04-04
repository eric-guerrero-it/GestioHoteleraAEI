# 🏨 Gestió Hotelera Espamus+

**Intermodular project ASIX M0372-M0370-MS003**  
**Course 2024/2025**

---

## 🎯 Project Objective

This project aims to develop an application for the integrated management of a hotel chain.  
It includes functionalities such as:

- Client management  
- Reservations  
- Staff management  
- Check-in / Check-out  
- Invoicing  
- Data export to XML and Power BI  
- Connection to external API (Mossos d'Esquadra)  
- Security and high availability of the database  

The application is developed in **Python** and **PostgreSQL**, structured to work with open source software and adaptable to environments with few resources — all with a clear structure for teamwork.

---

## 📁 Folder Structure
## 📁 Folder Structure

```text
/app
├── main.py                     # Main file (menu, login, execution)
│
├── llibreries/                 # Functions for hotel management modules
│   ├── bd.py                   # Connection and execution of SQL queries
│   ├── login.py                # User registration and validation
│   ├── client.py               # Client registration and management
│   ├── treballadors.py         # Staff management
│   ├── manteniment.py          # Check-in, check-out, reservations
│   ├── facturacio.py           # Invoicing and service calculation
│   ├── seguretat.py            # Permissions, data masking, etc.
│   └── alta_disponibilitat.py  # Replication and backups
│
├── extract/                    # Export block and external API connection
│   ├── export_xml.py           # Export reservations to XML + XSD
│   ├── powerbi.py              # Export to Power BI
│   └── api_mossos.py           # Send data to the Mossos API
│
├── dummy_data/                 # Test data generation
│   ├── generar_dades.py
│   └── eliminar_dades.py
│
├── logs/
│   └── registre.log            # Log of actions and errors
│
├── requirements.txt            # List of required Python libraries
└── README.md                   # This document
