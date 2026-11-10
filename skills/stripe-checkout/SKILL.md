---
name: stripe-checkout
description: Opera as contas Stripe da dona (organizações LeadGo = pessoal e Winx = parceria Luciola; dashboard.stripe.com) pelo painel logado ou pela API REST — criar produto/preço (único ou recorrente, BRL/USD/EUR), cupom/desconto por N meses, Payment Link, Checkout Session, portal do cliente, webhook, reembolso. Use quando o usuário pedir para criar produto/preço na Stripe, checkout Stripe, assinatura Stripe, cupom de desconto Stripe, Payment Link, webhook Stripe, ou mencionar cobrança/pagamento via Stripe.
allowed-tools: Bash(agent-browser:*), Bash(chromium:*), Bash(curl:*), Bash(node:*)
---

> **REGRA FIXA DA DONA (10/11/2026), vale em TODO checkout:** (1) order bump **"Upgrade Básico → Completo"** obrigatório no checkout do Básico (1º bump, produto próprio, libera o Completo); (2) **ofertas de membro** criadas neste gateway para tudo que a pessoa ainda não tem (internacional 50% off, piso 2,90; Brasil 30% off, piso R$ 9,90, preços BR de sempre; nome "<item> - Área de Membros", redirect `/painel`); (3) upsell/app no topo da área de membros (internacional: 30% abaixo do upsell pós-compra + 2 dias grátis; Brasil: preço de sempre) (Stripe; sem Stripe, este mesmo checkout). Tudo nos 2 webhooks (entrega + Trackeador). Regra completa: `area-membros-netflix` › REGRA FIXA 10/11/2026.


> **PERFIL `stripe` PERSISTENTE — NUNCA "SAIR" (dona, 01/11/2026):** a Stripe é operada SÓ pelo perfil de navegador `stripe` (porta **9299**, `~/.agent-profiles/stripe/`), logado pela dona. Pode FECHAR o navegador normalmente (fechar janela/`browsers.sh`) — o que NUNCA se faz é clicar em "Sair"/logout, apagar a pasta do perfil, limpar cookies ou usar outro perfil pra Stripe. TESTADO 01/11/2026: dona logou → navegador fechado normalmente (CDP `Browser.close`) → reaberto com `browsers.sh stripe` → voltou LOGADO direto no dashboard. Então fechar é seguro; o deslogue anterior foi alguém clicar em "Sair" (ou matar o processo à força). Fechar sempre de forma limpa (`Browser.close`), nunca `pkill`/`kill -9` no Chromium desse perfil. 2FA é chave de segurança/biometria: agente NÃO reloga sozinho. Antes de agir: subir o perfil e conferir `curl -s localhost:9299/json` → aba em `dashboard.stripe.com/...` (não `/login`). Caiu em login → PARAR e avisar a dona. Um pane por vez no perfil.

# stripe-checkout

## Estrutura da conta — CONFIRMADO 31/10/2026: sem organização, contas avulsas no mesmo login

> **REGRA DA DONA (10/11/2026) — ORGANIZAÇÃO POR SÓCIO. Esta regra vale sobre o texto abaixo.**
> - **Winx** = organização Stripe nova, pedida pela dona, para **tudo que é parceria com a Luciola** (ex.: Calendrier Magique FR, Calendário Mágico AR e qualquer oferta "Lua + Luciola"). Produto, preço, assinatura e webhook dessas ofertas são criados **dentro da Winx**, numa conta da oferta dentro dela.
> - **LeadGo** = coisas pessoais da dona (LeadGo, AdsTrackeador e o que não for parceria). Nada da parceria Luciola vai pra LeadGo.
> - Antes de criar algo: conferir o dono da oferta em `OFERTAS/<slug>/CLAUDE.md` (linha "Donas") e escolher a organização. Dúvida = perguntar à dona.
> - Se a Winx ainda não aparecer no seletor de contas/organizações do perfil `stripe`, **não criar conta avulsa no lugar**: parar e avisar a dona.
> - Variáveis: `STRIPE_WINX_<CONTA>_...` para contas da Winx.

Login `stripe` acessa **contas Stripe separadas no mesmo login**, não uma
Organização (recurso "Organizations" da Stripe) — essa hipótese anterior foi
testada e é falsa; "LeadGo" é/era conta solo, sem org. Cada produto/negócio
da dona vira uma **conta nova e independente** (menu do usuário → Criar →
Criar conta → "Crie uma conta separada", nunca "Nova organização" — essa
opção envolveria a conta já existente numa org nova, mexendo na estrutura
dela; só use se a dona pedir explicitamente).

