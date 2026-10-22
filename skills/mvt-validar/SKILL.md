---
name: mvt-validar
description: MECÂNICA chamada pela skill `criacao-low-ticket-mvt` (passo 4 · T9 VALIDAR; também a medição de demanda da T8 no cross-market). Valida a comunicação modelada com as 3 fontes (Biblioteca, YouTube+comentário recente, Trends) + TikTok orgânico e Uber Suggest: janelas, sinal de compra, obreiro×fiel, B2B técnico, demanda≠anúncio, território medido em todas, controle e falso-positivo, mecânica de medição na Biblioteca/Trends/YouTube. Use quando a orquestradora chegar em T9, quando o usuário pedir "validar", "medir demanda", "ver se tem vaga", ou ao retomar a validação.
---

# mvt-validar — passo 4 (T9 VALIDAR)

> **Nomes de seção no texto abaixo** (`GATES TRAVADOS`, `ADENDO §x`, `passo N`, `FASE DE CONSTRUÇÃO`, `ROTEADOR`, `PASSO 0a/0b`, `PROMPT-PADRÃO`) são os da skill original, já dividida: cada um agora mora onde o `## ÍNDICE` da skill `criacao-low-ticket-mvt` aponta. O texto das regras não foi alterado.

> **IDs dos subpassos** = os de `criacao-low-ticket-mvt/references/TRILHA-CHECKLIST.yaml`; evidência com nome de arquivo padronizado, conferida por `scripts/gate.py --passo T9`. Saída ≠ 0 = passo aberto.

## ENTRADA EXIGIDA (conferir ANTES de começar — GATE DE PASSAGEM da orquestradora)
- T7 fechado (GATE 3 em `mvt-modelar`; mesmo mercado A/E/F/D-BR) **ou** T8 fechado (cross, `mvt-cross-market` etapa 2).
- Perfis/panes: mecânica da Biblioteca e regras de pane estão em `mvt-minerar` (seção `Mecânica — Biblioteca de Anúncios`) e no prompt-padrão:
Entrada ausente = passo anterior ABERTO: volte a ele pela TRILHA do modo em `criacao-low-ticket-mvt`. 
Sem `ESTADO.md` com o bloco `## ROTEADOR` gravado, esta skill não roda (chame primeiro `criacao-low-ticket-mvt`).

`~/.claude/skills/criacao-low-ticket-mvt/references/PROMPT-PADRAO-PANE.md` (blocos obrigatórios de todo `pane_spawn` que toca browser, minera ou mede — copiados no prompt, nunca "veja a skill").

## Regras de medição de território/ranking (o campo do ranking medido em TODAS)

**ANTES DE RANKEAR, o campo do ranking precisa estar medido em TODAS as candidatas.**
Erro real 18/09/2026: ordenei por `territorio_anuncios` com 125 de 236 concepções sem território
medido. `None` virou zero na ordenação, então metade da base perdeu sem ter competido — e um
nicho inteiro ("profissional diverso", 20 concepções, zero medidas) não apareceu na cota. Ficaram
de fora os dois maiores territórios da rodada: `orçamento de serralheria` (2.200) e
`homologação energia solar` (2.100).

Regra: `None` significa **não medido**, nunca zero. Antes de qualquer corte, rode o contador:

```fish
python3 -c "
import json,collections
c=json.load(open('ofertas.json'))['concepcoes']
v=[x for x in c if x.get('validacao') not in ('DUPLICATA','DESCARTADA')]
g=collections.defaultdict(lambda:[0,0])
for x in v: g[(x.get('nicho') or '?').split('(')[0].strip()][0 if x.get('territorio_anuncios') is not None else 1]+=1
for k,(m,s) in sorted(g.items(), key=lambda kv:-kv[1][1]): print('%-40s medido %3d  sem %3d'%(k[:40],m,s))
"
```

Nicho com coluna "sem" alta não está fraco — está **cego**. Meça o território de todas antes de
ordenar (1 busca por concepção, barato), ou declare explicitamente que o ranking cobre só a parte
medida e que o resto segue elegível.

