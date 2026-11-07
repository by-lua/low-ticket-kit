# Preço na moeda do visitante (oferta vendida em vários países)

**Regra da dona (05/10/2026, formato revisto 07/11/2026):** toda página de vendas de oferta vendida
para vários países (Mundpay, Hotmart, Zenith, qualquer gateway multi-moeda) mostra o preço **na moeda
local do visitante em cima, grande**, embaixo **"valor aproximado na sua moeda"** e embaixo disso,
**menor**, o valor base na moeda em que o produto está cadastrado (US$, €). Motivo: ajuda muito a conversão.
O visitante entende o preço na moeda dele e o checkout confirma.

Vale para **qualquer país** do visitante (regra da dona 06/10), não só LATAM: nunca lista fixa de países.

Não vale para oferta de um país só que já vende na moeda local (ex.: BR em R$ na Wiven).

## Como fica — bloco de 3 linhas, SEMPRE (regra da dona 07/11/2026)
```
R$ 43                              ← linha 1: valor local GRANDE, estilo de preço da página
Valor aproximado na sua moeda      ← linha 2: pequena, cor apagada, idioma da página
US$ 7,90 · valor base              ← linha 3: pequena, moeda do cadastro
```
- **O valor local é o protagonista.** O "≈" sai do número grande (ou fica bem menor e discreto);
  quem diz que é aproximado é a linha 2. Código da moeda (BRL, MXN) no máximo pequeno, ou só o
  símbolo (R$, $). Nunca "≈ BRL 43" em fonte gigante — a dona achou feio.
- **Segue o design da página:** mesma fonte, peso e cor do preço que a página já usa. Linhas 2 e 3
  na fonte do corpo, ~13-14px, **sem destaque: preto normal, peso regular** (em fundo escuro, a cor
  do texto claro da seção). Nada de estilo genérico colado por cima.
- **Formato do número no padrão do país:** BR `R$52,28` (pt-BR), MX `$177 MXN`. Código da moeda só
  quando o símbolo é `$` puro; `R$`, `€`, `£` dispensam.
- **Base do cálculo = o gateway da oferta (regra da dona 07/11/2026).** O aproximado tem que bater
  com o que a pessoa vai ver no checkout. Hotmart: usar a conversão da própria Hotmart (ela converte
  e mostra o preço local no checkout). Outro gateway (Mundpay, Cakto, Stripe...): achar como esse
  gateway converte e seguir igual; só sem jeito melhor, câmbio do dia (`open.er-api`). Sempre ter o
  bloco, qualquer checkout.
- **Todo lugar onde aparece preço usa esse bloco** (plano, oferta, downsell, popup de saída,
  selo "Desde…"). Riscado ("de") converte e fica ao lado do valor grande, sem "≈".
- **PROIBIDO preço convertido inline** em chip, selo ou texto de botão (ex.: "Solo ≈R$52.28 BRL"
  dentro de pílula — a dona reprovou). Botão leva só o CTA ("Quiero empezar ahora →"); o bloco de
  3 linhas fica acima dele. Selo/chip que precisa de preço vira o bloco de 3 linhas ou perde o preço.
- Texto da linha 2 no idioma da página: `Valor aproximado en tu moneda` (ES), `Valor aproximado na
  sua moeda` (PT), `Valeur approximative dans votre devise` (FR), `Approximate value in your
  currency` (EN). Linha 3: `valor base` / `valeur de base` / `base price`.
- Sem conversão (mesma moeda do cadastro, país desconhecido, câmbio fora): só o valor base grande,
  linhas 2 e 3 escondidas.
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