- **AdsTrackeador já tem conta própria**: `acct_1UWg3pK4KjNuQhim`, criada
  31/10/2026, Brasil/BRL, avulsa (sem vínculo com a LeadGo). **ATIVADA em 02/11/2026** pela dona
  (mesmos dados da empresa da LeadGo): `details_submitted`, `charges_enabled` e
  `payouts_enabled` = true, modo live liberado. Chave LIVE continua exigindo
  autorização explícita dela (ver § Regras).
- **LIVE configurado 02/11/2026** (autorizado pela dona): chave restrita
  `rk_live_…Jq2e` ("AdsTrackeador producao (Coolify)", acesso total exceto
  operações que movem dinheiro pra fora) em `STRIPE_ADSTRACKEADOR_LIVE_SECRET_KEY`;
  produto "AdsTrackeador Premium", preço R$150/mês `lookup_key
  adstrackeador_premium_mensal` (`..._LIVE_PRICE_PREMIUM_ID`), cupom R$50,10 off
  × 3 meses `metadata.key adstrackeador_launch_3m` (`..._LIVE_COUPON_LAUNCH_ID`),
  webhook `https://app.adstrackeador.com/api/billing/stripe` com 7 eventos
  (`..._LIVE_WEBHOOK_SECRET`). No Coolify do app: STRIPE_SECRET_KEY,
  STRIPE_WEBHOOK_SECRET, STRIPE_PRICE_PREMIUM_ID, STRIPE_COUPON_LAUNCH_ID.
  Criar chave pede verificação por e-mail (contact@seudominio.com, perfil
  hostinger-mail) + código do autenticador (só a dona). A chave só aparece
  mascarada; "Copiar e fechar" põe na área de transferência → `wl-paste` direto
  pro arquivo, nunca na tela. Criar env no Coolify com `--is-literal
  --build-time=false` dá 422; crie sem essas flags.
- **Antes de QUALQUER ação**: confira o nome da conta no seletor (canto
  superior esquerdo, menu do usuário) — ação na conta errada afeta outro
  negócio da dona. "LeadGo" é conta LIVE e ativa (pk_live em uso); nunca
  mexer nela por engano.
- **Chaves de API são POR CONTA** (cada conta tem seu próprio par
  test/live), nunca da organização como um todo. Nomeie as variáveis em
  `~/.claude/.credentials.env` com o nome da conta, nunca genérico:
  `STRIPE_ADSTRACKEADOR_TEST_SECRET_KEY`, `STRIPE_ADSTRACKEADOR_TEST_WEBHOOK_SECRET`,
  `STRIPE_ADSTRACKEADOR_LIVE_SECRET_KEY` (esta última só com autorização
  explícita pra modo live — ver § Regras). Variável sem nome de conta
  (`STRIPE_SECRET_KEY` solto) é ambígua nesta organização — não crie assim
  no arquivo de credenciais (o app em produção pode continuar usando nome
  genérico no PRÓPRIO env do Coolify, que é escopado por app; o arquivo de
  credenciais compartilhado entre contas é que precisa do prefixo).

## Acesso

Perfil de browser do sistema **`stripe`**, porta **9299**, URL
`dashboard.stripe.com` (registrado em 31/10/2026). Credenciais
`$STRIPE_EMAIL`/`$STRIPE_PASSWORD` em `~/.claude/.credentials.env` — nunca
literal. Sempre headed. Todo comando: `agent-browser --session stripe ...`.

2FA/código por e-mail (quando a Stripe oferecer essa opção — não confirmado
se está disponível nesta conta, ver aviso no topo) vai pra
`contact@seudominio.com` → perfil `hostinger-mail` (porta 9274). Abra SÓ o
e-mail da Stripe com o código, o mais recente — nunca outro e-mail. Se não
achar pelo assunto, pare e pergunte.

**Preferência por API sobre clique no painel.** Toda operação de cadastro
(produto, preço, cupom, webhook) tem equivalente na API REST
(`api.stripe.com/v1/...`, autenticação HTTP Basic com a secret key como
usuário, senha vazia; corpo form-urlencoded, nunca JSON) — mais rápido,
sem depender de seletor/refs do painel mudando. Use o painel só pra: ver o
que já existe antes de criar (evitar duplicar), configurar métodos de
pagamento da conta (não é API), e o fluxo de 2FA/login em si. Exemplo de
chamada:

```bash
curl -s https://api.stripe.com/v1/products \
  -u "$STRIPE_ADSTRACKEADOR_TEST_SECRET_KEY:" \
  -d name="AdsTrackeador Premium"
```

**NUNCA imprima a chave inteira** em log/commit/chat — só os últimos 4
caracteres se precisar confirmar qual chave está em uso. Nunca modo LIVE
sem autorização explícita da dona (ver § Regras).

## 1. Criar produto + preço (único ou recorrente)

