---
name: low-ficha-oferta
description: Etapa E2 do sistema LOW-TICKET — escreve a OFERTA.md (ficha da oferta), a primeira memória de toda oferta, a partir da modelagem escolhida pela dona. Toda etapa seguinte (página, entregável, funil, checkout, criativo) lê ela antes. Use depois do low-modelador ou quando a dona mudar o que a oferta é (público, preço, funil).
---

# low-ficha-oferta — E2, a ficha da oferta

**Entrada:** `pesquisa/modelador-*-etapa2.json` (ou análise manual) · `pesquisa/VALIDACAO-*.md` com a dona dizendo
"segue" (sem isso não começa) · escolhas da dona.
**Saída:** `OFERTAS/<slug>/OFERTA.md` + **`FUNIL.md`** aprovados pela dona · `CLAUDE.md` e `STATUS.md` da oferta criados.

## `OFERTA.md` — uma página, nesta ordem
```
# <Nome do produto> — ficha da oferta          (atualizado em AAAA-MM-DD)
## O que vendemos      o que o cliente recebe na mão (itens do entregável principal)
## O que NÃO é         o que não prometemos / não entregamos (ex.: não é serviço, não é curso em vídeo)
## Pra quem            1 público principal (quem PAGA, não quem usa) — e por que ele (dado do Modelador/venda)
## Dor                 sintoma · cena (vira imagem do criativo) · custo (o que faz clicar)
## Mercado e idioma    país(es), idioma, moeda
## Preço               entrada · âncora · planos (o mais barato vai no criativo)
## Funil               bônus · order bump(s) · upsell · downsell · upgrade · combo — nome + preço + que dor resolve
## De onde veio        anunciante original + link · caminho escolhido · o que corrigimos dele (buracos)
## Visual              paleta = a da página original (ou a que a dona pediu) · DESIGN-SYSTEM.md
## Regras do nicho     ex.: não prometer cura, não infantilizar, não falar "PDF"
## Ângulo final        preenchido só depois da E3 (headline aprovada): molde (Inventário/Domínio/Descoberta)
                       + headline + subheadline final. Enquanto vazio, `?`.
```
**Contraprova:** "se o cliente comprar, o que ele recebe na mão?" tem que ser item de "O que vendemos".

## Passos
1. Preencher a ficha do JSON da etapa 2 + o que a dona disse. Campo sem dado = `?`, nunca inventado.
2. **Funil pensado AQUI, antes da página** (a página e o checkout dependem dele): `FUNIL.md` com bônus, order
   bump(s), upsell, downsell, upgrade e combo — nome · dor que resolve · preço · o que entrega · onde aparece
   (página, checkout, pós-compra, painel). Fontes: `spyx.oferta_modelada` (bonus, order_bump, upsell, funil,
   alavanca_por_item) + funil dos concorrentes da `VALIDACAO` + regras da `low-funil` (próxima dor, bônus nunca
   vira produto, tabela de preços).
3. Mostrar ficha + funil à dona → ajustar → "aprovada em AAAA-MM-DD" no topo dos dois.
4. `CLAUDE.md` da oferta (curto): o que é em 1 linha + ponteiros (`OFERTA.md`, `STATUS.md`, `pesquisa/`) +
   seção "Memória da oferta" vazia.
5. `STATUS.md` a partir de `MODELOS/_MODELO-STATUS.md`: etapa atual = E2 feita.
6. Venda real contradiz a ficha (quem compra é outro público) → corrigir a ficha no mesmo dia.
Próximo: `low-pagina`.
