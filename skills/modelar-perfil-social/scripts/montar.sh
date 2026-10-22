#!/usr/bin/env bash
# Monta o vídeo final: clipes concatenados + música do original + texto de story no topo.
# uso: montar.sh <saida.mp4> <musica_original.mp4|m4a> <duracao_s> "<linha1>" "<linha2|emoji>" <clip1.mp4> [clip2.mp4 ...]
# Corte do clipe: passe "arquivo.mp4@8.3" pra usar só os primeiros 8.3 s.
set -euo pipefail
OUT=$1; MUS=$2; DUR=$3; L1=$4; L2=$5; shift 5
HERE=$(cd "$(dirname "$0")" && pwd)
TMP=$(mktemp -d)
STORY_Y=${STORY_Y:-70} python3 "$HERE/story_text.py" "$TMP/texto.png" "$L1" "$L2" >/dev/null

inputs=(); filt=""; n=0
for c in "$@"; do
  f=${c%@*}; cut=""; [[ $c == *@* ]] && cut=${c##*@}
  inputs+=(-i "$f")
  if [[ -n $cut ]]; then filt+="[$n:v]trim=0:$cut,setpts=PTS-STARTPTS[c$n];"
  else filt+="[$n:v]setpts=PTS-STARTPTS[c$n];"; fi
  n=$((n+1))
done
for i in $(seq 0 $((n-1))); do filt+="[c$i]"; done
filt+="concat=n=$n:v=1:a=0[v];[v][$n:v]overlay=0:0,trim=0:$DUR,setpts=PTS-STARTPTS,format=yuv420p,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv[vo];"
FADE=$(python3 -c "print(max(0,$DUR-0.8))")
filt+="[$((n+1)):a]atrim=0:$DUR,asetpts=PTS-STARTPTS,afade=t=out:st=$FADE:d=0.8[ao]"

ffmpeg -v error -y "${inputs[@]}" -i "$TMP/texto.png" -stream_loop -1 -i "$MUS" -filter_complex "$filt" \
  -map "[vo]" -map "[ao]" -c:v libx264 -crf 18 -preset medium \
  -x264-params "colorprim=bt709:transfer=bt709:colormatrix=bt709:fullrange=off" \
  -c:a aac -b:a 192k -movflags +faststart "$OUT"
rm -rf "$TMP"
ffprobe -v error -show_entries format=duration:stream=width,height -of csv=p=0 "$OUT" | tr '\n' ' '; echo
