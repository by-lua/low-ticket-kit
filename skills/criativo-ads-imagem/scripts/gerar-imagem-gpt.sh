#!/bin/bash
# Gera 1 imagem no ChatGPT (chat novo já aberto na sessão). Uso: gerar-imagem-gpt.sh <sessao> <prompt.txt> <saida.png> <ref1> [ref2...]
# Sessão: S=$(~/.claude/bin/gpt-livre.sh <lane> | tail -1). Mecânica/erros: skill gpt-imagem-playwright.
# uso: gen1.sh <session> <prompt.txt> <saida.png> <ref1> [ref2...]
S=$1; P=$2; OUT=$3; shift 3
[ -s "$OUT" ] && { echo "salvou (ja existia) $OUT"; exit 0; }
exec 8>"/tmp/gpt-sessao-$S.lock"; flock -n 8 || { echo "FAIL sessao $S ocupada por outra geracao (nunca rodar 2 filas na mesma sessao)"; exit 1; }
AB="agent-browser --session $S"
T0=$(date +%s); ts(){ echo "[$(( $(date +%s)-T0 ))s] $1"; }
m=$(echo "(()=>document.querySelectorAll('.bg-user-message').length)()" | $AB eval --stdin | tr -dc '0-9')
[ "${m:-0}" = "0" ] || { echo "FAIL chat nao vazio ($m)"; exit 1; }
CNT="(()=>[...document.querySelectorAll('img')].filter(i=>i.src.startsWith('data:image')||i.src.startsWith('blob:')||i.src.includes('backend-api')).length)()"
for R in "$@"; do
  N0=$(echo "$CNT" | $AB eval --stdin | tr -dc '0-9')
  $AB upload 'input[type=file][accept="image/*,video/*"]' "$R" >/dev/null
  ok=0; for k in $(seq 1 40); do n=$(echo "$CNT" | $AB eval --stdin | tr -dc '0-9'); [ "${n:-0}" -gt "${N0:-0}" ] && { ok=1; break; }; sleep 3; done
  [ $ok = 1 ] || { echo "FAIL anexo $R"; exit 1; }; ts "anexou $(basename $R)"
done
sleep 4
TB=$($AB snapshot -i -c 2>/dev/null | grep -oiP 'textbox "Pergunte[^\]]*\[ref=\K[^\]]+' | head -1)
$AB focus "@$TB" >/dev/null
$AB keyboard inserttext "$(cat $P)" >/dev/null
sleep 2
L=$(echo "(()=>(document.querySelector('div.ProseMirror')?.innerText||'').length)()" | $AB eval --stdin | tr -dc '0-9'); ts "composer=$L / $(wc -c <$P)"
PRE=$(echo "(()=>[...document.querySelectorAll('img')].map(i=>i.src).join('|'))()" | $AB eval --stdin | tr -d '"')
cat <<'JS' | $AB eval --stdin
(()=>{const el=document.querySelector('button[aria-label="Enviar"]')||document.querySelector('button[aria-label="Enviar prompt"]')||document.querySelector('.composer-submit-btn');
if(!el||el.disabled) return 'sem botao';
const r=el.getBoundingClientRect();const o={bubbles:true,cancelable:true,view:window,clientX:r.left+r.width/2,clientY:r.top+r.height/2,pointerId:1,isPrimary:true,button:0};
['pointerover','mouseover','pointermove'].forEach(t=>el.dispatchEvent(new (t.startsWith('pointer')?PointerEvent:MouseEvent)(t,o)));
el.dispatchEvent(new PointerEvent('pointerdown',o));el.dispatchEvent(new MouseEvent('mousedown',o));
el.dispatchEvent(new PointerEvent('pointerup',o));el.dispatchEvent(new MouseEvent('mouseup',o));el.dispatchEvent(new MouseEvent('click',o));return 'clicou';})()
JS
sleep 8
L=$(echo "(()=>(document.querySelector('div.ProseMirror')?.innerText||'').length)()" | $AB eval --stdin | tr -dc '0-9'); ts "composer apos envio=$L"
[ "${L:-1}" -lt 20 ] || { echo "FAIL nao enviou"; exit 1; }
SIG=$(head -c 40 $P)
own=$(cat <<EOF | $AB eval --stdin | tr -d '"'
(()=>{const m=document.querySelectorAll('.bg-user-message');if(!m.length)return 'vazio';return (m[0].innerText||'').indexOf("$SIG")>=0?'MINHA':'ALHEIA';})()
EOF
); ts "dono=$own"; [ "$own" = "MINHA" ] || { echo "FAIL dono"; exit 1; }
echo "$PRE" | tr '|' '\n' > /tmp/claude-1000/pre.txt
for i in $(seq 1 120); do
  NEW=$(echo "(()=>[...document.querySelectorAll('img')].filter(i=>i.naturalWidth>1020&&i.complete).map(i=>i.src).join('|'))()" | $AB eval --stdin | tr -d '"' | tr '|' '\n' | grep -vxF -f /tmp/claude-1000/pre.txt | grep -v '^$' | tail -1)
  [ -n "$NEW" ] && break; sleep 5
