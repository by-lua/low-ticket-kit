---
name: stories-diarias-ofertas
description: Stories diários de toda oferta low ticket — 2 imagens por dia (1 da OFERTA + 1 de DEPOIMENTOS) agendadas às 08:00 no Postiz e publicadas no Instagram da oferta. Use quando pedirem "postar/agendar os stories da oferta", "stories das 8h", "stories diários", "stories do Instagram da oferta", "fazer as stories de hoje", ou quando for criar/regenerar essas imagens (oferta e depoimento) para BR/PT/ES.
---

# stories-diarias-ofertas — as 2 stories diárias de cada oferta

Rotina fixa do portfólio LOW-TICKET (dona, 09/10/2026): **toda oferta no ar publica 2 stories por
dia, sempre às 08:00 (Brasília)**, pelo Postiz, na conta Instagram dessa oferta. A ordem é:
**1ª = oferta · 2ª = depoimentos**. As imagens são sempre essas duas — o mesmo layout, mudando só
o texto/mercado. Esta skill guarda o padrão visual, as referências e o passo a passo de publicar.

## 1 · As duas imagens (padrão)

Formato **9:16** (referência: 941×1672 px, PNG). Design system da oferta: fundo creme, título em
serif escuro/roxo, cards arredondados com borda lilás, ilustrações sol/lua/estrelas douradas,
fonte display nos títulos + sans nas descrições.

**STORIE-1 — OFERTA** (`references/STORIE-1-<MERCADO>-OFERTA.png`)
- Topo: logo/nome da oferta + headline curta (2 linhas) + subtítulo ("O teu guia visual…").
- 4 cards de benefício, cada um com miniatura ilustrada à esquerda + título forte + 1 linha de
  descrição. Os 4 cards = os 4 argumentos reais do produto (conteúdo, método, prática, formato).
- Rodapé: mockup do produto em uso (notebook/celular) + **botão CTA** ("Quero começar hoje →") +
  linha de segurança ("Acesso imediato · Garantia de 7 dias").

**STORIE-2 — DEPOIMENTOS** (`references/STORIE-2-<MERCADO>-DEPOIMENTO.png`)
- Topo: "O que dizem de nós" + subtítulo "Mensagens que recebemos".
- **4 cards** de mensagem (estilo DM/comentário de rede social): avatar foto real à esquerda,
  nome do remetente **coberto por um bloco roxo** (anonimato), texto do depoimento, metadata
  ("14 s · Responder", "4 h · Adoro · 1 gosto", "1 sem").
- Rodapé: logo/nome da oferta + ilustrações de nuvem/lua.
- Avatares: pessoas reais e diferentes entre si, **faixa etária e gênero coerentes com o público
  da oferta** (tarot → majoritariamente mulheres 25-55; outro nicho → outro recorte). Trocar só a
  foto e o texto; o resto do layout é igual.
- Depoimento tem que **fazer sentido com o produto** (entrega por e-mail, material organizado,
  didático, imprimir) — nunca genérico de outro produto.

Referências prontas (Mapa do Tarot, 3 mercados): `references/`
`STORIE-1-{BR,PT,ES}-OFERTA.png` · `STORIE-2-{BR,PT,ES}-DEPOIMENTO.png`
Origem original (não mexer): `LOW-TICKET/OFERTAS/mapa-do-tarot/instagram/stories/`.

## 2 · Gerar/regenerar a imagem (só quando não existir a do mercado)

Porta de imagem: **`gpt-imagem-playwright`** (ChatGPT, perfil `gpt`). Anexar no prompt, sempre:

1. **A oferta inteira** — `OFERTAS/<slug>/STATUS.md` (o que é, preço, mercado, checkout).
2. **O site no ar** (screenshot da página de vendas) — BR `<slug>.leadgo.dev` · PT `pt.…` ·
   ES `…` (domínio próprio). Manda o site **e** as cores: `DESIGN-SYSTEM.md` da oferta.
