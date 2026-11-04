---
name: cakto-checkout
description: Cadastra e opera produto/oferta na Cakto (app.cakto.com.br) — gateway nacional (Cakto Pay, BR) e internacional (Cakto Commerce OÜ, Estônia, 190+ países/135 moedas). Tem API REST própria com OAuth2, usada por script, sem precisar de browser pra criar produto/oferta. Use quando o usuário pedir para criar produto/oferta na Cakto, checkout Cakto, vender internacional pela Cakto, ou mencionar Cakto, Cakto Pay, Cakto Commerce, Cakto API, CaktoMCP.
---

# Cakto — checkout nacional + internacional

Pesquisado e testado em 29/10/2026 (conta LeadGo, `contact@seudominio.com`). Fonte: `docs.cakto.com.br`,
`cakto.com.br/cobertura`, `cakto.com.br/pagamentos` — reconfirmar se algo não bater (preço/taxa muda rápido).

## Quando usar

- Oferta nova ou existente que vai vender fora do Brasil (190+ países) sem trocar de gateway.
- Criar produto/oferta/checkout via **API** (preferir isso, não Playwright — ver "Como operar" abaixo).
- Dúvida de taxa, método de pagamento por país, ou cobertura.

## Perfil e credenciais

- Perfil de browser: `cakto` (porta 9298) — só pro login inicial / 2FA / tarefas que a API não cobre.
  `~/.claude/bin/browsers.sh cakto`
- Login: **sem senha por padrão** (magic link) ou **com senha + código de 6 dígitos por e-mail**
  (toggle "Login com senha" na tela). Conta usa 2FA por e-mail sempre — não tem como pular.
  - E-mail de recebimento do código: `contact@seudominio.com`, webmail Hostinger, perfil `hostinger-mail-empresab`
    (credenciais `HOSTINGER_LEADGO_EMAIL`/`HOSTINGER_LEADGO_PASSWORD` em `~/.claude/.credentials.env`).
  - **Código expira rápido** (~60-90s) — entre pegar no e-mail e digitar na Cakto, não demorar.
    Se digitar e der "código inválido", é porque pegou um e-mail de tentativa anterior: clicar
    "Reenviar Código", esperar os ~90s de cooldown, abrir o e-mail **mais recente** de novo.
- Credenciais em `~/.claude/.credentials.env`:
  - `CAKTO_EMAIL` / `CAKTO_PASSWORD` — login do painel.
  - `CAKTO_CLIENT_ID` / `CAKTO_CLIENT_SECRET` — chave de API "low-ticket-skill" (escopos: leitura,
    escrita, produtos, pedidos, ofertas). Criada em Integrações → Cakto API → Criar Chave API.
    **O client_secret só aparece uma vez na tela** — se perdeu, cria chave nova (não tem como recuperar).
  - Atenção ao copiar client_secret da tela/print: fonte confunde `O`/`0` e `l`/`1`/`I` — preferir
    clicar no botão "Copiar" e ler clipboard, ou pegar pelo snapshot de acessibilidade (texto puro),
    nunca transcrever de imagem a olho.

## Como operar: API, não Playwright

A Cakto tem **API REST pública com OAuth2** (`docs.cakto.com.br`) que cobre criar produto, criar
oferta, listar produtos, ver pedidos. **Usar a API pra isso — não abrir browser.** Playwright só serve
pra: login inicial, pegar/criar a chave de API, e o que a API não expõe (configurações visuais do
checkout, Integrações de app, etc.).

### Autenticação (token OAuth2)

```bash
set -a; source ~/.claude/.credentials.env; set +a
curl -s -X POST https://api.cakto.com.br/public_api/token/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=$CAKTO_CLIENT_ID" \
  -d "client_secret=$CAKTO_CLIENT_SECRET"
# → {"access_token": "...", "expires_in": 36000, "token_type": "Bearer", "scope": "..."}
```

Token dura 10h (`expires_in: 36000`). Guardar em variável, usar em todo request:
`Authorization: Bearer <access_token>`.

**Não usar `grant_type` no body** — a Cakto não segue esse campo padrão OAuth2, só `client_id` +
`client_secret`. Mandar `grant_type` devolve `{"error": "unsupported_grant_type"}`.

### Criar produto

```bash
curl -X POST https://api.cakto.com.br/public_api/products/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Nome do produto",
    "description": "Descrição",
    "price": "27.90",
    "salesPage": "https://minhaoferta.com",
    "contentDeliveries": [],
    "paymentMethods": []
  }'
```

