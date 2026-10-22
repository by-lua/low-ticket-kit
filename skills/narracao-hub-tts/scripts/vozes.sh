#!/usr/bin/env bash
# lista vozes do NinjaVoice. uso: vozes.sh [male|female] [--online]
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
SRC="$DIR/voices.json"
for a in "$@"; do
  [ "$a" = "--online" ] && curl -sS https://captions.ninjabrhub.online/api/captions/voices > "$SRC"
done
G="${1:-}"; [ "$G" = "--online" ] && G=""
G="$G" SRC="$SRC" python3 <<'PY'
import json, os
v = json.load(open(os.environ["SRC"]))
g = os.environ.get("G", "")
for x in v:
    if g and x.get("gender") != g:
        continue
    print("%s  %-14s%-8s%-12s%s" % (x["id"], x["name"], x.get("gender", "?"),
                                    x.get("accent", ""), x.get("provider", "")))
PY
