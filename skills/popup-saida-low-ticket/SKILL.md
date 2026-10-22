---
name: popup-saida-low-ticket
description: Monta, publica e testa o popup de saída (exit-intent) de página de vendas low ticket com oferta mais barata (ex.: básico R$27,90 → R$17,90) — oferta "Exit" no checkout (Wiven), modal no index.html, gatilhos desktop/mobile sem disparo falso, InitiateCheckout com valor certo e bateria de 8 cenários com prova visual. Use quando o usuário pedir popup de saída, exit popup, intenção de saída, "oferta pra quem vai sair", ou reclamar que o popup aparece na hora errada.
---

# Popup de saída — low ticket

> **TROCAR PÁGINA (14/10/2026):** publicar index.html novo com o popup = rodar
> `adstrackeador pagina comparar <atual> <nova>` ANTES, pra confirmar que o
> bloco fbq, o loader do Trackeador e o script do popup foram levados pra
> página nova. Nunca publique página sem rastreio.

Receita provada no Mapa do Tarot BR (mapadotarot.leadgo.dev, commits b771ae0 + 33877c5, 28/09/2026).
Para CRO geral de popup (copy, frequência, tipos), ver `popup-cro`. Esta skill é a mecânica que já funcionou no nosso stack.

## 1. Oferta no checkout (antes do código)

- Criar uma **oferta nova "Exit"** no MESMO produto do plano que o popup vende (entrega igual, não precisa novo produto nem nova entrega). Wiven: Produto → Ofertas → Adicionar oferta → nome "Exit", preço, moeda Real, Nacional → Salvar. Pegar o código (`?offer=XXXXXXX`).
- Preço: abaixo do menor plano da página (padrão oferta nova: básico 17,90 → exit 16,90; tabela em `criacao-low-ticket-mvt/references/CONSTRUCAO.md` › PREÇO PADRÃO BR). Nunca abaixo do downsell se houver, sem pedido do dono.
- Conferir no print da lista de ofertas que o preço salvou (curl no checkout Wiven não mostra preço, a página renderiza por JS).
- Wiven pede 2FA por e-mail (contact@seudominio.com): código vence em minutos. Se o pane travar no 2FA, pedir ao humano que responda **direto no pane que pediu** e confira o campo depois (código colado em outro lugar não chega).

## 2. Modal (HTML)

- `<div id="exitpopup" role="dialog" aria-modal="true" style="display:none; position:fixed; inset:0; z-index:9998; ...">` com: selo "Espera", título "Espera! Antes de sair…", 1 linha de valor, caixa com preço riscado + preço novo, botão pro checkout com `?offer=<código exit>`, link "Não, obrigado".
- Fecha no X, no "Não, obrigado" e no clique fora (backdrop). Trava scroll do body enquanto aberto.
- Usar os tokens do DESIGN-SYSTEM da oferta (cores/fontes), nada inventado.

## 3. Gatilhos (JS) — regras que evitam disparo falso

```js
var KEY='<oferta>_exit_shown', START=Date.now(), MIN_DELAY=8000, INACTIVITY_MS=45000;
// canShow(): não mostrou nesta sessão (sessionStorage) && não clicou em checkout
//            && já passou MIN_DELAY && downsell/outro modal não está aberto
```

1. **Desktop — mouse sai pelo topo:** registrar `mouseleave` com `clientY <= 0` **só se**
   `matchMedia('(hover: hover) and (pointer: fine)').matches`.
   BUG real: no celular, tocar/rolar gera `mouseleave` sintético com clientY 0 → popup abria ao rolar.
2. **Mobile — botão voltar:** `history.pushState({guard:true})` + `popstate` **só depois da 1ª interação real** (`touchstart`/`click` com `{once:true}`), e no popstate ignorar se `ev.state && ev.state.guard` (é a entrada no guard, não o voltar). Depois de abrir, re-empurrar o guard.
   BUG real: pushState no load → webview do Instagram/Facebook e Safari disparavam popstate espúrio na rolagem.
3. **Mobile — inatividade:** 45s parado DEPOIS de ver os planos (IntersectionObserver no `.plan-card`, threshold .3); `touchstart`/`scroll`/`click` resetam o timer (rolar nunca abre).
4. Nunca abrir depois de clicar em qualquer link de checkout (listener de click em captura marcando flag).
5. 1x por sessão: `sessionStorage`, com try/catch.
6. **Guarda de clique em QUALQUER clique do documento (desktop E mobile) — cobre mouseleave E popstate:** clicar num CTA que só rola a página (`href="#oferta"`, âncora da 1ª dobra) dispara DOIS falsos-positivos diferentes, não um só:
   - **Desktop:** o salto de scroll gera `mouseleave` sintético com `clientY<=0`.
   - **Desktop E mobile (causa real, mais séria):** o back-guard (`armBackGuard`/`r()`) arma no PRIMEIRO clique/touch do documento (`{once:true}`) chamando `history.pushState({...Exit:true})`. A navegação pra âncora que o PRÓPRIO clique disparou dispara `popstate` com `state=null` — o handler lê isso como "o usuário apertou voltar" e abre o popup, mesmo sem nenhuma saída real. **Essa é a causa que mais gera falso-positivo**, porque qualquer CTA com `href="#algo"` arma e dispara no mesmo clique.
   - **Fix:** `var clickGuardUntil = 0;` + listener de `click` em captura no `document` (SEM filtrar por classe — página pode não usar `.btn`, ex. Tailwind) arma `clickGuardUntil = Date.now()+1200`. O handler de `mouseleave` ignora enquanto `Date.now() < clickGuardUntil`, e o handler de `popstate` também: `if (ev.state && ev.state.xxxExit) return; if (Date.now() < clickGuardUntil) return; openExitPopup();`.
   - **Nunca filtrar a guarda por seletor de classe** (`a.btn, button.btn`) — bateu no JJ/Tarot (usam `.btn` próprio) mas falhou silenciosamente na Elétrica (Tailwind, sem `.btn`). Guarda em QUALQUER clique, sem seletor.
   BUG real (JJ Sem Força → Mapa do Tarot BR/PT/ES → Elétrica, 14/10/2026): clicar só no CTA da 1ª dobra abria o popup na hora — reproduzido com teste headed (stack trace via `window.openExitPopup` wrapped confirmou `popstate` como gatilho, não `mouseleave`). Corrigido em todos os arquivos das 3 ofertas; teste headed desktop + mobile (iPhone 14 emulado) confirmou falso-positivo bloqueado e exit-intent real preservado nos 3 domínios.

