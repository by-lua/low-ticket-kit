// uso: node flow-send.cjs <prompt.txt> <shot-out> [send] -- digita o prompt na caixa (com o asset ja incluido) e, com 'send', inicia a geracao
const fs = require('fs');
const { chromium } = require(process.env.HOME + '/.local/share/google-flow-mcp/node_modules/playwright-core');
(async () => {
  const [pf, shot, send] = process.argv.slice(2);
  const b = await chromium.connectOverCDP('http://127.0.0.1:9333');
  const page = b.contexts()[0].pages().find(p => p.url().includes('flow.google.com/project'));
  const tb = page.locator('[role=textbox][aria-label*="O que você quer criar"], div[contenteditable=true]').first();
  await tb.click({ timeout: 8000 });
  await page.keyboard.press('Control+A'); await page.keyboard.press('Delete');
  await page.keyboard.insertText(fs.readFileSync(pf, 'utf8').trim());
  await page.waitForTimeout(1000);
  await page.screenshot({ path: shot });
  if (send === 'send') { await page.getByRole('button', { name: 'Iniciar geração' }).click({ timeout: 8000 }); console.log('enviado'); } else console.log('preparado');
  await b.close();
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
