---
name: criacao-low-ticket-mvt
description: Conduz a criação de uma oferta Low Ticket MVT do zero até o criativo pronto, na ordem exata do método "O Processo" (Heitor Nogueira). ORQUESTRADORA (porta de entrada): SEMPRE começa pelo `## ROTEADOR` (tipo de trabalho → modo → mercado → nicho → preço, gravados no ESTADO), segue a TRILHA do modo (T0-T15) com ENTRADA/SAÍDA verificável, as 3 PARADAS e o GATE DE PASSAGEM, e chama as MECÂNICAS `mvt-minerar`, `mvt-modelar`, `mvt-validar`, `mvt-cross-market`, `mvt-obra-100k` e, na construção, as skills que já existem (imagens-pagina-low, area-membros-netflix, banner-checkout-gpt, checkout-premium, ggcheckout-produto, wiven-checkout, hotmart-produto-playwright, criativo-ads, metaads-kevones). Registra tudo no Hub de Ofertas. Use quando o usuário pedir para criar uma oferta low ticket nova, minerar concepções, "vamos achar um produto para vender", rodar o processo do zero, retomar "onde paramos", "terminar/completar a entrega" (mapear promessa × área de membros e gerar o que falta — receita `references/TERMINAR-ENTREGA.md`), ou mencionar o Hub de Ofertas.
---

> **⛔ GATE DE PERSONA MECÂNICO (dona, 23/10/2026 — erro que não se repete):** antes de página, criativo,
> peça do funil ou preço, rodar `python3 ~/.claude/skills/criacao-low-ticket-mvt/scripts/gate-persona.py OFERTAS/<slug>`. **BLOQUEADO = não começa**; completa o
> `pesquisa/PERSONA-E-ANGULOS.md` no modelo `MODELOS/_MODELO-PERSONA-E-ANGULOS.md` (MERCADO na Biblioteca ≥5 anúncios,
> QUEM COMPRA DE VERDADE, dores com contagem+data, RECORTES com "por que está na oferta"). Casos: Elétrica estudou o
> estudante (comprador = eletricista na obra); Jiu usou "faixa branca/azul" (só vendeu quando tirou da página).
> **Pesquisa que alimenta (lição Atlas 23/10):** `criacao-low-ticket-mvt/references/PESQUISA-PADRAO-OFERTA.md` —
> Biblioteca 5 palavras + hashtag por idioma, YouTube/TikTok/Trends com contagem. O gate também cobra TERMOS DE
> BUSCA (nome do produto quase nunca é termo: "atlas" = 0 no Trends AR), unidade da peça, cena da dor,
> NARRATIVAS QUE RODAM (dias no ar) e ÂNCORA DE PREÇO.

> **TROCAR PÁGINA DE OFERTA (14/10/2026):** publicar página nova (V2, layout
> clonado, troca de funil) no lugar da atual = sempre levar o bloco fbq e o
> loader do Trackeador e rodar `adstrackeador pagina comparar <atual> <nova>`
> ANTES de promover. Incidente real: duas ofertas ficaram ~1h no ar sem pixel
> nenhum com anúncio rodando. Nunca publique página de oferta sem rastreio.

> **HUB DESATIVADO (02/10/2026, ordem da usuária):** NinjaBR Hub está SEM COTA e os perfis `hub`/`hubv2`/`hubts` foram removidos (backup em `~/.agent-profiles/_removidos-hub-2026-10-02/`). NÃO use Hub, NÃO rode `hub-livre.sh` (sai com erro), NÃO espere perfil do Hub liberar. Imagem: ChatGPT — se a cota de upload de uma conta acabar, troque de CONTA: `gpt-conta*` ↔ `gpt-conta*`. Vídeo: Google Flow (`flow-video-playwright`).


# Criação de oferta Low Ticket MVT — ORQUESTRADORA

> **REGRA FIXA DA DONA (repetida muitas vezes; não perguntar, não inventar alternativa):** área de membros é SEMPRE a NOSSA, externa, no site da oferta (`https://<site>/painel`). NUNCA a área de membros do checkout (Wiven, GG, Hotmart, Mundpay) nem página de obrigado genérica dele. Por isso: (1) redirect/página final pós-compra de TODA oferta e bump → `<site>/painel`; (2) link de entrega/e-mail do checkout, se existir → `<site>/painel`; (3) liberação por webhook no nosso servidor (e-mail → SKUs comprados); (4) e-mail de acesso pelo Resend da LeadGo (`no-reply@seudominio.com`) com o link do /painel e "entre com o e-mail da compra". Pronto só com venda-teste REAL provando: webhook liberou → login com o e-mail entra → e-mail chegou. Motivo: em 26/09/2026 a 1ª cliente do Mapa do Tarot BR pagou e não recebeu nada (webhook ignorava a venda, nenhum e-mail saía).

> **REGRA FIXA DA DONA (16/10/2026) — TODO produto/oferta criado entra nos DOIS webhooks NO MESMO DIA.** Não é só o principal. Vale pra **cada peça**: principal · **order bump** · **combo** · **Upsell 1/2** · **downsell** · **upgrade Essencial → Completo** · produto irmão/cross-sell · oferta de membro. Os webhooks da Wiven são **por produto** e nascem com **"Disparar para todos os produtos" OFF** — produto criado DEPOIS do webhook **não entra sozinho**. Obrigatório, na MESMA sessão do cadastro:
> 1. **Webhook da área de membros** (título `<Oferta> — área de membros`, URL `<site>/painel/api/webhooks/wiven`) → **marcar o produto novo na lista de produtos.**
> 2. **Webhook do Trackeador** (título `Trackeador — <oferta>`, URL `https://adstrackeador.leadgo.dev/api/webhooks/sale/c/<conexão>`) → **marcar o MESMO produto** (13 eventos — `wiven-checkout` §6).
> 3. **Servidor da oferta** (`site/server/index.mjs`) → o produto/offer entra no `PRODUCT_SKUS`/`COMPLETO_OFFERS`/`MUNDPAY_NAME_SKUS` (nosso lado).
> **Prova:** abrir `/panel/webhooks`, editar cada um e conferir que **TODOS** os produtos da oferta estão na lista — não só o principal. **Recontar depois de cada produto novo e depois de mexer em funil.** Produto fora do webhook = a Wiven não dispara nada ("Nenhum log de webhook encontrado"), a venda some do Trackeador/atribuição **e/ou** o comprador fica sem acesso — sem erro em lugar nenhum. Detalhe e incidente: `wiven-checkout` §6 · `mvt-funil` Passo 7.

**O método está em `low-ticket-metodo-mvt`. Leia o `SKILL.md` dela antes de começar** e
abra as references quando a etapa pedir. Esta skill só diz **o que fazer, em que ordem
e com quais ferramentas do nosso ambiente**. Não acrescenta regra ao método: onde o
método é omisso, decida com o usuário.

**Esta skill NÃO executa passo de método.** Ela roteia (ROTEADOR), ordena (TRILHAS), guarda o estado (ESTADO.md),
para nas 3 PARADAS e confere o GATE DE PASSAGEM. Cada passo tem sua skill MECÂNICA (índice abaixo); a regra de
cada passo mora só lá. Divisão feita em 24/09/2026 (decisão do dono) **sem mudar nenhuma regra** — mapa seção a seção em
`MINERACAO/RELATORIO-SPLIT-2026-09-24.md`.

Oferta para fora do Brasil com modelo "pague quanto quiser"/X1 → `x1-cross-market-mvt`.

> ⛔ **ANTES de qualquer passo da trilha, leia `references/ESTRUTURA-DE-PENSAMENTO.md`** — a ordem
> canônica `persona → dor → demanda orgânica → oferta → página → criativo → peças do funil`, com a
> contraprova do que a pessoa recebe na mão e a regra de dor-fora-do-escopo = bump/upsell.
> Regra da dona 10/10/2026: nada se cria antes de saber pra quem é e o que dói.

## ÍNDICE — onde mora cada coisa (passo da trilha → skill)

| Passo (TRILHA) | Skill MECÂNICA | O que ela tem |
|---|---|---|
| T2 MINERAR (todos os modos; modo D rastreadores; modo F recorte técnico→visual) | `mvt-minerar` | famílias de termos/Comandos 1-4, cota como parada, checklist 100k, 2 links, link não bloqueia, seguidores IG, falso-zero, mecânica Biblioteca, scripts link/preço, registro no Hub · **GATE 1** |
| T5 DESTRINCHAR + T7 MODELAR | `mvt-modelar` | 9 elementos, prova de leitura, raio X, mapa de personas, eliminar, 20→10→3, subnicho, prova≠leilão, elemento_mudado, território, descarte por método, pools evitados · **GATE 2 e 3** |
| T9 VALIDAR (e a medição da T8 usa a mesma mecânica) | `mvt-validar` | 3 fontes + TikTok/Uber Suggest, janelas, sinal de compra, obreiro×fiel, B2B técnico, demanda≠anúncio, mecânica Biblioteca/Trends/YouTube — **Trends SÓ no perfil `trends` (9234), nunca por HTTP (429)**, falso-positivo · **GATE 4** |
| T3 origem · T6 destino · T8 demanda no destino (só cross: B/B2/C/P/D-E-F-cross) | `mvt-cross-market` | gate de origem, gate de destino 2 etapas, quase-clone × MVT, playbook B2 França, divergências Heitor/Borba, gateway por região, oferta pontual → vários destinos, adendos §B/§E/§F · **GATE CROSS ORIGEM e DESTINO** |
| T11 OBRA DE ARTE 100K (+ conteúdo da Parada 3) | `mvt-obra-100k` | 8 elementos, bônus, garantia, mapa da vantagem, semáforo, regras da Obra, 8 erros · **GATE 5** |
| **Auditoria de irresistibilidade (oferta JÁ no ar, antes de qualquer leva de criativo nela)** | `references/AUDITORIA-IRRESISTIBILIDADE.md` | vira o lead na NOSSA página, nota 0-10 por alavanca, acha a mais fraca, melhora concreta no produto/bônus/bump/upsell (não só copy) — roda também como passo extra em T11 e em diagnóstico de queda de performance |
| **T13 funil (bônus · order bump · Upsell 1/2 · downsell · peça de FERRAMENTA/microSaaS)** | `mvt-funil` | pesquisa das peças (persona + o que o concorrente empilha), `FUNIL.md` com matriz anti-overlap e cadeia, preço na tabela da dona, MVP, gateway (delega `wiven-checkout`), entrega no `/painel`, webhook 2 destinos, gate de eventos, leitura por nó · regras em `references/PECAS-DO-FUNIL.md` · **bônus nunca vira produto no checkout** (regra 09/10, seção `## REGRA DO BÔNUS`) · **T13.24** |
| T13 CONSTRUÇÃO / T14 CONFIG / T15 TRÁFEGO | skills existentes (seção `## FASE DE CONSTRUÇÃO` abaixo) + `references/CONSTRUCAO.md` | ordem fixa, DESIGN-SYSTEM, MVP 40%, entrega=imagem, área de membros, padrões de low ticket, página/produto/criativo/config · **GATE 6 e 7** (nesta skill) |
| Prompt de todo pane | `references/PROMPT-PADRAO-PANE.md` | blocos obrigatórios, citado por todas as mecânicas |
| **Verificação mecânica** (todo passo) | `scripts/gate.py` + `references/TRILHA-CHECKLIST.yaml` · como usar/auditar: `mvt-auditar` | lista numerada T0…T15 + subpassos com evidência; exit ≠ 0 = não avança |


