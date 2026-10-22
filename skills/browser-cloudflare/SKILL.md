---
name: browser-cloudflare
description: Contorna bloqueio de Cloudflare, "Confirme que é humano", detecção de bot e telas de login em automação de browser. Sobe o Chromium do sistema com perfil persistente e porta CDP, e conecta o agent-browser nele em vez de deixar ele lançar o Chromium empacotado. Use sempre que o agent-browser empacar em desafio do Cloudflare, checkbox de verificação humana, "Just a moment", tela de bot detection, ou quando precisar automatizar site logado com várias contas ao mesmo tempo.
allowed-tools: Bash(agent-browser:*), Bash(chromium:*), Bash(curl:*), Bash(mkdir:*), Bash(nohup:*), Bash(pgrep:*)
---

# browser-cloudflare

Automação de browser que precisa passar por Cloudflare, login ou qualquer detecção de bot.

## O problema

`agent-browser open <url>` lança o Chromium **empacotado** (`~/.agent-browser/browsers/`). Ele roda com:

- perfil descartável em `/tmp/agent-browser-chrome-<uuid>` — some a cada sessão
- flags de automação injetadas pelo launcher
- headless por padrão (`--headed` **não** resolve — continua o mesmo binário)

Para o Cloudflare isso é assinatura de bot. O checkbox "Confirme que é humano" aparece e nunca resolve, porque não é o checkbox que decide — é o fingerprint por trás.

## A solução

Suba o Chromium do **sistema** na mão e **conecte** o agent-browser via CDP.

```fish
mkdir -p ~/.agent-profiles/PERFIL
nohup /usr/bin/chromium \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.agent-profiles/PERFIL" \
  --no-first-run --no-default-browser-check \
  https://SITE > /tmp/chromium-PERFIL.log 2>&1 &

# confirme que subiu antes de conectar
curl -s http://127.0.0.1:9222/json/version

agent-browser --session NOME connect 9222
```

A partir daí todo comando normal funciona, só passando `--session NOME`:

```fish
agent-browser --session NOME snapshot -i -c
agent-browser --session NOME click @e5
```

## Por que funciona

Três fatores, todos necessários:

1. **Binário real do sistema** — não instrumentado, sem flags de automação
2. **Perfil persistente** — cookies, fingerprint e histórico sobrevivem entre execuções. O Cloudflare passa a tratar como visitante recorrente em vez de sessão virgem. **Fator mais pesado.**
3. **`connect` em vez de `open`** — anexa a um browser já rodando normalmente, sem o launcher no meio

## Várias contas simultâneas

Uma porta e um perfil por conta. Cookies totalmente isolados.

```fish
# conta A
nohup /usr/bin/chromium --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.agent-profiles/contaA" ... &
agent-browser --session contaA connect 9222

# conta B
nohup /usr/bin/chromium --remote-debugging-port=9223 \
  --user-data-dir="$HOME/.agent-profiles/contaB" ... &
agent-browser --session contaB connect 9223
```

Sempre passe `--session` em **todo** comando. Sem a flag cai na sessão default e mistura as contas.

## Pegadinhas

| Sintoma | Causa | Correção |
|---|---|---|
| Browser abre mas a porta não responde | Chrome 136+ recusa `--remote-debugging-port` no perfil padrão | `--user-data-dir` separado é obrigatório, não opcional |
| Cloudflare continua travando | Ainda usando o Chromium empacotado | Nunca use `open` para o primeiro acesso; use `connect` |
| Nenhuma janela aparece | Rodou headless | O `--headed` do agent-browser não basta — suba o do sistema |
| Login perdido toda execução | Perfil em `/tmp` | Perfil persistente em `~/.agent-profiles/` |
| Sessão errada / conta trocada | Faltou `--session` | Passe sempre |

## O desafio do Cloudflare, uma vez no perfil certo, pode ser clicado

Com o Chromium do sistema e perfil persistente, o checkbox "Confirme que é humano" **valida normalmente quando clicado pela automação**. Não é a mesma situação do Chromium empacotado, onde ele nunca resolve por mais que se clique.

```bash
agent-browser --session NOME snapshot -i -c      # o iframe do desafio aparece inline
agent-browser --session NOME click @eCHECKBOX
agent-browser --session NOME wait 3000
```

Pode aparecer de novo depois de uma ação — clique de novo. Só envolva o usuário se o mesmo checkbox falhar duas vezes seguidas.

## O que continua manual

Senha e 2FA na **primeira** vez. O perfil persistente segura o login depois — nas execuções seguintes o browser já abre logado e não precisa de `state save`.

Para não deixar senha no histórico do shell, use o cofre: `agent-browser auth save <nome> --password-stdin`.

## Verificar o que está rodando

```fish
pgrep -af "remote-debugging-port" | grep -o "user-data-dir=[^ ]*" | sort -u
curl -s http://127.0.0.1:9222/json/version
```

## Outros browsers

`/usr/bin/chromium` é o padrão. Google Chrome via flatpak também serve (`flatpak run com.google.Chrome`), mas o `--user-data-dir` precisa estar dentro de caminho permitido pelo sandbox, ou conceder com `--filesystem`. Chromium do sistema é o caminho de menor atrito.
