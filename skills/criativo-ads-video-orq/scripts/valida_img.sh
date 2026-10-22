#!/bin/bash
# valida_img.sh <caminho-imagem-cena>  -> falha se a imagem nao for legitima
IMG="$1"
[ -f "$IMG" ] || { echo "IMGFAIL: nao existe $IMG"; exit 1; }
# 1) dimensao exata do lote
D=$(ffprobe -v error -show_entries stream=width,height -of csv=p=0 "$IMG")
[ "$D" = "941,1672" ] || { echo "IMGFAIL: dimensao $D (esperado 941,1672)"; exit 1; }
# 2) tem que ser byte-identica a alguma imagem aprovada DO PROPRIO criativo
N=$(echo "$IMG" | grep -oP 'CRIATIVO-\K[0-9]+')
BASE=$(echo "$IMG" | sed 's|/CRIATIVO-.*||')
H=$(md5sum "$IMG" | cut -d' ' -f1)
MATCH=$(md5sum "$BASE"/_IMG/numes-$N-*.png 2>/dev/null | grep -c "^$H")
[ "$MATCH" -ge 1 ] || { echo "IMGFAIL: $IMG nao bate com nenhuma imagem aprovada de CRIATIVO-$N"; exit 1; }
NOME=$(md5sum "$BASE"/_IMG/numes-$N-*.png 2>/dev/null | grep "^$H" | head -1 | sed 's|.*/||')
echo "IMGOK $(basename "$IMG") = $NOME"
