---
name: area-membros-netflix
description: Entregável de área de membros estilo Netflix (hero + grid de módulos, bloqueado/desbloqueado com modal de compra) para infoprodutos e produtos digitais. Use sempre que o usuário pedir "área de membros", "hub de módulos", "página de aluno", "dashboard do cliente pós-compra", "portal do produto", ou qualquer entrega logada onde o comprador acessa o conteúdo que pagou e vê add-ons que ainda não comprou. Também use quando o pedido for "cria uma área de membros como a Netflix/Creator Pack/[curso X]" ou mencionar grid de thumbnails com cadeado. NÃO é para landing page de venda (isso é copy/checkout) nem para admin/backoffice interno.
---

# Área de Membros estilo Netflix

> **REGRA FIXA DA DONA (repetida muitas vezes; não perguntar, não inventar alternativa):** área de membros é SEMPRE a NOSSA, externa, no site da oferta (`https://<site>/painel`). NUNCA a área de membros do checkout (Wiven, GG, Hotmart, Mundpay) nem página de obrigado genérica dele. Por isso: (1) redirect/página final pós-compra de TODA oferta e bump → `<site>/painel`; (2) link de entrega/e-mail do checkout, se existir → `<site>/painel`; (3) liberação por webhook no nosso servidor (e-mail → SKUs comprados); (4) e-mail de acesso pelo Resend da LeadGo (`no-reply@seudominio.com`) com o link do /painel e "entre com o e-mail da compra". Pronto só com venda-teste REAL provando: webhook liberou → login com o e-mail entra → e-mail chegou. Motivo: em 26/09/2026 a 1ª cliente do Mapa do Tarot BR pagou e não recebeu nada (webhook ignorava a venda, nenhum e-mail saía).

> **REGRA FIXA DA DONA (16/10/2026): FAVICON.** Toda oferta tem **favicon na PÁGINA e na ÁREA DE MEMBROS (`/painel`)**. Arquivos em `site/img/` (`favicon.svg` + `favicon-32.png` + `apple-touch-icon.png` — o servidor padrão só serve a raiz `index/terms/privacy` + as pastas `img/painel/assets`), com `<link rel="icon">` no `<head>` dos 4 arquivos (`index.html`, `terms.html`, `privacy.html`, `painel/index.html`).

> **REGRA FIXA DA DONA (16/10/2026): aviso "material em atualização" some pro USUÁRIO DE TESTE.** O aviso **"MATERIAL BEING UPDATED"**, os contadores **"X of Y published"** e o **"Content being updated"** do leitor existem pro **cliente real** (a área sobe antes do conteúdo final) — **vale pra toda oferta**. Mas pro **usuário de teste** (e-mail `teste-*@leadgo.dev`, ex.: `teste@seudominio.com`) eles **NÃO aparecem** — a área mostra tudo **"Complete"**, sem contador, pra gravar criativo com a área "pronta". Padrão a copiar: helper **`isTestUser()` = `/^teste.*@leadgo\.dev$/i.test(getEmail())`** (o e-mail da compra vive no `localStorage`, ex. `gn_email`). Aplicar em 3 pontos: (a) esconder `#aviso-atualizacao` no boot do hub (`renderHub`); (b) no `cardHtml`: `cnt=''` e pill `Complete` se teste, senão o `In update`/`X of Y published`; (c) o "Content being updated" do leitor só quando **não** for teste.

Entregável reutilizável: hub pós-compra onde o cliente vê, num grid de cards, o produto principal (sempre desbloqueado) e os add-ons/upsells (bloqueados até a compra). Layout de referência veio de um hub estilo "The Creator Pack" (hero grande + grid de thumbnails com badge). A referência é só de LAYOUT — hero + grid — não copie literalmente "N Módulos"/"N Aulas" se o produto não for um curso.

Imagem de referência: `assets/referencia-layout.png`.
Implementação real (Next.js) usada como base desta skill: `assets/PanelHub.reference.tsx` — componente completo testado em produção, adapte os nomes de domínio (SKU, produto) para o projeto novo.

## Quando usar

- Usuário já tem um produto principal + um ou mais add-ons/order bumps vendáveis separadamente.
- Precisa de uma tela pós-login onde o cliente vê o que já comprou (acessível, colorido) e o que ainda não (cinza, cadeado, preço).
- Quer consistência visual com o resto do site (paleta, tipografia), não um tema genérico "dashboard SaaS".

## Anatomia do entregável

1. **Hero** — saudação personalizada (nome do cliente) + título curto. Sem métricas fake, sem "N módulos" se não fizer sentido pro produto.
2. **Grid de cards** — um card por módulo/produto. Cada card:
   - Imagem quadrada (capa/ícone do módulo).
   - Título + subtítulo curto.
   - **Desbloqueado**: colorido, clicável, link direto pro conteúdo.
   - **Bloqueado**: imagem em grayscale + opacity reduzida, ícone de cadeado sobreposto, badge de preço. Clique abre modal, NUNCA leva direto pra um checkout de recompra sem contexto (ver seção de risco abaixo).
3. **Modal de módulo bloqueado** — título, descrição breve do que é, preço, CTA. O CTA aponta para o canal de venda pós-compra que já existe no projeto (suporte manual, WhatsApp, ou checkout de recompra SE já existir com o guard correto — ver abaixo). Nunca inventar checkout novo sem avaliar o fulfillment.
4. **Footer/topbar** — contato de suporte + logout. Preferir topbar (visível sem scroll) a footer enterrado.

## Estados de PRODUÇÃO do card (além de comprado/bloqueado)

Todo produto/módulo tem CAMADAS. O card reflete o estado de produção, não só o de compra —
assim a área já nasce "cheia" e vai completando conforme a demanda:

- **Comprado + completo** → card normal, colorido, clicável, conteúdo inteiro.
- **Comprado + só MVP (não completo)** → card acessível, MAS com faixa/badge *"Em
  atualização"* (nunca escrever "MVP" pro cliente — é termo interno nosso) e, quando fizer
  sentido, um segundo card/linha abaixo marcando o que ainda vem. O cliente já usa o
  conteúdo parcial; a gente completa quando a demanda confirmar.
- **Produto ainda NÃO produzido** (planejado, sem conteúdo) → card placeholder cinza com
  selo *"Em breve"* / *"Em produção"* (ou botão interno "atualizar/guardar" no modo edição).
  Não some da grade — fica reservando o lugar, mostrando a esteira completa.
- **Não comprado (add-on)** → grayscale + cadeado + preço (regra de compra acima).

**Por quê:** deixa a área mais completa visualmente desde o dia 1 e barata de preencher —
à medida que a demanda de cada item aparece, troca o placeholder/MVP pelo conteúdo final,
sem redesenhar a grade. Memória `entregavel-camadas-area-membros`.

## Organização por categoria + comprado × recebido

**Ordem das linhas no hub (regra da dona, 03/10/2026):**
1. **Linha 1 — "Seus Módulos": o que vem no produto**, nesta ordem: primeiro o **Básico** (só o principal — **bônus NÃO acompanha o básico**), DEPOIS o **Completo** (bônus 1-4 + módulo de upgrade, ex.: Arcanos Menores). **Bônus é parte do produto** (regra da dona 09/10/2026): liberado pelo webhook quando a oferta do COMPLETO é paga, nunca vira produto/oferta no checkout. Bônus do produto nunca fica depois das ofertas avulsas.
2. **Linha 2 — "Ofertas especiais"**: itens vendidos à parte no checkout (o que tecnicamente é order bump/combo). **NUNCA escrever "order bump" na área de membros** — para o cliente o nome é sempre "Ofertas especiais".
3. Implementação: lista explícita de SKUs do produto (ex.: `PRODUTO_SKUS = ['principal','bonus-1',...,'bonus-4','completo']`) define a ordem da linha 1; o resto do MODULES vai pra linha 2. Não depender da ordem do array MODULES.

