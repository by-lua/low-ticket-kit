---
name: mvt-cross-market
description: MECÂNICA chamada pela skill `criacao-low-ticket-mvt` (T3 gate de origem, T6 gate de destino, T8 demanda no destino — modos B, B2, C, P e D/E/F quando a saída do leilão é MERCADO). Gate de origem (1 criativo ≥15d OU 3-5 ≥7d, IG ≤10k, link não bloqueia), gate de destino em 2 etapas (10 termos nativos → ocupado vai pro MVT → demanda só nos candidatos → ranking), quase-clone × MVT, playbook B2 França/Rodrigo, divergências declaradas Heitor/Borba, gateway por região, oferta pontual → vários destinos, adendos §B/§E/§F. Use quando o usuário quiser levar oferta BR→fora, fora→BR, Europa francófona, "dá pra vender isso em X?", ou pedir gate de origem/destino.
---

# mvt-cross-market — T3 origem · T6/T8 destino

> **Nomes de seção no texto abaixo** (`GATES TRAVADOS`, `ADENDO §x`, `passo N`, `FASE DE CONSTRUÇÃO`, `ROTEADOR`, `PASSO 0a/0b`, `PROMPT-PADRÃO`) são os da skill original, já dividida: cada um agora mora onde o `## ÍNDICE` da skill `criacao-low-ticket-mvt` aponta. O texto das regras não foi alterado.

> **IDs dos subpassos** = os de `criacao-low-ticket-mvt/references/TRILHA-CHECKLIST.yaml`; evidência com nome de arquivo padronizado, conferida por `scripts/gate.py --passo T3` / `--passo T6` / `--passo T8`. Saída ≠ 0 = passo aberto.

## ENTRADA EXIGIDA (conferir ANTES de começar — GATE DE PASSAGEM da orquestradora)
- T3: T2 fechado em `mvt-minerar` (IG + link + datas colhidos na varredura) — ORIGEM.
- T6: T5 fechado em `mvt-modelar` (GATE 2) + lista dos ~10 termos NATIVOS por idioma.
- T8: T6 (gap puro) e/ou T7 (candidatos de recorte, `mvt-modelar`).
Saída de T8 alimenta T9 em `mvt-validar`.
Entrada ausente = passo anterior ABERTO: volte a ele pela TRILHA do modo em `criacao-low-ticket-mvt`. 
Sem `ESTADO.md` com o bloco `## ROTEADOR` gravado, esta skill não roda (chame primeiro `criacao-low-ticket-mvt`).

Prompt de todo pane: `~/.claude/skills/criacao-low-ticket-mvt/references/PROMPT-PADRAO-PANE.md` (blocos obrigatórios de todo `pane_spawn` que toca browser, minera ou mede — copiados no prompt, nunca "veja a skill").

## SEQUÊNCIA AUTOMÁTICA — toda vez que o dono trouxer 1 oferta (link de anúncio/Biblioteca)

**Gatilho:** o dono manda um link de anúncio/Biblioteca de Anúncios, ou descreve uma oferta que viu, pedindo análise/"dá pra levar pra fora"/"modela isso". Roda esta sequência SEMPRE, nesta ordem, **mesmo que o dono cole um prompt externo pronto com etapas próprias** (ex.: template de diagnóstico pedindo "modelagem", "copy", "ganchos") — a estrutura dele não substitui os gates abaixo (feedback `feedback-prompt-colado-nao-pula-gate`, 21/10/2026).

1. **IDENTIFICAÇÃO** — abrir o link, ler a página de destino INTEIRA (nunca responder de memória/só pelo texto do anúncio), extrair os 4 elementos (comunicação/persona-dor, formato, mecanismo, nicho) + `REFERENCIA.md` (T2.12).
2. **GATE DE ORIGEM** (T3) — essa oferta já vende de fato na origem? (≥1 criativo ≥~15 dias OU 3-5 diferentes ≥7 dias, ≤10k seguidores IG, link conferido). Sem isso passar, não segue.
3. **DECIDIR DESTINO(S)** — region/idioma candidatos (perguntar ao dono só se ele não tiver dito; registrar no ROTEADOR R3). Pontual → vários destinos em paralelo é válido (seção abaixo).
4. **GAP no destino** (T6, etapa 1) — Biblioteca do destino com ~10 termos nativos: gap puro / gap de ângulo / OCUPADO.
5. **DEMANDA no destino** (T8/T9) — **obrigatório antes de qualquer copy/gancho/modelagem final**: YouTube/TikTok/Trends do destino, comentário recente, `sinal_de_compra`, urgência. Isso é o passo que mais se pula sob pressa — não pular.
6. **SÓ DEPOIS de 1-5 fechados:** modelar (T7) e produzir copy/página/criativo. Pedido do dono por "copy já" antes do passo 5 fechar → responder com o que falta medir, não com copy especulativa.

Se o dono colar um prompt pronto com "Etapa 1 diagnóstico" + "Etapa 2 modelagem": trate a "Etapa 1" dele como os passos 1-2 acima (compatível), mas a "Etapa 2" dele (copy/ganchos/checklist) só roda depois do passo 5 (demanda) fechar — nunca direto depois da escolha de mercado.

---

## Abertura cross-market (gate de origem quantificado, oferta pontual, ideia solta)

