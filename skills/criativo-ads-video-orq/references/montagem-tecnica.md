# Montagem técnica — ferramentas, ffmpeg, layouts, mix, Drive (movido do SKILL.md em 26/10/2026)

> Detalhe de COMO executar. A regra de edição (o que fazer) é `EDICAO-PADRAO.md` e manda sobre este arquivo onde houver diferença (ex.: velocidade = 1.0; trilha contínua até o fim do card).


## Stack de edição (qual ferramenta pra quê) — revisado 2026-09-23

| Etapa | Ferramenta padrão | Fallback |
|---|---|---|
| B-roll de apoio: cutaway, insert, footage real, print de tela/notícia, "corte do X falando Y" | **get-brolls** (`/get-brolls-brief` → `/get-brolls-review` → entrega com origem/licença). Só coleta, NÃO edita: o trecho entregue entra na montagem pelas linhas abaixo | Pexels/Pixabay/Pinterest à mão (seção Vitrine Guiada) |
| Corte de cabeça/cauda/pausas, fim da fala, repetição do Veo | **video-use** (`~/.claude/skills/video-use`): `helpers/transcribe.py` (ElevenLabs Scribe, palavra a palavra, NÃO é whisper) → `edl.json` → `helpers/render.py` (corta em fronteira de palavra, fade de 30ms em toda junção, preserva fps nativo) | `scripts/tight.py` + `scripts/montar.sh` (silencedetect) |
| Legenda karaokê de fala | **`scripts/legenda_align.py`** (tempo por alinhamento forçado roteiro+áudio) → **Remotion** `references/legenda-karaoke-tiktok-CANONICA.jsx` (KaraokeV2, vídeo+legenda na mesma composição) | ffmpeg `subtitles` estilo VSL2-MARTA (só VSL sem Remotion) |
| Split meio a meio, PiP, tarja, call-out, transição de escala | **Remotion** (composição React sobre as cenas uniformes) | Hyperframes |
| Motion/legenda animada elaborada, cards gráficos, transição com velocidade casada | **Hyperframes** (`hyperframes-*`, `talking-head-recut` pra cards sobre fala, `cut-the-curve` pra costuras) | Remotion |
| Medir (ffprobe, silencedetect, volumedetect, mpdecimate), extrair frame, normalizar resolução, concat, mix narração+trilha | **ffmpeg** — é a ferramenta certa aqui, não troca | — |
| Ajuste fino à mão pelo dono (timeline visual) | **OpenCut classic** (`~/Projetos/opencut-classic`, http://localhost:3000) — ferramenta externa, não é passo automático | — |

Regras que valem pra qualquer ferramenta da tabela:

- **Timestamp de palavra NUNCA sai de whisper** (regra do dono, ver cabeçalho do `.jsx` canônico). Isso exclui `faster-whisper`, `whisper.cpp`, `@remotion/install-whisper-cpp` (o que a skill `remotion-captions` ensina) e `hyperframes transcribe` (motor `auto` cai em whisper no Linux; `parakeet-mlx` é só Mac). As skills `talking-head-recut` e `embedded-captions` chamam `hyperframes transcribe` (whisper) no passo de transcrição: pule esse passo e entregue o `transcript.json` pronto (array plano `[{text,start,end}]`) gerado de uma fonte aceita. Fontes aceitas: Scribe via video-use, timing devolvido pelo TTS, forced-alignment não-whisper, grade de um VO gêmeo, ou distribuir por duração.
- **video-use precisa de `ELEVENLABS_API_KEY`** (env ou `.env` na raiz de `~/Developer/video-use`). Em 2026-09-23 a key **não está configurada**: sem ela, use o fallback da tabela e não trave o loop pedindo key. Scribe é pago por minuto de áudio; o transcript fica em cache em `<videos_dir>/edit/transcripts/`, nunca transcreva de novo o mesmo arquivo.
- Do video-use aqui se usam **os helpers**, não o fluxo conversacional dele (entrevista + confirmação de estratégia): a estratégia já saiu da FASE 0/1 desta skill.
- Legenda sempre é a ÚLTIMA camada, em qualquer ferramenta.

Jeito antigo (ffmpeg pra tudo): ver `references/SKILL-ffmpeg-OLD-2026-09-23.md` (cópia integral do SKILL.md antes desta revisão).


### E.3 — Edição: os dois arranjos

Os dois arranjos existem no mesmo criativo, alternando. É essa alternância que
segura a atenção.

**Meio a meio (split 9:16).** Tela em cima, pessoa embaixo (ou o inverso). Use
enquanto a fala **descreve o que a tela mostra** — os dois canais dizem a mesma
coisa ao mesmo tempo e a prova entra sem interromper a fala.

**Foco alternado (PiP).** A pessoa começa em quadro cheio falando. Quando a fala
vira "olha aqui dentro", ela **encolhe pra miniatura no canto** e a tela toma o
quadro rolando por dentro. No CTA ela **volta ao foco** em quadro cheio.

Regra do arranjo: **quem está em quadro cheio é quem está carregando a
informação naquele segundo.** Personagem grande enquanto a tela mostra o que
importa é desperdício dos dois lados. A transição entre arranjos é escala
animada em ~0,3s, nunca corte seco — corte seco na troca de tamanho lê como bug.

Miniatura: canto inferior, ~28–32% da largura, cantos arredondados, sem borda
grossa. Menor que isso o rosto some no feed; maior, briga com a tela.

**Onde montar:** composição **Remotion** — cada cena/gravação é um `<OffthreadVideo>`
dentro de `<Sequence>`; a troca quadro cheio → miniatura é `interpolate`/`spring`
de escala e posição em ~0,3s (9 frames a 30fps, 7 a 24fps); a borda esfumaçada do
meio a meio é `maskImage: linear-gradient(...)` na camada de cima. Ver
`remotion-best-practices` / `remotion-multimedia`. Hyperframes serve igual
(`hyperframes-*`), quando o criativo já vai ter motion elaborado lá. O fps da
composição é o nativo do motor (ver FASE 7), não 30 por hábito. Não testado ainda
como template pronto desta skill: o primeiro criativo que usar, salve a composição
em `references/` pra reaproveitar.

**Referências reais de composição, 4 exemplos salvos** (2026-09-09) em
`references/composicao-tela-dividida/` — cobrem a variação que existe na
prática, além do que já ia descrito acima:

| Arquivo | Arranjo | Leitura |
|---|---|---|
| `exemplo-1-hook-meio-a-meio-blur.png` | Meio a meio, pessoa em cima, tela embaixo | Corte **NÃO é linha reta** — borda entre as duas camadas é esfumaçada/borrada (gradiente), não um corte seco de pixel. Legenda em destaque ("GREW UP" em vermelho) sentada bem na costura. |
| `exemplo-2-meio-a-meio-pessoa-baixo.png` | Meio a meio invertido, tela em cima, pessoa embaixo | Mesma borda esfumaçada; prova que a ordem (pessoa cima/baixo) é livre — decide pelo que a fala está descrevendo naquele segundo, não por regra fixa de posição. |
| `exemplo-3-split-corte-seco-play.png` | Split 50/50, linha reta (corte seco) | Ao contrário do E.3 acima: **corte seco na linha do split TAMBÉM é válido** quando o estilo é "demonstração de app/tela" — ícone de play sobreposto reforça que aquela metade é conteúdo navegável, não B-roll comum. Use linha reta quando quiser deixar claro "isto é uma tela", esfumaçado quando quiser fusão mais orgânica (b-roll/produto físico). |
| `exemplo-4-miniatura-pip-canto.png` | Miniatura/PiP, mas SEM o círculo perfeito da regra acima | Rosto pequeno com ícone de play ao lado — variação do PiP que sinaliza "isso é um vídeo dentro do vídeo", útil quando a demonstração em si parece um card/resultado de busca (ex: catálogo, feed).

**Ordem não é fixa.** Nenhuma regra obriga "hook em quadro cheio → split → CTA
em quadro cheio" como sequência única. O hook pode nascer já em split (exemplo
1/2) se a informação da tela já for a prova do hook; guarde o quadro cheio pra
quando a pessoa precisa carregar sozinha a atenção (identificação, CTA).

