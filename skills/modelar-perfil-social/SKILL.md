---
name: modelar-perfil-social
description: Modela um perfil de Instagram ou TikTok que está crescendo (persona de IA, vídeo sem fala, música em alta) e recria com uma persona NOSSA de rosto fixo, vídeo por vídeo, no Google Flow, com a mesma música do original, texto de story no topo e legenda orgânica com CTA leve pra oferta. Use quando a dona mandar um @ ou link de perfil e pedir "modela esse perfil", "cria uma persona igual", "refaz os vídeos dela com a nossa", "perfil orgânico pra oferta X", ou citar abuelabelica / La Jefa Rosa como exemplo.
---

# modelar-perfil-social

Referência viva: **La Jefa Rosa** (`LOW-TICKET/PERFIS-INSTAGRAM/la-jefa-rosa/`, ficha em `PERSONA.md`),
modelada de @abuelabelica em 22/10/2026. Abra a ficha dela antes de começar: é o padrão de saída.

## Regras da dona (não negociáveis)

1. **Um clipe só por vídeo, no máximo 8 s** (menor pode, maior não; dona 22/10). **Todo vídeo modela UM vídeo original**, e a **música é a MESMA do original** (mesmo trecho, mesma duração ou o corte do nosso clipe). Sem fala.
2. **Texto no topo = texto de story do Instagram**: caixa branca arredondada, letra preta, centralizado, colado no topo (y≈70 de 1280). **Nunca sobre o rosto**: conferir os quadros do close antes de entregar.
3. **Texto muda em todo vídeo** e tem que puxar o conceito da oferta (persona, dor, mecanismo), sem vender: a oferta aparece como a virada de vida da persona.
4. **Clima orgânico.** Nada de preço, link ou oferta no vídeo. Legenda = frase orgânica + **CTA pequeno no fim** ("👉 el link está en mi bio").
5. **Roupa varia a cada vídeo** (dona 22/10): rosto e cabelo fixos; mesmo estilo da persona (ex.: lenço, óculos, argolas, blusa bordada, xale), mas trocando cores e peças (lenço, armação dos óculos, blusa, vestido, xale) com paleta que combina. Bonito, nunca estranho. **Ordem da troca de roupa (dona 22/10):** (1) troca a roupa na **imagem da personagem sozinha** (`01-persona/variantes/<vídeo>.jpg`, i2i só da persona com `outfit_prompt`), (2) a dona aprova, (3) essa variação vira a **imagem 1 da cena** junto com o quadro do original, como sempre (o `scene_prefix` lista a roupa nova em `{outfit_list}`). Nunca trocar roupa depois da cena pronta nem tirar a lista de roupa do prompt da cena. No plano: campo `outfit` por vídeo.
5b. **Ambiente:** modelar em cima do vídeo-base, adaptando pro mercado (ex.: LATAM geral, sem bandeira, placa ou monumento de um país só).
6. **Imagem e vídeo pelo Google Flow** (não gastar o GPT). **Sempre imagem da cena ANTES do vídeo**, gerada no próprio Flow: vídeo com mais de uma cena = uma imagem por cena (i2i persona + quadro daquela cena do original), depois um i2v por imagem. Vídeo direto do texto ou de imagem de outra cena = o Flow alucina. Persona aprovada pela dona ANTES do primeiro vídeo; primeiro vídeo aprovado antes do lote.

## Fluxo

### 1. Baixar e ler a referência
- Mídia de terceiro vai pra `PROJETOS-MIDIA/PERFIS-E-CANAIS/<PROJETO>-<perfil>/` (regra do `PROJETOS/CLAUDE.md`), com symlink `00-referencia` na pasta do perfil.
- Grade do perfil: `agent-browser --session pinterest` (perfil sem login vê bio + links dos reels). A API pública do IG bloqueia.
- `yt-dlp --write-info-json -o "%(upload_date)s_<código>.%(ext)s" https://www.instagram.com/reel/<código>/` por reel (TikTok: `yt-dlp` na URL do vídeo).
- Contact sheet por vídeo (`ffmpeg ... fps=6/<dur>,tile=6x1`) e transcrição local (`whisper-ctranslate2 --model small`). Se só tiver música, a fórmula é visual + música.
- Tabela na ficha: código, duração, curtidas, cena, legenda dela. **O mais antigo é o V01** (valida a persona).

