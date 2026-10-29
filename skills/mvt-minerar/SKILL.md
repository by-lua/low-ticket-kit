---
name: mvt-minerar
description: MECÂNICA chamada pela skill `criacao-low-ticket-mvt` (passo 1 · T2 MINERAR, todos os modos). Minera concepções na Biblioteca de Anúncios pelo browser e registra no Hub: famílias de termos/Comandos 1-4, cota por termo como PARADA, checklist 100k, os 2 links (Biblioteca + página) e print, link não bloqueia, seguidores do Instagram na aba Sobre, falso-zero, scripts de link/preço (exceção do dono), registro no Hub; inclui modo D (rastreadores/oferta-first) e modo F (recorte técnico→visual). Use quando a orquestradora chegar em T2, quando o usuário pedir "minerar", "varrer a Biblioteca", "achar concepções", ou ao retomar a mineração.
---

# mvt-minerar — passo 1 (T2 MINERAR)

> **Nomes de seção no texto abaixo** (`GATES TRAVADOS`, `ADENDO §x`, `passo N`, `FASE DE CONSTRUÇÃO`, `ROTEADOR`, `PASSO 0a/0b`, `PROMPT-PADRÃO`) são os da skill original, já dividida: cada um agora mora onde o `## ÍNDICE` da skill `criacao-low-ticket-mvt` aponta. O texto das regras não foi alterado.

> **IDs dos subpassos** = os de `criacao-low-ticket-mvt/references/TRILHA-CHECKLIST.yaml`; evidência com nome de arquivo padronizado, conferida por `scripts/gate.py --passo T2`. Saída ≠ 0 = passo aberto.

## ENTRADA EXIGIDA (conferir ANTES de começar — GATE DE PASSAGEM da orquestradora)
- T0 gravado: bloco `## ROTEADOR` (R1-R5) no ESTADO + eco ao dono.
- T1 fechado: GATE 0 (método lido, ESTADO, Hub `bate: True`, modo/nicho/preço) — evidências coladas.
Entrada ausente = passo anterior ABERTO: volte a ele pela TRILHA do modo em `criacao-low-ticket-mvt`. 
Sem `ESTADO.md` com o bloco `## ROTEADOR` gravado, esta skill não roda (chame primeiro `criacao-low-ticket-mvt`).

Prompt de todo pane que toca browser: `~/.claude/skills/criacao-low-ticket-mvt/references/PROMPT-PADRAO-PANE.md` (blocos obrigatórios de todo `pane_spawn` que toca browser, minera ou mede — copiados no prompt, nunca "veja a skill").

> **Pergunta aberta do dono ("o que vender em X?") = início da MINERAÇÃO** [decisão do dono 25/09/2026]: entregue o PLANO DE MINERAÇÃO (modo, público, termos, pedido de ok), nunca lista de ideias. Ideia gerada por brainstorm/Comando 4 não é resultado de mineração: entra em T7 como candidata com prova de mercado (T7.30). Regra: `criacao-low-ticket-mvt` § REGRA DE FALA.

## Regra que vale para TODAS as mecânicas — link não bloqueia

**LINK DA PÁGINA NÃO ACHADO NUNCA ELIMINA NEM BLOQUEIA** (dono, 24/09/2026: "não conseguir pegar o link da oferta não é impedimento… não temos que pular uma oferta só porque o pane não achou o link naquele momento"). Sem link de página (WhatsApp, card sem `l.php`, página fora do ar, pane não achou) → registra `pagina_vendas: PENDENTE (motivo, data)`, mantém o link da Biblioteca, e a concepção SEGUE no fluxo e no gate. "Link conferido" no gate = conferir que os criativos contados são da mesma oferta QUANDO o link existe; sem link, conta pelos criativos do mesmo anunciante com a mesma promessa e anota a ressalva. Nunca NAO_PASSA, nunca passo aberto, nunca descarte por falta de link.

## Abertura da mineração (nicho/persona, formato, volume, direito autoral)

**Do ZERO (decisão do dono 25/09/2026; regra mora na orquestradora, ROTEADOR R1):** nada de rodada anterior entra por iniciativa própria — não excluir áreas/termos já minerados, não usar rodada antiga como referência de concorrente, não reaproveitar concepções. Se reaproveitar parecer útil, PERGUNTAR ao dono antes (1 pergunta) e registrar a resposta no ESTADO.

Pergunte também, em 1 linha: **"já tem nicho/persona definido?"** Não → Comando 1 amplo (sem nicho). Sim → rodar Comandos 2, 3 e 4 além do 1 e registrar as famílias usadas (R4 e R5 tinham nicho definido e só usaram termos formato×nicho escolhidos à mão).

**Filtro de FORMATO na abertura (R6, 24/09/2026):** o dono pode pedir "amplo, mas bem visual tipo mapa
mental". Isso NÃO é nicho: roda o Comando 1 amplo, só trocando os termos de formato pelos visuais —
`mapa mental` · `mapas mentais` · `resumo visual` · `infográfico` · `flashcards` · `esquema visual`
(3 termos por pane, 1 perfil por pane). Registrar no ESTADO como "nicho amplo, filtro de formato X".

**Protocolo desta operação** (decisão do usuário, 18/09/2026): minerar AMPLO como o método
manda — vários anúncios, vários nichos, tudo estruturado (dois links, print, preço quando der,
9 elementos, modelagem) — e só depois **estreitar para 55 a 60 concepções**, pegando **um pouco
de cada nicho** para não perder área nenhuma. Nicho saturado não é motivo de exclusão na coleta;
a saturação que importa é a da NOSSA comunicação modelada, medida na etapa 4.

**Direito autoral é motivo legítimo de descarte** — e o único tipo de corte que se faz cedo.
Conteúdo de terceiro revendido sem direito (acervo de HQ, packs de MP3, filmes/séries, livros
de editora, "+10.000 vídeos virais para revender") não vira produto nosso: além do risco
jurídico, o Facebook reprova anúncio de revenda de conteúdo não-original e o criativo
demonstrativo fica impraticável. Duas saídas, nesta ordem:
1. **Recortar para o que é nosso** — em vez do pack de MP3, "repertório de louvor por momento
   do culto + cifras simplificadas"; em vez do acervo de HQ, "guia de precificação + checklist
   para revendedor". Foi o que salvou R3-117 e R3-068 na rodada 3.
2. Não havendo recorte legítimo, **descarte com o motivo escrito** (foi o caso de R3-224,
   doramas — a única descartada de 243).
Vale para PLR também: só entra com direito de revenda comprovado.

**Nada com potencial é descartado, salvo descarte por método (definitivo, passo 3 item 6).** O que não entra na leva do momento recebe `leva:
"proximas-levas"` no Hub, com a modelagem e o checklist 100k já feitos — entra na leva seguinte
sem re-minerar. Descarte de verdade só por motivo de método escrito — e o descarte por método do passo 3 (item 6) é definitivo. Na rodada 3, de 243
concepções, exatamente 1 foi descartada (direito autoral) e 6 eram duplicatas cross-listadas.

Por que estreitar: o caro não é minerar nem modelar, é **aprofundar** — medir comunicação e
território na Biblioteca (até 4 buscas por concepção, com re-medição por causa do falso-zero),
YouTube, Trends e Obra de Arte. Esse gasto só se justifica em quem vai virar oferta agora.
Na rodada 3 isso baixou a fila de 282 buscas para 63.