**`[T9.2]` TERRITÓRIO COM TERMO DE SERVIÇO ("orçamento de X", "serviço de X", "conserto de X") = POSSIVELMENTE INFLADO por anúncio de serviço local.** Erro real R7 #7: `orçamento de serralheria` (2.200) e `orçamento de instalação elétrica` foram lidos como mercado de FERRAMENTA/produto digital, mas a maior parte dos anúncios é o próprio prestador captando cliente ("peça seu orçamento") — demanda de serviço, não concorrente nem comprador do nosso produto. Regra: (1) todo território cujo termo tem forma de serviço vai marcado no `validacao-<lote>.md` e na PARADA-2 como **"possivelmente inflado por serviço local"**; (2) antes de usar o número (VAGA/OCUPADO), abra ≥10 cards e classifique quantos são prestador de serviço × produto digital/ferramenta; escreva a fração e o número LIMPO ao lado do bruto; (3) sem essa leitura, o território fica "bruto, não limpo" — não entra como ranking. O `gate.py` (T9.2) acusa território de serviço sem a marca `inflado`/`serviço local`.

**O TERMO DO TERRITÓRIO MUDA O TAMANHO DO MERCADO — teste mais de um.** Erro real 18/09/2026:
`curso extensão de cílios` mediu 1.600 e entrou nas finalistas; `extensão de cílios` mediu
**12.000**. Mesmo mercado, termo diferente, 7x de diferença. Ao definir território, escreva o
NÚCLEO do mercado, sem qualificador que estreite (`curso`, `planilha`, `kit`, `pack`). Na dúvida
entre dois termos, meça os dois — é 1 busca a mais e evita subdimensionar o mercado inteiro.

**Território grande NÃO significa vaga.** Na R3, `redação enem` (2.600), `diagnóstico ar
condicionado` (1.600), `planilha controle financeiro` (1.500) e `planilha de treino` (1.500)
ficaram com ZERO comunicações livres — mercado cheio e todas as portas ocupadas. Tamanho é
pré-requisito, nunca critério isolado: o que decide é território vivo **E** comunicação zerada.

---

## 4 · VALIDAR a comunicação modelada

**Nomes de arquivo PADRÃO (evidência do gate):** território/específica/controle → `validacao-<lote>.md` (+ `.jsonl`); YouTube · TikTok · Trends · `sinal_de_compra` · urgência por finalista → `demanda-<lote>.md` (uma seção `### F.. — nome` por finalista, cada uma com as 5 fontes/campos ou "não medido"); Parada → `PARADA-2.md`. **Cada concepção que chega à Obra — inclusive a que apareceu no meio do caminho (pivô) — tem a SUA seção em `demanda-*.md` com as 3 fontes + sinal + urgência (T9.4 · T9.5 · T9.8).** Medida de outra concepção "parecida" não vale.

Método: §9 "Validar a direção escolhida". Sobre as finalistas **modeladas** (não sobre a
concepção original):

**São TRÊS fontes, não uma.** O quadro do método liga "Verificar se a sua nova concepção tem
demanda, as pessoas querem…" a três filhos: *ofertas sobre a nova concepção na biblioteca* ·
*youtube + comentários (tá tendo comentário recente?)* · *google trends*
[MATERIAL-FRAMEWORK, região à direita de MODELAR]. Rodar só a Biblioteca é meia validação —
erro real 2026-09-18: as 243 da rodada 3 foram medidas só na Biblioteca.

1. **Biblioteca** — a nova comunicação já existe? Populado → troca de direção, não insiste.
   Mede OCUPAÇÃO (o caminho está livre?), não demanda.
