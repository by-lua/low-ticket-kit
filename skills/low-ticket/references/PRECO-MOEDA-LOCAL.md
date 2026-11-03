# Preço na moeda do visitante (oferta vendida em vários países)

**Regra da dona (05/10/2026):** toda página de vendas de oferta vendida para vários países
(Mundpay, Hotmart, Zenith, qualquer gateway multi-moeda) mostra o preço **aproximado na moeda
local do visitante em cima, grande**, e embaixo, **menor**, o valor na moeda em que o produto
está cadastrado (US$, €), escrito como **valor de referência**. Motivo: ajuda muito a conversão.
O visitante entende o preço na moeda dele e o checkout confirma.

Vale para **qualquer país** do visitante (regra da dona 06/10), não só LATAM: nunca lista fixa de países.

Não vale para oferta de um país só que já vende na moeda local (ex.: BR em R$ na Wiven).

## Como fica
```
≈ $271 MXN                      ← grande, cor do preço; código da moeda menor (.45em)
US$ 14,90 · valor de referencia ← 13px, cor apagada
```
- Riscado ("de") também converte, sem o "≈".
- Converte **todo** preço visível: planos, selo "Desde…", texto de botão, popup de downsell e
  popup de saída. Nada pode ficar em US$ ao lado de valor local.
- Texto da referência no idioma da página: `valor de referencia` (ES), `valor de referência` (PT).
- Visitante de país que usa a mesma moeda do cadastro (EC, SV, PA, US para USD; zona do euro para
  EUR), país desconhecido ou câmbio fora do ar: a página fica só na moeda do cadastro, como antes.
- O pixel não muda: `value`/`currency` do ViewContent e do `data-tk-value`/`data-tk-currency` continuam
  na moeda do cadastro, porque é nela que o gateway cobra e o Purchase chega.

## Implementação (referência viva: `OFERTAS/mapa-do-tarot/site`, commits b9aadd7 e d3f48a7)
1. **Servidor:** `GET /painel/api/fx` → `{base:'USD', rates:{MXN:..}}`, buscando
   `https://open.er-api.com/v6/latest/<BASE>` com cache de 12h e o último valor bom se a fonte cair
   (`server/index.mjs`, `getFxRates`). Mesma origem, sem problema de CSP.
2. **HTML:** cada preço vira `<span data-usd="14.90">US$ 14,90</span>`. O riscado leva também
   `data-usd-strike`. Embaixo do preço grande vai `<div class="usd-ref" data-usd-ref="14.90"></div>`,
   escondida por CSS até a conversão ligar (`.fx-on .usd-ref{display:block}`).
3. **Qualquer país (06/10, commit 8fc81c9):** o mapa fuso→país (tzdata) e país→moeda (CLDR) mora no servidor em `server/fx-geo.json`; a página manda `/painel/api/fx?tz=<fuso>&lr=<região do idioma>&cc=<?pais>` e recebe `country`, `currency` e todas as taxas. Nada de lista fixa de países.
   Versão antiga (só LATAM): país pelo fuso (`Intl...timeZone` → mapa fuso→país), com o idioma do aparelho
   (`es-MX`) como fallback. País→moeda, busca `/painel/api/fx`, formata com
   `Intl.NumberFormat('es-'+país,{style:'currency',currency,currencyDisplay:'narrowSymbol'})`:
   sem centavos acima de 100, com centavos abaixo. Liga `fx-on` no `<html>`.
4. **Teste fora do país:** `?pais=MX` (CO, AR, CL, PE, ES…) força o país. Sempre deixar.
5. **Gate:** conferir no ar com `?pais=` em 2-3 países e de novo o gate de eventos
   (PageView, ViewContent e IC na moeda do cadastro). Prova com print e os requests.

## Página de obrigado de produto vendido em vários mercados
Quando um produto do gateway atende mais de um mercado, ele tem uma URL de agradecimento só. Não
editar o produto (na Mundpay a edição pode voltar pra análise). Fazer a URL cadastrada cair numa
página `/obrigado` que manda direto pro painel do idioma certo (fuso/idioma; `?lang=es|pt` para
testar), com os botões de cada painel como fallback. Referência: `site/obrigado.html` + 302 em
`server/index.mjs` (commit 821de03).
