import time
import requests
import os

# --- CONFIGURAÇÃO ---
LOG_PATH = r"whatsapp-bridge\bridge_log.txt"
RECIPIENT_JID = os.getenv("MY_WHATSAPP_JID", "YOUR_PHONE_NUMBER@s.whatsapp.net")
API_URL = "http://localhost:8080/api/send"

def send_msg(text):
    try:
        requests.post(API_URL, json={"recipient": RECIPIENT_JID, "message": text}, timeout=5)
    except:
        pass

if os.path.exists(LOG_PATH):
    size = os.path.getsize(LOG_PATH)
else:
    size = 0

print(f"Monitoramento Ativo. Ouvindo {LOG_PATH} para o JID {RECIPIENT_JID}...")

while True:
    try:
        if not os.path.exists(LOG_PATH):
            time.sleep(1)
            continue
            
        with open(LOG_PATH, 'r', encoding='utf-8', errors='ignore') as f:
            f.seek(size)
            lines = f.readlines()
            size = f.tell()
            
            for line in lines:
                # Extrai o ID numérico do JID para busca flexível
                my_number = RECIPIENT_JID.split("@")[0]
                if my_number in line and ":" in line:
                    if "Li seu comando" in line or "Monitoramento ultra-estavel" in line:
                        continue
                        
                    parts = line.split(":")
                    if len(parts) > 3:
                        content = parts[-1].strip()
                        if content:
                            print(f"Detectado via LOG: {content}")
                            send_msg(f"Comando recebido via log: '{content}'. Monitoramento ativo!")
    except Exception as e:
        pass
    time.sleep(1)
