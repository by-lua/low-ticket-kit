// Cloudflare Workers entry. Bindings (cloudflare.config.ts): DB (D1), ASSETS (static files from ./public).
// Secrets: STRIPE_SECRET_KEY, STRIPE_PUBLISHABLE_KEY, STRIPE_WEBHOOK_SECRET, PAYPAL_CLIENT_ID, PAYPAL_SECRET. Optional vars: PUBLIC_URL, PAYPAL_ENV, ALLOW_LIVE.
import Stripe from 'stripe';
import { createCore, loadConfig } from './core.mjs';
import { D1Store } from './store-d1.mjs';

export default {
  async fetch(request, env, ctx) {
    const cfg = loadConfig(env);
    if (!cfg.stripeSecret || !cfg.stripePublishable) return new Response('Missing Stripe keys (set the Worker secrets).', { status: 500 });
    const stripe = new Stripe(cfg.stripeSecret, { httpClient: Stripe.createFetchHttpClient() });
    const handle = createCore({
      cfg,
      stripe,
      store: new D1Store(env.DB),
      cryptoProvider: Stripe.createSubtleCryptoProvider(),
      // Static files (index.html, app.js, i18n.js, assets/...) are served by the Workers assets binding.
      serveStatic: (req, pathname) => env.ASSETS.fetch(new Request(new URL(pathname, req.url), req)),
    });
    return handle(request);
  },
};
