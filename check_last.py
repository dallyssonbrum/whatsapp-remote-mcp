import sqlite3
import os

DB_PATH = os.getenv("WHATSAPP_DB_PATH", "whatsapp-bridge/store/messages.db")
conn = sqlite3.connect(DB_PATH)
rows = conn.execute("SELECT sender, content, timestamp FROM messages WHERE is_from_me = 0 ORDER BY timestamp DESC LIMIT 10").fetchall()
print("--- LOG DE MENSAGENS NO BANCO ---")
for r in rows:
    print(f"[{r[2]}] {r[0]}: {r[1]}")
conn.close()
