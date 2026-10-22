#!/usr/bin/env bash
# Gera narracao WAV pelo NinjaVoice (NinjaBR Hub).
# uso: narrar.sh <saida.wav> "<texto>" [voiceId] [languageCode]
set -euo pipefail

OUT="${1:?saida.wav}"; TEXT="${2:?texto}"
VOICE="${3:-0s0tckZNA4EDjsNWIGpn}"   # Brandon, masc
LANG="${4:-pt-BR}"
API="https://captions.ninjabrhub.online/api/captions/tts"

if [ "${#TEXT}" -gt 2000 ]; then
  echo "erro: texto com ${#TEXT} chars, limite 2000. Quebre em blocos." >&2; exit 2
fi

BODY=$(TEXT="$TEXT" VOICE="$VOICE" LANG="$LANG" python3 -c \
  'import json,os;print(json.dumps({"text":os.environ["TEXT"],"voiceId":os.environ["VOICE"],"languageCode":os.environ["LANG"]}))')

RESP=$(curl -sS -X POST "$API" -H 'content-type: application/json' -d "$BODY")
URL=$(printf '%s' "$RESP" | python3 -c 'import sys,json;d=json.load(sys.stdin);print(d.get("audio_url",""))')
[ -n "$URL" ] || { echo "erro: sem audio_url. resposta: $RESP" >&2; exit 1; }

curl -sS -o "$OUT" "$URL"
# gate: arquivo tem que ser audio real, com duracao > 0
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT" 2>/dev/null || echo 0)
python3 -c "import sys;d=float('${DUR:-0}' or 0);sys.exit(0 if d>0.3 else 1)" \
  || { echo "erro: $OUT invalido ou vazio (dur=$DUR)" >&2; exit 1; }
printf '%s  %ss  %s\n' "$OUT" "$DUR" "$(du -h "$OUT" | cut -f1)"