**Os rótulos de nicho vêm errados da mineração — revise antes de usar em cota.** Na R3,
"diagnóstico de ar condicionado" estava em *Saúde/Terapia* e "criar vídeo com IA" em
*Educação/Concursos*. Cota de nicho sobre rótulo errado joga categorias inteiras para fora (foi
o que aconteceu com os ofícios técnicos). Antes de aplicar a cota, passe os olhos nos rótulos e
corrija os que não batem com o mercado real.

**Como estreitar:** cota por nicho (ex.: 5 por nicho × 11 nichos = 55), e dentro de cada nicho
priorize `checklist_100k = CABE` antes de `CABE COM RECORTE`, depois território maior. Ordenar
só por território concentra nicho sem querer (na rodada 3 o topo virou beleza e figurinhas) e
ignora esforço de entrega. **O ranking é decisão nossa — o método não dá critério de ordenação.**
O critério primário da seleção é o **comando de decisão + senso crítico** (querem · demanda · ninguém vende); cota por nicho e território só **desempatam**. Nº de anúncios do território é proxy nosso, e ele diz que nº de anúncios [05:37:20] "isso daí não diz nada": se o topo do ranking for pool de curso/IA/Excel, releia — é o "mais do mesmo" que ele manda evitar.

**1. Volume — regra permanente: 55 a 60 concepções por leva.** Vale SEMPRE, minerando do zero
ou reaproveitando base que já existe (decisão do usuário, 18/09/2026). É a faixa que o método
recomenda ["Pesquisar 10-50 concepções"; aula 04:11 "eu recomendo que você faça a mineração de
cinquenta"], depois 1 a 3 modelagens por concepção [04:11] e 3 a 5 Obras de Arte no fim do
funil [06:24]. Não pergunte o volume — aplique. Só confirme se o usuário pedir número diferente. **Gate (`T2.13`):** nº de concepções entre 55 e 60 OU linha no ESTADO `dono aceitou N=<n> em DD/MM`; termos extras além de 3-7 só com aprovação do dono (registrada).

Base grande já minerada? **Não minere de novo.** Estreite a base existente para 55–60 pela cota
de nicho e siga. O resto fica em `proximas-levas`, com modelagem e checklist prontos.

---

## 1 · MINERAR — encontrar referência de concepção

Método: `low-ticket-metodo-mvt` §8.

**Registro no Hub** (não usamos planilha; o método de Heitor fala em "planilha de 4 colunas" → no nosso ambiente vira 1 registro em `concepcoes` de `ofertas.json`): URL da
Biblioteca → `biblioteca_url` · página de vendas → `pagina_vendas` (+ `print_pagina`) · concepção principal → `nome` (+ `concepcao_frase`) · elementos da concepção → `elementos` (campos do passo 2; preenchidos na etapa 2). O lote bruto de cada varredura pode ir em `MINERACAO/<rodada>/` só como rascunho; a verdade é o Hub. Nesta etapa é **só coletar** — não modelar. Para extrair criativos e anúncios de concorrentes da Biblioteca ao vivo: skill **`competitive-ads-extractor`** — invocar via Skill tool ao minerar, pra salvar um lote de criativos ativos como referência.

**Dois checks universais ao coletar (valem em TODA mineração, 22/09/2026):**
- **Conferir o LINK da oferta em cada criativo** — mesma página/anunciante pode vender ofertas
  diferentes; anotar qual link cada criativo aponta, pra não confundir uma oferta escalando com várias.
- **Seguidores do anunciante = sinal suave** (na mineração BR): muito seguidor = vende por marca
  pessoal/autoridade, mais difícil replicar → preferir player pequeno. NÃO elimina automático (o valor
  é o ângulo/mecanismo da concepção, não o tamanho do perfil). No **gate cross-market** vira corte DURO
  (≤10k), porque lá é quase-clone e marca pessoal não transfere.
- **Seguidores entram JÁ na varredura, não em passe separado** (R6, 24/09/2026: pane deixou 31 concepções
  PENDENTE "seguidores não conferidos" e precisou de 2º pane só pra isso). Ver "GATE DE ORIGEM — como medir".

**Minerar o FUNIL do concorrente — peça por peça (decisão da dona 09/10/2026).** A oferta já nasce com
bump, Upsell 1, Upsell 2 e downsell pensados, então a coleta tem de trazer **o que ele empilha depois da
compra**, não só o principal. Em `concorrencia-*.md`/`destrinchar-*.md`, por anunciante com link:

| Coluna | O que anotar |
|---|---|
| `bônus` | quantos, o que é, em qual plano entra |
| `order_bump` | quantos, texto, preço de cada + combo |
| `upsell/downsell` | o que aparece pós-compra, preço, tem 2ª chance? |
| `ferramenta_app` | **entrega que é FERRAMENTA** (calculadora, planilha que gera, template, app, assinatura) — e o que é GRÁTIS cobrindo a mesma promessa |
| `escada` | preço de entrada → bumps → topo (ex.: eletricista R$10→27→67; jiu-jitsu bumps R$9,90-12,90 / manual 17,90-27,90 / programa R$97) |

O bloco `entrega: por anunciante` que já existe nas rodadas 7 e 10 é exatamente isso — manter o padrão e
completar as colunas que faltarem. Saída alimenta `mvt-funil` (peças do funil) e o Hub (`notas`).
Ferramenta achada aqui é candidata a **Upsell** nosso (a "próxima dor" que ele resolve) — mas só se passar
da checagem de grátis (`mvt-modelar`).

**GATE DE ORIGEM — como medir (dono, 24/09/2026; vale mineração BR e cross-market):**
1. **Seguidores:** no card do anúncio, clicar no NOME do anunciante (abre a página dele dentro da
   Biblioteca) → aba **"Sobre"** → card **"Páginas e contas"**. Ali aparecem DOIS números: ícone
   Facebook ("2 mil seguidores • Site educacional") e ícone Instagram (@handle, "74,5 mil seguidores").
   **Vale o do INSTAGRAM.** Erro real R6: pane anotou 2 mil (Facebook) da Fluente com Legenda; o IG
   tinha 74,5 mil → NAO_PASSA. Nunca gravar número de Facebook no gate. Sem Instagram listado → anotar
   "sem IG" + o do Facebook, e marcar PENDENTE pra decisão.
2. **Tempo:** data de início mais antiga do criativo (card "Veiculação iniciada em").
3. **Contagem:** criativos DIFERENTES com o MESMO link de destino.
4. Veredito: PASSA se (1 criativo ≥~15 dias OU 3-5 ≥7 dias) + ≤10k IG + link conferido. Criativo único
   com ≥15 dias NÃO é NAO_PASSA por "poucos criativos". Link não achado NÃO é NAO_PASSA: vira ressalva
   `link PENDENTE` (ver regra no topo de GATES TRAVADOS).

**GATE DE DEMANDA — VIRAIS POR PLATAFORMA + COMENTÁRIO RECENTE (dono, 10/10/2026).**
A janela de 15/30 dias do GATE DE ORIGEM acima vale só pra **veiculação de anúncio** (o criativo tá
rodando agora?). **Demanda de conteúdo não tem prazo**: um vídeo viral de 2021 prova que a dor é
real, não que ela morreu. Por isso, ao validar dor no YouTube/TikTok/Reels/Instagram:

| Plataforma | Vídeo "viral" = dor validada |
|---|---|
| YouTube / Shorts | **≥100.000 views** (regra da dona: "100k mais ou menos") |
| TikTok | ≥1.000.000 views, ou ≥500k em canal de nicho |
| Instagram Reels | ≥100.000 views |
| Facebook | ≥500.000 views |

Três sinais juntos, não um só — **PASSA** exige os TRÊS:
1. **Vídeo(s) viral(is)** no threshold da plataforma acima (conte os vídeos: quantos passam).
2. **Comentário recente** na dor — de **até ~6 meses** (3 meses é o ideal). Comentário de 6 meses,
   3 meses, "mano", "tô com 4 anos de faixa" = a dor AINDA está real e ainda dói. Comentário antigo
   (>1 ano), sem nenhum recente, = dor podre.
3. **Volume de oferta** — **muitos vídeos falando disso** é sinal de oferta boa (concorrência prova
   demanda), não de mercado morto. Se tem 1 vídeo só e é viral, é outlier, não evidência.

NÃO exija recência do vídeo. NÃO descarte vídeo viral antigo. Só o que importa: **views + comentário
de dentro de ~6 meses + mais de um vídeo**. Video novo com 900 views não vale nada; video de 2021 com
300k views e comentário de两个月 atrás vale tudo.

**É esse gate que abre as PEÇAS DO FUNIL.** Dor validada por aqui vira order bump / upsell
(`mvt-funil`) — nunca invente bump de dor não validada: bump que não vende é só retrabalho.

**Palavras-chave — 5 famílias, cada uma com seu comando** (`references/prompts-e-exemplos.md` do método, Comandos 1-4). O Heitor manda buscar por: produto · formato · oferta · **persona** · **nicho e subnicho** [YT cpmkuup83VY; aula 02:27:19; YT -UTDJP5eSrc].

| Família | Comando | Quando entra |
|---|---|---|
| Formato + Valor/Oferta | **Comando 1** — lista COMPLETA: `ebook, checklist, planilha, pack, mini curso, templates, guia, áudio, mapa mental` + `barato, rápido, simples, em casa, exclusivo, imediato, download imediato, acesso vitalício, oferta limitada, resultado em X dias, passo a passo, prático` | **Sempre**, na varredura ampla, SEM nicho (`X` é placeholder vazio, não nicho fixo; "de início eu não recomendo você ter um nicho" [aula 02:28:00]) |
| Nicho/subnicho | **Comando 2** (nichos→subnichos→dor única→formato→título) e **Comando 3** (principais + long tail + termos de dor/desejo/objeção + formatos + ganchos emocionais e intenção de compra) | Quando a rodada JÁ tem nicho (R4/R5/cross) ou o Comando 1 saturou. Combine `formato × subnicho` (ex.: "planilha hipertrofia" [YT -UTDJP5eSrc]) |
| **Persona** | **Comando 4** (dores, desejos, pensamentos internos de cada, 10 palavras por dor e por desejo) | Quando a rodada tem persona/público alvo e sempre que um subnicho for estreitado. Palavras de dor/desejo/pensamento interno vão direto na Biblioteca |

Meta: 10 a 50 concepções (o Heitor recomenda 50). **Cota por termo:** ao vivo ele tirou ~6 concepções de UM termo (`download imediato`) [02:53:01] "encontramos 6 concepções" e 7 no total em menos de 30 minutos [02:54:57] "encontramos aqui sete concepções em menos de 30 minutos"; o short do YT [cpmkuup83VY] fala em 1-3. Referência da aula: ~6 por termo; **na nossa operação a cota é PARADA (ver GATES · passo 1)**, não sugestão. Os 100–150 cards e os 3–7 termos da tabela "Volume e cota por termo" são regra NOSSA declarada, não dele.
Registre no arquivo da rodada, por termo: família (formato/oferta/nicho/persona/produto), comando de origem e nº de concepções. Se rodou só o Comando 1, escreva "famílias nicho/persona não rodadas" — escolha declarada, não falha.

**Achar território por VÍDEO, não só Biblioteca (22/09/2026).** Pra um tema/produto, brainstormar
**10 termos de busca** e jogar no YouTube / TikTok / Shorts — onde o tema tem vídeo, tem público e
demanda viva. Serve pra descobrir território e ângulos que a Biblioteca sozinha não mostra. **Vale BR
TAMBÉM, não só cross-market** — os 10 termos forçam mais formas de buscar o mesmo tema (ângulos que
não vêm de cara). **No cross-market: buscar no IDIOMA do destino, e a tradução NÃO é literal** — achar
como o nativo fala aquilo (gíria, termo de mercado real), não o Google Tradutor. Ex: o termo que o
americano digita pode não ser a tradução direta do termo BR. Os 10 termos viram também os termos-gancho
de medição de demanda.

**Vídeo VELHO com muitas views = público ainda forte (não corta por idade).** Vídeo de 2014/2015 com
muita visualização = audiência durável, evergreen — demanda que não morreu. Mesma lógica do gate
(idade do post não elimina). **Cruzar a leitura de demanda com Google Trends + YouTube (trends/busca) +
busca no Google** — nenhuma fonte sozinha decide; o conjunto (Biblioteca + vídeo viral + views de vídeo
antigo + Trends + Google) forma a lógica de que o tema vende e tem gente querendo comprar agora.

**Onde pescar (o Heitor lista 4 lugares, não só a Biblioteca)** [YT -UTDJP5eSrc]: (1) Biblioteca de Anúncios; (2) ferramentas de espionagem (Guru Killer, ED Miner — puxam a Biblioteca com mais dado), extensão **Spar** (filtra as páginas com mais anúncios) e **SpyX** (extensão da dona, registrada 30/10/2026 — ao abrir um anúncio na Biblioteca, extrai metadado estruturado direto: curtidas da página, dias no ar, criativos duplicados, nº de anúncios do anunciante na busca, plataformas, CTA, link de destino; também dá a **transcrição do vídeo** do criativo sob pedido — usar como fonte de transcrição em vez de rodar Whisper manual quando o anúncio já foi puxado por ela); (3) **YouTube**: vídeos mais vistos + comentários, com as MESMAS palavras das 5 famílias; (4) **ChatGPT** para persona/dores/desejos/pensamentos internos. Volume de busca de uma palavra: **Uber Suggest** (3 buscas grátis/dia) e Google Trends [YT e7MDJ2OgMNE].

**Prompt de modelagem via SpyX (dona, 30/10/2026) — já é a metodologia da casa, fonte única `4-alavancas.md` +
`virar-o-lead.md`:** quando a dona manda o dado estruturado do SpyX pra modelar um anúncio achado, o fluxo é:
(a) abrir o link de destino de verdade e ler a página inteira (checklist de extração do `virar-o-lead.md`);
(b) virar o lead por etapa (anúncio→página→checkout), 6 perguntas fixas; (c) nota 0-10 por alavanca
(`4-alavancas.md`) + a mais fraca; (d) brechas a explorar a partir das objeções do passo (b); (e) montar a
oferta modelada puxando as 4 alavancas, cada item marcado com a alavanca que move; (f) ganchos/roteiros de
criativo, cada um marcado com a alavanca atacada; (g) **nunca analisar o criativo (vídeo/imagem) sem a dona
mandar** — pede a transcrição (via SpyX) ou a imagem antes de analisar gancho/ângulo/prova/CTA, nunca inventa.
**Pra cross-market (outro idioma/mercado), roda em 2 ETAPAS, nunca junta:** Etapa 1 só diagnóstico — a dor é
UNIVERSAL ou depende do país de origem (cultura, religião, sistema escolar, datas, leis, moeda, referências
locais)? nota 0-10 por MERCADO candidato (não só por alavanca), marca 🔥 os de potencial forte, lista o que não
se traduz e os riscos (concorrência, saturação, política de anúncio). **PARA e pergunta pra qual mercado
modelar — espera a confirmação da dona antes de começar a Etapa 2 (modelagem).** Esse gate de pausa evita
modelar o mercado errado antes de validar a tese.

> ⚠️ **GOOGLE TRENDS = PERFIL `trends` (9234), NO BROWSER, HEADED. NUNCA POR HTTP.** Duas rodadas de
> pesquisa (Elétrica e Jiu Jitsu, 10/10/2026) pediram volume no Trends e voltaram com **HTTP 429** em
> todas as tentativas, **0 número medido** — porque mediram por WebFetch/curl anônimo. **Não caia no
> HTTP "só pra tentar"**: é aí que a rodada morre. Se o browser também bloquear, reporte "sem dado" e
> siga com Uber Suggest + Ad Library — mas **avise que o volume ficou sem medir**, nunca troque por
> estimativa silenciosa. Mecânica: `mvt-validar` › "Mecânica — Trends e YouTube".
Rotas que não são palavra: **experiência do dia a dia/brainstorm** ("barbearia → dores e desejos dos tatuadores" [YT -UTDJP5eSrc]), **calendário** (volta às aulas, Dia das Mães, concurso abrindo — "pega uma data" [YT Onp18JH6HL8]) e **referência de produto físico, curso ou lançamento** ("a gente olha para qualquer coisa e cria a concepção" [YT cpmkuup83VY]) — a concepção vale mesmo quando o produto não é digital. **Registre a rota de cada concepção** no campo `origem_referencia` da concepção no Hub (coluna "origem da referência" do método): mineração (família/termo) · dia a dia · calendário · produto físico/curso/lançamento [YT 2hSIIWKZlBs: referência vem "da mineração ou das suas experiências no dia a dia"].

**O critério de entrada é um só, e é qualitativo** [aula 02:43]: *"você precisa bater o olho
e entender: cara, eu consigo transformar isso aqui em uma coisa pronta? eu consigo adaptar isso
aqui à metodologia?"* Não é sobre o anunciante ir bem — é sobre a ideia dele servir de matéria
prima. *"Eu não preciso encontrar algo que está dentro da metodologia, eu preciso transformar
isso para a metodologia"* [02:42].

**Checklist 100k** — as 8 perguntas, aplicadas à versão que a gente vai modelar, não ao card:
consigo vender numa página de vendas? · vendo para quem já está no mercado? · encaixa nas 10
características? · formato escalável? · consigo vender pela faixa da rodada? · consigo
transformar em algo que as pessoas **querem**? · consigo aplicar modelagem? · consigo trazer
vantagem?

Ele passa cada achado por este checklist **antes** de a concepção entrar no Hub (`concepcoes`) [aula 02:32:21]. Aqui isso serve para **classificar** (CABE / CABE COM RECORTE), não para descartar: "nada com potencial é descartado" continua valendo. A pergunta "vendo para quem já está no mercado" é o **nível de consciência**; anote o nível junto (Hub `concepcoes.nivel_consciencia`; resultado do checklist em `checklist_100k`).

Regra que muda tudo [aula 02:39]: *"esse checklist não significa que a concepção que eu encontrei
tem que cumprir tudo. Significa que eu tenho que tentar **trazer ela** para esses objetivos."*
Exemplo dele: curso de bordado industrial → "20 modelos prontos de bordado comercial".

**Nosso entregável NÃO é só PDF** (decisão do usuário, 18/09/2026). Com Claude a gente constrói
app web com back-end, então "vira arquivo pronto?" é pergunta curta demais. A pergunta certa é:
**vira produto pronto que a pessoa usa sozinha?** Formatos válidos aqui:

| Formato | Quando escolher |
|---|---|
| PDF / pack / planilha | conteúdo que a pessoa consome ou imprime |
| **App web / ferramenta** | quando o valor está em CALCULAR, PREENCHER, ACOMPANHAR ou GERAR — calculadora de precificação, planilha que se preenche sozinha, gerador de documento, painel de acompanhamento, quiz de diagnóstico |
| Área de membros | quando há atualização recorrente |

**Todo formato é visual, palpável e demonstrável — inclusive app/microSaaS (22/09/2026).** PDF, mapa
mental, microSaaS, webapp: todos dão pra gravar criativo demonstrativo (passar por dentro, mostrar
funcionando). App NÃO é menos tangível que PDF — é mais, porque a pessoa VÊ resolvendo na tela.
**Preferir webapp a planilha quando resolve o mesmo problema de forma mais simples e mais visual** — em
vez de entregar planilha, entregar a ferramenta que faz aquilo sozinha, mais fácil de usar e mais visual
que a planilha. A planilha vira a versão pobre do que um app faz melhor. Só fica no PDF/planilha quando
o valor é consumir/imprimir conteúdo; quando é usar (calcular, preencher, acompanhar, gerar) → app.

**Ressalva — depende do PÚBLICO, não é padrão fixo** (Heitor, YT `2hSIIWKZlBs` ~17:00): "a onda agora
é vender aplicativo? Será que aquele público quer mesmo um aplicativo, ou quer um ebook simples que vai
baixar e imprimir?" — o estudante da Bíblia é acostumado a material físico/PDF e não quer app difícil,
então lá o ebook ganhou. Antes de escolher app, pergunte: **esse público usa ferramenta digital no dia a
dia, ou baixa/imprime?** Público pouco digital, mais velho, que imprime (igreja, professora, artesanato,
idoso) → PDF/ebook visual. Público que já vive na tela e o valor é calcular/gerar → app. Na dúvida,
olhe o formato que já vende naquele público (Biblioteca/comentários) e só troque o formato se a troca
servir a ele, nunca "pra deixar mais bonito".

Isso muda dois crivos do checklist:
- **"formato escalável"**: app entrega uma vez e serve infinitos compradores — é tão escalável
  quanto PDF, às vezes mais.
- **"NÃO CABE por não virar arquivo"** deixa de valer sozinho. Concepção que exigia preencher,
  calcular ou acompanhar era descartada como "só serve com acompanhamento" — agora vira
  ferramenta. Antes de marcar NÃO CABE, pergunte: dá para virar app?

O que continua NÃO CABENDO: valor que depende de **pessoa** (mentoria, consultoria, correção
individual, aula ao vivo), de presença física, ou de hardware/serviço de terceiro.

**Efeito no preço:** app ou ferramenta sustenta ticket acima da faixa base (R$17,90/R$27,90) —
entrega mais, percepção de valor maior, mais difícil de clonar. Mas isso é decisão da **etapa 5**,
escrita no campo `sustenta_preco`, nunca critério de mineração ou de modelagem.

Registre o veredito do checklist no Hub, concepção por concepção, em `checklist_100k`:
`CABE` · `CABE COM RECORTE` (escreva qual recorte) · `NAO CABE` (escreva por quê — em geral:
só entrega valor com mentoria, acompanhamento, aula ao vivo ou presencial; não vira arquivo).
Nada é apagado: o "não cabe" fica registrado com a razão e pode ser revisto depois.

**Volume de anúncios e tempo rodando NÃO entram — nem como sinal positivo, nem como negativo.** Aula: [05:37:20] "isso daí não diz nada" — neutro. "Muito rodando = erro nº1" vale para a CONCEPÇÃO populada (mais do mesmo), não para o nº de anúncios de uma oferta como sinal.
- [aula 02:19] "quantidade de anúncios ativos — **não precisa**; tempo que a oferta está
  rodando — **não precisa**. Faz o básico."
- [aula 02:48] o item "mais de 5 anúncios ativos, rodando há 2 dias" existia no checklist e ele
  **tirou ao vivo**: "não vai entrar no nosso crivo mais… confunde mais do que ajuda".
- [aula 05:36] "modelar oferta que não está escalada é risco? **isso daí é crença**… a
  quantidade de anúncios eu não me importo… **isso daí não diz nada**."
- [aula 02:16] "prefere modelar oferta escalada ou tanto faz? **Tanto faz.** O jogo é a concepção."
- No MATERIAL-FRAMEWORK, "Encontra um produto que já está vendendo e com muitos anúncios ativos"
  está em caixa **vermelha**, na coluna **"O QUE O MERCADO TE ENSINA"** — é o erro que ele
  critica, pareado com "Vendo algo que as pessoas querem, tem demanda e não tem ninguém vendendo"
  na coluna "MEU JOGO". E "já tem milhares / muitas pessoas rodando" é o **erro nº1 "NA
  CONCEPÇÃO"** dos 8 erros. (Verificado pelas coordenadas e cores do JSON do Whimsical, 18/09/2026
  — o export `.txt` cola painéis diferentes e já nos induziu ao erro oposto.)
