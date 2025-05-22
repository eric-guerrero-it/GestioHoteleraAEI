# Bloc de Notificacions via Telegram – Gestió Hotelera Espamus+
Aquest document recull les funcionalitats desenvolupades per integrar notificacions automàtiques mitjançant Telegram Bot API dins del projecte Espamus+. L’objectiu és millorar la qualitat del servei a l’usuari mitjançant avisos en temps real quan realitza accions com fer una reserva, fer check-in o check-out.

## 🔐 Configuració segura del Bot
El sistema llegeix el token del bot de Telegram de forma segura des d’un fitxer extern telegram.enu, per evitar exposar-lo en el codi font. Això segueix el mateix model de gestió de credencials que hotel.enu.

### Exemple de telegram.enu:

```bash
BOT_TOKEN=123456789:ABCdefGhIJKlmNOPqrsTUVwxYZ
```

### Estructura del fitxer telegram.py
Aquest fitxer conté:

Carregador del token des del fitxer extern

Funció per consultar el chat_id del client

Funció per enviar missatges a través de l'API oficial de Telegram

📸 (Captura recomanada): Pantalla del fitxer telegram.py mostrant la funció enviar_missatge_telegram.

## Vinculació de clients amb el seu chat_id
Quan el client inicia conversa amb el bot (via t.me/NOM_DEL_BOT?start=DNI0001), el sistema pot capturar el seu chat_id i guardar-lo a la taula client, fent possible l’enviament automàtic de notificacions.

### (Captura recomanada): Missatge de Telegram des del bot amb el primer "Hola!" i consulta getUpdates retornant el chat_id.

## 📩 Notificacions en fer una reserva
Quan un client realitza una reserva mitjançant la interfície, rep automàticament un missatge de confirmació amb el seu ID de reserva i l’hotel on s’ha registrat.

Missatge exemple:

```bash
Hola! La teva reserva a l'hotel 2 s'ha confirmat correctament. El teu ID de reserva és 47183.
```
📸 (Captura recomanada): Missatge rebut a Telegram confirmant la reserva.

## 🛎️ Notificació de Check-in
Quan un client fa el check-in a l’hotel, el sistema envia un missatge de benvinguda.

Missatge exemple:

```bash
Has fet check-in correctament a l'hotel 1. Et desitgem una bona estada!
```
📸 (Captura recomanada): Missatge de check-in rebut a Telegram.

## 🏁 Notificació de Check-out
En realitzar el check-out, el client rep un missatge d’agraïment automàticament:

Missatge exemple:

```bash
Has fet check-out de l'hotel 1. Gràcies per la teva visita!
```
📸 (Captura recomanada): Missatge de comiat per Telegram després del check-out.

🧠 Validacions intel·ligents
Per evitar errors amb les restriccions de la base de dades, el sistema valida que:

No es pugui fer el check-out el mateix dia que el check-in (si la restricció CHECK ho prohibeix)

El chat_id sigui vàlid i existent abans d’enviar qualsevol missatge

---

## Autors

**Grup 12 - AEI**  
Cicle Formatiu de Grau Superior d’**Administració de Sistemes Informàtics i Xarxes (ASIX)**  
**INS Sa Palomera – Curs 2024/2025**


---

## 🔗 Repositori principal del projecte
➡️ [Veure projecte principal a GitHub](../README.md)

---
