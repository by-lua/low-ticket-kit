import { makeT } from './i18n.js';
// V11 = REDIRECT mode: no card field on this page. Card / Apple Pay / Google Pay -> Stripe hosted page (POST /api/session);
// PayPal -> PayPal (POST /api/paypal/order). The server resolves every amount and creates the charge only on the buy click.
const V11 = {
  fr: { routeIdle: 'Choisissez un mode de paiement ci-dessus.', step2idle: 'Vous payez sur la page sécurisée', cardRow: 'Carte bancaire', cardSub: 'Visa, Mastercard, American Express', step1: 'Vous choisissez vos options ici', step3: 'Accès immédiat par e-mail',
    routeStripe: 'Vous finalisez sur la page de paiement sécurisée de Stripe.', routePaypal: 'Vous finalisez sur votre compte PayPal.',
    step2card: 'Vous saisissez votre carte sur Stripe', step2wallet: 'Vous confirmez avec {w} sur Stripe', step2paypal: 'Vous confirmez sur PayPal',
    ctaStripe: 'Continuer vers le paiement sécurisé', ctaPaypal: 'Continuer avec PayPal', ctaIdle: 'Acheter maintenant', redirecting: 'Redirection…', cancelled: 'Paiement annulé. Votre panier est toujours là.' },
  en: { routeIdle: 'Choose a payment method above.', step2idle: 'You pay on the secure page', cardRow: 'Card', cardSub: 'Visa, Mastercard, American Express', step1: 'You choose your options here', step3: 'Instant access by e-mail',
    routeStripe: 'You finish on the secure Stripe payment page.', routePaypal: 'You finish on your PayPal account.',
    step2card: 'You enter your card on Stripe', step2wallet: 'You confirm with {w} on Stripe', step2paypal: 'You confirm on PayPal',
    ctaStripe: 'Continue to secure payment', ctaPaypal: 'Continue with PayPal', ctaIdle: 'Buy now', redirecting: 'Redirecting…', cancelled: 'Payment cancelled. Your cart is still here.' },
  es: { routeIdle: 'Elige una forma de pago arriba.', step2idle: 'Pagas en la página segura', cardRow: 'Tarjeta', cardSub: 'Visa, Mastercard, American Express', step1: 'Eliges tus opciones aquí', step3: 'Acceso inmediato por e-mail',
    routeStripe: 'Terminas en la página de pago segura de Stripe.', routePaypal: 'Terminas en tu cuenta de PayPal.',
    step2card: 'Introduces tu tarjeta en Stripe', step2wallet: 'Confirmas con {w} en Stripe', step2paypal: 'Confirmas en PayPal',
    ctaStripe: 'Continuar al pago seguro', ctaPaypal: 'Continuar con PayPal', ctaIdle: 'Comprar ahora', redirecting: 'Redirigiendo…', cancelled: 'Pago cancelado. Tu carrito sigue aquí.' },
  pt: { routeIdle: 'Escolha uma forma de pagamento acima.', step2idle: 'Você paga na página segura', cardRow: 'Cartão', cardSub: 'Visa, Mastercard, American Express', step1: 'Você escolhe suas opções aqui', step3: 'Acesso imediato por e-mail',
    routeStripe: 'Você finaliza na página de pagamento segura da Stripe.', routePaypal: 'Você finaliza na sua conta PayPal.',
    step2card: 'Você digita o cartão na Stripe', step2wallet: 'Você confirma com {w} na Stripe', step2paypal: 'Você confirma no PayPal',
    ctaStripe: 'Continuar para o pagamento seguro', ctaPaypal: 'Continuar com PayPal', ctaIdle: 'Comprar agora', redirecting: 'Redirecionando…', cancelled: 'Pagamento cancelado. Seu carrinho continua aqui.' },
};
const t11 = (k, v = {}) => String((V11[state.lang] || V11.fr)[k] ?? V11.fr[k] ?? k).replace(/\{(\w+)\}/g, (_, x) => v[x] ?? '');
// Checkout (test build). The server is the source of truth for every amount.
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
  cfg: null,
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
  $$('[data-v11]').forEach((e) => { e.textContent = t11(e.dataset.v11); });
  paintRoute(); paintCountry(); renderTestimonials();
}

async function refresh() {
  state.quote = await api('/api/quote', cart());
  renderTotals();
}

