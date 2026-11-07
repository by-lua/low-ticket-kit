#!/usr/bin/env bash
# flow.sh — ÚNICA porta de entrada pra gerar no Google Flow (qualquer agente, qualquer skill).
#
#   flow.sh status                   estado de cada perfil (logado? resfriamento? envios? gerando?)
#   flow.sh check                    checagem REAL de login em cada perfil (abre o Flow); marca/desmarca deslogado
#   flow.sh novo-projeto             imprime id de projeto novo (projetos valem pra todos os perfis: mesma conta)
#   flow.sh image t2i --project <id> --out <dir> "<prompt>"
#   flow.sh image i2i --project <id> --ref a.png [--ref b.png ...] --out <dir> "<prompt>"
#   flow.sh video t2v|i2v --project <id> [--initial-frame f.png] --model omni-flash --duration 8 --out-dir <dir> "<prompt>"
#   flow.sh bloqueio [min]           registra "atividade incomum" vista NA TELA (45 min por padrão) em TODOS os perfis
#
# Perfis = todo ~/.local/share/gflow-cli/profile_* (hoje flow-gflow e flow-gflow-2, mesma conta
# contato.minhaempresa). Cada envio escolhe sozinho o perfil LOGADO, fora de resfriamento, livre e com
# menos envios recentes (igual gpt-livre.sh). Não passe --profile: o flow.sh escolhe.
# Ritmo e teto são da CONTA (todos os perfis somados): 45-120s entre envios e máx 8/30min — a conta é
# a mesma, então somar é o que o Google vê. Trava de 1 envio por vez é por perfil.
# Frame já enviado (--initial-frame) nunca sai 2x no mesmo projeto: o flow.sh recusa (exit 77).
# Resfriamento 45 min se bloquear (exit 10, log, ou "atividade incomum" na tela via `flow.sh bloqueio`).
# Perfil que cai na página pública (/about) é marcado deslogado e o envio repete no próximo.
set -uo pipefail
GPY="$HOME/.local/share/uv/tools/gflow-cli/bin/python"
DRIVER="$(dirname "$(readlink -f "$0")")/gflow_ref.py"
STATE="$HOME/.cache/pov-flow"; mkdir -p "$STATE"
export DISPLAY="${DISPLAY:-:1}" GFLOW_CLI_DEBUG_TRACEBACK=1
# perfil ocupado por quem não usa o flow.sh (gflow direto): espera liberar em vez de falhar (exit 11)
# gflow FIXO na 0.87.0 (06/11/2026): Patchright quebra o composer agent-only da nossa conta (botão 'tune'
# some, exit 23) e a 0.93 recusa imagem com referência (exit 36). Não ligar Patchright nem atualizar sem testar.
export GFLOW_CLI_BROWSER_ENGINE=playwright GFLOW_CLI_UPDATE_CHECK=0
export GFLOW_CLI_LEASE_WAIT_SECONDS="${GFLOW_CLI_LEASE_WAIT_SECONDS:-900}"
LOGIN_CMD="gflow auth login --browser chrome --profile"

perfis() { ls -d "$HOME"/.local/share/gflow-cli/profile_* 2>/dev/null | sed 's|.*/profile_||'; }
recent() { touch "$STATE/$1.sends"; awk -v t=$(( $(date +%s) - 1800 )) '$1>t' "$STATE/$1.sends" | wc -l; }
# a conta é UMA só (todos os perfis são o mesmo login): ritmo/teto somam os perfis
conta_recent() { local p t=0 x; for p in $(perfis); do x=$(awk -v t=$(( $(date +%s) - 1800 )) '$1>t' "$STATE/$p.sends" 2>/dev/null | wc -l); t=$((t+x)); done; echo "$t"; }
conta_last() { local p v m=0; for p in $(perfis); do v=$(tail -1 "$STATE/$p.sends" 2>/dev/null); v=${v:-0}; if [ "$v" -gt "$m" ]; then m=$v; fi; done; echo "$m"; }
conta_oldest() { local p v m=0; for p in $(perfis); do v=$(awk -v t=$(( $(date +%s) - 1800 )) '$1>t' "$STATE/$p.sends" 2>/dev/null | head -1); if [ -n "$v" ]; then if [ "$m" -eq 0 ] || [ "$v" -lt "$m" ]; then m=$v; fi; fi; done; echo "${m:-0}"; }
em_cooldown() { [ -f "$STATE/$1.cooldown-until" ] && [ "$(cat "$STATE/$1.cooldown-until")" -gt "$(date +%s)" ]; }
deslogado() { [ -f "$STATE/$1.login-needed" ]; }
# fingerprint do frame inicial + projeto: o MESMO frame nunca vai 2x (reenvio = crédito 2x + "atividade incomum")
fp_de_frame() { local a prev="" f="" proj="" i; for a in "$@"; do
    if [ "$prev" = "--initial-frame" ]; then f="$a"; fi
    if [ "$prev" = "--project" ]; then proj="$a"; fi
    prev="$a"; done
  if [ -n "$f" ] && [ -f "$f" ]; then echo "$proj $(sha1sum "$f" | cut -d' ' -f1)"; fi; }

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
    done
    echo "conta (todos os perfis somados): $(conta_recent)/8 envios em 30 min | último envio $(date -d @"$(conta_last)" +%H:%M:%S)"
    exit 0;;
  check) for p in $(perfis); do probe "$p"; done; exit 0;;
  bloqueio) # "atividade incomum" apareceu NA TELA (o processo morreu e não viu o exit 10)
    mins="${2:-45}"
    for p in $(perfis); do echo $(( $(date +%s) + mins * 60 )) > "$STATE/$p.cooldown-until"; done
    echo "flow.sh: bloqueio registrado — TODOS os perfis em resfriamento por ${mins} min (volta $(date -d @$(( $(date +%s) + mins * 60 )) +%H:%M))."
    exit 0;;
