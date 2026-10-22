---
name: mvt-funil
description: MECÂNICA chamada pela skill `criacao-low-ticket-mvt` (T13.24) — projetar e montar as peças do funil de VENDA de uma oferta: bônus, order bump, Upsell 1 (barato), Upsell 2 (cara), downsell, combo, cross-sell de oferta irmã e a peça de FERRAMENTA/microSaaS/webapp (calculadora, gerador, template que acelera o trabalho, app de topo em assinatura). Cobre a pesquisa (o que a persona faz na mão + o que o concorrente empilha, mineração), o desenho em `FUNIL.md`, preço na tabela da dona 08/10, MVP de cada peça, criação no gateway (delegando `wiven-checkout`), entrega no `/painel`, webhook dos 2 destinos, gate de eventos e leitura do resultado por nó. Use quando a oferta for montar/alterar bump, upsell, downsell, "opção 2 mais cara", vender ferramenta/app junto do PDF, ou quando o dono perguntar "o que põe depois da compra".
---

# mvt-funil — peças do funil (bump · upsell · downsell · bônus · ferramenta)

Regra da skill-mãe (`criacao-low-ticket-mvt`): **o funil é projetado junto com a oferta (T11 → T13),
não depois**. As regras de concepção/preço/gates estão em
`~/.claude/skills/criacao-low-ticket-mvt/references/PECAS-DO-FUNIL.md` — **ler antes de começar**;
aqui é a EXECUÇÃO passo a passo.

> ⛔ **`references/ESTRUTURA-DE-PENSAMENTO.md` §7 é a porta desta skill.** Toda peça do funil nasce
> de uma **dor da persona que o principal não resolve**. Filtro = "é dor da persona?" + "tem demanda?";
> **concorrente NÃO impede** (vende-se pra quem já comprou — o dado dele é preço/posicionamento);
> formato livre (visual, PDF, curso ou pasta vazia); simples = bump barato, complexo = **upsell mais
> caro**. ⛔ só sai quando a dor não é da persona (público errado) ou a peça foi refutada pelo dado
> de venda.

> **IDs de gate** = `TRILHA-CHECKLIST.yaml` · **T13.24** (funil/bumps/upsell/downsell em `FUNIL.md`) ·
> `T13.10`-`T13.13` (peça APP: SPEC/TESTES/DEPLOY) · `T13.14` (ACESSO-TESTE) · conferir com
> `mvt-auditar`: `python3 scripts/gate.py --rodada <rodada> --passo T13 --oferta <slug>`.

## ENTRADA EXIGIDA (conferir ANTES de começar)

- Parada 3 liberada + `pesquisa/obra-de-arte.md` existente (GATE 6) — sem Obra não se projeta funil.
- Inventário do que a oferta JÁ entrega: `produto/texto/INDICE.md` ou `produto/MANIFESTO-ENTREGAVEIS.md`
  (bônus e bumps já escritos) + página/planos atuais (básico, completo, popup, saída).
- Mineração da rodada com o bloco **"Minerar o funil do concorrente"** (stack de peças + preço de cada).
- Prompt de todo pane: `references/PROMPT-PADRAO-PANE.md` (copiar no prompt, nunca "veja a skill").
- Sem `ESTADO.md` com `## ROTEADOR` gravado, esta skill não roda (chame `criacao-low-ticket-mvt`).

> 🖼️ **PÁGINA DE UPSELL — USE O MODELO BOM (dona, 16/10/2026).** A página de Upsell 1/2 (e o downsell)
> segue o **`references/MODELO-PAGINA-UPSELL.md`** — exemplo canônico:
> **`mapadotarot.leadgo.dev/upsell-cigano/`** (estrutura enxuta, mesmo design system da oferta, CTA
> repetido em toda dobra, recusa → modal de downsell). **Copiar a ordem das 12 seções** e adaptar
> tokens/preço/texto. Não inventar layout do zero — a dona reprovou página de upsell feita fora desse molde.

## Passo 1 · Pesquisar as peças (antes de decidir qualquer preço)

> **Referência de mercado SINTETIZADA (ticket · bump · upsell · in-area · preços por mercado):**
> `references/FUNIL-MERCADO-2026.md` — ler antes de fixar preço/nó; atualizar a cada rodada de pesquisa.

