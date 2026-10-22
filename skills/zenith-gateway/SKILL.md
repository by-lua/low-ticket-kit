---
name: zenith-gateway
description: Integrar, avaliar ou decidir sobre a Zenith (Zenith Pay / Zenith World / Zenith Global) — gateway de pagamento global com CNPJ brasileiro que oferece métodos locais em BR, MX, CO, PE, AR, PH e IN (PIX, boleto, SPEI, OXXO, PSE, Nequi, Yape, Plin, GCash, Maya, UPI). Cobre a Payments API e o Zenith Elements (auth, criar checkout, nextAction, webhooks assinados, idempotência, códigos de erro), o acesso ao painel seller pelo browser persistente, a tabela real de taxas/reserva/prazos e os riscos apurados da empresa. Use quando o pedido citar Zenith, zenithworld.com.br, zenithwld.com.br, Zenith Pay, Zenith Elements, checkout global, ou quando for comparar gateway para vender low ticket fora do Brasil.
---

# Zenith — gateway global com CNPJ brasileiro

Levantamento feito em 08/09/2026 na conta `contact@seudominio.com`. Números conferidos direto no painel e na doc oficial, não em material de venda.

## Leia isto antes de integrar

A Zenith resolve um problema real: **método de pagamento local em 7 países com CNPJ brasileiro** — coisa que Stripe com sede BR não faz (Stripe BR só habilita boleto e Pix, e só para comprador brasileiro).

O preço disso é alto e mal documentado. Antes de escrever qualquer linha de código, leia `references/RISCOS.md`. Se a decisão de usar a Zenith ainda não foi tomada, a decisão vem primeiro; a integração depois.

## Mapa rápido

| Preciso de… | Vá para |
|---|---|
| Autenticar, escopos, rate limit | `references/authentication.txt` |
| Primeiro checkout ponta a ponta | `references/quickstart.txt` |
| Contrato completo da API | `references/payments-api.txt` |
| SDK embutido no meu site | `references/elements.txt` |
| Métodos por país e campos exigidos | `references/payment-methods.txt` |
| Confirmar pedido com segurança | `references/webhooks.txt` |
| Tratar erro e não duplicar cobrança | `references/errors.txt` |
| Checklist antes de produção | `references/go-live.txt` |
| **Montar checkout próprio (e o que está trancado)** | **`references/checkout-proprio.md`** |
| **Integração real ponta a ponta (CoDi/MX, com deploy)** | **`references/codi-numero-maestro.md`** |
| Um país específico | `references/countries-{ar,br,co,in,mx,pe,ph}.txt` |
| Taxas, prazos, risco da empresa | `references/RISCOS.md` |
| Entrar no painel | seção "Acesso" abaixo |

## Acesso ao painel

Perfil de browser persistente `zenith`, porta **9251**, já logado (sessão sobrevive a reboot).

```bash
~/.claude/bin/browsers.sh zenith          # sobe se estiver parado
agent-browser --session zenith snapshot   # usa
```

Credenciais em `~/.claude/.credentials.env`: `ZENITH_EMAIL`, `ZENITH_PASSWORD`.
Carregue com `set -a; source ~/.claude/.credentials.env; set +a` e **sempre use a variável**, nunca o valor literal.

**Login tem 2FA TOTP.** O fluxo automatizável vai até a tela do autenticador; o código de 6 dígitos precisa do humano. O Turnstile da Cloudflare valida sozinho nesse perfil — não trate como bloqueio.

Ordem: abrir `/login` → preencher email e senha → esperar o Turnstile virar "Sucesso!" → clicar Entrar → pedir o TOTP ao usuário.

**Rotas reais do painel** (conferidas no menu em 08/09/2026 — a doc da Zenith cita caminhos que dão 404):

