# Roteiro de ponta a ponta — novo produto com checkout próprio Stripe

Procedimento genérico (vale para qualquer oferta). Dados de conta, IDs, preços e mercados de cada oferta ficam em `OFERTAS/<slug>/STRIPE-PAYPAL.md` e `_memoria/contas-e-codigos.md`; esta skill não os cita. Siga na ordem.

## 0. Regras fixas (dona, 11/11/2026)

1. **Organização e conta da oferta primeiro.** "Criar o produto" = existir a **conta Stripe da oferta** dentro da organização do sócio. Descobrir a organização pela ficha da oferta (`OFERTAS/<slug>/CLAUDE.md`), listar as contas dela. Se a oferta não tiver conta, **pedir à dona que crie e informe organização e nome da conta; o agente não cria conta** (titularidade, dados públicos e banco de repasse são dela). Conferir `/v1/account` e o ambiente (teste/live) antes de escrever qualquer coisa. Conta errada = parar.
2. **Formas de pagamento sempre ligadas:** cartão de crédito, **Apple Pay**, **Google Pay** e **PayPal**. Nunca lançar sem checar cada uma no ambiente real; método que não aparecer não se anuncia (passo 5).
3. **PayPal: sempre confirmar QUAL conta PayPal recebe**, antes de ligar e a cada oferta nova (a conta é decisão da dona; ver fatos em `_memoria/contas-e-codigos.md`).
4. **Mesma oferta em vários idiomas/mercados:** uma conta por OFERTA e, dentro dela, **um Product por mercado/idioma**, nome `<Produto> <MERCADO>`. A conta guarda chaves, webhook, PayPal e domínio da oferta; o Product separa relatório e catálogo por mercado. Só abrir conta nova se mudar sócio, empresa ou país do recebedor (decisão padrão; a dona pode mudar). Listar Products antes de criar; dúvida = perguntar; nunca assumir.
5. **Visual e fluxo da tela** vêm do `checkout-premium`. Aqui só pagamento, moeda, entrega e tracking.
6. **Preços, moedas e mercados** são decisão da dona, por oferta. Nunca converter moeda automático; valor novo só com ordem dela.

## 1. Levantar a oferta

Ler `low-ticket`, `INDICE.md`, `OFERTAS/<slug>/CLAUDE.md`, `OFERTA.md`, `FUNIL.md`, `STATUS.md`. Conferir a **página publicada** contra a ficha (divergência = perguntar à dona). Montar a tabela de SKUs (planos, upgrade **aditivo**, bumps, upsell) com preço por moeda aprovado; item sem preço aprovado fica fora da cobrança. Garantia: Brasil 7 dias, internacional 15.

## 2. Mercados e moedas

- Definir com a dona os países, a moeda de cada um e o idioma da tela. País detectado no servidor (`CF-IPCountry` / `request.cf.country`); a pessoa troca no seletor; país fora da lista cai na moeda padrão.
- Conferir no ambiente da conta se cada moeda pode ser cobrada e se Apple/Google Pay/PayPal aceitam essa moeda (a Stripe converte para a moeda de repasse da conta, com taxa).
- **IVA/impostos:** preços com IVA incluído (`tax_behavior=inclusive`); Stripe Tax pode não existir para o país da conta. **Resolver o tratamento fiscal fora da Stripe antes de divulgar**; a automação não declara nada.

## 3. Catálogo (fonte única de preço)

O catálogo mora no **servidor do checkout** (`catalog.mjs` do modelo): SKU, nome, valor por moeda, tipo e regras. O total é calculado **no servidor**; o navegador nunca manda preço. PaymentIntent leva só `amount` + `currency`; os SKUs vão na `metadata`. Na Stripe, Product/Prices ficam como cadastro de referência.

## 4. Product e Prices na conta da oferta

1. Conferir organização/conta (regra 1) e listar Products/Prices existentes antes de criar (nada duplicado).
2. Product do mercado (`<Produto> <MERCADO>`); bumps e upsell ganham Product próprio quando houver preço aprovado.
3. Prices por moeda, `lookup_key` único (`<oferta>_<sku>_<moeda>`), `tax_behavior=inclusive`, teste e live separados.
4. Registrar IDs não secretos em `OFERTAS/<slug>/STRIPE-PAYPAL.md` e `STATUS.md`.

## 5. Formas de pagamento — checagem obrigatória

| Forma | Como entra | Checar |
|---|---|---|
| Cartão | Payment Element incorporado | habilitado na conta e na moeda |
| Apple Pay | Express Checkout | domínio HTTPS registrado na Stripe (teste e live), Safari/aparelho |
| Google Pay | idem | método ligado na configuração da conta, domínio registrado, Chrome |
| PayPal | ver abaixo | conta confirmada (regra 3) |

**PayPal — caminho** (a Stripe não processa PayPal nativo em conta brasileira), em ordem:
1. **PayPal como forma de pagamento personalizada na Stripe** (Elements + Payment Intents): criar no painel da conta da oferta, em teste e em live (cada ambiente tem o seu `cpmt_...`). Só vale se o fluxo completo passar em sandbox.
2. **PayPal separado:** botão próprio, API de Orders com um app de desenvolvedor da conta Business que recebe (credenciais sandbox e live separadas, no cofre), webhook do PayPal para entrega e Trackeador. É o caminho usado pelo modelo e o plano B da rota 1.

PayPal **não entra no upsell de um clique** (assumir que não até provar) e só é anunciado depois do teste completo (pagar, webhook, reembolso). Criar app live do PayPal só no go-live, com ordem da dona.

## 6. Tela e fluxo

Tela pelo `checkout-premium` / modelo `MODELOS/checkout-internacional-hotmart/`. Extras internacionais (país, moeda, idioma, locale do Stripe Elements). Ver `MAPA-PREMIUM-x-STRIPE.md`, `MODELO-INTERNACIONAL-HOTMART.md` e `CHECKOUT-PROPRIO-STRIPE.md`.

## 7. Entrega, tracking e upsell

- Webhook assinado: `payment_intent.succeeded` libera apenas os SKUs pagos, uma vez (idempotente); `charge.refunded` e `charge.dispute.*` tratados. Dois destinos: entrega e Trackeador.
- `_tkid` e `event_id` no pedido; `Purchase` do servidor e do pixel com o mesmo `event_id`.
- Upsell de um clique: `STRIPE-UPSELL-1-CLIQUE.md` (em `_skills/low-upsell-app/references/`), só cartão/carteira reutilizável, com consentimento.

## 8. Teste antes de publicar

Rodar a lista da seção 4 de `CHECKOUT-PROPRIO-STRIPE.md` em sandbox da conta da oferta **para cada forma de pagamento e cada moeda aprovada**, sem enviar venda fictícia ao Trackeador de produção. Só então apontar os CTAs públicos (não trocar antes).

## 9. Fechar

`low-ticket-salvar`: STATUS, `_memoria/contas-e-codigos.md`, INDICE e esta skill atualizados apenas com fatos observados.

## 10. Implementação de referência e lições

O modelo `MODELOS/checkout-internacional-hotmart/` é a implementação de referência (instâncias em `OFERTAS/<slug>/checkout/`). Lições: a CLI da Stripe serve de backend de teste (`stripe post|get --project-name <perfil>`) e `stripe listen --events ... --forward-to` entrega webhooks locais; as chaves de teste do sandbox estão no DOM da página de chaves (extrair sem imprimir e gravar no cofre); a captura PayPal só se prova com conta compradora sandbox.