- Contradição registrada, não resolvida: em [01:56] minerando ao vivo ele olha a biblioteca de um
  anunciante e diz "37 anúncios, tá vendendo, esse cara tá tendo resultado", e lê a data "2 de
  julho de 2024 — deve tá vendendo bem". É narração de tela, não regra. Não use como crivo.

**A direção de ouro** [MATERIAL-FRAMEWORK, painel FLUXO DE EXECUÇÃO]: a concepção tem que ser uma
em que **as pessoas querem · tem demanda · não tem ninguém vendendo**.

**O que NÃO é motivo de deixar um card de fora** (erro real 2026-09-16: um worker
registrou 2 concepções em 160 cards, virou 38 depois da correção): preço alto ou baixo ·
mercado populado · repetição de outro termo · curso, serviço ou expert · papelaria,
esotérico, religioso, PLR · livro físico com conteúdo aproveitável · falta de preço no card
(aí abre a página; se não achar, fica como pendência). Só fica de fora o que não tem
concepção de produto: SaaS/app, físico sem conteúdo **como produto a copiar** (como REFERÊNCIA de concepção ele entra — Heitor: "olhando para produtos físicos, cursos, lançamentos" [YT cpmkuup83VY]), serviço local, anúncio sem produto —
sempre com o motivo escrito.

