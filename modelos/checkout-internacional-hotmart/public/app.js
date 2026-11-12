import { makeT } from './i18n.js';
// checkout FR checkout (test build). The server is the source of truth for every amount.
let tr = makeT('fr');
const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];
const LOCALES = { FR: 'fr-FR', BE: 'fr-BE', CH: 'fr-CH', CA: 'fr-CA', LU: 'fr-LU', MC: 'fr-MC' };
const params = new URLSearchParams(location.search);
const rand = () => (crypto.randomUUID ? crypto.randomUUID().replace(/-/g, '') : String(Date.now()) + Math.random().toString(16).slice(2)).slice(0, 32);

const state = {
  country: 'FR', lang: 'fr', currency: 'eur', plan: params.get('plan') === 'complete' ? 'complete' : 'basic',
  upgrade: false, bumps: new Set(), catalog: null, quote: null, method: null,
  orderRef: rand(), tkid: params.get('_tkid') || params.get('tkid') || '', busy: false,
  stripe: null, elements: null, paymentEl: null, expressEl: null, cfg: null,
};

const api = async (path, body) => {
  const r = await fetch(path, body ? { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(body) } : undefined);
  const data = r.status === 204 ? {} : await r.json();
  if (!r.ok) throw Object.assign(new Error(data.error || 'Erreur'), { data });
  return data;
};
const track = (event, extra = {}) => { try { navigator.sendBeacon('/api/track', new Blob([JSON.stringify({ event, orderRef: state.orderRef, ...extra })], { type: 'application/json' })); } catch {} };
const fmtLocale = () => { const l = `${state.lang}-${state.country}`; try { return Intl.NumberFormat.supportedLocalesOf([l]).length ? l : state.lang; } catch { return state.lang; } };
const money = (minor) => new Intl.NumberFormat(fmtLocale(), { style: 'currency', currency: state.currency.toUpperCase() }).format(minor / 100);
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const cart = () => ({ currency: state.currency, plan: state.plan, upgrade: state.upgrade, bumps: [...state.bumps] });

// ---- Timer: 10:00 regressive, NO persistence (restarts on every visit/reload)
(() => { let s = 600; const el = $('#timer'); const p = (n) => String(n).padStart(2, '0');
  const t = () => { el.textContent = `${p(Math.floor(s / 3600))}:${p(Math.floor((s % 3600) / 60))}:${p(s % 60)}`; if (s > 0) s--; }; t(); setInterval(t, 1000); })();

// ---- Rendering
const BUMP_IMG = { bumpA: 'assets/img/bump-a.webp', bumpB: 'assets/img/bump-b.webp', bumpC: 'assets/img/bump-c.webp', upgrade: 'assets/img/cover.webp' };
function renderBumps() {
  const box = $('#bumps'); box.innerHTML = '';
  const item = (sku, kind) => {
    const on = kind === 'upgrade' ? state.upgrade : state.bumps.has(sku.id);
    const up = kind === 'upgrade';
    const refPrice = up ? sku.bundleCompareAt : sku.compareAt;
    const pct = refPrice ? Math.round((1 - (up ? sku.bundleTotal : sku.amount) / refPrice) * 100) : 0;
    const cmp = refPrice ? `<span class="gt-old">${money(refPrice)}</span><span class="gt-off">&#8595; ${pct}%</span>` : '';
    const name = up ? tr('upName') : tr(`${sku.id}Name`);
    const blurb = up ? tr('upDesc', { add: money(sku.amount), total: money(sku.bundleTotal), was: money(sku.bundleCompareAt) }) : tr(`${sku.id}Blurb`);
    const el = document.createElement('label');
    el.className = `gt-bump${on ? ' is-on' : ''}`;
    el.innerHTML = `<span class="gt-bump-top">
        <img class="gt-bump-img" src="${BUMP_IMG[sku.id] || BUMP_IMG.upgrade}" width="72" height="72" alt="">
        <span class="gt-bump-info"><b class="gt-bump-title">${esc(name)}</b>
        <span class="gt-bump-desc">${esc(blurb)}</span>
        <span class="gt-bump-prices">${cmp}</span><strong class="gt-bump-price">${up ? '+ ' : ''}${money(sku.amount)}</strong></span></span>
      <span class="gt-bump-add"><input type="checkbox" data-bump="${sku.id}" ${on ? 'checked' : ''}><span>${esc(tr('addProduct'))}</span></span>`;
    box.append(el);
  };
  if (state.plan === 'basic' && state.catalog.upgrade) item(state.catalog.upgrade, 'upgrade');
  for (const b of state.catalog.bumps) item(b, 'bump');
}

