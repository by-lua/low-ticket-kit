# Modelo Padrão — v1 (04/11/2026)

> **REGRA FIXA DA DONA (10/11/2026) — CONFIGURAÇÃO DA PÁGINA: IC SÓ NO CLIQUE QUE VAI PRO CHECKOUT (pixel Meta E Trackeador).** **O Modelo Padrão já vem configurado certo** (`modelos/modelo-padrao/index.html`, conferido 10/11/2026: botão do Básico `data-upsell` sem `data-tk-*`; Completo, botões do popup e saída com `data-plan` + `data-tk-value`/`data-tk-currency`; sem `fbq` de IC). Página feita a partir dele: **não reconfigurar, só CONFERIR** que isso se manteve (troca de valores, link de checkout por `data-plan`). Página fora do modelo: configurar igual.
> - Botão do Básico que só **abre o popup** de upgrade pro Completo mais barato: **sem** `data-tk-*`, **sem** `data-plan`, **sem** href de checkout (`data-upsell="1" href="#upgradepopup" role="button"`) e sem `fbq` próprio → 0 IC.
> - Botões do popup ("quero o Completo mais barato" / "sigo com o Básico"), botão do Completo na página e botão da oferta de saída: link real do checkout + `data-tk-value`/`data-tk-currency` com o valor DAQUELE botão → 1 IC no clique.
> - Popup de saída aparecer = 0 IC. Página não manda IC próprio (o Trackeador dispara; não duplicar).
> - Conferir antes de entregar: `scripts/qa-layout.js` + `low-gates-no-ar` › regra fixa do topo (contagem por botão no pixel Meta e no Trackeador).

**É a página padrão da casa, só nossa:** toda página nova parte daqui (a dona pede "Modelo Padrão"). Primeira oferta feita nele:
<Oferta Exemplo> FR (04/11/2026). Não depende de template de terceiros.

## Como usar
1. Copiar `index.html` + `img/` pra `OFERTAS/<slug>/site/`.
2. Trocar: textos (idioma da oferta), preços, `:root` (paleta/fontes do `DESIGN-SYSTEM.md`), imagens, `CONFIG.checkoutUrl`.
   Editar o `index.html` copiado (não há gerador; a página é editada direto).
3. QA obrigatório: `../../scripts/qa-layout.js` em 360×740, 375×667, 390×844, 1366×768, 1920×1080 → tudo `ok`.

> **Base de página nova = copiar o `index.html` deste modelo** (+ `img/`). Não há gerador: a página é editada direto.
> O gerador antigo está arquivado em `_arquivo/modelo-padrao-gerador-antigo-2026-11-06/`; não usar.

## Performance (regra 06/11/2026 — a página sai já otimizada)
A. **Fontes hospedadas, nunca Google Fonts.** O `<link>` do Google bloqueia a renderização (no navegador interno do
   Instagram em 4G atrasa o 1º paint e derruba "Vis. Página"). O template já traz `img/fonts/` (woff2 latin, `dmsans`
   variável 400-800 + Libre Baskerville) com `@font-face` + `font-display:swap` e `preload` das 2 principais. Fonte
   diferente da oferta → baixar o woff2 latin e trocar no `<style>`; nunca voltar ao `<link>` do Google.
   Fontes ficam em `img/fonts/` (o servidor já serve `img/` com cache de 1 ano; fora de `img/` o Dockerfile/allowlist barra).
B0. **Gate:** antes de subir, `../../scripts/qa-performance.js <url> --meta-id=<id>` tem que dar APROVADO (SKILL.md 9c).
B. **Imagens:** só hero com `fetchpriority=high` + `preload`; resto `loading="lazy"` com width/height. Antes do deploy
   rodar `../../scripts/otimizar-imagens.py <site/img>` (webp q75, só grava se ganhar ≥10%; <Oferta Exemplo>: 4,5→3,2 MB).
