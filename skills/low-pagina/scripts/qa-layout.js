// QA de layout da página de vendas (rodar com: agent-browser --session S eval --stdin < qa-layout.js)
// Checa: botão do hero acima da dobra · rolagem lateral · texto vazando da caixa · texto estourando botão.
(() => {
  const W = innerWidth, H = innerHeight, out = { viewport: W + 'x' + H, problemas: [] };
  if (!document.querySelector('link[rel~="icon"]')) out.problemas.push('sem favicon (<link rel="icon">)');
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
  // Imagem coberta/cortada por outro elemento (ex.: caixa de altura fixa + card por cima).
  document.querySelectorAll('img').forEach(im => {
    if (!im.offsetParent || im.closest('.rail, .marquee, .track, .t-viewport')) return;
    im.scrollIntoView({block: 'center', behavior: 'instant'});
    const r = im.getBoundingClientRect(); if (r.height < 40) return;
    for (const fx of [.3, .5, .7]) { const x = r.left + r.width * fx, y = r.bottom - 6;
      const top = document.elementFromPoint(x, y);
      if (top && top !== im && !im.contains(top) && !top.contains(im) && !top.closest('.offer-bar')) {
        out.problemas.push(`imagem coberta embaixo por ${top.tagName}.${String(top.className).slice(0,25)}: ${im.getAttribute('src')}`); break; } }
    const pa = im.parentElement, ps = getComputedStyle(pa);
    if (ps.overflow !== 'visible' && im.getBoundingClientRect().bottom > pa.getBoundingClientRect().bottom + 2)
      out.problemas.push(`imagem cortada pela caixa (${pa.className}): ${im.getAttribute('src')}`);
  });
  scrollTo(0, 0);
  // Teste de estresse: simula tradução automática do navegador (texto ~45% mais longo) em todo botão.
  document.querySelectorAll('a.btn, a.cta, button.btn, .btn, .cta').forEach(b => {
    if (!b.offsetParent) return; const tn = [...b.childNodes].find(n => n.nodeType === 3 && n.textContent.trim());
    if (!tn) return; const orig = tn.textContent; tn.textContent = orig + ' ' + orig.slice(0, Math.ceil(orig.length * .45));
    const r = b.getBoundingClientRect(), pr = b.parentElement.getBoundingClientRect();
    if (b.scrollWidth > b.clientWidth + 2 || r.left < pr.left - 2 || r.right > Math.min(W, pr.right) + 2)
      out.problemas.push(`botão não aguenta texto traduzido (+45%): "${orig.trim().slice(0,40)}"`);
    tn.textContent = orig; });
  out.problemas = [...new Set(out.problemas)].slice(0, 25); out.ok = out.problemas.length === 0;
  return JSON.stringify(out);
})()
