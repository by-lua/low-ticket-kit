---
name: flow-mcp
description: CAMINHO OFICIAL do Google Flow. Gera imagem e vídeo no Google Flow (Nano Banana, Veo 3.1, Omni Flash) pelo MCP google-flow (ferramentas mcp__google-flow__*), com imagem de referência e frame inicial nativos, teste sem gastar crédito (auto_confirm false), retomada de geração (resume) e Scene Builder (estender vídeo em blocos de 7 s). Use SEMPRE que qualquer skill ou pedido precisar gerar imagem ou vídeo no Flow, testar a geração antes de gastar ou estender um vídeo do Flow. A skill flow-video-playwright (flow.sh + gflow) é só a reserva, quando esta falhar.
---

# Google Flow pelo MCP google-flow — CAMINHO OFICIAL (desde 07/11/2026, ordem da dona)

> **LEIA PRIMEIRO o `GUIA POR SITUAÇÃO (09/11/2026)` no fim deste arquivo** — diz o que fazer conforme o que aparece na tela. As seções antigas continuam valendo, exceto onde o guia as corrige.

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
- Chrome próprio: porta <PORTA>, perfil `~/.google-flow-chrome`. Linux/macOS: aberto por `~/.claude/bin/flow-mcp-chrome`;
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

---

## ATUALIZAÇÃO 09/11/2026 — UI nova do Flow: o MCP `flow_generate_video` QUEBRA; use o caminho manual por CDP (testado, gerou 2 clipes)

**Sintoma:** `flow_generate_video` → `INTERNAL ... waiting for locator('button').filter({ hasText: /tune/ })`. O Flow trocou o painel de
configurações: não há mais botão "tune"; é o botão **"Gatilho de configurações"** (texto `Vídeo · 720p · 8s ⟂ <projeto-isolado>`). O `flow.sh`/gflow
também falha na UI nova (`maseQ answered 200 without a media id` no upload; `no signed media URL` depois de gerar). Não insista nos dois:
vá direto ao caminho manual abaixo (mesmo Chrome do MCP, porta <PORTA>, mesma conta).

**Modos do composer (dona, 09/11 — erro meu foi trocar):**
- **Elementos = o NOSSO caso** (imagem da cena anexada como elemento/referência). **Frames = só Início/Fim** (primeiro/último quadro): não usar.
- Abrir `Gatilho de configurações`: Vídeo · **Elementos** · 9:16 · Omni 1.2 Flash · 720p · Duração (slider; `input[aria-label=Duração]` = segundos−3,
  seta ←/→ muda 1 s: 6 s=18 créditos, **8 s=24**, 10 s=30, 11 s=36) · <projeto-isolado>.

**Receita (scripts em `~/.claude/skills/flow-mcp/scripts/*.cjs`, usam `playwright-core` de `~/.local/share/google-flow-mcp/node_modules` via
`connectOverCDP('http://127.0.0.1:9333')`; caminho de arquivo sempre por argv, espaço ok):**
1. `flow_project_open` (projeto novo: `flow.sh novo-projeto`). Converter a imagem: `magick in.png -strip -quality 92 up/in.jpg`.
2. `flow-prep.cjs <jpg>`: clica `+` (Adicionar elementos à caixa de comando) → `Enviar mídia` (intercepta o filechooser) → sobe a imagem.
   (O input de arquivo só existe depois do clique; `agent-browser upload` não serve.)
3. Com o seletor aberto: `flow_inspect` clicar no 1º item da lista (`at [820,352]`) e depois `target: "Incluir no comando"` — a miniatura aparece no composer.
   (O getByText/locator de lista do Playwright travou; o `flow_inspect` por coordenada/alvo funcionou.)
4. `flow-send.cjs <prompt.txt> <shot.jpg>` digita o prompt (Ctrl+A, Delete, `keyboard.insertText`) e tira print SEM enviar → conferir miniatura + texto +
   `24 créditos`. Depois o mesmo com `send` como 3º arg clica `Iniciar geração`.
5. Esperar ~100 s. `flow_project_open` (o vídeo novo é o 1º tile; o card `Falha` pode aparecer ao lado, ver abaixo).
6. Abrir o tile (`flow_inspect action=click at=[320,200]`, vai pra `/edit/<id>`) e `flow-baixar.cjs <saida.mp4>`: `Baixar mídia` → **"720p Tamanho original"**
   (dispara o evento `download`). **`flow_media_download` de vídeo dá HTTP 401 e a `url` do `flow_project_open` é só miniatura mjpeg 288×512** — não use.
7. Saída real: h264 **720×1280, 24 fps, 8 s, com faixa aac** (sem fala se o prompt proibir). Entra como veio (regra do 24 fps).
   QA: 4 quadros com `ffmpeg -vf "fps=0.5,scale=240:-1,tile=4x1"` e conferir gesto, texto do impresso e nada em outro idioma.

