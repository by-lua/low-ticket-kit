#!/usr/bin/env python3
"""Recomprime os .webp de uma pasta img/ de página (passo final antes do deploy).

Uso: python3 otimizar-imagens.py <site/img> [--q 75] [--backup <pasta>]

Regras (aprendidas no <Oferta Exemplo>, 06/11/2026: 4,5 MB -> 3,2 MB):
- Só .webp; qualidade 75 (selos/logos: 85), method 6, mesma dimensão.
- Só grava se ganhar >= 10% (páginas de calendário/texto raramente ganham: ficam como estão).
- Não toca jpg/png de img/checkout/ (a Hotmart já usa) nem fonts/.
- Backup dos originais em --backup (default: <img>/../.img-backup, fora do deploy).
"""
import io, os, shutil, sys
from PIL import Image

args = sys.argv[1:]
if not args:
    sys.exit(__doc__)
root = args[0]
q = int(args[args.index('--q') + 1]) if '--q' in args else 75
bk = args[args.index('--backup') + 1] if '--backup' in args else os.path.join(os.path.dirname(os.path.abspath(root)), '.img-backup')
tb = ta = 0
for r, _, fs in os.walk(root):
    if 'checkout' in r.split(os.sep) or 'fonts' in r.split(os.sep):
        continue
    for f in sorted(fs):
        if not f.endswith('.webp'):
            continue
        p = os.path.join(r, f)
        rel = os.path.relpath(p, root)
        b = os.path.getsize(p)
        os.makedirs(os.path.dirname(os.path.join(bk, rel)), exist_ok=True)
        if not os.path.exists(os.path.join(bk, rel)):
            shutil.copy2(p, os.path.join(bk, rel))
        im = Image.open(os.path.join(bk, rel))
        buf = io.BytesIO()
        im.save(buf, 'WEBP', quality=85 if any(k in f for k in ('selo', 'logo')) else q, method=6)
        a = b
        if buf.tell() < b * 0.9:
            open(p, 'wb').write(buf.getvalue())
            a = buf.tell()
        tb += b
        ta += a
        print(f'{rel}: {b // 1024} -> {a // 1024} KB')
print(f'TOTAL {tb // 1024} -> {ta // 1024} KB')
