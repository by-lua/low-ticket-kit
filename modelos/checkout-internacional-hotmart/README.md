# Checkout Premium Internacional — Stripe + PayPal (modelo)

Modelo de **checkout próprio** para vender em vários países, com cartão (Stripe), Apple Pay, Google Pay e PayPal, **idioma e moeda mudando pelo país** (IP e seletor). Layout inspirado em checkouts de plataformas de infoproduto. Todos os dados (produto, preços, textos, imagens, depoimentos) são **exemplo**: troque pelos da sua oferta.

Para montar, testar e publicar a partir deste modelo: **`docs/FICHA-INTEGRACAO.md`** (o que perguntar e integrar quando Stripe, produto e PayPal já estão cadastrados), **`AGENTS.md`** (regras e comandos, vale para pessoas e agentes) e **`docs/HANDOFF.md`** (passo a passo e checklist de go-live).

## O que o modelo entrega
- **Tela** (`public/index.html` + `checkout.css` + `app.js`): barra de urgência 10:00 (sem memória) → banner largo arredondado alinhado ao card estreito → seletor de país com busca → produto (capa, nome, fórmula, preço) → e-mail → **forma de pagamento** (cartão de débito/crédito, Apple Pay, Google Pay, PayPal) → **bumps** (borda dourada, desconto, "Adicionar produto"; upgrade **aditivo** primeiro) → detalhes da compra → botão de compra (aparece depois de escolher cartão ou PayPal; a carteira usa o botão dela) → garantias → prova social → "Protegido por Stripe".
- **Os dois checkouts:** **Checkout Premium Internacional — modelo Hotmart, pagamento na própria página** (`/`, `index.html`, descrito acima) e **Checkout Premium Internacional — modelo Hotmart com Stripe, cartão pelo link** — o padrão (`/stripe`, `stripe.html` + `stripe.css` + `app-stripe.js`): e-mail → bumps → forma de pagar → detalhes → botão, visual dourado próprio; cartão/Apple Pay/Google Pay/Link pagos na página segura da Stripe (Checkout Session) e um bloco de 3 passos mostra ao comprador para onde ele vai.
- **Núcleo único** (`src/core.mjs`, padrão Web `Request → Response`, sem `node:*`): total calculado no servidor (`catalog.mjs`); um PaymentIntent (incorporado) ou uma Checkout Session (redirecionamento) por clique de compra, idempotente; webhook Stripe assinado e idempotente (libera, confere valor/moeda, revoga em reembolso); PayPal (criar pedido → aprovar → capturar no servidor); país/idioma/moeda por `CF-IPCountry` (ou `request.cf.country`) ou `?pays=XX`; **entrega** assinada para a área de membros (`DELIVERY_WEBHOOK_URL`) e **espelho no Trackeador** (`TRACKEADOR_WEBHOOK_URL`) com papel front/bump de cada item, os dois sem travar a venda, com reenvio por `POST /api/admin/resend`; **recusa chave live** sem `ALLOW_LIVE=1`.
- **Três jeitos de hospedar**, mesmo núcleo: **Coolify ou qualquer Docker** (`Dockerfile`, `server.mjs` + `src/store-file.mjs`) e **Cloudflare Workers + D1** (`src/worker.mjs` + `src/store-d1.mjs` + `cloudflare.config.ts` + `vite.config.ts`).
- **Idiomas** (`public/i18n.js`): fr, en, es, pt; nomes de país no idioma da tela. Só a interface é traduzida.
- **Moedas** (`catalog.mjs`): EUR, CHF, CAD (exemplo); qualquer outro país cai em EUR.
- **Testes**: `npm test` (26: catálogo + núcleo contra o armazenamento em arquivo e contra um D1 simulado).

