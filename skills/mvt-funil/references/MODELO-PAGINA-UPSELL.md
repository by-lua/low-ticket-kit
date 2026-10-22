# MODELO DE PÁGINA DE UPSELL (referência boa)

> Escolhido pela dona (16/10/2026) como **o bom exemplo de página de upsell**:
> *"tem estrutura enxuta, visual massa — só faltava adaptar para a oferta"*.
> É o molde a copiar quando for montar a página de Upsell 1/2 (e, adaptando preço, o downsell).

## O exemplo

- **No ar:** https://mapadotarot.leadgo.dev/upsell-cigano/
- **Fonte:** `OFERTAS/mapa-do-tarot/site/upsell-cigano/index.html` (single-file, ~470 linhas, seções com
  `style` inline + um `<style>` curto de helpers)
- **Oferta:** Mapa do Baralho Cigano vendido como Upsell 1 do Mapa do Tarot (R$ 17,90).

## Por que é bom (o que copiar)

1. **Estrutura enxuta** — uma coisa por seção, cada seção empurra pro CTA. Nada de bloco decorativo.
2. **Mesmo design system da oferta** — puxa os tokens `:root` do `site/index.html` da oferta (cor/fonte),
   então o upsell parece continuação da compra, não outro produto. (TJ: navy laranja; Tarot-family:
   Cormorant/Poppins.)
3. **CTA repetido em toda dobra-chave** com preço âncora (riscado) → preço real.
4. **Recusa sempre presente e discreta** ("Não, obrigado. Quero seguir para minha área de membros") —
   e ela é que abre o **modal de downsell** (R$ 9,90), não a página.
5. **Prova visual = produto real** — mockup com as páginas/cartas reais do entregável, não ícone.

## A ordem das seções (copiar nesta sequência)

1. **Barra de confirmação** (topo, fina) — *"✓ Pedido do <principal> confirmado! Só falta 1 passo."*
2. **Hero** — eyebrow (`✦ <promo>`) · H1 do desejo · sub de 1–2 linhas · **mockup do produto**
   (3–5 imagens reais sobrepostas/rotacionadas + 1 aberta) · preço âncora riscado → preço real ·
   CTA grande · 3 selos (`✓ Acesso imediato · ✓ Garantia de 7 dias · ✓ Pagamento seguro`) · recusa.
3. **Frustração** (citação em itálico, card com borda de acento) — a frase que o comprador diria.
4. **Identificação** — *"Se você se identifica, esse material é pra você"* + 3 bullets ✦ (cards brancos).
5. **Mecanismo** (fundo escuro) — *"O problema não é X. É que Y."* + método nomeado em **3 passos**
   (ex.: Método Visual 3C: Compreender · Conectar · Consultar).
6. **Espie por dentro** (prova) — 3–4 imagens **reais** do entregável com legenda + 1 linha + CTA.
7. **Transformação** — *"Isso é o que muda para você"* + 4 resultados com ícone (cards).
8. **O que você recebe** (fundo escuro) — nome do produto + itálico + **"VOCÊ RECEBE:"** (checklist) +
   bloco de bônus/partes (`bonus-list`) + preço âncora → real + CTA + selo *"Acesso liberado direto na
   sua área de membros"* + recusa.
9. **Garantia** — selo SVG (N dias) + *"Garantia incondicional · Risco zero"* + CTA.
10. **Objeções** — *"O que você provavelmente está pensando"* + 3 perguntas/respostas.
11. **CTA final** (fundo escuro) — 1 frase de fecho + preço âncora → real + CTA + recusa.
12. **Footer** — 1 linha de disclaimer educativo + copyright.

## Mecânica técnica (o que a página já traz)

- **Pixel do Trackeador ANTES do `fbq`** no `<head>` (regra da casa — senão o `event_id` não casa com a CAPI).
- Bloco de **decorate** que propaga `utm_*` + `_tkid` em todo link de checkout (inclusive cross-domain).
- **Todo botão de compra** com `data-tk-value` / `data-tk-currency` (o IC sai pelo Trackeador).
- **Modal de downsell** disparado pelo clique na recusa (`a.js-ir-painel`) — preço menor, mesmo produto.
- **1-clique (upsell no funil Wiven):** script que troca os botões pelo **iframe** do funil quando a URL
  traz `OCB_FUNNEL_ID`/`OCB_SEC_TOKEN`; em visita direta, os links normais de checkout. O `IC` do clique
  dentro do iframe sai pelo `blur` da janela → clique sintético no `.ocb-slot` (`data-tk-cta`).

## Ao adaptar para outra oferta

- Troque os tokens `:root` pelos da oferta (mesmo arquivo `site/index.html` dela) e os textos/preços.
- **Só crie a oferta no gateway depois** — enquanto não existir, o CTA fica com placeholder e a página
  não vai pro ar (pasta precisa de `COPY` no `Dockerfile` + whitelist do `serveStatic` — ver memória do Tarot 15/10).
- Preço: Upsell 1 padrão **R$ 17,90** · downsell **R$ 12,90** (tabela da dona 08/10) — fora disso, decisão
  escrita no `FUNIL.md` com data.
