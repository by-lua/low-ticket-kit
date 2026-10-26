#!/usr/bin/env python3
"""abrir.py — abertura MECÂNICA de sessão no portfólio LOW-TICKET (padrão MazyOS /abrir).

O MazyOS nunca se desvia porque a memória dele cabe inteira no contexto. A nossa não cabe
(CLAUDE.md 25 KB, _memoria 225 KB, STATUS de oferta até 265 KB) — agente que "lê tudo" passa o
olho e pula. Este script faz a leitura no lugar dele: imprime o RECORTE certo (negócio + oferta +
tipo de tarefa), roda os gates, lista as skills obrigatórias e termina com o RECIBO que o agente
tem que devolver antes de agir.

Uso:
  python3 abrir.py                         # só o estado do negócio ("onde paramos")
  python3 abrir.py "<oferta>"              # estado da oferta (aceita apelido: "tarot ar")
  python3 abrir.py "<oferta>" "<tarefa>"   # + rota da tarefa (skills, gates, regras da dona)
  python3 abrir.py --ofertas               # lista slugs + nome

Fonte das skills por tarefa = tabela "Skills obrigatórias por tarefa" do CLAUDE.md da raiz
(lida ao vivo — editar lá, não aqui). Aqui só mora: palavra-chave → linha da tabela + arquivos
extras e gates por tipo.
"""
import re
import subprocess
import sys
import unicodedata
from datetime import date, datetime
from pathlib import Path

RAIZ_PADRAO = Path('~/Documentos/TRAMPO/PROJETOS/WORKING/PROJETOS - INTERNOS/LOW-TICKET')
SKILLS = Path.home() / '.claude/skills'
AUTO_MEMORIA = Path.home() / ('.claude/projects/-home-lua-Documentos-TRAMPO-PROJETOS-WORKING-'
                              'PROJETOS---INTERNOS-LOW-TICKET/memory')
LIMITE_INTEIRO = 12_000  # arquivo até isso sai inteiro; acima, só o recorte

# tipo: (palavras da tarefa, regex da 1ª coluna da tabela do CLAUDE.md, palavras p/ filtrar regras da dona)
TIPOS = {
    'criativo': (r'criativ|anunci|\bads?\b|carross|estatic|video|\bleva\b|hook|gancho|\bpeca|story|reels?|vsl',
                 r'criativo de an', r'criativ|carross|estatic|v[ií]deo|gancho|leva|persona'),
    'pagina': (r'pagina|landing|\bsite\b|headline|popup|copy da pag',
               r'p[aá]gina de vendas', r'p[aá]gina|headline|popup|identifica|favicon|pixel|evento'),
    'entrega': (r'entreg|modulo|area de membros|painel|\bpdf\b|o que falta|bonus|ebook',
                r'retomar entrega|produto / entreg', r'entreg|m[oó]dulo|[aá]rea de membros|pdf|b[oô]nus|painel|AGM'),
    'checkout': (r'checkout|wiven|mundpay|cooud|zenith|hotmart|\bgg\b|webhook|gateway',
                 r'^checkout', r'checkout|webhook|wiven|mundpay|cooud|gateway|banner|reembolso'),
    'funil': (r'\bbump|upsell|downsell|combo|upgrade|funil',
              r'bump, upsell', r'bump|upsell|downsell|combo|upgrade|pre[cç]o|webhook'),
    'trafego': (r'trafego|campanha|kevones|bidcap|verba|orcamento|\bcpa\b|escala',
                r'^tr[aá]fego', r'tr[aá]fego|campanha|or[cç]amento|cpa|kevones|bidcap'),
    'pixel': (r'pixel|evento|trackeador|\bcapi\b|initiatecheckout',
              r'pixel, eventos', r'pixel|evento|trackeador|webhook'),
    'mineracao': (r'minera|oferta nova|modelar|concep|biblioteca',
                  r'oferta nova, minerar', r'minera|biblioteca|persona|demanda|recorte'),
    'traducao': (r'tradu|outro mercado|cross|idioma|espanhol|portugal',
                 r'traduzir/adaptar|levar oferta', r'tradu|idioma|acento|mercado'),
    'stories': (r'stories diari|postiz', r'stories di[aá]rios', r'stories'),
}

