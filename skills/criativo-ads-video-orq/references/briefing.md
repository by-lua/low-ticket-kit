# Briefing do vídeo e a quem a narração fala (movido do SKILL.md em 26/10/2026)

> Ler antes de escrever roteiro/narração. Os "Modos A/D/E" abaixo são a nomenclatura antiga; os modos atuais estão em `estilos-de-video.md`.


## FASE 0 — Briefing

**Antes de decidir modo, cena ou fala: entenda o produto e quem compra.** Nunca
escreva a primeira linha de prompt de imagem, vídeo ou narração sem antes ler:

1. **A página de vendas** (`pagina/index.html` da oferta) — ela já carrega
   promessa, ângulo e **para quem fala** (comprador, não necessariamente usuário
   final), validados com o usuário antes de ir ao ar. É a fonte da verdade do
   projeto, não um detalhe a inferir depois.
2. **O entregável** (PDFs/imagens já gerados) — o que o comprador de fato recebe,
   pra demonstração usar conteúdo real (ver §E.0 mais abaixo).

Pular esse passo já custou caro: um criativo saiu com a narração falando
diretamente com o idoso ("vas a recibir", "tu equilibrio") num produto cujo
comprador real é o filho/cuidador — a própria página já usava
hijo/hija/papá/mamá, e ninguém checou antes de escrever. Ver §E.4 para a regra
completa de "a quem a narração se dirige".

**Se você é o orquestrador delegando essa skill pra um pane/subagente, o
prompt de spawn É o briefing.** Aconteceu de novo (2026-09-07): um pane
recebeu só caminho de arquivos de referência + "monte 1 criativo demonstrativo"
e produziu vídeo/imagem tecnicamente corretos mas sem ângulo de venda nenhum
— nunca soube produto, persona ou proposta, porque isso nunca chegou no
prompt de spawn. Passar arquivos não é briefing. Todo spawn pra essa skill
precisa incluir explicitamente: nome do produto, promessa/proposta real,
persona (pra quem fala), preço real, e a instrução de invocar esta skill
desde a FASE 0 — nunca pular direto pra "gere a cena X".

Só depois disso, decida o modo. Se não estiver claro no pedido, **pergunte**:

**Modo A — Criativo completo do zero.** Todas as cenas são geradas: hook, corpo,
oferta e CTA. **É o modo padrão desde 25/10/2026** (B/B2/C removidos — ver nota
abaixo). Toda dor/ângulo novo vira peça nova do zero, nunca reaproveitando body
de vencedor com variação de superfície.

> **⛔ Modo B, B2 e C REMOVIDOS (regra da dona, 25/10/2026).** Os três dependiam
> de reaproveitar o body de um vencedor trocando só o hook/gancho (matriz
> gatilho×ângulo do Kevones, ou "v2" com body variado). Confirmado em
> `criativo-ads/references/kevones-criativo.md` linhas 11-38: **o próprio Kevones
> abandonou essa lógica depois da Andrômeda** (out/2025) — o Meta passou a agrupar
> por IDEIA/CONTEXTO, não por superfície, então trocar gancho/voz/cor/matriz de
> abertura sobre o mesmo body é a variação rasa que ele hoje condena. O que ele
> ensina agora é **"um anúncio por dor/benefício"**: lista as dores do produto,
> 1 peça nova (gerada do zero, Modo A) por dor — é exatamente o que GATE 0.2 /
> MATRIZ ÚNICA de `criativo-ads` já fazem. A única variação de vencedor que ele
> ainda autoriza é o **"copo azul"** (mesmo produto+copy, troca quem/onde —
> `copo-azul-variacao-vencedor`), que é uma peça nova mesmo assim, não corte de
> hook sobre body velho.
>
> Se encontrar `HOOK/`, `CRIATIVO-N` com body reaproveitado, ou qualquer menção a
> "Modo B/C" em oferta antiga: é legado, não reproduzir o padrão numa leva nova.

**Modo D — Modelagem de escalados.** A leva não nasce de briefing nem de vencedor
próprio: nasce de um **formato que já está escalando na conta de outra pessoa**, com o
arquivo real anexado como referência. Existe uma biblioteca local de 103 formatos
(87 estáticos, 16 vídeos, 47 categorias) em `~/.claude/biblioteca-escalados`.

Quem conduz esse modo é a skill **`modelagem-escalados`** — leia-a antes de qualquer
coisa. A divisão é:

