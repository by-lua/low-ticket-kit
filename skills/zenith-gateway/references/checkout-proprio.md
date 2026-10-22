# Checkout próprio na Zenith — os três caminhos, e qual está realmente aberto

Apurado em 08/09/2026 na conta `contact@seudominio.com` (seller "Dona De lima assis Store", KYC aprovado), lendo a doc **e** clicando o painel. Onde os dois discordam, o painel manda — e eles discordam.

## Onde sai a credencial

**`/integracoes-zenith`** ("Integrações Zenith / DEVELOPER PRODUCTS"). Botão **"Criar nova chave"** na seção *2. ACESSO TÉCNICO · Credencial server-to-server*. A public key fica na lista; a **secret aparece uma única vez**, logo após a criação — guarde na hora.

**Essa tela vem trancada.** Antes da liberação ela retorna 404 e não aparece no menu lateral. Nesta conta foi preciso pedir ao suporte para liberar (feito em 08/09/2026). Um 404 aqui significa "Payments API ainda não liberada para a conta", não "URL errada" — abra chamado no Atendimento Zenith antes de concluir qualquer coisa.

Nela também estão: os produtos liberados (`Zenith Payments API`, `Zenith Elements`, cada um com Sandbox e Produção) e o **routing real** — o seletor "País, moeda e ambiente" lista só o que a conta tem, com o contrato de cada método (payload obrigatório, limites, como gerar) já preenchido com o país escolhido.

Não confunda com `/api-credentials`, que emite apenas a chave **API Sales PIX** (escopos fixos, só `POST /api-sales/pix`, só BRL), nem com `/integracoes`, que não emite chave nenhuma.

## Routing real da conta (produção, 08/09/2026)

| País | Moeda | Métodos |
|---|---|---|
| Argentina | ARS | `bank-transfer` |
| México | MXN | `oxxo`, `spei`, `codi` |
| Colômbia | COP | `pse`, `bre-b-llave`, `nequi` |
| Peru | PEN | `bank-transfer`, `yape`, `plin`, `cash` |
| Índia | INR | `upi` |
| Filipinas | PHP | `gcash`, `maya` |

**Sem cartão em nenhum país** e **sem Brasil** (PIX sai por `/api-sales/pix`). A doc lista para Argentina também `qr-interoperable`, `mercado-pago` e `debin`, e para México `paycash` e `paynet` — **a conta não tem nenhum desses**. É exatamente por isso que a regra "consulte `GET /integrations/payment-methods`, nunca fixe a lista" existe.

## Os três caminhos

### 1. Checkout Builder (`/checkouts`) — hospedado, e só serve BR

Builder visual com preview Desktop/Mobile, 4 temas, timer, selo de confiança, lista de benefícios e order bump nativo. Botão "Publicar checkout".

Duas limitações que só aparecem olhando a tela:

- **É brasileiro por dentro.** Campo **CPF** obrigatório, telefone no formato `(11) 9…`, valores em **R$**, parcelamento em reais. Métodos oferecidos: Apple Pay, Google Pay, Cartão, PIX, Boleto, Carteira. Nada de ARS/MXN, nada de SPEI, OXXO, CVU, QR interoperável ou Mercado Pago.
- **Não lê o catálogo de produtos.** Nome, subtítulo, benefícios, subtotal, desconto e order bump são campos de texto livre digitados na mão. Os produtos cadastrados em `/infoprodutos` não aparecem como opção. São dois cadastros independentes no mesmo painel — cadastrar produto ali **não** o coloca em nenhum checkout.

Serve para venda BR simples. Não serve para vender fora do Brasil.

### 2. API Sales PIX (`/api-sales`) — o único aberto hoje

Rota própria e mais enxuta que a Payments API. `amount` em centavos, `currency` BRL.

```bash
curl -X POST https://api.zenithworld.com.br/api-sales/pix \
  -H "Content-Type: application/json" \
  -H "x-api-key: $ZENITH_PUBLIC_KEY" \
  -H "x-api-secret: $ZENITH_SECRET_KEY" \
  -H "Idempotency-Key: pedido-1001-pix" \
  -d '{
    "amount": 12990,
    "currency": "BRL",
    "referenceId": "pedido_1001",
    "customer": {
      "name": "Cliente Teste",
      "email": "cliente@loja.com",
      "document": "12345678909",
      "phone": "11999999999"
    }
  }'
```

Resposta traz `pix.copyPaste` e `pix.qrCodeBase64` — renderize enquanto `status` for `PENDING`. Consulta: `GET /api-sales/pix/checkout_...`.

Exige KYC aprovado e Full PIX habilitado no seller. A chave aceita restrição por **IP/CIDR** (recomendado para server-to-server) e por domínio.

Note que os headers aqui são minúsculos (`x-api-key`) e o cliente vem aninhado em `customer`, diferente da Payments API. **Não são a mesma API** — não reaproveite o payload de uma na outra.

### 3. Payments API / Elements — o caminho certo para fora do Brasil, hoje trancado

É o que a doc descreve e o que atende AR, MX, CO, PE, PH e IN. Duas formas de montar:

**Payments API pura** — você desenha 100% do checkout, chama server-to-server e renderiza o `nextAction`:

```
GET  /integrations/payment-methods?country=AR&currency=ARS&environment=sandbox
POST /integrations/checkouts          (Idempotency-Key obrigatório)
GET  /integrations/checkouts/:id
POST /integrations/checkouts/:id/refresh
POST /integrations/checkouts/:id/cancel
```

**Elements** — SDK embutido no seu site; a Zenith renderiza o bloco de pagamento:

```
POST /elements/sessions   → elementSessionId, clientToken, elementUrl, sdkUrl, expiresAt
```