Modo B/B2/C/P (e D/E/F quando a saída for mercado): rodar o gate quantificado da memória `modelagem-cross-market` — **1 criativo rodando ≥~15 dias OU 3-5 criativos DIFERENTES ≥7 dias** (mesmo link), anunciante **≤10k seguidores no INSTAGRAM** (aba "Sobre"), link conferido (regra do dono 24/09/2026; tempo rodando pesa mais que nº de variações — "mesmo se tiver 1 criativo só mas tiver uns 15 dias ali já dá pra considerar mandar pra gringa"). Como ler seguidores: ver "GATE DE ORIGEM — como medir" no passo 1 — e, pra oferta escalada, aplicar uma **saída do leilão**
(ADENDO §A: outro mercado/público/ângulo/formato) ANTES de entrar no Hub (`concepcoes`). **Toda concepção achada vira registro no Hub (`concepcoes`).** O gate (**1 criativo rodando ≥~15 dias OU 3-5 criativos DIFERENTES ≥7 dias** (mesmo link), anunciante **≤10k seguidores no INSTAGRAM** (aba "Sobre"), link conferido) vira o campo `gate_origem` (`PASSA` · `NAO_PASSA` + motivo · `PENDENTE`) e **só as `PASSA` seguem como quase-clone cross-market nos modos B/B2/C/P**; o gate decide o que SEGUE, não o que ENTRA. Não filtre na coleta: na aula ele minera sem olhar nº de anúncios, seguidores ou tempo rodando [05:35:43] "isso daí é crença" [05:37:20] "isso daí não diz nada", e a R5 (gate na entrada) rendeu 1 oferta em 8 termos (~18 achados; ~10 eram físicos, 4 SaaS). Achado que não passa fica registrado com o motivo — pode virar referência de concepção mesmo sem ser clonável. Depois, o resto do fluxo (Destrinchar → Modelar → Validar → Obra de Arte
→ Construção) é o mesmo dos cinco modos; só a fonte da concepção muda.

