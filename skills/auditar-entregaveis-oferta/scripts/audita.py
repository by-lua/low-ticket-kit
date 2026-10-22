#!/usr/bin/env python3
"""Audita entregáveis de uma oferta low ticket.

Conta, por item: o que a página promete (MANIFESTO-ENTREGAVEIS.md), o que existe
escrito (produto/TEXTO/) e o que está publicado na área de membros
(site/painel/conteudo/). Reescreve produto/ENTREGAVEIS.yaml.

Além da contagem, faz as CHECAGENS que a contagem sozinha não vê (buraco que já
passou em branco mais de uma vez):
  A. card no /painel sem item no MANIFESTO      -> item vendido invisível pro audit
  B. pages[] do card × arquivo no disco         -> imagem quebrada / página órfã
  C. sku do card sem caminho no webhook          -> pagou e nunca libera
  D. sku que o webhook concede × item no MANIFESTO -> entrega fora do manifesto
  E. arquivo de página no disco e FORA do git   -> gerou mas não subiu (cliente não vê)
  F. pages: do card corrompido no index.html    -> [object Object] / .map repetido

Uso:
  audita.py OFERTAS/<slug> [--json] [--so-gap]
"""
import argparse, json, os, re, sys, unicodedata
from datetime import date

IMG_EXT = (".webp", ".jpg", ".jpeg", ".png")
GAPOS = {"VAZIO": 0, "MVP": 1, "COMPLETO": 2, "SOBRA_PAGINA": 2}
# data (12/10) e texto de Estado (publicado/agregador/lê os N SKUs) na coluna Estado
RE_DATA = re.compile(r"\d{1,2}/\d{1,2}")
RE_ESTADO = re.compile(r"publicad|produ[cç]|agregador|vazio|em falta|commit|\bSKUs?\b", re.I)


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def radical(w: str) -> str:
    """Radical simples para casar singular×plural entre item e pasta do painel.
    Medido 15/10/2026 (Jiu-Jitsu): o item "Order bump 5 — manual de defesa e
    escapes" NÃO casava com a pasta `bump-defesas` (item no singular, pasta no
    plural) e saía VAZIO com 5 páginas no disco — mesma classe do
    "finalizacao"×"finalizacoes" do bump 4."""
    if w.endswith("oes") or w.endswith("aes"):
        return w[:-3] + "ao"
    if w.endswith("s") and len(w) > 4:
        return w[:-1]
    return w


def primeiro_int(texto: str):
    m = re.search(r"(\d+)", (texto or "").replace(".", ""))
    return int(m.group(1)) if m else None


def manifesto(oferta: str):
    """Lê a tabela do MANIFESTO-ENTREGAVEIS.md, casando o cabeçalho por nome de coluna.

    Cabeçalho canônico: | Item | Tipo | Plano | Promessa | Nº páginas (completo) | Nº páginas (MVP) | Estado |
    Aceita variação de acento/caixa nas células e cauda extra.
    """
    path = os.path.join(oferta, "produto", "MANIFESTO-ENTREGAVEIS.md")
    if not os.path.exists(path):
        return []
    linhas = [l.strip() for l in open(path, encoding="utf-8")]
    #去哪 header: a linha de tabela cujo 1º campo é "Item"
    cab = None
    for i, l in enumerate(linhas):
        if not l.startswith("|"):
            continue
        cols = [norm(c.strip()) for c in l.strip("|").split("|")]
        if cols and cols[0].startswith("item") and len(cols) >= 5:
            cab = {"idx": i, "n": len(cols),
                   "promessa": next(j for j, c in enumerate(cols) if "promessa" in c),
                   "completo": next((j for j, c in enumerate(cols) if "completo" in c), None)}
            break
    if not cab:
        return []
    itens = []
    for l in linhas[cab["idx"] + 1:]:
        if not l.startswith("|"):
            if l.strip() == "":
                continue
            break
        cols = [c.strip() for c in l.strip("|").split("|")]
        if len(cols) < cab["n"] - 2 or not cols[0]:
            continue
        if set(cols[0]) <= set("- "):
            continue
        tipo = cols[1] if len(cols) > 1 else ""
        ic = cab["completo"]
        prometido = primeiro_int(cols[ic]) if ic is not None and ic < len(cols) else None
        if prometido is None:
            # Fallback pelas colunas de CONTAGEM. A coluna Estado fica fora: ela traz
            # data ("publicado 12/10") e nº de SKU ("agregador — lê os 4 SKUs") e o item
            # saía VAZIO com promessa inventada (Eletrotecnia 15/10/2026: Calculadora
            # com "prometido 12" e Kit Completo com "prometido 4" — os dois VAZIO).
            inicio = (ic + 1) if ic is not None else 3
            for c in reversed(cols[inicio:]):
                if RE_DATA.search(c) or RE_ESTADO.search(c):
                    continue
                v = primeiro_int(c)
                if v and v > 3:
                    prometido = v
                    break
        # Linha sem número de páginas = agregador (combo que "lê os 3 itens acima",
        # upsell sem página própria). ANTES ela era descartada e o card vendido
        # correspondente sumia do audit inteiro (Jiu 15/10: combo domínio à venda
        # e o audit dizia 14 itens — 15 existem). Agora entra, marcado.
        agregador = not prometido
        itens.append({
            "item": cols[0],
            "tipo": tipo,
            "plano": cols[2] if len(cols) > 2 else "",
            "promessa": (cols[cab["promessa"]][:300] if cab["promessa"] < len(cols) else ""),
            "prometido": prometido or 0,
            "agregador": agregador,
        })
    return itens


