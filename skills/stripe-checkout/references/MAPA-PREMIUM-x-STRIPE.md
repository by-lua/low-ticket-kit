# Mapa: checkout-premium × stripe-checkout (11/11/2026)

Decisão da dona em 11/11/2026: checkout próprio no estilo Hotmart. A pessoa entra, o país é reconhecido, aparecem a moeda e o idioma dela. Ela escolhe plano, bumps e forma de pagar. **Cartão incorporado na nossa página** (Stripe Payment Element), PayPal em botão próprio, Apple Pay e Google Pay com ícones oficiais. Selo "Link / Stripe" perto do cartão para passar segurança.

## 1. Quem manda em quê

| Assunto | Skill dona | Regra |
|---|---|---|
| Visual, ordem da tela, copy, timer, garantia, selos, bump com foto, prova social, popup de saída | `checkout-premium` | Parte de `MODELOS/checkout-base/index.html` |
| Conta, Product/Price, PaymentIntent, webhook, upsell de um clique, IVA, métodos disponíveis | `stripe-checkout` + `CHECKOUT-PROPRIO-STRIPE.md` | Valor sempre calculado no servidor |
| Entrega e Trackeador | `stripe-checkout` §6 | Dois webhooks, idempotentes |

Em conflito, a regra de **dinheiro e cobrança** vale a do Stripe; a de **tela** vale a do premium.

## 2. Pontos em que as duas já combinam (não mexer)

- Ordem: e-mail → bumps (desmarcados) → forma de pagamento (nenhuma marcada) → botão de compra.
- Cobrança criada **uma vez, no clique** = PaymentIntent adiado (Payment Element monta antes; o servidor cria o Intent só no clique, com `Idempotency-Key`).
- Marcar bump recalcula a tela e chama `elements.update({amount})`; o total vem do servidor.
- E-mail capturado no `onBlur` (lead) antes do clique.

## 3. Lacunas que o premium precisa ganhar para o Stripe

1. **Tabela de gateways do premium não tem linha Stripe.** Linha a acrescentar: Stripe (conta Winx/BR, cobra em EUR) = Cartão (Payment Element) + Apple Pay / Google Pay (Express Checkout, só se elegível no navegador) + PayPal separado.
2. **Tile de cartão tem campos dentro.** Tile "Cartão" ao ser escolhido abre o Payment Element; os outros tiles não abrem campo.
3. **Logos oficiais** (premium #7): Visa/Mastercard/Amex, Apple Pay, Google Pay, PayPal e Link, todos baixados da fonte oficial da marca, seguindo as regras de uso de cada uma. Nada gerado por IA. Selo "Pagamento seguro via Stripe" ao lado do cartão.
4. **Botão de compra** vira o `confirmPayment` do Stripe; ele trava ao clicar.
5. **Carteira (Express Checkout)** não passa pelo nosso botão: o pedido nasce no clique da carteira. O valor mostrado nela tem de acompanhar bumps e plano.

## 4. Fatos da conta que mudam o desenho (do SKILL do stripe, conferidos)

- **PayPal pela Stripe NÃO existe na conta Winx (BR).** Isso corrige o que eu disse antes no chat. O PayPal tem de ser integração separada (API de Orders do PayPal), com conta comercial e reconciliação próprias. Falta definir qual entidade recebe: a Business da Dona (login confirmado em 11/11) ou outra.
- **Google Pay estava desligado** na configuração consultada. Apple/Google Pay exigem domínio HTTPS **registrado** na Stripe, em teste e live. Só mostrar o botão se ele aparecer de fato no ambiente real.
- **Stripe Tax não é suportado** para a conta BR. Price com `tax_behavior=inclusive` só garante o valor final; IVA é tratado fora da Stripe antes do lançamento.
- **Upsell de um clique só em cartão (e carteiras reutilizáveis)**, com consentimento explícito para salvar o método na compra. PayPal separado não entra no upsell de um clique.
- Sem boleto, parcelado ou voucher nesta entrada.

## 5. Preços e moedas (meio-termo, ajustado ao Payment Element)

Com PaymentIntent adiado **não existe linha de item**: o Intent leva só `amount` e `currency`. Então, na prática:
- O **catálogo de preços por moeda mora no nosso `server/skus.mjs`** (Básico, Completo, Upgrade, bumps, upsell). É a fonte única da tela, do total e do Intent.
- Product/Prices na Stripe ficam como cadastro de referência e relatório; o Intent não aponta para eles. O SKU vai na `metadata`.
- Moeda nova = linhas novas no catálogo + checar métodos/IVA da moeda. Não converter automático.

## 6. Tracking com cartão incorporado

Não há problema; é melhor que redirect. Pontos de atenção:
- `InitiateCheckout` dispara só no clique de compra (e no clique da carteira/PayPal). Não disparar ao escolher forma de pagamento.
- `Purchase`: o servidor dispara pelo webhook `payment_intent.succeeded` (CAPI + Trackeador); a página de retorno dispara o pixel com o **mesmo `event_id`** (id do pedido) para deduplicar.
- `_tkid` e atribuição do clique entram na `metadata` do Intent e no pedido.
- PayPal separado: o `return_url` carrega o id do pedido; o webhook do PayPal faz o mesmo papel.
- O iframe do Stripe não bloqueia o pixel da página.

## 7. Extras que só valem para checkout internacional

Num checkout de **um só país**, nada disto é necessário:
- Detecção de país (cabeçalho do edge/CDN ou servidor) e escolha automática de moeda e idioma, com seletor manual.
- Tabela de preços por moeda e formatação `Intl.NumberFormat`.
- Tradução de todo o texto da tela (timer, selos, garantia, bumps) e `locale` do Stripe Elements.
- Garantia internacional (15 dias) e depoimentos do mercado certo.
- Métodos de pagamento filtrados por país/moeda; domínio registrado para carteiras.
- IVA por país e taxa de conversão na repasse da Stripe (~2% quando a moeda difere da do repasse).

## 8. Ordem de trabalho

1. Definir quem recebe o PayPal e conferir elegibilidade de Apple/Google Pay (domínio).
2. Catálogo de preços por moeda em `skus.mjs` (preço do bump e do Lenormand pendentes).
3. Páginas: copiar `MODELOS/checkout-base`, adaptar ao Payment Element e idioma.
4. Backend: rota que calcula total e cria o Intent; webhooks de entrega e Trackeador.
5. Teste completo em sandbox (lista da seção 4 de `CHECKOUT-PROPRIO-STRIPE.md`), depois publicar.
