# Modelo Padrão LeadGo — v1 (04/11/2026)

**É a página padrão da casa:** toda página nova parte daqui (a dona pode pedir "Modelo Padrão" ou "estilo Fernando").
Crédito: nasceu do PaginaPro V1 de Fernando Oliveira (original convertido em `MODELOS/MODELOS-DE-PAGINA/fernando/index.html`,
só pra consulta) com todas as mudanças da casa. Primeira oferta feita nele: Calendrier Magique FR (04/11/2026).

## Como usar
1. Copiar `index.html` + `img/` pra `OFERTAS/<slug>/site/`.
2. Trocar: textos (idioma da oferta), preços, `:root` (paleta/fontes do `DESIGN-SYSTEM.md`), imagens, `CONFIG.checkoutUrl`.
   Ou editar `build_page.py` (gera o HTML a partir do CSS do template + overrides + conteúdo) e rodar.
3. QA obrigatório: `../../scripts/qa-layout.js` em 360×740, 375×667, 390×844, 1366×768, 1920×1080 → tudo `ok`.

## Ordem das seções
barra → hero → dor (6 chips + ponte) → prévias (carrossel) → mecanismo (4 passos + frase + botão) → uso na vida real
(carrossel) → pitch intermediário (mockup diferente + botão) → pra quem é (6) → **o que recebe** (`#recebe`) → bônus
(cards) → [depoimentos: só reais] → oferta (2 planos + garantia) → passos de acesso → FAQ → fecho → rodapé → popup.
Antes × depois: só quando material técnico vira visual.

## Mudanças da casa (não desfazer)
1. **Barra de urgência vermelha e fixa** (`position:sticky;top:0`), data do dia por script.
2. **Hero centralizado** como o do Fernando: pill → headline → mockup no meio → subheadline → **bullets com ✓ em círculo**
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
9. **Garantia** dentro da seção de oferta, logo abaixo dos planos: linha "✉ Acesso imediato", **selo dourado com brilho e
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
18. **Barra de urgência fina:** 30px, 1 linha em qualquer tela (no celular o texto encurta, ex.: some o "+ 7 bonus").
19. **REGRA UNIVERSAL DA SEÇÃO « VEJA NO DIA A DIA / DANS LA VRAIE VIE »: cada card precisa de uma cena própria e diferente — pessoa, página real do produto, ambiente, ação e enquadramento. No Modelo Padrão, usar 9 cenas distintas; nunca preencher os 9 cards repetindo 4 imagens, duplicar a lista para simular variedade, nem usar still-life genérico.** Adaptar a direção das artes do Fernando ao produto e à identidade de cada oferta; conferir todos os cards, não apenas os primeiros visíveis. O arquivo original do Fernando tem 4 imagens únicas e cópias para loop: **essas cópias não contam como cenas novas**. Fotos em **4:5 (900×1125)**, com `height:auto` no `img`. **Referências adaptadas do Calendrier Magique FR: `img/usage/calendrier-magique-fr/` (+ `contact-sheet.jpg`); são referência de abordagem, não fotos para reutilizar em produtos diferentes.**