def painel_de(oferta: str):
    """Raiz do `/painel` desta oferta.

    Oferta que mora no painel de OUTRA declara isso no MANIFESTO (o Baralho do Cigano
    vive no painel do Mapa do Tarot por decisão da dona, 05/10/2026):

      > **Painel desta auditoria:** `../mapa-do-tarot/site/painel` (moramos nele)

    Sem a declaração o audit do Cigano lia a cópia velha parada em `site/painel/`
    (4 páginas de 36 cartas, contra 37 no ar) e dizia que 137 páginas publicadas eram
    VAZIO — medido 15/10/2026. O caminho pode ser relativo à oferta ou à raiz do portfólio.
    """
    padrao = os.path.join(oferta, "site", "painel")
    path = os.path.join(oferta, "produto", "MANIFESTO-ENTREGAVEIS.md")
    if not os.path.exists(path):
        return padrao
    m = re.search(r"\*\*Painel desta auditoria:\*\*\s*`([^`]+)`",
                  open(path, encoding="utf-8").read())
    if not m:
        return padrao
    alvo = m.group(1).strip()
    candidatos = [alvo]
    if not os.path.isabs(alvo):
        candidatos = [os.path.normpath(os.path.join(oferta, alvo)),
                      os.path.normpath(os.path.join(oferta, "..", "..", alvo))]
    for c in candidatos:
        if os.path.isdir(c):
            return c
    print(f"AVISO: painel declarado ({alvo}) não existe — usando {padrao}")
    return padrao


def ja_publicado(oferta: str):
    """Conta imagens por pasta de conteúdo do painel."""
    base = os.path.join(painel_de(oferta), "conteudo")
    out = {}
    global colisores
    colisores = {}
    if not os.path.isdir(base):
        return out
    for d in sorted(os.listdir(base)):
        p = os.path.join(base, d)
        if not os.path.isdir(p):
            continue
        n = 0
        paginas = set()
        por_numero = {}
        for root, _, files in os.walk(p):
            # `original` = arquivo bruto; `pdf/` = o JPEG irmão que alimenta o download,
            # uma cópia da MESMA página. Contar os dois dobra a entrega (medido 13/10:
            # principal dizia 186 = 93 webp + 93 jpg).
            if os.path.basename(root) in ("original", "pdf"):
                continue
            for f in files:
                if f.lower().startswith("capa") or not f.lower().endswith(IMG_EXT):
                    continue
                stem = os.path.splitext(f.lower())[0]
                m = re.match(r"pagina-0*(\d+)(?:-(.*))?$", stem)
                if m:
                    num = int(m.group(1))
                    paginas.add((num, norm(m.group(2) or "")))
                    por_numero.setdefault(num, set()).add(norm(m.group(2) or ""))
                else:
                    n += 1
                    paginas.add((None, stem))
        # Conta PÁGINA, não arquivo: no Tarot cada página sai em `.jpg` E `.webp` (o jpg
        # alimenta o PDF, o webp o leitor) — contar arquivo dobrava tudo (46 páginas saíam
        # como 92) e escondia página faltando: o Cigano dizia "38/38 COMPLETO" com o índice
        # de consulta ainda por gerar (medido 15/10/2026). A chave é (número, slug), não o
        # número sozinho: `pagina-01-simbologia` e `pagina-001-tensao` são páginas
        # DIFERENTES que colidem no 1 (Elétrica, 13/10 — 93 páginas contadas como 87).
        out[d] = len(paginas) or n
        ambiguas = sum(len(v) for v in por_numero.values()) - len(por_numero)
        if ambiguas > 0:                  # duas páginas DIFERENTES no mesmo número
            colisores.setdefault(d, ambiguas)
    return out


colisores = {}


def casar_item(chave: str, paineis: dict, nome_item: str = ""):
    """Associa pasta do painel ao item. `chave` = tipo + nome (o número do bônus
    costuma estar só no tipo: "Bônus 1 | +50 Flashcards ...")."""
    n = norm(chave)
    # Nome idêntico à pasta: no Mapa do Tarot os itens do manifesto se chamam
    # "completo", "guia-flash", "perguntas-80", "folha-consulta" — e as pastas do
    # painel têm esses MESMOS nomes. Sem este passe, o item saía VAZIO com a
    # pasta cheia (medido 14/10: 160 páginas "faltando" que já estavam no ar).
    ni = norm(nome_item)
    for d in paineis:
        if ni and norm(d) == ni:
            return d
    # Item é order bump? Então NUNCA casa com pasta de bônus. Medido no Jiu-Jitsu
    # 14/10/2026: tipo "Bônus 1 (OB)" casava com a pasta bonus-1 e um bump VAZIO
    # saía COMPLETO contando as páginas do bônus (o cliente via "em atualização").
    eh_ob = bool(re.search(r"\bob\b", n)) or bool(re.search(r"(?:order[\s-]*)?bump", n))
    for d in paineis:
        nd = norm(d)
        if nd.startswith("principal") and "principal" in n:
            return d
        mb = re.search(r"bonus[\s-]*(\d)", n)
        if mb and not eh_ob and re.search(r"bonus[\s-]*" + mb.group(1), nd):
            return d
        mb = re.search(r"(?:order[\s-]*)?bump[\s-]*(\d)", n)
        if mb and ("ob" in nd or "bump" in nd):
            if "combo" in nd and "combo" in n:
                return d
            # casa pelo assunto do item, não pelo número do bump (a numeração do
            # manifesto não bate com a pasta do painel). Escolhe a pasta MAIS
            # ESPECÍFICA entre as candidatas: `ob-manual-seguranca` também contém
            # "seguranca" e, na ordem alfabética, vinha antes de `ob-seguranca` —
            # engolia o Order bump 1 (+60 Mapas de Segurança Industrial), que saía
            # VAZIO com 10 páginas no ar (Eletrotecnia, 15/10/2026).
            # stem das palavras do item, para casar singular×plural (defesa×defesas)
            stems_n = {radical(w) for w in re.split(r"[^a-z]+", n) if w}
            melhor, melhor_score = None, (0.0, 0)
            for d2 in paineis:
                nd2 = norm(d2)
                if "ob" not in nd2 and "bump" not in nd2:
                    continue
                tk = [t for t in re.split(r"[^a-z]+", nd2)
                      if len(t) >= 4 and t not in {"order", "bump", "combo", "novo"}]
                if not tk:
                    continue
                casam = sum(1 for t in tk if radical(t) in stems_n)
                if not casam:
                    continue
                score = (casam / len(tk), casam)
                if score > melhor_score:
                    melhor, melhor_score = d2, score
            if melhor:
                return melhor
            # fallback: pasta bump-N / ob-N com o MESMO número do item
            if re.search(r"(?:ob|bump)[\s-]*" + mb.group(1) + r"(?!\d)", nd):
                return d
    return None


