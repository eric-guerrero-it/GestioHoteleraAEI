# 📚 Bloc d’Historial del Client – Gestió Hotelera Espamus+
Aquest document recull les funcionalitats desenvolupades per consultar fàcilment l’historial d’un client dins del projecte Espamus+. L’objectiu és oferir una eina àgil per visualitzar les reserves fetes pel client i els serveis utilitzats durant les seves estades.

## 🔍 Consulta detallada per DNI
L’usuari pot introduir el DNI d’un client per accedir al seu historial. Un cop introduït, el sistema mostra cronològicament totes les reserves realitzades per aquest client, juntament amb les dates i els serveis contractats (spa, excursions, etc.).

## 📋 Informació mostrada per cada entrada
Cada línia de l’historial inclou:

Data d’inici i fi de la reserva

Hotel on s’ha allotjat

Serveis utilitzats durant l’estada

Exemple de resultat:

```bash
Estada: 2024-07-01 al 2024-07-05 | Servei: Cap 
Estada: 2025-01-10 al 2025-01-12 | Servei: Restaurant
```

![image](https://github.com/user-attachments/assets/34261eda-8164-43b6-89af-98191c12db74)

## 🧠 Validacions i missatges d’error
El sistema comprova que el DNI sigui vàlid i estigui registrat com a client. Si no es troben dades, es mostra un missatge informatiu perquè l’usuari pugui corregir-ho.

## 🖼️ Interfície gràfica amb Tkinter
S’ha integrat una finestra nova a la interfície gràfica (Tkinter) amb:

Camps per introduir el DNI

Botó de consulta

Àrea de text on es mostra l’historial

## 📈 Aplicacions pràctiques
Aquest mòdul permet:

Donar millor atenció personalitzada al client

Consultar ràpidament els serveis que ha contractat habitualment

Ajudar en la presa de decisions per ofertes i recomanacions
---

## Autors

**Grup 12 - AEI**  
Cicle Formatiu de Grau Superior d’**Administració de Sistemes Informàtics i Xarxes (ASIX)**  
**INS Sa Palomera – Curs 2024/2025**


---

## 🔗 Repositori principal del projecte
➡️ [Veure projecte principal a GitHub](../README.md)

---
