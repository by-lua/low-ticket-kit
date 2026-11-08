#!/usr/bin/env bash
# uso: animar-imagem.sh <base.png|jpg> <saida.mp4> [props.json]
# Formato "imagem animada" 4:5 (1080x1350, 7,2 s, sem som): zoom lento + selo de preço pulsando + seta pulando
# + botão CTA pulsando com mãozinha (layout 'pill') ou anel pulsando em volta do botão que JÁ está na arte (layout 'ring').
# props.json (todos opcionais): {"price":"Desde $7.900","cta":"RECIBIR AHORA","band":"Recibí el Mapa del Tarot",
#   "arrow":true,"arrowX":720,"arrowY":1000,"sec":7.2,"badgePos":"bl|tr","layout":"pill|ring","ring":{"left":178,"top":1204,"width":660,"height":127}}
set -euo pipefail
BASE=$(realpath "$1"); OUT=$(realpath -m "$2"); PROPS=${3:-}
AQUI="$(cd "$(dirname "$0")" && pwd)"; RB="$HOME/Developer/remotion-base/node_modules"
[ -d "$RB" ] || { echo "FAIL falta $RB (base do Remotion)"; exit 1; }
W=$(ffprobe -v error -show_entries stream=width,height -of csv=p=0 "$BASE"); [ "$W" = "1080,1350" ] || { echo "FAIL base deve ser 1080x1350 (4:5), veio $W"; exit 1; }
T=$(mktemp -d); mkdir -p "$T/src" "$T/public"; cp "$AQUI/src/index.jsx" "$T/src/"; ln -s "$RB" "$T/node_modules"
cp "$BASE" "$T/public/base.png"; echo '{"name":"anim","private":true}' > "$T/package.json"
ARGS=(); [ -n "$PROPS" ] && ARGS+=(--props="$(realpath "$PROPS")")
( cd "$T" && node_modules/.bin/remotion render src/index.jsx Anim "$OUT" --codec=h264 --crf=21 --concurrency=6 "${ARGS[@]}" >/dev/null 2>&1 ) || { echo "FAIL render"; exit 1; }
rm -rf "$T"
echo "OK $OUT $(ffprobe -v error -show_entries stream=width,height -show_entries format=duration -of default=nw=1:nk=1 "$OUT" | tr "\n" " ")"
