#!/usr/bin/env bash
# flow.sh — ÚNICA porta de entrada pra gerar no Google Flow (qualquer agente, qualquer skill).
#
#   flow.sh status                   estado de cada perfil (logado? resfriamento? envios? gerando?)
#   flow.sh check                    checagem REAL de login em cada perfil (abre o Flow); marca/desmarca deslogado
#   flow.sh novo-projeto             imprime id de projeto novo (projetos valem pra todos os perfis: mesma conta)
#   flow.sh image t2i --project <id> --out <dir> "<prompt>"
#   flow.sh image i2i --project <id> --ref a.png [--ref b.png ...] --out <dir> "<prompt>"
#   flow.sh video t2v|i2v --project <id> [--initial-frame f.png] --model omni-flash --duration 8 --out-dir <dir> "<prompt>"
#
# Perfis = todo ~/.local/share/gflow-cli/profile_* (hoje flow-gflow e flow-gflow-2, mesma conta
# contato.minhaempresa). Cada envio escolhe sozinho o perfil LOGADO, fora de resfriamento, livre e com
# menos envios recentes (igual gpt-livre.sh). Não passe --profile: o flow.sh escolhe.
# Por perfil: trava (1 envio por vez), ritmo 45-120s, máx 8/30min, resfriamento 45 min se bloquear.
# Perfil que cai na página pública (/about) é marcado deslogado e o envio repete no próximo.
set -uo pipefail
GPY="$HOME/.local/share/uv/tools/gflow-cli/bin/python"
DRIVER="$(dirname "$(readlink -f "$0")")/gflow_ref.py"
STATE="$HOME/.cache/pov-flow"; mkdir -p "$STATE"
export DISPLAY="${DISPLAY:-:1}" GFLOW_CLI_DEBUG_TRACEBACK=1
# perfil ocupado por quem não usa o flow.sh (gflow direto): espera liberar em vez de falhar (exit 11)
export GFLOW_CLI_LEASE_WAIT_SECONDS="${GFLOW_CLI_LEASE_WAIT_SECONDS:-900}"
LOGIN_CMD="gflow auth login --browser chrome --profile"

perfis() { ls -d "$HOME"/.local/share/gflow-cli/profile_* 2>/dev/null | sed 's|.*/profile_||'; }
recent() { touch "$STATE/$1.sends"; awk -v t=$(( $(date +%s) - 1800 )) '$1>t' "$STATE/$1.sends" | wc -l; }
em_cooldown() { [ -f "$STATE/$1.cooldown-until" ] && [ "$(cat "$STATE/$1.cooldown-until")" -gt "$(date +%s)" ]; }
deslogado() { [ -f "$STATE/$1.login-needed" ]; }

probe() { # $1=perfil -> marca/desmarca deslogado
  local r; r=$(FLOW_PROFILE="$1" "$GPY" -I "$DRIVER" probe 2>>"$STATE/probe.log" | tail -1)
  if [ "$r" = ok ]; then rm -f "$STATE/$1.login-needed"; echo "$1: logado"
  else date +%s > "$STATE/$1.login-needed"; echo "$1: DESLOGADO ($r) — a usuária roda: $LOGIN_CMD $1"; fi
}

case "${1:-}" in
  status)
    for p in $(perfis); do
      s="$p: "
      if deslogado "$p"; then s+="DESLOGADO (rode: $LOGIN_CMD $p; depois flow.sh check)"
      elif em_cooldown "$p"; then s+="RESFRIAMENTO até $(date -d @"$(cat "$STATE/$p.cooldown-until")" +%H:%M)"
      else s+="ok"; fi
      s+=" | envios 30min: $(recent "$p")/8"
      pgrep -f -- "--profile $p( |$)" >/dev/null 2>&1 && s+=" | GERANDO agora"
      echo "$s"
    done; exit 0;;
  check) for p in $(perfis); do probe "$p"; done; exit 0;;
esac

