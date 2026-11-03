---
name: low-checkout
description: Etapa E8 do sistema LOW-TICKET — cadastra a oferta e as peças do funil no gateway, com banner, capa, PDF de entrega, webhooks nos 2 destinos e registro do código. Use para "cria o checkout", "cadastra na Wiven/Mundpay", "banner do checkout", "webhook", "link de checkout".
---

# low-checkout — E8, checkout

**Entrada:** página (E3) · `FUNIL.md` (E7) · `OFERTA.md` (preços, mercado).
**Saída:** produto + ofertas no gateway · link de checkout nos botões · linha em `_memoria/contas-e-codigos.md`.

## Antes de tudo
- **Fatos:** `_memoria/contas-e-codigos.md` (gateway, conta, código, perfil de browser). Nunca de cabeça.
- **Gateway pelo mercado:** BR → `wiven-checkout` (conta **LeadGo**; a Wiven PNZ está aposentada) ·
  EUR/USD → `mundpay` · global → `cooud-checkout` · LATAM → `zenith-gateway` · 250 Atividades → `ggcheckout-produto`.
- **Um perfil de browser por pane**, sempre headed.

## Passos
1. Produto principal + ofertas (planos) + cada peça do funil (bump, upsell, downsell, upgrade, combo).
2. **Banner** desktop + mobile e **imagem do produto** (mockup 3D do entregável): `banner-checkout-gpt`.
   Leves: banner ≤ ~400 KB, foto ≤ ~250 KB (redimensionar + JPEG).
3. **PDF de entrega** (Wiven: Entregas → Arquivos, só no principal): nome = nome do produto, tudo clicável
   (botão + endereço + e-mail) — gerador em `MODELOS/PDF-DE-ENTREGA/`.
4. **Os 2 webhooks, todo produto** (principal, bump, upsell, downsell, upgrade, combo, membro):
   área de membros (`<site>/painel/api/webhooks/<gateway>`) **e** Trackeador (webhook de venda da conexão da
   oferta — endereço em `_memoria/contas-e-codigos.md`), "todos os produtos" OFF. **E no servidor** o offer
   code entra no mapeamento (`OFFERS`/`COMPLETO_OFFERS`/`MUNDPAY_NAME_SKUS`) — fora dele o comprador fica sem
   acesso com HTTP 200. Produto criado depois do webhook não entra sozinho.
   Nunca disparar venda de teste no webhook de produção do Trackeador (manda Purchase real pro Meta): usar o
   modo teste oficial ("Simular venda").
5. Suporte no checkout: e-mail e WhatsApp de `_memoria/empresa.md`; reembolso = menor prazo do gateway.
6. Links de checkout nos botões da página e do popup (preço igual ao botão).
7. **Registrar no mesmo dia** em `_memoria/contas-e-codigos.md`: gateway · conta · código de cada item · perfil.

Prova (preço, banner, webhooks): `low-gates-no-ar`.
