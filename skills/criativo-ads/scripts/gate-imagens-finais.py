#!/usr/bin/env python3
"""gate-imagens-finais.py — confere as IMAGENS FINAIS de uma peça (estático ou carrossel).

O `gate-pecas-criativo.py` olha o que ENTRA na cena (páginas, referência, repetição).
Este olha o que SAI: tamanho, proporção e se o texto foi pedido ao modelo.

Uso:
  python3 gate-imagens-finais.py <final1> [final2 ...] --pasta CRIATIVO-N/ [--story]

Confere:
  1. Proporção 4:5 (0.800 ± 0.010) em toda imagem final — 9:16 (0.5625) com --story.
  2. Largura mínima 1080 (carrossel de crop pequeno ou página crua reprova aqui — foi o bug
     do Mapa del Tarot AR 25/10: cards de 480×483 e página 1200×848 passando como "pronta").
  3. Todas as imagens da MESMA peça com o MESMO tamanho (carrossel com cards de tamanhos
     diferentes o Meta rejeita / corta).
  4. `intermediarios/prompt*.txt` existe e pede o texto como "Instagram Stories text sticker"
     — texto aplicado por overlay de código não é criativo pronto. Não há dispensa (26/10/2026):
     impacto tem texto gerado; carrossel "só páginas" tem card de gancho e card de CTA gerados.

Saída: OK/FALHA por checagem, veredito na última linha. Exit 1 quando alguma falha.
"""
import sys
from pathlib import Path

ALVOS = {  # nome: (razão alvo, tolerância, largura mínima)
    '4:5': (1080 / 1350, 0.010, 1080),
    '9:16': (1080 / 1920, 0.010, 1080),
}


def main(argv):
    arquivos, pasta = [], None
    formato, sem_texto = '4:5', False
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == '--pasta':
            i += 1
            pasta = Path(argv[i])
        elif a == '--story':
            formato = '9:16'
        elif a in ('--sem-texto', '--só-páginas', '--so-paginas'):
            sys.exit(f'{a} não existe mais (26/10/2026): toda peça de imagem tem texto escrito pelo modelo — '
                     'até o carrossel só de páginas tem card de gancho e card de CTA gerados (GUIA DE IMAGEM).')
        elif a.startswith('--'):
            sys.exit(f'opção desconhecida: {a}')
        else:
            arquivos.append(Path(a))
        i += 1

    if not arquivos:
        sys.exit(__doc__)

    try:
        from PIL import Image
    except ImportError:
        sys.exit('FALTA Pillow — sem ele não dá pra conferir tamanho de imagem')

    razao_alvo, tol, largura_min = ALVOS[formato]
    falhas, oks = [], []
    tamanhos = {}

    for p in arquivos:
        if not p.is_file():
            falhas.append(f'arquivo não existe: {p}')
            continue
        with Image.open(p) as im:
            w, h = im.size
        tamanhos.setdefault((w, h), []).append(p.name)
        razao = w / h
        if abs(razao - razao_alvo) > tol:
            falhas.append(
                f'{p.name}: proporção {razao:.3f} ({w}x{h}) — a peça é {formato} '
                f'({razao_alvo:.3f}); recortar/remontar antes de chamar de pronta')
        if w < largura_min:
            falhas.append(
                f'{p.name}: {w}px de largura (mínimo {largura_min}) — crop/upscale pequeno '
                f'sai borrado no feed; usar o arquivo nativo da página')

    if len(tamanhos) > 1:
        detalhe = ' · '.join(f'{w}x{h}: {", ".join(n)}' for (w, h), n in tamanhos.items())
        falhas.append(f'cards com tamanhos diferentes na mesma peça → {detalhe}')
    else:
        oks.append(f'{len(arquivos)} imagem(ns), todas em {next(iter(tamanhos))}')

    if not sem_texto:
        if not pasta:
            falhas.append('informe --pasta CRIATIVO-N/ pra conferir o prompt do texto')
        else:
            prompts = sorted((pasta / 'intermediarios').glob('prompt*.txt'))
            if not prompts:
                falhas.append(
                    'sem intermediarios/prompt*.txt — peça de imagem sem prompt salvo não é '
                    'auditável (foi assim que o Tarot AR recebeu texto por overlay)')
            else:
                alvo = 'Instagram Stories text sticker'
                if not any(alvo in p.read_text(errors='ignore') for p in prompts):
                    falhas.append(
                        f'nenhum prompt pede o texto como "{alvo}" — se o texto não foi pedido ao '
                        f'modelo, ele foi aplicado por cima (reprovado); corrigir o prompt e regerar')
                else:
                    oks.append('prompt pede o texto como sticker de Stories')
    else:
        oks.append('texto na foto dispensado (--sem-texto): peça de impacto / só páginas')

    for x in oks:
        print('OK    ', x)
    for x in falhas:
        print('FALHA ', x)
    print('\n' + ('BLOQUEADO — peça não está pronta' if falhas else 'LIBERADO'))
    return 1 if falhas else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