> **REGRA FIXA (mesma lógica da Wiven): o NOME do produto/preço NÃO leva
> valor embutido.** Nunca "Premium R$150", só "AdsTrackeador Premium" — o
> valor fica só no campo de preço. Motivo idêntico ao da Wiven: nome com
> preço congelado mente assim que o preço mudar (promoção, reajuste).

Preço ÚNICO (cobrança avulsa, não recorrente):

```bash
curl -s https://api.stripe.com/v1/prices -u "$KEY:" \
  -d product=<product_id> -d currency=brl -d unit_amount=15000
```

Preço RECORRENTE (assinatura mensal):

```bash
curl -s https://api.stripe.com/v1/prices -u "$KEY:" \
  -d product=<product_id> -d currency=brl -d unit_amount=15000 \
  -d "recurring[interval]"=month
```

Três moedas suportadas pelo produto (BRL/USD/EUR, igual ao resto do
AdsTrackeador — nunca misturar moeda no mesmo cálculo): crie um **Price por
moeda** para o MESMO Product (a Stripe não converte sozinha; cada Price é
uma combinação fixa produto+moeda+valor+recorrência). `lookup_key` único
por price (ex.: `adstrackeador_premium_mensal_brl`) facilita achar sem
duplicar — sempre busque por `lookup_key` antes de criar (idempotência
manual, a API não tem "create or get").

## 2. Cupom/desconto por N meses

Duas formas, escolha pelo que o negócio pede:

- **`percent_off`** — desconto proporcional (ex.: 20% off), simples mas
  sofre arredondamento quando o valor final precisa ser exato.
- **`amount_off`** — desconto em valor fixo, na MESMA moeda do price
  (`currency` obrigatório no cupom). Preferir quando o valor final final
  importa exatamente (ex.: "R$99,90/mês", calculado como `amount_off =
  preço_cheio - preço_com_desconto` em centavos).

```bash
curl -s https://api.stripe.com/v1/coupons -u "$KEY:" \
  -d name="Lançamento 3 meses" -d currency=brl -d amount_off=5010 \
  -d duration=repeating -d "duration_in_months"=3
```

`duration`: `once` (só a 1ª cobrança), `repeating` (N meses,
`duration_in_months` obrigatório) ou `forever` (desconto permanente —
raro, confirme com a dona antes de usar). Aplicar o cupom automaticamente
no Checkout: `discounts: [{coupon: <id>}]` na criação da Session (não dá
pra usar `discounts` E `allow_promotion_codes` juntos). Pra deixar o
CLIENTE digitar um código (promotion code) em vez de aplicar sozinho, crie
um `promotion_code` apontando pro coupon e use `allow_promotion_codes:
true` na Session, sem `discounts`.

**Cliente que já usou o desconto não pode usar de novo** — decisão igual à
Wiven (`discount_reused`, ver `docs/assinatura-e-afiliados.md` do repo
`trackeador-mvp`): a aplicação (não a Stripe) decide, ANTES de criar a
Checkout Session, se aquele e-mail já teve assinatura — só manda
`discounts` quando for cliente novo. A Stripe não tem conceito de "1 cupom
por cliente pra sempre" nativo pra isso.

## 3. Payment Link (com `_tkid` do AdsTrackeador)

Payment Link é uma URL fixa reutilizável (ao contrário da Checkout Session,
que é 1 URL por tentativa de compra) — útil pra botão estático numa página
ou bio, não pra fluxo com e-mail pré-preenchido dinâmico (aí use Checkout
Session, § 4).

```bash
curl -s https://api.stripe.com/v1/payment_links -u "$KEY:" \
  -d "line_items[0][price]"=<price_id> -d "line_items[0][quantity]"=1
```

Pra levar o `_tkid` do AdsTrackeador (atribuição de clique) até o webhook:
Payment Link aceita `?client_reference_id=<valor>` na própria URL
(ecoado de volta no evento `checkout.session.completed` como
`client_reference_id`) — bote o `_tkid` ali
(`window.Trackeador.getTrackingId()`, igual a qualquer outro checkout, ver
skill `trackeador` § "Como implementar o espelho"). `metadata` customizada
num Payment Link não é por-clique (é fixa do link inteiro) — pra metadata
variável por compra, use Checkout Session com `metadata` na criação, não
Payment Link.

## 4. Checkout Session (e-mail pré-preenchido)

```bash
curl -s https://api.stripe.com/v1/checkout/sessions -u "$KEY:" \
  -d mode=subscription \
  -d customer_email=<email> \
  -d "line_items[0][price]"=<price_id> -d "line_items[0][quantity]"=1 \
  -d success_url=https://app.exemplo.com/sucesso \
  -d cancel_url=https://app.exemplo.com/cancelado \
  -d "metadata[client_reference]"=<_tkid ou ref de afiliado>
```