done
[ -n "$NEW" ] || { echo "FAIL sem imagem"; echo "(()=>document.body.innerText.slice(-400))()" | $AB eval --stdin; exit 1; }
# ⛔ 26/10/2026 (Tarot AR): o GPT gera em 2 passadas — a FOTO aparece primeiro e o TEXTO é escrito depois.
# Baixar quando a 1ª imagem aparece = peça SEM TEXTO (foi a causa das "imagens sem texto" de 25/10).
# Esperar o botão "Parar" sumir (geração terminou) e a imagem ficar estável antes de baixar.
busy="(()=>!!(document.querySelector('[data-testid=\"stop-button\"]')||[...document.querySelectorAll('button')].find(b=>/^(Parar|Stop)/i.test(((b.getAttribute('aria-label')||'')+' '+(b.innerText||'')).trim()))))()"
for i in $(seq 1 120); do
  [ "$(echo "$busy" | $AB eval --stdin | tr -d '"')" = "false" ] && break; sleep 5
done
ts "geracao terminou (sem botao Parar)"
sleep 6
NEW=$(echo "(()=>[...document.querySelectorAll('img')].filter(i=>i.naturalWidth>1020&&i.complete).map(i=>i.src).join('|'))()" | $AB eval --stdin | tr -d '"' | tr '|' '\n' | grep -vxF -f /tmp/claude-1000/pre.txt | grep -v '^$' | tail -1)
ts "gerou"
# ⛔ 26/10/2026: outro agente no MESMO perfil pode navegar a aba durante a geração (caso Tarot AR p08:
# baixou imagem da NeuroActiva). Reconfere o dono do chat ANTES de baixar; alheio = não baixa.
own2=$(cat <<EOF2 | $AB eval --stdin | tr -d '"'
(()=>{const m=document.querySelectorAll('.bg-user-message');if(!m.length)return 'vazio';return (m[0].innerText||'').indexOf("$SIG")>=0?'MINHA':'ALHEIA';})()
EOF2
); [ "$own2" = "MINHA" ] || { echo "FAIL dono mudou durante a geracao ($own2) — aba tomada por outra lane"; exit 1; }
cat <<EOF | $AB eval --stdin | tr -d '"' | sed 's/^data:image\/[a-z]*;base64,//' | base64 -d > "$OUT"
(async()=>{const r=await fetch("$NEW");const b=await r.blob();return await new Promise(res=>{const f=new FileReader();f.onload=()=>res(f.result);f.readAsDataURL(b);});})()
EOF
NM=$(md5sum < "$OUT"); for R in "$@"; do [ "$(md5sum < "$R")" = "$NM" ] && { echo "FAIL baixou referencia"; exit 1; }; done
ts "salvou $(python3 -c "from PIL import Image;print(Image.open('$OUT').size)")"
echo "(()=>location.href)()" | $AB eval --stdin
