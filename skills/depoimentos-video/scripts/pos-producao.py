#!/usr/bin/env python3
"""Pos-producao dos criativos: corta respiracao, remove fala repetida,
acelera 1.15x e queima legenda (Jost, dourada no destaque)."""
import json, os, re, subprocess, sys, unicodedata
from difflib import SequenceMatcher

SPEED = float(os.getenv("SPEED", "1.22"))
GAP_MAX = 0.50        # silencio maior que isso vira corte
PAD_IN, PAD_OUT = 0.16, 0.34
DUP_RATIO = 0.82      # similaridade que caracteriza fala repetida
MARGIN_V = 470        # px do rodape (safe area 9:16)
TITULO_MV = 210       # px do topo — abaixo do header dos stories
TITULO = os.getenv("TITULO", "")   # texto no topo, opcional
TITULO_DUR = float(os.getenv("TITULO_DUR", "5"))  # segundos no ar; 0 = o video todo
NOME_MV = 390         # px do rodape — ABAIXO da legenda (que fica em 470)
NOME_DUR = 2.6        # o nome entra no comeco da fala da pessoa e sai
FADE = 350            # ms de fade in/out do nome
# NOMES: JSON [{"t":0,"e":16,"txt":"Mariana, Recife - PE"}, ...] em tempos do
# video de ENTRADA (antes do corte e do 1.15x). O script remapeia sozinho.
NOMES = json.loads(os.getenv("NOMES", "[]"))
# Duracao de cada clipe no video montado. O whisper as vezes ancora a primeira
# palavra de uma cena ~0,5s antes do corte, e a legenda aparece sobre a pessoa
# anterior. Com isso, toda palavra que cruza um corte e empurrada para ele.
CENA_DUR = float(os.getenv("CENA_DUR", "0"))   # 0 = desliga
# CORTES: limites de cena explicitos em segundos, separados por virgula. Use este
# quando a montagem tem dissolve (as cenas deixam de cair em multiplos exatos).
CORTES = [float(x) for x in os.getenv("CORTES", "").replace(" ", "").split(",") if x]
# Chiado/room tone do Veo: highpass tira o rumble, afftdn tira o ruido de fundo.
# nr=12 dB e um valor conservador — acima de ~18 a voz comeca a soar metalica.
DENOISE = os.getenv("DENOISE", "1") != "0"
DENOISE_F = "highpass=f=70,afftdn=nr=12:nf=-28,dynaudnorm=f=200:g=5"
FONT = "Jost"

def norm(t):
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]", "", t).strip()

def load_words(js):
    """Palavras com o indice da frase (segmento) a que pertencem."""
    words = []
    for si, seg in enumerate(js["segments"]):
        for w in seg.get("words", []):
            txt = w["word"].strip()
            if txt:
                words.append({"t": float(w["start"]), "e": float(w["end"]),
                              "w": txt, "s": si})
    return words


# ---------------------------------------------------------------- moeda
# O whisper normaliza fala de dinheiro para digitos ("R$ 27,90", "14.900 pesos").
# Em legenda de criativo isso lê como preço escrito, e nao como a pessoa falou —
# alem de destoar do resto da frase. Aqui volta para extenso, mantendo os
# timestamps: o intervalo do token original e dividido entre as palavras novas.
UNI = ["zero","um","dois","três","quatro","cinco","seis","sete","oito","nove","dez",
       "onze","doze","treze","quatorze","quinze","dezesseis","dezessete","dezoito","dezenove"]
DEZ = ["","","vinte","trinta","quarenta","cinquenta","sessenta","setenta","oitenta","noventa"]
CEM = ["","cento","duzentos","trezentos","quatrocentos","quinhentos","seiscentos",
       "setecentos","oitocentos","novecentos"]

def extenso(n):
    n = int(n)
    if n < 20: return UNI[n]
    if n < 100:
        d, r = divmod(n, 10)
        return DEZ[d] + (" e " + UNI[r] if r else "")
    if n == 100: return "cem"
    if n < 1000:
        c, r = divmod(n, 100)
        return CEM[c] + (" e " + extenso(r) if r else "")
    if n < 1000000:
        m, r = divmod(n, 1000)
        cab = "mil" if m == 1 else extenso(m) + " mil"
        if not r: return cab
        return cab + (" e " if r < 100 or r % 100 == 0 else " ") + extenso(r)
    m, r = divmod(n, 1000000)
    cab = "um milhão" if m == 1 else extenso(m) + " milhões"
    return cab + (" e " + extenso(r) if r else "")