# arquivos e gates extras por tipo ({o} = pasta da oferta)
EXTRAS = {
    'criativo': {
        'ler': ['{o}/pesquisa/PERSONA-E-ANGULOS.md', '{o}/produto/MANIFESTO-ENTREGAVEIS.md',
                '{o}/criativos/PLANO-LEVA-*.md', '{o}/trafego/ANALISES.md#ultima',
                '_memoria/planos-criativos.md#oferta', 'CRIATIVOS.md#oferta'],
        'gates': ['python3 ~/.claude/skills/criacao-low-ticket-mvt/scripts/gate-persona.py {o}',
                  # plano da leva só trava quando a tarefa é planejar/produzir leva; em correção de peça vira aviso
                  ('python3 ~/.claude/skills/criativo-ads/scripts/gate-plano-leva.py {o}', r'leva|plano|nova|novos|novas')],
        'depois': ['LER ANTES DE PRODUZIR — trilha: `criativo-ads` seção "TRILHA DO CRIATIVO" (Kevones → Rodrigo → roteiro → imagem/vídeo)',
                   'imagem: ~/.claude/skills/criativo-ads/references/tipos-de-imagem.md (GUIA DE IMAGEM) inteiro',
                   'vídeo: ~/.claude/skills/criativo-ads-video-orq/references/estilos-de-video.md (modo) + EDICAO-PADRAO.md (edição, igual em todo modo) inteiros',
                   'python3 ~/.claude/skills/criativo-ads/scripts/gate-pecas-criativo.py <CRIATIVO-N>  (cada peça)',
                   'python3 ~/.claude/skills/criativo-ads/scripts/gate-imagens-finais.py <finais> --pasta <CRIATIVO-N>  (imagem)',
                   'ABRIR 1 imagem de cada peça e conferir o texto escrito na foto antes de dizer "pronto"'],
    },
    'pagina': {
        'ler': ['{o}/pesquisa/PERSONA-E-ANGULOS.md', '{o}/DESIGN-SYSTEM.md', '_memoria/pixel-eventos-checklist.md'],
        'gates': ['python3 ~/.claude/skills/criacao-low-ticket-mvt/scripts/gate-persona.py {o}'],
        'depois': ['Gate de eventos no ar (PageView, quiz, IC em todo botão) — prova = request facebook.com/tr',
                   'Trocar página principal = `adstrackeador pagina comparar <atual> <nova>` antes de publicar'],
    },
    'entrega': {
        'ler': ['{o}/produto/MANIFESTO-ENTREGAVEIS.md', '{o}/produto/ENTREGAVEIS.yaml#resumo'],
        'gates': ['python3 ~/.claude/skills/auditar-entregaveis-oferta/scripts/audita.py {o} --retomar'],
        'depois': ['Texto da entrega = composição: ficha com exercício/pôster/folha de imprimir já escreve a página w '
                   '(conteúdo exato + composição + gabarito) — PAGINAS-DE-ATIVIDADE.md; toda página é imagem GPT, nunca HTML/Pillow',
                   'node scripts/check-download-pdf.mjs <url> <email-teste>  (no ar, depois do deploy)',
                   'audita.py {o} --registrar'],
    },
    'checkout': {
        'ler': ['_memoria/contas-e-codigos.md#oferta'],
        'gates': [],
        'depois': ['Preço do checkout = botão da página; banner ≤400 KB; produto nos DOIS webhooks + mapa do servidor',
                   'Registrar conta/código em _memoria/contas-e-codigos.md no mesmo dia'],
    },
    'funil': {
        'ler': ['{o}/pesquisa/PERSONA-E-ANGULOS.md', '_memoria/contas-e-codigos.md#oferta'],
        'gates': ['python3 ~/.claude/skills/criacao-low-ticket-mvt/scripts/gate-persona.py {o}'],
        'depois': ['Produto novo nos DOIS webhooks + OFFERS/COMPLETO_OFFERS do servidor'],
    },
    'trafego': {
        'ler': ['{o}/trafego/ANALISES.md#ultima', 'KEVONES/README.md'],
        'gates': [],
        'depois': ['Nova entrada datada em {o}/trafego/ANALISES.md (mais nova em cima)'],
    },
    'pixel': {'ler': ['_memoria/pixel-eventos-checklist.md'], 'gates': [], 'depois': []},
    'mineracao': {'ler': ['{o}/pesquisa/PERSONA-E-ANGULOS.md'], 'gates': [], 'depois': []},
    'traducao': {'ler': ['{o}/DESIGN-SYSTEM.md'], 'gates': [], 'depois': []},
    'stories': {'ler': ['_memoria/stories-diarias.md'], 'gates': [], 'depois': []},
}


