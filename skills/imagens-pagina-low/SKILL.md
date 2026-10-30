---
name: imagens-pagina-low
description: Gera todas as imagens de uma página de vendas low ticket — capa/mockup do produto, mockups dos bônus, prints do conteúdo por dentro, fotos das pessoas dos depoimentos e a foto de pessoa segurando o material impresso. Usa gpt-imagem-playwright (ChatGPT, perfil gpt) como padrão e o NinjaBR Hub como fallback quando a cota do GPT estoura. Define o que cada imagem tem que mostrar, incluindo a regra de headline na capa. Use quando o usuário pedir imagens da página, mockup, capa do produto, imagem de bônus, foto de depoimento, pessoa segurando o material, ou quando for preencher os "Espaço da imagem" do MODELO-PAGINA-LOW.
---

> **HUB DESATIVADO (02/10/2026, ordem da usuária):** NinjaBR Hub está SEM COTA e os perfis `hub`/`hubv2`/`hubts` foram removidos (backup em `~/.agent-profiles/_removidos-hub-2026-10-02/`). NÃO use Hub, NÃO rode `hub-livre.sh` (sai com erro), NÃO espere perfil do Hub liberar. Imagem: ChatGPT — se a cota de upload de uma conta acabar, troque de CONTA: `gpt-conta*` ↔ `gpt-conta*`. Vídeo: Google Flow (`flow-video-playwright`).


# imagens-pagina-low

Preenche os slots de imagem do modelo de página low ticket. **Executa, não explica.**

## ⛳ ORDEM NOVA (dona, 14/10/2026) — MOCKUPS DA PÁGINA PRIMEIRO, MVP DEPOIS

Vale pra toda oferta (mesmo mercado e cross-market). **Sobrescreve** qualquer trecho abaixo que diga
"mockup só depois do MVP". É simples — um pedido só no GPT:

1. **Paleta definida ANTES de qualquer imagem**, já aplicada no NOSSO HTML. **Padrão = as mesmas cores
   da página original** (sem perguntar); só muda se a dona pedir outra paleta pra essa oferta (30/10/2026).
   Sem paleta fechada no HTML, não gera imagem (senão tem que ajustar o HTML depois e refazer).
2. **Baixar todas as imagens da página de referência** (todo `src` do clone) →
   `pesquisa/referencia/imagens-origem/`.
3. **Um chat no GPT** (gpt-imagem-playwright). Prompt SIMPLES, sem engenharia (regra da dona, 14/10/2026 —
   "GPT já é inteligente, só precisa de contexto; não inventa cor nem nada, a imagem tem que ser assim,
   diferente"): anexa a imagem original + nosso `index.html` atualizado (paleta já definida) e diz
   *"Estou adaptando esta página pra essa nova modelagem [nome da oferta + o que ela entrega, do
   MANIFESTO]. Preciso adaptar esta imagem pra minha oferta — mesma cena/composição, só o conteúdo
   trocado."* Pode ser tudo num lote (imagem a imagem anexada) ou uma de cada vez se der problema —
   sem diferença de resultado, escolher pelo que for mais estável no GPT no momento.
   **Escopo = TODAS as imagens da página**, incluindo as de depoimento/prova social (foto de pessoa
   segurando o material) — **só com aprovação explícita da dona pra ESSA oferta** (ela decide se quer
   nome/depoimento reais ou adaptados; sem essa aprovação, segue a regra padrão de prova social só real
   e esse bloco fica placeholder).
4. **Imagens "por dentro" (páginas internas do produto) ficam pra DEPOIS:** primeiro escreve/gera o MVP,
   e aí usa as páginas reais do MVP como referência visual pra essas imagens.
5. Plugar na página → **dona valida** → lote do MVP → imagens "por dentro" com o MVP de referência.

## ENTREGÁVEL — primeiras páginas e páginas de imprimir (dona, 30/10/2026)
1. **Texto da entrega escrito inteiro antes** (todas as páginas; cada exercício/pôster já descrito: conteúdo +
   como fica na folha).
2. **Primeiras páginas = as imagens "por dentro" da página original** (`pesquisa/referencia/imagens-origem/`:
   páginas internas, mapas, pôsteres, folhas que o concorrente mostra). Cada uma refeita no GPT pra NOSSA
   oferta: mesma composição, nosso conteúdo (do texto), nosso idioma, cor só muda se a paleta mudou.
3. **Apresentar essas primeiras páginas à dona** → ela avalia → só então o resto do MVP, usando as aprovadas
   como referência travada.
4. **Nunca HTML/SVG/Pillow/código** — toda página é imagem do GPT, A4, mesma cara visual.
5. **Item de fazer/imprimir = página própria, sempre:** exercício, pôster, folha, checklist, mapa, tabela de
   preencher. A explicação fica numa página e a folha de fazer/imprimir na **página seguinte** — nunca só a
   página de explicação. Mecânica de geração dessas folhas: `gpt-imagem-playwright` § "Páginas de ATIVIDADE".

## PASSO 0 de toda entrega — montar a REFERÊNCIA / design system ANTES de qualquer lote

