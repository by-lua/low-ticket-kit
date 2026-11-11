---
name: stripe-checkout
description: Opera contas Stripe (e PayPal) das ofertas LOW-TICKET por MCP oficial e CLI primeiro, API REST quando necessário e navegador como reserva — criar produto/preço (único ou recorrente, qualquer moeda), cupom, Payment Link, Checkout Session, checkout próprio (PaymentIntent), portal do cliente, webhook, reembolso. Contém o roteiro e o modelo de checkout internacional (Cloudflare ou Coolify). Use quando pedirem produto/preço na Stripe, checkout Stripe, assinatura, cupom, Payment Link, webhook, cobrança via Stripe ou o checkout internacional com Stripe e PayPal.
---

> **REGRA FIXA DA DONA (10/11/2026), vale em TODO checkout:** (1) order bump **"Upgrade Básico → Completo"** obrigatório no checkout do Básico (1º bump, produto próprio, libera o Completo); (2) **ofertas de membro** criadas neste gateway para tudo que a pessoa ainda não tem (internacional 50% off, piso 2,90; Brasil 30% off, piso R$ 9,90, preços BR de sempre; nome "<item> - Área de Membros", redirect `/painel`); (3) upsell/app no topo da área de membros (internacional: 30% abaixo do upsell pós-compra + 2 dias grátis; Brasil: preço de sempre) (Stripe; sem Stripe, este mesmo checkout). Tudo nos 2 webhooks (entrega + Trackeador). Regra completa: `area-membros-netflix` › REGRA FIXA 10/11/2026.



# stripe-checkout

> **ROTEIRO DE PONTA A PONTA (dona, 11/11/2026): novo produto com checkout próprio → abrir [references/ROTEIRO-NOVO-CHECKOUT.md](references/ROTEIRO-NOVO-CHECKOUT.md) primeiro.** Regras fixas: (1) confirmar organização e conta da oferta antes de criar qualquer coisa; (2) formas de pagamento sempre ligadas: **cartão, Apple Pay, Google Pay e PayPal**, cada uma checada no ambiente real; (3) PayPal: **sempre confirmar qual conta PayPal recebe**, a cada oferta; (4) **uma conta Stripe por oferta**, criada pela dona na organização do sócio (o agente pede e não cria; produto de uma oferta nunca mora na conta de outra); (5) **Product por oferta e mercado, nome `<Produto> <MERCADO>`**: listar os existentes antes, criar se não houver, perguntar se houver dúvida, nunca assumir; (6) mercados, moedas e preços são decisão da dona, por oferta. **Modelo pronto internacional** (Stripe + PayPal, idioma/moeda por país; roda em Cloudflare Workers+D1 OU Coolify/Node — PERGUNTAR onde hospedar antes de montar): `MODELOS/checkout-internacional-hotmart/` + [references/MODELO-INTERNACIONAL-HOTMART.md](references/MODELO-INTERNACIONAL-HOTMART.md). Mapa com o `checkout-premium`: [references/MAPA-PREMIUM-x-STRIPE.md](references/MAPA-PREMIUM-x-STRIPE.md). **Fatos de conta, ID, e-mail e estado de cada oferta NÃO ficam nesta skill:** `_memoria/contas-e-codigos.md` → "Stripe e PayPal" e `OFERTAS/<slug>/STRIPE-PAYPAL.md`.

## Organização e conta — como decidir (genérico)

- **Uma conta Stripe por oferta**, criada pela dona dentro da organização do sócio da oferta; o agente **não cria conta**: pede à dona para criar e informar organização e nome da conta. Conta de outra oferta nunca recebe produto desta.
- Descobrir a organização pela ficha da oferta (`OFERTAS/<slug>/CLAUDE.md`, linha "Donas"). Dúvida = perguntar.
- **Antes de QUALQUER ação**, conferir conta e ambiente (`/v1/account` pela CLI/MCP, ou o seletor do painel): ação na conta errada afeta outro negócio.
- **Chaves de API são POR CONTA** (par test/live). No cofre da máquina use o nome da conta/oferta na variável (`STRIPE_<CONTA>_TEST_SECRET_KEY`), nunca nome genérico solto. Nunca imprimir chave. Modo live só com autorização explícita da dona.
- Fatos de cada conta (IDs, e-mails, perfis, variáveis, estado de verificação): `_memoria/contas-e-codigos.md` → "Stripe e PayPal"; fatos de cada oferta: `OFERTAS/<slug>/STRIPE-PAYPAL.md`.

