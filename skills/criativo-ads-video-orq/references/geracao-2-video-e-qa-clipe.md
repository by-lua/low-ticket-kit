# Geração com IA — 2: prompt de vídeo, execução, QA de clipe e erros comuns (movido do SKILL.md em 26/10/2026)

> Continuação de `geracao-1-conceito-e-imagem.md`. Hub desativado: trechos de Hub/Grok são históricos; o motor é o Flow.


## FASE 4 — Prompt de vídeo

### Antes de escrever a primeira linha de qualquer prompt de vídeo

Estas decisões são tomadas **enquanto você escreve**, não conferidas depois. Cada
uma existe porque o defeito correspondente já queimou clipe em produção, e nenhum
deles tem conserto na pós — o único remédio é regerar, gastando cota.

**1. A fala cabe no clipe?** Escreva a fala e conte na hora. 10s = 25 palavras
(22 se o `VOICE` pedir 2.2 pal/s); 6s = 15. Se não cabe, **corte o texto agora** —
esticar o clipe não é opção. Texto que estoura faz o áudio correr além da animação:
a boca para e a voz continua.

**2. Tem objeto na mão?** Então gere em **6s**, não 10s — a degradação cresce com a
duração. E antes disso pergunte se o objeto precisa mesmo existir na cena: se a fala
já entrega a informação, **tirar o objeto é sempre melhor que domar o objeto**.

**3. O objeto tem apoio físico real?** Mão fechada, mesa, bolso. Se está "apoiado"
onde ninguém apoia (celular no volante), o modelo não sabe onde fixar e ele desgruda
e flutua. Isso é defeito de roteiro: volte e mude a cena, não o prompt.

**4. `CHARACTER` e `VOICE` são strings fixas.** Escreva uma vez por criativo e cole
byte a byte em todas as cenas. Resumir, reescrever ou trocar por "same woman as in
the reference" muda a pessoa e a voz.

**5. Nenhuma instrução meta no texto.** Nada de "same as scene 1", "keep consistent",
"do not paraphrase". O Grok lê isso como conteúdo da cena.

**6. A lista de objetos é fechada e nomeada.** Tudo que está em quadro, nada além.

**7. Nunca peça legenda.** `no subtitles, no burned-in text` no NEGATIVE, sempre.
   Mas saiba que o NEGATIVE **não basta sozinho**: numa cena real com o bloco
   completo de proibições (`captions, subtitles, burned-in text, on-screen text,
   closed captions`) a legenda apareceu mesmo assim — porque a fala tinha 29
   palavras para um clipe de 10s. Texto que não cabe faz o modelo "ajudar"
   imprimindo a frase na tela. A mesma cena, com a fala encurtada, saiu limpa.
   **Legenda queimada é quase sempre sintoma de fala longa demais** — trate pelo
   item 1, não por mais proibição.

**8. Papel, placa ou tela EM QUADRO: trave o conteúdo como prop fixo.** Se a cena
   tem uma superfície escrita e o personagem fala, o modelo **reescreve a
   superfície com a fala**. Não é legenda na tela: ele imprime o texto falado no
   próprio objeto, com a caligrafia da cena, e o resultado sai truncado e sem
   sentido.

   Caso real: cena de uma senhora segurando um papel com sete palavras e o número
   63. O `ACTION` dizia que ela **lia as palavras em voz alta**. O clipe voltou com
   o papel reescrito — `"Yo soy bendición, yo soy sod, properidad, yonfección,
   Repetilo antes Repetilo de dormir."` — enquanto as duas cenas irmãs, com o
   mesmo papel e sem "lê em voz alta", saíram intactas.

   Duas travas, as duas necessárias:

   - **Nunca escreva que o personagem lê o conteúdo em voz alta.** Troque
     `reads the words out loud to the lens` por `speaks to the lens`. É essa frase
     que convida o modelo a sincronizar objeto e fala.
   - **Declare a superfície como prop imutável** no `CONTINUITY`:

   ```
   The sheet of paper is a fixed prop: it shows exactly the same seven handwritten
   Spanish words and the number 63 as in the reference image, completely unchanged
   for the whole clip. No new words are written on it, no text on it changes,
   nothing is added or erased.
   ```

   E no `NEGATIVE`: `text changing on the paper, new handwriting appearing, words
   being written during the clip, altered handwriting, spoken words printed on the
   paper`.

   Vale para **toda** cena com superfície escrita em quadro, mesmo as que já saíram
   certas uma vez — o defeito é sorteado, não determinístico. Ao adicionar o bloco
   na versão `-short`, confira o limite de 2500 chars: no caso real os três
   prompts passaram para 2588 e tiveram que perder a cauda do `VOICE`.