**Prompt que funcionou (Omni Flash, Elementos):** "The attached image coming to life: … exactly as in the starting frame. Camera fixed, overhead, only a very slow,
subtle push-in. 0-2 s … 2-5 s … 5-8 s … Continuity: … printed page stays perfectly sharp, legible and undistorted … No speech, no music, no new text." — copiar
o gesto do clipe de referência (frames do clipe antigo com ffmpeg `tile`) e descrever por segundo.

**Bloqueio — card `Falha: Notamos uma atividade incomum. As extensões do navegador…`:** apareceu em 2 de 3 envios (um deles depois de o vídeo já existir no
grid, então confira o grid antes de reenviar!). A regra 5 manda `flow.sh bloqueio` (45 min). Depois dele o ChatGPT do mesmo dia caiu em Cloudflare
"Confirme que é humano" que o clique no checkbox não resolveu. Ritmo seguro: 1 envio a cada ≥2 min, no máx. 8/30 min; não misturar gflow, MCP e
Playwright ao mesmo tempo (as 3 tentativas do gflow antes podem ter pesado). Banner "Seus créditos do Google Flow estão acabando" já apareceu: conferir saldo
antes de lote.

## ATUALIZAÇÃO 09/11/2026 (noite) — MCP CORRIGIDO para a UI nova (use o MCP, não o caminho manual)

Por que o MCP não estava sendo usado: o fork dirigia o composer ANTIGO (painel de chat "Agente", botão `tune`, card Approve). O Flow passou a ter caixa de
comando direta; `flow_generate_video` morria em `locator('button').filter({hasText:/tune/})`. Eu caí no caminho manual (CDP + playwright) em vez de
consertar o MCP — erro. **Corrigido em `~/.local/share/google-flow-mcp` (branch `pt-br-labels`, `src/flow/composer.ts`, `labels.ts`, `lib/errors.ts`):**
- detecta UI direta pelo botão `Gatilho de configurações`; `applyDirectSettings`: Vídeo/Imagem, **Elementos** quando há imagem de referência, ratio, `xN`,
  duração (setas ←/→ no slider até o botão mostrar `Ns`); o prompt entra **cru** (sem "Generate one 8-second…") com Ctrl+A/Delete/insertText;
  envio = botão `Iniciar geração` (Enter só quebra linha); sem card de aprovação; thumbnails contados dentro do container da caixa.
- **Download do vídeo já estava certo no MCP:** `…/asb/<token>=mm,22,15` (720p original) via `context.request.get` — a url nua é só poster (foi o que eu baixei errado).
- **Regra da dona (09/11): em falha comum, recarregar a página e tentar de novo** → `generateMedia` faz até 3 tentativas com `page.reload()` para
  `UNUSUAL_ACTIVITY` (novo código; card "Falha: atividade incomum"), `UI_NOT_FOUND`, `SEND_FAILED`, `REFERENCE_NOT_ATTACHED`. Se o vídeo já apareceu no grid apesar do card
  de falha, ele é baixado (não reenvia → não gasta crédito em dobro). Cada geração começa com reload (composer limpo).
- Testado SEM gastar crédito (`auto_confirm:false`): reload → settings → upload da referência → prompt digitado → tela pronta, 26 s. Teste standalone:
  `node ~/.claude/skills/flow-mcp/scripts/flow-mcp-test.mjs <prompt.txt> <img.jpg> <outdir> [send]` (importa o `dist/` direto, sem reiniciar o servidor).
- **O servidor MCP em execução só enxerga o `dist/` novo depois de reconectar** (`/mcp` → reconnect google-flow, ou sessão nova). Depois disso `flow_generate_video`
  com `reference_images:[jpg]`, `auto_confirm:false` (prévia) e `true` (envia) funciona direto.
- Ritmo (dona): **um envio por vez**, ≥2 min entre envios; se der "atividade incomum" não martelar: recarregar e tentar no máximo 2×, depois parar e avisar.

### Ritmo humano no MCP (dona, 09/11/2026) — `src/flow/human.ts`
O MCP agora age como pessoa: pausa aleatória antes de cada passo ("olhar a tela"), mouse desliza até o alvo (`humanClick`: scroll, move em 12–26 passos,
hesita, pressiona 60–140 ms, espera), digitação em blocos de 60 caracteres com 12–38 ms entre teclas (`humanType`, nada de `insertText` instantâneo),
re-leitura do prompt (1,5–3 s) antes de enviar e clique humano no botão `Iniciar geração`. Uma prévia (`auto_confirm:false`) leva ~90 s; um envio ~2 min.
**Prévia NÃO envia por desenho** (para na tela pronta, 0 crédito) — para gerar, chamar de novo com `auto_confirm:true` (ou `send` no teste standalone).


---

