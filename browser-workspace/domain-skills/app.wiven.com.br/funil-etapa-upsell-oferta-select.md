# Funil de vendas — selecionar "Oferta desta etapa" no nó Upsell — app.wiven.com.br

**Perfil / porta CDP:** `wiven` / 9254
**Ferramenta padrao:** browser-harness (agent-browser falha sempre neste campo especifico — ver abaixo)
**Ultima validacao:** 2026-09-28
**Estado:** fragil — recipe funciona ~1 em cada 4-5 tentativas, mesma sequencia exata. Nao confie sem reconferir depois.

## O que é

Ao adicionar um produto como etapa no Funil de vendas (Produtos → produto → Funil de vendas →
Adicionar etapa → Produtos → escolher produto), o node vira tipo **"Upsell"**, com:
- campo obrigatorio **"Oferta desta etapa"** — combobox que busca ofertas do produto vinculado
- switch **"Usar página externa no upsell"** — liga campo "Link da página externa" + botão
  "Personalizar botões" (textos "Comprar"/"Não, obrigado", cores, prévia)
- handles do node: `previous-upsell`/`next-upsell` (verde, aceito) e `previous-downsell`/
  `next-downsell` (vermelho, recusado) — `Página final` só tem handle `previous-upsell`
  (não hà target de downsell dedicado nela; o path de recusa fica sem destino óbvio, não
  testado até o fim).

Salvar o funil (`Salvar funil`) fica bloqueado com **"Existem etapas sem oferta selecionada"**
até essa combobox fixar um valor.

## Pre-condições

- perfil no ar: `~/.claude/bin/browsers.sh wiven`
- login já persistido
- estar na aba **Funil de vendas** do produto, com o node Upsell já no canvas e o painel
  lateral dele aberto (clicar no node)

## O problema

`agent-browser`/`click()`/`dispatchEvent(new MouseEvent('click'))` **nunca** fixam a seleção
nesse campo especifico (diferente de TODOS os outros combobox do painel Wiven — tipo,
categoria, garantia, moeda — que funcionam com sequência completa
pointerdown→mousedown→pointerup→mouseup→click via `dispatchEvent`).

Causa raiz (confirmada via React fiber): a linha da opção (`.cursor-pointer` dentro do
listbox, achado por `el.closest('.cursor-pointer')` a partir do texto da oferta) só tem
`onMouseDown` (não `onClick`). O handler é `V=>{V.preventDefault(),ee(I.id)}` — só reage a
um **mousedown real**, e mesmo assim só commitou de fato quando usei
`Input.dispatchMouseEvent` cru do CDP (não JS `dispatchEvent`).

`fetchData('')` do combobox (chamado via fiber) retorna a lista real de ofertas do produto:
```js
{"success":true,"data":{"items":[{"id":"<CODIGO_OFERTA>","name":""}]}}
```
Se a oferta não tem "Nome da fatura"/nome próprio, aparece como **"Sem nome"** na lista —
não é bug, é só falta de nome (usar o código da oferta pra confirmar qual é).

## Receita que funcionou (uma vez, não reproduzível 100%)

```python
# BU_CDP_URL=http://127.0.0.1:9254, sessão anexada ao tab certo (switch_tab)
import time, json

# 1. Achar e clicar o trigger do campo "Oferta desta etapa"
res = cdp("Runtime.evaluate", expression="""
(function(){
  const labels = [...document.querySelectorAll('*')].filter(n=>n.children.length===0 && n.textContent.trim()==='Oferta desta etapa');
  const container = labels[0].closest('div');
  const trigger = container.querySelector('input');
  const rect = trigger.getBoundingClientRect();
  return JSON.stringify(rect.toJSON());
})()
""", returnByValue=True)
tr = json.loads(res['result']['value'])
click_at_xy(tr['x']+150, tr['y']+10)   # abre a lista
time.sleep(0.5)

# 2. Achar a linha clicável da oferta (NÃO o texto, o .cursor-pointer ancestral)
res = cdp("Runtime.evaluate", expression="""
(function(){
  const el = [...document.querySelectorAll('*')].find(n=>n.textContent.trim()==='<TEXTO_DA_OFERTA_NA_LISTA>' && n.children.length===0);
  const row = el.closest('.cursor-pointer');
  const rect = row.getBoundingClientRect();
  return JSON.stringify(rect.toJSON());
})()
""", returnByValue=True)
r = json.loads(res['result']['value'])
x, y = r['x']+160, r['y']+18

# 3. mousePressed CRU do CDP, esperar, mouseReleased CRU no MESMO ponto
cdp("Input.dispatchMouseEvent", type="mousePressed", x=x, y=y, button="left", clickCount=1)
time.sleep(0.4)
cdp("Input.dispatchMouseEvent", type="mouseReleased", x=x, y=y, button="left", clickCount=1)
time.sleep(0.6)

# 4. Conferir: node não deve mais mostrar "Sem oferta selecionada", banner some
cdp("Runtime.evaluate", expression="document.querySelector('[data-id=\"<NODE_ID>\"]').innerText", returnByValue=True)
```

