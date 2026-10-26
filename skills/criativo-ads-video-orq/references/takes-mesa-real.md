# Takes "mesa real" (imagem → vídeo no Flow) — catálogo A–O e regras (movido do SKILL.md em 26/10/2026)

> Fonte de cena do demonstrativo e do expert. UGC NÃO usa take genérico do banco (regra abaixo). Edição: `EDICAO-PADRAO.md`.


### §E.0c — Demonstrativo "mesa real" animada (imagem→vídeo, validado 20/10/2026)

Complemento ao Modo E de gravação de tela: em vez de só b-roll + tela gravada,
gera uma FOTO orgânica realista da pessoa com o aparelho/páginas reais na mesa e anima ela
direto no Flow (imagem vira 1º frame do vídeo). **Não é alternativa — é mandatório em TODO vídeo
da leva, junto com a tela gravada (regra da dona, 24/10/2026): cada peça monta os DOIS,
gravação de tela real do entregável + take mesa real do Flow.** Vídeo só com um dos dois está
incompleto.

**Antes de gerar qualquer imagem desse tipo, pense (não invente):**
- **Cenário**: mesa de casa real, luz de janela, props do dia a dia — nunca estúdio.
- **Quem aparece**: a persona da oferta (gênero, idade, como ela é de verdade — ver
  `pesquisa/PERSONA-E-ANGULOS.md` da oferta). Nunca genérico.
- **Páginas do entregável**: SEMPRE arquivo real anexado (`produto/ENTREGA/`), nunca a página
  inventada pelo modelo — mesma regra do Gate 0.1 de `criativo-ads`.

**Receita (2 ferramentas, nessa ordem):**
1. `gpt-imagem-playwright` — gera a foto-base (1 cena por mensagem, chat novo, referências reais
   anexadas: capa + 2-3 páginas do entregável + identidade visual). 9:16, sem texto/legenda
   queimada (a legenda final é sempre Remotion KaraokeV2 depois). Composição = uma das letras
   do CATÁLOGO abaixo.
2. `mecanica-flow.md` — anima a foto aprovada: upload por interceptação CDP
   (`Page.setInterceptFileChooserDialog` + `DOM.setFileInputFiles`, NUNCA o fallback
   prompt-only, que perde a imagem exata), 9:16, prompt só do MOVIMENTO (câmera/mão/dedo —
   a composição já está na imagem, não repete a cena inteira em texto).

#### Catálogo de takes — como pedir

Pra pedir, basta dizer **a letra** ("quero a take B desse criativo") ou **descrever a cena** em
1 frase ("quero uma de notebook" → cai na C). Quem gera cruza com `PERSONA-E-ANGULOS.md` pra
decidir QUEM aparece (gênero/idade) e quais páginas reais mostrar — nunca pede confirmação óbvia,
só avisa a escolha.

**Sem letra ("produz as takes dessa oferta", "faz o demonstrativo mesa real") = escolha
automática.** Não pergunte qual letra — espalhe sozinho **2-3 letras bem diferentes** entre si
(ex.: uma com pessoa + uma só-mão/sem-rosto + uma 100% papel, nunca duas parecidas), busque as
páginas reais certas pra cada cena (`produto/ENTREGA/`, 2 a 5 páginas conforme a cena pedir — nunca
só a capa) e produza as 2-3 até vídeo final, avisando no fim quais letras saíram e por quê.

| Take | Composição | Movimento no Flow |
|---|---|---|
| **A** | Multi-aparelho: notebook+tablet+celular na mesa, cada tela uma página diferente, pessoa aparece e aponta pra um detalhe numa das telas. | Só o dedo e leve drift de câmera. |
| **B** | Só a MÃO (sem rosto/corpo) + 1 tablet na mesa + páginas impressas soltas ao redor. | Dedo apontando + drift leve. |
| **C** | Notebook como peça central (tela com 1 página), páginas reais espalhadas do lado, pessoa aparece. | Dedo/mão + drift leve. |
| **D** | Páginas FÍSICAS impressas empilhadas/meio-fanned na mesa, SEM tela nenhuma, 100% papel. | Só drift de câmera (ninguém mexe, parece que vai folhear). |
| **E** | Tablet + caneta tipo Apple Pencil apontando/riscando um detalhe na tela, zoom — estilo "apresentador". *(pendente de gerar)* | Caneta se movendo + zoom. |
| **F** | Tablet E celular PARADOS lado a lado na mesa (cada um com uma página), SEM mão mexendo/rolando nada — a cena é estática. | **Movimento de câmera NATURAL/cinematográfico** (drift/pan leve, como mão segurando o celular gravando) aproximando das telas — **nunca zoom de lente puro/mecânico que corre reto até o ponto** (regra da dona, 20/10 + reforçada 24/10: "zoom até o ponto e para" parece automação; o certo é câmera se aproximando devagar, orgânico). Imagem de referência aprovada: `~/Downloads/ar-takeF.png`. |
| **G** | Tablet segurado BEM DE PERTO pela pessoa (close-up na mão/peito, não na mesa), página real na tela, enquadramento fechado. | **Zoom de câmera** aproximando mais ainda, sem a pessoa mexer o braço. |
| **H** | POV: a PRÓPRIA mão da pessoa segura o tablet lendo (ângulo em primeira pessoa, como quem fotografa o próprio colo), 1 página real na tela. | Dedo ou caneta mexendo/rolando a tela + leve drift. |
| **I** | Flat-lay limpo: 2 páginas IMPRESSAS reais levemente sobrepostas, vista de cima, mesa de madeira, caderno fechado + caneta do lado — SEM mão, SEM device, SEM pessoa. | Só zoom/drift bem sutil de câmera (cena estática de propósito). |