Código completo de referência: `OFERTAS/mapa-do-tarot/site/index.html` (bloco "Exit-intent popup").

## 4. Pixel (gate de eventos do projeto)

**⚠️ Confira primeiro se o Trackeador é o DONO do IC deste host** (`capi_ic_hosts`
— skill `trackeador` § "InitiateCheckout — dono em sites novos"). Se for (caso
do Mapa do Tarot desde 26/09/2026), o pixel core já detecta o clique no botão
do popup sozinho (link decorado cross-domain pro checkout) e dispara IC no
browser + CAPI com o MESMO event_id, deduplicado pelo Meta — **NÃO adicione o
código exit num handler de InitiateCheckout próprio do site.** Foi assim que o
Mapa do Tarot contou IC em dobro/triplo: o site mandava um IC com eventID
aleatório (fbq + beacon direto pra `facebook.com/tr`, que ignora o wrap de fbq
do Trackeador) AO MESMO TEMPO que o Trackeador mandava o dele — achado e
corrigido em 28/09/2026 (commit "remove InitiateCheckout duplicado do site").
- Site NÃO é dono do IC (checkout com CAPI própria, sem Trackeador nesse host):
  adicionar o código exit no mapa de valores do handler de InitiateCheckout
  (ex.: `VALUES = {..., '7FJCQSC': 17.90}`), currency do mercado, e esperar o
  evento sair antes de navegar (setTimeout curto de 150ms cortava o request —
  bug corrigido no edce0bc; usar callback/beacon ou delay seguro).
- Site É dono do Trackeador: só cadastrar o value/offer novo em `VALUES` se o
  handler ainda mandar **AddToCart** (sem eventID, sem CAPI — isso pode ficar);
  não adicione o código exit em nenhum lugar que dispare InitiateCheckout.
  O link do popup leva `data-tk-value` (preço exit) e `data-tk-currency`: é daí
  que o Trackeador tira o value do IC (browser + CAPI). Sem isso, o IC sai sem valor (29/09/2026).
- **Botão que só ABRE popup (ex.: "QUERO SÓ O BÁSICO" → popup de upgrade) não pode
  ter href de checkout.** `<a href="checkout...">` com `preventDefault` no onclick
  ainda conta como IC pro Trackeador (detecta pelo href) → IC no clique + outro IC
  no botão do popup = dobro. Padrão: `href="#upgradepopup" role="button"`, sem
  `data-tk-*`; o IC sai só nos links de checkout de DENTRO do popup (cada um com
  `data-tk-value`/`data-tk-currency` do próprio preço). Caso real: Mapas
  Elétricos, 05/10/2026, commit cc129f7.
- Provar no ar (os dois casos): PageView no load + 1 IC (não 2, não 3) com
  Integração "Várias" no Gerenciador de Eventos, no botão do popup e em todos
  os outros botões de checkout — nunca 2 eventIDs diferentes pro mesmo clique.

## 5. Deploy

Commit + push na main. Conferir no ar com `curl <url> | grep` do trecho novo (ex.: `pointer: fine`). Mapa do Tarot: se o Coolify não publicar em ~3 min, `coolify deploy uuid agbuxhags13d3ku8mvm13pxe --force` (nunca `coolify app list/get` sem filtro).

## 6. Bateria de teste (obrigatória, navegador VISÍVEL, sessão limpa por cenário)

| # | Dispositivo | Ação | Esperado |
|---|---|---|---|
| D1 | Desktop 1366x768 | esperar 10s, mouse real sai pelo topo | ABRE |
| D2 | Desktop | repetir na mesma sessão | não abre |
| D3 | Desktop | sair pelo topo antes de 8s | não abre |
| D4 | Desktop | só rolar a página | não abre |
| M1 | iPhone + Android (touch) | rolar página inteira 3x | não abre |
| M2 | Mobile | tocar, 10s, voltar | ABRE e fica na página |
| M3 | Mobile | parar 50s nos planos | ABRE |
| M4 | Mobile | clicar checkout, voltar | não abre |

- Print por cenário em `prints/teste-exit-<id>.png` + `eval` de `#exitpopup.style.display`.
- **O orquestrador abre os prints dos cenários ABRE.** Pegadinha real: print de 5 KB saiu preto e o pane reportou "passou". Print pequeno demais = refazer.
- Worker de teste = Sonnet (Haiku falha na captura).
