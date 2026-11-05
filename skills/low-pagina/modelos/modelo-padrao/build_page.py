"""Gera site/index.html do Calendrier Magique FR em cima do template PaginaPro V1 (Fernando).
Base: CSS e classes do template; troca paleta, fontes, textos; planos no padrão Mapa do Tarot."""
import re, pathlib

CSS_SRC = "/tmp/paginapro-template/dist/assets/index-DC2kexsT.css"
OUT = pathlib.Path("~/Documentos/TRAMPO/PROJETOS/WORKING/PROJETOS - INTERNOS/LOW-TICKET/OFERTAS/calendrier-magique-fr/site/index.html")

css = open(CSS_SRC).read()
css = re.sub(r":root\{[^}]*\}", (
    ":root{--bg:#FBF6EF;--surface:#fff;--tint:#F7E7D6;--line:#ead6b8;--ink:#3F151F;--text:#2E1A1F;--muted:#6e5a5e;"
    "--green:#571C2B;--green-dark:#3F151F;--yellow:#C89B66;--radius:16px;--shadow:0 10px 26px #571c2b17;"
    "--font-title:'Libre Baskerville',Georgia,serif;--font-body:'DM Sans',system-ui,sans-serif}"), css, count=1)
css = re.sub(r"@font-face\{[^}]*\}", "", css)
css = css.replace("#0b934e", "#3F151F").replace("#0e9f55", "#571C2B").replace("#08733d", "#3F151F").replace("#0e9f5533", "#571c2b33")  # fontes Fira do template saem; usamos Google Fonts

