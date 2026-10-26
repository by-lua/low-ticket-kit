# Legenda — detalhe técnico (movido do SKILL.md em 26/10/2026)

> Resumo e regra: `EDICAO-PADRAO.md` §5. Aqui: spec completa da KaraokeV2, fallback ffmpeg, área que não corta. Trechos sobre aceleração estão obsoletos (velocidade 1.0).


### Legenda, motion, trilha — Remotion (legenda), Hyperframes (motion), ffmpeg (mix)

O Grok já entrega voz, então música é opcional e fica baixa. Legenda queimada só na pós, casando com o estilo do criativo vencedor. Ver skills `remotion-create`, `remotion-captions` (**menos** a parte de transcrição: ela usa whisper.cpp, proibido — os timestamps vêm do Scribe/TTS, ver Stack de edição), `remotion-render`.

Legenda **animada** além do karaokê (palavra que entra com motion, destaque que
cresce, texto que interage com o sujeito): Hyperframes — skills `embedded-captions`
+ `captions-overlay` (doutrina: legenda é overlay por cima, nunca faixa reservada).
Mesma regra de timestamp: entregue o `transcript.json` pronto, não rode o
`hyperframes transcribe` delas.

#### ⭐ LEGENDA KARAOKÊ TIKTOK — CANÔNICA v2 (padrão fixo do dono, 2026-09-23)

Por que v2: a v1 (`references/legenda-karaoke-tiktok-v1-OLD.jsx`) tinha três defeitos
que o dono apontou: (1) **não acompanhava a fala** — timestamps de whisper/distribuição
por duração, grudados um no outro, legenda ficava na tela nas pausas; (2) **borda
grotesca** — `WebkitTextStroke` fica centrado na borda da letra, come o desenho e
serrilha as quinas, e o chroma-key do fundo `#0000FF` deixava halo; (3) **pequena e
chapada**, sem profundidade. Aprovado visualmente em `mapa-do-tarot/criativos/v4_imperatriz_KARAOKE-V2.mp4`.

**⛔ NUNCA REIMPLEMENTAR A LEGENDA DE CABEÇA (regra da dona, 25/10/2026 — erro repetido 3x no
mesmo dia, Mapa do Tarot CRIATIVO-7/30: tamanho errado, depois chunk errado, depois contorno
errado).** A tabela de spec abaixo (fonte, tamanho, posição) é **descrição**, não a fonte da
verdade — a fonte da verdade é o **projeto Remotion já aprovado**:
`mapa-do-tarot/criativos/BR/CRIATIVO-1/intermediarios/remotion-cap` (componente `KaraokeV2.jsx`
+ `words.json`). Traduzir a tabela de cabeça pra outra ferramenta (ffmpeg/ASS, CSS reescrito,
qualquer coisa) SEMPRE perde detalhe — tamanho de fonte CSS não bate 1:1 com outro motor de
render, chunk de palavras vira "parece bom" em vez do valor exato, contorno vira chute.
**Se o criativo já tem (ou pode copiar) um projeto Remotion: usa esse projeto, roda
`npx remotion render` nele, não reescreve o componente.** Só quando literalmente não existe
Remotion disponível (ambiente sem Node, sem tempo de setup) é que entra um fallback — e mesmo
nesse caso, **copia os valores exatos do componente `.jsx` linha por linha** (abre o arquivo,
lê o JSX, transpõe cada número pro novo formato) em vez de reconstruir a partir da tabela
resumida desta página. A tabela serve pra CONFERIR depois (bateu com o `.jsx`?), nunca pra
GERAR o prompt/script do zero.

**Passo 1 — tempo de cada palavra: `scripts/legenda_align.py` (alinhamento forçado, NÃO whisper).**
A gente sempre tem o texto falado (roteiro/prompt do Veo/texto do TTS). O alinhador
(wav2vec2/MMS via `ctc-forced-aligner`, local, grátis, CPU ~45s pra 30s de áudio)
só descobre ONDE cada palavra do roteiro cai no áudio — não adivinha palavra, então
não erra texto nem deriva no tempo. Venv pronta em `~/Developer/legenda-karaoke`:

