#!/usr/bin/env python3
"""gerar-prompts.py <roteiro.json> <pasta-do-projeto>

Escreve, para cada persona P e cena K:
  PROMPTS/img-cena-P-K.txt      prompt de imagem (cena 2 usa a 1 como referencia)
  PROMPTS/vid-cena-P-K.txt      prompt de video completo
  PROMPTS/vid-cena-P-K-short.txt   versao <2500 chars (obrigatoria no Veo)

Formato do roteiro.json: ver referencia no SKILL.md.
"""
import json, os, re, sys

MOUTH = ("MOUTH AND TEETH: her mouth is slightly open, caught mid-sentence as if she has just "
"started speaking, and her upper teeth are clearly and naturally visible. A complete, "
"even upper row of natural off-white enamel, matte, age-appropriate, slightly imperfect "
"but healthy. This is NOT a smile: no wide grin, no raised cheeks, no squinting — just "
"a relaxed talking mouth with the teeth showing.")

LOOK = ("Shot on 35mm, natural light, shallow depth of field, vertical 9:16 story format, "
"amateur phone footage look, slight grain, no studio lighting.")

FACE = ("natural evenly exposed face, no blown-out highlights on the skin, no overexposure, "
"soft natural skin tones, visible pores and fine lines, natural skin texture, relaxed "
"expression, no exaggerated expression, no wide grin, no raised eyebrows, no squinting, "
"no forced pose, candid unposed look. Still frame, subject at rest, not mid-gesture.")

NOSTOCK = ("no beauty retouching, no skin smoothing, no plastic skin, no airbrushing, no stock photo "
"look, no perfect studio lighting. Grounded documentary realism, real ordinary objects, "
"natural imperfections, no surreal elements, no decorative clutter.")

NEG_IMG = ("no brand names, no brand logos, no legible printed text, no text overlay, no captions, "
"no watermark, no UI overlay, closed mouth, sealed lips, teeth hidden, teeth not visible, "
"lips pressed together, posed static smile.")

NEG_VID = ("NEGATIVE: morphing, warping, melting, extra fingers, deformed hands, objects appearing out of "
"nowhere, identity change, face swap, glitch, text overlay, captions, subtitles, watermark, "
"background music, unsynced lips, frozen mannequin stillness, off-screen narrator, voice-over, "
"different voice, missing teeth, silver tooth, metallic teeth, gold tooth, yellow teeth, "
"crooked teeth, denture look.\n")


def img_prompt(p, mouth, ref=False, pron="she"):
    cab = (f"Same person as in the attached reference image: {p['char']}, same face, same age, same hair, "
           f"same clothes, same location and lighting. Only change: the framing is slightly tighter — a "
           f"closer medium shot from chest to top of head. {pron.capitalize()} looks directly into the "
           f"camera, calm neutral expression, speaking."
           if ref else
           f"A single vertical 9:16 photograph. {p['char']}, {p['scene']}, calm neutral expression, speaking.")
    return f"""{cab}

{mouth}

{LOOK}

Only these objects in the scene: {p['objs']}.

{FACE}

{NOSTOCK}

{p['ban']}. {NEG_IMG}

One single photograph only — not a grid, not a collage, not multiple poses.
"""


