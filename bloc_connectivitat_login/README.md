# Bloc de Connectivitat i Login – Espamus+

Aquest mòdul permet la connexió a la base de dades i la gestió d’usuaris per iniciar sessió o registrar-se, tal com s'indica a l'Annex 2 del projecte **Gestió Hotelera Espamus+**.

##  Funcionalitats

- Connexió a la base de dades PostgreSQL (fitxer `bd.py`)
- Registre i inici de sessió d’usuaris amb encriptació SHA-256 (`login.py`)
- Interfície gràfica opcional amb Tkinter per login i registre
- Guarda el registre d’usuaris en un fitxer local de registre (`logs/registre.log`)
- Validació amb contrasenya encriptada
- Crea automàticament la taula `usuaris` a la BD

## 📂 Fitxers implicats

- `app/llibreries/bd.py` → Connexió a PostgreSQL amb credencials ocultes a `hotel.enu`
- `app/llibreries/login.py` → Registre, login, encriptació i interfície
- `logs/registre.log` → Registre local d’accessos (en mode desenvolupament)

##  Estat actual

- [x] Connexió a PostgreSQL provada i funcional
- [x] Sistema de login funcional amb interfície Tkinter
- [x] Encriptació de contrasenyes mitjançant SHA-256
- [x] Creació automàtica de la taula `usuaris`

##  Notes

- Les credencials de la base de dades es troben al fitxer ocult `hotel.enu`, que està exclòs amb `.gitignore`.
- Es pot ampliar la interfície amb més funcionalitats (esborrar usuari, restablir contrasenya, etc.).

## Autors

 **Grup 12 - AEI** – ASIX INS Sa Palomera – Curs 2024/2025


---

## 🔗 Repositori principal del projecte
➡️ [Veure projecte principal a GitHub](../README.md)

---
