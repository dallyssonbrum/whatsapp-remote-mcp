import sqlite3
import os

DB_PATH = os.getenv("WHATSAPP_DB_PATH", "whatsapp-bridge/store/messages.db")
conn = sqlite3.connect(DB_PATH)
row = conn.execute("SELECT id, chat_jid, sender, content, timestamp FROM messages WHERE content LIKE '%agora vai%' ORDER BY timestamp DESC LIMIT 1").fetchone()
if row:
    print(f"MENSAGEM ENCONTRADA: ID={row[0]} | CHAT_JID={row[1]} | SENDER={row[2]} | CONTENT={row[3]} | TS={row[4]}")
else:
    print("MENSAGEM 'agora vai' NAO ENCONTRADA NO BANCO.")
conn.close()
