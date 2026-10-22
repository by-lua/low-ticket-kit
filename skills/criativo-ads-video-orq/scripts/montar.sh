#!/bin/bash
# montar.sh <dir-criativo> <n-cenas> <nome-saida>  — corta cabeca, cauda e pausas internas
set -e
P="$1"; N="$2"; OUT="$3"; T=/tmp/claude-1000
cd "$P/VIDEO"; rm -f s*.mp4 part-*.mp4
k=0
for i in $(seq 1 $N); do
  while read -r a b; do
    k=$((k+1))
    ffmpeg -nostdin -v error -ss "$a" -to "$b" -i cena-$i.mp4 \
      -vf "scale=1080:1920:flags=lanczos,format=yuv420p" \
      -c:v libx264 -crf 18 -preset slow -r 24 -c:a aac -b:a 192k -ar 48000 -ac 2 \
      -y "part-$(printf %03d $k).mp4"
  done < <(python3 $T/tight.py cena-$i.mp4)
done
IN=""; FC=""; j=0
for f in part-*.mp4; do IN="$IN -i $f"; FC="${FC}[${j}:v][${j}:a]"; j=$((j+1)); done
ffmpeg -v error $IN -filter_complex "${FC}concat=n=$j:v=1:a=1[v][a]" -map "[v]" -map "[a]" \
  -c:v libx264 -crf 18 -preset slow -r 24 -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart -y "$P/$OUT"
rm -f part-*.mp4
echo "== $OUT  ($j trechos de $N cenas)"
ffprobe -v error -show_entries stream=width,height,r_frame_rate -show_entries format=duration -of default=nw=1 "$P/$OUT" | head -4
echo "pausas restantes: $(ffmpeg -i "$P/$OUT" -af silencedetect=noise=-28dB:d=0.35 -f null - 2>&1 | grep -c silence_start)"
