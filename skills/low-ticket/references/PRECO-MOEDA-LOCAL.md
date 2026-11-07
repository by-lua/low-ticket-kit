# Preço na moeda do visitante (oferta vendida em vários países)

**Regra da dona (05/10/2026, formato revisto 07/11/2026):** toda página de vendas de oferta vendida
para vários países (Mundpay, Hotmart, Zenith, qualquer gateway multi-moeda) mostra o preço **na moeda
local do visitante no lugar do preço original, com o mesmo design**, e embaixo, centralizado com o
preço, "valor aproximado na sua moeda" (menor e mais claro) e o valor na moeda do cadastro (US$, €).
Motivo: ajuda muito a conversão. O visitante entende o preço na moeda dele e o checkout confirma.

Vale para **qualquer país** do visitante (regra da dona 06/10), não só LATAM: nunca lista fixa de países.

**Quando usar (regra da dona 07/11/2026):**
- **USA SEMPRE** quando a oferta vende para vários países: Hotmart no mundo todo, francês no estilo
  Rodrigo (idioma francês, países abertos), espanhol/LATAM em geral, qualquer campanha aberta por idioma.
- **NÃO usa** quando a oferta vende para UM país específico na moeda dele (Brasil em R$, Argentina
  em ARS, Portugal em €, etc.) — o preço já está na moeda da pessoa.
- Oferta que era de um país e passa a vender para mais países: liga o script.

## Como fica (regra da dona 07/11/2026)
```
[ Solo R$52,28 ]                 ← preço no MESMO elemento e design de antes (pílula, botão, card)
Valor aproximado en tu moneda    ← detalhe: 10px, peso 400, CINZA (ink-300), quase some
US$ 9,50                         ← 15px, peso 600 (não fininho), tom apagado (ink-500), sem rótulo
```
- **NÃO mexer no design nem no layout.** Pílula roxa continua pílula, preço dentro de botão continua
  dentro do botão, card continua card. Só troca o número pela moeda local e ACRESCENTA as 2 linhas
  embaixo. Erro já cometido (07/11): trocar a pílula por número gigante e tirar preço dos botões — a
  dona reprovou ("você mudou").
- **Sem "≈" e sem código BRL/MXN gigante no número.** Quem diz que é aproximado é a linha de baixo.
  Código da moeda só pequeno e só quando o símbolo é `$` puro (MXN, COP, ARS); `R$`, `€`, `£` dispensam.
  Nunca "Solo ≈R$52.28 BRL" — a dona achou feio.
- **Linhas de baixo sem destaque — o destaque é só o número local.** Fonte do corpo, peso regular.
  "Valor aproximado" é só uma informaçãozinha: pequena e cinza. O US$/€ logo abaixo, um pouco maior,
  em tom apagado (nunca preto forte nem cor de destaque). Fundo escuro: mesma hierarquia com o texto
  claro da página em opacidade baixa. Centralizadas com o preço. Referência visual aprovada pela
  dona: `≈ BRL 43` grande / `Valor aproximado en tu moneda` minúsculo cinza / `7,90 US$` cinza médio.
- **Formato do número no padrão do país:** BR `R$52,28` (pt-BR), MX `$177 MXN`.
- **Base do cálculo = o gateway da oferta (regra da dona 07/11/2026).** O aproximado tem que bater
  com o que a pessoa vai ver no checkout. Hotmart: usar a conversão da própria Hotmart (ela converte
  e mostra o preço local no checkout). Outro gateway (Mundpay, Cakto, Stripe...): achar como esse
  gateway converte e seguir igual; só sem jeito melhor, câmbio do dia (`open.er-api`). Sempre ter o
  bloco, qualquer checkout.
- Converte **todo** preço visível (plano, oferta, selo, botão, downsell, popup de saída). Riscado
  ("de") converte também, sem linhas embaixo dele. Preço dentro de botão: as 2 linhas vão logo abaixo
  do botão (ou abaixo do preço principal do mesmo card, se já houver).
- Texto da linha do meio no idioma da página: `Valor aproximado en tu moneda` (ES), `Valor aproximado
  na sua moeda` (PT), `Valeur approximative dans votre devise` (FR), `Approximate value in your
  currency` (EN).
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
