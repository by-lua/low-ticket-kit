# GUIA DE IMAGEM — tipos de estático e carrossel (índice único, revisado 26/10/2026)

**Quem manda em quê (dona, 26/10/2026):** o método do Rodrigo é a base (vale inteiro), somado aos
formatos que a dona já fixou; Kevones dá a quantidade; a biblioteca é opção extra. Eles dão os PAPÉIS
e a estrutura do texto (gancho → desenvolvimento → CTA); **o visual é sempre o nosso**: foto orgânica de
iPhone, texto de Stories, material impresso + digital (tablet, notebook, celular), **nunca mockup**.
Onde uma referência pede mockup (ex.: "clássica" do Rodrigo), a nossa versão é a orgânica com o
mesmo papel — com preço, se for peça de preço.

Toda peça de imagem da leva é UM tipo desta página. **O tipo decide o visual e o que aparece;
as regras da seção "Vale pra todo tipo" valem sempre** — igual o vídeo: modo muda, edição não.
Mecânica de geração: `gpt-imagem-playwright` (`scripts/gerar-imagem-gpt.sh` / `gen2.sh`).
Molde de prompt da cena orgânica: `PROMPT-ESTATICO-ORGANICO.md`. Formato da biblioteca:
`modelagem-escalados` (prompts 05–07, fidelidade à referência).

## Vale pra todo tipo (a "edição" da imagem)

1. **4:5, 1080×1350**, todos os cards iguais (9:16 só se a dona pedir).
2. **Texto escrito PELO GPT dentro da imagem**, nunca overlay de código com faixa/bloco. Prompt salvo em
   `intermediarios/prompt*.txt`. Na cena orgânica, o texto é pedido só como
   `Instagram Stories text sticker, as if typed by the person in the app, in <idioma>` — sem descrever cor/fonte/caixa.
   Nos tipos com visual próprio (impacto, clássica, biblioteca) o texto segue o visual do tipo.
3. **Toda peça tem gancho → desenvolvimento → CTA**, inclusive impacto, só-texto e carrossel de páginas.
   Conte os blocos no prompt antes de enviar: 2 blocos = falta o desenvolvimento (citando produto/mecanismo).
4. **Clareza em 1 segundo:** dá pra saber o que é, pra quem é e a entrega concreta? Curiosidade pode abrir, nunca esconder o produto.
5. **Produto é UMA coisa só (dona, 26/10/2026 — vale igual em vídeo).** Nunca fragmentar a copy ou a
   cena em "o Bono 1 faz isso, o Bono 2 faz aquilo, o Completo tem isso, o Básico tem aquilo" — isso
   é característica de PÁGINA (compara planos), não de criativo. O criativo mostra/fala do material
   como um todo ("una sola colección", "el material completo"); detalhe de bônus específico só
   aparece se a PÁGINA real que acompanha a peça mostrar esse bônus — nunca inventado pela copy.
   Mesma regra proíbe **grid/mosaico de capas separadas** como peça de prova (reprovado 26/10,
   NeuroActiva AR) — prova de volume mostra 1 objeto físico (livro/pasta) + 1 página real, nunca um
   grid recortando o produto em pedaços.
4b. **Conferir que o texto EXISTE na imagem** (contar caixas × prompt) e só então a ortografia palavra por palavra
   (acentos: declarar o idioma no prompt; nunca tirar acento).
5. **Páginas do produto = arquivo real** anexado (capa + 2–3 páginas). GPT nunca desenha página. Nada repete:
   cada aparelho e cada folha mostram página diferente. Nunca "PDF", nunca mockup 3D na peça (o mockup só existe no card CTA do vídeo).
6. **Margem de segurança SEMPRE (dona, 26/10/2026), em todo formato:** feed 4:5 → nada essencial
   (texto, rosto, material, preço, CTA) no topo ~14%, na base ~20% nem colado nas laterais (~5%); Stories/vídeo
   9:16 → idem (290 px topo, 360 px base, 60 px laterais). Sobra respiro em volta, nada cortado na borda.
   Pedir no prompt e conferir na imagem final.
7. **Preço:** só em peça de preço **estática**, sempre o **plano mais barato**. **Carrossel NUNCA tem preço** (dona, 27/10/2026), de nenhum tipo.
7b. **Nenhuma peça cita bônus, módulo/volume nem contagem** ("4 bonus", "Volumen 2", "400 fichas") — fala do produto e do que ele faz (`criativo-ads/references/texto-anuncio-por-angulo.md`, dona 27/10/2026).
8. Gates: `gate-pecas-criativo.py <CRIATIVO-N>` antes de gerar; `gate-imagens-finais.py <finais> --pasta <CRIATIVO-N>`
   depois; abrir 1 imagem de cada peça antes de dizer "pronta".

