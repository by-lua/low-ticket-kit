# AGENTS.md — Checkout Premium Internacional (Stripe + PayPal)

Instruções para qualquer agente de código (Codex, Claude Code, etc.) e para pessoas que forem montar um checkout a partir deste modelo. Leia também `README.md` (o que o modelo entrega) e `docs/HANDOFF.md` (passo a passo de entrega e go-live).

Este repositório é **modelo**: não contém segredo, conta, ID, e-mail nem oferta real. Todos os nomes, preços, textos, imagens e depoimentos são **exemplo**. Nunca commite chaves, `.dev.vars`, `.env`, `data/` nem `node_modules/`.

## 0. Antes de tudo: PERGUNTAR o que já existe (`docs/FICHA-INTEGRACAO.md`)
Mande a "pergunta de abertura" da ficha numa mensagem só (hospedagem, Stripe, PayPal, oferta, entrega, visual, qual tela). **O que já está cadastrado (organização, conta Stripe, produto, preços, PayPal, domínio) o agente só integra**: recebe os IDs e os NOMES das variáveis do cofre, confere pela API e liga. Só cria o que faltar, e só depois do ok. Segredo nunca no chat.

## 1. PERGUNTAR onde vai hospedar (não assuma)
Pergunte ao usuário: **"O checkout vai rodar na Cloudflare, em Coolify, ou em outro servidor com Docker/Node?"** Os três usam o mesmo núcleo `src/core.mjs` e passam nos mesmos testes.
- **Cloudflare (Workers + D1):** `src/worker.mjs` + `cloudflare.config.ts` + `vite.config.ts`. Local: `cp .dev.vars.example .dev.vars` e `npm run dev:cf` (sem login; roda no `workerd` com D1 local). País vem sozinho em `cf.country`. **Publicar (provado em 11/11/2026):**
  1. `npx cf auth whoami` tem de mostrar a conta DO DONO (nunca criar recurso em conta de outra pessoa). Node 22.18+ ou `NODE_OPTIONS='--experimental-strip-types'`.
  2. Em `cloudflare.config.ts`: `name` da oferta e `domains: ["checkout-<oferta>.<dominio-do-dono>"]` (subdomínio novo numa zona da conta; confira antes com `dig` que ele não existe) e `workersDev: false`. Sem domínio, a conta precisa de subdomínio workers.dev registrado no painel. O D1 é criado sozinho no primeiro deploy.
  3. Arquivo de segredos FORA do projeto (`chmod 600`), formato `.env`, com todos os `bindings.secret()` declarados (segredo declarado é obrigatório; os opcionais ficam comentados até existirem). `npx cf deploy --secrets-file <arquivo>`. Apague o arquivo depois.
  4. Cadastre o webhook da Stripe para `https://<domínio>/webhook` (eventos da seção 5), pegue o `whsec_` e rode o deploy de novo com ele no arquivo. No mesmo passo, registre o domínio para as carteiras (`stripe.paymentMethodDomains.create({ domain_name })`, conferir `apple_pay`/`google_pay` = `active`): **uma vez por domínio, por conta Stripe e por modo** (teste e live). Só o Checkout Hotmart (carteira na nossa página) precisa; o Checkout Stripe não. Confira também se o Google Pay está ligado na configuração de formas de pagamento da conta (`paymentMethodConfigurations`, `google_pay` = `on`): conta nova pode vir com ele desligado.
  5. Prove no domínio publicado: `/api/health`, cartão de teste → pedido `paid`, reembolso → `refunded`, recusado → `failed`, `/stripe` pagando na página da Stripe → volta em `/merci` e pedido `paid`, PayPal devolve link de aprovação.
- **Coolify:** Build Pack **Dockerfile** (já está no repositório), porta 4242, armazenamento persistente montado em `/data`, variáveis de `env.example` em Environment Variables. Health check pronto em `/api/health`. Ponha o domínio atrás do proxy da Cloudflare para o país vir em `CF-IPCountry` (sem isso cai em FR/EUR e o seletor de país resolve).
- **Outro servidor (VPS, Railway, Render, Fly…):** o mesmo `Dockerfile` (`docker run -p 4242:4242 --env-file .env -v checkout-data:/data …`) ou `node server.mjs` com Node 22.
- **Uma instância por oferta** (uma conta Stripe por oferta). `DATA_DIR` guarda pedidos em arquivo: um container só, nunca escalar para várias réplicas com o mesmo volume.

