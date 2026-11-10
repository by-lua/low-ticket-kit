#!/bin/bash
# uso: GPT_S=gpt-empresab-selo GPT_TAB=selo ./gerar-banco.sh  (roda dentro desta pasta)
cd "$(dirname "$(realpath "$0")")"
for id in es-15 en-15 fr-15 pt-7; do
  [ -f "bruto/$id.png" ] && continue
  bash ~/.claude/skills/gpt-imagem-playwright/scripts/gerar-1-imagem.sh "bruto/$id.txt" "bruto/$id.png" bruto/ref-padrao.jpg 2>&1 | tail -2
done