Primeira coisa ao produzir uma entrega: definir a identidade visual como imagens de referência.
1. Usar as referências que já temos (mockups do concorrente, design da página).
2. **Se não tiver referência boa pra algo, PERGUNTAR ao dono** se ele tem imagem de referência ou um
   design da página. Não inventar.
3. Com a referência em mãos, gerar as imagens-guia de cada peça (capa, cada tipo de seção/página,
   cada bônus) = o design system do produto. Validar e TRAVAR.
4. Só então gerar o lote, sempre anexando as imagens-guia travadas. Nunca o lote sem identidade antes.

## ⛔ MODELAGEM (copiar entregável/mockup de um concorrente validado) — regra dura

Causa de retrabalho real (21/09/2026): pediram "pega a imagem deles e muda SÓ cor + idioma" e o prompt
foi escrito DO ZERO com identidade nova (fundo escuro, card místico elaborado) → GPT inventou → refez tudo.

**Casar o TIPO da referência com o TIPO da peça (erro real 21/09):** pra gerar uma CAPA você anexa
uma CAPA (mockup do produto), não uma página de conteúdo. Página-diagrama puxa página-diagrama;
página-exercício puxa página-exercício; bônus puxa capa de bônus. Referência de tipo errado = saída
errada. Os entregáveis todos aparecem na PÁGINA DE VENDAS — puxe de lá o mockup do tipo certo.
No prompt do GPT diga o que é: *"Esta é minha página/referência visual. Quero fazer a CAPA deste
produto a partir deste mockup de capa"* — dá contexto do que a peça É, não só "edita a imagem".

| Peça a gerar | Referência que anexa |
|---|---|
| Capa do produto | mockup do produto (ex: `producto-basico.webp`) |
| Página-diagrama (arcano) | página-diagrama (ex: `map-fool.webp`) |
| Página-exercício (caderno) | página-exercício (ex: `practice-fool.webp`) |
| Capa de bônus | capa de bônus (ex: `b1.webp`) |

**Prompt pro GPT = pacote COMPLETO, não frase solta.** Anexe e nomeie tudo que tiver:
- **Referência** → a imagem do tipo certo ("esta é a referência de layout/capa").
- **Contexto** → o que o produto é, o que a peça é, o texto que vai na peça (do ENTREGAVEL-TEXTO).
- **Design system** → identidade travada (paleta/moldura/tipografia) quando já existir a IDENTIDADE-REF.
Se tem referência, manda referência; se tem contexto, manda contexto; se tem design system, manda design
system. GPT preenche lacuna inventando — então não deixe lacuna.

> **FUNDO vem da PÁGINA JÁ GERADA, nunca de uma lista de hex.** Se a oferta já tem
> peça aprovada (IDENTIDADE-REF ou entrega feita), ABRA-A e copie qual cor FORMA o
> fundo vs. qual é só tinta/accent. Nunca promova um hex de accent de um .md a cor
> de fundo. Erro real (Mapa do Tarot, order bumps 09-21): "violeta #6D4AA0" saiu de
> uma lista e virou o FUNDO — mas o fundo real é pergaminho creme #F5EFE6 e o roxo é
> só a tinta. Fundo errado = identidade inventada = REPROVAR e REGERAR ancorando na
> página gerada.

### **Passar SEMPRE a nossa identidade visual pro GPT (extrair + print) — aplica a TODA peça**

Método comprovado (21/09/2026): TODA geração de imagem — entregável (páginas), mockup, capa, bônus,
depoimento, banner, tudo sem exceção — começa com a extração da identidade visual NOSSA, nunca deixar
o GPT adivinhar ou inventar estilo.

**Passo 1: Extrair do design system / CSS da página**
- Paleta de cores: cor primária (hex), cor secundária, fundo, cor de texto. Tirar do `index.html` ou
  do CSS da página, não "que cores você acha que seria legal".
- Tipografia: fonte display (títulos), fonte de corpo (texto), pesos usados. Copiado exato do projeto.
- Estilo geral: minimalista? cards? moldura grossa? ilustração geométrica? Caracterizar em 1-2 adjetivos
  reais baseado no que a página mostra.
- Salvar numa nota rápida com os tokens reais (ex: `#7B4397` `#E8D4F8` `Montserrat Bold + Lato Regular`)
  — isso vai pro prompt do GPT palavra por palavra.

**Passo 2: Declarar EXPLÍCITO no prompt do GPT**
- Nunca: *"Cria uma imagem bonita de tarot"*.
- Sempre: *"Quero MEU visual assim: cor primária #7B4397, cor secundária #E8D4F8, tipografia Montserrat
  Bold + Lato Regular, estilo clean/minimalista/card-based. Fundo #F5F1FA. Sem cara do concorrente,
  100% nossa identidade."*
- Amarrar o prompt à identidade extraída acima (copiar os tokens) — lagoa no prompt = GPT inventa.

