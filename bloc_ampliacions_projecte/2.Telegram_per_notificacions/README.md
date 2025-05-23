# Bloc de Notificacions via Telegram – Gestió Hotelera Espamus+
Aquest document recull les funcionalitats desenvolupades per integrar notificacions automàtiques mitjançant Telegram Bot API dins del projecte Espamus+. L’objectiu és millorar la qualitat del servei a l’usuari mitjançant avisos en temps real quan realitza accions com fer una reserva, fer check-in o check-out.

## 🔐 Configuració segura del Bot
El sistema llegeix el token del bot de Telegram de forma segura des d’un fitxer extern telegram.enu, per evitar exposar-lo en el codi font. Això segueix el mateix model de gestió de credencials que hotel.enu.

### Exemple de telegram.enu:

```bash
BOT_TOKEN=123456789:ABCdefGhIJKlmNOPqrsTUVwxYZ
```

## 🏗️ Estructura del fitxer telegram.py
Aquest fitxer conté:

Carregador del token des del fitxer extern

Funció per consultar el chat_id del client

Funció per enviar missatges a través de l'API oficial de Telegram

![image](https://github.com/user-attachments/assets/d2a1885c-4220-4a10-ae0d-41138e0c7ae2)

## 📩 Notificacions en fer una reserva
Quan un client realitza una reserva mitjançant la interfície, rep automàticament un missatge de confirmació amb el seu ID de reserva i l’hotel on s’ha registrat.

Missatge exemple:

```bash
Hola! La teva reserva a l'hotel "Nom d'Hotel" ha estat confirmada.
Habitació número: 0
ID de reserva: 00000.
Gràcies per confiar en Espamus+!
```
![image](https://github.com/user-attachments/assets/2b5ae2b1-2402-473b-8bce-e5589549c372)

![image](https://github.com/user-attachments/assets/46603807-b2f6-43d5-a7a1-289c9249b0d5)


## 🛎️ Notificació de Check-in
Quan un client fa el check-in a l’hotel, el sistema envia un missatge de benvinguda.

Missatge exemple:

```bash
Has fet check-in correctament a l'hotel 1. Et desitgem una bona estada!
```
![image](https://github.com/user-attachments/assets/8ef6a218-25b7-4c91-9b95-f826cecef84d)

![image](https://github.com/user-attachments/assets/424e56ae-c290-4c1c-b579-29a43a787faa)


## 🏁 Notificació de Check-out
En realitzar el check-out, el client rep un missatge d’agraïment automàticament:

Missatge exemple:

```bash
Has fet check-out de l'hotel 1. Gràcies per la teva visita!
```
![image](https://github.com/user-attachments/assets/61a82d63-4b4d-4e8a-934c-fcddb3003d6c)

![image](https://github.com/user-attachments/assets/8c4aa259-c7ab-44e4-83b4-8670a120b43b)


🧠 Validacions intel·ligents
Per evitar errors amb les restriccions de la base de dades, el sistema valida que:

No es pugui fer el check-out el mateix dia que el check-in 

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
