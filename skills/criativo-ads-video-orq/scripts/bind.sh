#!/bin/bash
# bind.sh — liga cada imagem aprovada à cena certa e PROVA o vínculo.
# Roda depois que _IMG/numes-<n>-<KEY>.png estiverem aprovadas no gate visual.
# Sem isto, cena de ação recebe imagem de repouso — foi o erro da leva 22-08.
set -u
V="$(cd "$(dirname "$0")" && pwd)"
falhou=0
while read -r n cena key; do
  src="$V/_IMG/numes-$n-$key.png"
  dst="$V/CRIATIVO-$n/IMG/cena-$cena.png"
  if [ ! -f "$src" ]; then echo "FALTA imagem $src"; falhou=1; continue; fi
  cp -f "$src" "$dst"
done < <(python3 - "$V" <<'PY'
import re,sys,glob,os
V=sys.argv[1]
for f in sorted(glob.glob(f"{V}/CRIATIVO-*/PROMPTS/vid-cena-*.txt")):
    n=re.search(r'CRIATIVO-(\d+)',f).group(1); i=re.search(r'cena-(\d+)',f).group(1)
    m=re.search(rf'\| {i} \|.*`([A-Z])` ',open(f"{V}/PLANO-LEVA-V2.md").read().split(f"## CRIATIVO-{n}")[1].split("## CRIATIVO-")[0])
    print(n,i,m.group(1))
PY
)
# prova: toda cena aponta para uma imagem aprovada do PRÓPRIO criativo
for d in "$V"/CRIATIVO-*; do n=$(basename "$d" | tr -dc 0-9)
  for f in "$d"/IMG/cena-*.png; do
    [ -f "$f" ] || { echo "FALTA $f"; falhou=1; continue; }
    h=$(md5sum "$f" | cut -d' ' -f1)
    md5sum "$V"/_IMG/numes-$n-*.png 2>/dev/null | grep -q "^$h" || { echo "IMGFAIL $f não bate com nenhuma imagem aprovada de CRIATIVO-$n"; falhou=1; }
  done
done
[ $falhou = 0 ] && echo "BIND OK" || { echo "BIND FALHOU"; exit 1; }
