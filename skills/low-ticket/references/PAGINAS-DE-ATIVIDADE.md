# PÁGINAS DE ATIVIDADE — instrução + folha de fazer (regra, 18/10/2026)

Referência da orquestradora `criacao-low-ticket-mvt` (passo 7 · Entrega) e da skill
`auditar-entregaveis-oferta`. Vale para **toda oferta**, não só GeriNeuro.

## A regra

Toda atividade do entregável que pede um **material físico/imprimível** tem **DUAS páginas**:

1. **Página de instrução** (a ficha ilustrada): o que é, objetivo, instrução para o profissional,
   o que a pessoa faz, adaptação fácil/difícil. *(já era o padrão)*
2. **Página de atividade** (a folha do participante): o que a pessoa **imprime e faz** —
   a grade do caça-palavra, o labirinto, a folha de sequência, o recibo, os cartões para recortar,
   o pôster, o tabuleiro, a folha de ligar-colunas, os relógios, os rostos.

As duas são **escritas juntas no texto da entrega** e as duas são **imagem GPT** (seções abaixo).

> **Teste rápido:** a instrução diz "hand the person…", "show a grid…", "lay out coins…",
> "show picture cards…", "poster…"? Então **falta a segunda página**. Sem ela o cliente paga por
> um exercício que ele **não consegue aplicar** (caso real GeriNeuro US 18/10: "Printable Word
> Search" sem a grade).

## A composição nasce no TEXTO da entrega (regra da dona, 23/10 e 26/10/2026)

A folha de fazer não é coisa que se lembra na hora da imagem. **Quem escreve o texto da entrega
já escreve as DUAS páginas.** Caso real: explicação feita, pôster/folha nunca feito, porque o texto
só tinha a instrução.

No `produto/texto/<modulo>.md`, cada ficha que pede material sai assim:

```
### Ficha 012 — Ida ao mercado
**Página 012 (instrução, pro profissional):** Objetivo / Instrução / O que a pessoa faz / Mais fácil / Mais difícil
  Cena da ilustração: cuidadora e idosa conferindo a lista no carrinho.
**Página 012w (atividade, a pessoa imprime e faz):**
  Tipo: simulação de compra · Formato: A4 retrato
  Título na folha: "VAMOS AO MERCADO"
  Conteúdo exato: lista com 6 itens e preços (Arroz R$ 6,50 …), nota de R$ 50, "Quanto sobra de troco? ____"
  Composição: lista à esquerda, ilustração do carrinho à direita, caixas de resposta embaixo
  Gabarito: R$ 12,30
```

- **Conteúdo exato e concreto:** palavras reais da sopa de letras, números reais da conta, regra
  do jogo, frase do pôster. Nada de "uma sopa de letras com palavras do tema".
- **Composição escrita:** o que vai onde na folha (título, área do exercício, ilustração, espaço
  de resposta). Se não dá pra imaginar a folha impressa lendo o texto, o texto está incompleto.
- **Pôster, tabuleiro, cartões para recortar, rostos** = também página `w`, com o texto e a
  composição escritos do mesmo jeito.
- A `w` **não** leva Objetivo/Instrução — só o exercício, como a pessoa vê na folha.
- MANIFESTO e contagem incluem as `w`. Texto sem a `w` = texto incompleto, não vai pro GPT.

## Ficha de instrução SEMPRE com imagem ilustrativa (regra da dona, 22/10/2026)

Toda ficha de instrução tem uma **imagem ilustrativa da atividade**: cuidadora/profissional + pessoa fazendo
exatamente o que a instrução diz (ex.: "Vamos al médico, qué llevamos en la bolsa" = os dois arrumando a bolsa
com documento, remédios, óculos). **Proibido** ícone abstrato no lugar da imagem (arco-íris, círculos, pontos,
folha numa caixa vazia) e página com metade de linhas de NOTAS vazias — caso real GeriNeuro US / NeuroActiva AR,
22/10: metade das fichas saiu assim e a dona chamou de ridículo.

Como fazer (CORRIGIDO pela dona no mesmo dia — layout por código + foto colada foi REPROVADO):
- **A ficha inteira é gerada no GPT** como imagem ilustrativa real, igual às fichas que já nasceram ilustradas:
  anexar como referência uma ficha NOSSA aprovada da oferta (ex.: NeuroActiva `v1 pagina-001.webp`), dentro da
  identidade visual do produto (cabeçalho, selo FICHA, título grande, ilustração da cena, caixas com ícone, rodapé).
- O prompt **explica o exercício direito**: o que a cuidadora faz, o que a pessoa faz, quais objetos aparecem
  (ex.: "Vamos al médico, qué llevamos en la bolsa" = os dois arrumando a bolsa com documento, remédios, óculos)
  + MANDATORY TEXT exato de `produto/texto/<modulo>.md` (título, objetivo, instrução, "qué hace").
- **Proibido**: card montado em código com foto colada numa caixa ("parece outra coisa"), e GPT copiando o layout
  plano da origem (ícone abstrato).
- Folha "w" (caça-palavra, labirinto, tabela, formulário, pôster): **também imagem GPT**, nunca código
  (regra da dona 23/10/2026, ver "Como gerar").
- Gate antes de publicar: contact sheet do módulo; ficha sem imagem da cena = reprovada.
- Cross-market: trazer a ficha plana da origem do jeito que está NÃO é adaptar — é herdar o defeito. Corrigir na
  hora de levar (mínimo: MVP de cada módulo com imagem).

## O que NÃO precisa da segunda página
Atividade puramente oral/observacional (conversa, reminiscência com foto pessoal do paciente,
leitura de relógio "de memória", charada falada). Aí a instrução já é o exercício.

## Pipeline (como publica)
- Master: `produto/ENTREGA/<pasta>/ficha-NNNw.png` (sufixo **w**), ao lado do `ficha-NNN.png`.
- Manifesto do gerador: `produto/ATIVIDADES.json` = `[{pasta, num, title, tipo}]`.
- `scripts/publica-painel.py` lê o `ATIVIDADES.json` e publica
  `site/painel/conteudo/<sku>/pagina-NNNw.webp` **imediatamente após** o `pagina-NNN.webp`
  (+ `pdf/pagina-NNNw.jpg`). O leitor e o **PDF** usam o mesmo `pages[]` — nada a fazer à parte.
- Se a oferta usa outro publicador, aplica a **mesma regra de ordem**: a folha entra logo depois
  do card que a pede.

## Como gerar — SEMPRE imagem GPT, nunca HTML/SVG/Pillow (regra da dona, 23/10/2026)
- **Toda folha `w` é gerada no GPT**, no padrão visual premium da oferta, igual às fichas de
  instrução. Código (HTML, SVG, Pillow, HTML→PDF) foi **reprovado**: saiu feio, "psicodélico",
  ícone chapado. Os scripts `gera-worksheet.py`, `gera-atividades.py` e `gera-printables.py`
  (GeriNeuro/NeuroActiva) estão **obsoletos** para geração. Não rodar.
- Mecânica: skill `gpt-imagem-playwright` § "Páginas de ATIVIDADE": **1 folha por mensagem**
  (lote não funciona), chat novo com 1-2 refs (ficha aprovada + 1 `w` aprovada), pedir pelo
  número exato ("agora gera a 012w"), conferir md5 contra repetição, A4 retrato.
- O prompt leva o **texto e a composição da `w` escritos no `produto/texto/`** (seção acima),
  como MANDATORY TEXT. Também pedir: "use o gerador de imagem, não documento, canvas, HTML nem código".
- Conteúdo exato (palavra na grade, labirinto que fecha, conta certa): conferir na imagem baixada
  contra o gabarito do texto. Errou → regera (máx 2×). Sem referência boa do tipo de exercício →
  buscar modelo (Pinterest, material do concorrente modelado), nunca inventar layout.
- Design: tokens do `DESIGN-SYSTEM.md` da oferta; cabeçalho com volume/worksheet, título,
  "Name / Date", a atividade, rodapé da marca. Adulto e digno (nunca infantil).

## Checklist antes de dar por entregue
- [ ] Texto do módulo tem, pra cada ficha que pede material, a página `w` escrita (conteúdo exato + composição + gabarito).
- [ ] Toda `w` é imagem GPT (nenhuma feita por HTML/Pillow).
- [ ] Toda ficha de instrução tem imagem ilustrativa da cena (nenhum ícone abstrato em caixa vazia).
- [ ] Cada card que pede material impresso tem `ficha-NNNw.png` publicado como `pagina-NNNw.webp`.
- [ ] Ordem no `pages[]`: `NNN`, `NNNw`, `NNN+1`…
- [ ] Conteúdo da folha está **correto** (a palavra realmente está na grade; o labirinto realmente fecha).
- [ ] Gate no ar: `check-download-pdf.mjs` OK (o PDF tem a folha).
- [ ] Contagem do MANIFESTO inclui as folhas (não são "sobra").
