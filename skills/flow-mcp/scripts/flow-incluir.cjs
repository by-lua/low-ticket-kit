// uso: node flow-incluir.cjs <nome-do-asset-na-lista>  -- com o seletor '+' aberto: escolhe o asset pelo nome e 'Incluir no comando'
const { chromium } = require(process.env.HOME + '/.local/share/google-flow-mcp/node_modules/playwright-core');
(async () => {
  const name = process.argv[2];
  const b = await chromium.connectOverCDP('http://127.0.0.1:9333');
  const page = b.contexts()[0].pages().find(p => p.url().includes('flow.google.com/project'));
  await page.getByText(name, { exact: false }).first().click({ timeout: 8000 });
  await page.waitForTimeout(1500);
  await page.getByRole('button', { name: /Incluir no comando/ }).click({ timeout: 8000 });
  await page.waitForTimeout(1500);
  console.log('incluido', name);
  await b.close();
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