Resposta traz `id` e `short_id`. **Não existe endpoint "criar checkout" separado** — ao criar o
produto, a Cakto já gera checkout + link de pagamento automático. Pegar o link:

```bash
curl https://api.cakto.com.br/public_api/products/{id}/checkouts/ \
  -H "Authorization: Bearer $TOKEN"
# checkout com "default": true é o padrão
```

### Criar oferta (preço alternativo DO MESMO produto — não é order bump, ver seção própria abaixo)

```bash
curl -X POST https://api.cakto.com.br/public_api/offers/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product": "<id do produto>", "price": "17.90", "name": "...", "currency": "USD", "type": "unique"}'
```

`product` tem que ser id de produto **já criado na mesma conta** — senão 400
`{"detail": "Produto não encontrado."}`. **Oferta não herda a moeda do produto** — se o produto é
USD e a oferta vai sem `currency`, nasce em BRL (bug de app real, 29/10/2026: criei 4 ofertas de
teste sem `currency` e todas saíram em reais num produto que devia ser dólar — tive que deletar e
recriar). Link público de pagamento: `https://pay.cakto.com.br/{id_da_oferta}`.

### O modelo real (confirmado na doc + testado): Produto → Oferta → Checkout → Order Bump

```
Produto (name/description/price/currency/type) ──> Oferta padrão (nasce junto)
                                                 ──> Checkout padrão (nasce junto, sempre existe 1 default:true)
Oferta ──> link público: pay.cakto.com.br/{id_da_oferta}
Order Bump ──> é OUTRO PRODUTO inteiro, linkado ao principal por POST /products/{id}/bumps/
              {"product": "<id do produto complementar>", "offer": "<id da oferta dele>"}
```

- **Criar produto já cria oferta padrão + checkout + link de pagamento** — não existe endpoint
  "criar checkout" separado.
- **Order bump NÃO é uma oferta do mesmo produto.** É um produto PRÓPRIO (com sua própria oferta),
  anexado ao checkout do produto principal via `POST /public_api/products/{id_do_produto_PRINCIPAL}/bumps/`.
  Erro real já cometido nesta skill: tratei "upgrade/downgrade" e "combo" como ofertas do mesmo
  produto — isso é certo pra VARIAÇÃO DE PREÇO do mesmo item (ex.: entrada $5,90 vs combo $12,90
  do mesmo kit), mas pra um **item complementar de verdade** (ex.: order bump separado tipo
  "Environment Pack"), precisa ser produto novo + vínculo por `bumps/`.
- Campos do order bump: `offer` (id da oferta a exibir), `referencePrice` (preço riscado), `cta`,
  `title`, `description`, `position` (ordem no checkout), `showImage`.
- Mesma oferta não pode virar bump duas vezes do mesmo produto → 400
  `{"detail": "Oferta já cadastrada como order bump deste produto."}`.

### Vender em dólar (internacional) — regras reais, testadas 29/10/2026

- **A moeda se define SÓ na criação do produto**, com `"currency": "USD"`. Não dá pra editar depois
  — tentativa de PUT/PATCH com `currency` diferente volta 400
  `"A moeda não pode ser alterada após a criação do produto."`. Pra vender o mesmo conteúdo em
  BRL e USD, cria **dois produtos**, um em cada moeda.
- **Só pagamento único em dólar.** `"type": "subscription"` num produto USD é recusado:
  `"Assinatura não está disponível para produtos internacionais."`.
- **Preço mínimo: US$ 1,00** no produto em dólar (contra **R$ 5,00** no produto em BRL — o exit
  popup a US$4,90 que a dona pediu bateu nesse chão quando criei sem moeda, por isso o erro
  "O preço mínimo é R$ 5.00" apareceu num preço que devia ser dólar).
- **Oferta e order bump de produto em dólar têm que ser dólar também** — sem `currency: "USD"` no
  corpo, a API recusa com `"A oferta deve ter a mesma moeda do produto."` / `"O order bump deve
  ter a mesma moeda do produto."`.
- **Não manda `paymentMethods` num produto em dólar** — a Cakto resolve sozinha pelo país do
  comprador; se mandar, é ignorado em silêncio com um aviso em `warnings` na resposta.