**Passo 3: Se precisar de referência visual, PRINTAR a página no ar**
- Print de NOSSA página de vendas ao vivo (screenshot do desktop da `index.html` rodando).
- Print da NOSSA área de membros (if exists) ou página de conteúdo própria.
- Anexar essas prints no chat do GPT como *"Esta é minha identidade visual, siga exatamente este padrão
  de cores/fontes/layout. Cria a imagem COM esta paleta e este estilo."*
- Não mandar print da página do concorrente como se fosse a nossa — sempre a NOSSA página de verdade.

**Passo 4: Conteúdo e referência de MESMO TIPO**
- Quando a peça precisa de referência visual (capa, diagrama, exercício): anexar a imagem/página DE NOSSO
  PRODUTO (ou upload do arquivo `.webp`/`.png` nosso, ou link público da página rodando).
- Fonte de conteúdo sempre NOSSA: título copiado do `index.html`, textos da `ENTREGAVEL-TEXTO.md`,
  imagens já aprovadas da pasta `IDENTIDADE-REF/`.
- Nunca pedir ao GPT "extrai o estilo da página do concorrente" — sempre "segue ESTA imagem/cor/estilo
  QUE EU MANDO".

**Passo 5: Validar no resultado**
- Paleta saiu certa? Montserrat Bold + Lato Real? Fundo #F5F1FA?
- Texto 100% PT-BR, zero espanhol, zero caracteres estranhos?
- Layout/estilo é o nosso (clean/minimalista) ou copiado do concorrente (chique/afetado/cores vibrantes)?
  Se virou estilo do concorrente → **REPROVAR e REGERAR** com o token de cor/fonte EXPLÍCITO no prompt.
- **Objetivo:** cada peça sai idêntica visualmente (mesma paleta, mesma fonte, mesmo layout) → entrega
  toda consistente. Zero variação aleatória de estilo entre páginas.

### 🚨 VALIDAÇÃO CRÍTICA DO OUTPUT: nunca arte/mockup do concorrente numa peça nossa, nunca asset dele sem substituir

> **Cross-market (outro país/idioma):** aqui o método é o contrário do MVT — as imagens, mockups e entregável DELE são
> ADAPTADOS (mesma peça, só idioma + nossas cores). "Arte do concorrente" proibida = a peça CRUA, que não passou pela
> adaptação (texto na língua de origem, cor antiga). Ver seção "Cross-market: TODAS as imagens" logo abaixo.

**Ordem correta da entrega:** (1) entregável pronto → (2) construir os NOSSOS mockups (nossa identidade/idioma) → (3) SUBSTITUIR na página de vendas os mockups do concorrente pelos nossos adaptados → (4) só então banner, usando os NOSSOS mockups já publicados. Nunca usar o mockup/arte do concorrente numa peça nossa, nem deixar mockup do concorrente na página sem substituir.

**O critério é a peça ser arte do concorrente — não o idioma.** Texto em espanhol ou visual idêntico ao do concorrente é no máximo SINTOMA possível de ter usado a arte dele; não é a regra em si.

**Após o GPT gerar, VERIFICAR SEMPRE:** a imagem é uma peça NOSSA (gerada/adaptada por nós) ou é a arte do concorrente colada sem passar pelo processo? Cor de fundo é NOSSA paleta, não do original? Nenhum visual ou estilo copiado direto do concorrente? Se a peça é arte do concorrente reaproveitada sem virar nossa (sintomas comuns: texto em ESPANHOL, cores erradas, design que não é nosso) → **REPROVAR E REGERAR**. Isso não é refinamento — é violação da identidade do produto. Modelagem ≠ copiar visual do concorrente pra nossa página. Modelagem = recriar na nossa identidade (cor + idioma + marca). Toda peça (capa, diagrama, exercício, bônus) sai 100% nossa (PT-BR + paleta nossa). Se não saiu assim, não valida.

Quando a tarefa é MODELAR um visual que já existe (mockup/página do concorrente), o fluxo é EDITAR a
referência, não gerar do zero:
1. **Anexar a imagem de referência do TIPO CERTO** no GPT (a própria imagem deles), dizendo qual peça
   você está fazendo (capa/página/bônus).
2. Instrução curta e literal: *"Mantenha exatamente este layout, ilustração, composição e estilo.
   Mude SÓ (a) a cor principal para {NOSSA COR} e (b) o idioma dos textos para {IDIOMA}, usando estes
   textos: …"*. Nada além disso.
3. **Não** inventar fundo, estilo, moldura ou ilustração novos. **Não** deixar mais elaborado que a
   referência — se ficou mais "chique/afetado" que o original, está ERRADO.
