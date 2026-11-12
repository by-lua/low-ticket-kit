// Checkout catalog (EXAMPLE data: replace SKUs, names and prices per offer). Single source of price. Server-only: never trust an amount from the browser.
// Amounts are in minor units and already include VAT. Amounts are approved by the owner per offer.
// Stripe Price IDs below are sandbox references only (PaymentIntents carry amount + currency, not Prices).

export const WARRANTY_DAYS = 15;
export const CURRENCIES = Object.freeze(['eur', 'chf', 'cad']);
export const DEFAULT_CURRENCY = 'eur';
// Country (ISO-2) -> presentment currency. Anything else falls back to EUR.
export const MARKETS = Object.freeze({ FR: 'eur', BE: 'eur', CH: 'chf', CA: 'cad' });

const money = (eur, chf, cad) => Object.freeze({ eur, chf, cad });

// type: plan (the main purchase) | upgrade (replaces Basic with Complete at a promo TOTAL) | bump (extra, unchecked by default)
export const SKUS = Object.freeze({
  basic: Object.freeze({ type: 'plan', name: 'Basic', entitlement: 'basic', amount: money(590, 590, 890) }),
  complete: Object.freeze({ type: 'plan', name: 'Complete', entitlement: 'complete', amount: money(1290, 1290, 1990) }),
  // ADDITIVE upgrade (owner, 2026-11-11): Basic price + this add-on = the Complete plan at a discount.
  // 590 + 200 = 790 (EUR/CHF), 890 + 300 = 1190 (CAD): the same promo total the owner approved, shown as "plan + upgrade".
  upgrade: Object.freeze({
    type: 'upgrade',
    name: 'Upgrade to Complete',
    entitlement: 'complete',
    amount: money(200, 200, 300),
    bundleTotal: money(790, 790, 1190),
    bundleCompareAt: money(1290, 1290, 1990),
  }),
  bumpA: Object.freeze({
    type: 'bump',
    name: 'Bump A',
    blurb: 'Example description of bump A.',
    entitlement: 'bumpA',
    amount: money(590, 590, 890),
    compareAt: money(732, 732, 1104),
  }),
  bumpB: Object.freeze({
    type: 'bump',
    name: 'Bump B',
    blurb: 'Example description of bump B.',
    entitlement: 'bumpB',
    amount: money(390, 390, 590),
    compareAt: money(549, 549, 828),
  }),
  bumpC: Object.freeze({
    type: 'bump',
    name: 'Bump C',
    blurb: 'Example description of bump C.',
    entitlement: 'bumpC',
    amount: money(490, 490, 790),
    compareAt: money(690, 690, 1041),
  }),
});

export const BUMP_IDS = Object.freeze(Object.keys(SKUS).filter((id) => SKUS[id].type === 'bump'));

// Optional Stripe reference IDs for THIS offer (Product/Prices of the sandbox account). PaymentIntents do not use them; keep them in OFERTAS/<slug>/STRIPE-PAYPAL.md.
export const STRIPE_TEST_REFS = Object.freeze({ product: null, prices: Object.freeze({}) });

// Checkout language by country (UI only; the product content is French). Mixed-language countries follow the browser language.
const LANG_BY_COUNTRY = Object.freeze({
  FR: 'fr', BE: 'fr', CH: 'fr', CA: 'fr', LU: 'fr', MC: 'fr', RE: 'fr', GP: 'fr', MQ: 'fr', SN: 'fr', CI: 'fr', CM: 'fr', MA: 'fr', DZ: 'fr', TN: 'fr',
  PT: 'pt', BR: 'pt', ES: 'es', MX: 'es', AR: 'es', GB: 'en', IE: 'en', US: 'en',
});
const MIXED = new Set(['CA', 'CH', 'BE', 'LU']);
export const LANGUAGES = Object.freeze(['fr', 'en', 'es', 'pt']);
export function languageForCountry(country, acceptLanguage = '') {
  const c = String(country || '').toUpperCase();
  const pref = String(acceptLanguage).toLowerCase().split(',')[0].trim().slice(0, 2);
  if (MIXED.has(c) && LANGUAGES.includes(pref)) return pref;
  return LANG_BY_COUNTRY[c] ?? 'en';
}