```bash
~/Developer/legenda-karaoke/.venv/bin/python ~/.claude/skills/criativo-ads-video-orq/scripts/legenda_align.py \
  final_sem_legenda.mp4 roteiro.txt -o src/words.json        # --lang por (padrão)
```

- `roteiro.txt` = EXATAMENTE o que é falado, na ordem, com pontuação (pontuação quebra linha).
  Se o Veo improvisou/trocou palavra, corrija o roteiro pro que foi dito de fato.
- Números viram extenso só pro alinhamento ("78" alinha como "setenta e oito"), exibição fica "78".
- Saída: linhas de 1-3 palavras, quebra em pontuação e em pausa >0,30s; linha só existe
  enquanto é falada (+0,15s); **nas pausas a tela fica limpa**. Palavra ativa não pisca
  em gap <0,30s.
- Rodar no vídeo **montado final** (tempo da saída), não nos clipes soltos.
- Ele imprime palavras de confiança baixa: confira essas no vídeo.
- Alternativa paga equivalente: Scribe do video-use (precisa `ELEVENLABS_API_KEY`).
- Proibido: `hyperframes transcribe` (whisper `small.en`, só inglês), faster-whisper, whisper.cpp,
  `remotion-captions` com install-whisper-cpp, e "distribuir por duração".

**Passo 2 — render: `references/legenda-karaoke-tiktok-CANONICA.jsx` (componente `KaraokeV2`).**
Vídeo e legenda na MESMA composição Remotion (`<OffthreadVideo>` + legenda por cima) —
**sem fundo #0000FF, sem chroma-key, sem overlay ffmpeg**. Composição com o fps nativo
do vídeo (Veo = 24, montado pode ser 25) e 1080×1920. Precisa `@remotion/google-fonts`
na mesma versão do `remotion`. Projeto de referência pronto:
`mapa-do-tarot/criativos/BR/CRIATIVO-1/intermediarios/remotion-cap` (composição `KaraokeV2`,
vídeo em `public/`).

| Parâmetro | Valor |
|---|---|
| Fonte | **Montserrat 900** (`@remotion/google-fonts/Montserrat`), caixa alta, `letterSpacing 0.5px` |
| `fontSize` | **60** (canvas 1080×1920) |
| Posição | **centro vertical em 70% da altura** (`top: height*0.70`, `translateY(-50%)`) — centra igual com 1 ou 2 linhas, dentro da banda 4:5, fora do rodapé |
| Largura | `left 4%`, `width 92%`, flex-wrap centralizado, `gap 0 26px`, `lineHeight 1.25` |
| Cor base / ativa | `#FFFFFF` / `#FFD400` — SÓ a palavra sendo falada fica amarela |
| Contorno | **anel de 24 `text-shadow` de 5px, preto** — redondo, todo por FORA da letra (nunca `WebkitTextStroke`) |
| Profundidade | `0 7px 0 #000` (extrusão) + `0 10px 14px rgba(0,0,0,.55)` (sombra) |
| Pop | palavra ativa escala ~1,05 com `spring` (damping 12, stiffness 220) — o gap 26px absorve; não aumente o pop sem aumentar o gap (senão as palavras grudam: "IMPERATRIZSÓ") |
| Chunk | 1-3 palavras, vem pronto do `legenda_align.py` |

`words.json`: `[{ start, end, words: [{ text, start, end }] }, ...]`.

Jeito antigo (v1: Arial + WebkitTextStroke + chroma `#0000FF`, tamanhos 34/72): ver
`references/legenda-karaoke-tiktok-v1-OLD.jsx` e `references/SKILL-ffmpeg-OLD-2026-09-23.md`.

QA obrigatório: extrair frames em tempos de fala e provar que existe UMA palavra
`#FFD400` E que a posição do amarelo MUDA entre frames (karaokê real, não amarelo
fixo). Amarelo ausente ou estático = FAIL.

#### Fallback — legenda sem Remotion (ffmpeg puro): padrão validado da VSL2-MARTA

Só fallback: o padrão é o karaokê canônico acima. (O `render.py --build-subtitles`
do video-use cai nesta mesma classe — SRT/ASS queimado — e serve só aqui.)
Quando não há pipeline Remotion montado pro projeto (caso comum de VSL gerada
via `hub-video-playwright` + montagem própria em ffmpeg), reproduza o estilo
aprovado da VSL2-MARTA em vez de inventar um novo:

- **Fonte Inter Bold, sem itálico.** Itálico fino (ex. Georgia) foi tentado numa
  VSL e reprovado pelo usuário — pareceu fraco/errado comparado ao padrão.
- **Amarelo `#FFD21E`** (ASS: `&H001ED2FF`), contorno preto fino, sem fundo.
- **Fonte fina + linha larga, não fonte grande + linha curta.** São duas
  variáveis independentes e fáceis de confundir: "tá grosso/enorme" pede
  `FontSize`/`Outline` menores; "não preenche o espaço, fica um bloco
  centralizado sobrando lateral" pede `MAXCH` maior e `MarginL`/`MarginR`
  menores. Valores validados no monge (VSL-MONGE, 2026-09-08), depois de
  passar por "grosso demais" (FontSize=17) e "fino demais, pouca largura"
  (FontSize=12 com MAXCH=34):

  ```python
  MAXCH = 56  # char por linha antes de quebrar
  style = (
      "FontName=Inter,FontSize=10,Bold=1,Italic=0,"
      "PrimaryColour=&H001ED2FF,OutlineColour=&H00000000,BackColour=&H00000000,"
      "BorderStyle=1,Outline=1.0,Shadow=0.4,Alignment=2,MarginV=100,MarginL=15,MarginR=15,WrapStyle=0"
  )
  ```

  2 linhas por cue, tempos distribuídos proporcionalmente por caractere dentro
  da janela de fala da cena. Isso é ponto de partida, não valor fixo — confirme
  sempre extraindo um frame antes de aceitar como pronto (ver abaixo).
- **Posição embaixo, nunca no meio nem cobrindo boca/rosto.** Em 1080×1920 via
  filtro `subtitles` do ffmpeg: `MarginV≈100` (distância da base), dentro da
  faixa "que não corta" descrita abaixo.
- Implementação de referência (gera SRT chunked + queima via
  `ffmpeg -vf subtitles=...:force_style=...`, sem precisar de Remotion):
  `PERSONAGENS/MONGE/VSL-MONGE/TOOLS/gen_captions2.py` no projeto NUMERO-MESTRE.
  Copie e adapte (troca só o dict de falas e a lista de durações por cena) em
  vez de reescrever o estilo do zero.
- **Sempre compare contra um frame do vídeo de referência aprovado** (ex.:
  `PERSONAGENS/MARTA/VSL2-MARTA/VIDEO/VSL2-MARTA-legenda.mp4`) antes de dar como
  pronta — a primeira tentativa raramente bate no tamanho/posição certos de
  primeira, e o usuário nota na hora se destoar do padrão já validado.

#### Legenda mora na área que não corta — regra fixa

Todo vídeo final é 1080 × 1920. A legenda **nunca** encosta nas faixas que a
plataforma cobre ou corta:

- **Topo: 290 px livres.** Nome de perfil e notificações no Stories; corte no feed.
- **Base: 360 px livres.** Legenda da plataforma, nome do áudio, botões, "seguir".
- **Laterais: 60 px**, atenção redobrada à direita (botões de interação).

Isso deixa a legenda dentro de uma **caixa viva de 960 × 1270 px centralizada** — a
mesma do prompt 07 da skill `modelagem-escalados`, porque o feed recorta um 9:16
para 1080 × 1350 centralizado. Na prática: a linha de legenda assenta com a base
entre ~1300 px e ~1560 px do topo, nunca abaixo disso.

Duas armadilhas medidas em produção:

1. **Legenda de duas linhas cresce para cima, não para baixo.** Ancore a caixa pela
   base, senão a segunda linha invade a faixa dos 360 px.
2. **Legenda que "não pula"** — largura fixa e base fixa. Legenda que muda de altura
   a cada frase denuncia automação e cansa o olho. Ver a memória de pós-produção do
   projeto AstroDicas (1.15x, corte de respiração, legenda dourada estável).

#### Acelerar é padrão, não opcional
> ⚠️ **OBSOLETO (26/10/2026)** — vale `references/EDICAO-PADRAO.md` (velocidade 1.0, sem aceleração).