**Legenda nos exemplos:** texto bold, branco/amarelo claro, com 1 palavra-chave
em vermelho/destaque, tamanho médio (nunca ocupando mais que ~2 linhas curtas),
sentada na costura do split quando existe, ou no terço inferior quando é
quadro cheio/PiP. Isso é a MESMA regra da legenda de fala (branca, caixa viva
960×1270) — a diferença é que aqui é call-out/manchete, não transcrição da fala.


### Upload pro Drive: só o arquivo final, e nunca sem a pasta Kalodata

- **Só sobe o `*-final.mp4`** pra pasta `1 - FEED (postar)/` — nunca clipe de cena
  solto, TMP, ou intermediário sem trilha/aceleração.
- **Toda pasta datada de produto leva a pasta `0 - Pesquisa Kalodata/`** com
  `kalodata-metricas.png` + `link-kalodata.txt` daquele produto (já existem em
  `PRODUTOS/<produto>/` — copie de lá, nunca esqueça ao criar pasta nova no Drive).
- **Padrão fixo desde 09/09/2026: além da métrica, sempe inclua o print da
  TELA DE DETALHE DO PRODUTO no Kalodata** (`/product/detail?id=...`, a página
  que mostra foto, preço, categoria, avaliação e "Principais métricas" —
  não o card de ranking da busca). É esse print + o link dessa URL de detalhe
  (não o link genérico `/product` de busca) que o usuário usa pra se afiliar.
  Nomeie `"<Produto> - detalhe produto Kalodata.png"` e salve junto do
  `metricas Kalodata.png` na mesma pasta `0 - Pesquisa Kalodata/`.
  **Como achar o link de detalhe certo:** Hub -> `/tools` -> busca "kalodata"
  -> clica no card -> escolhe a conta certa (abre aba nova autenticada,
  `kalodata2.*`=Conta 1, `kalodata3.*`=Conta 2) -> aba `Produto` -> busca pelo
  nome exato do produto (da `ficha.md`) -> clica no resultado que bate (nome +
  preço + `id` batendo com o Cover CDN salvo em `link-kalodata.txt`) -> a URL
  vira `/product/detail?id=<id>&...` — é essa que entra no `link-kalodata.txt`
  e no `links-kalodata.txt` consolidado do Drive, substituindo qualquer link
  genérico de busca/ranking que estava lá antes.

**Trilha sempre.** Narração seca sobre gravação de tela soa como tutorial de
suporte técnico. Regras da trilha:

- Instrumental, sem letra — letra briga com a narração pelo mesmo canal.
- Coerente com o nicho e com o gatilho: rural/oficina pede algo seco e ritmado,
  não épico de trailer; e trilha alegre não entra em criativo de dor.
- **−18 a −22 dB abaixo da voz.** Se você percebe a música, está alta demais.
- Uma trilha por criativo, contínua do primeiro ao último frame — trocar de
  música no meio parece emenda de dois vídeos.
- Banco livre de royalties (Pixabay Music, Mixkit, Free Music Archive).
  Nunca música comercial: derruba o anúncio por direitos.

### Baixar a trilha do Pixabay Music — `WebFetch` NÃO pega o link de áudio

