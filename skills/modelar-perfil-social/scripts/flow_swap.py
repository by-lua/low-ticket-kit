#!/usr/bin/env python3
"""Troca a personagem de um vídeo pelo Omni Flash do Flow (vídeo + foto da persona no composer).

uso (com o python do gflow):
  GPY=~/.local/share/uv/tools/gflow-cli/bin/python
  DISPLAY=:1 $GPY -I flow_swap.py --video original.mp4 --persona rosa.jpg -- \
      video t2v --profile flow-gflow-2 --project <id> --model omni-flash --duration 8 --out-dir <dir> "<prompt>"

Reaproveita o anexo pelo "+" do tiktok-shop/scripts/gflow_ref.py: em vez do frame inicial,
anexa o VÍDEO original e a FOTO da persona antes de gerar.
"""
import importlib.util
import sys
from pathlib import Path

GREF = Path.home() / ".claude/skills/tiktok-shop/scripts/gflow_ref.py"

args = sys.argv[1:]
extra = []
while args and args[0] in ("--video", "--persona", "--ref"):
    extra.append(Path(args[1]).resolve())
    args = args[2:]
if args and args[0] == "--":
    args = args[1:]
if not extra or not args:
    sys.exit(__doc__)

spec = importlib.util.spec_from_file_location("gflow_ref", GREF)
gref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gref)  # aplica os patches do composer agente

_orig = gref._orig_run_video


async def _run_video(page, request, **kw):
    gref._pending[:] = list(extra)
    return await _orig(page, request, **kw)


gref.agent.run_agent_video = _run_video

from gflow_cli.cli import main  # noqa: E402

sys.argv = ["gflow", *args]
sys.exit(main())