**Todo criativo final acelera na pós-produção — sempre, em todos os modos.** É o
que faz a fala soar mais rápida e a peça não arrastar; sem isso o ritmo fica de
vídeo institucional, não de anúncio. Acelere o pré-final inteiro (vídeo + áudio
juntos, `setpts`+`atempo`, nunca só um dos dois — descasa lip-sync). Confirme a
legenda depois de acelerar: tempo de cena muda, ponto de troca de frase muda
junto.

- **Com personagem falando em quadro (lip-sync gerado no Veo): 1.10x a 1.20x.**
  Acima disso a boca visivelmente descasa da voz.
- **100% narração off / b-roll / gravação de tela (sem boca sincronizada pra
  proteger): 1.30x a 1.40x.** Testado em produção — 1.20x ficou lento demais
  pro ritmo de criativo demonstrativo; sem lip-sync, o teto sobe.
  Exceção aprovada: VO de TTS já em ritmo de anúncio (MiniMax, Mapa do Tarot) →
  **1.15x** é o ponto (dono, 2026-09-23: 1.25x ficou rápido demais). Acelere NO REMOTION: composição
  que roda o render final via `<OffthreadVideo playbackRate={1.15}>`,
  `durationInFrames = ceil(dur*fps/1.15)` — vídeo, voz e karaokê queimado andam juntos,
  pitch preservado (confira F0 antes×depois; tem que ficar ~igual, não +15%).

#### Tarja de marca — OPT-IN, não é mais padrão (regra da dona, 2026-10-04)

⚠️ **Mudança 2026-10-04: a tarja deixou de ser automática em qualquer modo.**
Antes desta data era obrigatória nos Modos A-D; a dona reportou que toda
entrega está saindo com a faixa vermelha sem ter sido pedida e não quer isso
por padrão. **A tarja só entra se o brief daquele criativo pedir
explicitamente.** Sem pedido explícito, nenhum criativo (A, B, C, D ou E) leva
tarja — e isso vale também pro Modo E, que já não usava por outro motivo (ver
`criativo-ads-video-orq/references/EDICAO-PADRAO.md`).

Quando o usuário pede ("quero a faixa com o nome do produto", "bota tarja"),
siga as regras abaixo. Fora isso, pule esta seção inteira.

Toda peça **que pedir tarja** leva uma **tarja sólida vermelha, letra branca, com o nome do
produto**, fixa na área que não corta (topo ou base da caixa viva de
960 × 1270 px, nunca dentro dela por cima da legenda de fala — são duas coisas
diferentes, não competem pelo mesmo espaço).

- **Onde:** topo (abaixo dos 290px livres) OU base (acima dos 360px livres) —
  escolha um lado e mantenha em todo o criativo, nunca alterna.
- **O quê:** nome do produto/oferta, curto — não é headline nem CTA, é
  identificação de marca visível o tempo todo.
- **Cor:** fundo vermelho sólido, texto branco, alto contraste — não é a legenda
  de fala (essa segue o estilo do criativo vencedor); a tarja é elemento fixo,
  a legenda de fala é dinâmica por frase.
- **Presença:** do primeiro ao último frame, ou pelo menos do fim do hook até o
  CTA — nunca só num flash de 1-2s, senão ninguém lê.

**Referência canônica (validada, print salvo em produção):** faixa vermelha com
borda rasgada (efeito "papel picado"), texto branco em caixa alta, 2-3 linhas,
sentada exatamente **na costura do Meio a meio** — onde o bloco de cima (tela:
planilha, dashboard, gravação) encontra o bloco de baixo (pessoa em quadro
falando). No bloco de cima ainda cabe uma **miniatura pequena no canto superior
direito** (a mesma pessoa, reagindo) — três camadas visuais ao mesmo tempo:
tela grande, rosto pequeno reagindo, faixa de manchete no meio, pessoa falando
embaixo com legenda própria (branca, sem fundo, separada da faixa). A frase da
faixa é a manchete que para o scroll ("não entra em X antes desse vídeo"), não
o CTA nem o preço — isso fica na fala. Quando o layout é Meio a meio, a faixa
**pode** sentar na costura em vez do topo/base da caixa viva; nos outros
layouts (Tela cheia, Miniatura/PiP) ela volta pro topo ou base, fora da área
que corta.

---