O player do Pixabay Music carrega a faixa via JS só depois do clique em play; a
página estática (o que `WebFetch` lê) não tem nenhum `<audio>`/`.mp3` no HTML.
Testado: `WebFetch` na página de busca devolveu "nenhum link .mp3 encontrado"
mesmo com dezenas de faixas listadas visualmente.

Correção — abra num browser real, clique o overlay de play da faixa, e o
`<audio>` aparece no DOM com o `src` direto do CDN (`cdn.pixabay.com/audio/...`),
baixável por `curl` sem sessão/cookie:

```bash
~/.claude/bin/browsers.sh gratuito                     # ou qualquer perfil livre
agent-browser --session gratuito navigate "https://pixabay.com/music/search/genre/pop/"
agent-browser --session gratuito eval "(() => {
  const btns = Array.from(document.querySelectorAll('button'));
  const play = btns.find(b => b.className.toLowerCase().includes('play'));
  play.click(); return 'clicked';
})()"
sleep 2
agent-browser --session gratuito eval "(() => Array.from(document.querySelectorAll('audio,source')).map(a=>a.src||a.currentSrc).filter(Boolean))()"
# -> ["https://cdn.pixabay.com/audio/2026/06/04/audio_xxxxxxxxxx.mp3"]
curl -sL "<url>" -o trilha.mp3
```

Troque `/genre/pop/` pelo gênero/mood do nicho (`/search/mood/calm/`,
`/genre/cinematic/` etc.) — a mecânica do clique é a mesma.

**Baixe um BANCO de faixas variadas, não uma só.** Usar a mesma trilha em todo
criativo da leva é o mesmo erro de "todos os hooks abrem igual" (ver FASE 1,
teste de similaridade) — só que no áudio. Navegue por **vários gêneros
diferentes** (`pop`, `corporate`, `acoustic`, `lofi`, `rnb`, `cinematic`...),
uma faixa de cada, e salve num banco reusável por nicho:

```
<PROJETO>/_ASSETS/trilhas/<genero>.mp3
```

**Cada `navigate` pede sleep de ~3s antes do clique** — o Pixabay é SPA e o
componente do player pode não ter re-renderizado ainda; clicar cedo demais
retorna o `src` da faixa anterior sem erro nenhum (parece ter funcionado, mas
é a mesma URL de antes). Confirme que a URL mudou antes de seguir pro próximo
gênero — se repetiu, aumente o sleep e tente de novo.

Na montagem, **sorteie/alterne a faixa por criativo** (ex.: `pop` no provador,
`corporate` no detalhe, `acoustic` no pov) — nunca a mesma faixa em todos os
formatos do mesmo produto, e nunca repita a mesma faixa em produtos vizinhos
da mesma leva.

### Nível real do mix — meça, não chute

(Mix narração+trilha continua no ffmpeg de propósito: os ganhos abaixo foram
calibrados de ouvido em produção. Se a trilha for pra dentro de uma composição
Remotion/Hyperframes, leve os MESMOS ganhos (`volume` do `<Audio>` / `data-volume`)
e confira com o `volumedetect` do mesmo jeito. Não use `hyperframes normalize-audio`
aqui: ele IGUALA a loudness da trilha à da narração, o oposto do que o mix pede.)

`-18 a -22dB` como ponto de partida genérico **não bate** com o que soa bem na
prática: testado em produção e ainda saiu alto demais / narração baixa demais.
O que funcionou depois de calibrar por ouvido:

```bash
ffmpeg -i vo.mp4 -i trilha.mp3 -filter_complex \
  "[0:a]volume=2.2[v0];[1:a]volume=-38dB[m];[v0][m]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[aout]" \
  -map 0:v -map "[aout]" -c:v copy -c:a aac final.mp4
```

- **`normalize=0` é obrigatório no `amix`.** Sem isso o filtro reduz os dois
  canais pela metade automaticamente, e o resultado depende de quantos inputs
  existem — o `-20dB` de um teste não soa igual ao `-20dB` de outro. Com
  `normalize=0`, os ganhos (`volume=`) são os únicos que decidem o nível.
- **Narração ganha `volume=2.2`** (sobe ~+7dB) antes de mixar — sem isso ela
  fica baixa demais perto da trilha mesmo com a trilha atenuada.
- **Trilha em `-38dB`**, bem mais baixo que o `-18/-22dB` da orientação
  genérica — meça de ouvido a cada leva nova, o valor certo varia com a
  loudness da faixa escolhida (uma faixa mais "cheia" precisa de mais corte).
- **Confirme com `volumedetect`, não só de ouvido:** compare o `mean_volume`
  do vídeo final contra o da narração sozinha — se subiu muito (>2-3dB), a
  trilha está competindo.

```bash
ffmpeg -i narracao.wav -af volumedetect -f null - 2>&1 | grep mean_volume
ffmpeg -i final.mp4 -af volumedetect -f null - 2>&1 | grep mean_volume
```


## FASE 6 — Registrar

Para cada cena, salve `PROMPTS/cena-N.md` com prompt de imagem, prompt de vídeo, duração, modelo e data. Sem isso não dá para reproduzir nem iterar uma cena que ficou quase boa.

---

## FASE 7 — Montagem

**Antes de cortar ou normalizar**, leia [Acabamento natural: áudio, cortes e clareza](references/acabamento-natural-audio-cortes.md). A revisão aprovada do Número Mestre AR/LATAM é o guia para falsas partidas, gestos tardios, ruído, música e diferenças de volume. `tight.py` é detector de candidatos, não aprovação de cortes; preserve pausas com função e confira o master.

### Cortar silêncio — cabeça, cauda E pausas internas

