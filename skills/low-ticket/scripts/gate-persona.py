#!/usr/bin/env python3
"""gate-persona.py — trava antes de página, criativo, peça do funil ou preço.

Uso:  python3 gate-persona.py OFERTAS/<slug>        (sai 1 se FALHA)

Lição da dona (23/10/2026): Elétrica estudou o estudante e quem compra é o eletricista na obra;
Jiu-Jitsu usou "faixa branca/azul" e só vendeu quando tirou da página. Todo recorte precisa de dado.

Confere em OFERTAS/<slug>/pesquisa/PERSONA-E-ANGULOS.md (modelo: MODELOS/_MODELO-PERSONA-E-ANGULOS.md):
  1. seções obrigatórias (O QUE VENDEMOS, NÃO É, MERCADO, QUEM COMPRA DE VERDADE, PERSONA, DORES, RECORTES, ÂNGULOS)
  2. MERCADO: >= 5 links da Biblioteca de Anúncios
  3. DORES: cada linha com contagem numérica + data, ou marcada "hipótese"; >= 3 dores com contagem
  4. RECORTES: recorte "sem dado" não pode aparecer no <h1>/headline da página
  5. QUEM COMPRA: tem evidência ou "sem vendas ainda" + plano de medição
  6. data do arquivo <= 30 dias (aviso)
  7. TERMOS DE BUSCA (lição Atlas 23/10): >= 2 termos com fonte+índice, >= 1 veredito "gancho";
     "Unidade da peça" e "Cena da dor" preenchidas. Nome do produto não é termo de busca.
  8. NARRATIVAS QUE RODAM: >= 2 linhas com dias no ar
  9. ÂNCORA DE PREÇO: >= 2 vizinhos com preço + linha "Decisão:"
Receita da pesquisa: references/PESQUISA-PADRAO-OFERTA.md
"""
import datetime, re, sys, unicodedata
from pathlib import Path


def n(s):
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()


SECOES = {
    'O QUE VENDEMOS': r'^##+ .*o que vendemos',
    'NÃO É': r'^##+ .*nao e\b',
    'MERCADO (Biblioteca)': r'^##+ .*(mercado|biblioteca)',
    'QUEM COMPRA DE VERDADE': r'^##+ .*quem compra',
    'PERSONA': r'^##+ .*(persona|a quem vendemos|quem a gente vende)',
    'DORES': r'^##+ .*dores',
    'RECORTES': r'^##+ .*recortes',
    'ÂNGULOS': r'^##+ .*angulos',
    'TERMOS DE BUSCA': r'^##+ .*termos de busca',
    'NARRATIVAS QUE RODAM': r'^##+ .*narrativas',
    'ÂNCORA DE PREÇO': r'^##+ .*ancora de preco',
    'TERMOS OBRIGATÓRIOS DO CRIATIVO': r'^##+ .*termos obrigat[oó]rios do criativo',
}


def secao(txt, rx):
    m = re.search(rx, txt, re.M)
    if not m:
        return None
    resto = txt[m.end():]
    fim = re.search(r'^## ', resto, re.M)
    return resto[:fim.start()] if fim else resto


def linhas_tabela(bloco):
    """Linhas de TODAS as tabelas do bloco, sem o cabeçalho de cada uma."""
    out, cab = [], True
    for l in (bloco or '').splitlines():
        l = l.strip()
        if not l.startswith('|'):
            cab = True  # fim de tabela: a próxima linha '|' é cabeçalho
            continue
        if re.match(r'^\|[\s:|-]+\|$', l):
            continue
        if cab:
            cab = False
            continue
        out.append([c.strip() for c in l.strip('|').split('|')])
    return out


