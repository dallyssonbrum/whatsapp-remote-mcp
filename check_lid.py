import sqlite3
conn = sqlite3.connect(r"C:\Users\brum9\whatsapp-mcp-server\whatsapp-bridge\store\messages.db")
query = "SELECT timestamp, content FROM messages WHERE chat_jid LIKE '%213618872287271%' ORDER BY timestamp DESC LIMIT 5"
rows = conn.execute(query).fetchall()
print(f"--- MENSAGENS DO JID IDENTIFICADO ({213618872287271}) ---")
for r in rows:
    print(f"[{r[0]}] {r[1]}")
conn.close()
