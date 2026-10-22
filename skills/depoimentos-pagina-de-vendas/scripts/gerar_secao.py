#!/usr/bin/env python3
"""Gera a secao de depoimentos (mockup de conversa WhatsApp, carrossel continuo).

    python3 gerar_secao.py depoimentos.json

Ver exemplo.json para o formato. O HTML gerado e inserido na pagina alvo entre
os marcadores <!-- DEPOIMENTOS:START --> e <!-- DEPOIMENTOS:END -->; rodar de
novo regenera no lugar, sem duplicar.
"""
import html
import json
import re
import sys
from pathlib import Path

CHECK = ('<svg width="16" height="11" viewBox="0 0 16 11" fill="none">'
         '<path d="M11.5 1L5 7.5L2 4.5" stroke="#53bdeb" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>'
         '<path d="M14.5 1L8 7.5M8 7.5L6.5 6" stroke="#53bdeb" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def signal_svg(bars):
    parts = []
    geo = [(0, 9, 3), (4.5, 6.5, 5.5), (9, 4, 8), (13.5, 1, 11)]
    for i, (x, y, h) in enumerate(geo):
        op = ".9" if i < bars else ".2"
        parts.append(f'<rect x="{x}" y="{y}" width="3" height="{h}" rx="1.5" fill="#111b21" fill-opacity="{op}"/>')
    return '<svg width="17" height="12" viewBox="0 0 17 12" fill="none">' + "".join(parts) + "</svg>"


def battery_svg(level):
    w = round(2 + 16 * level)
    return ('<svg width="25" height="12" viewBox="0 0 25 12" fill="none">'
            '<rect x=".5" y=".5" width="21" height="11" rx="2.5" stroke="#111b21" stroke-opacity=".35" fill="none"/>'
            f'<rect x="2" y="2" width="{w}" height="8" rx="1.5" fill="#111b21" fill-opacity=".9"/>'
            '<path d="M23 4V8C23.8 7.7 24.5 7 24.5 6C24.5 5 23.8 4.3 23 4Z" fill="#111b21" fill-opacity=".35"/></svg>')

CSS = '''<style>
.td-wrap{position:relative}
.td-viewport{overflow:hidden;-webkit-user-select:none;user-select:none;padding:6px 0;cursor:grab;
  -webkit-mask-image:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent);
  mask-image:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent)}
.td-viewport:active{cursor:grabbing}
.td-track{display:flex;align-items:flex-start;gap:20px;width:max-content;will-change:transform}
.td-slide{flex:0 0 auto;width:min(360px,84vw);background:#e5ddd5;border-radius:16px;overflow:hidden;display:flex;flex-direction:column;
  font-family:-apple-system,"SF Pro Text","Helvetica Neue",Helvetica,Arial,sans-serif;font-size:14.5px;
  box-shadow:0 18px 44px -22px rgba(0,0,0,.75),0 0 0 1px rgba(217,172,92,.22)}
.td-bar{display:flex;align-items:center;justify-content:space-between;padding:10px 14px 2px;background:#f0ede8;color:#111b21;font-size:12px;font-weight:600;line-height:1}
.td-bar-r{display:flex;align-items:center;gap:5px}
.td-bar-r b{font-size:11px;font-weight:400}
.td-head{display:flex;align-items:center;gap:8px;padding:6px 14px 8px 10px;background:#f0ede8;color:#111b21}
.td-av{width:36px;height:36px;border-radius:50%;object-fit:cover;flex-shrink:0;display:block}
.td-who{display:flex;flex-direction:column;min-width:0;text-align:left}
.td-who b{font-size:14px;font-weight:500;line-height:1.2;color:#111b21;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.td-who i{font-size:12px;font-style:normal;color:#667781}
.td-msgs{padding:12px 10px;display:flex;flex-direction:column;gap:7px;flex:1;
  background-color:#e5ddd5;
  background-image:radial-gradient(rgba(0,0,0,.045) 1px,transparent 1px),radial-gradient(rgba(0,0,0,.03) 1px,transparent 1px);
  background-size:22px 22px,22px 22px;background-position:0 0,11px 11px}
.td-row{display:flex}
.td-in{justify-content:flex-start}
.td-out{justify-content:flex-end}
.td-b{position:relative;max-width:86%;border-radius:8px;padding:6px 9px 5px;box-shadow:0 1px .5px rgba(11,20,26,.13)}
.td-in .td-b{background:#fff;border-radius:8px 8px 8px 0}
.td-out .td-b{background:#d9fdd3;border-radius:8px 8px 0 8px}
.td-b::after{content:"";position:absolute;bottom:0;width:0;height:0;border-style:solid}
.td-in .td-b::after{left:-8px;border-width:0 10px 10px 0;border-color:transparent #fff transparent transparent;transform:scaleY(-1)}
.td-out .td-b::after{right:-8px;border-width:0 0 10px 10px;border-color:transparent transparent transparent #d9fdd3;transform:scaleY(-1)}
.td-b p{margin:0;font-size:14.5px;line-height:1.35;color:#111b21;text-align:left;word-break:break-word;font-family:inherit}
.td-t{display:flex;align-items:center;justify-content:flex-end;gap:3px;margin-top:2px;font-size:11px;color:#667781}
.td-note{margin:26px auto 0;max-width:640px;text-align:center;font-size:12.5px;line-height:1.5;color:var(--cream-faint)}
@media(prefers-reduced-motion:reduce){.td-viewport{overflow-x:auto}}
</style>'''

JS = '''<script>
(function(){
  var sec=document.currentScript.parentElement.querySelector('.td-sec')||document.currentScript.previousElementSibling;
  while(sec&&!sec.classList.contains('td-sec')) sec=sec.previousElementSibling;
  if(!sec) return;
  var vp=sec.querySelector('.td-viewport'), track=sec.querySelector('.td-track');
  var reduce=window.matchMedia('(prefers-reduced-motion:reduce)').matches;
  var originals=Array.prototype.slice.call(track.children);
  originals.forEach(function(el){ var c=el.cloneNode(true); c.setAttribute('aria-hidden','true'); track.appendChild(c); });
  var pos=0, speed=32, last=0, raf=0, paused=false, drag=false, sx=0, spos=0, moved=false;
  function loopWidth(){ var el=originals[originals.length-1]; return el.offsetLeft+el.offsetWidth+20; }
  function apply(){ track.style.transform='translate3d('+(-pos)+'px,0,0)'; }
  function norm(){ var w=loopWidth(); if(!w) return; while(pos>=w) pos-=w; while(pos<0) pos+=w; }
  function step(ts){
    if(paused||drag){ raf=0; last=0; return; }
    if(!last) last=ts;
    var dt=Math.min((ts-last)/1000,0.1); last=ts;
    pos+=speed*dt; norm(); apply();
    raf=requestAnimationFrame(step);
  }
  function start(){ if(!raf&&!paused&&!drag&&!reduce) raf=requestAnimationFrame(step); }
  function stop(){ if(raf) cancelAnimationFrame(raf); raf=0; last=0; }
  ['pointerenter','mouseenter'].forEach(function(ev){ vp.addEventListener(ev,function(){ paused=true; stop(); }); });
  ['pointerleave','mouseleave'].forEach(function(ev){ vp.addEventListener(ev,function(){ paused=false; start(); }); });
  vp.addEventListener('pointerdown',function(e){ drag=true; moved=false; sx=e.clientX; spos=pos; stop(); });
  window.addEventListener('pointermove',function(e){
    if(!drag) return;
    var d=e.clientX-sx;
    if(Math.abs(d)>4) moved=true;
    pos=spos-d; norm(); apply();
  });
  window.addEventListener('pointerup',function(){ if(!drag) return; drag=false; start(); });
  vp.addEventListener('click',function(e){ if(moved){ e.preventDefault(); e.stopPropagation(); } },true);
  document.addEventListener('visibilitychange',function(){ document.hidden?stop():start(); });
  window.addEventListener('resize',function(){ norm(); apply(); });
  if(reduce){ apply(); } else { start(); }
})();
</script>'''


def slide(chat, cfg):
    rows = []
    for m in chat["mensagens"]:
        side = m.get("lado", "in")
        meta = html.escape(m.get("hora", "")) + (CHECK if side == "out" else "")
        rows.append(f'<div class="td-row td-{side}"><div class="td-b"><p>{html.escape(m["texto"])}</p>'
                    f'<span class="td-t">{meta}</span></div></div>')
    alt_attr = ""
    if chat.get("foto_alt"):
        alt_attr = f' data-src-alt="{html.escape(chat["foto_alt"])}"'
    return f'''          <article class="td-slide">
            <header class="td-bar"><span>{html.escape(chat.get("hora_status", "09:41"))}</span><span class="td-bar-r">{signal_svg(chat.get("sinal", 4))}<b>{html.escape(chat.get("rede", "4G"))}</b>{battery_svg(chat.get("bateria", 0.8))}</span></header>
            <div class="td-head">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#111b21" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg>
              <img class="td-av" src="{html.escape(chat["foto"])}"{alt_attr} alt="" width="96" height="96" loading="lazy">
              <span class="td-who"><b>{html.escape(chat["nome"])}</b><i>{html.escape(cfg.get("status_contato", "online"))}</i></span>
            </div>
            <div class="td-msgs">
{chr(10).join("              " + r for r in rows)}
            </div>
          </article>'''


def section(cfg):
    slides = "\n".join(slide(c, cfg) for c in cfg["depoimentos"])
    head = cfg.get("cabecalho_html") or (
        f'''    <div class="sec-head">
      <p class="eyebrow">{html.escape(cfg.get("kicker", ""))}</p>
      <h2>{cfg.get("titulo_html", "")}</h2>
    </div>''')
    attrs = cfg.get("section_attrs", "")
    return f'''<!-- DEPOIMENTOS:START -->
<section class="td-sec"{attrs}>
  <div class="{html.escape(cfg.get("wrap_class", "wrap"))}">
{head}
    <div class="td-wrap">
      <div class="td-viewport">
        <div class="td-track">
{slides}
        </div>
      </div>
    </div>
    <p class="td-note">{html.escape(cfg["consentimento"])}</p>
  </div>
</section>
{CSS}
{JS}
<!-- DEPOIMENTOS:END -->
'''


def main():
    cfg = json.loads(Path(sys.argv[1]).read_text())
    assert cfg.get("consentimento"), "campo 'consentimento' e obrigatorio"
    novo = section(cfg)
    for alvo in cfg["paginas"]:
        f = Path(alvo["arquivo"])
        s = f.read_text()
        pagina = novo
        for de, para in alvo.get("substituir", {}).items():
            pagina = pagina.replace(de, para)
        marcado = re.compile(r"<!-- DEPOIMENTOS:START -->.*?<!-- DEPOIMENTOS:END -->\n", re.S)
        if marcado.search(s):
            s = marcado.sub(pagina, s, count=1)
        else:
            ancora = alvo["antes_de"]
            assert s.count(ancora) == 1, f"ancora nao unica em {f}: {ancora}"
            s = s.replace(ancora, pagina + "\n" + ancora)
        f.write_text(s)
        print("ok", f)


if __name__ == "__main__":
    main()