## Acesso

Perfil de navegador do sistema reservado à Stripe, **nunca fazer logout** (fechar de forma limpa; login e 2FA são da dona; se cair em tela de login, parar e avisar). Credenciais só por variável do cofre, nunca literal. Perfil, porta e variáveis desta máquina: `_memoria/contas-e-codigos.md` → "Stripe e PayPal".

### Ordem de operação (dona, 10/11/2026)
1. **MCP oficial Stripe**, remoto `https://mcp.stripe.com`, OAuth, quando conectado à conta correta. Instalação e autenticação: [references/ACESSO-MCP-CLI.md](references/ACESSO-MCP-CLI.md).
2. **Stripe CLI**, perfil explícito por conta, para endpoints que o MCP não cobrir ou se o MCP ainda não estiver disponível. Conferir `/v1/account` antes de criar; usar o perfil correto em todo comando.
3. **API REST oficial**, quando adequada para código de servidor ou operação não coberta pelas ferramentas. Segredos só no servidor/cofre. Verificar conta e ambiente antes.
4. **Navegador/Playwright (perfil `stripe`) como reserva** para cadastro e para recursos exclusivos do painel, consentimento e 2FA. Nunca fazer logout. Não copiar tokens internos da sessão do dashboard.

A dona autorizou conectar MCP/CLI nesta retomada. Se o provedor pedir código do autenticador, pedir à dona e continuar apenas trabalho independente; não inventar código nem relogar com outro perfil. MCP registrado não significa OAuth concluído ou ferramentas disponíveis na sessão atual.

### Checkout próprio internacional + upsell
- Primeiro confirmar organização/conta e criar o **Product** sem duplicação. Depois criar **Prices** na moeda da oferta (EUR/USD/etc.) e montar o checkout próprio com os componentes oficiais da Stripe. Não converter moeda automaticamente.
- Checkout próprio é permitido e pedido pela dona. **Fluxo padrão para o modelo da casa:** Payment Element com **PaymentIntent adiado**; renderizar o formulário Stripe antes e criar o PaymentIntent somente no clique em comprar. Checkout Sessions com `ui_mode=elements` precisa de Session antes de inicializar o formulário e, portanto, não cumpre sozinha essa ordem da casa. Receita operacional e fontes: [references/CHECKOUT-PROPRIO-STRIPE.md](references/CHECKOUT-PROPRIO-STRIPE.md). Nunca coletar PAN/CVC em campos nossos.
- E-mail → bumps → pagamento → comprar; preço e itens são resolvidos no servidor. Criar pedido/PaymentIntent só no clique, uma vez por tentativa, com idempotência persistente. Total inclui bumps e upgrade aplicáveis à entrada. Atualizar `elements.update({amount})` quando o total mudar, antes de confirmar.
- Cartão + Apple Pay/Google Pay e demais métodos imediatos **disponíveis na conta/mercado**. Carteiras dependem do dispositivo, domínio e elegibilidade. PayPal processado pela Stripe não está disponível para a conta brasileira; integração PayPal separada exige conta/conexão própria. Não anunciar um método indisponível.
- Não habilitar boleto/voucher, parcelado ou meios de confirmação tardia neste checkout de entrada. Confirmação imediata de pagamento não significa repasse bancário imediato. Assinatura só para produto recorrente de fato.
- **Upsell 1 clique é obrigatório no desenho do funil** e exige salvar/reusar o método com consentimento desde a compra inicial. Procedimento único: `_skills/low-upsell-app/references/STRIPE-UPSELL-1-CLIQUE.md` (compra avulsa e assinatura, SCA, segurança e testes).
- Se o preço da oferta **já inclui IVA**, criar Price com `tax_behavior=inclusive` para impedir acréscimo ao valor exibido. Esse campo sozinho **não calcula, recolhe nem declara IVA**. Consultar Tax Settings/registrations da conta antes de prometer cálculo automático; se a API disser que Stripe Tax não é suportado no país, registrar o bloqueio e validar o tratamento fiscal por outro caminho antes de publicar. Nunca inventar cadastro tributário ou `tax_code`.
- Não chamar de pronto só porque existem Product/Price: precisa checkout + cobrança extra autorizada + fallback SCA + webhooks entrega/Trackeador provados. Valor indefinido não vira preço inventado.

