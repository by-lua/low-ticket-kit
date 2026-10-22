#!/usr/bin/env bash
# Busca formatos no catálogo local.
#   buscar.sh                       lista categorias com contagem
#   buscar.sh <termo>               busca por categoria/título
#   buscar.sh --tipo video          só vídeos (ou estatico)
#   buscar.sh --cat antes-e-depois  todos de uma categoria
set -euo pipefail
B="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/biblioteca"
C="$B/catalogo.json"

case "${1:-}" in
  "") python3 -c "
import json,collections
m=json.load(open('$C'))
for (t,c),n in sorted(collections.Counter((i['tipo'],i['categoriaLabel']) for i in m).items(),key=lambda x:-x[1]):
    print(f'{n:3}  {t:9} {c}')" ;;
  --tipo) python3 -c "
import json;m=json.load(open('$C'))
[print(f\"{i['id']:>4}  {i['categoriaLabel']:<24} {i['titulo']}\n      $B/formatos/{i['tipo']}/{i['categoria']}/\") for i in m if i['tipo']=='$2']" ;;
  --cat) ls -1 "$B/formatos"/*/"$2"/ ;;
  *) python3 -c "
import json,sys;m=json.load(open('$C'));q='$1'.lower()
[print(f\"{i['id']:>4}  {i['tipo']:<9} {i['categoriaLabel']:<24} {i['titulo']}\n      $B/formatos/{i['tipo']}/{i['categoria']}/{i['id']}-{i['nome']}\") for i in m if q in i['categoriaLabel'].lower() or q in i['titulo'].lower()]" ;;
esac
