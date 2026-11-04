#!/usr/bin/env python3
"""B-roll orgânico do TikTok, rápido (~2-3 min pra 4 termos), sem o ciclo do get-brolls.

Uso:
  broll-tiktok.py --out <pasta> [--min-views 50000] [--max-dur 90] [--top 5] [--sessao tiktok2] "termo 1" "termo 2" ...

Faz: busca cada termo no perfil logado do TikTok (agent-browser) → pega os links da página de resultados →
yt-dlp lê views/duração em paralelo (sem baixar) → filtra (views ≥ min, duração ≤ max) → baixa os melhores
em paralelo → folha de contato (4 quadros) de cada vídeo pra conferir texto queimado → ORIGEM.md com a fonte.
A pasta de saída deve ficar em PROJETOS-MIDIA (mídia de terceiro) com symlink na oferta.
"""
import argparse, json, subprocess, sys, time, urllib.parse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def sh(cmd, timeout=120):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def buscar(sessao, termo):
    url = 'https://www.tiktok.com/search/video?q=' + urllib.parse.quote(termo)
    sh(['agent-browser', '--session', sessao, 'open', url], 60)
    time.sleep(6)
    for _ in range(2):  # 2 rolagens = ~40-60 resultados
        sh(['agent-browser', '--session', sessao, 'eval', 'window.scrollBy(0, 4000)'], 30)
        time.sleep(2)
    js = 'JSON.stringify([...new Set([...document.querySelectorAll("a[href*=\\"/video/\\"]")].map(a=>a.href.split("?")[0]))])'
    out = sh(['agent-browser', '--session', sessao, 'eval', js], 30).stdout.strip()
    try:
        v = json.loads(out)
        return json.loads(v) if isinstance(v, str) else v
    except Exception:
        print(f'  ! não li resultados de "{termo}" (login/captcha?): {out[:120]}', file=sys.stderr)
        return []


def meta(url):
    r = sh(['yt-dlp', '--skip-download', '--no-warnings', '-J', url], 60)
    try:
        d = json.loads(r.stdout)
        return {'url': url, 'views': d.get('view_count') or 0, 'dur': d.get('duration') or 0,
                'autor': d.get('uploader') or d.get('channel') or '?', 'id': d.get('id'),
                'desc': (d.get('description') or '').replace('\n', ' ')[:100]}
    except Exception:
        return None


def baixar(item, pasta):
    pasta.mkdir(parents=True, exist_ok=True)
    nome = f"{item['autor']}-{item['views']}v-{item['id']}.mp4"
    dest = pasta / nome
    if not dest.exists():
        sh(['yt-dlp', '--no-warnings', '-f', 'mp4/best', '-o', str(dest), item['url']], 180)
    if dest.exists():
        sheet = dest.with_suffix('.sheet.jpg')
        dur = max(item['dur'] or 8, 4)
        sh(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(dest), '-vf',
            f'fps=4/{dur},scale=270:-1,tile=4x1', '-frames:v', '1', str(sheet)], 60)
        item['arquivo'] = str(dest.relative_to(pasta.parent))
    return item


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('termos', nargs='+')
    ap.add_argument('--out', required=True)
    ap.add_argument('--min-views', type=int, default=50000)
    ap.add_argument('--max-dur', type=int, default=90)
    ap.add_argument('--top', type=int, default=5)
    ap.add_argument('--sessao', default='tiktok2')
    a = ap.parse_args()
    out = Path(a.out).expanduser().resolve()
    sh(['bash', '-lc', f'~/.claude/bin/browsers.sh {a.sessao}'], 90)
    t0 = time.time()
    linhas, vistos = [], set()
    for termo in a.termos:
        urls = [u for u in buscar(a.sessao, termo) if u not in vistos]
        vistos.update(urls)
        with ThreadPoolExecutor(8) as ex:
            ms = [m for m in ex.map(meta, urls) if m]
        bons = sorted([m for m in ms if m['views'] >= a.min_views and 0 < m['dur'] <= a.max_dur],
                      key=lambda m: -m['views'])[:a.top]
        if not bons:  # termo com vídeos novos/pequenos: aceita os melhores com 1/5 do mínimo
            bons = sorted([m for m in ms if m['views'] >= a.min_views // 5 and 0 < m['dur'] <= a.max_dur],
                          key=lambda m: -m['views'])[:a.top]
        pasta = out / termo.replace(' ', '-')
        with ThreadPoolExecutor(5) as ex:
            bons = list(ex.map(lambda m: baixar(m, pasta), bons))
        print(f'"{termo}": {len(urls)} achados · {len(ms)} lidos · {len(bons)} baixados')
        linhas += [(termo, m) for m in bons if m.get('arquivo')]
    org = out / 'ORIGEM.md'
    with org.open('a') as f:
        f.write(f"\n## Coleta {time.strftime('%Y-%m-%d %H:%M')} — TikTok, orgânico\n\n"
                '**Licença:** não verificada (conteúdo de terceiros). Uso como b-roll só depois de conferir direitos '
                'ou trocar por material próprio. Conferir texto queimado nas `.sheet.jpg`.\n\n'
                '| Termo | @autor | Views | Dur | URL | Arquivo |\n|---|---|---|---|---|---|\n')
        for termo, m in linhas:
            f.write(f"| {termo} | @{m['autor']} | {m['views']:,} | {m['dur']}s | {m['url']} | `{m['arquivo']}` |\n")
    print(f'{len(linhas)} vídeos em {time.time() - t0:.0f}s → {org}')


if __name__ == '__main__':
    main()