**Toda concepção sai da mineração com os DOIS links** (regra do usuário, 2026-09-17 e
reafirmada 18/09) — e o motivo da página não é registro, é uso: **se a concepção for validada,
aquela página é o modelo de estrutura e copy para montar a nossa** (modelar, nunca copiar).
Página sai do ar, muda preço, troca de oferta: sem a cópia salva, a referência some.

o anúncio na Biblioteca (`facebook.com/ads/library/?id=<ID>`) e a página de vendas
(decodificar o `u=` do `l.facebook.com`, abrir, anotar preço e o que entrega, printar).
Os dois vão para o registro no Hub (`biblioteca_url`, `pagina_vendas`,
`print_pagina`) — o painel mostra os dois no cartão. Concepção sem link DA BIBLIOTECA não pode existir. Link da PÁGINA é diferente: se não achar (fora do ar, WhatsApp, pane não achou), registre `PENDENTE` com motivo e data e a concepção segue normal;
se a página estiver fora do ar, registre "fora do ar" com a data e mantenha o link da
Biblioteca.

**Custo diferente, momento diferente** (regra do usuário, 18/09/2026):

| Item | Quando | Por quê |
|---|---|---|
| **ID + URL da Biblioteca** | na varredura, sempre | já vem no card, custo zero |
| **URL da página de vendas** | na varredura, sempre | o `a[href*="l.php"]` está no DOM do card; é scrape, não visita — barato, e depois é caro de recuperar |
| **Print da página + preço** | **só na leva que avança** | exige abrir a página uma a uma, ~8s cada; em 243 concepções são horas |