**9. Prop que aparece na imagem DUPLICA na mesa — conte-o no prompt.** Se a imagem
   de referência tem um objeto pequeno em posição específica (um papelzinho dentro
   de uma tigela, uma moeda no copo), o Veo cria uma **segunda cópia** dele no
   quadro, tipicamente sobre a mesa, em cenas onde a mão não está mexendo em nada.

   Caso real: bacia com água e um papel "11" submerso. Em **4 de 8 cenas** do mesmo
   criativo nasceu um segundo papel "11" na mesa, na frente da bacia. A imagem de
   referência estava correta e o bloco anti-morphing padrão estava no prompt — não
   bastou, porque ele proíbe "objetos aparecerem" de forma genérica e não diz
   **quantos** existem.

   Escreva a contagem e o lugar, explicitamente:

   ```
   There is exactly ONE small white paper slip in the entire scene and it stays
   submerged inside the glass bowl for the whole clip. No second paper slip exists,
   none appears on the table, none is duplicated.
   ```

   `NEGATIVE`: `duplicated paper slip, second piece of paper appearing on the table,
   paper multiplying`.

   Regra geral: **todo prop pequeno e destacado leva numeral por extenso
   (`exactly ONE`) e o lugar onde fica.** "Only these objects: X, Y" não impede a
   duplicação de X — só impede a entrada de um Z.

Passe pelos nove **para cada cena**. Cinco minutos escrevendo evitam uma regeração
que custa cota e meia hora.

O Grok recebe **imagem + texto**. O texto descreve movimento, ação e fala. A aparência já está na imagem, mas o personagem precisa ser reafirmado para a voz sair certa.

### Estrutura (inglês)

```
CHARACTER: <idade, nacionalidade, aparência resumida, "must stay the same for the whole clip">
CAMERA: locked-off static <plano>, no camera movement, no zoom, no pan
ACTION: <o que acontece, em ordem, nos N segundos — UMA ação só>
  + <micro-movimento natural contínuo: piscar, respirar, peso do corpo,
     ombros e cabeça acompanhando a fala, mão que se ajusta>
DIALOGUE: she speaks on camera, in <idioma/sotaque>. Her lips must be accurately
  synced to these exact words: "<texto exato>"
  Her mouth moves visibly and continuously for the ENTIRE spoken line, from the first
  syllable to the last. The audio must never play while her mouth is closed or still.
  She finishes speaking before the clip ends.
VOICE: <idade, timbre, ritmo, emoção, "natural conversational pace">
AUDIO: <ambiente> only. No background music, no score, no sound effects, no subtitles.
CONTINUITY AND PHYSICS: <bloco abaixo>
NEGATIVE: <lista abaixo>
```

**As três linhas extras do `DIALOGUE` não são enfeite.** Sem elas o Grok trata a
fala como faixa de áudio independente da animação: quando o texto é longo, ele
mantém a voz tocando com o rosto parado. Escrever que a boca se move do primeiro ao
último sílabo, e que o áudio nunca toca com a boca fechada, amarra as duas coisas.

Isso **não substitui** o gate de contagem de palavras da FASE 1 — é a segunda
trava. Texto muito acima do orçamento estoura mesmo com a instrução; a instrução
segura a margem, a contagem segura o caso grosseiro.

### Cena SEM ROSTO sorteia outra voz — evite b-roll falado

O Veo deriva o timbre **do rosto que está no frame**. Numa cena de b-roll (só
mãos, só objeto) não há rosto, então ele sorteia uma voz nova — e o `VOICE`
idêntico, copiado byte a byte, **não segura**. O espectador ouve outra pessoa no
meio do criativo e a montagem se denuncia na hora.

Caso real: criativo de 8 cenas, sete com a senhora em quadro e uma de b-roll
(mãos com sal, sem rosto). Só essa saiu com voz diferente. O dono percebeu antes
de qualquer análise técnica: *"a voz não é a mesma"*.

**A saída é uma só: reenquadre para incluir o rosto.** Não existe insert de mãos
falado que funcione — o modelo inventa a pessoa. Se o objeto precisa aparecer, ela
o segura à altura do peito, com o rosto em quadro.

**Regra: toda cena falada tem rosto em quadro.**

Sobra b-roll de verdade? Então ele é **mudo**, e a fala fica na cena anterior ou
seguinte. Nunca gere b-roll com narração esperando que combine com o resto.

Ponha também no `NEGATIVE` das cenas faladas: `off-screen narrator, voice-over,
different voice`.

Para narração fora de quadro — só quando o criativo inteiro é narrado e nenhuma
cena tem rosto — troque o DIALOGUE por:

```
DIALOGUE: an off-screen female narrator speaks in <idioma/sotaque>, no one is
  visible speaking on camera. She says exactly: "<texto exato>"
  The narration starts within the first second and finishes before the clip ends,
  at a natural pace, without rushing and without trailing silence.
```

### `CHARACTER` e `VOICE` são texto FIXO — copie igual, nunca "same as reference"

O erro mais fácil de cometer e o mais caro: escrever a descrição completa na cena
1 (`35-year-old woman from Buenos Aires, of Spanish descent, fair skin, straight
dark brown hair…`) e, na cena 2, resumir para `same woman as in the reference
image, same face, same top`. Parece equivalente — **não é**. Texto diferente muda
o que o modelo sorteia: a personagem sai levemente diferente **e a voz junto**.

Regra: o bloco `CHARACTER` e o bloco `VOICE` são **strings fixas do criativo**.
Escreva uma vez, cole **byte a byte igual** em todas as cenas. A única coisa que
varia entre cenas é `CAMERA`, `ACTION`, `DIALOGUE` e a lista de objetos do
`CONTINUITY`.