**O motor entrega ar demais.** Cada clipe de 8s do Veo chega com 0,8 a 1,6s de
silêncio sobrando só nas pontas, mais as pausas de respiração no meio da fala.
Num criativo de 11 cenas isso somou **9 segundos de nada** — o dono assistiu e a
primeira coisa que apontou foi "as pausas de respiração ainda aparecem".

Aparar só a cauda **não resolve**: as pausas internas são a maior parte do
problema. Numa medição real, o mesmo criativo tinha **20 silêncios** com
`d=0.35` depois de aparado só nas pontas, e **3** depois do corte completo.

**Padrão (quando houver `ELEVENLABS_API_KEY`): corte por palavra no video-use.**
`silencedetect` mede "onde há som", e o Veo enche o fim do clipe de som que não é
fala (ver "Fim da fala" abaixo). O transcript Scribe dá a fronteira de cada palavra,
então o corte nunca come sílaba nem deixa sorriso sobrando:

```bash
VU=~/Developer/video-use; PY=$VU/.venv/bin/python
# 1. transcreve cada cena (cacheado em VIDEO/edit/transcripts/<cena>.json)
for i in $(seq 1 $N); do $PY $VU/helpers/transcribe.py VIDEO/cena-$i.mp4 --language pt; done
$PY $VU/helpers/pack_transcripts.py --edit-dir VIDEO/edit     # -> VIDEO/edit/takes_packed.md
# 2. monte VIDEO/edit/edl.json: um range por trecho falado, borda na palavra
#    (padding 30–200 ms, calibrado por fala e gesto; não use cauda fixa de 0,30 s)
# 3. renderiza: corta por trecho, fade de 30ms em cada junção, concat, fps nativo
$PY $VU/helpers/render.py VIDEO/edit/edl.json -o VIDEO/edit/preview.mp4 --preview --no-subtitles
$PY $VU/helpers/render.py VIDEO/edit/edl.json -o FINAL-sem-legenda.mp4 --no-subtitles --no-loudnorm
```

`edl.json` (formato do video-use):

```json
{"version": 1,
 "sources": {"cena-1": "/abs/VIDEO/cena-1.mp4", "cena-2": "/abs/VIDEO/cena-2.mp4"},
 "ranges": [
   {"source": "cena-1", "start": 0.26, "end": 2.90, "beat": "HOOK", "quote": "...", "reason": "..."},
   {"source": "cena-1", "start": 3.05, "end": 6.95, "beat": "HOOK", "quote": "...", "reason": "pausa interna cortada"},
   {"source": "cena-2", "start": 0.18, "end": 5.40, "beat": "BODY", "quote": "...", "reason": "..."}]}
```

- `--no-subtitles`: a legenda é a camada final no Remotion (canônica), não o SRT/ASS do video-use.
- `--no-loudnorm`: o render.py normaliza pra -14 LUFS por padrão; aqui o nível
  final sai do mix calibrado (E.4), então desligue e deixe o mix decidir.
- Não passe `--fps`: sem ele o render preserva o fps da fonte (Veo = 24), que é a regra.
- Uma cena que veio em resolução diferente continua precisando da normalização
  1080×1920 **antes** (seção "ANTES do concat" abaixo) — não testado se o render.py
  cobre isso sozinho.
- Os mesmos transcripts servem pro "Fim da fala" e pra caça de repetição do Veo,
  mais abaixo — uma transcrição por cena, nunca duas.

Status: helpers conferidos (`--help`) em 2026-09-23; o fluxo inteiro ainda **não
rodou num criativo real** desta skill. No primeiro uso, compare o resultado com o
`montar.sh` no mesmo material antes de trocar de vez.

**Fallback (sem key, ou se o video-use falhar): `scripts/tight.py`** — ele lê o
`silencedetect` e devolve candidatos. Revise fala, repetição, música e gesto antes de aprovar qualquer trecho:

```bash
python3 scripts/tight.py cena-1.mp4
# 0.360 2.747
# 3.111 6.653
# 7.218 7.712
```

Parâmetros no topo do arquivo, calibrados em produção:

| Constante | Valor | O que faz |
|---|---|---|
| `HEAD_PAD` | 0.10 | respiro antes da primeira sílaba |
| `TAIL_PAD` | 0.30 | respiro depois da última |
| `MINGAP` | 0.30 | pausa acima disso é cortada |
| `MAXGAP` | 0.16 | o que sobra da pausa cortada |

Trechos com menos de 0,35s são descartados — clipe de 0,1s quebra o encode e o
erro que aparece é enganoso (reclama do `-ss` da linha seguinte).

**O jump cut aqui é a estética, não um defeito.** Os criativos-modelo deste nicho
são cortados assim; ritmo frouxo é que destoa. Só preserve a pausa quando ela for
dramática de propósito.

`scripts/montar.sh <dir-criativo> <n-cenas> <saida.mp4>` faz tudo: corta, faz
upscale para 1080x1920, normaliza no fps nativo e concatena pelo filtro.
(Fallback. Atenção: o `montar.sh` fixa `-r 24` — em cena de outro motor, ajuste.)

### `ffmpeg` come o stdin do loop — sempre `-nostdin`

Bug que corrompe a montagem **em silêncio** e é dificílimo de ler pelo erro.
Dentro de `while read ... done < <(...)`, o `ffmpeg` lê o mesmo stdin e engole as
linhas restantes. A primeira cena sai certa e da segunda em diante os tempos
chegam truncados ou vazios:

```
Invalid duration for option ss: .360      # o "0" sumiu — linha meio consumida
Invalid duration for option to:           # linha inteira consumida
```

O erro aponta para o valor, então se perde tempo procurando bug de formatação
numérica ou de locale. A causa é o stdin.

