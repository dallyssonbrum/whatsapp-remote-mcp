import sqlite3
import os

DB_PATH = os.getenv("WHATSAPP_DB_PATH", "whatsapp-bridge/store/messages.db")
TARGET_PHONE = os.getenv("TARGET_PHONE", "554791880322")

conn = sqlite3.connect(DB_PATH)
# Busca mensagens onde o chat_jid OU o sender seja o seu número
query = f"SELECT timestamp, sender, is_from_me, content FROM messages WHERE chat_jid LIKE '%{TARGET_PHONE}%' OR sender LIKE '%{TARGET_PHONE}%' ORDER BY timestamp DESC LIMIT 10"
rows = conn.execute(query).fetchall()
print(f"--- MENSAGENS DO USUARIO ({TARGET_PHONE}) NO BANCO ATUAL ---")
if not rows:
    print("Nenhuma mensagem encontrada para este numero no banco de dados atual.")
for r in rows:
    origem = "BOT" if r[2] else "VOCE"
    print(f"[{r[0]}] {origem}: {r[3]}")
conn.close()