OVER = """
/* ===== Calendrier FR sobre o PaginaPro ===== */
.offer-bar{background:#c1121f;position:sticky;top:0;z-index:40;font-size:12.5px}
.hero h1 em,.closing h2 em{color:var(--yellow);font-style:italic}
.hero{padding-top:18px!important;padding-bottom:28px!important}
.hero-flow{gap:10px!important}
.hero h1{font-size:clamp(24px,3.6vw,40px)!important;line-height:1.15!important;margin:0!important}
.hero-pill{margin:0!important}
.hero-mock{width:100%;max-width:470px;margin:0 auto;min-width:0}
.hero-mock img{width:auto!important;max-width:100%;max-height:34vh;margin:0 auto;display:block}
.hero-sub{font-size:14.5px!important;line-height:1.45!important;margin:0!important}
.hero-bullets{margin:0 auto!important;gap:4px!important}.hero-bullets li{font-size:13.5px!important}
@media(min-width:900px){.hero-mock img{max-height:36vh}}
@media(max-height:700px) and (max-width:899px){.hero-mock img{max-height:24vh!important}}
@media(max-height:780px) and (max-width:899px){.hero-mock img{max-height:28vh}.hero h1{font-size:23px!important}}
.hero-mock img{height:auto;border-radius:14px;filter:drop-shadow(0 22px 26px #571c2b40)}
.ph{background:repeating-linear-gradient(45deg,#fbf1e3,#fbf1e3 10px,#f4e3cc 10px,#f4e3cc 20px);border:1.5px dashed var(--yellow);
  color:#996549;display:flex;align-items:center;justify-content:center;text-align:center;font-size:11px;font-weight:800;
  letter-spacing:.06em;text-transform:uppercase;padding:14px;border-radius:12px}
.gallery-card .ph{aspect-ratio:3/4;width:100%}
.usage-photo .ph{aspect-ratio:4/5;width:100%}
.usage-photo img{aspect-ratio:4/5!important;height:auto!important;object-fit:cover;width:100%}
.mid-pitch-media .ph,.receive-media .ph{aspect-ratio:4/3;width:100%}
.bonus-art .ph{width:150px;height:190px;margin:0 auto}
/* fundos limpos */
.section.offer{background:var(--tint);color:var(--text)} .section.offer .section-title h2{color:var(--ink)}
.offer-close{color:var(--muted)}
.footer{background:var(--ink);color:#e6cfc4} .footer a{color:#f3dcc6}
/* planos — padrão Mapa do Tarot */
.plans2{width:100%;min-width:0;display:flex;gap:22px;flex-wrap:wrap;align-items:center;justify-content:center;max-width:780px;margin:8px auto 0;text-align:left}
.pcard{color:var(--text);position:relative;flex:1 1 300px;min-width:0;max-width:100%;background:#fff;border:2px solid var(--line);border-radius:18px;padding:30px 26px;display:flex;flex-direction:column}
.pcard:not(.best){flex:0.82 1 280px;padding:24px 22px}
.pcard.best{background:#fffaf3;border:2.5px solid var(--green);box-shadow:0 26px 50px -26px #571c2b80}
.ptag{position:absolute;top:-14px;left:50%;transform:translateX(-50%);white-space:nowrap;background:var(--ink);color:#fbeee0;
  font-weight:800;font-size:11px;letter-spacing:.1em;text-transform:uppercase;padding:5px 16px;border-radius:999px}
.pcard.best .ptag{background:var(--green)}
.pname{display:flex;align-items:center;gap:8px;font-family:var(--font-title);font-weight:700;font-size:18px;color:var(--green);margin-bottom:10px}
.pcard ul{list-style:none;padding:0;margin:0 0 16px;display:flex;flex-direction:column;gap:7px;flex:1}
.pcard li{display:flex;gap:9px;align-items:flex-start;font-size:14.5px;line-height:1.4}
.pcard li .ok{color:var(--green);font-weight:800;flex:none}
.pcard li.no{color:#a8999b;font-size:13px;text-decoration:line-through}
.pcard li.no .x{color:#d93025;font-weight:800;flex:none;text-decoration:none}
.pmock{text-align:center;margin-bottom:16px}.pmock img{width:100%;max-width:280px;height:auto;margin:0 auto;filter:drop-shadow(0 10px 18px #571c2b38)}
.pkick{font-weight:800;font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--green);margin-bottom:6px}
.pall{margin:0 0 12px;font-size:13.5px;font-weight:700;color:var(--ink)}
.pmain{display:flex;align-items:center;gap:10px;background:var(--green);color:#fff;border-radius:12px;padding:12px 14px;margin-bottom:14px}
.pmain b{display:block;font-size:14px;line-height:1.25}.pmain small{font-size:12px;opacity:.92}.pmain i{font-style:normal;font-size:26px}
.pcard li.pexcl{display:block;margin-top:4px}.pexcl p{margin:0 0 4px;font-weight:800;font-size:12px;letter-spacing:.04em;text-transform:uppercase;color:var(--muted)}
.pexcl span{display:block;font-family:var(--font-title);font-weight:700;font-size:14.5px;color:var(--green);margin-bottom:3px}
.pprice{font-family:var(--font-title);font-weight:700;font-size:44px;color:var(--ink);line-height:1;margin:6px 0 8px}
.pcard.best .pprice{color:var(--green)}
.pold{font-size:16px;color:#a8999b;text-decoration:line-through;margin-right:8px;font-family:var(--font-body);font-weight:400}
.pnote{margin:0 0 16px;font-size:13px;color:var(--muted)}
.btn.btn--ghost{background:#fff;color:var(--green);border:2px solid var(--green);box-shadow:none}
.pattn{display:none;text-align:center;margin-top:14px}
.pattn p{margin:0;font-weight:800;font-size:14px;color:var(--green);line-height:1.4}
.pattn div{display:flex;justify-content:center;gap:10px;color:var(--yellow);font-size:26px;margin-top:6px;animation:pb 1.2s infinite}
@keyframes pb{0%,100%{transform:translateY(0)}50%{transform:translateY(7px)}}
@media(max-width:820px){.pattn{display:block}}
.seal-wrap{position:relative;width:clamp(170px,38vw,210px);margin:0 auto;aspect-ratio:1}
.seal-glow{position:absolute;inset:-24%;background:radial-gradient(circle,rgba(227,205,142,.55) 0%,rgba(200,155,102,.28) 42%,transparent 68%);border-radius:999px}
.seal-img{position:relative;width:100%;height:auto;display:block;filter:drop-shadow(0 6px 16px rgba(154,120,41,.5))}
.steps-grid article>span{position:static!important;margin:0 auto 12px;width:40px;height:40px;font-size:17px;background:var(--green)!important;box-shadow:0 0 0 5px #c89b6633}
.steps-grid h3{font-size:20px}
.section-sub{text-align:center;color:var(--muted);max-width:560px;margin:-6px auto 0;font-size:16px}
.btn{white-space:normal!important;text-align:center;line-height:1.25;height:auto;overflow-wrap:anywhere}
.btn>span{flex:none}
.receive-media{height:auto!important;margin:0 auto 26px!important}
.receive-media{max-width:100%!important;min-width:0}
.receive-media img{max-height:520px;width:auto!important;max-width:100%!important}
@media(max-width:600px){.receive-media img{width:100%!important;max-height:none}}
.hero-feats{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;width:100%;max-width:640px;margin:2px auto 4px}
.feat{background:#fff;border:1px solid var(--line);border-radius:14px;padding:12px 8px;display:flex;flex-direction:column;align-items:center;text-align:center;gap:2px;box-shadow:0 8px 18px -14px #571c2b66}
.feat i{font-style:normal;font-size:20px;width:40px;height:40px;border-radius:50%;display:grid;place-items:center;background:var(--tint);border:1px solid var(--yellow);margin-bottom:4px}
.feat b{font-family:var(--font-title);font-size:14px;color:var(--ink);line-height:1.2}
.feat span{font-size:12px;color:var(--muted);line-height:1.3}
@media(max-width:600px){.feat{padding:9px 5px}.feat i{width:32px;height:32px;font-size:16px}.feat b{font-size:12.5px}.feat span{font-size:11px}}
.hb{list-style:none;padding:0;max-width:560px;text-align:left;display:grid;gap:9px!important}
.hb li{display:flex;gap:10px;align-items:flex-start;font-size:14.5px!important;line-height:1.4;color:var(--text)}
.hb li::before{content:'✓';flex:0 0 22px;height:22px;border-radius:50%;background:var(--green);color:#fff;font-size:12px;font-weight:800;display:grid;place-items:center;margin-top:1px}
.price-pill{display:inline-block;background:var(--tint);border:1.5px solid var(--yellow);color:var(--green);font-weight:800;font-size:16px;padding:8px 20px;border-radius:999px;margin:4px auto 0}
.trust-row{display:flex;flex-wrap:wrap;justify-content:center;gap:6px 16px;font-size:12.5px;color:var(--text)}
.trust-row span{display:inline-flex;align-items:center;gap:6px}
.trust-row span::before{content:'✓';width:18px;height:18px;border-radius:50%;background:#efd2a8;color:var(--green);font-size:11px;font-weight:800;display:grid;place-items:center}
@media(max-width:600px){.hb li{font-size:13.5px!important}.trust-row{font-size:11.5px;gap:4px 10px}}
@media(max-height:780px) and (max-width:899px){.hero-mock img{max-height:22vh!important}.hero h1{font-size:21px!important}.hb{gap:5px!important}.hb li{font-size:12.5px!important}.hb li:nth-child(3){display:none}.price-pill{font-size:14px;padding:6px 16px}.hero-flow{gap:8px!important}}
@media(max-height:700px) and (max-width:899px){.hero-mock img{max-height:19vh!important}.hero-sub{font-size:13px!important}.hero-pill{display:none!important}}
.mdl{display:none;position:fixed;inset:0;z-index:9999;background:#2e1a1fb8;backdrop-filter:blur(3px);padding:20px;overflow-y:auto}
.mdl.on{display:block}
.mdl-box{max-width:440px;margin:6vh auto;background:var(--bg);border-radius:22px;box-shadow:0 30px 70px #00000073;padding:30px 24px 26px;text-align:center;position:relative}
.mdl-x{position:absolute;top:12px;right:14px;background:none;border:0;font-size:26px;line-height:1;color:var(--muted);cursor:pointer}
.mdl-tag{display:inline-block;background:var(--green);color:#fff;font-weight:800;font-size:11px;letter-spacing:.12em;text-transform:uppercase;padding:6px 16px;border-radius:999px;margin-bottom:14px}
.mdl h3{font-family:var(--font-title);font-size:clamp(21px,4.6vw,26px);line-height:1.18;color:var(--ink);margin:0 0 10px}.mdl h3 em{color:var(--yellow)}
.mdl-box>p{margin:0 0 14px;font-size:15px;line-height:1.55;color:var(--text)}
.mdl ul{list-style:none;padding:0;margin:0 0 16px;display:flex;flex-direction:column;gap:8px;text-align:left}
.mdl li{display:flex;gap:8px;font-size:13.5px;line-height:1.4;color:var(--text)}.mdl li span{color:var(--green);font-weight:800}
.mdl-offer{background:#fff;border:2px solid var(--green);border-radius:16px;padding:18px 16px;margin-bottom:14px}
.mdl-price{display:flex;align-items:baseline;justify-content:center;gap:10px}.mdl-price s{color:#a8999b;font-size:16px}.mdl-price b{font-family:var(--font-title);font-size:40px;color:var(--green);line-height:1.1}
.mdl-sub{margin:4px 0;font-size:12.5px;color:var(--muted)}.mdl-hl{margin:0 0 12px;font-weight:800;font-size:13.5px;color:var(--green)}
.mdl-offer .btn{max-width:none}
.mdl-no{display:inline-block;font-size:13px;color:var(--muted);text-decoration:underline}
.hero-pill{font-size:10.5px!important;padding:5px 12px!important;letter-spacing:.08em}
/* ajuste 04/11: mockup maior, texto menor, barra mais fina */
.offer-bar{min-height:30px!important;padding:5px 10px!important;font-size:11px!important;line-height:1.25}
.hero h1{font-size:clamp(22px,3.2vw,36px)!important}
.hero-sub{font-size:13.5px!important}
.hb{gap:6px!important}.hb li{font-size:13px!important}.hb li::before{flex-basis:19px;height:19px;font-size:11px}
.hero-mock{max-width:520px!important}
.hero-mock img{max-height:44vh!important}
@media(min-width:900px){.hero-mock img{max-height:46vh!important}}
@media(max-height:780px) and (max-width:899px){.hero-mock img{max-height:35vh!important}.hero h1{font-size:20px!important}.hb li{font-size:12px!important}}
@media(max-height:700px) and (max-width:899px){.hero-mock img{max-height:33vh!important}}
@media(max-width:600px){.hide-m{display:none}.offer-bar{font-size:10px!important;white-space:nowrap}}
/* popup */
.pop{position:fixed;inset:0;background:#2e1a1f99;display:none;align-items:center;justify-content:center;z-index:60;padding:20px}
.pop.on{display:flex}
.pop-box{background:var(--bg);border:2px solid var(--yellow);border-radius:20px;max-width:420px;width:100%;padding:30px 24px;text-align:center;position:relative}
.pop-box h3{font-family:var(--font-title);color:var(--green);font-size:24px;margin:6px 0}
.pop-x{position:absolute;top:8px;right:12px;background:none;border:0;font-size:26px;color:var(--muted);cursor:pointer}
.pop-price{font-size:40px;font-weight:800;color:var(--green);margin:10px 0}.pop-price s{font-size:18px;color:var(--muted);margin-right:8px}
.nothanks{display:block;margin:12px auto 0;color:var(--muted);font-size:13px;background:none;border:0;cursor:pointer;text-decoration:underline}
"""