## 1b. Os dois checkouts (os dois prontos; padrão = cartão pelo link, dona 11/11/2026)
- **Checkout Premium Internacional — modelo Hotmart, pagamento na própria página** (`/`, `public/index.html` + `app.js`): cartão dentro da página (Stripe Payment Element), Apple/Google Pay pelo Express Checkout. Visual "Hotmart". Cobra por `POST /api/intent`.
- **Checkout Premium Internacional — modelo Hotmart com Stripe, cartão pelo link** — o PADRÃO (`/stripe`; os botões da página de vendas apontam para cá; `public/stripe.html` + `app-stripe.js` + `stripe.css`): ordem e-mail → bumps → forma de pagar → detalhes → botão; cartão, Apple Pay, Google Pay e Link são pagos na página segura da Stripe (Checkout Session, `POST /api/session`). Menos código no navegador, Apple/Google Pay sem registrar domínio. Mostra ao comprador os 3 passos do que acontece depois do clique.
- PayPal é igual nas duas (`/api/paypal/order` → aprovação no PayPal → captura no servidor). Nas duas o cartão fica salvo com consentimento para o upsell de um clique.

## 1c. Entrega e Trackeador (fazer em toda oferta)
Quando a venda é confirmada (webhook assinado da Stripe ou captura do PayPal), o servidor envia, sem travar a venda (timeout 3 s):
1. **Entrega para a área de membros:** `POST DELIVERY_WEBHOOK_URL` com `{event:"order.paid"|"order.refunded", order_id, email, entitlements[], items[{sku,name,role,amount}], currency, amount, paid_at, method, mode, offer}`. Cabeçalhos: `x-checkout-secret` (= `DELIVERY_WEBHOOK_SECRET`) e `x-checkout-signature` = HMAC-SHA256 do texto `${x-checkout-timestamp}.${corpo}`. **No site da oferta**, crie essa rota igual à do webhook do gateway que ele já tem: confere o segredo, é idempotente por `order_id`, libera exatamente os `entitlements` (SKUs) no `/painel`, manda o e-mail de acesso e revoga no `order.refunded`.
2. **Trackeador:** `POST TRACKEADOR_WEBHOOK_URL` (conexão própria com gateway `generic`, `.../api/webhooks/sale/c/<id>`) com o payload canônico do espelho (`transaction_id`, `status`, `amount`, `currency`, `buyer.email`, `tracking_id` = o `_tkid` capturado na página, `approved_at`) e `items[]` com `role` front/bump/upsell. Cabeçalho `x-trackeador-secret`. Validar: `trackeador events --type sale_paid --tracking <tkid>` com `ATRIB. = sim`.
- Sem as variáveis, nada é enviado e a venda continua valendo (só fica no log `deliveries`). Falha de envio vai para o log `notify-failed`; depois de corrigir o receptor, reenvie com `POST /api/admin/resend?id=<pedido>` e `Authorization: Bearer <ADMIN_TOKEN>`.

## 2. Regras que não se negociam
1. **O preço nunca vem do navegador.** O total é calculado no servidor a partir de `catalog.mjs` (`quote()`); valor adulterado é recusado.
2. **Uma cobrança só, no clique de comprar** (PaymentIntent idempotente por pedido + carrinho). Escolher forma de pagamento ou marcar bump só atualiza a tela.
3. **Entrega só pelo webhook assinado da Stripe ou pela captura no servidor do PayPal**, nunca pela página de retorno. Webhook idempotente, confere valor e moeda, reembolso revoga.
4. **Modo teste por padrão.** O servidor recusa chave `sk_live`/`rk_live` a menos que `ALLOW_LIVE=1`. Chave live só com ordem explícita do dono da conta.
5. **Upgrade é aditivo** (plano + upgrade = plano completo com desconto); nunca substitui o preço do plano.
6. **Sem prova social falsa:** nada de "fulano acabou de comprar", de contador de clientes inventado ou de depoimento fictício em produção. `public/data/testimonials.json` vem com `placeholder: true` (só aparece em modo de teste); troque por avaliações reais autorizadas antes de publicar.
7. **Uma conta Stripe por oferta**, criada pelo dono da oferta; o agente pede e não cria. Confirme sempre a conta PayPal que vai receber.
8. **Só duas telas, sem versões numeradas** (dona, 11/11/2026): **Checkout Premium Internacional — modelo Hotmart com Stripe, cartão pelo link** (`/stripe`, **padrão**) e **Checkout Premium Internacional — modelo Hotmart, pagamento na própria página** (`/`). Ajuste = editar a própria tela; nada de `v2.html`, `v3.html`…
9. **Idioma e moeda mudam pelo país** (IP e seletor). Só a interface é traduzida; o conteúdo do produto fica no idioma original.

