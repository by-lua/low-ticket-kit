import assert from 'node:assert/strict';
import test from 'node:test';
import { quote, publicCatalog, currencyForCountry, languageForCountry, WARRANTY_DAYS } from './catalog.mjs';

test('approved plan totals per currency (VAT included)', () => {
  assert.equal(quote({ currency: 'eur', plan: 'basic' }).total, 590);
  assert.equal(quote({ currency: 'eur', plan: 'complete' }).total, 1290);
  assert.equal(quote({ currency: 'chf', plan: 'basic' }).total, 590);
  assert.equal(quote({ currency: 'cad', plan: 'complete' }).total, 1990);
});

test('upgrade is ADDITIVE: basic price + upgrade add-on = the Complete promo total', () => {
  const q = quote({ currency: 'eur', plan: 'basic', upgrade: true });
  assert.deepEqual(q.lines.map((l) => [l.id, l.amount]), [['basic', 590], ['upgrade', 200]]);
  assert.equal(q.total, 790);
  assert.deepEqual(q.skuIds, ['basic', 'upgrade']);
  assert.deepEqual(q.entitlements, ['complete']);
  assert.equal(quote({ currency: 'chf', plan: 'basic', upgrade: true }).total, 790);
  assert.equal(quote({ currency: 'cad', plan: 'basic', upgrade: true }).total, 1190);
  assert.ok(quote({ currency: 'eur', plan: 'basic', upgrade: true }).total < quote({ currency: 'eur', plan: 'complete' }).total);
});

test('bumps add to the total and grant their own entitlement', () => {
  const q = quote({ currency: 'eur', plan: 'basic', bumps: ['bumpA', 'bumpB', 'bumpC'] });
  assert.equal(q.total, 590 + 590 + 390 + 490);
  assert.ok(q.entitlements.includes('bumpA') && q.entitlements.includes('basic'));
  assert.equal(quote({ currency: 'cad', plan: 'complete', bumps: ['bumpA'] }).total, 1990 + 890);
});

test('rejects tampered carts instead of charging an arbitrary amount', () => {
  assert.throws(() => quote({ currency: 'usd', plan: 'basic' }), RangeError);
  assert.throws(() => quote({ currency: 'eur', plan: 'premium' }), RangeError);
  assert.throws(() => quote({ currency: 'eur', plan: 'complete', upgrade: true }), RangeError);
  assert.throws(() => quote({ currency: 'eur', plan: 'basic', bumps: ['upgrade'] }), RangeError);
  assert.throws(() => quote({ currency: 'eur', plan: 'basic', bumps: ['bumpA', 'bumpA'] }), RangeError);
});

test('country to currency mapping with EUR fallback', () => {
  assert.equal(currencyForCountry('FR'), 'eur');
  assert.equal(currencyForCountry('be'), 'eur');
  assert.equal(currencyForCountry('CH'), 'chf');
  assert.equal(currencyForCountry('CA'), 'cad');
  assert.equal(currencyForCountry('US'), 'eur');
  assert.equal(currencyForCountry(undefined), 'eur');
});

test('public catalog exposes display data and the 15-day warranty', () => {
  const c = publicCatalog('chf');
  assert.equal(c.warrantyDays, WARRANTY_DAYS);
  assert.equal(c.warrantyDays, 15);
  assert.equal(c.bumps.length, 3);
  assert.equal(c.upgrade.amount, 200);
  assert.equal(c.upgrade.bundleTotal, 790);
  assert.equal(c.upgrade.bundleCompareAt, 1290);
});

test('checkout language follows the country; mixed countries follow the browser language', () => {
  assert.equal(languageForCountry('FR'), 'fr');
  assert.equal(languageForCountry('BR'), 'pt');
  assert.equal(languageForCountry('ES'), 'es');
  assert.equal(languageForCountry('US'), 'en');
  assert.equal(languageForCountry('DE'), 'en');
  assert.equal(languageForCountry('CA', 'en-CA,en;q=0.9'), 'en');
  assert.equal(languageForCountry('CA', 'fr-CA,fr;q=0.9'), 'fr');
  assert.equal(languageForCountry('FR', 'en-US'), 'fr');
});
