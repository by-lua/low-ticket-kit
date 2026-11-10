#!/bin/bash
# uso: recortar-fundo.sh <entrada.png 1254x1254> <saida.png> — fundo branco liso (inclusive bolsões entre louros/fita) -> alpha real, sem PIL.
# Branco fora do disco central vira transparente; dentro do disco (letras creme) é protegido.
in=$(realpath "$1"); out=$(realpath -m "$2"); T=$(mktemp -d)
magick "$in" -fuzz 7% -fill black -opaque white -fill white +opaque black -colorspace Gray "$T/w.png" 2>/dev/null
# w.png: branco onde era branco-ish? reconstruir mais simples abaixo
magick "$in" -fuzz 8% -transparent white -alpha extract -threshold 50% "$T/a.png"          # 0 = branco-ish, 255 = resto
magick -size 1254x1254 xc:black -fill white -draw "circle 627,560 627,905" "$T/disc.png"   # disco protegido
magick "$T/a.png" "$T/disc.png" -compose Lighten -composite "$T/keep.png"
magick "$T/keep.png" -morphology Erode Disk:1 -blur 0x0.8 "$T/keep2.png"
magick "$in" -alpha set "$T/keep2.png" -compose CopyOpacity -composite -trim +repage "$out"
rm -rf "$T"; echo "$out $(magick identify -format '%wx%h' "$out") canto-alpha=$(magick "$out" -format '%[fx:p{0,0}.a]' info:)"