## Falhas observadas (o que NÃO funciona / cuidado)

- **Reload de página perde tudo que não foi salvo** — inclusive nodes/edges recém-montados.
  Se vai mexer nesse campo, monte o resto do funil (nodes + edges) **primeiro**, offer/toggle
  **por último**, porque reconectar edges depois de setar a oferta às vezes reseta o node e
  volta pra "Sem oferta selecionada" (observado 1x, não 100% reprodutível).
- **O dropdown fecha sozinho rápido** (parece <1-2s de inatividade). Se ler o rect da opção e
  demorar pra clicar, o clique cai no que estiver ATRÁS (uma vez cliquei sem querer no switch
  "Usar página externa no upsell" que ficava exatamente nas mesmas coordenadas da opção
  fechada — sempre confirme com `elementFromPoint` se o clique falhar).
- **`trigger.value = ''` direto via JS não reabre a lista nem limpa de verdade** (input
  controlado por React, assignment bypassa o estado).
- A mesma sequência exata (passo 1-3) funcionou uma vez e falhou ~4 vezes seguidas depois,
  inclusive logo em seguida, sem mudar nada visível. Não achei o gatilho determinístico.

## Recomendação

Se automatizar de novo: tentar em loop (3-5x) com verificação depois de cada tentativa,
parando no primeiro sucesso. Se for mexer manualmente (mouse real), deve funcionar de
primeira — a flakiness parece ser específica de clique sintético/CDP, não da UI em si.

## Alternativa não testada

Investigar se dá pra fazer POST direto pra API do funil com o body já contendo o
`offerId`/`offerCode` certo (bypassando o combobox inteiro) — não tentei por falta de
visibilidade do endpoint exato (não abri o painel de Network do CDP pra capturar o PUT/POST
do "Salvar funil").

## 2026-09-28 — tentativa de conectar edges (Tarot→Cigano→Página final), BLOQUEADA antes de chegar no combobox

Nem cheguei a tentar o select de oferta desta vez — travei no passo anterior (step 3 do
manual: arrastar os handles verdes pra conectar os nodes no canvas React Flow).

**Achado novo: a tela inteira do canvas do funil vem renderizada com `transform: rotate(90deg)`**
(perfil `wiven` porta 9254, janela real 500×806 — landscape forçado numa janela portrait).
Isso quebra qualquer automação que assuma eixos X/Y normais:
- `getBoundingClientRect()` de qualquer elemento (incl. os handles `.react-flow__handle`)
  continua retornando coordenadas de VIEWPORT corretas (pós-transform) — isso bateu com
  `elementFromPoint` sempre.
- MAS o PAN do canvas (arrastar o fundo/pane) usa os deltas de mouse **trocados e com sinal
  invertido**: um drag visual em X move o conteúdo em Y (mesmo sinal), e um drag visual em Y
  move o conteúdo em X (sinal invertido). Ou seja: `content_dx = -mouse_dy` e
  `content_dy = mouse_dx`. Isso me custou ~15 tentativas até perceber (cada drag que eu achava
  que ia conectar o handle só panava o canvas inteiro, porque a leitura de coordenada ficava
  obsoleta a cada pan acidental).
