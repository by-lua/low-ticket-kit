#!/usr/bin/env python3
"""gate-corpo-video.py — bloqueia vídeo que repete o CORPO de outro trocando só o gancho.

Uso:  python3 gate-corpo-video.py OFERTAS/<slug> [--limite 0.6]

Regra da dona (25/10 e 27/10/2026): peça nova = gancho E corpo diferentes. Pegar o corpo de um vídeo
e trocar só a 1ª frase é a mesma peça pro Meta (Andrômeda agrupa). Caso real: Atlas AR, CRIATIVO-01,
02, 12, 13 e 22 com o mesmo corpo ("No es que no estudiaste. Es que memorizar el nombre del músculo...").

Lê a fala de cada vídeo em:
  - criativos/**/anuncio.md  → linhas "**VO...:**" e as citações (>) logo abaixo de "VO"/"Fala";
  - criativos/ROTEIROS*.md   → uma peça por seção "##"/"###": citações (>) e a coluna "Fala" das tabelas.
Corpo = fala sem a 1ª frase (gancho) e sem a última (CTA). Compara todos os pares; semelhança
>= limite (padrão 0.6) = FALHA.
"""
import difflib, re, sys, unicodedata
from pathlib import Path


def norm(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9 ]+', ' ', s)


def frases(texto):
    return [f.strip() for f in re.split(r'(?<=[.!?…])\s+', texto) if len(f.strip()) > 2]


def corpo(texto):
    fs = frases(texto)
    return ' '.join(fs[1:-1]) if len(fs) >= 3 else ''


def fala_anuncio(md):
    t = md.read_text(errors='ignore').splitlines()
    partes, em_vo = [], False
    for l in t:
        s = l.strip()
        # "VO" palavra inteira (não pega "**Voz:**") ou "Fala"
        m = re.match(r'\*\*(VO\b|Fala\b)[^*]*\*\*\s*:?\s*(.*)', s, re.I)
        if m:
            em_vo = True
            if m.group(2).strip():
                partes.append(m.group(2).strip())
            continue
        if not em_vo:
            continue
        if not s or s.startswith(('**', '#', '|', '-', '```')):
            em_vo = False          # fim do bloco de fala
        else:
            partes.append(s.lstrip('>').strip())  # citação ou linha que continua o parágrafo
    return ' '.join(partes)


def falas_roteiro(md):
    pecas, nome, buf, col = {}, None, [], None
    for l in md.read_text(errors='ignore').splitlines():
        h = re.match(r'#{2,3}\s+(.*)', l)
        if h:
            if nome and buf:
                pecas[nome] = ' '.join(buf)
            nome, buf, col = h.group(1).strip()[:60], [], None
            continue
        if not nome:
            continue
        s = l.strip()
        if s.startswith('>'):
            buf.append(s.lstrip('>').strip())
        elif s.startswith('|'):
            cels = [c.strip() for c in s.strip('|').split('|')]
            if any(n(c) == 'fala' for c in cels):
                col = [n(c) for c in cels].index('fala')
            elif col is not None and len(cels) > col and not set(cels[col]) <= set('-: '):
                buf.append(cels[col])
    if nome and buf:
        pecas[nome] = ' '.join(buf)
    return pecas


def n(s):
    return norm(s).strip()


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        sys.exit(__doc__)
    limite = 0.6
    if '--limite' in sys.argv:
        limite = float(sys.argv[sys.argv.index('--limite') + 1])
    cri = Path(args[0]).resolve() / 'criativos'
    if not cri.is_dir():
        sys.exit(f'sem pasta {cri}')
    pecas = {}
    for md in sorted(cri.rglob('anuncio.md')):
        if '_arquivo' in md.parts:
            continue
        f = fala_anuncio(md)
        if f:
            pecas[str(md.parent.relative_to(cri))] = f
    for md in sorted(cri.glob('ROTEIROS*.md')):
        for nome, f in falas_roteiro(md).items():
            pecas[f'{md.name} › {nome}'] = f
    corpos = {k: norm(corpo(v)).split() for k, v in pecas.items()}
    corpos = {k: v for k, v in corpos.items() if len(v) >= 8}
    falhas = []
    ks = sorted(corpos)
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            r = difflib.SequenceMatcher(None, corpos[ks[i]], corpos[ks[j]]).ratio()
            if r >= limite:
                falhas.append((r, ks[i], ks[j]))
    proibidos = []
    proib = re.compile(r'\bb[oô]n(o|u)s\b|\bvol[uú]me(n|s)?\b|\bm[oó]dulos?\b|'
                       r'\+?\d{2,}[.\d]*\s*(fichas|p[aá]ginas|mapas|actividades|atividades|hojas)', re.I)
    for k, v in pecas.items():
        h = proib.search(v)
        if h:
            proibidos.append(f'{k}: fala cita bônus/módulo/contagem "{h.group(0)}" — fala do produto (dona 27/10/2026)')
    print(f'OK     {len(corpos)} vídeo(s) com corpo falado lido(s)')
    for r, a, b in sorted(falhas, reverse=True):
        print(f'FALHA  corpo {r:.0%} igual: {a}  ×  {b}')
    for x in proibidos:
        print('FALHA ', x)
    if falhas or proibidos:
        print('\nBLOQUEADO — reescrever: corpo repetido = mesma peça; bônus/módulo/contagem na fala = proibido '
              '(METODO-RODRIGO-SLOTS.md · texto-anuncio-por-angulo.md)')
    else:
        print('\nLIBERADO')
    sys.exit(1 if (falhas or proibidos) else 0)


if __name__ == '__main__':
    main()
