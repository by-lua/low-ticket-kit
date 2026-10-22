#!/usr/bin/env bash
# Raio-x de uma pasta antes de organizar. Só lê.
# uso: inventario.sh <pasta-raiz> [profundidade=3]
set -uo pipefail
R="${1:?pasta}"; P="${2:-3}"
cd "$R" || exit 1
X=(-not -path '*/node_modules*' -not -path '*/.git/*' -not -path '*/.overclock-app/*' -not -path '*/.playwright*')

echo "## Raiz: $R"
echo; echo "## Tamanho por item da raiz"
du -sh -- * .[!.]* 2>/dev/null | sort -rh | head -40

echo; echo "## Árvore (profundidade $P, só pastas + .md)"
find . -mindepth 1 -maxdepth "$P" "${X[@]}" \( -type d -o -name '*.md' \) | sort | head -400

echo; echo "## Arquivos soltos que não são .md (raiz e 1º nível)"
find . -mindepth 1 -maxdepth 2 -type f ! -name '*.md' ! -path './.*' ! -path '*/.*' | head -60

echo; echo "## Repos git (remote)"
find . -maxdepth 5 -name .git "${X[@]}" 2>/dev/null | while read -r g; do
  d=$(dirname "$g"); echo "$d  $(git -C "$d" remote get-url origin 2>/dev/null || echo '(sem remote)')  sujo=$(git -C "$d" status --short 2>/dev/null | wc -l)"
done

echo; echo "## Symlinks (e quebrados)"
find . -maxdepth 5 -type l "${X[@]}" -printf '%p -> %l\n' | head -60
find -L . -maxdepth 5 -type l "${X[@]}" -printf 'QUEBRADO %p\n' 2>/dev/null | head

echo; echo "## Scripts com caminho relativo pra fora (../)"
grep -rlE '\.\./' --include='*.sh' --include='*.mjs' --include='*.py' --include='Dockerfile' . 2>/dev/null | grep -v node_modules | head -30

echo; echo "## Quem referencia esta pasta (skills, memórias, docs)"
base=$(basename "$R")
for dir in "$HOME/.claude/skills" "$HOME/.claude/docs" "$HOME/.claude/projects" "$HOME/.overclock-app/claude-accounts"; do
  [ -d "$dir" ] && grep -rlF --include='*.md' --include='*.py' --include='*.sh' "$base/" "$dir" 2>/dev/null | head -40
done

echo; echo "## CLAUDE.md / STATUS.md / AGENTS.md existentes"
find . -maxdepth 4 "${X[@]}" \( -name CLAUDE.md -o -name STATUS.md -o -name AGENTS.md -o -name README.md \) | sort | head -60
