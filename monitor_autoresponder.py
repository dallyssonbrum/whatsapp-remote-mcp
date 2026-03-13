import sqlite3
import time
import requests
import os

DB_PATH = os.getenv("WHATSAPP_DB_PATH", "file:whatsapp-bridge/store/messages.db?mode=ro")
RECIPIENT_JID = os.getenv("RECIPIENT_JID", "554791880322@s.whatsapp.net")
# Filtro por numeros chave
MONITOR_NUMBERS = [
    os.getenv("TARGET_PHONE", "554791880322"), 
    os.getenv("TARGET_LID", "213618872287271")
]
API_URL = os.getenv("BRIDGE_API_URL", "http://localhost:8080/api/send")

def send_msg(text):
    try:
        requests.post(API_URL, json={"recipient": RECIPIENT_JID, "message": text}, timeout=5)
    except:
        pass

def get_last_msg():
    try:
        conn = sqlite3.connect(DB_PATH, uri=True)
        conn.execute("PRAGMA wal_checkpoint(PASSIVE)")
        # Filtro hibrido usando LIKE para maior flexibilidade
        query = "SELECT id, chat_jid, content FROM messages WHERE (chat_jid LIKE ? OR chat_jid LIKE ?) AND is_from_me = 0 ORDER BY timestamp DESC LIMIT 1"
        res = conn.execute(query, (f"%{MONITOR_NUMBERS[0]}%", f"%{MONITOR_NUMBERS[1]}%")).fetchone()
        conn.close()
        return res
    except:
        return None

last_id = get_last_msg()[0] if get_last_msg() else None
print(f"Monitoramento FLEXIVEL iniciado. Ouvindo {MONITOR_NUMBERS}. Ultimo ID: {last_id}")

while True:
    try:
        current = get_last_msg()
        if current and current[0] != last_id:
            msg_id, jid, content = current
            last_id = msg_id
            print(f"Detectado: {content}")
            send_msg(f"Fabricio, seu comando '{content}' foi detectado com sucesso pelo novo filtro flexivel!")
    except:
        pass
    time.sleep(2)
