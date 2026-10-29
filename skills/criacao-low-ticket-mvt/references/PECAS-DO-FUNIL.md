# PEÇAS DO FUNIL — bônus · order bump · Upsell 1 · Upsell 2 · downsell · ferramenta

**Criado em:** 2026-10-09 (decisão da dona 09/10/2026) · skill mecânica que executa: **`mvt-funil`**
Alimenta: `SKILL.md` (GATE 6, T13.24) · `CONSTRUCAO.md` §5 (padrões) · `mvt-minerar` (pesquisa do funil do concorrente) ·
`TRILHA-CHECKLIST.yaml` (T13.24).

> **A regra nova:** o funil **não é inventado depois da venda**. Quando a gente monta a oferta (T11 Obra →
> T13 construção) a gente **já sai com bônus, order bump, Upsell 1, Upsell 2 e downsell definidos**, com a
> pesquisa do que é interessante colocar em cada um. Isso é parte do processo, e a prova do que os
> concorrentes empilham entra na **mineração** (`mvt-minerar` › "Minerar o funil do concorrente").

> 🚫 **REGRA PERMANENTE (dono, 10/10/2026): bump existente NUNCA vira bônus automaticamente.**
> Bump no ar é decisão da dona. Pesquisa que diz "esse bump repete a promessa do principal" é
> **diagnóstico, não autorização** — registra como pendência no `FUNIL.md` e **para**. Erro real:
> em 10/10/2026 o orquestrador escreveu sozinho que os OB1/OB2/OB3 da Elétrica passavam a ser bônus
> dentro do Completo, sem ordem, e teve que ser revertido. Destino de bump (sair · virar bônus · ficar)
> **sempre se pergunta à dona**.

> **ATUALIZAÇÃO 10/10/2026 — a pesquisa das peças é trigger T10b, ANTES da Obra (T11).** A dona: "a pesquisa
> tinha que estar rolando desde que começamos a arte". Cada dor de peça do funil passa pelo **GATE DE
> DEMANDA** (`mvt-validar`): **vídeo viral** (YouTube/Shorts **≥100k views** · TikTok **≥1M** ·
> Reels **≥100k** · FB **≥500k**) + **comentário de até ~6 meses** (≤3m = quente; 3-6m ainda válido) +
> **mais de um vídeo** na dor. **O vídeo pode ser antigo — não exija recência**; o que prova que a dor
> segue viva é o comentário recente. Janela era 12m, a dona baixou pra ~6m. Três sinais juntos ou a peça
> não entra.
>
> **Teste da peça, em uma frase — "qual é a PRÓXIMA coisa que essa pessoa precisa depois de comprar o
> principal?"** Peça que repete o que o principal já entrega (no caso dos mapas visuais: mais mapa
> visual) **não é bump, é retrabalho**. Bump tem que ser **irresistível**: resolve dor que o principal
> não resolveu. Dor grande demais pra bump → **Upsell 1/2**.

---

## 1 · Mapa das peças (onde cada uma mora, quanto custa, o que resolve)

| Peça | Etapa do funil | Preço padrão BR (dona 08/10/2026) | Construir em |
|---|---|---|---|
| **VALIDAÇÃO DE TODA PEÇA** | — | — | **Biblioteca de Anúncios: 3-5 criativos ~a cada 15 dias = PASSA; 1 criativo ≥30 dias = PASSA. Menos que isso = não validado** (dono 10/10/2026). Peça validada pra **outro público** pode ser adaptada, desde que a dor exista no público-alvo (validar no Trends+YouTube). |
| **Bônus** (3-4, no principal) | **dentro do plano Completo** (decidido na **T11 Obra**) — **NÃO vira produto/oferta no checkout** (dona, 09/10/2026) | Completo R$27,90 | `mvt-obra-100k` → produção (MVP 40%) |
| **Order bump** (≤3, cada um relacionado ao principal) | **no checkout**, entra no **2º dia** da oferta (Heitor: "não espere validar") | R$7,90 · R$8,90 · R$9,90 · combo dos 3 R$17,90 | `wiven-checkout` §order bumps + imagem/preço/ancoragem |
| **Upsell 1 (barato)** | **1º nó pós-compra** (1 clique, já tem o cartão) | **R$17,90** · downsell **R$12,90** · membro **R$9,90** | `wiven-checkout` › "Upsell no funil" |
| **Upsell 2 (cara)** | **2º nó** (depois da recusa do barato) | 2-3× o principal (R$47,90-67) ou **assinatura** R$19,90+/mês | idem + produto novo no `/painel` |
| **Downsell** | depois da recusa do Upsell 2 → página final | R$12,90 (0,7× o barato) | idem (`next-downsell` ligado a um nó) |
| **Oferta de membro** | no `/painel`, pra quem já comprou | 30% off do normal, piso R$9,90 | `area-membros-netflix` › Ofertas de membro |
| **Cross-sell de oferta irmã** | pode ocupar o lugar do Upsell 2 | preço público da irmã | `criacao-low-ticket-mvt` › "Oferta irmã clonada" |