def texto_declarado(oferta: str):
    """Itens cujo texto o MANIFESTO declara onde mora (`item` = `caminho`).

    Oferta que guarda o manuscrito FORA de `produto/TEXTO/` declara item a item:
    o Tarot tem um manuscrito único (`produto/ENTREGA-COMPLETA-TXT.md`, só o Básico) e
    um texto por order bump (`produto/ORDER-BUMPS/<bump>/TEXTO.md`); o Cigano guarda o
    texto por página no pacote (`produto/paginas/pacote-*/02-textos-e-dados/<módulo>/`).
    `—` = declaradamente não escrito. Item não citado cai na regra antiga (`produto/TEXTO/`).
    Sem a declaração a coluna `txt` mente (medido 15/10/2026: o Tarot saía "ausente" nos
    9 itens, com 4 deles já escritos; o Cigano, nos 13).
    """
    mapa = {}
    path = os.path.join(oferta, "produto", "MANIFESTO-ENTREGAVEIS.md")
    if not os.path.exists(path):
        return mapa
    for it, cam in re.findall(r"`([^`=\n]{2,60})`\s*=\s*`([^`=\n]{1,200})`",
                              open(path, encoding="utf-8").read()):
        mapa[norm(it)] = cam.strip()
    return mapa


def caminho_tem_texto(oferta: str, cam: str):
    alvo = cam if os.path.isabs(cam) else os.path.normpath(os.path.join(oferta, cam))
    if "*" in alvo:
        import glob
        achados = glob.glob(alvo, recursive=True)
        return any(os.path.isfile(p) for p in achados) or any(
            f.endswith(".md") for p in achados if os.path.isdir(p)
            for _, _, fs in os.walk(p) for f in fs)
    if os.path.isfile(alvo):
        return True
    if os.path.isdir(alvo):
        return any(f.endswith(".md") for _, _, fs in os.walk(alvo) for f in fs)
    return False


def tem_texto(oferta: str, chave: str, declarado=None, item: str = ""):
    # (0) o MANIFESTO manda: item declarado com caminho ou com "—" (não escrito).
    if declarado and item:
        cam = declarado.get(norm(item))
        if cam is not None:
            if not cam or cam in ("—", "-", "--"):
                return False
            return caminho_tem_texto(oferta, cam)
    # Aceita TEXTO/ ou texto/ — Linux é case-sensitive e o Jiu-Jitsu guarda em
    # `produto/texto/`, o que marcava "ausente" nos 11 itens (14/10/2026).
    base = None
    for nome in ("TEXTO", "texto"):
        p = os.path.join(oferta, "produto", nome)
        if os.path.isdir(p):
            base = p
            break
    if base is None:
        return False
    n = norm(chave)
    for root, _, files in os.walk(base):
        for f in files:
            if not f.endswith(".md") or f == "REVISAO.md":
                continue
            fn = norm(os.path.splitext(f)[0])
            mb = re.search(r"bonus[\s-]*(\d)", n)
            if mb and re.search(r"bonus[\s-]*" + mb.group(1), fn):
                return True
            mb = re.search(r"(?:order[\s-]*)?bump[\s-]*(\d)", n)
            # casa `bump1`, `bump-1`, `order-bump-1` no nome do arquivo
            if mb and re.search(r"bump[\s-]*" + mb.group(1) + r"(?!\d)", fn):
                return True
            # bumps NOVOS sem número no nome ("Order bump — guia completo de
            # finalizações") casam pelo assunto: arquivo `09-bump-finalizacoes.md`
            if ("bump" in n or "combo" in n) and any(
                    p in fn for p in re.split(r"[^a-z]+", n)
                    if len(p) >= 5 and p not in
                    {"guia", "manual", "order", "bump", "completo", "estrategias",
                     "bonus", "kit", "combo", "dominio"}):
                return True
            if "principal" in n and "principal" in fn:
                return True
    return False


def auditar(oferta: str):
    itens = manifesto(oferta)
    paineis = ja_publicado(oferta)
    declarado = texto_declarado(oferta)
    linhas = []
    for it in itens:
        chave = f'{it["tipo"]} {it["item"]}'
        pasta = casar_item(chave, paineis, nome_item=it["item"])
        pub = paineis.get(pasta, 0) if pasta else 0
        prom = it["prometido"]
        if it.get("agregador"):
            sit = "AGREGADOR"          # combo/upsell sem página própria — lê outros itens
        elif not pasta or pub == 0:
            sit = "VAZIO"
        elif prom and pub >= prom:
            sit = "COMPLETO"
        elif prom and pub >= max(1, round(prom * 0.4)):
            sit = "MVP"
        else:
            sit = "MVP"
        linhas.append(
            {
                "item": it["item"],
                "tipo": it["tipo"],
                "plano": it["plano"],
                "pasta_painel": pasta or "",
                "prometido": prom,
                "texto": "n/a" if it.get("agregador") else (
                    "ok" if tem_texto(oferta, chave, declarado, it["item"]) else "ausente"),
                "publicado": pub,
                "falta": max(0, (prom or 0) - pub),
                "situacao": sit,
            }
        )
    return linhas, paineis


