import sqlite3
import time
import os

DB_PATH = os.getenv("WHATSAPP_DB_PATH", "whatsapp-bridge/store/messages.db")
# O seu JID pessoal baseado no número fornecido
TARGET_JID = os.getenv("TARGET_JID", "YOUR_WHATSAPP_JID@s.whatsapp.net") 

def get_last_msg_id():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM messages WHERE sender LIKE ? ORDER BY timestamp DESC LIMIT 1", (f"%{TARGET_JID.split('@')[0]}%",))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None
    except:
        return None

last_id = get_last_msg_id()
print(f"Monitoramento RESTRICTO iniciado para: {TARGET_JID}. Ultima msg ID: {last_id}")

while True:
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Busca apenas mensagens do SEU número específico
        cursor.execute("SELECT id, sender, content, timestamp FROM messages WHERE (sender LIKE ? OR chat_jid LIKE ?) AND is_from_me = 0 ORDER BY timestamp DESC LIMIT 1", (f"%{TARGET_JID.split('@')[0]}%", f"%{TARGET_JID.split('@')[0]}%"))
        row = cursor.fetchone()
        conn.close()

        if row and row[0] != last_id:
            msg_id, sender, content, ts = row
            last_id = msg_id
            print(f"--- NOVO COMANDO DE VOCE ({sender}) ---")
            print(f"Conteudo: {content}")
            print(f"Horario: {ts}")
            
    except Exception as e:
        pass
    
    time.sleep(5) # Verificação mais frequente (5s)