Cadeia padrão (fonte: `wiven-checkout` › "Upsell no funil"; hoje só existe de verdade no funil Tarot→Cigano):

```
checkout → UPSELL 1 (barato) ─ aceitou → UPSELL 2 (cara) ─ aceitou → Página final
                       └ recusou ────────┘                    └ recusou → DOWNSELL (barato de novo) → Página final
```

- **Ordem padrão: barato primeiro** (maior CVR no calor da compra) e o caro no recusa.
  **Variante B (testar):** caro primeiro — serve quando a peça cara é o produto que já existe pronto
  (ex.: SiteExpress) e a gente quer medir exposição real.
- **Bônus nunca cria produto na gateway** (regra da dona 09/10/2026): ele é **parte do produto** —
  quem paga a oferta do **Completo** recebe `principal + bônus` pelo webhook; o básico libera **só**
  `principal`. Produto/oferta próprio só para **bump, upsell, downsell e combo**. Caso proibido:
  30/09/2026, 4 produtos de bônus R$12,90 criados na Wiven e o webhook não os reconhecia (pagou e
  não recebeu). Regra completa: `criacao-low-ticket-mvt` › `## REGRA DO BÔNUS × PLANO × BUMP`.
- Nunca pular o downsell: quem recusa o caro ainda recebe uma oferta (achado do diagnóstico do Cigano
  `OFERTAS/mapa-do-tarot/produto/UPSELL-CIGANO/DIAGNOSTICO-UPSELL-WIVEN.md` — "recusa ia direto pra
  página final, não apresentava segunda proposta").

## 2 · Regra da PRÓXIMA dor (vale pra tudo: bônus, bump, up/downsell)

Heitor, 5 passos do bônus (transcrição, `CONSTRUCAO.md` §5): **"resolve a PRÓXIMA dor, não a mesma"** —
o principal resolve um problema, a peça resolve a etapa que vem logo depois e que a pessoa também vai
precisar.

Teste de 3 perguntas por peça (3× sim ou não entra):
1. É a **próxima** dor depois do principal (ou a mesma com outro nome → corta)?
2. Formato **rápido** de produzir e fácil de consumir (checklist, mini guia, planilha, app de 1 tela)?
3. Cobre uma **lacuna** que o concorrente não entrega?

**Matriz anti-overlap — preencher antes de criar qualquer peça** (uma coluna por peça já existente):

| Dor da persona | Principal | Bônus 1-4 | Bump 1-3 | Upsell 1 | Upsell 2 |
|---|---|---|---|---|---|

Duas peças na mesma célula = uma delas é redundante (ex.: Jiu-Jitsu — 4 bônus táticos + 3 bumps
fôlego/pegada/combustível; sobrou "lesão" e "progressão" pra upsell). Fonte do inventário:
`produto/texto/INDICE.md` (JJ) · `produto/MANIFESTO-ENTREGAVEIS.md` (Eletrotecnia).

## 3 · FERRAMENTA / microSaaS / webapp como peça do funil (decisão da dona 09/10/2026)

Sendo a entrega um **PDF na área de membros**, um dos upsells mais fortes é **uma FERRAMENTA** — porque
passa de "estudo" pra "trabalho" e porque o método já classifica assim: **característica 8 = Ferramental**
("pode ser usado de forma repetida, como ferramenta") + 6 **Economiza tempo** + 10 **Tangível**
(`CONHECIMENTO/METODO-O-PROCESSO-MVT.md` §3), e **Tipo A = transformar algo difícil em algo fácil**
(§1). A ferramenta não é obrigatória em toda oferta ("nem sempre é assim"), mas é **sempre analisada**
na hora de projetar o funil.

> **⛔ REGRA DURA (dona, 17/10/2026): a ferramenta/webapp é OUTRA DOR / OUTRO PRODUTO — NUNCA "o mesmo
> conteúdo reorganizado".** Se a peça só **busca/filtra/organiza** o que o cliente **JÁ comprou** (ex.: um
> buscador das fichas, um índice do próprio PDF, um "planner" que só rearranja as mesmas páginas), ela **NÃO
> vale como upsell** — o cliente sente "é a mesma coisa organizada". A ferramenta tem que resolver um trabalho
> **DIFERENTE** do que o principal resolve (outro job-to-be-done), com entrega própria. Corolário: se a
> ferramenta é sobre o MESMO acervo, ou ela entra **GRÁTIS como diferencial do principal**, ou **não existe**.
> Caso real GeriNeuro (17/10): um "Card Finder" (filtra as 400 fichas que o comprador já tem) foi **reprovado**
> como Upsell 1 exatamente por essa regra.