def escrever_yaml(oferta, linhas, buracos=()):
    caminho = os.path.join(oferta, "produto", "ENTREGAVEIS.yaml")
    out = [
        "# Registro vivo de entregáveis — gerado por",
        "# ~/.claude/skills/auditar-entregaveis-oferta/scripts/audita.py",
        "# NÃO editar à mão. Rode o script de novo após gerar/publicar qualquer coisa.",
        f"gerado_em: {date.today().isoformat()}",
        "oferta: " + os.path.basename(os.path.abspath(oferta)),
        "itens:",
    ]
    for l in linhas:
        out.append(f"  - item: {l['item']}")
        out.append(f"    tipo: {l['tipo']}")
        out.append(f"    painel: {l['pasta_painel']}")
        out.append(f"    prometido: {l['prometido']}")
        out.append(f"    publicado: {l['publicado']}")
        out.append(f"    texto: {l['texto']}")
        out.append(f"    falta: {l['falta']}")
        out.append(f"    situacao: {l['situacao']}")
    if buracos:
        out.append("buracos:")
        for tipo, sku, det in buracos:
            out.append(f"  - tipo: {tipo}")
            out.append(f"    sku: {sku}")
            out.append(f"    detalhe: {det}")
    open(caminho, "w", encoding="utf-8").write("\n".join(out) + "\n")
    return caminho


def ordem(linhas):
    """Ordem da casa: item vazio que já é vendido primeiro; depois completar os
    que já têm MVP, do item mais vendido ao mais complementar."""
    peso_tipo = {"principal": 0, "bonus": 1, "order bump": 2, "combo": 9}
    def chave(l):
        t = norm(l["tipo"])
        p = 3
        for k, v in peso_tipo.items():
            if t.startswith(k):
                p = v
                break
        return (p, -l["falta"])
    return sorted(linhas, key=chave)


def retomar(oferta: str, linhas, lote: int = 10):
    """Imprime o próximo passo de produção, pronto pra executar."""
    print("\nRETOMADA — próximo passo de cada item (ordem da casa)\n")
    for l in ordem(linhas):
        if l["falta"] <= 0:
            print(f"[{l['situacao'].lower()}] {l['item']}")
            continue
        prox = l["publicado"] + 1
        ate = min(l["prometido"], prox + lote - 1)
        pasta = l["pasta_painel"] or "(criar pasta no painel)"
        print(f"→ {l['item']}")
        print(f"  estado   : {l['situacao']} — {l['publicado']}/{l['prometido']} no ar")
        print(f"  texto    : {'ok' if l['texto']=='ok' else 'AUSENTE — escrever antes (ordem texto→visual)'}")
        print(f"  gerar    : páginas {prox}–{ate}  ({ate-prox+1} nesta rodada)")
        print(f"  destino  : site/painel/conteudo/{pasta}/pagina-{prox:03d}-<slug>.webp")
        print(f"  refs     : produto/MVP/{l['pasta_painel'] or '<item>'}/ (2–3 páginas nossas já aprovadas)")
        print(f"  depois   : rodar de novo este script (atualiza ENTREGAVEIS.yaml) e subir no painel\n")


def _linha_status(linhas):
    partes = []
    for l in linhas:
        partes.append(f"{l['publicado']}/{l['prometido']} {l['situacao']}")
    return ", ".join(partes)


