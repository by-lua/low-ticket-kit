#!/usr/bin/env node
// QA de PERFORMANCE da página de vendas, no ar ou em preview (regra da dona 06/11/2026: nenhuma oferta sobe com erro
// de velocidade descoberto depois). Roda em QUALQUER página: nossa, clonada ou otimizada de modelo.
//
// Uso:  node qa-performance.js <url> [--meta-id=<id esperado do pixel>]
// Precisa: playwright-core global (npm i -g playwright-core) + Chrome/Chromium/Edge (Linux, macOS ou Windows; CHROMIUM_PATH opcional).
// Emula celular 390x844, CPU 4x mais lenta, cache desligado, em 4G lento (1,6 Mbps / 150 ms) e 3G rápido.
// Sai com código 1 se algum item FALHA; AVISO não reprova mas precisa de motivo no STATUS.md.
const { execSync } = require('child_process');
const fs = require('fs');
let chromium;
try { chromium = require(execSync('npm root -g 2>' + (process.platform === 'win32' ? 'nul' : '/dev/null')).toString().trim() + '/playwright-core').chromium; }
catch (e) { console.error('playwright-core ausente. Rode:  npm i -g playwright-core   (o Low Ticket Kit instala sozinho na próxima atualização)'); process.exit(2); }
// Chrome/Chromium: CHROMIUM_PATH manda; senão procura nos lugares de Linux, macOS e Windows.
const CHROMES = [process.env.CHROMIUM_PATH, '/usr/bin/chromium', '/usr/bin/chromium-browser', '/usr/bin/google-chrome-stable', '/usr/bin/google-chrome',
  '/Applications/Chromium.app/Contents/MacOS/Chromium', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  (process.env.PROGRAMFILES || '') + '\\Google\\Chrome\\Application\\chrome.exe', (process.env['PROGRAMFILES(X86)'] || '') + '\\Google\\Chrome\\Application\\chrome.exe',
  (process.env.LOCALAPPDATA || '') + '\\Google\\Chrome\\Application\\chrome.exe', (process.env.PROGRAMFILES || '') + '\\Microsoft\\Edge\\Application\\msedge.exe'];
const CHROME = CHROMES.find(c => c && fs.existsSync(c));
if (!CHROME) { console.error('Chrome/Chromium não encontrado. Instale um ou defina CHROMIUM_PATH.'); process.exit(2); }

const url = process.argv[2];
const metaId = (process.argv.find(a => a.startsWith('--meta-id=')) || '').split('=')[1];
if (!url) { console.error('uso: node qa-performance.js <url> [--meta-id=ID]'); process.exit(2); }

const LIM = { fcp: 2000, lcp: 2500, cls: 0.1, loadKB: 1500, imgWarnKB: 250, eagerImgs: 3 };
const falhas = [], avisos = [];
const F = m => { falhas.push(m); console.log('  FALHA ' + m); };
const A = m => { avisos.push(m); console.log('  AVISO ' + m); };
const OK = m => console.log('  ok    ' + m);

