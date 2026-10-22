---
name: gerador-depoimentos-instagram-gpt
description: Gera 5 imagens individuais de depoimento (foto de "cliente" real, uma pessoa diferente em cada imagem) para uma oferta/produto, num ÚNICO prompt/mensagem no ChatGPT, sem gerar cada imagem separada em chats diferentes. Use quando o usuário pedir "gera depoimentos pra essa oferta", "quero fotos de cliente contando resultado", "prova social em imagem", ou pedir pra rodar de novo esse gerador de depoimentos.
---

# gerador-depoimentos-instagram-gpt

Gera **5 imagens de depoimento JÁ PRONTAS**, estilo print/story do Instagram —
foto da pessoa + o texto do depoimento escrito DENTRO da própria imagem
(nome, estrelas, frase), pronta pra usar direto, sem precisar de componente
HTML por cima. Cada uma de uma pessoa diferente, num **único prompt**, pedindo
pro ChatGPT devolver as 5 como anexos separados na mesma resposta — não é o
fluxo "uma cena por chat" da `gpt-imagem-playwright`.

**Isto NÃO é retrato/selfie sem texto.** Se o pedido for só a foto do rosto
(sem depoimento escrito na imagem, pra montar depois em HTML com avatar+
estrelas+frase pelo código), isso é o fluxo de `gpt-imagem-playwright`, não
este. Confirme com o usuário qual dos dois ele quer antes de gerar, se não
estiver claro pelo pedido.

## Quando usar isto em vez de `gpt-imagem-playwright`

- `gpt-imagem-playwright` é pra **cenas de um roteiro/criativo de vídeo** (mesma
  narrativa, precisa de controle fino por cena) — lá, pedir lote sempre volta
  grid, então a regra de lá é uma cena por chat, sempre.
- Este skill é pra **depoimentos de pessoas independentes entre si** (não são
  cenas de uma história, são 5 "clientes" que não se conhecem) — o pedido é
  estruturalmente mais simples pro modelo (5 pessoas soltas, não 5 momentos de
  uma narrativa), então vale tentar o lote de 1 mensagem só primeiro. Se voltar
  grid mesmo assim, caia pro fallback abaixo (uma imagem por chat, igual
  `gpt-imagem-playwright`).

## Entrada que o usuário te dá

Junte o que a pessoa mandar — link do produto, contexto, textos da oferta — e
normalize antes de montar o prompt:

- **O que o produto entrega** (pra frase do depoimento fazer sentido: resultado
  específico, não genérico)
- **Perfil do público-alvo** — se a pessoa não especificar idade/gênero/
  nacionalidade, pergunte ou infira do produto/mercado (ex.: oferta AR = argentino,
  não "latino" genérico — ver seção de nacionalidade em `gpt-imagem-playwright`)
- Se vier link de página de vendas, leia a oferta (WebFetch) pra puxar a frase
  de resultado real, não inventar genérico tipo "mudou minha vida" sem contexto

## Pegar a lane — igual `gpt-imagem-playwright`

```bash
~/.claude/bin/lane.sh take gpt <lane>
G=gpt-<lane>
```

## Montar o prompt único

Chat novo, sempre (`https://chatgpt.com/`, nunca reusar chat com imagem
anterior — ancora no assunto errado).

Estrutura do prompt — as 3 travas abaixo são obrigatórias, tiradas do que já
funcionou (e do que falhou) em `gpt-imagem-playwright`:

```
Generate 5 images and return them as 5 SEPARATE image attachments — one
attachment per person, 5 files in total.

Do NOT merge them into one picture. No grid, no 2x2, no collage, no contact
sheet, no mosaic, no side-by-side, no panel layout, no single image containing
more than one person. Each image is its own standalone photograph, vertical
9:16 story format, full-bleed filling the entire frame edge to edge with a
single person.

Do not generate variations or alternate takes. Exactly 5 images, no more and
no fewer, 5 different people.

STYLE — apply identically to all 5 images: looks like a real Instagram Story
screenshot / testimonial screenshot, vertical 9:16, phone-screenshot aspect
ratio and framing. Background is the person's selfie/photo (amateur phone
look, natural evenly exposed face, no blown-out highlights, no overexposure,
visible pores and fine lines, natural skin texture, no beauty retouching, no
skin smoothing, no plastic skin, no airbrushing, no stock photo look, relaxed
neutral expression, mouth closed, candid unposed look, no studio lighting,
slight grain). Overlaid ON TOP of the photo, styled like a real Instagram
testimonial/review card: the person's first name + last initial, a 5-star
rating row, and a short testimonial quote in <idioma do público>, in a clean
readable sans-serif with good contrast against the photo (soft dark gradient
or translucent card behind the text so it stays legible). Text must be
CORRECTLY SPELLED and grammatically correct in <idioma>, short (1-2 sentences
max), no gibberish, no placeholder lorem ipsum. No app chrome, no like/comment
icons, no username handle, no logos, no watermark — just the photo + the
testimonial text treatment, nothing else.

CONTEXT — the product being talked about: <resumo do produto/oferta, 1-2 frases>

PERSON 1 — <nacionalidade específica + ascendência>, around <idade> years old,
<gênero>, <ambiente doméstico casual: quarto/cozinha/sala/varanda>, <roupa
casual simples>. Only these objects in the background: <lista fechada> —
nothing else.

PERSON 2 — <idem, outra idade/gênero/ambiente>

PERSON 3 — <idem>

PERSON 4 — <idem>

PERSON 5 — <idem>

Render ALL FIVE people, not just the first one.
```