### 2. Persona
- Ler a oferta antes (CLAUDE.md da raiz: Gate 0): persona compradora, dor, mecanismo, vocabulário permitido/proibido (ex.: VSL LATAM: "dinero", nunca "plata"; sem carga religiosa pesada).
- Reaproveitar o rosto de uma persona nossa já existente quando houver (ex.: Rosa da VSL), pra quem vem do perfil reconhecer na VSL.
- Ficha `PERSONA.md`: nome pan-mercado, @ livre (checar no IG pelo título da página: "Profile não está disponível" = livre), bio com CTA leve, link da bio com UTM, CANON visual, plano dos vídeos.
- Imagem-base: `flow.sh image i2i` com a foto da persona → 2 opções → dona escolhe.

### 3. V01 sozinho, depois o lote
- Plano JSON (modelo: `la-jefa-rosa/02-videos/plano-v02-v07.json`): para cada vídeo, ref_video, ref_frame (quadro do original), duração (4/6/8/10), prompt da cena, prompt do movimento, 2 linhas de texto (`linha|emoji`), legenda.
- **Gate da dona (22/10): primeiro SÓ as imagens** — `python3 scripts/lote_flow.py plano.json --so-imagens` (com roupa nova sai o par `base-roupa-base.jpg` + `base.jpg`), mostrar contact sheet, a dona aprova; **só depois** rodar sem a flag pra fazer os vídeos (imagem aprovada é reaproveitada, não regera).
- Rodar: `python3 scripts/lote_flow.py plano.json` em background. Por vídeo: i2i (persona + quadro do original) → pausa 120–180 s → i2v Omni Flash → pausa → `scripts/montar.sh`.
- Montagem avulsa: `scripts/montar.sh <saida> <original.mp4> <dur> "<linha1>" "<linha2|emoji>" clip1.mp4 [clip2.mp4@8.3]` (`@N` corta o clipe em N s; música do original com fade de 0,8 s; cor bt709).

### Prompt de movimento: LONGO e detalhado (dona 22/10)
O Flow é complexo: ação vaga = objeto some, troca de mão, óculos somem. Prompt de movimento tem que ter:
- câmera (distância fixa, quem filma);
- **em qual mão está cada objeto do começo ao fim** (copo, maço de dinheiro, volante);
- ação **por segundo** (0–3 s, 3–6 s, 6–8 s), uma coisa de cada vez;
- bloco de continuidade (objeto não some nem troca de mão, óculos não somem, 5 dedos, rosto e roupa iguais, fundo parado, sem fala).
Modelo pronto: `la-jefa-rosa/02-videos/plano-v02-v07.json` (V05–V07). Mesmo assim, se no QA algo sumir no fim: **cortar antes** com `clip.mp4@<segundos>` (V04: copo sumia em 5,5 s → corte 5,3 s).