> 🚫 **REGRA PERMANENTE (dona, 10/10/2026): SÓ ABRIR PERFIL DE BROWSER QUE VAI USAR.**
> Dois panes com a mesma pesquisa abrem perfis do Playwright ao mesmo tempo e poluem a tela da dona —
> e abrem sessão **`stock`** (não logada, fora da lista). **Antes de abrir browser: `pane_list` e ver se
> outro pane já está nessa pesquisa.** Já duplicou várias vezes.
> Erro real: 10/10/2026, pane-4161 abriu sessão `stock` no YouTube buscando "erro de cálculo instalação
> elétrica" enquanto o pane-4160 já rodava essa mesma pesquisa na Ad Library. Fechado.
> **Um pane = uma pesquisa.** Só sessão da lista: `adslib2/3/4` · `trends` (9234) · `tiktok2/3/4`.
> **Nunca `stock`**, nunca sessão não listada.

> ⚠️ **GOOGLE TRENDS NUNCA POR HTTP (dono, 10/10/2026).** Duas rodadas seguidas de pesquisa de peças
> (Elétrica e Jiu Jitsu) voltaram com **HTTP 429 e 0 número medido** porque mediram volume por
> WebFetch/curl anônimo. **Trends = perfil `trends` (9234), pane visível, headed, com print e o índice
> real (0-100) + direção 12m, por termo e por país.** Se nem no browser destravar, o veredito escreve
> **"volume não medido"** e segue por Ad Library + YouTube — **nunca preenche o buraco com estimativa
> silenciosa.** Mecânica: `mvt-validar` › "Mecânica — Trends e YouTube".

> 🚫 **REGRA PERMANENTE (dono, 10/10/2026): NUNCA transformar bump já existente em bônus por conta própria.**
> Bump que existe e está no ar é **decisão da dona**. A pesquisa pode dizer que ele repete a promessa do
> principal — **isso é diagnóstico, não autorização.** Registrar o diagnóstico no `FUNIL.md` como
> pendência e **parar**. Não mover, não renomear, não reclassificar, não "limpar o campo".
> Erro real desta regra: em 10/10/2026 o orquestrador escreveu sozinho "os bumps atuais passam a ser
> bônus dentro do Completo" no `FUNIL.md` da Elétrica — **sem autorização** — e teve que ser revertido.
> Destino possível de um bump (sair · virar bônus · ficar como está) **sempre se pergunta**.

> **REGRA DA DONA (10/10/2026) — a pesquisa das peças do funil roda EM PARALELO com a arte, nunca depois.**
> "A pesquisa tinha que estar rolando desde que começamos a arte."obra de arte que começa sem as dores
> das peças do funil já validadas gera piece de funil que não vende, e retrabalho. Trigger **T10b** da
> skill-mãe: antes de T11 (OBRA DE ARTE), as dores de OB / Upsell 1 / Upsell 2 já estão pesquisadas
> e passadas no **GATE DE DEMANDA** (`mvt-validar`): **vídeo viral** (YouTube/Shorts **≥100k** ·
> TikTok **≥1M** · Reels **≥100k** · FB **≥500k**) + **comentário de até ~6 meses** (≤3m quente) +
> **mais de um vídeo** falando da dor. **Vídeo pode ser antigo — não exija recência do vídeo**; o que
> prova que a dor segue viva é o **comentário recente**, não a data do vídeo. Faltou um dos três
> sinais = a peça não entra no funil.

**Cada peça do funil responde a UMA pergunta: "qual é a PRÓXIMA coisa que essa pessoa precisa, logo
depois de comprar o principal?"** — não "o que mais combina com o produto". Peça que responde a
outra pergunta é peça que não passa. O formato segue da dor, não do inverso: PDF · template ·
planilha · checklist · **web app plug-and-play** · microsite. Dói "quanto eu cobro" → gerador de
orçamento. Dói "não consigo treinar" → plano dos primeiros 30 dias. Dói "não sei se é seguro" →
checklist de serviço. Dor grande demais pra bump (curso inteiro) vira **Upsell 1/2**, não OB.

