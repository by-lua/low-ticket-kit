---
name: low-gates-no-ar
description: Etapa E9 do sistema LOW-TICKET — prova no ar que a oferta está pronta pra tráfego: eventos do pixel, download do PDF na área de membros e checkout (preço, banner, webhooks). Use antes de liberar tráfego e depois de qualquer mudança em página, painel, servidor, preço, SKU ou webhook.
---

# low-gates-no-ar — E9, prova no ar

Nada vai pra tráfego sem os gates (eventos, página leve, download, checkout) com **prova colada** no `STATUS.md` da oferta. Nunca "deve estar funcionando".

## Gate 1 — Eventos (página)
Capturar requests `facebook.com/tr` no ar (headed + rede, skill `trackeador`):
- PageView ao carregar · cada etapa do quiz (se tiver) · outros eventos da página;
- **InitiateCheckout em TODO botão** que leva ao checkout, com `value` e `currency` certos do mercado.
- Sem `facebook.com/tr`: conferir se o fbq inline vem antes do Trackeador no `<head>`. Botão que só abre popup
  não leva href de checkout (IC dobrado). Página não manda IC próprio.

## Gate 1b — Página leve (performance)
- Lighthouse mobile no ar (comando em `otimizacao-pagina-vendas`): colar score, LCP, TBT e peso total.
- Nenhuma imagem acima de ~80 KB sem motivo; todo vídeo em player com `preload="none"` (ou fachada que carrega
  no clique); nenhum vídeo baixando no carregamento. Conferir na aba de rede: o que baixa ao abrir a página.
- Otimizar não pode quebrar o pixel: rodar o Gate 1 de novo depois.

## Gate 2 — Download (área de membros)
- `node scripts/check-download-pdf.mjs <url-da-oferta> <email-de-teste> [--lang=es]` (na raiz LOW-TICKET),
  **depois** do deploy terminar (~1 min no Coolify). Tem que sair OK em todo módulo com conteúdo.
  AVISO (404) = módulo sem páginas — conferir se é esperado; módulo COM páginas dando 404 = rota faltando.
- **Botão no leitor:** `grep -i pdf site/painel/index.html` acha o handler e o `pdfBottomButton`. Logar com a
  conta de teste, abrir um módulo e clicar.
- Bloco de dados do `painel/index.html` (de `PRINCIPAL_CATEGORIES` até `LOCK_SVG`) = só dado puro (helper/DOM
  ali derruba todos os PDFs com 500).

## Gate 3 — Checkout
- Abrir o checkout público: cobra exatamente o que o botão (e o popup/downsell) promete.
- Banner e imagem leves (≤ ~400 KB / ≤ ~250 KB).
- `/panel/webhooks` reaberto com **todos** os produtos da oferta nos 2 webhooks.
- Acesso liberado no `/painel` pelo modo teste oficial do gateway/Trackeador — nunca venda de teste no webhook
  de produção do Trackeador.

Fecho: prova de todos no `STATUS.md` → oferta pronta → `criativo` e `metaads-kevones`.
