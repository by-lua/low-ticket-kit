#!/bin/bash
# compara o rosto de cada cena com a MEDIANA das outras do mesmo criativo
B="~/Documentos/TRAMPO/PROJETOS/WORKING/PROJETOS - INTERNOS/NUMEROLOGIA/NUMERO-MESTRE/ANUNCIO/22-08-ES"
for c in 48 49 50 51 52 53 54 55 56; do
  D="$B/CRIATIVO-$c/VIDEO"; N=$(ls "$D"/cena-*.mp4 2>/dev/null | wc -l); [ "$N" = 0 ] && continue
  rm -f /tmp/claude-1000/aud*.png
  for f in "$D"/cena-*.mp4; do i=$(basename "$f" .mp4 | sed 's/cena-//')
    ffmpeg -v error -ss 3 -i "$f" -frames:v 1 -vf "crop=iw*0.6:ih*0.30:iw*0.2:ih*0.06,scale=120:-1" /tmp/claude-1000/aud$(printf %02d $i).png -y
  done
  echo "== CRIATIVO-$c"
  for a in /tmp/claude-1000/aud*.png; do
    ia=$(basename "$a" .png | sed 's/aud0*//')
    tot=0; cnt=0
    for b in /tmp/claude-1000/aud*.png; do
      [ "$a" = "$b" ] && continue
      r=$(magick compare -metric RMSE "$a" "$b" null: 2>&1 | grep -oP '\(\K[0-9.]+')
      tot=$(awk -v t=$tot -v r=${r:-0} 'BEGIN{print t+r}'); cnt=$((cnt+1))
    done
    m=$(awk -v t=$tot -v c=$cnt 'BEGIN{printf "%.3f", t/c}')
    flag=""; awk -v m=$m 'BEGIN{exit !(m>0.20)}' && flag="   <-- SUSPEITA"
    echo "   cena $ia: dist media $m$flag"
  done
done
