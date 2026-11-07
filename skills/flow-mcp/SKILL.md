---
name: flow-mcp
description: CAMINHO OFICIAL do Google Flow. Gera imagem e vídeo no Google Flow (Nano Banana, Veo 3.1, Omni Flash) pelo MCP google-flow (ferramentas mcp__google-flow__*), com imagem de referência e frame inicial nativos, teste sem gastar crédito (auto_confirm false), retomada de geração (resume) e Scene Builder (estender vídeo em blocos de 7 s). Use SEMPRE que qualquer skill ou pedido precisar gerar imagem ou vídeo no Flow, testar a geração antes de gastar ou estender um vídeo do Flow. A skill flow-video-playwright (flow.sh + gflow) é só a reserva, quando esta falhar.
---

# Google Flow pelo MCP google-flow — CAMINHO OFICIAL (desde 07/11/2026, ordem da dona)

**Toda geração no Flow começa aqui.** A `flow-video-playwright` (flow.sh + gflow) é a **reserva**: usar só quando
este caminho falhar (MCP fora do ar, `UI_NOT_FOUND` que não dá para corrigir na hora, login do Chrome do MCP
caído sem a dona disponível) e dizer à dona que caiu na reserva. Exceção: scripts que já chamam o `flow.sh` sozinhos
(ex.: `tiktok-shop/scripts/pov-flow.sh`, `modelar-perfil-social/scripts/lote_flow.py`) seguem no `flow.sh`, porque
script não chama MCP.

As duas usam a MESMA conta do Flow (`contato.minhaempresa`). Regras de prompt, cena e QA moram na
`flow-video-playwright`; aqui só a mecânica do MCP.

## Instalação

O Low Ticket Kit instala sozinho (`install.sh` / `install.ps1`, função `setup_flow_mcp`) e atualiza a cada
update do kit. Sem o kit, os mesmos passos à mão:

- Servidor: fork `github.com/by-lua/google-flow-mcp`, branch `pt-br-labels`, em `~/.local/share/google-flow-mcp`
  (`git clone --branch pt-br-labels … && npm ci && npm run build`), registrado como `google-flow`:
  `claude mcp add --scope user google-flow -- node ~/.local/share/google-flow-mcp/dist/cli.js`.
  **Não troque pelo pacote do npm**: o original não lê o Flow em português e anexava a referência errada
  (corrigido nos commits `f83f7a0` e `db34b65`; PR `ParkSangGwon/google-flow-mcp#10`, aceito = volta ao npm).
- Chrome próprio: porta 9333, perfil `~/.google-flow-chrome`. Linux/macOS: aberto por `~/.claude/bin/flow-mcp-chrome`;
  Windows: `chrome.exe` direto. Config: `~/.config/google-flow-mcp/config.json`. Logs: `~/.google-flow-mcp/logs/`;
  prints: `~/.google-flow-mcp/screenshots/`.
- **Login (uma vez, e quando cair):** `cd /tmp && node ~/.local/share/google-flow-mcp/dist/cli.js doctor`; a dona
  entra na conta do Flow na janela do Chrome que abrir e roda o `doctor` de novo (`flow: logged in`).
- Ferramentas só aparecem em sessão nova. Pane: `pane_spawn` com `mcpServers: ["google-flow"]`.
- Máquina da dona: o repositório de trabalho é `~/Developer/google-flow-mcp` (o caminho acima é atalho para ele).

## Ferramentas

| Ferramenta | Uso | Crédito |
|---|---|---|
| `flow_connect`, `flow_status` | conecta/abre o Chrome, mostra login e jobs em andamento | não |
| `flow_project_open` | abre `https://flow.google.com/project/<id>` e lista mídias | não |
| `flow_generate_image` | Nano Banana Pro/2/2 Lite, 1–4 imagens, `reference_images` | imagem: não (conferir saldo) |
| `flow_generate_video` | Veo 3.1 Lite/Fast/Quality, Omni Flash, 4–10 s, frame inicial em `reference_images` | sim |
| `flow_scene_add`, `flow_scene_extend`, `flow_scene_status` | Scene Builder: estende o último clipe em +7 s (Veo 3.1 Lite) | extend: sim |
| `flow_media_download` | baixa uma mídia pelo id | não |
| `flow_inspect`, `flow_screenshot` | ver a tela real (diagnóstico) | não |

Projeto: reuse um projeto por leva. Criar projeto novo: `~/.claude/skills/flow-video-playwright/scripts/flow.sh novo-projeto`.

## Regras (aprendidas na flow-video-playwright, valem aqui)

1. **Primeiro sem gastar:** chame com `auto_confirm: false`, abra o `screenshot` e confira a referência no
   composer. Só então repita com `auto_confirm: true`.
2. **Referência = arquivo local com caminho absoluto.** Um frame por cena. Imagem da cena SEMPRE antes do vídeo.
3. **Nunca reenvie do zero uma geração que caiu:** chame de novo com `resume: true` e o `job_id`.
   Matar e reenviar = "atividade incomum" e crédito em dobro.
4. **Ritmo da CONTA:** mínimo 2 min entre envios e no máximo 8 envios por 30 min, somando MCP e flow.sh.
   Antes de enviar, rode `flow.sh status` (resfriamento ou "GERANDO agora" = espere). **Nunca use MCP e
   flow.sh ao mesmo tempo.**
5. **"Atividade incomum" ou reCAPTCHA na tela:** pare e rode `flow.sh bloqueio` (resfria a conta 45 min para os dois caminhos).
6. **Diálogo "Direitos de uso" no upload** (erro `REFERENCE_NOT_ATTACHED` com print `upload-dialog`): é da
   dona aceitar, uma vez, à mão. Vídeo de terceiro: nunca aceitar em nome dela.
7. **O servidor deixa "Confirmar antes de gerar" em "Nunca"** e muda os padrões do agente (modelo,
   proporção). Vale para a conta toda: qualquer envio gasta crédito direto.
8. **Prompt de vídeo longo, por segundo, com bloco de continuidade**, conteúdo de tela fechado, corrigir
   cor bt709 e QA no fim do clipe: seguir `flow-video-playwright` §§ "Lições de 22/10", "Modelo de prompt
   de movimento", "Conteúdo de tela fechado".

## Erros

| Código | O que fazer |
|---|---|
| `NOT_LOGGED_IN` | `doctor` e login da dona |
| `REFERENCE_NOT_ATTACHED` | caminho errado, upload não terminou em 90 s ou diálogo de direitos (ver print) |
| `UI_NOT_FOUND` | o Flow mudou um texto: compare `details` com `src/flow/labels.ts`, acrescente o pt-BR, build e teste |
| `GENERATION_TIMEOUT` | `resume: true` com o `job_id` |
| `POLICY_BLOCKED` | reescrever o prompt |
| `BUSY` | outra chamada usa a aba; espere |

## Pendências do teste (07/11/2026)

- Correção do anexo (`db34b65`) testada 07/11 com imagem real: a referência certa entrou no preparo e no envio.
  Vídeo com frame inicial depois da correção ainda não testado.
- Textos pt-BR de "gerando", política e Scene Builder não foram vistos na tela; o primeiro uso de cena confere.
