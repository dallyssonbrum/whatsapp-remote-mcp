import sqlite3
conn = sqlite3.connect(r"C:\Users\brum9\whatsapp-mcp-server\whatsapp-bridge\store\messages.db")
# Busca mensagens onde o chat_jid OU o sender seja o seu número
query = "SELECT timestamp, sender, is_from_me, content FROM messages WHERE chat_jid LIKE '%554791880322%' OR sender LIKE '%554791880322%' ORDER BY timestamp DESC LIMIT 10"
rows = conn.execute(query).fetchall()
print(f"--- MENSAGENS DO USUARIO (554791880322) NO BANCO ATUAL ---")
if not rows:
    print("Nenhuma mensagem encontrada para este numero no banco de dados atual.")
for r in rows:
    origem = "BOT" if r[2] else "VOCE"
    print(f"[{r[0]}] {origem}: {r[3]}")
conn.close()
