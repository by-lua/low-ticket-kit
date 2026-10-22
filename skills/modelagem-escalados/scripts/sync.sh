#!/usr/bin/env bash
# Atualiza a biblioteca local com o que entrou de novo em
# sistema.antonioferriani.com/modelos-de-criativos. So baixa o que nao existe
# (diff por id contra catalogo.json) — nunca rebaixa os 103 ja no disco.
set -euo pipefail

B="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/biblioteca"
C="$B/catalogo.json"
SESSION="ferriani"
LOG="$HOME/.claude/skills/modelagem-escalados/scripts/sync.log"

echo "[$(date -Is)] sync start" >> "$LOG"

~/.claude/bin/browsers.sh "$SESSION" >>"$LOG" 2>&1
agent-browser --session "$SESSION" navigate 'https://sistema.antonioferriani.com/modelos-de-criativos' >>"$LOG" 2>&1
sleep 2

# le os cards da pagina (data-id, data-tipo, data-categoria, data-nome)
CARDS_JSON=$(agent-browser --session "$SESSION" eval "
JSON.stringify(Array.from(document.querySelectorAll('article[data-id]')).map(a => ({
  id: a.dataset.id, tipo: a.dataset.tipo, categoria: a.dataset.categoria, nome: a.dataset.nome
})))
")

echo "$CARDS_JSON" > /tmp/ferriani-cards.json

NEW_IDS=$(python3 -c "
import json
cards = json.load(open('/tmp/ferriani-cards.json'))
local = {i['id'] for i in json.load(open('$C'))}
novos = [c for c in cards if c['id'] not in local]
print(json.dumps(novos))
")

COUNT=$(python3 -c "import json,sys; print(len(json.loads(sys.argv[1])))" "$NEW_IDS")
echo "[$(date -Is)] $COUNT formatos novos" >> "$LOG"

if [ "$COUNT" = "0" ]; then
  echo "[$(date -Is)] nada novo, sync ok" >> "$LOG"
  exit 0
fi

# cookie de sessao pra baixar
agent-browser --session "$SESSION" eval "document.cookie" > /tmp/ferriani-cookie.txt

python3 - "$NEW_IDS" <<'PY' >> "$LOG" 2>&1
import json, sys, os, urllib.request

novos = json.loads(sys.argv[1])
B = os.path.expanduser("~/.claude/biblioteca-escalados")
cookie = open("/tmp/ferriani-cookie.txt").read().strip().strip('"')

for c in novos:
    dest_dir = f"{B}/formatos/{c['tipo']}/{c['categoria']}"
    os.makedirs(dest_dir, exist_ok=True)
    url = f"https://sistema.antonioferriani.com/api/criativos/download?id={c['id']}&formato=arquivo"
    req = urllib.request.Request(url, headers={"Cookie": cookie})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            ext = ".mp4" if c["tipo"] == "video" else ".jpg"
            path = f"{dest_dir}/{c['id']}-{c['nome']}{ext}"
            open(path, "wb").write(r.read())
            print(f"baixado: {path}")
    except Exception as e:
        print(f"FALHOU id={c['id']}: {e}")

    if c["tipo"] == "video":
        try:
            req2 = urllib.request.Request(
                f"https://sistema.antonioferriani.com/api/criativos/download?id={c['id']}&formato=txt",
                headers={"Cookie": cookie})
            with urllib.request.urlopen(req2, timeout=30) as r:
                open(f"{dest_dir}/{c['id']}-{c['nome']}.txt", "wb").write(r.read())
        except Exception:
            pass

# atualiza catalogo.json e regrava CATALOGO.md
cat = json.load(open(f"{B}/catalogo.json"))
existentes = {i["id"] for i in cat}
for c in novos:
    if c["id"] not in existentes:
        cat.append({**c, "transcricao": c["tipo"] == "video"})
json.dump(cat, open(f"{B}/catalogo.json", "w"), ensure_ascii=False, indent=1)
print(f"catalogo.json: {len(cat)} itens (era {len(cat)-len(novos)})")
PY

echo "[$(date -Is)] sync fim — RODE buscar.sh pra conferir e reescreva CATALOGO.md a mao se precisar" >> "$LOG"
