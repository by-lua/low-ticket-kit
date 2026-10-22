#!/usr/bin/env python3
"""Legenda karaokê: alinhamento forçado roteiro+áudio -> words.json (Remotion).

NÃO é whisper. Usa ctc-forced-aligner (wav2vec2/MMS, multilíngue): o texto é o
roteiro conhecido, o modelo só descobre ONDE cada palavra cai no áudio.

Uso:
  .venv/bin/python align.py AUDIO_OU_VIDEO ROTEIRO.txt -o words.json [--lang por]

Saída: [{start, end, words:[{text,start,end}]}]  (formato do .jsx canônico)
  - linha = 1-3 palavras, quebra em pontuação e em pausa > PAUSA_QUEBRA
  - linha só existe enquanto é falada (+ HOLD curto); nas pausas, tela limpa
"""
import argparse, json, re, subprocess, sys, tempfile, os

MAX_PALAVRAS = 3
PAUSA_QUEBRA = 0.30   # pausa entre palavras que força linha nova (s)
HOLD = 0.15           # quanto a linha fica depois da última palavra (s)
COLA = 0.30           # gap menor que isso: palavra ativa segue amarela até a próxima


def numeros_por_extenso(palavra, lang):
    if not re.search(r"\d", palavra):
        return palavra
    try:
        from num2words import num2words
        return re.sub(r"\d+", lambda m: " " + num2words(int(m.group()), lang="pt_BR" if lang == "por" else "en") + " ", palavra).strip()
    except Exception:
        return palavra


def extrai_wav(src):
    fd, wav = tempfile.mkstemp(suffix=".wav"); os.close(fd)
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", src, "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
    return wav


def alinha(wav, palavras_alinhar, lang):
    import torch
    from ctc_forced_aligner import (load_audio, load_alignment_model, generate_emissions,
                                    preprocess_text, get_alignments, get_spans, postprocess_results)
    model, tok = load_alignment_model("cpu", dtype=torch.float32)
    audio = load_audio(wav, model.dtype, model.device)
    emissions, stride = generate_emissions(model, audio, batch_size=4)
    tokens, text = preprocess_text(" ".join(palavras_alinhar), romanize=True, language=lang)
    segs, scores, blank = get_alignments(emissions, tokens, tok)
    spans = get_spans(tokens, segs, blank)
    return postprocess_results(text, spans, stride, scores)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio"); ap.add_argument("roteiro"); ap.add_argument("-o", "--out", default="words.json")
    ap.add_argument("--lang", default="por")
    a = ap.parse_args()

    exibir = open(a.roteiro, encoding="utf-8").read().split()
    # cada palavra exibida vira 1+ tokens de alinhamento (número por extenso); guarda o mapa
    alinhar, dono = [], []
    for i, p in enumerate(exibir):
        for t in numeros_por_extenso(p, a.lang).split():
            alinhar.append(t); dono.append(i)

    wav = extrai_wav(a.audio)
    try:
        ts = alinha(wav, alinhar, a.lang)
    finally:
        os.remove(wav)
    if len(ts) != len(alinhar):
        sys.exit(f"alinhador devolveu {len(ts)} palavras, esperava {len(alinhar)}")

    words = []
    for i, p in enumerate(exibir):
        parte = [ts[k] for k in range(len(ts)) if dono[k] == i]
        words.append({"text": p, "start": round(parte[0]["start"], 3), "end": round(parte[-1]["end"], 3),
                      "score": round(min(x.get("score", 0) for x in parte), 3)})

    # palavra ativa não pisca em gap curto
    for w, nx in zip(words, words[1:]):
        if 0 < nx["start"] - w["end"] < COLA:
            w["end"] = nx["start"]

    linhas, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nx = words[i + 1] if i + 1 < len(words) else None
        quebra = (len(cur) >= MAX_PALAVRAS or re.search(r"[.,!?;:…]$", w["text"])
                  or nx is None or nx["start"] - w["end"] > PAUSA_QUEBRA)
        if quebra:
            fim = cur[-1]["end"] + HOLD
            if nx is not None:
                fim = min(fim, nx["start"])
            linhas.append({"start": cur[0]["start"], "end": round(fim, 3),
                           "words": [{"text": x["text"], "start": x["start"], "end": x["end"]} for x in cur]})
            cur = []

    json.dump(linhas, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    fracas = [w["text"] for w in words if w["score"] < -5]
    print(f"{len(words)} palavras, {len(linhas)} linhas -> {a.out}")
    if fracas:
        print("confiança baixa (conferir):", " ".join(fracas))


if __name__ == "__main__":
    main()