## REGRA DO BÔNUS × PLANO × BUMP (decisão da dona, 09/10/2026) — vale na T11, na T13 e no `/painel`

- **Bônus é do Plano Completo.** O **básico** leva **só o principal**; o **completo** leva
  **principal + todos os bônus**. Página promete igual: básico ✕ bônus · completo ✓ bônus.
- **Bônus NUNCA vira produto, oferta ou bump no checkout.** Bônus é **parte do produto**: quem paga
  a oferta do **Completo do mesmo produto** recebe `principal + bônus` num evento só (webhook
  `PRODUCT_SKUS` + `COMPLETO_OFFERS`); o básico libera **só** `principal`. Não existe "criar o
  produto Bônus X" na gateway — nem pra vender avulso, nem pra entregar.
- **Só order bump e upsell viram produto/oferta próprios** na gateway (item vendido à parte, preço
  próprio). Bônus entra no **produto**; bump é **produto solto**.
- Área de membros: card do bônus **sem preço próprio** → "Incluso no Completo" + o preço do Completo.
- **Caso real que motivou a regra (30/09/2026):** 4 produtos de bônus criados na Wiven (R$12,90,
  ofertas `9NJJEEC`/`QVQHVIX`/`ISRJ3UY`/`R635KZC`) — o webhook não os reconhecia, então quem pagasse
  não recebia nada. Reprodução proibida. Evidência: `OFERTAS/mapa-do-tarot/produto/UPSELL-CIGANO/TABELA-CHECKOUTS-MEMBROS.md`.
- Espalhamento: `_memoria/preferencias.md` › "Bônus × plano × bump".

## GATE DE PASSAGEM (regra desta skill — vale entre TODAS as mecânicas) — MECÂNICO, não de memória

**A passagem é verificada por SCRIPT, não por lembrança.** A lista de itens (todo passo e subpasso de todas as skills, com
ID `T7.2` etc., condição e evidência) mora em `references/TRILHA-CHECKLIST.yaml`; quem a confere é `scripts/gate.py`:
```fish
python3 ~/.claude/skills/criacao-low-ticket-mvt/scripts/gate.py --rodada "…/MINERACAO/<rodada>" --passo T7     # um passo
python3 ~/.claude/skills/criacao-low-ticket-mvt/scripts/gate.py --rodada "…/MINERACAO/<rodada>" --ate T12      # tudo até ali
```
Ele lê o bloco ROTEADOR do ESTADO (condições: R4 nicho, cross, modo…), os arquivos da rodada e de `OFERTAS/<slug>/` e o Hub
decifrado (se não estiver: `uv run cifrar.py --verificar` em `HUB-OFERTAS`), imprime OK/FALTA/N-A por item com a evidência
achada e **sai com código ≠ 0 se faltar item obrigatório**. Como usar e o que fazer com FALTA: skill `mvt-auditar`.

**Rode `gate.py` (a) antes de chamar a próxima mecânica, (b) antes de TODA Parada (T4, T10, T12) e (c) antes de liberar construção
(T13).** Cole a saída (a linha `RESULTADO` + os FALTA/DONO) no `ESTADO.md` com a data — o gate exige a linha `gate.py … Tn` e a do
Verificador Haiku (abaixo). **Saída ≠ 0 = NÃO avança e NÃO pergunta ao dono: a próxima ação é fechar cada FALTA** (voltar à
mecânica do item, cujo ID diz a `skill_fonte`). Só o dono dispensa item, por escrito, e vira linha `ABERTO-POR-DECISÃO` no ESTADO
(o gate imprime `[DONO]`); iniciativa própria de atalho é proibida (ver ROTEADOR). Gate que falha por evidência mal-nomeada
(arquivo fora do padrão de nome) → renomear/gravar a evidência, não mexer no YAML para passar.

**Verificador Haiku obrigatório em cada Parada (T4, T10, T12).** Antes de apresentar ao dono, despache um subagente `model: haiku`
com: o `TRILHA-CHECKLIST.yaml`, a saída do `gate.py --ate <passo da Parada>` e os artefatos citados; ele confere item a item se a
evidência é REAL (não só existe: abre o arquivo e diz se o conteúdo cumpre o item — ex.: `persona-*.md` tem 10 dores urgentes mesmo?)
e devolve lista de furos. Furo = fecha antes de apresentar. Cole no ESTADO `Verificador Haiku P1|P2|P3: <data> — <n furos, todos fechados>`.
Nunca apresentar Parada sem esta linha e sem `gate.py` exit 0.

**Regra de PIVÔ** (uma só, aqui): qualquer concepção/mecanismo/oferta **NOVO que surja depois do T7** (concorrente derruba a premissa,
achado transversal, "e se…", ideia do dono ou de worker) **RE-ENTRA na trilha em T7 como concepção nova**: persona-first/Comando 4
quando há persona (R4 nicho) → funil 20→10→3 → `elemento_mudado` → território → **T9 completo** (3 fontes YouTube·TikTok·Trends +
`sinal_de_compra` + urgência PRÓPRIOS da nova) → **Parada 2** formal (PARADA-2 citando a nova + aprovação datada) → T11 → **Parada 3**.
Proibido "lista de alternativas → Obra". A Obra existente vira `PAUSADA`/`pivô` no ESTADO até a nova fechar T9/T10. O gate acusa
(`T7.13`, `T9.8`, `T10.4`): toda oferta com `obra-de-arte.md` precisa de modelagem, medição e Parada 2 PRÓPRIAS.

**OCUPAÇÃO POR MECANISMO é parte do T9 [decisão do dono 25/09/2026]:** por finalista, `concorrencia-<id>.md` (T9.13, regra em `mvt-validar`) ANTES da Parada 2 e da Obra; sem ele T9 não fecha, Parada 2 não abre (T10.0), Obra não é montada. T11.8 = re-conferência; T13.19 = frescor ≤48h.
**LIÇÃO R7 (3 casos — "ninguém vende" saiu de 1 busca específica e o concorrente só apareceu DEPOIS da Obra):** orçamento elétrico → Ajuda Eletricista (R$37, desde 14/09); gerador de PMOC → Kit PMOC Pronto (R$19,90); dimensionador → 80 Diagramas (R$10/27, com app-bônus). Por isso a regra acima vale por MECANISMO, com ~10 termos do comprador e página de todo anunciante aberta.

**"Ninguém vende" = checado pelo MECANISMO** (o que o concorrente ENTREGA), não só pelo termo de busca: antes da Parada 3, cada Obra
carrega `OFERTAS/<slug>/pesquisa/checagem-mecanismo*.md` com concorrentes achados por mecanismo e página ABERTA (URL + o que entrega). Regra
completa em `mvt-obra-100k` (item T11.8); aqui só o ponteiro.

Antes de chamar a próxima mecânica, confira ainda que a SAÍDA da anterior EXISTE — arquivo (`test -f` / `ls`), campo do Hub (contador-base abaixo) ou
contador colado no `ESTADO.md`; o `gate.py` é essa conferência automatizada. **Não existe = passo ABERTO**: a próxima ação é fechá-lo, nunca chamar a seguinte,
nunca "voltar depois". Cada mecânica começa por `ENTRADA EXIGIDA` e termina por `GATE DE SAÍDA` (cada subpasso com o ID do YAML); a orquestradora só marca o passo
FECHADO com a saída COLADA no `ESTADO.md`. Ordem entre as mecânicas = a coluna ENTRADA/SAÍDA da tabela de passos-mestre (T0-T15) e a TRILHA do modo.

## REGRA DE FALA — o que pode ser dito ao dono [decisão do dono 25/09/2026] (regra ÚNICA; as outras skills só apontam para cá)

Falha que originou: `MINERACAO/FALHA-OFERTA-NAO-VALIDADA-2026-09-25.md` (tabela de "ideias" apresentada como ofertas, sem mineração nem validação).
1. **TAG obrigatória.** Toda concepção/ideia/produto citada ao dono leva a tag do seu status REAL (conferido no Hub/ESTADO, nunca de cabeça): `[HIPÓTESE — não minerada, não medida]` · `[MINERADA T2]` · `[VALIDADA T9]` · `[OBRA T11 + cor]` · `[LIBERADA T12]`. **HIPÓTESE nunca aparece como oferta:** proibido tabela de "ideias" com formato/dor/preço, proibido "dá pra vender X", proibido recomendar construir.
2. **Pergunta aberta do dono** ("o que vender em X?", "o que seria legal pra Y?", "tem algo pra Z?") **= começo de trabalho, não pedido de opinião.** Abre o ROTEADOR (R1-R5); a resposta máxima é o **PLANO DE MINERAÇÃO** (modo, público, termos, pedido de ok). **Proibido responder com lista de ideias.**
3. **Ideia gerada** (persona-first, Comando 4, brainstorm, rota "gerar concepção do zero" do método §8) só existe DENTRO do T7 como candidata do funil 20→10→3 e precisa de **PROVA DE MERCADO** (T7.30, `mvt-modelar`) antes de seguir; sem prova = DESCARTE/PENDENTE, nunca Obra.
5. **SEM "MODO OPINIÃO"** [decisão do dono 25/09/2026]: com esta skill ativa, TODA pergunta do dono é trabalho dentro do método ("quando estou criando produto não estou pedindo opinião; se quisesse opinião abria um chat qualquer"). Se algo não cabe num passo, a resposta diz em qual passo cai e o que falta — nunca resposta solta.
4. **Antes de enviar** qualquer mensagem que cite concepções: AUDITORIA DE FALA (`mvt-auditar` §6).

## ROTEADOR — que tipo de trabalho é este?

**REGRA GERAL (dono, 24/09/2026): NÃO EXISTE PULAR ETAPA.** Tudo isto é um método: cada passo tem
ENTRADA exigida e SAÍDA verificável (arquivo, campo do Hub, contador colado). Passo sem SAÍDA
verificada = ABERTO, e a próxima ação é fechá-lo — nunca avançar, nunca "voltar depois".
- **Falta de dado nunca pula nem elimina.** Sem link, preço, seguidor, print, página no ar: anota
  `PENDENTE (motivo, data)` no campo e SEGUE no fluxo e no gate (memória `link-pagina-nao-bloqueia`).
  Pendência é registro, não filtro; só cai do ciclo o que tem motivo de MÉTODO escrito.
