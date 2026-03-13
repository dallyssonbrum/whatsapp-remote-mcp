import sqlite3
conn = sqlite3.connect(r"C:\Users\brum9\whatsapp-mcp-server\whatsapp-bridge\store\messages.db")
rows = conn.execute("SELECT sender, content, timestamp FROM messages WHERE is_from_me = 0 ORDER BY timestamp DESC LIMIT 10").fetchall()
print("--- LOG DE MENSAGENS NO BANCO ---")
for r in rows:
    print(f"[{r[2]}] {r[0]}: {r[1]}")
conn.close()
