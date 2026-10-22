#!/bin/bash
# montar2.sh <projeto> <saida> [xfade]
# Junta cena-N-1 + cena-N-2 da MESMA pessoa com dissolve (jump cut fica estranho:
# e a mesma pessoa em enquadramento parecido). Entre pessoas, corte seco.
P="$1"; OUT="$2"; XF="${3:-0.35}"; cd "$P" || exit 1
W=/tmp/depo/m2; rm -rf $W; mkdir -p $W
FPS=24
PER=()
for n in 1 2 3 4; do
  a="VIDEO/cena-$n-1.mp4"; b="VIDEO/cena-$n-2.mp4"
  [ -f "$a" ] && [ -f "$b" ] || { echo "FALTA cena $n"; exit 1; }
  da=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$a")
  off=$(awk -v d="$da" -v x="$XF" 'BEGIN{printf "%.3f", d-x}')
  ffmpeg -nostdin -v error -i "$a" -i "$b" -filter_complex \
   "[0:v]scale=1080:1920:flags=lanczos,format=yuv420p,fps=$FPS[v0];
    [1:v]scale=1080:1920:flags=lanczos,format=yuv420p,fps=$FPS[v1];
    [v0][v1]xfade=transition=fade:duration=$XF:offset=$off[v];
    [0:a][1:a]acrossfade=d=$XF:c1=tri:c2=tri[a]" \
   -map "[v]" -map "[a]" -c:v libx264 -crf 18 -preset slow -r $FPS \
   -c:a aac -b:a 192k -ar 48000 -ac 2 -y "$W/p$n.mp4" || exit 1
  PER+=("$W/p$n.mp4")
  echo "pessoa $n: $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$W/p$n.mp4")s"
done
IN=(); FC=""; i=0
for f in "${PER[@]}"; do IN+=(-i "$f"); FC="$FC[$i:v][$i:a]"; i=$((i+1)); done
ffmpeg -nostdin -v error "${IN[@]}" -filter_complex "${FC}concat=n=$i:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 18 -preset slow -r $FPS \
  -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart -y "$OUT" || exit 1
# limites de pessoa, para a legenda nao vazar entre pessoas
d1=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$W/p1.mp4")
awk -v d="$d1" 'BEGIN{printf "CORTES=%.2f,%.2f,%.2f\n", d, 2*d, 3*d}'
echo "montado: $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")s"