async function loadCatalog() {
  state.catalog = await api(`/api/catalog?currency=${state.currency}`);
  renderBumps();
  await refresh();
  applyI18n();
}

function showError(msg) { const p = $('#paymsg'); p.textContent = msg; p.classList.toggle('hidden', !msg); }
function validEmail() {
  const v = $('#email').value.trim();
  const ok = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);
  $('#err').classList.toggle('hidden', ok);
  if (!ok) { $('#email').focus(); $('#email').scrollIntoView({ behavior: 'smooth', block: 'center' }); }
  return ok ? v.toLowerCase() : null;
}
const WALLET = { applepay: 'Apple Pay', googlepay: 'Google Pay' };
function paintRoute() {
  const m = state.method; const box = $('#route');
  $('#ctatext').textContent = !m ? t11('ctaIdle') : m === 'paypal' ? t11('ctaPaypal') : t11('ctaStripe');
  // The box is always shown with the same size: choosing a method only swaps its text, so the page never moves.
  box.classList.remove('hidden');
  box.dataset.via = !m ? '' : m === 'paypal' ? 'paypal' : 'stripe';
  $('#routetext').textContent = !m ? t11('routeIdle') : m === 'paypal' ? t11('routePaypal') : t11('routeStripe');
  $('#step2').textContent = !m ? t11('step2idle') : m === 'paypal' ? t11('step2paypal') : WALLET[m] ? t11('step2wallet', { w: WALLET[m] }) : t11('step2card');
}
function lockBtn(on) { const b = $('#buybtn'); b.disabled = on; b.classList.toggle('opacity-60', on); if (on) $('#ctatext').textContent = t11('redirecting'); else paintRoute(); }

// Card + Apple Pay + Google Pay: Stripe hosted page. Apple/Google Pay show there automatically when the device has the wallet.
async function payWithStripe() {
  const email = validEmail(); if (!email) return;
  if (state.busy) return; state.busy = true; lockBtn(true); showError('');
  try {
    track('InitiateCheckout', { method: state.method, value: state.quote.total / 100, currency: state.currency.toUpperCase() });
    const r = await api('/api/session', { ...cart(), email, orderRef: state.orderRef, tkid: state.tkid, lang: state.lang, back: '/stripe' });
    if (!r.url) throw new Error(tr('errPay'));
    location.href = r.url;
  } catch (e) { showError(e.message || tr('errPay')); state.busy = false; lockBtn(false); }
}

async function payWithPaypal() {
  const email = validEmail(); if (!email) return;
  if (state.busy) return; state.busy = true;
  lockBtn(true); showError('');
  try {
    track('InitiateCheckout', { method: 'paypal', value: state.quote.total / 100, currency: state.currency.toUpperCase() });
    const r = await api('/api/paypal/order', { ...cart(), email, orderRef: state.orderRef, tkid: state.tkid });
    if (!r.approveUrl) throw new Error(tr('errPaypal'));
    location.href = r.approveUrl;
  } catch (e) {
    showError(e.message || tr('errPaypal'));
    state.busy = false; lockBtn(false);
  }
}

// ---- Events
document.addEventListener('change', async (e) => {
  const t = e.target;
  if (t.matches('[data-bump]')) {
    if (t.dataset.bump === 'upgrade') state.upgrade = t.checked; else t.checked ? state.bumps.add(t.dataset.bump) : state.bumps.delete(t.dataset.bump);
    await refresh();
  }
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
  state.method = b.dataset.pay;
  $$('[data-pay]').forEach((x) => { x.classList.remove('is-on'); x.setAttribute('aria-checked', 'false'); });
  b.classList.add('is-on'); b.setAttribute('aria-checked', 'true');
  showError(''); paintRoute();
}));
$('#buybtn').addEventListener('click', () => (state.method === 'paypal' ? payWithPaypal() : state.method ? payWithStripe() : showError(tr('errChoose'))));
// Back from Stripe/PayPal with "cancel": keep the page as it was and say so.
window.addEventListener('pageshow', (e) => { if (e.persisted) { state.busy = false; lockBtn(false); } });

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
  { const u = $('#buy'); u.style.transition = 'none'; u.style.gridTemplateRows = '1fr'; u.style.opacity = '1'; } // buy button always in place (no late expansion)
  if (params.get('annule')) showError(t11('cancelled'));
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
