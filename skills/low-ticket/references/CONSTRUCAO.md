# CONSTRUÇÃO — regras originais dos passos 6-10 (T13-T15)

Referência da orquestradora `criacao-low-ticket-mvt` (era `## FASE DE CONSTRUÇÃO`, `## PADRÕES DE LOW TICKET VENCEDOR` e passos `6·PÁGINA`…`10·TRÁFEGO`). Texto original intacto; a mecânica de cada item mora nas skills apontadas na seção `## FASE DE CONSTRUÇÃO` da orquestradora. O gateway por região e a modelagem cross-market foram para `mvt-cross-market`.

## FASE DE CONSTRUÇÃO (passos 6-8) — ordem única, não furar

Depois de escolhida a concepção vencedora (parada 3 liberada). Decisão do usuário 21/09/2026: não
pular, não fazer fora de sequência. A ordem inteira em memória `ordem-execucao-oferta`.

1. **Página** (passo 6) — estrutura, copy, visual definidos.
2. **Entrega** (passo 7), nesta ordem interna:
   (a0) **DUAS PÁGINAS POR EXERCÍCIO (dona, 18/10/2026):** toda atividade que pede material
       físico/imprimível (caça-palavra, labirinto, sequência, recibo, cartões para recortar,
       pôster, tabuleiro, ligar-colunas…) precisa da **página de instrução** (a ficha) **e** da
       **página de atividade** (a folha que a pessoa imprime e faz). Sem a segunda, o exercício
       não é aplicável. **As duas páginas são escritas JUNTAS no texto da entrega** (conteúdo exato
       + composição + gabarito da folha `w`) e **as duas são imagem GPT**, 1 por mensagem — nunca
       HTML/SVG/Pillow (reprovado pela dona 23/10/2026). Conferir o conteúdo exato na imagem contra
       o gabarito. Regra, modelo de texto e receita: `references/PAGINAS-DE-ATIVIDADE.md`;
   (a) DEFINIR TODA a entrega **em texto** (sessões, capa, textos, item principal + bônus) — dono
       monta/aprova;
   (b) só então **referências visuais** + direção visual (a mecânica é da skill `imagens-pagina-low`).
       **Montar aqui o `DESIGN-SYSTEM.md` na raiz da pasta da oferta** = fonte de verdade única da
       identidade: paleta com o PAPEL de cada cor (qual FORMA o fundo vs. qual é só tinta/accent —
       nunca promover accent a fundo), tipografia, ornamentos/molduras, e a **tabela de referências
       visuais JÁ GERADAS** (capa, página interna, diagrama, exercício) com o path de cada uma —
       geradas no GPT com as NOSSAS cores, sobre a estrutura do concorrente quando houver (copiar
       layout, nunca cor/idioma). **Todo chat/pane novo PUXA este doc antes de gerar
       qualquer ENTREGÁVEL, MOCKUP ou CRIATIVO da oferta, ou ao buscar mockups — nunca inventar cor
       nem derivar paleta de outra lista de hex.** (Entregável/mockup = identidade limpa deste doc.
       Criativo/ad = visual orgânico, ver regra de criativo orgânico na skill de criativo.) Regenerou/aprovou
       peça nova → atualiza o doc. Memória `design-system-doc-por-oferta`;
   (c) **amostra** (capa + algumas páginas) pra validar o visual → aprovada vira IDENTIDADE-REF travada
       e entra como referência no `DESIGN-SYSTEM.md`;
   (d) produzir o **MVP de cada coisa** (principal, bônus, order bump) a ~**40%** (memória
       `mvp-40-porcento`): só o bastante pra pôr na página e começar a vender; completa depois da
       venda. MVP reduz VOLUME de cada etapa, não pula etapa. **MVP = 10 páginas por entregável,
       inclusive order bump** (curto demais gera reembolso — memória `entregavel-sempre-imagem-nunca-pdf`). O board separa Entregável MVP (1ª versão) de Entregável MODELO (10/15 páginas diagramadas para criativo e página) [BOARD PRODUTO]: nesta operação são o **mesmo lote** — mínimo 10; mockup, página e criativo só usam páginas desse lote, e o ESTADO da oferta registra `MVP/MODELO: n páginas`.

       **DIVISÃO DE TRABALHO (eu × GPT Work mode)** — como a oferta já está entendida (página feita),
       os textos saem MUITO melhores; então:
       - **MINHA tarefa (orquestrador):** (1) gerar ANTES o CONJUNTO de refs visuais partindo da base
         do concorrente (capa/seções/interno, nas NOSSAS cores) — quanto mais fonte pronta, melhor ele
         gera; (2) escrever TODO o texto, organizado e bem escrito (capas, sumários, seções, por
         página); (3) montar o pacote pro GPT = refs anexadas + contexto (produto/página/DESIGN-SYSTEM)
         + texto completo + **manifesto imagem-por-imagem numerado** ("imagem 1 = capa …; imagem 2 =
         seção …; … imagem 10 = …").
       - **Tarefa do GPT (Work mode):** receber esse pacote e gerar o LOTE visual inteiro de uma vez
         (extremamente visual, nunca parede de texto). Base de prompt = `PROMPT-PRODUTO-DIGITAL-PREMIUM.md`.
       Mecânica de lote/Work em `browser-workspace/domain-skills/chatgpt.com/work-mode-lote-entrega.md`;
       memória `entregavel-gerar-com-referencia-visual`;
   (e) **área de membros** sempre a NOSSA (skill `area-membros-netflix`), não a do concorrente.
   (e2) **SEQUÊNCIA DO MVP DOS ENTREGÁVEIS (dono, 27/09/2026 — mapas-visuais-eletrotecnia):**
       1. **Texto de TUDO primeiro:** analisar página de vendas (nossa + original), o checkout original (order
          bumps) e cada entregável prometido → escrever o texto de principal (essencial + completo), bônus e
          order bumps — **texto INTEGRAL de TODAS as páginas do completo** (não só do MVP; dono 27/09) — ANTES de
          gerar qualquer imagem. **Só a GERAÇÃO é MVP** (~10 págs por item); o texto já fica todo pronto.
          **Texto = composição da entrega:** cada página escrita com o que vai nela e onde (título,
          ilustração/cena, área de conteúdo). Exercício, pôster, cartão de recortar, tabuleiro → já
          escreve a página `w` junto (conteúdo exato + composição + gabarito), modelo em
          `PAGINAS-DE-ATIVIDADE.md` § "A composição nasce no TEXTO". Texto sem a `w` = incompleto.
       2. **Começa pelo mais básico** (principal): referência visual (páginas do produto já adaptadas; no
          cross-market, as DELE adaptadas) + texto MVP → GPT Work mode gera **só 2-3 páginas de teste**;
          orquestrador + dono conferem. Aprovado → gera o resto do MVP (~7 págs, fechando ~10). Depois o
          próximo item, mesmo ciclo, até acabar.
       3. **Todo item tem CAPA própria organizada**, mesmo no MVP — inclusive order bump e bônus sem conteúdo.
       4. **Área de membros em CAMADAS** (skill `area-membros-netflix` › estados de produção): só capa, sem
          conteúdo → card "Em breve / em atualização"; conteúdo parcial (MVP) → faixa "em atualização · mais
          páginas em breve"; completo → normal. Igual ao Mapa do Tarot.
       5. **Checkout Wiven**: produto + order bumps modelados do checkout ORIGINAL (abrir e listar os bumps
          dele), cada bump com capa e entrega na nossa área `/painel`.
   (f) **COMPLETAR A ENTREGA (pós-MVP / pós-venda) — UM ITEM POR VEZ** (decisão do dono 27/09/2026,
       depois de um orquestrador abrir 6 panes em paralelo e virar bagunça):
       1. **Inventário primeiro:** contar páginas na área de membros por item × o que a página de vendas
          promete (ex.: "78 cartas", "150+ combinações"). Tabela item | tem | promessa | falta.
       2. **Ordem:** item que ainda NÃO TEM NADA → faz o MVP dele (10 págs) e publica na área de membros.
          Depois completa item a item: **principal → nível completo/upgrade → bônus → order bumps.**
       3. **Sequencial, não paralelo:** UM item em produção por vez (no máximo 1 pane gerando + 1
          escrevendo o texto do PRÓXIMO item). Terminou, publicou, conferiu → abre o próximo. Nunca
          vários panes disputando os perfis do GPT, cada um num item — dá conflito de perfil, de pasta e
          de área de membros. **Ciclo do pane: 1 pane = 1 item.** Terminou o item → orquestrador fecha
          o pane (`pane_close`) → abre pane NOVO, contexto limpo, pro próximo item. Nunca reaproveitar
          pane cansado nem deixar pane idle aberto.
       4. **Texto completo ANTES de gerar:** o item só vai pro GPT quando TODO o texto que vai virar
          imagem está escrito em arquivo (MVP ou resto). Faltou texto → escreve primeiro, depois gera.
       **SEM Work mode (padrão desde 07/10/2026):** receita inteira de mapear → texto → gerar 1×1 no chat com 2-3 refs nossas → conferir → publicar em `references/TERMINAR-ENTREGA.md` — ela vale no lugar do item 5 abaixo.
       5. **Geração no GPT = skill `gpt-imagem-playwright` + WORK MODE** (só se a conta tiver Work; receita
          `work-mode-lote-entrega.md`), nunca chat uma-imagem-por-vez: um pedido com o lote inteiro
          do item (todas as páginas pendentes), anexando **a NOSSA referência** (páginas já aprovadas
          do mesmo tipo + a capa do item, tabela do `DESIGN-SYSTEM.md`) — **nunca a do concorrente** nesta
          fase (MVT mesmo mercado); **CROSS-MARKET: o entregável é o DELE adaptado** — anexa as páginas dele +
          link original + nosso HTML, e pede só idioma + nossa identidade de cor (`mvt-cross-market` › REGRA CROSS-MARKET) — + contexto + tokens do design system + texto página a página numerado. MVP já validado →
          o resto do item sai todo num lote só.
          **Prompt tem que dizer, com todas as letras (dono 27/09):** "gere N IMAGENS INDIVIDUAIS,
          uma imagem separada por página, com o gerador de imagens — não junte páginas, não faça
          grid, não renderize com HTML/SVG/código" + manifesto "Imagem 1 = … / Imagem 2 = …" com o
          texto de cada. Sem isso o Work mode desenhou a página por código (carta placeholder). Modelo completo + checklist de erros: skill `gpt-imagem-playwright`, "Prompt-modelo OBRIGATÓRIO do lote de entregável" — o orquestrador COLA esse modelo no brief de todo pane de geração.
       6. **Fecha o item:** QA visual → sobe na área de membros → deploy → confere no ar → só então o próximo.
3. **Mockups** — ⛳ **ORDEM NOVA 14/10/2026:** mockups da página vêm ANTES do lote do MVP (paleta fechada no NOSSO HTML antes de qualquer imagem — perguntar à dona se ela não disse → baixar todas as imagens da página de referência → UM chat no GPT: "estou modelando esta página <URL>, minha oferta é X" + nosso HTML + todas as imagens dela anexadas, refazer só ajustando pro nosso produto → dona valida → MVP → imagens "por dentro" por último, com as páginas do MVP de referência). Receita: `imagens-pagina-low` › ORDEM NOVA. Texto antigo: só depois da entrega MVP produzida; usa imagens reais da entrega (substituem os do
   concorrente). **Cross-market:** os mockups DELE adaptados (idioma + cor) no mesmo lote Work mode das imagens da página. Exemplos bons em `imagens-pagina-low/assets/exemplos-mockups-*`.
4. **Banner** (skill `banner-checkout-gpt`) — só depois de ter mockups (logo, só após MVP entregue).
   Banner direto: título/objetivo real, garantia, entrega imediata, acesso vitalício, mockup do
   produto, selos. 3 saídas: checkout **desktop** (16:9), checkout **mobile** (1:1/retrato) e
   **imagem do produto**.
5. **Checkout** — por último; precisa do link da página + banners + produto definidos. Checkout PRÓPRIO (página de alta conversão no projeto Next.js/React: barra urgência, banner colado, form só-email, order bump com foto+checkbox pré-marcado, pagamento por país, prova social, notificação fake, popup de saída) = skill **`checkout-premium`** — invocar via Skill tool ao montar o checkout, não recriar do zero. Se for checkout hospedado em gateway (GG Checkout) usar skill `ggcheckout-produto`; checkout hospedado na Wiven (LeadGo) — produto, order bumps, link de entrega, webhook — usar skill `wiven-checkout`; banner do checkout = `banner-checkout-gpt`.

Baixar referência do concorrente (imagens, criativos) NÃO é produzir — pode a qualquer momento. Nada
de gerar capa/entrega antes de texto+visual definidos, nem montar checkout antes de página/link/banner.


**Toda a mecânica de imagem da entrega/mockup vive na skill `imagens-pagina-low`** — fonte de verdade,
não se duplica aqui. Lá estão: pipeline de 8 passos, tabela peça↔referência (capa puxa mockup de capa,
diagrama puxa diagrama, exercício puxa exercício, bônus puxa bônus), modelagem = EDITAR a referência
(muda só cor+idioma, não inventa), prompt-pacote-completo (referência + contexto + design system) e
iconografia canônica de domínio público (ex: carta Rider-Waite), não símbolo genérico.

**Entrega é 100% IMAGEM** (decisão do dono): o GPT renderiza CADA página do PDF com o texto dentro
dela, seguindo o visual travado — sem overlay, sem caixas vazias. Legibilidade se garante por: **1
página por imagem em tamanho cheio** (nunca montagem espremida — foi o que garatujou o texto), geração
**página a página**, e **regerar** toda página que sair com texto torto. Produção: amostra → validar →
gerar o ~40% em lotes de 10 → PDF final na ordem.

**Entrega final = SEMPRE ÁREA DE MEMBROS, não PDF solto** (decisão do dono): as páginas geradas (+
bônus, + PDF) são organizadas dentro de uma área de membros logada. Usar a skill **`area-membros-netflix`**
(hero + grid de módulos, cadeado nos bloqueados, modal de compra) — invocar via Skill tool na hora de
montar a entrega, não recriar do zero. Vantagens: tudo organizado por módulo; quem comprou o Básico vê o
Pro/Completo BLOQUEADO com upsell embutido (compra ali mesmo); fica muito mais bonito e com cara de
ferramenta que um PDF avulso. Fluxo: gerar páginas/PDF → subir na área de membros → principal desbloqueado,
add-ons bloqueados. Só cai pra PDF puro se o dono pedir explícito. Para otimizar o fluxo de login e acesso do comprador: skill **`signup-flow-cro`** — invocar pra testar e melhorar taxa de acesso à entrega após compra.

**FLUXO DE FECHAMENTO DO MVP — PDF + vídeo-walkthrough (decisão do dono 21/09/2026):** quando o MVP das
imagens fecha (10 de cada bloco: principal + cada bônus), monta-se **1 PDF por bloco** (PDF do principal,
PDF do bônus 1, do bônus 2, do bônus 3…) a partir das imagens da pasta `produto/ENTREGA/` (ferramenta:
`img2pdf` ou `convert`, 1 imagem = 1 página, ordem numérica). Esses PDFs são a "orçamento/entrega completa"
que o dono **grava no celular passando cada um** (vídeo mostrando o material por dentro) — e esse
vídeo-walkthrough **entra DENTRO da entrega** (área de membros) como parte do produto. Além disso os PDFs
sobem no **Drive Innova** (rclone remote `tsdrive:`) na estrutura FIXA (verificada 21/09/2026):
`tsdrive:PROJETOS/INTERNOS/LOW TICKET/<Nome do Produto>/` → 1 PDF por bloco. Sequência: PROJETOS → INTERNOS → LOW TICKET (uppercase) → pasta do produto.
Ex real: `tsdrive:PROJETOS/INTERNOS/LOW TICKET/Mapa do Tarot Brasil/mapa-do-tarot-PRINCIPAL.pdf`. Sempre esse padrão,
repetível pra todo produto low ticket. Subir com
`rclone copy <arquivo> "tsdrive:PROJETOS/INTERNOS/LOW TICKET/<produto>/"`. Nota: o remote antigo `drive:` é outro drive (raiz com INTERNOS+EmpresaB DIGITAL) — NÃO usar pra low ticket.

---

## PADRÕES DE LOW TICKET VENCEDOR (aplicam a página + criativo + funil)

Cinco padrões que toda oferta low ticket que vende tem (ref transcrição Rodrigo Liedson
`MINERACAO/referencia-rodrigoliedson/METODO-RODRIGO-EUROPA.md`, vídeo 4). Universal — vale BR e
cross-market. Checar na página, no criativo e no funil:

1. **Promessa clara** — a pessoa bate o olho e sabe EXATO o que recebe ("1000 sermões prontos"), sem
   precisar interpretar. Oferta ambígua ("ative a proteção do arcanjo, limpe a energia, restaure a
   paz…") faz a pessoa interpretar antes de decidir = mata a conversão. Headline direta na 1ª dobra.
2. **Página com mais elemento VISUAL que texto** — ninguém no feed quer ler; mockup/imagem vende. Cada
   seção mostra o que a pessoa recebe em imagem, texto curto de apoio. (Casa com nossa entrega
   demonstrativa e com webapp/mockup.)
3. **Criativo DIRETO, não curioso** — headline + mockup + preço + CTA; a pessoa chega semipronta. O
   criativo CURIOSO é pra VSL/ticket alto (a VSL qualifica no meio do caminho); no low ticket não há VSL
   pra qualificar, então o criativo já mostra o que é. **Criativo em imagem é o padrão** (rápido de
   modelar); vídeo é opcional.
4. **Over delivery** — bônus acima do esperado, mas **~3 bônus que fazem sentido** com o principal,
   nunca empilhar 8-10 sem relação (satura, sobrecarrega, trava a decisão). (Mesma lógica do MVP 40%.)
   **Como criar o bônus (Heitor, post "bônus que faz a oferta parecer valiosa sem custar quase nada")** —
   "bônus bem pensado empurra a decisão mais do que desconto". 5 passos, rodar em cada bônus:
   1. **Resolve a PRÓXIMA dor, não a mesma.** Principal resolve um problema; bônus resolve a etapa que vem
      logo depois e que a pessoa também vai precisar (guia de receitas → bônus lista de compras).
   2. **Formato rápido de produzir** — checklist, mini guia, planilha, áudio curto. Não precisa ser grande,
      precisa ser útil e fácil de fazer. Meta = sensação de "estou ganhando mais do que paguei".
   3. **Preço baixo ≠ oferta forte.** Preço é convite; quem vende é a concepção (demanda real). Bônus não
      conserta oferta fraca, e baixar preço só derruba margem. Barato sem concepção certa continua encalhado.
   4. **Bônus vence onde o mercado é fraco** — olhar o que os concorrentes NÃO entregam (suporte rápido,
      modelo pronto…) e pôr ali. Bônus = vantagem construída sem mexer no preço. (Casa com o Mapa da Vantagem:
      puxar a lacuna do concorrente da mineração.)
   5. **Limitar a quantidade** — 1 ou 2 bônus fortes valem mais que 5 fracos empilhados; muito bônus fraco
      passa impressão de produto principal fraco que precisa de enchimento. Menos, mas relevante.
   Gate por bônus antes de produzir: (a) resolve a próxima dor? (b) formato rápido? (c) cobre lacuna do
   concorrente? Se 3× não → cortar. Bônus custa quase nada e muda a percepção de valor da oferta inteira.
5. **Funil de alta conversão** — não parar na venda única: **order bumps COM relação ao principal**
   (ex: 1000 sermões → order bump "200 temas prontos") + um **microSaaS de ASSINATURA mensal** de topo
   (app que gera/faz a coisa) = LTV recorrente (cliente renova mês a mês). Order bump aleatório do mesmo
   nicho não converte; tem que completar o principal.
   Combo (Borba): order bump extra que junta os dois bumps por preço de desconto — "uma order bump que é o combo desses dois" [BORBA Pspr8S9fbbA]; "eu uni essas duas em um combo por um preço ali de desconto" [BORBA f8HMw89DAOE].

**Regra de botão (padrão de página):** o botão da 1ª dobra **NÃO vai direto pro checkout** — leva pra
próxima seção com mais info visual. Botão seco → checkout = CTR alto e venda baixa. Só manda pro
checkout depois que a pessoa viu conteúdo + bônus + preço.

**PREÇO PADRÃO BR — oferta nova (dona, 08/10/2026; substitui o padrão 27,90/37,90 de 27/09):**

| Peça | Página / checkout | Área de membros (/painel) |
|---|---|---|
| Básico (só o principal) | **R$ 17,90** | — |
| Popup do completo (downsell ao clicar no básico) | **R$ 22,90** | — |
| Completo (principal + bônus) | **R$ 27,90** | — |
| Popup de saída (o básico mais barato) | **R$ 16,90** | — |
| Order bump 1 | **R$ 7,90** | **R$ 5,00** |
| Order bump 2 | **R$ 8,90** | **R$ 5,00** |
| Order bump 3 | **R$ 9,90** | **R$ 5,00** |
| Combo "leve os 3 com desconto máximo" (último bump, entrega os 3 SKUs) | **R$ 17,90** | **R$ 9,90** |
| Upsell 1 | **R$ 17,90** | **R$ 9,90** |
| Downsell do upsell 1 | **R$ 12,90** | — |

Oferta nova usa esses valores sem perguntar; preço diferente só se a dona declarar. Ofertas já no ar
mantêm o preço delas (não reprecificar sem pedido). Nessa tabela o preço de membro é FIXO (substitui o
cálculo de 30% off e o piso R$ 9,90 da `area-membros-netflix` pra bumps/combo/upsell); upgrade de tier
continua 50% off do completo.

**Estrutura de funil de referência (cross-market/Europa):** entrada $9,90–$19,99 → 3 order bumps ~$4,90
relacionados → microSaaS $7,90/mês → produto de topo ~$11,90. Entrega sempre na NOSSA área de membros.

**PEÇAS DO FUNIL — regra de 09/10/2026 (dona): o funil é projetado JUNTO com a oferta, em T11/T13** —
bônus, order bump, **Upsell 1 (barato) e Upsell 2 (cara)**, downsell e a peça de **FERRAMENTA/microSaaS**
(calculadora, gerador, template que acelera o trabalho dele; ou app de topo em assinatura) saem
pesquisados antes da 1ª venda, e o que os concorrentes empilham entra na mineração.
Tudo em `references/PECAS-DO-FUNIL.md` (mapa das peças · regra da próxima dor · matriz anti-overlap ·
ferramenta/microSaaS e as 4 perguntas da persona · preços e simulação de ticket · gates) e a execução em
**`mvt-funil`** → grava `OFERTAS/<slug>/FUNIL.md` (gate **T13.24**).

---

## 6 · PÁGINA

Método: `references/pagina-produto-criativo.md` §1. 3 pilares; **10 blocos obrigatórios
na ordem**; opcionais só quando o nível de consciência pedir; copy de clareza, sem
persuasão; headline sobre o produto; copy gerada a partir da Obra com o comando "altere
a comunicação para a nova concepção, não modifique as ideias".

**Registros obrigatórios da página** (Obra → escolha dos blocos → mapa de inserção → copy [BOARD MAPA DE INSERÇÃO DOS BLOCOS OPCIONAIS]) — sem eles não abre a montagem:
- `OFERTAS/<id>/site/BLOCOS.md`: a lista final dos blocos na ordem; cada opcional escolhido com o motivo (persona + oferta + nível de consciência) e a posição; só entra opcional que a Obra pede. Regras do board: Comparativo de Vida e Comparativo de Solução **não entram juntos**; Autoridade e Missão/Propósito **não entram juntos**; Prova Social antes de "Tudo o que você vai receber"; Garantia antes de "Como é o Acesso".
- `OFERTAS/<id>/site/COPY.md`: a copy da página gerada da Obra (headline = produto / desejo ou dor / pensamento interno — promessa única e específica, botão da 1ª dobra leva aos planos, não ao checkout).
- **Tom (YT 2hSIIWKZlBs):** o público é fundo de funil/consciente; a comunicação é simples e focada no produto, **não emocional nem de dor**. Dor/desejo/pensamento interno alimentam headline e bullets, não viram texto de apelo emocional. Bloco opcional de dor ("Intensificação da Dor") só se a persona estiver acomodada [BOARD blocos opcionais].

Onde montar:
- **WordPress + Elementor + template JSON** (stack do método) se o usuário tiver o
  ambiente.
- Sem esse ambiente: HTML local em `LOW-TICKET/MODELOS/MODELOS-DE-PAGINA/` ou
  `low-ticket-metodo-mvt/references/modelo-de-pagina/` (ler o README — o modelo não traz
  todos os 10 blocos na ordem do método; complete e reordene). Copie para
  `OFERTAS/<id>/site/`.

Visual: paleta do produto (≥3 cores), mockups básico e completo, demonstrativo com o que a
pessoa recebe, 4–5 ícones, imagens leves (WebP). Imagens no nosso ambiente: skill
`gpt-imagem-playwright` (perfil `gpt`, 9222).

**Cards de preço, bônus e downsell (Borba — hipótese a testar, números são do caso dele, não regra dura).** Prova social ACIMA dos cards de preço. Bônus com preço riscado e fecho "128 reais totalmente gratuitos porque os bônus são todos grátis" [BORBA f8HMw89DAOE]. 2 cards: âncora de entrada (R$10, o preço do criativo, SEM bônus) × completo (R$27,90, com os 4 bônus); a maioria leva o completo. Clicar na âncora abre pop-up de downsell "do seu produto de 27,90 para 17,90" [BORBA f8HMw89DAOE]. Opcional: pop-up de saída (exit-intent) com preço menor ("pop-up com uma da Dacell de 9,99" na saída da página) [BORBA-GA GwKEMxzTSjg]. Casa com "criativo ≡ página ≡ ticket"; o criativo continua sem mostrar bônus.

**Prova social na página:** skill **`depoimentos-pagina-de-vendas`** — coletar depoimentos estruturados pra página; skill **`gerador-depoimentos-instagram-gpt`** — gerar vídeos de depoimento curtos pra redes. **Otimização de conversão:** skill **`page-cro`** — testar elementos da página pra taxa de clique; skill **`popup-cro`** — testar popup de saída e oferta de último minuto.

---

## 7 · PRODUTO

Método: `references/pagina-produto-criativo.md` §2. Primeiro entenda o que está vendendo
("o que preciso entregar de produto para a persona compradora?"). **MVP** para ir ao ar
(sem 30 dias criando) + **MODELO** (páginas diagramadas para mockup, página e criativo);
o completo vem com a oferta rodando. Aviso na área de membros de que está sendo
atualizado. Salve em `OFERTAS/<id>/produto/`.

Ferramentas do nosso ambiente: ChatGPT pelo browser (`gpt-imagem-playwright`; o perfil
`gptwork`, 9243, é a mesma conta), Canva, curadoria, PLR com direito de revenda.

A ordem interna da entrega (texto → referência → amostra → MVP 40% → área de membros) e a mecânica de
imagem estão na seção `## FASE DE CONSTRUÇÃO` acima + skill `imagens-pagina-low`. Não repetir aqui.

---

## 8 · CRIATIVO

Método: `references/pagina-produto-criativo.md` §3. **3 a 5 demonstrativos.** Copy em 3
partes saída da página (headline → subheadline/benefícios → "clique em saiba mais"),
takes mostrando o produto (arquivos, impresso, tela, resultado final), narração natural,
edição com início forte, cortes, legenda e destaque visual. Checar a lista de erros do
board antes de exportar. Salve em `OFERTAS/<id>/criativos/`.

Ferramentas do nosso ambiente, se for gerar em vez de gravar: comece por `criativo-ads`
(porta única: estratégia da leva e escolha do formato), que puxa `narracao-hub-tts` (voz),
`gpt-imagem-playwright` (imagens), `criativo-ads-video-orq` / `hub-video-playwright`
(vídeo). A regra continua a do método: se a pessoa precisa imaginar o produto, está errado.

**O criativo mostra a CONCEPÇÃO e o PRODUTO PRINCIPAL — não os bônus nem a garantia** [YT 2hSIIWKZlBs: "a pessoa não sabia os bônus… mostrava a minha concepção, mostrava o produto principal"]. Bônus e garantia ficam na página.
**Criativo em IMAGEM (feed 4:5) — estrutura do Borba:** headline chamativa com a quantidade de itens → mockup do produto → preço → benefícios empilhados → CTA apontando pra baixo; "criativo na resolução 4x5 do Instagram" [BORBA lttuZrujLEE]. Complementa o padrão "criativo direto" (headline + mockup + preço + CTA), sem repetir a regra de não mostrar bônus.

**Gate antes de exportar — checklist dos erros do criativo demonstrativo** [BOARD ESTRUTURA DO CRIATIVO DEMONSTRATIVO]; marque OK/NÃO por linha no roteiro do criativo (`CRIATIVO-N/roteiro-*.md`), e um NÃO bloqueia a exportação: (1) diz claramente o que é o produto · (2) não é curiosidade sem explicação · (3) o que se diz bate com a página · (4) gera identificação ("isso é pra mim") · (5) mostra o produto por dentro · (6) tudo o que aparece tem relação com o produto · (7) tangibiliza (a pessoa entende o que compra) · (8) voz natural, não robótica · (9) mostra mais do que fala · (10) duração curta para tráfego frio · (11) tem legenda. Copy = a da página (agente executor no ChatGPT), em 3 partes já acima.

---

## 9 · CONFIGURAÇÕES TÉCNICAS

Método: `references/pagina-produto-criativo.md` §4 — proteção (Protectify no método),
plataforma de vendas, Facebook Ads, UTMify (5 configurações). **Checklist do board** [BOARD CHECKLIST — CONFIGURAÇÕES TÉCNICAS GERAIS], registre cada linha feita/não no ESTADO da oferta antes do passo 10: Protectfy (config completa · baixar o txt com link/parâmetro/script · inserir o script na página) · Plataforma de vendas (cadastrar produto · subir conteúdo · formas de pagamento · link de checkout nos botões da página) · Facebook Ads (BM · conta de anúncio · pixel + configuração · forma de pagamento · pixel na plataforma de vendas) · UTMify (configuração · script do pixel na página · script de UTM na página). Se o dono não usa Protectfy, escreva "Protectfy: não usada" — decisão dele, não pulo silencioso. Mecânica de plataformas do
nosso ambiente: `hotmart-produto-playwright`, `ggcheckout-produto`; receitas de UTMify e
Events Manager em `~/.claude/browser-workspace/domain-skills/`.

---

## 10 · TRÁFEGO

Tráfego: skill `metaads-kevones`. Esta skill não traz metodologia de tráfego.

Entregue ao usuário, antes de subir (GATE 7 — exige os quatro itens com evidência): página no ar · checkout · 3–5 criativos · GATE 6 marcado. **Configurações de tracking:** skill **`trackeador`** — invocar pra instalar pixel Meta, remover trackers de terceiros, eventos de conversão; skill **`analytics-tracking`** — configurar eventos adicionais pra Dashboard e reporte.
