---
name: stripe-checkout
description: Opera as contas Stripe da dona (organizações LeadGo = pessoal e Winx = parceria Luciola; dashboard.stripe.com) por MCP oficial e CLI primeiro, API REST quando necessário e navegador como reserva — criar produto/preço (único ou recorrente, BRL/USD/EUR), cupom/desconto por N meses, Payment Link, Checkout Session, portal do cliente, webhook, reembolso. Use quando o usuário pedir para criar produto/preço na Stripe, checkout Stripe, assinatura Stripe, cupom de desconto Stripe, Payment Link, webhook Stripe, ou mencionar cobrança/pagamento via Stripe.
---

> **REGRA FIXA DA DONA (10/11/2026), vale em TODO checkout:** (1) order bump **"Upgrade Básico → Completo"** obrigatório no checkout do Básico (1º bump, produto próprio, libera o Completo); (2) **ofertas de membro** criadas neste gateway para tudo que a pessoa ainda não tem (internacional 50% off, piso 2,90; Brasil 30% off, piso R$ 9,90, preços BR de sempre; nome "<item> - Área de Membros", redirect `/painel`); (3) upsell/app no topo da área de membros (internacional: 30% abaixo do upsell pós-compra + 2 dias grátis; Brasil: preço de sempre) (Stripe; sem Stripe, este mesmo checkout). Tudo nos 2 webhooks (entrega + Trackeador). Regra completa: `area-membros-netflix` › REGRA FIXA 10/11/2026.


> **PERFIL `stripe` PERSISTENTE — NUNCA "SAIR" (dona, 01/11/2026):** a Stripe é operada SÓ pelo perfil de navegador `stripe` (porta **9299**, `~/.agent-profiles/stripe/`), logado pela dona. Pode FECHAR o navegador normalmente (fechar janela/`browsers.sh`) — o que NUNCA se faz é clicar em "Sair"/logout, apagar a pasta do perfil, limpar cookies ou usar outro perfil pra Stripe. TESTADO 01/11/2026: dona logou → navegador fechado normalmente (CDP `Browser.close`) → reaberto com `browsers.sh stripe` → voltou LOGADO direto no dashboard. Então fechar é seguro; o deslogue anterior foi alguém clicar em "Sair" (ou matar o processo à força). Fechar sempre de forma limpa (`Browser.close`), nunca `pkill`/`kill -9` no Chromium desse perfil. 2FA é chave de segurança/biometria: agente NÃO reloga sozinho. Antes de agir: subir o perfil e conferir `curl -s localhost:9299/json` → aba em `dashboard.stripe.com/...` (não `/login`). Caiu em login → PARAR e avisar a dona. Um pane por vez no perfil.

# stripe-checkout

## Organização e conta — fatos conferidos em 10/11/2026

> **REGRA DA DONA (10/11/2026) — ORGANIZAÇÃO POR SÓCIO. Esta regra vale sobre o texto abaixo.**
> - **Winx** = organização Stripe existente, criada pela dona, para **tudo que é parceria com a Luciola** (ex.: Calendrier Magique FR, Calendário Mágico AR e qualquer oferta "Lua + Luciola"). Produto, preço, assinatura e webhook dessas ofertas são criados **dentro da Winx**, na conta existente indicada pela dona; não criar outra conta por oferta automaticamente.
> - **LeadGo** = coisas pessoais da dona (LeadGo, AdsTrackeador e o que não for parceria). Nada da parceria Luciola vai pra LeadGo.
> - Antes de criar algo: conferir o dono da oferta em `OFERTAS/<slug>/CLAUDE.md` (linha "Donas") e escolher a organização. Dúvida = perguntar à dona.
> - Se a Winx ainda não aparecer no seletor de contas/organizações do perfil `stripe`, **não criar conta avulsa no lugar**: parar e avisar a dona.
> - Variáveis: `STRIPE_WINX_<CONTA>_...` para contas da Winx.

**Winx existe** (`org_6VjhbL1n9Pw4udAS6hP97zs`). Em 10/11/2026, o painel de organização mostrou uma conta: **Calendrier Magique**, Brasil, ativada, `acct_1UaIGiABfkUzod1X`. A dona mandou usar por padrão a conta já configurada e criar o produto Guide Tarot nela; se quiser outra, ela avisa. Não renomear a conta nem criar uma por oferta. A conta LeadGo e a AdsTrackeador continuam separadas. Conferir a conta efetiva em cada credencial/conexão antes de escrever.

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