A área é o CANAL de entrega padrão (não PDF solto). Ao popular, subir CAPA + arquivos
do MVP de cada item, organizado — mas SEM forçar 3 seções rígidas Principal/OrderBump/Bônus:
- Cada ORDER BUMP e cada BÔNUS com NOME PRÓPRIO e identidade clara; **nunca confundir bônus
  com order bump** — são coisas distintas (bônus mora no produto; bump é produto solto no checkout).
- **Card de bônus bloqueado NUNCA diz "incluso/somente no Completo"** (regra da dona
  13/10/2026, substitui a redação de 09/10): diz **"Upgrade com desconto"** (badge, CTA,
  linha do modal, botão) + o preço de upgrade (R$5,90, fórmula fixa, nunca os 30%/50% off
  antigos) + link direto do upgrade Essencial→Completo. Só bump/upsell têm preço próprio
  deles mesmos. Regra cheia: `criacao-low-ticket-mvt` › `## REGRA DO BÔNUS × PLANO × BUMP` +
  `_memoria/preferencias.md`.
- O PRODUTO PRINCIPAL pode ter CATEGORIAS INTERNAS pro cliente (ex.: Cat. 1 = Arcanos Maiores,
  Cat. 2 = Arcanos Menores) — organizar o conteúdo dele por dentro à vontade.
- Respeitar **comprado × recebido**: acessa só o que comprou (ownership por SKU); não comprado
  bloqueado (cadeado+preço); não-produzido como placeholder.

## Leitor do módulo e download (PDF do módulo inteiro)

Conteúdo de cada módulo é entregue como PÁGINAS EM IMAGEM (texto escrito → cada página gerada como imagem via GPT com referência visual travada), exibidas em sequência vertical dentro do leitor do próprio painel, mantendo o header/visual da área e botão Voltar. Não é HTML solto com design próprio.

**Regras obrigatórias:**

1. **PROIBIDO download por imagem individual.** Nem botão "baixar esta página" embaixo de cada imagem, nem link de imagem solto. Fallback de erro de carregamento pode exibir "tentar novamente", só isso.

2. **Botão "Baixar PDF" no topo do leitor E repetido no FIM do módulo** (botão grande, centralizado, "📥 Baixar PDF do módulo inteiro", depois da última página — quem terminou de ler procura o download lá embaixo; regra da dona, 03/10/2026). Os dois entregam o **MÓDULO INTEIRO** num PDF (1 página PDF = 1 imagem do módulo, na ordem de leitura, A4/retrato, sem margens brancas extras), pronto pra imprimir.

3. **PDF sai do PRÓPRIO módulo, na hora — nunca arquivo PDF separado** (regra da dona, 03/10/2026). PDF pré-gerado e guardado no repo fica velho assim que entra página nova (caso real Mapa do Tarot: leitor com 61 páginas, PDF com 41). Receita:
   - O servidor lê o MESMO array `pages` que o leitor usa (`const MODULES = [...]` do `painel/index.html`, avaliado com `node:vm`, cacheado pelo mtime do HTML) e monta o PDF com essas imagens, na ordem do leitor: 1 JPEG por página, `DCTDecode` sem recompressão, largura A4 e altura proporcional à imagem.
   - Zero dependência (não precisa img2pdf/Chromium no container alpine). Referência pronta: `assets/modulo-pdf.reference.mjs` (`modulePdf(root, sku, lang)` → `{ buf, etag, title }`), rota `GET /painel/api/modulo-pdf/<sku>` com a **mesma checagem de sessão + posse do SKU** das imagens.
   - Cache em memória pela assinatura (lista de páginas + tamanho/mtime de cada imagem). Mudou `pages` ou trocou uma imagem = PDF novo na próxima requisição. Módulo de 61 páginas monta em ~20 ms.
   - **Nome do arquivo = nome do módulo** (`title` do MODULES): `Content-Disposition: attachment; filename*=UTF-8''<título>.pdf` no servidor e `a.download = title + '.pdf'` no cliente. Nada de prefixo tipo "Produto - " nem sku.
   - ⛔ Módulo NOVO nunca é HTML: folha de exercício, pôster, checklist e página de imprimir = imagem gerada no GPT, A4, com a referência visual da oferta (nunca HTML/SVG/Pillow). O caso abaixo é só legado.
   - Módulo legado que é HTML (não imagens, ex.: Cigano): PDF estático gerado do `index.html` do módulo com `chromium --headless --no-pdf-header-footer --print-to-pdf`, e o **pre-commit bloqueia** se o PDF estiver mais velho que o HTML. Módulo sem PDF = botão quebrado no ar.

4. **Erro de download: aviso inline com link direto — NUNCA `window.print()` como fallback.** Em 15/10 o Tarot tinha `window.print()` no `.catch()` do download: quando o `fetch` do PDF falhava (sessão expirada, 404, rede), o cliente recebia a **caixa de impressão** em vez do arquivo e reportava "o PDF não baixa / dá erro". O método correto, no cliente:
   ```js
   // HEAD confere antes de navegar (nunca navega pra 404/403); download é NAVEGAÇÃO
   // DIRETA (o servidor manda Content-Disposition com o nome) — sem blob na memória
   // do celular; erro vira aviso com link de retry, não impressão.
   function downloadPDF(sku, btn){
     const url = '/painel/api/modulo-pdf/' + sku;
     fetch(url, {method:'HEAD', credentials:'same-origin', cache:'no-store'}).then(r => {
       if (!r.ok) throw new Error('pdf-' + r.status);
       window.location.href = url;                  // baixa de verdade
     }).catch(() => {
       const p = document.createElement('p');
       p.className = 'pdf-erro';
       p.innerHTML = 'Não deu pra baixar agora. <a href="' + url + '">Tentar de novo</a>';
       btn.insertAdjacentElement('afterend', p);
     });
   }
   ```
   - **Dentro do app do Instagram/Facebook o download é bloqueado em SILÊNCIO** (WebView ignora `a.download`/navegação) — o cliente vê "não baixa" sem erro nenhum. Mostre um aviso **preventivo** no topo do leitor quando `isInAppBrowser()` (`/Instagram|FBAN|FBAV|FB_IAB|WhatsApp/`), com botão "Copiar link do painel" (referência: `painel/index.html` da Elétrica).
   - Blob (`fetch → blob → <a download>`) só como caminho alternativo: em PDF grande (Tarot `completo` = 42 MB) falha calado no celular.
   - Histórico: **TODO painel novo copia este bloco pronto** — não reescreve o download à mão (JJ 15/10 saiu sem botão nenhum; Tarot 15/10 caiu na impressão; Elétrica já tinha o certo).