**Peça de bumps tem que ser IRRESISTÍVEL.** Se ela é "nice to have" ou repete o que o principal já
entrega (mapa visual a mais, no caso dos mapas), ela não vende: o comprador já tem o produto e não
precisa da mesma promessa cobrada de novo. **Bump que não vende é só tempo queimado** — nesse caso
troque a peça, não o preço.

**4 · VALIDAÇÃO DE PEÇA NA BIBLIOTECA DE ANÚNCIOS (dono, 10/10/2026) — a régua mais forte que existe.**
Buscar a **persona** na Biblioteca de Anúncios e ver **o que já está sendo vendido e RODANDO**. Produto
que tem愛 outro alguém pagando anúncio todo dia é produto **validado de mercado**, não hipótese nossa.
Candidate **low ticket, curso, ferramenta, programa** — tudo que dá pra adaptar em peça nossa.

**Régua de rodagem (a que vale pra PEÇA DE FUNIL, mais tolerante que o GATE DE ORIGEM):**
- **3 a 5 criativos rodando, um a cada ~15 dias → PASSA.** Válido mesmo com público pequeno: o que
  importa é que o anunciante **sustenta a veiculação**. Isso é dinheiro real gastado por terceiro.
- **1 criativo rodando há ≥30 dias → PASSA TAMBÉM.** Um criativo que segura 30 dias sozinho é forte
  sinal —，意味着 o anúncio converte e o anunciante não precisa trocar por outro.
- Menos que isso (criativo de 7-10 dias e nenhum outro) = **não validado**, ainda é achismo.

Só essa régua, para **PEÇA DE FUNIL**. O GATE DE ORIGEM (15d/7d, ≤10k IG) continua valendo para
concepção/quase-clone — são coisas diferentes, não misture.

**Adaptação entre AUDIÊNCIAS é o caminho, não o problema (dono, 10/10/2026).** Achou peça validada
pra **outro público**? Ex.: "anunciando jiu-jitsu infantil, e esse produto é pra adulto" — aí a pergunta
**não é** "descarte por ser infantil", é **"o problema do adulto é o mesmo?"**. Se a peça validada
resolve uma dor que o adulto também tem, ela é candidata — e aí **valide a adaptação** no Trends +
YouTube do público ADULTO antes de construir. Descartar por público diferente é erro; só é seguro
descartar quando a dor de fato não existe no outro público.

a) **Persona / tarefa na mão** — Comando 4 da mineração + a lista de dores ★: o que ele faz **manualmente,
toda semana, com tempo ou risco de erro**? Dali saem os candidatos de **ferramenta** (calculadora,
gerador de PDF/planilha, template/modelo, app de consulta/progresso).
   - **A pesquisa de PERSONA/DOR também é FONTE DE PEÇA (dona, 17/10/2026):** varrer
     `pesquisa/PERSONA-E-ANGULOS.md` — o **banco de dores** e, principalmente, as **dores FORA DO ESCOPO** do
     principal — dessas saem **bônus/bump/upsell novos**. E a mineração às vezes revela uma **dor nova** que
     ninguém tinha mapeado → **é candidata a peça** (entra no `FUNIL.md`). Filtro de sempre: é dor da
     persona? o comprador **NÃO tem isso** no que acabou de comprar? (senão é "mesma coisa organizada" = reprovado).
b) **Concorrente** — bloco "Minerar o funil do concorrente": o que ele empilha (bônus, bumps, upsell,
ferramenta, preço por peça, o que é grátis).
   - **E o funil POR DENTRO da área de membros (dona, 17/10/2026):** estudar como o mercado **vende o que
     está BLOQUEADO na área** (cards com cadeado → **oferta nova/bump in-area**), o **ticket típico** do low
     ticket gringo (principal), a escada de **order bump / upsell** dele e o que ele entrega em cada nó.
     Registrar em `checkout/PESQUISA-FUNIL-<mercados>.md`. Vale pra US/BR/ES.
c) **YouTube — vídeos RECENTES de low ticket (últimos ~6 meses) (dona, 17/10/2026):** buscar no YouTube
   (`yt-dlp "ytsearchN:<termo>"`, sem browser) por conteúdo **recente** de low ticket/funil e **transcrever**
   (`yt-transcricao`) — de onde saem **ticket típico, escada de bump/upsell, monetização in-area e preço por
   mercado**. Filtro: **≤ ~6 meses** (o assunto muda rápido; o recente é o que vale).