O mesmo vale para o sotaque: `Argentine Spanish with Buenos Aires accent` numa
cena e `Argentine woman, Buenos Aires accent` na outra já é variação suficiente
para o sotaque escorregar. Uma frase, sempre a mesma.

Verificação antes de gerar:

```bash
diff <(grep '^CHARACTER' v-cena-1.txt) <(grep '^CHARACTER' v-cena-2.txt)   # tem que ser vazio
diff <(grep '^VOICE'     v-cena-1.txt) <(grep '^VOICE'     v-cena-2.txt)   # tem que ser vazio
```

### A imagem da cena 2 sai da cena 1, não do zero

Gerar as duas imagens do mesmo hook em paralelo, a partir da mesma descrição
textual, dá duas pessoas parecidas — não a mesma. Gere a cena 1, aprove, e então
gere a cena 2 **anexando a imagem da cena 1 como referência**, pedindo só a
mudança de enquadramento e o que ela tem nas mãos. Consistência de rosto, roupa,
luz e cenário sai de graça.

### Cena de "verso"/folhear página: o verso sai EM BRANCO se nenhuma imagem mostra o conteúdo dele

Caso real (equilibrio-seguro-60, cena de mão virando página): o verso da folha saiu
em branco. Causa raiz — a mesma regra de sempre desta skill, "o que não está na
imagem, o modelo inventa (ou deixa vazio)": a imagem de referência mostrava só a
FRENTE da folha, com o texto e a ilustração daquele lado. Ao animar o giro, o Veo
não tem nenhum pixel de onde copiar o que fica atrás — e sem isso ele não inventa
conteúdo plausível, ele apaga: o verso vira uma folha branca lisa.

É um defeito diferente (e mais comum) do que a mistura de páginas — ver abaixo. Um
é falta total de informação (verso branco); o outro é informação demais e ambígua
(duas folhas soltas, o modelo mistura). O remédio dos dois é o mesmo: **decidir na
imagem, não no prompt de vídeo.**

Correção: gerar uma imagem própria já mostrando o estado do verso — outra página
real do PDF, foto separada — e usar essa imagem como referência daquela cena
específica (ou como frame final, se o motor aceitar). Nunca escrever no prompt de
vídeo "a hand turns the page revealing the back" esperando que o modelo desenhe um
verso plausível sozinho: sem imagem de origem, ele não tem o que desenhar.

**Melhor ainda: não anime a virada, corte entre dois clipes estáticos.** Girar a
página fisicamente dentro de um único clipe é a parte mais frágil do pedido — pede
ao modelo física de papel (dobra, sombra, ângulo) E o conteúdo do verso ao mesmo
tempo, dois problemas somados. Como o Grok Imagine é **ilimitado** no plano do Hub
(regra 8 desta skill), sai mais barato e mais confiável gerar **dois clipes
separados, cada um de uma imagem de referência diferente** — um em repouso com a
frente da página, outro em repouso já com o verso — e resolver a "virada" na
**montagem** (corte seco ou crossfade curto no ffmpeg), não na geração. Zero física
de papel pro Veo/Grok errar, zero conteúdo inventado: cada clipe só precisa
sustentar o que já está na própria imagem.

Use a virada animada apenas quando o movimento em si for o ponto de venda da cena
(ex.: mostrar o material é grosso, várias páginas). Quando o objetivo é só mostrar
duas páginas de conteúdo, dois clipes estáticos + corte é mais barato e mais seguro
que uma virada animada.

**A regra generaliza pra qualquer plano do modo demonstrativo, não só folhear.**
Folha deitada na mesa, folha em pé/segurada, pilha de folhas desfocada com uma em
foco, tela de notebook/celular mostrando a página — cada um desses é um **estado
visual diferente**, e cada um vira **uma imagem própria**, gerada no GPT com a(s)
página(s) real(is) certa(s) anexada(s) como referência daquele estado específico.

Isso vale mesmo quando a composição da imagem tem **várias folhas espalhadas** de
propósito (dá volume, mostra "são 60 guias"): não tem problema nenhum ter 3-4
folhas na mesma foto — o que quebra o vídeo é a folha ENTRAR EM MOVIMENTO sem
imagem de origem pra aquele exato enquadramento. Pra pilha espalhada funcionar:

- Ao montar o prompt de imagem, anexe as páginas reais que vão aparecer legíveis
  naquela composição (a que estiver em foco, pelo menos) — nunca peça "várias
  páginas do guia" sem anexar quais.
- A cena de vídeo gerada a partir dessa imagem é **estática** (repouso, só
  micro-movimento) — não peça ação que mude qual folha está em foco ou que
  reorganize a pilha; isso volta a ser "movimento sem imagem de origem".
- Precisa de outro enquadramento da mesma pilha (outra folha em foco, ângulo
  diferente)? É outra imagem, gerada e aprovada separadamente — mesmo raciocínio
  do verso: o que muda de estado visual pede referência própria.

Segundo defeito possível na mesma cena, causa oposta: o modelo misturou um pouco de
cada página, como se houvesse 2-3 folhas soltas em quadro, ou focou em uma e borrou
o resto. A causa mais provável é a imagem de referência mostrar mais de uma folha
solta, ou a folha entrando em ângulo/dobra que expõe uma segunda superfície — o Veo
não sabe qual delas é o "verso" e tenta desenhar as duas ao mesmo tempo, ou soma
texto de ambas.

