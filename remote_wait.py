import time
import os
import sys
import re
import sqlite3
from datetime import datetime

# Configurações
BRUM_IDS = ["213618872287271", "554791880322"]
DB_PATH = "whatsapp-bridge/store/messages.db"

print(f"--- Monitoramento Remoto v30 (Estrito via Banco de Dados) ---")
print(f"Sincronizado com: {BRUM_IDS}")
print(f"Regra: APENAS comandos enviados no seu próprio chat (Self-Chat).")
sys.stdout.flush()

processed_msg_ids = set()

def sanitize_string(s):
    # Remove tudo que não for letra ou número para "Brute Force Match"
    return re.sub(r'[^a-zA-Z0-9]', '', s).lower()

TARGET_COMMAND = sanitize_string("Encerrar Controle Remoto")

def get_latest_self_command():
    """Consulta o banco de dados em busca do último comando válido no Self-Chat."""
    if not os.path.exists(DB_PATH):
        return None, None, None
    
    try:
        # Abre em modo Read-Only para evitar conflitos com o Bridge Go no Windows
        conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
        cursor = conn.cursor()
        
        # Busca a última mensagem enviada por mim
        # A regra 'chat_jid = sender' garante que é um Self-Chat
        query = """
            SELECT id, content, sender, chat_jid 
            FROM messages 
            WHERE is_from_me = 1 
            ORDER BY timestamp DESC LIMIT 1
        """
        cursor.execute(query)
        row = cursor.fetchone()
        conn.close()
        
        if row:
            msg_id, content, sender, chat_jid = row
            
            # Limpa JIDs para comparação (remove @s.whatsapp.net ou @lid)
            clean_sender = re.sub(r'[^0-9]', '', sender)
            clean_chat = re.sub(r'[^0-9]', '', chat_jid)
            
            # Validação Estrita: 
            # 1. Remetente deve ser um dos IDs do Brum
            # 2. Destinatário (Chat) deve ser o próprio Remetente (Self-Chat)
            if clean_sender in BRUM_IDS and clean_sender == clean_chat:
                return msg_id, content, clean_sender
            
        return None, None, None
    except Exception as e:
        # Silencioso para não poluir o terminal, mas loga erro se for crítico
        if "locked" not in str(e).lower():
            print(f"[Erro DB]: {e}")
        return None, None, None

# Pre-carrega a última mensagem para não executar comandos antigos ao iniciar
last_id, _, _ = get_latest_self_command()
if last_id:
    processed_msg_ids.add(last_id)

print("Aguardando novas mensagens no seu Self-Chat...")
sys.stdout.flush()

last_keepalive = time.time()

try:
    while True:
        # Keep-Alive: evita timeout de 5 minutos do Gemini CLI
        now = time.time()
        if now - last_keepalive > 60:
            print(f"[Keep-Alive] {time.strftime('%H:%M:%S')} - Aguardando comando no seu chat...")
            sys.stdout.flush()
            last_keepalive = now

        # Consulta o Banco
        msg_id, content, sender_jid = get_latest_self_command()
        
        if msg_id and msg_id not in processed_msg_ids:
            processed_msg_ids.add(msg_id)
            
            print(f"\n✅ [COMANDO DETECTADO]: '{content}' (via Self-Chat: {sender_jid})")
            
            # Validação do comando de encerramento (Brute Force Match)
            sanitized_content = sanitize_string(content)
            if TARGET_COMMAND in sanitized_content:
                print("\n!!! DESATIVACAO REMOTA SOLICITADA !!!\n")
                sys.stdout.flush()
                sys.exit(99)

            print("\n" + "!"*50)
            print(f"!!! COMANDO CAPTURADO COM SUCESSO !!!")
            print("!"*50 + "\n")
            sys.stdout.flush()
            sys.exit(0)
        
        time.sleep(1) # Intervalo de 1 segundo entre consultas ao banco

except KeyboardInterrupt:
    print("\nMonitoramento encerrado pelo usuário.")
except Exception as e:
    print(f"Erro Fatal no Loop: {e}")
    sys.stdout.flush()
