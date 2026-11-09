#!/bin/bash
# uso: gen.sh <prompt.txt> <saida.png> <ref.jpg>
S=${GPT_S:-gpt-empresab-calendrier}; agent-browser --session "$S" tab "${GPT_TAB:-calendrier}" >/dev/null 2>&1 || { echo "FAIL sem aba propria (rode: lane.sh take gpt-empresab calendrier)"; exit 1; }; P=$(realpath "$1"); OUT=$(realpath -m "$2"); REF=$3; REFS=(); for _r in "${@:3}"; do REFS+=("$(realpath "$_r")"); done; REF=${REFS[0]}; T0=$(date +%s); ts(){ echo "[$(( $(date +%s)-T0 ))s] $1"; }
agent-browser --session "$S" navigate "https://chatgpt.com/" >/dev/null 2>&1; sleep 5
m=$(echo "(()=>document.querySelectorAll('.bg-user-message').length)()" | agent-browser --session "$S" eval --stdin | tr -dc '0-9'); [ "$m" = "0" ] || { echo "FAIL aba suja"; exit 1; }
CNT="(()=>[...document.querySelectorAll('img')].filter(i=>i.src.startsWith('data:image')||i.src.includes('backend-api')||i.src.startsWith('blob:')).length)()"
N0=$(echo "$CNT" | agent-browser --session "$S" eval --stdin | tr -dc '0-9')
i=0; for R in "${REFS[@]}"; do i=$((i+1)); agent-browser --session "$S" upload 'input[type=file]:nth-of-type(2)' "$R" >/dev/null 2>&1
  for k in $(seq 1 40); do n=$(echo "$CNT" | agent-browser --session "$S" eval --stdin | tr -dc '0-9'); [ "${n:-0}" -ge $(( ${N0:-0} + i )) ] && break; sleep 3; done; done
[ "${n:-0}" -ge $(( ${N0:-0} + ${#REFS[@]} )) ] || { echo "FAIL anexo"; exit 1; }
TB=$(agent-browser --session "$S" snapshot -i -c 2>/dev/null | grep -oiP '(textbox|textarea)[^\]]*\[ref=\K[^\]]+' | head -1); agent-browser --session "$S" focus "@$TB" >/dev/null
echo "(()=>{const t=document.querySelector('div.ProseMirror');t.innerHTML='<p></p>';t.dispatchEvent(new Event('input',{bubbles:true}));return t.innerText.length})()" | agent-browser --session "$S" eval --stdin >/dev/null; sleep 1
agent-browser --session "$S" focus "@$TB" >/dev/null
agent-browser --session "$S" keyboard inserttext "$(cat "$P")" >/dev/null; sleep 2
CL=$(echo "(()=>document.querySelector('div.ProseMirror').innerText.trim().length)()" | agent-browser --session "$S" eval --stdin | tr -dc '0-9'); PL=$(tr -d '\n' < "$P" | wc -m)
[ $(( CL - PL )) -lt 15 ] && [ $(( PL - CL )) -lt 15 ] || { echo "FAIL composer com lixo (composer=$CL prompt=$PL)"; exit 1; }
cat <<'JS' | agent-browser --session "$S" eval --stdin >/dev/null
(()=>{const el=document.querySelector('button[aria-label="Enviar"]')||document.querySelector('button[aria-label="Enviar prompt"]')||document.querySelector('.composer-submit-btn');
if(!el||el.disabled) return 'x';const r=el.getBoundingClientRect();
const o={bubbles:true,cancelable:true,view:window,clientX:r.left+r.width/2,clientY:r.top+r.height/2,pointerId:1,isPrimary:true,button:0};
['pointerover','mouseover','pointermove'].forEach(t=>el.dispatchEvent(new (t.startsWith('pointer')?PointerEvent:MouseEvent)(t,o)));
el.dispatchEvent(new PointerEvent('pointerdown',o));el.dispatchEvent(new MouseEvent('mousedown',o));el.dispatchEvent(new PointerEvent('pointerup',o));el.dispatchEvent(new MouseEvent('mouseup',o));el.dispatchEvent(new MouseEvent('click',o));return 'ok';})()
JS
sleep 8; SIG=$(head -c 40 "$P")
own=$(echo "(()=>{const m=document.querySelector('.bg-user-message');return m&&(m.innerText||'').includes('$SIG')?'MINHA':'X'})()" | agent-browser --session "$S" eval --stdin | tr -d '"'); [ "$own" = "MINHA" ] || { echo "FAIL envio ($own)"; exit 1; }
ts enviado
for i in $(seq 1 90); do
 st=$(echo "(()=>{const stop=document.querySelector('[data-testid=\"stop-button\"],button[aria-label*=\"Parar\"]');return (stop?'busy':'idle')+' '+document.querySelectorAll('button[aria-label=\"Imagem 1 gerada\"]').length})()" | agent-browser --session "$S" eval --stdin | tr -d '"')
 [ "$st" = "idle 1" ] && break; sleep 8; done
[ "$st" = "idle 1" ] || { echo "FAIL timeout ($st)"; exit 1; }
sleep 6; agent-browser --session "$S" key F5 >/dev/null 2>&1; sleep 7
echo "(async()=>{const g=document.querySelector('button[aria-label^=Imagem] img')||[...document.querySelectorAll('img')].filter(x=>x.naturalWidth>600).pop();if(!g)return 'none';const b=await (await fetch(g.src)).blob();return await new Promise(ok=>{const f=new FileReader();f.onload=()=>ok(f.result);f.readAsDataURL(b)})})()" | agent-browser --session "$S" eval --stdin > "$OUT.b64"
python3 -c "
import json,base64,sys;o=sys.argv[1];s=json.loads(open(o+'.b64').read());assert s.startswith('data:'),s[:40];open(o,'wb').write(base64.b64decode(s.split(',',1)[1]))" "$OUT" && rm "$OUT.b64"
for R in "${REFS[@]}"; do [ "$(md5sum < "$OUT")" = "$(md5sum < "$R")" ] && { echo "FAIL baixou ref"; exit 1; }; done
ts "OK $OUT $(ffprobe -v error -show_entries stream=width,height -of csv=p=0 "$OUT")"