const lineName = (l) => (l.id === 'basic' ? tr('planEss') : l.id === 'complete' ? tr('planComp') : l.id === 'upgrade' ? tr('upLine') : tr(`${l.id}Name`));
function renderTotals() {
  const q = state.quote;
  $$('[data-total]').forEach((e) => { e.textContent = money(q.total); });
  $$('[data-planprice]').forEach((e) => { e.textContent = money(q.lines[0].amount); });
  $('#planname').textContent = state.upgrade || state.plan === 'complete' ? tr('planComp') : tr('planEss');
  $('#lines').innerHTML = q.lines.map((l) => `<div class="gt-line"><span>${esc(lineName(l))}</span><span>${money(l.amount)}</span></div>`).join('');
  $$('.gt-bump').forEach((el) => { const c = el.querySelector('input'); el.classList.toggle('is-on', c.checked); });
}

// ---- i18n: swap every marked string; language follows the country (IP or picker)
function applyI18n() {
  document.documentElement.lang = state.lang;
  $$('[data-i18n]').forEach((e) => { const n = e.dataset.n; e.textContent = tr(e.dataset.i18n, n ? { n } : {}); if (e.tagName === 'TITLE') document.title = e.textContent; });
  $$('[data-i18n-ph]').forEach((e) => { e.placeholder = tr(e.dataset.i18nPh); });
  $$('[data-i18n-aria]').forEach((e) => { e.setAttribute('aria-label', tr(e.dataset.i18nAria)); });
  $$('[data-i18n-alt]').forEach((e) => { e.alt = tr(e.dataset.i18nAlt); });
  const w = state.quote ? state.quote.warrantyDays : 15;
  $$('[data-warranty]').forEach((e) => { e.textContent = String(w); });
  $$('[data-i18n="guarantee"]').forEach((e) => { e.textContent = tr('guarantee', { n: w }); });
  $('#proofcount').textContent = tr('clientsMade');
  try { sessionStorage.setItem('gt_lang', state.lang); } catch {}
  if (state.catalog) { renderBumps(); if (state.quote) renderTotals(); }
  paintCountry(); renderTestimonials();
}

async function refresh() {
  state.quote = await api('/api/quote', cart());
  renderTotals();
  if (state.elements) {
    try { state.elements.update({ amount: state.quote.total, currency: state.currency, setupFutureUsage: $('#savecard').checked ? 'off_session' : null }); } catch {}
  }
}

async function loadCatalog() {
  state.catalog = await api(`/api/catalog?currency=${state.currency}`);
  renderBumps();
  await refresh();
  applyI18n();
}

// ---- Stripe
function mountStripe() {
  if (!state.stripe) return;
  if (state.elements) { state.paymentEl?.destroy(); state.expressEl?.destroy(); state.expressEl = null; }
  state.elements = state.stripe.elements({
    mode: 'payment', amount: state.quote.total, currency: state.currency, paymentMethodTypes: ['card'],
    setupFutureUsage: $('#savecard').checked ? 'off_session' : undefined,
    locale: state.lang, appearance: { theme: 'stripe', variables: { colorPrimary: '#b26a00', borderRadius: '10px', fontFamily: 'Inter, system-ui, sans-serif' } },
  });
  state.paymentEl = state.elements.create('payment', { layout: 'tabs', wallets: { applePay: 'never', googlePay: 'never' }, defaultValues: { billingDetails: { address: { country: state.country } } } });
  state.paymentEl.mount('#payment-element');
  if (state.method === 'applepay' || state.method === 'googlepay') showWallet(state.method);
}


// Apple Pay / Google Pay: one wallet button (Stripe Express Checkout). Real buttons need HTTPS + a registered domain + a wallet on the device.
function showWallet(kind) {
  if (!state.elements) return;
  state.expressEl?.destroy(); state.expressEl = null;
  const note = $('#walletnote'); note.classList.add('hidden');
  $('#express').innerHTML = '';
  try {
    state.expressEl = state.elements.create('expressCheckout', {
      paymentMethods: { applePay: kind === 'applepay' ? 'always' : 'never', googlePay: kind === 'googlepay' ? 'always' : 'never', link: 'never', paypal: 'never' },
      buttonHeight: 48,
    });
    state.expressEl.on('ready', (e) => {
      if (!e.availablePaymentMethods) {
        note.textContent = tr(kind === 'applepay' ? 'walletApple' : 'walletGoogle');
        note.classList.remove('hidden');
      }
    });
    state.expressEl.on('click', (e) => { track('InitiateCheckout', { method: kind, value: state.quote.total / 100, currency: state.currency.toUpperCase() }); e.resolve({ emailRequired: true }); });
    state.expressEl.on('confirm', async (e) => { await payWithWallet(e); });
    state.expressEl.mount('#express');
  } catch { note.textContent = tr('walletFail'); note.classList.remove('hidden'); }
}