C. Cache: `img/` imutável de 1 ano → imagem trocada = **nome novo** (senão o Cloudflare serve a velha).
D. **Paleta = a da oferta modelada** (não o vermelho da casa; vermelho só na barra de urgência). A pergunta
   "manter ou mudar" com sugestões vem antes de montar (`SKILL.md` § 2a); as sugestões de paleta têm que combinar
   com o tema da oferta (nunca cor aleatória ou da casa).

## Ordem das seções
barra → hero → dor (6 chips + ponte) → prévias (carrossel) → mecanismo (4 passos + frase + botão) → uso na vida real
(carrossel) → pitch intermediário (mockup diferente + botão) → pra quem é (6) → **o que recebe** (`#recebe`) → bônus
(cards) → [depoimentos: só reais] → oferta (2 planos + garantia) → passos de acesso → FAQ → fecho → rodapé → popup.
Antes × depois: só quando material técnico vira visual.

## Mudanças da casa (não desfazer)
1. **Barra de urgência vermelha e fixa** (`position:sticky;top:0`), data do dia por script.
2. **Hero centralizado:** pill → headline → mockup no meio → subheadline → **bullets com ✓ em círculo**
   (organizado, nunca cards espalhados nem parágrafos empilhados) → **pílula com o preço do plano mais barato**
   (« seulement 5,90 € ») **logo acima do botão** → botão → **linha de confiança** (✓ acesso imediato · ✓ garantia N dias ·
   ✓ pagamento seguro).
3. **Hero cabe na tela até o botão, sem rolar**, em todo celular (até 375×667) e PC: mockup com `max-height` em vh,
   em tela baixa some o 3º bullet e o pill do topo.
4. **Botão do hero → seção "o que recebe" (`#recebe`).** Botões do meio → `#oferta`. Só o botão do card de preço vai pro checkout.
5. Fundos claros; paleta e fontes no `:root`; cores verdes fixas do template trocadas (hover e sombra do botão).
6. **Botões quebram linha** (sem `white-space:nowrap`) e aguentam texto +45% (tradução automática do navegador).
7. **Imagem do "o que recebe"** com altura automática + espaço antes do card (o template fixava 420px e cortava).
8. **Planos padrão Mapa do Tarot:** Básico sem imagem, menor e centralizado na altura do Completo, itens que não leva
   riscados (✗), seta « oferta ainda melhor ↓↓↓ » no celular; Completo com imagem (máx. ~280px), selo "O preferido",
   bônus principal em caixa destacada, "Bônus exclusivos" com 🎁, preço riscado → preço.
9. **Garantia** dentro da seção de oferta, logo abaixo dos planos: linha "✉ Acesso imediato", **selo dourado do banco `img/selos-garantia/` (GPT, alpha; criar se faltar idioma/prazo) com brilho e
   fundo transparente**, "Garantia incondicional · Risco zero" + texto.
10. **Passos de acesso:** headline + subheadline + bolinha numerada em cima de cada passo (nunca colada no título).
11. Sem seção "pensado pro país X" (a página já está no idioma do país).
12. Popup de saída com o básico mais barato; `CONFIG.checkoutUrl` único.
13. QA de layout (`qa-layout.js`): botão do hero acima da dobra, sem rolagem lateral, texto não vaza, texto não estoura
    botão, botão aguenta texto traduzido, nenhuma imagem coberta/cortada.