def headline(of: Path) -> str:
    for cand in ['site/index.html', 'pagina/index.html', 'site/public/index.html']:
        p = of / cand
        if p.exists():
            h = p.read_text(encoding='utf-8', errors='ignore')
            partes = re.findall(r'<h1[^>]*>(.*?)</h1>', h, re.S | re.I)
            partes += re.findall(r'<title>(.*?)</title>', h, re.S | re.I)
            return n(re.sub(r'<[^>]+>', ' ', ' '.join(partes)))
    return ''


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    of = Path(sys.argv[1]).resolve()
    arq = of / 'pesquisa' / 'PERSONA-E-ANGULOS.md'
    falhas, avisos, oks = [], [], []
    if not arq.exists():
        print(f'FALHA  {arq} não existe — criar a partir de MODELOS/_MODELO-PERSONA-E-ANGULOS.md')
        sys.exit(1)
    raw = arq.read_text(encoding='utf-8')
    txt = n(raw)

    for nome, rx in SECOES.items():
        (oks if re.search(rx, txt, re.M) else falhas).append(f'seção {nome}' + ('' if re.search(rx, txt, re.M) else ' ausente'))

    merc = secao(txt, SECOES['MERCADO (Biblioteca)'])
    links = len(re.findall(r'facebook\.com/ads/library', merc or ''))
    if merc is not None:
        (oks if links >= 5 else falhas).append(f'Biblioteca: {links} links (mín. 5)')

    bloco_d = secao(txt, SECOES['DORES']) or ''
    data_secao = re.search(r'\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}', '\n'.join(l for l in bloco_d.splitlines() if not l.strip().startswith('|')))
    dores = linhas_tabela(bloco_d)
    com_cont, sem = 0, []
    for c in dores:
        linha = ' '.join(c)
        tem_num = any(re.fullmatch(r'[\d.,]+', x.replace(' ', '')) and x not in ('0',) for x in c[2:]) or \
            re.search(r'\b\d{2,}\b(?!-\d)', ' '.join(c[2:]).replace('2026', ''))
        tem_data = re.search(r'\d{4}-\d{2}-\d{2}|\d{2}/\d{2}', linha) or data_secao
        if 'hipotese' in linha:
            continue
        if tem_num and tem_data:
            com_cont += 1
        else:
            sem.append(c[1][:60] if len(c) > 1 else linha[:60])
    if dores:
        (oks if com_cont >= 3 else falhas).append(f'dores com contagem+data: {com_cont} (mín. 3)')
        for d in sem:
            falhas.append(f'dor sem contagem/data e não marcada "hipótese": {d}')

    rec = linhas_tabela(secao(txt, SECOES['RECORTES']))
    h1 = headline(of)
    for c in rec:
        if not c or not c[0]:
            continue
        sem_dado = 'sem dado' in ' '.join(c) or (len(c) > 2 and c[2] in ('', '-', '—'))
        termo = re.sub(r'["“”*`]|ex\.:', '', c[0]).strip()
        if sem_dado and termo and h1 and termo in h1:
            falhas.append(f'recorte SEM DADO na headline/página: "{termo}"')
        elif sem_dado:
            avisos.append(f'recorte sem dado (ok só como ângulo de teste): "{termo}"')

    qc = secao(txt, SECOES['QUEM COMPRA DE VERDADE']) or ''
    if qc and not re.search(r'sem vendas ainda|venda|vendas|comentario|pergunta|trackeador|suporte', qc):
        falhas.append('QUEM COMPRA: sem evidência nem "sem vendas ainda" + plano de medição')

    # 7 · termos de busca
    bt = secao(txt, SECOES['TERMOS DE BUSCA'])
    if bt is not None:
        termos = [c for c in linhas_tabela(bt) if c and c[0]]
        validos = [c for c in termos if len(c) > 2 and re.search(r'\d', c[2])]
        (oks if len(validos) >= 2 else falhas).append(f'termos de busca com índice/contagem: {len(validos)} (mín. 2)')
        if not any('gancho' in ' '.join(c[3:]) for c in termos):
            falhas.append('TERMOS DE BUSCA: nenhum termo com veredito "gancho" — o gancho fica sem termo validado')
        for rot in ('unidade da peca', 'cena da dor'):
            mm = re.search(r'\*\*' + rot + r':\*\*\s*(.+)', bt)
            if not mm or mm.group(1).strip().startswith('(') or len(mm.group(1).strip()) < 4:
                falhas.append(f'TERMOS DE BUSCA: "{rot}" não preenchida')
    # 8 · narrativas
    bn = secao(txt, SECOES['NARRATIVAS QUE RODAM'])
    if bn is not None:
        narr = [c for c in linhas_tabela(bn) if c and c[0] and len(c) > 2 and re.search(r'\d', c[2])]
        (oks if len(narr) >= 2 else falhas).append(f'narrativas com dias no ar: {len(narr)} (mín. 2)')
    # 9 · âncora de preço
    ba = secao(txt, SECOES['ÂNCORA DE PREÇO'])
    if ba is not None:
        viz = [c for c in linhas_tabela(ba) if c and c[0] and len(c) > 1 and re.search(r'\d', c[1])]
        (oks if len(viz) >= 2 else falhas).append(f'âncora de preço: {len(viz)} vizinhos (mín. 2)')
        if not re.search(r'decisao:\**\s*\w', ba):
            falhas.append('ÂNCORA DE PREÇO: falta a linha "Decisão:"')

    # 10 · termos obrigatórios do criativo (dona 30/10/2026 — caso GeriNeuro CRIATIVO-14 genérico)
    bto = secao(txt, SECOES['TERMOS OBRIGATÓRIOS DO CRIATIVO'])
    if bto is not None:
        mt = re.search(r'^`([^`]+)`\s*$', bto, re.M)
        termos = [t.strip() for t in mt.group(1).split(',') if t.strip()] if mt else []
        (oks if len(termos) >= 2 else falhas).append(
            f'termos obrigatórios do criativo: {len(termos)} (mín. 2)' if len(termos) >= 2 else
            'TERMOS OBRIGATÓRIOS DO CRIATIVO: lista vazia ou mal formatada — precisa de uma linha só '
            'com crase, ex.: `Alzheimer, dementia, cognitive`. Sem isso o criativo sai genérico '
            '(reprovado depois por gate-imagens-finais.py / gate-corpo-video.py).')

    m = re.search(r'\*\*data:\*\*\s*(\d{4}-\d{2}-\d{2})', txt)
    if m:
        dias = (datetime.date.today() - datetime.date.fromisoformat(m.group(1))).days
        (avisos if dias > 30 else oks).append(f'arquivo com {dias} dias' + (' — revisar' if dias > 30 else ''))
    else:
        avisos.append('sem "**Data:** AAAA-MM-DD" no topo')

    for x in oks:
        print('OK    ', x)
    for x in avisos:
        print('AVISO ', x)
    for x in falhas:
        print('FALHA ', x)
    print('\n' + ('BLOQUEADO — corrigir antes de página/criativo/funil/preço' if falhas else 'LIBERADO'))
    sys.exit(1 if falhas else 0)


if __name__ == '__main__':
    main()
