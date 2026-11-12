import assert from 'node:assert/strict';
import test from 'node:test';
import { mkdtemp } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { DatabaseSync } from 'node:sqlite';
import { createCore, loadConfig } from './src/core.mjs';
import { FileStore } from './src/store-file.mjs';
import { D1Store } from './src/store-d1.mjs';

// Minimal D1 emulation on node:sqlite so the SAME core tests run against both stores.
async function fakeD1() {
  const db = new DatabaseSync(':memory:');
  return {
    async batch(statements) { for (const st of statements) await st.run(); return []; },
    prepare(sql) {
      let args = [];
      return { // compile lazily, like D1 does
        bind(...a) { args = a; return this; },
        async first() { return db.prepare(sql).get(...args) ?? null; },
        async run() { const r = db.prepare(sql).run(...args); return { meta: { changes: Number(r.changes) } }; },
      };
    },
  };
}

function fakeStripe() {
  const calls = { intents: [], sessions: [], customers: 0 };
  return {
    calls,
    customers: { list: async () => ({ data: [] }), create: async ({ email }) => { calls.customers++; return { id: 'cus_test', email }; } },
    paymentIntents: { create: async (params, opts) => { calls.intents.push({ params, opts }); return { id: 'pi_test_' + calls.intents.length, client_secret: 'pi_secret_' + calls.intents.length }; } },
    checkout: { sessions: { create: async (params, opts) => { calls.sessions.push({ params, opts }); const n = calls.sessions.length; return { id: 'cs_test_' + n, url: 'https://checkout.stripe.com/c/pay/cs_test_' + n, expires_at: Math.floor(Date.now() / 1000) + 1800 }; } } },
    webhooks: { constructEventAsync: async (raw, sig) => { if (sig !== 'ok') throw new Error('bad'); return JSON.parse(raw); } },
  };
}

const staticOk = async () => new Response('static', { status: 200 });

async function boot(kind, extra = {}, fetcher) {
  const store = kind === 'd1' ? new D1Store(await fakeD1()) : await new FileStore(await mkdtemp(path.join(os.tmpdir(), 'ck-'))).init();
  const stripe = fakeStripe();
  const cfg = { ...loadConfig({}), stripePublishable: 'pk_test_x', webhookSecret: 'whsec_<secret>', offerSlug: 'test-offer', ...extra };
  const handle = createCore({ cfg, stripe, store, serveStatic: staticOk, ...(fetcher ? { fetcher } : {}) });
  const post = (p, body, headers = {}) => handle(new Request('http://x.test' + p, { method: 'POST', headers: { 'content-type': 'application/json', ...headers }, body: typeof body === 'string' ? body : JSON.stringify(body) }));
  const get = (p, headers = {}) => handle(new Request('http://x.test' + p, { headers }));
  return { post, get, stripe, store };
}

const cart = { email: 'buyer@example.com', orderRef: 'ref_12345678', currency: 'eur', plan: 'basic', upgrade: false, bumps: [] };