`customer_email` pré-preenche e trava o campo (cliente não pode trocar na
tela) — se precisar permitir edição, use `customer_creation: always` sem
`customer_email` e deixe o cliente digitar. Resposta trae `url` — redirecione
o navegador pra lá (nunca tente desenhar o checkout você mesmo; é hospedado
pela Stripe).

## 5. Portal do cliente (trocar cartão, ver faturas, cancelar)

Precisa de `customer` (id do Customer da Stripe, gravado no seu banco a
partir do `checkout.session.completed`):

```bash
curl -s https://api.stripe.com/v1/billing_portal/sessions -u "$KEY:" \
  -d customer=<customer_id> -d return_url=https://app.exemplo.com/assinatura
```

Resposta tem `url`, válida por uma sessão só — gere uma nova a cada clique
do cliente, nunca reutilize/guarde a URL.

## 6. Webhook (eventos e segredo)

Cadastro: Dashboard → Developers → Webhooks → "Add endpoint" (ou API
`POST /v1/webhook_endpoints`, mas o painel mostra o **signing secret** só
uma vez na criação — prefira o painel pra esta etapa específica). Eventos
mínimos pra assinatura recorrente:

- `checkout.session.completed` — 1ª ativação.
- `invoice.paid` — renovação mensal (cobrança seguinte).
- `invoice.payment_failed` — pagamento falhou (vira "past_due").
- `customer.subscription.updated` — mudança de status (ex.: `past_due`,
  `unpaid`).
- `customer.subscription.deleted` — cancelamento efetivo.
- `charge.refunded` — estorno.
- `charge.dispute.created` — chargeback/disputa.

Verificação da assinatura: header `Stripe-Signature` é
`t=<timestamp>,v1=<hmac>` — HMAC-SHA256(signing_secret,
`${t}.${body_bruto}`) tem que bater, em tempo constante, e o timestamp não
pode ser mais velho que ~5min (anti-replay). **Sempre leia o BODY BRUTO**
(nunca `req.json()` antes de verificar) — reserializar o JSON muda o hash.
Implementação de referência (sem SDK): `web/lib/stripe-signature.ts` no
repo `trackeador-mvp`.

**Produto novo → já cadastrar no webhook do AdsTrackeador no MESMO dia**
(mesma regra da Wiven, § acima dela): se o produto Stripe alimenta uma
oferta rastreada pelo AdsTrackeador, cadastre a conexão de checkout
(`adstrackeador checkout create` ou painel) e o webhook da Stripe pra ela
ANTES de divulgar o link — produto sem webhook cadastrado não gera venda
rastreada nenhuma, sem erro visível em lugar nenhum (mesmo padrão de falha
silenciosa da Wiven).

## 7. Reembolso

```bash
curl -s https://api.stripe.com/v1/refunds -u "$KEY:" -d payment_intent=<pi_...>
```

Reembolso dispara `charge.refunded` no webhook — do lado do AdsTrackeador,
isso cancela só a comissão de afiliado DAQUELE pagamento (nunca todas do
indicado), igual à Wiven.

## Métodos de pagamento no Brasil — A CONFIRMAR

Pix e boleto funcionam bem pra cobrança ÚNICA na Stripe Brasil. Pra
cobrança RECORRENTE (assinatura), cartão é o método maduro; Pix/boleto
recorrente dependem de recursos mais novos da Stripe (ex.: "Pix" como
método em invoice recorrente) cuja disponibilidade PRECISA ser confirmada
dentro da conta "AdsTrackeador" específica (Dashboard → Settings → Payment
methods) — não documentado aqui como fato até alguém logar e ver. Ao
confirmar, atualize esta seção com o que REALMENTE está disponível nesta
conta, não o que a doc geral da Stripe promete.

## Regras

1. **Nunca modo LIVE sem autorização explícita da dona.** Toda receita
   acima usa a chave de TESTE por padrão; trocar pra `sk_live_`/`rk_live_`
   em qualquer script ou chamada exige pedido direto dela, nunca decisão
   do agente. `scripts/stripe-setup-test.mjs` (repo `trackeador-mvp`)
   recusa rodar com chave que não comece com `sk_test_`/`rk_test_`.
2. **Nunca imprima a chave** (secret key, signing secret) em chat, log,
   commit ou README — só os últimos 4 caracteres se precisar confirmar
   qual está em uso. Mesma regra do resto do projeto (`AGENTS.md` do
   `trackeador-mvp` § segredos).
3. **Nome de produto/preço sem valor embutido** (§ 1).
4. **Produto novo → cadastrar no webhook do AdsTrackeador no mesmo dia**
   (§ 6), se a oferta for rastreada por ele.
5. **Confirme a CONTA certa** (seletor do painel, ou a chave certa por
   `STRIPE_<CONTA>_...`) antes de qualquer ação — a organização Leadgo tem
   mais de uma conta Stripe.
