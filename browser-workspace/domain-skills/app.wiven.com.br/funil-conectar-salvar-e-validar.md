# Funil: conectar aresta, salvar e validar persistência (aprendido 01/10/2026)

Rodada Mapas Visuais de Eletrotécnia: 5 funis (principal + 4 order bumps) com página final
externa + 1 aresta cada, todos conferidos após reload. Este arquivo registra o método que
funcionou de ponta a ponta e o que NÃO funciona (marcado ✗), pra não repetir a bagunça.

Rota do editor: `/panel/products/<productId>/funnel`.
⚠ O `/checkout` NÃO é o editor de funil — é personalização de checkout (Aparência/Pagamento/
Order Bumps/Upsell-Downsell/Gatilhos). Às vezes uma rota renderiza o conteúdo da outra por
carregamento atrasado; confiar SEMPRE no `location.pathname`, não nos tabs que aparecem.

## 0. Estado inicial (padrão, não é bug)

Ao abrir `/funnel`:
- Existem 2 nós (FRONT do produto + THANKYOU "Página final"), mas com
  `style.visibility:hidden` e `innerText=""`.
- `.react-flow__edge` = 0 **mesmo com a aresta já salva** — a 1ª medição sempre dá 0 falso.
- Às vezes os tabs ainda são os da rota anterior.

## 1. Forçar renderização antes de medir (SEMPRE)

Trocar de aba dispara o re-render do canvas:

```sh
agent-browser --session wiven eval "(()=>{const t=[...document.querySelectorAll('[role=tab]')].find(x=>x.innerText.trim()==='Desempenho');t&&t.click();return 'o'})()"
sleep 3
agent-browser --session wiven eval "(()=>{const t=[...document.querySelectorAll('[role=tab]')].find(x=>x.innerText.trim()==='Editor do funil');t&&t.click();return 'i'})()"
sleep 5
agent-browser --session wiven eval "JSON.stringify({edges:[...document.querySelectorAll('.react-flow__edge')].map(e=>e.dataset.id),nodes:[...document.querySelectorAll('.react-flow__node')].map(n=>n.innerText.replace(/\n+/g,' | ').slice(0,45))})"
```

**Regra: contagem de edge só é confiável DEPOIS do ciclo de aba. Medir antes = 0 falso =
conclusão errada de "não persistiu".**

## 2. Preparar o canvas pra conectar

```js
document.querySelectorAll('.react-flow__node').forEach(n=>{n.style.visibility='visible'});
document.querySelectorAll('.react-flow__handle').forEach(h=>{h.style.pointerEvents='all'});
['aside.w-96','#editingPanel'].forEach(sel=>document.querySelectorAll(sel).forEach(x=>x.style.display='none'));
```

Por quê (cada um é um bloqueio real desta rodada):
- **nós `visibility:hidden`** → handle não recebe evento; `elementFromPoint` volta
  `react-flow__pane` e o clique real não faz nada.
- **`.react-flow__handle.source` nasce com `pointer-events:none` computed** (classes
  `source connectablestart connectableend`, SEM `connectionindicator` — o target tem).
  Sem o force, `pointerdown` NUNCA chega no handle (confirmado com listener de captura em
  `window`: evento chegava no handle mas o React Flow não iniciava conexão — é o pe:none).
  Force `style.pointerEvents='all'` (e opcionalmente `classList.add('connectionindicator')`).
- **drawer "Adicionar etapa" (`aside.w-96`, x≈859..1243 em scale 1), `#editingPanel` e o
  preview do checkout** ficam POR CIMA dos handles direitos (S geralmente x≥1000). ✗ Tentar
  clicar "em volta" do overlay: clique cai no painel. Escondê-los (`display:none`) — esconder
  não muda o layout do canvas (são overlays absolutos).
- Zoom Out (`button[aria-label='Zoom Out']`) ajuda mas **não resolve sozinho**: o drawer
  continua cobrindo em qualquer scale. Zoom sem esconder overlay = handle ainda inatingível.

## 3. Click-to-connect (único método que funciona; drag não cria edge em nenhuma variante)

