// Checkout core — Web-standard (Request -> Response). Runs unchanged on Node (Coolify, see server.mjs) and on Cloudflare Workers (src/worker.mjs).
// Rules: amounts are resolved here from catalog.mjs (never from the browser); ONE PaymentIntent per buy click (idempotent);
// delivery is granted only from the signed Stripe webhook or the server-side PayPal capture, never from a return page.
// No node:* imports here on purpose (Workers). Storage, Stripe client and static files are injected.
import { SKUS, quote, publicCatalog, currencyForCountry, languageForCountry, LANGUAGES, CURRENCIES, WARRANTY_DAYS } from '../catalog.mjs';

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const iso = (v) => (/^[A-Z]{2}$/.test(v) ? v : '');

export function loadConfig(env = {}) {
  const cfg = {
    publicUrl: (env.PUBLIC_URL || '').replace(/\/$/, ''), // empty = use the request origin
    stripeSecret: env.STRIPE_SECRET_KEY || '',
    stripePublishable: env.STRIPE_PUBLISHABLE_KEY || '',
    webhookSecret: env.STRIPE_WEBHOOK_SECRET || '',
    paypalId: env.PAYPAL_CLIENT_ID || '',
    paypalSecret: env.PAYPAL_SECRET || '',
    paypalBase: env.PAYPAL_ENV === 'live' ? 'https://api-m.paypal.com' : 'https://api-m.sandbox.paypal.com',
    allowLive: env.ALLOW_LIVE === '1',
    offerSlug: env.OFFER_SLUG || '',
    description: env.OFFER_DESCRIPTION || '',
    brand: env.BRAND || '',
    // Delivery: the members area of the offer site receives a signed POST and grants the SKUs (same job the gateway webhook does today).
    deliveryUrl: env.DELIVERY_WEBHOOK_URL || '',
    deliverySecret: env.DELIVERY_WEBHOOK_SECRET || '',
    // Trackeador mirror: connection with gateway "generic" (.../api/webhooks/sale/c/<connection_id>) + its secret.
    trackeadorUrl: env.TRACKEADOR_WEBHOOK_URL || '',
    trackeadorSecret: env.TRACKEADOR_SECRET || '',
    adminToken: env.ADMIN_TOKEN || '', // enables POST /api/admin/resend?id=<order> (re-sends delivery + Trackeador)
    mode: 'test',
  };
  const live = cfg.stripeSecret.startsWith('sk_live') || cfg.stripeSecret.startsWith('rk_live');
  if (live && !cfg.allowLive) throw new Error("Refusing a live Stripe key: this build is for the sandbox. Set ALLOW_LIVE=1 only with the owner's order.");
  if (live) cfg.mode = 'live';
  return cfg;
}