### 3.1 Duas formas de usar a ferramenta

| Forma | Quando | Exemplo real | Preço |
|---|---|---|---|
| **Ferramenta como UPSELL 1** (ajuda no TRABALHO dele) | persona tem tarefa **manual, repetida e com custo de erro/tempo** | calculadora/dimensionador, gerador de PDF com a marca dele, template/modelo pronto que substitui o que ele faz na mão, planilha que acelera o serviço | R$12,90-17,90 (add-on de 1 clique) |
| **Ferramenta como TOPO / assinatura** (app que gera/faz a coisa) | a ferramenta tem uso **mês a mês** e dá pra entregar sem serviço humano contínuo | SiteExpress R$150/mês · App de Treino (Tarot/Cigano) · clube com kit novo/mês | R$19,90-150 **/mês** = LTV recorrente (o "microSaaS de topo" do funil de alta conversão, `CONSTRUCAO.md` §5) |

### 3.1b Trial grátis no microSaaS de assinatura (Rodrigo Liedson, método Clube do Dólar — pesquisa 29/10/2026)

Pra reduzir fricção no Upsell 2/topo de assinatura: **cliente clica, assina SEM pagar nada, cobrança só
depois de 1-2 dias de teste grátis.** Card já capturado no clique (1-clique pós-compra), cobrança roda
sozinha no fim do trial — cliente não precisa agir de novo pra virar pagante. Testar junto com a
cadeia já existente (barato→caro→downsell), como variante do Upsell 2/topo quando ele é assinatura.

**KPI que falta no nosso funil: renovação por cliente (cohort), não só MRR agregado.** Rastrear quantas
vezes CADA assinante renovou (1ª compra + N renovações), não só "quantas assinaturas ativas". É o que
prova retenção de verdade — cliente com 8-11 renovações seguidas é o que sustenta o LTV, e sem contar
por cliente isso fica invisível atrás da média. Acrescentar essa coluna/métrica em qualquer dashboard
de assinatura (Trackeador ou gateway de recorrência) quando a oferta tiver microSaaS no funil.

Ferramenta de billing recorrente dele é terceira (fora da gateway principal, tipo "Pretfy") — puramente
pra gerenciar cobrança de assinatura e trial. Registrar se a gente adotar algo equivalente; hoje nosso
padrão é SKU próprio no gateway (Wiven/Mundpay/Zenith) + webhook, não ferramenta externa de recorrência.

### 3.2 Como decidir QUAL ferramenta (pesquisa da persona, não achismo)

Quatro perguntas, respondidas com material que já existe (Comando 4 da mineração, `mvt-minerar`):
1. **O que ele faz NA MÃO hoje** e repete toda semana? (listar as 10 dores/desejos ★ e apontar a tarefa)
2. **Quanto tempo/erro custa** aquilo? (se custa pouco → não vira peça, vira conteúdo)
3. **Já existe GRÁTIS?** Rodar a checagem de mecanismo (`mvt-modelar` › checagem) **antes** de projetar:
   se o grátis cobre 100% da promessa, a ferramenta **não sustenta preço alto** — vira add-on BARATO
   (caso real: `MINERACAO/rodada7-oficios-br/concorrencia-dimensionador-eletrico.md` → App Elétrico e
   5 apps grátis cobrem o dimensionador → "ticket real R$10-17, não R$27"; como *upsell de R$17,90* ao
   lado do mapa, funciona; como oferta de R$37, não).
4. **Qual o formato do resultado?** PDF com marca · tela que imprime · planilha que exporta ·
   app de consulta · app de progresso/tracking · gerador. (O "PDF com a marca do eletricista" é o
   formato que os concorrentes cobram caro e nenhum entrega no celular.)

### 3.3 Escada de implementação (MVP 40% vale pro app também)

