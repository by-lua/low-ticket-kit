---
name: yt-transcricao
description: Pega a transcrição completa de vídeos, playlists ou canais inteiros do YouTube sem login e sem API key. Método rápido (youtube-transcript-api em paralelo, ~0.4-0.6s/vídeo) com fallback automático pra yt-dlp por vídeo. Entrega um .txt limpo por vídeo (sem timestamps, sem tags), preferindo pt-BR e caindo para inglês. Use sempre que o usuário mandar um link do YouTube e pedir para ver, ler, resumir, analisar ou estudar o conteúdo — inclusive "vê tudo desse canal", "lê essa playlist", "o que esse vídeo fala".
allowed-tools: Bash, Read, Grep, Glob
---

# yt-transcricao

Transcrição de YouTube em texto limpo. Um comando.

## Método (por que é rápido)

`yt-dlp` sozinho abre uma extração completa de player por vídeo (~2-3s cada,
sequencial) — pra 184 vídeos isso é ~8min. O gargalo é a extração do player,
não a legenda em si.

`yt-txt.sh` faz diferente:
1. Lista id+título do canal/playlist com **uma** chamada `yt-dlp --flat-playlist` (~1s pra 184 vídeos).
2. Busca a legenda de cada vídeo direto no endpoint `timedtext` via
   [`youtube-transcript-api`](https://github.com/jdepoix/youtube-transcript-api)
   (CLI Python, instalado via `uv tool install youtube-transcript-api`),
   rodando **8 em paralelo** (`xargs -P`).
3. Fallback automático por vídeo: se o rápido falhar (raro — vídeo sem CC
   detectável, erro de rede), tenta `yt-dlp` isolado pra aquele vídeo só.

Medido em canal real (@jhonatasilvai, 10 vídeos, sem login): **10/10
sucesso, ~0.44s/vídeo**, zero rate-limit/429. yt-dlp sequencial bateu 429
(Too Many Requests) na mesma sessão de teste — o endpoint timedtext aguenta
paralelismo bem melhor que a extração de player do yt-dlp.
Estimativa pra 184 vídeos: ~80s (vs ~8min do yt-dlp puro).

## Uso

```bash
~/.claude/skills/yt-transcricao/scripts/yt-txt.sh <url> [outdir] [max_videos]
```

- `<url>`: vídeo, playlist, `@canal`, `/channel/...`, `/c/...` (canal cru vira `/videos` sozinho).
- `[outdir]`: padrão `./transcricoes`.
- `[max_videos]`: corta a playlist/canal nos N primeiros. Vazio = tudo.

Saída: um `Titulo [videoID].txt` por vídeo, texto corrido, dedup de linha (legenda automática repete muito).

## Regras

- Depende de `youtube_transcript_api` no PATH (`uv tool install youtube-transcript-api`). Se não tiver instalado, o script cai direto pro fallback yt-dlp em todo vídeo — mais lento mas funciona.
- **Canal grande ainda vale rodar em background** se >50 vídeos (mesmo rápido, 200+ vídeos passa de 1min). Conte antes:
  `yt-dlp --flat-playlist --print "%(title)s" <url>/videos | wc -l`.
- Ajuste de paralelismo: `YT_TXT_JOBS=N yt-txt.sh ...` (padrão 8). Não tem evidência de rate-limit do YouTube até 8 workers; suba com cautela.
- Idioma: prioridade `pt-BR > pt > en > en-orig`. Um arquivo por vídeo.
- Vídeo **sem nenhuma legenda** falha (FAIL na saída, script continua os outros) → aí sim escale para a skill `watch` (baixa o áudio e transcreve por Whisper) ou `hub-transcricao-audio` (lote no TurboScribe).
- Não precisa de cookie/login para vídeo público. Vídeo privado/idade-restrita: use o fallback yt-dlp direto com `--cookies-from-browser chromium`.

## Depois de baixar

Não leia os 184 arquivos de uma vez. Ordem certa:
1. `wc -w transcricoes/*.txt | sort -n` — ver tamanho e nomes.
2. Ler os títulos para mapear os temas.
3. `grep -il "<tema>" transcricoes/*.txt` para achar os relevantes.
4. Ler inteiros só os que importam para a pergunta.
