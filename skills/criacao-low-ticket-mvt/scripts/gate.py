#!/usr/bin/env python3
"""gate.py — verificação MECÂNICA de passagem entre passos do método MVT.

Uso:
  gate.py --rodada <pasta da rodada> --passo T7 [--concepcao <id> | --oferta <slug>]
  gate.py --rodada <pasta da rodada> --ate T12

Lê references/TRILHA-CHECKLIST.yaml (lista de itens + evidência), o ESTADO.md da rodada (bloco
ROTEADOR decide as condições), os arquivos da rodada / OFERTAS/<slug>/ e o Hub decifrado
(HUB-OFERTAS/ofertas.json; se não estiver, rode `uv run cifrar.py --verificar`).
Imprime OK / FALTA / N/A / DONO por item com a evidência achada. Sai com código 1 se faltar
qualquer item obrigatório (saída ≠ 0 = NÃO avança, NÃO pergunta ao dono: fecha o item).
Sem dependências além da stdlib (o YAML é um subconjunto parseado aqui).
"""
import argparse, glob, json, os, re, sys, unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
YAML = HERE.parent / "references" / "TRILHA-CHECKLIST.yaml"
GENERIC = {"kit", "de", "do", "da", "app", "para", "calculadora", "pronto", "pack", "curso", "planilha"}


