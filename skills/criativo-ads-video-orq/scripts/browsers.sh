#!/usr/bin/env bash
# Browsers persistentes, sempre logados, um por conta.
#
# Chromium do SISTEMA (não o empacotado do agent-browser, que trava no Cloudflare),
# com perfil persistente em ~/.agent-profiles/<nome> e porta CDP fixa por perfil.
# O login sobrevive entre execuções e reboots — logue uma vez, use sempre.
#
#   browsers.sh status         mostra o que está de pé e se está logado (TAMBÉM é o padrão sem argumento)
#   browsers.sh gpt hub        sobe só esses
#   browsers.sh all            sobe TODOS os perfis registrados (explícito — nunca por acidente)
#   browsers.sh add <nome> <porta> <url>    registra um perfil novo
#
# Sem argumento NÃO sobe nada: mostra o status. Antes, "browsers.sh" puro caía em
# "all" e abria todos os perfis de uma vez — foi o que já causou sustos repetidos.
#
# Depois: agent-browser --session <nome> <comando>

set -uo pipefail

CHROMIUM="${CHROMIUM_BIN:-/usr/bin/chromium}"
REGISTRY="$HOME/.agent-profiles/registry.conf"

mkdir -p "$HOME/.agent-profiles"

# nome porta url — porta fixa por perfil, nunca reutilize
if [ ! -f "$REGISTRY" ]; then
  cat > "$REGISTRY" <<'EOF'
gpt  9222 https://chatgpt.com
hub  9223 https://ninjabrhub.io/studio
ggcheckoutpnzdona 9224 https://ggcheckout.app
EOF
fi

launch() {
  local name="$1" port="$2" url="$3"
  local profile="$HOME/.agent-profiles/$name"

  if curl -sf -m 3 "http://127.0.0.1:$port/json/version" >/dev/null 2>&1; then
    echo "• $name já rodando (porta $port)"
  else
    mkdir -p "$profile"
    # extensões descompactadas por perfil (~/.agent-profiles/extensions.conf)
    local ext_args=()
    local ext
    ext=$(awk -v n="$name" '$1==n {print $2}' "$HOME/.agent-profiles/extensions.conf" 2>/dev/null)
    if [ -n "$ext" ]; then
      ext_args=(--load-extension="$ext" --disable-features=DisableLoadExtensionCommandLineSwitch)
      echo "  + extensão: $ext"
    fi
    # Sobe como servico proprio do systemd (unit browser-<perfil>), fora da arvore de
    # processos de quem chamou. Antes era `nohup ... &`: fechar o pane do Overclock que
    # rodou este script matava o Chromium junto (21/10/2026) e a automacao seguia sem ele.
    local unit="browser-${name//[^A-Za-z0-9_.-]/_}"
    systemctl --user reset-failed "$unit" >/dev/null 2>&1
    systemctl --user stop "$unit" >/dev/null 2>&1
    systemd-run --user --quiet --collect --unit="$unit" \
      -p StandardOutput="truncate:/tmp/chromium-$name.log" -p StandardError=inherit \
      "$CHROMIUM" \
      --remote-debugging-port="$port" \
      --user-data-dir="$profile" \
      --disk-cache-size=104857600 \
      --no-first-run --no-default-browser-check \
      "${ext_args[@]}" \
      "$url" >/dev/null 2>&1 \
    || nohup setsid "$CHROMIUM" \
      --remote-debugging-port="$port" \
      --user-data-dir="$profile" \
      --disk-cache-size=104857600 \
      --no-first-run --no-default-browser-check \
      "${ext_args[@]}" \
      "$url" > "/tmp/chromium-$name.log" 2>&1 &
    for _ in $(seq 1 20); do
      curl -sf -m 3 "http://127.0.0.1:$port/json/version" >/dev/null 2>&1 && break
      sleep 0.5
    done
    if curl -sf -m 3 "http://127.0.0.1:$port/json/version" >/dev/null 2>&1; then
      echo "✓ $name subiu (porta $port)"
    else
      echo "✗ $name não subiu — veja /tmp/chromium-$name.log"
      return 1
    fi
  fi

  agent-browser --session "$name" connect "$port" >/dev/null 2>&1 \
    && echo "  conectado: agent-browser --session $name ..." \
    || echo "  ! agent-browser não conectou na sessão $name"
}

status() {
  printf "%-6s %-6s %-9s %s\n" PERFIL PORTA ESTADO URL
  while read -r name port url; do
    [ -z "${name:-}" ] && continue
    case "$name" in \#*) continue;; esac
    if curl -sf -m 3 "http://127.0.0.1:$port/json/version" >/dev/null 2>&1; then
      current=$(curl -s "http://127.0.0.1:$port/json" | grep -oE '"url": "https?://[^"]*"' | head -1 | cut -d'"' -f4)
      printf "%-6s %-6s %-9s %s\n" "$name" "$port" "ATIVA" "${current:-?}"
    else
      printf "%-6s %-6s %-9s %s\n" "$name" "$port" "parada" "$url"
    fi
  done < "$REGISTRY"

  echo
  echo "Credenciais: ~/.claude/.credentials.env  (set -a; source ~/.claude/.credentials.env; set +a)"
  echo "Cloudflare:  o checkbox pode ser clicado, valida normalmente nesses perfis."

  local stray
  stray=$(pgrep -af "agent-browser-chrome" 2>/dev/null | wc -l)
  [ "$stray" -gt 0 ] && echo && echo "! $stray processo(s) do Chromium EMPACOTADO rodando com perfil em /tmp." && echo "  Esses não guardam login e travam no Cloudflare. Feche com: agent-browser close --all"
  return 0
}

# Sem argumento = só leitura (status). NÃO sobe nada — evita abrir todos os perfis
# sem querer (era o comportamento antigo, que caía em "all").
if [ $# -eq 0 ]; then
  echo "uso: browsers.sh <perfil...> | all | status | add <nome> <porta> <url>"
  echo "  (sem argumento só mostra o status — não sobe nenhum perfil)"
  echo
  status
  exit 0
fi

case "$1" in
  status) status ;;
  add)
    [ $# -eq 4 ] || { echo "uso: browsers.sh add <nome> <porta> <url>"; exit 1; }
    echo "$2 $3 $4" >> "$REGISTRY"; echo "✓ perfil '$2' registrado na porta $3"
    ;;
  all)
    while read -r name port url; do
      [ -z "${name:-}" ] && continue
      case "$name" in \#*) continue;; esac
      launch "$name" "$port" "$url"
    done < "$REGISTRY"
    ;;
  *)
    for want in "$@"; do
      line=$(grep -E "^$want[[:space:]]" "$REGISTRY" | head -1)
      [ -z "$line" ] && { echo "perfil '$want' não registrado — use: browsers.sh add $want <porta> <url>"; continue; }
      launch $line
    done
    ;;
esac
