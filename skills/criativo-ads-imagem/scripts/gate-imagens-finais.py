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
  5. `anuncio.md` existe e o Título fala da dor/pessoa — rótulo de produto ("Lado luz y lado
     sombra", "Cada símbolo, explicado") reprova (dona 27/10/2026).

Saída: OK/FALHA por checagem, veredito na última linha. Exit 1 quando alguma falha.
"""
import re
import sys
from pathlib import Path

ALVOS = {  # nome: (razão alvo, tolerância, largura mínima)
    '4:5': (1080 / 1350, 0.010, 1080),
    '9:16': (1080 / 1920, 0.010, 1080),
}


def ler_titulo(md):
    """Título do anuncio.md: '**Título:** X' ou '## Título ...' seguido da linha."""
    if not md.is_file():
        return None
    linhas = md.read_text(errors='ignore').splitlines()
    for i, l in enumerate(linhas):
        m = re.match(r'\s*\*\*T[ií]tulo[^*]*\*\*\s*:?\s*(.+)', l, re.I)
        if m and m.group(1).strip():
            return m.group(1).strip()
        if re.match(r'\s*#+\s*T[ií]tulo', l, re.I):
            for nxt in linhas[i + 1:]:
                if nxt.strip():
                    return nxt.strip()
    return None


# Sinais de que a frase fala com/sobre a pessoa ou nega a dor. Rótulo de produto não tem nenhum.
SINAL_DOR = re.compile(
    r'\?|\b(voc[eê]|vc|seu|sua|te|tu|t[uú]|vos|ti|le|ela|ele|ella|[eé]l|mi|meu|minha|'
    r'n[aã]o|no|nunca|nem|ni|sem|sin|cero|nada|ningu[eé]m|nadie|nenhuma?|ninguna?|'
    r'trava|travou|traba|olvid\w*|esquec\w*|decorar|memorizar|erro|err\w+|medo|miedo|'
    r'pare de|para de|deja de|dej[aá] de|cans\w+|outra vez|otra vez|de novo|de nuevo|'
    r'pergunta\w*|pregunta\w*|adivinh\w*|adivin\w*|'
    # promessa (Rodrigo: headline = promessa/benefício) e entrega pronta pra usar
    r'aprend\w*|descubr\w*|entend\w*|domin\w*|consig\w*|pront[oa]s?|list[oa]s?|ready|learn\w*|discover\w*)\b'
    r'|\b\w+(aste|iste|ás|és|ís)\b',  # voseo / 2ª pessoa (sabés, comprás, diste, armaste)
    re.I)


def eh_rotulo(titulo):
    return not SINAL_DOR.search(titulo)


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
                # visual próprio (fase de impacto, biblioteca): texto pedido ao modelo por linha/texto exato também vale
                pede = lambda t: alvo in t or re.search(r'(exact text|line 1\b)', t, re.I)
                if not any(pede(p.read_text(errors='ignore')) for p in prompts):
                    falhas.append(
                        f'nenhum prompt pede o texto como "{alvo}" — se o texto não foi pedido ao '
                        f'modelo, ele foi aplicado por cima (reprovado); corrigir o prompt e regerar')
                else:
                    oks.append('prompt pede o texto ao modelo (sticker de Stories ou texto exato)')
    else:
        oks.append('texto na foto dispensado (--sem-texto): peça de impacto / só páginas')

    # 5. Título = dor virada frase, nunca rótulo do produto (dona 27/10/2026, Tarot AR leva 9)
    if pasta:
        titulo = ler_titulo(pasta / 'anuncio.md')
        if titulo is None:
            falhas.append('sem anuncio.md com Título — escrever junto do prompt (passo 4) antes de chamar de pronta')
        elif eh_rotulo(titulo):
            falhas.append(
                f'título-rótulo: "{titulo}" — só descreve uma parte do material. Headline = promessa/'
                f'benefício ligado à dor (ou a dor medida em frase) + texto de baixo com mecanismo/entrega '
                f'(criativo-ads/references/texto-anuncio-por-angulo.md §1)')
        else:
            oks.append(f'título fala da dor/pessoa: "{titulo}"')

    for x in oks:
        print('OK    ', x)
    for x in falhas:
        print('FALHA ', x)
    print('\n' + ('BLOQUEADO — peça não está pronta' if falhas else 'LIBERADO'))
    return 1 if falhas else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
