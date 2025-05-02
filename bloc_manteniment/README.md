# 🛠️ Bloc de Manteniment – Gestió Hotelera Espamus+

Aquest mòdul conté la gestió principal del manteniment operatiu de la cadena hotelera: alta i modificació de dades, reserves, check-in/check-out, i consultes diverses relacionades amb hotels, clients i treballadors. Tot el codi està desenvolupat en Python amb entorn gràfic **Tkinter** i connexió a PostgreSQL.

---

## 🎯 Objectiu

Donar suport a les funcionalitats bàsiques de l’**Annex 3** del projecte, garantint que el sistema permet:

- Alta i modificació d’hotels
- Alta de personal de qualsevol tipus (recepció, cuina, altres)
- Alta de reserves
- Procés de check-in i check-out
- Consultes útils sobre empleats, idiomes, habitacions, serveis i sol·licituds
- Execució de triggers i procediments PL/pgSQL per validar informació

---

## 📁 Fitxer principal

- `app/llibreries/manteniment.py`: conté totes les finestres gràfiques i la connexió a la BD per realitzar les operacions requerides.

---

## ✅ Funcionalitats implementades

### Alta i modificació de dades:
- 🔹 Alta i modificació d’hotels
- 🔹 Alta de treballadors amb registre automàtic segons tipus
- 🔹 Alta de reserves

### Gestió de reserves:
- ✅ Check-in (actualitza data d'inici)
- ✅ Check-out (actualitza data final)

### Consultes i visualitzacions:
- 📆 Reserves planificades per dia (amb client i habitació)
- 🧑‍💼 Empleats d’un hotel (funció, experiència...)
- 🗣️ Idiomes i nivell del personal de recepció
- 🍳 Categoria i revisor del personal de cuina
- 🏨 Habitacions d’un hotel amb característiques
- 📋 Reserves per hotel amb dates i client
- 🧾 Serveis que ofereix cada hotel
- 🙋‍♀️ Sol·licituds de serveis fetes per cada client

### Validacions i PL/pgSQL
- 🔄 Triggers i procediments creats per validar dades i simular operacions amb PostgreSQL

---

## ⚙️ Llibreries utilitzades

- `tkinter`: interfície gràfica
- `psycopg2`: connexió PostgreSQL
- `os`: gestió del fitxer de credencials

---

## 📂 Estructura

/app/llibreries/manteniment.py

├── obrir_finestra_alta_modificacio_hotels()
├── obrir_finestra_alta_personal()
├── obrir_finestra_nova_reserva()
├── obrir_finestra_checkin()
├── obrir_finestra_checkout()
├── obrir_finestra_reserves_per_dia()
├── obrir_finestra_empleats_per_hotel()
├── obrir_finestra_recepcio_idiomes_nivell()
├── obrir_finestra_cuina_categoria_revisor()
├── obrir_finestra_habitacions_per_hotel()
├── obrir_finestra_reserves_per_hotel()
├── obrir_finestra_serveis_per_hotel()
├── obrir_finestra_solicituds_per_client()
├── obrir_finestra_manteniment()

---

## 🧪 Estat del lliurament

- ✅ Tots els requisits **obligatoris** implementats
- ✅ Accés a la base de dades 100% funcional
- ✅ Validacions i comprovacions d'errors
- ✅ Preparat per entrega 02/05/2025

---

## 👥 Autors

**Grup 12 – AEI**  
ASIX – INS Sa Palomera  
Curs 2024/2025

---

## 🔗 Repositori principal
➡️ [Torna al projecte principal](../README.md)
