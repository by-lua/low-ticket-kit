// QA da secao de depoimentos: node qa.mjs <url> [url-outro-idioma]
// Confere fotos carregando, erro de console, movimento do carrossel, pausa no hover e mobile.
import { chromium } from 'playwright';

const urls = process.argv.slice(2);
if (!urls.length) { console.error('uso: node qa.mjs <url> [url2]'); process.exit(1); }

const browser = await chromium.launch();
let falhou = false;

for (const url of urls) {
  for (const [w, h, tag] of [[1280, 900, 'desktop'], [390, 844, 'mobile']]) {
    const page = await browser.newPage({ viewport: { width: w, height: h } });
    const erros = [];
    page.on('pageerror', e => erros.push('JS: ' + e.message));
    page.on('console', m => m.type() === 'error' && erros.push('console: ' + m.text()));
    page.on('requestfailed', r => !r.url().includes('fonts.gstatic') && erros.push('falhou: ' + r.url()));

    await page.goto(url, { waitUntil: 'networkidle' });
    const sec = await page.$('.td-sec');
    if (!sec) { console.log(`✗ ${url} [${tag}] secao .td-sec nao encontrada`); falhou = true; await page.close(); continue; }
    await sec.scrollIntoViewIfNeeded();
    await page.waitForTimeout(500);

    const fotos = await page.$$eval('.td-av', els => els.map(e => ({ src: e.getAttribute('src'), ok: e.naturalWidth > 0 })));
    const quebradas = fotos.filter(f => !f.ok).map(f => f.src);

    const t1 = await page.$eval('.td-track', e => e.style.transform);
    await page.waitForTimeout(900);
    const t2 = await page.$eval('.td-track', e => e.style.transform);
    const andando = t1 !== t2;

    const vpBox = await (await page.$('.td-viewport')).boundingBox();
    await page.mouse.move(vpBox.x + vpBox.width / 2, Math.min(vpBox.y + vpBox.height / 2, h - 10));
    await page.waitForTimeout(300);
    const p1 = await page.$eval('.td-track', e => e.style.transform);
    await page.waitForTimeout(700);
    const pausou = p1 === (await page.$eval('.td-track', e => e.style.transform));

    const larguraCard = await page.$eval('.td-slide', e => e.offsetWidth);
    const cardsVisiveis = +(w / larguraCard).toFixed(1);

    const problemas = [
      quebradas.length ? `fotos quebradas: ${quebradas.join(', ')}` : null,
      !andando ? 'carrossel parado' : null,
      !pausou ? 'nao pausa no hover' : null,
      tag === 'mobile' && cardsVisiveis > 1.4 ? `mobile mostrando ${cardsVisiveis} cards` : null,
      ...erros,
    ].filter(Boolean);

    if (problemas.length) { falhou = true; console.log(`✗ ${url} [${tag}]\n   - ${problemas.join('\n   - ')}`); }
    else console.log(`✓ ${url} [${tag}] ${fotos.length} fotos ok, carrossel andando, pausa no hover`);

    await page.close();
  }
}

await browser.close();
process.exit(falhou ? 1 : 0);
