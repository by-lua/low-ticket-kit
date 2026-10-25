---
name: low-ticket-painel
description: "PORTA DE ENTRADA do portfólio LOW-TICKET. Carrega o estado real do negócio antes de qualquer trabalho (PANORAMA, STATUS geral, memória da empresa e a CLAUDE/STATUS/memória da oferta em que se vai mexer) e grava o estado de volta ao terminar. Use SEMPRE que a tarefa for do portfólio low ticket: pedir pra mexer numa oferta, criar oferta, retomar entrega, gerar criativo, 'como tá o negócio', 'onde paramos', 'qual oferta tá pronta'. Nenhuma ação começa sem esta skill."
---

# LOW-TICKET — porta de entrada

> **TROCAR PÁGINA DE OFERTA (14/10/2026):** trocar a página principal de uma
> oferta = levar o bloco do pixel + loader do Trackeador e rodar
> `adstrackeador pagina comparar <atual> <nova>` antes de publicar. Nunca
> publique página sem rastreio (incidente real: ~1h sem pixel com anúncio
> rodando).

> **TODO PRODUTO/Oferta nos DOIS webhooks (regra da dona, 16/10/2026):** produto novo de qualquer
> oferta — principal, **order bump**, combo, upsell, downsell, **upgrade Essencial → Completo**,
> produto irmão/cross e oferta de membro — entra, na MESMA sessão do cadastro, no **webhook da área
> de membros** (`<site>/painel/api/webhooks/<gateway>`) **e** no **webhook do Trackeador**
> (`adstrackeador.leadgo.dev/api/webhooks/sale/c/<conexão>`), "todos os produtos" OFF, e no
> `PRODUCT_SKUS`/`COMPLETO_OFFERS` do servidor. O webhook (Wiven/Cooud/GG…) é **por produto** —
> produto criado depois **não entra sozinho**. Prova: `/panel/webhooks` com **TODOS** os produtos da
> oferta nos dois. Caso real: order bump "Combo Domínio Total" (Jiu-Jitsu) vendeu e não entrou no
> Trackeador. Detalhe: `_memoria/preferencias.md` (bloco 16/10), `wiven-checkout` §6,
> `criacao-low-ticket-mvt` (topo + GATE 6).

Ninguém trabalha em oferta low ticket sem passar por aqui. A skill não "ajuda": ela
**carrega o estado antes e grava o estado depois**. Se um agente age direto no disco
sem isso, ele trabalha com informação velha — foi assim que o `PANORAMA.md` ficou
defasado e um manifestoVier "vazio" com 30 imagens no ar.

## FASE 0 · Carrega (obrigatória, antes de qualquer outra coisa)

Navegando até a raiz `LOW-TICKET` e lendo, nesta ordem:

1. `CLAUDE.md` (raiz) — regras da casa. Já vem no contexto; mesmo assim, as regras
   importam mais do que o resto.
2. `PANORAMA.md` — em que ponto o negócio inteiro está.
3. `STATUS.md` (raiz) — painel das ofertas.
4. `_memoria/INDICE-MEMORIA.md` — o mapa do que mora no centro e do que mora em cada oferta.
5. Se a tarefa é de **uma oferta**: `OFERTAS/<slug>/CLAUDE.md` + `STATUS.md` +
   `DESIGN-SYSTEM.md` (se existir) + a seção "Memória da oferta" do CLAUDE.md.
6. `ENTREGAVEIS.yaml` da oferta (`produto/ENTREGAVEIS.yaml`) quando a tarefa toca
   entrega — e recontar com `auditar-entregaveis-oferta` se a pergunta for "o que falta".

Nada de responder "como está a oferta X" de memória. O estado mora nos arquivos.

## FASE 1 · Encontra a oferta certa

`STATUS.md` da raiz tem as 5 ofertas. Cruzando com a tarefa, escolher a oferta e dizer
qual é em uma linha antes de começar. Tarefa transversal (empresa, gateway, mineração,
perfis) → segue a seção "Frentes" do mesmo `STATUS.md`.

