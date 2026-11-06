---
name: low-checkout
description: Etapa E8 do sistema LOW-TICKET — cadastra a oferta e as peças do funil no gateway, com banner, capa, PDF de entrega, webhooks nos 2 destinos e registro do código. Use para "cria o checkout", "cadastra na Wiven/Mundpay", "banner do checkout", "webhook", "link de checkout".
---

# low-checkout — E8, checkout

**Entrada:** página (E3) · `FUNIL.md` (E7) · `OFERTA.md` (preços, mercado).
**Saída:** produto + ofertas no gateway · link de checkout nos botões · linha em `_memoria/contas-e-codigos.md`.

## Antes de tudo
- **Fatos:** `_memoria/contas-e-codigos.md` (gateway, conta, código, perfil de browser). Nunca de cabeça.
- **Gateway pelo mercado:** BR → `wiven-checkout` (conta **LeadGo**; a Wiven EmpresaB está aposentada) ·
  EUR/USD → `mundpay` · global → `cooud-checkout` · LATAM → `zenith-gateway` · 250 Atividades → `ggcheckout-produto` ·
  Hotmart (quando a dona escolher) → `hotmart-produto-playwright`, seção "Rastreamento com o AdsTrackeador" obrigatória.
- **Trackeador na organização certa (incidente 04-06/11/2026, Calendrier FR):** a oferta foi criada na Leadgo, quando era da WINX, e o funil ficou sem medir.
  Antes de `trackeador init/checkout create/dashboard create`, confirme com a dona **de qual organização é a oferta**. Passe sempre `--org <org>` e `--dashboard <oferta>`.
  Nunca crie dashboard só para destravar um comando. Relate tudo o que criou (dashboard, conexão, pixel, host).
- **Uma oferta = um dashboard + uma conexão + um pixel próprios.** Não reaproveite o pixel de outra oferta ou de outro mercado.
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
   **Segredo do webhook igual nos 2 destinos e lido de onde o gateway manda.** Na Hotmart é o hottok, no HEADER
   `X-Hotmart-Hottok`. Servidor da área de membros que lê o token do corpo devolve 401 (Calendrier, 06/11/2026).
   Prova obrigatória: um evento real com resposta 2xx nos dois destinos. No Trackeador: último aviso OK, sem
   `secret_invalido`. Sem essa prova, o checkout NÃO está pronto.
   **Link de checkout leva a sessão:** o botão sai com `utm_*` e o id da visita no campo que o gateway devolve
   (Hotmart: `sck`, até 30 caracteres, sem `_`; Wiven: `utm_medium`; Mundpay: `_tkid`). Confira no navegador.
5. Suporte no checkout: e-mail e WhatsApp de `_memoria/empresa.md`; reembolso = menor prazo do gateway.
6. Links de checkout nos botões da página e do popup (preço igual ao botão).
7. **Registrar no mesmo dia** em `_memoria/contas-e-codigos.md`: gateway · conta · código de cada item · perfil.

Prova (preço, banner, webhooks): `low-gates-no-ar`.
