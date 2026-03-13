import os
import re

LOG_PATH = r"whatsapp-bridge/bridge_log.txt"

def find_my_jid():
    if not os.path.exists(LOG_PATH):
        print(f"Erro: O arquivo de log '{LOG_PATH}' não foi encontrado.")
        print("Certifique-se de que o bridge em Go está rodando.")
        return

    print("--- Buscando seu JID no log do WhatsApp ---")
    print("Dica: Mande qualquer mensagem para você mesmo pelo WhatsApp para aparecer no log.")
    
    with open(LOG_PATH, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
        
    jids = []
    # Busca por padrões de JID no log (números@s.whatsapp.net ou números@lid)
    pattern = re.compile(r'(\d+@(s\.whatsapp\.net|lid))')
    
    for line in reversed(lines):
        match = pattern.search(line)
        if match:
            jid = match.group(1)
            if jid not in jids:
                jids.append(jid)
        
    if jids:
        print("\nJIDs encontrados recentemente no log (do mais novo para o mais antigo):")
        for i, jid in enumerate(jids[:5], 1):
            print(f"{i}. {jid}")
        print("\nCopie o JID acima que corresponde ao seu número e use-o na configuração!")
    else:
        print("\nNenhum JID encontrado ainda. Mande uma mensagem no WhatsApp e tente novamente.")

if __name__ == "__main__":
    find_my_jid()