2. **YouTube + comentários recentes** — mede DEMANDA, e é a fonte que ele usa no estudo de
   caso 1 com número ("40 mil visualizações", "135 mil", "salmos era disparado o mais
   buscado"). Comentário recente = gente interessada agora.
3. **Google Trends** — curva de interesse.

Senso crítico também é fonte declarada [aula 01:12]: *"se eu analisar um grupo de mil pessoas,
eu encontro esse tipo de pessoa querendo comprar isso?"* E o **teste de urgência**: a dor é *pneu furado* (quer resolver já) ou *para-brisa ruim* (precisa, mas deixa pra depois)? [YT e7MDJ2OgMNE]

**Nossas fontes de demanda vão além das dele** (decisão do usuário, 18/09/2026). Ele usou
YouTube e Trends porque era o que tinha; a gente tem mais, e demanda é justamente onde a
Biblioteca é cega:

| Fonte | O que mede | Sinal que interessa |
|---|---|---|
| **YouTube** | interesse consolidado | **quantos** vídeos vão bem (não um só) + **comentário recente ordenado por data** |
| **Google Trends** | curva no tempo | subindo, estável ou morrendo; sazonalidade |
| **Uber Suggest / volume Google** (3 buscas grátis/dia: nunca preencher sem medir; sem vaga no dia = "não medido") | volume mensal de busca | "alta busca mensal = com certeza tem demanda" [YT e7MDJ2OgMNE]; 3 buscas grátis/dia — use nas finalistas |
| **TikTok (conteúdo orgânico)** | interesse jovem e emergente | volume de vídeo no termo, views, data dos posts, **comentários pedindo/perguntando** |

**Como ler cada fonte sem se enganar** (janelas e critérios definidos por nós — o método não dá
número; o framework dele pede só "youtube + comentários: tá tendo comentário recente?", e no caso
Salmos ele olha views):

1. **Conte quantos vídeos vão bem, não olhe o topo.** Um vídeo com 2M views pode ser o algoritmo
   tendo empurrado aquilo para fora do nicho — audiência que nunca compraria. Demanda é
   **vários vídeos, de canais diferentes, indo bem**. Registre a distribuição (ex.: "8 vídeos
   acima de 50K, de 6 canais"), não só o maior. Um pico isolado com o resto no chão = outlier,
   leia como sinal médio, não forte.
2. **Comentário: ORDENE POR MAIS RECENTES.** O padrão do YouTube é "Principais", que traz
   comentário fixado e curtido de anos atrás — ler o padrão é ler o passado. Troque a ordenação
   e veja se tem gente falando nos últimos ~6 meses, separando "≤3m" (sinal QUENTE) de "3-6m" (ainda válido; janela era 12m — dona 10/10/2026).
3. **Data do vídeo não decide; interação recente decide.** Vídeo de 1 ano com comentário desta
   semana vale mais que vídeo de 2 meses sem comentário nenhum. Exemplo real da rodada 3: R3-122
   (vida espiritual) tem vídeo de 1 ano com 2,3M views e **comentário há 3 dias** — vivo.
   R3-199 (ansiedade) tem 211K likes mas conteúdo de 2024, e os posts de 2026 têm 10 likes —
   momentum morto, foi rebaixado.

**GATE DE DEMANDA — 3 SINAIS JUNTOS (dono, 10/10/2026).** Dor validada = **vídeo viral + comentário recente + volume de vídeos**. Falta um, não valida:

1. **Vídeo viral**, no threshold da plataforma (o do YouTube é a régua-mãe: "100k mais ou menos"):
   YouTube/Shorts **≥100.000 views** · TikTok **≥1.000.000** (≥500k em canal de nicho) ·
   Instagram Reels **≥100.000** · Facebook **≥500.000**. **A DATA DO VÍDEO NÃO CORTA** — vídeo de
   2021 com 300k views prova que a dor é real; não descarte por ser antigo. Vídeo novo com 900
   views não vale nada.
2. **Comentário recente — de até ~6 meses.** Ordenado por mais recentes. ≤3m = QUENTE (peso maior);
   3-6m = ainda válido, a dor segue real. Comentário tipo "mano", "tô com 4 anos de faixa", "tô
   travado nisso há anos", postado há 6 meses = evidência forte. **Acima de ~1 ano sem nenhum
   comentário novo = dor podre.** (Janela era 12m até 25/09/2026; **10/10/2026 a dona baixou pra
   ~6m**.)
3. **Volume de vídeos** — **muitos vídeos** falando da dor é sinal de **oferta boa** (concorrência
   prova demanda), não de mercado morto. **Um** vídeo viral isolado = outlier, não evidência.

**100k é a régua do YouTube GERAL — NÃO corte o público pelo número (dono, 10/10/2026).**
*"Você também tem que considerar a audiência. Qual é o vídeo MAIS VISTADO daquele artista? Quantas
views ele tem? Você não precisa se limitar ao número."* 100k vale para mercado grande; **nicho com
audiência menor valida com menos**, desde que:

1. **Meça a escala real do público ANTES de reprovar** — nº de inscritos do canal, views típicas dos
   vídeos do MESMO criador. 50k num canal de 60k inscritos é sinal forte; 50k num canal de 3 milhões
   é ruído. Reprovar sem esse contexto é erro.
2. **Julgue pela posição relativa, não pelo número absoluto** — o vídeo está entre os mais vistos do
   próprio criador? É o tema que ele mais repete? É onde ele investiu? Isso vale mais que o número.
3. **Nunca reprove uma dor por ser de nicho.** Subscriber que dói compra melhor que lead de mercado
   grande. Dor rejeitada só com **número medido + contexto medido** — nunca com o número solto.
4. **A régua é por plataforma E por tamanho de mercado.** YouTube 100k é a referência geral; adapts
   pela escala medida do canal/público.

**Janelas que usamos:** comentário recente = **até ~6 meses** (era 12m; dona 10/10/2026), contado em
DUAS faixas nos relatórios: **≤3m = sinal QUENTE (peso maior)** e **3-6m = sinal morno**; nunca somar as
faixas num número só · views = **sem janela**
(é estoque de interesse, não vence) · vídeo novo em 6 meses = sinal de apoio, não requisito ·
Trends = 12 meses para direção, 5 anos quando a dúvida for "está morrendo?" · TikTok = **idade
do post NÃO corta** (até 6-12 meses conta): o gate é a mesma régua do YouTube — comentário
recente (dias/semanas) + intenção de compra + engajamento, não a data do vídeo. Vídeo de 1 ano
com comentários desta semana em volume pedindo ("quero isso", "onde compro") é demanda viva agora
(caso real: exercícios para idoso — post antigo, comentários recentes querendo → produto). Só
descarta quando, além de velho, os comentários também estão parados (momentum morto, R3-199).

**Cuidado com o produto de impulso.** FRACA no YouTube/Trends + FORTE no TikTok significa produto
**descoberto no feed, não procurado na busca** — vende, mas o criativo carrega tudo. Caso real:
R3-240 (planner de revenda) deu FRACA nas buscas e FORTE no TikTok (44,8K likes, post de 22h).
Medindo só por busca, a gente teria descartado uma categoria inteira.

**Audiência não é mercado — procure SINAL DE COMPRA.** Em nicho com muito conteúdo gratuito,
view alta engana. Além das 3 fontes, registre `sinal_de_compra`: comentário pedindo o material
("onde compro", "manda o link", "vende?"), pergunta de preço, criador com PDF/link na bio,
gente vendendo nos comentários. Caso real 18/09/2026: `campanha de salmos` tinha **235K no TikTok
e nenhum sinal de compra**; medindo só por view teria entrado na lista.

**Padrão do nicho cristão (e provavelmente de qualquer nicho de fé ou hobby com cultura de
compartilhar):** quem paga é o **obreiro**, não o fiel. Das 13 concepções cristãs medidas, só 3
tinham sinal de compra — e as três vendem para quem TRABALHA na igreja: pastor (guia de condução
de casamento e funeral, 323K no YouTube com comentários de pastores se preparando), pianista
(songbook para o culto) e professor de escola dominical. Todas as de conteúdo devocional para o
fiel deram FRACA: "audiência massiva no bíblico, mas consumo 100% gratuito". O obreiro tem
obrigação com DATA MARCADA e compra ferramenta de trabalho; o fiel acha o mesmo conteúdo de graça
em qualquer canal. Aplique a mesma pergunta em outros nichos: existe alguém que PRECISA entregar
isso para outra pessoa, com prazo?

**Cuidado com o B2B técnico.** FRACA nas três fontes pode significar "não tem rastro orgânico",
não "não tem demanda": engenheiro de SST não procura PGR no TikTok, compra porque precisa
entregar. Nesses casos o sinal válido é anunciante ativo na Biblioteca pagando tráfego (R3-109
tem 110) e busca no Google — nunca vídeo.

**Demanda é conteúdo ORGÂNICO, nunca anúncio.** Erro real 18/09/2026: eu tinha posto o TikTok
Creative Center como fonte de demanda — ele mostra o que está sendo ANUNCIADO, ou seja, é
ocupação, irmão da Biblioteca da Meta. Se entrar na conta de demanda, a gente conta concorrente
como se fosse comprador e inverte o sinal: mercado cheio de anúncio pareceria "demanda forte"
quando é justamente o que o método manda evitar.

Na dúvida sobre uma fonte, pergunte: **isso mostra gente querendo comprar, ou gente vendendo?**
Querendo comprar = demanda (vídeo orgânico, busca, comentário, view). Vendendo = ocupação
(Biblioteca da Meta, Creative Center, anúncio patrocinado no feed).

**No TikTok, só conteúdo orgânico. O Creative Center fica fora do fluxo** (decisão do usuário,
18/09/2026) — não entra na demanda nem na ocupação. Ocupação se mede na Biblioteca da Meta, que
é onde a gente vai anunciar; o que o TikTok tem de anúncio não diz nada sobre a nossa vaga lá.

### Atualização Borba — validação aberta via TikTok/IG, sem custo [decisão do dono 28/09/2026]

Fonte: validar-oferta-slides.vercel.app (ADS Borba). Método dele é mais SOLTO que o nosso — não
exige as 3 fontes fechadas por finalista, só demanda orgânica em TikTok/Instagram com sinal de
compra explícito. Adotado como **via de entrada mais rápida, em paralelo às 3 fontes**, não
substituto:

1. **Gerar ~30 termos de busca com Claude/GPT** cobrindo dor do público, termo de formato ("pdf",
   "planilha", "template") e gíria/jargão da comunidade — não só o nome técnico do produto. Rodar
   isso ANTES de ir pro YouTube/Trends/Biblioteca, é mais barato que pensar termo por termo.
2. **Buscar os termos no TikTok e Instagram**, achar vídeo com engajamento acima da média (views,
   like proporcional, comentário, salvamento).
3. Ler comentário atrás de intenção de compra explícita ("onde compro", "manda o link", "vende
   isso pronto?") — igual ao `sinal_de_compra` que já usamos, mesmo critério.
4. Formato do entregável se lê no que já viralizou (visual/infográfico, app, PDF, planilha,
   template) — informa a modelagem, não só a validação.

**Onde isso AFROUXA nosso critério:** TikTok/IG com sinal de compra explícito, sozinho, já é
sinal suficiente pra avançar a finalista pra Biblioteca (T9.13) — não precisa esperar YouTube +
Trends também baterem antes de gastar a busca na Biblioteca. Continua valendo tudo que já temos
(janela ~6m, ≤3m quente, produto de impulso, obreiro×fiel, B2B técnico não usa vídeo): isso
só adianta a decisão quando o TikTok/IG já respondeu sozinho, e os 30 termos por IA substituem a
etapa manual de pensar termo de busca (usa também no T9.13, técnica dos ~10 termos de
concorrência — mesma lógica, lote maior aqui porque é busca livre, não Biblioteca).

Vantagem de ordem: **demanda antes de ocupação**. É o que ele fez no caso Salmos — viu no
YouTube que salmos era "disparado o mais buscado", e só então foi para onde ninguém anunciava.
E é operacionalmente mais barato: nenhuma dessas fontes tem o throttle da Biblioteca da Meta,
então dá para rodar nas 50 e reservar as buscas da Biblioteca (recurso escasso) só para as ~10
finalistas. Na rodada 3 isso baixou o gasto na Biblioteca de 282 buscas para ~40.

Divirja do método aqui de propósito e de forma declarada: o método valida demanda DEPOIS de
medir ocupação; a gente inverte porque a Biblioteca é o recurso que bloqueia. O resultado é o
mesmo funil, gastando o escasso por último.

**Ordem dele:** modelar → comando de decisão → escolher 1-3 → **só então** olhar a Biblioteca [01:55:55] "a última coisa que eu faria aqui era" (1 busca [01:56:05] "sinesiologia para fisioterapeuta ó não tem nada aqui"). Nossa variante mede antes de decidir e **tem custo**: na R3 foram 662 comunicações medidas e 134 de 197 arquivos de medição/fila, com o passo 5 ainda aberto. Limite: medir na Biblioteca só as ≤10 finalistas — o corte vem do comando de decisão, não da medição — + teste de urgência. Não existe certeza [05:02:58] "não tem como a gente ter a certeza do que vai vender mais": a validação confirma encaixe e ausência de saturação; venda se descobre no teste de 3-7 dias [03:59:55] "isso vai durar uma média de 3 a 7 dias".

**A leitura dele na Biblioteca é qualitativa, não numérica** — "não tem nada aqui",
"pouquíssima coisa", "já está populado", "muita gente vendendo" [01:56, 05:03, 01:13]. Ele
nunca dá número de corte, e nunca instrui filtro de status. O `active_status=active` é
**decisão nossa de engenharia**, não regra do método: mantenha, mas não atribua a ele.
Veredito = leitura qualitativa com EVIDÊNCIA colada (ver `### Leitura qualitativa com evidência`).

Não mediu → escreva "não medido". Não invente número.

### Leitura qualitativa com evidência — demanda, ocupação, veredito  [T9.10 · T9.12 · decisão do dono 25/09/2026 (revisão): jeito do Heitor]
**Regra ÚNICA (vale para `mvt-minerar` modo F, `mvt-cross-market` e Obra).** Não há limiar numérico de corte. FORTE/MÉDIA/FRACA e DESERTO/VAGA/DISPUTADA/OCUPADO são **leitura qualitativa** do que o Heitor lê ("tá populado", "não tem nada aqui", "tem gente pedindo") e o relatório **COLA A EVIDÊNCIA** que sustenta a leitura: views (a distribuição, não só o topo), nº e link de cada comentário pedindo/perguntando preço, quem vende (páginas/anunciantes vistos), print da Biblioteca. **Número é evidência registrada, NUNCA corte automático** — nenhum número sozinho aprova ou descarta. Leitura sem evidência colada não vale. O que não foi medido fica "não medido".

- **Biblioteca (território × específica):** descreva o que se vê — vazio, poucos, populado, muita gente vendendo o mesmo — com o print e os anunciantes. Território vazio e específica vazia = ninguém anuncia ESSE termo (não prova ausência de concorrente: T9.13): desconfie de nicho sem comprador. Território com gente e específica vazia = vaga. Específica populada = ocupado/disputado: troca de direção (MVT: subnicho/ângulo/formato; no cross, não descarta). Modo F: na versão visual com controle bom, ver algo igual já rodando = ocupado.
- **YouTube:** vários vídeos de canais diferentes indo bem + comentário recente (≤3m quente, 3-6m morno) pedindo/perguntando = forte; um pico isolado com o resto no chão = outlier. **Trends:** direção subindo/estável/caindo. **TikTok:** vídeos com tração e comentário pedindo/perguntando preço.
- **`sinal_de_compra`** = cada comentário pedindo/perguntando preço COM link/print; registre quantos e quais — o dono/Heitor lê a força, a IA não fecha por contagem.
**Fontes que divergem:** combinação em que as leituras não concordam (ex.: Biblioteca vazia + YouTube forte + Trends caindo) = decisão do DONO na Parada 2, nunca da IA; produto de impulso (busca fraca + TikTok forte) segue a regra própria acima. O relatório da finalista lista as leituras lado a lado, cada uma com sua evidência.

### Mecânica — medir a comunicação na Biblioteca
`keyword_unordered` funciona quase como AND: query longa zera fácil. Para um zero ter
valor, meça em duas camadas e rode antes um controle
(`atividades de alfabetização para imprimir professora` → ~290; zerou = motor quebrado):

| específica (6–8 palavras) | território (3–4 palavras) | leitura |
|---|---|---|
| 0 | alto | comunicação livre **provisória** — só vira "vaga" depois de `concorrencia-<id>.md` (T9.13); específica vazia sozinha não prova que ninguém vende o mecanismo |
| 0 | 0 | ninguém anuncia — desconfie de nicho sem comprador |
| >0 | alto | ocupado ou disputado — leitura qualitativa com a evidência colada (`### Leitura qualitativa com evidência`) |

Escreva a busca como o comprador escreveria. UI em inglês muda o contador
(`results`). Script em lote `scripts/validar.sh` existe, mas **só se o dono pedir** (regra: medição na Biblioteca é por pane visível). Receita:
`~/.claude/browser-workspace/domain-skills/facebook.com/biblioteca-anuncios-validar-comunicacao.md`.

### Mecânica — Trends e YouTube

> ⚠️ **TRENDS É SEMPRE NO BROWSER, PERFIL `trends` (9234). NUNCA POR HTTP.**
> **Prova de que falhou (10/10/2026):** duas rodadas seguidas de pesquisa (Elétrica e Jiu Jitsu) pediram
> volume no Google Trends e voltaram com **HTTP 429** em todas as tentativas — 0 número medido. A causa foi
> medir por **WebFetch/curl anônimo**, não pelo browser. O IP toma bloqueio e a leitura se perde inteira.
>
> **Regra:** Trends = pane visível, perfil `trends`, headed. **Nada de HTTP.** Se o browser também der 429,
> reporte o erro — mas **nunca caia no HTTP "só pra tentar"**: é aí que a rodada morre.
> Print de cada comparação + valor real do índice (0-100) + direção 12m, por termo e por país.

- Trends: perfil `trends` (9234), `sleep 22` antes do print —
  `domain-skills/trends.google.com/print-e-lote.md`.
- YouTube: exceção declarada (usada na R7; **exceção PERMANENTE — decisão do dono 25/09/2026**; regra geral continua: medição por pane visível) — sem browser (`MINERACAO/scripts/yt-busca.py` + `yt-dlp` de comentários
  recentes) — `domain-skills/youtube.com/busca-e-comentarios-recentes.md`.
- **TikTok: perfil LOGADO, headed** — `tiktok2` (9256) · `tiktok3` (9257) · `tiktok4` (9258).
  (`tiktok` 9255 cai na tela de login — **não use**.) Busca anônima de TikTok não devolve volume;
  logado entrega **visualizações reais por termo + nº de vídeos no tema + comentários com data** — que é
  a mesma régua do gate (comentário de até ~6m). Rodada 10/10/2026 (Jiu Jitsu): o tema vencedor só ficou
  claro depois de olhar o volume, não só o gancho.

### ⏸ Parada 2
Mostre as 1-3 modelagens escolhidas de cada concepção (as ~10 ideias ficam em rascunho), a decisão do comando e a validação (o que foi
medido e o que não foi). Recomende a direção e espere. Atualize o Hub. Formato: `FORMATO DAS PARADAS` (cross: inclui a tabela de candidatos da etapa 2).

---

## GATE DE SAÍDA — GATE 4 · VALIDAR → Parada 2

### GATE 4 · VALIDAR → Parada 2
- [ ] `T9.1` **Território medido em TODAS** as candidatas (1 busca por concepção, barato; termo-NÚCLEO sem qualificador `curso/planilha/kit/pack`, na dúvida meça 2 termos): `sem territorio: 0`. `None` = não medido, nunca zero. **A busca ESPECÍFICA (comunicação modelada) e as 3 fontes são só nas ≤10 finalistas** — território = todas, específica = finalistas (é a reconciliação dos dois trechos; não confundir).
- [ ] `T9.1` Roda no país/idioma de **DESTINO** (cross) — origem não valida destino. Em cross, este item e a etapa 2 do GATE DESTINO usam a MESMA medição feita uma vez sobre os candidatos; os dois gates têm que ficar marcados.
- [ ] `T9.3 · T9.4 · T9.5 · T9.9` Por finalista (≤10 na Biblioteca): as 3 fontes — Biblioteca (específica + território + controle) · YouTube (distribuição + comentário recente ordenado por data, até ~6m com faixas ≤3m e 3-6m + VÍDEO VIRAL ≥100k views, sem exigir recência do vídeo (dono 10/10/2026)) · Trends — + `sinal_de_compra` + teste de urgência. Fonte faltando = "não medido", e a finalista não fecha.
- [ ] `T9.6` Controle (`emagrecer` ≈42.000 ou o do método) rodado a cada ~12 buscas; zerou = descartar desde o último controle bom.
- [ ] `T9.6` **Falso-positivo:** número idêntico ao do controle medido logo antes = contaminação (navegação não aplicou o termo) → remedir (memória `medicao-igual-ao-controle`).
- [ ] `T9.13` **OCUPAÇÃO POR MECANISMO (obrigatória por finalista, antes da Parada 2 e da Obra) [decisão do dono 25/09/2026]** — arquivo `concorrencia-<id>.md` com: (a) **TÉCNICA ÚNICA DE ~10 TERMOS** (a MESMA do cross-market; regra só aqui, `mvt-cross-market` aponta pra cá): escolhida a concepção, pensar ~10 termos que achariam CONCEPÇÕES SEMELHANTES — produto, formato, dor, desejo, público, jeito que o comprador fala, sinônimos do mecanismo — e buscar TODOS na Biblioteca (não 1 específica), **listando os ~10 termos no `concorrencia-<id>.md`** com o resultado de cada um; abrir a página ABERTA de TODO anunciante que aparecer, com a linha `entrega:` (o que recebe, preço, formato, URL); (b) busca no Google pelo mecanismo; (c) marketplaces (Hotmart, Kiwify, Eduzz); (d) lojas de app quando o entregável for app/ferramenta; (e) criadores com "link na bio" vendendo no YouTube/TikTok. `veredito:` NINGUÉM / PARECIDO (diferença escrita) / MESMO — **MESMO volta ao T7**. Sem o arquivo: T9 não fecha, Parada 2 não abre (T10.0), Obra não é montada. Lição R7: Ajuda Eletricista, Kit PMOC Pronto R$19,90, 80 Diagramas R$10/27 só apareceram depois da Obra porque "ninguém vende" saiu de 1 busca específica.
- [ ] `T9.7` Medição toda por pane visível, **máx. 1-2 na Biblioteca simultâneos**, tabela pane→perfil no ESTADO (R6 #6, #11).
- [ ] `T10.1` **Parada 2 montada** no `FORMATO DAS PARADAS` (medido × "não medido" explícito).
- [ ] `T9.2` Território com termo de serviço ("orçamento de X") marcado como possivelmente inflado por serviço local, com fração serviço × produto e número limpo (seção acima).
- [ ] `T9.8` **Pivô:** toda oferta com Obra tem a SUA medição completa (3 fontes + sinal + urgência) em `demanda-*.md`; senão volta a T7 (regra do pivô: orquestradora).
- [ ] **Antes de devolver / da Parada 2:** `gate.py --ate T9` exit 0 (+ Verificador Haiku, regra na orquestradora).
- [ ] `T9.10` Cada leitura FORTE/MÉDIA/FRACA no `demanda-*.md` traz a EVIDÊNCIA colada (views, nº+link dos comentários, quem vende) — número é evidência, não corte (`### Leitura qualitativa com evidência`, decisão do dono 25/09/2026 (revisão)); `sinal_de_compra` = cada comentário com link.
- [ ] `T9.12` Território × específica de cada finalista lido em `validacao-*.md` (deserto/vaga/disputada/ocupado) com a evidência colada (print/anunciantes), sem corte numérico.