5. **Verificação obrigatória antes de dar como pronto — API E UI (as duas, sempre):**
   - **UI (o que faltava):** o leitor tem que ter botão de PDF ligado no endpoint. `grep -i pdf painel/index.html` precisa achar o handler **e** a função do botão (`pdfBottomButton`). Verifique no ar com a conta de teste: logar, abrir um módulo e **clicar** — o arquivo tem que aparecer no Downloads com o número de páginas = `pages` do módulo.
   - **API:** `node scripts/check-download-pdf.mjs <url-da-oferta> <email-de-teste>` (LOW-TICKET) ou `curl -b cookie.txt -OJ https://<site>/painel/api/modulo-pdf/<sku>` → HTTP 200, `%PDF-`, nome = título do módulo, `pdfinfo | grep Pages` == tamanho do array `pages`.
   - Deslogado/sem o SKU → **403** (não 404: 404 genérico mascara rota inexistente).
   - **Passar SÓ a API não prova entrega** — foi exatamente assim que o JJ ficou "verde no gate" com o cliente sem baixar nada (rota no ar, zero botão na UI). Os três casos de 15/10 estão no `CLAUDE.md` da raiz, seção do gate de download.
   - **Módulo agregador (combo/kit) não gera página própria**: confira que ele concede os SKUs dos módulos que agrega (no webhook **e** derivando a posse pra quem já comprou antes do fix) e que o card mostra "Liberado/Incluído abaixo" — item **pago** aparecendo como "Em breve"/"Desbloquear" é o que faz o cliente achar que a área de membros "não funciona".

## Regra de ouro: tema da marca, não tema genérico

Nunca assuma dark mode "estilo Netflix" literal. Use a paleta e tipografia que já existem no projeto (cores, fontes, componentes de UI já usados nas outras páginas do site). Se o projeto usa tema claro, o hub fica claro — "estilo Netflix" descreve a ESTRUTURA (hero + grid + cadeado), não a cor. Confirme com o usuário antes de assumir dark, principalmente se ele já corrigiu isso antes num projeto anterior.

**Arte do card/banner da área (oferta de membro):** mesma régua de mockup — **produto visível e legível** na arte, **cena na paleta da marca**, **sem preço queimado** (preço sai da fonte única), banner **1600×533 (desktop)** + **778×836 (mobile)**, webp leve. Boa × feia (caso Diário Astral, 16/10/2026): `imagens-pagina-low` › "Imagem de PRODUTO/oferta (capa de checkout, card e banner da área) — boa × feia".

**Toda peça de venda da área EXPLICA o que vem** (dona, 16/10/2026): a **barra fixa** e o **banner/card** não podem dizer só "Diário Astral · R$12,90" — levam uma **linha curta do que está incluso** (ex.: "Horóscopo diário no seu mapa · Mapa Astral de brinde · Guia do Mês"), em bullets curtos, vinda da **mesma fonte única** da peça. No celular, até 2 linhas curtas (a barra pode ser mais alta que o padrão, sem overflow em 390px). Vale pra toda oferta de membro, não só essa.

## Risco que quebra em produção: venda de add-on pelo hub — e como resolver de verdade

Este é o erro mais caro e mais fácil de cometer. Quase todo backend de fulfillment (webhook de pagamento → aplica status → agenda entrega → reenvia PDF/e-mail → dispara evento de conversão pro pixel/CAPI) foi escrito assumindo que **toda ordem aprovada = venda nova do produto principal completo**. Se o hub linkar direto para um checkout de recompra de add-on sem adaptar esse fluxo primeiro, a venda do add-on:

- reenvia o e-mail/PDF completo como se fosse o produto principal de novo;
- pode disparar o evento de conversão (Purchase) com o valor cheio do produto principal, inflando métricas de tráfego pago;
- pode reagendar a entrega do zero.

**Não pare em "manda pro suporte"** — isso é só o estado seguro temporário até implementar de verdade. A implementação real, feita e testada nesta skill (09/09/2026), tem 4 peças:

1. **Guard no fulfillment**: no ponto onde a aprovação agenda a entrega completa (tipo `if (status === APPROVED && !order.deliverAt) { ...agenda... }`), acrescente `&& orderSkus(order).includes(SKU_DO_NUCLEO)`. Uma ordem de add-on avulso nunca leva o SKU do núcleo, então nunca entra nesse bloco — zero regressão pro fluxo que já vende hoje (toda ordem existente TEM o núcleo).
2. **Rota de API separada** (`/api/panel/comprar`, não a `/api/checkout` principal): a rota principal tem uma guarda "já pagou? não deixa comprar de novo" que é correta para venda nova e é EXATAMENTE o que precisa ser contornado aqui (ela já tem uma aprovada, por isso está no hub). Resista à tentação de abrir uma exceção dentro da rota principal — uma rota nova, pequena e auditável, é mais seguro que uma exceção escondida na rota que move a maior parte do dinheiro do site. Essa rota:
   - Exige sessão (`currentUser()`), não é anônima como o checkout normal.
   - Exige que o lead já tenha uma ordem aprovada com o núcleo (senão devolve 403 — sem núcleo, o caminho certo é o checkout normal, não este).
   - Filtra os SKUs pedidos contra os que ela já tem aprovados (não deixa comprar de novo o que já tem).
   - Cria a ordem com só os SKUs pedidos (sem o núcleo) e chama o MESMO gateway de pagamento (Mercado Pago/preferência, ou o gateway local) que a rota principal já usa — o webhook de aprovação é genérico por `orderId`, não precisa mudar.
   - Precisa de uma função de cotação PRÓPRIA para add-ons sem núcleo (a função de cotação principal geralmente antepõe o produto principal sozinho, e cobraria ele de novo).
3. **Página de compra** (`/panel/comprar/[sku]`): server component que valida sessão + ownership (redireciona pro hub se não tiver o núcleo, ou se já tiver esse SKU) e passa pro componente client os OUTROS add-ons que ainda faltam, como opcionais na mesma compra — a mesma lógica de "aproveche y sume" do checkout principal, agora pós-venda.
4. **Ligar o CTA do modal** a essa rota (`/panel/comprar/${sku}`), não mais a um canal manual.

**A página de compra tem que parecer o mesmo checkout, não uma tela minimalista aparte.** Primeira versão desta skill fez uma página client bem básica (sem banner, sem os cards com imagem) — o feedback real foi "era pra abrir o checkout normal como é aqui, só com o item selecionado e os outros bumps". Reuse o MESMO banner (`/checkout/banner-<país>-desktop.jpg`), a MESMA classe de card do bump (`border p-3.5`, imagem 56×56, preço tachado+final) e o MESMO layout de resumo (coluna da direita com as linhas + total). O item que trouxe ela até ali fica pré-marcado e **travado** (checkbox disabled) — ela não veio até aqui pra desmarcar o que já queria comprar.

**Teste as 3 guardas antes de considerar pronto** (todas via `curl` direto na API, mais rápido que clicar): (a) usuário sem o núcleo tentando comprar um add-on → 403; (b) usuário comprando um SKU que já tem aprovado → filtrado, erro "nada para comprar" se sobrar vazio; (c) usuário comprando um add-on que falta → cria ordem com o valor CORRETO (só o add-on, não o núcleo de novo) e devolve o link/QR de pagamento real do gateway.

## Login SEM SENHA — só o e-mail da compra (regra da dona, 29/09/2026)

A área de membros entra SÓ com o e-mail usado na compra. Nenhum campo de senha, nem
"senha só para contas de demonstração", nem senha opcional. Conta de teste/demo também
entra só com e-mail. Se a tela de login tiver qualquer campo de senha, é bug — remover.

