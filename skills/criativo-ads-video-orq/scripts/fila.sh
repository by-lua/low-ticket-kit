#!/bin/bash
# retoma sozinha: pula cena que ja tem clipe em VIDEO/
P="~/Documentos/TRAMPO/PROJETOS/WORKING/PROJETOS - INTERNOS/NUMEROLOGIA/NUMERO-MESTRE/ANUNCIO/22-08-ES"
for n in 52 53 54 55 56; do
  echo "############ CRIATIVO-$n"
  for i in $(seq 1 6); do
    if [ -f "$P/CRIATIVO-$n/VIDEO/cena-$i.mp4" ]; then echo "  cena $i ja existe, pulando"; continue; fi
    echo "======== CRIATIVO-$n cena $i"
    if /tmp/claude-1000/gen.sh "$P/CRIATIVO-$n/IMG/cena-$i.png" "$P/CRIATIVO-$n/PROMPTS/vid-cena-$i-short.txt" "$n-$i" 2>&1 | tail -5; then
      mv "$HOME/Downloads/numes-$n-$i.mp4" "$P/CRIATIVO-$n/VIDEO/cena-$i.mp4" 2>/dev/null
    fi
    sleep 8
  done
  ok=$(ls "$P/CRIATIVO-$n/VIDEO"/cena-*.mp4 2>/dev/null | wc -l)
  echo "### CRIATIVO-$n: $ok/6"
  [ "$ok" -lt 6 ] && { echo "### PAROU no $n"; exit 1; }
done
echo "### LEVA COMPLETA"