| Tela | Rota |
|---|---|
| Dashboard | `/dashboard` |
| Vendas | `/transactions` |
| Produtos | `/infoprodutos` |
| Checkout Builder | `/checkouts` |
| API Sales PIX | `/api-sales` |
| Chaves de API | `/api-credentials` |
| **Integrações Zenith** (developer products, credencial da Payments API) | **`/integracoes-zenith`** |
| Integrações (conta de recebimento, canais) | `/integracoes` |
| Webhooks | `/webhooks` |
| Clientes | `/clients` |
| Financeiro · Saques · Taxas · KYC | `/financeiro`, `/saques`, `/minhas-taxas`, `/kyc` |

`/produtos` e `/checkout` **não existem** — retornam 404.

`/integracoes-zenith` é a tela mais importante para integrar, e **vem trancada**: antes da liberação ela retorna 404 e nem aparece no menu lateral. Nesta conta foi preciso **falar com o suporte** para liberar (feito em 08/09/2026); só então a rota passou a responder e o item "Integrações Zenith" surgiu no menu.

Se ela der 404 numa conta nova, isso não é bug nem URL errada — é o produto Payments API ainda não liberado. Abra chamado no "Atendimento Zenith" pedindo acesso às Integrações Zenith / Payments API. Não conclua que a rota não existe.

## API em 6 linhas

Base: `https://api.zenithworld.com.br`

```
X-API-Key: zp_pub_...      # identifica a credencial
X-API-Secret: zp_sec_...   # prova que veio do teu servidor — só backend, HTTPS
```

| Endpoint | Faz |
|---|---|
| `GET /integrations/payment-methods` | métodos liberados + campos exigidos em runtime |
| `POST /integrations/checkouts` | cria o checkout (exige `Idempotency-Key`) |
| `GET /integrations/checkouts/:id` | estado atual |
| `POST /integrations/checkouts/:id/refresh` | força consulta à rota financeira |
| `POST /integrations/checkouts/:id/cancel` | cancela |
| `POST /elements/sessions` | sessão efêmera do SDK embutido |
| `POST /integrations/webhooks/endpoints` | registra endpoint de webhook |

Escopos: `CHECKOUT_CREATE`, `CHECKOUT_READ`, `WEBHOOKS_READ`, `WEBHOOKS_WRITE`. Crie credencial com o mínimo necessário.

Rate limit: 300/min por credencial, 1200/min em leitura de checkout, 60/min em `POST /elements/sessions`. Em 429, respeite `Retry-After` e os headers `RateLimit-*`.

## As cinco regras que quebram integração

**1. Nunca fixe a lista de métodos no código.** Consulte `GET /integrations/payment-methods` e renderize o que voltar — `code`, `customerFields`, `requiredPayloadFields`, `amountLimits`. Cada método pede campos diferentes; supor que nome e e-mail bastam gera `PAYMENT_PAYLOAD_FIELDS_REQUIRED`. Se dois roteamentos internos empatarem, o método **some de `items` e aparece em `conflicts`** — não escolha rota na mão.

**2. `Idempotency-Key` é por intenção lógica, não por chamada de rede.** UUID/ULID gerado uma vez e persistido. Retry técnico mantém chave e payload idênticos. Pedido novo, chave nova. Mesma chave com payload diferente → `409 IDEMPOTENCY_KEY_CONFLICT`. Chave constante para todos os pedidos é bug garantido.

**3. `amount` é inteiro na menor unidade.** `10990` = MXN 109,90. Errar isso cobra 100× a mais.

**4. Só o webhook assinado confirma pedido.** Evento do navegador e polling servem para atualizar tela. Valide HMAC SHA-256 de `timestamp + "." + rawBody` com o **corpo bruto**, rejeite timestamp com mais de 300s, compare em tempo constante, e guarde `X-Zenith-Event-Id` com restrição única. Responda 2xx só depois de persistir.

**5. Dados fictícios bloqueiam a conta.** `customerName` precisa de nome e sobrenome reais; e-mail temporário ou de teste é recusado (`CUSTOMER_EMAIL_INVALID`, `CUSTOMER_NAME_INVALID`). A doc avisa que uso reiterado leva a **bloqueio permanente após análise de conformidade**.

## nextAction — o que renderizar

