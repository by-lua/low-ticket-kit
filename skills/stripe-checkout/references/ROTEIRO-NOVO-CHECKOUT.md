# Roteiro de ponta a ponta — novo produto com checkout próprio Stripe

Criado em 11/11/2026 a partir das ordens da dona. É o **primeiro teste** do checkout premium com Stripe (oferta Guide Tarot FR). Siga na ordem; cada passo aponta para a regra detalhada.

## 0. Regras fixas deste roteiro (dona, 11/11/2026)

1. **Organização e conta da oferta primeiro (dona, 11/11/2026).** "Criar o produto" = criar a **conta Stripe da oferta** dentro da organização do sócio. Descobrir a organização (dono em `OFERTAS/<slug>/CLAUDE.md`; parceria Luciola = **Winx**), listar as contas dela, e só criar se aquela oferta ainda não tiver a sua. **Calendrier Magique é a conta de outra oferta** (`acct_1UaIGiABfkUzod1X`): nada do Guide Tarot mora nela. Confirmar `/v1/account` e o ambiente (test/live) antes de qualquer escrita. Dúvida = perguntar.
2. **Formas de pagamento sempre ligadas:** cartão de crédito, **Apple Pay**, **Google Pay** e **PayPal**. Nunca lançar sem checar cada uma no ambiente real; método que não aparecer não se anuncia (ver passo 5).
3. **PayPal: sempre confirmar QUAL conta recebe, antes de ligar.** Conta definida pela dona em 11/11/2026: a Business **Dona** (perfil `paypal-dona-leadgo`, porta 9315, dashboard `49.265.147 DONA DE LIMA ASSIS`, BRL, login confirmado). Repetir a confirmação a cada oferta nova; se a oferta for outra, perguntar.
4. **Mesma oferta em vários idiomas/mercados (decisão padrão, dona pode mudar):** uma conta por OFERTA e, dentro dela, **um Product por mercado/idioma**, nome `<Produto> <MERCADO>` (ex. `Guide Tarot FR`, `Guide Tarot ES`). A conta guarda chaves, webhook, PayPal e domínio da oferta; o Product separa relatório e catálogo por mercado. Só abrir conta nova se mudar sócio, empresa ou país do recebedor. Listar Products antes de criar; dúvida = perguntar. Plano, bumps e upgrade são SKUs do catálogo. Nome sem valor embutido.
5. **Visual e fluxo da tela** vêm do `checkout-premium`. Aqui só o que é pagamento, moeda, entrega e tracking.

## 1. Levantar a oferta

Ler `low-ticket`, `INDICE.md`, `OFERTAS/<slug>/CLAUDE.md`, `OFERTA.md`, `FUNIL.md`, `STATUS.md`. Conferir a **página publicada** contra a ficha (divergência = perguntar à dona).

**Guide Tarot FR (`luciola-guidetarot-fr`), página `https://guidetarot.pages.dev/`, conferida em 11/11/2026:**

| SKU | Preço na página (EUR, IVA incluído) | Observação |
|---|---|---|
| Essentielle (Básico) | 5,90 € | 78 fiches; sem os 4 bônus |
| Complète | 12,90 € | 78 fiches + 4 bônus |
| Upgrade Básico → Complète (popup) | 7,90 € preço total | 1º bump obrigatório no checkout do Básico |
| Order bumps adicionais | **preço FR a definir** | origem BR (colagem da dona, 11/11/2026): Kit Manual do Tarô Carreira + Relacionamentos (R$ 50,22 → R$ 40,48, 19%), Guia de Interpretação Relacionamentos Românticos (R$ 37,67 → R$ 26,75, 29%), Manual de Interpretação Carreira e Finanças (R$ 47,34 → R$ 33,62, 29%). Texto "Aproveitem e comprem juntos" + "Adicionar produto". Adaptar ao FR com preço em EUR/CHF/CAD aprovado pela dona; não converter o real |
| Upsell pós-compra (Lenormand) | **a definir** | preço pendente |

Garantia: 15 dias. Todos os preços na página são em euros.

## 2. Mercados e moedas

Anúncio no mercado francófono: **França, Bélgica, Suíça e Canadá**. Idioma da tela: **francês** nos quatro.

| País | Moeda | Preços (Essentielle / Complète / Upgrade) |
|---|---|---|
| França, Bélgica | EUR | 5,90 / 12,90 / 7,90 — **aprovados** (= página) |
| Suíça | CHF | 5,90 / 12,90 / 7,90 — **aprovados pela dona (11/11/2026)** |
| Canadá | CAD | 8,90 / 19,90 / 11,90 — **aprovados pela dona (11/11/2026)** |

- Números de CHF e CAD aprovados pela dona em 11/11/2026 (referência: CHF ≈ EUR; CAD ≈ 1,5 × EUR, arredondado). Nunca converter automático; mudar valor só com ordem dela.
- País detectado no servidor (cabeçalho do edge/CDN, ex. `CF-IPCountry`): FR/BE → EUR, CH → CHF, CA → CAD, qualquer outro → EUR. A pessoa pode trocar no seletor.
- Conferir no ambiente da conta se CHF e CAD podem ser cobrados e se Apple/Google Pay/PayPal aceitam essas moedas (a Stripe converte para o repasse da conta BR, com taxa de conversão).
- **IVA/impostos:** preços com IVA incluído; Stripe Tax não existe para a conta BR. FR/BE/CH/CA têm regras diferentes (OSS na UE, TVA suíça, GST/QST no Canadá). **Resolver o tratamento fiscal fora da Stripe antes de divulgar**; a automação não declara nada.

