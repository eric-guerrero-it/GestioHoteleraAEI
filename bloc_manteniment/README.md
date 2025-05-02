# Bloc de Manteniment – Gestió Hotelera Espamus+

Aquest mòdul conté la gestió principal del manteniment operatiu de la cadena hotelera: alta i modificació de dades, reserves, check-in/check-out, i consultes diverses relacionades amb hotels, clients i treballadors. Tot el codi està desenvolupat en Python amb entorn gràfic **Tkinter** i connexió a PostgreSQL.

---

## 🎯 Objectiu

Donar suport a les funcionalitats de l’**Annex 3** del projecte, garantint que el sistema permet:

- Alta i modificació d’hotels
- Alta de personal de qualsevol tipus (recepció, cuina, altres)
- Alta de reserves
- Procés de check-in i check-out
- Consultes útils sobre empleats, idiomes, habitacions, serveis i sol·licituds
- Execució de triggers i procediments PL/pgSQL per validar informació

---

## 📁 Fitxer principal

- `app/llibreries/manteniment.py`: conté totes les finestres gràfiques i connexió a la BD per realitzar les operacions requerides.

---

## ✅ Funcionalitats obligatòries implementades

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

## 🔹 Funcionalitats opcionals implementades

- 🛏️ **Reserves futures per habitació**  
  Amb la funció `obrir_finestra_reserves_per_habitacio()`, es poden consultar les reserves futures d'una habitació, amb data d’arribada, sortida i client.

- 📖 **Historial de serveis d’un client**  
  Amb `obrir_finestra_historial_client()`, es poden consultar totes les reserves i serveis utilitzats per un client concret.

---

## 🔺 Funcionalitats “top” pendents

- ❌ Proposta de dates alternatives o altres hotels si no hi ha disponibilitat
- ❌ Frontend complet amb Tkinter per totes les funcions

---

## 🧪 Estat del lliurament

- ✅ Requisits **obligatoris** implementats
- ✅ Requisits **opcionals** implementats (2)
- ✅ Validació de dades mitjançant PL/pgSQL
- ✅ Entorn funcional i estable

---

## 📂 Estructura de funcions

`app/llibreries/manteniment.py`

```text
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
├── obrir_finestra_reserves_per_habitacio()      ← Opcional
├── obrir_finestra_historial_client()            ← Opcional
├── obrir_finestra_manteniment()
````

---

## Llibreries utilitzades 
- `tkinter`: interfície gràfica

--- 

## 👥 Autors 

**Grup 12 – AEI** ASIX – INS Sa Palomera Curs 2024/2025 

--- 

## 🔗 Repositori principal ➡️ [Torna al projecte principal](../README.md)