def norm(s):
    s = unicodedata.normalize('NFKD', s.lower())
    return ''.join(c for c in s if not unicodedata.combining(c))


def achar_raiz():
    p = Path.cwd()
    for d in [p, *p.parents]:
        if (d / 'OFERTAS').is_dir() and (d / '_memoria').is_dir():
            return d
    return RAIZ_PADRAO


def ler(p):
    try:
        return p.read_text(errors='ignore')
    except OSError:
        return None


def titulo(txt):
    print(f'\n{"=" * 78}\n## {txt}\n{"=" * 78}')


def mostrar(rotulo, txt):
    print(f'\n--- {rotulo} ---\n{txt.rstrip()}')


def secoes(txt, nivel=r'#{2,3}'):
    """Divide markdown em (titulo, corpo) por cabeçalho ## / ###."""
    partes, atual, corpo = [], None, []
    for linha in txt.splitlines():
        if re.match(rf'^{nivel} ', linha):
            if atual is not None:
                partes.append((atual, '\n'.join(corpo)))
            atual, corpo = linha, [linha]
        elif atual is not None:
            corpo.append(linha)
    if atual is not None:
        partes.append((atual, '\n'.join(corpo)))
    return partes


def ofertas(raiz):
    out = []
    for d in sorted((raiz / 'OFERTAS').iterdir()):
        if not d.is_dir() or d.name.startswith(('_', '.')):
            continue
        st = ler(d / 'STATUS.md') or ''
        nome = re.sub(r'^#\s*STATUS\s*[:—-]?\s*', '', st.splitlines()[0]) if st else '(sem STATUS.md)'
        out.append((d.name, nome.strip()))
    return out


def achar_oferta(raiz, consulta):
    toks = norm(consulta).replace('-', ' ').split()
    achou = []
    for slug, nome in ofertas(raiz):
        partes = set(re.split(r'[-\s]+', norm(slug))) | set(re.split(r'[\W_]+', norm(nome)))
        partes.discard('')

        def bate(t):
            return t in partes or (len(t) >= 3 and any(t in p for p in partes))
        if norm(consulta) == norm(slug) or all(bate(t) for t in toks):
            achou.append((slug, nome))
    return achou


def nomes_busca(slug, nome):
    """Palavras que identificam a oferta nos arquivos centrais (planos-criativos, CRIATIVOS, contas)."""
    base = re.sub(r'\(.*?\)', '', nome)
    ts = [t for t in re.split(r'[\W_]+', base) if len(t) >= 3 and norm(t) not in
          {'status', 'mapa', 'mapas', 'del', 'dos', 'das', 'luciola', 'venda', 'real', 'sem'}]
    extra = [t for t in re.split(r'[-]+', slug) if len(t) == 2]  # sufixo de mercado: ar, us, pt
    return ts, extra


def recorte_oferta(txt, slug, nome):
    ts, mercado = nomes_busca(slug, nome)
    if not ts:
        return []
    out = []
    for cab, corpo in secoes(txt):
        c = norm(cab)
        if all(norm(t) in c for t in ts[:2]) and all(re.search(rf'\b{m}\b', c) for m in mercado):
            out.append(corpo)
    return out


