# Carrossel demonstrativo "iPhone cru" + páginas do entregável

Formato de **imagem** que está dando muito certo (low ticket / infoproduto / app /
ferramenta). É o irmão estático do criativo demonstrativo em vídeo (Modo E de
`criativo-ads-video-orq`): mostra o entregável POR DENTRO, sem cara de anúncio.

**Estética "ugly iPhone":** imagem que parece foto/print de celular, não arte de
agência. Print nativo, enquadramento meio torto, luz de ambiente, sem gradiente,
sem moldura polida, sem fonte de design. O feio é proposital: é o que faz o Meta
e a pessoa lerem como orgânico. **Proporção 1:1 (1080×1080) em todos os cards**, tudo
dentro da safe area (regra da dona, 04/10/2026; 4:5 só se pedido).

## Card 1 (capa) — DUAS estruturas válidas (regra da dona, 2026-10-04)

A capa tem **duas versões**, escolha uma por carrossel — não misture as duas:

**Estilo A — com benefícios + garantia/vitalício:**
1. Em cima: **a promessa principal** do ângulo daquela oferta (uma frase).
2. No meio ou do lado: **mockup do entregável em um ou mais formatos** —
   impresso, celular, notebook, ou os três juntos — fundo bem orgânico, nada de
   "ar de banco de imagem".
3. Pode listar **benefícios específicos** ali na capa (curtos, estilo
   nota/etiqueta).
4. Embaixo: **acesso vitalício + garantia de 7 dias**.

**Estilo B — só promessa/benefício + entregável + CTA:**
1. Em cima: a promessa principal **ou** um benefício específico (um dos dois,
   não os dois empilhados).
2. Mockup do entregável (mesma regra de formato acima).
3. CTA pra saber mais ("saiba mais", "o link tá aí") — **sem** garantia, sem
   vitalício, sem lista de benefícios.

**Preço:** só entra em qualquer um dos dois estilos se a dona pedir
explicitamente. Sem pedido de preço, nenhuma versão da capa leva preço.

| Card | Conteúdo |
|---|---|
| 1 · Capa | Estilo A ou Estilo B, acima |
| 3 a 6 · Por dentro | **~4 páginas ou telas reais do entregável**: sumário, uma página aberta, um exemplo, uma tela em uso. App/ferramenta = telas do app; PDF/guia = páginas do PDF |

Ordem fixa: **capa (promessa + mockup) → benefícios (+ garantia/vitalício) → páginas
reais do entregável**. Os cards de benefício vêm antes das páginas, não depois.

Regras:
- **Os cards 3–6 são o entregável de verdade** (print/gravação/páginas exportadas), nunca imagem gerada de "como seria". Mascare e-mail, nome, token e dado pessoal.
- **Encaixe das páginas reais no 1:1:** preencha o card de ponta a ponta (full bleed),
  **sem moldura/borda** — página centralizada "com respiro" e borda branca sobre fundo
  escuro foi reprovada pela dona ("borda feia", 08/10). Recorte é livre: corte um
  pedaço da imagem, inclusive o fim, se a fonte for longa/PDF — o que importa é o
  conteúdo aparecer do início ao fim, card a card. Alternativa aceita: foto orgânica
  da página impressa/no celular feita por composição com o arquivo real (anexo de
  referência + ordem explícita no prompt).
- **Proibido o GPT inventar/desenhar páginas do produto** em qualquer card. Folhas com
  texto ou fotos falsas espalhadas na mesa = erro (visto em 04/10, jiu-jitsu). Se a cena
  tem folha ou celular, o conteúdo visível tem que ser a página real.
- Uma ideia por card; a promessa do card 1 é a única promessa. Não repita a mesma dor nos cards.
- Um ângulo (dor/bolha) por carrossel; o carrossel do mesmo ângulo pode virar vídeo (Modo E) e estático de uma frase.
- Sem promessa falsa; benefício real do produto.

## Texto no estilo Story (em alguns cards)

Em alguns cards, coloque o texto como se fosse de **Story do Instagram**: a fonte e o
balão/fundo de texto nativos do Story (texto branco com tarja preta, ou fundo colorido
arredondado), posicionado como quem digitou por cima da foto, sem fonte de design nem
alinhamento perfeito. Deixa o carrossel ainda mais orgânico e ajuda a **reduzir o CPM**.
Bons candidatos: a promessa do card 1 e as frases curtas de benefícios/garantia
(Estilo A); nas páginas do entregável, no máximo uma legenda curta por card. Não usar em
todos os cards (vira template). O chrome de Story completo (barra de status, avatar)
está em `modelagem-escalados/SKILL.md` (seção do Story nativo) e `prompts/07-arte-stories.md`.

## Como produzir

1. Estratégia: `criativo-ads` (dor/bolha, formato, quantidade).
2. Card 1 (capa): `gpt-imagem-playwright`, prompt pedindo foto/print cru de iPhone (sem acabamento de design), com a referência real do entregável anexada (nunca descrição só em texto — ver regra em `gpt-imagem-playwright/SKILL.md`).
3. Cards 3–6: capture o entregável (`agent-browser` em modo mobile para app/ferramenta; export de página para PDF/guia).
4. Gate de QA: `modelagem-escalados/prompts/10-gate-qa.md` + dado pessoal + texto dentro da safe area.
5. Nomenclatura e entrega: `prompts/12-nomenclatura-entrega.md`.