def gallery(n, label):
    cards = "".join(f'<figure class="gallery-card"><div class="ph">IMAGEM (E5) · {label} {i+1}</div></figure>' for i in range(n))
    return cards + cards.replace('<figure class="gallery-card">', '<figure class="gallery-card" aria-hidden="true">')

USAGE = [('calendrier-magique-fr/quotidien-frigo.webp', 'Une femme installe le calendrier de mars 2027 sur son frigo'), ('calendrier-magique-fr/quotidien-bureau.webp', 'Un homme écrit dans l’Agenda Magique d’avril 2027 à son bureau'), ('calendrier-magique-fr/quotidien-bus.webp', 'Une femme consulte le calendrier de septembre 2027 sur son téléphone dans le bus'), ('calendrier-magique-fr/quotidien-autel.webp', 'Une femme suit le calendrier de novembre 2027 près de son autel'), ('calendrier-magique-fr/quotidien-canape.webp', 'Une femme consulte l’Agenda Magique de février 2027 sur sa tablette dans le salon'), ('calendrier-magique-fr/quotidien-cafe.webp', 'Une femme note ses intentions dans l’Agenda Magique de juin 2027 à la terrasse d’un café'), ('calendrier-magique-fr/quotidien-impression.webp', 'Une femme récupère le calendrier de janvier 2027 à la sortie de son imprimante'), ('calendrier-magique-fr/quotidien-jardin.webp', 'Une femme consulte le calendrier de mai 2027 pendant sa cueillette au jardin'), ('calendrier-magique-fr/quotidien-mural.webp', 'Une femme consulte le calendrier de décembre 2027 affiché dans son entrée')]
usage = "".join(f'<figure class="usage-photo"><img src="img/usage/{f}" width="900" height="1125" loading="lazy" alt="{a}"></figure>' for f, a in USAGE)

