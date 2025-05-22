"""
Fitxer: telegram.py

"""
import requests
from llibreries.bd import connectar_bd

BOT_TOKEN = '7246405871:AAEBqldoLZLtxszGD3DgcluM3Y0sTG21fxk'

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

"""
import requests

TOKEN = '7246405871:AAEBqldoLZLtxszGD3DgcluM3Y0sTG21fxk'  
res = requests.get(f'https://api.telegram.org/bot{TOKEN}/getUpdates')
print(res.json())
"""