- **Atalho só do dono.** Se o dono pedir para pular/juntar/adiar um passo, faça o que ele pediu MAS
  registre no `ESTADO.md`, em "Decisões tomadas", como **decisão dele com data** ("dono pediu X em
  DD/MM/AAAA; passo N fica ABERTO-POR-DECISÃO"). Iniciativa própria de atalho é proibida; quem vê
  "opcional", "se quiser" ou "pode" nesta skill lê como "faça, a menos que o dono dispense por escrito".
- **Números do método com "~" ou "≥~" (cota ~6, ~30 queries, ≥~15 dias, 3-5 criativos ≥7 d) valem como o número EXATO** escrito; só o dono dispensa, com data (buraco 54c).
- **Sem roteamento gravado = nada começa.** Nenhuma busca, nenhum pane, nenhuma escrita no Hub antes
  de R1-R5 estarem gravados no ESTADO, repetidos ao dono em 1 linha (o eco) **e o dono responder "ok"** — linha `ok do dono (DD/MM/AAAA)` no ESTADO (decisão do dono 25/09/2026 (revisão)). Sem o ok, T0 não fecha.

### Árvore de decisão — a IA responde e GRAVA antes de qualquer ação

**R1 · Que tipo de trabalho?** (uma resposta)
1. **Mineração NOVA** (rodada nova) → segue R2-R5, depois a TRILHA do modo.
   - **[decisão do dono 25/09/2026]** Mineração nova = do ZERO. Nada de rodada anterior entra por iniciativa própria: não excluir áreas/termos já minerados antes, não usar rodada antiga como referência de concorrente, não reaproveitar concepções. Se reaproveitar parecer útil, PERGUNTAR ao dono antes (1 pergunta) e registrar a resposta no ESTADO. (Origem R8: serralheria/elétrica/hidráulica foram cortadas e a R7 usada de referência sem perguntar.)
2. **RETOMADA** (rodada em andamento, "onde paramos") → TRILHA R abaixo.
3. **CONSTRUÇÃO de oferta já escolhida** (Obra verde + Parada 3 liberada) → TRILHA K abaixo.
Não dá pra classificar → pergunte em UMA linha; nunca presuma.

**R2 · Se mineração: qual MODO?** (percorra as perguntas em ordem; a 1ª que der "sim" decide)
| Pergunta | Sim → modo |
|---|---|
| O dono trouxe UMA oferta/ideia pontual ("dá pra vender isso em X?")? | **P — oferta pontual** (ideia sem concepção: exigir 1 frase "N coisas para <público>" + os 4 elementos antes) |
| A fonte é rastreador externo (urlscan/utmify, reclamação-recência, SEMrush-plataforma, sitemap)? | **D — oferta-first** |
| Parte de território/oferta escalada para trocar o FORMATO de PDF/apostila técnica → visual (mapa mental/esquema/infográfico)? | **F — recorte de mecanismo "PDF → visual"** |
| Parte de território/oferta escalada para estreitar o público (ou ampliar a fatia)? | **E — sub-nicho / recorte** |
| Destino = Europa francófona (FR/BE/CH/CA, em francês), origem BR **ou** EN? | **B2** |
| Origem BR/Latam (ou qualquer mercado) e destino OUTRO idioma/país? | **B — origem → fora** |
| Origem fora (EN/ES/FR…) e destino BR? | **C — fora → BR** |
| Origem = destino = BR, sem concepção de partida? | **A — do zero** |
Modos combináveis (**decisão do dono 24/09/2026**: um modo principal + saída de mercado): D/E/F **acham** a concepção; se a saída do leilão for o eixo MERCADO, a trilha continua
como B/B2/C. Grave "modo primário + combinado com" (ex.: `F + B2`). Oferta X1 / "pague quanto quiser" →
skill `x1-cross-market-mvt`, fora desta trilha (registrar no ESTADO).

**R3 · Mercado de ORIGEM e de DESTINO** — país + idioma de cada um (ex.: origem BR/pt-BR → destino FR/fr).
Cross (B/B2/C/P/D-cross): origem ≠ destino, obrigatório. A: BR/pt-BR nos dois. Pontual (P): destino =
lista de candidatos (todos os que o dono citou; nenhum "escolhido no chute").
**R4 · Nicho/persona ou AMPLO?** "Amplo" + filtro de formato (ex.: visual) é válido e NÃO é nicho —
registrar como "nicho amplo, filtro de formato X". Com nicho/persona: registrar quais comandos (2/3/4) rodam.
**R5 · Faixa de preço da rodada** (**decisão do dono 24/09/2026**: "sem faixa" é o padrão e só trava se o dono disser): "sem faixa" (padrão; valor sai na Obra) OU faixa declarada pelo dono.
Nunca inventar nem herdar (memória `mvt-sem-alvo-de-preco`). Teto de complexidade do entregável: padrão
Rápido+Ferramenta; só muda se o dono disser.

**Bloco obrigatório no topo de `MINERACAO/<rodada>/ESTADO.md`:**
```markdown
## ROTEADOR (gravado DD/MM/AAAA HH:MM — antes de qualquer ação)
R1 tipo: mineração nova | retomada | construção
R2 modo: <A|B|B2|C|D|E|F|P> (combinado com: <—|X>)
R3 origem: <país/idioma> → destino: <país/idioma | lista de candidatos>
R4 nicho/persona: <amplo | nicho X> · filtro de formato: <—|visual|…> · comandos: <1|1+2+3+4>
R5 faixa de preço: <sem faixa | R$ x/y declarada pelo dono em DD/MM> · teto entregável: Rápido+Ferramenta
Eco ao dono (1 linha): "<o que vou fazer, em qual mercado, com qual trilha>"
ok do dono (DD/MM/AAAA): "<frase do dono>"   ← EXIGIDO antes de começar; sem essa linha T0 não fecha
```
**Mudança do dono em R2-R5 no meio da rodada** (ex.: ampliou o nicho) = NOVO bloco `## ROTEADOR` datado + nota "o que já foi feito continua valendo / refazer" + eco + novo `ok do dono (data)`; nunca editar o antigo em silêncio (buraco 31). Campo faltando → PERGUNTE (1 linha) antes; roteamento incompleto não abre o GATE 0.

---

## TRILHAS POR MODO — passos numerados, ENTRADA exigida, SAÍDA verificável


Os GATES (cada um mora na skill mecânica do seu passo — ver `## ÍNDICE`; os de CONSTRUÇÃO/TRÁFEGO estão nesta skill) definem os itens de cada passo. A trilha diz **em que
ordem** eles rodam em cada modo e **o que tem que existir antes** de cada um. Não duplicar: onde diz
"GATE n", o critério é o que está na mecânica. Antes de cada passo, confira a ENTRADA (arquivo/contador); depois,
cole a SAÍDA no ESTADO. ENTRADA ausente = volte ao passo aberto.

### Passos-mestre (a ordem do método)
| Passo | O que é | ENTRADA exigida | SAÍDA verificável | Gate |
|---|---|---|---|---|
| **T0** | ROTEAR | — | bloco `## ROTEADOR` (R1-R5) no ESTADO + eco ao dono + linha `ok do dono (data)` | ROTEADOR |
| **T1** | Abrir | T0 gravado | 4 evidências do GATE 0 coladas (método lido, ESTADO, Hub `bate: True`, modo/nicho/preço) | GATE 0 |
| **T2** | MINERAR / obter a concepção (varia por modo) | T1 | concepções no Hub (`total` == lotes) · `raw-<termo>.json` · tabela termo→nº · checklist 100k · seguidores IG e 2 links já na varredura | GATE 1 (exceto Parada) |
| **T3** | GATE DE ORIGEM — só cross (B, B2, C, P, D/E/F-cross) | T2 (IG + link + datas colhidos na varredura) | `gate_origem` em 100% (`PASSA`/`NAO_PASSA`+motivo/`PENDENTE`); só `PASSA` segue como quase-clone | GATE CROSS · ORIGEM |
| **T4** | ⏸ PARADA 1 | GATE 1 (+T3) fechados, contador colado | aprovação do dono no ESTADO (data + lista das que seguem) | FORMATO DAS PARADAS |
| **T5** | DESTRINCHAR os 9 elementos | T4 | `elementos` + ★ em 100% das que seguem · `prova_leitura` · pensamento interno 2+2 · urgência | GATE 2 |
| **T6** | GAP NO DESTINO — só cross (ordem do dono: Biblioteca PRIMEIRO): ~10 termos NATIVOS por idioma, Biblioteca `country=ALL` em TODOS os destinos; OCUPADO/gap de ângulo vai p/ MVT (subnicho/ângulo/formato), não descarta | T5 + lista dos 10 termos por idioma | destino classificado (gap puro · gap de ângulo · OCUPADO) → decide T7: **gap puro = quase-clone com adaptação cultural, SEM modelagem de elemento**; OCUPADO/gap de ângulo = T7 modela | GATE DESTINO · etapa 1 |
| **T7** | MODELAR 20 → 10 → 3 — mesmo mercado (A/E/F-BR): sempre, logo após T5. Cross: só se T6 deu OCUPADO/gap de ângulo (MVT subnicho/ângulo/formato); gap puro só registra a adaptação cultural (`elemento_mudado: nenhum — mercado`). Cross: depois de modelar, **gap DO RECORTE** na Biblioteca do destino → candidatos | T5 fechado (mesmo mercado) ou T6 (cross) | tabela 20→10→3 + `o que é` em `modelagem-<lote>.md` · frase/elemento_mudado/território/3 comunicações · comando de decisão · cross: tabela recortes×gap → **lista de CANDIDATOS** (nunca ranking) | GATE 3 (+ GATE DESTINO · etapa 1) |
| **T8** | DEMANDA + SINAL DE COMPRA + URGÊNCIA — só nos candidatos | T6 (gap puro) e/ou T7 (candidatos de recorte) | por candidato: **GATE DE DEMANDA (viral + comentário recente)** — YouTube/Shorts **≥100k views**, TikTok **≥1M**, Reels **≥100k**, FB **≥500k** + **comentário de até ~6m** (3m quente; 3-12m ainda válido) + **mais de um vídeo** falando disso. **Vídeo pode ser antigo: não exija recência do vídeo** (dono 10/10/2026) · TikTok orgânico · Trends · `sinal_de_compra` · urgência (fiel × obreiro) · gateway | GATE DESTINO · etapa 2 |
| **T9** | VALIDAR a comunicação modelada (no país/idioma de DESTINO) | T7 (A/E/F/D-BR) ou T8 (cross) | `sem territorio: 0` · ≤10 finalistas com Biblioteca específica+território+controle + as 3 fontes + sinal + urgência | GATE 4 |
| **T10** | ⏸ PARADA 2 | GATE 4 (e etapa 2 se cross) fechados | aprovação da direção no ESTADO (data) | FORMATO DAS PARADAS |
| **T10b** | **PESCISA DAS PEÇAS DO FUNIL — OB/upsell 1/upsell 2 ANTES da arte** (dono, 10/10/2026: "a pesquisa tinha que estar rolando desde que começamos a arte") | T10 (direção aprovada) + passar pelo **GATE DE DEMANDA** (T8) | por peça (OB, upsell 1, upsell 2): dor validada (viral + comentário ≤~6m + volume de vídeos) · **é a PRÓXIMA coisa que ele precisa depois de comprar o principal** · formato decidido (PDF · template · planilha · **web app plug-and-play** · microsite) · quem é o público da peça | GATE DESTINO · etapa 2 + `mvt-funil` |
| **T11** | OBRA DE ARTE 100K + mapa da vantagem + semáforo | T10 **+ T10b** | `OFERTAS/<id>/pesquisa/obra-de-arte.md` (`test -f`) · `semaforo`+`semaforo_motivo` · 8 erros OK/NÃO | GATE 5 |
| **T12** | ⏸ PARADA 3 | GATE 5 fechado; 3-5 Obras verdes | "libera operação" no ESTADO (data) | FORMATO DAS PARADAS |
| **T13** | CONSTRUÇÃO na ordem fixa: página → entrega em texto + amostra → **paleta fechada no HTML → mockups da página (1 chat GPT: URL ref + nosso HTML + imagens dela, refazer pro nosso produto) → dona valida** → MVP ≥10 págs → imagens "por dentro" com o MVP de ref → área de membros → banner → checkout → criativo (3-5) | T12 liberado | cada item = arquivo existente (BLOCOS/COPY, `ENTREGA/*`, DESIGN-SYSTEM, mockups, banners, checkout, `roteiro-*.md` 11 linhas) | GATE 6 |
| **T14** | CONFIGURAÇÕES TÉCNICAS | T13 | checklist do board linha a linha no ESTADO | GATE 6 · config |
| **T15** | TRÁFEGO — só ponteiro `metaads-kevones` | T14 + página no ar + checkout + 3-5 criativos | linha "entregue ao dono p/ tráfego" no ESTADO | GATE 7 |

### Trilha por modo (mesma ordem; o que muda está em negrito)
**A — do zero (BR → BR).** T0 → T1 → **T2** (Comando 1 amplo sem nicho; se R4 tem nicho, Comandos 2/3/4 também;
3-7 termos; cota ~6/termo = PARADA; seguidores IG entram como sinal SUAVE, não corte) → T4 → T5 → T7
(**sair do leilão por ≥1 eixo: público/ângulo/formato — clonar BR→BR é proibido**) → **T9** (sem T3/T6/T8: não
há origem/destino de outro mercado) → T10 → T11 → T12 → T13 → T14 → T15.
**B — origem → fora (BR/Latam/qualquer → outro idioma).** T0 → T1 → **T2 no mercado de ORIGEM** → **T3 (obrigatório)**
→ T4 → T5 → **T6 gap destino** → (só `PASSA`: gap puro = quase-clone cultural, `elemento_mudado: nenhum — mercado`, sem T7; OCUPADO/gap de ângulo = **T7 modelar + gap do recorte**; origem PRÓPRIA morta
= risco pago, ver divergência Borba) → **T8** → T9 → T10 → T11 → T12 → T13 → T14 → T15.
**B2 — Europa francófona.** Igual a B com: T2 por **dois eixos** (formato×nicho **e** busca por preço na copy, `country=ALL`);
**T6 com ~10 termos em FRANCÊS não-literal**, Biblioteca em FR/BE/CH/CA; T8 com "où acheter/combien" como sinal;
gateway card-first (+PayPal); T13 com os 5 PADRÕES e funil (bumps relacionados + microSaaS); página/entrega NOSSAS.
**C — fora → BR.** Igual a B com origem fora e **destino BR**: T2 na Biblioteca do país de origem; T3; T6 = Biblioteca BR com
~10 termos nativos pt-BR (ninguém rodando igual no BR, ou só em outro ângulo); T8 com demanda BR; gateway = método local (PIX).
**D — oferta-first (rastreador).** T0 → T1 → **T2 = §E do ADENDO** (urlscan/utmify · reclamação-recência · SEMrush · sitemap →
achou a oferta → **saída do leilão (§A: mercado/público/ângulo/formato)** → confirma na Biblioteca → registra no Hub) → se a
saída foi MERCADO: T3 → … como B/B2/C; se foi público/ângulo/formato: T4 → T5 → T7 → T9 → … como A. Toda oferta achada volta
ao gate padrão; rastreador só semeia.
**E — sub-nicho / recorte.** T0 → T1 → **T2 = partida** (território/oferta escalada já no Hub ou achada) → **estreitar/ampliar** por
Comando 2 + mapa de personas + IA ("10 subnichos com dor mais latente") → T4 → T5 → T7 (sub-nicho de 1ª classe; funil 20→10→3 em
`funil_subnicho`) → **T9 em 3 camadas barato→caro** (1 território do subnicho >0 · 2 comunicação livre = vaga · 3 demanda orgânica +
`sinal_de_compra` >0; só avança quem passa a anterior; **fundo só se a demanda foi MEDIDA**) → T10 → … Cross combinado → inclui T3/T7/T8.
**F — recorte de mecanismo "PDF/apostila técnica → visual" (NOVO modo; era o adendo §D).** T0 → T1 →
**T2 em 4 sub-passos, todos com saída no Hub/ESTADO:** **F1** buscar o FORMATO genérico + ofício/área (`apostila`/`pdf`/`pack` × área técnica) ·
**F2** confirmar TERRITÓRIO GRANDE com demanda provada no genérico (≥~100 anúncios; sem território grande não há o que recortar) ·
**F3** medir a versão VISUAL (`mapa mental`/`esquema visual`/`infográfico` × mesma área): específica + território, com controle ·
**F4** (zero da Biblioteca = vaga de formato PROVISÓRIA até `concorrencia-<id>.md`, T9.13) **zero confirmado (4 tentativas limpas, `q` preenchido, controle bom) = VAGA de formato**; número >0 = ocupado → troca de direção, não insiste.
Registrar cada concepção com `elemento_mudado: formato` + `evidencia_formato` (o público da área já usa/quer visual? — ressalva
"depende do público": público que imprime → PDF visual) → T4 → T5 → T7 ("mapa mental" é ÂNGULO de venda; a entrega segue padrão: imagem por
página → área de membros) → T9 → T10 → … Sustenta ticket acima da base (registrar em `sustenta_preco` só na T11). Cross combinado → T3/T7/T8.
**P — oferta pontual trazida pelo dono.** T0 → T1 → **T2 = orquestrador abre a página e salva `REFERENCIA.md`** (concepção, entrega, bônus,
o que PROTEGE a oferta) — sem isso não se escolhe destino → **T3 no mercado de origem** → T4 (Parada 1 = a referência + o gate de origem)
→ T5 → **T6 em PARALELO nos destinos** (panes com perfis diferentes, termos nativos não-literais, `country=ALL`; **máx. 1-2 panes
simultâneos na Biblioteca** — idiomas extras esperam vaga ou vão em sequência) → T8 só nos candidatos → **ranking de mercados só com as 3 colunas
(gap · demanda · urgência) + gateway (Latam = método local; IT/FR/EN = cartão)** (gap puro: quase-clone cultural; OCUPADO/gap de ângulo: T7 modela + gap do recorte, antes da demanda) → T9 → T10 → … Ideia sem concepção → não mede; pede os 4 elementos.
**K — construção de oferta já escolhida.** ENTRADA (todas conferidas, cole a saída): `test -f OFERTAS/<id>/pesquisa/obra-de-arte.md` · `semaforo: VERDE` +
motivo · 8 erros OK/NÃO · linha "Parada 3 liberada (data)" no ESTADO · se cross: `gate_origem: PASSA` + etapa 2 fechada + gateway definido. **Qualquer
uma ausente → NÃO constrói: volta ao passo aberto pela TRILHA do modo original.** **Mais (25/09/2026, `references/CONSTRUCAO-GATES.md`):** `checagem-pre-construcao.md` ≤48 h (T13.19: re-checagem de concorrente por mecanismo + preço dos 2 do mapa; concorrente novo/preço mudou = volta a T11) · semáforo só VERDE (condição pendente = AMARELA; "VERDE com condição liberado pelo dono" só com linha `CONDIÇÃO → id·responsável·prazo·evidência` que vira item bloqueante de T13) · se o entregável é APP → trilha K-APP (T13.10–T13.14). Depois: T13 → T14 → T15.
**R — retomada.** T0' = ler `ESTADO.md` (existe bloco ROTEADOR? **Rodada antiga sem ROTEADOR → grave-o agora, antes de agir, preenchendo SÓ o que está escrito; o resto = `DESCONHECIDO` → 1 pergunta ao dono (nunca deduzir R5)**) → PASSO 0b (Hub) →
rodar o contador-base e o de Condução → dizer em 1 linha o passo atual → revalidar o perecível (`pane_list` + perfis vivos; medição >7 dias = re-controle `emagrecer` antes de reusar; tabela pane→perfil reconciliada) e executar o **primeiro passo ABERTO** da trilha do modo. Nunca "continuar de onde
parece", nunca confiar no texto do ESTADO sem contar.

### FORMATO DAS PARADAS (⏸ = aprovação do dono; nenhuma é pulável, nenhuma abre sem os gates do passo anterior)
Comum às três: `gate.py --ate <passo>` exit 0 + Verificador Haiku colados (ver GATE DE PASSAGEM) · contador do passo colado · resultado + **recomendação com o porquê** (nunca menu sem opinião) · **sem AskUserQuestion antes de fechar os
itens do gate** · depois de apresentar, PARA e espera · aprovação vira linha no ESTADO com **a frase VERBATIM do dono + a lista/IDs exatos do que foi liberado** (aprovação genérica sem lista não vale; T4.4/T10.3/T12.3) · **antes da Parada 2, tabela de DESCARTES por método** (concepção · regra de `mvt-modelar` citada · trecho) para o dono resgatar (T7.15; descarte sem motivo citado é inválido).
- **⏸ Parada 1 (T4)** — tabela: concepção · formato · mecanismo · público · **os 2 links + print** (ou `PENDENTE (motivo, data)` — nunca coluna sumida) ·
  **por que passa no checklist 100k** · `gate_origem` (cross) · cota por termo. Faltou coluna sem PENDENTE = não apresento.
- **⏸ Parada 2 (T10)** — por concepção: 1-3 modelagens (frase · elemento mudado · território · 3 comunicações) · resultado do comando de decisão · validação com **o que foi
  medido e o que ficou "não medido"** (Biblioteca específica+território+controle · YouTube · Trends · TikTok · `sinal_de_compra` · urgência) · cross: tabela
  candidatos × gap × demanda × sinal × urgência × gateway. Fonte faltando = a finalista não fecha, e aparece como tal.
- **⏸ Parada 3 (T12)** — tabela do semáforo (obra · cor · motivo · ajuste tentado) · Obra(s) verde(s) INTEIRA(s) · **1 linha OK/NÃO por erro do board "8 erros"** em cada
  verde (um NÃO = não libera) · pergunta explícita "libera a parte operacional?". **Menos de 3 Obras verdes:** libera a(s) verde(s) e segue montando Obra das próximas da fila até 3 na esteira, registrado no ESTADO (T12.4, decisão do dono 25/09/2026); proibido reclassificar cor para completar 3.
Liberada a Parada 3, toque T13→T15 sem nova parada — mas **os itens do GATE 6/7 continuam valendo** e qualquer bloqueio volta ao passo aberto.

---

## Convenção de pastas (obrigatória — manter tudo organizado)

Padrão da skill `organizar-projeto` (fonte única: `~/.claude/skills/organizar-projeto/references/estrutura-padrao.md`).
Raiz do projeto e raiz de cada oferta = **só .md + pastas**. NUNCA imagem, print, `.zip` solto.

```
LOW-TICKET/OFERTAS/<slug>/
  CLAUDE.md  STATUS.md  DESIGN-SYSTEM.md      # contexto+skills da oferta · estado · identidade
  pesquisa/        obra-de-arte.md, checagem-mecanismo*.md, oferta.md, referencia/, CLONE-ORIGINAL, prints/ da mineração
  produto/         ENTREGA/{BASICO,COMPLETO,BONUS-*,ORDER-BUMPS/<slug>}  MOCKUPS-NOSSOS/  IDENTIDADE-REF/  texto/
  site/            página de vendas (BLOCOS.md, COPY.md, index.html) + painel/ — repo git do deploy
  checkout/        banners/, order-bumps/, upsell/, config do gateway (.md)
  criativos/       [<MERCADO>/]CRIATIVO-<N>[-slug]/ (final solto + intermediarios/) · MATERIAL-ENTREGAVEL/ · _broll/
  instagram/       stories/posts orgânicos da oferta (depoimento, bastidor)
  trafego/         campanhas, relatórios
  prints/          QA e prova de gate (por propósito)
  _arquivo/        versão velha, revogado, lixo conferido
```
- **`LOW-TICKET/KEVONES/MUDANCAS.md`** = registro **único** das mudanças de preço/ticket/bump,
  página/headline, público, verba e **troca de anúncio** de TODA oferta, com o campo **"→ Como ler"**.
  Toda mudança feita nesta trilha entra lá **na hora**; as análises de tráfego leem o arquivo
  inteiro antes de decidir (regra da dona 09/10/2026).
- O gate (`scripts/gate.py`) acha `obra-de-arte.md` / `checagem-*` na raiz OU em `pesquisa/`, e `pagina/` OU `site/`. Oferta nova: use `pesquisa/` e `site/`.
- Print → `prints/` (QA) ou `pesquisa/prints/` (mineração). Criativo: final na raiz do CRIATIVO-N, intermediários em `intermediarios/`. Nada em /tmp.
- Achou arquivo solto → mover pro destino (não deletar sem conferir se é lixo).

```
PASSO 0 · abrir o Hub
1 · MINERAR ─────────────────────────► ⏸ parada 1 (quais concepções seguem)
2 · DESTRINCHAR os 9 elementos de todas
3 · MODELAR (eliminar → rascunho ~10 ideias → 1-3 modelagens por concepção → comando de decisão)
4 · VALIDAR a comunicação modelada ──► ⏸ parada 2 (qual direção)
5 · OBRA DE ARTE 100K ───────────────► ⏸ parada 3 (libera a operação)
6 · PÁGINA → 7 · PRODUTO → 8 · CRIATIVO → 9 · CONFIGURAÇÕES → 10 · TRÁFEGO (ponteiro: `metaads-kevones`)
```

As paradas são pontos de aprovação do usuário, não etapas do método. Entre elas, siga
sem pedir confirmação de passo intermediário. Em cada parada: resultado + recomendação
com o porquê + espera.

---

---

## PASSO 0a · LER O ESTADO — antes de qualquer coisa

`MINERACAO/<rodada>/ESTADO.md` é a fonte de verdade do andamento. **Contador do Hub/arquivos VENCE o texto do ESTADO; divergência = passo aberto + correção do ESTADO (buraco 28).** **Leia esse arquivo antes de
tocar em qualquer etapa, inclusive ao retomar sessão, e atualize a cada mudança de estado.**
Erro real 18/09/2026: sem esse arquivo eu li o Hub, vi campo vazio e concluí que 36 concepções
não tinham sido modeladas — já estavam, em arquivo, só não registradas. E montei a Obra de Arte
(passo 5) com o passo 3 aberto.

Formato (uma linha por passo, sempre com número, nunca com "quase" ou "quase tudo"):

```markdown
# ESTADO — rodada <N> · atualizado <data/hora>

## ROTEADOR (ver seção ROTEADOR — R1-R5 gravados ANTES de qualquer ação)

| Passo | Estado | Números | Onde está |
|---|---|---|---|
| T2 MINERAR | FECHADO | 243/243 | Hub `concepcoes` (243 registros) |
| T5-T7 DESTRINCHAR+MODELAR | FECHADO | 243/243 | modelagem-lote*.md |
| T9 VALIDAR | EM ANDAMENTO | 386 medidas / 282 na fila | rz-validos.jsonl, fila.txt |
| T11 OBRA DE ARTE | NÃO INICIADO | 0/3-5 | — |
| T13 CONSTRUÇÃO / T14 CONFIG / T15 TRÁFEGO | NÃO INICIADO | — | — (só depois da Parada 3 liberada) |

## Gate atual
Passo 4 aberto. NADA do passo 5 em diante começa antes dele fechar.

## Em andamento agora
- 5 panes medindo; pontos de retomada: N023 · N179 · X0303 · X2111
- IP bloqueado desde 15:0x — panes parados

## Decisões tomadas (não re-litigar)
- leva-1 = 52 concepções, cota de nicho; 184 em proximas-levas
- sem faixa de preço travada nesta rodada
- atalho do dono (só ele pede; sempre com data): "DD/MM — dono pediu X; passo N ABERTO-POR-DECISÃO"
```

**Regra dos gates:** só avança para o passo N+1 quando o passo N está FECHADO nas 100%. Passo com
buraco → o próximo passo é fechar o buraco, não seguir com o que já dá. Ao retomar, diga em uma
linha o passo atual antes de agir, e confira o número contando (PASSO 0b), não confiando no texto.

**A fase de CONSTRUÇÃO (passos 6-8, depois de escolhida a concepção vencedora) tem ordem própria e
regras próprias — estão consolidadas na seção `## FASE DE CONSTRUÇÃO` logo antes do passo 6.** Não
repetir aqui: este passo 0a é só sobre o arquivo de estado e os gates de mineração/validação.

**Ritmo de referência do Heitor** (o tempo vai para PENSAR, não para medir; referência, não gate): dia 1 minerar (recomenda 50) → dia 2 entender/destrinchar todas [04:11:30] "segundo dia você só vai ficar entendendo aquela concepção" → dias 2-3 modelar 1-3 direções por concepção → dias 3-4 montar 3-5 Obras (≈30 min cada, [05:29:03] "a gente consegue montar em 30 minutinhos"). [cauda ≈11:09] "usa um dia para cada fluxo"; [cauda ≈11:11] "a sua primeira concepção, ela vai sair com 7 dias, mais ou menos", depois [cauda ≈11:11] "esse número fica entre 3 e 5 dias para você lançar uma nova concepção"; [cauda ≈11:12] "é muito melhor você ter assertividade do que velocidade". Passou de 1 dia num passo estratégico sem fechar → escreva no ESTADO o porquê + qual item do gate está bloqueando.

---

## GATES TRAVADOS — não avança sem (gates de passagem: 0, 6, 7; os demais estão nas mecânicas)

GATE 1 → `mvt-minerar` · GATE 2 e 3 → `mvt-modelar` · GATE 4 → `mvt-validar` · GATE 5 → `mvt-obra-100k` · GATE CROSS-MARKET ORIGEM e DESTINO → `mvt-cross-market`. **LINK DA PÁGINA NÃO ACHADO NUNCA ELIMINA NEM BLOQUEIA** — regra completa no topo de `mvt-minerar` (vale para todas as mecânicas).

**Regra-mãe:** cada item abaixo tem EVIDÊNCIA concreta (arquivo, número de contador, campo do Hub).
**Item sem evidência = passo ABERTO. A próxima ação é fechar o item — não avançar, não perguntar ao dono.**
Marque cada item no `ESTADO.md` com a evidência colada (número/caminho), nunca "ok"/"quase". Antes de
qualquer Parada, rode o contador do passo e cole a saída. Se o dono pegar um item aberto, o erro é
meu: eu tinha o gate e não rodei.

Contador-base (rodar no diretório do Hub, com `ofertas.json` decifrado por `uv run cifrar.py --verificar`):
```fish
python3 -c "
import json,os
d=json.load(open('ofertas.json')); c=d['concepcoes']
n=lambda f:sum(1 for x in c if f(x))
print('total',len(c))
print('sem checklist_100k:',n(lambda x:not x.get('checklist_100k')))
print('sem biblioteca_url:',n(lambda x:not x.get('biblioteca_url')),'| sem pagina_vendas:',n(lambda x:not x.get('pagina_vendas')))
print('sem gate_origem:',n(lambda x:not x.get('gate_origem')),'| gate PENDENTE:',n(lambda x:x.get('gate_origem')=='PENDENTE'))
print('sem modelagem (p2-3):',n(lambda x:not x.get('comunicacoes_modeladas')))
print('sem territorio:',n(lambda x:x.get('validacao') not in ('DUPLICATA','DESCARTADA') and x.get('territorio_anuncios') is None))
print('obra sem arquivo:',sum(1 for o in d['ofertas'] if o.get('obra') and not os.path.exists(o['obra'])))
"
```

### GATE 0 · antes de tocar em qualquer coisa
- [ ] `low-ticket-metodo-mvt/SKILL.md` LIDO nesta sessão — evidência: abri o arquivo (Read) e cito no ESTADO 1 regra dele COM nº de linha + mtime (`stat -c %y`) e 1 regra do passo que vou executar (T1.4). Sem isso, conduzo de memória (R6 #1).
- [ ] `MINERACAO/<rodada>/ESTADO.md` lido e atualizado — evidência: linha "passo atual" com data/hora.
- [ ] Hub aberto — evidência: `uv run cifrar.py --verificar` deu "bate: True" e o contador-base foi colado.
- [ ] **ROTEADOR gravado (R1-R5)** — evidência: bloco `## ROTEADOR` no ESTADO com tipo, modo (A/B/B2/C/D/E/F/P), origem→destino (país+idioma), nicho/persona ou amplo (+filtro de formato), faixa de preço, a linha de eco ao dono **e a linha `ok do dono (data)`**. Sem isso o GATE 0 não abre.

### GATE 6 · CONSTRUÇÃO (página → entrega → mockups → banner → checkout → criativo)
> IDs no YAML: `T13.1`–`T13.9`, `T14.1`, `T15.1–2`. Antes de liberar construção: `gate.py --ate T12` exit 0; durante: `--passo T13`.
- [ ] **Entrada:** linha "Parada 3 liberada (data)" no ESTADO + `test -f obra-de-arte.md` + semáforo VERDE. Sem ela, NÃO constrói (trilha K).
- [ ] **MANIFESTO mudou → PROPAGAR, nunca deixar rastro velho (incidente GeriNeuro, 14/10/2026):** toda vez
  que o `MANIFESTO-ENTREGAVEIS.md` muda de versão (nome de volume/bônus, conceito, contagem), os itens
  abaixo têm que ser conferidos e atualizados NO MESMO PASSO — nunca só editar o Manifesto e seguir:
  1. `site/index.html` — textos de volumes/bônus/contagens batendo com a versão nova (grep pelo nome
     antigo tem que dar zero).
  2. `produto/texto/*.md` — o texto do entregável (fichas) escrito com os nomes/conceitos da versão nova;
     texto de versão anterior que não bate é reescrito, não mantido "porque já tava pronto".
  3. `produto/prompts/MOCKUPS.md` e qualquer prompt de imagem já escrito — se cita nome/conceito antigo,
     reescrever antes de mandar pro GPT.
  4. `STATUS.md` da oferta registra a troca de versão e qual desses três foi atualizado.
  Regra geral: mudança de conceito é commit atômico nos 3 (manifesto + página + texto do entregável),
  nunca só o manifesto sozinho. Pane que só edita manifesto sem tocar nos outros três FALHA o gate.
- [ ] Página: `pagina/BLOCOS.md` + `pagina/COPY.md` existem antes de montar; página montada em `pagina/` (ou no ar) com link — é a entrada do checkout.
- [ ] Entrega: texto completo definido (= composição de cada página; exercício/pôster/folha de imprimir já com a página `w` escrita junto — `references/PAGINAS-DE-ATIVIDADE.md`; toda página, `w` inclusa, é imagem GPT, nunca HTML/Pillow) → `DESIGN-SYSTEM.md` na raiz da oferta → amostra aprovada (IDENTIDADE-REF) → MVP ≥10 páginas por entregável (`ls produto/ENTREGA/*`; ESTADO registra `MVP/MODELO: n páginas`) → PDF por bloco + vídeo-walkthrough + upload `tsdrive:`. Entregável com carta (tarô/cigano/oráculo): a carta é o SCAN real do baralho tradicional (RWS 1909/Lenormand, domínio público) composto na página; GPT nunca redesenha a carta. Auditoria = carta recortada lado a lado com o scan (memória `carta-real-nunca-redesenhada`).
- [ ] **Promessa × entregue sempre medida, nunca de memória** (dona, 10/10/2026): `python3 ~/.claude/skills/auditar-entregaveis-oferta/scripts/audita.py OFERTAS/<slug> --retomar --registrar` — escreve `produto/ENTREGAVEIS.yaml` (registro vivo gerado: prometido × texto × páginas no painel × falta), imprime a próxima faixa exata de páginas a produzir e grava o estado no `STATUS.md` da oferta + linha dela no `STATUS.md` da raiz. Rodar ao retomar oferta parada (tokens/cota acabaram) e no GATE 6 antes de marcar a entrega por pronta. Complementa `references/TERMINAR-ENTREGA.md`; skill `auditar-entregaveis-oferta`.
- [ ] Mockups da página ANTES do lote MVP (ordem nova 14/10: imagens da página de referência baixadas e adaptadas, paleta confirmada com a dona, dona valida a página antes do MVP), sempre com as NOSSAS páginas de amostra no "por dentro"; banner só com mockups, SEM preço queimado (salvo pedido explícito), só no checkout DA oferta/leva (memórias `banner-sem-preco-mockup-nosso`, `banner-escopo-oferta`); checkout só com página+link+banner+produto (cada um = arquivo existente). TODO checkout da oferta (principal E upsell/produto irmão) sai com banner desktop+mobile, imagem do item, contagem regressiva igual à do principal e imagem em cada order bump inclusive o combo (`wiven-checkout` › 5b). Link de checkout Wiven = ID do checkout, nunca do produto; conferir no navegador.
- [ ] **Entrega por arquivo + upgrade (Wiven):** o produto **principal** sai com o **PDF de entrega** em Entregas → Arquivos — nome **= o nome do produto**, tudo clicável (botão + endereço + e-mail); gerador `MODELOS/PDF-DE-ENTREGA/` (`wiven-checkout` §3b). Se a oferta tem Essencial/Completo, o **upgrade** é produto próprio (**R$ 5,90 fixo**, nome **com o produto**, capa = mockup do Completo com "UPGRADE PARA COMPLETO" por cima) e entra como **1º order bump escopado SÓ à oferta Básica** (`wiven-checkout` §2b).
- [ ] **TODO produto/oferta novo nos DOIS webhooks no mesmo dia (regra da dona 16/10/2026 — "toda oferta tem que estar no webhook, nos dois"):** principal · **order bump** · combo · upsell · downsell · **upgrade Essencial → Completo** · produto irmão/cross e oferta de membro. Cada um marcado em (1) `<site>/painel/api/webhooks/wiven` (entrega) **e** (2) `adstrackeador.leadgo.dev/api/webhooks/sale/c/<conexão>` (medição), "todos os produtos" OFF, e no `PRODUCT_SKUS`/`COMPLETO_OFFERS` do servidor. Prova: `/panel/webhooks` com **TODOS** os produtos da oferta nos dois. Produto fora = venda some do Trackeador e/ou cliente sem acesso, sem erro (`wiven-checkout` §6 · `mvt-funil` Passo 7).
- [ ] Identidade: nenhuma arte/mockup do concorrente em peça nossa (memória `anti-arte-concorrente`; critério = ser arte dele, não o idioma). **Cross-market:** peça dele ADAPTADA (idioma + nossas cores) é o método; proibido é peça crua (texto na língua de origem/cor antiga) — `mvt-cross-market` › REGRA CROSS-MARKET.
- [ ] Acesso pós-compra verificado antes de dar a área de membros por pronta: webhook→login, libera só o comprado, bloqueado abre checkout só daquele item, add-on não re-entrega o principal (memória `acesso-pos-compra-verificar`). Login do /painel SÓ com e-mail da compra, zero campo de senha (nem pra demo). Conta de teste **teste@seudominio.com** com TUDO liberado em todo mercado, no mesmo deploy (aprovação de checkout + gravação do criativo; `area-membros-netflix` › Conta de teste).
- [ ] Ofertas de membro no /painel: tudo que a cliente não tem (upgrade de tier com 50% off; cada bump, combo, produto irmão/upsell com 30% off) do normal, ,90 abaixo, piso R$9,90 ou €4,90 em EUR (abaixo disso = preço normal); oferta dentro do produto existente de cada item ("<item> - Área de Membros", nunca produto novo), item único, redirect /painel, IC em todo botão via Trackeador (`data-tk-value`/`data-tk-currency` com o preço de membro; `area-membros-netflix` › Ofertas de membro). Criar junto com o checkout da oferta, não depois.
- [ ] **Oferta vendida em vários países** (Mundpay/Hotmart/Zenith/multi-moeda): página mostra preço aproximado na moeda local em cima e, menor, o valor do cadastro (US$/€) como "valor de referência", em TODO preço visível (planos, botões, popups de downsell e saída); `?pais=XX` para testar; obrigado único do produto redireciona pro painel do idioma. Regra e código: `references/PRECO-MOEDA-LOCAL.md` (decisão da dona 05/10/2026).
- [ ] Criativo: 3-5 demonstrativos; cada `CRIATIVO-N/roteiro-*.md` com as 11 linhas OK/NÃO, nenhuma NÃO, antes de exportar; mostra concepção + produto principal, não bônus/garantia.
- [ ] **Antes de gerar qualquer peça de criativo: ler `references/LICOES-CRIATIVOS-2026-10-09.md`** (dona, 09/10). Resumo seco: imagem = **capa + 2/3 páginas reais anexadas, modelo escolhe 2** · título pode ser da cor da marca (não só branco) · vídeo de leva **abre com o produto na tela** (gravação real com zoom; proibido PNG/Ken Burns; fonte única = gravações da dona; sem gravação = PERGUNTAR) · **`adelay` é em ms** (offsets em segundos empilham a fala e deixam o vídeo mudo — e o GATE não pega: confira a envoltória) · **toda peça entrega com `anuncio.md`** · prompt no ChatGPT **sem aspas** (`inserttext` trunca) · **confere o slug do b-roll** (busca ≠ conteúdo) · **meça a trilha** (−38 dB genérico já saiu fora da régua).
- [ ] Config técnica: checklist do board (Protectfy/plataforma/FB Ads/UTMify) linha a linha no ESTADO antes do passo 10 ("Protectfy: não usada" só se decisão do dono, com data).

### GATE 6 — itens de 25/09/2026 (regra única em `references/CONSTRUCAO-GATES.md`; conferidos por `gate.py --passo T13|T14`)
- [ ] `T13.10–T13.14` entregável APP: SPEC → validação dos dados por nós c/ fonte pública (cálculo regulado) → testes com casos nossos → deploy (Coolify) URL testada → acesso pós-compra com prova · `T13.13b` página no ar (URL pública, curl 200)
- [ ] `T13.16` prova social só real (decisão do dono 25/09/2026) · `T13.17` texto/amostra aprovado pelo DONO (frase verbatim) · `T13.19` re-checagem pré-construção ≤48 h
- [ ] `T13.15` sem "Espaço da imagem" · `T13.20` garantia/suporte/preço iguais em Obra=página=banner=checkout=criativo · `T13.23` DESIGN-SYSTEM antes da página · `T13.24` **FUNIL.md com bumps + Upsell 1 + Upsell 2 + downsell** (skill `mvt-funil`, regras em `references/PECAS-DO-FUNIL.md`; peça de ferramenta/app cai em `T13.10-14`) · `T13.25` plataforma de checkout (BR = Wiven) · `T13.26` anti-arte com comando · `T13.21` licenças · `T13.22` política Meta · `T13.27` criativo em imagem · `T13.29` 1º criativo aprovado pelo dono · `T13.28` cross: idioma (sem checklist legal de país)
- [ ] `T14.2` config técnica COM PROVA (Events Manager + UTMify) · `T15.3` critério venceu/perdeu gravado (fonte `metaads-kevones`)

### GATE 7 · TRÁFEGO (ponteiro `metaads-kevones` — nenhuma metodologia de tráfego aqui)
- [ ] Página no ar (URL testada) · checkout funcionando · 3-5 criativos exportados (arquivos existentes) · GATE 6 inteiro marcado. Sem os quatro, não entrega para tráfego.
- [ ] **Mudanças desta rodada gravadas em `LOW-TICKET/KEVONES/MUDANCAS.md`** — preço/ticket/bump, página/headline/checkout, público, verba/lance e **troca/pausa de anúncio**, no formato `data · oferta · tipo · o que mudou → Como ler`. **Registrar na hora, antes de fechar a rodada.** Sem isso a análise de tráfego lê errado: CPA "sobe" porque o preço caiu · IC fica caro porque a página mudou · venda "some" porque trocaram o anúncio. Quem analisa **lê o arquivo inteiro antes de decidir** (skill `analise-kevones-paineis`, etapa 2c) e mudança no meio do teste **zera o relógio** de 48h/7d.
- [ ] Hub atualizado (`status`, motivo em `notas`) com `uv run cifrar.py --verificar` → `bate: True`.

---

## GATE DE GASTO (T13.0) [decisão do dono 25/09/2026] — regra em `references/CONSTRUCAO-GATES.md` §0b

Nenhuma ação que custa dinheiro ou horas de produção (gerar imagem/vídeo, construir app/página, cadastrar checkout, contratar, subir tráfego) sem `gate.py --ate T12 --oferta <slug>` = OK colado no ESTADO + T13.19 (≤48h). Concorrente novo = T11 reaberto = gasto bloqueado. Todo pane de construção repete esta condição no prompt (`PROMPT-PADRAO-PANE.md`).

## PROMPT-PADRÃO DE PANE

**Pane de CONSTRUÇÃO (T13–T15, app, criativo) usa o `PRM-CONSTRUCAO` do mesmo arquivo** (briefing, DESIGN-SYSTEM, referência real, prova social só real, perfil livre `gpt-livre.sh`/`hub-livre.sh`, fechar pane); o orquestrador junta a referência antes e DELEGA (pane Sonnet/Haiku), não executa. Regras de pane que falha/some e de IP bloqueado: idem no arquivo.

Todo `pane_spawn` de pane que toca browser, minera ou mede carrega TODOS os blocos de `~/.claude/skills/criacao-low-ticket-mvt/references/PROMPT-PADRAO-PANE.md` (blocos obrigatórios de todo `pane_spawn` que toca browser, minera ou mede — copiados no prompt, nunca "veja a skill"). Prompt sem um bloco = não despacho. **Pane de CONSTRUÇÃO (T13–T15/app) usa o `PRM-CONSTRUCAO` do mesmo arquivo** (briefing, DESIGN-SYSTEM, referência, prova social real, perfil livre…), e o orquestrador delega — não executa. Antes de despachar, releio o prompt contra a lista. Tabela pane→perfil e nº de panes ativos na Biblioteca ficam no `ESTADO.md`; atualizar a cada despacho e a cada handoff.

---

## PASSO 0b · Abrir o Hub de Ofertas

Toda invocação, inclusive "onde paramos". O `ofertas.json` em claro está no
`.gitignore` — `ls`/`cat` do repo não mostram o que já foi feito.

```fish
cd "…/LOW-TICKET/HUB-OFERTAS"
set -a; source ~/.claude/.credentials.env; set +a   # HUB_SENHA
uv run cifrar.py --verificar                        # confere senha e conta registros
python3 -c "
import json,collections
d=json.load(open('ofertas.json'))
print('atualizado_em:',d['atualizado_em'])
print('ofertas:',len(d['ofertas']),'| concepcoes:',len(d['concepcoes']))
print(collections.Counter(c.get('veredito') for c in d['concepcoes']))
"
ls ../MINERACAO ../OFERTAS
```

Diga em uma linha em que etapa o ciclo está. Não repita busca que já está registrada;
se medir de novo, compare com o valor antigo lado a lado.

---

## ⏸ ABERTURA DA RODADA (partes de roteamento; o resto foi para as mecânicas — ver `## ÍNDICE`)

**⏸ O modo já foi decidido no ROTEADOR (R2) — esta seção só o detalha.** Se o ROTEADOR não está gravado, PARE e faça T0 antes de ler o resto: qual o modo desta rodada?

| Modo | O que é | Onde minerar |
|---|---|---|
| **A — do zero** | Método normal: minerar amplo na Biblioteca BR, sem concepção de partida | Biblioteca, país BR, `1 · MINERAR` abaixo |
| **B — origem → fora** | Pegar algo forte rodando (BR **ou qualquer mercado**) e levar pra outro idioma/país sem ninguém rodando lá. Inclui BR/Latam → EUA e **EUA/EN → Europa francófona** (França, Bélgica, Suíça, Canadá, em francês). A origem NÃO precisa ser BR. | Biblioteca do mercado de origem pra achar a concepção forte, depois gate `modelagem-cross-market` pro destino · origem pode ser oferta PRÓPRIA morta (quase-clone, risco pago) ou de TERCEIRO (quase-clone só se passar o gate) — ver divergências do Borba após o passo 3 [BORBA M0lixH8qNxo] |
| **C — fora → BR** | Pegar algo forte rodando fora (EN/ES/FR, ex. Latam) e trazer pro BR, gap aqui | Biblioteca com país/idioma trocado, gate `modelagem-cross-market` |
| **B2 — Europa francófona** | Caso concreto do B: destino França/Bélgica/Suíça/Canadá em **francês**, origem BR **ou** EN. Nichos que vendem lá: cristão, crochê/amigurumi, artesanato, relacionamento. Ticket entrada $9,90–$19,99. | Ref `MINERACAO/referencia-rodrigoliedson/METODO-RODRIGO-EUROPA.md`; mesmo gate cross-market |
| **D — oferta-first (rastreador)** | Achar oferta já escalada por rastreador externo (urlscan/utmify, reclamação-recência, SEMrush-plataforma, sitemap) em vez de busca por termo — depois aplicar uma saída do leilão | ADENDO §E → escapa leilão pelo §A → volta pro gate padrão |
| **E — sub-nicho / recorte** | Partir de território ou oferta escalada e estreitar (ou ampliar) o público (sub-nicho) | ADENDO §C (agora no passo 3) |
| **F — recorte de mecanismo "PDF/apostila técnica → visual"** (NOVO) | Formato genérico + ofício/área → território grande → medir a versão visual (mapa mental/esquema/infográfico) → zero confirmado = vaga | ADENDO §D + TRILHA F do ROTEADOR |
| **P — oferta pontual do dono** | "dá pra vender isso em X?" — 1 oferta que o dono trouxe, vários destinos candidatos | `REFERENCIA.md` + TRILHA P do ROTEADOR |

Modo B/C/D/E/F: são as **alavancas do ADENDO** (fim da skill) trazidas pra abertura como modo —
o veredito final continua o gate padrão dos passos. O modo NÃO se pergunta ao dono: a árvore do ROTEADOR (R2) decide e grava; esta tabela só o detalha (buraco 22, 25/09/2026).

Registre na abertura do arquivo da rodada: modo escolhido, volume (regra permanente abaixo) e
faixa de preço (só esta se pergunta).

**⏸ PERGUNTE AQUI, não na mineração: qual o teto de complexidade do entregável desta leva?**
Na abertura da rodada isso viraria filtro de coleta (erro que já cometemos com preço). No momento
de escolher a leva, não: você já sabe o que cada concepção pede, e a resposta muda quais avançam
e a faixa de preço possível.

| Opção | Entregável | Prazo típico | Ticket |
|---|---|---|---|
| **Rápido** | PDF, pack, planilha, templates | horas | faixa base R$17,90/27,90 |
| **Ferramenta** | app web simples: calculadora, gerador, checklist interativo, quiz de diagnóstico | 1-2 dias | acima da faixa base |
| **Completo** | app com back-end: preenche, salva, acompanha, gera documento | dias | bem acima |

**Padrão desta operação: Rápido + Ferramenta** (decisão do usuário, 18/09/2026). "Completo"
(app com back-end, dias de trabalho) fica fora por default — só entra se o usuário pedir na hora.
Não pergunte o teto toda rodada; aplique o padrão e só confirme se ele quiser mudar.

**2. Faixa de preço da rodada** — regra ÚNICA (= R5): padrão "sem faixa", grava e NÃO pergunta; o dono muda quando quiser (buraco 21, 25/09/2026):
- *Sem faixa* (padrão): minera e modela sem teto e sem piso; o valor sai na etapa 5.
- *Faixa declarada*: o usuário trava agora (o padrão do método é R$17,90 / R$27,90) e ela
  passa a valer como escopo da rodada — nunca como filtro do que entra no Hub (`concepcoes`), só como
  a pergunta 5 do checklist 100k ("consigo vender ISSO por esse valor?").

Nunca invente a faixa de preço nem pergunte o volume de novo no meio da rodada.

> Alavancas extras de busca (recorte de mecanismo, sub-nicho, cross-market, mineração
> oferta-first) NÃO são passo do método base — estão no **ADENDO · referências externas**
> no fim desta skill. Consultar como opção; o veredito final é sempre o gate padrão.

---

## FASE DE CONSTRUÇÃO (T13-T15) — só ponteiros; ordem única, não furar

Depois de escolhida a concepção vencedora (Parada 3 liberada; trilha K confere a ENTRADA). A ordem inteira está em memória `ordem-execucao-oferta`; as regras (DESIGN-SYSTEM, MVP 40%, entrega 100% imagem, área de membros, PDF+walkthrough+`tsdrive:`, padrões de low ticket vencedor, página/produto/criativo/config) estão em `references/CONSTRUCAO.md` (texto original, intacto). Cada item = arquivo existente (GATE 6 acima).

| Ordem | Item | Skill/ponteiro |
|---|---|---|
| 1 | Página (`pagina/BLOCOS.md` + `COPY.md`) — **página no ar = entregar na hora as keywords da Biblioteca em PT/EN/ES** (dona 27/10/2026; passo A do Gate 0.2 de `criativo-ads`, grava `pesquisa/KEYWORDS-BIBLIOTECA-<data>.md`) | `references/CONSTRUCAO.md` §6 · `imagens-pagina-low` (imagens) · `depoimentos-pagina-de-vendas` · `page-cro`/`popup-cro` |
| 2 | Entrega: texto → DESIGN-SYSTEM/visual → amostra → MVP ≥10 págs → área de membros. **"Terminar a entrega"** = receita `references/TERMINAR-ENTREGA.md` (mapear → texto → GPT 1×1 com 2-3 refs → conferir → publicar) | `imagens-pagina-low` (mecânica de imagem) · `traduzir-entregavel-imagem` (oferta em outro idioma: entregável e imagens da página, sem regenerar) · `area-membros-netflix` (entrega final) · `signup-flow-cro` |
| 3 | Mockups — **da página E do produto** (mesma mecânica; ver a regra grande abaixo) | `imagens-pagina-low` |
| 4 | Banner | `banner-checkout-gpt` |
| 5 | Checkout | **BR = `wiven-checkout` (Wiven; decisão do dono 25/09/2026 (revisão))**; hospedagem de página/app = **Coolify**. Alternativas só por decisão do dono: `checkout-premium` · `ggcheckout-produto` · `hotmart-produto-playwright` |
| 5b | **Funil de venda — bônus, order bump, Upsell 1 (barato), Upsell 2 (cara), downsell, combo e a peça de FERRAMENTA/microSaaS** (decisão da dona 09/10/2026: pesquisado e definido JUNTO com a oferta, não depois) | **`mvt-funil`** + regras em `references/PECAS-DO-FUNIL.md` · gateway `wiven-checkout` · entrega `area-membros-netflix` · gate `T13.24` (+ `T13.10-14` se for app) |
| 6 | Criativo (leva de teste = 30, Kevones §21) | `criativo-ads` — receita `~/.claude/skills/criativo-ads/references/RECEITA-LEVA-PONTA-A-PONTA.md` (porta única; puxa `narracao-hub-tts`, `gpt-imagem-playwright`, `criativo-ads-video-orq`/`hub-video-playwright`). **Ler antes: `references/LICOES-CRIATIVOS-2026-10-09.md`** |
| 7 | Config técnica | `hotmart-produto-playwright` · `ggcheckout-produto` · `trackeador` · receitas em `~/.claude/browser-workspace/domain-skills/` |
| 8 | Tráfego | `metaads-kevones` (nenhuma metodologia de tráfego aqui) · `analytics-tracking` |

**Oferta irmã clonada de outra oferta nossa (ex.: Cigano ← Tarot):** antes do tráfego, rodar a auditoria de herança (`imagens-pagina-low` › "Oferta irmã"), espelhar planos e bumps da oferta-mãe, e passar o checklist do pós-compra (`area-membros-netflix` › "SEMPRE verificar", itens de 05/10/2026: todo offerCode mapeado, tier com SKU próprio, painel compartilhado, e-mail por produto, ofertas de membro, bônus prometido abrindo). Entregável abaixo do MVP 40% no principal (ex.: 4 de 36 cartas) segura o tráfego.

---

## 📦 REGRA PERMANENTE · IMAGEM DE PRODUTO É **MOCKUP**, NUNCA CAPA SOLTA (dona, 10/10/2026)

> **Toda imagem de produto — capa de manual, capa de order bump, capa de upsell, card da área de
> membros, imagem de item no checkout — é um MOCKUP DO PRODUTO.** Não é frase de efeito em fundo
> chapado. **A pessoa tem que ver o livro/aplicativo/planilha que vai receber na mão.**

**Por quê (a dona mediu):** *"as capas que eu tinha antes não vendiam. Refiz a capa certa e vendeu."*
Duas rodadas de refação no Jiu-Jitsu Sem Força custaram tempo antes de a régua ficar escrita.

**O que é mockup aqui:** o entregável em 3D, de pé, com **capa + lombada + espessura visíveis**,
com a arte real do produto aplicada nele, sombra suave, fundo neutro. **Combinações** = vários
volumes em leque, o do meio maior e à frente.

**O MOCKUP DA PÁGINA E O MOCKUP DO PRODUTO SÃO A MESMA COISA.** Se o passo 3 faz o da página, o da
peça é exatamente o mesmo passo com outro objeto. Não existe "a arte da capa é mais simples".

### Como gerar (a ordem que evita o erro)

1. **Primeiro a arte da capa/emoji do entregável** (a arte que vai *dentro* do mockup).
2. **Depois o mockup**, aplicando essa arte no objeto — a peça é `gpt-imagem-playwright` **com a
   arte como referência anexada**, nunca como texto só.
3. **Anexar 2-3 referências REAIS da oferta** no upload. Descrever em texto não funciona: já saiu
   errado 3 vezes assim (a GPT puxa o estilo da referência errada).
4. **Cores e fontes do `DESIGN-SYSTEM.md` escritas no prompt**, sempre — pela mesma razão.

### Os 4 erros que já custaram reprovação

| Erro | O que fazer |
|---|---|
| Mandar só o texto, sem referência | Anexar a referência. **Sempre.** |
| GPT copiando a referência em vez de adaptar | `CRITICAL` no início + `MANDATORY` no fim do prompt |
| Inventar página/técnica que não existe no entregável | A arte só mostra conteúdo real — abrir o entregável antes |
| Rótulo errado na arte ("BÔNUS DE CHECKOUT" em peça que é bump) | O rótulo é o da marca; o checkout confere o tipo |

**Gate antes de gravar:** capa só vai pro `/painel`, pro checkout ou pro criativo depois de **A
DONA VER**. Ela reprova no privado o que só ela decide.

**Referência viva:** `OFERTAS/jiujitsu-sem-forca/produto/referencia-visual/` tem 6 imagens do padrão
certo (3 avulsos + combo, em 3D). Toda oferta nova que venda guia/apostila/manual começa copiando
essa pasta.

---

## Registro no Hub

A cada mudança de status (`ideia` → `producao` → `rodando` → `venceu` | `perdeu` |
`pausada`), inclusive o que morreu, com o motivo em `notas`:

```fish
cd "…/LOW-TICKET/HUB-OFERTAS"
# edite ofertas.json
uv run cifrar.py && uv run cifrar.py --verificar   # tem que dizer "bate: True"
git add ofertas.enc && git commit -m "oferta <nome>: <status>" && git push
```
**Concorrência (buraco 29):** panes escrevem só `.jsonl`; UM consolidador (o orquestrador, via pane) grava no Hub; `cifrar.py --verificar` ≠ "bate: True" = parar e reportar, backup antes de qualquer sobrescrita; "bate: True" só prova que decifra igual — cole junto o contador-base.
`python3 cifrar.py` falha — a lib `cryptography` vem pelo header PEP 723; use `uv run`.
Campos: `HUB-OFERTAS/README.md`. Painel: https://huboferlaslowticket.minhaempresa.com.br

**Obra pronta só com arquivo (E13):** só grave `obra:` ou "Obra de Arte 100K pronta" em `notas` depois de `test -f OFERTAS/<id>/pesquisa/obra-de-arte.md`. `cifrar.py --verificar` não confere arquivo. Contador de Condução: `sum(1 for o in d['ofertas'] if o.get('obra') and not os.path.exists(o['obra']))` deve dar 0 (R3: 11 ofertas com "Obra pronta 18/09/2026" e 0 arquivos; `ESTADO.md` 0/3-5).

## Condução

**Antes de agir em QUALQUER passo, audite em que ponto o ciclo está — nas 100% das
concepções, não nas que têm dado.** Erro real 2026-09-18: montei a Obra de Arte (passo 5)
com o passo 3 ainda aberto em 36 de 243 concepções, e recomendei direção sobre as 201 que
tinham dado. Recomendação sobre amostra enviesada não é recomendação.

Auditoria obrigatória na abertura e a cada retomada — conte, não presuma:

```fish
python3 -c "
import json,collections
c=json.load(open('ofertas.json'))['concepcoes']
print('total',len(c))
print('SEM destrinchar/modelar (passo 2-3):',sum(1 for x in c if not x.get('comunicacoes_modeladas')))
print('modelado SEM veredito (passo 4):',sum(1 for x in c if x.get('comunicacoes_modeladas') and not x.get('validacao')))
print('Obra pronta SEM arquivo:',sum(1 for o in json.load(open('ofertas.json'))['ofertas'] if o.get('obra') and not __import__('os').path.exists(o['obra'])),'(deve dar 0)')
print('sem pagina:',sum(1 for x in c if not x.get('pagina_vendas')),'| sem preco:',sum(1 for x in c if not x.get('preco') or 'sem preço' in str(x.get('preco'))))
"
```

Regra: **só avança para o passo N+1 quando o passo N está fechado nas 100%.** Se o passo
anterior tem buraco, o próximo passo é FECHAR o buraco — não seguir com o que já dá.
Diga em uma linha o passo em que o ciclo está antes de fazer qualquer coisa.

**Não existe pular etapa (ver ROTEADOR).** **Falta de dado nunca é motivo de pular concepção.** Sem preço, sem página, página fora do
ar, destino em WhatsApp/Instagram: registre a pendência com a data e modele igual às outras.
Preço é informação, nunca filtro (regra do usuário). Concepção só sai do ciclo por motivo de
método escrito (travou, opções mais-ou-menos, complexo demais, criativo demonstrativo difícil)
— e cross-listada (linha que aponta para outro código) não é buraco, é duplicata: marque como tal.

- Uma oferta por vez até o usuário pedir paralelo.
- **Constância** [BOARD 8 erros, erros pessoais]: "lançar concepções até acertar" — oferta `perdeu` na primeira concepção não encerra a rodada: registre o motivo no Hub e abra a próxima da `proximas-levas` **re-entrando em T9** (a modelagem já existe; a validação não). `perdeu`/`venceu` = decisão do dono com critério da skill `metaads-kevones` (`CONSTRUCAO-GATES.md §5`). **Ordem** [BOARD 8 erros, falta de organização]: não fazer tudo ao mesmo tempo nem fora de ordem — vale o PASSO 0a e a FASE DE CONSTRUÇÃO. (Obs.: no board o operacional não tem setas entre as caixas; a ordem fixa da construção é decisão do dono de 21/09/2026, divergência declarada.)
- Nas paradas, recomende com o porquê — não devolva menu sem opinião.
- Concepção fraca: diga que é fraca e por quê.
- Modelar não é copiar: nunca copie página ou criativo de concorrente.

---

# ADENDO · Referências externas (NÃO fazem parte do método base)

Material de fora (canal @guilhermeasvi / entrevista Borba; 2 vídeos de mineração por rastreador).
Borba: material completo em `MINERACAO/referencia-adsborba/` (INDICE + METODO-BORBA). Atribuição: subnichar (bidirecional) + BR→EUA são DELE; "ou o contrário" (gringa→BR) e "MVT no destino" são NOSSOS. "Lateralizar contas de anúncio" ≠ lateralização de produto (N4): a 1ª é tráfego (skill `metaads-kevones`).
São **opções e alavancas**, não passos. O método base (minerar → destrinchar → modelar → validar
→ obra 100K → construir → tráfego) e seus gates ficam intocados. Toda oferta achada por aqui
**volta pro gate padrão** (território>0 + comunicação livre = vaga + demanda orgânica com
comentário recente/intenção/engajamento + sinal_de_compra>0) e pra **entrega padrão** (nunca PDF
solto: GPT gera texto → 1 imagem por página → área de membros com upsell interno; sempre alguma
funcionalidade/app — ver passos 1 e da construção). Transcrições-fonte:
`MINERACAO/referencia-guilhermeasvi/` e `MINERACAO/metodo-2-fora-biblioteca/`.
