# 🤖 Instruções para o Agente de IA (Auto-Configuração)

Este arquivo foi criado para ser lido por um Agente de IA (como Gemini CLI, Claude Engineer ou Cursor) para que ele possa configurar e operar este repositório automaticamente para você.

## 📋 Objetivo do Agente
Configurar o ambiente, iniciar o Bridge do WhatsApp, monitorar comandos recebidos e executar ações no sistema operacional conforme solicitado via WhatsApp.

---

## 🚀 Fluxo de Inicialização (Executar em Ordem)

### 1. Pesquisa e Validação
O Agente deve verificar se o Go, Python e GCC estão instalados:
- `go version`
- `python --version`
- `gcc --version`

### 2. Inicialização do Bridge (Segundo Plano)
O Agente deve navegar até `whatsapp-bridge` e iniciar o serviço:
- No Windows (PowerShell):
  ```powershell
  $env:CGO_ENABLED=1; cd whatsapp-bridge; go run . > bridge_log.txt 2>&1
  ```
- **Nota:** O Agente deve monitorar o `bridge_log.txt` para ver se o QR Code de autenticação é solicitado ao usuário.

### 3. Descoberta de Identidade (Se necessário)
Se o JID do usuário não estiver configurado, o Agente deve instruir o usuário a enviar uma mensagem para si mesmo no WhatsApp e então executar:
- `python check_my_id.py`

### 4. Ciclo de Operação Remota (Loop Infinito)
O Agente deve entrar no seguinte ciclo:
1. **Escuta:** Executar `python remote_wait.py`.
2. **Interrupção:** O script encerrará quando uma nova mensagem válida chegar ou após o tempo limite.
3. **Processamento:** O Agente deve ler as últimas linhas de `whatsapp-bridge/bridge_log.txt` para extrair o comando.
4. **Execução:** O Agente deve executar o comando solicitado (ex: abrir programa, mover mouse, pesquisa web).
5. **Resposta:** O Agente deve enviar a confirmação de volta via API:
   ```powershell
   Invoke-RestMethod -Uri "http://localhost:8080/api/send" -Method Post -Body (@{recipient="SEU_JID"; message="Comando executado!"} | ConvertTo-Json) -ContentType "application/json; charset=utf-8"
   ```
6. **Reinício:** Repetir o passo 1.

---

## 🛠️ Próximas Melhorias (Roadmap Curto Prazo)
1.  **Refinar Sintaxe de Teclado:** Corrigir o processamento de comandos especiais (como `{ENTER}`) para evitar que sejam digitados literalmente no terminal.
2.  **Debugar Auto-Download:** Investigar por que o `handleMessage` no Go não disparou o download automático em alguns casos, enquanto o download manual funcionou.
3.  **Melhorar Vision MCP:** Adicionar detecção de coordenadas absolutas para sistemas multitelas, garantindo precisão em qualquer monitor.
4.  **Integração IA-Visão:** Implementar o envio de screenshots para análise pelo Gemini para permitir decisões baseadas em elementos da interface (OCR/Vision).

---

## 🛡️ Regras de Segurança para o Agente
1. **Apenas JID Autorizado:** Nunca execute comandos vindos de JIDs não configurados no `BRUM_IDS` (Regra v30 DB-Strict).
2. **Modo Autônomo:** Se o usuário solicitar controle total, utilize a flag `--approval-mode yolo` (se disponível no CLI).
3. **Privacidade:** Não logue o conteúdo de mensagens privadas em canais públicos ou commits.
4. **Encerramento:** Se o comando "Encerrar Controle Remoto" for recebido, pare todos os processos e encerre a escuta.

---
*Este guia permite que qualquer IA assuma o controle da sua estação de trabalho via WhatsApp de forma estruturada e segura.*