- **Mapa premium × Stripe (11/11/2026):** divisão entre as skills, lacunas do premium, tracking e extras internacionais em [references/MAPA-PREMIUM-x-STRIPE.md](references/MAPA-PREMIUM-x-STRIPE.md). Cartão incorporado (Payment Element); preços por moeda no catálogo do servidor.

### Casos reais
Dados de cada oferta (conta, Product, Prices, PayPal personalizado, mercados e moedas) ficam em `OFERTAS/<slug>/STRIPE-PAYPAL.md`. 

### PayPal — opções (genérico)
- **PayPal nativo pela Stripe** só em países/contas elegíveis (não em conta brasileira).
- **PayPal como forma de pagamento personalizada na Stripe** (Elements + Payment Intents): criada no painel da conta (cada ambiente tem o seu `cpmt_...`); processamento é do PayPal. Só vale depois de provar o fluxo em sandbox.
- **PayPal separado** (plano B usado pelo modelo): app de desenvolvedor da conta Business que vai receber (credenciais sandbox e live separadas, no cofre), API de Orders (criar → aprovar → capturar no servidor) e webhook próprio. **Sempre confirmar qual conta PayPal recebe**, a cada oferta.
- Existe MCP oficial do PayPal; não há CLI oficial independente. PayPal **não entra no upsell de um clique** (assumir que não até provar).
- Contas, perfis, IDs e estado: `_memoria/contas-e-codigos.md` → "Stripe e PayPal" e `OFERTAS/<slug>/STRIPE-PAYPAL.md`.

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

`customer_email` pré-preenche o e-mail. Ao passar um Customer existente com e-mail válido, o Checkout usa esse e-mail; conferir comportamento na UI escolhida. Para checkout hospedado, usar `url`; para checkout próprio, inicializar os componentes oficiais com o `client_secret` da Session, conforme a integração vigente. O servidor nunca entrega sua chave secreta ao browser.

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

## Métodos de pagamento no Brasil — conferir na conta

A disponibilidade geral não é configuração desta oferta: Pix/boleto ficam fora do checkout internacional pedido. Cartão, Apple/Google Pay dependem das capacidades da conta e das condições do dispositivo/domínio. PayPal processado pela Stripe não é elegível na conta brasileira confirmada; ver fontes em `references/ACESSO-MCP-CLI.md`. Pra
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
   `STRIPE_<CONTA>_...`) antes de qualquer ação — uma organização pode ter
   mais de uma conta Stripe.


## Padrão de checkout da casa (dona, 10/11/2026) — vale neste gateway
- **Timer:** 10 min, regressivo, **reinicia em 10:00 sempre que a pessoa entra de novo/recarrega** (sem prazo fixo, sem memória). Texto: "Discount available for a limited time only" traduzido pro idioma do mercado. Configure o contador do gateway assim; se o gateway não reiniciar por visita, avise a dona.
- **Garantia sempre igual ao produto:** Brasil 7 dias · internacional 15 dias. Conferir no produto, no checkout e no selo.
- **Entrega:** "Acesso imediato por e-mail".
- **Banner:** gerado por `banner-checkout-gpt` (seta pequena pra baixo no rodapé da imagem, título, garantia, acesso imediato por e-mail, vitalício).
- **Confiança:** ícone preto + texto (Privacidade · Compra segura · Conteúdo aprovado) quando o gateway permitir bloco/HTML na página; o estilo azul com cards é só do Hotmart; visual-base em `MODELOS/checkout-base/index.html`.