def ultima_entrada(txt):
    s = secoes(txt, r'#{2}')
    return s[0][1] if s else txt[:3000]


def corta(linha, n=500):
    return linha if len(linha) <= n else linha[:n] + ' […]'


def status_oferta(txt):
    if len(txt) <= LIMITE_INTEIRO:
        return txt
    linhas = txt.splitlines()
    topo = txt[:8000].rsplit('\n', 1)[0]
    resto = txt[len(topo):].splitlines()
    pend = [corta(l) for l in resto if re.match(r'\s*- \[ \]', l)][:30]
    return topo + ('\n\n[...corte — pendências abertas do resto do arquivo:]\n' + '\n'.join(pend) if pend else
                   f'\n\n[...arquivo tem {len(linhas)} linhas; resto é histórico antigo]')


def tabela_skills(claude_md):
    """Linhas da tabela 'Skills obrigatórias por tarefa' → [(coluna1, [skills])]."""
    m = re.search(r'## Skills obrigat[oó]rias por tarefa(.*?)\n## ', claude_md, re.S)
    if not m:
        return []
    rows = []
    for l in m.group(1).splitlines():
        if not l.startswith('|') or '---' in l or 'Vai fazer' in l:
            continue
        cols = [c.strip() for c in l.strip('|').split('|')]
        if len(cols) >= 2:
            rows.append((cols[0], re.findall(r'`([a-z0-9:_-]+)`', ' '.join(cols[1:]))))
    return rows


def skill_existe(s):
    if ':' in s:  # skill de plugin
        plug, nome = s.split(':', 1)
        return any(Path.home().glob(f'.claude/plugins/**/{plug}*/**/skills/{nome}/SKILL.md'))
    return (SKILLS / s / 'SKILL.md').exists()


def rodar(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120, cwd=RAIZ)
        out = (r.stdout + r.stderr).strip().splitlines()
        veredito = next((l for l in reversed(out) if l.strip()), '(sem saída)')
        falhas = [l for l in out if l.startswith(('FALHA', 'FALTA', '⛔'))][:8]
        return veredito, falhas
    except Exception as e:  # gate quebrado não pode sumir em silêncio
        return f'ERRO ao rodar: {e}', []


def idade(txt):
    m = re.search(r'Atualizado em:?\**\s*(\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})', txt or '')
    if not m:
        return None
    v = m.group(1)
    d = datetime.strptime(v, '%Y-%m-%d' if '-' in v else '%d/%m/%Y').date()
    return (date.today() - d).days


# Regra 26/10/2026: ficha que pede material tem a página "w" escrita NO TEXTO e gerada no GPT (nunca código).
MARCA_W = re.compile(r'worksheet|printable|imprim|hoja para|folha para|sopa de letras|ca[cç]a.?palavra|'
                     r'word search|laberint|labirint|\bmaze\b|recortar|\bcut.?out|tabuleiro|tablero|'
                     r'p[oó]ster|cartel|ligar.?colunas|spot the difference', re.I)
SPEC_W = re.compile(r'\b\d{1,3}w\b|p[aá]gina\s*w\b|folha\s*w\b|hoja\s*w\b', re.I)
GERADORES_CODIGO = ('gera-worksheet.py', 'gera-atividades.py', 'gera-printables.py')