### Caso real — Guide Tarot FR, conta Winx (verificar de novo antes de escrever)
- Oferta `luciola-guidetarot-fr`: Product live `prod_VbZvtyqHcgx67d`, Price Essentielle live `price_1UaMlxABfkUzod1XM8beaURz` = EUR 790, avulso; conferidos pelo MCP em 10/11/2026. **MCP ativo**, contexto `acct_1UaIGiABfkUzod1X` live. **CLI 1.55.10 reautenticada em 11/11/2026**: perfil `winx-calendrier` = live active; **perfil separado `winx-calendrier-test` = sandbox active** na mesma conta, sem alterar o live. Procedimento em `references/ACESSO-MCP-CLI.md`.
- Conta BR: cartão e Apple Pay ligados, Google Pay indisponível/desligado na configuração consultada; PayPal pela Stripe indisponível para empresa BR; nenhum domínio de carteira registrado na consulta anterior. Rechecar no ambiente da conta antes de publicar. Meio que não puder ser reutilizado oferece novo pagamento no upsell.
- Em 11/11/2026, a dona confirmou **Essentielle €5,90, Complète €12,90, popup Básico→Completo €7,90 como preço total**, garantia 15 dias e preços com IVA incluído. Bump adicional fica para depois. Product live `prod_VbZvtyqHcgx67d`; Prices live com `tax_behavior=inclusive`: Básico `price_1UadjZABfkUzod1XVhsRLcBz` (default), Completo `price_1UadjeABfkUzod1X2Z4esWRu`, popup `price_1UadjiABfkUzod1X8dV2CeXJ`. Price inicial `price_1UaMlxABfkUzod1XM8beaURz` arquivado por estar sem comportamento fiscal e não ser mais o Básico. Sandbox separado: Product `prod_VbrU18hVpmTe10`, Prices `price_1UadlrABfkUzod1XMLNsHGpg` / `price_1UadlsABfkUzod1XimDUUF2D` / `price_1UadltABfkUzod1Xe6jVJ2O7` na mesma ordem.
- A CLI live retornou **“Stripe Tax isn't yet supported for your country”** ao ler Tax Settings e registrations da conta BR. O flag inclusivo conserva o preço final mas não configura cálculo/recolhimento automático. PayPal direto em conta própria pode receber pagamentos internacionais segundo o acordo PayPal BR, mas a conta/conexão PayPal da parceria ainda não foi fornecida e Stripe não processa PayPal nesta conta BR. O código/backend e a entrega pertencem à Luciola e ainda não estão nesta pasta. Preço do Lenormand pós-compra pendente. Não apontar CTAs públicos ao checkout novo até integrar, resolver taxação e provar os dois webhooks.

### PayPal separado — ferramentas verificadas em 11/11/2026
- Existe [MCP oficial do PayPal](https://developer.paypal.com/ai-tools/mcp-server/): remoto `https://mcp.paypal.com/http` (produção) / `https://mcp.sandbox.paypal.com/http` (teste), com login/consentimento, ou local `npx -y @paypal/mcp --tools=all` com `PAYPAL_ACCESS_TOKEN` e `PAYPAL_ENVIRONMENT`. **Ainda não está conectado nesta sessão.** Não confundir o pacote que inicia um servidor MCP com uma CLI independente para a operação do comerciante.
- Não foi localizada uma CLI oficial independente do PayPal nas fontes oficiais consultadas. Para operações sem MCP, usar a [REST API oficial](https://developer.paypal.com/api/rest) via cURL/SDK com token OAuth, separando sandbox de produção e guardando client ID/secret fora do repositório. O PayPal Business e as credenciais do app precisam existir antes de autenticar; apenas o e-mail da dona não concede acesso.
- Perfil local `paypal-dona-leadgo` (9315), e-mail e senha nas variáveis `PAYPAL_DONA_LEADGO_EMAIL` e `PAYPAL_DONA_LEADGO_PASSWORD` do cofre da máquina; a senha foi fornecida pela dona. **Login ainda não confirmado:** PayPal manteve o desafio por e-mail após envio do código. Esse perfil Dona/LeadGo não define por si só qual recebedor será usado na parceria Winx/Luciola. Fatos em `_memoria/contas-e-codigos.md`.

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
   `STRIPE_<CONTA>_...`) antes de qualquer ação — a organização Leadgo tem
   mais de uma conta Stripe.


## Padrão de checkout da casa (dona, 10/11/2026) — vale neste gateway
- **Timer:** 10 min, regressivo, **reinicia em 10:00 sempre que a pessoa entra de novo/recarrega** (sem prazo fixo, sem memória). Texto: "Discount available for a limited time only" traduzido pro idioma do mercado. Configure o contador do gateway assim; se o gateway não reiniciar por visita, avise a dona.
- **Garantia sempre igual ao produto:** Brasil 7 dias · internacional 15 dias. Conferir no produto, no checkout e no selo.
- **Entrega:** "Acesso imediato por e-mail".
- **Banner:** gerado por `banner-checkout-gpt` (seta pequena pra baixo no rodapé da imagem, título, garantia, acesso imediato por e-mail, vitalício).
- **Confiança:** ícone preto + texto (Privacidade · Compra segura · Conteúdo aprovado) quando o gateway permitir bloco/HTML na página; o estilo azul com cards é só do Hotmart; visual-base em `MODELOS/checkout-base/index.html`.
