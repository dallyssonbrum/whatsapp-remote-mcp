# Gemini CLI - Manual de Boot do Terminal Remoto AUTÔNOMO

Este projeto foi configurado para operar o terminal do seu computador remotamente via WhatsApp de forma 100% autônoma (Modo YOLO).

## Procedimento de Inicialização:
1.  **Abrir o Terminal (PowerShell) como Administrador.**
2.  **Iniciar o Gemini CLI no Modo Autônomo:**
    ```powershell
    gemini --approval-mode yolo
    ```
    *(Isso desabilita o prompt de confirmação para todos os comandos).*

## Após o Início, o Agente Gemini executará:
1.  **WhatsApp Bridge (Go):**
    - Ir para a pasta `whatsapp-bridge`
    - Definir a variável de ambiente `CGO_ENABLED=1`
    - Rodar o bridge em Go redirecionando a saída para `bridge_log.txt`.
2.  **Verificação de Conexão:**
    - O Agente Gemini deve validar se o log mostra "Logged in" ou se o QR Code já foi escaneado.
    - Se o Bridge estiver pedindo QR Code, o monitoramento remoto não deve ser iniciado até que o usuário escaneie.
3.  **Modo de Vigilância Ativa:**
    - Após a confirmação de conexão, o Agente Gemini iniciará o script `remote_wait.py` para aguardar comandos via WhatsApp.

## Segurança e Autonomia:
- **Modo YOLO:** Ativado via flag `--approval-mode yolo` para permitir o controle do PC pelo WhatsApp sem precisar tocar no teclado do computador.
- **Configuração de Variáveis de Ambiente:**
  - `MY_WHATSAPP_JID`: Seu JID pessoal (ex: `YOUR_PHONE_NUMBER@s.whatsapp.net`).
  - `WHATSAPP_DB_PATH`: Caminho para o banco de dados (default: `whatsapp-bridge/store/messages.db`).
  - `TARGET_PHONE`: Número de telefone para filtros (ex: `YOUR_PHONE_NUMBER`).
  - `TARGET_LID`: ID LID para filtros (ex: `YOUR_LID_NUMBER`).
- **Identidades Autorizadas:** Configure o seu JID através da variável de ambiente `MY_WHATSAPP_JID` ou diretamente nos scripts.

## Histórico de Versões Estáveis:
- **Versão Estável Controle Remoto Brum (v30)**: O script `remote_wait.py` agora utiliza a regra de **Banco de Dados Estrita**. O comando só é válido se `is_from_me = 1` E `chat_jid == sender` (Self-Chat real no SQLite). Esta lógica é imune a caracteres de terminal corrompidos e à ordem das linhas de log técnicas. Mantém Keep-Alive e Brute Force Match. Esta é a nova base de segurança para uso remoto.