def checa_folhas_w(od):
    """Sugestões de alteração p/ oferta existente: folha w faltando no texto ou feita por código."""
    sug = []
    textos = [p for pat in ('produto/texto*/**/*.md', 'produto/TEXTO*/**/*.md') for p in od.glob(pat)]
    sem_spec, total = [], 0
    for p in textos:
        txt = ler(p) or ''
        blocos = re.split(r'(?m)^(?=#{2,4} )', txt)
        faltam = [b.splitlines()[0].lstrip('# ').strip()[:60] for b in blocos
                  if re.match(r'#{2,4} ', b) and MARCA_W.search(b) and not SPEC_W.search(b)]
        total += len(faltam)
        if faltam:
            sem_spec.append(f'{p.relative_to(od)} ({len(faltam)}: {"; ".join(faltam[:2])}…)')
    if total:
        sug.append(f'{total} ficha(s) pedem material imprimível e o TEXTO não traz a página w '
                   f'(conteúdo exato + composição + gabarito) → escrever antes de gerar: '
                   + ' | '.join(sem_spec[:4]))
    w_painel = len(list(od.glob('site/painel/conteudo/**/pagina-*w.webp')))
    cod = [g for g in GERADORES_CODIGO if (od / 'scripts' / g).exists()]
    if w_painel and (cod or (od / 'produto/ATIVIDADES.json').exists()):
        sug.append(f'{w_painel} página(s) w no painel e a oferta tem gerador por código '
                   f'({", ".join(cod) or "ATIVIDADES.json"}) → provavelmente feitas em Pillow/HTML; '
                   f'conferir contact sheet e regerar no GPT 1 por mensagem (scripts obsoletos, não rodar)')
    return sug