MOEDAS = {"R$": ("reais", "centavos"), "US$": ("dólares", "centavos"),
          "$": ("pesos", "centavos"), "€": ("euros", "centavos")}

def moeda_extenso(words):
    """Expande 'R$ 27,90' -> 'vinte e sete reais e noventa centavos'."""
    out = []
    i = 0
    while i < len(words):
        w = words[i]
        txt = w["w"]
        sim = next((s for s in ("R$", "US$", "€", "$") if s in txt), None)
        num = re.sub(r"[^\d,.]", "", txt)
        nxt = words[i + 1]["w"] if i + 1 < len(words) else ""
        if not sim and re.fullmatch(r"[\d.,]+", txt) and re.match(r"(reais|pesos|d[óo]lares|euros)", nxt.lower()):
            sim = {"reais": "R$", "pesos": "$", "dólares": "US$", "dolares": "US$", "euros": "€"}[
                re.sub(r"[^a-zãóô]", "", nxt.lower())]
            num = txt
        simbolo_solto = False
        if sim and not num and re.fullmatch(r"[\d.,]+", nxt):
            num = nxt; simbolo_solto = True          # "R$" e "27,90" em tokens separados
        if not sim or not num:
            out.append(w); i += 1; continue
        moeda, cent = MOEDAS[sim]
        inteiro, _, dec = num.replace(".", "").partition(",")
        if not inteiro: out.append(w); i += 1; continue
        frase = extenso(inteiro) + " " + moeda
        if dec and int(dec.ljust(2, "0")) > 0:
            frase += " e " + extenso(dec.ljust(2, "0")) + " " + cent
        # se a palavra seguinte era a unidade falada ("reais"), ela vira redundante
        j = i + 2 if simbolo_solto else i + 1
        fim = words[j - 1]["e"]
        if j < len(words) and re.match(r"(reais|pesos|d[óo]lares|euros)", words[j]["w"].lower()):
            fim = words[j]["e"]; j += 1
        novas = frase.split()
        ini = w["t"]; passo = max((fim - ini) / len(novas), 0.06)
        for k, p in enumerate(novas):
            out.append({"t": ini + k * passo, "e": ini + (k + 1) * passo, "w": p,
                        "s": w.get("s", 0)})
        i = j
    return out


def drop_repeats(words, bounds=()):
    drop_repeats._blk = -1
    """Remove FRASES repetidas (Veo falando a mesma linha 2x).

    Compara por frase, nao por bloco: um bloco pode juntar duas frases e
    diluir a similaridade da repeticao.
    """
    order, byseg = [], {}
    for w in words:
        if w["s"] not in byseg:
            byseg[w["s"]] = []; order.append(w["s"])
        byseg[w["s"]].append(w)
    keep, cut, seen = [], [], []
    for si in order:
        # Repeticao do Veo acontece DENTRO de um clipe. Pessoas diferentes podem
        # dizer a mesma frase ("lo leo todos los dias") — comparar atraves do
        # corte de cena apaga fala legitima de outro depoente.
        ini = byseg[si][0]["t"]
        blk = sum(1 for b in bounds if b <= ini)
        if blk != drop_repeats._blk:
            drop_repeats._blk = blk
            seen = []
        txt = norm(" ".join(x["w"] for x in byseg[si]))
        dup = False
        if len(txt) > 12:
            for prev in seen[-6:]:
                # fragmento curto nao caracteriza repeticao: o whisper quebra
                # "Recomendo." + "Recomendo para qualquer um da minha idade." em
                # dois segmentos, e a regra de contencao matava a frase inteira.
                if len(prev) <= 12:
                    continue
                cont = (txt in prev or prev in txt)
                if cont and min(len(txt), len(prev)) < 0.6 * max(len(txt), len(prev)):
                    continue
                if SequenceMatcher(None, txt, prev).ratio() >= DUP_RATIO or cont:
                    dup = True; break
        if dup:
            cut.append(txt)
        else:
            seen.append(txt); keep.extend(byseg[si])
    return keep, cut