const json = (status, body) => new Response(status === 204 ? null : JSON.stringify(body), { status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' } });
const redirect = (location) => new Response(null, { status: 302, headers: { location } });
const fail = (status, message) => Object.assign(new Error(message), { status });

async function sha(text) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('').slice(0, 16);
}
const fingerprint = (email, q) => sha(JSON.stringify({ email, c: q.currency, s: [...q.skuIds].sort(), t: q.total }));
const amountString = (minor) => (minor / 100).toFixed(2);
const b64 = (text) => btoa(text);

async function readJson(request, limit = 64 * 1024) {
  const text = await request.text();
  if (text.length > limit) throw fail(413, 'Payload too large');
  return text ? JSON.parse(text) : {};
}

async function parseCart(request) {
  const body = await readJson(request);
  const email = String(body.email || '').trim().toLowerCase();
  if (!EMAIL_RE.test(email)) throw fail(400, 'E-mail invalide');
  const orderRef = String(body.orderRef || '');
  if (!/^[A-Za-z0-9_-]{8,64}$/.test(orderRef)) throw fail(400, 'orderRef invalide');
  let q;
  try { q = quote({ currency: String(body.currency || ''), plan: body.plan, upgrade: Boolean(body.upgrade), bumps: body.bumps || [] }); }
  catch (e) { throw fail(400, e.message); }
  const lang = LANGUAGES.includes(String(body.lang || '')) ? String(body.lang) : 'fr';
  const back = /^\/[A-Za-z0-9_-]{0,40}$/.test(String(body.back || '')) ? String(body.back) : '/';
  return { email, orderRef, q, lang, back, tkid: String(body.tkid || '').slice(0, 80), saveCard: Boolean(body.saveCard) };
}

// ---- Delivery + Trackeador (both fail-safe: a slow or broken receiver never blocks or undoes the sale).
const ROLE = { plan: 'front', upgrade: 'bump', bump: 'bump', upsell: 'upsell' };
/** Items of a paid order with role (front/bump/upsell) and amount in major units, rebuilt from the catalog. */
export function orderItems(order) {
  return order.skuIds.map((id) => {
    const sku = SKUS[id];
    return { sku: id, name: sku ? sku.name : id, role: ROLE[sku?.type] || 'bump', amount: sku ? sku.amount[order.currency] / 100 : null };
  });
}

async function hmacHex(secret, text) {
  const key = await crypto.subtle.importKey('raw', new TextEncoder().encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const sig = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(text));
  return [...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

async function post(fetcher, url, headers, body) {
  try {
    const r = await fetcher(url, { method: 'POST', headers: { 'content-type': 'application/json', ...headers }, body, signal: AbortSignal.timeout(3000) });
    return { ok: r.ok, status: r.status };
  } catch (e) { return { ok: false, status: 0, error: String(e.message || e).slice(0, 120) }; }
}

/**
 * Members-area delivery. Body = {event: order.paid|order.refunded, order_id, email, entitlements, items[], currency, amount, paid_at, method, mode, offer}.
 * Headers: x-checkout-secret (shared secret, simplest check) and x-checkout-signature = HMAC-SHA256(secret, `${timestamp}.${body}`) with x-checkout-timestamp.
 * The receiver must be idempotent by order_id (it can be called again by /api/admin/resend).
 */
export async function notifyDelivery(cfg, order, event, fetcher = fetch) {
  if (!cfg.deliveryUrl || !cfg.deliverySecret) return { skipped: true };
  const body = JSON.stringify({ event, order_id: order.id, email: order.email, entitlements: order.entitlements, items: orderItems(order), currency: order.currency.toUpperCase(), amount: order.total / 100, paid_at: order.paidAt, method: order.paidVia, mode: cfg.mode, offer: cfg.offerSlug || '' });
  const ts = String(Math.floor(Date.now() / 1000));
  return post(fetcher, cfg.deliveryUrl, { 'x-checkout-secret': cfg.deliverySecret, 'x-checkout-timestamp': ts, 'x-checkout-signature': await hmacHex(cfg.deliverySecret, `${ts}.${body}`) }, body);
}

/** Trackeador mirror (canonical payload of the "generic" connection; idempotent by transaction_id). */
export async function notifyTrackeador(cfg, order, status, fetcher = fetch) {
  if (!cfg.trackeadorUrl || !cfg.trackeadorSecret) return { skipped: true };
  const method = order.paidVia === 'paypal-capture' ? 'paypal' : 'credit_card';
  const body = JSON.stringify({
    transaction_id: order.id, status, payment_method: method, amount: order.total / 100, currency: order.currency.toUpperCase(),
    buyer: { email: order.email }, product: { name: orderItems(order)[0]?.name || '' }, items: orderItems(order),
    tracking_id: order.tkid || null, created_at: order.paidAt || new Date().toISOString(), approved_at: order.paidAt || null,
  });
  return post(fetcher, cfg.trackeadorUrl, { 'x-trackeador-secret': cfg.trackeadorSecret }, body);
}

async function notifyAll(store, cfg, order, kind, fetcher) {
  const d = await notifyDelivery(cfg, order, kind === 'paid' ? 'order.paid' : 'order.refunded', fetcher);
  const t = await notifyTrackeador(cfg, order, kind === 'paid' ? 'paid' : 'refunded', fetcher);
  await store.log('deliveries', { orderId: order.id, email: order.email, entitlements: order.entitlements, kind, delivery: d, trackeador: t, mode: cfg.mode });
  if (d.ok === false || t.ok === false) await store.log('notify-failed', { orderId: order.id, kind, delivery: d, trackeador: t });
  return { delivery: d, trackeador: t };
}

/** Grant: idempotent per order. Called only from the signed Stripe webhook or the server-side PayPal capture. */
export async function grant(store, order, source, cfg = { mode: 'test' }, fetcher = fetch) {
  if (order.delivered) return order;
  order.status = 'paid'; order.delivered = true; order.paidAt = new Date().toISOString(); order.paidVia = source;
  await store.put(order);
  await notifyAll(store, cfg, order, 'paid', fetcher);
  return order;
}

async function paypalToken(cfg) {
  const r = await fetch(`${cfg.paypalBase}/v1/oauth2/token`, { method: 'POST', headers: { authorization: 'Basic ' + b64(`${cfg.paypalId}:${cfg.paypalSecret}`), 'content-type': 'application/x-www-form-urlencoded' }, body: 'grant_type=client_credentials' });
  const j = await r.json();
  if (!r.ok) throw new Error('PayPal auth failed');
  return j.access_token;
}

/**
 * @param {{cfg:object, stripe:object, store:object, serveStatic:(request:Request, pathname:string)=>Promise<Response>, cryptoProvider?:any, paypal?:{token:Function}}} deps
 * store: async { get(id), put(order), seen(eventId), log(name,payload), findByIntent(pi) }
 */
export function createCore({ cfg, stripe, store, serveStatic, cryptoProvider, paypal = { token: paypalToken }, fetcher = (...a) => fetch(...a) }) {
  // Which wallets the Stripe account really offers (default payment method configuration). Cached 10 min.
  // A wallet the account cannot use (e.g. Google Pay on some countries' accounts) must not be shown as an option.
  let walletCache = null;
  async function walletsOn() {
    if (walletCache && walletCache.at > Date.now() - 600000) return walletCache.v;
    let v = { applePay: true, googlePay: true };
    try {
      const pmc = (await stripe.paymentMethodConfigurations.list({ limit: 20 })).data.find((x) => x.is_default);
      const on = (k) => Boolean(pmc?.[k]?.available && pmc[k].display_preference?.value !== 'off');
      if (pmc) v = { applePay: on('apple_pay'), googlePay: on('google_pay') };
    } catch { /* unknown: let the device decide */ }
    walletCache = { at: Date.now(), v };
    return v;
  }

  return async function handle(request) {
    try {
      const url = new URL(request.url);
      const p = url.pathname;
      const base = cfg.publicUrl || url.origin;
      const method = request.method;

      if (method === 'GET' && p === '/api/health') return json(200, { ok: true, mode: cfg.mode });

      if (method === 'GET' && p === '/api/context') {
        const forced = (url.searchParams.get('pays') || '').toUpperCase();
        const header = (request.headers.get('cf-ipcountry') || request.cf?.country || '').toString().toUpperCase();
        const country = iso(forced) || iso(header) || 'FR';
        const qLang = (url.searchParams.get('lang') || '').toLowerCase();
        const lang = LANGUAGES.includes(qLang) ? qLang : languageForCountry(country, request.headers.get('accept-language') || '');
        return json(200, { country, currency: currencyForCountry(country), lang, currencies: CURRENCIES });
      }

      if (method === 'GET' && p === '/api/config') return json(200, { publishableKey: cfg.stripePublishable, paypal: Boolean(cfg.paypalId && cfg.paypalSecret), warrantyDays: WARRANTY_DAYS, mode: cfg.mode, wallets: await walletsOn() });

      if (method === 'GET' && p === '/api/catalog') {
        try { return json(200, publicCatalog((url.searchParams.get('currency') || '').toLowerCase())); } catch { return json(400, { error: 'Devise non prise en charge' }); }
      }

      if (method === 'POST' && p === '/api/quote') {
        const b = await readJson(request);
        try { return json(200, quote({ currency: String(b.currency || ''), plan: b.plan, upgrade: Boolean(b.upgrade), bumps: b.bumps || [] })); }
        catch (e) { return json(400, { error: e.message }); }
      }

      // The ONLY place the charge is created: the buy click. Idempotent per (orderRef, cart).
      if (method === 'POST' && p === '/api/intent') {
        const { email, orderRef, q, tkid, saveCard } = await parseCart(request);
        const existing = await store.get(orderRef);
        if (existing?.delivered) return json(409, { error: 'Commande déjà payée', orderId: orderRef });
        const fp = await fingerprint(email, q);
        if (existing && existing.fingerprint === fp && existing.clientSecret) {
          return json(200, { clientSecret: existing.clientSecret, orderId: orderRef, amount: q.total, currency: q.currency, reused: true });
        }
        const customers = await stripe.customers.list({ email, limit: 1 });
        const customer = customers.data[0] ?? (await stripe.customers.create({ email, metadata: { offer: cfg.offerSlug || 'checkout' } }));
        const params = {
          amount: q.total, currency: q.currency, customer: customer.id, payment_method_types: ['card'], receipt_email: email,
          description: cfg.description || 'Checkout',
          metadata: { offer_slug: cfg.offerSlug || '', order_id: orderRef, skus: q.skuIds.join(','), entitlements: q.entitlements.join(','), tkid, event_id: orderRef },
        };
        if (saveCard) params.setup_future_usage = 'off_session';
        const intent = await stripe.paymentIntents.create(params, { idempotencyKey: `pi-${orderRef}-${fp}` });
        await store.put({ id: orderRef, email, method: 'card', status: 'pending', fingerprint: fp, currency: q.currency, total: q.total, skuIds: [...q.skuIds], entitlements: [...q.entitlements], tkid, paymentIntent: intent.id, clientSecret: intent.client_secret, customer: customer.id, saveCard, createdAt: new Date().toISOString() });
        return json(200, { clientSecret: intent.client_secret, orderId: orderRef, amount: q.total, currency: q.currency });
      }

      // REDIRECT mode (V11): card, Apple Pay, Google Pay and Link are paid on the page hosted by Stripe (Checkout Session).
      // Same rules as /api/intent: amounts from catalog.mjs, one Session per (orderRef, cart), delivery only by webhook.
      // The card is saved for the one-click upsell (setup_future_usage off_session) and metadata rides on the PaymentIntent,
      // so payment_intent.succeeded / charge.refunded below work for both modes.
      if (method === 'POST' && p === '/api/session') {
        const { email, orderRef, q, tkid, lang, back } = await parseCart(request);
        const existing = await store.get(orderRef);
        if (existing?.delivered) return json(409, { error: 'Commande déjà payée', orderId: orderRef });
        const fp = await fingerprint(email, q);
        if (existing && existing.fingerprint === fp && existing.sessionUrl && existing.sessionExpiresAt > Date.now() / 1000 + 60) {
          return json(200, { url: existing.sessionUrl, orderId: orderRef, reused: true });
        }
        const customers = await stripe.customers.list({ email, limit: 1 });
        const customer = customers.data[0] ?? (await stripe.customers.create({ email, metadata: { offer: cfg.offerSlug || 'checkout' } }));
        const metadata = { offer_slug: cfg.offerSlug || '', order_id: orderRef, skus: q.skuIds.join(','), entitlements: q.entitlements.join(','), tkid, event_id: orderRef, mode: 'redirect' };
        const session = await stripe.checkout.sessions.create({
          mode: 'payment',
          customer: customer.id,
          client_reference_id: orderRef,
          locale: lang,
          line_items: q.lines.map((l) => ({ quantity: 1, price_data: { currency: q.currency, unit_amount: l.amount, product_data: { name: l.name } } })),
          payment_intent_data: { setup_future_usage: 'off_session', receipt_email: email, description: cfg.description || 'Checkout', metadata },
          metadata,
          success_url: `${base}/merci.html?order=${orderRef}&lang=${lang}&m=card`,
          cancel_url: `${base}${back}?annule=1`,
          expires_at: Math.floor(Date.now() / 1000) + 30 * 60,
        }, { idempotencyKey: `cs-${orderRef}-${fp}` });
        await store.put({ id: orderRef, email, method: 'card-redirect', status: 'pending', fingerprint: fp, currency: q.currency, total: q.total, skuIds: [...q.skuIds], entitlements: [...q.entitlements], tkid, checkoutSession: session.id, sessionUrl: session.url, sessionExpiresAt: session.expires_at, customer: customer.id, saveCard: true, createdAt: new Date().toISOString() });
        return json(200, { url: session.url, orderId: orderRef });
      }

      if (method === 'GET' && p === '/api/order') {
        const o = await store.get(String(url.searchParams.get('id') || ''));
        if (!o) return json(404, { error: 'Commande introuvable' });
        return json(200, { id: o.id, status: o.status, currency: o.currency, total: o.total, method: o.method, delivered: Boolean(o.delivered) });
      }

      // Re-send delivery + Trackeador for one paid order (after fixing the receiver). Off unless ADMIN_TOKEN is set.
      if (method === 'POST' && p === '/api/admin/resend') {
        if (!cfg.adminToken || request.headers.get('authorization') !== `Bearer ${cfg.adminToken}`) return json(401, { error: 'unauthorized' });
        const o = await store.get(String(url.searchParams.get('id') || ''));
        if (!o || !o.delivered) return json(404, { error: 'paid order not found' });
        return json(200, await notifyAll(store, cfg, o, o.status === 'refunded' ? 'refunded' : 'paid', fetcher));
      }

      if (method === 'POST' && p === '/api/track') {
        const b = await readJson(request);
        await store.log('tracking-browser', { event: String(b.event || '').slice(0, 40), orderRef: String(b.orderRef || '').slice(0, 64), value: Number(b.value) || null, currency: String(b.currency || '').slice(0, 3) });
        return json(204, {});
      }

      // ---- PayPal: server creates the order, buyer approves on PayPal, server captures.
      if (method === 'POST' && p === '/api/paypal/order') {
        if (!cfg.paypalId) return json(503, { error: 'PayPal non configuré' });
        const { email, orderRef, q, tkid } = await parseCart(request);
        const existing = await store.get(orderRef);
        if (existing?.delivered) return json(409, { error: 'Commande déjà payée', orderId: orderRef });
        const fp = await fingerprint(email, q);
        const token = await paypal.token(cfg);
        const r = await fetch(`${cfg.paypalBase}/v2/checkout/orders`, {
          method: 'POST',
          headers: { authorization: `Bearer ${token}`, 'content-type': 'application/json', 'PayPal-Request-Id': `pp-${orderRef}-${fp}` },
          body: JSON.stringify({
            intent: 'CAPTURE',
            purchase_units: [{ reference_id: orderRef, custom_id: orderRef, description: cfg.description || 'Checkout', amount: { currency_code: q.currency.toUpperCase(), value: amountString(q.total) } }],
            payment_source: { paypal: { experience_context: { brand_name: cfg.brand || 'Checkout', user_action: 'PAY_NOW', shipping_preference: 'NO_SHIPPING', return_url: `${base}/paypal/return?ref=${orderRef}`, cancel_url: `${base}/?annule=1` } } },
          }),
        });
        const j = await r.json();
        if (!r.ok) return json(502, { error: 'PayPal indisponible', detail: j.name || null });
        const approve = (j.links || []).find((l) => l.rel === 'payer-action' || l.rel === 'approve');
        await store.put({ id: orderRef, email, method: 'paypal', status: 'pending', fingerprint: fp, currency: q.currency, total: q.total, skuIds: [...q.skuIds], entitlements: [...q.entitlements], tkid, paypalOrder: j.id, createdAt: new Date().toISOString() });
        return json(200, { approveUrl: approve?.href, orderId: orderRef });
      }

      if (method === 'GET' && p === '/paypal/return') {
        const ref = String(url.searchParams.get('ref') || '');
        const order = await store.get(ref);
        if (!order || order.method !== 'paypal') return redirect('/?erreur=commande');
        if (!order.delivered) {
          const token = await paypal.token(cfg);
          const r = await fetch(`${cfg.paypalBase}/v2/checkout/orders/${order.paypalOrder}/capture`, { method: 'POST', headers: { authorization: `Bearer ${token}`, 'content-type': 'application/json', 'PayPal-Request-Id': `cap-${ref}` }, body: '{}' });
          const j = await r.json();
          const unit = j.purchase_units?.[0]?.payments?.captures?.[0];
          const paid = j.status === 'COMPLETED' && unit?.status === 'COMPLETED' && unit.amount?.currency_code === order.currency.toUpperCase() && unit.amount?.value === amountString(order.total);
          if (!paid) { order.status = 'failed'; await store.put(order); return redirect('/?erreur=paypal'); }
          order.paypalCapture = unit.id;
          await grant(store, order, 'paypal-capture', cfg, fetcher);
        }
        return redirect(`/merci.html?order=${ref}&m=paypal`);
      }

      // ---- Stripe webhook: signed, idempotent, raw body.
      if (method === 'POST' && p === '/webhook') {
        const raw = await request.text();
        let event;
        try { event = await stripe.webhooks.constructEventAsync(raw, request.headers.get('stripe-signature') || '', cfg.webhookSecret, undefined, cryptoProvider); }
        catch { return json(400, { error: 'Signature invalide' }); }
        if (await store.seen(event.id)) return json(200, { received: true, duplicate: true });
        const obj = event.data.object;
        if (event.type === 'payment_intent.succeeded') {
          const order = await store.get(obj.metadata?.order_id);
          if (order && obj.amount === order.total && obj.currency === order.currency) await grant(store, order, 'stripe-webhook', cfg, fetcher);
          else await store.log('webhook-anomalies', { event: event.id, reason: 'order missing or amount mismatch', pi: obj.id });
        } else if (event.type === 'checkout.session.completed' || event.type === 'checkout.session.async_payment_succeeded') {
          // Redirect mode: the Session confirms the same order (grant is idempotent with payment_intent.succeeded).
          const order = await store.get(obj.metadata?.order_id || obj.client_reference_id);
          if (order && obj.payment_status === 'paid' && obj.amount_total === order.total && obj.currency === order.currency) {
            if (obj.payment_intent && !order.paymentIntent) order.paymentIntent = obj.payment_intent;
            await grant(store, order, 'stripe-checkout-session', cfg, fetcher);
          } else if (obj.payment_status === 'paid') await store.log('webhook-anomalies', { event: event.id, reason: 'session order missing or amount mismatch', cs: obj.id });
        } else if (event.type === 'checkout.session.expired') {
          const order = await store.get(obj.metadata?.order_id || obj.client_reference_id);
          if (order && !order.delivered) { order.status = 'expired'; order.sessionUrl = null; await store.put(order); }
        } else if (event.type === 'payment_intent.payment_failed') {
          const order = await store.get(obj.metadata?.order_id);
          if (order && !order.delivered) { order.status = 'failed'; await store.put(order); }
        } else if (event.type === 'charge.refunded') {
          const order = (await store.get(obj.metadata?.order_id)) || (await store.findByIntent(obj.payment_intent));
          if (order && order.status !== 'refunded') { const wasPaid = order.delivered; order.status = 'refunded'; await store.put(order); if (wasPaid) await notifyAll(store, cfg, order, 'refunded', fetcher); }
        }
        return json(200, { received: true });
      }

      if (method === 'GET') {
        let path = p === '/' ? '/index.html' : p;
        if (!/\.[a-z0-9]+$/i.test(path)) path += '.html'; // /merci -> /merci.html, /v3 -> /v3.html
        return serveStatic(request, path);
      }
      return new Response('Not found', { status: 404 });
    } catch (e) {
      const status = e.status || (e instanceof SyntaxError ? 400 : 500);
      if (status === 500) console.error('[checkout] error:', e.message);
      return json(status, { error: status === 500 ? 'Erreur serveur' : e.message });
    }
  };
}