## 3. Mapa dos arquivos
- `catalog.mjs` — SKUs, preços por moeda (EUR/CHF/CAD de exemplo), país → moeda/idioma, `quote()`, upgrade aditivo.
- `src/core.mjs` — roteador Web (`Request → Response`): contexto, catálogo, cotação, PaymentIntent (`/api/intent`), Checkout Session (`/api/session`), PayPal (criar/capturar), webhook, entrega + Trackeador, reenvio, estáticos. Sem `node:*`.
- `src/store-file.mjs` (Node) e `src/store-d1.mjs` (Cloudflare D1; cria o esquema sozinho) — mesma interface.
- `server.mjs` (Node/Docker/Coolify) e `src/worker.mjs` (Workers) — entradas. `Dockerfile` + `.dockerignore` para Coolify/Docker.
- `public/index.html`, `checkout.css`, `app.js` (incorporado) · `stripe.html`, `stripe.css`, `app-stripe.js` (redirecionamento) · `i18n.js` (fr/en/es/pt), `merci.html` — as telas. Imagens em `public/assets/img/` são placeholders.
- `core.test.mjs`, `catalog.test.mjs` — `npm test` (26 testes; os de pedido rodam contra o arquivo e contra o D1 simulado).

## 4. Como adaptar a uma oferta
1. Copie este diretório para o projeto da oferta (sem `node_modules`, `data/`, `.dev.vars`).
2. `catalog.mjs`: SKUs, nomes, preços por moeda aprovados pelo dono, upgrade e bumps. Atualize os testes.
3. `public/i18n.js`: nome do produto, nomes e descrições dos bumps nos 4 idiomas (confira a tradução com o dono). Garantia em dias.
4. `public/assets/img/`: banner (1024×576), capa, miniaturas dos bumps, favicon (`favicon.svg/.ico`, `apple-touch-icon.png`).
5. Variáveis (veja `env.example` e `.dev.vars.example`): chaves de **teste** da Stripe e do PayPal, `OFFER_SLUG`, `OFFER_DESCRIPTION`, `BRAND`, `PUBLIC_URL`, e as da entrega/Trackeador (seção 1c).
6. `npm test` e depois os testes de ponta a ponta (seção 5).

## 5. Como testar (sandbox)
- Node: `npm install`, exporte as variáveis, `node server.mjs`; Cloudflare: `cp .dev.vars.example .dev.vars`, `npm run dev:cf`.
- Webhook local: `stripe listen --events payment_intent.succeeded,payment_intent.payment_failed,charge.refunded,checkout.session.completed,checkout.session.expired --forward-to localhost:<porta>/webhook`. Em produção, cadastre o endpoint `https://<domínio>/webhook` com esses mesmos eventos.
- Provar: cartão aprovado (`pm_card_visa`), recusado (`pm_card_chargeDeclined`), 3D Secure, reembolso (revoga), webhook duplicado, valor adulterado (400), PayPal sandbox (criar pedido; a captura exige conta compradora sandbox).
- Apple Pay / Google Pay só aparecem com HTTPS + domínio registrado na Stripe + carteira no aparelho.

## 6. O que NÃO está pronto (a fazer em cada oferta)
A rota de entrega no site da oferta (seção 1c) e a conexão do Trackeador, tratamento de IVA/impostos por país, páginas legais e aviso de cookies, domínio HTTPS, conta live verificada, depoimentos reais, página do upsell de um clique (o cartão já fica salvo), logos de pagamento oficiais, tradução revisada por nativo.

## 7. Segurança
Segredos só em variáveis de ambiente / segredos do Worker. Nunca imprima chave em log ou chat. Não coloque dado de cliente real no repositório.