```bash
ffmpeg -nostdin -v error -ss "$a" -to "$b" -i cena-$i.mp4 ...
```

Regra: **todo `ffmpeg` dentro de laço que lê linhas leva `-nostdin`.**

### Upscale + normalização

```bash
VF="scale=1080:1920:flags=lanczos,unsharp=5:5:0.7:5:5:0.0,fps=30,format=yuv420p"
ffmpeg -ss <ini> -to <fim> -i cena-N.mp4 -vf "$VF" \
  -c:v libx264 -crf 18 -preset slow -c:a aac -b:a 192k -ar 48000 -ac 2 -y s<N>.mp4
```

Acelerar uma cena arrastada (vídeo e voz juntos, sem subir o tom):

```bash
ffmpeg -i cena.mp4 -vf "setpts=PTS/1.3,$VF" -af "atempo=1.3" ... -y saida.mp4
```

Se a cena não tem boca em quadro, dá para acelerar só o vídeo e deixar a voz no ritmo natural.

### Voz robótica = fala longa demais. O teto do Veo é 16 palavras.

Quando o texto não cabe no clipe, o Veo **não corta a fala: ele acelera**. O
resultado soa sintético, "robótico do nada", e nenhuma métrica técnica acusa — o
arquivo fica perfeito, só a voz é que está comprimida.

Medido em produção, no mesmo criativo:

| Fala | Ritmo resultante | Resultado |
|---|---|---|
| 20 palavras | 2,82 pal/s | robótica |
| 18 palavras | 2,56 pal/s | robótica |
| 18 palavras (ocupa os 8s) | 2,25 pal/s | **cortada no fim**, sem respiro |
| 17 palavras | 2,29 pal/s | natural |

**O Veo fala mais devagar que o Grok** — ~2,2 pal/s contra 2,5. Não reaproveite a
régua de um motor no outro.

| Motor | Clipe | Teto real |
|---|---|---|
| **Veo 3.1** | 8s | **16 palavras** |
| Grok | 10s | 22 palavras |
| Grok | 6s | 13 palavras |

Depois de gerar, confirme que a fala terminou **antes** do fim do clipe:

```bash
# tem que sobrar respiro: fim da fala < duracao - 0.5s
ffmpeg -i clipe.mp4 -af silencedetect=noise=-34dB:d=0.35 -f null - 2>&1 | grep -oP 'silence_start: \K[0-9.]+' | tail -1
ffprobe -v error -show_entries format=duration -of csv=p=0 clipe.mp4
```

Se não houver nenhum `silence_start`, a fala foi até o último frame: **o texto
estourou**. Encurte e regere — a montagem não conserta.

**Antes de condenar o clipe, repita a -28dB.** O Veo entrega ruído de sala audível,
e a -34dB esse room tone conta como som: o `silencedetect` não acha silêncio nenhum
e o clipe parece estourado quando não está. Num clipe real, `-34dB` não devolveu uma
linha sequer, e `-28dB:d=0.2` mostrou a fala terminando em **6,0s de 8,0s**, com
1,9s de respiro.

```bash
# checagem primária
ffmpeg -i clipe.mp4 -af silencedetect=noise=-34dB:d=0.35 -f null - 2>&1 | grep silence_
# se vier VAZIO, confirme antes de regerar:
ffmpeg -i clipe.mp4 -af silencedetect=noise=-28dB:d=0.2 -f null - 2>&1 | grep silence_
```

Só é estouro de verdade quando **as duas** passagens não acham silêncio no fim.
Regerar por leitura errada do limiar gasta cota à toa.

### O Veo degrada DEPOIS que a fala acaba — corte ali, não regere

Quando a fala termina antes dos 8s, o modelo precisa preencher o resto e é aí que
ele inventa: a pessoa baixa o objeto, o texto escrito desbota, a roupa muda, um
microfone de lapela aparece. O miolo do clipe está perfeito.

Caso real: cena regerada saiu com o papel correto e, a partir de ~6,3s — depois do
fim da fala em 6,75s — as primeiras linhas do papel começaram a apagar e o suéter
mudou de textura. Regerar de novo custaria cota e provavelmente repetiria o
padrão, porque a causa é estrutural.

**A correção é o corte, não a regeração:**

```bash
# 1. onde a fala termina de fato
ffmpeg -i clipe.mp4 -af silencedetect=noise=-28dB:d=0.12 -f null - 2>&1 | grep -oP 'silence_start: \K[0-9.]+' | tail -1
# 2. corte logo depois disso
ffmpeg -nostdin -v error -ss 0 -to 6.80 -i clipe.mp4 -c:v libx264 -crf 18 -preset slow -r 24 \
  -c:a aac -b:a 192k -ar 48000 -ac 2 -y cena-N.mp4
```

Antes de condenar um clipe, **amostre o fim** (`-ss <dur-1.5>`, `-ss <dur-0.3>`).
Se o defeito só existe depois da última sílaba, é corte de 10 segundos — não uma
geração nova.

### NUNCA force fps — respeite o nativo do motor

O Veo entrega **24fps**. Forçar `fps=30` na normalização **duplica frames de forma
irregular** e o clipe fica com travadinho (judder) perceptível, sobretudo em
movimento de mão e cabeça. Nenhum `ffprobe` acusa: o arquivo fica 30fps certinho.

```bash
# descobre o fps nativo ANTES de normalizar
ffprobe -v error -select_streams v -show_entries stream=r_frame_rate -of csv=p=0 clipe.mp4
```

Normalize mantendo o nativo — sem `fps=` no filtro, e `-r` igual ao de origem:

```bash
ffmpeg -ss 0 -to $end -i clipe.mp4 \
  -vf "scale=1080:1920:flags=lanczos,format=yuv420p" \
  -c:v libx264 -crf 18 -preset slow -r 24 \
  -c:a aac -b:a 192k -ar 48000 -ac 2 -y sN.mp4
```

### Concat de cenas com fps diferente: o fps do CRIATIVO é o do motor, o resto se adapta

Cenas geradas em motores diferentes (Veo 24fps, outra fonte 30fps) dentro do
mesmo criativo. Uma tem que ceder, e a escolha não é opinião — se mede:

```bash
# para cada candidato: total de frames vs frames únicos
tot=$(ffprobe -v error -select_streams v -show_entries stream=nb_frames -of csv=p=0 x.mp4)
uni=$(ffmpeg -i x.mp4 -vf mpdecimate -f null - 2>&1 | grep -oP 'frame=\s*\K[0-9]+' | tail -1)
```

Medido num hook real de 8s:

| Caminho | Hook | Veredito |
|---|---|---|
| forçar tudo a **30** (converte o hook 24→30) | 240 total / **173 únicos** = **67 frames duplicados** | judder |
| manter **24** (converte o body 30→24) | 192 total / 173 únicos, nativo | limpo |

O detalhe que fecha a questão: o hook tem **173 frames únicos nas duas versões**. Subir
para 30 não acrescenta informação nenhuma, só duplica — e a duplicação cai justamente
no hook, que é a parte que segura a atenção no feed.

Portanto: **o criativo inteiro sai no fps do motor (Veo = 24), e o body é reamostrado
para esse fps.** O body perde frames numa conversão real de taxa, que é bem menos
visível que padrão de duplicação. Nunca o contrário.

Todos os clipes do mesmo criativo precisam do **mesmo** fps antes do concat — mas
esse fps é o do motor, não 30 por hábito. Verifique que não sobrou frame duplicado:

```bash
# frames unicos tem que bater com o total
ffmpeg -i FINAL.mp4 -vf mpdecimate -f null - 2>&1 | grep -oP 'frame=\s*\K[0-9]+' | tail -1
ffprobe -v error -select_streams v -show_entries stream=nb_frames -of csv=p=0 FINAL.mp4
```

### ANTES do concat: normalize TODA cena pra 1080x1920 — cenas de resoluções diferentes DISTORCEM o vídeo inteiro

Erro real (2026-09-09): um vídeo saiu com a pessoa **esticada horizontalmente**,
tipo espelho deformado — não era morphing do Veo, era montagem. Cada cena de um
mesmo criativo pode voltar do Hub numa resolução diferente (720×1280, 1080×1920,
e às vezes até **1920×1080 paisagem** por engano de engine/fallback) — motores e
fallbacks diferentes entregam tamanhos diferentes, e nada nisso aparece no
`ffprobe` de forma óbvia se você só olhar duração.

**Concatenar cenas com resolução diferente sem normalizar produz um vídeo final
com o canvas do PRIMEIRO clipe, e as cenas seguintes espremidas/estiradas para
caber ali** — silenciosamente, sem erro no ffmpeg. Uma cena paisagem (1920×1080)
misturada com cenas retrato (1080×1920) é o caso mais visível, mas **duas cenas
retrato de tamanhos diferentes** (720×1280 vs 1080×1920) já basta pra distorcer.

Confira as dimensões de TODAS as cenas antes de montar:

```bash
for i in 1 2 3; do ffprobe -v error -show_entries stream=width,height -of csv=p=0 VIDEO/cena-$i.mp4; done
```

Se não bater 100% entre todas, normalize cada cena **antes** do concat — nunca
confie que "todas são 9:16" só porque a proporção parece certa em cada uma:

```bash
VF="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1"
ffmpeg -y -i cena-N.mp4 -vf "$VF" -c:v libx264 -crf 18 -preset fast normN.mp4
```

`force_original_aspect_ratio=increase` + `crop` cobre o quadro inteiro e recorta
a sobra (nunca deixa barra preta) — funciona tanto pra ajustar 720×1280→1080×1920
quanto pra "salvar" uma cena que veio paisagem por engano, recortando pro centro
em vez de esticar. Rode isso **sempre**, mesmo quando as cenas parecem OK —
o defeito só aparece assistindo o vídeo final, não em nenhum comando de checagem
rápida.

### Concat: use o FILTRO, não `-c copy`

`-c copy` emenda os arquivos sem realinhar os frames de áudio. O vídeo fica certo e
**o áudio sai picotado nas junções** — estalo audível a cada troca de cena. Só se
percebe ouvindo; nenhum `ffprobe` acusa.

```bash
ffmpeg -i q1.mp4 -i q2.mp4 -i q3.mp4 -i q4.mp4 \
 -filter_complex "[0:v][0:a][1:v][1:a][2:v][2:a][3:v][3:a]concat=n=4:v=1:a=1[v][a]" \
 -map "[v]" -map "[a]" -c:v libx264 -crf 18 -preset slow \
 -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart -y FINAL.mp4
```

Reencoda, mas é o único jeito de emendar áudio limpo. Confira depois:

```bash
# só devem sobrar as pausas naturais entre cenas, nenhum estalo
ffmpeg -i FINAL.mp4 -af silencedetect=noise=-40dB:d=0.25 -f null - 2>&1 | grep silence_
```

### A ordem do histórico do Hub é CRESCENTE — não inverta

`document.querySelectorAll('video')[0]` é o clipe MAIS ANTIGO, não o mais novo.
Inverter a lista monta o criativo de trás para frente, e isso passa por qualquer
checagem técnica: resolução, fps e duração ficam corretos, as cenas é que estão
trocadas.