Ou seja: **link é sempre, print é só para quem vai seguir.** O que estiver sem print e sem preço
fica com a pendência anotada e a URL salva — se a concepção subir de leva depois, o print sai
nessa hora. Erro real 18/09: 55 concepções ficaram com URL e sem print, e eu tratei isso como
buraco grave quando é o comportamento correto para quem não está na leva.

**Guarde a página de vendas de toda concepção aberta** (regra do usuário, 2026-09-17):
URL completa em `concepcoes.pagina_vendas` + screenshot full-page em `MINERACAO/<rodada>/paginas-referencia/<slug>.png` (caminho/data em `print_pagina` e `pagina_capturada_em`)
(`agent-browser --session <perfil> screenshot <arquivo>`), com a data da captura. Página sai do
ar, muda preço ou troca de oferta — sem a cópia, a referência some. Se a concepção for validada
depois, essa página é a inspiração de estrutura/copy na hora de montar a nossa (modelar, nunca copiar).

**Volume e cota por termo** (regra do usuário, 18/09/2026 — calibrada com os números da rodada 3):

| Parâmetro | Valor | De onde vem |
|---|---|---|
| Cards por termo | **100 a 150** | abaixo disso só aparecem os maiores anunciantes; acima começa a repetir |
| Termos por rodada | **3 a 7**, de formato/oferta | `checklist`, `pack`, `templates`, `planilha`, `acesso vitalício`, `oferta limitada`, `direito de revenda` |
| **Cota de concepções POR TERMO** | **~6 = PARADA** (aula [02:53:01] tirou ~6 por termo; nossa: cota total ÷ nº de termos, bateu → para) | evita que um termo domine a rodada |
| Taxa de aproveitamento medida | **~1 concepção a cada 6 cards** (17%) | 1.422 cards → 243 concepções na R3 |

**Cota por termo, não por rodada.** Termo diferente entrega mercado diferente: `checklist` traz
profissional, `pack` traz artes digitais, `templates` traz Canva e papelaria, `acesso vitalício`
traz curso para reciclar, `direito de revenda` traz PLR. Sem cota, o termo mais abundante domina:
na R3 o `templates` deu 325 cards contra 153 do `checklist`, e a base saiu enviesada.

Bateu a cota do termo → **pare e vá para o próximo**, mesmo com card bom rolando. O excedente fica
no `raw-<termo>.json` e alimenta a próxima leva sem minerar de novo.

**Escreva a cota no prompt do pane como PARADA, não como referência.** R6: prompt dizia "~6 por termo,
sem teto rígido" e o pane voltou 71 concepções de 3 termos (~24/termo) — base inflada, o erro que
motivou o reset de 22/09. Diga: "bateu ~6 no termo → para e vai pro próximo".

**Termo seco:** não chegou na cota depois de ~150 cards, não force — registre quantas deu e
redistribua o que faltou entre os outros. Termo seco é informação sobre o mercado, não falha.

**Sinal de saturação:** 30 cards seguidos sem concepção nova = aquele termo já deu o que tinha.

**Não minere demais.** Na R3 fizemos 1.422 cards para uma meta de 60 concepções — 4x mais que o
necessário. Sobraram 184 concepções paradas e 125 sem território medido: trabalho feito e não
usado. O caro não é minerar, é aprofundar; base inflada só empurra custo para a frente.

Salve sempre os cards crus em `MINERACAO/<rodada>/raw-<termo>.json` — sem eles não dá para revisar
um corte sem minerar de novo, e é de lá que sai a próxima leva.

