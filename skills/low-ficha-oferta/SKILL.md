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
## Checkout            gateway + conta (conferido em _memoria/contas-e-codigos.md) · moeda · métodos de pagamento do
                       país · modelo (do gateway ou checkout-premium) · banner · bumps · garantia
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
2a. **CHECKLIST do modelo escolhido (dona, 04/11/2026) — todo item com resposta escrita no `FUNIL.md`/`OFERTA.md`:**
   1. **Título:** headline/sub pelas regras da `low-pagina` 1b (3 moldes) — opções por extenso.
   2. **Copy:** promessa, mecanismo, bullets na regra `recurso → ação → ganho → custo evitado`.
   3. **Objeções:** 5-8 na voz do comprador (abaixo, 2b).
   4. **Bônus:** cada um do original → manter / **melhorar** (pra matar qual objeção) / **cortar** (não faz sentido);
      **criar** bônus novo só onde sobrou objeção.
   5. **Order bumps:** cada bump do original → **usar igual / melhorar / cortar / virar upsell**; bump novo se faltar
      "próxima dor". Teto: 2-3 bumps (excesso = pressão no checkout).
   6. **Upsell:** padrão = **microSaaS do próprio produto** (app que faz o que o produto ensina/organiza; assinatura,
      `PECAS-DO-FUNIL.md` §3). Escrever **a copy do upsell** (título, 3 bullets, preço, CTA sim/não) já aqui.
   7. **Upgrade / downsell / saída:** preço e o que leva cada um.
   8. **Valores e checkout:** planos, moeda, gateway, métodos (ver campo Checkout).
   9. **Furos do SpyX** aplicados (2b) e **plano da página** (2c).
2b. **Melhorar a oferta — sempre, mesmo quando é o original "igual"** (dona, 04/11/2026). Antes de mostrar o funil:
   - **Objeções do avatar** = `spyx.persona.etapas[].objecao/duvida/desistiria_em` + buracos do diagnóstico +
     dor da `OFERTA.md`. Lista curta (5-8), cada uma em 1 frase na voz do comprador.
   - **Auditoria peça a peça do original** (bônus, bumps, upsell, downsell, upgrade) — tabela no `FUNIL.md`:
     `peça dele · objeção que mata · decisão (manter / melhorar como / cortar)`. Bônus sem objeção = corta ou funde.
   - **Peças novas** onde sobrou objeção sem resposta (bônus novo, garantia/prova, downsell) — cada uma com a
     objeção que mata e a "próxima dor" (`low-funil`). Sugestões do `spyx.oferta_modelada` entram aqui, filtradas.
   - **Alavancas:** partir das notas do SpyX (`alavancas_oferta_dele`, `fraquezas`, `lead_oferta_nova`) — cada
     mudança diz qual das 4 sobe/desce (transformação ↑, probabilidade ↑, tempo ↓, esforço ↓) e a alavanca mais
     fraca dele tem que ter pelo menos uma correção no funil ou no plano da página.
   - **Furos do SpyX APLICADOS, não só mostrados** (dona, 04/11/2026: "a oferta que copiamos tem furos e a gente
     melhora na nossa modelagem — leva pro outro país mais estruturada"). Tabela obrigatória no `FUNIL.md`:
     `furo dele (fraquezas + o que trava no lead_oferta_nova) · alavanca · correção nossa · onde entra (funil /
     plano da página / criativo / entregável)`. Todo furo sai com correção ou com "não corrigível agora — por quê".
     A E2e (copies) e a E3 (página) recebem essas correções já decididas.
   - Mostrar à dona **por extenso**: objeções → o que mudou no funil e por quê. A E3 usa isso direto (bônus no
     value stack, objeções no FAQ e nos cards).
2c. **Plano de melhoria da PÁGINA — decidido aqui, junto do funil** (dona, 04/11/2026: "na modelagem a gente já
   devia ter decidido isso também"). Ler a página original seção por seção (`REFERENCIA.md` + `spyx.pagina[]`) e
   escrever em `OFERTA.md` § **Plano da página**, por extenso:
   - **Títulos:** headline/sub dele × 3 opções nossas (moldes da `low-pagina` 1b) — ela escolhe ou deixa pra E3.
   - **Seções:** lista na ordem dele → o que **manter / reordenar / cortar / acrescentar** e por quê (objeção que
     resolve). Ex.: preço escondido → bloco de preço visível; prova inventada → corta sem buraco.
   - **Popup de saída** (oferta e texto), **barra de urgência** (só se real), **CTA** (destinos).
   - **Bônus na página:** como cada um aparece (value stack, card, mockup) — nome igual ao `FUNIL.md`.
   A E3 só executa o que foi aprovado aqui.
3. Mostrar ficha + funil + plano da página à dona → ajustar → "aprovada em AAAA-MM-DD" no topo.
4. `CLAUDE.md` da oferta (curto): o que é em 1 linha + ponteiros (`OFERTA.md`, `STATUS.md`, `pesquisa/`) +
   seção "Memória da oferta" vazia.
5. `STATUS.md` a partir de `MODELOS/_MODELO-STATUS.md`: etapa atual = E2 feita.
6. Venda real contradiz a ficha (quem compra é outro público) → corrigir a ficha no mesmo dia.
Próximo: `low-pagina`.