**Confirme por conteúdo, não por posição.** Cada clipe começa na imagem que o
gerou, então casar frame 0 contra as imagens de referência resolve:

```bash
for n in 1 2 3 4; do ffmpeg -v error -ss 0.1 -i clipe-$n.mp4 -frames:v 1 -vf scale=200:-1 /tmp/v$n.png; done
for n in 1 2 3 4; do magick IMG/cena-$n.png -resize 200x /tmp/i$n.png; done
for v in 1 2 3 4; do for i in 1 2 3 4; do
  echo "v$v vs i$i: $(magick compare -metric RMSE /tmp/v$v.png /tmp/i$i.png null: 2>&1 | grep -oP '^[0-9.]+')"
done; done
# menor RMSE de cada linha = a cena daquele clipe
```

### Concat

Todos os trechos precisam ter mesma resolução, fps, codec e taxa de áudio — normalize antes.

```bash
printf "file '%s'\nfile '%s'\n" /abs/s1.mp4 /abs/s2.mp4 > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy -y HOOK-1.mp4
```


### Fim da fala: use a ÚLTIMA PALAVRA (transcript), não `silencedetect`

`silencedetect` responde "onde há som", não "onde há fala". No Veo os dois divergem
sempre, porque o modelo **preenche o resto do clipe depois que a fala acaba** — e o
que ele põe ali (respiração, riso, um "hmm", roupa roçando) é som audível.

Medido num hook real de 8s: a última palavra terminava em **4,94s**, e o
`silencedetect` apontava o último início de silêncio em **6,92s**. Cortar por ele
deixava **2 segundos de sorriso** no fim do hook — exatamente o trecho que o corte
existia para remover.

Com o transcript Scribe da cena (o mesmo do corte, ver FASE 7 acima), o fim da
fala sai de graça — whisper está proibido (regra do dono):

```bash
VU=~/Developer/video-use
$VU/.venv/bin/python $VU/helpers/transcribe.py "$CLIP" --language pt   # cacheado
T=$(dirname "$CLIP")/edit/transcripts/$(basename "$CLIP" .mp4).json
END=$(python3 -c "import json,sys;w=[x for x in json.load(open(sys.argv[1]))['words'] if x.get('type','word')=='word'];print(round(w[-1]['end'],2))" "$T")
CUT=$(awk -v e="$END" 'BEGIN{print e+0.15}')               # ponto de partida; valide fala/gesto
```

O mesmo vale para o **início**: `start` da primeira palavra `- 0.15` apara a cabeça
sem cortar a primeira sílaba. Sem key do ElevenLabs, volte ao `silencedetect` a
`-28dB` e **amostre o fim no olho** (frames em `END`, `END+0.5`, `END+1`) antes de cortar.

Jeito antigo (faster-whisper local): ver `references/SKILL-ffmpeg-OLD-2026-09-23.md`
§"Fim da fala: use a ÚLTIMA PALAVRA (whisper)".

`silencedetect` continua útil para o que ele de fato mede: detectar que a fala
**estourou** o clipe (nenhum silêncio no fim = texto longo demais, regere) e cortar
pausas internas na montagem.


### Fala CURTA demais: o Veo REPETE a frase para preencher o clipe

O teto de 16 palavras protege contra fala longa (voz acelerada, boca parada, legenda
queimada). Mas existe o defeito oposto, e ele é mais difícil de ver: **fala curta
demais num clipe de 8s faz o Veo repetir a frase inteira.**

Caso real (leva 29-08): fala de 13 palavras, `"Si todos los meses terminás en la misma
cuenta, esto es para vos."` O clipe voltou com:

```
Si todos los meses terminás en la misma cuenta, esto es para vos, esto es para vos.
```

A repetição começou em 5,86s e a primeira ocorrência terminava em **4,82s**. Nada no
`ffprobe` acusa: 8,00s, áudio normal, lip-sync correto — o modelo dubla a repetição
direitinho. E o QA por frames não pega, porque a imagem está perfeita. **Só se pega
lendo a transcrição**, e o dono do anúncio pegou antes de mim.

Pior: o corte pela última palavra (a regra da seção anterior) **mantém as duas** —
ele corta em 6,82s, que é o fim da repetição.

**Faixa segura de fala para o Veo em 8s: 11 a 16 palavras.** Abaixo de ~11 o risco de
repetição sobe; acima de 16 a voz acelera. Escreva dentro da faixa.

**No QA, procure repetição na transcrição** — não em frames. `words` = as palavras
do transcript Scribe da cena (`[x for x in json['words'] if x.get('type','word')=='word']`,
chaves `text`/`start`/`end`):

```python
norm = [re.sub(r"[^\w]", "", x["text"]).lower() for x in words]
for L in range(min(8, len(words)//2), 2, -1):
    for i in range(len(norm) - 2*L + 1):
        if norm[i:i+L] == norm[i+L:i+2*L] and norm[i]:
            fim = words[i+L-1]["end"]    # corta no fim da PRIMEIRA ocorrencia
```

Achou repetição? **Não regere** — corte no fim da primeira ocorrência. O trecho até
ali está perfeito, e a regeração pode repetir o padrão, porque a causa é estrutural:
sobra tempo no clipe.

Deixe o aviso visível no log da montagem. Defeito silencioso que ninguém vê é defeito
que chega ao cliente.

### Toda cena é a MESMA pessoa em quadro falando — não peça edição ao modelo

Não peça ao Veo variação de enquadramento, insert de mãos, close de prop ou
qualquer "dinâmica de edição". Cena a cena, sempre o mesmo plano: a pessoa sentada
de frente, falando. É o formato que sai limpo.