function showError(msg) { const p = $('#paymsg'); p.textContent = msg; p.classList.toggle('hidden', !msg); }
function validEmail() {
  const v = $('#email').value.trim();
  const ok = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);
  $('#err').classList.toggle('hidden', ok);
  if (!ok) { $('#email').focus(); $('#email').scrollIntoView({ behavior: 'smooth', block: 'center' }); }
  return ok ? v.toLowerCase() : null;
}
const returnUrl = () => `${location.origin}/merci.html?order=${state.orderRef}&lang=${state.lang}`;

async function createIntent(email) {
  return api('/api/intent', { ...cart(), email, orderRef: state.orderRef, tkid: state.tkid, saveCard: $('#savecard').checked });
}

async function payWithCard() {
  const email = validEmail(); if (!email) return;
  if (state.busy) return; state.busy = true;
  const btn = $('#buybtn'); btn.disabled = true; btn.classList.add('opacity-60'); showError('');
  try {
    track('InitiateCheckout', { method: 'card', value: state.quote.total / 100, currency: state.currency.toUpperCase() });
    const sub = await state.elements.submit();
    if (sub.error) throw new Error(sub.error.message);
    const { clientSecret } = await createIntent(email); // the ONLY place the charge is created
    const res = await state.stripe.confirmPayment({ elements: state.elements, clientSecret, confirmParams: { return_url: returnUrl(), receipt_email: email }, redirect: 'if_required' });
    if (res.error) throw new Error(res.error.message);
    location.href = returnUrl();
  } catch (e) {
    showError(e.message || tr('errPay'));
    state.busy = false; btn.disabled = false; btn.classList.remove('opacity-60');
  }
}

async function payWithWallet(ev) {
  const email = (ev.billingDetails && ev.billingDetails.email) || ($('#email').value || '').trim();
  if (state.busy) return; state.busy = true;
  try {
    const sub = await state.elements.submit(); if (sub.error) throw new Error(sub.error.message);
    const { clientSecret } = await createIntent(email);
    const res = await state.stripe.confirmPayment({ elements: state.elements, clientSecret, confirmParams: { return_url: returnUrl() }, redirect: 'if_required' });
    if (res.error) throw new Error(res.error.message);
    location.href = returnUrl();
  } catch (e) { showError(e.message); state.busy = false; }
}

async function payWithPaypal() {
  const email = validEmail(); if (!email) return;
  if (state.busy) return; state.busy = true;
  const btn = $('#buybtn'); btn.disabled = true; btn.classList.add('opacity-60'); showError('');
  try {
    track('InitiateCheckout', { method: 'paypal', value: state.quote.total / 100, currency: state.currency.toUpperCase() });
    const r = await api('/api/paypal/order', { ...cart(), email, orderRef: state.orderRef, tkid: state.tkid });
    if (!r.approveUrl) throw new Error(tr('errPaypal'));
    location.href = r.approveUrl;
  } catch (e) {
    showError(e.message || tr('errPaypal'));
    state.busy = false; btn.disabled = false; btn.classList.remove('opacity-60');
  }
}

// ---- Events
document.addEventListener('change', async (e) => {
  const t = e.target;
  if (t.matches('[data-bump]')) {
    if (t.dataset.bump === 'upgrade') state.upgrade = t.checked; else t.checked ? state.bumps.add(t.dataset.bump) : state.bumps.delete(t.dataset.bump);
    await refresh();
  } else if (t.id === 'savecard') { await refresh(); }
});

