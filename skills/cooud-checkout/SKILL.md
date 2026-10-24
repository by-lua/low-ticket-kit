---
name: cooud-checkout
description: Cadastra e configura oferta na Cooud (dashboard.cooud.com) pelo painel logado - loja, produto, preço/oferta, entrega pós-compra (Thanks Page do funil), temporizador/contagem, imagem do produto, banner, idioma e webhook pós-venda. Use quando o usuário pedir criar produto na Cooud, checkout Cooud, checkout.cooud.com, dashboard.cooud.com, entrega pós-compra Cooud, countdown/temporizador no checkout Cooud, banner/imagem de produto Cooud, ou pegar link/URL de checkout Cooud.
allowed-tools: Bash(agent-browser:*), Bash(chromium:*), Bash(curl:*)
---

# cooud-checkout

Mecânica pra montar e configurar oferta na **Cooud** no nosso ambiente. Complementa
[[browser-cloudflare]]. Herdada da montagem real da **GeriNeuro US** (16/10/2026) — abaixo,
o que foi **aprendido na prática** (seletores, API, bug e bloqueio reais), não teoria.

> **REGRA FIXA DA DONA (vale pra todo gateway):** área de membros é SEMPRE a NOSSA, externa,
> `https://<site>/painel`. A entrega nativa da Cooud (**Cooud TV**) é plataforma de VÍDEO e
> **não serve pra PDF**. Sempre configurar o pós-compra pra cair no nosso `/painel` (ver
> "Entrega pós-compra") + liberação por webhook no nosso servidor.

> **DE ONDE VÊM AS PEÇAS:** o que vai em bump/upsell/downsell é decidido ANTES na mecânica
> `mvt-funil` (regras em `criacao-low-ticket-mvt/references/PECAS-DO-FUNIL.md`); aqui só se
> monta o que já está no `FUNIL.md` da oferta, com preço na tabela da dona.

> **REGRA FIXA DA DONA (16/10/2026) — TODO produto/oferta criado entra nos DOIS webhooks NO MESMO DIA.** Vale pra toda peça: principal · **order bump** · combo · upsell/downsell · **upgrade Essencial → Completo** · produto irmão/cross · oferta de membro. Cada produto novo, na MESMA sessão do cadastro, marcado em (1) **webhook de ENTREGA** (`<site>/painel/api/webhooks/cooud`) e (2) **webhook de MEDIÇÃO** (Trackeador, `https://adstrackeador.leadgo.dev/api/webhooks/sale/c/<conexão>`) — "todos os produtos" OFF. Produto fora do webhook = a venda some do Trackeador/atribuição e/ou o comprador fica sem acesso, **sem erro em lugar nenhum**. Padrão/incidente (order bump "Combo Domínio Total", Jiu-Jitsu, 16/10): `wiven-checkout` §6.

## Acesso

**Conta em uso = Dona/EmpresaB** (dona 16/10 — a do Sócio está **com problema**):
perfil do sistema **`cooud-dona-empresab`**, porta **9276**, conta **`voce@exemplo.com`**.
Sessão agent-browser = `--session cooud-dona-empresab`. Subir se estiver parado:
`~/.claude/bin/browsers.sh cooud-dona-empresab`. Antes de agir: `curl -s localhost:9276/json` (aba em `dashboard.cooud.com`).

- **Login é por CÓDIGO de uso único (não tem senha):** em `auth.cooud.com` digitar o e-mail →
  **Continuar** → a Cooud manda um código de **6 caracteres** por e-mail (vale **5 min**) → pegar no
  **webmail EmpresaB** (perfil **`hostinger-mail-empresab`**, porta 9295, `mail.hostinger.com`) → colar no
  campo "Código de acesso" → Confirmar. Marcar **"Manter conectado"** (90 dias).
- Perfil antigo **`cooud`** (porta 9269) = conta Sócio `voce@exemplo.com` — **aposentado
  para item novo** (usar só para consultar o que já existe lá).

Um perfil por pane (não dividir a sessão); nunca `agent-browser open` nu — anexar no perfil.

Taxa Cooud: **6,99%/transação + fixa, sem mensalidade**.

## Estrutura (loja → produto → oferta)

- **Loja** (`store`): gateway(s) de pagamento em **Configurações → Pagamentos** (ex.: `Stripe: Conectar`,
  `Cooud LLC: Conectar`).
- **Produto** = `course` (tem `slug`). **Oferta/preço** = `price` (id; `amount` em **centavos**,
  `currency` usd/brl/eur; ex.: `1990` = US$19,90).
- Link público do checkout: **`https://checkout.cooud.com/<offerId>`**.

## Criar LOJA e PRODUTO do zero (UI) — GeriNeuro US na conta Dona, 16/10/2026

Conta nova = começar pela loja + produto. Tudo pela UI; sem certeza de que exista rota direta
(`/store/new`, `/store/create` etc. **não** são páginas de criação — caem num shell de loja vazia).