**Antes de aceitar um zero, confira se a BUSCA ACONTECEU** (descoberto 18/09/2026). O falso-zero
da Biblioteca tem uma assinatura: a página carrega, a categoria aparece certa ("Todos os anúncios",
que o `ad_type=all` da URL já seleciona sozinho — não precisa marcar na mão), mas **o campo de
busca volta VAZIO**: a Meta descartou o `q=`. Isso não é "nenhum anúncio corresponde", é busca que
nunca rodou.

```js
(function(){var i=document.querySelector('input[type=search], input[placeholder*="alavra"], input[placeholder*="eyword"]');
var t=document.body.innerText; var m=t.match(/~?[\d.,]+\s*(resultados|results)/i);
return JSON.stringify({q: i?i.value:null, contador: m?m[0]:null});})()
```

- `q` vazio → falha, não zero. Recarrega; repetiu, é throttle: pare.
- `q` com o termo e contador nulo → zero de verdade (ainda assim, 4 tentativas antes de gravar).

Vale também para a query de controle, e é mais confiável que contar tentativas.

**Zero/pouco resultado não é resposta:** a Biblioteca devolve zero falso intermitente
(mesma URL alterna entre ~26.000 e "Nenhum anúncio corresponde") e zera a contagem quando a
UI vem em inglês. Recarregue até 3x com 15 s e troque de perfil antes de concluir vazio;
receitas em `~/.claude/browser-workspace/domain-skills/facebook.com/`.

### Mecânica — Biblioteca de Anúncios

Perfis sem login: `adslib` (9232), `adslib2` (9235), `adslib3` (9236), `adslib4` (9237).
**Máx. 1-2 panes simultâneos na Biblioteca** (throttle por IP; ver `## GATE 1` e PROMPT-PADRÃO). Os 4 perfis existem pra rodízio, não pra rodar todos juntos.

**Toda busca na Biblioteca e toda validação de demanda são conduzidas por panes Sonnet com o
navegador VISÍVEL — nunca por script** (regra do usuário, 18/09/2026). Vale para a medição de
comunicação/território, para a mineração e para Trends e YouTube. Script em background só se o
usuário pedir; sem isso, "não funciona direito".

**Divida a fila em panes Sonnet, MÁX. 1-2 ao mesmo tempo na Biblioteca** (Trends/YouTube/TikTok não têm o throttle da Meta e podem ir em paralelo), um perfil por pane, em rodízio — `adslib` (9232),
`adslib2` (9235), `adslib3` (9236), `adslib4` (9237), `trends` (9234). Cada pane recebe seu
pedaço da fila (`split -n l/2 -d fila.txt fila-p` — 2 pedaços; mais fatias só rodam em sequência, nunca mais de 1-2 na Biblioteca de uma vez) e grava seu próprio `.jsonl`; o orquestrador
consolida no fim. Paralelizar assim (dentro do teto de 1-2) é o jeito certo de ganhar tempo — nunca voltando pro script.

**Pane de medição reporta por EVENTO, não por item** (18/09/2026). No prompt, diga: avise só
(1) no fim do lote, com o resumo — quantas mediu, quantas zeraram, quais vieram com número alto;
(2) se o controle falhar ou o campo de busca voltar vazio, dizendo em qual ID parou; (3) se
aparecer algo que precise de decisão. Zero é o resultado ESPERADO numa comunicação modelada, então
"mais um zero" não é evento. Sem isso o pane reporta query a query e consome o contexto do
orquestrador sem informação nova — especialmente ruim com várias frentes em paralelo.

**Escreva a proibição no prompt do pane**, senão ele reinventa o script sozinho: já aconteceu
um pane despachar dois lotes em background por conta própria depois de receber a fila. O prompt
tem que dizer: proibido script, nohup, lote paralelo ou qualquer coisa que meça sozinha; se o
ritmo virar problema, ele REPORTA quantas queries por hora consegue em vez de mudar de método.
O que continua valendo, e vai no prompt do pane: zero só é aceito após 4 tentativas limpas
(com o campo `tentativas` gravado) · query de controle a cada ~12 buscas (`emagrecer`, tem que
dar ~42.000; zerou = motor quebrado, descarte tudo desde o último controle bom) · o regex do
contador precisa aceitar `results` além de `resultados`, senão UI em inglês vira zero falso ·
throttle da Meta é por VOLUME acumulado no IP, não por nº de perfis, então ~30 queries por
perfil e intervalo. Script em background só se o usuário pedir.

**FECHE O PERFIL AO TERMINAR** (regra do usuário, 18/09/2026). Todo pane que usa browser —
Biblioteca da Meta, YouTube, Google Trends, TikTok — fecha o perfil quando acaba a sua parte, e
avisa o orquestrador que liberou. Escreva isso no prompt do pane.

```fish
pkill -f "user-data-dir=$HOME/.agent-profiles/<perfil>"   # ou feche a janela
```

Por quê: perfil é recurso compartilhado e **invadir perfil ocupado não dá erro nenhum** — a aba é
a mesma, e o pane seguinte lê na tela o resultado da busca do anterior achando que é o dele.
Aconteceu duas vezes em 18/09: dois processos no `adslib` (medições descartadas) e o perfil
`tiktok` com um pane esperando enquanto outro usava. Perfil aberto e ocioso também segura a vez
de quem está na fila.

**Colisão acontece até sem você querer (R6, 24/09/2026):** um `pane_spawn` recusado pelo usuário ABRIU
o pane mesmo assim (pane-2838), que pegou o `adslib` já em uso por outro pane. Sintoma: "a URL da aba
mudou sozinha entre duas leituras". Regra: antes de reusar perfil, confira em `pane_list` se não há pane
órfão nele; ao ver o sintoma, o pane PARA e reporta (não navega mais) e o orquestrador fecha o duplicado
SEM `pkill` no perfil (derrubaria o dono legítimo). Mantenha no ESTADO a tabela pane → perfil.

Quem fica de pé o dia todo é só o que o orquestrador usa para conferência pontual. Perfil de
trabalho de pane: sobe, usa, fecha, avisa.

**Navegador SEMPRE visível — nunca headless.** Vale para toda etapa do MVT que toca browser
(mineração, validação, abrir página de oferta) e também para pane delegado: escreva a regra no
prompt do pane. Use só os perfis Chromium do sistema, que já sobem com janela; nunca
`agent-browser open` puro nem flag headless. Motivo prático além do pedido do usuário: sessão sem
interação humana recebe shell vazio / checkpoint da Meta, e com a tela à vista você VÊ o captcha
ou o pedido de login em vez de gravar zero falso.

```fish
~/.claude/bin/browsers.sh adslib adslib2
agent-browser --session adslib open "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=BR&q=<TERMO>&search_type=keyword_unordered&media_type=all"
```

- Vá pela URL, não pelo formulário. `country=ES`/`US`/`MX` para ofertas em espanhol ou
  inglês — o método aceita as três línguas.
- "Entrar" no topo é falso positivo de login.
- Rolagem: `open` + `sleep 8` + ciclos de `scroll down 2500` / `sleep 2.5`. Se a
  contagem de IDs travar em ~30, clique em **"Ver mais"**
  (`agent-browser --session <perfil> find text 'Ver mais' click`, espera 4 s).
- Extração card a card, regex de campos e armadilha do JSON duplamente codificado:
  `~/.claude/browser-workspace/domain-skills/facebook.com/biblioteca-anuncios-varredura-profunda.md`.

| Dado | Como pegar |
|---|---|
| ID | `Identificação da biblioteca: <número>` |
| URL do anúncio | `facebook.com/ads/library/?id=<ID>` |
| Página de vendas | link `l.facebook.com/l.php?u=<URL-ENCODED>` → decodifique `u=` e abra no mesmo perfil |
| Texto do anúncio | texto do card (serve para entender a concepção quando não há página) |

