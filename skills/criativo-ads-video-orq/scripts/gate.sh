#!/bin/bash
# gate.sh <n> — gate BLOQUEANTE por cena, roda antes de montar o criativo.
# 1) o clipe veio da imagem daquela cena  (RMSE frame0 x imagem, teto 0.16)
# 2) o clipe não derivou de cenário/figurino (rosto x mediana das outras cenas)
# 3) sobrou silêncio no fim (fala não estourou os 8s)
set -u
V="$(cd "$(dirname "$0")" && pwd)"; n="$1"; T=$(mktemp -d); falhou=0
for f in "$V/CRIATIVO-$n/VIDEO"/cena-*.mp4; do
  i=$(basename "$f" .mp4 | sed 's/cena-//')
  img="$V/CRIATIVO-$n/IMG/cena-$i.png"
  ffmpeg -nostdin -v error -ss 0.1 -i "$f" -frames:v 1 -vf scale=160:-1 "$T/v.png" -y
  magick "$img" -resize 160x "$T/i.png"
  r=$(magick compare -metric RMSE "$T/v.png" "$T/i.png" null: 2>&1 | grep -oP '\(\K[0-9.]+')
  ok=$(awk -v r="$r" 'BEGIN{print (r<0.16)?"OK":"CLIPE-ERRADO"}')
  [ "$ok" = OK ] || falhou=1
  sil=$(ffmpeg -nostdin -v error -i "$f" -af silencedetect=n=-32dB:d=0.25 -f null - 2>&1 | grep -c silence_start)
  [ "$sil" -gt 0 ] || { echo "   cena $i: SEM RESPIRO (fala estourou o tempo)"; falhou=1; }
  echo "   cena $i: RMSE=$r $ok"
  ffmpeg -nostdin -v error -ss 3 -i "$f" -frames:v 1 -vf "crop=iw*0.6:ih*0.30:iw*0.2:ih*0.06,scale=120:-1" "$T/face$(printf %02d $i).png" -y
done
for a in "$T"/face*.png; do
  ia=$(basename "$a" .png | sed 's/face0*//'); tot=0; cnt=0
  for b in "$T"/face*.png; do [ "$a" = "$b" ] && continue
    r=$(magick compare -metric RMSE "$a" "$b" null: 2>&1 | grep -oP '\(\K[0-9.]+')
    tot=$(awk -v t=$tot -v r=${r:-0} 'BEGIN{print t+r}'); cnt=$((cnt+1)); done
  [ $cnt = 0 ] && continue
  m=$(awk -v t=$tot -v c=$cnt 'BEGIN{printf "%.3f", t/c}')
  awk -v m=$m 'BEGIN{exit !(m>0.20)}' && { echo "   cena $ia: DERIVA DE SET/FIGURINO (dist $m)"; falhou=1; }
done
rm -rf "$T"
[ $falhou = 0 ] && echo "GATE OK CRIATIVO-$n" || { echo "GATE FALHOU CRIATIVO-$n — não monte"; exit 1; }