4. Ilustração clássica de domínio público (ex: gravura de carta de tarot) pode ser mantida igual —
   não reinventar. Só não copiar personagem/arte protegida por direito autoral.
   **Peça ao GPT a ilustração de domínio público EXPLÍCITA** (ex: "carta de tarot Rider-Waite,
   domínio público") em vez de deixar ele inventar imagem genérica/aleatória (ex: uma lua qualquer).
   Nicho com iconografia canônica de domínio público (tarot, astrologia, runas) → usar a arte real
   clássica, não símbolo inventado.
5. Manter simplicidade (estilo caderno/workbook, fundo claro se o original é claro).
Regra vale pra entregável, mockup, capa e bônus na modelagem cross-market ([[modelagem-cross-market]]).

#### Cross-market: TODAS as imagens da página num lote só (WORK MODE) — decisão do dono 27/09/2026
> **Atualização 05/10/2026:** quando muda **só o idioma** (nossa oferta indo pra outro país, oferta gringa vindo pro BR com as cores dele, pt-BR→pt-PT), a rota padrão é `traduzir-entregavel-imagem` — apaga o texto e reescreve por script, sem regenerar (arte intacta, sem cota de GPT). GPT Work Mode abaixo fica para quando também precisa trocar as cores.
Levar oferta validada de um país pro outro = manter o que já converte. Vale pra imagens da página,
MOCKUPS e ENTREGÁVEL (páginas do produto/bônus), salvo ordem contrária do dono. As imagens da página dele
são ADAPTADAS (não recriadas do zero): **identidade visual dele predominante, muda SÓ idioma e cores**.
Ordem: (1) página nossa pronta primeiro = CLONE LITERAL (DOM renderizado + CSS compilado do original, mesmas
classes/tamanhos/blocos; muda só texto, variáveis de cor e src — nunca reconstruir layout) + paleta ajustada "um pouco"
(mesma claridade de fundo; DESIGN-SYSTEM.md gravado); (2) GPT em
WORK MODE (receita `domain-skills/chatgpt.com/work-mode-lote-entrega.md`), UM pedido com o lote
inteiro: link da página original + nosso `index.html` anexado + as imagens originais + os tokens de cor
do DESIGN-SYSTEM + tabela arquivo→texto PT de cada imagem. Prompt-base: *"Estou modelando esta oferta
(link original). Já troquei as cores e adaptei pro português do Brasil (HTML anexo). Adapte TODAS estas
imagens pro português do Brasil e pras nossas cores, mantendo a identidade visual, layout, ilustração e
composição de cada uma — mude só idioma e cores."* (3) contact sheet original × nossa, lado a lado:
reprovar a que manteve texto na língua de origem, cor antiga, ou que mudou layout/ilustração.

### Carta/item citado = SEMPRE com a ilustração (regra geral p/ qualquer nicho)
Toda vez que uma página CITA uma carta/item que tem imagem canônica, mostrar a ilustração junto — nunca só o nome em texto:
- **Uma só** citada → destaca GRANDE, ilustração central da página.
- **Várias** citadas (lista, sumário, "22 arcanos", combinações) → thumbnails PEQUENAS ao lado de cada nome.
Vale pra tarot (cartas), astrologia (signos), runas etc. Sem ilustração a página fica seca e o GPT tende a preencher com texto embolado.

### Variar orientação da página (retrato × paisagem)
Não deixar tudo no mesmo formato. Página com muito diagrama/muitas caixas/leque de cartas → **paisagem (deitada)**, cabe mais e o texto respira. Página de exercício/leitura corrida → **retrato (em pé)**. A variação dá ritmo à entrega e evita texto espremido. Manter a mesma identidade visual em ambas.

### Capa ≠ mockup — não confundir os dois artefatos
- **CAPA** = imagem ÚNICA, limpa (só o card/arte principal). É uma página da entrega.
- **MOCKUP** (produto-shot: leque de páginas + tablet no meio, fundo recortado) = feito DEPOIS, quando as páginas soltas reais já estão prontas e legíveis; usa páginas REAIS como recorte. É pra página de vendas, não é a capa.
- Nunca gerar a capa modelando um mockup (sai com fundo recortado e leque de texto garatuja). Capa modela capa; mockup se monta no fim.
- **Mockup só depois das páginas prontas.** Com as páginas soltas REAIS em mãos (capa da entrega, página de seção/conteúdo, capa do bônus, página do bônus etc.), aí sim monta o leque/produto-shot usando essas páginas de verdade — nunca com página inventada ou texto garatuja. Sequência: gerar entrega → validar páginas → só então mockup.
- **Mockup multi-dispositivo (formato padrão, dá percepção de valor):** mostrar o produto em VÁRIOS formatos ao mesmo tempo — **tablet no centro** (a capa/página principal), **celular na lateral**, um **desktop/PC** também, e **páginas soltas em leque atrás**. Passa a sensação de "acessa em qualquer tela" e enche o olho. Sempre com as páginas REAIS renderizadas nas telas.
- **Mockup "completo" = combo do que se vende:** montar o produto principal + as **CAPAS dos bônus** + **páginas soltas do principal** juntos na mesma imagem. Mesmo sem o conteúdo dos bônus pronto, basta ter a CAPA de cada bônus pra compor — passa a percepção de "olha tudo que vem". Ou seja: gerar cedo as capas dos bônus (barato) pra já ter mockup completo, e completar o conteúdo depois (MVP 40%).

**Travar a identidade validada como REFERÊNCIA e reusar.** Quando a amostra (capa + páginas de
exemplo) for aprovada pelo dono, SALVAR essas imagens aprovadas numa pasta de referência do produto
(ex: `produto/ENTREGA/IDENTIDADE-REF/`). Ao gerar TODO o resto da entrega (demais páginas, arcanos,
bônus), **anexar essas imagens aprovadas como referência visual** em cada geração — mesma paleta,
moldura, tipografia, layout. Assim a entrega inteira sai consistente, não cada página num estilo.
Nunca produzir o lote sem a identidade travada antes.

## Oferta irmã / clonada de outra oferta nossa: auditoria de herança (Cigano ← Tarot, 05/10/2026)

Página clonada de outra oferta nossa herda texto e imagem errados sem ninguém ver. Antes de publicar:
- **Nenhum asset do produto-mãe.** Folha de contato de TODA imagem referenciada pelo `index.html` (e pelo painel), classificando o que cada imagem mostra de verdade, não o nome do arquivo. Qualquer título ou carta do produto-mãe = refazer.
- **Texto dos bônus = entregável real.** Nome, descrição, `alt` e valor riscado de cada card, mais as listas ✓/✗ dos planos, o popup e "tudo incluído", conferidos contra a pasta do produto. Item herdado que não existe ("modelos de leitura", "naipes") sai.
- **Bônus ≠ order bump.** Item vendido como bump não aparece como bônus grátis do Completo. A estrutura de planos e bumps espelha a oferta-mãe, a não ser que a dona decida outra coisa.

## Mockup: o que reprova (05/10/2026)
- **Recorte de print não é mockup.** Tablet ou celular cortado na borda, texto cortado embaixo = refazer por composição, com o device inteiro.
- **Básico e Completo com imagens diferentes:** Básico = só o principal; Completo = principal + capas dos bônus. A mesma imagem nos dois cards esconde o valor do Completo.
- **Capas de bônus no mesmo padrão** (livro 3D em perspectiva, se os outros são assim). Capa chapada no meio de capas 3D destoa. Duas capas com a mesma carta ou arte ficam iguais: cada uma mostra o próprio conteúdo (folha de consulta = grade das cartas).
- **Nada de jargão interno na arte.** Rodapé ou selo com "Order bump", "MVP", "placeholder" é texto que o cliente vê.
- **Conferir na página no ar a 390 px e a 1280 px** que nenhum mockup sai cortado.
- **Mockup de app só depois que o app existe** e abre no painel. Vender o app pelo mockup sem o app pronto = promessa falsa.

## Imagem de PRODUTO/oferta (capa de checkout, card e banner da área) — boa × feia (dona, 16/10/2026)

Aplica a **toda imagem de produto**: foto do produto no checkout, card da área de membros, banner
de oferta de membro. Mesma régua do mockup — mas aqui o inimigo é a arte "feia/genérica".

**BOA (referência aprovada, Diário Astral 16/10):** mostra **o produto em uso** — o que a pessoa
recebe na mão (tablet/app/PDF com a **tela legível**, o entregável visível) — numa **cena
aspiracional da persona** (velas, livros, cristal, fundo estelar), na **paleta da marca**
(roxo/dourado), com acabamento **premium** (luz, profundidade, sombra) e **título legível +
subtítulo curto** ("Seu horóscopo personalizado"). Ref.:
`MODELOS/REFERENCIAS-VISUAIS/produto-mockup-bom-exemplo-diario-astral.png`.

**FEIA / reprova:** produto **invisível ou abstrato** (símbolo solto, "clima" sem entregável),
colagem tosca, capa chapada, **fundo chapado sem cena**, cara de **template**/clipart, baixa-res,
**texto torto ou errado** na arte, imagem **genérica de IA**. **Caso real:** as imagens antigas do
**Diário Astral (GGCheckout)** reprovaram por isso e foram refeitas — e o 1º banner do Diário na
área de membros (16/10) também ("muito feia", trocada pela arte do tablet na cena mística).

**Regras práticas:**
- **Mostrar o produto** — o entregável tem que estar visível e legível na arte.
- **Cena coerente** com persona/marca (não fundo chapado); paleta do `DESIGN-SYSTEM` da oferta.
- **Sem preço queimado** na arte (preço sai do HTML/fonte única; vale pra banner da área).
- Razão/tamanho certos: produto/capa **quadrado ~1:1**; banner da área **1600×533 desktop** +
  **778×836 mobile**; **webp leve** (≤ ~120 KB); **achatar em fundo** (nunca PNG RGBA solto).
- Banner de oferta **lê a arte + a faixa HTML** de uma **fonte única** (uma tabela de ofertas);
  a faixa **lista o que vem** em bullets curtos (não parede de texto).
- Antes de aceitar: abrir no **390 px e no desktop** — arte cortada ou texto comendo borda = refazer.

## 📱💻🖨️ MOCKUP SEMPRE EM DISPOSITIVOS + IMPRESSO (regra da dona, 14/10/2026 — IMPORTANTE)

**Todo mockup de produto mostra o material em: celular + tablet + notebook + folhas impressas**
(na mesa) — e, no composite, as capas dos bônus em pé atrás. É o que mais converte ("acessa em
qualquer tela e ainda imprime"). Mockup só com capa, só tablet, ou objeto solto = reprovado.

Referência APROVADA (anexar no GPT como exemplo de composição):
`assets/exemplos-mockups-jiujitsu/composite-devices-impresso-aprovado.jpg` —
notebook com a capa à esquerda · tablet central com a capa · celular com uma página POR DENTRO ·
folhas impressas de páginas internas espalhadas na mesa · capas dos 4 bônus em pé atrás · fundo e
objetos do nicho na paleta da oferta.

- Capa nos devices grandes; **página real por dentro** no celular e nas folhas impressas (do NOSSO MVP —
  enquanto não houver MVP, o composite espera; nunca página inventada pelo GPT).
- Vale pra modelagem/cross-market também: a cena da referência dá a composição, mas os 4 suportes
  (celular, tablet, notebook, impresso) entram sempre.

## Mockup completo: capa + POR DENTRO + devices (obrigatório)

Toda entrega digital em imagem requer conjunto COMPLETO de mockups que mostre a **experiência do produto**, não só capa fechada. Owner rule (21/09/2026): INSIDE PAGES importam tanto quanto COVERS. Aplica a **PRODUTO PRINCIPAL** e a **CADA BÔNUS** independentemente:

**O que gerar por cada peça (principal ou bônus):**

1. **Capa isolada** — a capa sozinha, limpa, sem moldura de device.
2. **Capa em multi-device** — tablet centralizado exibindo a capa + celular lateral + desktop/PC também → percepção "acessa em qualquer tela".
3. **Página por dentro (OBRIGATÓRIO)** — uma página interna renderizada do produto (exercício ilustrado, diagrama preenchido, checklist, página-exemplo). **Nunca capa de novo**, sempre conteúdo DENTRO da entrega.
4. **Conteúdo espalhado atrás** — leque de 3-5 páginas soltas (papel impresso) mostrando depth do material; texto legível em cada folha.
   **⚠️ Regra dura:** o leque deve exibir **VÁRIAS PÁGINAS DIFERENTES** (conceito, diagrama, exercício, checklist — o que sua entrega tem), nunca apenas uma folha ou a mesma página repetida. Mínimo 3, máximo 5 tipos de página por mockup. Aplica ao PRINCIPAL e a CADA BÔNUS.
5. **Composite final (OBRIGATÓRIO)** — tudo junto: tablet central + páginas soltas em leque atrás + devices laterais + **CADA CAPA DE BÔNUS** (composição que dá percepção "olha tudo que vem").

**Regra aplicável a PRODUTO PRINCIPAL + CADA BÔNUS:**
- Nenhum bônus sai com "capa fechada apenas". Se tem conteúdo interno pronto, gera também a página por dentro daquele bônus.
- Bônus em MVP (só capa aprovada)? A capa dele aparece no composite do principal como item adicional — assim mockup comunica promessa dos bônus sem esperar conteúdo interno.
- Conteúdo sempre das **NOSSAS páginas/covers renderizadas** — nunca placeholder genérico, nunca mockup/interior do concorrente.

**Checklist de aprovação do mockup completo:**
- [ ] Capa isolada renderizada?
- [ ] Capa + inside pages (mínimo 1 tipo: diagrama, exercício, ou página-exemplo)?
- [ ] Multi-device exibido (tablet + celular + desktop)?
- [ ] Cada BÔNUS tem sua capa no composite final?
- [ ] Inside pages dos bônus também renderizadas (quando já prontas)?
- [ ] Texto 100% PT-BR, paleta NOSSA (não do concorrente)?
- [ ] Zero "capa só" — sempre closed cover + mínimo 1 inside page por peça?

**Composição do mockup por TIER de oferta:**

O mockup ACOMPANHA o tier vendido. Dois formatos distintos:

- **Oferta BÁSICA (R$17,90 — só o principal):** mockup mostra capa do produto principal + ALGUMAS páginas internas atrás em leque (3-4 páginas soltas) + device (tablet/celular/PC). Composição simples, focada no core — nenhuma capa ou página de bônus.
- **Oferta COMPLETA (R$27,90 — principal + bônus):** mockup mostra capa do "Completo" + páginas internas do principal + **TODAS AS CAPAS DOS BÔNUS** renderizadas como itens separados + páginas internas dos bônus também em leque atrás. Composição mais densa/cheia (comunica "tudo que vem").

**Regra fixa:** nunca misturar tiers no mockup. Básico mostra SÓ principal (zero bônus); Completo mostra principal + TODOS os bônus visíveis (capas + inside pages quando prontas). Se um bônus ainda está em MVP (só capa), capa aparece no completo; inside fica pronto depois (MVP 40%).

**Nota conceitual:** **Capa isolada ≠ Mockup.** Capa isolada = um artefato único, limpo (a imagem de apresentação). Mockup = composição multi-device + inside pages + bônus completo (usado na página de vendas pra vender valor). Sequência: entrega textual pronta → validar páginas renderizadas → montar mockup composite → publicar na página de vendas.

**Sem referência boa pra algum item?** (ex: um bônus que o concorrente não mostra a arte). Então:
(1) a partir do que você tem (a referência geral do produto), GERAR primeiro as imagens-âncora
daquele item — capa, uma página de seção, etc.; (2) validar e SALVAR como identidade travada; (3) só
então passar essas imagens-âncora pro GPT como referência visual pra gerar o resto do item. Gera a
identidade primeiro, guarda, e produz o lote em cima dela — nunca o lote solto sem âncora.

Mecânica de geração: skill `gpt-imagem-playwright` (perfil `gpt`, porta 9222).
Cota do GPT estourada -> Hub (`hub`, porta 9223), modo Imagem.
Nunca gerar desenho técnico com medida aqui — isso sai de código, não de IA.

**Exemplos de mockup bons (referência de qualidade)** em `assets/exemplos-mockups-*`. O conjunto
`exemplos-mockups-mapa-tarot/` (oferta Mapa do Tarot, modelada do concorrente mapadeltaro.online —
aprovado pelo dono como padrão) tem: mockup principal (`producto-basico`, `producto-bundle`),
páginas internas diagrama+exercício (`map-*`, `practice-*`) e os 4 bônus (`b1`-`b4`), com
`MANIFESTO.md` explicando cada um. Anexar como referência de LAYOUT ao gerar mockups novos (copia a
estrutura, adapta cor/idioma).

## Slots do modelo

| Slot no HTML | Quantas | O que é |
|---|---|---|
| hero / mockup principal | 1 | capa do produto em mockup (tablet + folhas impressas) |
| carrossel demonstrativo | 4-6 | prints do CONTEÚDO POR DENTRO |
| `Espaço da imagem` do WhatsApp | 3-5 | foto que o "cliente" mandou no chat |
| foto do contato do WhatsApp | 1 por depoente | rosto, avatar redondo |
| `Espaço da imagem do bônus` | 1 por bônus | mockup do bônus |
| autoridade | 1 | retrato do especialista |
| prova de uso | 1-2 | pessoa segurando o material impresso |

## Regras de conteúdo (não negociáveis)

1. **Capa/mockup principal:** a headline impressa NA CAPA é a promessa do produto,
   igual à headline da página — mesmo número, mesmo nicho, mesma entrega.
   Nunca texto genérico ("Guia Completo"), nunca headline diferente da página.
2. **Carrossel = conteúdo por dentro**, nunca capa de novo. Cada imagem mostra uma
   página real do produto: exercício ilustrado, checklist, tabela, planner preenchido.
   Se o produto tem 4 tipos de página, o carrossel mostra os 4 tipos.
3. **Bônus:** cada mockup mostra a capa do bônus com o nome exato do bônus na página.
   Estilo visual igual ao do produto principal (mesma família, capa secundária).
4. **Pessoas:** idade, etnia e cenário do público real do nicho, não modelo de banco
   de imagem. Foto de celular, luz de casa, nada de estúdio.
5. **Pessoa segurando o material:** o que ela segura tem que ser reconhecível como
   o produto — mesma capa, mesma cor, mesmo título da capa gerada no slot 1.
6. Texto dentro da imagem sempre no idioma da página (PT ou ES conforme o arquivo).
   Gerou texto torto/errado -> regera, não aceita.

## Prompts base

Trocar `{PRODUTO}`, `{HEADLINE}`, `{NICHO}`, `{PUBLICO}`.

**Capa / mockup principal**
```
Mockup fotográfico de produto digital: tablet na diagonal exibindo a capa de um
ebook e, ao lado, folhas A4 impressas do mesmo material empilhadas.
A capa mostra o título "{HEADLINE}" em tipografia grossa e legível, no idioma
{IDIOMA}, com uma ilustração de {NICHO}. Fundo neutro claro, luz suave de estúdio,
sombra realista, 4:3, alta resolução. Sem marca d'água, sem texto extra.
```

**Conteúdo por dentro (carrossel)**
```
Print de uma página interna de um ebook de {NICHO}, vista de cima, folha branca
impressa sobre mesa de madeira clara. A página mostra {TIPO DE PÁGINA: exercício
ilustrado passo a passo / checklist com caixinhas / tabela de acompanhamento}.
Layout limpo, títulos curtos legíveis em {IDIOMA}, ilustrações simples em linha.
Foto realista de celular, luz natural. 4:5.
```

**Bônus**
```
Mockup do bônus "{NOME DO BÔNUS}": folhas A4 impressas e um tablet mostrando a
capa do bônus com esse título em {IDIOMA}. Mesmo estilo visual da capa principal,
porém em cor secundária. Fundo neutro, luz suave, 1:1.
```

**Rosto do depoente (avatar WhatsApp)**
```
Retrato de selfie casual de {PUBLICO: ex. mulher brasileira de 45 anos},
em casa, luz natural de janela, expressão natural, foto de celular, enquadramento
de rosto e ombros, 1:1. Nada de estúdio, nada de sorriso de banco de imagem.
```

**Foto que o cliente manda no chat**
```
Foto de celular tirada por uma pessoa comum em casa: {CENA: folhas impressas do
material sobre a mesa da cozinha / idosa fazendo o exercício na sala}.
Luz de ambiente, leve imperfeição, sem edição, 3:4.
```

**Pessoa segurando o material impresso**
```
Foto realista de {PUBLICO} segurando um material impresso encadernado cuja capa
mostra "{HEADLINE}" em {IDIOMA}, olhando para a câmera, dentro de casa,
luz natural. Foto de celular, sem cara de propaganda. 4:5.
```

## Completar entrega pós-MVP — um item por vez (dono 27/09/2026)
Regra completa em `criacao-low-ticket-mvt/references/CONSTRUCAO.md` passo 2(f). Resumo: inventário
(tem × promessa) → item sem nada ganha MVP primeiro → depois principal → completo → bônus → OBs.
UM item por vez, 1 pane por item (terminou → fecha → pane novo, contexto limpo). Texto completo
escrito em arquivo ANTES de gerar. Geração = `gpt-imagem-playwright` em WORK MODE, lote inteiro do
item num pedido, anexando a NOSSA referência (páginas aprovadas do mesmo tipo + capa), nunca a do
concorrente nesta fase.
**Prompt do lote:** usar o "Prompt-modelo OBRIGATÓRIO do lote de entregável" da skill
`gpt-imagem-playwright` (imagens INDIVIDUAIS pelo gerador de imagem, nunca código; teste de 2
páginas; gate contra referência devolvida). Orquestrador que delega cola esse modelo no brief do pane.

## Pipeline canônico de QUALQUER entrega (regra geral, não só esta oferta)

Ordem fixa pra montar o entregável (principal + bônus) todo em imagens:
1. **Referência visual primeiro** — ter a referência de cada tipo de peça (do concorrente ou gerada).
2. **Entender o que vai fazer** — ler a página de vendas toda, definir o que o produto É.
3. **Textos bem-feitos, organizados** — categorias/capítulos/páginas escritos: entrega principal +
   bônus, cada página com seu conteúdo. Sem texto organizado, GPT gera aleatório.
4. **Prompts de imagem corretos + referências** — casar tipo da peça com tipo da referência, pacote
   completo (referência + contexto + design system).
5. **Montar as imagens-âncora de CADA tipo primeiro** (capa, página-diagrama, página-exercício, capa
   de bônus) → validar → TRAVAR como design system.
6. **Gerar 10 em 10 num pedido só, no WORK MODE do ChatGPT** (não uma a uma). MODO COMPROVADO
   (21/09/2026, aprovado pelo dono depois de 3 tentativas falhas fora do work mode):
   - Ativar o **WORK MODE** (modo trabalho/agente) do ChatGPT ANTES de mandar o prompt. É ele que faz o
     GPT entregar as 10 separadas de verdade — fora do work mode saía 1 montagem só ou ia pro 1-por-vez.
   - **Prompt em INGLÊS, instrução PRIMEIRO**: 1a linha deixa explícito *"Generate 10 INDIVIDUAL images —
     one separate image per page, 10 distinct outputs. NOT a single combined image, NOT a montage/grid.
     Each page full-size with its text INSIDE the image, in Brazilian Portuguese."* SÓ DEPOIS lista
     "Image 1: … / Image 2: … / … / Image 10:" com o texto de cada página + as referências juntas.
   - Devolve as 10 separadas (1 página por imagem) — mais rápido que 1-por-vez.
   - **Ritmo de produção (MVT geral, decisão dono 21/09/2026): 10 de cada bloco importante** — 10 do
     principal, 10 do bônus 1, 10 do bônus 2, etc. Valida visual, depois completa o resto.
   ⚠ **Escopo: só pra ENTREGA low ticket (esta skill).** NÃO aplicar na mecânica geral `gpt-imagem-playwright`
   — lá pedir 10 de uma vez faz o GPT gerar tudo junto/errado. Lote único no work mode = exclusivo da
   entrega de páginas. Nunca montagem espremida numa imagem só (texto vira garatuja). GPT **para no limite de ~10** por lote: peça "continuar/gerar
   as próximas" pra retomar. Entrega 100% imagem = texto renderizado DENTRO da página pelo GPT, sem
   overlay depois; texto curto por bloco sai legível, parágrafo longo garatuja → condensar.
7. **Pouco a pouco:** gera um lote, VALIDA, próximo. Nunca despejar tudo sem validar.
8. **Fechar:** pedir ao GPT o PDF final na ORDEM certa → usar esse PDF como entregável.

## Fluxo (slots de página de vendas)

1. Ler a página (`pagina/index.html` ou o MODELO) e listar os slots vazios.
2. Montar a lista de prompts preenchidos — headline e nomes de bônus copiados
   LITERALMENTE da página, sem reescrever.
3. Rodar `gpt-imagem-playwright` em levas de até 10, salvando em
   `pagina/assets/` com nome do slot (`hero.png`, `bonus-01.png`, `dentro-03.png`).
4. Gate: abrir cada imagem, conferir regras 1-6. Reprovada -> regera só ela.
5. Trocar os `Espaço da imagem` do HTML pelos caminhos e conferir a página no browser.