**Criar a loja:**
1. Sidebar → **`Minhas lojas`** → botão **`Criar nova loja`** (abre o diálogo **Cronus · Vision**).
2. No diálogo há dois caminhos: IA (**`O que vamos criar?`** + **`Continuar com Cronus`**) ou o botão
   de baixo **`Configurar manualmente`** (`Loja, produto e preço, passo a passo`). Usar o **manual**
   (controle total). Ele abre o wizard **`Criar novo projeto`** (passos **Loja → Produto → Preço**).
3. Passo **Loja**: **`Nome da loja`** (`textbox`), **`E-mail de contato`** (`textbox`), grupo
   **`Como você vai receber`** — **`Cooud (Brasil)`** = **nativo/default (aria-pressed=true)**,
   `Cooud LLC (EUA e Europa)` = externo. **`Moeda`** (`combobox`, pode já vir **USD** p/ conta US).
   **`Tipo de produto`**: **`Digital`** / **`Físico`** (Digital já vem `aria-pressed=true`).
4. **`Próximo`** cria a loja → toast **`Loja criada com sucesso!`**.
   ⚠️ **ARMADILHA (bug real):** **cada clique em `Próximo` cria uma loja NOVA** — cliquei 2× e
   nasceram **duas lojas "GeriNeuro"**. **Não há como excluir loja** (`DELETE orbit.cooud.com/stores/<id>`
   → **404** `route not found`; a UI não tem excluir/arquivar em Configurações → `Geral`).
   → **Dar UM clique só** e conferir o toast antes de qualquer outro clique.
5. `storeId` fica na URL `dashboard.cooud.com/store/<storeId>` (aparece nos links do dropdown
   `Minhas lojas`) e no `course.store_id` do GET de qualquer oferta.

**Criar o produto:**
1. Dentro da loja → **`Produtos`** → **`Novo produto`** (ou "Criar primeiro produto").
2. Slide-over **`Novo Produto`**: **`Nome`** (`textbox`), `Imagem do produto` (opcional),
   **`Categoria`** (`combobox` custom — opções: Programação, Design, Marketing, Finanças,
   Empreendedorismo, Música, Escrita, Vídeo, Desenvolvimento Pessoal, Idiomas, **Bem-estar** =
   `domain:"well_being"`), **`Descrição`** (`textbox`) → **`Novo produto`**.
3. O produto criado tem **`slug` = `<nome-slugificado>-<rand>`** (ex.
   `gerineuro-complete-collection-mvbfkxix`); URL de edição = `/store/<storeId>/products/<slug>`.
   A aba **`Ofertas`** nasce vazia ("Nenhuma oferta ainda") → criar preços lá (seção abaixo).

**🐛 Três armadilhas de UI que custam tempo (todas reais nesta rodada):**
1. **Slide-over abre FORA da tela** — o painel (`[role=dialog]`) às vezes fica com
   `getBoundingClientRect().x === innerWidth` (transform de entrada não roda); aí **clique real não
   acerta o botão** (Salvar/Próximo/Nova oferta) e nada salva. **Fix:** via eval, forçar
   `dialog.style.setProperty('transform','none','important')` (e nos 3-4 ancestrais) → o painel volta
   pra `x ≈ innerWidth - 560` e os cliques passam. Alternativa: esperar ~2-3 s a animação.
