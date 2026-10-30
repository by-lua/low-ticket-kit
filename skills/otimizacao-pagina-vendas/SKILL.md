---
name: otimizacao-pagina-vendas
description: Use esta skill sempre que alguém mencionar "página lenta", "otimizar carregamento", "pagespeed", "lighthouse" ou "velocidade da página de vendas". Audita, otimiza e valida performance mobile sem quebrar conversão, pixel Meta ou eventos de checkout.
---

# Otimização de página de vendas

> **TROCAR PÁGINA (14/10/2026):** se a otimização gerar uma página nova
> (V2) pra publicar no lugar da atual, rode `adstrackeador pagina comparar
> <atual> <nova>` ANTES de promover — nunca publique página sem o bloco fbq
> e o loader do Trackeador. Incidente real: oferta ficou ~1h sem pixel nenhum
> com anúncio rodando.

Meça a URL publicada antes de editar e salve o resultado:

```bash
mkdir -p _prints
npx --yes lighthouse 'https://exemplo.com' --only-categories=performance --form-factor=mobile --screenEmulation.mobile --throttling-method=simulate --output=json --output-path=_prints/perf-antes.json --chrome-flags='--headless=new --no-sandbox'
node - <<'NODE'
const x=require('./_prints/perf-antes.json'),a=x.audits;
console.log({score:Math.round(x.categories.performance.score*100),FCP:a['first-contentful-paint'].displayValue,LCP:a['largest-contentful-paint'].displayValue,TBT:a['total-blocking-time'].displayValue,CLS:a['cumulative-layout-shift'].displayValue,peso:a['total-byte-weight'].displayValue});
NODE
```

Priorize o elemento LCP e oportunidades reais; não altere texto ou layout para melhorar métricas artificialmente.

## Imagens

Redimensione para duas vezes o maior CSS exibido. Com ImageMagick, use o script `scripts/otimizar-webp.sh`:

```bash
scripts/otimizar-webp.sh assets/origem.webp assets/destino.webp 800 75
```

800 px serve hero de 400 px; 880/960 px serve peça de 440/480 px; 680 px serve bônus de até 340 px no celular. Reduza a qualidade (70, 65, 60) somente se ainda ultrapassar aproximadamente 80 KB e a inspeção visual estiver boa. Não recomprima arquivos que outro trabalho esteja editando.

Todo `img` precisa de `width` e `height` compatíveis com o arquivo. Abaixo da dobra, use `loading="lazy" decoding="async"`. O LCP precisa ser eager, prioritário e pré-carregado:

```html
<link rel="preload" as="image" href="assets/hero.webp" type="image/webp" fetchpriority="high">
<img src="assets/hero.webp" width="800" height="600" loading="eager" fetchpriority="high" decoding="async" alt="...">
```

Crie `srcset` apenas quando variantes menores gerarem economia real.

## Vídeos (regra da dona, 30/10/2026)

Todo vídeo da página fica **dentro de um player** e **leve** — nunca baixa no carregamento.

- Vídeo próprio: MP4 H.264 + AAC, 720p (vertical 720×1280), `-crf 28 -preset slow -movflags +faststart`; alvo ≤ ~4 MB
  por vídeo (subir o CRF se passar). Sem áudio → `-an`.
- `<video controls playsinline preload="none" poster="assets/video-poster.webp" width=".." height="..">` — poster em
  WebP leve (mesma regra das imagens). Nada de `autoplay` com vídeo pesado acima da dobra.
- VSL/vídeo longo: player externo (YouTube/Vimeo/Bunny) carregado só no clique (fachada: poster + botão play;
  o iframe só entra ao tocar).
- GIF animado não: vira MP4/WebM em `<video autoplay muted loop playsinline preload="none">` com poster.

## Fontes, CSS e scripts

Preconecte `fonts.gstatic.com` com `crossorigin`, carregue só pesos usados e prefira `display=swap` ou `optional`. Mantenha CSS crítico pequeno inline e remova código herdado só depois de testar modais, timer e CTAs.

Meta Pixel e Trackeador devem carregar com `async` ou `defer`, mas nunca serem removidos para inflar pontuação. Preserve `fbq('track', 'PageView')`, `data-tk-value`/`data-tk-currency` e um único dono do `InitiateCheckout`, evitando duplicidade browser/CAPI.

## Cache nginx

Para páginas estáticas, habilite gzip para texto e deixe HTML curto, assets imutáveis por um ano:

```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/javascript application/javascript application/json application/manifest+json image/svg+xml;
location ~* \.(?:css|js|mjs|json|svg|webp|avif|png|jpe?g|gif|ico|woff2?)$ { expires 1y; add_header Cache-Control "public, max-age=31536000, immutable" always; try_files $uri =404; }
location ~* \.html$ { add_header Cache-Control "public, max-age=300, must-revalidate" always; try_files $uri =404; }
```

Em Node, mantenha conteúdo autenticado privado e aplique a mesma política somente aos estáticos públicos.

## Checklist final

Antes de commit, rode `git status --short`, preserve alterações alheias, execute `git diff --check`, valide sintaxe e `docker build` quando houver Dockerfile. Depois do deploy, repita a mesma auditoria em `_prints/perf-depois.json` e compare score, FCP, LCP, TBT, CLS e peso.

O gate de conversão é obrigatório: capture em produção requests `facebook.com/tr`. A carga precisa enviar `ev=PageView`; cada CTA de checkout precisa enviar `ev=InitiateCheckout` com `value` e `currency` corretos. Registre URLs/valores/moedas capturados, além de headers de HTML, asset imutável e gzip. Reporte tabela antes/depois, commits e limitações de terceiros restantes.
