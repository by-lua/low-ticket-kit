# chatgpt.com — WORK MODE: lote de páginas de entrega (imagens individuais)

Validado 2026-09-21 (Mapa do Tarot, bônus 1-4, perfil gpt-conta / 9229).

## Work mode pode decidir gerar PDF/documento em vez de imagem — mesmo com "não é PDF" no prompt

Aconteceu 2026-09-27 (Mapa do Tarot, regeração das 18 diagramas dos arcanos IV-XXI):
o prompt JÁ tinha "IMPORTANTE sobre o formato de entrega: cada página é uma IMAGEM
PNG separada, standalone, não um PDF, não um documento" escrito explicitamente — e
mesmo assim o Work mode processou o pedido como um PDF diagramado (usando a
ferramenta de arquivo/canvas do Work mode, não a de gerar imagem) e devolveu algo
fora do formato. Só corrigiu depois que o dono mandou, no MESMO chat, uma mensagem
curta e direta: "Não, tá errado. O entregável tem que ser gerado em IMAGEM. Não é
um PDF diagramado que você converte. Você vai gerar cada página individual em
imagens separadas, de acordo com a referência visual que eu te mandei." Só isso já
foi suficiente — a resposta seguinte confirmou "Vou gerar cada uma das 18 páginas
como imagem individual" e entrou no fluxo certo (`Preparando prompts de imagem` →
`Criando imagem NN%`).

**Causa:** o Work mode tem a ação nativa "Criar arquivo ou site" (visível na tela
inicial do Work) ao lado da geração de imagem — com um pedido de "18 páginas" bem
descritivo, o modelo pode escolher essa ferramenta de documento em vez da de
imagem, e uma frase de proibição isolada dentro de um prompt longo (~6k chars) não
pesa o suficiente pra evitar essa escolha.

**Correção, se acontecer de novo:** não reformule o prompt inteiro. Mande uma
mensagem curta e imperativa no MESMO chat, no molde exato que funcionou: "Não,
[o que saiu] está errado. O entregável tem que ser gerado em IMAGEM — não é PDF/
documento que você converte. Gere cada página como imagem individual, igual à
referência visual que anexei." Confirme que ele respondeu assumindo o erro
("Entendi, vou gerar como imagem") antes de deixar rodando.

**Prevenção pro próximo lote:** repita a frase "cada página é uma IMAGEM PNG
separada — nunca PDF, nunca documento, nunca canvas" em pelo menos dois pontos do
prompt (abertura E fechamento do pedido), não só uma vez no meio de um bloco longo
de texto.

Work mode aguenta até ~**90 imagens numa única tacada** — mandar o lote inteiro de
uma vez, NUNCA uma por vez. MVP ~10 imagens = um lote só, rápido. Dar contexto
completo e organizado no prompt (produto, página de vendas, ref visual, design
system, "vou montar o bônus agora", texto por página) — quanto mais claro, mais
certo ele entrega.

## Ativar Work mode
Toggle no topo central = dois `button[role=radio]` com texto "Chat"/"Work".
`.click()` simples NÃO troca — precisa sequência de pointer events:
```js
let b=[...document.querySelectorAll('button[role=radio]')].find(x=>/Work/.test(x.innerText)&&x.getAttribute('data-state')==='off');
let r=b.getBoundingClientRect(),cx=r.left+r.width/2,cy=r.top+r.height/2;
for(let t of['pointerdown','mousedown','pointerup','mouseup','click'])
  b.dispatchEvent(new(t.startsWith('pointer')?PointerEvent:MouseEvent)(t,{bubbles:true,cancelable:true,clientX:cx,clientY:cy,button:0}));
```
Confirmar: `data-state` vira Chat=off / Work=on. Persiste entre chats na sessão.

## Anexo
`upload "input[type=file]"` funciona SÓ no composer da home vazia com Work on.
Confirma = contar `button[aria-label^="Remover ficheiro"]`. NÃO anexar refs de
arcano numa entrega de BÔNUS: work mode CLONA a estrutura da ref e ignora o texto
(gerou páginas de arcano em vez do bônus). Anexar só a CAPA como âncora de estilo +
1ª linha do prompt: "estas são 10 páginas NOVAS de um bônus, NÃO reproduza páginas
de arcano; a imagem anexa é SÓ referência de estilo visual".