```js
if (result.nextAction?.instructions) renderBuyerInstructions(result.nextAction.instructions);

switch (result.nextAction?.type) {
  case "redirect":      window.location.assign(result.nextAction.url); break;
  case "qr_code":       renderQrCode(result.nextAction.code); break;
  case "voucher":       renderVoucher(result.nextAction.code); break;
  case "bank_transfer": renderBankTransfer(result.nextAction.details); break;
  case "app_approval":  renderAppApproval(result.nextAction.app); break;
}
```

Em MX, CO e PE vem `instructions` com `locale`, `title` e `steps` prontos — renderize junto, é aditivo e não altera o pagamento.

`nextAction.url` é opaco e sensível: envie exatamente como veio. Nada de scraping, iframe, reverse proxy ou rehospedagem. GCash e Maya expiram em 1440 min — use `nextAction.presentation.expiresAt` como verdade, não calcule.

Estados públicos: `pending`, `authorized`, `succeeded`, `failed`, `canceled`, `refunded`.

## Zenith Elements (SDK embutido)

Backend cria a sessão; o navegador recebe só `elementSessionId`, `clientToken` efêmero e `elementUrl`. A secret nunca cruza essa fronteira.

- Sessão inicial expira em **15 minutos**
- `origin` precisa ser HTTPS e bater **exatamente** com uma origem autorizada no painel (`ORIGIN_NOT_ALLOWED`)
- `referenceId` fica vinculado — reusar com valor/moeda/país/ambiente/origem diferentes dá `409 ELEMENT_REFERENCE_BINDING_CONFLICT`
- Contexto serializado (metadata + appearance) até **24.000 bytes**
- `element.confirm()` gerencia a chave interna; essa chave **não** é a `Idempotency-Key` da Payments API

## Criar a credencial: o botão vem desabilitado por 2FA

Em `/integracoes-zenith`, "Criar nova chave" aparece **desabilitado**, com o
cabeçalho dizendo "Configuração pendente / Conclua os itens indicados abaixo" e
**nenhum item marcado como pendente** — sem tooltip, sem `title`, sem texto
explicativo. Selecionar o produto, o país e o método não destrava.

O que destrava é **2FA**: ao abrir a tela logado, o painel pede um código de 6
dígitos do autenticador ("AÇÃO PROTEGIDA — Confirmação de segurança"), válido
por cinco minutos e só para esse tipo de ação. Confirmado o código, o botão
libera e o par sai na hora. Não é bloqueio de conta e não precisa de chamado.

A secret aparece **uma única vez**. Capture direto para o `.env`.

## Sandbox não existe por padrão

`environment: "sandbox"` responde:

```
HTTP 403  {"code":"ENVIRONMENT_NOT_ALLOWED",
           "message":"Environment is not allowed for this product"}
```

Verificado em 09/09/2026 para MX/MXN (referência de suporte ZEN-AQESSPMK). O
seletor de "País, moeda e ambiente" do painel também só lista entradas
`production:*` nos seis países — o "Sandbox" que aparece no card do produto é
rótulo estático, não ambiente disponível.

Consequência: **a primeira cobrança tem que ser com dinheiro real**. Liberar
sandbox exige chamado no suporte, com essa referência.

## O login do painel trava fora do Chromium persistente

O Chromium empacotado do `agent-browser` não passa no Turnstile do login:
`Falha no Turnstile (600010)`, três tentativas, com desafio novo entre elas. Não
é senha errada — as credenciais nem chegam a ser testadas. Use o perfil
persistente do sistema (`~/.claude/bin/browsers.sh zenith`, porta 9251), onde a
sessão já fica logada.

## Credencial: onde ela realmente sai

**`/integracoes-zenith`** — tela "Integrações Zenith / DEVELOPER PRODUCTS". É ali que se cria o par `zp_pub_…` / `zp_sec_…` da Payments API, botão **"Criar nova chave"**. A secret aparece **uma única vez**, logo após a criação.

Três telas diferentes emitem coisas diferentes — não confunda:

| Tela | Emite | Serve para |
|---|---|---|
| `/integracoes-zenith` | Credencial **Payments API** (`zp_pub`/`zp_sec`) | Todo método local, todos os países |
| `/api-credentials` | Chave **API Sales PIX**, escopos fixos | Só `POST /api-sales/pix`, só BRL |
| `/integracoes` | Nada — conecta parceiro (ZapData) ou canal de recebimento | Terceiro cria checkouts por você |

A mesma tela mostra os produtos liberados (`Zenith Payments API`, `Zenith Elements`, cada um com Sandbox e Produção) e o **routing real da conta**. Leia o routing ali antes de prometer método para alguém: ele é bem menor que o catálogo da doc.

### O bloco Stripe em `/integracoes` não é pré-requisito

A tela `/integracoes` mostra "Perfil interno do Connect" com uma lista de pendências em maiúsculas (`MCC_REQUIRED`, `BUSINESS_ADDRESS_REQUIRED`, `BANK_ACCOUNT_COLLECTION_REQUIRED`, `STRIPE_TOS_ACCEPTANCE_REQUIRED`…), conta bancária "não configurada" e aceite Stripe "pendente".

**Isso não bloqueia nada.** O rodapé do próprio bloco diz: *"Esse bloco só prepara o modo novo. O fluxo atual de pagamento permanece igual."* — e o suporte da Zenith confirmou que não precisa preencher. É preparação de uma migração interna deles para Stripe Connect, não requisito para cobrar.

Mesma tela também exibe canais (Canal A–E, PagSeguro International, Movantis) e status como `TEST` / `PENDENTE`. Não leia esses rótulos como impedimento sem confirmar com o suporte: a nomenclatura é interna e engana.

## Routing real desta conta (produção, 08/09/2026)

Lido em `/integracoes-zenith`, país por país. Isto é o que a conta `contact@seudominio.com` tem — não o catálogo da doc:

| País | Moeda | Métodos liberados |
|---|---|---|
| Argentina | ARS | `bank-transfer` (CVU, aceita origem CBU) |
| México | MXN | `oxxo`, `spei`, `codi` |
| Colômbia | COP | `pse`, `bre-b-llave`, `nequi` |
| Peru | PEN | `bank-transfer`, `yape`, `plin`, `cash` |
| Índia | INR | `upi` |
| Filipinas | PHP | `gcash`, `maya` |

**Cartão não existe em nenhum dos seis.** A doc chama `card` de "cobertura global condicionada à conta"; nesta conta a condição não foi atendida. Não prometa cartão sem reconferir esta tela.

**Brasil não aparece** no routing da Payments API — PIX nesta conta sai pela rota separada `/api-sales/pix`.

Argentina tem **só transferência por CVU**: nada de Mercado Pago, QR interoperável ou DEBIN, apesar de a doc listar os quatro. México não tem PayCash nem PayNet.

Limites técnicos publicados: mín. 0,01 e máx. 20.000.000,00 na moeda local, é o teto genérico — mas **2 países têm mínimo REAL bem mais alto**, confirmado em `GET /integrations/payment-methods` (09/09/2026):

| País | Moeda | Min real | Max real | Em US$ aprox. |
|---|---|---|---|---|
| Colômbia | COP | **10.000** | 20.000.000 | mín. ≈ US$2,50 — filtra micro-ticket |
| Índia | INR | **200** | **50.000** | mín. ≈ US$2,40 |
| Filipinas | PHP | **300** | **50.000** | mín. ≈ US$5,40 |
| México/Argentina/Peru | MXN/ARS/PEN | 0,01 | 20.000.000 | mínimo técnico, na prática zero |

Não prometa checkout de ticket muito baixo em CO/IN/PH sem checar contra esse mínimo — um produto de US$1 não passa.

## Cobertura por país (catálogo da doc — não é o que a conta tem)


