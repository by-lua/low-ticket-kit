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
    # ⚠️ 25/10/2026: a versão instalada em ~/Developer/legenda-karaoke/.venv NÃO
    # tem get_word_stamps (nem a antiga API alta-nível) — tem a API de baixo
    # nível (load_alignment_model/load_audio/generate_emissions/preprocess_text/
    # get_alignments/get_spans/postprocess_results). Tentamos a alta-nível
    # primeiro (se algum dia a lib for atualizada com ela) e caímos pra
    # baixo-nível, que é a que funciona hoje nesta máquina. Confirmado em
    # produção (Mapa do Tarot CRIATIVO-7/30, 25/10/2026).
    try:
        from ctc_forced_aligner import get_word_stamps
        fd, roteiro_tmp = tempfile.mkstemp(suffix=".txt")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(" ".join(palavras_alinhar))
        try:
            word_stamps, _model, _lyrics = get_word_stamps(wav, roteiro_tmp)
        finally:
            os.remove(roteiro_tmp)
        return [{"start": w["start"], "end": w["end"], "score": w.get("score", 0.0)} for w in word_stamps]
    except ImportError:
        pass

    import torch
    from ctc_forced_aligner import (
        load_audio, load_alignment_model, generate_emissions,
        preprocess_text, get_alignments, get_spans, postprocess_results,
    )
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, tokenizer = load_alignment_model(device, dtype=torch.float32)
    audio_waveform = load_audio(wav, model.dtype, model.device)
    emissions, stride = generate_emissions(model, audio_waveform, batch_size=8)
    text = " ".join(palavras_alinhar)
    tokens_starred, text_starred = preprocess_text(text, romanize=True, language=lang)
    segments, scores, blank_token = get_alignments(emissions, tokens_starred, tokenizer)
    spans = get_spans(tokens_starred, segments, blank_token)
    word_stamps = postprocess_results(text_starred, spans, stride, scores)
    return [{"start": w["start"], "end": w["end"], "score": w.get("score", 0.0)} for w in word_stamps]


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
