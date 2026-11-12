# Modelo internacional "Hotmart adaptado" — passo a passo para uma oferta nova

Modelo pronto em `modelos/checkout-internacional-hotmart/` (README lá = o que ele entrega e as regras da casa). Instâncias ficam em `OFERTAS/<slug>/checkout/`. Este arquivo é o roteiro de uso; o roteiro geral de Stripe (organização, conta, PayPal, testes) é `ROTEIRO-NOVO-CHECKOUT.md`.

## Quando usar
Checkout **próprio** com Stripe + PayPal vendendo em **vários países** (idioma e moeda por país). Um país só, gateway nacional: `modelos/checkout-base/`.

**Estado em 11/11/2026 (provado no ar):** o modelo tem os DOIS checkouts — **Checkout Premium Internacional — modelo Hotmart com Stripe, cartão pelo link** (`public/stripe.html`, rota `/stripe`, **padrão**; formas de pagar depois dos bumps) e **Checkout Premium Internacional — modelo Hotmart, pagamento na própria página** (`public/index.html`, rota `/`). As duas salvam o cartão para o **upsell de 1 clique** (cobrança off-session testada). Rodam em **Cloudflare** (deploy real provado: domínio próprio, D1, webhook real, cartão/recusa/reembolso/redirect/PayPal), **Coolify** ou qualquer **Docker** (`Dockerfile`). Entrega à área de membros e espelho do Trackeador já saem do núcleo quando as variáveis existem (`AGENTS.md` §1c do modelo). Publicar na Cloudflare: `AGENTS.md` §1 do modelo, passo a passo. Falta em cada oferta: rota de entrega no site, conexão `generic` no Trackeador, página do upsell.

**Ficha de integração:** `modelos/checkout-internacional-hotmart/docs/FICHA-INTEGRACAO.md` — pergunta de abertura única; organização, conta, produto, preços e PayPal já cadastrados = só pedir os IDs/nomes de variável e integrar.

**PASSO 0 (OBRIGATÓRIO) — PERGUNTAR ONDE VAI HOSPEDAR, nunca assumir (ordem da dona, 11/11/2026):** quando alguém pedir o checkout internacional com Stripe, antes de copiar o modelo pergunte com `AskUserQuestion`: **"Onde o checkout vai rodar?"** — (a) **Cloudflare (Workers + D1)**: para quem só tem Cloudflare; (b) **Coolify / Node**: para quem usa Coolify (a dona). O mesmo núcleo (`src/core.mjs`) serve aos dois; a resposta define só qual entrada usar (`src/worker.mjs` + `cloudflare.config.ts`, ou `server.mjs`) e como publicar. Se for Cloudflare: conferir `cf auth whoami` (conta do cliente, nunca a de outro) e pedir o login ao usuário. Se for Coolify: domínio atrás do Cloudflare para o país vir em `CF-IPCountry`, `PUBLIC_URL` e volume persistente em `DATA_DIR`.

## Hospedagem (decisão da dona, 11/11/2026)
O modelo roda em **Coolify (Node)** ou **só Cloudflare (Workers + D1)**, com o mesmo núcleo (`src/core.mjs`). Parceiro que só tem Cloudflare usa o Worker; a dona usa Coolify. Detalhes e comandos no README do modelo (seção "Hospedagem"). Regra do `cf`: o projeto usa `cloudflare.config.ts`, então `cf dev`/`cf deploy` (não Wrangler). **Antes de publicar, `cf auth whoami` tem de mostrar a conta certa; a CLI desta máquina estava logada em conta de OUTRO cliente: nunca criar recurso nela, pedir à dona para fazer `! cf auth login --force`.**

## Passos
1. **Organização e conta:** seguir `ROTEIRO-NOVO-CHECKOUT.md` §0–§4 (uma conta Stripe por oferta, criada pela dona; PayPal Business confirmado; chaves de teste no cofre com nome da oferta, ex. `STRIPE_<OFERTA>_TEST_SECRET_KEY`).
2. **Copiar o modelo** para `OFERTAS/<slug>/checkout/` (sem `node_modules`, `data/`, `.dev.vars`; pasta é sincronizada) e `npm install`. Escolher a hospedagem: Coolify (`npm start`) ou Cloudflare (`npm run dev:cf` / `npm run deploy:cf`).
3. **Preços e produtos:** editar `catalog.mjs`: SKUs (planos, upgrade **aditivo**, bumps), valores por moeda aprovados pela dona, `compareAt`, `STRIPE_TEST_REFS` (Product/Prices criados na conta da oferta), mercados (`MARKETS`) e idiomas (`LANG_BY_COUNTRY`). Nome do Product leva o mercado (`<Produto> <MERCADO>`).
4. **Textos:** `public/i18n.js`: nome do produto, "Fórmula ...", nomes e descrições dos bumps nos 4 idiomas (conferir tradução com a dona), garantia (`{n}` dias: Brasil 7, internacional 15).
5. **Imagens:** `public/assets/img/` banner (gerado por `banner-checkout-gpt`, setinha no rodapé, título, garantia, acesso imediato), capa, miniaturas dos bumps. Logos de pagamento em `assets/pay/` (Google Pay colorido oficial; trocar por oficiais da marca antes de publicar).
6. **Depoimentos:** `public/data/testimonials.json` (`placeholder:true` até haver avaliações reais com autorização). Nunca inventar nome, número ou depoimento.
7. **Testar em sandbox** (README do modelo): `npm test`; `stripe listen --events payment_intent.succeeded,payment_intent.payment_failed,charge.refunded,checkout.session.completed,checkout.session.expired --forward-to localhost:4242/webhook --project-name <perfil>`; provar cartão aprovado, recusado, reembolso, webhook duplicado, valor adulterado, PayPal sandbox (criar pedido; a captura exige conta compradora sandbox).
8. **Antes do live (só com ordem da dona):** conta verificada, chave live (`ALLOW_LIVE=1` só com ordem), domínio HTTPS registrado na Stripe, Apple/Google Pay ligados na conta, webhooks de produção (entrega + Trackeador), entrega real (e-mail + área de membros), IVA tratado fora da Stripe se a conta for BR, depoimentos reais.
9. **Registrar** em `STATUS.md`/`INDICE.md` e fechar com `low-ticket-salvar`.

## Lições do primeiro uso (não repetir)
- **Só duas telas, sem versões numeradas** (dona, 11/11/2026): **Checkout Premium Internacional — modelo Hotmart com Stripe, cartão pelo link** (`/stripe`, **padrão**) e **Checkout Premium Internacional — modelo Hotmart, pagamento na própria página** (`/`). Ajuste = editar a própria tela; nada de `v2.html`, `v3.html`…
- A CLI do Stripe serve de backend de teste e entrega webhooks locais; as chaves de teste do sandbox estão no DOM da página de chaves (extrair sem imprimir, gravar no cofre). Clique por texto às vezes não pega no painel da Stripe: usar coordenada.
- Rolar a página para o botão de compra ao escolher a forma de pagamento escondia os campos do cartão: rolar para a linha escolhida.
- O botão de compra escondido não pode ocupar espaço (`display:none` até escolher).
- Imagem de depoimento/nome de outro produto não entra: é prova falsa. Contador de clientes e "avaliações" precisam refletir dado real antes de publicar.
