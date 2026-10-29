#!/usr/bin/env python3
"""gate-plano-leva.py — confere o plano de leva ANTES de mostrar pra dona e ANTES de produzir.

Uso:  python3 gate-plano-leva.py OFERTAS/<slug> [criativos/PLANO-LEVA-1.md] [--producao]
      --producao: sem "- [x] OK da dona" no plano também é FALHA (use antes de gerar qualquer peça).

Regras da dona (23/10/2026) que este script cobra:
  1. gate-persona.py da oferta LIBERADO (persona, termos de busca, narrativas, âncora de preço)
  2. DESIGN-SYSTEM.md na oferta (cor/fonte vêm dele; sem ele o GPT inventa cor)
  3. por campanha (## Campanha N): os 3 formatos (vídeo, estático, carrossel); >= 2 vídeos;
     imagens >= vídeos; 3 campanhas de 10 = 7+3, 5+5 e 6+4 (uma de cada, dona 26/10/2026)
  4. nenhuma linha de peça com "PDF" ou "mockup" (vendemos material organizado na área de membros)
  5. ângulo citado (A0, A1…) existe no BANCO DE ÂNGULOS e não está DESCARTADO
  6. termo marcado "só nome do produto"/"descartado" em TERMOS DE BUSCA não vira gancho (aviso)
  7. tabela de personagens com voz; orçamento por campanha escrito; feed 4:5
  8. vídeo no plano → criativos/MATERIAL-ENTREGAVEL/ com gravação de tela
  9. 1 peça com preço por campanha (aviso)
 12. regra digital + impresso escrita no plano
 10. preço no criativo = SEMPRE o do plano mais barato quando a página tem 2 planos (dona, 23/10/2026).
     Plano da leva traz a linha "**Preço no criativo:** <moeda> <valor>"; o valor tem que ser o menor
     plano do O QUE VENDEMOS (popup/saída/bump não contam como plano).
"""
import re, subprocess, sys, unicodedata
from pathlib import Path

GATE_PERSONA = Path.home() / '.claude/skills/criacao-low-ticket-mvt/scripts/gate-persona.py'


