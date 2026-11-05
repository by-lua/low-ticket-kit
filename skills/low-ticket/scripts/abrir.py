#!/usr/bin/env python3
"""abrir.py — abertura do sistema LOW-TICKET (padrão MazyOS: índice curto, puxa só o que precisa).

Uso:
  python3 abrir.py                      # índice + métodos ativos + lista de ofertas
  python3 abrir.py "<oferta>"           # + arquivos da oferta (aceita apelido: "tarot ar")
  python3 abrir.py "<oferta>" "<etapa>" # + etapa pedida (E1..E9 ou palavra: pagina, checkout, criativo…)
"""
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
OFERTAS = RAIZ / 'OFERTAS'
ARQ = RAIZ / '_arquivo/memoria-antiga-2026-10-30'

ETAPAS = {
    'E1': ('escolher a oferta', ['oferta', 'biblioteca', 'link', 'referencia', 'minerar', 'escolher']),
    'E2': ('direção + ficha da oferta', ['direcao', 'modelador', 'modelar', 'ficha', 'caminho']),
    'E3': ('página', ['pagina', 'landing', 'copy da pagina']),
    'E4': ('entregável', ['entregavel', 'entrega', 'mvp', 'produto', 'exercicio', 'poster']),
    'E5': ('imagens da página', ['mockup', 'imagens', 'depoimento']),
    'E6': ('área de membros', ['painel', 'area de membros', 'membros', 'pdf']),
    'E7': ('funil', ['funil', 'bump', 'upsell', 'downsell', 'upgrade', 'combo', 'bonus']),
    'E8': ('checkout', ['checkout', 'wiven', 'mundpay', 'gateway', 'banner', 'webhook']),
    'E9': ('gates no ar', ['gate', 'pixel', 'evento', 'no ar', 'publicar']),
    'CTV': ('criativo → skill mãe `criativo`', ['criativo', 'anuncio', 'video', 'estatico', 'carrossel', 'leva']),
}


def norm(s):
    return unicodedata.normalize('NFKD', s.lower()).encode('ascii', 'ignore').decode()


def mostra(p, limite=None):
    if not p.exists():
        print(f'\n--- {p.relative_to(RAIZ)} — NÃO EXISTE')
        return False
    linhas = p.read_text(encoding='utf-8', errors='replace').splitlines()
    corte = linhas[:limite] if limite else linhas
    print(f'\n--- {p.relative_to(RAIZ)} ({len(linhas)} linhas{", primeiras " + str(limite) if limite and len(linhas) > limite else ""}) ---')
    print('\n'.join(corte))
    return True


def acha_oferta(q):
    alvo = norm(q).replace('-', ' ').split()
    achadas = [d for d in sorted(OFERTAS.iterdir()) if d.is_dir() and all(t in norm(d.name).replace('-', ' ') for t in alvo)]
    return achadas


def main():
    args = sys.argv[1:]
    mostra(RAIZ / 'INDICE.md')
    mostra(RAIZ / '_memoria/METODOS-ATIVOS.md')
    oferta = None
    if args:
        achadas = acha_oferta(args[0])
        if len(achadas) == 1:
            oferta = achadas[0]
        else:
            print(f'\n⛔ oferta "{args[0]}": {len(achadas)} resultados — use o slug exato.')
    if not oferta:
        print('\nOfertas:', ', '.join(d.name for d in sorted(OFERTAS.iterdir()) if d.is_dir()))
    else:
        s = oferta.name
        print(f'\n===== OFERTA {s} =====')
        mostra(oferta / 'CLAUDE.md')
        tem_ficha = mostra(oferta / 'OFERTA.md')
        tem_status = mostra(oferta / 'STATUS.md', 60)
        if not mostra(oferta / 'ATIVOS.md'):
            print('⚠ Sem ATIVOS.md — não há registro do que é NOSSO oficial × DESCARTADO × CONCORRENTE. '
                  'Criar de MODELOS/_MODELO-ATIVOS.md ANTES de usar capa/mockup/persona como referência (skill low-ticket § 2b).')
        mod = sorted((oferta / 'pesquisa').glob('modelador-*.md')) if (oferta / 'pesquisa').exists() else []
        print('\nModelador salvo:', ', '.join(m.name for m in mod) or 'NENHUM')
        if not tem_status and (ARQ / 'ofertas' / s / 'STATUS.md').exists():
            print(f'Fatos antigos (só consulta): _arquivo/memoria-antiga-2026-10-30/ofertas/{s}/STATUS.md')
        if not tem_ficha:
            print('⚠ Sem OFERTA.md — etapa E2 não feita. Nada de página/entregável/criativo antes dela.')
    etapa = None
    if len(args) > 1:
        t = norm(' '.join(args[1:]))
        etapa = next((k for k in ETAPAS if k.lower() == t.strip()), None) or \
            next((k for k, (_, kws) in ETAPAS.items() if any(kw in t for kw in kws)), None)
    print('\n===== RECIBO (devolver à dona antes de agir) =====')
    print(f'Oferta: {oferta.name if oferta else "—"}')
    print(f'Etapa: {etapa + " · " + ETAPAS[etapa][0] if etapa else "— (dizer qual)"}')
    print('Li: INDICE.md · METODOS-ATIVOS.md' + (' · arquivos da oferta acima' if oferta else ''))
    print('Vou chamar: <filha/skill da etapa, conforme SKILL.md do low-ticket>')
    print('Métodos desligados que NÃO vou usar: <ver METODOS-ATIVOS.md>')


if __name__ == '__main__':
    main()