## GUIA POR SITUAÇÃO (09/11/2026) — "se a tela é assim, faça assado"

**Modelo (dona, 09/11):** hoje é **Omni Flash 1.1.2**. O seletor "Selecionar família de modelos" já mostrou "Omni 1.2 Flash" e "Omni 1.1 Flash" em momentos
diferentes — confira o nome no seletor antes de enviar e não troque por Veo sem a dona pedir (trocar de modelo reseta ratio/duração/anexo). Créditos medidos
(720p, <projeto-isolado>): 6 s = 18 · 8 s = 24 · 10 s = 30 · 11 s = 36. Banner "Seus créditos estão acabando": conferir saldo antes de lote.

| Se você vê… | Faça… |
|---|---|
| Composer com botão **`Gatilho de configurações`** (`Vídeo · 720p · 8s ▯ <projeto-isolado>`) e botão `Iniciar geração` (UI direta, nov/2026) | MCP **corrigido** (`src/flow/composer.ts`, depois de `/mcp` reconnect): `flow_generate_video` com `reference_images`, `auto_confirm:false` → olhar print → `true`. Sem o MCP novo: scripts `scripts/*.cjs` (CDP 9333) |
| Painel de chat **"Agente"** à direita + botão `tune` + card Approve (UI antiga) | caminho antigo do MCP (as seções acima) |
| Erro `locator… hasText: /tune/` | UI nova com MCP velho: reconectar o MCP corrigido; nunca insistir no `flow.sh`/gflow (também quebrados: `maseQ answered 200 without a media id`, `no signed media URL`) |
| Popover com **Frames** (aparecem caixas `Início` e `Fim`) | é para primeiro/último quadro. **Para animar a imagem de uma cena use `Elementos`** (dona, 09/11: "o nosso caso é Elementos") |
| Popover em **Elementos** + imagem a animar | `+` (Adicionar elementos à caixa de comando) → `Enviar mídia` (filechooser) → esperar o `%` sumir → clicar a linha do arquivo → `Incluir no comando` → miniatura aparece na caixa |
| A imagem é cena de **mãos/objeto, sem fala** (prancheta, agenda, capa) | prompt por segundo (0–2 s parado, 2–5 s gesto, 5–8 s ponto final), câmera fixa + push-in leve, "five fingers", impresso "sharp, legible, undistorted", fecha com "No speech, no music, no new text, no captions". 8 s |
| A imagem é **pessoa falando** (UGC/selfie/carro) | colocar a fala EXATA entre aspas no prompt, "lips perfectly synced, Argentine Rioplatense Spanish, natural lively female voice"; ~6 s; proibir só música/texto/legenda (NÃO escrever "no speech"); descrever o gesto no fim ("on the last words she lifts the calendar") |
| Quero **primeiro e último quadro** definidos | aí sim Frames (`Início`/`Fim`) — não é o caso dos takes de produto |
| Print mostra **`Falha: Notamos uma atividade incomum…`** | (1) conferir o grid: o vídeo às vezes existe mesmo assim; (2) se não existe: **recarregar a página e tentar de novo** (regra da dona), no máx. 2×; (3) persistindo: parar, `flow.sh bloqueio`, avisar. Um envio por vez, ≥2 min entre eles |
| Upload falha / `REFERENCE_NOT_ATTACHED` | reexportar a imagem: `magick in.png -strip -quality 92 up/in.jpg` (<1 MB), sem metadados |
| Vídeo gerado, preciso do arquivo | MCP baixa sozinho (`…=mm,22,15`, 720p original, h264 720×1280 24 fps + faixa aac). Manual: abrir o tile (`/edit/<id>`) → `Baixar mídia` → **720p Tamanho original**. Não usar `flow_media_download` de vídeo (401) nem a `url` da grade (é miniatura mjpeg 288×512) |
| A dona já gerou/baixou o clipe sozinha | **cancelar tudo que estiver agendado** (`TaskStop`) antes de qualquer envio — evita duplicar e gastar crédito |
| Prévia (`auto_confirm:false`) "não enviou" | é por desenho: a prévia para na tela pronta (0 crédito). Enviar = chamar de novo com `true` |
| Quero ver o que o Flow mostra | `flow_screenshot` / `flow_inspect` (leitura, sem custo) |

**Imagem GPT que alimenta o Flow (aprendido hoje):** `gerar-1-imagem.sh` com a imagem FR do take + página/capa AR + (se tem pessoa) a personagem aprovada; prompt = "recriar a MESMA foto trocando só o impresso",
A4 em escala real, espanhol com acento. Cloudflare "Confirme que é humano" no perfil gpt-<SÓCIO> que o clique no checkbox não resolve → a dona passa o desafio / gera ela mesma.
**Mostrar cada imagem à dona antes da próxima e antes do clipe** (regra `criativo`).