BONUS = [
    ("Rituel de Passage 2026 → 2027", "Un rituel guidé pour clôturer 2026 et ouvrir 2027 avec une intention claire.", "Vous commencez l'année avec une intention, pas une liste oubliée.", "14,90 €"),
    ("Calendrier Lunaire 2027", "Toute l'année lunaire sur une seule page, à imprimer ou en fond d'écran.", "Vous savez d'un coup d'œil quand vient la prochaine lune.", "5,90 €"),
    ("Atlas Magique du Zodiaque", "12 pages, une par signe, avec correspondances et rituels.", "Chaque signe devient une page à consulter, pas une recherche.", "5,90 €"),
    ("Roue de l'Année et 8 Sabbats", "Les 8 sabbats, leur sens et quoi faire en 15 minutes.", "Fêter chaque sabbat avec ce que vous avez à la maison.", "7,90 €"),
    ("Guide de la Sorcière Débutante", "Outils de base, autel simple et première pratique.", "Commencer sans se perdre dans le vocabulaire.", "9,90 €"),
    ("12 Fonds d'écran Magiques", "Un fond d'écran par mois, dans l'énergie du cycle.", "Votre mois magique visible à chaque fois que vous ouvrez le téléphone.", "7,90 €"),
    ("Stickers Magiques", "Lunes, cristaux, plantes et symboles pour votre agenda.", "Personnaliser votre agenda et votre grimoire.", "9,90 €"),
]
bcards = "".join(
    f'<article class="bonus-card"><div class="bonus-card-top"><p class="bonus-num">BONUS {i+1:02d}</p><div class="bonus-art"><img src="img/bonus/{i+1:02d}.webp" width="900" height="900" loading="lazy" alt="{n}"></div></div>'
    f'<div class="bonus-card-body"><h3>{n}</h3><p>{d}</p><div class="bonus-gain"><span>{g}</span></div>'
    f'<div class="bonus-price"><s>{v}</s><strong>OFFERT AUJOURD\'HUI</strong></div></div></article>'
    for i, (n, d, g, v) in enumerate(BONUS))

HTML = f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Calendrier Magique 2027 — Édition Roue du Nord</title>
<meta name="description" content="12 calendriers mensuels illustrés et 12 pages d'Agenda Magique pour vivre 2027 au rythme de la lune et des sabbats.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="icon" type="image/svg+xml" href="img/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="img/favicon-32.png">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png">
<link rel="preload" as="image" href="img/kit-complet-700.webp">
<!-- TRACKING (E9): fbq inline + loader do Trackeador (skill trackeador). -->
<!-- Base: template PaginaPro V1 (Fernando) · MODELOS/MODELOS-DE-PAGINA/fernando/ -->
<style>{css}{OVER}</style></head>
<body><div id="root">
<div class="offer-bar">⚡ PRIX DE LANCEMENT<span class="hide-m"> + 7 BONUS</span> UNIQUEMENT AUJOURD'HUI <span data-today></span></div>
<main>

<section class="hero"><div class="content content--860 hero-flow">
  <p class="hero-pill"><span aria-hidden="true"></span>CALENDRIER MAGIQUE 2027</p>
  <h1>Votre Calendrier Magique <em>2027</em> est arrivé.</h1>
  <div class="hero-mock"><img src="img/kit-complet-700.webp" width="700" height="933" alt="Calendrier Magique 2027" fetchpriority="high"></div>
  <p class="hero-sub"><strong>12 calendriers illustrés + 12 pages d'Agenda Magique</strong> pour vivre chaque lune et chaque sabbat de 2027.</p>
  <ul class="hero-bullets hb">
    <li>Sachez chaque mois quand agir : lunes, sabbats et transits déjà placés.</li>
    <li>Pratiquez en 10 minutes avec le rituel du mois, cristaux, plantes et couleurs.</li>
    <li>Imprimez-le ou gardez-le sur votre téléphone, comme vous préférez.</li>
  </ul>
  <span class="price-pill">seulement 5,90 €</span>
  <a class="btn" href="#recebe">JE VEUX MON CALENDRIER<span aria-hidden="true">→</span></a>
  <div class="trust-row"><span>Accès immédiat</span><span>Garantie 14 jours</span><span>Paiement sécurisé</span></div>
</div></section>

<section class="section pain"><div class="content content--880 section-flow">
  <header class="section-title"><h2>Votre pratique magique<br>n'a pas besoin de s'arrêter en février.</h2></header>
  <div class="ornament" aria-hidden="true"><span></span></div>
  <div class="pain-grid">
    <div class="pain-chip"><span>Les semaines débordent</span></div><div class="pain-chip"><span>Les dates se mélangent</span></div>
    <div class="pain-chip"><span>Fichiers jamais ouverts</span></div><div class="pain-chip"><span>Sabbat oublié</span></div>
    <div class="pain-chip"><span>Pas d'idée de rituel</span></div><div class="pain-chip"><span>Pleine lune ratée</span></div>
  </div>
  <p class="bridge"><span>Celles qui pratiquent toute l'année ont </span><strong>un calendrier qui leur dit quoi faire, et quand.</strong></p>
