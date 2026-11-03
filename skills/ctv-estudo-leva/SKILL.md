---
name: ctv-estudo-leva
description: Monta a ficha da leva de criativos do sistema LOW-TICKET — junta as ideias (Modelador, concorrente, dona), escolhe quantas peças e quais formatos e escreve 1 linha por peça pra dona aprovar antes de gerar qualquer coisa. Use para "planeja a leva", "quantos criativos", "ficha da leva", antes de produzir criativo.
---

# ctv-estudo-leva — ficha da leva

**Entrada:** `OFERTA.md` · `modelador-*.json` (ganchos, roteiros, copies, estáticos) · `criativos/IDEIAS-*.md`
(`ctv-modelar-concorrente`) · `trafego/ANALISES.md` (o que já funcionou ou não, com métrica).
**Saída:** `criativos/FICHA-LEVA-<AAAA-MM-DD>.md` **aprovada pela dona**. Nada é gerado antes.

## Passos
1. **Quantas peças e que mix:** a dona disse ("3 vídeos e 3 imagens") → vale o dela; dentro disso, variar formato
   (nunca 2 peças do mesmo formato e ângulo). Ela não disse → se o método Kevones estiver ativo, a estrutura da campanha e o mix
   imagem × vídeo (70/30, 50/50…) vêm de `criativo/references/METODO-KEVONES-LEVA.md`. Toda campanha de teste
   leva vídeo + estático + carrossel.
2. **Escolher as ideias:** priorizar as que vêm de anúncio real (do original/concorrente) e as que atacam a
   alavanca mais fraca do original. Cada peça = 1 ângulo e 1 alavanca; ângulos não se repetem na campanha.
3. **Ficha — 1 linha por peça:**
   `# · formato (ctv-formatos) · mídia · ângulo · alavanca · fonte da ideia (link/arquivo) · gancho ·
   texto na imagem ou fala completa · título · texto principal · cena (o que aparece; estático ou cena de vídeo)`
   — no idioma do anúncio **e** em português pra dona ler.
4. Copy de cada linha pelo método da `ctv-copy`.
5. **Mostrar à dona** → ajustes → "aprovada em AAAA-MM-DD" no topo.

## Mix padrão — a dona só diz a quantidade, o agente escolhe o formato
Pegar na ordem, sem repetir formato. Preço: **uma** peça por campanha (iPhone com preço **ou** frase direta com preço).
- **Imagem:** 1 iPhone feio (6) → 2 frase direta (9) → 3 carrossel de páginas (11) → 4 iPhone feio com preço (7)
  (se a frase direta não levou preço) → 5 caixinha de perguntas (5) → 6 antes e depois (8).
- **Vídeo:** 1 demonstrativo (1) → 2 UGC (2) → 3 expert (3) → 4 POV (12) → 5 caixinha com expert (4).
- Ajuste pelo que já vendeu na oferta (`trafego/ANALISES.md`): formato campeão entra primeiro, com ângulo novo.
- Ex.: "3 vídeos e 3 imagens" = demonstrativo · UGC · expert + iPhone feio · frase direta · carrossel.

## Regras da leva
- Preço em criativo = plano mais barato; uma peça de preço por campanha; carrossel sem preço.
- Nenhuma imagem/página repete entre peças nem entre aparelhos da mesma cena.
- Análise de tráfego anterior diz algo contra o ângulo → dizer à dona antes de repetir.

Depois: produzir (`ctv-imagem` / `ctv-video`) → revisar (`ctv-revisor`).
