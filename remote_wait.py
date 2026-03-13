import time
import os

# --- CONFIGURAÇÃO ---
# O JID (ID do WhatsApp) deve ser o seu número seguido de @s.whatsapp.net ou @lid
# Se preferir, crie um arquivo .env ou defina a variável de ambiente MY_WHATSAPP_JID
MY_JID = os.getenv("MY_WHATSAPP_JID", "554791880322@s.whatsapp.net") # Default JID
LOG_PATH = r"whatsapp-bridge\bridge_log.txt"

if os.path.exists(LOG_PATH):
    size = os.path.getsize(LOG_PATH)
else:
    size = 0

print(f"--- Monitoramento Remoto Ativado para JID: {MY_JID} ---")
print("Aguardando comando via WhatsApp...")

last_heartbeat = time.time()

while True:
    # Heartbeat a cada 60 segundos para evitar timeout do terminal/agente
    if time.time() - last_heartbeat > 60:
        print("[Sinal de Vida] Aguardando novos comandos...")
        last_heartbeat = time.time()

    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r", encoding="utf-8", errors="ignore") as f:
            f.seek(size)
            lines = f.readlines()
            size = f.tell()
            for line in lines:
                # Extrai o ID numérico do JID para busca flexível
                my_number = MY_JID.split("@")[0]
                if my_number in line and ":" in line:
                    if "Message sent" in line or "Received request" in line:
                        continue
                    parts = line.split(":")
                    if len(parts) > 3:
                        cmd = parts[-1].strip()
                        print(f"--- NOVO COMANDO RECEBIDO: {cmd} ---")
                        
                        # Comando Especial para Sair
                        if "encerrar controle remoto" in cmd.lower():
                            print("Comando de encerramento recebido. Desligando...")
                            exit(0)
                        
                        # Sai do loop para o Agente processar o comando
                        exit(0)
    time.sleep(2)