export function currencyForCountry(country) {
  return MARKETS[String(country || '').toUpperCase()] ?? DEFAULT_CURRENCY;
}

function assertCurrency(currency) {
  if (!CURRENCIES.includes(currency)) throw new RangeError('Unsupported currency');
}

/**
 * Resolve a cart on the server. Validation is strict so a tampered request cannot change what is charged.
 * @param {{currency:string, plan:'basic'|'complete', upgrade?:boolean, bumps?:string[]}} input
 */
export function quote({ currency, plan, upgrade = false, bumps = [] }) {
  assertCurrency(currency);
  if (plan !== 'basic' && plan !== 'complete') throw new RangeError('Unknown plan');
  if (upgrade && plan !== 'basic') throw new RangeError('Upgrade only applies to the Basic plan');
  if (!Array.isArray(bumps) || new Set(bumps).size !== bumps.length) throw new RangeError('Invalid bumps');
  for (const id of bumps) if (!BUMP_IDS.includes(id)) throw new RangeError('Unknown bump');

  const lines = [];
  const entitlements = new Set();
  const skuIds = [];
  const main = SKUS[plan];
  lines.push({ id: plan, name: main.name, amount: main.amount[currency], role: 'front' });
  skuIds.push(plan);
  if (upgrade) {
    const up = SKUS.upgrade;
    lines.push({ id: 'upgrade', name: up.name, amount: up.amount[currency], role: 'bump' });
    skuIds.push('upgrade');
    entitlements.add(up.entitlement); // Complete includes Basic, so only "complete" is granted
  } else {
    entitlements.add(main.entitlement);
  }
  for (const id of bumps) {
    const sku = SKUS[id];
    lines.push({ id, name: sku.name, amount: sku.amount[currency], role: 'bump' });
    entitlements.add(sku.entitlement);
    skuIds.push(id);
  }
  const total = lines.reduce((sum, line) => sum + line.amount, 0);
  return Object.freeze({
    currency,
    total,
    lines: Object.freeze(lines),
    skuIds: Object.freeze(skuIds),
    entitlements: Object.freeze([...entitlements]),
    warrantyDays: WARRANTY_DAYS,
    taxIncluded: true,
  });
}


// ---- Post-purchase upsell flow (one click, off-session charge on the card saved at checkout) ----
// EXAMPLE data: replace per offer. A stage is offered after the previous one is resolved; declining 'up1' offers 'down1'.
export const UPSELLS = Object.freeze({
  up1: Object.freeze({ type: 'upsell', name: 'Upsell A', blurb: 'Example description of upsell A.', entitlement: 'upsellA', amount: money(790, 790, 1190), compareAt: money(1490, 1490, 2190), onDecline: 'down1' }),
  down1: Object.freeze({ type: 'downsell', name: 'Downsell A', blurb: 'Example description of the cheaper alternative.', entitlement: 'downsellA', amount: money(390, 390, 590), compareAt: money(790, 790, 1190), onDecline: null }),
});
export const FIRST_UPSELL = 'up1';

export function resolveUpsell(stage, currency) {
  assertCurrency(currency);
  if (!Object.hasOwn(UPSELLS, stage)) throw new RangeError('Unknown upsell stage');
  const u = UPSELLS[stage];
  return Object.freeze({ id: stage, type: u.type, name: u.name, blurb: u.blurb, entitlement: u.entitlement, amount: u.amount[currency], compareAt: u.compareAt ? u.compareAt[currency] : null, currency, onDecline: u.onDecline });
}

/** Public catalog for the browser: display data only. Totals are always re-resolved by quote() on the server. */
export function publicCatalog(currency) {
  assertCurrency(currency);
  const view = (id) => {
    const sku = SKUS[id];
    return {
      id,
      type: sku.type,
      name: sku.name,
      blurb: sku.blurb ?? null,
      amount: sku.amount[currency],
      compareAt: sku.compareAt ? sku.compareAt[currency] : null,
      bundleTotal: sku.bundleTotal ? sku.bundleTotal[currency] : null,
      bundleCompareAt: sku.bundleCompareAt ? sku.bundleCompareAt[currency] : null,
    };
  };
  return { currency, warrantyDays: WARRANTY_DAYS, plans: ['basic', 'complete'].map(view), upgrade: view('upgrade'), bumps: BUMP_IDS.map(view) };
}
