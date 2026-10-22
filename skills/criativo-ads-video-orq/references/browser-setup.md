# Browser persistente e lanes (vale para ChatGPT, Hub e Flow)

Toda geração por browser (imagem no ChatGPT, vídeo no Hub, vídeo no Flow) roda no
**Chromium do sistema** com **perfil persistente e logado**, comandado pelo
`agent-browser` via CDP. Nunca use `agent-browser open` (o Chromium empacotado não
guarda login e trava no Cloudflare).

## Uma vez só

```bash
~/.claude/bin/browsers.sh status                 # perfis registrados e se estão de pé
~/.claude/bin/browsers.sh gpt hub flow           # sobe os três (janelas do Chromium abrem)
# → faça login À MÃO em cada janela (ChatGPT, Hub, Flow/Google). O login sobrevive.
~/.claude/bin/browsers.sh add gpt-2 9226 https://chatgpt.com   # perfil extra (outra conta ou cota)
```

Registro: `~/.agent-profiles/registry.conf` (`nome porta url`, porta fixa por perfil).
Precisa de `chromium` (ou `CHROMIUM_BIN=/caminho`), `agent-browser`, `curl`, `python3`.

## Lane = uma aba sua

Vários agentes no mesmo perfil só não se atropelam se cada um fixar a PRÓPRIA aba.
Sem isso o comando cai na última aba criada e dois agentes escrevem no mesmo chat.

```bash
S=$(~/.claude/bin/gpt-livre.sh minha-lane)      # perfil ChatGPT livre + aba sua → imprime a sessão
S=$(~/.claude/bin/hub-livre.sh  minha-lane)     # idem Hub
# Flow: NÃO usa perfil de browser — gere só por ~/.claude/skills/flow-video-playwright/scripts/flow.sh
agent-browser --session $S <comando>            # SEMPRE com --session
~/.claude/bin/lane.sh take <perfil> <lane>      # refixa a aba (idempotente)
~/.claude/bin/lane.sh drop <perfil> <lane>      # ao terminar: fecha a SUA aba
~/.claude/bin/lane.sh collect <lane> <pasta>    # downloads da lane → pasta do projeto
```

Regras: nunca `agent-browser close --all` (mata as abas dos outros); feche as
próprias abas ao terminar; nomeie todo download com o prefixo da lane
(`<lane>-cena-1.mp4`), senão duas lanes se sobrescrevem em `~/Downloads`.
`*-livre.sh` sai com "SEM PERFIL LIVRE" se todos estiverem ocupados: espere, não
dispute. Perfil disputado não dá erro — só estraga o resultado em silêncio.

## Cloudflare / "Confirme que é humano"

Nesses perfis o checkbox pode ser clicado pela automação e valida normalmente.
Clique e siga; se reaparecer, clique de novo. Só chame a pessoa se falhar duas
vezes seguidas ou pedir 2FA. Skill `browser-cloudflare` tem o detalhe.

## Segredos

Nunca escreva senha em comando nem em arquivo do projeto (fica no histórico e no
transcript). Login é manual, uma vez, no perfil persistente.
