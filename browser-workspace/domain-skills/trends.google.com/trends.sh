#!/bin/bash
# Le "Interesse ao longo do tempo" (media 5 anos, BR) para ate 3 termos.
# Uso: trends.sh "termo1" "termo2" "termo3"
Q=$(python3 -c "
import urllib.parse,sys
print(','.join(urllib.parse.quote(t) for t in sys.argv[1:]))" "$@")
URL="https://trends.google.com/trends/explore?date=today%205-y&geo=BR&q=$Q&hl=pt-BR"
timeout 120 agent-browser --session trends open "$URL" >/dev/null 2>&1
for i in 1 2 3 4 5 6 7 8; do
  R=$(timeout 40 agent-browser --session trends eval 'var t=document.body.innerText.replace(/\s+/g," ");var i=t.indexOf("Interesse ao longo do tempo");i<0?"":t.slice(i,i+280)' 2>/dev/null | tail -1)
  case "$R" in
    *"Média"*) echo "$R"; exit 0;;
  esac
  sleep 5
done
echo "(sem leitura) $*"