- O checkout internacional identifica país pela conexão do comprador (pode trocar no seletor), abre
  no idioma do país (inglês se o país não tem idioma definido), mostra preço convertido pra moeda
  local em países com cobrança local (ex. peso mexicano) ou em dólar nos demais/PayPal. Documento
  (CPF/equivalente) só é pedido em países que exigem (Argentina, Colômbia).
- **Venda em dólar entra em saldo separado** do saldo em reais — converte ou saca (Payoneer) à parte
  no Financeiro do painel.

### Listar produtos (smoke test / auditoria)

```bash
curl https://api.cakto.com.br/public_api/products/ -H "Authorization: Bearer $TOKEN"
```

### Escopos de API (ao criar chave nova)

`read` · `write` · `products` · `offers` · `orders` · `subscriptions` · `webhooks` ·
`card_tokenization` · `payments` · `withdrawals_read` · `withdrawals_write` · `nfse`.
`withdrawals_write` nunca vem por herança de `write`/`payments` — tem que marcar explícito (é o
único escopo que tira dinheiro da conta).

### MCP oficial (CaktoMCP)

A Cakto tem **MCP server próprio** ("CaktoMCP"), visível no painel em Integrações → Cakto MCP,
e um conjunto de ferramentas de descoberta **sem login** (`cakto_search_docs`, `cakto_get_guide`,
`cakto_search_help`) documentadas em `docs.cakto.com.br/mcp/ferramentas-de-descoberta` — consultam
o contrato da API e a central de ajuda sem credencial. Não testado neste pane se compensa configurar
como MCP server do Overclock vs. só chamar a API via Bash/curl — pra criar produto/oferta em lote,
curl direto é mais simples e já validado. Se precisar conectar via MCP de verdade (ex. uso
conversacional direto no painel), configurar pelo botão "Configurar o CaktoMCP" dentro de Cakto API.

## Cobertura internacional

- **190+ países, 135 moedas, 100+ métodos locais de pagamento** (`cakto.com.br/cobertura`).
- Checkout detecta localização do comprador e ajusta **idioma + moeda + métodos automaticamente**
  (ex.: sem Pix pra comprador nos EUA, mas com cartão internacional/Apple Pay/Google Pay).
- Preço em moeda estrangeira **não precisa ser conversão 1:1 do BRL** — define separado por mercado
  (mesma lógica de [[preco-moeda-local-qualquer-pais]] nas outras ofertas do portfólio).
- Mesmo checkout, mesma área de membros, mesmo painel do nacional — não é produto à parte.
- Juridicamente: nacional = **Cakto Pay** (Brasil); internacional = **Cakto Commerce OÜ** (Estônia).
  Isso aparece em termos/recibos, não muda a operação no painel.
- Exemplos de cobertura por região (lista não é exaustiva, confirmar no `/cobertura` antes de prometer
  um país específico): Brasil (BRL, Pix/Visa/Mastercard), EUA (USD, Visa/Mastercard/Amex), União
  Europeia (EUR, SEPA/iDEAL/Bancontact).

## Taxas — confirmadas NO PAINEL (Menu da conta → Planos e Taxas → seletor de país), 29/10/2026

A doc pública (`cakto.com.br/pagamentos`) só dá o quadro geral BRL. **Taxa real por país só existe
no painel**, não na API — `Minha Conta` → aba `Planos E Taxas`, campo `Pais` troca o conjunto de
métodos + taxas exibido. Conferido direto na tela, conta LeadGo:

| País | Métodos disponíveis | Taxa (todos os métodos locais, exceto PayPal) | PayPal | Recebimento |
|---|---|---|---|---|
| **Brasil (BRL)** | Cartão, Boleto, Pix, Pix Automático, PicPay | Cartão/Boleto 4,99%+R$2,49 · Pix 0%+R$2,49 · Pix Automático 8,99%+R$2,49 | — | Cartão 15d · Boleto 2d · Pix 1d · Pix Autom. 7d |
| **EUA (USD)** | Cartão, PayPal | 4,99%+US$0,70 | 6,99%+US$0,70 | 7 dias |
| **México (USD)** | Cartão crédito/débito, OXXO, SPEI, Mercado Pago, PayPal | 4,99%+US$0,70 | 6,99%+US$0,70 | 7 dias (SPEI 6d) |

**Achado principal: a taxa % é a MESMA em todo país internacional (4,99%+US$0,70 cartão/método
local, 6,99%+US$0,70 PayPal) — só o CONJUNTO DE MÉTODOS disponível muda por país**, não a taxa em
si. Isso simplifica a decisão de SKU: não precisa de tabela de taxa por país, só de tabela de
MÉTODO por país (pra saber o que vai aparecer pro comprador).

