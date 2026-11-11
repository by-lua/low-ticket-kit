# Checkout próprio Stripe — modelo da casa

Revisado em 10/11/2026 para a oferta Guide Tarot FR. Este é o procedimento de integração; IDs e capacidades da conta ficam em `SKILL.md` e `OFERTAS/<slug>/STATUS.md`. Aplicar somente após ler `low-ticket`, `INDICE.md`, `CLAUDE.md`, `OFERTA.md`, `FUNIL.md`, `_memoria/contas-e-codigos.md` e `ATIVOS.md` da oferta.

## 1. Confirmar a entrada

1. Confirmar organização, conta, ambiente e dono da oferta via MCP `list_available_accounts_or_orgs` e leitura de `/v1/account` (ou CLI perfil explícito, se autenticada). Não misturar IDs de teste/live ou de contas diferentes.
2. **Oferta já no ar:** conferir página/JS publicados e checkout atual contra `OFERTA.md`/`FUNIL.md` antes de copiar preços, prazo de garantia ou trocar links. Divergência pede decisão da dona; não inferir que o arquivo local ou o site público venceu. Listar Product/Prices existentes antes de criar. Criar preços somente para valores reconciliados e aprovados; moeda e valor em centavos no servidor. Nome não inclui preço. Conferir `tax_behavior` e política de IVA antes de cadastrar Price; não presumir que `tax_behavior=unspecified` serve a Stripe Tax. Se a conta não suportar Stripe Tax, `inclusive` define o valor final mas **não calcula/declara IVA**; resolver a obrigação fiscal fora da automação Stripe antes do lançamento.
3. Definir os SKUs de cada entrada (Básico, Completo, Upgrade, Saída), bumps em **todas** as entradas, upsell e downsell. Um item sem preço aprovado fica fora da cobrança. A conta Stripe precisa ser a mesma na compra inicial e no upsell de um clique.
4. Confirmar onde mora o código/backend do site, quem controla o domínio e qual serviço libera a área de membros. Endpoints de pagamento, webhook e autorização do upsell exigem servidor e armazenamento persistente. Página estática sozinha não conclui o funil.

## 2. Formulário e cobrança inicial

**Ordem obrigatória da casa:** e-mail → bumps/upgrade → forma de pagamento → botão comprar. O total visível e o valor apresentado por carteiras devem acompanhar as escolhas. No modelo `MODELOS/checkout-base/index.html`, usar o Stripe Payment Element e, quando elegível, Express Checkout Element; carregar Stripe.js direto de `js.stripe.com`, em HTTPS, sem capturar cartão/CVC no HTML próprio.

