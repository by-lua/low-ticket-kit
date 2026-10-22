#!/usr/bin/env bash
# Atualiza o Low Ticket Kit: git pull + religa skills novas.
#   bash update.sh                 atualiza agora, mostrando o que mudou
#   bash update.sh --background    usado pelo hook do Claude Code: no máximo 1x a cada 6h, silencioso
set -uo pipefail
KIT_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STAMP_FILE="$KIT_HOME/.last-update"
INTERVAL=$((6*3600))

do_update() {
  local before after
  before=$(git -C "$KIT_HOME" rev-parse HEAD 2>/dev/null)
  git -C "$KIT_HOME" fetch -q origin 2>/dev/null || return 0
  git -C "$KIT_HOME" reset -q --hard origin/main 2>/dev/null || return 0
  after=$(git -C "$KIT_HOME" rev-parse HEAD)
  date +%s > "$STAMP_FILE"
  if [ "$before" != "$after" ]; then
    bash "$KIT_HOME/install.sh" --link-only
    echo "Low Ticket Kit atualizado: $(cat "$KIT_HOME/VERSION" 2>/dev/null)"
    git -C "$KIT_HOME" log --oneline "$before..$after" 2>/dev/null | head -10
  else
    [ "${1:-}" = quiet ] || echo "Low Ticket Kit já está na última versão ($(cat "$KIT_HOME/VERSION" 2>/dev/null))."
  fi
}

if [ "${1:-}" = "--background" ]; then
  last=$(cat "$STAMP_FILE" 2>/dev/null || echo 0)
  [ $(( $(date +%s) - last )) -lt $INTERVAL ] && exit 0
  ( do_update quiet >/dev/null 2>&1 & ) ; exit 0
fi
do_update
