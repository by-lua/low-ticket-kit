#!/usr/bin/env bash
# yt-txt.sh — transcrição limpa de vídeo, playlist ou canal do YouTube.
# uso: yt-txt.sh <url> [outdir] [max_videos]
#
# Método rápido: youtube-transcript-api (endpoint timedtext direto, sem
# extração de player por vídeo) rodando em paralelo via xargs -P.
# ~0.6s/vídeo medido em canal real, vs ~2-3s/vídeo do yt-dlp sequencial.
# Fallback automático por vídeo: se o rápido falhar, tenta yt-dlp (legendas).
set -uo pipefail

URL="${1:?uso: yt-txt.sh <url-video|playlist|canal> [outdir] [max]}"
OUT="${2:-./transcricoes}"
MAX="${3:-}"
LANGS_STR="pt-BR pt en en-orig"
JOBS="${YT_TXT_JOBS:-8}"

mkdir -p "$OUT"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

case "$URL" in
  *youtube.com/@*|*youtube.com/c/*|*youtube.com/channel/*)
    case "$URL" in */videos|*/streams|*/shorts) ;; *) URL="${URL%/}/videos";; esac ;;
esac

# 1) lista id + título (rápido, uma chamada só, sem extrair player por vídeo)
LIST_ARGS=(--flat-playlist --print "%(id)s	%(title)s" --no-warnings)
[ -n "$MAX" ] && LIST_ARGS+=(--playlist-end "$MAX")
yt-dlp "${LIST_ARGS[@]}" "$URL" > "$TMP/list.tsv"

if [ ! -s "$TMP/list.tsv" ]; then
  echo "não consegui listar vídeos de: $URL" >&2
  exit 1
fi

slugify() {
  # mesmo espírito do --restrict-filenames do yt-dlp
  printf '%s' "$1" | tr -c 'A-Za-z0-9._-' '_' | cut -c1-120 | sed 's/_*$//'
}

# 2) para cada vídeo: tenta youtube-transcript-api; fallback yt-dlp na hora
fetch_one() {
  local id="$1" title="$2" out="$3" stem slug lang f
  slug="$(slugify "$title")_[${id}]"
  stem="$out/$slug"

  if command -v youtube_transcript_api >/dev/null 2>&1; then
    # shellcheck disable=SC2086 (LANGS_STR é lista fixa sem aspas/glob)
    if youtube_transcript_api "$id" --languages $LANGS_STR --format text \
         > "$stem.txt" 2>"$stem.err" \
       && [ -s "$stem.txt" ] \
       && ! head -c 40 "$stem.txt" | grep -q "^Could not retrieve"; then
      # remove linhas repetidas (legenda automática duplica trecho)
      awk '!seen[$0]++' "$stem.txt" > "$stem.tmp" && mv "$stem.tmp" "$stem.txt"
      rm -f "$stem.err"
      echo "OK   $slug  ($(wc -w < "$stem.txt") palavras) [rápido]"
      return 0
    fi
    rm -f "$stem.txt" "$stem.err"
  fi

  # fallback: yt-dlp (vídeo isolado, mais lento mas mais robusto)
  local tmp2; tmp2="$(mktemp -d)"
  yt-dlp --skip-download --write-subs --write-auto-subs \
    --sub-langs "pt-BR,pt,en,en-orig" --sub-format vtt \
    --no-warnings --ignore-errors --no-progress \
    -o "$tmp2/v.%(ext)s" "https://youtu.be/$id" >/dev/null 2>&1

  for lang in $LANGS_STR; do
    f="$tmp2/v.$lang.vtt"
    if [ -f "$f" ]; then
      sed -e "1,/^$/d" -e "/-->/d" -e "/^WEBVTT/d" -e "/^Kind:/d" -e "/^Language:/d" \
          -e "s/<[^>]*>//g" -e "/^[0-9]*$/d" "$f" \
        | sed "s/[[:space:]]*$//" | grep -v "^$" | awk '!s[$0]++' > "$stem.txt"
      rm -rf "$tmp2"
      echo "OK   $slug  ($(wc -w < "$stem.txt") palavras) [fallback yt-dlp]"
      return 0
    fi
  done
  rm -rf "$tmp2"
  echo "FAIL $slug  (sem legenda em nenhum método)" >&2
  return 1
}
export -f fetch_one slugify
export LANGS_STR

# 3) roda em paralelo — id/title/outdir passados como argv (NUL-separado, sem
# interpolação de string) para não sofrer injeção com título malicioso
awk -F'\t' -v out="$OUT" -v RS='\n' 'BEGIN{ORS=""} {printf "%s%c%s%c%s%c", $1, 0, $2, 0, out, 0}' "$TMP/list.tsv" \
  | xargs -0 -n 3 -P "$JOBS" bash -c 'fetch_one "$1" "$2" "$3"' _

n_total=$(ls -1 "$OUT"/*.txt 2>/dev/null | wc -l)
echo "TOTAL: $n_total transcrições em $OUT"
[ "$n_total" -gt 0 ] || { echo "nenhuma legenda (vídeo sem CC) -> usar skill watch/Whisper" >&2; exit 1; }