- Handles NUNCA foram agarrados corretamente: testei com listener real
  (`addEventListener('mousedown', ..., true)`) capturando `e.target.className` no ato — mesmo
  movendo o mouse pro centro exato do handle (`getBoundingClientRect` + `elementFromPoint`
  confirmando hit ANTES do down) o mousedown real (via `agent-browser mouse move/down`, CDP
  `Input.dispatchMouseEvent` por baixo) sempre registrou o alvo como
  `react-flow__pane draggable` — nunca o handle. Clicar no CORPO do node (não no handle de
  12px) funciona perfeitamente (mesmo listener confirmou hit correto). Então o problema é
  específico do hit-target pequeno (12×12 CSS px) do handle, não da rotação nem do mapeamento
  de eixo geral.
- Zoom in/out via `mouse wheel` funciona (aumenta o espaçamento entre handles), mas não
  resolvi se aumentar bastante o zoom (handle visualmente bem maior) destrava o hit — não
  cheguei a testar com zoom extremo por falta de tempo/orçamento na sessão.

**Não tentado:**
- Zoom extremo (>300%) antes do drag, pra aumentar a área de acerto do handle em px reais.
- `browser-harness` com CDP cru (`Input.dispatchMouseEvent` com `mousePressed`/`mouseReleased`
  discretos, sem "move" intermediário) — só cheguei a testar a CONEXÃO via `agent-browser
  mouse` (que já usa CDP por baixo, então provavelmente mesmo resultado). `browser-harness`
  pediu aprovação manual em `chrome://inspect` (popup "Allow remote debugging") que não
  consegui clicar sem mouse real do SO — ver seção "mouse real do SO" abaixo.
- Mouse REAL do sistema operacional (`ydotool`/`xdotool`) pedido pela dona explicitamente
  pra este caso: **não deu pra fazer no ambiente sandboxed desta sessão**. O Chromium do
  perfil `wiven` roda nativo em Wayland (`--ozone-platform=wayland`), não em XWayland — então
  `xdotool` (ferramenta X11) não enxerga a janela nem sua posição na tela (`xdotool search`
  não encontra o processo). GNOME Wayland não expõe geometria de janela pra clientes externos
  por segurança, e as vias alternativas testadas falharam: `org.gnome.Shell.Eval` desabilitado
  (unsafe mode off), `org.gnome.Shell.Screenshot` nega com `AccessDenied` (sem portal/permissão
  concedida numa sessão não-interativa), sem `grim`/`slurp`/`wlr-randr`/`kdotool` instalados.
  `ydotool` (uinput, funciona em qualquer compositor) FUNCIONARIA para mover/clicar, mas sem
  saber a posição real da janela na tela não dá pra converter coordenada de página em
  coordenada de tela com confiança — arriscado demais pra um clique em "Salvar funil"/toggle
  errado. Não tentei mais a fundo por causa disso (risco de quebrar o funil salvo).

**Recomendação pra próxima tentativa:** ou (a) fazer manualmente com mouse físico numa sessão
com acesso real à tela (RDP/VNC pro desktop, não só CDP), ou (b) instalar `grim`+`slurp` (ou
habilitar `org.gnome.Shell.Eval`) só pra ESSA tarefa pra permitir screenshot de tela cheia e
cálculo de offset janela-tela pro `ydotool`, ou (c) tentar zoom extremo (400-500%) + o mapeamento
de eixo documentado acima antes de desistir do drag sintético.

## 2026-09-28 (2ª rodada) — EDGES RESOLVIDO, combobox de oferta AINDA NÃO

### Causa raiz dos edges, e correção que funcionou 100%

1. **Alargar a janela primeiro.** Perfil `wiven` abre em 500×806 — é isso que forçava o canvas
   a renderizar `transform: rotate(90deg)` (landscape forçado numa janela portrait), o que
   quebrava qualquer cálculo de coordenada. Redimensionar via CDP puro resolve, `agent-browser`
   não tem comando de resize de janela:
   ```python
   # websocket-client já instalado em /tmp/wsenv (uv venv) nesta máquina
   import json, websocket
   ws = websocket.create_connection("ws://127.0.0.1:9254/devtools/browser/<ID de /json/version>", suppress_origin=True)
   # suppress_origin=True é OBRIGATÓRIO — sem isso Chrome rejeita com 403 "Rejected an incoming
   # WebSocket connection ... Use --remote-allow-origins"
   def send(method, params=None):
       ...  # id incremental, ws.send(json.dumps), ws.recv até bater o id
   targets = send("Target.getTargets")
   page = [t for t in targets["result"]["targetInfos"] if t["type"]=="page"][0]
   wid = send("Browser.getWindowForTarget", {"targetId": page["targetId"]})["result"]["windowId"]
   send("Browser.setWindowBounds", {"windowId": wid, "bounds": {"width": 1400, "height": 900}})
   ```
   Depois disso, recarregar `/funnel` — canvas vem RETO (sem rotação), coordenadas normais.