def registrar(oferta_raiz: str, oferta: str, linhas, buracos=()):
    """Escreve o estado onde toda sessão lê: STATUS.md da oferta + linha dela no
    STATUS.md da raiz. Idempotente por data (reexecutar no mesmo dia atualiza,
    não duplica entrada)."""
    hoje = date.today().isoformat()
    slug = os.path.basename(oferta)
    resumo = _linha_status(linhas)
    gaps = [l for l in linhas if l["falta"] > 0]
    txt_curto = {"ok": "ok", "n/a": "n/a"}

    bloco = (
        f"\n### {hoje} — auditoria de entregáveis (skill `auditar-entregaveis-oferta`)\n"
        f"Registro vivo: `produto/ENTREGAVEIS.yaml` (gerado; não editar à mão).\n"
        f"\n**Prometido × no painel:** {resumo}.\n"
        f"\n| Item | Texto | No painel | Falta |\n|---|---|---|---|\n"
        + "\n".join(
            f"| {l['item']} | {txt_curto.get(l['texto'], 'AUSENTE')} | "
            f"{l['publicado']}/{l['prometido']} | {l['falta']} |"
            for l in linhas
        )
        + "\n\n**Falta (ordem da casa: item vendido vazio → completar os que já têm MVP):** "
        + ("; ".join(f"{l['item']} ({l['falta']} pág)" for l in gaps) if gaps else "nada")
        + (" — **mas há {} buraco(s) A–H: tabela limpa NÃO é auditoria limpa**".format(len(buracos))
           if buracos else "")
        + "\n"
        + (("\n**Checagens A–H (buracos que a contagem não pega):**\n"
            + "\n".join(f"- `{t}` {s} — {d}" for t, s, d in buracos) + "\n")
           if buracos else "\n**Checagens A–H:** limpas (card × manifesto, pages[] × disco, sku × webhook, deploy git, menu index.html).\n")
    )

    # 1) STATUS.md da oferta
    sp = os.path.join(oferta, "STATUS.md")
    txt = open(sp, encoding="utf-8").read() if os.path.exists(sp) else "# STATUS — " + slug + "\n"
    if f"### {hoje} — auditoria de entregáveis" in txt:
        # Reexecução no mesmo dia: substitui SÓ o bloco antigo, preservando tudo
        # depois dele (Histórico!). Bug real 14/10: o `txt[:rindex]` truncava o
        # arquivo e apagou o Histórico inteiro da oferta Jiujitsu.
        ini = txt.rindex(f"\n### {hoje} — auditoria de entregáveis") + 1
        fim_linha = txt.index("\n", ini)              # fim da linha de heading do bloco
        mh = re.search(r"^#{2,3} ", txt[fim_linha + 1:], re.M)  # próximo heading DEPOIS do bloco
        fim = fim_linha + 1 + mh.start() if mh else len(txt)
        txt = txt[:ini] + bloco + ("\n" if not bloco.endswith("\n\n") else "") + txt[fim:]
    elif re.search(r"^##\s*Hist.rico", txt, re.M):
        h = re.search(r"^##\s*Hist.rico", txt, re.M).start()
        txt = txt[:h] + bloco.lstrip("\n") + "\n" + txt[h:]
    else:
        txt = txt.rstrip("\n") + "\n\n## Histórico\n" + bloco
    # Data do topo: NÃO sobrescrever a data de uma entrada que já existe (o parágrafo
    # abaixo dela descreve o fato DAQUELE dia). Antes o script trocava "2026-10-16
    # (webhooks...)" por "2026-10-20 (webhooks...)" — data nova com texto velho.
    # Agora entra uma linha nova de auditoria, preservando o histórico do topo.
    m = re.search(r"^\*\*Atualizado em:?\*\*\s*(\d{4}-\d{2}-\d{2})?", txt, re.M)
    if not (m and m.group(1) == hoje):
        t = txt.split("\n")
        pos = 1 if t and t[0].startswith("# ") else 0
        t.insert(pos, f"\n**Atualizado em:** {hoje} — auditoria de entregáveis "
                      f"(números e buracos A–H no bloco `### {hoje}` abaixo).")
        txt = "\n".join(t)
    open(sp, "w", encoding="utf-8").write(txt)

    # 2) linha da oferta na tabela do STATUS.md da raiz
    rp = os.path.join(oferta_raiz, "STATUS.md")
    if os.path.exists(rp):
        raiz = open(rp, encoding="utf-8").read().split("\n")
        alvo = None
        for i, l in enumerate(raiz):
            if l.startswith("|") and slug in l:
                alvo = i
                break
        if alvo is not None:
            celulas = raiz[alvo].split("|")
            # tabela canônica: | Oferta | Fase | Mercado | No ar | Atualizado | Próximo passo |
            if len(celulas) >= 7:
                celulas[5] = f" {hoje} "
                passo = celulas[6].strip()
                marca = f"**{hoje}: promessa × entrega** — {resumo}."
                if not passo.startswith(marca):
                    celulas[6] = f" {marca} {passo}"
                raiz[alvo] = "|".join(celulas)
            else:
                print(f"AVISO: formato inesperado da linha de {slug} no STATUS.md da raiz")
            open(rp, "w", encoding="utf-8").write("\n".join(raiz))
        else:
            print(f"AVISO: linha de {slug} não encontrada em STATUS.md da raiz — não atualizada")
    return sp, rp


def cards_do_painel(oferta: str):
    """Lê os cards do /painel (MODULES + BUMPS) direto do index.html.

    Devolve {sku: {title, soon, pages}}. O painel é a ÚNICA coisa que o cliente
    vê — se o card existe aqui e não existe no MANIFESTO, ele está à venda fora
    de qualquer registro (Jiu-Jitsu 14/10: 4 bumps novos invisíveis).
    """
    path = os.path.join(painel_de(oferta), "index.html")
    cards = {}
    if not os.path.exists(path):
        return cards
    txt = open(path, encoding="utf-8").read()
    marcas = [m.start() for m in re.finditer(r"sku:\s*['\"]", txt)]
    for i, s in enumerate(marcas):
        fim = marcas[i + 1] if i + 1 < len(marcas) else len(txt)
        bloco = txt[s:fim]
        mk = re.match(r"sku:\s*['\"]([^'\"]+)['\"]", bloco)
        if not mk:
            continue
        sku = mk.group(1)
        # só o array pages: o resto do bloco vaza pra dentro se cortar por regex solta
        mp = re.search(r"pages\s*:\s*\[(.*?)\]", bloco, re.S)
        pages = re.findall(r"['\"]([^'\"]+\.(?:webp|jpg|jpeg|png))['\"]", mp.group(1)) if mp else []
        mt = re.search(r"title:\s*['\"]([^'\"]*)['\"]", bloco)
        ms = re.search(r"soon:\s*(true|false)", bloco)
        mpar = re.search(r"partial:\s*(true|false)", bloco)
        cards[sku] = {
            "title": mt.group(1) if mt else "",
            "soon": (ms.group(1) == "true") if ms else None,
            "partial": (mpar.group(1) == "true") if mpar else None,
            "pages": pages,
            # card sem `pages:` não é card de conteúdo desta oferta (é link/cross-sell
            # de outro produto, ex.: Tarot vendendo Cigano) — não entra nas checagens
            "conteudo": mp is not None,
        }
    return cards


STOP = {"guia", "manual", "order", "bump", "completo", "bonus", "bônus", "kit",
        "combo", "dominio", "dominância", "dominancia", "no", "de", "da", "do",
        "em", "e", "com", "para", "pr", "que", "seu", "sua"}


def _palavras(s: str):
    return {p for p in re.split(r"[^a-z0-9]+", norm(s)) if len(p) >= 4 and p not in STOP}


def parece_o_mesmo(a: str, b: str) -> bool:
    """Régua barata de 'é o mesmo item?': metade das palavras do menor no maior."""
    pa, pb = _palavras(a), _palavras(b)
    if not pa or not pb:
        return False
    comum = len(pa & pb)
    return comum >= max(1, min(len(pa), len(pb)) * 0.4)


