# Wiven — subir banner de checkout (Mídias)

Rota: Produto → Personalizar checkout → aba **Gatilhos** → toggle **Mídias** ON → **Adicionar mídia**.
Slots: "Acima do checkout" (topo), "Lateral do checkout", "Abaixo do checkout".
Banner topo desktop = Acima+Desktop; banner topo mobile = Acima+Mobile (2 mídias separadas).

Dialog "Adicionando mídia": Tipo(Imagem) · upload · Posição · Dispositivos(multi) · Ofertas(obrigatório).
Upload: `agent-browser --session wiven upload "input[type=file]" <arquivo.jpg>`.

## ARMADILHA (custou ~20 tentativas 2026-09-21)
Os dropdowns são HeroUI Select. Os **refs @eN do snapshot embaralham** a cada re-render e
os popovers de multiselect **não fecham** — qualquer clique/Escape seguinte re-alterna a opção
(Desktop volta a ficar marcado). Clicar por ref/texto é não-confiável aqui.

**Solução que funciona: dirigir por eval disparando eventos reais** (HeroUI sincroniza o React state
e reflete no <select> escondido, que dá pra ler pra confirmar):

```bash
# abrir um trigger pelo texto do label:
agent-browser --session wiven eval "(()=>{const b=[...document.querySelectorAll('button[data-slot=trigger]')].find(x=>x.textContent.includes('Ofertas'));b.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}));b.dispatchEvent(new PointerEvent('pointerup',{bubbles:true}));b.click();return 'ok'})()"
# clicar uma opção (portal role=option) pelo texto exato:
agent-browser --session wiven eval "(()=>{const o=[...document.querySelectorAll('[role=option]')].find(x=>x.textContent.trim()==='Completo');o.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}));o.dispatchEvent(new PointerEvent('pointerup',{bubbles:true}));o.click();return 'ok'})()"
# CONFERIR estado real (fonte de verdade = <select> escondidos):
agent-browser --session wiven eval "JSON.stringify([...document.querySelectorAll('select')].map(s=>[...s.selectedOptions].map(o=>o.text)))"
# => [[Tipo],[Posição],[Dispositivos...],[Ofertas]]
```
Multiselect Dispositivos: clicar a opção alterna (toggle). Ex.: pra Mobile-only, clique "Desktop" pra desmarcar.
Depois: botão **Adicionar** (eval por texto exato 'Adicionar'), depois **Salvar** (toast "Configurações salvas com sucesso").
"Ofertas*" em vermelho na lista é só o label do campo, não é erro. Confirme recarregando a página.

## GATE ANTI-DUPLICATA (regra 2026-09-24 — nunca subir banner repetido)
Já saíram 2 banners desktop + 2 mobile no mesmo produto (comprador vê banner dobrado).
Regra: **1 banner por (posição × dispositivo) por produto. Máximo 1 desktop + 1 mobile.**
ANTES de "Adicionar mídia": listar as mídias existentes do produto (aba Gatilhos → Mídias).
- Já existe uma na mesma posição+dispositivo → **substituir** (editar/excluir a antiga), nunca adicionar outra.
DEPOIS de Salvar e recarregar: contar as mídias. Esperado = 2 (1 desktop, 1 mobile).
Se >2 ou dispositivo repetido → excluir a sobra e recontar. Só reportar "banner ok" com a contagem conferida.
Reexecutar o fluxo após erro/timeout também duplica: sempre recontar antes de repetir.

## ARMADILHA 2 (2026-09-29, checkout Cigano): banner cadastrado mas NÃO aparece no checkout
Cada mídia tem o campo **Ofertas** e só aparece no checkout dessas ofertas. As 2 mídias do Cigano
estavam só na oferta JXE3KNA; o checkout vendido é `?offer=AQNS7ED` → sem banner. A lista não tem
"editar": ler as ofertas pelo fiber (`img` → 5× `.return` → `memoizedProps.offer/devices`), e se
estiver errado, **adicionar as novas com TODAS as ofertas e apagar as antigas** (lixeira), Salvar,
recarregar e recontar (=2). Prova só no checkout público com o `?offer=` real (desktop E mobile).
Upload sem agent-browser: CDP `DOM.setFileInputFiles` no `[role=dialog] input[type=file]`.
Janela do perfil minimizada = `visibilityState hidden` = animação de fechar dialog trava e
clique cai no overlay: `Browser.setWindowBounds {windowState:"normal"}` antes.

## ARMADILHA 3 (2026-09-29, Jiu-Jitsu): agent-browser upload trava em blob:, fluxo que funcionou

`agent-browser upload` (Playwright) não commitava — preview em blob: local, toast "Insira a mídia"
mesmo com arquivo "selecionado". Sem `websocat`/`pychrome` instalados: usar Node 22+ (tem `WebSocket`
global, zero deps) pra falar CDP puro: `fetch http://127.0.0.1:<porta>/json` pega `webSocketDebuggerUrl`
da page, manda `Browser.setWindowBounds{windowState:normal}`, `DOM.getDocument{depth:-1,pierce:true}`
(percorre children/contentDocument/shadowRoots pra achar `[role=dialog] input[type=file]`),
`DOM.setFileInputFiles{nodeId,files:[caminho]}`. Script pronto seguiu o padrão da receita (~70 linhas).
Cada upload precisa de dialog FRESCO: reaproveitar dialog de edição de mídia já salva não tem
`input[type=file]` (0 inputs) — sempre fechar com "Fechar" (não só Escape) e reabrir "Adicionar mídia".

Depois do upload: dropdown Dispositivos nasce com Desktop+Mobile marcados — pra 1 mídia por
dispositivo, ABRIR o dropdown e clicar na opção que quer TIRAR (clique = toggle, ex.: clicar
"Mobile" pra sobrar só Desktop). O clique final em "Adicionar" as vezes reabre visualmente o
popover Ofertas por cima (artefato de render) — não é bug de estado: conferir sempre pelo
`<select>` escondido (fonte de verdade), nunca confiar no screenshot do popover.
Depois de "Salvar", RECARREGAR a página e recontar as mídias — só assim confirma persistência real.