Antes de gerar a cena de folhear:

- **A imagem de referência mostra exatamente UMA folha**, plana ou com dobra
  mínima — nunca duas ou três páginas soltas na mesma foto, mesmo que a intenção
  seja mostrar "o material tem várias páginas".
- **Se a cena precisa mostrar o verso**, gere uma imagem própria só pra esse
  estado — a folha já virada, mostrando o conteúdo de trás, foco único e nítido
  — em vez de esperar o vídeo criar esse estado a partir de uma folha vista de
  frente.
- No prompt de vídeo, declare no `CONTINUITY`: `there is exactly ONE sheet of
  paper in frame, single, flat or with a single natural fold — never two or
  three loose sheets, never a blurred mix of two pages`. E no `NEGATIVE`:
  `multiple loose sheets, blended pages, two pages overlapping, out-of-focus
  second page`.
- Se sair errado mesmo assim, não tente "consertar" no vídeo — regere a IMAGEM
  primeiro (fonte da verdade, ver seção seguinte), garantindo folha única em
  foco antes de gastar cota de vídeo de novo.

### Bloco CANON_VOICE — a voz TEM que ser a mesma nas duas cenas

O Grok sorteia uma voz nova a cada clipe. Duas cenas do mesmo criativo com
descrições de voz diferentes — ou vagas — saem com **pessoas diferentes falando**,
e o hook morre: o espectador percebe na hora que é montagem.

Escreva a voz **uma vez**, como um bloco fixo, e cole **literalmente igual, palavra
por palavra**, em todas as cenas daquele criativo. Não reescreva, não resuma, não
"melhore" na cena 2 — qualquer variação de texto muda a voz sorteada.

O bloco precisa fechar seis eixos. Vago em qualquer um deles = voz solta:

```
VOICE: age <idade numérica>, <sexo>, native <idioma + sotaque regional>.
  Pitch: <registro — ex. low chest register, no head voice>.
  Texture: <textura — ex. slightly husky, dry, faint vocal fry at sentence ends>.
  Pace: <ritmo em palavras por segundo + pausas>.
  Energy: <energia — ex. contained and matter-of-fact, never bright, never salesy>.
  Delivery: <entrega — ex. speaking to one person across a table>.
  No echo, no reverb, no processing, no announcer tone.
```

> **NUNCA escreva instrução meta dentro do prompt.** Nada de
> `(identical in every scene of this creative — do not paraphrase)`,
> `same as scene 1`, `keep consistent with the other clip` ou qualquer nota de
> processo. O Grok não tem memória entre gerações: ele lê isso como **texto da
> cena** e a qualidade cai — no caso real que originou esta regra, o clipe saiu com
> a **voz tocando sobre o rosto parado**, e só depois a boca entrava em sincronia.
> A consistência se obtém **copiando o mesmo texto descritivo**, em silêncio.
> Escreva sempre como se aquele clipe fosse o único que existe.

Regras que fazem o bloco valer:

- **Idade numérica**, não "meia-idade". O modelo trata `48` e `40s` como vozes diferentes.
- **Registro e textura explícitos** (`low chest register`, `slightly husky`) — sem
  isso a cena 2 volta ao padrão claro e jovem do modelo.
- **Ritmo em palavras por segundo**, não "natural". "Natural" oscila entre clipes.
- **Sotaque no bloco de voz também**, mesmo já estando no `DIALOGUE`.
- **A mesma imagem de referência de pessoa** nas duas cenas: o Grok deriva timbre
  do rosto. Roupa, luz e idade diferentes na imagem puxam a voz junto.
- **Nunca** descreva emoção diferente entre cenas do mesmo hook (`calm` na 1 e
  `emotional` na 2 vira outra atriz). Se a emoção precisa evoluir, ponha a evolução
  no `ACTION` e mantenha o `VOICE` intacto.

Confira sempre ouvindo as duas cenas em sequência antes de montar. Se destoou,
**regere a cena** — não tem conserto na pós.

### Bloco anti-morphing — obrigatório

Sem isso o modelo faz coisa brotar do nada: objeto aparecendo na mesa, dedo extra, mão virando outra mão, roupa mudando no meio do clipe, fundo se reorganizando. É o defeito que mais queima criativo.

```
CONTINUITY AND PHYSICS: Everything must stay physically consistent and natural
for the entire clip. The scene contains ONLY the objects visible in the reference
image: <liste-os>. No new objects appear, nothing materializes, grows, multiplies
or fades in. Objects keep their exact shape, size, color and position unless the
described action moves them. Hands keep exactly five fingers, correct anatomy,
natural skin, no extra limbs, no fusing, no melting. The face keeps the same
identity, same age, same features throughout — no morphing, no drifting, no face
swap. Clothing, hair and jewelry stay exactly as in the reference image. The
background stays static and stable, no warping, no shifting walls, no sliding
furniture. Real-world physics, natural gravity, natural human motion. Grounded
documentary realism. Vertical 9:16.
NEGATIVE: morphing, warping, melting, extra fingers, extra limbs, deformed hands,
objects appearing out of nowhere, floating objects, duplicated objects, identity
change, face swap, distorted anatomy, surreal artifacts, dreamlike transitions,
glitch, flicker, text overlay, captions, subtitles, watermark, logo, camera whip,
unnatural zoom, background music, unsynced lips.
```