2. **Handle tem `pointer-events: none` em repouso — essa é a causa raiz de todas as falhas
   anteriores**, não a rotação (a rotação era um problema à parte, empilhado). Confirmado via
   `getComputedStyle(handle).pointerEvents === 'none'`. Um clique ou drag sintético (CDP ou
   Playwright) NUNCA acerta o handle porque ele literalmente não recebe eventos de ponteiro —
   `elementFromPoint` no centro exato do handle retorna o **node por baixo**, não o handle,
   mesmo com coordenada certa. Fix: forçar via JS antes de cada interação (é só hit-testing,
   não muda nada que é salvo; o handler React real do handle continua disparando normal):
   ```js
   document.querySelectorAll('.react-flow__handle').forEach(h => h.style.pointerEvents = 'auto')
   ```
   Reaplicar a cada leitura de coordenada (o React pode re-renderizar e resetar o style).

3. **Com pointer-events forçado + janela larga (sem rotação), o DRAG clássico funciona de
   primeira**: `mouse move` até o handle source → `mouse down` → 2-3 `mouse move` intermediários
   até o handle target → `mouse up`. Confirmei ANTES de cada drag que `elementFromPoint(x,y)`
   bate exatamente com a classe do handle esperado (senão a coordenada ficou obsoleta — o canvas
   dá pan sozinho quando o painel lateral (edição do node) sobrepõe fisicamente o node no canvas
   e o clique cai nesse painel em vez do handle; children de node fora da faixa ~x<860 na janela
   1400px ficam livres do painel).
   - **NÃO tentar click-to-connect (down+up sem movimento)** — testei com `agent-browser click`
     via seletor `[data-auto=...]` (Playwright real, actionability check passou) e via CDP cru
     idêntico ao passo 3 abaixo: NUNCA criou edge, mesmo com o alvo corretamente hit-testado.
     Só o DRAG (down → move → move → up) cria a edge. A entrada anterior deste arquivo que dizia
     "click real (down+up)" funcionar pra conectar node final provavelmente era, na verdade, um
     drag mal-lembrado.
   - Depois de conectar Tarot→Cigano e Cigano→Página final, sobra a edge antiga direta
     Tarot→Página final: selecionar clicando no **`.react-flow__edge-interaction`** (path
     invisível de 20px de largura, MUITO mais fácil de acertar que o `.react-flow__edge-path`
     visível de 3px) e apertar **Backspace** (`agent-browser press Backspace`). Confirma
     `classList.contains('selected')` antes de apertar.

### Combobox "Oferta desta etapa" — AINDA sem solução determinística (2ª sessão de tentativas)

Com o node já conectado (sobra só fixar a oferta), tentei nesta ordem, todas sem sucesso após
~7 tentativas cada:
1. `agent-browser click` no textbox pra abrir + CDP cru `mousePressed`/`mouseReleased` no centro
   da linha "Sem nome" (mesma receita documentada acima) — confirmei hit-test certo
   (`elementFromPoint` bate com a linha, `pointerEvents: auto`) e MESMO ASSIM nunca fixou.
2. Igual, mas com offset fixo `x+160,y+18` da linha (como a receita original recomendava, em
   vez do centro) — mesmo resultado.
3. Adicionar `mouseMoved` antes do `mousePressed` (hover explícito) + `buttons:1`/`buttons:0`
   nos eventos — mesmo resultado.
4. Chamar o handler `onMouseDown` do React DIRETO via fiber
   (`row[reactPropsKey].onMouseDown({preventDefault(){}, ...})`) — a chamada não deu erro mas
   também não mudou o estado (o node continuou "Sem oferta selecionada").

