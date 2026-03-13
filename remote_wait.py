import time
import os
import sys
import re

BRUM_IDS = ["213618872287271", "554791880322"]
LOG_PATH = "whatsapp-bridge/bridge_log.txt"

print(f"--- Monitoramento Remoto v19 (Keep-Alive + Deactivation) ---")
print(f"Sincronizado com: {BRUM_IDS}")
sys.stdout.flush()

processed_lines = set()

# Pre-carrega histórico
if os.path.exists(LOG_PATH):
    with open(LOG_PATH, "rb") as f:
        content = f.read().decode("utf-8", "ignore")
        for line in content.splitlines():
            processed_lines.add(line.strip())

print("Aguardando seu comando... (Envie uma nova mensagem agora)")
sys.stdout.flush()

start_time = time.time()
last_status_time = time.time()

try:
    while True:
        # Mensagem de Keep-Alive a cada 60 segundos para evitar timeout da ferramenta
        current_time = time.time()
        if current_time - last_status_time > 60:
            uptime = int((current_time - start_time) / 60)
            print(f"... Monitoramento ativo (Uptime: {uptime} min) ...")
            sys.stdout.flush()
            last_status_time = current_time

        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, "rb") as f:
                content = f.read().decode("utf-8", "ignore")
                lines = content.splitlines()
                
                for line in lines:
                    original_line = line.strip()
                    if not original_line or original_line in processed_lines:
                        continue
                    
                    # LOG_RAW para acompanhamento em tempo real
                    print(f"LOG_RAW: {original_line}")
                    sys.stdout.flush()
                    processed_lines.add(original_line)
                    
                    # 1. Limpa a linha deixando apenas Letras e Números (remove espaços e lixo invisível)
                    alnum_only = re.sub(r"[^a-zA-Z0-9]", "", original_line)
                    
                    # 2. Ignora logs técnicos conhecidos
                    if any(x in alnum_only for x in ["Usingexisting", "messagesent", "ClientINFO", "ConnectedtoWhatsApp"]):
                        continue

                    # 3. Limpa a linha deixando APENAS números para conferir seu ID
                    numbers_only = re.sub(r"\D", "", original_line)
                    
                    for bid in BRUM_IDS:
                        if bid in original_line or bid in numbers_only:
                            # Detectar protocolo de desativação
                            if "Encerrar Controle Remoto" in original_line:
                                print("\n" + "X"*50)
                                print("!!! DESATIVAÇÃO REMOTA SOLICITADA PELO WHATSAPP !!!")
                                print("X"*50 + "\n")
                                sys.stdout.flush()
                                sys.exit(99) # Código de saída especial para desativação

                            # Se chegamos aqui, é uma mensagem real!
                            print("\n" + "!"*50)
                            print(f"!!! COMANDO CAPTURADO COM SUCESSO: {original_line}")
                            print("!"*50 + "\n")
                            sys.stdout.flush()
                            sys.exit(0)
        
        time.sleep(0.5)
except Exception as e:
    print(f"Erro: {e}")
    sys.stdout.flush()