> **⛔ GATE DE PERSONA MECÂNICO (dona, 23/10/2026 — erro que não se repete):** antes de página, criativo,
> peça do funil ou preço, rodar `python3 ~/.claude/skills/criacao-low-ticket-mvt/scripts/gate-persona.py OFERTAS/<slug>`. **BLOQUEADO = não começa**; completa o
> `pesquisa/PERSONA-E-ANGULOS.md` no modelo `MODELOS/_MODELO-PERSONA-E-ANGULOS.md` (MERCADO na Biblioteca ≥5 anúncios,
> QUEM COMPRA DE VERDADE, dores com contagem+data, RECORTES com "por que está na oferta"). Casos: Elétrica estudou o
> estudante (comprador = eletricista na obra); Jiu usou "faixa branca/azul" (só vendeu quando tirou da página).
> **Pesquisa que alimenta (lição Atlas 23/10):** `criacao-low-ticket-mvt/references/PESQUISA-PADRAO-OFERTA.md` —
> Biblioteca 5 palavras + hashtag por idioma, YouTube/TikTok/Trends com contagem. O gate também cobra TERMOS DE
> BUSCA (nome do produto quase nunca é termo: "atlas" = 0 no Trends AR), unidade da peça, cena da dor,
> NARRATIVAS QUE RODAM (dias no ar) e ÂNCORA DE PREÇO.

## FASE 2 · Executa

Carrega a skill da linha da tabela do `CLAUDE.md` da raiz — sem ela, não começa.
Se a tarefa for entrega/promessa × entregue: `auditar-entregaveis-oferta`.
Se a tarefa for **criativos de uma oferta** (leva, peça ou correção pontual numa peça
existente): `criativo-ads` — ela própria carrega a mecânica certa (video-orq/modelagem-escalados)
e o gate de inventário de material; não duplicar esse roteamento aqui.

## FASE 3 · Grava o estado (obrigatória, antes de encerrar)

Nada termina sem deixar registrado onde parou:

- **Entrega/quantidade**: `python3 ~/.claude/skills/auditar-entregaveis-oferta/scripts/audita.py OFERTAS/<slug> --registrar`
  (reexecutar depois de gerar/publicar qualquer coisa).
- **Fase, dinheiro, pendências, bloqueio**: entrada datada no `STATUS.md` da oferta +
  "Atualizado em".
- **Linha da oferta no painel**: `STATUS.md` da raiz.
- **Visão do negócio inteiro**: `PANORAMA.md` da raiz (só se a fase/maior buraco mudou).
- **Regra que vira regra da empresa**: `_memoria/preferencias.md` (ou o arquivo certo
  da `_memoria/`) + o `MEMORY.md` do usuário se for regra de portfólio.
- **Plano de criativo**: `_memoria/planos-criativos.md`, a cada peça entregue.
- **Inventário de material de gravação/take** (`criativos/MATERIAL-ENTREGAVEL/INVENTARIO.md`,
  `criativos/FLOW-TAKES/README.md`, `criativos/BROLL-3D/INVENTARIO.md` ou equivalente da oferta):
  toda vez que gravação nova (celular/PC) ou take novo (Flow) entrar na pasta, atualizar o
  inventário (ffprobe: duração+resolução+conteúdo) NA HORA — nunca deixar pra quando alguém for
  montar vídeo. Sem isso, a próxima montagem só vê 1-2 fontes e repete o erro de "segurar 1 take
  muito tempo" (`criativo-ads-video-orq` item 11). Caso real: Atlas AR 25/10 — 7 gravações + 2
  Flow existiam, nenhum inventário registrava isso, CT11/CT21 usaram só 1-2.
- **Hub (site `huboferlaslowticket.leadgo.dev`, topo "O que falta em cada oferta"):** depois de mexer em
  qualquer STATUS, na pasta `HUB-OFERTAS/`: `python3 sincroniza-ofertas.py` → `set -a; source
  ~/.claude/.credentials.env; set +a; uv run cifrar.py && uv run cifrar.py --verificar` (tem que dar
  `True`) → commit + push do `ofertas.enc`. Sem isso o site congela (ficou parado de 25/09 a 23/10).
  Pendência = `- [ ]` no STATUS da oferta; quem depende da dona escreve "dona"/"aprovar" no texto.

## Regras de convivência

- Fonte da verdade de uma oferta = `OFERTAS/<slug>/STATUS.md`. Se divergir do
  `STATUS.md` da raiz, **manda o da oferta**.
- O que é regra do negócio inteiro mora na `_memoria/`; o que é regra só de uma oferta
  mora na seção "Memória da oferta" do `CLAUDE.md` dela.
- Registro gerado (`ENTREGAVEIS.yaml`) nunca editado à mão.
- Toda tarefa entra pela Fase 0 e sai pela Fase 3. Sem exceção — inclusive quando a
  resposta é só "olha e me fala" (aí a Fase 3 é atualizar o que estava errado).