1. Medir centros: `getBoundingClientRect` do `.react-flow__handle.source` e `.target`.
2. `elementFromPoint(cx,cy)`:
   - volta o handle ou `react-flow__pane` → ok pra clicar;
   - volta elemento do drawer/panel (`aside`, `w-96`, `h-[500px] w-full rounded-lg`…) →
     voltar ao passo 2 da seção acima.
3. CDP real, com sleep entre:

```sh
agent-browser --session wiven mouse move $SX $SY; sleep 1
agent-browser --session wiven mouse down; agent-browser --session wiven mouse up; sleep 2
agent-browser --session wiven mouse move $TX $TY; sleep 1
agent-browser --session wiven mouse down; agent-browser --session wiven mouse up; sleep 3
```

✗ **Dispatch sintético** (PointerEvent/MouseEvent direto no handle) — chega no DOM, mas o
React Flow não inicia a conexão. Só mouse real do CDP.

## 4. Salvar (e a armadilha estado ≠ DOM)

Botão com texto exato **"Salvar funil"**:

```js
const b=[...document.querySelectorAll('button')].find(x=>x.innerText.trim()==='Salvar funil');b.click();
```

POST `/panel/products/<id>/funnel` com body `[productId, nodes, edges, settings]` →
toast **"Funil atualizado com sucesso"**.

⚠ **O edge pode estar no PAYLOAD do POST mesmo com `.react-flow__edge` = 0 na DOM** (neste
canvas estado React e DOM divergem). Pra depurar, hook de fetch antes de salvar:

```js
window.__cap=null;const of_=window.fetch;
window.fetch=async(...a)=>{const u=String((a[0]&&a[0].url)||a[0]);
 if(u.includes('/funnel')&&((a[1]&&a[1].method)||'GET')==='POST'){try{window.__cap=JSON.parse(a[1].body)}catch(e){}}
 return of_(...a);};
```

Depois do clique: `window.__cap[2]` = array de edges — se tem a aresta ali, o save vai
gravar. ✗ Concluir "perdeu a aresta" pela DOM antes do reload.

## 5. Validar persistência (ciclo obrigatório)

`open` de novo na URL do funil → sleep 13 → ciclo de aba (seção 1) → edges = 1.
Aresta esperada: `xy-edge__<frontNodeId>next-upsell-<thankyouNodeId>previous-upsell`.
Se voltou 0 no 1º ciclo, repetir o ciclo de aba (pode ser render atrasado) antes de refazer
a conexão — refazer às cegas cria edge duplicado no estado.

## 6. Página final externa (conferir antes de salvar)

Engrenagem do nó final (só aparece em hover): dispatch sintético **funciona** no botão gear
(`pointerdown`→`pointerup`→`click`, bubbles:true) e abre `#editingPanel`. Ler:

- `input[type=checkbox]` = true (switch "Usar página final externa")
- `input[type=text]` = `<site>/painel`

O save persiste o rascunho do painel junto — conferir a URL ANTES de clicar Salvar, senão
grava o que estava no formulário (que pode ser o de outro produto se a página trocou).

## 7. Fechamento comprovado nesta rodada (01/10/2026)

5 funis → 1 aresta + página final `https://mapaseletricos.leadgo.dev/painel` cada:
- principal `cmulrrekz014801ookjczraz1` → `xy-edge__glhz12lo8wnext-upsell-1hng4gcr07previous-upsell`
- bump Segurança `cmulrtppu015c01oom5b5svwr` → `xy-edge__jtwip6irydnext-upsell-kpbvsj8u2eprevious-upsell`
- bump Medição `cmulruab9015l01oop6kbb2sj` → `xy-edge__dc41nhv7q2next-upsell-fk6iaiyguxprevious-upsell`
- bump Comandos `cmulrutgf016001oowqdff7o3` → `xy-edge__iah8zgbaxknext-upsell-pb4gz4jaxtprevious-upsell`
- bump Combo `cmulrvglr016l01ooihpjhe0q` → `xy-edge__nad2r8ny5onext-upsell-9ggm8po0fzprevious-upsell`
