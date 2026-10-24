# Tipos de imagem/carrossel — índice único (24/10/2026)

Toda peça de imagem da leva é UM destes tipos. Escolhe pela linha, segue a regra —
nenhum tipo pula GATE 0.1 (referência real anexada) nem a margem de segurança.

## Estático

| Tipo | Composição | Regra específica |
|---|---|---|
| **Orgânico iPhone (padrão)** | cena real, digital+impresso, texto Stories | `PROMPT-ESTATICO-ORGANICO.md` |
| **Fase de impacto** | fundo BRANCO ou PRETO, só texto preto+vermelho (ou branco+vermelho) | única exceção à regra digital+impresso |
| **Caixa de perguntas** | pergunta + expert respondendo, material na mão | sempre o expert da leva, nunca UGC |
| **Peça de preço — impacto** | fase de impacto + nome do produto + valor na mesma peça | nunca preço solto sem produto |
| **Peça de preço — orgânico** | reaproveita composição já aprovada, troca só o texto Stories pro valor | não gera cena nova |
| **Antes/depois** | puxado direto da Biblioteca de Anúncios, referência real já rodando | nunca gerado do zero sem referência |

## Carrossel (3 tipos, nunca repete tipo na mesma campanha)

| Tipo | Card 1 | Cards seguintes |
|---|---|---|
| **1 — Imagem principal + páginas** | arte gerada (a validada) | páginas reais do entregável, full bleed |
| **2 — Só páginas** | página real (sem arte gerada) | páginas reais, início ao fim |
| **3 — Estilo Henrique** | páginas reais em vários aparelhos, sem mockup | card final = CTA "mirá por dentro" |

## Checklist antes de montar QUALQUER peça de imagem

1. GATE 0.1 — capa + 2-3 páginas reais do entregável ANEXADAS no prompt (nunca só descrição)
2. Formato: 4:5 (1080×1350) padrão; 9:16 só se pedido
3. Digital + impresso (exceto fase de impacto e carrossel tipo 2)
4. Texto = sempre Stories, pedido curto e sem cor/forma no prompt
   (`texto-stories-gpt-curto-sem-cor`)
5. Margem de segurança: nada essencial no top 14%/bottom 20%
6. QA de ortografia palavra por palavra (gerador erra acento)
7. Dentro da mesma campanha, nenhum tipo se repete — relistar antes de fechar

Isso organiza o que já estava certo mas espalhado em `criativo-ads/SKILL.md` —
nenhuma regra nova aqui, só agrupada por tipo em vez de por data de correção.
