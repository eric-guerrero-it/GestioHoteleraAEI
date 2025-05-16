# Generació de Dades Dummy – Espamus+

Aquest projecte conté els scripts per generar i eliminar dades de prova (dummy data) dins del sistema de gestió hotelera **Espamus+**. Està dissenyat per validar el correcte funcionament i rendiment del sistema en entorns de desenvolupament, test o demostració.

---

## Eines i Tecnologies

- **Llenguatge**: Python 3.x  
- **Llibreries**: [`faker`](https://faker.readthedocs.io/) per generar dades sintètiques  
- **Base de dades**: PostgreSQL  
- **Connexió**: mòdul `connectar_bd()` via `psycopg2`, ubicat a `llibreries/bd.py`

---

## Estratègia de generació

S’han aplicat bones pràctiques per garantir eficiència i coherència de les dades:

- **Batch inserts**: es fan insercions en lots (per exemple, 5.000 clients) per reduir l’ús de memòria i augmentar la velocitat.
- **Relacions consistents**: totes les dades respecten les claus foranes (ex: reserves associades a hotels i clients vàlids).
- **Telèfons de prova**: comencen per `999` per facilitar el filtratge i eliminació.
- **Diversitat internacional**: els noms es generen en diferents idiomes (català, rus, japonès, xinès).
- **Evitem duplicats**: gràcies a `faker.unique`.

---

## 📊 Taules generades i volum aproximat

| Taula               | Quantitat       | Comentaris                                       |
|---------------------|-----------------|--------------------------------------------------|
| `HOTEL`             | 100             | Amb estrelles, adreça i telèfon únic (`999`)     |
| `CLIENT`            | 50.000          | Amb nacionalitat i dades personals               |
| `TREBALLADOR`       | 10.000          | Associats a hotels                               |
| `ACTIVITAT`         | 150.000         | Amb preus, descripcions i hotel vinculat         |
| `RESERVA`           | 100.000         | Associades a client i hotel                      |
| `RESERVA_HABITACIO` | ≥100.000        | 1 o 2 habitacions per reserva                    |
| `HABITACIO`         | 1.500           | 15 per hotel, amb característiques variables     |

---

## Consideracions de rendiment

- S’usen **lots més petits** en taules grans per evitar errors com `malloc(): invalid size`.
- El procés pot durar diversos minuts, amb **progrés mostrat per consola**:
  ```text
  10000/50000 clients generats...
  ```
- Finalitzada la generació, es creen índexs útils per millorar el rendiment de consultes SQL.

---

## Codi i estructura

Totes les funcions de generació estan definides a `generar_dades.py`.

Cada taula té la seva pròpia funció:

- `generar_clients()`
- `generar_reserves()`
- `generar_activitats()`
- `generar_hotels()`
- `generar_treballadors()`
- `generar_habitacions()`
- `crear_indexos()`

L’script s’executa automàticament si s’executa:

```bash
python generar_dades.py
```

---

## ✅ Validacions realitzades
- Consulta SELECT COUNT(*) a PgAdmin per verificar el nombre de registres.

- Visualització directa de les taules generades a PgAdmin.

- Execució de funcionalitats a Tkinter per comprovar la integritat de les dades.

---

## Eliminació segura de dades dummy – eliminar_dades.py

També s’inclou un script per netejar totes les dades de prova generades:

### Funcionalitat destacada:
- Elimina només les dades de prova usant el prefix 999 en telèfons.

- Respecta l’ordre de dependències per evitar errors de clau forana.

- Requereix confirmació manual abans d’eliminar (si s’executa des de terminal).

- Permet reinicialitzar la base de dades per fer noves proves o demos.

### Taules afectades:
- Reserves i habitacions (RESERVA, RESERVA_HABITACIO)

- Clients i treballadors (CLIENT, TREBALLADOR, PERSONA)

Activitats (ACTIVITAT)

Hotels i habitacions associades (HOTEL, HABITACIO)

--- 

## 👥 Autors 

**Grup 12 – AEI** ASIX – INS Sa Palomera Curs 2024/2025 

--- 

## 🔗 Repositori principal  [Torna al projecte principal](../README.md)
