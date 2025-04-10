# Disseny ER i Model Relacional – Espamus+

Aquesta carpeta conté tota la documentació i fitxers relacionats amb el **disseny de la base de dades** del projecte **Gestió Hotelera Espamus+**, dins del projecte intermodular **ASIX M0372-M0370-MS003**.

---

## 📂 Contingut

- `model_er_hotel.pdf`: Diagrama **Entitat-Relació (ER)** creat amb dbdiagram.io segons els requisits funcionals del projecte.
- `model_relacional.txt`: **Model Relacional complet**, comentat i justificat amb:
  - Claus primàries (PK)
  - Claus foranes (FK)
  - Especialitzacions i relacions N:M
- `script_creacio_taules_bd_espamus.sql`: **Script SQL** de creació de totes les taules amb restriccions, referències i validacions (CHECKs).
- `creacio_base_dades_bd_espamus.sql`: Script per a la **creació de la base de dades** en PostgreSQL amb codificació UTF-8.
- `Disseny_ER_Model_Relacional_Espamus_COMPLET.pdf`: Document explicatiu amb objectius, estructura, comentaris i justificació del disseny.

---

## Objectiu

L’objectiu d’aquesta fase és definir amb precisió l’estructura de la base de dades per al sistema de gestió hotelera. El model cobreix:

- Tractament de **clients** i **treballadors**, amb especialitzacions (cuina, recepció, etc.)
- Assignació d’**habitacions**, **reserves** i gestió de serveis per hotel
- **Sol·licituds de serveis** i **facturació** detallada
- Preparació per **entorns multilingües**
- Arquitectura preparada per a ser **escalable i robusta**

---

## Estat del Lliurament

- ✔️ Model ER validat segons enunciat
- ✔️ Model relacional complet i justificat
- ✔️ Scripts provats a PostgreSQL (amb FK, PK, CHECKs)
- ✔️ Documentació en PDF preparada per entrega

---

## Autors

**Grup 12 - AEI**  
Cicle Formatiu de Grau Superior d’**Administració de Sistemes Informàtics i Xarxes (ASIX)**  
**INS Sa Palomera – Curs 2024/2025**