**Suspeita não confirmada:** esse componente é HeroUI/React Aria (stack do app), cujo
`usePress` propaga através de um sistema de gestos mais estrito que espera PointerEvent real
com sequência específica (não só MouseEvent), e pode ter proteção contra re-render/timing que
invalida a linha entre o `mousePressed` de abertura e o clique na opção. Não tive tempo de
confirmar isso nem de testar teclado (Tab até a opção + Enter/Space), que é o próximo passo
óbvio a tentar — accessible components React Aria quase sempre respondem bem a teclado real
mesmo quando o mouse sintético falha.

**Não fiz "Salvar funil" em nenhum momento** — funil real no ar ficou intacto o tempo todo.

## 2026-09-29 — RESOLVIDO de ponta a ponta (upsell Cigano no funil do Mapa do Tarot, salvo e conferido)

Tudo via CDP cru (`Input.dispatchMouseEvent` mouseMoved → mousePressed → mouseReleased), janela ~1920 px.
Script de apoio: websocket-client + `Runtime.evaluate`/`Input.*` na aba do /funnel (porta 9254).

**Causa raiz do "Oferta desta etapa" que "nunca fixava":** fixava sim. A oferta AQNS7ED tinha
**nome vazio** ("Sem nome"). O nó grava `settings.offer = {code:"AQNS7ED", name:""}`, mas a UI
mostra "Sem oferta selecionada" e o "Salvar funil" bloqueia com "Existem etapas sem oferta
selecionada" porque a validação olha o NOME. Correção: Produto do upsell → Ofertas → editar →
"Nome da oferta" (ex. `Upsell Cigano R$27,90`) → Salvar alterações. Depois RECARREGAR o /funnel
(o combobox cacheia a lista antiga; fechar/reabrir painel não basta) e selecionar de novo.
Conferir pelo fiber: `node.memoizedProps.data.settings.offer`.

**Conectar = click-to-connect com mouse CDP funciona** (3/3 na 1ª tentativa, 2 sessões):
click no `.react-flow__handle.source` (ex. `data-handleid=next-upsell` do Tarot) e depois click
no `.react-flow__handle.target` (`previous-upsell` do Cigano). Ramo recusou: `next-downsell` do
upsell → `previous-upsell` da Página final (sai edge vermelha). Não precisou forçar pointer-events
(o handle source ocupado vira `pointer-events:none`, é normal). Antes, apagar a edge antiga:
click no meio do `.react-flow__edge-path` (via `getPointAtLength`+`getScreenCTM`) → conferir
`.selected` → tecla Backspace (`rawKeyDown` com `windowsVirtualKeyCode:8`).

**Abrir o painel do nó upsell:** a engrenagem (`[data-id=<nó>] button`) só aparece e DESLIZA
(~70 px pra esquerda) com hover. Fazer mouseMoved no corpo do nó, esperar ~0.8 s, reler o rect do
botão e só então clicar. Se o edge de saída passar por cima, o `.react-flow__edge-interaction`
rouba o clique — dar pan no canvas antes.

**Pegadinhas:** pan acidental (drag no fundo) desloca tudo — sempre reler coordenadas. Campo de
busca de "Adicionar etapa" é o 1º `input` da página: `focus()` + `Input.insertText`. O perfil
9254 foi fechado por fora no meio do trabalho (sem salvar = perde tudo): montar e salvar numa
tacada só.

**Script do upsell 1 clique:** Configurações do funil → "Script do botão" = iframe
`checkout.wiven.com.br/ext/funnel/<funnelId>` + `app.wiven.com.br/scripts/product-funnel.js`,
ÚNICO pro funil (não por etapa). O script dá `alert()` se a página abrir sem
`OCB_SEC_TOKEN`/`OCB_FUNNEL_ID`/`OCB_FUNNEL_CURRENT_STEP_ID` na URL → só injetar quando os
params vierem (visita direta mantém link normal de checkout). Clique dentro do iframe não chega
na página: IC via `window blur` + `document.activeElement` = iframe → click sintético num wrapper
`[data-tk-cta][data-tk-value][data-tk-currency]` (Trackeador manda IC browser+CAPI).
Mapa do Tarot: funil `cmubuvy1503ql01pqfjt1sqsk`, nó Cigano `skqwh56xgr`.