</div></section>

<section class="section section--tint gallery" id="previas"><div class="content content--1180 section-flow">
  <header class="section-title"><h2>Découvrez les pages<br>que vous allez recevoir</h2></header>
  <div class="rail-stage gallery-rail"><button type="button" class="rail-arrow rail-arrow--left" aria-label="Précédent">‹</button>
    <div class="rail rail--loop" tabindex="0">{gallery(6, "page")}</div>
  <button type="button" class="rail-arrow rail-arrow--right" aria-label="Suivant">›</button></div>
</div></section>

<section class="section mechanism"><div class="content content--1120 section-flow">
  <header class="section-title"><h2>Chaque mois, votre pratique en 4 étapes :</h2></header>
  <div class="mechanism-grid">
    <article><span class="mechanism-icon">🌙</span><h3>Ouvrez le mois</h3><p>Le calendrier montre les lunes, le sabbat et les transits du mois.</p></article>
    <article><span class="mechanism-icon">🕯️</span><h3>Allumez une bougie</h3><p>L'Agenda Magique donne l'énergie, les cristaux, les plantes et les couleurs.</p></article>
    <article><span class="mechanism-icon">✨</span><h3>Suivez le rituel</h3><p>Un rituel de 10 minutes, étape par étape, sans matériel cher.</p></article>
    <article><span class="mechanism-icon">📝</span><h3>Notez votre intention</h3><p>Les questions de réflexion et les notes ferment le cycle.</p></article>
  </div>
  <p class="mechanism-close">Rien à préparer : ce soir, 10 minutes suffisent pour reprendre le fil.</p>
  <a class="btn" href="#oferta">JE CHOISIS MA FORMULE<span aria-hidden="true">→</span></a>
</div></section>

<section class="usage-carousel"><div class="content content--860 usage-heading"><p>DANS LA VRAIE VIE</p><h2>Un calendrier fait pour votre quotidien.</h2><span>Sur le frigo, à côté de l'autel, sur le téléphone ou imprimé dans votre grimoire.</span></div>
  <div class="rail-stage usage-rail"><button type="button" class="rail-arrow rail-arrow--left" aria-label="Précédent">‹</button><div class="rail rail--loop" tabindex="0">{usage}</div><button type="button" class="rail-arrow rail-arrow--right" aria-label="Suivant">›</button></div>
</section>

<section class="section mid-pitch"><div class="content content--1040 mid-pitch-grid">
  <div class="mid-pitch-media"><div class="ph">IMAGEM (E5) · mockup diferente do topo (agenda aberta)</div></div>
  <div class="mid-pitch-copy"><h2>Combien de pleines lunes et de sabbats sont passés cette année sans que vous les fêtiez ?</h2>
    <p>Avec le Calendrier Magique, chaque date a déjà sa place et son rituel. Vous ouvrez le mois et vous savez quoi faire.</p>
    <a class="btn" href="#oferta">JE VEUX MON CALENDRIER 2027<span aria-hidden="true">→</span></a></div>
</div></section>

<section class="section audiences"><div class="content content--1040 section-flow">
  <header class="section-title"><h2>Ce calendrier est fait pour vous si vous…</h2></header>
  <div class="audience-grid">
    <article><span></span><div><h3>Suivez déjà la lune</h3><p>Ayez enfin les phases, les sabbats et le rituel au même endroit.</p></div></article>
    <article><span></span><div><h3>Commencez en sorcellerie</h3><p>Pratiquez pas à pas, sans vous perdre dans le vocabulaire.</p></div></article>
    <article><span></span><div><h3>Abandonnez en février</h3><p>Le mois suivant est déjà prêt : il suffit de l'ouvrir.</p></div></article>
    <article><span></span><div><h3>Manquez de temps</h3><p>10 minutes par mois suffisent pour garder le fil.</p></div></article>
    <article><span></span><div><h3>Collectionnez des fichiers</h3><p>Remplacez les dossiers oubliés par un seul calendrier qui sert.</p></div></article>
    <article><span></span><div><h3>Aimez le papier</h3><p>Imprimez de belles pages illustrées pour votre grimoire.</p></div></article>
  </div>
</div></section>

<section class="section section--tint receive" id="recebe" style="scroll-margin-top:50px"><div class="content content--1000 section-flow">
  <header class="section-title"><h2>Tout ce qu'il faut pour vivre 2027, mois après mois</h2></header>
  <div class="receive-media"><img src="img/kit-complet-700.webp" width="700" height="933" loading="lazy" alt="Le Calendrier Magique 2027 complet" style="width:100%;max-width:420px;height:auto;margin:0 auto;display:block;border-radius:14px"></div>
  <article class="receive-card"><p class="access-badge">✦ 12 CALENDRIERS + 12 PAGES D'AGENDA + 7 BONUS</p><h3>Calendrier Magique 2027</h3>
    <p>Chaque mois suit la même structure : vous savez toujours où trouver la lune, le sabbat et le rituel.</p>
    <ul>
      <li><span>12 calendriers mensuels, une illustration exclusive par mois.</span></li>
      <li><span>Phases de lune, sabbats et transits astrologiques déjà marqués.</span></li>
      <li><span>Semaines du lundi au dimanche.</span></li>
      <li><span>12 pages d'Agenda Magique : énergie, déesses, cristaux, plantes, couleurs.</span></li>
      <li><span>Le rituel du mois en 10 minutes, étape par étape.</span></li>
      <li><span>Checklist spirituelle, questions de réflexion et notes du cycle.</span></li>
      <li><span>Guide d'impression : maison ou imprimerie.</span></li>
      <li><span>Fichiers haute résolution, à imprimer ou sur téléphone.</span></li>
    </ul></article>