## Estático

| Tipo (slot) | Visual | O que aparece | Regra específica |
|---|---|---|---|
| **Orgânico iPhone** (padrão) | foto feia de celular, luz real, torta, grão | **digital + impresso**: 1–2 aparelhos + 3–4 folhas, cada um com página diferente, cenário da persona | `PROMPT-ESTATICO-ORGANICO.md` + REF-FORMATO anexada |
| **UGC estático** (slot 4) | orgânico iPhone com pessoa | pessoa comum **com o material**, apresentação variada peça a peça: segurando como livro (fechado com a capa ou aberto em 2 páginas), na estante, impresso na mão, tablet/celular com a capa — olhando pra câmera, como quem dá opinião | mão nua = reprovado; capa limpa primeiro, página real só se não houver capa |
| **Fase de impacto** (slot 7) | fundo **branco** (texto preto + vermelho) ou **preto** (branco + vermelho) | só texto | gancho + desenvolvimento citando o produto + CTA; varia branco/preto peça a peça |
| **Só texto** (slot 5) | nota/tweet/frase de impacto em visual nativo | só texto | sobe consciência; mesmo assim 3 blocos e cita o produto no desenvolvimento |
| **Benefício central** (slot 6, antes "original") | orgânico iPhone | **maior texto = o benefício/quantidade verdadeira** ("78 mapas, uma página por carta"), 1 linha de apoio (como recebe/usa), CTA; material impresso + digital | sem história, sem mockup; só número real do produto (Rodrigo, estudo `CONHECIMENTO/ESTUDOS/2026-10-26-delta-criativo-rodrigo.md`) |
| **Peça de preço** (slot 8 — a "clássica" do Rodrigo na nossa versão) | **orgânico iPhone** (padrão): digital + impresso + texto Stories com o valor — de preferência reaproveitando a cena já aprovada de outra peça e trocando só o texto | gancho + desenvolvimento + valor do plano mais barato + CTA | **sem mockup e sem fundo preto de catálogo**; alternativa: impacto com nome do produto + valor; nunca preço solto sem produto; única peça do conjunto com valor; é **pré-qualificação**: CTR menor com conversão maior é o esperado, não reprova |
| **Caixa de perguntas / expert respondendo** | story nativo + orgânico iPhone | caixa de pergunta (dor/objeção real) + **expert** respondendo com o material na mão (impresso/tablet) e texto Stories com a resposta | nunca UGC respondendo; resposta com mecanismo |
| **Antes/depois** | o da referência | puxado da Biblioteca de Anúncios (anúncio real rodando) | nunca inventado do zero |
| **Formato da biblioteca** (print WhatsApp, notícia, story nativo, tweet…) | **o da referência** (`modelagem-escalados`, fidelidade: layout, cor, fonte iguais) | nosso conteúdo real dentro | prova não se fabrica: sem depoimento real, sem formato de prova social |

## Carrossel (mínimo 5 cards; nunca 2 do mesmo tipo na mesma campanha; **nunca com preço**)

| Tipo | Card 1 | Meio | Último |
|---|---|---|---|
| **1 · Imagem principal + páginas** | arte gerada (orgânico iPhone com texto) | páginas reais full bleed, em sequência | página real ou card CTA |
| **2b · Só páginas puro** (padrão da vaga fixa do 1-1-5, dona 27/10/2026) | página real | páginas reais inteiras, uma por card | página real — **sem card gerado, sem preço**; a mensagem vai no texto do anúncio |
| **2 · Só páginas** | **card de gancho gerado** (texto Stories sobre cena orgânica, ou impacto) | páginas reais (são o desenvolvimento) | **card de CTA gerado** — nunca páginas soltas sem gancho nem fechamento |
| **3 · Henrique** | páginas em vários aparelhos (sem mockup) + a dor | idem, 1 por card | card CTA "mirá por dentro" |
| **Objeção** (slot 9) | a objeção | 1 objeção por card, respondida | CTA |
| **História / catálogo** (slot 10) | gancho | história em 5–10 cards ou acervo | CTA |
| **Demonstrativo iPhone** | capa estilo A (promessa + material + benefícios + garantia/vitalício) ou B (promessa + material + CTA) | ~4 páginas reais | — (`modelagem-escalados/references/carrossel-demonstrativo-iphone.md`) |

Página real no card: largura inteira na resolução nativa; página em paisagem → sobra preenchida com o
papel da própria página (`criativos/scripts/montar-cards.py` do Tarot AR é a referência); A4 em retrato →
recorte do topo até 4:5. Sem moldura, sem tarja branca, sem crop pequeno ampliado.