## Conta de teste padrão — TUDO liberado (regra da dona, 29/09/2026)
Todo /painel nasce com a conta **teste@seudominio.com** (mesmo e-mail em TODO
projeto e mercado), com todos os SKUs liberados: principal, tier completo, cada bump,
combo e upsell/irmão. Ela entra só com o e-mail, como cliente normal. Serve pra aprovação de
checkout (analista do gateway entra sem comprar) e pra gravação de tela dos criativos.
Criar no mesmo deploy do painel. Prova no ar: logar e ver tudo aberto, sem cadeado nem
card de oferta de membro. Formulário de gateway que exige senha (Mundpay): esse e-mail +
senha de apoio, que o painel ignora.

## Ofertas de membro — preço de quem já é cliente (regra da dona, 29/09/2026)

Toda área de membros vende pra quem JÁ comprou: ela já confia, só vai levar mais um.
Por isso tudo que ela ainda não tem aparece com **30% off** do preço normal:
(**Oferta BR nova a partir de 08/10/2026:** bumps R$ 5,00, combo R$ 9,90 e upsell R$ 9,90 fixos — tabela
`low-ticket/references/CONSTRUCAO.md` › PREÇO PADRÃO BR; vale sobre o 30% off e o piso abaixo.)

- **Upgrade de tier** (comprou o básico/Essencial → tem o completo/PRO bloqueado):
  **SUPERSEDE a regra de % abaixo (dona, 13/10/2026): upgrade BR = SEMPRE R$5,90 fixo**,
  sem cálculo de percentual, numa oferta própria "Upgrade Essencial → Completo - Área de
  Membros" na gateway, cadastrada uma vez por oferta (ver `wiven-checkout` + exemplo real
  em `_memoria/preferencias.md`). Mercado sem essa oferta cadastrada (PT/ES/outros): usa o
  cálculo velho de 50-60% off (`normal × 0,50`, ,90 abaixo) até cadastrar a oferta fixa.
- **Cada order bump / bônus** que ela não tem: 30% off.
- **Combo** dos que faltam: 30% off do combo normal.
- **Produto irmão / upsell** (ex.: Cigano no Mapa do Tarot): 30% off.
- Qualquer outro item vendável que apareça no painel: mesma regra.

Cálculo: `normal × 0,70`, arredonda pro final **,90** mais próximo abaixo.
**Piso R$9,90:** se o preço com desconto ficar abaixo de 9,90, NÃO dá desconto — o
item fica no preço normal. Nunca vender nada abaixo de 9,90. **Em EUR (Mundpay/Europa) o piso é €4,90** (decisão da dona 29/09).

Visual: preço normal riscado + preço de membro. Só mostra o que ela NÃO tem (ownership
por SKU). Checkout: OFERTA criada dentro do produto já existente de cada item (bump → no produto do bump; upgrade → no produto principal), nunca produto novo, nome "<item> - Área de Membros", item
único, redirect pós-compra → `<site>/painel`, webhook libera o SKU certo (ver seção
abaixo sobre add-on não reenviar o núcleo). InitiateCheckout com value/currency em
todo botão (gate de eventos do LOW-TICKET). Em host com Trackeador dono do IC
(`capi_ic_hosts`): `data-tk-value`/`data-tk-currency` em cada botão, com o preço de membro.

**Mudança de preço: gateway primeiro, painel depois.** Trocar o preço no checkout
(Wiven/Mundpay), conferir o checkout real mostrando o valor novo, e só então publicar o
preço novo no /painel. Nunca o painel mostrar um valor e o checkout cobrar outro.
Prova de cada card: abrir o link numa sessão de navegador separada e ver nome + preço
certos (link errado = "Checkout não encontrado"; curl na Wiven dá 403, não prova).
Config por item: `CHECKOUT_MEMBROS` no painel, com código da oferta mapeado pro SKU no
webhook.

## Camada de monetização da área — barra fixa + banner (dona, 16/10/2026)

Aprendido na prática do Mapa do Tarot (desenho completo em
`OFERTAS/mapa-do-tarot/produto/CAMADA-MONETIZACAO-AREA-MEMBROS.md`).

- **Onde a peça aparece:** **banner fora das views** → home **E** tela dos módulos, mas **NÃO no
  leitor** (o leitor não tem `main.wrap`). Pra vender enquanto o cliente lê, é a **barra fixa
  inferior** (hub **E** leitor). Fechável (X), 1 modal por vez, memória por sessão/dia.
- **Fonte única:** uma tabela no topo do painel (ex. `OFERTAS_AREA`/`OFERTAS_BARRA`/`DIARIO_ASTRAL`)
  manda em **url + preço + arte** de TODAS as camadas — mudar preço = mudar num lugar só;
  **zero preço literal** no card (regra do `PRECOS_AREA`).
- **A peça EXPLICA o que vem:** barra e banner **não** dizem só "produto · preço" — levam uma
  **linha curta do que está incluso** (bullets), no PC e no celular (até 2 linhas, sem overflow em
  390px). Vale pra toda oferta de membro.
- **Arte:** régua "boa × feia" em `imagens-pagina-low`; banner **1600×533 (desktop)** + **778×836
  (mobile)**, webp leve, **sem preço queimado** na arte.
- **Camada ADITIVA:** não mexe nos cards/preços/checkouts atuais nem nos módulos do leitor.
- **Oferta de membro pode ter ENTREGA EXTERNA** (ex.: Diário Astral / Mapa Astral = **AstroDicas**):
  não é módulo do `conteudo/` — o `audita.py` **não conta**; entra no MANIFESTO como "entrega
  externa" e o produto tem os **2 webhooks** próprios (entrega + Trackeador). A venda sai pelo botão
  (`data-tk-value`/`data-tk-currency`); IC pelo Trackeador, sem `fbq` manual (não duplicar).
- **Código novo FORA da região que o `modulo-pdf.mjs` avalia no `vm`** (do `const MODULES` ao
  `LOCK_SVG`): helper/DOM ali dentro derruba o PDF do módulo inteiro (caso Elétrica 13/10). O que
  mora ali é só dado puro (o bloco lido de `OFERTAS_*` é avaliado no `vm`).
- **Gates antes de "pronto":** 390px sem overflow (`scrollWidth ≤ innerWidth`) · `check-download-pdf.mjs`
  no ar · `adstrackeador verificar-site` (IC no clique) · prova com a conta de teste logada · deploy
  (Coolify) provado no ar (HTML + assets 200). Ordem de risco: começar pela **barra fixa** (menor
  risco); bolha/popup/card-no-módulo numa 2ª rodada.

## Passo a passo de implementação

1. **Levantar os módulos**: liste produto principal + add-ons, com sku/id, título, subtítulo curto, imagem, e o "para onde vai" quando desbloqueado (rota própria de conteúdo — não force todo mundo pra fora do hub).
2. **Modelo de dados de ownership**: uma função/query que, dado o usuário logado, devolve o conjunto de skus que ele já comprou (união de todas as ordens aprovadas). Card decide bloqueado/desbloqueado a partir disso, não de um campo solto.
3. **Componente do hub** (ver `assets/PanelHub.reference.tsx` como esqueleto):
   - Lista de módulos como array de config (sku, title, subtitle, image, href).
   - `desbloqueado = sempreDesbloqueado || skusComprados.has(sku)`.
   - Grid responsivo (`repeat(auto-fit, minmax(200px, 220px))` funcionou bem).
   - Estado de modal (`useState<Sku | null>`) para o módulo clicado quando bloqueado.
