#!/usr/bin/env python3
"""Monta card 4:5 (1080x1350) a partir de UMA pagina real do entregavel (1200x848, paisagem).

A pagina ocupa a largura inteira do card, na resolucao nativa (1080 de largura = 0.9x, texto
legivel). A sobra vertical e preenchida com o proprio papel da pagina: repete a faixa limpa da
borda (topo/base), sem espelhar conteudo e sem criar faixa branca de slide.

Uso:
  python3 montar-cards.py <pagina> <saida>
"""
import sys
from PIL import Image

W, H = 1080, 1350
STRIP = 6  # faixa de papel limpa copiada do topo/base da pagina


def abre(caminho):
    im = Image.open(caminho)
    return im.convert('RGB') if im.mode != 'RGB' else im


def papel(base, altura, faixa, de_baixo=False):
    """Repete a faixa de papel ate preencher a altura pedida (grao preservado, sem esticar)."""
    tela = Image.new('RGB', (W, altura))
    y = 0
    while y < altura:
        tela.paste(faixa, (0, y))
        y += faixa.size[1]
    return tela.crop((0, 0, W, altura)) if de_baixo else tela


def card(pagina, destino):
    p = abre(pagina)
    pw, ph = p.size
    nh = round(ph * W / pw)
    if nh > H:
        raise SystemExit(f'pagina mais alta que o card: {nh}>{H}')
    p = p.resize((W, nh), Image.LANCZOS)
    sobra = H - nh
    topo = sobra // 2
    base = sobra - topo

    tela = Image.new('RGB', (W, H))
    if topo:
        tela.paste(papel(p, topo, p.crop((0, 0, W, STRIP))), (0, 0))
    tela.paste(p, (0, topo))
    if base:
        tela.paste(papel(p, base, p.crop((0, nh - STRIP, W, nh))), (0, topo + nh))

    tela.save(destino, quality=93, method=6)
    return tela.size


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    print(card(sys.argv[1], sys.argv[2]), sys.argv[2])