### Por que a imagem da cena saía errada e como acertou (22/10, V05)
A cena é gerada com **2 referências**: imagem 1 = persona, imagem 2 = quadro do vídeo original. O prompt
precisa dizer com clareza **o que vem de cada uma**, senão o Flow mistura:
- **Erro 1, personagem errada:** tirei do prompt a lista da roupa da persona ("lenço vermelho, xale escuro…
  EXATAMENTE como na imagem 1") pra trocar a roupa. Sem essa âncora, o Flow tratou a roupa da imagem 2
  como a roupa "certa" e trouxe junto **a mulher do original**, só recolorida. A lista explícita da roupa
  da imagem 1 é o que segura a identidade. **Não mexer na roupa e no rosto na mesma geração.**
- **Erro 2, cena diferente do original:** o prompt dizia que a imagem 2 era "só referência do lugar". O
  Flow pegou o lugar e inventou o enquadramento (ela sentada, plano aberto, maço pequeno).
- **O que acertou:** (a) imagem 1 com rosto, cabelo e roupa listados e "EXATAMENTE como na imagem 1"; (b)
  imagem 2 descrita como referência da **composição 1:1** (mesmo corte, distância, ângulo, pose, posição
  das mãos, tamanho dos objetos); (c) a descrição da cena repete o enquadramento do original em texto
  (ex.: "close de baixo, inclinada pra câmera, leque enorme de notas ocupando a metade de baixo da tela").
  Prompt pronto: `scene_prefix` em `la-jefa-rosa/02-videos/plano-v02-v07.json`.
- **Pessoa do original grande/de perto no quadro = borrar a cabeça dela ANTES de anexar** (padrão, não conserto).
  O V07 puxou rosto, cabelo e lenço estampado da mulher original e a dona pegou. Receita: `ffmpeg -i quadro.jpg
  -filter_complex "[0]crop=W:H:X:Y,boxblur=40:5[b];[0][b]overlay=X:Y" quadro-sem-rosto.jpg` + no prompt "a área borrada
  da imagem 2 é só onde vai a cabeça DELA (rosto, cabelo e lenço da imagem 1)". Mesmo assim, gate lado a lado com a persona.
- Roupa diferente por vídeo: troca primeiro na imagem da persona sozinha, aprova, e usa essa variação como imagem 1 da cena.

### Vídeo que se afasta da imagem aprovada (V05, 22/10)
O i2v começou no close aprovado e no meio a câmera recuou e o leque de notas encolheu até virar um maço pequeno.
Motion prompt de cena em close tem que **travar o enquadramento**: "camera LOCKED at the same framing as the image,
NO zoom out, no pulling back"; o objeto principal "stays exactly the same size, never folds/shrinks"; só movimentos
pequenos. QA = contact sheet do **clipe inteiro** a 1 fps comparado com a imagem aprovada, não só o fim.

### 4. QA antes de entregar
- Contact sheet do final: mesmo rosto em todos, texto fora do rosto, nada sumindo ou derretendo (óculos sumiram no fim do clipe 2 do V01 → cortado em 8,3 s).
- `ffprobe`: 720×1280, duração certa.
- Registrar na ficha + STATUS da oferta + `_memoria/planos-criativos.md` se for criativo.

## Flow: o que já quebrou (22/10/2026)
- **Todo envio ao Flow passa por `~/.claude/skills/flow-video-playwright/scripts/flow.sh`** (ritmo e fila compartilhados com os outros panes, freio de bloqueio). O `lote_flow.py` já usa ele; perfil 2 = `FLOW_PROFILE=flow-gflow-2`. Leia a skill `flow-video-playwright` antes.
- **Nunca** operar a UI do Flow por agent-browser/CDP: "atividade incomum".
- Perfil `flow-gflow` ocupado por outro pane → usar `flow-gflow-2` (login próprio, feito pela dona). Cópia de diretório perde o login em ~25 min; perfil novo = `gflow auth login --profile <nome> --browser chrome` com a dona confirmando.
- `novo-projeto` do `gflow_ref.py` é fixo no `flow-gflow`: no perfil 2, reusar um `--project` existente.
- **Troca de personagem (Omni Flash editando vídeo enviado, `scripts/flow_swap.py`)**: ao subir vídeo o Flow pede "Direitos de uso deste vídeo". Vídeo de terceiro = NÃO aceitar em nome da dona; a dona escolheu (22/10) ficar no imagem→vídeo, usando só um quadro do original como referência de ambiente.
- **Nunca matar o lote no meio de uma geração e reiniciar logo em seguida**: dá dois envios colados e o Flow bloqueia ("atividade incomum", 22/10). Pausar só durante a linha "pausa" do log; reiniciar respeitando o intervalo.
- Ritmo: 45–120 s mínimo entre envios, máx. ~8 por 30 min; bloqueio = parar 45 min.