1 função que resolve (1 tela) → `SPEC.md` (entradas/saídas/fórmulas + fonte oficial) → `TESTES.md`
(esperado × obtido com caso nosso) → `DEPLOY.md` (URL + curl 200) → acesso pós-compra com prova.
IDs no gate: **`T13.10`–`T13.13`** (só entram quando a Obra menciona app/calculadora/gerador/dimensionador/
ferramenta — `obrigatorio: oferta_app`); área sensível (cálculo regulado: NR/NBR, saúde) exige
**`T13.11` VALIDACAO-DADOS.md** com fonte pública + data, validação FEITA POR NÓS (decisão da dona
25/09/2026, sem revisor contratado).
Stack nossa: HTML/JS servidos do `/painel` (rota isolada), login só por e-mail da compra, webhook Wiven
liberando o SKU, deploy Coolify. Exemplos prontos: `painel/treino-cigano/`, `painel/treino-es/`
(`OFERTAS/mapa-do-cigano/STATUS.md` 05/10).

### 3.4 Proibido aqui

- **Serviço humano contínuo** (mentoria, comunidade, ajuste manual por cliente) — corte do funil
  20→10→3 (`mvt-modelar`); exceção única = produto já pronto da casa com equipe (SiteExpress, 72h).
- Ferramenta **sem SPEC/TESTES** quando o cálculo é regulado.
- Ferramenta entregue **fora da nossa área de membros** (sempre `/painel`, SKU próprio).

## 4 · Preços e simulação de ticket médio

**TABELA DE PREÇO DAS PEÇAS — CHECKOUT × ÁREA DE MEMBROS (dona, 10/10/2026).**
Esta é a tabela da casa; não inventar outra, não arredondar por conta própria.

| Peça | Checkout | Área de membros |
|---|---|---|
| Bump avulso | escadinha **7,90 · 8,90 · 9,90** | **5,90** |
| Combo de bumps | **17,90** | **9,90** |
| Upsell 1 | **17,90** | **9,90** |
| Downsell | **12,90** | **não existe na área** (é oferta de quem NÃO comprou) |
| Upsell 2 (o cara) | **27,90+** | **50% off** |

Regras que acompanham a tabela:

- **Área de membros é SEMPRE mais barata que o checkout** — quem já está lá não custa
  mídia, é lucro. Bump avulso 9,90→5,90, combo 17,90→9,90, upsell 17,90→9,90.
- **O escada do bump é 7,90/8,90/9,90** — os bumps sobem um pouco a cada um no checkout,
  o último da lista é o combo. Na área de membros vão todos a 5,90.
- **Downsell não aparece na área de membros**: é a oferta de quem recusou a principal.
- **Upsell 2 na área = metade do preço** (50% off), não o preço cheio.
- **Cada peça da área de membros precisa de checkout próprio com URL pública.** Card de
  compra com `null` / link de WhatsApp = cliente perdida no WhatsApp (aconteceu na
  Eletrotecnia, 10/10/2026). Gate do `5 · Gates`: nenhum card de venda sem URL.
- Oferta já no ar **não é reprecificada** (só a peça NOVA usa o padrão novo).

Tabela oficial em `CONSTRUCAO.md` §5 (**"PREÇO PADRÃO BR — oferta nova, dona 08/10/2026"**):
básico 17,90 · popup completo 22,90 · completo 27,90 · saída 16,90 · bumps 7,90/8,90/9,90 · combo 17,90 ·
**upsell 17,90 · downsell 12,90** · membro 5,00/9,90.

**Escada por nicho** (medida na mineração, não chute — sempre colher a escada do concorrente em
`concorrencia-*.md`): entrada → bump ~40-60% da entrada → upsell 1 ≈ 1× principal → topo 2-3× → assinatura.
Exemplos colhidos: eletricista R$10 → R$27 → R$67; jiu-jitsu bumps R$9,90-12,90, manual R$17,90/27,90,
programa de progressão R$97.

**Simulação de ticket médio** (hipótese, nunca dado — calcular antes de prometer ganho):

```
ticket = principal + (%bump × preço_bump) + (%up1 × 17,90) + (%up2 × preço_cara) + (%down × 12,90)
ex.: 17,90 + (25% × 17,90) + (10% × 17,90) + (2% × 47,90) + (5% × 12,90) ≈ R$25,8  (+44%)
```