| País | Métodos | Observação |
|---|---|---|
| BR | PIX, boleto | |
| MX | SPEI, OXXO, PayCash, PayNet, CoDi | SPEI exige RFC, data e país de nascimento; CoDi é QR |
| CO | PSE, Nequi | Nequi: 10 dígitos começando por 3 |
| PE | Yape, Plin, bank-transfer, cash | aliases do mesmo checkout agregado, sempre `redirect` |
| AR | QR interoperável, Mercado Pago, DEBIN, bank-transfer (CVU/CBU) | `mercado-pago` devolve QR + instruções de transferência |
| PH | GCash, Maya | link de 24h, fica `pending` até webhook |
| IN | UPI | INR 200 a 50.000, rúpias inteiras |

## Taxas reais da conta (confirmadas pelo suporte, 08/09/2026)

**Métodos locais** (PIX, boleto, SPEI, OXXO, PSE, Nequi, Yape, Plin, GCash, Maya, UPI) — **todos os países, mesma taxa**:

| | |
|---|---|
| Taxa por transação | **7,99% + R$ 5,00** |
| Fundo de reserva | **10%, retido 90 dias** |
| Liquidação padrão | **D+30** |
| Tarifa de saque | R$ 10,00 por solicitação |
| Antecipação para **D+3** | **+4,5%** sobre o valor antecipado |
| Saque em USDT | **3% sobre o montante total** |

**Cartão de crédito** roda em tabela diferente e pior (do painel `/minhas-taxas`): 8,99% + R$ 5,00, reserva 15%, repasse 180 dias, e mais 2% de câmbio quando internacional. Antecipação de cartão 2,50%.

Isso desfaz a contradição antiga do painel: os 90/180 dias eram cartão, o D+30 é método local.

**O fixo de R$ 5,00 é o que mata low ticket:**

| Venda | Custo | % |
|---|---|---|
| R$ 17,90 | R$ 6,43 | **35,9%** |
| R$ 27,90 | R$ 7,23 | 25,9% |
| US$ 10 | R$ 9,07 | 17,8% |
| US$ 14 | R$ 10,69 | 15,0% |
| US$ 30 | R$ 16,20 | 11,3% |

Só fica saudável acima de ~US$ 30. Cálculo completo por ticket em `references/RISCOS.md`.

Para o cálculo completo por ticket e a comparação com Stripe e Cartpanda, veja `references/RISCOS.md`.

## Cartão: onde aparece, onde NÃO (3 produtos de checkout, confirmado 09/09/2026)

A conta tem 3 formas de gerar checkout — **cartão só existe numa delas, e só pra BR**:

| Produto | Rota | Tem cartão? | Cobertura |
|---|---|---|---|
| **Checkout Builder** | `/checkouts` | **Sim, só BR** (parcelas 1x-12x) — preview mostra métodos BR fixo, produção renderiza routing real do país (CO mostra PSE/Nequi/Bre-B, sem cartão) | visual, hospedado, tem order bump |
| **API Sales PIX** | `/api-sales` | Não — é PIX/BRL only | `POST /api-sales/pix`, chave separada de `/api-credentials` |
| **Zenith Elements / Payments API** | `/integracoes-zenith` | Não — renderiza o routing real da conta (0 cartão internacional) | SDK embutido ou checkout próprio, todos os países |

**Veredicto:** pra vender fora do Brasil com cartão, a Zenith não serve com esta conta — nenhum dos 3 produtos libera. Se precisar de cartão internacional, é outro gateway (Stripe não cobre método local BR-CNPJ fora do Brasil de qualquer forma — ver `references/RISCOS.md`).

## Antes de recomendar a Zenith para alguém

Pergunte o país-alvo e o meio de pagamento real do público:

- **Público paga no cartão** → Stripe entrega ~91% líquido em D+5, sem reserva. Zenith perde feio.
- **Público paga em OXXO/SPEI/Yape/Nequi/GCash/UPI** → Stripe com CNPJ brasileiro simplesmente não atende. Aí a Zenith é uma das poucas saídas — mas compare antes com gateway local do país-alvo.
- **Precisa receber em 2 dias** → nenhuma das duas; ver Cartpanda em `references/RISCOS.md`.
