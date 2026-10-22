#!/usr/bin/env python3
"""tight.py <clipe.mp4> -> imprime lista de segmentos (ini,fim) a manter,
cortando silencio de cabeca, de cauda e pausas internas longas."""
import subprocess, sys, re
f=sys.argv[1]
HEAD_PAD=0.10; TAIL_PAD=0.30; MAXGAP=0.16; MINGAP=0.30
out=subprocess.run(["ffmpeg","-i",f,"-af","silencedetect=noise=-28dB:d=0.15","-f","null","-"],
                   capture_output=True,text=True).stderr
dur=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f],
                   capture_output=True,text=True).stdout.strip())
sil=[]
cur=None
for m in re.finditer(r'silence_(start|end): ([0-9.]+)', out):
    k,v=m.group(1),float(m.group(2))
    if k=='start': cur=v
    elif cur is not None: sil.append((cur,v)); cur=None
if cur is not None: sil.append((cur,dur))
# fala = complemento dos silencios
segs=[]; t=0.0
for a,b in sil:
    if a-t>0.05: segs.append([t,a])
    t=b
if dur-t>0.05: segs.append([t,dur])
if not segs: print(f"0 {dur:.3f}"); sys.exit()
# padding nas pontas do bloco falado
segs[0][0]=max(0.0, segs[0][0]-HEAD_PAD)
segs[-1][1]=min(dur, segs[-1][1]+TAIL_PAD)
# junta segmentos separados por pausa curta; encurta pausa longa
merged=[segs[0]]
for s in segs[1:]:
    gap=s[0]-merged[-1][1]
    if gap < MINGAP:
        merged[-1][1]=s[1]          # pausa curta: mantem inteira
    else:
        merged[-1][1]+=MAXGAP/2     # deixa um respiro minimo
        s[0]-=MAXGAP/2
        merged.append(s)
out=[(max(0.0,a),min(dur,b)) for a,b in merged]
out=[(a,b) for a,b in out if b-a>=0.35]
if not out: out=[(0.0,dur)]
for a,b in out:
    print(f"{a:.3f} {b:.3f}")
