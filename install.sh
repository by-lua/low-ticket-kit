#!/usr/bin/env bash
# Low Ticket Kit — instalador.
#
#   ./install.sh              instala tudo: dependências + skills + plugin + scripts + auto-update
#   ./install.sh --dry-run    só mostra o que faria
#   ./install.sh --no-deps    pula a instalação de dependências do sistema
#   ./install.sh --link-only  só religa skills/scripts (usado pelo update.sh)
#
# Funciona em Linux (apt, pacman, dnf, zypper) e macOS (brew).
# Skill ou script com o mesmo nome que já existe vira <nome>.bak-<data> antes de ser trocado.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KIT_HOME="${LOW_TICKET_KIT_HOME:-$HOME/.local/share/low-ticket-kit}"
REPO_URL="https://github.com/by-lua/low-ticket-kit.git"
CLAUDE_DIR="${CLAUDE_HOME:-$HOME/.claude}"
STAMP=$(date +%Y%m%d-%H%M%S)

DRY=0; DEPS=1; LINK_ONLY=0
for a in "$@"; do
  case "$a" in
    --dry-run) DRY=1 ;;
    --no-deps) DEPS=0 ;;
    --link-only) LINK_ONLY=1; DEPS=0 ;;
  esac
done
run(){ if [ $DRY = 1 ]; then echo "[dry] $*"; else "$@"; fi; }
have(){ command -v "$1" >/dev/null 2>&1; }
say(){ [ $LINK_ONLY = 1 ] || echo "$@"; }

# ── 1. Cópia fixa do repo (é dela que o auto-update puxa) ─────────────────────
if [ "$HERE" != "$KIT_HOME" ]; then
  if [ -d "$KIT_HOME/.git" ]; then
    say "→ atualizando $KIT_HOME"
    run git -C "$KIT_HOME" pull --ff-only -q
  else
    say "→ clonando em $KIT_HOME"
    run mkdir -p "$(dirname "$KIT_HOME")"
    if [ -d "$HERE/.git" ]; then run git clone -q "$HERE" "$KIT_HOME"; run git -C "$KIT_HOME" remote set-url origin "$REPO_URL"
    else run git clone -q "$REPO_URL" "$KIT_HOME"; fi
  fi
  [ $DRY = 1 ] || exec "$KIT_HOME/install.sh" "$@"
fi

# ── 2. Dependências ──────────────────────────────────────────────────────────
install_deps() {
  echo "→ dependências do sistema"
  local SUDO=""; [ "$(id -u)" = 0 ] || SUDO="sudo"
  local pkgs_common="git curl jq ffmpeg python3 imagemagick"
  if have brew; then
    run brew install $pkgs_common node uv yt-dlp || true
    run brew install --cask chromium || true
  elif have apt-get; then
    run $SUDO apt-get update -y
    run $SUDO apt-get install -y $pkgs_common python3-pip python3-venv nodejs npm chromium || \
      run $SUDO apt-get install -y $pkgs_common python3-pip python3-venv nodejs npm chromium-browser || true
  elif have pacman; then
    run $SUDO pacman -S --needed --noconfirm $pkgs_common python-pip nodejs npm chromium || true
  elif have dnf; then
    run $SUDO dnf install -y $pkgs_common python3-pip nodejs npm chromium || true
  elif have zypper; then
    run $SUDO zypper install -y $pkgs_common python3-pip nodejs npm chromium || true
  else
    echo "  ! gerenciador de pacotes não reconhecido: instale à mão: $pkgs_common node npm chromium"
  fi

  # uv (gerenciador Python) — ferramentas Python ficam isoladas, sem sujar o sistema
  if ! have uv; then run sh -c 'curl -LsSf https://astral.sh/uv/install.sh | sh'; export PATH="$HOME/.local/bin:$PATH"; fi

  echo "→ ferramentas Python (uv tool)"
  for t in yt-dlp youtube-transcript-api gflow-cli browser-harness; do
    run uv tool install -q "$t" 2>/dev/null || run uv tool upgrade -q "$t" 2>/dev/null || echo "  ! falhou: $t"
  done
  echo "→ bibliotecas Python (Pillow, imagehash, num2words)"
  run python3 -m pip install --user -q --break-system-packages Pillow imagehash num2words 2>/dev/null || \
    run python3 -m pip install --user -q Pillow imagehash num2words || echo "  ! instale Pillow imagehash num2words à mão"

  echo "→ ferramentas Node (npm -g)"
  if have npm; then
    local NPM_SUDO=""
    [ -w "$(npm prefix -g 2>/dev/null)/lib" ] 2>/dev/null || { [ "$(uname)" = Darwin ] || NPM_SUDO="$SUDO"; }
    run $NPM_SUDO npm i -g -s agent-browser hyperframes @remotion/cli || echo "  ! npm -g falhou"
    have agent-browser && run agent-browser install >/dev/null 2>&1 || true
  else
    echo "  ! npm ausente — instale Node.js 20+ (https://nodejs.org) e rode de novo"
  fi
}

