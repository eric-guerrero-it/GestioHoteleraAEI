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
- Alta i modificació d’hotels
- Alta de treballadors amb registre automàtic segons tipus
- Alta de reserves

### Gestió de reserves:
- Check-in (actualitza data d'inici)
- Check-out (actualitza data final)

### Consultes i visualitzacions:
- Reserves planificades per dia (amb client i habitació)
- Empleats d’un hotel (funció, experiència...)
- Idiomes i nivell del personal de recepció
- Categoria i revisor del personal de cuina
- Habitacions d’un hotel amb característiques
- Reserves per hotel amb dates i client
- Serveis que ofereix cada hotel
- Sol·licituds de serveis fetes per cada client

### Validacions i PL/pgSQL
- Triggers i procediments creats per validar dades i simular operacions amb PostgreSQL

Validar telèfon (només dígits i mínim 9 caràcters)
```bash
CREATE OR REPLACE FUNCTION validar_telefon()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.telefon IS NULL OR NEW.telefon !~ '^\d{9,}$' THEN
        RAISE EXCEPTION 'El telèfon ha de contenir només dígits i tenir com a mínim 9 caràcters.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validar_telefon
BEFORE INSERT OR UPDATE ON persona
FOR EACH ROW
EXECUTE FUNCTION validar_telefon();

```
Evitar duplicats de reserva per client, hotel i data
```bash
CREATE OR REPLACE FUNCTION evitar_duplicacio_reserva()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM reserva
        WHERE dniClient = NEW.dniClient
        AND idHotel = NEW.idHotel
        AND NEW.dataInici BETWEEN dataInici AND dataFinal
    ) THEN
        RAISE EXCEPTION 'Reserva duplicada';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_evitar_duplicacio_reserva
BEFORE INSERT ON reserva
FOR EACH ROW
EXECUTE FUNCTION evitar_duplicacio_reserva();

```
---

## Funcionalitats opcionals implementades

- **Reserves futures per habitació**  
  Amb la funció `obrir_finestra_reserves_per_habitacio()`, es poden consultar les reserves futures d'una habitació, amb data d’arribada, sortida i client.

- **Historial de serveis d’un client**  
  Amb `obrir_finestra_historial_client()`, es poden consultar totes les reserves i serveis utilitzats per un client concret.

---

## 🧪 Estat del lliurament

-  Requisits **obligatoris** implementats
-  Requisits **opcionals** implementats (2)
-  Validació de dades mitjançant PL/pgSQL
-  Entorn funcional i estable

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
![image](https://github.com/user-attachments/assets/76b5fb58-ad43-46ba-8558-0038a503cdd7)

## 📂 Estructura de funcions per usuaris NO administradors

```text
├── obrir_finestra_nova_reserva()
├── obrir_finestra_checkin()
├── obrir_finestra_checkout()
````

![image](https://github.com/user-attachments/assets/1ef90672-50c1-4a28-a865-3b19cfccfc59)

---

## Llibreries utilitzades 
- `tkinter`: interfície gràfica

--- 

## 👥 Autors 

**Grup 12 – AEI** ASIX – INS Sa Palomera Curs 2024/2025 

--- 

## 🔗 Repositori principal  [Torna al projecte principal](../README.md)