3. **Imagens reais da entrega** — `produto/ENTREGA/` / capa + 2 a 3 páginas do PDF: capa + 2/3
   páginas reais, sempre (regra da dona 09/10). O mockup do rodapé mostra página real, nunca
   desenhada pelo modelo.
4. **Depoimentos** — no mesmo estilo das referências, trocando só foto e texto, com cara real.
5. **Formato 9:16 story**, português do mercado (pt-BR / pt-PT / es neutro latino).

Nunca inventar preço, benefício, número de módulos ou depoimento: tudo vem da oferta, do site e do
entregável. Prompt sem aspas duplas no meio (regra da oferta: `keyboard inserttext` truncava).

## 3 · Publicar no Postiz (conta da oferta)

Credenciais self-hosted ficam em `~/.postiz/credentials.json`
(`apiUrl: https://postiz.empresa-b.com.br/api`, chave da API no `~/.claude.json` →
`projects…mcpServers.postiz.headers.Authorization`, gravada **sem** o prefixo `Bearer `).
Se `postiz auth:status` falhar, regravar o arquivo e conferir de novo antes de qualquer coisa.

**Contas Instagram por oferta** (acha id com `postiz integrations:list`, campo `profile`):

| Oferta | Instagram | integration id |
|---|---|---|
| mapa-do-tarot | `mapavisualtarot` | `cmuzu2b1100xfrt7ajt98a7ob` |
| *(nova oferta → linha nova aqui e no `_memoria/stories-diarias.md`)* | | |

Passo a passo (1 imagem por story — **regra do Postiz**: story só aceita 1 anexo):

```bash
S1=$(postiz upload STORIE-1-PT-OFERTA.png | tail -n +2 | jq -r '.path')
S2=$(postiz upload STORIE-2-PT-DEPOIMENTO.png | tail -n +2 | jq -r '.path')

# 08:00 BRT = 11:00Z. Posta a oferta primeiro, depoimento ~5 min depois (ordem garantida)
postiz posts:create -c "Mapa do Tarot 🌙 …" -m "$S1" \
  -s "2026-10-10T11:00:00Z" --settings '{"post_type":"story"}' -i "<integration-id>"
postiz posts:create -c "O que dizem de nós 💜 …" -m "$S2" \
  -s "2026-10-10T11:05:00Z" --settings '{"post_type":"story"}' -i "<integration-id>"
```

- Todo valor em `-m` é **path devolvido por `postiz upload`** — nunca caminho local.
- `postiz integrations:settings <id>` antes de agendar (regras/descrições do provider).
- Conferir depois: `postiz posts:list` → estado `QUEUE`, `publishDate` certo, integration certo.
- Dia que 8h já passou e a dona mandar "postar agora": publica na hora (agendar +2/+7 min pra
  garantir a ordem) e avisa no relatório.
- **Lote do mês** (a dona pode pedir "agendar até o fim do mês às 8h"): mesma receita em loop por
  dia — oferta `11:00Z`, depoimento `11:05Z` — gravando id por dia em `/tmp/agendamento-<mercado>.log`
  e conferindo no fim com `postiz posts:list` (esperado: 2/dia em `QUEUE`, todas no horário).
  Depois: registrar no histórico de `_memoria/stories-diarias.md` e avisar que o lote do mês
  seguinte precisa ser pedido de novo.

## 4 · Checklist antes de fechar a tarefa

- [ ] As 2 imagens existem pro mercado pedido (BR/PT/ES) e são 9:16.
- [ ] Texto bate com a oferta real (preço, benefícios, garantia) — nada inventado.
- [ ] Conta certa da tabela, `post_type: story`, 1 imagem por post.
- [ ] Story da oferta agendado ANTES do de depoimento.
- [ ] `posts:list` mostra os 2 em `QUEUE` com a data/hora esperadas.
- [ ] Registro da rodada em `_memoria/stories-diarias.md` (o que foi postado e quando).