// ---- Country picker (Hotmart style + search): flag + "Changer de pays" under the banner; type to filter the list
const COUNTRIES = [["FR", "France"], ["BE", "Belgique"], ["CH", "Suisse"], ["CA", "Canada"], ["LU", "Luxembourg"], ["MC", "Monaco"], ["DE", "Allemagne"], ["ES", "Espagne"], ["IT", "Italie"], ["PT", "Portugal"], ["NL", "Pays-Bas"], ["AT", "Autriche"], ["IE", "Irlande"], ["GB", "Royaume-Uni"], ["US", "États-Unis"], ["BR", "Brésil"], ["AR", "Argentine"], ["MX", "Mexique"], ["MA", "Maroc"], ["DZ", "Algérie"], ["TN", "Tunisie"], ["SN", "Sénégal"], ["CI", "Côte d'Ivoire"], ["CM", "Cameroun"], ["RE", "La Réunion"], ["GP", "Guadeloupe"], ["MQ", "Martinique"]];
const norm = (t) => t.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
const flagImg = (c) => `<img src="assets/flags/${c.toLowerCase()}.svg" alt="" width="22" height="16" loading="lazy">`;
const regionNames = () => { try { return new Intl.DisplayNames([state.lang], { type: 'region' }); } catch { return null; } };
const countryName = (c) => { const dn = regionNames(); const base = (COUNTRIES.find((x) => x[0] === c) || [c, c])[1]; try { return (dn && dn.of(c)) || base; } catch { return base; } };
function paintCountry() {
  const known = COUNTRIES.some((x) => x[0] === state.country);
  $('#curflag').innerHTML = known ? flagImg(state.country) : '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.500 3 14.500 0 18M12 3c-3 3.500-3 14.500 0 18"/></svg>';
  $('#curname').textContent = state.country ? countryName(state.country) : tr('changeCountry'); // always name the detected country, even outside the list
}
function renderCountryList(q = '') {
  const n = norm(q.trim());
  const all = COUNTRIES.some((x) => x[0] === state.country) || !state.country ? COUNTRIES : [[state.country, countryName(state.country)], ...COUNTRIES];
  const rows = all.filter(([c, fr]) => !n || norm(countryName(c)).includes(n) || norm(fr).includes(n) || c.toLowerCase() === n);
  $('#countrylist').innerHTML = rows.length
    ? rows.map(([c]) => `<li role="option" data-c="${c}" aria-selected="${c === state.country}">${COUNTRIES.some((x) => x[0] === c) ? flagImg(c) : '<span class="gt-flag-globe">&#127760;</span>'}<span>${esc(countryName(c))}</span></li>`).join('')
    : `<li class="gt-empty">${esc(tr('noCountry'))}</li>`;
}
async function setCountry(c) {
  const ctx = await api(`/api/context?pays=${c}`);
  state.country = c; state.currency = ctx.currency; state.lang = ctx.lang; tr = makeT(state.lang);
  await loadCatalog(); // re-renders prices; applyI18n() runs inside
  state.stripe = window.Stripe ? window.Stripe(state.cfg.publishableKey, { locale: state.lang }) : state.stripe;
  mountStripe();
}
const closeCountry = () => { $('#countrymenu').classList.add('hidden'); $('#countrybtn').setAttribute('aria-expanded', 'false'); };
$('#countrybtn').addEventListener('click', (e) => {
  e.stopPropagation();
  const m = $('#countrymenu'); const open = m.classList.toggle('hidden') === false;
  $('#countrybtn').setAttribute('aria-expanded', String(open));
  if (open) { $('#countrysearch').value = ''; renderCountryList(); setTimeout(() => $('#countrysearch').focus(), 30); }
});
$('#countrymenu').addEventListener('click', async (e) => {
  e.stopPropagation();
  const li = e.target.closest('li[data-c]'); if (!li) return;
  closeCountry(); if (li.dataset.c !== state.country) await setCountry(li.dataset.c);
});
$('#countrysearch').addEventListener('input', (e) => renderCountryList(e.target.value));
$('#countrysearch').addEventListener('keydown', async (e) => {
  if (e.key === 'Escape') closeCountry();
  if (e.key === 'Enter') { const li = $('#countrylist li[data-c]'); if (li) { closeCountry(); if (li.dataset.c !== state.country) await setCountry(li.dataset.c); } }
});
document.addEventListener('click', closeCountry);

$$('[data-pay]').forEach((b) => b.addEventListener('click', () => {
  const anchorTop = b.getBoundingClientRect().top; // keep the clicked row where the finger is
  state.method = b.dataset.pay;
  $$('[data-pay]').forEach((x) => { x.classList.remove('is-on'); x.setAttribute('aria-checked', 'false'); });
  b.classList.add('is-on'); b.setAttribute('aria-checked', 'true');
  const wallet = state.method === 'applepay' || state.method === 'googlepay';
  $('#cardpanel').classList.toggle('hidden', state.method !== 'card');
  $('#walletpanel').classList.toggle('hidden', !wallet);
  showError('');
  if (wallet) showWallet(state.method);
  // The wallet button itself pays; card and PayPal use the green buy button.
  const u = $('#buy'); u.style.transition = 'none'; u.style.gridTemplateRows = wallet ? '0fr' : '1fr'; u.style.opacity = wallet ? '0' : '1';
  // A panel that closed above moves the row: compensate at once so nothing jumps.
  window.scrollBy({ top: b.getBoundingClientRect().top - anchorTop, behavior: 'instant' });
  // Keep the chosen method (and the card fields below it) on screen; never jump down to the buy button.
  setTimeout(() => { const panel = state.method === 'card' ? $('#cardpanel') : null; const r = (panel || b).getBoundingClientRect(); if (r.bottom > innerHeight || r.top < 0) (panel || b).scrollIntoView({ behavior: 'smooth', block: 'nearest' }); }, 350); // move only if the form is cut off
}));
$('#buybtn').addEventListener('click', () => (state.method === 'paypal' ? payWithPaypal() : state.method === 'card' ? payWithCard() : showError(tr('errChoose'))));

