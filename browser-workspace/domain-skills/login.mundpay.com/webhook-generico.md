# Mundpay — Webhook Genérico (verificado 2026-09-29)

Rota: `https://login.mundpay.com/integrations/configurations` → card
**Webhook Genérico** (`/integrations/webhook`) → **Conectar integração**.

Preencher: Título, URL de postback, produto, Tipo de Evento e Tipo de
pagamento. Para Trackeador: Pago + Reembolsado + Chargeback; Aguardando
pagamento é opcional. URL completa:
`https://<trackeador>/api/webhooks/sale/c/<connection-id>?token=<secret>`.
Nunca imprimir/copiar o secret para logs, chat ou receita.

O formulário não mostra campo de secret/header. A Central Mundpay cita
`X-Mundpay-Signature` HMAC-SHA256, mas não documenta obtenção da chave nem
o manifest. O preset Trackeador usa token aleatório na query, validado antes
de persistir o payload.

Payload oficial: `event` + `data.transaction_id/status/amount/currency/
payment_method/customer/product/tracking/created_at`; amount em centavos.
O botão Testar atual pode mandar shape achatado com `id`, `event_type`,
`status`, `customer` e `offers`; o preset aceita ambos.

Tracking do checkout: `utm_*`, `src` e parâmetros extras entram em
`tracking`. `ref` é excluído explicitamente. Parâmetro recomendado para o
tracking id: **`_tkid`**; no webhook, ler `tracking._tkid`. Isso é
SUPOSIÇÃO baseada na doc/bundle da Mundpay — não provado por webhook real
ainda (ver bloco "Testar" abaixo).

## Formulário "Conectar integração" — armadilhas de automação (29/09/2026)

- **`fill` não basta**: preencher Título/URL de postback com `agent-browser
  fill` não atualiza o estado React (campo controlado) — ao clicar "Salvar
  integração" o formulário volta vazio com "Essa informação é obrigatória" /
  "URL inválida" / "Selecione pelo menos um produto." mesmo com os campos
  visualmente preenchidos. Use `click` no campo + `type` (não `fill`) + Tab
  pra sair — só assim o valor gruda no state.
- **Combobox de Produto**: clicar a opção da lista com `find text "<nome>"
  click` funciona (mostra ✓ e atualiza o combobox); `ArrowDown`+`Enter` NÃO
  seleciona nesse componente. Fechar o dropdown com `Escape` fecha o MODAL
  INTEIRO (perde tudo) — feche clicando em outro campo do formulário
  (ex.: no campo Título) em vez de Escape.
- **Nome do produto no dropdown ≠ nome exibido em Produtos do painel**: o
  produto com id na URL bate pelo campo "Nome do produto" da página
  `/products/edit-product/<id>/geral`, não pelo nome do link do checkout.
  Ex.: produto `01a0d98a-e8f5-72a6-b1d4-43b36f5ee190` = "Mapa do Tarot
  Essencial - PT" no dropdown, não "Mapa do Tarot - PT".
- **Botão "Testar" (dentro de Editar) tem bug de automação**: abre o modal
  "Testar Webhook" certo, mas QUALQUER clique real (mouse down+up) num rádio
  de Tipo de Evento/Método de Pagamento fecha o modal inteiro (parece
  handler de "clique fora" disparando antes do clique no rádio — bug de
  z-index/portal do lado deles, reproduzido 29/09/2026, várias tentativas).
  `element.click()` via JS puro mantém o modal aberto mas não marca o rádio
  (handler não é um onClick simples). Não veio solução — se precisar usar o
  Testar, tente manualmente no navegador humano; não confie em automação
  pra isso ainda.
- **Confirme salvamento pela rede, não pela UI**: "Salvar integração"
  fechando o modal NÃO significa que salvou — só confia se aparecer
  `POST .../api/v1/integrations?integration=webhook` com `201` (via
  `agent-browser network requests`) ou recarregando a lista.