Para a exigência “pedido/cobrança criado só no clique”, seguir o [PaymentIntent adiado](https://docs.stripe.com/payments/accept-a-payment-deferred?platform=web&type=payment): inicializar Elements com `mode: 'payment'`, `currency` e `amount` **calculado pelo servidor**; montar Payment Element antes de criar Intent. Quando bump/plano muda, o servidor recalcula e devolve o total; chamar `elements.update({amount: total})`. Não usar total fornecido pelo browser como preço final.

**Preço com IVA incluído no PaymentIntent direto:** o `tax_behavior=inclusive` do Price do catálogo não é aplicado automaticamente ao `amount` passado ao PaymentIntent. O backend deve cobrar exatamente o total aprovado (por exemplo, 590/1290/790 centavos para as três entradas Guide Tarot FR), sem somar imposto ao valor exibido. Cálculo, registro e emissão de IVA são processos separados quando Stripe Tax não está disponível para a conta.

No clique explícito em comprar:

1. Desabilitar o botão durante a tentativa e chamar `elements.submit()` para validar o formulário.
2. O servidor valida sessão, e-mail, entrada, bumps, preço, moeda, consentimento para salvar método e regra de taxação; grava o pedido com chave única persistente. Cria **um** PaymentIntent com Customer da mesma conta, `amount`, `currency`, metadata com `offer_slug`, `order_id`, `entry`, SKUs e referência de atribuição. Usar `Idempotency-Key` estável do pedido. Repetição devolve o mesmo Intent/client secret; erro ambíguo é reconciliado antes de tentar de novo.
3. O browser confirma com `stripe.confirmPayment({elements, clientSecret, confirmParams:{return_url}})`. Tratar autenticação adicional/redirect e falhas. A página de retorno consulta estado; **não concede acesso**.
4. O webhook assinado de `payment_intent.succeeded` concede somente os SKUs pagos, uma vez. `processing`, `requires_action` ou falha não liberam entrega.

**Método para upsell:** expor consentimento claro antes da compra para salvar e usar o método em uma oferta posterior opcional. Configurar Customer e `setup_future_usage` ou o salvamento nativo por CustomerSession de modo coerente entre Elements e Intent; verificar que o PaymentMethod ficou associado ao Customer. Se não houver consentimento ou se o método não puder ser reutilizado, o upsell abre um novo fluxo de pagamento. **Nunca cobrar o upsell automaticamente** só porque o cartão foi salvo. Ver [salvar métodos com Payment Element](https://docs.stripe.com/payments/accept-a-payment-deferred?platform=web&type=payment#save-and-retrieve-customer-payment-methods).

Checkout Sessions com `ui_mode=elements` é outra integração válida, mas exige criar Session para obter `client_secret` **antes** de montar o formulário. Não descrevê-la como “Session criada apenas no clique” se o pagamento já estava visível na página. Se a dona mudar a ordem, reavaliar essa opção pela [documentação do Checkout](https://docs.stripe.com/payments/checkout/how-checkout-works?payment-ui=checkout-elements).

## 3. Upsell de um clique

Seguir `_skills/low-upsell-app/references/STRIPE-UPSELL-1-CLIQUE.md`. O browser só recebe uma referência opaca de funil, nunca IDs de Customer ou PaymentMethod escolhidos pelo cliente. O servidor exige pedido inicial **pago**, sessão/cookie seguro associado ao comprador e proteção CSRF; resolve o método salvo pelo pedido. Mostrar produto, preço, moeda e natureza avulsa/recorrente antes do botão. O aceite cria uma única cobrança idempotente por `order_id + stage`; mesmo após expirar a janela de idempotência da Stripe, a restrição única do banco impede duplicação. Quando banco exige 3DS, devolver o client secret da cobrança existente para Stripe.js concluir. Recusa leva ao downsell/obrigado, sem cancelar a compra inicial. Meio não reutilizável abre novo checkout vinculado ao mesmo pedido.

## 4. Métodos, domínio e webhooks

- Ativar somente métodos disponíveis na **conta e moeda** da oferta, com confirmação imediata conforme a preferência da dona. Não habilitar Pix, boleto, parcelado ou vouchers nesta entrada. Apple/Google Pay dependem de conta, domínio HTTPS, navegador, dispositivo e carteira do comprador. [Registrar cada domínio/subdomínio](https://docs.stripe.com/payments/payment-methods/pmd-registration.md?dashboard-or-api=api) que exibe carteira em teste e live. Não prometer um botão que não apareceu no ambiente real.
- PayPal processado pela Stripe [não está disponível para conta brasileira](https://docs.stripe.com/payments/paypal#business-locations). PayPal separado exige conta comercial e integração/reconciliação próprias, inclusive para o upsell. O [acordo do PayPal BR](https://www.paypal.com/br/legalhub/paypal/useragreement-full?locale.x=en) contempla recebimento internacional, sujeito à elegibilidade e às tarifas da conta. O [adaptador PayPal da Stripe](https://docs.stripe.com/payments/payment-methods/custom-payment-methods/paypal) é preview com acesso solicitado à Stripe; não assumir que está habilitado. O método da compra inicial deve ser testado para reutilização; carteira não é automaticamente um cartão reutilizável.
- Cadastrar endpoint assinado de entrega e endpoint de medição Trackeador para **todos** os SKUs e eventos necessários. A aplicação verifica `Stripe-Signature` no body bruto, timestamp e `event.id`; processa eventos de modo idempotente e fora de ordem. Para PaymentIntent adiado, usar `payment_intent.succeeded|payment_failed|canceled`, `charge.refunded`, `charge.dispute.created|closed`; abandono da página é medido pela aplicação, e não por suposto webhook instantâneo da Stripe. Adicionar os eventos de assinatura quando houver assinatura real.
- Comprovar, em ambiente de teste da conta correta: compra principal, bump, upsell, recusa/downsell, autenticação 3DS, cartão recusado, clique duplo/reload/timeout, webhook duplicado e fora de ordem, reembolso/disputa, e 2xx nos **dois destinos** sem enviar venda fictícia ao Trackeador de produção. Conferir IC no clique que realmente leva ao checkout. Só então ligar os CTAs públicos.

## 5. Registro e estado

Salvar IDs não secretos, conta/ambiente, domínio, endpoints e provas em `STATUS.md` e `_memoria/contas-e-codigos.md`. Atualizar a skill somente com fatos observados, separando catálogo criado, integração local, teste e publicação. Fechar com `low-ticket-salvar`.

Fontes oficiais adicionais: [Payment Element adiado](https://docs.stripe.com/payments/accept-a-payment-deferred?platform=web&type=payment), [PaymentIntents](https://docs.stripe.com/payments/payment-intents), [idempotência](https://docs.stripe.com/api/idempotent_requests), [webhooks](https://docs.stripe.com/webhooks), [métodos de pagamento](https://docs.stripe.com/payments/payment-methods), [testes](https://docs.stripe.com/testing).