for (const kind of ['file', 'd1']) {
  test(`[${kind}] intent charges the server-resolved total and ignores a tampered amount`, async () => {
    const s = await boot(kind);
    const r = await s.post('/api/intent', { ...cart, amount: 1, total: 1, upgrade: true, bumps: ['bumpA'] });
    const j = await r.json();
    assert.equal(r.status, 200);
    assert.equal(s.stripe.calls.intents[0].params.amount, 590 + 200 + 590); // basic + additive upgrade + bumpA
    assert.equal(j.amount, 1380);
  });

  test(`[${kind}] same order and cart creates ONE PaymentIntent`, async () => {
    const s = await boot(kind);
    await s.post('/api/intent', cart); await s.post('/api/intent', cart);
    assert.equal(s.stripe.calls.intents.length, 1);
  });

  test(`[${kind}] rejects invalid e-mail and unknown plan`, async () => {
    const s = await boot(kind);
    assert.equal((await s.post('/api/intent', { ...cart, email: 'nope' })).status, 400);
    assert.equal((await s.post('/api/intent', { ...cart, plan: 'vip' })).status, 400);
    assert.equal(s.stripe.calls.intents.length, 0);
  });

  test(`[${kind}] webhook: bad signature rejected, wrong amount not granted, success grants once, duplicate ignored, refund revokes`, async () => {
    const s = await boot(kind);
    await s.post('/api/intent', cart);
    const ev = (id, amount, type = 'payment_intent.succeeded') => JSON.stringify({ id, type, data: { object: { id: 'pi_test_1', amount, currency: 'eur', payment_intent: 'pi_test_1', metadata: { order_id: cart.orderRef } } } });
    assert.equal((await s.post('/webhook', ev('evt_1', 590), { 'stripe-signature': 'bad' })).status, 400);
    assert.equal((await s.post('/webhook', ev('evt_2', 1), { 'stripe-signature': 'ok' })).status, 200);
    assert.notEqual((await s.store.get(cart.orderRef)).status, 'paid');
    assert.equal((await s.post('/webhook', ev('evt_3', 590), { 'stripe-signature': 'ok' })).status, 200);
    assert.equal((await s.store.get(cart.orderRef)).status, 'paid');
    const dup = await (await s.post('/webhook', ev('evt_3', 590), { 'stripe-signature': 'ok' })).json();
    assert.equal(dup.duplicate, true);
    await s.post('/webhook', ev('evt_4', 590, 'charge.refunded'), { 'stripe-signature': 'ok' });
    assert.equal((await s.store.get(cart.orderRef)).status, 'refunded');
  });

  test(`[${kind}] redirect session: server total in line items, card saved for upsell, one Session per cart, tampering ignored`, async () => {
    const s = await boot(kind);
    const r = await s.post('/api/session', { ...cart, amount: 1, upgrade: true, bumps: ['bumpA'], lang: 'en', back: '/v11' });
    const j = await r.json();
    assert.equal(r.status, 200);
    assert.match(j.url, /^https:\/\/checkout\.stripe\.com\//);
    const p = s.stripe.calls.sessions[0].params;
    assert.equal(p.line_items.reduce((t, l) => t + l.price_data.unit_amount, 0), 590 + 200 + 590);
    assert.equal(p.payment_intent_data.setup_future_usage, 'off_session');
    assert.equal(p.payment_intent_data.metadata.order_id, cart.orderRef);
    assert.equal(p.locale, 'en');
    assert.match(p.cancel_url, /\/v11\?annule=1$/);
    await s.post('/api/session', { ...cart, upgrade: true, bumps: ['bumpA'], lang: 'en' });
    assert.equal(s.stripe.calls.sessions.length, 1);
    assert.equal((await s.post('/api/session', { ...cart, back: 'https://evil.test' })).status, 200);
    assert.match(s.stripe.calls.sessions.at(-1).params.cancel_url, /^http:\/\/x\.test\/\?annule=1$/);
  });

  test(`[${kind}] redirect webhook: checkout.session.completed grants once, wrong amount or unpaid never grants`, async () => {
    const s = await boot(kind);
    await s.post('/api/session', cart);
    const ev = (id, amount_total, payment_status = 'paid', type = 'checkout.session.completed') => JSON.stringify({ id, type, data: { object: { id: 'cs_test_1', amount_total, currency: 'eur', payment_status, payment_intent: 'pi_x', client_reference_id: cart.orderRef, metadata: { order_id: cart.orderRef } } } });
    await s.post('/webhook', ev('evt_a', 1), { 'stripe-signature': 'ok' });
    await s.post('/webhook', ev('evt_b', 590, 'unpaid'), { 'stripe-signature': 'ok' });
    assert.notEqual((await s.store.get(cart.orderRef)).status, 'paid');
    await s.post('/webhook', ev('evt_c', 590), { 'stripe-signature': 'ok' });
    const o = await s.store.get(cart.orderRef);
    assert.equal(o.status, 'paid');
    assert.equal(o.paymentIntent, 'pi_x');
  });

  test(`[${kind}] return-page endpoint never grants access`, async () => {
    const s = await boot(kind);
    await s.post('/api/intent', cart);
    const o = await (await s.get(`/api/order?id=${cart.orderRef}`)).json();
    assert.equal(o.status, 'pending');
    assert.equal(o.delivered, false);
  });
}

test('context: country header or Cloudflare cf.country picks currency and language; falls back to EUR', async () => {
  const s = await boot('file');
  const ch = await (await s.get('/api/context', { 'cf-ipcountry': 'CH', 'accept-language': 'fr-CH' })).json();
  assert.deepEqual([ch.currency, ch.lang], ['chf', 'fr']);
  const br = await (await s.get('/api/context', { 'cf-ipcountry': 'BR' })).json();
  assert.deepEqual([br.currency, br.lang], ['eur', 'pt']);
  const us = await (await s.get('/api/context?pays=US')).json();
  assert.deepEqual([us.currency, us.lang], ['eur', 'en']);
});

test('static files and /merci alias go through the injected serveStatic', async () => {
  const s = await boot('file');
  assert.equal(await (await s.get('/')).text(), 'static');
  assert.equal((await s.get('/merci')).status, 200);
  assert.equal((await s.get('/v3')).status, 200);
  assert.equal((await s.get('/v11')).status, 200);
});

test('refuses a live Stripe key unless explicitly allowed', () => {
  assert.throws(() => loadConfig({ STRIPE_SECRET_KEY: 'sk_live_abc' }));
  assert.equal(loadConfig({ STRIPE_SECRET_KEY: 'sk_live_abc', ALLOW_LIVE: '1' }).mode, 'live');
  assert.doesNotThrow(() => loadConfig({ STRIPE_SECRET_KEY: 'sk_test_abc' }));
});

test('delivery + Trackeador: signed POST with items/roles on paid, refunded on refund, broken receiver never blocks, resend needs token', async () => {
  const sent = [];
  let down = true;
  const fetcher = async (url, init) => { sent.push({ url, init }); if (down && url.includes('members')) throw new Error('ECONNREFUSED'); return new Response('{}', { status: 200 }); };
  const extra = { deliveryUrl: 'https://site.test/members/webhook', deliverySecret: 'dsecret', trackeadorUrl: 'https://tk.test/api/webhooks/sale/c/1', trackeadorSecret: 'tsecret', adminToken: 'adm' };
  const s = await boot('file', extra, fetcher);
  await s.post('/api/intent', { ...cart, upgrade: true, bumps: [(await (await s.get('/api/catalog?currency=eur')).json()).bumps[0].id], tkid: 'tk_abc' });
  const ev = (id, type, amount) => JSON.stringify({ id, type, data: { object: { id: 'pi_test_1', amount, currency: 'eur', payment_intent: 'pi_test_1', metadata: { order_id: cart.orderRef } } } });
  const order = await s.store.get(cart.orderRef);
  const r = await s.post('/webhook', ev('evt_p', 'payment_intent.succeeded', order.total), { 'stripe-signature': 'ok' });
  assert.equal(r.status, 200);                                     // receiver down: sale still confirmed
  assert.equal((await s.store.get(cart.orderRef)).status, 'paid');
  const d = sent.find((x) => x.url.includes('members'));
  const body = JSON.parse(d.init.body);
  assert.equal(body.event, 'order.paid');
  assert.deepEqual(body.items.map((i) => i.role), ['front', 'bump', 'bump']);
  const { createHmac } = await import('node:crypto');
  assert.equal(d.init.headers['x-checkout-signature'], createHmac('sha256', 'dsecret').update(`${d.init.headers['x-checkout-timestamp']}.${d.init.body}`).digest('hex'));
  const t = JSON.parse(sent.find((x) => x.url.includes('tk.test')).init.body);
  assert.deepEqual([t.transaction_id, t.status, t.tracking_id, t.amount], [cart.orderRef, 'paid', 'tk_abc', order.total / 100]);
  // resend after the receiver is fixed
  down = false;
  assert.equal((await s.post(`/api/admin/resend?id=${cart.orderRef}`, '{}')).status, 401);
  const rs = await (await s.post(`/api/admin/resend?id=${cart.orderRef}`, '{}', { authorization: 'Bearer adm' })).json();
  assert.equal(rs.delivery.ok, true);
  // refund
  sent.length = 0;
  await s.post('/webhook', ev('evt_r', 'charge.refunded', order.total), { 'stripe-signature': 'ok' });
  assert.equal(JSON.parse(sent.find((x) => x.url.includes('members')).init.body).event, 'order.refunded');
  assert.equal(JSON.parse(sent.find((x) => x.url.includes('tk.test')).init.body).status, 'refunded');
});

test('no delivery/Trackeador config: sale still confirmed and nothing is sent', async () => {
  const sent = [];
  const s = await boot('file', {}, async (u) => { sent.push(u); return new Response('{}'); });
  await s.post('/api/intent', cart);
  await s.post('/webhook', JSON.stringify({ id: 'e1', type: 'payment_intent.succeeded', data: { object: { amount: 590, currency: 'eur', metadata: { order_id: cart.orderRef } } } }), { 'stripe-signature': 'ok' });
  assert.equal((await s.store.get(cart.orderRef)).status, 'paid');
  assert.equal(sent.length, 0);
});