4. **Páginas de conteúdo por módulo**: cada módulo desbloqueado tem sua própria rota (`/panel/<modulo>`), gated por ownership no servidor (não só esconder no client) — confira a sessão/ordem aprovada antes de renderizar o conteúdo pago.
5. **Página dev-only pra iterar rápido no visual**: uma rota tipo `/dev-seed/panel` que renderiza o hub direto com props mockadas (nome fixo, lista de skus fixa), gated por `NODE_ENV !== "production"`, evita precisar logar e comprar de verdade toda vez que ajustar CSS.
6. **Screenshot antes de dar por pronto**: suba o dev server num DATA_DIR/porta isolados (nunca produção), abra a rota via browser automation, tire screenshot, confira contraste, alinhamento e se o cadeado/preço aparecem só nos bloqueados.

## Aviso "Material em atualização" — PADRÃO em toda área nova (regra da dona, 03/10/2026)

Toda área de membros criada já nasce com um aviso grande no topo: na entrada (hub) e no topo de cada produto/seção. Motivo: a área sobe junto com o criativo, antes de todo o conteúdo estar pronto; o cliente que compra cedo vê o aviso e não reclama.

- Bloco desenhado com os tokens da marca (fundo claro quente, borda forte, ícone ⏳/✨, título em caixa alta 19–24px), `role="status"`, não texto solto.
- Texto padrão (sem prometer dia, ajustar o nome do produto):
  > **MATERIAL EM ATUALIZAÇÃO**
  > Estamos fazendo refinamentos para deixar seu material ainda melhor. Por isso, o conteúdo final e alguns módulos podem ainda não aparecer para você. Seu acesso está garantido: assim que liberarmos, tudo aparece aqui automaticamente, sem você precisar fazer nada.
- "Liberado ainda hoje" só se a dona pedir para aquele caso.
- Fica até a dona mandar tirar (conteúdo completo). Não remover sozinho.

## Conteúdo parcial / em atualização — card de aviso, nunca imagem quebrada (MVP 40%)

Padrão de entrega quando o produto sobe em MVP (~40% pronto, ver memória `mvp-40-porcento`) ou quando um módulo ainda não tem o conteúdo interno finalizado. Regra: **nunca deixar imagem quebrada ou conteúdo de produção vazio aparecer pro comprador.** No lugar, um card desenhado de aviso.

Como aplica:

- **A CAPA do módulo (mockup) fica liberada normal** — o card do grid mostra a capa/mockup como sempre, colorido, clicável. Só o CONTEÚDO POR DENTRO é que vira o aviso quando o comprador entra.
- **Ao abrir um módulo sem conteúdo interno pronto**: em vez das imagens do conteúdo (que estariam quebradas/faltando), renderiza um cardzinho desenhado no meio da área: "Conteúdo em atualização, aguarde" (com a paleta/tokens da marca, ícone leve, não texto solto). Mesmo tratamento para módulo sem quadro/thumbnail — o card de aviso ocupa o lugar.
- **Módulo com pouco conteúdo (poucas páginas/blocos)**: mostra o que já tem em cima e, **no final (lá embaixo)**, um card com o mesmo aviso — sinaliza que vem mais, sem deixar buraco vazio.
- **No lugar exato onde falta conteúdo** (imagem/bloco específico que não carregou): o card de aviso substitui aquele slot, não a página inteira.

O card de aviso é um componente reutilizável (mesma classe/tokens do site) — não é `<img>` com fallback de alt, é um bloco desenhado. Assim o entregável parece intencional ("estamos atualizando") e não bug ("imagem quebrada").

## Performance — área de membros tem que abrir rápido (regra da dona, 03/10/2026)

Área com páginas-imagem fica lenta fácil (módulo de 46 páginas JPG = ~17 MB). Obrigatório:

1. **WebP ao lado de cada JPG/PNG** do painel (páginas, capas, assets): máx. 1200 px de largura, qualidade ~78, `-strip`. Script idempotente no repo (ex.: `scripts/otimiza-painel-webp.sh` do Mapa do Tarot, ImageMagick `magick ... -resize 1200x> -quality 78 -define webp:method=6`). Rodar SEMPRE depois de adicionar/regerar páginas, antes do commit. Resultado medido no Tarot: 17 MB → 5 MB no módulo principal.
2. **Servidor negocia o formato:** pedido de `.jpg` em `/painel/` + `Accept: image/webp` + `.webp` irmão existe → entrega o `.webp` na mesma URL com `Vary: Accept`. O HTML e o PDF continuam usando os JPG originais (PDF sai com qualidade de impressão).
3. **Leitor carrega preguiçoso:** só as 2 primeiras páginas `loading="eager"` (a 1ª com `fetchPriority="high"`); o resto `loading="lazy"`. Cada `<img>` reserva a altura com `aspect-ratio` (pega a proporção real da 1ª página quando ela carrega) — sem isso todas as imagens nascem com altura 0, cabem na tela e o lazy carrega tudo de uma vez.
4. **Cache — cliente SEMPRE vê a versão atual, em qualquer área de membros nossa (regra da dona, 03/10/2026):** tudo em `/painel` (HTML, páginas, capas, assets, PDF) sai `Cache-Control: no-cache` (pago: `private, no-cache`) + `ETag` → browser revalida toda vez e recebe 304 barato quando nada mudou. PROIBIDO `max-age` longo ou `immutable` em qualquer coisa da área de membros (antes: conteúdo 7 dias, capas 1 ano immutable, HTML 5 min = cliente via página/PDF velho). `immutable` só para asset do site de vendas fora do painel. Reforço no cliente: imagens com `?v=ASSET_VERSION` (subir a cada atualização de conteúdo) e `fetch` do PDF com `{cache:'no-store'}`.
5. **gzip** em HTML/JS/CSS/JSON acima de 1 KB.
6. **Hub:** capas dos cards `loading="lazy"` (exceto o que aparece na 1ª dobra); nada de vídeo/GIF pesado no hero.
7. **Verificar:** `curl -sI -H 'Accept: image/webp' <url-da-pagina.jpg>` → `content-type: image/webp`; DevTools/agent-browser abrindo um módulo: requests iniciais ≤ 3 páginas.

## Conteúdo real por trás de cada módulo — não pule esta pergunta

Antes de declarar um add-on "pronto para vender" no hub, confirme que ele tem conteúdo de verdade por trás (PDF, página, áudio, o que for) — ou trate como bloqueado/pendente e avise o usuário. Vender um SKU que abre um módulo vazio é pior que não ter o módulo. Se o conteúdo depender de lógica de domínio sensível (ex.: um cálculo específico, uma gravação de áudio), NÃO invente o conteúdo sozinho — pergunte ou trate como placeholder explícito gated por flag, nunca como texto definitivo sem validação.

## Hero com imagem de fundo: altura fixa, não `aspect-ratio` + `position:absolute`

Se o hero levar uma imagem de banner (não só gradiente CSS), NÃO monte o título como `position:absolute` ancorado ao fundo de um container com `aspect-ratio`. Foi tentado nesta skill e quebrou: o container de aspect-ratio calculava uma altura maior do que a área visualmente ocupada pela imagem (a largura real do container não era a esperada por causa do layout ao redor), e o título — corretamente posicionado NO CÓDIGO — ficava visualmente atrás/abaixo do grid de cards seguinte, invisível, sem erro nenhum no console.