## Regras embutidas
1. Ordem da tela: e-mail → forma de pagamento → bumps → detalhes → comprar. Cobrança criada **uma vez**, no clique de comprar.
2. **Upgrade aditivo**: plano + upgrade = plano completo com desconto (ex.: 5,90 + 2,00 = 7,90). Nunca substitui o preço do plano.
3. **Sem notificação de compra falsa** nem contador/depoimento inventado em produção. Os depoimentos de exemplo estão marcados `placeholder` e só aparecem em modo de teste.
4. Bumps em amarelo/dourado; botão de compra verde; ícones das formas de pagamento no mesmo tamanho.
5. Ao escolher a forma de pagamento a tela não pula para o botão: alinha a linha escolhida e o formulário fica visível. Sem espaço vazio antes da escolha.
6. **Só duas telas, sem versões numeradas** (dona, 11/11/2026): **Checkout Premium Internacional — modelo Hotmart com Stripe, cartão pelo link** (`/stripe`, **padrão**) e **Checkout Premium Internacional — modelo Hotmart, pagamento na própria página** (`/`). Ajuste = editar a própria tela; nada de `v2.html`, `v3.html`…

## Hospedagem
**Pergunte onde vai hospedar (Cloudflare, Coolify ou outro Docker/Node) antes de montar; não assuma.**
- **Coolify / Docker / Node:** Build Pack Dockerfile (porta 4242, volume em `/data`, health em `/api/health`) ou `npm start`; `env.example` é a lista de variáveis. `PUBLIC_URL` = domínio do checkout; domínio atrás do Cloudflare para o país vir em `CF-IPCountry`; `DATA_DIR` num volume persistente (para produção, troque o arquivo por Postgres/SQLite).
- **Cloudflare Workers:** `npm install`; `cp .dev.vars.example .dev.vars` (chaves de TESTE); `npm run dev:cf` (usa `cf dev`, local, sem login; no Node < 22.18 o script já passa `--experimental-strip-types`). Para publicar: a conta logada tem de ser a do cliente (`cf auth whoami`), criar o D1 e preencher o `id` em `bindings.d1`, subir os segredos, `npm run deploy:cf`, rota/domínio. O esquema do D1 também se cria sozinho no primeiro uso (`migrations/0001_init.sql` é o mesmo).

## Estado de verificação
Provado em teste (11/11/2026): Node (cobrança + webhook + PayPal sandbox + estáticos); **imagem Docker** construída e rodando (health `healthy`, PaymentIntent e Checkout Session reais no sandbox, volume `/data`); Worker local em workerd com D1 local (contexto CH→CHF, PaymentIntent, Checkout Session, pedido gravado no D1, telas). Testes cobrem entrega assinada, espelho do Trackeador, reembolso, receptor fora do ar e reenvio.
**Deploy real na Cloudflare provado em 11/11/2026** (conta própria, domínio próprio, D1 criado no deploy, webhook Stripe real): cartão aprovado/recusado, reembolso, Checkout Session paga na página da Stripe e devolvida ao `/merci`, PayPal sandbox criando pedido. **Não provado:** captura PayPal com conta compradora sandbox; Apple/Google Pay (precisam HTTPS + domínio registrado + carteira no aparelho); upsell de um clique (o cartão já é salvo com consentimento, mas não há página de upsell); a rota de entrega no site de cada oferta e a conexão real do Trackeador; IVA por país; logos de pagamento oficiais (os atuais vêm do pacote `simple-icons` e de um ativo público do Google Pay: troque pelos oficiais antes de publicar).

## Imagens e marcas
`public/assets/img/` tem **placeholders** (banner 1024×576, capa e miniaturas de bump): substitua pela arte da oferta e pelo favicon (`favicon.svg`, `favicon.ico`, `apple-touch-icon.png`). Bandeiras: `flag-icons` (MIT). Fontes: Open Sans, Libre Baskerville, Inter e Cormorant Garamond (SIL OFL). Os logos de Apple Pay, Google Pay, PayPal, Visa, Mastercard e Stripe são marcas de seus donos: siga as regras de uso de cada marca.
