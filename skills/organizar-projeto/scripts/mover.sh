#!/usr/bin/env bash
# Executa plano de reorganização. Idempotente (pula o que já foi movido), nunca sobrescreve.
# uso: mover.sh <base> <plano.tsv>
#   plano.tsv: origem<TAB>destino<TAB>link(0|1)   caminhos relativos a <base>; linha com # = comentário
#   link=1 deixa symlink relativo no caminho antigo.
# Log: <base>/_arquivo/REORGANIZACAO-<data>.log (ou $LOG)
set -uo pipefail
B="${1:?base}"; PLANO="${2:?plano.tsv}"
LOG="${LOG:-$B/_arquivo/REORGANIZACAO-$(date +%F).log}"
mkdir -p "$(dirname "$LOG")"; echo "== $(date -Iseconds) plano=$PLANO" >> "$LOG"
ok=0; skip=0; err=0
while IFS=$'\t' read -r s d l; do
  [ -z "${s// }" ] && continue; [[ "$s" == \#* ]] && continue
  l="${l:-0}"
  if [ -L "$B/$s" ] && [ -e "$B/$d" ]; then echo "SKIP já movido: $s"; skip=$((skip+1)); continue; fi
  if [ ! -e "$B/$s" ] && [ ! -L "$B/$s" ]; then echo "SKIP não existe: $s"; skip=$((skip+1)); continue; fi
  if [ -e "$B/$d" ]; then echo "ERRO destino existe: $d"; err=$((err+1)); continue; fi
  mkdir -p "$(dirname "$B/$d")"
  if mv -- "$B/$s" "$B/$d"; then
    echo "MV $s -> $d" >> "$LOG"; ok=$((ok+1))
    if [ "$l" = 1 ]; then
      rel=$(realpath -s --relative-to="$(dirname "$B/$s")" "$B/$d")
      ln -s "$rel" "$B/$s" && echo "LN $s -> $rel" >> "$LOG"
    fi
  else echo "ERRO mv $s"; err=$((err+1)); fi
done < "$PLANO"
echo "movidos=$ok pulados=$skip erros=$err  log=$LOG"
find -L "$B" -maxdepth 5 -type l -not -path '*/node_modules/*' -printf 'SYMLINK QUEBRADO %p\n' 2>/dev/null | head