def blocks(words):
    out, cur = [], [words[0]]
    for w in words[1:]:
        if w["t"] - cur[-1]["e"] > GAP_MAX:
            out.append(cur); cur = [w]
        else:
            cur.append(w)
    out.append(cur)
    return out

def esc(t):
    return t.replace("{", "(").replace("}", ")")

def build(src, dst, workdir, tag, lang="pt"):
    os.makedirs(workdir, exist_ok=True)
    jsp = os.path.join(workdir, tag + ".json")
    if not os.path.exists(jsp):
        subprocess.run(["whisper-ctranslate2", "--model", "large-v3", "--language", lang,
                        "--word_timestamps", "True", "--output_format", "json",
                        "--output_dir", workdir, src], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        got = os.path.join(workdir, os.path.splitext(os.path.basename(src))[0] + ".json")
        if got != jsp: os.replace(got, jsp)
    js = json.load(open(jsp))
    dur = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration",
                                         "-of","default=nw=1:nk=1",src]).strip())
    ws = moeda_extenso(load_words(js))
    bounds = list(CORTES)
    if not bounds and CENA_DUR > 0:
        k = 1
        while k * CENA_DUR < dur:
            bounds.append(k * CENA_DUR); k += 1
    if bounds:
        for c in bounds:
            for w in ws:
                if w["t"] < c < w["e"] or (0 < c - w["t"] < 1.0 and w["e"] > c - 0.2):
                    w["t"] = max(w["t"], c)
                    w["e"] = max(w["e"], w["t"] + 0.12)
    ws, cut = drop_repeats(ws, bounds)
    kept = blocks(ws)

    # intervalos a manter (com pad, sem estourar vizinhos)
    ivs = []
    for b in kept:
        s = max(0.0, b[0]["t"] - PAD_IN)
        e = min(dur, b[-1]["e"] + PAD_OUT)
        if ivs and s <= ivs[-1][1] + 0.05:
            ivs[-1][1] = max(ivs[-1][1], e)
        else:
            ivs.append([s, e])
    # timeline nova + palavras remapeadas
    newwords, acc = [], 0.0
    for s, e in ivs:
        for b in kept:
            for w in b:
                if s <= w["t"] < e:
                    newwords.append({"t": (acc + w["t"] - s) / SPEED,
                                     "e": (acc + min(w["e"], e) - s) / SPEED,
                                     "w": w["w"]})
        acc += e - s
    total = acc / SPEED

    # ASS
    groups, cur = [], []
    for w in newwords:
        cur.append(w)
        joined = " ".join(x["w"] for x in cur)
        if len(cur) >= 4 or len(joined) >= 20 or re.search(r"[.,!?;:]$", w["w"]):
            groups.append(cur); cur = []
    if cur: groups.append(cur)

    ass = [f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,{FONT},74,&H00FFFFFF,&H00FFFFFF,&H00190D05,&H96000000,1,0,0,0,100,100,0.6,0,1,5,2,2,110,110,{MARGIN_V},1
Style: Nom,{FONT},46,&H00FFFFFF,&H00FFFFFF,&H00190D05,&HC8000000,0,0,0,0,100,100,1.2,0,1,4,2,2,110,110,{NOME_MV},1
Style: Tit,{FONT},52,&H00FFFFFF,&H00FFFFFF,&H00000000,&HB4000000,0,0,0,0,100,100,4.0,0,3,12,0,8,90,90,{TITULO_MV},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"""]
    def ts(x):
        h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
        return f"{h}:{m:02d}:{s:05.2f}"
    for gi, g in enumerate(groups):
        gs = g[0]["t"]
        # fim do grupo encosta no inicio do proximo: sem piscada entre eventos
        ge = groups[gi + 1][0]["t"] if gi + 1 < len(groups) else g[-1]["e"] + 0.30
        ge = min(ge, g[-1]["e"] + 0.25)
        for i in range(len(g)):
            a = g[i]["t"] if i else gs
            b = g[i + 1]["t"] if i + 1 < len(g) else ge
            if b <= a:
                continue
            txt = " ".join(
                (r"{\c&H4FD8FF&}" if j == i else r"{\c&HFFFFFF&}") + esc(x["w"])
                for j, x in enumerate(g))
            ass.append(f"Dialogue: 0,{ts(a)},{ts(b)},Cap,,0,0,0,,{txt}")
    def remap(x):
        """tempo do video de entrada -> tempo na timeline nova (pos corte e speed)"""
        acc2 = 0.0
        for s, e in ivs:
            if x < s:
                return acc2 / SPEED
            if x <= e:
                return (acc2 + x - s) / SPEED
            acc2 += e - s
        return acc2 / SPEED

    for nm in NOMES:
        a, b = remap(float(nm["t"])), remap(float(nm["e"]))
        b = min(b, a + NOME_DUR)          # entra e sai, nao acompanha a fala inteira
        if b - a < 0.6:
            continue
        fx = r"{\fad(%d,%d)}" % (FADE, FADE)
        ass.append(f"Dialogue: 0,{ts(a)},{ts(b)},Nom,,0,0,0,,{fx}{esc(nm['txt'])}")
    if TITULO:
        fx = r"{\fad(400,400)}"
        tfim = total if TITULO_DUR <= 0 else min(total, TITULO_DUR)
        ass.append(f"Dialogue: 0,{ts(0)},{ts(tfim)},Tit,,0,0,0,,{fx}{esc(TITULO.upper())}")
    assp = os.path.join(workdir, tag + ".ass")
    open(assp, "w").write("\n".join(ass) + "\n")

    # ffmpeg: trim + concat + speed + legenda
    fc = []
    for i, (s, e) in enumerate(ivs):
        fc.append(f"[0:v]trim={s}:{e},setpts=PTS-STARTPTS[v{i}];"
                  f"[0:a]atrim={s}:{e},asetpts=PTS-STARTPTS[a{i}]")
    cat = "".join(f"[v{i}][a{i}]" for i in range(len(ivs)))
    fc.append(f"{cat}concat=n={len(ivs)}:v=1:a=1[vc][ac]")
    fc.append(f"[vc]setpts=PTS/{SPEED},ass='{assp}'[vo]")
    ach = f"atempo={SPEED}"
    if DENOISE:
        ach = f"{DENOISE_F},{ach}"
    fc.append(f"[ac]{ach}[ao]")
    fps = subprocess.check_output(["ffprobe","-v","error","-select_streams","v",
                                   "-show_entries","stream=r_frame_rate","-of","csv=p=0",src]).decode().strip()
    num, den = (fps.split("/") + ["1"])[:2]
    fps = str(round(int(num) / max(int(den), 1)))
    subprocess.run(["ffmpeg","-y","-i",src,"-filter_complex",";".join(fc),
                    "-map","[vo]","-map","[ao]","-c:v","libx264","-preset","medium",
                    "-crf","19","-pix_fmt","yuv420p","-r",fps,"-c:a","aac","-b:a","192k",
                    "-movflags","+faststart",dst], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"{tag}: {dur:.1f}s -> {total:.1f}s | blocos {len(kept)} | frases repetidas cortadas {len(cut)}")
    for c in cut: print(f"   dup: {c[:70]}")

if __name__ == "__main__":
    # LANG=es ./pos-producao.py video.mp4   (padrao pt)
    #
    # O workdir do cache leva o caminho do video, nao so o nome. Antes era um
    # diretorio unico com a chave no basename: BR/CRIATIVO-4.mp4 e
    # AR/CRIATIVO-4.mp4 colidiam, e o segundo a rodar reaproveitava a
    # transcricao do primeiro — legenda em portugues sobre video em espanhol,
    # com os tempos do video errado.
    lang = os.getenv("LANG_ASR", "pt")
    for src in sys.argv[1:]:
        tag = os.path.splitext(os.path.basename(src))[0]
        dst = os.path.join(os.path.dirname(src), tag + "-v2.mp4")
        key = re.sub(r"[^A-Za-z0-9]+", "-", os.path.dirname(os.path.abspath(src))).strip("-")[-60:]
        build(src, dst, os.path.join("/tmp/claude-1000/astro", key), tag, lang)
