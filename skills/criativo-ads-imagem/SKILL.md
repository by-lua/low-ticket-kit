---
name: criativo-ads-imagem
description: MECÂNICA DE IMAGEM de anúncio (estático e carrossel), chamada pela orquestradora criativo-ads. Cobre o GUIA DE IMAGEM (tipos — orgânico iPhone, UGC estático, fase de impacto, só texto, original, peça de preço, caixa de perguntas/expert respondendo, antes/depois, formatos da biblioteca; carrosséis 1/2/3, objeção, história, demonstrativo), o molde de prompt orgânico (texto de Stories escrito pelo GPT, material impresso + digital, páginas reais, nunca mockup), a montagem de carrossel com página real (montar-cards.py) e os gates de imagem. Use para qualquer criativo de imagem, estático, carrossel, peça de preço, capa de carrossel, texto de story na imagem, "imagem orgânica", ou quando o plano da leva chega no passo de imagem.
---

# criativo-ads-imagem — mecânica de imagem

> Imagem NÃO começa aqui: começa na **TRILHA DO CRIATIVO** de `criativo-ads` (Kevones → Rodrigo +
> nossos formatos → roteiro/texto). Esta skill é o passo 5a: fazer a peça de imagem.

**Visual é sempre o nosso (dona, 26/10/2026):** foto orgânica de iPhone, texto de Stories escrito pelo
GPT dentro da foto, material **impresso + digital** (tablet, notebook, celular), páginas REAIS, **nunca
mockup**. Rodrigo/biblioteca dão o papel da peça; o visual segue esta skill. O CPM cai com isso.

## Arquivos

| Preciso de… | Arquivo |
|---|---|
| **Qual tipo é e o que vale pra todos** | `references/tipos-de-imagem.md` — **GUIA DE IMAGEM (ler inteiro)** |
| Escrever o prompt da cena orgânica | `references/PROMPT-ESTATICO-ORGANICO.md` (molde em 8 blocos, inglês, uma linha) |
| Regras da dona com os incidentes (consulta) | `references/regras-da-dona-imagem.md` — onde contradiz o GUIA, vale o GUIA |
| Capa aprovada de referência de estilo | `references/capa-referencia-low-ticket-jj.png` |
| Formato da biblioteca (print WhatsApp, notícia, story nativo, antes/depois) | skill `modelagem-escalados` (fidelidade à referência) |
| Carrossel demonstrativo iPhone (capa A/B) | `modelagem-escalados/references/carrossel-demonstrativo-iphone.md` |
| Por que orgânico (doutrina, CPM) | `criativo-ads/references/DOUTRINA-ORGANICO.md` |

## Fluxo de uma peça

1. **Tipo** — achar a linha no GUIA (vem do plano da leva). Texto já escrito no passo 4 da trilha:
   gancho → desenvolvimento (cita produto/mecanismo) → CTA. Preço só na peça de preço, plano mais barato.
2. **Referências** — capa + 2–3 páginas REAIS do entregável (`produto/ENTREGA/`, `produto/MVP/`, painel),
   REF-FORMATO da cena, `DESIGN-SYSTEM.md` da oferta. Escolher em `CRIATIVO-N/selecionados/`, cada
   aparelho e cada folha com página diferente.
3. **Gate antes de gerar:** `python3 ~/.claude/skills/criativo-ads/scripts/gate-pecas-criativo.py <CRIATIVO-N>`.
4. **Prompt** — pelo molde (`PROMPT-ESTATICO-ORGANICO.md`) ou pela referência da biblioteca; salvar em
   `CRIATIVO-N/intermediarios/prompt-vN.txt`. Texto como `Instagram Stories text sticker` + idioma, sem
   descrever cor/fonte; margens (topo 14%, base 20%, laterais) pedidas no prompt.
5. **Gerar** — `gpt-imagem-playwright` (perfil via `gpt-livre.sh | tail -1`; `scripts/gerar-imagem-gpt.sh`
   ou `gen2.sh`). Uma cena por mensagem, referências anexadas (nunca só descrição).
6. **Carrossel** — card 1 (e o de CTA, no tipo 2) gerados; páginas reais montadas com
   `scripts/montar-cards.py <pagina> <saida>` (4:5, largura inteira, sobra com o papel da página).
7. **Conferir** — (a) o texto pedido EXISTE na imagem (contar caixas); (b) ortografia palavra por palavra;
   (c) a página visível é o arquivo real certo; (d) margens; depois
   `python3 ~/.claude/skills/criativo-ads-imagem/scripts/gate-imagens-finais.py <finais> --pasta <CRIATIVO-N>`.
8. **Entregar** — final solto em `CRIATIVO-N/`, `anuncio.md` (copy de fora, diferente do texto da foto)
   escrito pelo molde + gate de `criativo-ads/references/texto-anuncio-por-angulo.md` — **1ª frase do
   Texto principal endereça quem compra** ("Si coordinás...", "Si tu mamá..."), nunca só descreve o
   produto. **Texto da ARTE = 3 andares do Rodrigo: headline (promessa/benefício ligado à dor) +
   texto de baixo (mecanismo ou entrega concreta) + CTA; nunca rótulo de seção sozinho**
   ("Lado luz y lado sombra" reprova; "Aprenda a ler o Tarot sem decorar nenhuma carta" passa) —
   método completo em `criativo-ads/references/texto-anuncio-por-angulo.md` —,
   `ls` de cada arquivo citado, registrar no STATUS da oferta e em `_memoria/planos-criativos.md`.

## Nunca

- Texto colado por código (faixa/bloco) · página desenhada pelo GPT · mockup 3D · "PDF" no anúncio ·
  mesma página em dois lugares · preço que não é do plano mais barato · peça "pronta" sem abrir a imagem.
- Exceção a regra da dona sem ordem dela, com data e citação (caso Tarot AR 25/10: "peça 9 sem texto").