Medido numa leva de 6 criativos: as cenas com enquadramento diferente (mãos na
carteira, mãos escrevendo, close do celular) trocaram a personagem ou a voz em
**4 criativos**. As cenas de plano fixo com rosto não deram um defeito.

Split, PiP, corte seco, tarja — tudo isso é **pós-produção** no Remotion (ou
Hyperframes, se o criativo já tem motion lá; ver E.3), aplicada sobre cenas uniformes. Não é coisa que se pede na geração.


## Modos de edição — só DEPOIS do pré-final

**Ordem obrigatória. Editar antes de fechar o pré-final é retrabalho garantido:**
qualquer corte de silêncio ou mudança de ritmo depois desloca todos os pontos de
troca de layout, e a peça inteira precisa ser remontada.

1. **Pré-final** — concatenar as cenas aprovadas no gate. É um vídeo assistível,
   com a fala inteira, sem nenhuma edição de layout.
2. **Pós-produção base** — ~~acelerar~~ (obsoleto: velocidade 1.0, `EDICAO-PADRAO.md`), cortar respiração e
   fala repetida, queimar legenda dentro da caixa viva. Só aqui o **tempo final de
   cada fala** existe de verdade.
3. **Modos de edição** — agora sim, com os segundos reais em mãos.

### O material B: gravação de tela OU b-roll de banco

O que entra na outra metade depende do que o criativo precisa provar:

- **Produto digital** (portal, app, dashboard): gravação de tela em modo mobile,
  navegada como um usuário novo. Ver Modo E (Vitrine Guiada).
- **Produto físico ou serviço** (coleira de pet artesanal, marcenaria, estética):
  cenas de banco público e Pinterest, montadas na ordem da fala. Um plano por
  ideia, nunca um plano genérico "de enfeite".
- **Com ou sem narração:** a fala da personagem pode continuar por cima, ou o
  trecho vira narração pela skill `narracao-hub-tts` com a voz da peça.

A regra de enquadramento é a mesma para os dois: material vertical entra em
moldura deitada com **zoom e foco próprios**, senão a metade fica com sobra morta
e a peça parece dois vídeos empilhados.

### O menu — escolha UM por criativo

Os quatro layouts são linguagens diferentes, não um combo. Três trocas de
linguagem em dez segundos viram mostruário: sinalizam edição automática e
queimam a atenção que o hook comprou. **A peça abre na pessoa, usa UM estilo no
miolo para provar o que ela disse, e volta pra ela no fecho.**

| Estilo | Serve pra | Uso típico |
|---|---|---|
| **Meio a meio** (B em cima, ela embaixo) | provar o que ela acabou de afirmar | uma inserção, na fala do mecanismo |
| **Meio a meio invertido** (ela em cima, B embaixo) | devolver o peso pra ela sem soltar o B | quando a fala volta a ser pessoal |
| **Miniatura / PiP** (B em foco, ela no canto) | demonstração longa em que o B é protagonista | trecho de 4-8s, voz off narrando |
| **Tela cheia dela** | hook e fecho | sempre começo e fim |
| **Print + POV + Meme** | prova social/resultado sem rosto nenhum em quadro | ver abaixo |

### Print + POV + Meme — o único layout sem rosto real

Três zonas empilhadas, fundo preto sólido, sem faixa colorida:

1. **Topo — print de prova.** Screenshot real (chat, dashboard, resultado,
   métrica) — ROAS, ROI, conversa, o que for a prova daquele criativo.
2. **Meio — texto POV.** Amarelo, itálico, negrito, fundo preto. Sempre começa
   com "POV:" e conta a situação em 1-2 linhas — é a piada/gancho, não a oferta.
3. **Base — personagem meme recortado.** PNG com fundo removido (Shrek, Doge,
   etc.), reagindo à situação do POV. É a assinatura visual do formato — sem
   ele vira só um print com legenda.

Sem narração, sem b-roll, sem gravação de tela em movimento — é 100% estático
em composição, o "vídeo" é só o efeito de entrada de cada zona (fade/slide
curto) e som de fundo opcional. Cabe no Modo E como variante estática dele, ou
no Modo D pela biblioteca de escalados (categoria "meme"/"ilustração"). Nunca
misture com faixa vermelha do layout Meio a meio — são dois vocabulários visuais
diferentes.

Implementação de referência (Remotion, com os quatro layouts e o menu de estilos
já escritos): `marketing/anuncios/2026-09-02-BR-gratis/editor/` no projeto
AstroDicas — `src/layouts.ts` (retângulo + zoom + foco de cada layout),
`src/estilos.ts` (o menu), `src/MeioAMeio.tsx` (a viagem entre layouts).

A troca **não é fade**: os dois vídeos viajam entre os retângulos, então a pessoa
encolhe de verdade enquanto o B cresce. Fade entre dois layouts lê como corte de
software; a viagem lê como decisão de edição.

## Estrutura de pastas

```
<PROJETO>/ANUNCIO/<DD-MM>/
  REFERENCIA/                frames de referência (persona, look)
  CRIATIVO-<N>/
    IMG/     cena-1.png ...
    VIDEO/   cena-1.mp4 ...
    PROMPTS/ cena-1.md  ...
    CRIATIVO-<N>.mp4         entregável final
```

**Numeração: continue a série do projeto, não recomece do 1.** Antes de criar as pastas, veja até que número os anúncios já chegaram e siga daí. Se o projeto já tem AD1…AD9, os novos são CRIATIVO-10, 11, 12. Recomeçar do 1 gera colisão de nome no gerenciador de anúncios e some com o histórico de qual criativo é qual.

```bash
ls <PROJETO>/ANUNCIO/*/ | grep -oE "(AD|CRIATIVO-)[0-9]+" | sort -uV | tail -3
```

---