Correção que funcionou: banner com **altura fixa em rem** (`height: "13rem"`, não `aspectRatio`), degradê de rodapé só pra fundir com o fundo da página, e o título **em fluxo normal, DEPOIS do banner** (outro `<div>` sequencial, nunca `position:absolute` sobreposto). Mais simples, sem esse modo de falha silencioso. Sempre confira com `getBoundingClientRect()` via `agent-browser eval` se o elemento de texto realmente cai dentro da área visível — não confie só no screenshot em si (ele pode ter sido tirado antes do layout assentar).

## Imagem de fundo clara ≠ texto claro por cima

Se pedir a imagem do hero "clara/luminosa" (pra combinar com um site de tema claro), o texto por cima tem que ser ESCURO (`var(--color-bone)` ou equivalente), não creme/branco — champagne-on-champagne é invisível. Esse é o MESMO erro de contraste do tema genérico dark (ver seção "Regra de ouro" acima), só que na direção oposta: sempre confirme o tom de fundo real antes de decidir a cor do texto, não assuma.

## BUG GRAVE: nunca reuse a classe de fundo decorativo do site no container de conteúdo

Se o site já tem um padrão de fundo decorativo global (tipo `.aura`/`.grain` — `position:fixed; inset:0; z-index:-2`, pintado UMA vez no `layout.tsx` raiz), **nunca** aplique essa mesma classe no `<div>` que envolve o conteúdo REAL da página nova (hub, leitura, etc.). Aconteceu nesta skill, em 4 arquivos: o hub e as 3 páginas de conteúdo usaram `className="aura grain"` no wrapper principal, "porque parecia o jeito certo de pintar o fundo".

Resultado: a página inteira (hero, cards, tudo) ficou com `position:fixed` e `z-index:-2` — visualmente **idêntica ao normal**, sem nenhum erro no console, mas **nenhum clique funcionava em lugar nenhum da página**. `document.elementFromPoint(x,y)` no centro de qualquer card devolvia `<body>`, não o card. O sintoma reportado foi literalmente "clico e não abre nada" — sem pista visual de que algo estava errado.

**Diagnóstico**: se cliques não funcionam mas a página parece normal, teste `document.elementFromPoint()` no centro do elemento clicável e compare com o próprio elemento. Se vier `body` ou outro elemento, suspeite de `position:fixed`/`z-index` negativo em algum ancestral — comece pelo classe de fundo global do site.

**Correção**: NUNCA reaplique a classe de fundo decorativo do layout raiz dentro de uma página nova. Se precisar de fundo, use só `style={{ minHeight: "100vh" }}` (ou nem isso, se o body já cobre) — o fundo global do `layout.tsx` já está por baixo de tudo.

## Grid de cards: flexbox, não `grid-template-columns: repeat(auto-fit, ...)`

Com poucos cards (3-5) e tela larga, `repeat(auto-fit, minmax(min,max))` reparte o espaço sobrando de forma torta entre as colunas em vez de jogar tudo pra fora do grupo — produz um buraco enorme no meio e cards grudados nas bordas, mesmo com `justifyContent:center`. Aconteceu nesta skill, só apareceu numa tela bem larga (2560px), não no viewport de teste padrão (1280px) — por isso sempre suspeitar de auto-fit quando o layout parecer bom no teste e o usuário reportar desalinhado numa tela real maior.

Correção: `display:flex; flexWrap:wrap; justifyContent:center` no container, e cada card com **largura fixa** (`width: "220px", flexShrink: 0`) no wrapper. Flexbox manda o espaço sobrando pras margens do grupo inteiro, nunca entre os itens — comportamento garantido, não depende da largura da tela.

## Mobile: grade de 2 colunas, nunca carrossel (regra da dona, 03/10/2026)

No celular os cards ficam em **grade de 2 colunas**, tudo à vista, rolando só pra baixo. PROIBIDO carrossel horizontal/arrastar pro lado — cliente não percebe que tem que deslizar e acha que o módulo sumiu. CSS: `.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}` + `.grid .card{width:auto;min-width:0}`; no desktop (`min-width:820px`) volta para `display:flex;flex-wrap:wrap` com cards de largura fixa. Conferir: `document.documentElement.scrollWidth > innerWidth` tem que dar `false` em 390px.

## Banner de oferta de TERCEIRO na área de membros (dona, 09/10/2026)

Promoção de produto de fora (ex.: SiteExpress na Eletrotécnia) no topo do hub. **Não é card de
módulo nem oferta de membro**: é um banner clicável que sai do site. Só no HUB (não no leitor).

**Dimensões de referência (as que a dona mandou, 09/10/2026) — usar em qualquer banner novo:**

| VERSÃO | PX | PROPORÇÃO | OTIMIZADO (q82) |
|---|---|---|---|
| Desktop | **1600 × 533** | ~3:1 (faixa larga) | webp 47 KB |
| Mobile | **778 × 836** | ~0,93:1 (retrato) | webp 38 KB |

- **Troca em 700px:** `media="(max-width:700px)"` pega o retrato; acima disso, a faixa 3:1.
- Guardar o **PNG original** junto do webp (fonte pra reuso no checkout/Wiven); em produção só o webp.
- Pasta: `site/painel/assets/banner/<slug>-{desktop,mobile}.{png,webp}`.
- **Cache-busting `?v=<data-slug>`** — `/painel/assets` não recebe header de cache imutável.
- `<img width/height>` com as medidas da versão desktop (evita CLS), `loading` eager, `decoding="async"`.
- Link `target="_blank" rel="noopener"` + `aria-label` com a oferta inteira; **fora do gate de
  eventos** (não é botão de checkout desta oferta → sem `data-tk-value`, sem IC).
- `alt` descreve preço/prazo/garantia — é o que sobe se a imagem falhar.

```html
<a class="promo-banner" href="https://PARCEIRO/" target="_blank" rel="noopener" aria-label="…">
  <picture>
    <source media="(max-width:700px)" srcset="assets/banner/<slug>-mobile.webp?v=<AAAAMD-slug>" type="image/webp">
    <source srcset="assets/banner/<slug>-desktop.webp?v=<AAAAMD-slug>" type="image/webp">
    <img src="assets/banner/<slug>-desktop.png?v=<AAAAMD-slug>" width="1600" height="533" alt="…" decoding="async">
  </picture>
</a>
```

CSS mínimo (topo do `main.wrap`, antes do primeiro `.section-title`):
`.promo-banner{display:block;margin:0 0 6px;border-radius:18px;overflow:hidden;background:#0B1220;box-shadow:var(--shadow-md)}` +
`:hover{transform:translateY(-3px);box-shadow:var(--shadow-lg)}`.

Referência no ar: `mapaseletricos.leadgo.dev/painel` (banner SiteExpress, commit `92ef1ec`).
Arquivos-fonte em `OFERTAS/mapas-visuais-eletrotecnia/site/painel/assets/banner/`.

## Preço de venda na área de membros — SEMPRE mais barato que o checkout (dona, 10/10/2026)

Card de peça na área de membros **nunca** mostra o preço de checkout. Quem já está lá não
custa mídia: é lucro puro. Tabela da casa (fonte: `low-ticket/references/PECAS-DO-FUNIL.md` §4):

| Peça | Checkout | Área de membros |
|---|---|---|
| Bump avulso | escadinha 7,90 · 8,90 · 9,90 | **5,90** |
| Combo de bumps | 17,90 | **9,90** |
| Upsell 1 | 17,90 | **9,90** |
| Upsell 2 (o cara) | 27,90+ | **50% off** |
| Downsell | 12,90 | **não existe na área** (é oferta de quem NÃO comprou) |