14. **Favicon** (`img/favicon.svg` + `favicon-32.png` + `apple-touch-icon.png`) na paleta da oferta — o QA acusa se faltar.
15. **Popup de upgrade no clique do Básico** (`#downsell`, padrão Mapa do Tarot): « leve tudo por quase o mesmo preço » — Completo num preço intermediário (básico < upgrade < completo), botão sim → checkout do upgrade, link "não, continuar com o básico" → checkout do básico.
16. **Popup de saída** (`#exitpopup`, padrão Mapa do Tarot): básico com desconto; 1x por sessão; PC = mouse sai pelo topo; celular = botão voltar (só depois de interação) ou 45s parada após ver os planos; nunca nos primeiros 8s, nem depois de clicar num checkout, nem com o de upgrade aberto. O QA acusa se faltar algum dos dois.
17. **Proporção do hero:** mockup GRANDE (max-height 44vh no celular, 46vh no PC, 35/33vh em tela baixa), texto pequeno (h1 ~22-36px, sub 13,5px, bullets 13px) — o mockup é o protagonista.
18a. **Imagem recortada = fundo TRANSPARENTE de verdade (regra da dona 07/11/2026):** selo de garantia, capas/mockups
   dos bônus e qualquer imagem "solta" sobre o fundo da página vão em WebP/PNG com canal alfa. Imagem gerada no GPT
   vem com fundo creme/branco embutido e vira **caixa branca atrás do selo/bônus** (erro real no <Oferta Exemplo> FR).
   Antes de publicar: `magick identify -format "%A" arquivo` tem que dar `Blend`/`True`; se der `Undefined`, recortar
   (`magick in.webp -alpha set -fuzz 9% -fill none -draw "color 0,0 floodfill"` nos 4 cantos, erode 1px) e conferir
   num fundo escuro. `drop-shadow` em imagem sem alfa desenha a sombra da caixa inteira.
18. **Barra de urgência fina:** 30px, 1 linha em qualquer tela (no celular o texto encurta, ex.: some o "+ 7 bonus").
19. **REGRA UNIVERSAL DA SEÇÃO « VEJA NO DIA A DIA / DANS LA VRAIE VIE »: o material precisa parecer REAL em uso por pessoas comuns, em situações normais da rotina. Impressos são folhas A4 de tamanho plausível, com espessura, proporção, perspectiva e manuseio naturais; celulares/tablets são aparelhos normais, com tela, escala e pegada reais. Usar as páginas verdadeiras da oferta; nunca pôster gigante no lugar de A4, tela inventada, mãos/anatomia impossíveis, pessoa com aparência artificial ou mockup com aspecto de montagem.** Cada card tem uma cena própria e diferente — pessoa, página, ambiente, ação e enquadramento. **No Modelo Padrão, usar 9 cenas distintas; nunca preencher os 9 cards repetindo 4 imagens ou duplicar a lista para simular variedade.** Conferir todos os cards, não apenas os primeiros visíveis, comparando o tamanho da folha/aparelho com mãos, rosto e objetos reais. Adaptar a direção das artes ao produto e à identidade de cada oferta. Cópias de imagem para loop não contam como cenas novas. Fotos em **4:5 (900×1125)**, com `height:auto` no `img`. **Referências do <Oferta Exemplo> FR: `img/usage/<slug-da-oferta>/` (+ `contact-sheet.jpg`); são referência de abordagem, não aprovação automática de realismo/escala nem fotos para reutilizar em produtos diferentes.**
20. **Preço de página internacional = valor na moeda da oferta + aviso cinza embaixo (regra da dona 09/11/2026, SEM script de conversão):**
   todo lugar em que o preço aparece (pílula do hero, card de plano, popups, downsell) leva logo abaixo
   `<div class="price-note">* Le prix est converti dans votre devise locale lors du paiement.</div>` (~11px, peso 400, cinza,
   alinhado com o preço: esquerda no card de plano, centro no hero/popup). Já vem pronto no template; ao trocar de idioma
   troque o texto (ES/PT/EN em `low-ticket/references/PRECO-MOEDA-LOCAL.md`). Sem `/painel/api/fx`, sem `fx-geo.json`, sem
   `data-eur`. Oferta de UM país só (BR em R$, AR em ARS, PT em €): apagar os `.price-note`. Regra completa:
   `low-ticket/references/PRECO-MOEDA-LOCAL.md`.