# --- escolhe perfil e pega a trava dele ---------------------------------------------------
escolhe() { # imprime perfil escolhido com a trava 9 aberta; espera se todos ocupados
  local cands=() p
  for p in $(perfis); do deslogado "$p" || em_cooldown "$p" || cands+=("$p"); done
  if [ ${#cands[@]} -eq 0 ]; then
    echo "flow.sh: nenhum perfil do Flow disponível:" >&2; "$0" status >&2; return 76
  fi
  # menos envios recentes primeiro
  mapfile -t cands < <(for p in "${cands[@]}"; do echo "$(recent "$p") $p"; done | sort -n | cut -d' ' -f2)
  for p in "${cands[@]}"; do
    exec 9>"$STATE/$p.lock"
    if flock -n 9; then CHOSEN="$p"; return 0; fi
  done
  echo "flow.sh: todos os perfis ocupados; esperando ${cands[0]}..." >&2
  exec 9>"$STATE/${cands[0]}.lock"; flock 9; CHOSEN="${cands[0]}"
}

pace() { # $1=perfil
  local p="$1" now last gap wait n
  now=$(date +%s); n=$(recent "$p")
  if [ "$n" -ge 8 ]; then
    wait=$(( $(awk -v t=$((now-1800)) '$1>t' "$STATE/$p.sends" | head -1) + 1800 - now + 30 ))
    echo "flow.sh: $p fez 8 envios em 30 min — pausa de ${wait}s" >&2; sleep "$wait"; now=$(date +%s)
  fi
  last=$(tail -1 "$STATE/$p.sends" 2>/dev/null); last=${last:-0}
  gap=$((45 + RANDOM % 76)); wait=$((last + gap - now))
  if [ "$wait" -gt 0 ]; then echo "flow.sh: $p ritmo humano, esperando ${wait}s" >&2; sleep "$wait"; fi
  date +%s >> "$STATE/$p.sends"
}

if [ "${1:-}" = novo-projeto ]; then
  escolhe || exit 76
  echo "flow.sh: perfil $CHOSEN" >&2
  FLOW_PROFILE="$CHOSEN" "$GPY" -I "$DRIVER" novo-projeto 2>>"$STATE/novo-projeto.log" | tail -1; exit "${PIPESTATUS[0]}"
fi

[ $# -ge 2 ] || { sed -n '2,20p' "$0"; exit 2; }
LOG=$(mktemp "$STATE/run-XXXX.log")
for tentativa in 1 2 3; do
  escolhe || { rm -f "$LOG"; exit 76; }
  echo "flow.sh: perfil $CHOSEN" >&2
  args=("$1" "$2" --profile "$CHOSEN" "${@:3}")
  pace "$CHOSEN"; "$GPY" -I "$DRIVER" "${args[@]}" >"$LOG" 2>&1; rc=$?
  if [ $rc -eq 23 ]; then
    echo "flow.sh: falha antes do envio (exit 23, sem gasto) — 1 nova tentativa" >&2
    pace "$CHOSEN"; "$GPY" -I "$DRIVER" "${args[@]}" >"$LOG" 2>&1; rc=$?
  fi
  if [ $rc -eq 10 ] || grep -qiE "UNUSUAL_ACTIVITY|atividade incomum|WafRejection" "$LOG"; then
    echo $(( $(date +%s) + 2700 )) > "$STATE/$CHOSEN.cooldown-until"; rc=10
    echo "flow.sh: Flow BLOQUEOU o perfil $CHOSEN (atividade incomum). Resfriamento de 45 min nele. Pare." >&2
    break
  fi
  if grep -qiE "public landing page|flow.google.com/about|not to the Flow app|Confirm it.s you" "$LOG"; then
    date +%s > "$STATE/$CHOSEN.login-needed"; rc=76
    echo "flow.sh: perfil $CHOSEN DESLOGADO (rode: $LOGIN_CMD $CHOSEN). Tentando outro perfil..." >&2
    flock -u 9; continue
  fi
  break
done
cat "$LOG"; rm -f "$LOG"; exit $rc
