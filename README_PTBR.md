# Servidor MCP de WhatsApp (Edição Customizada)

Este é um servidor Model Context Protocol (MCP) para o WhatsApp.

Com ele, você pode pesquisar e ler suas mensagens pessoais (incluindo imagens, vídeos, documentos e áudios), buscar contatos e enviar mensagens para indivíduos ou grupos. Você também pode enviar arquivos de mídia.

Ele se conecta diretamente à sua **conta pessoal do WhatsApp** via API Web multidevice (usando a biblioteca [whatsmeow](https://github.com/tulir/whatsmeow)). Todas as suas mensagens são armazenadas localmente em um banco de dados SQLite e apenas enviadas para um LLM (como o Claude ou Gemini) quando o agente as acessa através das ferramentas (que você controla).

> **Atenção:** Como qualquer servidor MCP, o WhatsApp MCP está sujeito a riscos de injeção de prompt que podem levar à exfiltração de dados privados. Use com responsabilidade.

---

## 🚀 Modo Controle Remoto (Edição Customizada)

Esta versão inclui um recurso personalizado de **Controle Remoto** que permite controlar seu PC através de mensagens do WhatsApp.

### Como usar:

1.  **Inicie o Bridge**: Rode o bridge em Go em um terminal (`go run .` dentro da pasta `whatsapp-bridge`).
2.  **Encontre seu JID**: Para descobrir seu ID único do WhatsApp (JID/LID), envie qualquer mensagem para você mesmo no WhatsApp e depois execute:
    ```bash
    python check_my_id.py
    ```
    Copie o JID que corresponde ao seu número (ex: `123456789@s.whatsapp.net` ou `123456789@lid`).
3.  **Configure seu JID**: Coloque esse valor na variável `MY_JID` dentro do arquivo `remote_wait.py` ou use uma variável de ambiente:
    ```powershell
    $env:MY_WHATSAPP_JID = "seu_jid_aqui"
    ```
4.  **Inicie o Monitoramento**: Rode o script Python em outro terminal:
    ```bash
    python remote_wait.py
    ```

4.  **Envie Comandos**: Envie mensagens do seu celular para o seu próprio número. O agente detectará os comandos no log e os executará (ex: "Abrir Google", "Mover o mouse", "Verificar espaço em disco").

### Recursos de Segurança:
*   **Filtro de JID**: O script apenas escuta o número específico que você configurou.
*   **Heartbeat (Sinal de Vida)**: Envia uma mensagem ao terminal a cada 60 segundos para evitar que a sessão expire.
*   **Desligamento Remoto**: Envie "Encerrar Controle Remoto" para parar o monitoramento à distância.

---

## 🤖 Usando com ChatGPT Plus / OpenAI

Se você é usuário do **ChatGPT Plus**, você também pode usar este projeto! Embora o aplicativo desktop do ChatGPT ainda não suporte MCP nativamente como o Claude, você tem três ótimas opções:

### 1. Via Cursor ou VS Code (Recomendado para Desenvolvedores)
Se você usa o editor **Cursor** ou a extensão **Roo Code (antigo Claude Dev)** no VS Code:
- Configure o servidor MCP nas configurações.
- Selecione o seu modelo da OpenAI (GPT-4o, etc.).
- O editor usará as ferramentas MCP automaticamente para interagir com seu WhatsApp.

### 2. Via Custom GPT Actions (Sem necessidade de código)
Você pode criar um **Custom GPT** na sua conta do ChatGPT Plus:
1. Use uma ferramenta como o [ngrok](https://ngrok.com/) para expor seu bridge local (`localhost:8080`) para a internet.
2. Nas configurações de "Actions" do seu Custom GPT, importe o esquema da API fornecido pelo bridge.
3. Seu Custom GPT agora poderá enviar e ler mensagens diretamente da interface do ChatGPT (web ou mobile).

### 3. Via Pontes MCP-para-OpenAI
Existem ferramentas da comunidade que permitem "conectar" qualquer servidor MCP à interface do ChatGPT. Verifique a [lista da comunidade MCP](https://modelcontextprotocol.io/community) para os conectores mais recentes.

---

## Instalação

### Pré-requisitos

*   **Go** (Linguagem de programação)
*   **Python 3.6+**
*   **Anthropic Claude Desktop** ou **Cursor**
*   **UV** (Gerenciador de pacotes Python)
*   **FFmpeg** (*Opcional*) - Apenas para conversão automática de áudio.

### Passos

1.  **Clone este repositório**
    ```bash
    git clone https://github.com/dallyssonbrum/whatsapp-remote-mcp.git
    cd whatsapp-remote-mcp
    ```

2.  **Inicie o Bridge do WhatsApp**
    Vá até a pasta `whatsapp-bridge` e rode:
    ```bash
    go run .
    ```
    Na primeira vez, um QR Code aparecerá no terminal. Escaneie com seu WhatsApp para autenticar.

3.  **Conecte ao Servidor MCP**
    Adicione a configuração do servidor ao seu `claude_desktop_config.json` ou `mcp.json` do Cursor, apontando para o caminho correto do `uv` e do diretório do projeto.

---

## Compatibilidade com Windows

Se você estiver no Windows, o `go-sqlite3` requer que o **CGO esteja habilitado**.

1.  **Instale um compilador C**: Recomendamos o [MSYS2](https://www.msys2.org/) (MinGW).
2.  **Habilite o CGO e rode**:
    ```bash
    go env -w CGO_ENABLED=1
    go run .
    ```

## Ferramentas Disponíveis (Ferramentas MCP)

O agente terá acesso às seguintes funções:
*   `search_contacts`: Buscar contatos.
*   `list_messages`: Listar mensagens com filtros.
*   `send_message`: Enviar mensagens de texto.
*   `send_file`: Enviar imagens, vídeos ou documentos.
*   `download_media`: Baixar arquivos recebidos no WhatsApp.

---

## Detalhes Técnicos

1. O Claude/Gemini envia requisições para o servidor Python MCP.
2. O servidor MCP consulta o Bridge em Go ou o banco SQLite.
3. O Bridge em Go acessa a API do WhatsApp e mantém o banco de dados atualizado.
4. Os dados fluem de volta para o agente de IA.

---

## Solução de Problemas

*   **QR Code não aparece**: Certifique-se de que seu terminal suporta renderização de caracteres.
*   **Banco de dados travado (SQLITE_BUSY)**: No Windows, evite que dois processos tentem escrever no banco ao mesmo tempo. Use o monitoramento via logs (`remote_wait.py`) para evitar conflitos.

---
*Desenvolvido pela Comunidade & Gemini CLI.*