**Gate obrigatório — nenhum card de venda sem checkout próprio:**

- Todo bump / combo / upsell vendido na área de membros tem **produto + oferta próprios na
  gateway e URL pública** preenchida no mapa de `CHECKOUT_URL` do painel.
- **Item bloqueado é venda, não parede.** O card cadeado mostra **preço de área de membros**
  (5,90 / 9,90 / 50% off, conforme a tabela acima) e **o clique tem que abrir o checkout**.
  Clicar num item bloqueado e não sair nada — ou cair no WhatsApp — é a venda morrendo na
  tela. Momento do clique é o momento da decisão: ou abre o checkout com o preço que o card
  annunciou, ou o card está errado.
- **Três coisas têm que concordar no item bloqueado:** (a) o preço que o card mostra,
  (b) o nome da oferta no checkout, (c) o valor que o checkout cobra. Divergência entre
  eles faz o comprador **fechar a aba** (regra do nome sem preço, skill `wiven-checkout`).
- Card com `null` **não pode cair em link de WhatsApp** — em 10/10/2026 os 4 bumps da
  Mapas Eletrotecnia estavam sem checkout e a cliente acabou pedindo no WhatsApp
  (compradora já existe, não se perde a venda: ela só sai do funil). Link de WhatsApp
  é o **último** recurso (emergência, serviço manual), nunca o padrão.
- Conferir no ar: abrir o painel logado, clicar no botão e **ver o checkout abrindo com o
  preço certo**. Preço do card = preço que o checkout cobra. Vale para **cada** card
  bloqueado, um a um — não basta provar um só.
- Bônus **não** tem preço próprio na área: é do plano Completo — card bloqueado mostra
  **"Upgrade com desconto"** + preço de upgrade (nunca "Incluso no Completo", redação velha).
- **Flag de "soon"/"em atualização" nunca pode esconder o preço de quem AINDA NÃO comprou**
  (bug achado 13/10/2026 no Jiu-Jitsu Sem Força: bump marcado como conteúdo futuro mostrava
  "Em atualização" no lugar do preço pra quem não tinha comprado — escondia a venda).
  `soon`/parcial só pode trocar o badge de quem **já é dono** do item (conteúdo não chegou
  ainda); bloqueado é sempre preço + link, sem exceção.
- **Banner de upgrade/combo/cross-sell mora FORA das views do painel** (fora de
  `view-hub`/`view-home` e de `view-reader`/`view-market`), pra aparecer em TODA tela —
  home E tela de leitura de módulo — nunca só na entrada (regra da dona, 13/10/2026).

### Preço do card = fonte única, nunca literal no card (dona, 10/10/2026)

O card **não escreve o preço**. Ele lê de uma tabela única, no topo do painel, que espelha
o que está sendo ofertado na Wiven como oferta de membro. Mudou o preço da oferta de membro
→ muda **só essa tabela** → o painel inteiro acompanha. Preço espalhado em 9 linhas de card
é preço que um dia fica desatualizado e vende pelo valor errado.

```js
// PREÇO DA ÁREA DE MEMBROS = FONTE ÚNICA
const PRECOS_AREA = {
  'principal': 17.90,
  'ob-seguranca': 5.90, 'ob-medicao': 5.90, 'ob-comandos': 5.90,
  'ob-combo': 9.90,
};
function brl(v){ return v == null ? '' : 'R$ ' + v.toFixed(2).replace('.', ','); }
// no card:
{ sku:'ob-comandos', price:brl(PRECOS_AREA['ob-comandos']), /* … */ }
```

Gate: **zero** ocorrência de `price:'R$` no painel. Tudo passa por `PRECOS_AREA`.
`grep -n "price:'R\$" index.html` tem que voltar vazio.

## Camada de monetização dentro da área de membros (dona, 16/10/2026)

A área de membros é lucro puro (o cliente já pagou, não custa mídia) — vender de novo
ali é obrigatório. Mas **não basta um banner no topo**: espalhe as peças do funil em
vários pontos e formatos, sempre **fecháveis, responsivos e rotativos**. Nada de parede
de popup.

**5 pontos de contato** (do menos pro mais intrusivo):

| # | Mecanismo | Onde aparece | Como |
|---|---|---|---|
| 1 | Banner superior | topo do hub | imagem clicável (3:1 desktop · retrato mobile) |
| 2 | **Barra fixa inferior (sticky)** | hub **E leitor** | 1 linha: ícone · oferta · preço · CTA · X |
| 3 | Bolha flutuante | canto inf. direito | bolha → mini-card da oferta do dia |
| 4 | Popup de entrada/tempo | sobre o hub | 1× ao dia ou no clique de um módulo |
| 5 | Card de oferta no fim do módulo | fim do leitor | card inline "próxima dor" |

**Regra de ouro:** mecanismo que mora **fora das views** (barra, bolha) aparece em **TODA
tela — hub E leitor**. O leitor é onde o cliente passa mais tempo e onde hoje a venda some.

**Motor config-driven — uma tabela manda em tudo.** Nunca espalhar oferta/card no HTML:

```js
const OFERTAS_BARRA = [
  { id:'cigano', ctx:['tarot'], peso:3,            // só aparece no contexto Tarot
    titulo:'Mapa do Baralho Cigano', sub:'O segundo oráculo, do mesmo jeito',
    url:()=>CIGANO_OFERTAS.entrada.url, valor:()=>CIGANO_OFERTAS.entrada.price,
    need:(owned)=>!ciganoAny(owned) },             // só pra quem AINDA não tem
  // … cada peça do funil com seu ctx / peso / need
];
```

- Só entra o que o cliente **ainda não tem** (`need(owned)`) — ownership por SKU.
- **Contexto** decide a peça (no leitor do Tarot → Cigano/Mapa Astral; no Cigano → cross Tarot).
- **Preço = fonte única** (a mesma `PRECOS_AREA`/tabela de cima); zero preço literal no HTML.

**Rotação, fechar e memória** (é o que faz não parecer empurro):
- Rodízio por **peso + contexto**; mesma oferta não repete por **24h** (`localStorage`,
  ex.: `mdt_bar_seen`); popup no máximo **1× por dia**.
- **X** fecha e marca visto; nunca abrir 2 mecanismos com a **mesma** peça ao mesmo tempo.
- Preço **de área de membros** sempre (tabela da casa) — nunca o de checkout.

**Responsivo (PC × celular):**
- Celular: barra fina (~56px, 1 linha), `env(safe-area-inset-bottom)`, popup full-width.
- Desktop (≥820px): barra **centralizada** `min(680px)` (não full) **ou** bolha no canto.
- Reservar o espaço da barra no body (`body.has-offer-bar{padding-bottom}`) pra não cobrir
  o botão de PDF no fim do leitor.
- Gate: `document.documentElement.scrollWidth > innerWidth` = `false` em 390px.

**Rastreio:** todo botão de checkout leva `data-tk-value`/`data-tk-currency` (o Trackeador
emite o IC; **não** mandar `fbq('track','InitiateCheckout')` à mão = duplica).

**Implementação de referência:** `site/painel/index.html` do Mapa do Tarot (2026-10-16) —
`OFERTAS_BARRA` + `barCtx/barElegiveis/barPick/renderOfferBar`, com a chamada no `show()`
(cobre hub, leitor e Cigano; esconde no login). ⚠️ Ao adicionar código, **não encostar na
região que o servidor avalia no `vm`** (no Tarot, o array `const MODULES` — o `modulo-pdf.mjs`
faz regex + `vm.runInNewContext`; helper/DOM ali derruba **todos** os PDFs com 500). Pôr o
motor **depois** dessa região.

