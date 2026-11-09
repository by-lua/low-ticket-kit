// uso: node flow-upload.cjs <arquivo> <screenshot-out>   (caminhos por argv, com espaço ok)
const { chromium } = require(process.env.HOME + '/.local/share/google-flow-mcp/node_modules/playwright-core');
(async () => {
  const [file, shot] = process.argv.slice(2);
  const b = await chromium.connectOverCDP('http://127.0.0.1:9333');
  const page = b.contexts()[0].pages().find(p => p.url().includes('flow.google.com/project'));
  if (!page) throw new Error('sem aba do projeto');
  const plus = page.getByRole('button', { name: 'Adicionar elementos à caixa de comando' });
  if ((await plus.getAttribute('aria-expanded')) !== 'true') await plus.click();
  await page.waitForTimeout(800);
  const [fc] = await Promise.all([page.waitForEvent('filechooser', { timeout: 10000 }), page.getByRole('button', { name: /Enviar mídia/ }).click()]);
  await fc.setFiles(file);
  await page.waitForTimeout(8000);
  await page.screenshot({ path: shot });
  console.log('ok');
  await b.close();
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