(async () => {
  const b = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox'] });
  const redes = [['4G lento', 1.6 * 1024 * 1024 / 8, 750 * 1024 / 8, 150], ['3G rápido', 4 * 1024 * 1024 / 8, 1024 * 1024 / 8, 100]];
  let html = '', reqs = [];
  for (const [nome, dl, ul, lat] of redes) {
    console.log(`\n== ${nome} (celular 390x844, CPU 4x)`);
    const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, serviceWorkers: 'block',
      userAgent: 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 Chrome/120 Mobile Safari/537.36' });
    // QA nunca ingere eventos no pixel/Trackeador de produção. O SDK estático
    // connect.facebook.net continua carregando para validar a instalação.
    await ctx.route('**/*', route => {
      const u = new URL(route.request().url());
      if (/(^|\.)facebook\.com$/.test(u.hostname) || ['/api/track', '/api/collect'].includes(u.pathname)) return route.abort();
      return route.continue();
    });
    const p = await ctx.newPage(); const c = await ctx.newCDPSession(p);
    await c.send('Network.enable'); await c.send('Network.setCacheDisabled', { cacheDisabled: true });
    await c.send('Network.emulateNetworkConditions', { offline: false, downloadThroughput: dl, uploadThroughput: ul, latency: lat });
    await c.send('Emulation.setCPUThrottlingRate', { rate: 4 });
    let bytes = 0; const rs = {};
    c.on('Network.requestWillBeSent', e => { rs[e.requestId] = { url: e.request.url }; });
    c.on('Network.responseReceived', e => { if (rs[e.requestId]) { rs[e.requestId].type = e.response.mimeType; rs[e.requestId].cc = e.response.headers['cache-control'] || e.response.headers['Cache-Control'] || ''; rs[e.requestId].status = e.response.status; } });
    c.on('Network.loadingFinished', e => { bytes += e.encodedDataLength; if (rs[e.requestId]) rs[e.requestId].size = e.encodedDataLength; });
    await p.addInitScript(() => { window.__m = { cls: 0 };
      new PerformanceObserver(l => { for (const e of l.getEntries()) if (e.name === 'first-contentful-paint') __m.fcp = e.startTime; }).observe({ type: 'paint', buffered: true });
      new PerformanceObserver(l => { const a = l.getEntries(); __m.lcp = a[a.length - 1].startTime; }).observe({ type: 'largest-contentful-paint', buffered: true });
      new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) __m.cls += e.value; }).observe({ type: 'layout-shift', buffered: true }); });
    await p.goto(url, { waitUntil: 'load' }); await p.waitForTimeout(2500);
    const m = await p.evaluate(() => __m);
    if (nome === '4G lento') { html = await p.content(); reqs = Object.values(rs); }
    m.fcp <= LIM.fcp ? OK(`FCP ${Math.round(m.fcp)}ms`) : F(`FCP ${Math.round(m.fcp)}ms > ${LIM.fcp}ms`);
    m.lcp <= LIM.lcp || nome !== '4G lento' ? OK(`LCP ${Math.round(m.lcp)}ms`) : F(`LCP ${Math.round(m.lcp)}ms > ${LIM.lcp}ms`);
    m.cls <= LIM.cls ? OK(`CLS ${m.cls.toFixed(3)}`) : F(`CLS ${m.cls.toFixed(3)} > ${LIM.cls}`);
    const kb = Math.round(bytes / 1024);
    kb <= LIM.loadKB ? OK(`transferido até o load: ${kb} KB`) : F(`transferido ${kb} KB > ${LIM.loadKB} KB (imagem pesada ou sem lazy)`);
    await ctx.close();
  }
  await b.close();

  console.log('\n== Recursos e HTML');
  const origem = new URL(url).origin;
  const g = reqs.filter(r => /fonts\.googleapis|fonts\.gstatic/.test(r.url));
  g.length ? F('Google Fonts em uso (bloqueia a renderização): hospedar woff2 em img/fonts/') : OK('nenhuma requisição ao Google Fonts');
  const fontes = reqs.filter(r => /woff2?(\?|$)/.test(r.url));
  if (!fontes.length) A('nenhuma fonte web carregada (ok se a página usa fonte do sistema)');
  fontes.forEach(r => { if (!/^font\//.test(r.type || '')) F(`fonte com content-type "${r.type}" (precisa font/woff2): ${r.url.replace(origem, '')}`);
    if (new URL(r.url).origin !== origem) F('fonte fora do domínio: ' + r.url); });
  if (!/font-display\s*:\s*swap/.test(html)) A('sem font-display:swap');
  const imgs = reqs.filter(r => /^image\//.test(r.type || ''));
  imgs.filter(r => r.size / 1024 > LIM.imgWarnKB).forEach(r => A(`imagem ${Math.round(r.size / 1024)} KB: ${r.url.replace(origem, '')}`));
  imgs.filter(r => !/immutable|max-age=(\d{7,})/.test(r.cc || '') && new URL(r.url).origin === origem).slice(0, 3).forEach(r => A(`imagem sem cache longo: ${r.url.replace(origem, '')} (${r.cc || 'sem cache-control'})`));
  const tags = html.match(/<img\b[^>]*>/g) || [];
  const eager = tags.filter(t => !/loading="lazy"/.test(t));
  eager.length <= LIM.eagerImgs ? OK(`${eager.length} <img> sem lazy (de ${tags.length})`) : F(`${eager.length} <img> sem loading="lazy" (máx ${LIM.eagerImgs}): só o hero é eager`);
  const semDim = tags.filter(t => !/\bwidth=/.test(t) || !/\bheight=/.test(t));
  semDim.length ? A(`${semDim.length} <img> sem width/height (risco de layout pular)`) : OK('todo <img> com width/height');
  /rel="preload"[^>]*as="image"|as="image"[^>]*rel="preload"/.test(html) || /fetchpriority="high"/.test(html) ? OK('hero com preload/fetchpriority') : A('hero sem preload nem fetchpriority=high');

  console.log('\n== Rastreamento (não pode quebrar ao otimizar)');
  const fb = html.match(/fbq\(\s*['"]init['"]\s*,\s*['"]([^'"]+)['"]/);
  if (!fb) F('pixel Meta ausente (fbq init)');
  else if (/AQUI|PIXEL/i.test(fb[1])) F(`pixel Meta com placeholder: ${fb[1]}`);
  else if (metaId && fb[1] !== metaId) F(`pixel Meta ${fb[1]} ≠ esperado ${metaId}`);
  else OK(`pixel Meta ${fb[1]}`);
  /fbq\(\s*['"]track['"]\s*,\s*['"]PageView['"]/.test(html) ? OK('PageView no load') : F('sem fbq track PageView');
  /adstrackeador\.leadgo\.dev\/api\/pixel/.test(html) ? OK('loader do Trackeador') : F('loader do Trackeador ausente (sem venda × campanha)');
  const vis = reqs.some(r => /facebook\.com\/tr|connect\.facebook\.net/.test(r.url));
  vis ? OK('requisição do Meta saiu no carregamento') : A('nenhuma requisição ao Meta no carregamento (pixel bloqueado ou lento demais)');

  console.log(`\nRESULTADO: ${falhas.length ? 'REPROVADO' : 'APROVADO'} — ${falhas.length} falha(s), ${avisos.length} aviso(s)`);
  process.exit(falhas.length ? 1 : 0);
})().catch(e => { console.error('ERRO', e.message); process.exit(2); });