**Pendente/não confirmado:** Reino Unido, Alemanha, Colômbia — tentei checar e bati num bug do
seletor de país do painel (abaixo), os dados que saíram de lá eram resíduo do México, descartados.
Reconferir quando precisar de verdade de um desses.

**Bug do seletor de país no painel (anotar pra próxima sessão de browser):** o campo `Pais` é um
combobox com busca por texto — `keyboard type` digita **sem limpar o valor anterior**, concatenando
o texto digitado por cima do nome do país já selecionado (ex.: ficou "MéxicoColômAlemanhaColômbia...").
A seleção F-ArrowDown+Enter não necessariamente troca o país de verdade quando isso acontece — os
dados de taxa continuaram mostrando México mesmo depois de "selecionar" Colômbia/Alemanha. **Corrigir
da próxima vez:** limpar o campo antes de digitar (`Control+a` + `Delete`, ou usar `fill` em vez de
`keyboard type` se o CLI suportar nesse combobox), e **conferir que o texto do combobox bateu com
o país pedido antes de ler a taxa** — nunca confiar que Enter funcionou sem essa checagem.

- **Sem mensalidade, sem adesão** em nenhuma moeda. Cobrança só por venda aprovada.
- Saque BRL: R$ 4,59. Saque USD: Payoneer (taxa não conferida ainda).
- Taxa efetiva pesa mais em produto barato (ticket R$27 → ~14% efetivo no cartão BR; ticket R$997 →
  ~5,2%) — mesma lógica vale em dólar: ticket $4,90-5,90 (padrão Rodrigo Liedson,
  `metodo-rodrigo-liedson`) tem taxa % efetiva bem mais alta que ticket $29,90+.

## Próximos passos se for usar de verdade

1. Primeira venda real: criar produto de teste pela API, conferir checkout no ar, rodar o
   [gate de eventos](../../CLAUDE.md) (PageView/IC) igual qualquer checkout novo do portfólio.
2. Webhook: a chave de API criada tem escopo `webhooks` liberado mas o cadastro do endpoint de
   webhook em si não foi testado neste pane — seguir `docs.cakto.com.br` seção Webhooks quando a
   oferta real entrar em produção, e registrar nos dois webhooks de praxe
   (área de membros + Trackeador, regra da dona 16/10/2026).
3. Registrar a conta em `_memoria/contas-e-codigos.md` (gateway · conta · perfil de browser) assim
   que a primeira oferta real for cadastrada aqui.

## Caso real: GeriNeuro US — régua de teste (29/10/2026)

Primeiro uso de verdade desta skill. Criado via API (produto em USD, correto na 2ª tentativa depois
do erro de moeda documentado acima):

- **Produto:** `d5294830-24f4-402d-9d42-1b78acc59016` — "GeriNeuro Basic — Cognitive Stimulation Kit",
  USD, type `unique`.
- **Oferta entrada ($5,90):** `b32mgtm` (oferta padrão, nasceu junto do produto) →
  `pay.cakto.com.br/b32mgtm`
- **Oferta upgrade/downgrade ($7,90):** `cmnyy2i` → `pay.cakto.com.br/cmnyy2i`
- **Oferta combo/completo ($12,90):** `3fm42f7` → `pay.cakto.com.br/3fm42f7`
- **Oferta saída/exit popup ($4,90):** `vg3hgz7` → `pay.cakto.com.br/vg3hgz7`

Régua decidida com a dona usando o método `metodo-rodrigo-liedson` (ticket de validação, mais barato
que o ticket de escala já no ar na Cooud/Mundpay — $14,90/$19,90). **Os 3 order bumps da GeriNeuro
($4,90/$5,90/$6,90) ainda não foram criados aqui** — pelo modelo real (seção acima), cada um precisa
virar produto próprio + vínculo via `bumps/`, não uma oferta do produto principal. Próximo passo
quando for migrar de vez: criar os 3 produtos-bump em USD e linkar ao produto principal.

**Status:** testes criados pra servir de referência de ticket/estrutura — a oferta ao vivo continua
na Cooud/Mundpay (ver `OFERTAS/gerineuro-us/CLAUDE.md` e `checkout/MAPA-DE-PRECOS.md`) até decisão
de migrar o checkout de verdade.