## 3. Catálogo (fonte única de preço)

O catálogo mora no **servidor do site** (`server/skus.mjs`): SKU, nome, valor por moeda, tipo (plano, bump, upgrade, upsell) e regras de quando cada um aparece. O checkout calcula o total **no servidor**; o navegador nunca manda o preço. PaymentIntent leva só `amount` + `currency`; os SKUs vão na `metadata`.

Na Stripe, mantém-se Product/Prices **de referência** (já criados em 10–11/11/2026, ver "Caso real" no SKILL.md), com `tax_behavior=inclusive`. Para CHF/CAD, criar Prices de referência (passo 2 já aprovado).

## 4. Product e Prices na Winx

1. Conferir organização/conta (regra 1) e listar Products/Prices existentes antes de criar (nada duplicado).
2. Product do mercado na conta da oferta (Guide Tarot FR: a conta ainda será criada na Winx; os Products antigos `prod_VbZvtyqHcgx67d` e `prod_VbrU18hVpmTe10` foram APAGADOS da conta Calendrier Magique em 11/11/2026 por ordem da dona). Bump adicional e Lenormand ganham Product próprio quando houver preço.
3. Prices por moeda, `lookup_key` único (`<oferta>_<sku>_<moeda>`), `tax_behavior=inclusive`, sandbox e live separados.
4. Registrar IDs não secretos em `STATUS.md` e `_memoria/contas-e-codigos.md`.

## 5. Formas de pagamento — checagem obrigatória

| Forma | Como entra | Checar |
|---|---|---|
| Cartão | Payment Element incorporado | habilitado na conta e na moeda |
| Apple Pay | Express Checkout / Payment Element | domínio HTTPS registrado na Stripe (teste e live), Safari/dispositivo |
| Google Pay | idem | método ligado na configuração da conta (estava **desligado**), domínio registrado, Chrome |
| PayPal | ver abaixo | conta confirmada (regra 3) |

**PayPal — caminho:** a Stripe não processa PayPal nativo em conta brasileira. Duas rotas, em ordem:
1. **PayPal como forma de pagamento personalizada na Stripe** (Elements + Payment Intents): criar em Configurações → Pagamentos, **na conta Winx**, em teste e em live (cada ambiente tem seu `cpmt_...`; em 11/11/2026 existem: live `cpmt_1UafaQABfkUzod1XYwjPVcas` e teste `cpmt_1Uag8CABfkUzod1XTgLrKslU`, ambos na Winx/Calendrier Magique; a dona chamou o live de "outro produto", confirmar com ela antes de usar). Só vale se o fluxo completo passar em sandbox.
2. **PayPal separado:** botão próprio na nossa página, API de Orders do PayPal com um app de desenvolvedor da conta Business Dona (credenciais no cofre da máquina, `PAYPAL_DONA_LEADGO_*`), webhook do PayPal para entrega e Trackeador. Plano B se a rota 1 falhar.

**Estado do PayPal Dona (11/11/2026):** login no PayPal Developer feito no perfil `paypal-dona-leadgo` (9315). Credenciais **sandbox** do app "Default Application" salvas no cofre da máquina como `PAYPAL_DONA_LEADGO_SANDBOX_CLIENT_ID` e `PAYPAL_DONA_LEADGO_SANDBOX_SECRET`; token OAuth sandbox testado (HTTP 200). **Live:** nenhum app criado ainda (a aba Live está vazia); criar só no go-live, com ordem da dona, e salvar como `PAYPAL_DONA_LEADGO_LIVE_*`. Webhook do PayPal (entrega e Trackeador) ainda não cadastrado.

Seja qual for a rota: PayPal **não entra no upsell de um clique** (assumir que não até provar), e ele é anunciado só depois do teste completo (pagar, webhook, reembolso).

## 6. Tela e fluxo

Tela pelo `checkout-premium` (e-mail → bumps desmarcados → forma de pagamento → comprar; cobrança só no clique). Extras internacionais ligados aqui (país, moeda, idioma, locale do Stripe Elements). Ver `MAPA-PREMIUM-x-STRIPE.md` e `CHECKOUT-PROPRIO-STRIPE.md`.

## 7. Entrega, tracking e upsell

- Webhook assinado: `payment_intent.succeeded` libera apenas os SKUs pagos, uma vez (idempotente); `charge.refunded` e `charge.dispute.*` tratados. Dois destinos: entrega e Trackeador.
- `_tkid` e `event_id` no pedido; `Purchase` do servidor e do pixel com o mesmo `event_id`.
- Upsell de um clique (Lenormand): `STRIPE-UPSELL-1-CLIQUE.md`, só cartão/carteira reutilizável, com consentimento.

## 8. Teste antes de publicar

Rodar a lista da seção 4 de `CHECKOUT-PROPRIO-STRIPE.md` em sandbox da Winx **para cada forma de pagamento e cada moeda aprovada**, sem enviar venda fictícia ao Trackeador de produção. Só então apontar os CTAs públicos (a página `guidetarot.pages.dev` hoje usa o checkout atual; não trocar antes).

## 9. Fechar

`low-ticket-salvar`: STATUS, `_memoria/contas-e-codigos.md`, INDICE e esta skill atualizados apenas com fatos observados.