</div></section>

<section class="section bonuses"><div class="content content--980 section-flow">
  <header class="bonus-intro"><p>ET CE N'EST PAS TOUT…</p><h2>AVEC LE COMPLET, VOUS RECEVEZ AUSSI</h2><span>7 BONUS EXCLUSIFS</span></header>
  <div class="bonus-grid">{bcards}</div>
</div></section>

<!-- DEPOIMENTOS: espaço reservado; só entra com depoimento real de compradora (ver STATUS) -->

<section class="section offer" id="oferta"><div class="content content--720 section-flow">
  <p class="countdown">⏳ L'OFFRE SE TERMINE DANS <strong data-countdown>--:--:--</strong></p>
  <header class="section-title"><h2>Choisissez la meilleure option pour vous :</h2></header>
  <div class="plans2">
    <div class="pcard">
      <span class="ptag">Essentiel</span>
      <div class="pname">✦ Calendrier Magique 2027</div>
      <ul>
        <li><span class="ok">✓</span>12 calendriers mensuels illustrés</li>
        <li><span class="ok">✓</span>12 pages d'Agenda Magique</li>
        <li><span class="ok">✓</span>Rituel « Ce soir, 10 minutes » + Guide d'impression</li>
        <li class="no"><span class="x">✗</span>Rituel de Passage 2026 → 2027</li>
        <li class="no"><span class="x">✗</span>Calendrier Lunaire 2027</li>
        <li class="no"><span class="x">✗</span>Atlas Magique du Zodiaque</li>
        <li class="no"><span class="x">✗</span>Roue de l'Année et 8 Sabbats</li>
        <li class="no"><span class="x">✗</span>Guide de la Sorcière Débutante</li>
        <li class="no"><span class="x">✗</span>12 Fonds d'écran + Stickers Magiques</li>
      </ul>
      <div class="pprice">5,90 €</div>
      <p class="pnote">⏱ Accès immédiat juste après l'achat</p>
      <a class="btn btn--ghost" data-plan="essentiel" data-tk-value="5.90" data-tk-currency="EUR" data-upsell="1" href="#">JE PRENDS L'ESSENTIEL<span aria-hidden="true">→</span></a>
      <div class="pattn"><p>ATTENTION : nous avons une offre encore meilleure pour vous ! Regardez juste en dessous</p><div><span>↓</span><span>↓</span><span>↓</span></div></div>
    </div>
    <div class="pcard best">
      <span class="ptag">★ Le préféré</span>
      <div class="pmock"><img src="img/kit-complet-700.webp" width="700" height="933" loading="lazy" alt="Le Complet : calendrier, agenda et 7 bonus"></div>
      <div class="pkick">Complet</div>
      <p class="pall">Tous les contenus — accès immédiat :</p>
      <div class="pmain"><i>🎁</i><div><b>BONUS : Rituel de Passage 2026 → 2027</b><small>Clôturez 2026 et ouvrez 2027 avec une intention claire</small></div></div>
      <ul>
        <li><span class="ok">✓</span>12 calendriers mensuels illustrés</li>
        <li><span class="ok">✓</span>12 pages d'Agenda Magique</li>
        <li><span class="ok">✓</span>Rituel « Ce soir, 10 minutes » + Guide d'impression</li>
        <li class="pexcl"><p>Bonus exclusifs :</p>
          <span>🎁 Calendrier Lunaire 2027</span><span>🎁 Atlas Magique du Zodiaque</span><span>🎁 Roue de l'Année et 8 Sabbats</span>
          <span>🎁 Guide de la Sorcière Débutante</span><span>🎁 12 Fonds d'écran + Stickers Magiques</span></li>
      </ul>
      <div class="pprice"><span class="pold">82,20 €</span>12,90 €</div>
      <p class="pnote">Accès immédiat — envoyé directement sur votre e-mail.</p>
      <a class="btn" data-plan="complet" data-tk-value="12.90" data-tk-currency="EUR" href="#">JE VEUX LE COMPLET<span aria-hidden="true">→</span></a>
    </div>
  </div>
  <p class="offer-close">✉ <strong>Accès immédiat</strong> envoyé sur votre e-mail dès la confirmation du paiement · paiement unique, sans abonnement.</p>
  <div class="seal-wrap"><div class="seal-glow" aria-hidden="true"></div><img class="seal-img" src="img/selo-14-jours.webp" width="600" height="600" loading="lazy" alt="Garantie satisfaite ou remboursée 14 jours"></div>
  <div style="max-width:580px;margin:6px auto 0;text-align:center"><h3 style="font-family:var(--font-title);font-size:clamp(20px,2.6vw,26px);color:var(--ink);margin:0 0 10px">Garantie inconditionnelle · Risque zéro</h3>
  <p style="margin:0;color:var(--text);line-height:1.65">Prenez votre calendrier, ouvrez-le, pratiquez. Si pour une raison quelconque vous sentez qu'il n'est pas pour vous, écrivez-nous dans les 14 jours et nous vous remboursons 100 %. Sans questions. Le risque est pour nous — vous n'avez qu'à décider de commencer.</p></div>
</div></section>



