#!/usr/bin/env python3
"""gate-pecas-criativo.py — confere a pasta de UM criativo antes de gerar a cena/montar o vídeo.

Uso:  python3 gate-pecas-criativo.py OFERTAS/<slug>/criativos/[ES/]CRIATIVO-<N>[-slug]

Regra da dona (23/10/2026):
  - Os takes de vídeo e as imagens que vão ENTRAR na peça (capa + páginas) ficam em
    CRIATIVO-N/selecionados/, separados do resto (intermediarios/, gravações brutas).
  - Nada repete: PC, celular, tablet e folha solta mostram cada um uma página DIFERENTE.
    Capa + 3-5 páginas distintas que façam sentido juntas. Nunca a mesma imagem em vários aparelhos.

Confere: selecionados/ existe; >= 3 imagens distintas (capa conta); nenhuma duplicata
(md5 e, com Pillow, hash visual — o GPT re-renderiza a mesma página com bytes diferentes).
"""
import hashlib, sys
from pathlib import Path

IMG = {'.png', '.jpg', '.jpeg', '.webp'}
VID = {'.mp4', '.mov', '.webm', '.mkv'}


def ahash(p):
    try:
        from PIL import Image
    except ImportError:
        return None
    im = Image.open(p).convert('L').resize((16, 16))
    px = list(im.tobytes())
    m = sum(px) / len(px)
    return int(''.join('1' if x > m else '0' for x in px), 2)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    d = Path(sys.argv[1]).resolve()
    sel = d / 'selecionados'
    falhas, oks = [], []
    if not sel.is_dir():
        print(f'FALHA  {sel} não existe — separar os takes e as imagens que entram na peça antes de gerar')
        sys.exit(1)
    imgs = sorted(p for p in sel.rglob('*') if p.suffix.lower() in IMG)
    vids = sorted(p for p in sel.rglob('*') if p.suffix.lower() in VID)
    oks.append(f'{len(imgs)} imagens e {len(vids)} takes em selecionados/')
    md5 = {}
    for p in imgs:
        md5.setdefault(hashlib.md5(p.read_bytes()).hexdigest(), []).append(p.name)
    for nomes in md5.values():
        if len(nomes) > 1:
            falhas.append('mesma imagem repetida: ' + ', '.join(nomes))
    hs = [(p.name, ahash(p)) for p in imgs]
    hs = [(nm, h) for nm, h in hs if h is not None]
    for i in range(len(hs)):
        for j in range(i + 1, len(hs)):
            if bin(hs[i][1] ^ hs[j][1]).count('1') <= 8:  # ~3% de 256 bits
                falhas.append(f'imagens quase iguais (mesma página?): {hs[i][0]} × {hs[j][0]}')
    distintas = len(imgs) - sum(len(v) - 1 for v in md5.values())
    if distintas < 3:
        falhas.append(f'só {distintas} imagem(ns) distinta(s) — usar capa + 3-5 páginas diferentes')
    for x in oks:
        print('OK    ', x)
    for x in falhas:
        print('FALHA ', x)
    print('\n' + ('BLOQUEADO — trocar as repetidas antes de gerar a cena' if falhas else 'LIBERADO'))
    sys.exit(1 if falhas else 0)


if __name__ == '__main__':
    main()