2. **React controlled inputs** — **`fill` e `eval .click()` NÃO persistem o estado**: o
   `Novo produto`/`Nova oferta` continua `disabled` e a **prévia mostra `$ 0,00`**. Usar **`type`**
   (keystrokes reais) para Nome/Descrição/**Valor**; para o **Valor** (`spinbutton`), **clicar dentro
   do campo com o mouse e digitar** (ex.: `12.90`) até a prévia virar `$ 12,90`; para a **Categoria**,
   abrir o combobox e **clicar a `[role=option]` com click real** (eval `.click()` não troca o estado).
   O estado do form **reseta** quando outro campo ganha foco → preencher e **submeter na sequência**,
   sem re-render no meio.
3. **Splash `Você sempre no topo`** trava o SPA em navegação direta (inclusive no próprio
   `dashboard.cooud.com/`) — não é erro de console; **`reload` resolve**. Repetir no fluxo.

**Confirmar o gateway (padrão):** `.../settings/gateway` → linha **`Cooud`** com badge **`Ativo`**
(*"Processamento, custódia e repasses pela Cooud"*) é o **nativo = PADRÃO NOSSO** (já vem Ativo; nada
a conectar). `Stripe` e `Cooud LLC` ficam como **`Conectar`**.

## Criar nova oferta (preço) e mudar o preço da oferta (GeriNeuro, 16/10/2026)

Produto pode ter **VÁRIAS ofertas** (preços) no mesmo curso — é assim que nasce a **oferta de
saída** (popup de saída da página) sem criar produto novo. Ambas ficam na aba **Ofertas**.

**Mudar o preço de uma oferta (UI):**
1. **Produtos → abrir o produto → aba `Ofertas`.**
2. No card da oferta: botão **`Editar oferta`** → painel **"Editar oferta"** abre à direita.
3. Preencher o **campo `Valor`** (`spinbutton`, mostra o valor atual; ex.: `19.89999…`; **digitar o
   valor absoluto**, ex.: `12.90` — não é delta) → botão **`Salvar`** (fica `disabled` até o valor mudar).
4. Se o valor for baixo, abre o modal **`Confirmar preço baixo`** (`Revisar` / **`Confirmar e salvar`**)
   → clicar **`Confirmar e salvar`**.
5. **Provar com GET na API** (a UI não confirma sozinha): `curl -s
   https://orbit.cooud.com/prices/<offerId>` → conferir `"amount": <centavos>`.

**Criar uma nova oferta (UI):**
1. Mesmo produto → aba **`Ofertas`** → botão **`Nova oferta`**.
2. Painel **"Nova Oferta"**: **`Nome da oferta`** (`textbox`), **`Valor`** (`spinbutton`),
   **`Descrição`** (`textbox`) e o switch **`Cobrança recorrente`** (deixar **OFF** = pagamento único).
3. Botão **`Nova oferta`** (fica `disabled` até ter nome + valor) → modal **`Confirmar preço baixo`**
   (se valor baixo) → **`Confirmar e salvar`**.
4. A oferta nova aparece como **segundo card** na região "Pagamento único". Pegar **id/link** no
   **`Copiar ID da oferta`** ou no **href do link "… Abrir checkout builder"**
   (`/checkout-builder/<storeId>/<slug>/<offerId>`) → checkout público = `https://checkout.cooud.com/<offerId>`.

**API (o que a UI dispara por baixo):**
- **Criar oferta:** `POST https://orbit.cooud.com/courses/<slug>/prices` → **201** (corpo com `name`,
  `amount` em centavos, `currency`, `description`). Devolve o `price` novo.
- **Mudar preço / metadata:** `PATCH https://orbit.cooud.com/prices/<offerId>` — **`amount` aceita
  partial** (`{"amount":1290}`) e **`metadata` também** (merge; ex.: `{"metadata":{"thanks_page_url":"…"}}`).
  ⚠️ Diferente do `/courses/<slug>`, que é **replace total**.
- **Auth:** **`GET` é público** (sem cookie). **`PATCH`/`POST` exigem sessão** → fora do dashboard dá
  **`401 {"message":"Requires authentication"}`**. Para PATCH autenticado sem browser dedicado, rodar
  **de dentro do dashboard** com `fetch(..., {credentials:"include"})` (o CORS libera origem
  `dashboard.cooud.com`). Receita (agent-browser eval):
  ```js
  await fetch("https://orbit.cooud.com/prices/<offerId>", {
    method:"PATCH", headers:{"Content-Type":"application/json"}, credentials:"include",
    body: JSON.stringify({ metadata:{ thanks_page_url:"https://<site>/painel/" } })
  }); // → 200
  ```
- **Replicar no/para nova oferta:** repetir o que o principal tem — **Thanks Page**
  (`metadata.thanks_page_url`), mesmo `currency`/`payment_model: one_time` (o padrão já é único). Idioma
  é **auto pelo comprador** (nada a setar). Countdown é **por oferta** — só criar se for o caso
  (`metadata.countdown_deal.enabled`), a oferta de saída **não leva**.
- **Prova real no ar (não "deve estar"):** abrir `https://checkout.cooud.com/<offerId>` no browser e ler
  o preço renderizado (`Subtotal`/`Total`), não só o GET da API.

## Order bump NATIVO (Flow/Funis) — exige PRODUTO separado (17/10/2026)

- A Cooud **TEM order bump nativo**: checkout builder → **Flow (Funis)** → **`Adicionar Order Bump`** → diálogo
  *"Adicione um produto complementar à compra"* com **Produto + Preço** (o cliente inclui **antes** de finalizar).
  Funil: **principal → order bump (cobrado junto no checkout, vale cartão E boleto) → upsell (1 clique, só cartão)
  → downsell → Thanks Page**.
- ⚠️ **O campo `Produto` só lista OUTROS produtos** — **um produto NÃO é bump de si mesmo**. Com **1 produto** na
  loja, o seletor vem **desabilitado**. **Ofertas/preços do MESMO produto NÃO viram order bump nativo** (são
  checkouts válidos por link, mas não aparecem como checkbox no checkout).
- **Regra:** pra order bump **nativo**, cada peça é um **PRODUTO separado** (com o preço dela) → depois ligar no Flow.
- **Produto não é excluível** na Cooud (UI e `DELETE` → 404): **conferir antes de criar** pra não deixar duplicado.
- **O webhook não muda:** o webhook da Cooud é por **LOJA + evento** (`order.paid`), **sem filtro de produto**
  (`GET orbit.cooud.com/stores/<id>/event_destinations`) → ofertas/produtos novos são **cobertos automaticamente**.
  O que muda é só o **mapeamento `offerId→SKU` no nosso servidor** (`PRODUCT_SKUS`): oferta nova **fora do mapa =
  venda sem acesso**. Reaplicar e redeployar a cada peça nova.

## Gateway de pagamento (Configurações da loja → Pagamentos)

URL: `dashboard.cooud.com/store/<storeId>/settings/gateway`. Três opções — **"Você pode escolher o
provedor até a primeira venda paga"**:

| Provedor | Estado padrão | Regra |
|---|---|---|
| **Cooud** (nativo) | **Ativo** (default) | **PADRÃO NOSSO** (dona 16/10) — processamento, custódia e repasses pela Cooud; não conectar outro sem ela pedir |
| **Stripe** | botão **Conectar** | recebe direto na sua conta Stripe; a Cooud não custodia nem repassa |
| **Cooud LLC** | botão **Conectar** | venda em dólar, recebe em banco no exterior — **exige pessoa/empresa + banco nos EUA, Reino Unido, Europa, Canadá ou Suíça; banco brasileiro NÃO recebe da Cooud LLC** |

- **Cooud (nativo) já chega Ativo** e **É O PADRÃO NOSSO** (dona 16/10): na GeriNeuro não foi preciso
  conectar nada (correção de 16/10: antes se supôs "loja sem gateway"; era falso). Só conectar
  **Stripe** ou **Cooud LLC** se a dona pedir explicitamente.
- Cooud LLC só habilita com: moeda USD, **sem** coprodutores, **sem** afiliados, **sem** assinatura,
  nenhuma venda paga + **abrir a conta Cooud LLC**. ⚠️ Esse checklist (`Pronto/Falta → Abrir conta Cooud
  LLC`) é **exclusivo da LLC** — **não vale pro Cooud nativo** (que já está Ativo e é o nosso padrão).
- Alerta *"Adquirente e bandeiras estão solicitando informações adicionais. Envie até … para continuar
  vendendo"* → **KYC pendente** (botão **"Enviar agora"**); sem resolver, o processamento de cartão
  pode travar.


## Publicar produto

- O badge **"Não publicado"** é **só tooltip** (`button.products-studio-module__kXSuTa__status`,
  `data-slot="tooltip-trigger"`) — **não é botão, não dispara API**. Hover diz literalmente:
  *"Este produto está ativo e o checkout funciona normalmente. Ele apenas não está publicado na
  Cooud TV."* → ou seja, **o produto está ativo**; "não publicado" = só relativo à **Cooud TV**.
- Backend: `course.live=false` (`GET orbit.cooud.com/courses/<slug>`).
  `PATCH /courses/<slug> {live:true}` → **200 mas NÃO flipa** (segue `live=false`).
- **Gateway:** a loja já vem com **Cooud (nativo) = Ativo** — o checkout já processa por ele. O que
  costuma aparecer no topo é o KYC da adquirente: *"Adquirente e bandeiras estão solicitando
  informações adicionais… Enviar agora"* → resolver (ver "Gateway de pagamento"). Nada disso muda o
  `live=false` do produto (que é só o tooltip da Cooud TV — o produto está ativo).
- ⚠️ **`PATCH /courses/<slug>` é REPLACE TOTAL.** Payload parcial **zera `description`/`thumbnail_url`
  e troca `domain`** (ex.: virou `programming`). Sempre **GET antes**, editar e mandar o **objeto
  inteiro**; se quebrar, **restaurar do GET** (foi o que salvou a GeriNeuro). Conferir por GET depois.

## Entrega pós-compra (o cliente recebe)

- Modal **"Como o cliente recebe"** (aba Detalhes do produto): **Cooud TV** (nativo, **Ativo** por
  padrão — só vídeo) ou **MemberKit / Astron Members / HuskyApp** (`Conectar`). **NÃO há upload/redirect
  de URL nativo de entrega** — o redirect por URL é na Thanks Page (abaixo).
- **Redirect pós-compra = Thanks Page do FUNIL** (caminho real, testado):
  checkout builder → aba **Flow (Funis)** → botão **"Adicionar" → "Adicionar Thanks Page"** →
  modal *"Redirecione o cliente para uma página de agradecimento"* → campo
  **"URL da Thanks Page"** (`textbox[placeholder="https://..."]`, **obrigatório**) →
  gravar `https://<site>/painel/`.
  - Persistido em **`metadata.thanks_page_url`** (PATCH `orbit.cooud.com/prices/<offerId>`; toast
    *"Configurações do checkout salvas!"*). `flow_enabled` pode seguir `false` — `thanks_page_url`
    é campo de topo (URL de sucesso).
  - **Só funciona depois do deploy do `site/`** (nossa área de membros no ar).
- **E-mail de compra → "Link do email de compra"** (aba Detalhes → *Entrega e acesso* → seção **E-mail de compra**,
  `<details>/<summary>`: clicar o summary p/ expandir): campo `input[type=text]` com placeholder
  **`https://members.example.com/access`**, legenda *"Usado no botão principal do email de compra. Vazio usa Cooud TV."*
  → **preencher com `https://<site>/painel/`** (é `type` com keystrokes reais — React) → botão **"Salvar alterações"**.
  - É um **segundo campo de URL** (além da Thanks Page): o botão do **e-mail de compra** da Cooud. Vazio = o e-mail manda pra **Cooud TV** (errado pra PDF). O switch **"Email padrão da Cooud"** (AppSell/MemberKit/Astron Members) fica **OFF**.
  - **Endpoint real:** `PATCH orbit.cooud.com/courses/<slug>/purchase-email-link` com body
    **`{"access_url":"https://<site>/painel/"}`** (autenticado, `credentials:"include"`). Grava em
    **`course.metadata.cooud_purchase_email_access_url`** (é **por PRODUTO/curso**, vale pras duas ofertas; **GET é público** pelo `/prices/<offerId>`).

## Temporizador / contagem (urgência)

- Caminho: checkout builder → **Elementos → Urgência → Contagem regressiva** — 12 variações
  (Padrão / Lightning / Banner / Strip / Ring / Drama / Soft Tone / Anchor Top / Apple Sheet /
  Glass Capsule / Industrial Block / Mercury Compact) → escolher → **"Selecionar como padrão"**
  (entra em "Meus elementos").
- ⚠️ **BUG/limitação: o "Salvar" do builder NÃO persiste o elemento** (nenhum PATCH;
  `element_variants`/`custom_elements`/`elements_order` seguem vazios).
  **GRAVAR DIRETO NA API:** `metadata.countdown_deal.enabled=true` (+ `minutes`, ex.: `10`;
  `text` opcional). O preview do builder passa a mostrar **"Oferta expira em 10:00"**.
- Existem também elementos **"Banner"** (discount) e **"Timer"** (`timer`) separados.

## Imagem do produto / banner do checkout

- **Foto do produto no checkout:** **Produtos → Editar produto → aba Detalhes** → botão
  **"Adicionar imagem"** (produto sem thumb — `Arraste ou clique · Máx 5MB`) ou **"Trocar"**
  (quando já tem) → **grava `course.thumbnail_url`**.
- **Receita exata de subir a imagem (testada 16/10/2026, GeriNeuro):**
  1. O bloco tem um **`input[type=file]` escondido** (`class="hidden"`, `aria-label="Upload de imagem"`,
     `accept="image/png,image/jpeg,image/webp,image/gif,image/avif"`). Subir pelo seletor
     **`input[type=file]`**: `agent-browser --session <s> upload "input[type=file]" <arquivo.webp>` —
     não precisa clicar antes; o input aceita **webp** (o mockup 1000×563 subiu nice).
  2. Ao escolher o arquivo o app faz sozinho, nessa ordem: **`POST orbit.cooud.com/files`**
     (cria o registro → devolve o id `01M5…`) → **`PUT`** no R2
     (`avatars.a37aaa2bd777ccd1d7f87694cda016db.r2.cloudflarestorage.com/<id>`) →
     **`GET avatars.cooud.com/<id>`**. Ou seja: **a URL final do thumbnail é
     `https://avatars.cooud.com/<id>`**.
  3. O botão vira **"Trocar"** + **"Remover imagem"** (imagem só *staged*). Ainda **não** está no produto:
     clicar **"Salvar"** (rodapé) → dispara **`PATCH orbit.cooud.com/courses/<slug>`**.
  4. ⚠️ **`PATCH /courses/<slug>` é REPLACE TOTAL** — o body do Salvar manda o objeto inteiro
     (`{name, description, thumbnail_url, domain}`). Se algum campo estiver vazio no form, ele **zera**.
     Por isso: **conferir por GET** e, se tiver zerado `description`/`domain`, **restaurar com o objeto completo**.
  5. **Prova:** `curl -s orbit.cooud.com/prices/<offerId> | jq '.course.thumbnail_url'` (GET é público) +
     `curl -o /dev/null -w '%{http_code}' https://avatars.cooud.com/<id>` → **200 image/webp**.
- **"Imagem embaçada" no checkout = quase sempre display, não upload:** a thumb do produto renderiza
  pequena (~70px) no resumo do pedido; print com zoom borra qualquer imagem nítida. **Antes de reupar,
  provar com a fonte real:** `GET orbit.cooud.com/prices/<offerId>` → `course.thumbnail_url` →
  baixar (`curl`) e checar `identify` (resolução/peso). Se a fonte bate com o arquivo local
  (`checkout/banners/...`) e tá nítida, **não é bug de upload** — fecha sem reupar. (GeriNeuro combo,
  24/10/2026: fonte 1080×1080 253KB, idêntica à local — blur era só o zoom do print.)
- **Banner do checkout:** campos de metadata **`banner_url`** e **`checkout_bg_image`**. O upload
  NÃO apareceu no bloco Visual (só Explorar temas / Personalizar / Mais opções / Textos).
  Para subir imagem do produto, usar o `input[type=file]` acima.
- Arte do banner: seguir a skill **`banner-checkout-gpt`** (desktop 16:9 + mobile + imagem do produto;
  texto queimado na imagem). Nunca mockup do concorrente — só identidade nossa.

## Idioma do checkout

- Idiomas nativos: **pt / es / en, automático pelo comprador** — **NÃO existe seletor de idioma**
  na loja/oferta. `?lang=` e `Accept-Language` **não** mudam. IP BR → `pt`. Validar `en` com **IP US**.
- ⚠️ O checkout pode servir **skeleton** (`animate-smooth-pulse`, sem
  `window.__COOUD_CHECKOUT_ORBIT_BASE_URL__` injetado → nenhuma request de dados) quando falta
  bootstrap/gateway — **não confundir com "quebrado"**; recarregar/investigar o bootstrap.

## Skins do checkout (tema)

builder → painel **Visual** → **"Tema atual"** → **Explorar temas** → escolher tema + layout → **"Aplicar tema"** → **"Salvar"** (topo).

- Temas: **Glass** (layouts **Uma tela** / **Tela ampla** / **Split**) · Base (3 layouts) · Noir · Soft · Linear · Editorial.
- **Skin PADRÃO NOSSO = `Glass · Split`** (dona 16/10/2026): layout em 2 colunas — bloco escuro à esquerda (produto + valor) + formulário branco à direita. Aplicar em **todas** as ofertas da oferta (principal **e** saída).
- **Chave na metadata:** `checkout_theme_v2 = { "id": "mono-split", "mode": "light" }`.
  - `id` = **`mono-split`** para **Glass Split**; `mode` = `light` (o diálogo Personalizar tem Claro/Escuro).
- **Fluxo real na UI (16/10):** `Explorar temas` abre `[role=dialog]` *"Escolha um tema"*; os layouts são
  `button.theme-layouts-module__qS4FyW__layoutChoice` (`aria-pressed` marca o selecionado — Split = **3º**, use
  `agent-browser find nth 2 ".theme-layouts-module__qS4FyW__layoutChoice" click`); o rodapé
  `.theme-studio-module__oTDQJa__dialogFooter` tem **Cancelar/Aplicar tema**; toca **"Salvar"** no editor.
  ⚠️ O diálogo fecha sozinho às vezes — reabrir e conferir o `h3` do painel (**"Glass Split"**).
- **✅ O "Salvar" do builder PERSISTE o tema** (diferente do countdown!): dispara
  **`PATCH orbit.cooud.com/prices/<offerId>`** com o `metadata` inteiro (inclui `checkout_theme_v2`).
  Se a UI não persistir, gravar direto:
  `fetch("https://orbit.cooud.com/prices/<offerId>",{method:"PATCH",credentials:"include",headers:{"Content-Type":"application/json"},body:JSON.stringify({metadata:{checkout_theme_v2:{id:"mono-split",mode:"light"}}})})`
  (PATCH de `metadata` é **merge**).
- **Prova:** `GET orbit.cooud.com/prices/<offerId>` → `metadata.checkout_theme_v2.id == "mono-split"` + o painel Visual lê **"Glass Split"**.

### Preço na moeda do cliente (Configurações do checkout)

builder → painel **Pagamento** → seção **"Campos"** → grupo **"MOEDA E PAGAMENTO"** (não fica no bloco Visual!).

- **`Exibir na moeda do cliente`** = **`local_currency_display`** — *"Mostra uma estimativa do preço na moeda do visitante."* → **LIGAR (`true`)** em todas as ofertas. **REGRA DA CASA** (preço em moeda local): o checkout mostra o preço **estimado na moeda do visitante**, mas o **cadastro/pixel segue na moeda da oferta** (US$).
- **`Cobrar na moeda do cliente`** = **`local_currency_charge`** — *"O cliente será cobrado na moeda local dele. Melhora a taxa de aprovação."*
- **`local_currency`** = flag mestre (default `true` no Salvar do builder). As 3 ficam `true` no padrão (GeriNeuro 16/10).
- Gravar/confirmar por API (PATCH de `metadata` é merge):
  `{metadata:{local_currency:true,local_currency_charge:true,local_currency_display:true}}` → **GET** de prova.
  O switch na UI reflete (`[role=switch][aria-checked="true"]`).

## API privada (Orbit)

- `orbit.cooud.com/prices/<offerId>` — **GET/PATCH** metadata da oferta (countdown_deal,
  thanks_page_url, banner_url, checkout_bg_image…).
- `orbit.cooud.com/courses/<slug>/prices` — **POST** cria oferta (201); `orbit.cooud.com/courses/<slug>`
  — GET/PATCH (**replace total!**).
- `orbit.cooud.com/stores/<storeId>/connections` — conexões da loja (gateway).
- `orbit.cooud.com/stores/<storeId>` — GET 200; **DELETE → 404** (`route not found`): **não dá pra excluir loja** nem por API.

## Webhooks da Cooud (onde mora, como funciona) — CONFIRMADO 16/10/2026

**Caminho:** dashboard → loja → **Desenvolvedor** (`/store/<storeId>/developer`) → aba **Webhooks**.
(A tela **Integrações** só tem o atalho "APIs e webhooks" que aponta pra lá; o link é
`/store/<storeId>/developer`.) Abas: Chaves de API · Versão da API · Domínios do checkout ·
**Webhooks** · Tokens de acesso.

⚠️ **BUG da Cooud (16/10/2026):** a aba **Webhooks** **não monta o conteúdo** — o
`[role=tabpanel]#developer-panel-webhooks` renderiza o painel de **Chaves de API** (`#native-api-keys`);
o clique troca `aria-selected` e o `id` do painel, mas o HTML do painel continua o de API keys
(sintoma igual nas outras abas). **Contorno: criar/listar/remover webhook pela API** (o MESMO endpoint
que a UI usaria).

**API real (base `https://orbit.cooud.com`; precisa de sessão — `credentials:"include"` de dentro do dashboard):**
- **LISTAR** `GET /stores/<storeId>/event_destinations?limit=100` → `{items:[…],total_count}`.
- **CRIAR** `POST /stores/<storeId>/event_destinations` body **`{url, enabled_events:["order.paid"]}`**
  → **201**; a resposta traz **`webhook_secret` (mostrado UMA vez)** + `signature_enabled:true`.
- **REMOVER** `DELETE /event_destinations/<id>`.

**Aceita MÚLTIPLOS webhooks** (uma `event_destination` por URL; `total_count`>1 é normal) — **não há
limite de 1**, então entrega e medição são **2 registros distintos**.

**Eventos** (`enabled_events`, com ponto): `store.updated` · `order.created` · `order.updated` ·
**`order.paid`** (confirmação de pagamento — libera acesso externo) · `order.refunded` · `subscription.renewed`.

**🔑 NÃO existe campo de token/secret customizado.** O formulário tem **só URL + checkboxes de eventos**.
A Cooud **gera** um `webhook_secret` (mostrado uma vez) e **assina** cada POST com o header
**`X-Cooud-Signature`**. Logo: **não dá pra a Cooud mandar o nosso `COOUD_WEBHOOK_TOKEN`** (sem campo,
sem header custom). Pra autenticar no NOSSO servidor, 2 caminhos: **(a)** token na URL
(`?token=<token>`) + o servidor ler `url.searchParams.get('token')` — padrão das ofertas
`mapa-do-tarot`/`mapa-do-cigano` (a confirmar que a Cooud preserva a query no destino); **(b)** verificar
**`X-Cooud-Signature`** (HMAC do corpo com o `webhook_secret`) — é o que a própria Cooud recomenda
("Use-o no seu servidor para verificar X-Cooud-Signature antes de confiar no webhook").

### Dois webhooks distintos na Cooud (ENTREGA × MEDIÇÃO) — criados 16/10/2026

Ambos em `event_destinations` da loja `<id>`, evento **`order.paid`**:
1. **ENTREGA (nosso):** `https://gerineuro.leadgo.dev/painel/api/webhooks/cooud` · id `<id>` · secret `whsec_<secret>`.
2. **MEDIÇÃO (Trackeador):** `https://adstrackeador.leadgo.dev/api/webhooks/sale/c/<id-conexao>` · id `<id>` · secret `whsec_<secret>`.

**Formato do payload (`order.paid`):** `data.customer_email`, `data.payment.state`/`status`,
`data.order.id` (+ o id da oferta em algum campo do pedido). O parser da nossa área de membros lê
e-mail/status/id **nos dois níveis** (topo e `data.*`) e aceita `token`/`webhook_token` no corpo OU
`Bearer`/`x-webhook-token`. Payload desconhecido é **LOGADO**.

**Gate do produto novo (OBRIGATÓRIO):** o `offerId` da Cooud tem que entrar no mapeamento do webhook
que libera o SKU (no nosso servidor: `PRODUCT_SKUS` / env `COOUD_OFFERS_EXTRA`). **Caso real GeriNeuro
16/10:** as ofertas do Dona (`<id>` e a saída `<id>`)
**não estavam** no mapa → POST autorizado devolveu `no-known-product` (**200, sem liberar**); só a
oferta ANTIGA do Sócio (`<id>`) liberou. **Oferta recriada = re-cadastrar o id no servidor.**

**Assinatura (a Cooud NÃO manda token):** ela assina o corpo no header **`X-Cooud-Signature`**. O nosso
servidor precisa **aceitar a assinatura** — senão a venda real leva **401**. No `site/server/index.mjs`:
aceita **token OU `X-Cooud-Signature`**; se houver `COOUD_SIGNING_SECRET`, verifica o **HMAC** (hex/base64);
sem o secret, aceita a presença da assinatura via env **`COOUD_ACCEPT_SIGNATURE=1`** (⚠️ pendência: achar o
`signing secret` da Cooud p/ verificar de verdade em vez de só aceitar). Provado 16/10: POST **só com
`x-cooud-signature`** (sem token) → **200 `granted`** → login → 9 módulos.

**Persistência (não pode zerar no deploy):** o servidor grava os compradores em `DATA_DIR` (`/data`). No
Coolify, **criar volume persistente** `mount_path=/data`:
`coolify app storage create <app> --type persistent --name <n> --mount-path /data` — sem ele, **todo
redeploy zera os clientes**. Provado 16/10: comprei por webhook, redeployei e o comprador **continuou com acesso**.

## Estado de referência — GeriNeuro US (conta Dona, 16/10/2026) — CANÔNICO

Conjunto recriado do ZERO na conta **Dona/EmpresaB** (`cooud-dona-empresab` 9276), o atual.

- **Loja** `GeriNeuro` (USD, digital) = **`<id>`**
- **Produto** (`course`) `GeriNeuro Complete Collection` = `<id>`,
  slug `gerineuro-complete-collection-mvbfkxix`, `domain: well_being`, `live: false` (só tooltip Cooud TV)
- **Oferta principal** = **`<id>`** (`amount:1290` usd, pagamento único) →
  `https://checkout.cooud.com/<id>`
- **Oferta de saída** = **`<id>`** (`amount:990` usd) →
  `https://checkout.cooud.com/<id>`
- **Thanks Page nas DUAS** = `https://gerineuro.leadgo.dev/painel/` (`metadata.thanks_page_url`)
- **Skin das DUAS** = **`Glass Split`** (`metadata.checkout_theme_v2.id = "mono-split"`, `mode:"light"`)
- **Moeda do cliente nas DUAS** = `metadata.local_currency=true`, `local_currency_charge=true`, `local_currency_display=true`
- **Imagem do produto** (course) = `thumbnail_url = https://avatars.cooud.com/<id>` (nosso `checkout/banners/gerineuro-product.jpg` — 9 capas + 1 ficha; trocada 17/10/2026) · antiga: `<id>` (`hero-mockup.webp`)
- **Link do e-mail de compra** (course) = `metadata.cooud_purchase_email_access_url = https://gerineuro.leadgo.dev/painel/`
- **Countdown** só na principal (`metadata.countdown_deal.enabled=true`, `minutes:10`); saída sem countdown.
- **Gateway** = `Cooud` **Ativo** (nativo).
- ⚠️ **Loja duplicada vazia** `<id>` (clique duplo no `Próximo` do wizard) —
  sem produto; **não excluível**.

```json
{ "amount": 1290, "currency": "usd",
  "checkout_theme_v2": { "id": "mono-split", "mode": "light" },
  "local_currency": true, "local_currency_charge": true, "local_currency_display": true,
  "countdown_deal": { "enabled": true, "minutes": 10, "text": "" },
  "thanks_page_url": "https://gerineuro.leadgo.dev/painel/",
  "live": false, "domain": "well_being" }
```

_(Conta Sócio `cooud` 9269 — aposentada p/ item novo: loja `<id>` ·
principal `<id>` · saída `<id>`.)_

## Armadilhas (resumo)

1. `PATCH /courses/<slug>` = replace total → GET antes; restaurar se quebrar.
2. Badge "Não publicado" **não é botão** — é tooltip de Cooud TV; produto está ativo.
3. **Gateway:** **Cooud (nativo) já vem Ativo** — não confundir "Não publicado" (tooltip da Cooud TV)
   com falta de gateway. O que trava é o **KYC da adquirente** (alerta "Enviar agora"), não um botão de publicar.
4. **Save do builder não persiste** elementos de urgência → gravar `metadata.countdown_deal` na API.
   (⚠️ **Exceção:** o **tema** e as opções de **moeda** **persistem** pelo Salvar do builder — PATCH `/prices`.)
5. Checkout de IP BR vem `pt`; sem seletor de idioma — validar `en` com IP US.
6. Skeleton no `checkout.cooud.com` ≠ quebrado (falta bootstrap/gateway).
7. **Form do produto pode zerar `description`/`thumbnail_url`** (o Salvar é replace total e o form às
   vezes remonta vazio, ex.: depois do splash/reload) — sempre **conferir por GET** e **restaurar** com o
   objeto completo. A **imagem sobe pelo `input[type=file]` escondido** (`upload`), não por clique em botão.
8. **Webhooks:** moram em **Desenvolvedor → aba Webhooks**; a aba está **bugada** (renderiza Chaves de API) →
   usar a API `orbit.cooud.com/stores/<storeId>/event_destinations`. **Aceita vários**; eventos com ponto
   (`order.paid`); **sem campo de token** — Cooud assina com `X-Cooud-Signature` (secret mostrado 1×). Pra
   mandar o NOSSO token, usar `?token=` na URL + servidor ler a query (padrão tarot/cigano) ou verificar a assinatura.