## Prompt = keyboard inserttext
`agent-browser keyboard inserttext "$P"` (não `type`/`fill`). Enviar:
`document.querySelector('button[aria-label="Enviar prompt"]').click()`.

## Geração: ~12-16 min. Fim = sumir botão "Parar"/Stop. Poll a cada 20s.

## Baixar — ARMADILHAS
1. **DOM acumula imagens de VÁRIOS chats** (SPA mantém montado). `querySelectorAll('img')`
   pega imgs de outros chats → baixa conteúdo errado. Isolar: `location.reload()` no
   chat (navigate direto p/ /c/<id> BOUNCEIA pra home e às vezes trava em spinner —
   reload resolve o spinner).
2. **browser-harness (BU_CDP_URL) anexa em TARGET/tab ERRADO** do mesmo browser →
   baixa imgs de outra conversa com md5 idênticos falsos. Use agent-browser (tab da lane).
3. **Chromium bloqueia download múltiplo** (anchor a.click em loop salva só o 1º).
   Solução: fetch base64 in-page e gravar no disco via Python (base64 fica no
   subprocess, não no contexto do agente):
   `(async()=>{const r=await fetch(URL);const b=await r.arrayBuffer();const a=new Uint8Array(b);let s='';const CH=8192;for(let i=0;i<a.length;i+=CH)s+=String.fromCharCode.apply(null,a.subarray(i,i+CH));return btoa(s)})()`
4. Cada lote vem com 1-2 EXTRAS: a capa roxa "Mapa do Tarot" (produto principal) e
   drafts (ex. versão vertical de uma página depois refeita em paisagem). Sempre montar
   contact sheet (`montage`) e mapear visualmente as 10 válidas na ordem; descartar extras.

## Cloudflare "Um momento…" de PÁGINA INTEIRA (não é o turnstile embutido)
Depois de muitas navegações/reloads o perfil pode cair num interstitial Cloudflare
full-page (document.title="Um momento…", sem iframe acessível). Click sintético
(agent-browser mouse / CDP dispatchMouseEvent) NÃO passa. Precisa click humano real
no checkbox ou esperar. Evitar: não spammar navigate/reload; reload só quando preciso.

## ARMADILHA: Work mode desenha a página por CÓDIGO (27/09/2026, reprovado pelo dono)
Lote do principal do Mapa do Tarot (chat 6ab9767a): o Work mode renderizou as páginas com
HTML/SVG — carta virou boneco cinza placeholder, fonte diferente, caixas genéricas. Não é imagem
gerada. Prevenção: 1ª linha do prompt = "Gere CADA página como IMAGEM com o gerador de imagens,
uma por página, NÃO renderize com HTML/SVG/Python/código; a gravura da carta é a ilustração
Rider-Waite clássica completa, como na referência anexa — nunca ícone/placeholder" + "copie
exatamente o estilo da referência, trocando só carta e texto". Validar 2 páginas antes do lote.
Se insistir em código → voltar pro modo Chat (uma página por mensagem, com referência).
- Mesmo com o prompt-modelo explícito, o 2º lote (36 págs) veio com a carta em ÍCONE simplificado.
  Conclusão: página que precisa de gravura/ilustração fiel → modo CHAT, uma por mensagem.

## Cota de imagem esgotada (28/09)
bloqueio de imagem NÃO é cota até descartar com prova (dono 28/09): (a) rate limit por pedido rápido demais ("too many requests" ≠ cota — esperar 2-3 min, 1 pedido por vez); (b) aba fechada/errada; (c) modo errado — conferir seletor em Chat no chat novo; (d) perfil antigo sem login (`gpt` 9222, `gpt-play-1`) em vez de `gpt-conta*`. Se os 4 checks passarem e aparecer o card nativo "Você atingiu o limite de imagens… Tente de novo à(s) HH:MM", é cota real do Plus e vale em Chat E Work (provado 28/09 com prints, Mapas Elétricos). Os perfis `gpt-conta*` são a MESMA conta (Dona) e outros panes (ex.: tarot) gastam a mesma cota: aí é esperar o horário e retomar sozinho.