| **J** | TV grande em primeiro plano com a página real cheia (tela, não papel), caneta apontando pra ela; tablet + notebook menores e desfocados ao fundo/embaixo, de apoio. | Caneta risca diagonal, do canto superior até embaixo da tela, **câmera dá zoom junto** (não fica parada) — os dois movimentos simultâneos, não um depois do outro. |

| **K** | Over-the-shoulder: câmera ATRÁS da pessoa (só cabelo/ombro em quadro, rosto nunca aparece), tablet na mão dela de frente mostrando a página real, dedo tocando a tela. | Dedo tocando um ponto + zoom de câmera aproximando por trás do ombro. |

| **M** | Mesa com VÁRIAS páginas físicas espalhadas (5+, diferentes cartas), a mão folheia/desliza uma por cima da outra revelando cada página em sequência — câmera PASSEIA pela mesa acompanhando (pan), não fica parada num ponto só. Mostra volume e variedade, não uma pilha estática. Referência: vídeos de concorrente analisados 20/10 (`pesquisa/referencia-vsl` style, folheando cartas uma a uma). | Mão folheando + câmera em pan contínuo acompanhando o movimento — mais dinâmico que a D (que é só drift sutil numa pilha parada). |
| **L** | Close-up na tela de um celular mostrando página real. Dois dedos (polegar+indicador) visíveis fazendo o gesto físico de pinça (pinch-to-zoom) sobre a tela — igual quem dá zoom numa foto no próprio celular. Resto do corpo fora de quadro. | Os dois dedos abrindo em pinça, tela ampliando o detalhe em sincronia com o gesto (zoom = ação da mão, não só drift de câmera). |
| **N** | Mão segurando o material como um LIVRO fechado (capa do entregável bem visível, como produto físico) e depois abrindo em livro, mostrando 2 páginas reais abertas lado a lado. Ou só a capa sendo exibida pra câmera, sem abrir — o que fizer sentido pro criativo. | Mão abre o "livro" revelando as 2 páginas + leve drift de câmera; ou só sustenta a capa com leve drift, sem mecânica de abrir. |
| **O** | 100% papel: VÁRIAS páginas reais impressas espalhadas/semi-empilhadas na mesa (como M), e por CIMA delas a mão segura a CAPA do entregável virada pra câmera — as páginas de baixo ficam parcialmente visíveis/espiando pelas bordas, mostrando que tem conteúdo por trás da capa. Referência: `~/.overclock-app/dropped/1792854006010-pasted-image.png`. | Só drift/zoom cinematográfico leve de câmera, mão parada segurando a capa (sem abrir/folhear) — variação mais estática que N, serve pra diversificar a leva. |

### Regras fixas 24/10/2026 (dona) — valem em toda take, novas e antigas

- **Combinação obrigatória de material em cena:** sempre **1-2 aparelhos digitais** (celular/tablet/notebook,
  qualquer combinação) **+ 3-4 páginas impressas soltas**. Nunca só papel, nunca só tela — a combinação é
  o padrão, salvo a take ser deliberadamente 100% papel (D, I) ou servir de variação proposital.
- **Nada repete, em lugar nenhum da cena:** o que está numa tela não aparece em outra tela nem numa folha
  impressa; cada folha impressa mostra uma página diferente das outras folhas e das telas. Dispositivo e
  folha = sempre conteúdo exclusivo.
- **Zoom corrigido 24/10 (2ª rodada):** o zoom que a dona quer é o de CÂMERA, só que **cinematográfico/
  orgânico** — câmera se aproximando devagar como se uma pessoa estivesse filmando/segurando o aparelho,
  NUNCA o zoom mecânico que corre reto até o ponto e para ("zoom de lente", tipo motion graphics). A
  diferença é o movimento: orgânico tem leve imperfeição/drift, não é uma trajetória perfeita e previsível.
  **Gesto da mão é, por padrão, APONTAR** (dedo indicando o trecho, como M/K), não pinça. **Pinça
  (pinch-to-zoom, extensão/expansão) é EXTRA opcional**, só quando a cena pedir (ex.: tablet no colo/na
  mão, dá pra ela "esticar" uma parte com os dedos) — se não couber na cena, não force, use só o apontar
  + o zoom de câmera orgânico.