**Gate antes de "pronto":** deploy + gate de eventos (`adstrackeador verificar-site`) + gate
de PDF (`check-download-pdf.mjs`) + mobile 390px + print na conta de teste. Peça nova só entra
na camada com **checkout real** (nunca WhatsApp nem esconder preço).

## "Como libera pro cliente" — o fluxo de acesso

1. Cliente compra o produto principal → pagamento aprovado → sistema já deve ter (ou você cria) um usuário/sessão vinculado ao lead/pedido (login por email+senha, magic link, o que o projeto já usa).
2. Login manda pra rota do hub (`/panel` ou equivalente), NUNCA direto pro conteúdo — o hub é a tela de entrada.
3. Servidor calcula `skusComprados` (união de SKUs de todas as ordens aprovadas daquele usuário) e passa pro componente do hub — nunca decida bloqueado/desbloqueado só no client, o servidor tem que gatear o CONTEÚDO de cada módulo também (alguém pode adivinhar a URL de um módulo que não comprou).
4. Cada card desbloqueado linka pra sua própria rota de conteúdo, que reconfirma ownership no servidor antes de renderizar (dupla checagem: hub decide o que MOSTRAR, a rota de conteúdo decide o que ENTREGAR — nunca confie só na primeira).

## SEMPRE verificar (fluxo de acesso pós-compra) — checklist obrigatório

**Verificar SEMPRE, em toda oferta, seja qual for o checkout/gateway (Wiven, GG Checkout, Hotmart, qualquer um — Wiven é só exemplo), antes de declarar a área de membros pronta:**

- **Webhook/retorno de compra do gateway ligado e puxando email da compra.** Ex. Wiven: evento "Transação paga" → `client.email` + `transaction.status === "COMPLETED"`; outro gateway = evento equivalente dele. Testar: pessoa compra de verdade, tenta logar com o email da compra → tem que ENTRAR. Se o webhook não estiver wireado num endpoint que libera o email, isso falha mesmo com produto certo e página certa.
- **O que libera = exatamente o que a pessoa comprou.** Ownership tem que vir de SKU das ordens aprovadas (união de todas as ordens do lead), nunca de lista fixa/hardcoded ou de um único SKU-padrão pra todo mundo.
- **Clicar pra comprar item bloqueado abre checkout SÓ daquele item.** Order bump bloqueado → checkout só do bump. Nível completo bloqueado → checkout só do completo. NUNCA manda pro checkout/`#planos` do produto inteiro de novo — isso reabre a oferta principal pra quem já é cliente, confunde e pode recobrar o núcleo.
- **Comprar add-on não re-entrega o produto principal nem dispara Purchase com valor cheio.** Ver seção de risco de fulfillment acima — mesma causa raiz, mesmo guard (`orderSkus(order).includes(SKU_DO_NUCLEO)`).
- **Conteúdo do módulo: sem download por imagem individual.** Nem botão "baixar esta página" nem link de imagem solto embaixo de cada página — só os botões "Baixar PDF" (topo e fim do leitor) entregam o módulo inteiro.
- **Aviso "Material em atualização" presente** no hub e no topo de cada produto (ver seção própria).
- **Performance conferida** (ver seção Performance): `.webp` gerado, servidor negocia, leitor lazy, ETag/304.
- **Cache conferido:** `curl -sI` numa página, numa capa e no HTML do painel → `cache-control` com `no-cache`, nunca `max-age` longo/`immutable`.
- **PDF do módulo validado com `pdfinfo`.** Baixar logado → HTTP 200, `pdfinfo` mostrando Pages = número de imagens do módulo. Deslogado/sem SKU → HTTP 403 ou redirect pra login.

**Itens que furaram no Cigano (05/10/2026). Conferir também:**
- **Todo offerCode libera.** Produto com vários planos (Básico, Completo, popup Básico, popup Completo, oferta de membro) = mapear CADA offerCode no servidor. Antes de dar por pronto, liste as ofertas do produto no gateway e confira uma a uma no código. Um offerCode esquecido = cliente pagou e não entra.
- **Tier = SKU próprio.** Básico e Completo nunca dividem o mesmo SKU (senão o Básico ganha os bônus). Bump libera só o próprio módulo, Combo libera os itens dele, e nenhum dos dois libera o pacote.
- **Prova por webhook simulado em prod**, um POST por offerCode e por bump, com o token lido da env do app no Coolify (variável, nunca impressa) e e-mails de teste distintos. Depois, print logado de cada conta (Básico, Completo, Básico+bump).
- **Painel que serve 2 produtos** (ex.: Cigano dentro do painel do Tarot): o card "SEU PRODUTO · Acessar" só aparece para o que a pessoa comprou. O outro produto aparece como oferta de membro, com cadeado e preço. Cabeçalho, título e paleta seguem o produto que a pessoa tem (quem tem só o Cigano não vê "Mapa do Tarot" roxo). O produto que a pessoa tem vem primeiro.
- **E-mail de acesso por produto:** texto, cor e lista de itens do produto comprado. Nunca "Acessar meu Mapa do Tarot" para quem comprou o Cigano.
- **`/painel` no domínio da página de vendas** redireciona (302) para o painel real. Fallback do nginx que devolve a página de vendas em `/painel` é bug.
- **Bônus prometido existe e abre.** App ou módulo prometido na página tem que abrir com a conta do plano certo. Card com `href="#"` ou pasta vazia = não pronto (o App de Treino do Cigano foi vendido sem existir).
- **Ofertas de membro nascem junto** (seção Ofertas de membro). Cada card bloqueado tem link do checkout DELE, preço de membro com o normal riscado e `data-tk-value` igual ao preço da oferta. Ordem: upgrade de tier → combo → bumps do mais caro pro mais barato → produto irmão.
- **Aviso com prazo** ("será liberado AINDA HOJE") só enquanto for verdade. Ao completar o conteúdo, tirar o aviso e registrar no STATUS.

Sem os 6, a área de membros parece pronta (visual ok, roteamento ok) mas não gateia comprador de verdade — só passa no teste manual com email de mentira.

## Adaptando para outro projeto

- Troque a paleta/tokens de cor pelos do projeto (ler o design system existente antes, nunca copiar cores do exemplo de referência).
- Troque `formatMoney`/`product`/`Sku` pelos equivalentes do catálogo de preços do projeto novo.
- Mantenha a separação: hub (grid) É SEPARADO das páginas de conteúdo de cada módulo — não vire tudo um componente gigante.
- Se o projeto não tem sistema de sessão/ownership ainda, isso é pré-requisito, não parte opcional do hub.

## Ficha de instrução plana (ícone abstrato) — NÃO traduzir/copiar, refazer ilustrada (regra da dona, 22/10/2026)
Ficha de instrução cuja arte é ícone abstrato (arco-íris, círculos, pontos, folha) em caixa vazia + bloco de NOTAS não se traduz nem se copia (nem por Pillow, nem no GPT). Refazer a FICHA INTEIRA no GPT como imagem ilustrativa real, com uma ficha nossa aprovada como referência e o prompt explicando o exercício + texto exato do módulo. Nunca card de código com foto colada. Regra completa: `low-ticket/references/PAGINAS-DE-ATIVIDADE.md` › "Ficha de instrução SEMPRE com imagem ilustrativa".