def n(s):
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    producao = '--producao' in sys.argv
    if not args:
        sys.exit(__doc__)
    of = Path(args[0]).resolve()
    plano = of / (args[1] if len(args) > 1 else 'criativos/PLANO-LEVA-1.md')
    falhas, avisos, oks = [], [], []
    if not plano.exists():
        print(f'FALHA  {plano} não existe — plano em texto vem antes de qualquer peça')
        sys.exit(1)
    raw = plano.read_text(encoding='utf-8')
    txt = n(raw)

    # 1 · persona
    r = subprocess.run([sys.executable, str(GATE_PERSONA), str(of)], capture_output=True, text=True)
    (oks if r.returncode == 0 else falhas).append(
        'gate-persona LIBERADO' if r.returncode == 0 else 'gate-persona BLOQUEADO — rodar e corrigir a persona primeiro')

    # 2 · cores
    (oks if (of / 'DESIGN-SYSTEM.md').exists() else falhas).append(
        'DESIGN-SYSTEM.md existe' if (of / 'DESIGN-SYSTEM.md').exists()
        else 'DESIGN-SYSTEM.md ausente — tirar cores/fontes da página no ar antes de gerar peça (senão a cor sai errada)')

    # 3 · campanhas
    blocos = re.split(r'^## +campanha +(\d+)[^\n]*$', txt, flags=re.M)
    camp = {}
    for i in range(1, len(blocos), 2):
        linhas = [l for l in blocos[i + 1].split('\n## ')[0].splitlines() if re.match(r'^\|\s*\d+\s*\|', l)]
        camp[blocos[i]] = linhas
    if not camp:
        falhas.append('nenhuma seção "## Campanha N" com tabela de peças')
    splits, todas = [], []
    for k, linhas in camp.items():
        cols = [[c.strip() for c in l.strip().strip('|').split('|')] for l in linhas]
        fmt = [c[1] if len(c) > 1 else '' for c in cols]
        v = sum('video' in f for f in fmt)
        e = sum('estatic' in f or f.startswith('imagem') for f in fmt)
        c = sum('carross' in f for f in fmt)
        img = e + c
        splits.append((img, v))
        todas += linhas
        tag = f'C{k}: {img} img ({e} estático + {c} carrossel) + {v} vídeo'
        erros = []
        if len(linhas) <= 3:   # 1-1-3: 1 vídeo + 1 estático + 1 carrossel (trio base, dona 27/10/2026)
            if v < 1:
                erros.append('1-1-3 sem vídeo')
        elif v < 2:
            erros.append('< 2 vídeos')
        if img < v:
            erros.append('mais vídeo que imagem (nunca 70% vídeo)')
        if not (v and e and c):
            erros.append('falta um dos 3 formatos')
        (falhas if erros else oks).append(tag + (' — ' + ', '.join(erros) if erros else ''))
        cx = [l for l in linhas if re.search(r'caixinha|caixa de pergunta|caja de pregunta', l)]
        if len(cx) > 1:
            falhas.append(f'C{k}: {len(cx)} peças de caixinha de perguntas na mesma campanha — vídeo e imagem de caixinha vão em campanhas diferentes (dona 27/10/2026)')
        if not any(re.search(r'preco|precio|price', l) for l in linhas):
            avisos.append(f'C{k}: nenhuma peça com preço')
    # trio base (dona, 27/10/2026): campanha de 3 ou 5 peças = demonstrativo + carrossel só páginas + ugly iPhone.
    # 1-1-3: uma campanha só = trio; com 2-3 campanhas, pelo menos a C1 é o trio. 1-1-5: toda campanha tem o trio.
    def trio(linhas):
        tx = ' '.join(linhas)
        return {'demonstrativo': bool(re.search(r'video[^|]*\|[^|]*demonstrativ', tx)),
                'carrossel so paginas': bool(re.search(r'carross[^|]*\|[^|]*so (com )?paginas', tx)),
                'ugly iphone': bool(re.search(r'ugly', tx))}
    peq = {k: l for k, l in camp.items() if len(l) in (3, 5)}
    for k, l in peq.items():
        falta = [x for x, ok in trio(l).items() if not ok]
        obrig = len(l) == 5 or len(camp) == 1 or k == min(camp, key=int)
        if falta and obrig:
            falhas.append(f'C{k}: trio base incompleto — falta {", ".join(falta)} (1-1-3/1-1-5, dona 27/10/2026)')
        elif not falta:
            oks.append(f'C{k}: trio base (demonstrativo + carrossel só páginas + ugly iPhone)')
    # mistura por campanha (dona, 26/10/2026): C1 70/30, C2 50/50, C3 60/40 (imagem+vídeo)
    alvo = {(7, 3), (5, 5), (6, 4)}
    dez = [x for x in splits if sum(x) == 10]
    if len(dez) >= 3 and set(dez[:3]) != alvo:
        falhas.append(f'mistura imagem+vídeo das 3 campanhas = {dez[:3]} — tem que ser 7+3, 5+5 e 6+4 (uma de cada)')
    elif len(splits) > 1 and len(set(splits)) == 1:
        avisos.append(f'todas as campanhas com o mesmo split {splits[0]} — usar 7+3 / 5+5 / 6+4')

    # 4 · PDF / mockup
    for l in todas:
        if re.search(r'\bpdf\b|mockup', l):
            falhas.append(f'peça cita PDF/mockup: {l[:90]}')

    # 5 · ângulos × banco
    pers = of / 'pesquisa/PERSONA-E-ANGULOS.md'
    ptxt = n(pers.read_text(encoding='utf-8')) if pers.exists() else ''
    banco = re.search(r'^##+ [^\n]*banco de angulos(.*?)(?=^## |\Z)', ptxt, re.M | re.S)
    banco = banco.group(1) if banco else ''
    usados = sorted(set(re.findall(r'\ba(\d{1,2})\b', ' '.join(todas))), key=int)
    for a in usados:
        lin = [l for l in banco.splitlines() if re.search(rf'\ba{a}\b', l)]
        if not lin:
            falhas.append(f'ângulo A{a} usado no plano e ausente do BANCO DE ÂNGULOS')
        elif all('descartad' in l for l in lin):
            falhas.append(f'ângulo A{a} está DESCARTADO no banco e entrou no plano')
    if usados and not [f for f in falhas if 'ngulo A' in f]:
        oks.append(f'ângulos do plano existem no banco: {", ".join("A" + a for a in usados)}')

    # 6 · termos sem busca no gancho
    termos = re.search(r'^##+ [^\n]*termos de busca(.*?)(?=^## |\Z)', ptxt, re.M | re.S)
    for l in (termos.group(1).splitlines() if termos else []):
        if l.startswith('|') and re.search(r'so nome do produto|descartad', l):
            for t in re.split(r'\s*/\s*', l.strip('|').split('|')[0].strip()):
                if len(t) > 3 and any(t in x for x in todas):
                    avisos.append(f'termo sem busca "{t}" aparece nas peças — gancho deve usar termo validado')

    # 7 · personagens, orçamento, 4:5
    pb = re.search(r'^## +personagens(.*?)(?=^## |\Z)', txt, re.M | re.S)
    if pb and 'voz' in pb.group(1) and len(re.findall(r'^\|', pb.group(1), re.M)) >= 3:
        oks.append('personagens com voz')
    else:
        falhas.append('tabela de personagens (quem, visual, ambiente, voz) ausente')
    (oks if re.search(r'r\$ ?\d+.{0,40}campanha', txt) else falhas).append(
        'orçamento por campanha escrito' if re.search(r'r\$ ?\d+.{0,40}campanha', txt)
        else 'orçamento por campanha não escrito (regra: <R$47 = 60-65% do ticket médio; >=R$47 = R$30-35)')
    (oks if '4:5' in txt else falhas).append('feed 4:5' if '4:5' in txt else 'formato 4:5 do feed não citado')

    # 8 · base de vídeo: gravação de tela OU páginas reais (receita E.0d, sem tela)
    if any('video' in l for l in todas):
        mat = of / 'criativos/MATERIAL-ENTREGAVEL'
        tem = mat.exists() and any(p.suffix.lower() in ('.mp4', '.mov', '.webm', '.mkv') for p in mat.rglob('*'))
        paginas = of / 'site/painel/conteudo'
        n_pag = sum(1 for p in paginas.rglob('*.webp')) if paginas.exists() else 0
        if tem:
            oks.append('gravação de tela do entregável existe')
        elif n_pag >= 20:
            oks.append(f'vídeo sem tela: {n_pag} páginas reais em site/painel/conteudo (receita E.0d)')
        else:
            falhas.append('sem base de vídeo: nem gravação em criativos/MATERIAL-ENTREGAVEL/ '
                          'nem >=20 páginas reais em site/painel/conteudo/')

    # 10 · preço do criativo = plano mais barato
    def valores(t):
        return [float(x.replace('.', '').replace(',', '.')) for x in re.findall(r'(?:ars|r\$|us\$|usd|eur|€|\$|mxn|cop|clp)\s*([\d.]+(?:,\d{1,2})?)', t)]
    vend = re.search(r'^##+ [^\n]*o que vendemos(.*?)(?=^## |\Z)', ptxt, re.M | re.S)
    planos = []
    for l in (vend.group(1).splitlines() if vend else []):
        if l.lstrip().startswith('- ') and not re.search(r'popup|saida|exit|bump|upsell|downsell|combo|upgrade', l):
            planos += valores(l)[:1]
    menor = min(planos) if planos else None
    lp = re.search(r'\*\*preco no criativo:\*\*([^\n]+)', txt)
    if not lp:
        falhas.append('plano sem linha "**Preço no criativo:**" (sempre o plano mais barato'
                      + (f': {menor:,.0f}'.replace(',', '.') if menor else '') + ')')
    else:
        v = valores(lp.group(1))
        if menor and v and v[0] != menor:
            falhas.append(f'preço no criativo {v[0]:,.0f} ≠ plano mais barato {menor:,.0f}'.replace(',', '.'))
        else:
            oks.append('preço no criativo = plano mais barato')
    for l in todas:
        for v in valores(l):
            if menor and v != menor:
                falhas.append(f'peça com preço {v:,.0f} ≠ plano mais barato: {l[:70]}'.replace(',', '.'))

    # 12 · digital + impresso
    di = re.search(r'impress', txt) and re.search(r'celular|tablet|notebook', txt)
    (oks if di else falhas).append('regra digital + impresso escrita' if di
        else 'plano sem a regra: toda imagem com material = 1+ aparelho E folhas impressas (página diferente em cada)')

    # 13 · TRILHAS da leva — UGC e só-texto são obrigatórios (Rodrigo 21/10, cobrado pela dona 25/10)
    if len(todas) >= 5:
        ugc = [l for l in todas if 'ugc' in n(l)]
        stx = [l for l in todas if re.search(r'so[- ]?texto', n(l))]
        sem_ugc = re.search(r'sem ugc[^\n]*dona', txt)  # decisão da dona escrita no plano/STATUS (ex.: NeuroActiva 25/10)
        if not ugc and sem_ugc:
            avisos.append('leva sem UGC por decisão da dona escrita no plano — conferir que ainda vale')
        elif not ugc:
            falhas.append('leva sem peça UGC — trilha UGC é obrigatória (pessoa com o material na mão, 1 a cada 9)')
        elif not any(re.search(r'na mao|material|pasta|folha|ficha', n(l)) for l in ugc):
            falhas.append('peça UGC sem o material na mão (regra 25/10: pessoa vazia/mão nua = reprovado)')
        else:
            oks.append(f'trilha UGC presente ({len(ugc)} peça[s] com material)')
        if not stx:
            falhas.append('leva sem peça SÓ TEXTO (frase de impacto sem produto, 1 a cada 9) — método Rodrigo')
        else:
            oks.append(f'peça só-texto presente ({len(stx)})')
        if not re.search(r'papel|consciencia', txt):
            avisos.append('plano sem o papel de consciência de cada peça (apresentação/mecanismo, dor, objeção, prova real, oferta/preço, demonstração) — Kevones 23/10/2026')
        if 'mecanismo' not in txt:
            avisos.append('plano não diz que o corpo do vídeo desenvolve o mecanismo (gancho -> mecanismo -> CTA)')

    # 14 · COPY NASCE DA OFERTA E DA PESQUISA (dona, 29/10/2026 — caso GeriNeuro: método todo escrito no
    #      Gate 0.2 + RECEITA §3, agente pulou banco/roteiros/YouTube e a copy saiu genérica; nada travava).
    #      Cobra os ARQUIVOS que a receita já manda fazer, não regra nova.
    pq = of / 'pesquisa'
    pastas = [plano.parent, of / 'criativos']

    def acha(pad):
        return sorted({p for d in pastas if d.exists() for p in d.glob(pad)})

    tb = re.search(r'^##+ [^\n]*termos obrigat[oó]rios do criativo(.*?)(?=^## |\Z)', ptxt, re.M | re.S)
    tm = re.search(r'^`([^`]+)`\s*$', tb.group(1), re.M) if tb else None
    termos_ob = [t.strip() for t in tm.group(1).split(',') if t.strip()] if tm else []

    anun = sorted(pq.glob('ANUNCIANTES-*.md'))
    atxt = n(' '.join(p.read_text(errors='ignore') for p in anun))
    if not anun:
        falhas.append('pesquisa/ANUNCIANTES-<data>.md ausente — Gate 0.2 Passo B/C (anunciantes dissecados, TODOS os ativos de cada um)')
    elif not re.search(r'mandado pela dona|achado pelo agente', atxt):
        falhas.append('ANUNCIANTES sem seção "Mandado pela dona" (links crus) nem "achado pelo agente"')
    else:
        oks.append(f'anunciantes dissecados ({anun[-1].name})')
    # tudo que a dona mandou (pesquisa/da-dona/) tem que estar no ANUNCIANTES
    dd = pq / 'da-dona'
    if dd.exists():
        ids = set()
        for p in dd.rglob('*'):
            if p.is_file() and p.suffix.lower() in ('.md', '.txt'):
                ids |= set(re.findall(r'(?:view_all_page_id|[?&]id)=(\d{6,})', p.read_text(errors='ignore')))
        faltam = sorted(i for i in ids if i not in atxt)
        (falhas if faltam else oks).append(
            f'material da dona sem uso: {len(faltam)} link(s) de pesquisa/da-dona/ fora do ANUNCIANTES ({", ".join(faltam[:4])})'
            if faltam else f'todos os {len(ids)} link(s) de pesquisa/da-dona/ estão no ANUNCIANTES')

    dem = sorted(pq.glob('DEMANDA-ORGANICA-*.md'))
    dtxt = n(dem[-1].read_text(errors='ignore')) if dem else ''
    if not dem:
        falhas.append('pesquisa/DEMANDA-ORGANICA-<data>.md ausente — Gate 0.2 Passo D (YouTube top vídeos + comentários, TikTok, Trends)')
    elif not ('youtube' in dtxt and 'coment' in dtxt):
        falhas.append(f'{dem[-1].name} sem YouTube + comentários lidos (Passo D)')
    else:
        oks.append(f'demanda orgânica medida ({dem[-1].name})')

    est = acha('ESTUDO-LEVA-*.md')
    if not est:
        falhas.append('criativos/ESTUDO-LEVA-N.md ausente — raciocínio da leva em 7 passos (oferta → Biblioteca → orgânico → '
                      'virar o lead → alavancas → ângulos → roteiros), molde LOW-TICKET/MODELOS/_MODELO-ESTUDO-LEVA.md')
    else:
        eraw = est[-1].read_text(errors='ignore')
        et = n(eraw)
        passos = {'1 oferta': r'1\W*a oferta', '2 biblioteca': r'2\W*biblioteca', '3 organico': r'3\W*organico',
                  '4 virar o lead': r'4\W*virar o lead', '5 alavancas': r'5\W*alavancas', '6 angulos': r'6\W*transforma',
                  '7 roteiros': r'7\W*roteiros'}
        # conteúdo = linhas que NÃO vieram do molde (instrução do molde não conta como trabalho feito)
        molde = of.parents[1] / 'MODELOS/_MODELO-ESTUDO-LEVA.md'
        do_molde = {l.strip() for l in n(molde.read_text(errors='ignore')).splitlines()} if molde.exists() else set()
        vazios = []
        for k, rx in passos.items():
            m = re.search(rf'^## +{rx}[^\n]*\n(.*?)(?=^## |\Z)', et, re.M | re.S)
            novas = [l for l in (m.group(1).splitlines() if m else []) if l.strip() and l.strip() not in do_molde]
            if not m or len(re.sub(r'\s|\|', '', ''.join(novas))) < 120:
                vazios.append(k)
        (falhas if vazios else oks).append(
            f'{est[-1].name}: passo(s) vazio(s) ou ausente(s): {", ".join(vazios)}' if vazios
            else f'{est[-1].name}: 7 passos preenchidos')
        sec1 = re.search(r'^## +1\W*a oferta(.*?)(?=^## |\Z)', et, re.M | re.S)
        if termos_ob and sec1 and not any(n(t) in sec1.group(1) for t in termos_ob):
            falhas.append('passo 1 não cita nenhum termo obrigatório do produto — a oferta não foi lida')
        r7 = re.search(r'^## +7\W*roteiros(.*)', et, re.M | re.S)
        pecas = re.split(r'^### ', r7.group(1), flags=re.M)[1:] if r7 else []
        if len(pecas) < len(todas):
            falhas.append(f'passo 7: {len(pecas)} roteiro(s) escritos × {len(todas)} peças no plano')
        campos = {'gancho': r'gancho', 'mecanismo': r'mecanismo', 'cta': r'cta', 'na imagem/cena': r'na imagem',
                  'titulo': r'titulo', 'texto principal': r'texto principal', 'fonte': r'fonte', 'pt': r'pt'}
        for pc in pecas:
            nome = pc.splitlines()[0][:40]
            faltam = [k for k, rx in campos.items() if not re.search(rf'^\s*[-*]\s*\*\*{rx}[^*]*:\*\*\s*\S', pc, re.M)]
            if faltam:
                falhas.append(f'roteiro "{nome}": falta/vazio {", ".join(faltam)}')
            if termos_ob and not any(n(t) in pc for t in termos_ob):
                falhas.append(f'roteiro "{nome}": nenhum termo obrigatório do produto — copy genérica')
            if not re.search(r'passo [1-6]', pc):
                falhas.append(f'roteiro "{nome}": fonte não aponta pra um passo do estudo (1-6)')
        if pecas and not [f for f in falhas if 'roteiro "' in f]:
            oks.append(f'{len(pecas)} roteiros completos, com termo do produto e fonte no estudo')
        rev = re.search(r'- \[x\] \**revisor', et)
        (oks if rev else (falhas if producao else avisos)).append(
            'revisor de copy aprovou (pane limpo)' if rev else
            'estudo sem "- [x] Revisor" — rodar o revisor em pane limpo (criativo-ads/references/REVISOR-COPY.md) antes de produzir')

    # aprovação
    aprovado = re.search(r'- \[x\] \**ok da dona', txt)
    if aprovado:
        oks.append('OK da dona marcado')
    else:
        (falhas if producao else avisos).append('plano sem "- [x] OK da dona" — mostrar pra dona, NÃO produzir')

    for x in oks:
        print('OK    ', x)
    for x in avisos:
        print('AVISO ', x)
    for x in falhas:
        print('FALHA ', x)
    print('\n' + ('BLOQUEADO — corrigir o plano' if falhas else ('LIBERADO pra produzir' if aprovado else 'PLANO OK — falta o OK da dona')))
    sys.exit(1 if falhas else 0)


if __name__ == '__main__':
    main()
