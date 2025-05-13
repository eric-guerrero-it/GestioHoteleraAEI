# Bloc de Consultes i Informes – Espamus+

Aquest document descriu la implementació tècnica del **Bloc de Consultes i Informes** de l’aplicació **Espamus+**, desenvolupada amb Python, Tkinter i PostgreSQL.

---

## 🎯 Objectiu

Aquest sistema permet consultar i mostrar, en format gràfic i tabulat, informació rellevant per a la gestió d’una cadena hotelera.

---

## ⭐ Funcionalitat TOP implementada

Una de les propostes opcionals destacades (TOP) de l’enunciat consistia en crear una **interfície gràfica amb Tkinter** que facilités la visualització dels informes i millorés l’experiència de l’usuari.

Aquesta interfície ha estat completament desenvolupada, és funcional, clara i permet operar amb els informes mitjançant radiobuttons i camps de text.

---

## 📊 Informes implementats (Annex 4)

S’han desenvolupat els següents informes descrits a l’annex 4:

### Obligatòris:
1. Nombre d’habitacions i personal d’un hotel concret  
2. Llistat del personal que treballa a un hotel  
3. Arribades i sortides (check-in / check-out) d’un hotel per una data seleccionada

### Opcional:
4. Rànquing d’hotels amb més visites, ordenats per nombre de reserves totals

---

## 🧪 Inserció de dades

Per poder generar els informes, s’ha realitzat la inserció de dades a la base de dades `gestiohoteleraaei`, incloent:

- Dades de dos hotels  
- Clients, treballadors, habitacions i reserves  
- Facturació, serveis i sol·licituds

📂 Aquesta inserció està recollida a l’arxiu `insercio_dades_espamus.sql`, que conté totes les sentències `INSERT INTO` necessàries per poblar les taules i facilitar la prova i validació dels informes desenvolupats.

---

## 🛠️ Tecnologia utilitzada

- **Llenguatge:** Python  
- **Llibreries:**  
  - `tkinter` – Interfície gràfica d’usuari  
  - `tabulate` – Visualització de resultats en format taula ASCII  
  - `psycopg2-binary` – Connexió amb PostgreSQL  
- **SGBD:** PostgreSQL amb connexió segura mitjançant SSL

---

## ⚙️ Característiques tècniques

- Interfície gràfica clara i dividida en seccions:
  - Selecció de l’informe amb radiobuttons  
  - Dades d’entrada (ID hotel / data)  
  - Resultats presentats amb `tabulate` i fonts monoespai

- Validació d’entrades i gestió d’errors:
  - Comprovació de camps buits  
  - Gestió d’errors de connexió o consulta SQL

- Connexió a PostgreSQL amb SSL activat

---

## 📁 Estructura del projecte

```plaintext
app/
└── llibreries/
    ├── bd.py           # Gestió de la connexió segura a la base de dades PostgreSQL mitjançant SSL
    └── inform.py       # Bloc de consultes: execució de consultes i visualització amb Tkinter