// ---- Boot
(async () => {
  const qs = new URLSearchParams(); if (params.get('pays')) qs.set('pays', params.get('pays')); if (params.get('lang')) qs.set('lang', params.get('lang'));
  const [cfg, ctx] = await Promise.all([api('/api/config'), api('/api/context' + (qs.toString() ? `?${qs}` : ''))]);
  state.cfg = cfg; state.country = ctx.country; state.currency = ctx.currency; state.lang = ctx.lang; tr = makeT(state.lang);
  paintCountry();
  if (!cfg.paypal) $('#paypal-tile').classList.add('hidden');
  // Show a wallet only where it can really be used: the Stripe account offers it AND the device can pay with it.
  // Apple Pay: Safari on iPhone/iPad/Mac with a card in Wallet. Google Pay: not on Apple devices.
  {
    const w = cfg.wallets || { applePay: true, googlePay: true };
    let apple = false;
    try { apple = Boolean(window.ApplePaySession && window.ApplePaySession.canMakePayments()); } catch {}
    const isApple = /iPhone|iPad|Macintosh/.test(navigator.userAgent) && /Safari/.test(navigator.userAgent) && !/Chrome|CriOS|Edg|Firefox|FxiOS/.test(navigator.userAgent);
    const hide = (m) => { const b = document.querySelector(`[data-pay="${m}"]`); if (b) (b.closest('.gt-pm') || b).classList.add('hidden'); };
    if (!(w.applePay && apple)) hide('applepay');
    if (!w.googlePay || isApple) hide('googlepay');
  }
  if (cfg.mode !== 'test') $('#testbar').classList.add('hidden');
  await loadCatalog();
  // Lead capture on e-mail blur (remarketing): stored by the tracking log in this test build
  // Remember the e-mail on this device: a buyer who leaves and comes back finds it filled (browser storage only, never sent anywhere else).
  const EMAIL_KEY = 'ck_email';
  try { const saved = localStorage.getItem(EMAIL_KEY); if (saved && !$('#email').value) $('#email').value = saved; } catch {}
  $('#email').addEventListener('input', () => { const v = $('#email').value.trim(); try { if (/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) localStorage.setItem(EMAIL_KEY, v.toLowerCase()); } catch {} });
  $('#email').addEventListener('blur', () => { const v = $('#email').value.trim(); if (/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) track('Lead', { }); });
  if (cfg.publishableKey && window.Stripe) { state.stripe = window.Stripe(cfg.publishableKey, { locale: state.lang }); mountStripe(); }
})().catch((e) => showError(e.message || tr('errLoad')));

// ---- Prova social: contador (regra da casa: número não redondo, fixo por visita) + depoimentos (placeholders só em teste)
state.proofN = 700 + Math.floor(Math.random() * 180);
let TESTI = null;
function renderTestimonials() {
  const box = $('#testimonials'); const count = $('#proofcount');
  if (!TESTI || !TESTI.items || !TESTI.items.length) return;
  const hide = TESTI.placeholder && state.cfg && state.cfg.mode !== 'test'; // unverified layout placeholders never reach production
  count.classList.toggle('hidden', !!hide); box.classList.toggle('hidden', !!hide);
  if (hide) return;
  box.innerHTML = TESTI.items.slice(0, 4).map((x) => `<div class="gt-t"><span class="gt-avatar" aria-hidden="true">${esc(x.name[0])}</span><div><p class="gt-t-name">${esc(x.name)} <span class="gt-stars">${'\u2605'.repeat(x.stars)}<i>${'\u2605'.repeat(5 - x.stars)}</i></span></p><p class="gt-t-text">${esc(x['text_' + state.lang] || x.text_pt)}</p></div></div>`).join('');
}
fetch('data/testimonials.json').then((r) => r.json()).then((d) => { TESTI = d; renderTestimonials(); }).catch(() => {});
