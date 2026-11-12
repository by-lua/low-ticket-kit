# Ficha de integração — o que o agente PEDE antes de montar

Objetivo: quando alguém disser "monta o Checkout Premium Internacional da oferta X", o agente **não sai criando nada**. Primeiro pergunta, numa mensagem só, o que já existe. Se a pessoa já cadastrou tudo (organização, conta Stripe, produto, preços, PayPal, domínio), o agente **só integra**: recebe os dados, liga e testa. Só cria o que faltar, e só depois de perguntar.

## Envelope de segredos (cada pessoa, o seu — separado do kit)
Cada pessoa guarda as PRÓPRIAS chaves num arquivo só dela, fora do kit e fora do projeto: `~/.config/low-ticket-kit/segredos/<oferta>.env` (`chmod 600`). Ela mesma cola os valores lá; ninguém mais vê.
- O kit, as skills, os scripts e o agente **não leem, não conferem e não mostram** o conteúdo do envelope. O agente só pergunta se a variável existe (`grep -c '^STRIPE_SECRET_KEY=' <arquivo>`, nunca o valor) e passa o arquivo inteiro para quem precisa dele: `cf deploy --secrets-file <arquivo>`, `--env-file` do Docker ou as variáveis do Coolify.
- Nada do envelope vai para o chat, para log, para o Git ou para o kit. O sincronizador do kit não toca nessa pasta.
- Nomes padrão das variáveis: `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_WEBHOOK_SECRET`, `PAYPAL_CLIENT_ID`, `PAYPAL_SECRET`, `DELIVERY_WEBHOOK_URL`, `DELIVERY_WEBHOOK_SECRET`, `TRACKEADOR_WEBHOOK_URL`, `TRACKEADOR_SECRET`, `ADMIN_TOKEN`. Um envelope por oferta (uma conta Stripe por oferta).
- Valor que o agente gera (o `whsec_` do webhook, o `ADMIN_TOKEN`): ele grava direto no envelope, sem imprimir.

## Pergunta de abertura (copiar e mandar)

> Para montar o checkout, me diga o que você já tem pronto. O que já existe eu só integro; o que faltar eu crio com você.
> 1. **Hospedagem:** Cloudflare, Coolify ou outro servidor? Qual domínio/subdomínio do checkout?
> 2. **Stripe:** a conta da oferta já existe? (organização + conta, modo teste e/ou live) O produto e os preços já estão cadastrados?
> 3. **PayPal:** vai ter PayPal? A conta Business e o app de desenvolvedor já existem?
> 4. **Oferta:** preços por moeda, upgrade, bumps, upsell (ou "pega da página de vendas").
> 5. **Entrega:** a área de membros já tem rota para receber a venda? E o Trackeador já tem conexão?
> 6. **Visual:** banner, capa, fotos dos bumps, favicon (ou "usa os da página").
> 7. **Qual tela:** cartão pelo link da Stripe (padrão) ou cartão na própria página?

## O que pedir em cada bloco

### 1. Hospedagem
| Dado | Exemplo | Se não tiver |
|---|---|---|
| Onde roda | Cloudflare / Coolify / Docker | perguntar; nunca assumir |
| Domínio do checkout | `checkout-minhaoferta.meudominio.com` (zona na conta da pessoa) | sugerir subdomínio novo e conferir com `dig` que não existe |
| Conta logada | `npx cf auth whoami` mostra a conta DELA | pedir login dela; nunca usar conta de outra pessoa |

### 2. Stripe (uma conta por oferta)
| Dado | Onde a pessoa acha | Vai para |
|---|---|---|
| Organização e conta da oferta (`acct_…`) | Dashboard → nome da conta | nota da oferta |
| Chave publicável teste/live (`pk_test_…`/`pk_live_…`) | Developers → API keys | `STRIPE_PUBLISHABLE_KEY` |
| Chave secreta ou restrita (`sk_`/`rk_`) | Developers → API keys | **envelope** → `STRIPE_SECRET_KEY` (a pessoa cola; nunca no chat) |
| Produto e preços JÁ cadastrados? (`prod_…`, `price_…` por moeda) | Product catalog | `catalog.mjs` → referência (o valor cobrado continua vindo do `catalog.mjs`) |
| Empresa verificada para o live? | Settings → Business | só liga live com isso + ordem do dono |
| Formas de pagamento | Settings → Payment methods: cartão, Apple Pay, **Google Pay ligado** (conta nova pode vir desligado) | o agente confere pela API |
| Webhook | o agente cria (`https://<domínio>/webhook`, eventos do `AGENTS.md` §5) e grava o `whsec_` no envelope sem imprimir | `STRIPE_WEBHOOK_SECRET` |
| Domínio das carteiras | o agente registra (`paymentMethodDomains`), teste e live | — |

**Se já está tudo cadastrado:** o agente só pede `pk_`, se o `STRIPE_SECRET_KEY` já está no envelope e os IDs de produto/preço, confere pela API que a conta é a certa e integra.
**Se falta:** o agente mostra o que vai criar (produto, preços por moeda) e cria só com o ok.

### 3. PayPal
| Dado | Vai para |
|---|---|
| Conta Business que recebe (qual entidade/pessoa) | nota da oferta |
| Client ID (sandbox e live) | `PAYPAL_CLIENT_ID` |
| Secret (sandbox e live) | **envelope** → `PAYPAL_SECRET` |
| Ambiente | `PAYPAL_ENV=live` só no go-live |

Sem PayPal: deixar vazio; a opção some da tela sozinha.

### 4. Oferta (vira `catalog.mjs` + `public/i18n.js`)
Plano básico e completo por moeda (EUR/CHF/CAD ou as da oferta) · upgrade **aditivo** (+ quanto) · bumps (nome, descrição, preço, preço riscado) · upsell/downsell pós-compra (nome, preço) · garantia em dias · países/mercados · nome do produto nos idiomas · IVA incluso ou não.

### 5. Entrega e rastreio
| Dado | Vai para |
|---|---|
| URL da rota da área de membros que recebe a venda | `DELIVERY_WEBHOOK_URL` |
| Segredo compartilhado com essa rota | **envelope** → `DELIVERY_WEBHOOK_SECRET` |
| Conexão do Trackeador (gateway `generic`): URL `.../api/webhooks/sale/c/<id>` | `TRACKEADOR_WEBHOOK_URL` |
| Secret da conexão (aparece só na criação) | **envelope** → `TRACKEADOR_SECRET` |

Se a rota da área de membros não existe: criar no site da oferta, seguindo o contrato do `AGENTS.md` §1c.

### 6. Visual
Banner 1024×576, capa, miniaturas dos bumps, cor da marca, depoimentos REAIS (ou nenhum). Favicon: o cadeado padrão do modelo serve.

## Depois de receber
1. Conferir pela API que a conta Stripe é a da oferta (nome e `acct_`).
2. Preencher `catalog.mjs`, `i18n.js`, imagens, `cloudflare.config.ts`/variáveis.
3. `npm test` → publicar em **teste** → webhook → domínio das carteiras → testes do `AGENTS.md` §1 passo 5.
4. Mandar à pessoa os dois links de teste e o cartão `4242 4242 4242 4242`.
5. Live só com ordem dela: chaves live, `ALLOW_LIVE=1`, webhook e domínio no live, uma compra real pequena com reembolso.
