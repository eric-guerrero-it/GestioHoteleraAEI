# Bloc de Connectivitat i Login – Espamus+

Aquest mòdul permet la connexió a la base de dades i la gestió d’usuaris per iniciar sessió o registrar-se, tal com s'indica a l'Annex 2 del projecte **Gestió Hotelera Espamus+**.

## Funcionalitats

- Connexió a la base de dades PostgreSQL ([`bd.py`](../app/llibreries/bd.py))
- Registre i inici de sessió d’usuaris amb encriptació SHA-256 ([`login.py`](../app/llibreries/login.py))
- Interfície gràfica opcional amb Tkinter per login i registre
- Registre local dels usuaris en un fitxer (`[logs/registre.log`](../logs/registre.log))
- Validació amb contrasenya encriptada
- Creació automàtica de la taula `usuaris` a la BD

## 📂 Fitxers implicats

- [`app/llibreries/bd.py`](../app/llibreries/bd.py) → Connexió a PostgreSQL amb credencials ocultes (`hotel.enu`)
- [`app/llibreries/login.py`](../app/llibreries/login.py) → Registre, login, encriptació i interfície gràfica
- [`logs/registre.log`](../logs/registre.log) → Registre local d’accessos (només desenvolupament)

## ✅ Estat actual

- [x] Connexió a PostgreSQL provada i funcional
- [x] Sistema de login funcional amb interfície Tkinter
- [x] Encriptació de contrasenyes mitjançant SHA-256
- [x] Creació automàtica de la taula `usuaris`

## Notes

- Les credencials de connexió es troben al fitxer ocult `hotel.enu`, exclòs amb `.gitignore`.
- Es pot ampliar la interfície amb funcionalitats extres (esborrar usuari, restablir contrasenya, etc.).

## Autors

**Grup 12 - AEI**  
Cicle Formatiu de Grau Superior d’Administració de Sistemes Informàtics i Xarxes (ASIX)  
INS Sa Palomera – Curs 2024/2025

---

## 🔗 Repositori principal del projecte
📁 [Veure projecte principal a GitHub](../README.md)
