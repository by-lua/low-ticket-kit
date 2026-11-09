// teste do MCP patcheado sem reiniciar o servidor: node flow-mcp-test.mjs <prompt.txt> <img.jpg> <outdir> [send]
import fs from 'node:fs';
const D = process.env.HOME + '/.local/share/google-flow-mcp/dist/';
const { loadConfig } = await import(D + 'config.js');
const { BrowserSession } = await import(D + 'browser/session.js');
const { JobStore } = await import(D + 'flow/jobs.js');
const { createLogger } = await import(D + 'lib/logger.js');
const { Mutex } = await import(D + 'lib/mutex.js');
const { generateMedia } = await import(D + 'flow/composer.js');
const config = { ...loadConfig(), logLevel: 'info' };
const log = createLogger({ level: 'info', dir: config.stateDir + '/logs' });
const ctx = { config, log, session: new BrowserSession(config, log), jobs: new JobStore(config.stateDir + '/jobs'), lock: new Mutex() };
const [pf, img, out, send] = process.argv.slice(2);
const r = await generateMedia(ctx, { kind: 'video', prompt: fs.readFileSync(pf, 'utf8').trim(), model: 'omni-flash', ratio: '9:16', duration: 8, count: 1,
  referenceImages: [img], projectUrl: 'https://flow.google.com/project/86d60ee4-ac82-4636-a480-0951aaf1fb82', outputDir: out, autoConfirm: send === 'send', resume: false, jobId: undefined, editMode: false });
console.log(JSON.stringify(r, null, 1));
process.exit(0);