| | `modelagem-escalados` | esta skill |
|---|---|---|
| Estático | pipeline inteiro (01→12) | não entra |
| Vídeo | decupa o formato e devolve o briefing (prompt `11`) | produz: imagem → vídeo → QA → montagem |

Fluxo de vídeo no Modo D:

1. `scripts/buscar.sh --tipo video` na skill `modelagem-escalados` lista os 16 formatos;
   13 têm transcrição `.txt` ao lado do arquivo.
2. Prompt `11` decupa o vídeo escalado em blocos (hook / agitação / mecanismo / prova /
   oferta / CTA), acha o corte de atenção e nomeia o mecanismo do hook.
3. O briefing que sai dali entra aqui como **Modo A**, já com persona, ângulo e
   falas por cena. Todas as regras desta skill continuam valendo — 16 palavras por cena
   no Veo, rosto em quadro, bloco de dentes, anti-morphing.

Regra que não muda no Modo D: **modela-se o mecanismo, não o produto.** Pessoa, marca,
logo, prova e número da referência não sobrevivem à adaptação. Sem depoimento real no
briefing, formato de prova social não entra.

**Modo E — Vitrine Guiada (b-roll de banco + demonstração do entregável + guia
falante, MISTURADOS no mesmo criativo).** Nenhuma cena de mundo real é gerada por
IA. O criativo é montado com quatro fontes que já existem ou já foram geradas
antes (imagem do entregável, ver FASE 0/§E.0), e a única coisa que pode ser gerada
agora é a pessoa que fala (ou nem ela, quando é só narração).

⚠️ **PADRÃO VALIDADO (Receita Aprovada Tarot, 2026-09-23):** O modo demonstrativo
segue o padrão **b-roll + gravação de tela/entregável + VO + legenda karaokê,
SEM tarja vermelha, SEM geração de pessoa por IA**. Ver seção **`criativo-ads-video-orq/references/EDICAO-PADRAO.md`** para receita
completa e detalhes de estrutura, layout, regras que funcionaram.

| Camada | Fonte | Para que serve |
|---|---|---|
| **B-roll** | banco público (Pexels, Pixabay, Coverr, Mixkit) e Pinterest | contexto e dor: cenas do mundo do comprador que o acervo próprio não tem |
| **Demonstração do entregável** | gravação de tela ou mão apontando página real (§E.2 ou §E.0) — o material físico/mockup do produto | prova principal em produto PDF/guia: mostra exatamente o que o comprador recebe |
| **Tela** | gravação do próprio produto em modo mobile no DevTools (§E.2) | prova em produto navegável (portal, app, área de membros) — alternativa à demonstração acima, não soma com ela no mesmo criativo salvo casos específicos |
| **Guia** | personagem falante (imagem→vídeo, pipeline normal desta skill, ou UGC de leva anterior — nunca com áudio trocado, ver §E.6) ou só narração off | conduz, promete e chama pra ação; editado com as outras camadas via Meio a meio ou PiP (§E.3) |

**As quatro camadas não são modos separados — são um kit.** Um único criativo pode
abrir com b-roll (dor), passar pra demonstração do entregável (prova via gravação
de tela ou visual), voltar pro b-roll (contexto), e fechar com o guia falando em
PiP ou VO sobre a demonstração (CTA). A composição cena a cena decide qual camada
entra onde — não existe regra de "este criativo é só b-roll" ou "este é só
demonstração"; cada cena usa a fonte que prova melhor aquela frase do roteiro.

Use quando: o produto é **digital e navegável** (site, área de membros, catálogo,
app) — a tela real vende mais que qualquer cena inventada; ou quando o b-roll do
nicho existe pronto em banco e gerar aquilo por IA seria pagar caro por pior; ou
quando o produto é um PDF/guia e a prova mais forte é ele mesmo, físico, na mão.

**Inspiração de estrutura vem da biblioteca de escalados também — sempre olhe
antes de inventar o corte.** `~/.claude/skills/modelagem-escalados/scripts/buscar.sh
--tipo video` lista os 16 formatos de vídeo já escalados, por categoria:

| Categoria | Qtd | Corresponde a |
|---|---|---|
| UGC (verde, tela dividida, expert reagindo) | 7 | Meio a meio / Miniatura-PiP |
| Tela dividida | 2 | Meio a meio |
| Antes e depois (com tela dividida) | 2 | Meio a meio |
| Tela verde | 1 | Miniatura-PiP (fundo composto) |
| POV em Vídeo | 1 | Print + POV + Meme, sem meme físico — só POV+prova |
| Identificação | 1 | Tela cheia |
| Animação 3D | 1 | fora do escopo do Modo E |
| Estilo stories | 1 | Tela cheia, ritmo de story nativo |

Não é o Modo D (que decupa um vencedor específico e vira briefing formal): aqui
é consulta rápida de referência validada, e entra em **dois momentos, não só
um**:

1. **Antes de pensar em como vai ser o criativo** — primeiro passo, antes de
   decidir estrutura, persona ou ângulo. Busca referência validada primeiro,
   inventa depois em cima do que já funciona; nunca o inverso.
2. **Antes de montar** (FASE 7, já com os clipes/imagens prontos) — confere se
   o layout escolhido pra edição (Meio a meio, PiP, Tela cheia, Print+POV+Meme)
   ainda bate com o formato de referência, porque decisão de montagem muda
   depois de ver o material pronto: às vezes o corte planejado não sobra tempo
   pro layout que virou referência, e é melhor trocar de layout do que forçar.

Rode a busca **de qualquer ponto do processo**, sempre que o corte ou a
montagem do criativo estiver em dúvida — nenhum arquivo da biblioteca entra na
peça final, é referência de estrutura, não material.

**Cuidado ao ler a referência: o que é edição não vira prompt de vídeo.** O
formato escalado mostra o resultado **já montado** (split, PiP, faixa, corte).
Isso é decisão de pós-produção — mesma regra do começo desta seção (## Regra de
voz/rosto, "Modos de edição"). Ao escrever o roteiro a partir de uma referência,
separe sempre os dois: o que o **guia fala e faz** (vira prompt de vídeo,
gerado em quadro cheio, normal) e o **layout que a referência usa** (vira nota
de edição, aplicado depois no clipe pronto). Copiar a montagem da referência
pro prompt do Veo ("cena dividida ao meio", "tela no canto") é o erro que gera
clipe quebrado — o modelo tenta desenhar a divisão dentro da própria imagem.


### E.4 — Narração e trilha

**A quem a narração se dirige sai de QUEM COMPRA, não de quem USA o produto.**
Caso real (equilibrio-seguro-60): a narração falava na segunda pessoa como se o
próprio idoso estivesse comprando ("vas a recibir", "tu equilibrio") — mas em
nicho de idosos/terceira idade, saúde do idoso, cuidados especiais, quem decide
e paga quase sempre é o filho/filha ou cuidador, não o idoso. Falar como se o
idoso fosse o comprador erra o alvo da dor: o gatilho de quem cuida é
preocupação/culpa/responsabilidade pelo bem-estar de outra pessoa, não
autocuidado.

Antes de escrever a narração de qualquer criativo, pergunte **quem decide a
compra**, não só quem usa o produto:

| Nicho | Quem usa | Quem decide/paga | Narração fala com |
|---|---|---|---|
| Guias/produtos pra idosos | o idoso | filho(a), cuidador(a) | o cuidador — "para tu papá/mamá", nunca "para ti" no idoso |
| Material infantil/escolar | a criança | pai/mãe | o responsável |
| Produto pet | o pet | o dono | o dono |
| Produto B2B de uso técnico | o operador | quem compra na empresa | quem decide a compra, se for diferente de quem usa |

Regra prática: se usuário final e comprador são pessoas diferentes, a narração
(e a matriz persona×ângulo×oferta da FASE 1) é escrita **para o comprador**,
descrevendo o benefício pela ótica dele ("dá tranquilidade pra você saber que
ele está seguro"), não pela ótica de quem usa.

**Gênero da voz sai do nicho, não do gosto.** Nicho tocado majoritariamente por
homens (serralheria, mecânica, pesca, obra) → voz masculina. Nicho majoritariamente
feminino (cozinha, artesanato, maternidade, beleza) → voz feminina. Voz fora do
nicho lê como anúncio de fora, não como alguém de dentro. Na dúvida, teste as duas
como variação — teste as duas em peças diferentes da leva.

A narração é gerada pela skill **`narracao-hub-tts`** (API do NinjaVoice, sem
browser, 82 vozes, pt-BR nativo, WAV síncrono). Invoque-a, não reescreva a
mecânica aqui. Escolhida a voz do projeto, ela não muda entre cenas.

