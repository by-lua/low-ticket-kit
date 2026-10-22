---
name: x1-cross-market-mvt
description: Adapta uma concepção Low Ticket já validada no Brasil pro modelo "X1 pague quanto quiser" automatizado, em outro país/idioma (hoje Argentina, México, Colômbia — espanhol neutro). Reaproveita a disciplina de concepção do método MVT ("O Processo") e troca só o mecanismo de entrega/cobrança: em vez de página+checkout fixo, um chat no site (widget Chatwoot ou bot próprio) entrega o produto de graça e cobra contribuição livre com piso mínimo via Zenith, liberando bônus por webhook. Use quando o usuário mencionar X1, "pague quanto quiser", pay-what-you-want, adaptar oferta pra gringo/AR/MX/CO, ou pedir pra rodar em outro país algo que já validou no Brasil.
---

# X1 Cross-Market — MVT adaptado pra "pague quanto quiser" automático

**Não é um método novo do zero.** É o MVT (`low-ticket-metodo-mvt`) com o mecanismo de
entrega/cobrança trocado. A disciplina de concepção — 9 elementos, 10 características,
"querer > precisar", os 4 elementos operacionais de modelagem — **é a mesma**. O que
muda é só a Fase 3 em diante: preço fixo + checkout → **contribuição livre com piso +
chat automático**.

**Viva/atualizável:** conforme mais mercado/gateway for testado, atualize esta skill —
ela é o ponto único de verdade pra esse mecanismo, não um documento de uma vez só.

---

## Quando usar isto em vez do MVT puro

| Sinal | Ação |
|---|---|
| Usuário quer rodar BR normal, preço fixo | `low-ticket-metodo-mvt` + `criacao-low-ticket-mvt`, sem esta skill |
| Usuário menciona X1, "pague quanto quiser", pay-what-you-want | Esta skill |
| Usuário quer adaptar algo **já validado no BR** pra AR/MX/CO | Esta skill — pule mineração, comece do passo 1 abaixo |
| Usuário quer minerar concepção nova direto em espanhol/gringo | `low-ticket-metodo-mvt` fase de mineração, trocando `country=BR` por `AR`/`MX`/`CO` na Biblioteca — depois volte pra esta skill na Fase 3 |

---

## O mecanismo (fixo, não modelar)

1. **Produto grátis primeiro.** A pessoa recebe o microproduto real (não teaser) sem
   pagar nada — é a moeda de reciprocidade que sustenta o "pague quanto quiser".
2. **Chat automático entrega**, não WhatsApp manual. Reaproveitar o **WebWidget
   isolado do Chatwoot** que o usuário já tem rodando (não um bot novo do zero) —
   ver `references/arquitetura-x1.md` pra detalhe de implementação.
3. **Depois da entrega, pede contribuição livre com piso mínimo por país** — nunca
   PWYW puro sem piso: a taxa fixa do Zenith (R$5-equivalente) devora contribuição
   pequena. Ver tabela de pisos abaixo.
4. **Zenith Elements abre fora do balão do chat** (checkout dinâmico embutido, não
   dentro da caixa de mensagem).
5. **Webhook assinado (HMAC) do Zenith libera o bônus.** Nunca libera por
   confirmação verbal/tela do usuário — só por `payment.captured` validado.

### Pisos mínimos por país (2026-09-09, revisar se a taxa do Zenith mudar)

| País | Moeda | Piso sugerido | Bônus em ~2× o piso |
|---|---|---|---|
| Argentina | ARS | 6.000 | ~12.000 |
| México | MXN | 79 | ~160 |
| Colômbia | COP | 15.000 | ~30.000 |

Pagamento local por país (confirmado, ver `references/arquitetura-x1.md`):
- **AR:** QR interoperável, Mercado Pago, DEBIN, CVU/CBU, cartão.
- **MX:** OXXO, PayCash, PayNet, SPEI, CoDi, cartão.
- **CO:** PSE, Nequi, Bre-B/Llave, cartão.

---

## Passo 1 — pegar a concepção validada no BR

Não minerar do zero. Puxar do Hub de Ofertas (`LOW-TICKET/HUB-OFERTAS/ofertas.json`,
ver Passo 0 de `criacao-low-ticket-mvt`) uma concepção com `status: rodando` ou
`venceu` — já provou que tem demanda no Brasil.

## Passo 2 — adaptação cultural (não é tradução)

> Imagens do entregável e da página no idioma novo: skill `traduzir-entregavel-imagem` (traduz por script, sem regenerar).

Rodar os 9 elementos da concepção de novo, mudando só o que muda por país:
- **Persona/comunicação:** espanhol neutro, não regionalismo de um país só — a menos
  que o usuário confirme rodar por país separado.
- **Nicho/subnicho:** confirmar que a dor/desejo atravessa cultura (ex: documento
  jurídico BR não atravessa — contrato de aluguel muda de lei por país; mapa mental
  de matéria escolar atravessa melhor).
- **Formato/mecanismo:** mantém, é o que já validou.

Se a concepção BR depende de lei/norma local (jurídico, fiscal), **não adapte
direto** — modele de novo a partir do território gringo, não force tradução.

## Passo 3 — Obra de Arte adaptada

Mesma estrutura da Obra de Arte 100K do MVT (concepção + 8 elementos + mapa da
vantagem), com 2 diferenças:
- **Preço vira "sugestão + piso"**, não dupla oferta fixa 17,90/27,90.
- **Garantia vira "produto já é seu, pagou o quanto quis"** — não tem reembolso
  tradicional porque não tem cobrança obrigatória antes da entrega.

## Passo 4 — arquitetura técnica

Ver `references/arquitetura-x1.md` (gerado 2026-09-09, cobre AR/MX/CO): fluxo do
chat, schema de estado (pagou básico vs pagou acima do piso), webhook, e a
recomendação de MVP — microproduto real + widget Chatwoot isolado + Zenith Elements
fora do balão.

---

## Regras que não mudam do MVT

- Sem persuasão, gatilho, storytelling na copy de entrega.
- Sem expert/autoridade fake.
- Produto precisa ser visual (ver regra de "produto visual é requisito" do MVT).
- Empilhar ofertas — não depender de uma só.

## Ferramentas

| Para | Use |
|---|---|
| Disciplina de concepção/modelagem | skill `low-ticket-metodo-mvt` |
| Condução multi-fase / Hub de Ofertas | skill `criacao-low-ticket-mvt` |
| Gateway, taxas, webhook, países | skill `zenith-gateway` |
| Widget de chat | Chatwoot do usuário (WebWidget isolado, não recriar do zero) |
