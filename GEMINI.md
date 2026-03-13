# Gemini CLI - Manual de Boot do Terminal Remoto AUTÔNOMO (Brum)

Este projeto foi configurado para que o Brum possa operar o terminal do seu computador remotamente via WhatsApp de forma 100% autônoma (Modo YOLO).

## Procedimento de Inicialização:
1.  **Abrir o Terminal (PowerShell) como Administrador.**
2.  **Iniciar o Gemini CLI no Modo Autônomo:**
    ```powershell
    gemini --approval-mode yolo
    ```
    *(Isso desabilita o prompt de confirmação "1" para todos os comandos).*

## Após o Início, o Agente Gemini executará:
1.  **WhatsApp Bridge (Go):**
    - Ir para: `C:\Users\brum9\whatsapp-mcp-server\whatsapp-bridge`
    - Definir `$env:CGO_ENABLED=1`
    - Rodar: `go run main.go` com saída para `bridge_log.txt`.
2.  **Modo de Vigilância Ativa:**
    - O Agente Gemini iniciará o script `remote_wait.py` para aguardar comandos do Brum.

## Segurança e Autonomia:
- **Modo YOLO:** Ativado via flag `--approval-mode yolo` para permitir que o Brum controle o PC pelo WhatsApp sem precisar tocar no teclado do computador.
- **Identidades Autorizadas:** 554791880322 (Brum) e 213618872287271 (LID).