def vid_prompt(p, k, fala, pron, poss, short=False):
    frame = ("locked-off static medium shot, framing from mid-torso to top of head, camera at eye level"
             if k == 1 else
             "locked-off static closer medium shot, framing from chest to top of head, camera at eye level")
    if short:
        act = (f"ACTION: {pron.capitalize()} stays in place and speaks straight to camera, giving a personal "
               f"testimonial calmly, picking nothing up. Continuous natural micro-movement: {pron} blinks, "
               f"breathes visibly, {poss} shoulders settle with body weight, {poss} head tilts a fraction on "
               f"key words, {poss} hands rest with natural weight.")
        voice = re.sub(r" (No echo|Delivery:).*", "", p['voice'])
        voice = voice.replace(", brief pauses between thoughts", "").replace(", never bright, never salesy", "")
        cont = ("CONTINUITY AND PHYSICS: Everything stays physically consistent. The scene contains ONLY: "
                f"{p['objs']}. No new objects appear or multiply. Hands keep five fingers, correct anatomy. "
                "Same identity, age and features throughout — no morphing, no face swap. Clothing and hair "
                "exactly as in the reference image. Background static. Teeth stay natural the whole clip: "
                "complete rows, off-white matte enamel, aligned, no missing, metallic, gold, yellow or "
                "crooked teeth. Real-world physics. Grounded documentary realism. Vertical 9:16.\n")
        neg = NEG_VID
    else:
        act = (f"ACTION: {pron.capitalize()} stays in the same position and speaks directly to the camera, "
               f"giving a personal testimonial in a calm everyday way. {pron.capitalize()} does not pick "
               f"anything up and does not gesture widely. Continuous natural micro-movement throughout: "
               f"{pron} blinks, breathes visibly, {poss} shoulders settle with the weight of {poss} body, "
               f"{poss} head tilts a fraction on key words, {poss} hands rest with natural weight.")
        voice = p['voice']
        cont = ("CONTINUITY AND PHYSICS: Everything stays physically consistent and natural for the entire "
                f"clip. The scene contains ONLY the objects visible in the reference image: {p['objs']}. No "
                "new objects appear, nothing materializes, grows, multiplies or fades in. Objects keep their "
                "exact shape, size, color and position. Hands keep exactly five fingers, correct anatomy, no "
                "extra limbs, no fusing, no melting. The face keeps the same identity, same age, same "
                "features throughout — no morphing, no drifting, no face swap. Clothing, hair and jewelry "
                "stay exactly as in the reference image. The background stays static and stable, no warping, "
                "no shifting walls. Teeth stay natural the whole clip: complete rows, off-white matte "
                "enamel, aligned, no missing, metallic, silver, gold, yellow, stained or crooked teeth, no "
                "crown, no cap. Real-world physics, natural human motion. Grounded documentary realism. "
                "Vertical 9:16.\n")
        neg = NEG_VID.rstrip("\n") + " duplicated objects, extra limbs, surreal artifacts, unnatural zoom.\n"
    return f"""CHARACTER: {p['char']}, must stay the same for the whole clip.
CAMERA: {frame}, no camera movement, no zoom.
{act}
DIALOGUE: {pron} speaks on camera, in {p['idioma']}. {poss.capitalize()} lips must be accurately synced to these exact words: "{fala}"
  {poss.capitalize()} mouth moves visibly and continuously for the ENTIRE spoken line, from the first syllable to the last. The audio must never play while {poss} mouth is closed or still. {pron.capitalize()} finishes speaking before the clip ends.
{voice}
AUDIO: {p['amb']} only. No background music, no score, no sound effects, no subtitles.
{cont}{neg}"""


def main():
    roteiro = json.load(open(sys.argv[1]))
    proj = sys.argv[2]
    os.makedirs(f"{proj}/PROMPTS", exist_ok=True)
    for d in ("IMG", "VIDEO"):
        os.makedirs(f"{proj}/{d}", exist_ok=True)
    problemas = []
    for i, p in enumerate(roteiro["personas"], 1):
        pron = "he" if p.get("masculino") else "she"
        poss = "his" if p.get("masculino") else "her"
        mouth = MOUTH.replace("her ", poss + " ").replace("she ", pron + " ")
        for k in (1, 2):
            open(f"{proj}/PROMPTS/img-cena-{i}-{k}.txt", "w").write(
                img_prompt(p, mouth, ref=(k == 2), pron=pron))
            fala = p["falas"][k - 1]
            n = len(fala.split())
            if not 11 <= n <= 16:
                problemas.append(f"cena {i}-{k}: {n} palavras (faixa segura 11-16)")
            for short in (False, True):
                t = vid_prompt(p, k, fala, pron, poss, short)
                suf = "-short" if short else ""
                open(f"{proj}/PROMPTS/vid-cena-{i}-{k}{suf}.txt", "w").write(t)
                if short and len(t) >= 2500:
                    problemas.append(f"cena {i}-{k}: prompt short {len(t)} chars (teto 2500)")
            print(f"cena {i}-{k}: {n} palavras")
    if problemas:
        print("\nPROBLEMAS — corrija antes de gerar:")
        for x in problemas:
            print(" -", x)
        sys.exit(1)
    print("\nprompts OK")


if __name__ == "__main__":
    main()
