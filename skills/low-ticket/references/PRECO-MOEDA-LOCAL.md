# Preço em página internacional: valor na moeda da oferta + aviso de conversão

**Regra da dona (09/11/2026, SUBSTITUI a conversão automática de 05/10 e 07/11):** em toda página de vendas de
oferta vendida para vários países (Hotmart no mundo todo, francês estilo Rodrigo, espanhol/LATAM, qualquer gateway
multi-moeda), **o preço aparece na moeda da oferta (US$, €...), no tamanho normal, e logo embaixo vai um aviso
pequeno e cinza** dizendo que o valor é convertido pra moeda local no checkout. **Não existe mais script de conversão
na página**: nada de câmbio, API de cotação, `/painel/api/fx`, `fx-geo.json`, `data-eur`.

Motivo: nenhuma cotação que a página estimasse batia com o checkout (a Hotmart cobra até 30% a mais que o câmbio de
mercado: spread por moeda + arredondamento pra cima em número inteiro; 5,90 € = 7 CHF, 10 CAD, R$ 39,84; a página
mostrava 5,39 CHF). Mostrar só o valor da moeda da oferta + aviso é sempre verdadeiro.

## Como fica
```
12,90 €                                    ← preço no tamanho/design de sempre, moeda da oferta
* Le prix est converti dans votre devise locale lors du paiement.    ← aviso: ~11px, peso 400, cinza, logo abaixo
```
- **Todo lugar em que o preço aparece:** pílula/selo do hero, card de cada plano, popups (upgrade, saída), downsell,
  qualquer bloco de preço. Preço riscado ("de") e preço dentro de botão não levam aviso próprio: o aviso vai no bloco
  do preço principal (ou logo abaixo do botão, se o botão for o único lugar com preço).
- **Alinhado com o preço:** preço à esquerda (card de plano) → aviso à esquerda; preço centralizado (hero, popup) →
  aviso centralizado. Desalinhado a dona reprova.
- **Tamanho conforme a seção:** sempre menor que o preço; em pílula/popup apertado pode ir a ~10px; em card de plano 11–12px.
  Cinza um pouco mais escuro (dona 09/11/2026; Calendrier: `#7a6c6f`). Quebra de linha livre.
- **NÃO mexer no design nem no layout.** Pílula continua pílula, preço dentro de botão continua dentro do botão.
- **Texto no idioma da página** (começa com `*`):
  - FR: `* Le prix est converti dans votre devise locale lors du paiement.` (PT: o preço é convertido para a sua moeda local no pagamento)
  - ES: `* El precio se convierte a tu moneda local en el checkout.`
  - PT: `* O preço é convertido para a sua moeda local no checkout.`
  - EN: `* The price is converted to your local currency at checkout.`
  Texto em francês/espanhol mostrado à dona sempre com a tradução em PT ao lado.
- **Oferta de UM país só, na moeda dele** (Brasil em R$, Argentina em ARS, Portugal em €): sem aviso, o preço já é a moeda da pessoa.
- O pixel não muda: `value`/`currency` do ViewContent e do `data-tk-value`/`data-tk-currency` ficam na moeda do cadastro.

## Implementação
- HTML: `<div class="price-note">TEXTO</div>` logo depois do elemento de preço (no hero, depois da `.price-pill`).
- CSS (já no Modelo Padrão): `.price-note{font-family:var(--font-body);font-weight:400;font-size:11px;line-height:1.35;color:#7a6c6f;text-align:center;margin:3px 0 0}.pcard .price-note{text-align:left}`.
- Referência viva: `low-pagina/modelos/modelo-padrao/index.html` e `OFERTAS/calendrier-magique-fr/site/index.html`.
- Gate: abrir a página (celular 430px e desktop) e conferir que **todo** preço visível tem o aviso embaixo, no idioma certo,
  sem script de conversão no `<head>`/`<body>` e sem `data-eur`.

## Fora de uso (não copiar pra oferta nova)
- O conversor antigo (`/painel/api/fx`, `getFxRates`, `fx-geo.json`, `data-eur`/`data-usd`) segue só em páginas antigas
  (ex.: Mapa del Tarot ES) até a dona mandar trocar.
- A API `hotmart-fx-api` (repo `leadgodev/hotmart-fx-api`, `https://hotmart-fx.leadgo.dev`, código local `_servicos/fx-hotmart/`)
  mede o preço que o checkout da Hotmart cobra por país. Está no ar mas **parada, sem uso** (decisão da dona 09/11/2026:
  "deixa em segundo plano"). Só religar com ordem da dona.

## Página de obrigado de produto vendido em vários mercados
Quando um produto do gateway atende mais de um mercado, ele tem uma URL de agradecimento só. Não
editar o produto (na Mundpay a edição pode voltar pra análise). Fazer a URL cadastrada cair numa
página `/obrigado` que manda direto pro painel do idioma certo (fuso/idioma; `?lang=es|pt` para
testar), com os botões de cada painel como fallback. Referência: `site/obrigado.html` + 302 em
`server/index.mjs` (commit 821de03).