```html
<script src="https://api.zenithworld.com.br/elements/sdk.js"></script>
<div id="zenith-payment"></div>
<script>
  const element = ZenithElements.create({
    elementSessionId: session.elementSessionId,
    clientToken: session.clientToken,
    elementUrl: session.elementUrl,
    returnUrl: session.returnUrl
  });
  element.mount("#zenith-payment");
</script>
```

Escolha rápida: **Elements** se você quer os campos exigidos por método (RFC no SPEI, etc.) resolvidos por eles; **Payments API** se você quer controle total do visual e aceita montar cada `customerFields` na mão.

## Receita ponta a ponta para Argentina (Payments API)

Preços do exemplo em ARS, unidade minoritária (centavos): ARS 14.900,00 = `1490000`.

**1. Consulte os métodos — nunca fixe a lista no código:**

```bash
curl "https://api.zenithworld.com.br/integrations/payment-methods?country=AR&currency=ARS&environment=sandbox" \
  -H "X-API-Key: $ZENITH_PUBLIC_KEY" \
  -H "X-API-Secret: $ZENITH_SECRET_KEY"
```

Renderize o que voltar em `items` — `code`, `customerFields`, `requiredPayloadFields`, `amountLimits`. Código que aparecer em `conflicts` (empate de rota interna) **some de `items`**: não escolha rota na mão.

**2. Crie o checkout:**

```bash
curl -X POST "https://api.zenithworld.com.br/integrations/checkouts" \
  -H "X-API-Key: $ZENITH_PUBLIC_KEY" \
  -H "X-API-Secret: $ZENITH_SECRET_KEY" \
  -H "Idempotency-Key: $PAYMENT_INTENT_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 1490000,
    "currency": "ARS",
    "country": "AR",
    "environment": "sandbox",
    "paymentMethod": "bank-transfer",
    "referenceId": "pedido-123",
    "customerName": "Ana Silva",
    "customerEmail": "voce@exemplo.com",
    "returnUrl": "https://sualoja.com/gracias",
    "cancelUrl": "https://sualoja.com/carrito"
  }'
```

Os onze campos obrigatórios do contrato: header `Idempotency-Key`, `amount`, `currency`, `country`, `environment`, `paymentMethod`, `referenceId`, `customerName`, `customerEmail`, `returnUrl`, `cancelUrl`. Qualquer campo além disso vem de `requiredPayloadFields` do passo 1.

**3. Renderize o `nextAction`** conforme o tipo (`qr_code` para QR interoperável e Mercado Pago, `bank_transfer` para DEBIN, `redirect` para CVU/cartão). Sempre renderize `nextAction.instructions` junto quando vier.

**4. Confirme só pelo webhook assinado.** Redirect concluído e polling atualizam tela, não liberam pedido.

## Métodos AR e MX: catálogo vs. o que a conta tem

A doc publica um catálogo maior do que o routing desta conta. A coluna da direita é o que existe de verdade hoje:

| Código | Método | `nextAction` | Nesta conta? |
|---|---|---|---|
| `bank-transfer` | Transferência por CVU (aceita CBU) | `bank_transfer` com a CVU de destino | **AR: sim** |
| `qr-interoperable` | QR interoperável | `qr_code` | não |
| `mercado-pago` | Mercado Pago | `qr_code` + instruções | não |
| `debin` | DEBIN | `bank_transfer` | não |
| `oxxo` | OXXO | `voucher` | **MX: sim** |
| `spei` | SPEI | `bank_transfer` (CLABE) | **MX: sim** |
| `codi` | CoDi | `qr_code` | **MX: sim** |
| `paycash` / `paynet` | vouchers MX | `voucher` | não |
| `card` | Cartão | `redirect` | **não, em país nenhum** |

Sobre a CVU na Argentina, o painel avisa: a Zenith devolve a CVU de destino da ordem, e o comprador pode transferir para ela tanto de conta identificada por CBU quanto de carteira identificada por CVU. Alguns apps mostram a opção só como "CBU" ou "CBU/CVU/Alias" — o nome exibido não muda a CVU de destino.

## Armadilhas que só aparecem depois

- **Cadastrar produto em `/infoprodutos` não cria checkout nenhum.** O status `ACTIVE` ali não coloca o produto à venda em lugar algum — o Builder não lê esse catálogo, e a Payments API recebe `amount` e `referenceId` direto no payload, sem consultar produto.
- **`amount` é inteiro na menor unidade.** ARS 14.900,00 é `1490000`, não `14900`. Errar isso cobra 100× a mais.
- **`Idempotency-Key` é por intenção lógica**, gerada uma vez e persistida. Retry técnico mantém chave e payload; pedido novo, chave nova. Mesma chave com payload diferente → `409 IDEMPOTENCY_KEY_CONFLICT`.
- **Dados fictícios bloqueiam a conta.** `customerName` precisa de nome e sobrenome reais; e-mail temporário ou de teste é recusado. A doc avisa que reincidência leva a bloqueio permanente após análise de conformidade. Em sandbox, use dados reais de alguém do time.
- **A secret nunca cruza para o navegador.** Nem em payload, URL, log, analytics ou repositório.

## Antes de montar isso para Argentina

O Astrodicas já roda Mercado Pago nativo em AR, que cobre cartão, saldo em conta e transferência. A Zenith nesta conta oferece **só transferência por CVU** — um subconjunto — cobrando 7,99% + R$ 5,00 fixo e retendo 10% por 90 dias. Não é upgrade de método; é menos método, mais caro. Em ticket de ARS 12.819 (~R$ 38), o fixo de R$ 5 sozinho já é ~13%.

Zenith em AR só ganha sentido se o objetivo for **consolidar o recebimento no CNPJ brasileiro**, não reduzir taxa.
