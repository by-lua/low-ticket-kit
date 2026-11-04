// QA de layout da página de vendas (rodar com: agent-browser --session S eval --stdin < qa-layout.js)
// Checa: botão do hero acima da dobra · rolagem lateral · texto vazando da caixa · texto estourando botão.
(() => {
  const W = innerWidth, H = innerHeight, out = { viewport: W + 'x' + H, problemas: [] };
  const hero = document.querySelector('section.hero, header.hero, .hero');
  const heroBtn = hero && hero.querySelector('a.btn, a.cta, .btn, .cta');
  if (heroBtn) { const b = heroBtn.getBoundingClientRect().bottom + scrollY; out.heroBotaoBottom = Math.round(b);
    if (b > H) out.problemas.push(`botão do hero abaixo da dobra (${Math.round(b)}px > ${H}px)`); }
  else out.problemas.push('hero sem botão');
  if (document.documentElement.scrollWidth > W + 1) out.problemas.push(`rolagem lateral (${document.documentElement.scrollWidth}px)`);
  const inRail = e => e.closest('.rail, .marquee, .track, .t-viewport');
  [...document.querySelectorAll('body *')].forEach(e => {
    if (inRail(e) || !e.offsetParent) return;
    const cs = getComputedStyle(e), r = e.getBoundingClientRect();
    if (r.right > W + 2 && cs.position !== 'fixed') out.problemas.push(`sai da tela: ${e.tagName}.${String(e.className).slice(0,30)} (${Math.round(r.right)}px)`);
    const hasText = [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (hasText && e.scrollWidth > e.clientWidth + 2 && cs.overflowX === 'visible' && cs.display !== 'inline')
      out.problemas.push(`texto vazando: ${e.tagName}.${String(e.className).slice(0,30)} "${e.textContent.trim().slice(0,40)}"`);
  });
  document.querySelectorAll('a.btn, a.cta, button.btn, .btn, .cta').forEach(b => {
    if (!b.offsetParent) return; const r = b.getBoundingClientRect();
    if (b.scrollWidth > b.clientWidth + 2) out.problemas.push(`texto estoura o botão: "${b.textContent.trim().slice(0,40)}"`);
    const lh = parseFloat(getComputedStyle(b).lineHeight) || 20;
    if (r.height > Math.max(90, lh * 3.2)) out.problemas.push(`botão alto demais (texto quebrou em muitas linhas): "${b.textContent.trim().slice(0,40)}"`);
  });
  out.problemas = [...new Set(out.problemas)].slice(0, 25); out.ok = out.problemas.length === 0;
  return JSON.stringify(out);
})()
