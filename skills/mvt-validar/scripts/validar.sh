#!/bin/bash
# uso: validar.sh <sessao> <queries.txt> <saida.jsonl>
SESSAO=$1
QFILE=$2
OUT=$3
> "$OUT"
while IFS='|' read -r id query; do
  [ -z "$query" ] && continue
  enc=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$query")
  agent-browser --session "$SESSAO" open "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=BR&q=${enc}&search_type=keyword_unordered&media_type=all" > /dev/null 2>&1
  sleep 7
  res=$(agent-browser --session "$SESSAO" eval "(function(){var m=document.body.innerText.match(/~?[\d.,]+\s*(resultados|results)/i); return m?m[0]:'0';})()" 2>/dev/null | tail -1)
  echo "{\"id\":\"$id\",\"query\":\"$query\",\"resultado\":$res}" >> "$OUT"
done < "$QFILE"