d) **Mapa de preços por mercado (dona, 17/10/2026):** manter um **mapeamento de preços por mercado** —
   **BR (R$) · LATAM · EUA (US$) · genérico inglês · Europa (€) · Portugal (€) · França (€)** — principal +
   cada nó do funil. A tabela 08/10 é **BR**; cada mercado tem o seu ponto. Registro: `MAPA-DE-PRECOS.md`
   (ou a referência de preços do portfólio). Não inventar: cruzar tabela da dona + pesquisa do mercado.

> 🔑 **BÔNUS DO CONCORRENTE É BLUEPRINT (dona, 10/10/2026).** *"O bônus do cara pode ser nosso order
> bump, nosso produto principal, qualquer coisa."* Ao entrar numa página de concorrente para analisar,
> **os bônus dele são fonte de peça** — muito mais que o preço dele. Referência dada pela dona:
> `jiu-jitsutreinos.lovable.app` (97 dias rodando), bônus = Finalizações · Defesas e Escapes ·
> Controle e Dominância no Tatame (os 3 "grátis", R$ 29,90 riscado).

> 🚫 **BÔNUS DELE = NOSSO ORDER BUMP, NÃO BÔNUS (dona, 10/10/2026).** Peça que vem da tela de bônus de
> um concorrente **entra no checkout como order bump** — bônus é coisa que mora dentro do Completo e é
> liberada pelo webhook, não peça avulsa. O que **se mantém** é o **combo** dele (o pacote das 3), se
> quiser copiar essa parte. Provado no Jiu-Jitsu: os 3 bônus do `jiu-jitsutreinos` viraram os 3 bumps
> novos da oferta, e o combo ficou.
> **Como pegar o blueprint certo (o caminho que a dona usou, 10/10/2026):** Ad Library → buscar a
> **persona** → achar oferta **low ticket** → entrar na **página** → entrar no **checkout** → ler os
> **bônus** e os **upsells** dele. Bônus e upsell de checkout são a mineração mais barata que existe:
> é o concorrente **já recolhendo o dinheiro** e te mostrando a carteira.
> **Preço e formato saem de lá também** — não invente o que ele já cobrou. Ex.: o bloco dele
> "APROVEITE E LEVE JUNTO COM 90% DE DESCONTO" (âncora R$ 15–19 → R$ 4,97–6,97) é a tática dele.

> 🚫 **RÉGUA DA PEÇA — a que mais morde, e ela já mordeu (dona, 10/10/2026).**
> **A régua é a PEÇA, não a DOR.** Dor validada + peça repetida = bump que não vende.
> Erro real: a peça "Defesas Que Funcionam Sem Força" passou no Autocomplete (**10/10 nos 4 países**),
> no gap contra o concorrente e na régua de rodagem — e a dona reprovou: *"isso ainda é muito o produto
> principal. A pessoa olha e pensa: já tem isso aqui, não vai querer comprar"*. A dor que a peça
> prometia resolver **era o produto principal em si**.
> **Antes de propor qualquer peça, abra o entregável do principal e responda por escrito:**
> **"o comprador já tem isso no que ele acabou de comprar?"** → **✅ gapa** (não está) · **⚠️ parcial**
> (toca e vai além) · **❌ repete** (já está — não serve de bump, sai da lista).
> Passar no gate de demanda **não autoriza construir**. Falta essa pergunta.
c) **Grátis** — checagem de mecanismo (`mvt-modelar`): se app/grátis cobre 100%, a ferramenta só entra
como peça **barata** (add-on), nunca como opção cara.
d) **Escada de preço do nicho** colhida em `concorrencia-*.md` (ex.: eletricista R$10→27→67).

## Passo 2 · Desenhar o funil → gravar `OFERTAS/<slug>/FUNIL.md` (na RAIZ, também aceito em `checkout/` ou `pesquisa/`)

Conteúdo obrigatório (é o que T13.24 verifica):
1. Tabela de peças: `peça · etapa · preço · formato · próxima dor que resolve · arquivo de conteúdo`.
2. **Matriz anti-overlap** dor × (principal · bônus · bumps · up1 · up2) — célula repetida = corta.
3. **Cadeia ligada:** checkout → Upsell 1 → (aceite/recusa) → Upsell 2 → (aceite/recusa) → Downsell →
   página final. Registrar se a ordem é **barato-primeiro** (padrão) ou **caro-primeiro** (variante B,
   decidida com dona).
