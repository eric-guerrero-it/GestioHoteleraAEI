"""
Fitxer: telegram.py

Conté les funcions per gestionar l'enviament de notificacions als clients mitjançant Telegram.
Inclou la càrrega segura del token des d’un fitxer extern (telegram.enu), la consulta del chat_id
a la base de dades i l’enviament de missatges a usuaris amb comptes vinculats.

Funcionalitats:
- Llegeix automàticament el token del bot des del fitxer 'telegram.enu'.
- Recupera el chat_id del client des de la taula 'client' de la base de dades.
- Envia missatges mitjançant la Telegram Bot API a través d’una crida HTTP.

Pensat per ser reutilitzat des de qualsevol mòdul del sistema (check-in, reserva, serveis...).
"""
import requests
import os
from llibreries.bd import connectar_bd


def carregar_token():
    """
    Llegeix el token del fitxer telegram.enu (format: BOT_TOKEN=...)
    """
    ruta = os.path.join(os.path.dirname(__file__), "telegram.enu")
    with open(ruta, "r") as f:
        for linia in f:
            if linia.startswith("BOT_TOKEN="):
                return linia.strip().split("=", 1)[1]
    raise ValueError("No s'ha trobat el token al fitxer telegram.enu")


BOT_TOKEN = carregar_token()

def obtenir_chat_id(dni_client):
    conn = connectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id FROM client WHERE dni = %s", (dni_client,))
    resultat = cursor.fetchone()
    conn.close()
    return resultat[0] if resultat else None


def enviar_missatge_telegram(dni_client, missatge):
    chat_id = obtenir_chat_id(dni_client)
    if not chat_id:
        print(f"[Telegram] No s'ha trobat el chat_id per al client amb DNI {dni_client}")
        return False

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': missatge
    }
    res = requests.post(url, data=data)
    return res.status_code == 200
