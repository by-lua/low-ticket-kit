// uso: node flow-prep.cjs <arquivo.jpg> -- sobe a imagem (+ > Enviar midia), espera, inclui o 1o asset da lista 'Recentes' no comando
const { chromium } = require(process.env.HOME + '/.local/share/google-flow-mcp/node_modules/playwright-core');
(async () => {
  const file = process.argv[2];
  const b = await chromium.connectOverCDP('http://127.0.0.1:9333');
  const page = b.contexts()[0].pages().find(p => p.url().includes('flow.google.com/project'));
  const plus = page.getByRole('button', { name: 'Adicionar elementos à caixa de comando' });
  if ((await plus.getAttribute('aria-expanded')) !== 'true') await plus.click();
  await page.waitForTimeout(800);
  const [fc] = await Promise.all([page.waitForEvent('filechooser', { timeout: 10000 }), page.getByRole('button', { name: /Enviar mídia/ }).click()]);
  await fc.setFiles(file);
  await page.waitForTimeout(12000);
  await page.locator('mat-list-item').filter({ hasText: /Imagem/ }).first().click({ timeout: 8000 });
  await page.waitForTimeout(1500);
  await page.getByRole('button', { name: /Incluir no comando/ }).click({ timeout: 8000 });
  await page.waitForTimeout(1500);
  console.log('incluido');
  await b.close();
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
