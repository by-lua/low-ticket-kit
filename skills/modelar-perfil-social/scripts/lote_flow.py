#!/usr/bin/env python3
"""Gera um lote de vídeos modelados no Google Flow, um vídeo por vez, no ritmo seguro.

uso: python3 lote_flow.py plano.json [--so-imagens]   (--so-imagens: gera só as imagens das cenas pra dona validar; rode sem a flag depois)

plano.json:
{
  "profile": "flow-gflow-2", "project": "<uuid do projeto Flow>",
  "persona_ref": "/abs/rosa-jefa-B.jpg",          # rosto + roupa fixos
  "videos_dir": "/abs/.../02-videos",
  "scene_prefix": "texto fixo colado antes de toda cena (persona canon)",
  "videos": [
    {"slug": "V02-sala-boxe", "ref_video": "/abs/original.mp4", "ref_frame": "/abs/frame.jpg",
     "duration": 6, "scene": "prompt da imagem-base", "motion": "prompt do movimento",
     "line1": "texto story linha 1", "line2": "linha 2|😎", "caption": "legenda do post"},
    {"slug": "V08-duas-cenas", "ref_video": "...", "line1": "...", "line2": "...", "caption": "...",
     "scenes": [{"ref_frame": "quadro cena 1", "scene": "...", "motion": "...", "duration": 10},
                {"ref_frame": "quadro cena 2", "scene": "...", "motion": "...", "duration": 10, "cut": 8.3}]}
  ]
}
Para cada vídeo: i2i (persona + quadro do original) -> pausa -> i2v -> pausa -> montar.sh.
Para no primeiro erro (bloqueio = esfriar 45 min, nunca insistir). Vídeo já pronto é pulado.
"""
import json, os, random, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
FLOW = Path.home() / ".claude/skills/flow-video-playwright/scripts/flow.sh"  # ritmo/fila/freio compartilhados
ENV = {**os.environ, "DISPLAY": ":1", "GFLOW_CLI_DEBUG_TRACEBACK": "1"}


def log(msg):
    print(time.strftime("[%H:%M:%S] ") + msg, flush=True)


def pause():
    log("pausa (o flow.sh controla o ritmo entre envios)")


def gflow(args, cwd, profile):
    r = subprocess.run(["bash", str(FLOW), *args], cwd=cwd, env=ENV,
                       capture_output=True, text=True)
    tail = "\n".join((r.stdout + r.stderr).strip().splitlines()[-4:])
    if r.returncode != 0:
        raise RuntimeError(f"gflow exit {r.returncode}: {tail}")
    return tail


def newest(d, ext, since):
    c = [p for p in Path(d).glob(f"*{ext}") if p.stat().st_mtime >= since]
    if not c:
        raise RuntimeError(f"nada novo {ext} em {d}")
    return max(c, key=lambda p: p.stat().st_mtime)


def main():
    plan = json.loads(Path(sys.argv[1]).read_text())
    so_imagens = "--so-imagens" in sys.argv  # dona valida as imagens antes de gastar com vídeo
    prof, proj = plan["profile"], plan["project"]
    first = True
    for v in plan["videos"]:
        vd = Path(plan["videos_dir"]) / v["slug"]
        mid = vd / "intermediarios"
        mid.mkdir(parents=True, exist_ok=True)
        final = vd / f"{v['slug']}.mp4"
        if final.exists():
            log(f"{v['slug']}: já existe, pulando")
            continue
        (vd / "LEGENDA.txt").write_text(v["caption"] + "\n")
        # Regra da dona: SEMPRE imagem da cena no Flow antes do vídeo; várias cenas = uma imagem por cena.
        scenes = v.get("scenes") or [{k: v[k] for k in ("ref_frame", "scene", "motion", "duration", "cut", "outfit") if k in v}]
        multi = len(scenes) > 1
        clip_args = []
        for n, sc in enumerate(scenes, 1):
            sfx = f"_{n}" if multi else ""
            base = mid / f"base{sfx}.jpg"
            outfit = sc.get("outfit", v.get("outfit"))
            persona = Path(sc.get("persona_ref", v.get("persona_ref", plan["persona_ref"])))
            outfit_list = plan.get("base_outfit", "")
            if outfit:
                # Roupa nova (dona 22/10): troca a roupa na IMAGEM DA PERSONAGEM sozinha, ANTES da cena.
                # A variação aprovada vira a imagem 1 da cena, como sempre.
                var = persona.parent / "variantes" / f"{v['slug']}{sfx}.jpg"
                var.parent.mkdir(exist_ok=True)
                if not var.exists():
                    if not first:
                        pause()
                    first = False
                    t0 = time.time()
                    log(f"{v['slug']}: persona com roupa nova (i2i só da persona)")
                    gflow(["image", "i2i", "--project", proj, "--aspect", "9:16", "-n", "1", "--ref", str(persona),
                           "--out", str(var.parent), plan["outfit_prompt"].replace("{outfit}", outfit)], mid, prof)
                    newest(var.parent, ".jpg", t0).rename(var)
                persona, outfit_list = var, outfit
            if not base.exists():
                if not first:
                    pause()
                first = False
                t0 = time.time()
                log(f"{v['slug']}: imagem da cena {n}/{len(scenes)} (i2i, persona + quadro)")
                gflow(["image", "i2i", "--project", proj, "--aspect", "9:16", "-n", "1", "--ref", str(persona),
                       *(["--ref", sc["ref_frame"]] if sc.get("ref_frame") else []), "--out", str(mid),
                       plan.get("scene_prefix", "").replace("{outfit_list}", outfit_list) + " " + sc["scene"]
                       + plan.get("scene_suffix", "")], mid, prof)
                newest(mid, ".jpg", t0).rename(base)
            clip = mid / f"clip{sfx}.mp4"
            if so_imagens:
                log(f"{v['slug']}: imagem pronta pra validar: {base}")
                continue
            if not clip.exists():
                if not first:
                    pause()
                first = False
                t0 = time.time()
                log(f"{v['slug']}: clipe da cena {n}/{len(scenes)} {sc['duration']}s (i2v)")
                gflow(["video", "i2v", "--project", proj, "--initial-frame", str(base),
                       "--model", "omni-flash", "--duration", str(sc["duration"]), "--out-dir", str(mid),
                       sc["motion"]], mid, prof)
                newest(mid, ".mp4", t0).rename(clip)
            clip_args.append(f"{clip}@{sc['cut']}" if sc.get("cut") else str(clip))
        if so_imagens:
            continue
        dur = v.get("final_duration", sum(float(sc.get("cut", sc["duration"])) for sc in scenes))
        out = subprocess.run(["bash", str(HERE / "montar.sh"), str(final), v["ref_video"], str(dur),
                              v["line1"], v["line2"], *clip_args], capture_output=True, text=True)
        if out.returncode != 0:
            raise RuntimeError(f"montagem falhou: {out.stderr[-400:]}")
        log(f"{v['slug']}: PRONTO {final} ({out.stdout.strip()})")
    log("LOTE COMPLETO")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"PAROU: {e}")
        sys.exit(1)
