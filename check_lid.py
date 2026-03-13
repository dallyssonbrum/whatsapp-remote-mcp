import sqlite3
import os

DB_PATH = os.getenv("WHATSAPP_DB_PATH", "whatsapp-bridge/store/messages.db")
TARGET_LID = os.getenv("TARGET_LID", "YOUR_LID_NUMBER")

conn = sqlite3.connect(DB_PATH)
query = f"SELECT timestamp, content FROM messages WHERE chat_jid LIKE '%{TARGET_LID}%' ORDER BY timestamp DESC LIMIT 5"
rows = conn.execute(query).fetchall()
print(f"--- MENSAGENS DO JID IDENTIFICADO ({TARGET_LID}) ---")
for r in rows:
    print(f"[{r[0]}] {r[1]}")
conn.close()