# ── 3. Ligar skills, plugin, scripts ─────────────────────────────────────────
link_one() { # origem destino
  local src="$1" dst="$2"
  if [ -L "$dst" ] && [ "$(readlink "$dst")" = "$src" ]; then return; fi
  if [ -e "$dst" ] || [ -L "$dst" ]; then run mv "$dst" "$dst.bak-$STAMP"; say "  (backup: $dst.bak-$STAMP)"; fi
  run ln -s "$src" "$dst"
}

link_all() {
  say "→ skills em $CLAUDE_DIR/skills"
  run mkdir -p "$CLAUDE_DIR/skills" "$CLAUDE_DIR/bin" "$CLAUDE_DIR/plugins/cache" "$CLAUDE_DIR/browser-workspace/domain-skills"
  for d in "$KIT_HOME"/skills/*/; do link_one "${d%/}" "$CLAUDE_DIR/skills/$(basename "$d")"; done

  say "→ plugin get-brolls"
  for p in "$KIT_HOME"/plugins/*/; do
    pn=$(basename "$p"); run mkdir -p "$CLAUDE_DIR/plugins/cache/$pn"
    for d in "$p"*/; do link_one "${d%/}" "$CLAUDE_DIR/plugins/cache/$pn/$(basename "$d")"; done
  done

  say "→ scripts em $CLAUDE_DIR/bin"
  for f in "$KIT_HOME"/bin/*; do
    n=$(basename "$f")
    case "$n" in *.example) continue ;; esac
    link_one "$f" "$CLAUDE_DIR/bin/$n"
  done
  [ -f "$CLAUDE_DIR/bin/gpt-contas.lst" ] || run cp "$KIT_HOME/bin/gpt-contas.lst.example" "$CLAUDE_DIR/bin/gpt-contas.lst"

  say "→ mapas de site (browser-workspace)"
  [ -e "$CLAUDE_DIR/browser-workspace/agent_helpers.py" ] || run ln -s "$KIT_HOME/browser-workspace/agent_helpers.py" "$CLAUDE_DIR/browser-workspace/agent_helpers.py"
  for d in "$KIT_HOME"/browser-workspace/domain-skills/*/; do
    link_one "${d%/}" "$CLAUDE_DIR/browser-workspace/domain-skills/$(basename "$d")"
  done
}

# ── 4. Auto-update: hook SessionStart do Claude Code ─────────────────────────
add_hook() {
  say "→ auto-update (hook SessionStart em $CLAUDE_DIR/settings.json)"
  [ $DRY = 1 ] && { echo "[dry] adiciona hook: bash $KIT_HOME/update.sh"; return; }
  python3 - "$CLAUDE_DIR/settings.json" "$KIT_HOME/update.sh" <<'PY'
import json, os, sys
path, upd = sys.argv[1], sys.argv[2]
cmd = f"bash {upd} --background"
data = {}
if os.path.exists(path):
    with open(path) as f:
        txt = f.read().strip()
        data = json.loads(txt) if txt else {}
hooks = data.setdefault("hooks", {}).setdefault("SessionStart", [])
if any(cmd == h.get("command") for g in hooks for h in g.get("hooks", [])):
    sys.exit(0)
if os.path.exists(path):
    import shutil; shutil.copy2(path, path + ".bak-lowticketkit")
hooks.append({"hooks": [{"type": "command", "command": cmd}]})
with open(path, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print("  hook adicionado")
PY
}

check_deps() {
  echo "→ conferência"
  for c in git curl jq ffmpeg ffprobe python3 node npm uv yt-dlp agent-browser gflow browser-harness hyperframes; do
    if have "$c"; then echo "  ok    $c"; else echo "  FALTA $c"; fi
  done
  if have chromium || have chromium-browser || [ -d "/Applications/Chromium.app" ]; then echo "  ok    chromium"; else echo "  FALTA chromium"; fi
}

if [ $DEPS = 1 ]; then install_deps; fi
link_all
if [ $LINK_ONLY = 1 ]; then exit 0; fi
add_hook
check_deps

cat <<MSG

Pronto. Versão: $(cat "$KIT_HOME/VERSION" 2>/dev/null || echo "?")
Atualiza sozinho: toda vez que o Claude Code abre (no máximo 1x a cada 6h).
Atualizar na mão: bash $KIT_HOME/update.sh

Falta (uma vez):
  1. Logar as contas nos browsers persistentes (sempre visíveis, nunca headless):
       ~/.claude/bin/browsers.sh add gpt 9222 https://chatgpt.com   && ~/.claude/bin/browsers.sh gpt
       gflow auth login --browser chrome --profile flow-gflow        (Google Flow, vídeo)
     e pôr seus perfis do ChatGPT em ~/.claude/bin/gpt-contas.lst   (linha: <conta> <perfil> <porta>)
  2. Checkout: crie conta no gateway que for usar (Wiven, Mundpay, GGCheckout, Hotmart, Cooud, Zenith).
  3. Sem hospedagem? Leia "Sem hospedagem? Use a Cloudflare" no README.md.
  4. Reinicie o Claude Code e peça: "vamos criar uma oferta low ticket do zero".
MSG