- **Folha impressa sempre proporção A4:** retrato (~1:1.414) na maioria dos casos; se a página do
  entregável for deitada, a folha é A4 **landscape** (~1.414:1), nunca uma proporção fora disso tipo
  "mini-folha" quadrada ou esticada — fica torto/feio e denuncia que não é impressão real.
- **Capa é bem-vinda:** incluir 1 página/plano com a CAPA do entregável (como produto físico) é um reforço
  bom em qualquer take — soma-se às 3-4 páginas de conteúdo, não substitui.
- **Prop tipo "livro":** segurar o material fechado como livro (capa visível) ou aberto mostrando 2 páginas
  reais lado a lado (take N) é uma composição válida sempre que fizer sentido pro criativo — não é
  obrigatória, é mais uma ferramenta do catálogo.
- **O mesmo acabamento orgânico do estático vale no vídeo:** cara de foto/filmagem real de iPhone, sem
  legenda queimada na cena (a legenda final é sempre Remotion depois) — não é um visual separado, é a
  MESMA regra de `criativo-imagem-organica-iphone` aplicada ao frame de vídeo.
- **Expert pensado ANTES, não genérico:** rosto/idade/gênero/figurino do expert tem que combinar com a
  oferta e com quem exerce aquele papel na vida real — ex.: oferta pra cuidador de idoso → expert com cara,
  idade e roupa de cuidador profissional de verdade (não qualquer adulto de jaleco). Decidir isso lendo
  `pesquisa/PERSONA-E-ANGULOS.md` da oferta ANTES de gerar a imagem-base, igual se faz pro estático.
- **Voz: gerar primeiro para acertar a boca, trocar depois.** Pode gerar a cena no Flow com qualquer voz
  (inclusive a nativa do Flow, mesmo sendo ruim) só pra garantir que o lip-sync/movimento de boca saia bom;
  o áudio final da fala é sempre trocado pela nossa voz fixa (`narracao-hub-tts`, Rocha) antes de entregar —
  nunca a voz do Flow fica no criativo final.

**⛔ UGC não usa take genérico do banco compartilhado (regra da dona, 25/10/2026, caso CT22
Atlas/Nico).** `FLOW-TAKES/take-geral`/`take-C` (§E.0c, "reaproveitáveis em todos os 10 vídeos")
servem pro **demonstrativo** (mão anônima, sem persona — mesa real sem rosto). Peça rotulada
**UGC/UGC** é outra coisa: é recomendação de UMA pessoa específica — o corpo tem que mostrar ESSA
pessoa segurando o material, cena gerada só pra ela (imagem GPT da persona segurando o produto +
Flow i2v), nunca o clipe de mão genérica do banco. Usar o take compartilhado numa peça UGC quebra
o formato: hook mostra rosto, corpo vira mão anônima sem conexão — lê como demonstrativo, não
recomendação. Sinal de que errou: a mesma mão/mesa aparece em UGC de personas diferentes na leva.

**Preferência padrão: pessoa de COSTAS/over-the-shoulder, não de frente (regra da dona,
20/10/2026).** Quando a take tiver pessoa (A, C, G, K…), o padrão é rosto NÃO aparecer — só
cabelo/ombro/mão, como a K. Rosto de frente só entra se o criativo realmente precisar (ex.:
reação, expressão). Motivo dela: fica mais orgânico, "menos cara de IA" (rosto gerado de frente
entrega mais o giveaway de IA que o corpo de costas). Aplicar isso como padrão em qualquer take
nova que incluir pessoa, a menos que a cena peça expressão facial.

**Diversifique IMPRESSO × DIGITAL na mesma leva** — não repita só tela (regra da dona, 20/10):
D e I são 100% papel; A/B/C/F/G/H têm tela. Uma leva boa mistura os dois tipos, não só variações
de "gente com tablet".

**Regra fixa em TODA take (já embutida no prompt do Flow, não é opcional):** dentro de UM clipe
os elementos nunca mudam do início ao fim — nada aparece, some ou pisca (`nothing ever flickers
or changes content`, `no jumping, no cuts`). Composição pode variar LIVRE de take pra take (A
vira G sem problema); dentro da MESMA take é sempre a mesma cena, só com o movimento pedido.

Toda letra nova que não existir ainda: criar seguindo o mesmo gate (cenário real + persona pensada
+ páginas reais anexadas) e **acrescentar linha nesta tabela** depois de validada — é o catálogo
vivo, não lista fechada.

Depois do clipe cru: segue o acabamento normal (KaraokeV2, `narracao-hub-tts`, gate de
`acabamento-natural-audio-cortes.md`) igual qualquer outro take. Pasta: `criativos/<MERCADO>/
CRIATIVO-N/take-<letra>/`.