def caminhos_entrega(oferta: str):
    """Do servidor: (todos os skus citados, skus que o webhook concede).

    `todos` evita falso "sem entrega" quando a liberação passa por outro mapa: no
    Tarot os 4 bônus e o `completo` saem do COMPLETO_OFFERS (offer code), não do
    PRODUCT_SKUS — medido 15/10, 5 cards marcados errados.
    """
    path = os.path.join(oferta, "site", "server", "index.mjs")
    if not os.path.exists(path):
        return None, None
    txt = open(path, encoding="utf-8").read()
    todos = set(re.findall(r"['\"]([A-Za-z][\w-]{1,40})['\"]", txt))
    concedidos = set()
    for nome in set(re.findall(r"const\s+([A-Z_]*(?:SKUS|OFFERS|ACCESS|EXPAND|BUMPS)\w*)\s*=", txt)):
        m = re.search(nome + r"\s*=\s*(?:new Set\()?\s*(\{.*?\n\}|\[[^\]]*\])", txt, re.S)
        if m:
            concedidos.update(re.findall(r"['\"]([^'\"]+)['\"]", m.group(1)))
    return todos, concedidos


def escopo(oferta: str):
    """Famílias de card que o MANIFESTO diz serem de OUTRA oferta (mesmo painel).

    No Tarot o `/painel` hospeda também o Baralho Cigano (`cigano-*`), que tem
    manifesto próprio em `mapa-do-cigano/`. Sem esta linha no MANIFESTO, todo card
    cigano saía como "vendido fora do manifesto" (16 falsos positivos medidos
    15/10). Declaração no MANIFESTO:
      > **Escopo desta auditoria:** só os itens da tabela abaixo. Fora: `cigano-*` (oferta própria).
    """
    path = os.path.join(oferta, "produto", "MANIFESTO-ENTREGAVEIS.md")
    pref = set()
    if not os.path.exists(path):
        return pref
    # Só o PARÁGRAFO da declaração conta (a linha quebra no meio da frase): o resto do
    # manifesto tem outros `code spans` (`site/painel/`, caminhos de referência) que não
    # são escopo.
    bloco, dentro = [], False
    for linha in list(open(path, encoding="utf-8")) + [""]:
        if not dentro:
            dentro = "escopo desta auditoria" in norm(linha)
            if dentro:
                bloco = [linha]
            continue
        if not linha.strip():
            break
        bloco.append(linha)
    for linha in bloco:
        for m in re.finditer(r"`([a-z][\w./*-]*)`", linha):
            tok = m.group(1)
            if tok.endswith("-*"):
                pref.add(tok[:-1])                    # `cigano-*` = família cigano-
            elif "/" not in tok and "." not in tok:
                pref.add(tok)                         # `principal` = item exato/prefixo
    return pref


def checar_deploy(oferta: str):
    """E. Página no disco/painel mas FORA do git (untracked, não ignorada).

    "Gerar" não é "publicar": o que o cliente vê é o que está **commitado e deployado**.
    Medido 16/10/2026 (Eletrotecnia): o publicador fazia só `git add painel/index.html`,
    então toda página NOVA (arquivo untracked) ficava no disco e nunca subia — o menu no
    ar apontava pra webp inexistente no servidor (leitor quebrado). O `pub` do audit
    contava o arquivo do disco e dizia "publicado". Esta checagem fecha esse buraco.

    Devolve None se `site/` não é repositório git (não dá pra checar).
    """
    import subprocess
    painel = painel_de(oferta)
    base = os.path.join(painel, "conteudo")
    if not os.path.isdir(base):
        return []
    try:
        root = subprocess.run(["git", "-C", painel, "rev-parse", "--show-toplevel"],
                              capture_output=True, text=True, timeout=20).stdout.strip()
    except Exception:
        root = ""
    if not root:
        return None
    rel = os.path.relpath(painel, root).replace(os.sep, "/")
    alvo = rel + "/conteudo"

    def _git(*args):
        try:
            out = subprocess.run(["git", "-C", root, *args], capture_output=True,
                                 text=True, timeout=90)
            return out.stdout.splitlines()
        except Exception:
            return []

    rastreados = set(_git("ls-files", "--", alvo))
    # untracked que NÃO está no .gitignore = vai ficar de fora do deploy
    untracked = set(_git("ls-files", "--others", "--exclude-standard", "--", alvo))
    achados = []
    for relfile in sorted(untracked):
        # `original/` é arquivo bruto do processo, não vai pro painel público
        partes = relfile.split("/")
        if "original" in partes:
            continue
        if not relfile.lower().endswith(IMG_EXT):
            continue
        try:
            mod = partes[partes.index("conteudo") + 1]
        except (ValueError, IndexError):
            mod = partes[-2] if len(partes) >= 2 else "?"
        achados.append(("E · NÃO-DEPLOYADA", mod,
                        f"{relfile} — no disco/painel mas fora do git (não sobe no deploy; "
                        f"o cliente não vê)"))
    _ = rastreados
    return achados


def menu_corrompido(oferta: str, cards):
    """F. `pages:` do card resolvendo pra caminho quebrado no `index.html`.

    Medido 16/10/2026 (Eletrotecnia): o `wire-bump-pages.py` não era idempotente e cada
    `--apply` colava outro `.map(...)` na lista. O 2º `.map` recebia objetos `{webp:...}` e
    virava `conteudo/<mod>/[object Object].webp` — o módulo INTEIRO quebrava no leitor e no
    PDF (`ob-seguranca`/`ob-medicao`/`ob-comandos`/`ob-materiais` ficaram quebrados no ar por
    4 publicações seguidas sem ninguém ver). Esta checagem pega isso na fonte.
    """
    path = os.path.join(painel_de(oferta), "index.html")
    if not os.path.exists(path):
        return []
    txt = open(path, encoding="utf-8").read()
    achados = []
    if "[object Object]" in txt:
        achados.append(("F · MENU-CORROMPIDO", "-",
                        "index.html contém '[object Object]' — alguma lista de páginas foi "
                        "cruzada com .map() mais de uma vez; o módulo abre sem imagem"))
    for sku in cards:
        sufixo = ".map(n=>({webp:'conteudo/%s/'+n+'.webp'}))" % sku
        n = txt.count(sufixo)
        if n > 1:
            achados.append(("F · MENU-CORROMPIDO", sku,
                            f"`pages:` com o mesmo .map() repetido {n}× — lista resolvendo pra "
                            f"'conteudo/{sku}/[object Object].webp' (leitor e PDF quebrados)"))
    return achados