<section class="section section--tint access-steps"><div class="content content--980 section-flow">
  <header class="section-title"><h2>Comment ça marche après le paiement</h2></header>
  <p class="section-sub">Trois étapes simples : vous choisissez, vous recevez, vous commencez ce soir.</p>
  <div class="steps-grid">
    <article><span>1</span><h3>Choisissez votre formule</h3><p>Paiement unique et sécurisé par carte.</p></article>
    <article><span>2</span><h3>Recevez par e-mail</h3><p>Accès immédiat, tout est numérique.</p></article>
    <article><span>3</span><h3>Commencez ce soir</h3><p>Sur le téléphone, l'ordinateur ou imprimé.</p></article>
  </div>
  <a class="btn" href="#oferta">JE CHOISIS MA FORMULE<span aria-hidden="true">→</span></a>
</div></section>

<section class="section faq"><div class="content content--780 section-flow">
  <header class="section-title"><h2>Questions fréquentes</h2></header>
  <div class="faq-list">
    <details><summary>Qu'est-ce que je reçois ?</summary><p>Les 12 calendriers mensuels, les 12 pages d'Agenda Magique, le rituel du mois et le Guide d'impression. Le Complet ajoute les 7 bonus.</p></details>
    <details><summary>C'est un calendrier papier ?</summary><p>Non, il est numérique. Les pages sont en haute résolution : vous les imprimez chez vous ou en imprimerie, ou vous les consultez sur votre téléphone.</p></details>
    <details><summary>Ça marche sur le téléphone ?</summary><p>Oui, sur téléphone, tablette et ordinateur.</p></details>
    <details><summary>Je suis débutante, est-ce pour moi ?</summary><p>Oui. Chaque rituel tient en 10 minutes, et le Complet inclut le Guide de la Sorcière Débutante.</p></details>
    <details><summary>J'abandonne toujours en février…</summary><p>Le calendrier vous dit quoi faire chaque mois : vous n'avez rien à préparer, juste à ouvrir le mois en cours.</p></details>
    <details><summary>Quelle différence entre l'Essentiel et le Complet ?</summary><p>L'Essentiel contient le calendrier et l'agenda. Le Complet ajoute les 7 bonus.</p></details>
    <details><summary>Comment je reçois l'accès ?</summary><p>Par e-mail, juste après la confirmation du paiement.</p></details>
    <details><summary>Existe-t-il une garantie ?</summary><p>Oui : 14 jours satisfaite ou remboursée, par simple e-mail.</p></details>
  </div>
</div></section>

<section class="closing"><div class="content content--780 closing-inner">
  <p>PRIX DE LANCEMENT UNIQUEMENT AUJOURD'HUI</p>
  <h2>Votre Calendrier Magique <em>2027</em> est arrivé.</h2>
  <a class="btn" href="#oferta">JE CHOISIS MA FORMULE<span aria-hidden="true">→</span></a>
  <small>Produit numérique. Paiement unique.</small>
</div></section>
</main>
<footer class="footer"><div class="footer-inner"><p>Support : support@seudominio.com</p><p class="footer-legal">Produit numérique indépendant. Les rituels proposés sont des pratiques de bien-être et ne remplacent aucun avis professionnel.</p><p>LeadGo</p><nav><a href="#">Conditions générales</a><span>•</span><a href="#">Politique de confidentialité</a></nav></div></footer>
</div>

<!-- ===== POPUP DE UPGRADE (clique no Básico) — padrão Mapa do Tarot ===== -->
<div class="mdl" id="downsell" role="dialog" aria-modal="true" aria-labelledby="ds-title"><div class="mdl-box">
  <button type="button" class="mdl-x" data-close aria-label="Fermer">×</button>
  <span class="mdl-tag">Attendez — offre spéciale</span>
  <h3 id="ds-title">Prenez <em>tout</em> pour presque le même prix</h3>
  <p>Avant de prendre l'Essentiel, recevez le <strong>Complet avec les 7 bonus</strong> pour presque rien de plus.</p>
  <ul>
    <li><span>✓</span>Rituel de Passage 2026 → 2027</li>
    <li><span>✓</span>Calendrier Lunaire 2027 + Atlas Magique du Zodiaque</li>
    <li><span>✓</span>Roue de l'Année et 8 Sabbats + Guide de la Sorcière Débutante</li>
    <li><span>✓</span>12 Fonds d'écran + Stickers Magiques</li>
  </ul>
  <div class="mdl-offer">
    <div class="mdl-price"><s>12,90 €</s><b>7,90 €</b></div>
    <p class="mdl-sub">Le Complet : calendrier + agenda + 7 bonus</p>
    <p class="mdl-hl">Tout ça pour seulement 2 € de plus</p>
    <a class="btn" data-plan="upgrade" data-tk-value="7.90" data-tk-currency="EUR" href="#">OUI ! JE PASSE AU COMPLET — 7,90 €<span aria-hidden="true">→</span></a>
  </div>
  <a class="mdl-no" data-plan="essentiel" data-tk-value="5.90" data-tk-currency="EUR" href="#">Non merci, je continue avec l'Essentiel (5,90 €)</a>
</div></div>