4. Preços + de onde vieram (tabela 08/10 ou decisão da dona com data).
5. Se a peça é **ferramenta**: 4 perguntas da §3.2 respondidas (tarefa manual? custo de erro? grátis?
   formato do resultado) + como será o MVP de 1 função.

**Bônus não cria produto no gateway** (dona, 09/10/2026): bônus mora **dentro do Completo** e é
liberado pelo webhook (`COMPLETO_OFFERS`); o básico leva só o principal. Produto/oferta próprio só
pra **bump · upsell · downsell · combo**. Regra cheia: `criacao-low-ticket-mvt` › `## REGRA DO BÔNUS × PLANO × BUMP`.

> **Upgrade de tier (Essencial → Completo)** = produto próprio, **R$ 5,90 fixo** (nunca o % off — dona
> 13/10): nome **com o produto** (`Upgrade <Produto> Essencial → Completo - Área de Membros - Idioma
> Português (BR)`), **capa = mockup do Completo com "UPGRADE PARA COMPLETO" por cima**, e entra no
> checkout do principal como **1º order bump escopado SÓ à oferta Básica** (não aparece no Completo).
> Mecânica: `wiven-checkout` §2b.
>
> **PDF de entrega** do produto principal (Wiven → Entregas → Arquivos, só os principais): nome **= o
> nome do produto**, tudo clicável; gerador `MODELOS/PDF-DE-ENTREGA/`. Detalhe: `wiven-checkout` §3b.

Cotas da `PECAS-DO-FUNIL.md`: **bônus ~3-4 · bumps ≤3 · 1 combo** · Upsell 1 e 2 no máximo ·
peça que repete dor de outra = corta.

## Passo 3 · Preço (sem inventar)

Tabela oficial (`CONSTRUCAO.md` §5, dona 08/10/2026): bumps 7,90/8,90/9,90 · combo 17,90 ·
**upsell 17,90** · **downsell 12,90** · membro 5,00/9,90 · **upgrade de tier = R$ 5,90 fixo** (dona 13/10; nunca o % off).
Oferta já no ar mantém o preço dela; a peça NOVA usa o padrão novo. Preço fora da tabela = decisão da
dona escrita no `FUNIL.md` (data) — nunca derivar de "parece que vende".

## Passo 4 · MVP de conteúdo de cada peça (~40%)

Mesmo ritmo do produto: texto → 10 páginas-imagem → publicar → completar. **Peça APP** segue
`T13.10`-`T13.13` (`SPEC.md` → `TESTES.md` esperado × obtido → `DEPLOY.md` URL + curl 200), e se o
cálculo for regulado (NBR/NR/saúde) também `T13.11 VALIDACAO-DADOS.md` com fonte oficial + data,
validação feita por nós. **Gate duro: peça nova só sai depois de tudo o que já foi vendido estar
entregue** (ex.: 3 bumps do Jiu-Jitsu sem nenhuma página = não vender mais nada antes).

## Passo 5 · Montar no gateway (delegar a mecânica de tela)

- **BR padrão = Wiven** → skill **`wiven-checkout`**: criar produto + **oferta com NOME**; bumps com
  imagem/preço/ancoragem; Adicionar etapa → Produtos → nó Upsell; ligações `next-upsell` /
  `next-downsell`; **Salvar funil → reabrir** (React Flow mostra 0 arestas até o ciclo de abas);
  script **1-clique** em "Script do botão" (`product-funnel.js`, só com params `OCB_*`);
  §5b pacote do checkout novo (banner d+m, imagem do item, contagem, imagem de cada bump).
- Outros gateways só por decisão da dona: `mundpay` (EUR/USD) · `ggcheckout-produto` ·
  `hotmart-produto-playwright`. Multi-moeda: `references/PRECO-MOEDA-LOCAL.md` em TODO preço visível,
  inclusive página de upsell e popup de downsell.

## Passo 6 · Entrega no `/painel` (skill `area-membros-netflix`)