def principal_fora_do_menu(oferta: str):
    """B (principal). Página do módulo principal no disco e FORA do `PRINCIPAL_CATEGORIES`.

    O principal monta o menu por categoria (`const PRINCIPAL_CATEGORIES = [{cat, pages:[…]}]`),
    não pelo `pages:` do card — o check de órfã por card o pulava inteiro (medido 16/10/2026:
    o publicador ligava só bônus/bumps e a página nova do principal ficaria commitada e
    invisível pro cliente).

    Só roda quando o menu é LITERAL (nomes `'pagina-…'`). Menu gerado por código
    (`Array.from` / `.map`, ex.: Tarot guia-flash) devolve vazio — não dá pra conferir sem
    falso positivo, então não arrisca.
    """
    painel = painel_de(oferta)
    idx = os.path.join(painel, "index.html")
    d = os.path.join(painel, "conteudo", "principal")
    if not (os.path.exists(idx) and os.path.isdir(d)):
        return []
    txt = open(idx, encoding="utf-8").read()
    m = re.search(r"const PRINCIPAL_CATEGORIES\s*=\s*\[(.*?)\n\];", txt, re.S)
    if not m:
        return []
    nomes = set(re.findall(r"'(pagina-[^']+)'", m.group(1)))
    if not nomes:                     # menu do principal não é literal — não arrisca
        return []
    achados = []
    for f in sorted(os.listdir(d)):
        if not (f.startswith("pagina-") and f.lower().endswith(IMG_EXT)):
            continue
        stem = os.path.splitext(f)[0]
        if stem in nomes:
            continue
        achados.append(("B · ÓRFÃ", "principal",
                        f"conteudo/principal/{f} — no disco e fora do PRINCIPAL_CATEGORIES "
                        f"(publicada mas fora do menu: cliente nunca vê)"))
    return achados