Registre cada concepção salva no Hub com `status: "ideia"`.

**Preço NUNCA é critério de descarte, nem de corte, nem de classificação.** Nem preço alto,
nem preço baixo, nem "distância grande até o ticket que a gente quer". O valor da NOSSA oferta
é decisão do usuário, tomada depois, sobre a direção escolhida — não é régua de mineração nem
de modelagem. O preço do concorrente entra só como informação registrada.

Erro real 2026-09-18: rotulei as concepções em "modo A / modo B" por faixa de preço e escrevi
isso nos prompts dos panes; um worker descartou uma concepção por "distância de 30x até R$37".
Rótulo inventado virou filtro. Se precisar anotar que uma concepção barata exigiria entrega
maior para sustentar um preço maior, isso é observação da ETAPA 5 (Obra de Arte, campo
`sustenta_preco`) — nunca da 1, 3 ou 4.

Descarte só por motivo de método, escrito: travou, opções todas mais-ou-menos, complexo demais
de entregar, criativo demonstrativo impraticável, sem dor/desejo clara.

**O que o método diz** (transcrição do workshop de 11h, conferida 18/09/2026):

- `01:22:16` "Eu não quero saber o que a pessoa está entregando, não quero saber a página de
  vendas, nada. Concepção eu faço exatamente assim."
- `01:35:29` "eu não olhei a página de vendas, eu não vi como que a pessoa tá vendendo e eu não
  olhei os bônus, não olhei nada — por isso que eu falo, a biblioteca de anúncio é o ouro"
- `02:30:18` "não fica agarrado no preço… você vai vender R$17,90, R$27,90, depende da concepção"
- `05:29:56` "o valor de venda já está definido, é 17,90 o plano básico, 27,90 o plano completo"

Preço não é nenhum dos 9 elementos, e não existe item de preço no checklist de mineração dele.
O preço do concorrente NUNCA entra na decisão — a gente registra porque o usuário pediu os dois
links e o print, como acervo de referência, não como critério.