Reforços que valem mais que o bloco em si:

- **Micro-movimento é obrigatório no `ACTION`.** Sem ele o Grok anima só a boca e
  o resto congela — lê como boneco falante e queima o criativo. Uma frase de ação
  principal + uma frase de movimento contínuo. Para cenas de mãos: dedos com peso
  e atrito, pequenas hesitações, punho que se ajusta. Ponha também
  `frozen mannequin stillness, static doll-like body` no `NEGATIVE`.
- **Câmera travada.** `locked-off static camera`. Quanto mais a câmera anda, mais cenário o modelo inventa.
- **Nomear e fechar a lista de objetos** em cena.
- **Preferir 6s quando tem objeto na mão.** A degradação cresce com a duração.
- **Texto escrito em quadro oscila.** Nome ou número manuscrito treme entre frames. Mantenha pequeno, fora do centro, ou mascare na pós.

---

## Disciplina de execução — as cinco falhas que mais custam

Não são bugs de ferramenta. São jeitos de trabalhar que produziram, num único dia,
uma correção que nunca aconteceu, um defeito entregue ao cliente, um lote perdido
numa queda de sessão e um browser preso enquanto outro agente esperava.

### 1. Correção em background não é correção — verifique o ARQUIVO

Um script foi posto em background para regerar uma cena defeituosa "assim que o
lote anterior terminasse". Ele esperou, destravou, e mandou ao Hub o **prompt
antigo**. O relatório da sessão dizia que a correção estava na fila; o arquivo em
disco continuava com data e conteúdo velhos. O dono descobriu abrindo o vídeo.

Regras:

- **Nunca reporte "corrigido" ou "na fila" sem olhar o arquivo.** `ls -la` na data
  de modificação e um frame extraído. Intenção não é resultado.
- **Correção pontual roda em primeiro plano**, acompanhando cada passo. Background
  serve para lote longo e repetitivo, não para conserto.
- Encadear scripts com `while pgrep ...; do sleep; done` é frágil: quando destrava,
  o estado da página já é outro. Prefira rodar em sequência explícita.

```bash
# antes de dizer que trocou:
ls -la VIDEO/cena-8.mp4                       # data tem que ser de agora
ffmpeg -ss 4 -i VIDEO/cena-8.mp4 -frames:v 1 /tmp/check.jpg && <abrir e olhar>
```

### 2. A sessão pode cair — o estado da verdade é o DISCO, não a memória

Uma leva longa atravessa quedas de sessão. Quando isso acontece, **todo job em
background morre sem aviso** e as notificações que você esperava nunca chegam: elas
voltam depois marcadas como `stopped`, sem dizer o que ficou pronto.

Retomar é sempre o mesmo procedimento, na ordem:

```bash
# 1. o que já está montado
for c in $CRIATIVOS; do [ -f "CRIATIVO-$c/CRIATIVO-$c.mp4" ] && \
  echo "$c $(ffprobe -v error -show_entries format=duration -of csv=p=0 CRIATIVO-$c/CRIATIVO-$c.mp4)"; done
# 2. o que tem clipe mas não foi montado
ls CRIATIVO-*/VIDEO/cena-*.mp4 | wc -l
# 3. o que tem imagem mas não tem clipe   (cobertura cena a cena)
# 4. só então decidir o que falta gerar
```

Duas armadilhas na retomada:

- **Arquivo existir não é arquivo certo.** Depois de uma queda, um `.png` no lugar
  esperado pode ser a versão **reprovada** que nunca foi substituída. Confira o
  conteúdo, não o caminho — foi assim que uma imagem descartada quase virou clipe.
- **O browser persiste, a sessão não.** A barra do Hub costuma sobreviver com motor,
  Quality e 9:16 intactos. Confirme com o gate em vez de reconfigurar às cegas.

### 3. Leva longa roda em FILA IDEMPOTENTE — o disco é o checkpoint

Uma leva de 36 cenas leva horas e **vai** atravessar queda de sessão. Aconteceu
duas vezes no mesmo dia. O que decide se você perde o trabalho é como a fila foi
escrita, não a sorte.

Duas propriedades, as duas obrigatórias:

**1. Pule o que já existe.** A fila checa o destino final antes de gerar. Relançar
o mesmo comando depois de uma queda retoma na cena exata, sem regerar nada e sem
gastar cota:

```bash
[ -f "$P/CRIATIVO-$n/VIDEO/cena-$i.mp4" ] && { echo "cena $i ja existe"; continue; }
```

**2. Mova o arquivo para o destino NA HORA.** Nada de acumular em `~/Downloads`
para organizar depois — "depois" é justamente quando a sessão cai, e aí o clipe
existe mas a fila não sabe:

```bash
STAGING="$(LANE_AREA=HUB ~/.claude/bin/lane.sh dir "$LANE")"
/tmp/gen.sh ... && mv "$STAGING/$LANE-$n-$i.mp4" "$P/CRIATIVO-$n/VIDEO/cena-$i.mp4"
```

Com as duas, a recuperação vira uma linha: `scripts/fila.sh`. Sem elas, é
inventário manual do que sobreviveu — e o risco de regerar o que já estava pronto.