def norm(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def rx(pat):
    return re.compile(norm(pat), re.I | re.M | re.S)


# ───────────── parser do subconjunto YAML ─────────────
def unq(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] == '"':
        return v[1:-1].replace("\\\\", "\x00").replace('\\"', '"').replace("\x00", "\\")
    if len(v) >= 2 and v[0] == v[-1] == "'":
        return v[1:-1]
    return v


def load_items():
    items, cur, ev = [], None, False
    for raw in YAML.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        s = raw.strip()
        if raw.startswith("- id:"):
            cur = {"id": unq(s[5:]), "evidencia": []}
            items.append(cur)
            ev = False
        elif cur is not None and s == "evidencia:":
            ev = True
        elif cur is not None and ev and s.startswith("- "):
            k, _, v = s[2:].partition(":")
            cur["evidencia"].append((k.strip(), unq(v)))
        elif cur is not None and ":" in s:
            k, _, v = s.partition(":")
            cur[k.strip()] = unq(v)
            ev = False
    return items


def passo_num(p):
    m = re.match(r"T(\d+)", p or "")
    return int(m.group(1)) if m else -1


# ───────────── contexto da rodada ─────────────
class Ctx:
    def __init__(s, rodada, concepcao=None, oferta=None, root=None):
        s.rodada = Path(rodada).resolve()
        s.root = Path(root).resolve() if root else s.rodada.parent.parent
        s.hubdir = s.root / "HUB-OFERTAS"
        s.ofertas_dir = s.root / "OFERTAS"
        s.estado_txt = ""
        p = s.rodada / "ESTADO.md"
        if p.exists():
            s.estado_txt = p.read_text(encoding="utf-8", errors="ignore")
        s.estado = norm(s.estado_txt)
        s.concepcao = concepcao
        s.oferta_arg = oferta
        m = re.search(r"rodada\s*(\d+)", s.rodada.name, re.I)
        s.rid = ("r" + m.group(1)) if m else None
        s.hub = None
        hp = s.hubdir / "ofertas.json"
        if hp.exists():
            try:
                s.hub = json.loads(hp.read_text(encoding="utf-8"))
            except Exception:
                s.hub = None
        s.cache = {}
        s.rot = s._rot()

    def _rot(s):
        e = s.estado_txt
        g = lambda k: (re.search(r"^%s\s*(.*)$" % k, e, re.M) or [None, ""])[1]
        r2, r3, r4 = g("R2 modo:"), g("R3 origem:"), g("R4 nicho/persona:")
        modo = (re.match(r"\s*<?\s*([A-Z][0-9]?)\b", r2) or [None, ""])[1]
        m = re.search(r"origem:\s*(.+?)\s*→\s*destino:\s*(.+)", "origem: " + r3.replace("origem:", ""))
        cty = lambda t: norm(re.split(r"[/\s(]", t.strip())[0]) if t else ""
        cross = modo in ("B", "B2", "C", "P") or bool(m and cty(m.group(1)) != cty(m.group(2)))
        r4n = norm(r4).strip(" <>")
        return {"modo": modo, "cross": cross, "r4_nicho": bool(r4n) and not r4n.startswith("amplo")}

    # arquivos
    def files(s, pattern, oferta=None):
        base = s.rodada
        if pattern.startswith("oferta/"):
            if not oferta:
                return []
            base, pattern = s.ofertas_dir / oferta, pattern[len("oferta/"):]
            # padrão organizar-projeto (2026-10-04): docs de pesquisa em pesquisa/, página em site/
            # (2026-10-09: FUNIL.md e afins também aceitos em checkout/ — peças do funil moram lá)
            for alt in (pattern, "pesquisa/" + pattern, "checkout/" + pattern, re.sub(r"^pagina/", "site/", pattern)):
                found = sorted(Path(p) for p in glob.glob(str(base / alt), recursive=True) if Path(p).is_file())
                if found:
                    return found
            return []
        return sorted(Path(p) for p in glob.glob(str(base / pattern), recursive=True) if Path(p).is_file())

    def text(s, path):
        k = str(path)
        if k not in s.cache:
            try:
                s.cache[k] = norm(Path(path).read_text(encoding="utf-8", errors="ignore"))
            except Exception:
                s.cache[k] = ""
        return s.cache[k]

    def glob_text(s, pattern, oferta=None):
        return {str(f): s.text(f) for f in s.files(pattern, oferta)}

    # Hub
    def conc(s):
        if not s.hub:
            return []
        c = s.hub.get("concepcoes", [])
        if s.rid:
            c = [x for x in c if x.get("rodada") == s.rid]
        if s.concepcao:
            c = [x for x in c if x.get("id") == s.concepcao or x.get("id", "").endswith("-" + s.concepcao)]
        return c

    def ofertas(s):
        """ofertas em jogo: --oferta, ou Hub rodada==rid, ou pasta OFERTAS/<slug> citada no ESTADO."""
        if s.oferta_arg:
            return [s.oferta_arg]
        out = []
        if s.hub:
            out += [o["id"] for o in s.hub.get("ofertas", []) if s.rid and o.get("rodada") == s.rid]
        if s.ofertas_dir.exists():
            for d in sorted(p.name for p in s.ofertas_dir.iterdir() if p.is_dir()):
                if d not in out and norm(d) in s.estado:
                    out.append(d)
        return [o for o in out if (s.ofertas_dir / o).is_dir()]


def stems(slug):
    w = [x for x in re.split(r"[-_\s]+", norm(slug)) if x and x not in GENERIC]
    return [x[:6] if len(x) > 6 else x for x in w] or [norm(slug)]


def near(text, st, win=45):
    """raízes de `st` NA ORDEM do slug, no máx. 2 palavras entre elas (ex.: «orçamento da instalação elétrica»)."""
    pat = r"\b" + r"\w*(?:\W+\w+){0,2}?\W+".join(re.escape(x) for x in st) if len(st) > 1 else re.escape(st[0])
    m = re.search(pat, text)
    return m.start() if m else -1


def chunks_with(text, st):
    """seções (por título/tabela) onde as raízes aparecem juntas; fallback ±1200 chars."""
    outs = []
    parts = re.split(r"(?m)^#{1,4} ", text)
    for p in parts:
        if near(p, st) >= 0:
            outs.append(p)
    if not outs:
        i = near(text, st)
        if i >= 0:
            outs.append(text[max(0, i - 1200): i + 1200])
    return outs


# ───────────── checagens do Hub ─────────────
def _seguem(c):
    return [x for x in c if x.get("validacao") != "NAO_SEGUE"]


def _vivas(c):
    return [x for x in c if x.get("validacao") not in ("DUPLICATA", "DESCARTADA", "NAO_SEGUE")]


def _count_missing(lst, f, label, total=None):
    miss = [x.get("id", "?") for x in lst if not f(x)]
    t = len(lst)
    return (not miss, "%s: %d/%d%s" % (label, t - len(miss), t, "" if not miss else " — faltam: " + ", ".join(miss[:8]) + ("…" if len(miss) > 8 else "")))


def _has(k):
    return lambda x: x.get(k) not in (None, "", [], {})


def hub_check(ctx, name):
    if name == "decifrado":
        if ctx.hub:
            return True, "ofertas.json decifrado (atualizado_em %s)" % ctx.hub.get("atualizado_em")
        return False, "ofertas.json ausente/ilegível em %s — rode: cd HUB-OFERTAS && set -a; source ~/.claude/.credentials.env; set +a; uv run cifrar.py --verificar" % ctx.hubdir
    if not ctx.hub:
        return False, "Hub não decifrado (rode `uv run cifrar.py --verificar` em HUB-OFERTAS)"
    c = ctx.conc()
    if name == "concepcoes_no_hub":
        ids = set()
        for t in ctx.glob_text("lote-*.md").values():
            ids |= set(re.findall(r"\b[a-z]-\d{2}\b", t))
        n_hub = len(c)
        n_lote = len(ids)
        ok = n_hub > 0 and (n_lote == 0 or n_hub >= n_lote)
        return ok, "Hub=%d concepções da rodada; lotes .md citam %d ids" % (n_hub, n_lote)
    simple = {
        "sem_checklist_100k_0": ("checklist_100k", c, "checklist_100k"),
        "sem_nivel_consciencia_0": ("nivel_consciencia", c, "nivel_consciencia"),
        "sem_gate_origem_0": ("gate_origem", c, "gate_origem"),
        "sem_biblioteca_url_0": ("biblioteca_url", c, "biblioteca_url"),
        "sem_pagina_vendas_0": ("pagina_vendas", c, "pagina_vendas"),
        "sem_origem_referencia_0": ("origem_referencia", c, "origem_referencia"),
        "elementos_principais_100": ("elementos_principais", _seguem(c), "elementos+★"),
        "prova_leitura_100": ("prova_leitura", _seguem(c), "prova_leitura"),
        "pensamento_interno_100": ("pensamento_interno_amplo", _seguem(c), "pensamento_interno_amplo"),
        "urgencia_100": ("urgencia", _seguem(c), "urgencia"),
        "querem_precisam_100": ("querem_precisam", _seguem(c), "querem_precisam"),
        "sem_territorio_0": ("territorio_anuncios", _vivas(c), "territorio_anuncios"),
        "comunicacoes_modeladas_100": ("comunicacoes_modeladas", _vivas(c), "comunicacoes_modeladas"),
    }
    if name in simple:
        k, lst, label = simple[name]
        if name == "sem_territorio_0":
            return _count_missing(lst, lambda x: x.get(k) is not None, label)
        if name == "pensamento_interno_100":
            return _count_missing(lst, lambda x: _has("pensamento_interno_amplo")(x) and _has("pensamento_interno_tecnico")(x), label + "+tecnico")
        return _count_missing(lst, _has(k), label)
    if name == "producao_sem_parada3":  # T13.0 — decisão do dono 25/09/2026
        bad = []
        for o in ctx.hub.get("ofertas", []):
            if o.get("rodada") == ctx.rid and norm(str(o.get("status") or "")) in ("producao", "em producao", "construcao"):
                sl = str(o.get("id"))
                if not re.search(r"parada 3[^\n]*liberad[^\n]*" + re.escape(norm(sl)), ctx.estado):
                    bad.append(sl)
        return (not bad), ("nenhuma oferta em produção sem 'Parada 3 LIBERADA <slug>'" if not bad else "GASTO SEM GATE — oferta(s) com status producao e sem linha 'Parada 3 LIBERADA <slug>' no ESTADO: " + ", ".join(bad))
    if name == "concepcoes_hipotese_fora_de_obra":  # T7.30 — decisão do dono 25/09/2026
        bad = [x.get("id", "?") for x in c if x.get("origem_referencia") in (None, "", "GERADA") and not _has("prova_mercado")(x) and x.get("validacao") not in ("DESCARTADA", "PENDENTE", "DUPLICATA")]
        return (not bad), ("toda concepção gerada tem prova_mercado ou está DESCARTADA/PENDENTE" if not bad else "concepção gerada SEM prova_mercado e ainda viva (=> DESCARTE/PENDENTE, nunca Obra): " + ", ".join(bad[:8]))
    if name == "descartadas_com_nota":
        d = [x for x in c if x.get("validacao") == "DESCARTADA"]
        return _count_missing(d, _has("nota_descarte"), "DESCARTADA com nota_descarte")
    if name == "volume_55_60_ou_aceite":
        n = len(c)
        aceite = re.search(r"dono aceitou n ?= ?[0-9]+", ctx.estado)
        return (55 <= n <= 60 or bool(aceite)), "concepções da rodada = %d; %s" % (n, "linha de aceite do dono achada" if aceite else "sem linha 'dono aceitou N=<n> em DD/MM'")
    if name == "verdes_ge3_ou_decisao":
        v = [o["id"] for o in ctx.hub.get("ofertas", []) if o.get("rodada") == ctx.rid and o.get("semaforo") == "VERDE"]
        ok = len(v) >= 3 or bool(re.search(r"<3 verdes|menos de 3 verdes", ctx.estado))
        return ok, "%d verde(s) (%s); %s" % (len(v), ", ".join(v) or "—", "ok" if ok else "SEM linha '<3 verdes: liberou N, próximas da fila: …' no ESTADO")
    if name == "oferta_verde_existe":
        v = [o["id"] for o in ctx.hub.get("ofertas", []) if o.get("rodada") == ctx.rid and o.get("semaforo") == "VERDE"]
        return bool(v), "ofertas VERDE da rodada: %s" % (", ".join(v) or "nenhuma")
    if name == "territorio_servico_marcado":
        terms = []
        for f in ctx.files("fila-territorio.txt") + ctx.files("validacao-*.md") + ctx.files("PARADA-2.md"):
            for m in re.finditer(r"or[cç]amento (?:de|para|do|da) [a-z]+|servico de [a-z]+", ctx.text(f)):
                terms.append(m.group(0))
        if not terms:
            return True, "nenhum território com termo de serviço ('orçamento de X') encontrado"
        alltxt = " ".join(list(ctx.glob_text("validacao-*.md").values()) + list(ctx.glob_text("PARADA-2.md").values()))
        ok = bool(re.search(r"inflad|servico local|ruido de servico|anuncio de servico", alltxt))
        return ok, "termos de serviço: %s → %s" % (", ".join(sorted(set(terms))[:4]), "marcados como possivelmente inflados" if ok else "NENHUM marcado 'inflado por serviço local' (validacao-*.md / PARADA-2.md)")
    return False, "checagem de Hub desconhecida: " + name


# ───────────── cobertura por oferta (pivô) ─────────────
def coberta(ctx, passo, oferta):
    st = stems(oferta)
    if passo == "T7":
        for pat in ("modelagem-*.md", "persona-*.md", "finalistas.md"):
            for f, t in ctx.glob_text(pat).items():
                for ch in chunks_with(t, st):
                    if "elemento" in ch and "mudado" in ch and "territ" in ch:
                        return True, "T7 de '%s' em %s" % (oferta, os.path.basename(f))
        return False, "'%s' NÃO tem modelagem própria (elemento_mudado + território) em modelagem-*/persona-*/finalistas.md — concepção nova depois do T7 tem que RE-ENTRAR em T7 (pivô)" % oferta
    if passo == "T9":
        best = None
        for f, t in list(ctx.glob_text("demanda-*.md").items()) + list(ctx.glob_text("validacao-*.md").items()):
            for ch in chunks_with(t, st):
                miss = [n for n, k in (("YouTube", "youtube"), ("TikTok", "tiktok"), ("Trends", "trends"), ("sinal_de_compra", "sinal"), ("urgência", "urg")) if k not in ch]
                if best is None or len(miss) < len(best[1]):
                    best = (os.path.basename(f), miss)
        if best and not best[1]:
            return True, "T9 completo de '%s' em %s (YouTube+TikTok+Trends+sinal+urgência)" % (oferta, best[0])
        if best:
            return False, "'%s' em %s mas SEM: %s" % (oferta, best[0], ", ".join(best[1]))
        return False, "'%s' NÃO aparece em demanda-*.md/validacao-*.md — 3 fontes (YouTube·TikTok·Trends) + sinal + urgência não medidos (T9 do pivô)" % oferta
    if passo == "T10":
        for f, t in ctx.glob_text("PARADA-2*.md").items():
            if near(t, st) >= 0:
                for m in re.finditer(r"[^\n]*parada 2[^\n]*aprovad[^\n]*", ctx.estado):
                  if near(m.group(0), st) >= 0:
                    return True, "'%s' citada em %s e na linha 'Parada 2 APROVADA' do ESTADO" % (oferta, os.path.basename(f))
        return False, "'%s' não está numa PARADA-2*.md com aprovação do dono datada no ESTADO — sem Parada 2 formal" % oferta
    return False, "cobertura desconhecida " + passo


# ───────────── avaliação de evidência ─────────────
def split_gp(v):
    g, _, p = v.partition("::")
    return g.strip(), p.strip()


def eval_ev(ctx, kind, val, oferta):
    if kind == "arquivo":
        fs = [f for alt in val.split(" | ") for f in ctx.files(alt.strip(), oferta)]
        if val.startswith("oferta/") and not oferta:
            return None, "sem oferta"
        return bool(fs), ("%d achado(s): %s" % (len(fs), ", ".join(os.path.relpath(f, ctx.root) if val.startswith("oferta/") else f.name for f in fs[:3])) if fs else "não existe: " + val)
    if kind in ("arquivo_contem", "arquivo_sem"):
        g, p = split_gp(val)
        if g.startswith("oferta/") and not oferta:
            return None, "sem oferta"
        texts = ctx.glob_text(g, oferta)
        if not texts:
            return (kind == "arquivo_sem"), "nenhum arquivo em " + g
        r = rx(p)
        hits = []
        for f, t in texts.items():
            if ctx.concepcao and norm(ctx.concepcao) not in t:
                continue
            m = r.search(t)
            if m:
                hits.append((os.path.basename(f), t[max(0, m.start() - 20): m.end() + 40].replace("\n", " ")))
        if kind == "arquivo_contem":
            return bool(hits), ("achado em %s: «…%s…»" % (hits[0][0], hits[0][1].strip()[:90]) if hits else "regex /%s/ ausente em %s" % (p, g))
        return (not hits), ("padrão proibido /%s/ ausente" % p if not hits else "PADRÃO PROIBIDO em %s: «…%s…»" % (hits[0][0], hits[0][1].strip()[:100]))
    if kind == "estado":
        m = rx(val).search(ctx.estado)
        return bool(m), ("linha no ESTADO: «%s»" % ctx.estado[max(0, m.start()): m.end() + 60].split("\n")[0][:100] if m else "ESTADO sem /%s/" % val)
    if kind == "hub":
        return hub_check(ctx, val)
    if kind == "mtime_antes":
        if not oferta:
            return None, "sem oferta"
        a, b = [x.strip() for x in val.split("|")]
        fa, fb = ctx.files(a, oferta), ctx.files(b, oferta)
        if not fa or not fb:
            return False, "falta arquivo: %s%s" % ("" if fa else a + " ", "" if fb else b)
        ok = min(os.path.getmtime(f) for f in fa) <= min(os.path.getmtime(f) for f in fb)
        return ok, "%s %s %s (mtime)" % (os.path.basename(fa[0]), "anterior a" if ok else "POSTERIOR a", os.path.basename(fb[0]))
    if kind == "arquivo_recente":
        if not oferta:
            return None, "sem oferta"
        g, h = split_gp(val)
        fs = ctx.files(g, oferta)
        if not fs:
            return False, "não existe: " + g
        import time
        age = (time.time() - max(os.path.getmtime(f) for f in fs)) / 3600
        return age <= float(h), "%s modificado há %.1f h (limite %sh)" % (os.path.basename(fs[0]), age, h)
    if kind == "condicao_bloqueante":
        if not oferta:
            return None, "sem oferta"
        obr = " ".join(ctx.glob_text("oferta/obra-de-arte.md", oferta).values())
        sem = re.search(r"verde\W{1,4}(com|c/)\W{1,3}(condicao|ressalva)|verde condicionad", obr)
        if not sem:
            return True, "sem 'verde com condição/ressalva' no texto da Obra"
        line = re.search(r"^[^\n]*condicao ?(→|->)[^\n]*$", ctx.estado, re.M)
        if line and near(line.group(0), stems(oferta)) >= 0:
            return True, "condição liberada pelo dono e gravada: «%s»" % line.group(0)[:100]
        return False, "Obra diz 'verde com condição/ressalva' e o ESTADO não tem linha 'CONDIÇÃO → <id> · responsável · prazo · evidência' da oferta (condição pendente = AMARELA)"
    if kind == "oferta_coberta":
        if not oferta:
            return None, "sem oferta"
        return coberta(ctx, val, oferta)
    return False, "tipo de evidência desconhecido: " + kind


def oferta_cond(ctx, cond, oferta):
    """condições por oferta (avaliadas dentro do laço de ofertas)."""
    obr = " ".join(ctx.glob_text("oferta/obra-de-arte.md", oferta).values()) if oferta else ""
    app = bool(re.search(r"\b(app|calculadora|gerador|dimensionador|ferramenta)\b", obr[:6000]))
    sens = bool(re.search(r"area sensivel ?: ?sim", obr))
    if cond == "oferta_app":
        return app
    if cond == "oferta_app_sensivel":
        return app and sens
    return True


def applies(ctx, cond):
    c = (cond or "sempre").strip()
    if c.startswith("oferta_"):
        return True
    if c == "cross_construcao":
        return ctx.rot["cross"] and bool(re.search(r"parada 3.*liberad|t12.*liberad", ctx.estado))
    if c == "sempre" or c == "construcao" and re.search(r"parada 3.*liberad|t12.*liberad", ctx.estado):
        return True
    if c == "construcao":
        return False
    if c == "r4_nicho":
        return ctx.rot["r4_nicho"]
    if c == "cross":
        return ctx.rot["cross"]
    if c.startswith("modo:"):
        return ctx.rot["modo"] in c[5:].split(",")
    mod = "\n".join(ctx.glob_text("modelagem-*.md").values()) + "\n".join(ctx.glob_text("modelagem-*.jsonl").values())
    if c == "formato_mudou":
        return bool(re.search(r"elemento[_ ]mudado[^\n]{0,160}formato", mod))
    if c == "comunicacao_mudou":
        return bool(re.search(r"elemento[_ ]mudado[^\n]{0,160}(comunica|persona|dor|desejo)", mod))
    if c == "pivo":
        if re.search(r"piv[oô]", ctx.estado):
            return True
        return any(not coberta(ctx, "T7", o)[0] for o in ctx.ofertas())
    return True


def dono_dispensou(ctx, iid, passo):
    for pat in (re.escape(norm(iid)), re.escape(norm(passo))):
        m = re.search(r"[^\n]*\b%s\b[^\n]*aberto-por-decis[^\n]*" % pat, ctx.estado)
        if m:
            return m.group(0)[:120]
    return None


def encerrada(ctx, slug):
    """oferta morta no Hub (status perdeu/pausada/… ou semáforo VERMELHA) -> motivo, senão None."""
    if not ctx.hub:
        return None
    o = next((x for x in ctx.hub.get("ofertas", []) if x.get("id") == slug), None)
    if not o:
        return None
    st = norm(str(o.get("status") or ""))
    if st in ("perdeu", "pausada", "encerrada", "descartada") or o.get("semaforo") == "VERMELHA":
        return "status=%s semáforo=%s — %s" % (o.get("status"), o.get("semaforo"), (o.get("semaforo_motivo") or o.get("notas") or "sem motivo no Hub")[:110].replace("\n", " "))
    return None


def retroativo(ctx, iid):
    for m in re.finditer(r"^[^\n]*retroativo:[^\n]*$", ctx.estado, re.M):
        ln = m.group(0)
        if re.search(r"\b%s\b" % re.escape(norm(iid)), ln):
            f = re.search(r"auditoria\s+(\S+\.\w+)", ln)
            if f and (ctx.rodada / f.group(1).strip("`.,;")).exists():
                return ln.strip()[:140]
    return None


def run(ctx, items, passos):
    falta = 0
    out = []
    for it in items:
        if it.get("passo") not in passos:
            continue
        iid, passo = it["id"], it["passo"]
        if not applies(ctx, it.get("obrigatorio")):
            out.append("[N/A]   %-6s %s  (condição não vale: %s)" % (iid, it["titulo"], it.get("obrigatorio")))
            continue
        d = dono_dispensou(ctx, iid, passo)
        if d:
            out.append("[DONO]  %-6s %s\n           ABERTO-POR-DECISÃO registrado: «%s»" % (iid, it["titulo"], d))
            continue
        if it.get("retroativo") == "sim":
            r = retroativo(ctx, iid)
            if r:
                out.append("[RETRO] %-6s %s\n           RETROATIVO aceito: «%s»" % (iid, it["titulo"], r))
                continue
        targets = [None]
        if it.get("nivel") == "oferta" or (it.get("obrigatorio") or "").startswith("oferta_") or any(k == "oferta_coberta" or v.startswith("oferta/") or "oferta/" in v.split("::")[0] for k, v in it["evidencia"]):
            targets = ctx.ofertas() or [None]
        for of in targets:
            if of and not oferta_cond(ctx, it.get("obrigatorio"), of):
                out.append("[N/A]   %-6s %s  «oferta %s»  (condição não vale: %s)" % (iid, it["titulo"], of, it.get("obrigatorio")))
                continue
            if of and (mot := encerrada(ctx, of)):
                out.append("[N/A]   %-6s %s  «oferta %s»\n           N/A — encerrada: %s" % (iid, it["titulo"], of, mot))
                continue
            lines, ok_all = [], True
            for kind, val in it["evidencia"]:
                ok, det = eval_ev(ctx, kind, val, of)
                if ok is None:
                    ok, det = False, "nenhuma oferta encontrada (passe --oferta <slug>)"
                ok_all &= bool(ok)
                lines.append("           %s %s: %s" % ("✔" if ok else "✘", kind, det))
            tag = "[OK]   " if ok_all else "[FALTA]"
            falta += 0 if ok_all else 1
            head = "%s %-6s %s%s" % (tag, iid, it["titulo"], "  «oferta %s»" % of if of else "")
            out.append(head + "\n" + "\n".join(l for l in lines if (not ok_all or True)))
    return out, falta


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rodada", required=True, help="pasta MINERACAO/<rodada>")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--passo", help="ex.: T7")
    g.add_argument("--ate", help="ex.: T12 (verifica T0 … T12)")
    ap.add_argument("--concepcao")
    ap.add_argument("--oferta")
    ap.add_argument("--root", help="raiz LOW-TICKET (padrão: dois níveis acima da rodada)")
    ap.add_argument("--so-falta", action="store_true", help="imprime só os itens FALTA")
    a = ap.parse_args()
    if not Path(a.rodada).is_dir():
        sys.exit("rodada inexistente: " + a.rodada)
    ctx = Ctx(a.rodada, a.concepcao, a.oferta, a.root)
    items = load_items()
    if a.passo:
        n = passo_num(a.passo)
        passos = {"T%d" % n}
    else:
        n = passo_num(a.ate)
        passos = {"T%d" % i for i in range(0, n + 1)}
    print("GATE  rodada=%s  %s  modo=%s cross=%s r4_nicho=%s  hub=%s" % (
        ctx.rodada.name, ("passo " + a.passo) if a.passo else ("até " + a.ate), ctx.rot["modo"] or "?", ctx.rot["cross"], ctx.rot["r4_nicho"], "decifrado" if ctx.hub else "NÃO DECIFRADO (rode `uv run cifrar.py --verificar` em HUB-OFERTAS)"))
    if not ctx.estado_txt:
        print("[FALTA] ESTADO.md inexistente em", ctx.rodada)
    out, falta = run(ctx, items, passos)
    for o in out:
        if a.so_falta and not o.startswith("[FALTA]"):
            continue
        print(o)
    tot = len(out)
    print("\nRESULTADO: %s — %d item(ns) FALTA de %d verificados%s" % ("FALTA (exit 1) — NÃO AVANÇA" if falta or not ctx.estado_txt else "OK (exit 0)", falta, tot, ""))
    sys.exit(1 if falta or not ctx.estado_txt else 0)


if __name__ == "__main__":
    main()