Regras pra variar as 5 pessoas de forma que pareça depoimento real, não clone:

- **Nunca repita idade exata nem gênero em sequência** — misture (ex.: 27F,
  46M, 56F, 34M, 40F)
- **Nacionalidade específica, não continente** — "Argentine from Buenos Aires,
  Italian-Spanish descent" nunca "Latin American"
- **Ambiente varia por pessoa** (quarto, cozinha, sala, varanda, espelho) — todo
  mundo na mesma cozinha denuncia lote fabricado
- **Sem texto na imagem** — a frase do depoimento entra depois, como copy HTML
  ao lado da foto (é assim que já está implementado em
  `lp-diario-astral/carta-proposito/index.html` e `portal-demo/checkout.html`
  desta oferta: avatar + nome + estrelas + frase, a foto é só o rosto)

## Enviar

Igual `gpt-imagem-playwright` — `keyboard inserttext` (nunca `fill` com prompt
longo), depois o clique via eventos completos (o `button[aria-label="Enviar
prompt"]` às vezes não responde a `click @ref`):

```bash
agent-browser --session $G navigate "https://chatgpt.com/"
sleep 3
# confirmar chat vazio antes de enviar
echo "(()=>document.querySelectorAll('[data-message-author-role]').length)()" | agent-browser --session $G eval --stdin   # tem que ser 0

agent-browser --session $G snapshot -i -c   # pegar o ref do textbox
agent-browser --session $G focus @eN
agent-browser --session $G keyboard inserttext "$(cat prompt.txt)"

cat <<'EOF' | agent-browser --session $G eval --stdin
(()=>{const el=document.querySelector('button[aria-label="Enviar prompt"]')
       ||document.querySelector('.composer-submit-btn');
if(!el||el.disabled) return 'sem botao';
const r=el.getBoundingClientRect();
const o={bubbles:true,cancelable:true,view:window,clientX:r.left+r.width/2,clientY:r.top+r.height/2,pointerId:1,isPrimary:true,button:0};
['pointerover','mouseover','pointermove'].forEach(t=>el.dispatchEvent(new (t.startsWith('pointer')?PointerEvent:MouseEvent)(t,o)));
el.dispatchEvent(new PointerEvent('pointerdown',o)); el.dispatchEvent(new MouseEvent('mousedown',o));
el.dispatchEvent(new PointerEvent('pointerup',o)); el.dispatchEvent(new MouseEvent('mouseup',o));
el.dispatchEvent(new MouseEvent('click',o)); return 'clicou';})()
EOF
sleep 8
echo "(()=>'prompt='+(document.querySelector('#prompt-textarea')?.innerText.length||0))()" | agent-browser --session $G eval --stdin   # tem que ser 0 (enviou)
```

## Esperar — rate limit é real, não insista cego

O plano do ChatGPT usado aqui tem limite de geração de imagem por janela de
tempo. Já aconteceu de travar (`msgs=1`, nenhuma resposta, ~9min) e depois
mostrar explicitamente `"Excesso de solicitações... aguarde alguns minutos"`.

```bash
for i in $(seq 1 60); do
  n=$(echo "(()=>Array.from(document.querySelectorAll('img')).filter(i=>i.naturalWidth>400).length)()" | agent-browser --session $G eval --stdin | tr -dc '0-9')
  rl=$(echo "(()=>document.body.innerText.includes('Excesso de solicita'))()" | agent-browser --session $G eval --stdin)
  [ "${n:-0}" -ge "5" ] && { echo READY; break; }
  [ "$rl" = "true" ] && { echo "RATE_LIMIT — pare e avise o usuário, não insista"; break; }
  sleep 5
done
```

**Se bater rate limit: pare, avise o usuário quantas imagens já saíram e quantas
faltam, e pergunte se quer que você agende um retry depois de alguns minutos
(`ScheduleWakeup`) ou se prefere acionar na mão.** Nunca insista em loop cego —
cada tentativa nova durante o rate limit pode alongar o cooldown.

## Se voltar grid em vez de 5 separadas

Confirmado como comportamento possível do modelo (documentado em
`gpt-imagem-playwright` pra cenas de roteiro). Se acontecer aqui:

1. Abra a imagem e confira — se for uma imagem só com 5 pessoas coladas, é grid.
2. **Não regenere pedindo "separado" de novo no mesmo chat** — abre chat novo.
3. Caia pro fallback: gere uma pessoa por chat, igual `gpt-imagem-playwright`
   (mesmo prompt de PERSON N isolado, sem as travas de lote).

## Baixar e validar

Mesma mecânica de `gpt-imagem-playwright` — filtro por proporção (`naturalWidth
> 800 && naturalHeight/naturalWidth > 1.5`), confirmar dono do chat por
conteúdo antes de baixar (aba pode ser roubada por outra lane), prefixar nome
com a lane, e validar dimensão de cada arquivo com `ffprobe` no final:

```bash
for f in <lane>-*.png; do
  d=$(ffprobe -v error -show_entries stream=width,height -of csv=p=0 "$f")
  echo "$f = $d"
done
```

Staging obrigatório: `~/.claude/bin/lane.sh collect <lane>` → depois pra pasta
do projeto.

## Integração com a página

As imagens viram o `photo` de cada item do array `TESTIMONIALS` (já existe nos
dois arquivos desta oferta — `lp-diario-astral/carta-proposito/index.html` e
`portal-demo/checkout.html`, ambos com o mesmo formato `{ photo, rating, name,
city, result }`). Sem `photo`, o componente já cai pra iniciais — trocar pela
URL da imagem gerada (hospedada em `assets/`) ativa a foto real.
