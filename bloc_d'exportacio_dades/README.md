📦 Bloc d’Exportació de Dades – Gestió Hotelera Espamus+
Aquest document recull les funcionalitats desenvolupades per al bloc d’exportació de dades del projecte Espamus+, que inclou: generació de fitxers XML, enviament de dades a l’API dels Mossos d’Esquadra, registre d'enviaments i la creació d’un Dashboard Power BI connectat a la base de dades.

1️⃣ Exportació de reserves a XML
L’usuari pot seleccionar dues dates per exportar totes les reserves dins d’aquest interval. Les dades exportades inclouen el client, hotel, dates i habitació, i es guarden en un fitxer XML ben estructurat i validat.

✅ Menu inicial

![image](https://github.com/user-attachments/assets/a60b62b5-d2d5-4aac-9b92-c2863247ea6b)

💾 Guardar XML entre dues dates

![image](https://github.com/user-attachments/assets/7f28fc40-d14e-4c9a-83f2-191ca6b3b808)

📊 Rànquing d’hotels amb més reserves

![image](https://github.com/user-attachments/assets/ade20901-582f-4ff1-af1c-319fa5cfe172)


---

2️⃣ Enviament de dades a l’API dels Mossos d’Esquadra
S’ha desenvolupat una funcionalitat per exportar i enviar les reserves dels clients (amb DNI, nacionalitat i habitació) entre dues dates en format JSON a una API externa. L'enviament queda registrat a la taula enviaments_api.

✅ Menu inicial

![image](https://github.com/user-attachments/assets/55f8748d-073d-4b0d-a7ee-8503abb46359)

📤 Enviar JSON entre dues dates

![image](https://github.com/user-attachments/assets/e992e13d-a86b-47ae-9374-2e0eac64a340)

📝 Enregistrar l’enviament a la base de dades

![image](https://github.com/user-attachments/assets/ab6ef2f6-3051-48f5-8217-7302b9e51c1f)


---
3️⃣ Dashboard amb Power BI
S’ha creat un quadre de comandament (dashboard) amb Power BI connectat a la base de dades PostgreSQL, on es visualitzen:

📅 Reserves per dia i per hotel

💰 Ingressos previstos

🛎️ Serveis més contractats

📈 Estadístiques d’ocupació i estades

🔌 Connexió a la base de dades

![image](https://github.com/user-attachments/assets/701f67ac-c6f9-43ed-a498-e3a4dd125bf8)

![image](https://github.com/user-attachments/assets/3ce270ae-c6e6-4648-a0be-43356a79af70)

📥 Importar taules necessàries

![image](https://github.com/user-attachments/assets/7571e921-3b67-42b0-a18d-99d9b3398f6f)

---

## Autors

**Grup 12 - AEI**  
Cicle Formatiu de Grau Superior d’**Administració de Sistemes Informàtics i Xarxes (ASIX)**  
**INS Sa Palomera – Curs 2024/2025**


---

## 🔗 Repositori principal del projecte
➡️ [Veure projecte principal a GitHub](../README.md)

---