esac

# --- escolhe perfil e pega a trava dele ---------------------------------------------------
escolhe() { # imprime perfil escolhido com a trava 9 aberta; espera se todos ocupados
  local cands=() p
  if [ -f "$STATE/bloqueio-ate" ] && [ "$(cat "$STATE/bloqueio-ate")" -gt "$(date +%s)" ]; then
    echo "flow.sh: PAUSADO até $(date -d @"$(cat "$STATE/bloqueio-ate")" +%H:%M) — o envio anterior saiu sem aprovar o take; recupere/resolva antes de enviar de novo." >&2
    return 78
  fi
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

pace() { # $1=perfil — ritmo e teto são da CONTA (todos os perfis são o mesmo login)
  local p="$1" now last gap wait n oldest
  now=$(date +%s); n=$(conta_recent)
  if [ "$n" -ge 8 ]; then
    oldest=$(conta_oldest)
    wait=$(( oldest + 1800 - now + 30 ))
    echo "flow.sh: conta fez 8 envios em 30 min (todos os perfis) — pausa de ${wait}s" >&2; sleep "$wait"; now=$(date +%s)
  fi
  last=$(conta_last)
  gap=$((45 + RANDOM % 76)); wait=$((last + gap - now))
  if [ "$wait" -gt 0 ]; then echo "flow.sh: ritmo humano da conta, esperando ${wait}s" >&2; sleep "$wait"; fi
  date +%s >> "$STATE/$p.sends"
}

if [ "${1:-}" = novo-projeto ]; then
  escolhe || exit 76
  echo "flow.sh: perfil $CHOSEN" >&2
  FLOW_PROFILE="$CHOSEN" "$GPY" -I "$DRIVER" novo-projeto 2>>"$STATE/novo-projeto.log" | tail -1; exit "${PIPESTATUS[0]}"
fi

[ $# -ge 2 ] || { sed -n '2,20p' "$0"; exit 2; }
FRAMES="$STATE/enviados.frames"; touch "$FRAMES"
FP=$(fp_de_frame "$@")
if [ -n "$FP" ] && grep -qxF "$FP" "$FRAMES"; then
  if [ "${FLOW_FRAME_RETRY:-0}" = "1" ]; then
    echo "flow.sh: AVISO — reenvio do MESMO frame autorizado por FLOW_FRAME_RETRY=1. Só vale se você conferiu no projeto que o clipe desse frame NÃO existe." >&2
  else
    echo "flow.sh: RECUSADO — esse frame já foi enviado neste projeto. Não reenvie: o take pode estar no projeto." >&2
    echo "  recupere com: flow_listar_projeto.py <perfil> <project_id> (seção da skill: 'Aprovar no take / exit 25')." >&2
    echo "  se o projeto NÃO tem o clipe desse frame, repita com FLOW_FRAME_RETRY=1 na frente." >&2
    exit 77
  fi
fi
LOG=$(mktemp "$STATE/run-XXXX.log")
for tentativa in 1 2 3; do
  escolhe || { rm -f "$LOG"; exit 76; }
  echo "flow.sh: perfil $CHOSEN" >&2
  args=("$1" "$2" --profile "$CHOSEN" "${@:3}")
  pace "$CHOSEN"; [ -n "$FP" ] && echo "$FP" >> "$FRAMES"
  "$GPY" -I "$DRIVER" "${args[@]}" >"$LOG" 2>&1; rc=$?
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
if [ $rc -ne 0 ] && grep -q "migrated.agent_only.submitted" "$LOG" && ! grep -qE "gate_approved|video_ready" "$LOG"; then
  echo "flow.sh: o envio SAIU mas o take não foi aprovado/baixado (gate pendente — foi isso que gerou crédito 2x em 04/11)." >&2
  echo "  NÃO reenvie. Rode: flow_listar_projeto.py <perfil> <project_id> e baixe o clipe; se o 'Aprovar' estiver na tela, a usuária clica UMA vez." >&2
  depth=$(( $(cat "$STATE/bloqueio-ate" 2>/dev/null || echo 0) ))
  [ "$depth" -lt $(( $(date +%s) + 600 )) ] && echo $(( $(date +%s) + 600 )) > "$STATE/bloqueio-ate"
fi
cat "$LOG"; rm -f "$LOG"; exit $rc