def checar_buracos(oferta: str, linhas, cards):
    """As 6 classes de buraco que a contagem de páginas não enxerga."""
    achados = []
    fora = escopo(oferta)
    todos_cards = set(cards)
    cards = {s: c for s, c in cards.items()
             if not any(s.startswith(p) for p in fora)}

    # A. card no painel sem item no manifesto -> vendido fora de todo registro
    for sku, c in cards.items():
        if not c["conteudo"]:
            continue
        if not any(parece_o_mesmo(c["title"], l["item"]) or sku == l["pasta_painel"]
                   or norm(sku) == norm(l["item"])
                   for l in linhas):
            achados.append(("A · SEM-MANIFESTO", sku,
                            f"card \"{c['title']}\" não casa com nenhum item do "
                            f"MANIFESTO-ENTREGAVEIS.md — está à venda sem registro"))

    # G. card `partial:true` num módulo já COMPLETO -> o cliente vê "conteúdo inicial ·
    #    mais em breve" e o leitor fecha com "Em atualização" num módulo inteiro.
    #    Jiu 20/10: bonus-1..4 com 5 páginas no ar e promessa 4, `partial:true` desde o
    #    MVP — parecia "em construção" pra quem pagou. A contagem de páginas não vê isso.
    for sku, c in cards.items():
        if not c.get("partial") or not c["conteudo"]:
            continue
        alvo = next((l for l in linhas
                     if parece_o_mesmo(c["title"], l["item"]) or sku == l["pasta_painel"]
                     or norm(sku) == norm(l["item"])), None)
        if not alvo or not alvo["prometido"]:
            continue
        if alvo["publicado"] >= alvo["prometido"]:
            achados.append(("H · PARCIAL FALSO", sku,
                            f"card `partial:true` com {alvo['publicado']}/{alvo['prometido']} "
                            f"páginas no ar — leitor mostra \"conteúdo inicial · mais em breve\" "
                            f"e fecha com \"Em atualização\" num módulo completo"))

    # B. pages[] × disco: imagem quebrada (card aponta pra arquivo que não existe)
    #    e página órfã (arquivo publicado e fora do menu = cliente nunca vê).
    #    Comparação SEM extensão: no Tarot cada página sai em .jpg E .webp e o card
    #    lista só um — por caminho completo toda página virava "órfã" (falso positivo).
    base = painel_de(oferta)
    for sku, c in cards.items():
        if not c["conteudo"]:
            continue
        for ref in c["pages"]:
            if not os.path.exists(os.path.join(base, ref)):
                achados.append(("B · QUEBRADA", sku, f"{ref} — card aponta e o arquivo não existe"))
        # Órfã por card: arquivo no disco e fora do `pages:` do card (cliente nunca vê).
        # Comparação SEM extensão (no Tarot a página sai em .jpg E .webp e o card lista um).
        if c["pages"]:
            no_menu = {os.path.splitext(p)[0] for p in c["pages"]}
            disco = set()
            alvo = os.path.join(base, "conteudo", sku)
            if os.path.isdir(alvo):
                for root, _, files in os.walk(alvo):
                    if os.path.basename(root) in ("original", "pdf"):
                        continue
                    for f in files:
                        if f.lower().endswith(IMG_EXT):
                            rel = os.path.relpath(os.path.join(root, f), base).replace(os.sep, "/")
                            disco.add(os.path.splitext(rel)[0])
            for f in sorted(disco - no_menu):
                achados.append(("B · ÓRFÃ", sku, f"{f}.* — publicada mas fora do pages[] do card"))
    # Órfã do PRINCIPAL: o menu dele sai de PRINCIPAL_CATEGORIES (categoria), não do
    # `pages:` do card — o check por card o pulava inteiro (medido 16/10/2026). Só roda
    # quando o menu é LITERAL (evita falso positivo em menu gerado por Array.from/map,
    # ex.: Tarot guia-flash/bonus-3).
    achados.extend(principal_fora_do_menu(oferta))

    # C. sku do card que o servidor NEM CITÁ -> o comprador paga e nada libera
    todos, concedidos = caminhos_entrega(oferta)
    if todos is None:
        achados.append(("C · SEM-CHECAGEM", "-", "site/server/index.mjs não encontrado — entrega não conferida"))
    else:
        for sku, c in cards.items():
            if not c["conteudo"] or sku in todos:
                continue
            achados.append(("C · SEM-ENTREGA", sku,
                            "sku do card não aparece em nenhum mapa do servidor "
                            "(webhook responde no-known-product e o cliente fica sem acesso)"))

    # D. sku que o webhook concede e que nenhum item do manifesto cobre
    if concedidos:
        mapeados = {l["pasta_painel"] for l in linhas if l["pasta_painel"]}
        for s in sorted(concedidos):
            # só sku de verdade: o regex de mapa pega string de comentário também
            # ("Mapa do Tarot - Área de Membros" saiu como sku 15/10)
            if not re.fullmatch(r"[a-z][\w-]*", s or "") or "-" not in s:
                continue
            if s in mapeados or s in todos_cards or any(s.startswith(p) for p in fora):
                continue
            achados.append(("D · ENTREGA-SÓ", s,
                            "webhook concede este sku e não existe card nem item do manifesto — "
                            "comprador antigo com acesso que ninguém vê"))

    # E. gerou mas não subiu: arquivo de página no disco e fora do git (ver docstring)
    dep = checar_deploy(oferta)
    if dep is None:
        achados.append(("E · SEM-CHECAGEM", "-",
                        "site/ não é repositório git — deploy não conferido (gerar ≠ publicar)"))
    else:
        achados.extend(dep)

    # F. lista de páginas do card corrompida no index.html (ver docstring)
    achados.extend(menu_corrompido(oferta, cards))
    return achados


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("oferta")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--so-gap", action="store_true")
    ap.add_argument("--retomar", action="store_true", help="próximo passo de produção de cada item")
    ap.add_argument("--lote", type=int, default=10, help="páginas por item no --retomar")
    ap.add_argument("--registrar", action="store_true",
                    help="escreve o estado no STATUS.md da oferta e na linha dela no STATUS.md da raiz")
    a = ap.parse_args()

    oferta = a.oferta.rstrip("/")
    linhas, paineis = auditar(oferta)
    if not linhas:
        print(f"AUDIT-SKIP {oferta}: sem MANIFESTO-ENTREGAVEIS.md legível em produto/")
        return 2
    cards = cards_do_painel(oferta)
    buracos = checar_buracos(oferta, linhas, cards)
    caminho = escrever_yaml(oferta, linhas, buracos)

    if a.json:
        print(json.dumps({"itens": linhas, "buracos": buracos},
                         ensure_ascii=False, indent=2))
        return 0

    print(f"Oferta: {os.path.basename(oferta)}   registro: {caminho}")
    print(f"{'item':<52}{'prom':>6}{'txt':>6}{'pub':>6}{'falta':>7}  situação")
    for l in linhas:
        if a.so_gap and l["situacao"] == "COMPLETO":
            continue
        nome = l["item"][:50]
        marca_txt = {"ok": "ok", "n/a": " - "}
        print(
            f"{nome:<52}{str(l['prometido']):>6}{marca_txt.get(l['texto'], 'NÃO'):>6}"
            f"{l['publicado']:>6}{l['falta']:>7}  {l['situacao']}"
        )
    vazios = [l for l in linhas if l["situacao"] == "VAZIO"]
    sem_txt = [l for l in linhas if l["texto"] not in ("ok", "n/a")]
    print(f"\nItens: {len(linhas)} | VAZIO: {len(vazios)} | sem texto: {len(sem_txt)} | "
          f"total a gerar: {sum(l['falta'] for l in linhas)} páginas | buracos: {len(buracos)}")
    if buracos:
        print(f"⚠️  {len(buracos)} BURACO(S) A–H abaixo — NÃO reportar a oferta como "
              f"completa sem resolvê-los")
    if colisores:
        detalhe = ", ".join(f"{d}: {n}" for d, n in sorted(colisores.items()))
        print(f"\nAVISO numeração ambígua ({detalhe}) — "
              f"duas ou mais páginas DIFERENTES disputam o MESMO número "
              f"(ex.: pagina-01-simbologia e pagina-001-tensao). São páginas diferentes, "
              f"todas no ar; renomear a família antiga para 3 dígitos com número livre "
              f"quando for reindexar. (jpg + webp da MESMA página não entra mais aqui.)")
    if buracos:
        print("\nBURAÇOS INVISÍVEIS (a contagem de páginas não pega — corrigir antes de gerar)")
        for tipo, sku, det in buracos:
            print(f"  {tipo:<20} {sku:<22} {det}")
    if not buracos and cards:
        print(f"\nChecagens A–H limpas: {len(cards)} card(s) no /painel × manifesto, "
              f"pages[] × disco, sku × webhook, deploy (git) e menu (index.html).")
    if a.retomar:
        retomar(oferta, linhas, a.lote)
    if a.registrar:
        raiz = os.path.dirname(os.path.dirname(os.path.abspath(oferta)))
        sp, rp = registrar(raiz, oferta, linhas, buracos)
        print(f"\nregistrado: {sp}" + (f" + {rp}" if os.path.exists(rp) else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())