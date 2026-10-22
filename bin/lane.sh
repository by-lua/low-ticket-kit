#!/usr/bin/env bash
# Lanes — vários Claudes no MESMO browser logado, cada um na sua aba e no seu chat.
#
# Um perfil de browser por conta (gpt/hub/gg) continua sendo UM só: o login é
# desse perfil e clonar perfil quebra sessão. O isolamento é por LANE:
#   sessão agent-browser  = <perfil>-<lane>     (ponteiro de aba próprio, persistente)
#   aba do Chromium       = label <lane>        (id estável, nunca reusado)
#
# Duas sessões apontando para o mesmo perfil NÃO brigam desde que cada uma fixe
# sua aba por label. Sem fixar, todo comando cai na última aba criada — foi assim
# que dois Claudes acabavam escrevendo no mesmo chat.
#
#   lane.sh take gpt cozinha [url]   pega/cria a lane, imprime a sessão a usar
#   lane.sh list                     todas as lanes ativas, com URL
#   lane.sh drop gpt cozinha         fecha a aba e apaga o estado da sessão
#   lane.sh dir cozinha              pasta de staging da lane (cria se faltar)
#   LANE_AREA=HUB lane.sh dir cozinha    staging noutra área (ver ÁREA abaixo)
#   lane.sh collect cozinha <dest>   move os downloads da lane p/ o projeto
#
# Downloads: TUDO cai primeiro na pasta de staging da lane e só depois vai pro
# projeto. Nomeie sempre o arquivo com o prefixo da lane no `a.download`
# (ex.: `cozinha-cena-1.mp4`), senão duas lanes se sobrescrevem em ~/Downloads.
#
# ÁREA: a pasta de staging é ~/Downloads/<AREA>/<lane>/, e a área separa
# ferramentas que não têm nada a ver uma com a outra:
#
#   PLAYWRIGHT  (padrão)  geração por browser: ChatGPT, bancos de imagem
#   HUB                   NinjaBR Hub: vídeo, criativo, transcrição
#
# Trocar com LANE_AREA=HUB, ou exportar uma vez no início do fluxo.

set -uo pipefail

AREA="${LANE_AREA:-PLAYWRIGHT}"
STAGING="$HOME/Downloads/$AREA"
REGISTRY="$HOME/.agent-profiles/registry.conf"
LANES="$HOME/.agent-profiles/lanes.conf"
touch "$LANES" 2>/dev/null

usage() { sed -n '2,26p' "$0" | sed 's/^# \?//'; }

profile_url() {
  awk -v n="$1" '$1==n {print $3; exit}' "$REGISTRY"
}

take() {
  local prof="$1" lane="$2" url="${3:-}"
  local sess="$prof-$lane"

  [ -n "$(profile_url "$prof")" ] || { echo "perfil '$prof' não registrado em $REGISTRY" >&2; return 1; }
  [ -z "$url" ] && url="$(profile_url "$prof")"

  "$HOME/.claude/bin/browsers.sh" "$prof" >/dev/null || return 1
  local port; port=$(awk -v n="$prof" '$1==n {print $2; exit}' "$REGISTRY")
  agent-browser --session "$sess" connect "$port" >/dev/null 2>&1 \
    || { echo "não conectou na porta $port" >&2; return 1; }

  # a aba já existe? (labels e ids t<N> são namespace PRÓPRIO de cada sessão)
  if ! agent-browser --session "$sess" tab "$lane" >/dev/null 2>&1; then
    agent-browser --session "$sess" tab new --label "$lane" >/dev/null 2>&1
  fi
  # FIXAR sempre: sem isto o ponteiro da sessão salta para a aba criada por outra lane
  agent-browser --session "$sess" tab "$lane" >/dev/null 2>&1

  # tab new às vezes abre em about:blank e ignora a url — navegue explicitamente
  case "$(agent-browser --session "$sess" get url 2>/dev/null)" in
    about:blank|"") agent-browser --session "$sess" navigate "$url" >/dev/null 2>&1 \
                     || agent-browser --session "$sess" open "$url" >/dev/null 2>&1 ;;
  esac

  grep -q "^$prof $lane\$" "$LANES" 2>/dev/null || echo "$prof $lane" >> "$LANES"

  mkdir -p "$STAGING/$lane"
  echo "sessão:  $sess"
  echo "aba:     $lane   $(agent-browser --session "$sess" get url 2>/dev/null)"
  echo "staging: $STAGING/$lane"
  echo
  echo "use SEMPRE: agent-browser --session $sess <comando>"
}

list() {
  [ -s "$LANES" ] || { echo "(nenhuma lane ativa)"; return 0; }
  printf "%-20s %-12s %s\n" SESSÃO LANE URL
  while read -r prof lane; do
    [ -z "${prof:-}" ] && continue
    local sess="$prof-$lane"
    agent-browser --session "$sess" tab "$lane" >/dev/null 2>&1
    printf "%-20s %-12s %s\n" "$sess" "$lane" \
      "$(agent-browser --session "$sess" get url 2>/dev/null || echo '- (aba fechada)')"
  done < "$LANES"
  return 0
}

drop() {
  local sess="$1-$2"
  agent-browser --session "$sess" tab "$2" >/dev/null 2>&1 \
    && agent-browser --session "$sess" tab close "$2" >/dev/null 2>&1
  if [ -f "$LANES" ]; then
    grep -v "^$1 $2\$" "$LANES" > "$LANES.tmp" 2>/dev/null; mv "$LANES.tmp" "$LANES"
  fi
  echo "✓ lane $2 do perfil $1 liberada"
}

collect() {
  local lane="$1" dest="${2:-}"
  mkdir -p "$STAGING/$lane"
  local n=0
  for f in "$HOME/Downloads/$lane-"*; do
    [ -e "$f" ] || continue
    mv "$f" "$STAGING/$lane/" && n=$((n+1))
  done
  echo "$n arquivo(s) recolhidos em $STAGING/$lane"
  if [ -n "$dest" ]; then
    mkdir -p "$dest"
    mv "$STAGING/$lane/"* "$dest"/ 2>/dev/null && echo "→ movidos para $dest"
  fi
  return 0
}

case "${1:-help}" in
  take)    shift; [ $# -ge 2 ] || { usage; exit 1; }; take "$@" ;;
  list)    list ;;
  drop)    shift; [ $# -eq 2 ] || { usage; exit 1; }; drop "$@" ;;
  dir)     shift; mkdir -p "$STAGING/$1"; echo "$STAGING/$1" ;;
  collect) shift; [ $# -ge 1 ] || { usage; exit 1; }; collect "$@" ;;
  *)       usage ;;
esac
