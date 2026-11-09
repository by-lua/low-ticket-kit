// uso: node flow-baixar.cjs <saida.mp4>  -- na pagina /edit/<id> do video: abre 'Baixar mídia' e escolhe '720p Tamanho original'
const { chromium } = require(process.env.HOME + '/.local/share/google-flow-mcp/node_modules/playwright-core');
(async () => {
  const out = process.argv[2];
  const b = await chromium.connectOverCDP('http://127.0.0.1:9333');
  const page = b.contexts()[0].pages().find(p => p.url().includes('flow.google.com'));
  if (await page.getByText('Tamanho original').count() === 0) { await page.getByRole('button', { name: /Baixar mídia/ }).first().click(); await page.waitForTimeout(1000); }
  const [dl] = await Promise.all([page.waitForEvent('download', { timeout: 120000 }), page.getByText('Tamanho original').first().click()]);
  await dl.saveAs(out);
  console.log('salvo', out);
  await b.close();
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
