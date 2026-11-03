---
name: low-funil
description: Regras do funil (usadas na E2, quando o FUNIL.md é desenhado junto da ficha) e Etapa E7 do sistema LOW-TICKET — produz as peças do funil (bônus, order bump, upsell, downsell, upgrade Essencial→Completo, combo, ofertas de membro, ferramenta/microSaaS) a partir da ficha da oferta. Use para "monta o funil", "order bump", "upsell", "combo", "upgrade".
---

# low-funil — regras do funil (E2) e produção das peças (E7)

**O desenho do funil NÃO é aqui:** o `FUNIL.md` nasce na E2 (`low-ficha-oferta`), antes da página, usando as regras abaixo.
**Entrada (E7):** `FUNIL.md` aprovado · entregável principal pronto.
**Saída (E7):** entregável de cada peça + card no `/painel` + peça pronta pro checkout.

## Regras
- **Próxima dor:** cada peça resolve a dor que o principal NÃO resolve. Sem sobreposição entre peças.
- **Bônus nunca vira produto no checkout** (bônus mora dentro do principal/plano).
- **Bônus mata objeção, não é brinde solto:** antes de fechar a lista de bônus no `FUNIL.md`, lista as objeções
  que travam a compra desse avatar (preço alto pro que entrega? vai dar trabalho aplicar? serve pro meu caso
  específico? e se eu não conseguir usar?) e liga cada bônus a UMA objeção que ele mata. Bônus sem objeção
  clara atrás = corta ou funde com outro antes de aprovar o funil. Isso já sai pronto pra E3 (badge/card usam
  o nome oficial e a contagem real direto do `FUNIL.md` — ver `low-pagina` § sincronia de bônus).
- **Preços:** tabela em `low-ticket/references/PECAS-DO-FUNIL.md` §4 e `_memoria/empresa.md`. Ofertas de membro
  com desconto (área de membros). Nada de preço inventado.
- **Upgrade Essencial → Completo:** produto próprio, 1º order bump, só na oferta Básica. **Capa de upgrade/combo
  é regerada no GPT** com o título integrado (nunca colar texto em mockup pronto) — `banner-checkout-gpt`
  `references/CAPA-PRODUTO-UPGRADE-COMBO.md`.
- Ferramenta/microSaaS como peça: `PECAS-DO-FUNIL.md` §3.
- Entregável de cada peça segue a `low-entregavel` (imagem A4, página separada pra imprimir).

## Passos
1. Conferir o `FUNIL.md` aprovado na E2 (mudou algo? dona aprova de novo).
2. Entregável de cada peça (`low-entregavel`), card no `/painel` (`area-membros-netflix`).
3. Cadastro no gateway e webhooks → `low-checkout`.

Detalhe completo: `low-ticket/references/PECAS-DO-FUNIL.md` e skill `mvt-funil` (mecânica de funil, ativa).