A ÚNICA pergunta de preço válida na triagem é sobre o NOSSO preço, e só quando ele já está
definido: "dá pra vender ISSO por esse valor?" (`02:36:21` "A gente consegue vender por R$ 17,90
e R$ 27,90? Beleza."). É teste de viabilidade da concepção, nunca comparação com o anunciante.

Ele também **removeu ao vivo** o crivo de "mais de 5 anúncios ativos, rodando há 2 dias"
(`02:48:30`: "eu vou até tirar isso aqui… não precisa ter anúncio ativo"). Volume de anúncios e
tempo rodando não entram no checklist 100k.

**Como o preço entra nesta operação** (decisão do usuário, 18/09/2026):

1. **Nunca descartar concepção pelo preço que o anunciante pratica.** Lista tudo, sempre.
   Na modelagem a concepção pode ser trazida para a NOSSA faixa — a modelagem é justamente o
   que resolve isso. Preço do outro não elimina ninguém.
2. **Nosso preço padrão mínimo é R$17,90 / R$27,90** (a dupla oferta do método). É o piso de
   referência, não um alvo que filtra a busca.
3. **Corte por preço, se existir, é passo separado e posterior**: só depois de TODAS as
   concepções modeladas, e só se o usuário pedir ("agora vamos focar nas que dão pra vender
   por X"). Nunca durante mineração ou modelagem, nunca por iniciativa própria.
4. **Anotar o preço da página sempre que der** — é referência valiosa. Anunciante vendendo a
   R$67 enquanto a gente vende a R$27 é sinal ótimo: a vantagem de preço já está dada e
   economiza verificação depois.
5. **Ausência de preço não impacta nada.** Não bloqueia, não rebaixa, não adia. Registre
   "sem preço exposto (data)" e siga — mas vale tentar achar antes de desistir.

**DOMÍNIO NÃO DIZ O QUE O PRODUTO É — abra a página antes de afirmar.** Erro real 18/09/2026:
vi destinos em `lovable.app` e `vercel.app` e concluí que os concorrentes do nicho cristão
"já vendem app". Abri as três: **zero campo de input, sem login, com checkout** — são landing
pages de PDF hospedadas em plataforma de vibecoding. Lovable, Vercel, Netlify, Replit e afins são
HOSPEDAGEM; o domínio não prova produto interativo.

Como verificar em uma chamada, antes de tratar concorrente como app:
```js
(function(){var t=document.body.innerText;
return JSON.stringify({inputs:document.querySelectorAll('input,select,textarea').length,
temLogin:/entrar|login|minha conta|senha/i.test(t), temCheckout:/comprar|checkout|R\$/i.test(t)});})()
```
`inputs: 0` + checkout = página de vendas. App de verdade tem campo para preencher, ou login, ou
estado que persiste. Vale a mesma régua para julgar o que a CONCORRÊNCIA entrega e para decidir
se o nosso combo com ferramenta é de fato um diferencial naquele mercado.

**Concepção sem preço continua no jogo** (regra do usuário, 2026-09-17): página que não
expõe valor (checkout só depois do clique, cadastro, WhatsApp) entra na modelagem igual às
outras — o preço é informação, nunca filtro. Registre "sem preço exposto (data)" e siga; o
valor da nossa oferta é decisão nossa (faixa do método), não cópia do concorrente.

### Mecânica — fechar link e preço em lote (scripts)

**Quem roda: um pane Sonnet de script despachado pelo orquestrador (não o pane que varre a Biblioteca)** — e **durante a mineração**, não depois.
Fluxo por termo: o pane varre e devolve o lote com os IDs (que entra em `concepcoes.biblioteca_ids`) → o orquestrador roda os
dois scripts abaixo em background para os IDs daquele termo → só então a concepção está
completa (dois links + preço + print). Deixar para o fim gera o retrabalho de 2026-09-17
(150 concepções sem link e sem preço, uma de cada vez depois).

Worker não dá conta de abrir 150 páginas a mão (um pane travou nisso em 2026-09-17).
Os dois passos são script, rodando em background com `nohup`, um anúncio/página por vez. **Exceção declarada à regra "nunca script" — decisão do dono 24/09/2026 (nohup continua)** (que é para MEDIR comunicação/território): estes scripts só leem link e preço; rodam pelo ORQUESTRADOR, em perfil de janela visível, e contam como 1 dos máx. 1-2 usos simultâneos da Biblioteca (`destino-anuncio.sh`). Se o dono não quiser script aqui, faz-se por pane visível:

```fish
# 1. link de destino de cada anúncio (lista `codigo|id_biblioteca`)
bash MINERACAO/scripts/destino-anuncio.sh adslib3 ids.txt destinos.jsonl
# 2. preço + print de cada página (lista `codigo|url`)
bash MINERACAO/scripts/preco-pagina.sh adslib4 urls.txt precos.jsonl paginas-referencia
```

- **`destino-anuncio.sh`**: abre `ads/library/?id=<ID>`, acha o bloco do anúncio pelo
  próprio ID e lê o `a[href*="l.php"]` de dentro dele, decodificando o `u=`. O link ESTÁ no
  DOM — não precisa clicar no CTA. Pegar o primeiro `l.php` da página inteira traz o anúncio
  errado (a página mostra outros anúncios); filtrar pelo bloco do ID é o que dá precisão.
- **`preco-pagina.sh`**: abre a URL, extrai por regex `R$ / US$ / 12x de R$` do `innerText`
  e salva screenshot em `paginas-referencia/<codigo>.png`.
- Ritmo: ~8 s por item (sleep 7-8 + eval). 150 itens ≈ 20-25 min. Rode em background e
  espere com `until ! pgrep -f <script>; do sleep 10; done` — nunca fique dando poll.
- Destino que não é site (wa.me, api.whatsapp, instagram.com) vira `destino_tipo` no Hub: a
  referência ali é o próprio anúncio, não existe página para modelar.

### ⏸ Parada 1
Formato obrigatório: `FORMATO DAS PARADAS` (ROTEADOR) + GATE 1 — tabela com concepção · formato · mecanismo · público · os 2 links + print (ou PENDENTE) · por que passa no checklist 100k. Recomende quais seguem para destrinchar/modelar e
espere. (O método destrincha **todas**; deixar alguma de fora só por decisão EXPLÍCITA do dono, registrada no ESTADO com data.)

---

## Modo D — oferta-first (rastreadores)  [ex-ADENDO §E]

## E · Método 2 de mineração — OFERTA-FIRST (rastreadores, fora da busca por termo)
Método 1 (nosso padrão) = território-first: concepção → mede vaga na Biblioteca. Método 2 =
oferta-first: acha 1 oferta que JÁ escala por rastreador externo → aplica uma saída do leilão (A) →
**só então volta pro gate padrão**. Ferramentas (todas terminam confirmando na Biblioteca):
- **urlscan / RL Scan** (grátis) — lista ofertas escaladas pelo parâmetro de tracking (`utmify`).
  Pega página + checkout (Hotmart/Cakto/Kirvano).
- **Reclamação como sinal de venda** — Reclame Aqui (BR) + equivalente Hotmart Global + ReclameKI.
  Reclamação RECENTE = oferta vendendo; **data da reclamação = há quanto tempo escala**.
- **SEMrush → Tráfego e Mercado** (trial 7 dias; $289/mo) — cola link da PLATAFORMA de checkout
  (Kirvano/PerfectPay/Cakto) → origens de tráfego (páginas das ofertas) + principais páginas
  (checkouts mais acessados = ofertas TOP da plataforma).
- **sitemap.xml** no fim da slug → funil inteiro exposto (pg01, upsell, opcel); ordena por data.
- **Termos-gancho por nicho** na Biblioteca — com aspas (frase exata) vs sem (ampla); filtra recentes.
- Ferramentas de estudo: Go Full Page (print da página), Video DownloadHelper (baixa VSL) — só para
  ESTUDAR copy, nunca clonar.
**Ressalva de fidelidade:** esses canais miram VSL/high-ticket/prosperidade/gringa; o "tem reclamação
logo vende" é o critério DELES. Pro nosso low-ticket o veredito final continua sendo o gate de 4
camadas. Método 2 só SEMEIA candidatos provados; Método 1 mede a vaga. Não competem — o forte é 1+2.
Quando usar cada um: M1 pra varredura ampla de território (volume); M2 pra prova rápida de escala
antes de modelar/subnichar/levar pra gringa.

## Modo F — recorte de mecanismo "PDF/apostila técnica → visual"  [ex-ADENDO §D]

## D · Recorte de mecanismo (ex. PDF → mapa mental)
Território com demanda provada em formato genérico (PDF/pack, ≥100 anúncios) × comunicação VISUAL
livre ('mapa mental / infográfico / esquema') = 0 na Biblioteca → vaga de formato: mesmo conteúdo,
formato mais desejado, sustenta ticket acima da base. **"Mapa mental" é ÂNGULO de venda, não formato
de entrega** — a entrega segue padrão (imagem por página → área de membros). Registrado em
o recorte PDF→mapa mental da R3 (~45 OPORTUNIDADE; arquivo original `RECORTE-PDF-PARA-MAPA-MENTAL.md` não existe mais — reconstruir a lista a partir do Hub se precisar).

---

## GATE DE SAÍDA — GATE 1 · MINERAR → Parada 1

Só devolve para a orquestradora quando todos os itens têm evidência colada no `ESTADO.md`. Contador-base: seção `GATES TRAVADOS` da orquestradora.

### GATE 1 · MINERAR → Parada 1
- [ ] `T2.1` **Concepções no Hub:** nº de registros em `concepcoes` = nº de concepções mineradas nos .md. Evidência: `total` do contador == contagem dos lotes. **Hub = 0 com lote em .md = passo ABERTO** (R6 #2). Registrar no Hub DURANTE a mineração, por termo.
- [ ] `T2.2` **Checklist 100k aplicado:** `sem checklist_100k: 0`. Cada concepção com CABE / CABE COM RECORTE (qual) / NAO CABE (por quê) + `nivel_consciencia` (R6 #3).
- [ ] `T2.3` **Cota por termo = PARADA:** por termo, nº de concepções ≤ ~6 (tabela termo → nº no ESTADO). Bateu a cota → o pane PARA e vai pro próximo; passou = base inflada, refazer o corte (R6 #4).
- [ ] `T2.4` **Seguidores IG NA VARREDURA:** `gate_origem` preenchido em toda concepção (PASSA / NAO_PASSA+motivo / "sem IG"+nº do Facebook marcado PENDENTE de decisão). Evidência: `gate_origem PENDENTE` só com "sem IG". Leitura = Biblioteca → nome → aba Sobre → ícone **Instagram**, NUNCA Facebook (R6 #5).
- [ ] `T2.5 · T2.6` **2 links + print (só p/ leva que avança):** `sem biblioteca_url: 0` e `sem pagina_vendas: 0` (ou "fora do ar (data)"); print em `paginas-referencia/<slug>.png` para as que avançam.
- [ ] `T2.7` **Rota da concepção + direito autoral:** `origem_referencia` preenchido (mineração/dia a dia/calendário/produto físico); conteúdo de terceiro revendido sem direito = recorte para o que é nosso OU descarte com motivo escrito. Preço e falta de dado NÃO descartam.
- [ ] `T2.8` **Cards crus salvos:** `raw-<termo>.json` existe por termo (`ls MINERACAO/<rodada>/raw-*.json`).
- [ ] `T2.9` **Falso-zero descartado:** (registrar no `validacao`/`lote` ou ESTADO com a palavra `controle`) todo zero gravado tem `tentativas=4` e controle bom anterior.
- [ ] `T4.1` **Parada 1 montada com:** tabela (concepção · formato · mecanismo · público · **os 2 links + print** — ou `PENDENTE (motivo, data)`, nunca coluna sumida · **por que passa no checklist 100k**) + recomendação. Faltou coluna = não apresento. **Sem AskUserQuestion antes de fechar os itens acima** (R6 #10). Formato completo: `FORMATO DAS PARADAS`.
- [ ] `T2.10 · T2.11` Modo D: `rastreador-<fonte>.md` com fonte + saída do leilão · Modo F: F1..F4 com saída nos `.md` (F4 = zero confirmado ou ocupado). (Só quando o modo vale; senão N/A.)
- [ ] **Antes da Parada 1:** `gate.py --ate T3` exit 0 (T3 só se cross) + Verificador Haiku (regra: orquestradora, GATE DE PASSAGEM). Não apresentar antes.
- [ ] `T2.13` Volume 55-60 (ou aceite do dono com N e data). Modo F: "ocupado" = leitura qualitativa com evidência colada (`mvt-validar`, `### Leitura qualitativa com evidência`), sem corte numérico.
- Regra do orquestrador × scripts (buraco 35): quem RODA script/edita Hub é pane Sonnet despachado pelo orquestrador, Haiku verifica (memórias `delegar-sempre-sonnet-haiku`, `delegar-tudo-fechar-pane`) — exceção só com decisão do dono registrada.
