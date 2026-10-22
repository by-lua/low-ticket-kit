#!/usr/bin/env bash
set -euo pipefail
# Uso: otimizar-webp.sh origem destino largura [qualidade]
if [ "$#" -lt 3 ] || [ "$#" -gt 4 ]; then echo "Uso: $0 origem destino largura [qualidade]" >&2; exit 64; fi
origem=$1
destino=$2
largura=$3
qualidade=${4:-75}
magick "$origem" -resize "${largura}x" -quality "$qualidade" "$destino"
identify -format '%f %wx%h %b\n' "$destino"
