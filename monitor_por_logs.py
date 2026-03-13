import time
import requests
import os

LOG_PATH = r"C:\Users\brum9\whatsapp-mcp-server\whatsapp-bridge\bridge_log.txt"
RECIPIENT_JID = "554791880322@s.whatsapp.net"
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

print(f"Monitoramento Brum Ativo. Ouvindo {LOG_PATH}...")

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
                if ("213618872287271" in line or "554791880322" in line) and (":" in line):
                    if "Li seu comando" in line or "Monitoramento ultra-estavel" in line:
                        continue
                        
                    parts = line.split(":")
                    if len(parts) > 3:
                        content = parts[-1].strip()
                        if content:
                            print(f"Detectado via LOG: {content}")
                            send_msg(f"Brum! Li seu comando via log (estavel): '{content}'. Monitoramento 100% ativo!")
    except Exception as e:
        pass
    time.sleep(1)