Card novo **bloqueado → modal → checkout do SKU** (`CHECKOUT_URL[sku]` preenchido; `null` hoje cai no
WhatsApp), conteúdo em `/painel/conteudo/<sku>/` protegido por sessão + ownership, PDF do bloco,
**oferta de membro do item criada junto com o checkout** (30% off, piso 9,90, item único, redirect
/painel), e a **conta de teste `teste@seudominio.com` com o item liberado**.

## Passo 7 · Rastreio e entrega (os 2 webhooks) — na MESMA hora do cria

- Produto novo marcado nos **2** webhooks: Wiven→`/painel/api/webhooks/wiven` (entrega) e
  Wiven→Trackeador (medição). **"Disparar para todos os produtos" OFF** sempre. Vale pra **TODA**
  peça: principal, **order bump**, combo, upsell, downsell, **upgrade Essencial → Completo**,
  produto irmão/cross e oferta de membro — e o produto/offer entra no `PRODUCT_SKUS`/`COMPLETO_OFFERS`
  do servidor. O webhook é **por produto**: produto criado depois **não entra sozinho**; recontar
  `/panel/webhooks` depois de cada produto novo e de mexer em funil (regra da dona 16/10/2026 —
  order bump "Combo Domínio Total", Jiu-Jitsu, vendeu e não entrou no Trackeador).
- Peça de OUTRA oferta dentro deste funil (cross-sell) = exceção → decisão da dona por escrito antes.
- Produtos fora do webhook = pedido sem log, venda some do tracker e cliente sem acesso
  (`wiven-checkout` › §6, caso do Cigano 05/10).
- ACESSO-TESTE.md: compra-teste → 4 pontos de acesso (T13.14).

## Passo 8 · Gate de eventos + prova

Todo botão da peça com `data-tk-value`/`data-tk-currency` (inclusive o 1-clique do upsell) e **prova do
request `facebook.com/tr` no ar** (browser, nunca "deve estar funcionando"). Botão que só abre popup não
leva href de checkout (IC dobrado). Se a página tem quiz/eventos, rodar o gate inteiro da raiz.

## Passo 9 · Medir e ajustar (fecha o ciclo)

- Relatório **por nó** do funil (Wiven → Desempenho): exibições × aceites de cada upsell/downsell —
  **traquear o upsell também** (transcrição 110: mais dado de conversão = melhor).
- Conferir a venda da peça no Trackeador (produto no dashboard certo) e registrar em
  `OFERTAS/<slug>/trafego/ANALISES.md` (entrada datada) +, se mudou preço/ticket, no
  `KEVONES/README.md` (observações duráveis da dona).
  **Mudou preço/página/headline/público/verba ou trocou/pausou anúncio? → `KEVONES/MUDANCAS.md`**
  (`data · oferta · tipo · o que mudou → Como ler`), na hora: a próxima análise de tráfego lê
  esse arquivo antes de decidir e não julga CPA/IC/venda de antes da mudança.
- Simulação de ticket médio antes de prometer ganho: `PECAS-DO-FUNIL.md` §4.
- Caiu (0-1% de aceite)? Trocar a peça (próxima dor), não o preço. Subiu? Variante B (caro-primeiro)
  como teste A/B do 2º nó.

## GATE DE SAÍDA (saída verificável — senão o passo não fecha)

- [ ] `OFERTAS/<slug>/FUNIL.md` existe com tabela + matriz + cadeia + preços → `gate.py --passo T13` sem FALTA em T13.24.
- [ ] Toda peça tem conteúdo MVP existente (arquivo/URL), não "vamos criar depois".
- [ ] Tudo que já estava vendido está ENTREGUE antes da peça nova ir ao ar.
- [ ] Produtos novos com oferta NOMEADA no gateway, nos 2 webhooks, e a venda de teste aparece no Trackeador.
- [ ] Prova `facebook.com/tr` da peça capturada (valor e moeda certos) + ACESSO-TESTE.md (T13.14).
- [ ] Card bloqueado + oferta de membro + conta de teste com o item liberado no `/painel`.
- [ ] Hub (`notas`) e `trafego/ANALISES.md` com a peça, o preço e a decisão da dona (quando houver desvio).

Ponteiro da skill-mãe: `criacao-low-ticket-mvt` › `## ÍNDICE` (linha "T13 funil") e `## FASE DE CONSTRUÇÃO` item 5b.