**Oferta pontual → vários destinos EM PARALELO (R6, caso Mapa da Bíblia católico):** quando o dono manda
UMA oferta ("tem algum país tipo francês, italiano, latam que dê pra vender isso?"), não escolha o
destino no chute. (1) Orquestrador abre a página e salva `REFERENCIA.md` (concepção, entrega, bônus,
o que PROTEGE a oferta — ex.: católico = 73 livros; material protestante de 66 é outro produto);
(2) 1 pane faz gate de origem no BR + idioma A; outro pane faz idiomas B/C/D — cada um com seu perfil,
termos NATIVOS não-literais, country=ALL, gap (puro/ângulo/ocupado) + demanda YouTube com comentário
recente; (3) volta ranking de mercados com gateway (Latam = método local; IT/FR/EN = cartão).
**Ordem na gringa: Biblioteca PRIMEIRO, demanda DEPOIS, só nos candidatos** (dono, 24/09/2026). **Gap também se mede com ~10 termos NATIVOS por idioma** (dono, 24/09/2026 — "tá pensando em uns 10 termos pra achar ofertas semelhantes na Biblioteca?"): produto · formato · dor/desejo · público/obreiro · como o nativo fala (não-literal), curtos (2-4 palavras). Com 3-5 termos o "gap puro" é frágil (R6: França saiu "gap puro" com ~4 termos). Os mesmos 10 servem depois pra demanda (YouTube/TikTok). Etapa 1 =
gap em todos os destinos (barato). **OCUPADO não é descarte** — só perde o quase-clone e vai pro MVT:
subnicho (obreiro com data, fatia com dor mais aguda), ângulo ou formato → gerar recortes e medir o gap
DE CADA RECORTE na Biblioteca do destino (dono, 24/09/2026: "se tá ocupado não devia cair em
subnichação ou no método MVT?"). Mercado ocupado costuma ser o de MAIOR demanda (R6: EN tinha 5,2M views).
Etapa 2 = só nos candidatos (gap puro, gap de ângulo, ou recorte MVT com gap): demanda (YouTube distribuição + comentário recente até 12m (≤3m quente + 3-12m separados; decisão do dono 25/09/2026), TikTok orgânico, Trends) · `sinal_de_compra`
· urgência por público (fiel × OBREIRO com data). **Resultado da etapa 1 é lista de CANDIDATOS, nunca
ranking/"destino nº1".** Erro real R6: chamei a França de "destino nº1, gap puro" só com a etapa 1; o
dono pegou. Gap com demanda fraca na etapa 2 = "desconfie de nicho sem comprador". Pastas:
`MINERACAO/<rodada>/<slug>-cross/`.

**Ideia solta do dono ("será que X vende?") não se mede.** Peça a concepção em 1 frase no formato "N coisas para <público>" e os 4 elementos (comunicação, formato, mecanismo, nicho/subnicho): ele mesmo responde assim — [cauda ≈11:30] "Traz a concepção, pô" / [cauda ≈11:30] "Me fala os quatro elementos dessa concepção". Sem os 4 elementos ainda não é concepção; com eles entra como registro do Hub e segue o fluxo.

---

## GATE DE ORIGEM (modos B/B2/C/P e D/E/F-mercado)

### GATE CROSS-MARKET · ORIGEM (modos B/B2/C/P e D/E/F quando a saída do leilão for MERCADO)
- [ ] `T3.1` Por origem: ≥1 criativo ≥~15 dias OU 3-5 diferentes ≥7 dias (mesmo link, conferido) + **≤10k seguidores no INSTAGRAM** (evidência: nº + @handle) — o pane que mede seguidores lê Instagram, não Facebook.
- [ ] `T2.12` Oferta pontual do dono: `REFERENCIA.md` salva (concepção, entrega, bônus, o que PROTEGE a oferta) antes de escolher destino.
- [ ] `T3.1` Resultado registrado em `gate_origem`; só `PASSA` segue como quase-clone. **Link da página não achado NÃO é `NAO_PASSA`** (`link PENDENTE`, concepção segue); `NAO_PASSA` só por tempo/criativos/seguidores IG, com o motivo escrito.

---

## Quase-clone × MVT — exceção do eixo MERCADO e divergências declaradas (Heitor / Borba)

**Exceção: o eixo MERCADO permite quase-clone; os outros não.** Mudar país/idioma já tira do leilão
sozinho — então uma oferta muito validada pode ir pro destino **quase igual, só adaptada
culturalmente** (idioma + modelagem cultural). Foi feito e funcionou. No **MESMO** mercado (BR→BR)
clonar NUNCA funciona: você entra no leilão do dono do pixel maduro e perde — ali é obrigatório mudar
público/ângulo/formato (sub-nicho etc.). Quanto mais forte a prova (muitos anúncios + rodando há
bastante tempo), mais seguro o cross-market. **Sempre validar demanda no destino antes** (o gate do
passo 4 roda no país/idioma de destino, não no de origem).

> **Divergência DECLARADA do Heitor (decisão do dono, 24/09/2026).** Pelo Heitor, trocar só o país
> sem mexer em nenhum dos 4 elementos seria cópia, e "20-30 anúncios ativos rodando há X dias" não
> valida nada. No cross-market a gente faz diferente DE PROPÓSITO (adendo Rodrigo Liedson): é a MESMA
> concepção levada pra outro mercado, então o risco não é reduzido pela modelagem de elemento — por
> isso a **prova de escala na origem vira obrigatória** (1 criativo ≥~15 dias OU 3-5 criativos
> diferentes ≥7 dias, mesmo link, anunciante ≤10k seguidores no Instagram). Oferta que ainda está em teste na origem não vai pra
> fora: se não se provou lá, quase-clone aqui só herda o fracasso. Ordem no destino: **gap primeiro**
> (Biblioteca do destino: ninguém rodando igual, ou só em outro ângulo) → **depois demanda** (YouTube/
> TikTok/Trends/comentários no idioma do destino, termo não-literal). Sem gap → aí sim modela um
> elemento (ângulo/formato) em cima do validado. No MESMO mercado vale a regra do Heitor sem exceção.

> **Divergências DECLARADAS do Borba (decisão do dono, 24/09/2026; ref `MINERACAO/referencia-adsborba/METODO-BORBA.md`). Em todas, MANTÉM a nossa regra.**
> 1. **Quase-clone de oferta de TERCEIRO que passa no gate segue permitido.** O Borba só faz quase-clone da oferta PRÓPRIA ("eu peguei uma oferta minha do Brasil que eu já tinha validado, porém ela já tinha morrido. Adaptei e transcrevi ela completamente" [BORBA M0lixH8qNxo]); na de terceiro cria produto novo no destino ("Não é a mesma oferta… é o mesmo nicho, porém é um produto diferente" [BORBA M0lixH8qNxo]). Caminho válido extra dele: **oferta PRÓPRIA morrendo no BR → quase-clone no destino no mesmo dia** (risco já pago, sem precisar do gate de terceiro).
> 2. **Gate de origem segue o nosso: 1 criativo ≥~15 dias OU 3–5 criativos ≥7 dias, ≤10k seguidores IG, link conferido.** O dele é mais baixo: "sempre mais de três dias rodando… menos de 10.000 seguidores" [BORBA-GA GwKEMxzTSjg]; "sempre mais de 5 criativos diferentes" [BORBA M0lixH8qNxo]; filtro RatoAds "entre 5 e 300 anúncios, rodando há mais de 3 dias e com menos de 30 mil seguidores" [BORBA dgqmIJ8bP4g]; iniciante "acompanhar por dois ou três dias" e quem tem operação "7, 14 dias" [BORBA-GA iIOMI4OOCXA]. Não rebaixar por causa dele.
> 3. **No destino segue "ninguém rodando, senão MVT" (ângulo ou formato).** Para o Borba concorrente no destino é confirmação: "primeiro entender se já tem gente fazendo isso lá fora. Qual que é o grau de sofisticação" [BORBA M0lixH8qNxo]; ele só lê formato (VSL, quiz) e diferencia por subnicho.
> 4. **"Ou o contrário" (gringa→BR) é regra NOSSA**, não aparece em nenhuma transcrição do Borba (só BR→EUA). Idem "rodar o MVT no destino".
> 5. **Teste inicial de criativo: tráfego, skill `metaads-kevones`.** Aqui só entra a criação do criativo (Heitor: 3–5 demonstrativos).
> 6. **"Lateralizar" tem 2 sentidos no Borba:** (a) produto lateral ao mesmo público validado ("produtos laterais a esse pro mesmo público validado ou… subnichado e dê 10 ideias" [BORBA-GA GwKEMxzTSjg]) = nossa modelagem lateral/N4; (b) o outro sentido é de tráfego, fora daqui (skill `metaads-kevones`).
>
> **Subnicho pedido à IA (Borba).** Com a oferta escalada escolhida: jogar biblioteca+página no Claude e perguntar quem compra ("entender o público validado… Quem compra aquele produto?" [BORBA W4X3F8oa9H8]) e pedir "me dá 10 ideias de produtos subnichados que tem uma dor mais latente" [BORBA-GA iIOMI4OOCXA]; oferta já estreita → pedir a fatia MAIOR. Resposta da IA é hipótese: fecha com demanda medida.
> **Demanda no destino (Borba).** Termos no idioma do destino → TikTok/YouTube/Instagram gringo (views, comentários) → Biblioteca do destino → volta pro Claude com os comentários: "você acha que esse nicho é interessante pra gente rodar fora?" [BORBA-GA GwKEMxzTSjg]. Complementa (não substitui) o gate de demanda acima.

**Modelagem cross-market** (memória `modelagem-cross-market`): oferta VALIDADA em outro país/idioma
(ES/EN/FR → BR, ou BR → fora) → copiar a estrutura validada é o próprio método, não criação original.
Bidirecional, qualquer par de mercado. Quase-clone = **mesma CONCEPÇÃO/estrutura de oferta** = página CLONE LITERAL + imagens/mockups/entregável DELE adaptados (só idioma + cultura + cores um pouco); ver **REGRA CROSS-MARKET** no passo 4. Proibido: peça dele crua, sem adaptar (memória `anti-arte-concorrente`; item T13.26). Antes de modelar como quase-clone, passa o
**gate de validação quantificado** (registrado em `gate_origem`; decide o que SEGUE, não o que entra no Hub) (vale SÓ mercado→mercado — BR→fora, EN→ES, EN→BR — nunca no mesmo
mercado): (1) **1 criativo rodando há ≥~15 dias OU 3 a 5 variações de criativo DIFERENTES** da mesma oferta rodando há **≥7 dias** (contagem
alta — 40/100/150 — e mais tempo = mais seguro) = prova
de demanda, medido na Biblioteca de Anúncios. **Dois cuidados ao conferir:** (a) mesma página pode vender
ofertas DIFERENTES — checar o LINK da oferta em cada criativo, contar só variação do MESMO link; (b) o
anunciante NÃO pode ser expert/autoridade — **até 10.000 seguidores no INSTAGRAM** (Biblioteca → nome do anunciante → aba "Sobre") (acima = guru por
marca pessoal, não replicável; player pequeno escalando = converte pela oferta, modelável).
(2) NINGUÉM vende igual no destino = gap puro, **ou** já tem gente vendendo mas em outro ângulo/formato
= gap de ângulo, aplica MVT em cima do validado em vez de clone direto (ex: tarô já roda no BR, mas
ninguém no ângulo "mapa/diagrama visual" — não descarta, modela o ângulo). Só com (1) + algum tipo de
(2) → aplica o método.

---

## MODO B2 · FRANÇA — PLAYBOOK CONSOLIDADO (método Rodrigo Liedson, ajustado ao MVT)

Quando o dono disser "quero minerar/vender na França" (ou Europa francófona), este é o fluxo inteiro,
método completo do Rodrigo Liedson (canal @Rodrigoliedson, "Clube do Dólar") já ajustado ao MVT.
Fonte: `MINERACAO/referencia-rodrigoliedson/` (transcritos 1-5, A1, B1-B5, C1-C7, D1-D7 + os 4
METODO-RODRIGO-*.md de síntese) e, pro canal completo (85 vídeos, 21/10/2026), `CONHECIMENTO/
FONTES-DE-CONHECIMENTO/RODRIGO-LIEDSON/TRANSCRICOES/`. Cada peça detalhada mora na sua seção; aqui é a SEQUÊNCIA.
Vídeo de TRÁFEGO puro (BidCap, ROAS, taxa de 12,5%) **não entra aqui** — método de tráfego segue sempre
`metaads-kevones` (memória `trafego-segue-kevones`), mesmo quando é o Rodrigo ensinando.

**1. Achar oferta (origem BR, EN/US, ou QUALQUER idioma).** Rodrigo busca **em inglês, MUNDO TODO**
(Biblioteca **country=ALL** — a língua já define o mercado, nunca trava em 1 país) e usa DOIS eixos de
busca, não só nicho:
  - **Busca por FORMATO × NICHO** no idioma de origem (`sermon printables`, `bible study workbook`…
    ver `TERMOS-DE-BUSCA.md`).
  - **Busca por PREÇO na própria copy do anúncio** — técnica que ele chama de "antiga mas eficaz":
    digitar o valor exato que aparece no texto do anúncio (ex.: `$9.90`, `R$19,90`, `9 e 90`) na
    barra de pesquisa da Biblioteca. Acha ofertas low ticket direto pela faixa de preço, sem precisar
    saber o nicho antes. Usar os DOIS eixos, nunca só um.
  - Gate de ORIGEM (nosso, 24/09/2026): **1 criativo rodando ≥~15 dias OU 3-5 criativos DIFERENTES ≥7 dias** (mesmo link), anunciante **≤10k seguidores no INSTAGRAM** (aba "Sobre"), link conferido. Rodrigo usa **≥3-5 criativos em IMAGEM** do mesmo link/anunciante · rodando **≥7-15 dias
    seguidos com a MESMA quantidade de anúncios ativos (ou crescendo)** — a partir de ~5 dias já dá
    pra analisar, ele considera "validado" a partir de ~10 dias de constância · anunciante **≤10.000
    seguidores** (corte duro) · **promessa clara, sem ambiguidade** · oferta de **"solução rápida"**
    entregando coisa PRONTA ("1000 sermões", "500 moldes prontos"), nunca "aprenda a fazer do zero".
  - **Distinguir escalada de escalável**: escalada = vendendo AGORA, anúncios ativos e constantes.
    Escalável = teve pico de resultado (ex. 1.400 resultados) e caiu quase a zero agora — "sucesso
    deixa rastro": vale estudar por que caiu (ângulo/criativo) e se dá pra reativar, mas não é a
    prioridade — priorizar sempre a ESCALADA primeiro.
  - Evitar oferta com VSL ou rosto do dono aparecendo (mais difícil de modelar sem invadir identidade);
    preferir página sem rosto, anônima, fácil de clonar.
  - Nichos que ele cita vendendo em FR: **cristão/espiritualidade** (alta demanda, pouca concorrência,
    é o nicho preferido dele), crochê/amigurumi, artesanato, relacionamento.
  - Atalho/adendo: plataformas agregadoras que já filtram por "escalado" (GreenGuedes/GringAds/AdSpyro/
    RadaAds/Detetive Ads) — §E.

**2. O que Rodrigo chama de "validado" (e o que ele NÃO faz — nosso adendo por cima).**
  - **Validado pra ele = lucro líquido diário POSITIVO e REPETIDO**, não faturamento bruto e não
    "vendeu uma vez". Ele mesmo dá o exemplo: parou de escalar uma oferta assim que bateu lucro
    diário repetido (cita ~R$250/dia), porque considerou "validada" e foi focar outro funil — não
    precisa virar oferta gigante pra contar como validada.
  - Antes de rodar tráfego, ele estima a **tese de potencial** por fora: tráfego do site concorrente
    via SimilarWeb × taxa de conversão de 1-3% × ticket = faturamento potencial estimado.
  - **Ele NÃO valida demanda no país/idioma de destino antes de lançar.** Em nenhuma das transcrições
    ele mede gap ou demanda em FR antes de traduzir — a lógica dele é "se já está escalada num
    idioma/mercado, deveria funcionar em outro parecido" (pressuposto de transferência direta). A
    escolha de francês em vez de espanhol é por **intuição de poder de compra + "pouco explorado"**
    (espanhol já saturado), não por medição. O único "teste" dele pós-lançamento é ajustar o FUNIL
    (headline, order bump, checkout) até bater lucro — validação de funil, não de mercado.
  - **Isso é a lacuna que o NOSSO gate de destino cobre.** O passo 3 abaixo é ADENDO NOSSO por cima do
    método dele, não algo que ele faz — não herdar essa lacuna.

**3. Validar no DESTINO — França (NOSSA adição, não do Rodrigo).**
Gate de destino ANTES de modelar (na TRILHA roda em T6, logo depois de destrinchar; gap puro = quase-clone cultural sem modelar elemento, ocupado/gap de ângulo = T7 modela e mede o gap do recorte — ordem do dono): (a) **gap** — buscar o nicho na Biblioteca **country=FR, em
francês**; se já tem gente rodando igual, não é gap puro → muda ângulo/formato (MVT). (b) **demanda** —
YouTube/TikTok FR + comentários recentes em francês + Google Trends FR + **sinal de compra** ("où
acheter", "combien"). Termo francês **não-literal** (como o nativo fala, não Google Tradutor). Só
avança com gap (ou gap de ângulo) + demanda comprovada.

**4. Modelar (quase-clone cross-market).** Mudar idioma/país já sai do leilão → vai quase igual, **só
adaptando idioma + cultura** (não traduzir seco). Nunca colocar o produto modelado no MESMO idioma do
original (ex.: original em inglês → nunca vender de novo em inglês, só em francês/outro). Página
hospedada por nós; entrega na **NOSSA área de membros**.

**REGRA CROSS-MARKET (dono, 27/09/2026 — vale sempre que levar oferta de um país/idioma pra outro, salvo ordem contrária):**
estrutura validada NÃO se mexe. (1) **Página = CLONE LITERAL** do original (DOM renderizado + CSS compilado, mesmas
classes/tamanhos/blocos/ordem): muda só idioma (com adaptação cultural, não tradução seca), moeda/preço e as cores "um
pouco" (mesma claridade de fundo, tom deslocado, só pra ter identidade própria — tokens no `DESIGN-SYSTEM.md`).
Nunca reconstruir layout "do nosso jeito" (saiu menor/centralizado/com cards que ele não tem). (2) **Imagens, mockups
e ENTREGÁVEL = os DELE, adaptados**: mesmas peças, só idioma + nossa identidade de cor. Mecânica: GPT **Work mode**,
um pedido com o lote: link da página original + nosso `index.html` + as imagens/páginas dele + tokens de cor →
"estou modelando esta oferta pro <idioma>, já troquei as cores; adapte TODAS estas imagens pro <idioma> e pra nossa
identidade, mantendo layout/ilustração/composição". Receita: `imagens-pagina-low` › "Cross-market: TODAS as imagens".
Proibido continua: peça dele CRUA (texto na língua de origem, cor antiga) e texto/copy/criativo sem adaptar.
 Aplicar os **5 PADRÕES DE LOW TICKET VENCEDOR**
(seção acima).

**Bônus = MESMO NÚMERO e MESMO PAPEL da origem, mapeado 1:1 (incidente GeriNeuro, 14/10/2026):**
cada bônus da origem tem um papel (ex.: "mobilidade reduzida" = versão mais fácil pro estágio avançado
do problema). O nosso bônus equivalente herda ESSE PAPEL, adaptado pro nosso recorte — nunca um conceito
novo inventado do zero nem objeto-clichê genérico (ex.: "telefone antigo", "caixa de ferramentas") que não
existe na origem e não tem relação com a dor da persona. Antes de nomear/desenhar um bônus: (1) olhar o
bônus equivalente da origem e o papel que ele cumpre no funil, (2) traduzir esse papel pro recorte novo,
(3) só então nomear. Se não houver equivalente claro na origem, perguntar à dona em vez de inventar.

**5. Funil.** Estrutura completa dele, repetida em vários vídeos (D1/D2/D4, ep.2):
  - **Entrada $9,90–$19,99** (Europa aguenta ticket mais alto que Latam — ele usa $9,90 fixo na
    França vs $4,90-5,90 no Latam, poder aquisitivo permite).
  - **2-3 order bumps ~$3,90-4,90**, sempre relacionados/complementares ao principal ("o que falta pro
    que ela já comprou" — comprou esboços de pregação → bump é "temas prontos pra pregar"). **Nunca
    empilhar mais que isso** — satura e trava a decisão.
  - **Upsell 1 (página de obrigado) = microSaaS de assinatura mensal ~$7,90/mês, SEMPRE amarrado a um
    produto estático do MESMO nicho do produto de entrada.** Regra dele, sem exceção nas transcrições:
    o SaaS nunca é vendido sozinho de cara — ele nasce como upsell/complemento de um produto estático
    já validado, resolvendo o que o produto estático não cobre (ex.: vendeu "1000 sermões prontos"
    estático → upsell é "Pretify", app que GERA sermão sob demanda por tema/passagem). Conversão de
    ~40% nesse upsell com a estrutura certa (modelo de página de upsell entregue no clube dele). Cases
    dele mostram clientes renovando a assinatura 8, 9, até 11 vezes — LTV é o motor do funil, não a
    venda de entrada.
  - Variante "presente": oferecer os 7 dias grátis do SaaS como upsell **one-click** (cartão já salvo
    no checkout principal) em vez de venda direta — sem one-click a conversão cai (pessoa não quer dar
    cartão de novo pra algo "grátis").
  - **Upsell 2** maior, ex. ~$12.
  - **Botão da 1ª dobra da página NUNCA vai direto pro checkout** — leva pra 2ª seção com mais prova
    visual antes. Botão seco = CTR alto, venda baixa.
  - **Funil gamificado (quiz) via Lead Flux** — alternativa/complemento ao funil de página: estudar o
    público primeiro (dores/medos/desejos/objeções), colar o estudo no ChatGPT pedindo "funil
    interativo gamificado", montar no Lead Flux (drag-and-drop: roleta, tela de "carregando" falsa de
    3s pra simular personalização, perguntas de múltipla escolha). Cada etapa tem 1 objetivo
    psicológico (identificação → impacto → poder de mudança → desejo de transformação) até entregar a
    oferta como "resultado personalizado". Gamificação aqui = simular customização pra elevar valor
    percebido antes de mostrar preço, não é qualificação de lead.
  - **Venda SEM página, direto no checkout** — só serve pra produto tipo PACK/PACOTE pronto (não
    "aprenda a fazer X", que ainda precisa de página normal). Mecânica: banner de checkout (imagem
    única 1080×2000, Canva) substitui a LP inteira — headline + subheadline + mockup + checklist de
    benefícios + preço ancorado (de $27 por $4,90) + selos/contador/depoimentos, subido em Hotmart →
    Ferramentas → Aparência da página de pagamento → Nova página → Imagem. Funciona porque o criativo
    já convenceu antes; o banner só fecha.

**6. Criativo — passo a passo de vídeo alta conversão.**
  - **Estrutura AIDA**: atenção → interesse → desejo → ação. Copy sempre gerada primeiro em
    PORTUGUÊS (mesmo pra produto em francês/inglês/espanhol) — só traduz no fim, porque toda a criação
    do criativo é feita em pt-BR.
  - Passo a passo dele (B4): (1) pega a copy da página de vendas, pede pro ChatGPT reescrever em
    modelo AIDA, sem títulos/emojis, "como se fosse alguém falando" — vira o texto de voz; (2) gera
    áudio no **ElevenLabs** (text-to-speech) com essa copy; (3) monta no **CapCut**: corta os
    silêncios do áudio (nunca deixar espaço sem voz — fica monótono), sobe imagens/vídeos do Pexels
    (ou banco próprio) que ilustrem cada frase, guarda espaço em cima do vídeo pra legenda; (4)
    **dublagem**: exporta o vídeo AINDA em português, sobe no **ElevenLabs Dub** e traduz pro idioma
    de destino (francês/espanhol) só o áudio, sem legenda ainda; (5) volta pro CapCut com o vídeo já
    dublado e SÓ AÍ coloca a legenda traduzida por cima (nunca legendar antes de dublar — dobra o
    trabalho de tradução). Legenda + red line no topo aumenta retenção (curiosidade de "que ferramenta
    é essa"). Formato retrato com espaço no topo, funciona em vários posicionamentos.
  - **IMAGEM continua o padrão mais rápido** (headline + mockup + preço + CTA; direto, nunca curioso —
    curioso é pra VSL de ticket alto). Cross-language de imagem: GPT/Gemini "recria a MESMA imagem,
    só traduz o texto pro francês" (mais barato e rápido que refazer do zero).
  - Teste e validação do criativo no gerenciador: tráfego → skill `metaads-kevones`.

**7. Super-entregável — múltiplos materiais no mesmo pacote (B1).** Pra ofertas tipo "1000 X prontos"
sem ter que criar os 1000 itens do zero: baixa material de bancos de conteúdo pronto (ex. sites de
receitas/planilhas), NÃO sobe o arquivo original direto no Hotmart (risco de direitos autorais) — sobe
pro Drive próprio, gera link `.../preview` (troca `view` por `preview` na URL de compartilhamento), e
entrega uma "capa" no Canva (Doc) com boas-vindas + o link externo. Alternativa mais robusta: pedir pro
ChatGPT montar uma área de membros estilo Netflix (prompt: "crie área de membros para [nicho], estilo
Netflix, entregue estes produtos: [links]") com produtos BLOQUEADOS que, ao clicar, levam direto pro
checkout de um order bump/upsell — mais uma forma de subir ticket médio dentro da própria entrega.

**8. Configuração.** **Gateway card-first** (Europa francófona = cartão resolve; Hotmart provado,
somar PayPal em FR; perfis `cooud` 9269 e `mundpay` 9270 já criados — verificar cobertura EUR antes de
migrar). Fanpage no idioma FR (nome cristão traduzido); países **França/Bélgica/Suíça/Canadá** — cluster
por IDIOMA comum (francófono), **1 tradução serve os 4 países**, multiplica o alcance de 1 trabalho de
tradução só; idioma francês.
Tráfego (estrutura de campanha, orçamento, contas): skill `metaads-kevones`.

**8b. Novo destino testado por ele: África do Sul + Filipinas (vídeo "Testei Low Ticket na África",
canal Rodrigo Liedson).** Continente inteiro NÃO funciona (baixo poder aquisitivo na maioria dos
países) — recorte por PAÍS dentro do continente: **África do Sul** (melhor poder aquisitivo do
continente, fala inglês) + **Filipinas** (mercado "subestimado" que ele testou junto e também vendeu),
sempre em **inglês**. Ticket de entrada mais baixo que Europa: **$3,90** (vs $9,90-19,99 na França) —
resultado dele: CPA <$1, ROAS ~5x. Estrutura de funil usada ali: front $3,90 + 3 order bumps
($3,90-5,90) + Upsell 1 $7,90 (microSaaS assinatura) com **downsell de teste grátis 2 dias → cobra
$9,90 depois** (em vez de downsell = versão mais barata, aqui é trial pago) + Upsell 2 $8,90 sem
downsell. Não promove a um destino sozinho — roda o MESMO gate de destino (gap + demanda) antes de
escalar; o vídeo é só precedente de ticket/país, não substitui o gate.

**8c. Order bump de mensalidade (variante nova, vídeo "Marketing em 2026").** Além do Upsell 1 =
microSaaS assinatura (padrão da seção 5), ele também testou o produto recorrente como **3º order bump**
em vez de upsell — mesmo princípio (recorrência = previsibilidade), só muda ONDE no funil entra a
cobrança mensal. Se o bump de recorrência não for usado, upsell de recorrência imediato vira
obrigatório — ele nunca deixa o funil sem NENHUMA peça recorrente. Exemplo dele: front $4,90 ("1000
esboços prontos pra pregar") + bumps temáticos + Upsell app de IA que GERA sermão por tema/passagem
($7,90/mês) — mesmo padrão do Upsell 1 da seção 5, aqui só confirma que a peça recorrente pode ser bump
OU upsell, nunca ausente.

**Ferramentas de espionagem citadas por ele (adendo, não método base — §E/§F):** Biblioteca de Anúncios
com filtro de edição Europa; **reverse image search** (achar outros anunciantes rodando a mesma
imagem/produto); **rastreador de concorrente por e-mail** (Edge Tracker — avisa quando o anunciante sobe
novo criativo); **dublagem automática de vídeo** (legenda + áudio traduzido mantendo fundo, atalho pra
modelar criativo em vídeo trocando só idioma); **clone HTML 1:1** (Save Web/savewebzip.com baixa a
página do concorrente inteira pra hospedar em cPanel próprio — nosso método É clonar 1:1 — DOM+CSS — trocando só
texto/cor/imagem; ver REGRA CROSS-MARKET no passo 4).

> Tudo isto continua MVT: vende (gate origem) → demanda + urgência (gate destino, ADENDO NOSSO que
> Rodrigo não faz) → twist (modelagem cultural + 5 padrões). Não pula validação de destino mesmo que o
> método original pule. Peças detalhadas: PADRÕES DE LOW TICKET VENCEDOR, `modelagem-cross-market`,
> adendo §B/§E/§F, TERMOS-DE-BUSCA.md.

---

## Gateway por região

> **Imagens no outro idioma (entregável + página de vendas, BR→fora e fora→BR):** skill `traduzir-entregavel-imagem` — traduz por script sem regenerar a imagem (dona 05/10/2026).
>
> **Página de oferta multi-país:** preço aproximado na moeda local em cima, valor do cadastro (US$/€) menor embaixo como "valor de referência" — obrigatório (dona 05/10/2026). Regra e código: `criacao-low-ticket-mvt/references/PRECO-MOEDA-LOCAL.md`.

**Gateway por REGIÃO (regra de método):** o método de pagamento depende do MERCADO de destino, não é
um só:
- **Europa francófona (FR/BE/CH/CA) e EUA = CARD-FIRST** — cartão resolve a maioria esmagadora;
  **vender só cartão NÃO é handicap** ali. Em França ajuda somar **PayPal** (e CB/Carte Bancaire é o
  esquema local, mas é cartão). Gateway provado: **Hotmart** (aceita cartão EUR/USD + payout). Mundpay é
  alternativa a verificar (cobertura EUR/país/saque) antes de trocar.
- **Latam/BR = precisa MÉTODO LOCAL** — só cartão trava a venda; exige PIX (BR), OXXO/SPEI (MX), etc.
  Ver memórias `xpag-gateway-mexico`, `zenith-*`. NÃO reaproveitar a régua card-only da Europa aqui.
Regra: definir gateway pela sofisticação de pagamento do destino, nunca copiar a de outro mercado.

---

## Adendos §B / §E (atalho) / §F

### §B · Cross-market BR ↔ gringa (por sofisticação de mercado)
Oferta saturada/morrendo no BR → rodar em mercado de **sofisticação MENOR** (Latam/EUA conforme o
caso): público ainda cru pra aquele ângulo = conversão mais fácil, leilão mais barato. Bidirecional
(gringa→BR também). Complementa a memória `modelagem-cross-market` (gate: 1 criativo ≥~15 dias OU 3-5
variações ≥7 dias, anunciante ≤10k seguidores IG, link da oferta conferido). Régua nova aqui = escolher destino pela sofisticação, não só pelo idioma.
**Único eixo que permite quase-clone** (ver princípio no passo 3): mudar país/idioma já sai do
leilão, então dá pra ir quase igual, **só adaptando culturalmente** (idioma + modelagem cultural).
Quanto mais forte a prova (muitos anúncios, rodando há tempo), mais seguro. Sempre checar demanda no
destino antes — nunca clonar no mesmo mercado.

### §E (parte cross) · Plataforma de ofertas gringas validadas
- **Plataforma de ofertas gringas validadas** (ex: GreenGuedes/"Green Guedes") — catálogo só de
  ofertas gringas (EN/ES) já validadas, prontas pra levar pra Europa/outro mercado. Atalho do M2 pro
  cross-market. Nós também achamos isso sozinhos na Biblioteca do mercado de origem — a plataforma é só
  conveniência, não obrigatória.

### §F · Ferramentas de execução cross-market (Europa/França) — NÃO são passo do método
Mecânica pra rodar oferta validada em outro idioma. Método (destino, gate, 5 padrões, funil) está no
CORPO; aqui só a caixa de ferramentas. Ref `MINERACAO/referencia-rodrigoliedson/METODO-RODRIGO-EUROPA.md`.
- **ElevenLabs Dub** — dubla o ÁUDIO de um criativo em VÍDEO pro idioma destino (clona voz + traduz
  fala). Só pra criativo em vídeo; depois CapCut tira marca d'água + põe legenda traduzida. Criativo em
  IMAGEM (o padrão) não usa Dub — é só GPT "mesma imagem, traduz o texto".
- **Antidetect browser** (Wolf/Walf ou o que o dono já tem) — roda a mesma oferta em EN/FR/ES em contas
  de anúncio ISOLADAS; se uma conta cai, as outras seguem vendendo. Blindagem da operação multi-idioma.
  **O dono já tem antidetect** — usar o dele.
- **Página nós fazemos aqui** (nosso processo/skills de página), não depender de Bolt/Lovable/WordPress
  do vídeo. A entrega final continua na NOSSA área de membros.
- **Fanpage no idioma do destino**; direcionamento por interesse (ex cristão FR: pastor, teologia,
  religiosos); países FR = França/Bélgica/Suíça/Canadá; gateway card-first (ver PADRÕES/gateway no corpo).

---

## GATE DE SAÍDA — GATE CROSS-MARKET · DESTINO (2 etapas)

### GATE CROSS-MARKET · DESTINO (2 etapas — não existe ranking antes da etapa 2)
**Etapa 1 — GAP (barato, todos os destinos):**
- [ ] `T6.1` **~10 termos NATIVOS por idioma** (produto · formato · dor/desejo · público/obreiro · como o nativo fala; não-literal; 2-4 palavras) — evidência: lista dos 10 por idioma no `<slug>-cross/`. 3-5 termos = etapa 1 ABERTA (R6 #9).
- [ ] `T6.2` **Gap só na Biblioteca é evidência fraca [decisão do dono 25/09/2026]:** o candidato que segue para T9 ganha `concorrencia-<id>.md` no destino (idioma nativo: marketplaces locais, Google, lojas de app, criadores) — T9.13. **A técnica dos ~10 termos (concepções semelhantes: produto, formato, dor, desejo, público, fala do comprador, sinônimos do mecanismo) tem regra ÚNICA em `mvt-validar` [T9.13]; aqui só se aplica no idioma do destino, sem duplicar.** Biblioteca, `country=ALL`, em TODOS os destinos candidatos; cada destino classificado: **gap puro · gap de ângulo · OCUPADO**.
- [ ] `T6.3` **OCUPADO NÃO É DESCARTE** (R6 #8): vai pro MVT (subnicho/ângulo/formato) → gerar recortes e medir o gap DE CADA RECORTE na Biblioteca do destino. Evidência: tabela recortes × gap para cada destino ocupado. Sem essa tabela, destino ocupado não sai da lista.
- [ ] `T6.4 · T7.12` Saída da etapa 1 = **lista de CANDIDATOS**. Proibido escrever "destino nº1"/"ranking" aqui (R6 #7).

**Etapa 2 — só nos candidatos (gap puro, gap de ângulo, recorte MVT com gap):**
- [ ] `T8.1` Demanda (YouTube distribuição + comentário recente até 12m (≤3m quente + 3-12m separados; decisão do dono 25/09/2026), TikTok orgânico, Trends) com os mesmos ~10 termos.
- [ ] `T8.2` `sinal_de_compra` por candidato (comentário pedindo, "où acheter"/"how much"…).
- [ ] `T8.2` Urgência por público (fiel × OBREIRO com data).
- [ ] `T8.2` Gateway do destino (card-first × método local).
- [ ] `T8.3` **Só com as 3 colunas preenchidas por candidato → ranking.** Gap com demanda fraca = "desconfie de nicho sem comprador".
- [ ] `T13.26 · T13.28` Construção cross: `ANTI-ARTE.md` (comando + saída, frases idênticas = 0) e `IDIOMA.md` (nossa revisão do idioma; **sem checklist legal de país**, decisão do dono 25/09/2026 (revisão) — `criacao-low-ticket-mvt/references/CONSTRUCAO-GATES.md`). Gateway por região cita as memórias `xpag-*`/`zenith-*` (cartão só BR; CO/MX… sem cartão).
