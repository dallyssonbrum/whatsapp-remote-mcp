import sqlite3
import time
import requests

DB_PATH = r"C:\Users\brum9\whatsapp-mcp-server\whatsapp-bridge\store\messages.db"

def get_last_msg():
    try:
        conn = sqlite3.connect(DB_PATH)
        res = conn.execute("SELECT id, content FROM messages WHERE is_from_me = 0 ORDER BY timestamp DESC LIMIT 1").fetchone()
        conn.close()
        return res
    except Exception as e:
        print(f"ERRO: {e}")
        return None

last_id = get_last_msg()[0] if get_last_msg() else None
print(f"Monitor Simples iniciado. Ultimo ID: {last_id}")

while True:
    current = get_last_msg()
    if current and current[0] != last_id:
        last_id = current[0]
        print(f"MENSAGEM DETECTADA: {current[1]}")
        # Tenta responder via bridge
        try:
            requests.post("http://localhost:8080/api/send", json={"recipient": "5547991880322@s.whatsapp.net", "message": f"Respondendo via monitor simples: {current[1]}"}, timeout=5)
        except:
            pass
    time.sleep(2)