Banda de referência de aceite pós-compra (ORDEM DE GRANDEZA, medir no próprio funil antes de decidir
verba): bump 10-30% · upsell pós-compra 3-10% · downsell 1-3%. **A métrica da peça é o relatório do nó
do funil na Wiven** — traquear o upsell também (transcrição 110: "quanto mais dados de conversão,
melhor"), e a venda do nó novo tem de aparecer no Trackeador.

## 5 · Gates antes de publicar qualquer peça (checklist de saída)

1. **🔴 Entregar o que JÁ foi vendido antes de vender peça nova.** Caso real: 3 bumps do Jiu-Jitsu
   vendidos com entrega ZERO (13 páginas) = maior buraco do portfólio (`PANORAMA.md`). Vender mais com
   entrega pendente = reembolso/chargeback e venda fantasma.
2. `FUNIL.md` **na raiz da oferta** (também aceito em `checkout/` ou `pesquisa/`) com: tabela de peças,
   a matriz da §2, os preços e a cadeia ligada (**T13.24**).
3. Produto + oferta **com NOME** na Wiven (oferta "Sem nome" = validação falha mesmo gravado).
4. **Webhook: o produto novo entra nos DOIS webhooks na mesma hora** (Wiven→nosso `/painel` para entregar
   E Wiven→Trackeador para medir), **"todos os produtos" OFF**. Caso real 1: Cigano criado sem entrar no
   webhook → venda de R$27,90 nunca chegou (05/10). Caso real 2: webhook do SiteExpress em "todos os
   produtos" recebeu venda do Tarot (26/09). Peça vendida dentro do funil de OUTRA oferta = exceção que
   precisa de decisão da dona por escrito.
5. **Gate de eventos:** `data-tk-value`/`data-tk-currency` em TODO botão (inclusive o 1-clique do upsell)
   + prova do request `facebook.com/tr` no ar (`CLAUDE.md` da raiz). Sem prova = "deve estar funcionando".
6. Pacote do checkout novo: banner desktop+mobile, imagem do item, contagem regressiva e imagem em cada
   bump — o checkout de upsell/irmão nasce com os 4 (`wiven-checkout` › 5b).
7. Card do item novo no `/painel` **bloqueado → modal → checkout do SKU** (`CHECKOUT_URL` do SKU preenchido;
   `null` hoje cai no WhatsApp) + oferta de membro do item criada junto.
8. ACESSO-TESTE.md: compra-teste → 4 pontos de acesso (T13.14).
9. Registrar no Hub (`notas`: preço da peça, status) e, se mudou preço/ticket, na entrada do
   `trafego/ANALISES.md` (regra 07/10/2026) e nas observações do `KEVONES/README.md`.
   **E, sempre que mudou preço/página/headline/público/verba ou trocou/pausou um anúncio, no
   `KEVONES/MUDANCAS.md`** (`data · oferta · tipo · o que mudou → Como ler`) — as análises de
   tráfego leem esse arquivo antes de decidir; mudança no meio do teste zera o relógio de 48h/7d.

## 6 · Anti-padrões (cortar na hora)

- Peça que repete dor do principal ou de outra peça (matriz §2 vazia = não pesquisou).
- Bump aleatório do mesmo nicho que não **completa** o principal (`CONSTRUCAO.md` §5 — Borba).
- Empilhar 8-10 bônus (satura e passa impressão de produto fraco) — ~3-4 bônus, ≤3 bumps.
- Subir o ticket da frente pra "ganhar mais": regra da dona no `KEVONES/README.md` — ticket baixo é
  volume de propósito; o ticket sobe **no pós-compra**.
- Ferramenta cara sem checar grátis/app concorrente antes.
- Downsell esquecida (recusa vira fim de funil).
- Preço novo inventado fora da tabela 08/10 sem decisão da dona com data.

## 7 · Onde a pesquisa entra (fecho do processo)

| Onde | O que registrar |
|---|---|
| `MINERACAO/<rodada>/concorrencia-*.md` + `destrinchar-*.md` | **stack do funil do concorrente**: bônus, order bumps, upsell/downsell, **ferramenta/app entregue**, preço de cada peça, o que é grátis (bloco "Minerar o funil do concorrente" em `mvt-minerar`) |
| `HUB-OFERTAS/ofertas.json` | `preco_basico`/`preco_completo` + `notas` com as peças (bumps/upsell/ferramenta) |
| `OFERTAS/<slug>/FUNIL.md` | tabela final de peças + matriz §2 + cadeia + preços (T13.24) |
| `OFERTAS/<slug>/checkout/` | textos e artes de cada peça (`order-bumps/`, `upsell/`, banners) |
| `OFERTAS/<slug>/trafego/ANALISES.md` | resultado por peça depois no ar (ex.: "IC R$27 vs R$6") |
| `KEVONES/MUDANCAS.md` | **mudança feita nesta rodada** (preço/ticket, página/headline, bump, público, verba, **troca/pausa de anúncio**) → campo "Como ler" — fonte que a análise de tráfego lê antes de decidir |