def main(argv):
    global RAIZ
    RAIZ = achar_raiz()
    avisos = []

    if argv and argv[0] == '--ofertas':
        for slug, nome in ofertas(RAIZ):
            print(f'{slug:32} {nome}')
        return 0

    consulta = argv[0] if argv else ''
    tarefa = ' '.join(argv[1:]) if len(argv) > 1 else ''
    claude_md = ler(RAIZ / 'CLAUDE.md') or ''

    # ---------- 1. NEGÓCIO ----------
    titulo('1. NEGÓCIO — foco e empresa (sempre)')
    for f in ['_memoria/estrategia.md', '_memoria/empresa.md']:
        t = ler(RAIZ / f)
        mostrar(f, t) if t else avisos.append(f'falta {f}')

    oferta = None
    if consulta:
        achou = achar_oferta(RAIZ, consulta)
        if len(achou) != 1:
            print(f'\n⛔ OFERTA "{consulta}" ' + ('não encontrada.' if not achou else 'é ambígua:'))
            for slug, nome in (achou or ofertas(RAIZ)):
                print(f'   {slug:32} {nome}')
            print('\nRepita com o slug exato. NÃO comece a tarefa sem a oferta certa.')
            return 2
        oferta = achou[0]

    if not oferta:
        titulo('2. PAINEL — PANORAMA (topo)')
        pan = ler(RAIZ / 'PANORAMA.md') or ''
        mostrar('PANORAMA.md', '\n'.join(pan.splitlines()[:120]))
        titulo('OFERTAS')
        for slug, nome in ofertas(RAIZ):
            print(f'   {slug:32} {nome}')
        print('\nPróximo: `abrir.py "<oferta>" "<tarefa>"` antes de mexer em qualquer oferta.')
        return 0

    slug, nome = oferta
    od = RAIZ / 'OFERTAS' / slug
    o_rel = f'OFERTAS/{slug}'

    # ---------- 2. OFERTA ----------
    titulo(f'2. OFERTA — {nome}  ({o_rel})')
    cl = ler(od / 'CLAUDE.md')
    if cl:
        mostrar(f'{o_rel}/CLAUDE.md (regras SÓ desta oferta)', cl)
    else:
        avisos.append(f'{o_rel}/CLAUDE.md NÃO EXISTE — oferta sem "Memória da oferta"; criar pelo '
                      f'`organizar-projeto` antes de fechar a sessão')
    st = ler(od / 'STATUS.md')
    if st:
        mostrar(f'{o_rel}/STATUS.md (fonte da verdade da oferta)', status_oferta(st))
        dias = idade(st)
        if dias is not None and dias > 3:
            avisos.append(f'STATUS da oferta atualizado há {dias} dias — conferir se ainda vale')
    else:
        avisos.append(f'{o_rel}/STATUS.md NÃO EXISTE')
    linha_raiz = [l for l in (ler(RAIZ / 'STATUS.md') or '').splitlines() if slug in l or
                  (nome.split('(')[0].strip() and nome.split('(')[0].strip() in l)][:4]
    if linha_raiz:
        mostrar('STATUS.md da raiz — linha da oferta', '\n'.join(corta(l, 800) for l in linha_raiz))
    if (od / 'DESIGN-SYSTEM.md').exists():
        print(f'\n(design: {o_rel}/DESIGN-SYSTEM.md — ler antes de gerar qualquer visual)')

    sug_w = checa_folhas_w(od)
    if sug_w:
        titulo('SUGESTÃO DE ALTERAÇÃO — exercício/pôster sem folha w no texto ou feito por código')
        print('Regra: criacao-low-ticket-mvt/references/PAGINAS-DE-ATIVIDADE.md (texto traz as 2 páginas; '
              'tudo imagem GPT). Oferecer à dona no RECIBO, não corrigir sem OK.')
        for s in sug_w:
            print(f'   - {s}')
        avisos += [f'SUGESTÃO: {s}' for s in sug_w]

    # ---------- 3. ROTA DA TAREFA ----------
    tipos = [t for t, (kw, _, _) in TIPOS.items() if tarefa and re.search(kw, norm(tarefa))]
    if not tarefa:
        print('\nSem tarefa: devolver "onde paramos" desta oferta (fase + maior pendência) e perguntar o que fazer.')
    elif not tipos:
        avisos.append(f'tarefa "{tarefa}" não casou com nenhum tipo — conferir a tabela de skills do '
                      f'CLAUDE.md da raiz na mão')

    skills, regras_kw = ['low-ticket-painel'], []
    tabela = tabela_skills(claude_md)
    for t in tipos:
        _, linha_re, regkw = TIPOS[t]
        for col1, sk in tabela:
            if re.search(linha_re, norm(col1)):
                skills += sk
        skills += EXTRAS.get(t, {}).get('skills_extra', [])
        regras_kw.append(regkw)
    PLUGIN = {'get-brolls': 'get-brolls:get-brolls'}  # skill de plugin: ID com prefixo
    skills = list(dict.fromkeys(PLUGIN.get(x, x) for x in skills))

    if tipos:
        titulo(f'3. TAREFA — "{tarefa}"  →  tipo: {", ".join(tipos)}')
        for t in tipos:
            for alvo in EXTRAS.get(t, {}).get('ler', []):
                caminho, _, modo = alvo.format(o=o_rel).partition('#')
                for p in sorted(RAIZ.glob(caminho)) if '*' in caminho else [RAIZ / caminho]:
                    txt = ler(p)
                    rel = p.relative_to(RAIZ)
                    if txt is None:
                        avisos.append(f'{rel} não existe (pedido pelo tipo "{t}")')
                        continue
                    if modo == 'ultima':
                        mostrar(f'{rel} — ÚLTIMA entrada (dizer o que ela muda)', ultima_entrada(txt))
                    elif modo == 'oferta':
                        rec = recorte_oferta(txt, slug, nome)
                        if rec:
                            mostrar(f'{rel} — seções desta oferta', '\n\n'.join(rec)[:LIMITE_INTEIRO])
                        else:
                            ts, mercado = nomes_busca(slug, nome)
                            hits = [l for l in txt.splitlines() if ts and all(norm(x) in norm(l) for x in ts[:2])
                                    and all(re.search(rf'\b{m}\b', norm(l)) for m in mercado)][:12]
                            mostrar(f'{rel} — linhas que citam a oferta',
                                    '\n'.join(hits) if hits else '(nada sobre esta oferta)')
                    elif modo == 'resumo':
                        mostrar(f'{rel} — topo', '\n'.join(txt.splitlines()[:40]))
                    elif len(txt) <= LIMITE_INTEIRO:
                        mostrar(str(rel), txt)
                    else:
                        mostrar(f'{rel} (grande — topo; ler o resto com Read)', txt[:9000].rsplit('\n', 1)[0])

        # regras da dona filtradas pelo tipo
        titulo('4. REGRAS DA DONA que valem pra esta tarefa (_memoria/preferencias.md)')
        pref = ler(RAIZ / '_memoria/preferencias.md') or ''
        rx = re.compile('|'.join(regras_kw), re.I)
        achadas = [(c, b) for c, b in secoes(pref, r'#{2}') if rx.search(c)]
        usado = 0
        for cab, corpo in achadas:
            if usado + len(corpo) > 16_000:
                print(f'   (também vale, ler com Read) {cab}')
                continue
            mostrar(cab.lstrip('# '), corpo)
            usado += len(corpo)
        if not achadas:
            print('(nenhuma seção específica — vale o geral do CLAUDE.md)')

        # auto-memória (feedback acumulado em sessões)
        idx = ler(AUTO_MEMORIA / 'MEMORY.md') or ''
        rx_tarefa = re.compile('|'.join(TIPOS[t][0] for t in tipos))
        hits = [l for l in idx.splitlines() if l.startswith('- [') and rx_tarefa.search(norm(l))]
        if hits:
            titulo(f'5. MEMÓRIA DE SESSÕES (abrir com Read os que tocam a tarefa) — {AUTO_MEMORIA}')
            print('\n'.join(hits[:25]))

        # gates
        titulo('6. GATES — rodados agora')
        for t in tipos:
            for g in EXTRAS.get(t, {}).get('gates', []):
                g, trava_se = (g if isinstance(g, tuple) else (g, None))
                cmd = g.format(o=f'"{o_rel}"')
                veredito, falhas = rodar(cmd)
                print(f'\n$ {cmd}\n→ {veredito}')
                for f in falhas:
                    print(f'   {f}')
                if 'BLOQUEADO' in veredito.upper():
                    if trava_se and not re.search(trava_se, norm(tarefa)):
                        avisos.append(f'plano com pendência ({cmd}) — não trava correção de peça, mas avisar a dona')
                    else:
                        avisos.append(f'GATE BLOQUEADO: {cmd} — não começa a tarefa')
        depois = [d.format(o=o_rel) for t in tipos for d in EXTRAS.get(t, {}).get('depois', [])]
        if depois:
            print('\nAntes de dizer "pronto":')
            for d in dict.fromkeys(depois):
                print(f'   - {d}')

    # ---------- skills ----------
    titulo('SKILLS OBRIGATÓRIAS — carregar TODAS agora (Skill tool), antes de qualquer arquivo/ação')
    for s in skills:
        print(f'   {"✓" if skill_existe(s) else "?"} {s}')
    if any(not skill_existe(s) for s in skills):
        print('   (? = não achei a pasta; invocar pelo ID mesmo assim — lista do pane pode estar velha)')

    # ---------- avisos ----------
    if avisos:
        titulo('⚠ AVISOS')
        for a in avisos:
            print(f'   - {a}')

    # ---------- recibo ----------
    titulo('RECIBO — o agente responde ISTO à dona antes de agir (sem ele, não começa)')
    print(f'''ABERTURA · {nome} ({slug})
Fase / onde paramos: <1 linha do STATUS da oferta>
Tarefa: {tarefa or '<nenhuma ainda>'}  → tipo: {", ".join(tipos) or '-'}
O que vendemos / o que NÃO é: <do PERSONA-E-ANGULOS ou CLAUDE da oferta>
Regras da dona que valem aqui (3-5, com arquivo de origem): <...>
Última análise de tráfego diz: <ou "sem análise">
Gates: <veredito de cada um>
Skills carregadas: {", ".join(skills)}
Avisos: {len(avisos)}
Próximo passo: <1 linha>''')
    print('\nAO TERMINAR: skill `low-ticket-salvar` (STATUS da oferta + linha na raiz + regra nova na '
          'memória certa). Correção da dona no meio → perguntar "quer que eu salve isso?".')
    return 1 if any('BLOQUEADO' in a for a in avisos) else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