A fila também para no primeiro criativo que não fechar as 6 cenas, em vez de
seguir queimando cota contra um teto ou um bloqueio.

Modelo pronto em `scripts/fila.sh`.

### 4. Solte a lane assim que terminar — tem gente na fila

Os browsers são compartilhados entre Claudes. Terminou de gerar imagem? Solte a lane
do `gpt` na hora, mesmo que o vídeo ainda vá levar horas no `hub`:

```bash
~/.claude/bin/lane.sh drop gpt $LANE
~/.claude/bin/browsers.sh status     # confirme que o perfil sumiu da lista
```

Segurar uma lane ociosa é o que produz o roubo de aba do outro lado. E ao pedirem o
browser de volta, **cheque antes se você ainda precisa dele**: numa ocasião a
resposta era "não preciso de nenhuma imagem nova", e o que faltava era só copiar
arquivo já gerado — trabalho de disco, zero navegador.

### 5. Defeito visto no QA é defeito reportado — nunca "deixa passar por cota"

No QA de um criativo apareceu um papel duplicado (um dentro da tigela, outro
brotando na mesa) em 4 de 8 cenas. A decisão foi seguir em frente para poupar
cota, **sem avisar**. O dono achou o mesmo defeito minutos depois, e a regeração
teve que ser feita de qualquer jeito — com a diferença de que agora havia um
criativo montado em cima do material errado.

- Defeito percebido, **fala**. A decisão de aceitar ou regerar é de quem paga a
  veiculação, não de quem monta.
- Economizar cota escondendo defeito **não economiza nada**: o retrabalho vem
  depois, maior, e com a confiança quebrada.
- Nenhum criativo é montado sobre cena reprovada. Corrige antes.
## FASE 5 — Gerar o vídeo

### ⛔ MECÂNICA DO HUB — invoque `hub-video-playwright` ANTES de tocar no browser

<EXTREMELY-IMPORTANT>
Nesta fase você **tem que** invocar a skill `hub-video-playwright` pelo tool
`Skill` antes do primeiro comando de browser. Ela é a fonte única da mecânica:
lane, scroll até a barra, escolha de motor e nível (**Veo 3.1 Quality**, nunca
Lite), proporção 9:16, duração, sequência canônica de envio (apagar texto E
imagem antes de tudo), prompt pelo setter nativo do React, gate de envio, gate de
imagem por hash, rate limit do botão Enviar, Cloudflare, download por conteúdo e
leitura do contador de cota.

**Não improvise seletor e não faça retry rápido no Enviar** — cada clique conta
como requisição e derruba a sessão por um minuto.
</EXTREMELY-IMPORTANT>

O que **esta** skill decide, e a outra apenas executa:

| Decisão | Onde está |
|---|---|
| quantas cenas, que fala, quantas palavras | FASE 1 |
| que imagem cada cena usa | FASE 3 |
| o texto do prompt de vídeo, com os blocos obrigatórios | FASE 4 |
| se o clipe voltou aceitável | QA de clipes, abaixo |
| como emendar e montar | FASE 7 |

Regra de ouro que atravessa as duas: **um criativo por vez, fechado antes do
próximo.** Vídeo é o recurso escasso — a cota do Veo repõe por geração, 24h depois
de cada uma.

## QA de clipes — diagnóstico e gate antes de montar


### 1. Voz tocando com a boca parada (dessincronia por fala longa)

Causa quase sempre a mesma: **o texto não cabia no clipe**. O Grok não acelera a
fala — deixa o áudio correr além da animação. Ver o gate de contagem de palavras na
FASE 1; se você pulou, é aqui que a conta chega.

```bash
# quanto do clipe é fala: se ocupa ~100% da duração, o texto estourou
ffmpeg -i cena-N.mp4 -af silencedetect=noise=-32dB:d=0.3 -f null - 2>&1 | grep silence_
ffprobe -v error -show_entries format=duration -of csv=p=0 cena-N.mp4
```

Fala terminando junto com o último frame, sem respiro no fim, é sinal forte. Confirme
assistindo os últimos 2 segundos. **Não tem conserto na pós: corte o texto e regere.**

Causa secundária, se o texto cabia: **instrução meta dentro do prompt** — ver FASE 4.

### 1b. Corte automático por RMS pega respiração/eco, não o fim real da palavra

Defeito oposto do anterior, e mais traiçoeiro porque **passa despercebido no
QA de imagem e no ffprobe** — só aparece assistindo a transição entre cenas.

O corte de silêncio por RMS (usado pra achar onde a fala de uma cena termina)
mede energia de áudio, não fala. Numa pessoa que "esvai" a voz aos
poucos em vez de calar abruptamente, o resíduo de respiração/eco continua
acima do limiar por 1-2s **depois** que ela já parou de falar e já está
sorrindo de boca fechada. O corte então:

1. inclui esse trecho de sorriso estático antes da transição (parece "sobra
   estranha" no fim do hook);
2. e ao mesmo tempo o corpo (cena seguinte) começa achando que o hook terminou
   ali — quando na verdade a **última palavra da fala nem chegou a ser dita**,
   porque o corte foi medido pelo fim do ÁUDIO alto, não pelo fim da FALA.

Caso real (leva 08-09-MONJE-V2, `CT69/70/71-AR`): o corte automático deu
`[0.30, 7.68]` (7.38s) pro hook de CT69, quando a fala real ("...esconde.")
terminava em torno de **5.75s** — 1.9s de respiração/sorriso incluídos, e a
palavra final cortada no meio porque o corpo já tinha começado antes dela sair.

**Não confie no `silencedetect`/RMS sozinho pra cena de hook curta com fala
terminando perto do fim do clipe.** Depois do corte automático:

```bash
# contact sheet da boca nos últimos 2-3s do hook, pra ver onde a fala PARA de verdade
for t in $(seq 4.5 0.3 7.5); do
  ffmpeg -v error -ss $t -i cena-1.mp4 -frames:v 1 -vf scale=300:-1 /tmp/m$t.jpg -y
done
montage /tmp/m*.jpg -tile 3x3 -geometry 300x+3+3 -background '#111' /tmp/sheet.jpg
```

Olhe o sheet: ache o último frame com boca ainda em movimento de fala (não
sorriso), some ~0.1-0.2s de folga, e use isso como fim do corte manual —
ignore onde o RMS achou que a energia caiu.

### 2. Morphing (objeto duplicando, flutuando, desgrudando)

Frame estático não pega. Amostre ao longo do clipe e olhe a sequência:

```bash
for k in 1 2 3 4 5 6; do
  ffmpeg -v error -ss $(awk -v k=$k 'BEGIN{print k*1.4}') -i cena-N.mp4 -frames:v 1 f$k.jpg
done
montage f?.jpg -tile 6x1 -geometry 180x320+3+3 sheet.jpg
```

Se o objeto muda de posição sem a mão levar, ou aparece um segundo, é morphing. E se
o objeto está "apoiado" onde não se apoia, o defeito é do roteiro — ver a regra de
verossimilhança na FASE 3.

### 3. Clipe de outro criativo

Com vários itens no histórico da conta, é fácil baixar o vídeo errado. Confira a
**pessoa e o ambiente** do frame contra o roteiro daquela cena, não só o prompt
exibido na página.

### O gate de clipes — um sheet por criativo, dois tempos por cena

Olhar "um frame de cada cena" não pega os defeitos que apareceram hoje: papel
duplicado, texto reescrito e degradação de fim de clipe **só existem em parte da
duração**. Amostre no mínimo dois tempos por cena — um no meio e um perto do fim,
que é onde o Veo degrada.

```bash
# faixa inferior (mesa/props) de cada cena, aos 3s e aos 6,8s
for i in $(seq 1 $N); do
  for t in 3 6.8; do
    ffmpeg -v error -ss $t -i cena-$i.mp4 -frames:v 1 \
      -vf "crop=iw:ih*0.45:0:ih*0.55,scale=200:-1" /tmp/z$i-$t.jpg -y
  done
done
montage /tmp/z*.jpg -tile 4x2 -geometry 200x+3+3 -background '#111' /tmp/qa.jpg
```

Recortar a **faixa inferior** é o truque: é onde ficam mesa, props e mãos, e é
onde nascem os objetos duplicados. No quadro inteiro o papelzinho extra some no
meio da imagem.

| Checagem | Como | Defeito real que ela pega |
|---|---|---|
| prop único | sheet da faixa inferior, 2 tempos | 2º papel "11" brotando na mesa |
| superfície escrita intacta | frame do meio, ler o texto | fala impressa no papel |
| fim do clipe limpo | frame a ~0,3s do fim | papel desbotando, roupa mudando |
| mesma voz | **ouvir** as cenas em sequência | b-roll sem rosto com voz sorteada |
| respiro sobrando | `tight.py` em cada cena | pausas de respiração |
| cena é do criativo certo | RMSE frame 0 × imagem de origem | clipe de outro job |

**O tamanho do arquivo é um sinal grátis.** Numa leva de 8 cenas, sete tinham
~4,7 MB e uma tinha 2,3 MB — era justamente a de b-roll sem rosto, a que saiu com
voz diferente. Clipe muito fora da média dos irmãos merece um olhar:

```bash
ls -la cena-*.mp4 | awk '{print $NF, $5}'
```

### Checklist antes de montar

- [ ] Palavras da fala dentro do orçamento (contadas ANTES de gerar)
- [ ] Boca acompanha a fala até o fim, com respiro no final
- [ ] Sem objeto duplicando, flutuando ou desgrudando
- [ ] Sem legenda ou texto queimado na imagem
- [ ] Mesma pessoa, roupa e cabelo das outras cenas do criativo
- [ ] Pessoa e ambiente batem com o roteiro desta cena
- [ ] `r_frame_rate` igual ao dos outros segmentos
- [ ] Superfície escrita em quadro continua com o texto da imagem de referência
- [ ] Cortes revisados por fala e gesto: sem falsa partida ou cauda inútil; pausas com função preservadas. `tight.py` só propõe candidatos.


## Erros comuns

| Sintoma | Causa | Correção |
|---|---|---|
| Boca não bate com o áudio | Fala não foi literal no prompt | `lips accurately synced to these exact words: "<texto>"` |
| Pessoa muda de rosto entre cenas | Cada imagem gerada do zero | Anexe frame de `REFERENCIA/` e peça "same woman, same face" |
| Objeto brotando na cena | Falta bloco de continuidade | Cole o bloco anti-morphing e feche a lista de objetos |
| Mão deformada, dedo a mais | Idem, pior em clipe longo | Bloco anti-morphing + prefira 6s com objeto na mão |
| Fundo se reorganizando | Câmera com movimento demais | `locked-off static camera` |
| Elemento místico vazando pra cena nova | Referência tinha vela/cristal | Proíba explicitamente no prompt de imagem |
| Sotaque neutro em vez do regional | Sotaque não especificado | `Argentine Spanish, voseo, Buenos Aires accent` |
| Fala cortada no fim | Texto longo demais | 6s ≈ 15 palavras, 10s ≈ 25 |
| **Frase repetida no clipe ("esto es para vos, esto es para vos")** | fala CURTA demais para os 8s | faixa segura 11-16 palavras; corte no fim da 1a ocorrencia, nao regere |
| **Voz tocando com a boca parada** | **Texto estourou o orçamento do clipe** | **Conte as palavras ANTES (FASE 1). Corte o texto e regere — não tem conserto na pós** |
| Trilha indesejada | Grok adiciona por padrão | `no background music, ambient sound only` |
| Legenda queimada no clipe | Não foi proibido | `no subtitles, no burned-in text` |
| Vídeo horizontal | Formato não travado na imagem | `vertical 9:16 story format` desde o GPT |
| Total do hook estourou o alvo | Cenas escritas soltas e somadas no fim | Orçamento de tempo na FASE 1 |
| Cena gerada com o prompt da cena anterior | Hub não limpa o textarea | sequência canônica de envio em `hub-video-playwright` |
| Loop de espera trava para sempre | src do `<video>` vira `blob:` | ver `hub-video-playwright` |
| Rosto vira careta ao animar | Imagem de origem estourada ou com expressão exagerada | Gere o rosto em repouso e exposição correta; a emoção vai no `ACTION` do vídeo |
| Clique em `Enviar` responde OK e nada acontece | Crisp por cima, ou ref expirado | ver `hub-video-playwright` |
| Loop de espera estoura sem clipe novo | Verificação de Segurança na tela | ver `hub-video-playwright` |
| Cena parada, boca mexendo e corpo congelado | `ACTION` sem micro-movimento | Descreva piscar, respirar, peso do corpo, mão que se ajusta |
| Imagens do GPT chegam fora de ordem | ordem do DOM ≠ ordem das cenas | ver `gpt-imagem-playwright` |
| Só 2 de N imagens baixam do GPT | downloads em rajada bloqueados | ver `gpt-imagem-playwright` |
| "Muitas requisições em pouco tempo" | cada clique em Enviar é requisição | ver `hub-video-playwright` |
| **Clipe gerado da imagem reprovada** | regerou a imagem mas não redistribuiu às cenas | `valida_img.sh` por hash antes de cada envio |
| Imagem baixada é miniatura (416x681) | filtro de download frouxo | valide dimensão com `ffprobe`; tamanho fora da média dos irmãos = lixo |
| Cena sem imagem descoberta só na hora de gerar | distribuição rodou antes de a imagem existir | cobertura **cena a cena**, não contagem total |
| Objeto flutuando apesar do bloco anti-morphing | prompt descreve o prop em lugar diferente da imagem | imagem aprovada é a fonte da verdade; adapte o prompt a ela |
| Lote reporta sucesso com item faltando | falha de envio no meio não para o loop | reconcilie pedido × disco no fim do lote |
| **Dente prateado/metálico** | Veo põe coroa ou capa de metal | bloco de esmalte natural no `CONTINUITY` + negativo de metal |
| **Banguela — dentes somem enquanto fala** | Veo apaga dentes no movimento da boca | bloco de dentes no `CONTINUITY` + `NEGATIVE`; amostre a boca em 5 tempos |
| **Personagem TROCADA numa cena** | `DIALOGUE` (fala em quadro) usado em imagem sem rosto — o modelo inventa a pessoa | declare narração explícita + `no new character`, ou reenquadre com rosto |
| **Voz muda no meio do criativo** | cena de b-roll sem rosto em quadro | Toda cena falada mostra o rosto; b-roll é mudo — ver "Cena SEM ROSTO sorteia outra voz" |
| **Prop pequeno duplicado (2 papéis, 2 moedas)** | prompt não disse QUANTOS existem | `exactly ONE ... stays inside the bowl` + negativo de duplicação — item 9 da FASE 4 |
| **Papel/tela reescrito com a fala** | `ACTION` dizia que ela lê em voz alta | Trave a superfície como prop fixo no `CONTINUITY` + `NEGATIVE` — ver item 8 da FASE 4 |
| **Respiração e pausas sobrando no final** | montagem conservou cauda inútil | corte por palavra + gesto (FASE 7); sem key, revise candidatos do `tight.py`, preservando pausas úteis |
| Tempos de corte truncados/vazios da 2ª cena em diante | `ffmpeg` comeu o stdin do `while read` | `ffmpeg -nostdin` |
| Cloudflare travando | Chromium empacotado | skill `browser-cloudflare`; `~/.claude/bin/browsers.sh status` |
| Sessão errada / conta trocada | Faltou `--session` | Passe sempre |

