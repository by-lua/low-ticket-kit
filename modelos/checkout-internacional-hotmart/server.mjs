// Node / Coolify entry. Run: PORT=4242 STRIPE_SECRET_KEY=... STRIPE_PUBLISHABLE_KEY=... STRIPE_WEBHOOK_SECRET=... node server.mjs
// (Cloudflare entry is src/worker.mjs; both share src/core.mjs.)
import http from 'node:http';
import path from 'node:path';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import Stripe from 'stripe';
import { createCore, loadConfig } from './src/core.mjs';
import { FileStore } from './src/store-file.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const PUBLIC = path.join(HERE, 'public');
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.mjs': 'text/javascript', '.woff2': 'font/woff2', '.jpg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp', '.svg': 'image/svg+xml', '.json': 'application/json', '.ico': 'image/x-icon' };

export async function serveStatic(_request, pathname) {
  const file = path.normalize(path.join(PUBLIC, pathname));
  if (!file.startsWith(PUBLIC + path.sep)) return new Response('Forbidden', { status: 403 });
  try {
    const data = await readFile(file);
    return new Response(data, { headers: { 'content-type': TYPES[path.extname(file)] || 'application/octet-stream', 'cache-control': 'no-store' } });
  } catch { return new Response('Not found', { status: 404 }); }
}

// node:http <-> Web Request/Response
export function toNodeListener(handle, origin) {
  return async (req, res) => {
    const chunks = [];
    for await (const c of req) chunks.push(c);
    const body = chunks.length ? Buffer.concat(chunks) : undefined;
    const headers = new Headers();
    for (const [k, v] of Object.entries(req.headers)) if (v !== undefined) headers.set(k, Array.isArray(v) ? v.join(', ') : v);
    const request = new Request(new URL(req.url, origin), { method: req.method, headers, body: ['GET', 'HEAD'].includes(req.method) ? undefined : body });
    const response = await handle(request);
    res.writeHead(response.status, Object.fromEntries(response.headers));
    res.end(Buffer.from(await response.arrayBuffer()));
  };
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const port = Number(process.env.PORT || 4242);
  const cfg = loadConfig(process.env);
  if (!cfg.stripeSecret || !cfg.stripePublishable) { console.error('Missing STRIPE_SECRET_KEY / STRIPE_PUBLISHABLE_KEY.'); process.exit(1); }
  cfg.publicUrl = cfg.publicUrl || `http://localhost:${port}`;
  const store = await new FileStore(process.env.DATA_DIR || path.join(HERE, 'data')).init();
  const handle = createCore({ cfg, stripe: new Stripe(cfg.stripeSecret), store, serveStatic });
  http.createServer(toNodeListener(handle, cfg.publicUrl)).listen(port, () => {
    console.log(`Checkout (${cfg.mode}) on ${cfg.publicUrl}  webhook: ${cfg.webhookSecret ? 'configured' : 'NOT configured'}  paypal: ${cfg.paypalId ? 'on' : 'off'}`);
  });
}