<!-- ===== POPUP DE SAÍDA — padrão Mapa do Tarot ===== -->
<div class="mdl" id="exitpopup" role="dialog" aria-modal="true" aria-labelledby="ep-title"><div class="mdl-box">
  <button type="button" class="mdl-x" data-close aria-label="Fermer">×</button>
  <span class="mdl-tag">Attendez</span>
  <h3 id="ep-title">Attendez ! Avant de partir…</h3>
  <p>Prenez le <strong>Calendrier Magique 2027</strong> au prix le plus bas que nous ayons jamais proposé.</p>
  <div class="mdl-offer">
    <div class="mdl-price"><s>5,90 €</s><b>4,90 €</b></div>
    <p class="mdl-sub">Calendrier Magique 2027 — Essentiel</p>
    <a class="btn" data-plan="saida" data-tk-value="4.90" data-tk-currency="EUR" href="#">JE LE PRENDS À 4,90 €<span aria-hidden="true">→</span></a>
  </div>
  <a class="mdl-no" href="javascript:void(0)" data-close>Non merci</a>
</div></div>

<script>
const CONFIG = {{ checkoutUrl: {{ essentiel: "", upgrade: "", complet: "", saida: "" }} }}; // TODO E8: links Mundpay (upgrade = Complet a 7,90 no popup)
(() => {{
  const $$ = q => [...document.querySelectorAll(q)];
  const today = () => $$('[data-today]').forEach(e => e.textContent = new Date().toLocaleDateString('fr-FR'));
  today(); setInterval(today, 60000);
  const cd = () => {{ const n = new Date(), e = new Date(n); e.setHours(23,59,59,999); const s = Math.max(0, Math.floor((e - n) / 1000));
    return [s/3600|0, (s%3600)/60|0, s%60].map(v => String(v).padStart(2,'0')).join(':'); }};
  const tick = () => $$('[data-countdown]').forEach(x => x.textContent = cd()); tick(); setInterval(tick, 1000);
  $$('.rail-stage').forEach(st => {{ const r = st.querySelector('.rail'); if (!r) return;
    st.querySelector('.rail-arrow--left')?.addEventListener('click', () => r.scrollBy({{left: -r.clientWidth*.82, behavior:'smooth'}}));
    st.querySelector('.rail-arrow--right')?.addEventListener('click', () => r.scrollBy({{left: r.clientWidth*.82, behavior:'smooth'}}));
    let p = false; r.addEventListener('mouseenter', () => p = true); r.addEventListener('mouseleave', () => p = false);
    setInterval(() => {{ if (p || document.hidden) return; const a = r.children[0], b = r.children[1]; const step = b ? b.offsetLeft - a.offsetLeft : r.clientWidth*.82;
      if (r.scrollLeft + r.clientWidth >= r.scrollWidth - 4) r.scrollTo({{left: 0}}); else r.scrollBy({{left: step, behavior:'smooth'}}); }}, 3200);
  }});
  $$('[data-plan]').forEach(a => {{ const u = CONFIG.checkoutUrl[a.dataset.plan]; if (u) a.href = u; else a.addEventListener('click', e => {{ e.preventDefault(); alert('Checkout en cours de configuration.'); }}); }});

  const open = id => {{ document.getElementById(id).classList.add('on'); document.body.style.overflow = 'hidden'; }};
  const close = id => {{ document.getElementById(id).classList.remove('on'); document.body.style.overflow = ''; }};
  $$('.mdl').forEach(m => m.addEventListener('click', e => {{ if (e.target === m || e.target.closest('[data-close]')) close(m.id); }}));
  addEventListener('keydown', e => {{ if (e.key === 'Escape') $$('.mdl.on').forEach(m => close(m.id)); }});
  // Básico → popup de upgrade (antes do checkout)
  $$('[data-upsell]').forEach(a => a.addEventListener('click', e => {{ e.preventDefault(); e.stopImmediatePropagation(); open('downsell'); }}, true));
  // Saída: 1x por sessão; PC = mouse sai pelo topo; celular = botão voltar (depois de interação) ou 45s parada após ver os planos
  (() => {{
    const KEY = 'cm_exit_shown', START = Date.now(); let checkout = false, guard = 0;
    const can = () => {{ try {{ if (sessionStorage.getItem(KEY) === '1') return false; }} catch (e) {{}}
      return !checkout && Date.now() - START > 8000 && !document.querySelector('#downsell.on'); }};
    const show = () => {{ if (!can()) return; try {{ sessionStorage.setItem(KEY, '1'); }} catch (e) {{}} open('exitpopup'); }};
    document.addEventListener('click', e => {{ if (e.target.closest('[data-plan]')) checkout = true; guard = Date.now() + 1200; }}, true);
    if (matchMedia('(hover: hover) and (pointer: fine)').matches)
      document.addEventListener('mouseleave', e => {{ if (Date.now() > guard && e.clientY <= 0) show(); }});
    let armed = false;
    const arm = () => {{ if (armed) return; armed = true; try {{ history.pushState({{cmExit: 1}}, '');
      addEventListener('popstate', ev => {{ if (ev.state && ev.state.cmExit) return; if (Date.now() < guard) return; show(); try {{ history.pushState({{cmExit: 1}}, ''); }} catch (e) {{}} }}); }} catch (e) {{}} }};
    ['touchstart', 'click'].forEach(n => document.addEventListener(n, arm, {{once: true, passive: true}}));
    const plans = document.querySelector('.plans2');
    if (plans && 'IntersectionObserver' in window) {{ let t; const io = new IntersectionObserver(es => es.forEach(en => {{ if (en.isIntersecting) {{ io.disconnect();
      const reset = () => {{ clearTimeout(t); t = setTimeout(show, 45000); }}; ['scroll', 'touchstart', 'click'].forEach(n => addEventListener(n, reset, {{passive: true}})); reset(); }} }})); io.observe(plans); }}
  }})();
}})();
</script>
</body></html>
"""
OUT.write_text(HTML)
print("ok", len(HTML))
