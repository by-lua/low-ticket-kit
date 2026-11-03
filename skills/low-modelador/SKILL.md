---
name: low-modelador
description: Etapas E1/E2 do sistema LOW-TICKET pelo MineraAds — roda o Modelador combinado (SpyX + Rato) num anunciante ou página, mostra os caminhos pra dona escolher, roda a modelagem do caminho escolhido e salva o relatório na oferta. Use quando a dona disser "roda o modelador", "modela essa oferta", "joga no MineraAds", ou depois do low-referencia.
---

# low-modelador — E1/E2 pelo MineraAds

O Modelador (SpyX + Rato) monta a oferta: extração do que o original tem (bônus, bump, upsell, downsell,
checkout), buracos, lead reagindo, alavancas, caminhos de modelagem, e — depois da escolha — oferta nossa,
funil, página seção por seção e criativo (ganchos, roteiros, copies, estáticos).

**Entrada:** link da Biblioteca do anunciante (`view_all_page_id`) ou da página de vendas.
**Saída:** `OFERTAS/<slug>/pesquisa/modelador-<AAAA-MM-DD>.md` + `.json`. **Rodou e não salvou = não feito.**

## Os 5 modos
| Modo | `modo` na API | O que faz | Quando usar |
|---|---|---|---|
| Rato | `rato` | Só caminhos de modelagem (subnichar, trocar ângulo/público/nicho/formato) a partir da leitura direta. | Rápido, sem diagnóstico de conversão — raramente o ponto de partida. |
| SpyX | `spyx` | Só diagnóstico profundo: 4 alavancas, persona cética reagindo etapa a etapa, oferta modelada, ganchos. Sem passar pelos 6 pilares antes. | Quando já se sabe o produto e só falta achar fraqueza de conversão/copy. |
| Rato+SpyX (Combinado) | `combinado` | SpyX primeiro, Rato abre caminhos **em cima** do diagnóstico SpyX. | Alternativa ao Raio-X+SpyX quando não precisa das 10 propostas estruturadas. |
| Raio-X | `raiox` | Leitura disciplinada pelos 6 pilares (público, resultado, conteúdo, mecanismo, formato, mercado), motor da oferta, voz do comprador, **10 propostas ranqueadas** trocando 1 decisão por vez (+ upgrade/cultural), com filtro comercial e classificação trocado/adaptado/mantido por pilar. | Decidir **qual produto** modelar a partir de uma referência. |
| **Raio-X+SpyX (padrão)** | `raiox` depois `combinado` | Roda o Raio-X, a dona escolhe 1 das 10 propostas, depois roda o Combinado nessa proposta escolhida (SpyX acha fraqueza de conversão nela, Rato detalha o funil). | **Default** desta skill — decide o produto primeiro (Raio-X), só depois ajusta a venda (SpyX). |

Raio-X decide **o quê** modelar (produto); SpyX decide **como vender** melhor. Por isso SpyX sempre entra
**depois** da escolha, nunca antes — misturar as duas camadas quebra a disciplina de "uma decisão trocada,
resto preservado".

## Como chamar
Token: `MINERAADS_EXT_KEY` (`set -a; source ~/.claude/.credentials.env; set +a`). Base: `$MINERAADS_URL`
(padrão `https://mineraads.leadgo.dev`). Contrato: `RATO-ADS/API-CONTRATO.md` § CLI.
- Comando (quando instalado, spec v3): `mineraads modelador analisar|caminhos|mercado|modelar|salvar`.
- Sem o comando: rotas com `Authorization: Bearer $MINERAADS_EXT_KEY`:
  1. **Fluxo padrão (Raio-X+SpyX), 3 chamadas em sequência — nenhuma pula a próxima:**
     a. `POST /api/cli/modelador` `{"url":"<link>","modo":"raiox"}` → guardar `page_id` e as 10 `propostas`.
        Mostrar à dona, ela escolhe uma pelo `ranking`.
     b. `POST /api/cli/modelador` de novo, mesma `url`, `{"modo":"combinado","refazer":true}` (sobrescreve o
        resultado salvo — esperado). Isso só dá o diagnóstico SpyX + caminhos do Rato, **ainda não gera
        página/ganchos/roteiros/copies**.
     c. **Obrigatório, não pula:** `POST /api/cli/modelador/modelar` `{"page_id":…,"direcao":{"ideia":{"titulo":…,
        "entrega":…,"publico":…},"publico_principal":…,"regras_nicho":…}}` montando `direcao.ideia` a partir da
        proposta do Raio-X escolhida em (a) — só essa chamada roda a etapa 2B de verdade (`pagina[]`, 5
        `ganchos`, 3 `roteiros`, 4 `copies_anuncio`, `diferenciacao`, `checklist_lancamento`). Sem (c), a E2a
        não tem saída real — vira só diagnóstico sem direção.
  2. Outro modo: `POST /api/cli/modelador` `{"url":"<link>","modo":"rato"|"spyx"|"combinado"}` → etapa 1
     (2-4 min; timeout ≥ 6 min). Guardar `oferta.page_id`.
  3. `POST /api/cli/modelador/mercado` `{"page_id":…}` → só se o caminho for outro idioma/mercado.
  4. `POST /api/cli/modelador/modelar` `{"page_id":…,"direcao":{…}}` → etapa 2 (v3: `direcao.ideia_id`).
  5. `GET /api/cli/modelador/<page_id>/markdown` → relatório inteiro.
- A dona já rodou na tela? Não rodar de novo: buscar pelo `page_id` (fica salvo no MineraAds).
- Ela não disser o modo? Roda o **padrão (Raio-X+SpyX)**. Só usa outro modo se ela pedir explicitamente.

## Passos
1. Etapa 1 → salvar `.json` (resposta bruta) e `.md` na oferta.
2. **Mostrar à dona, curto:** o que o original vende · alavanca mais fraca e a que ele nem tocou · 3-5 buracos ·
   os caminhos (top 1, top 3 e as famílias: mesma oferta melhorada, subnicho, público, ângulo, roupagem, formato,
   nicho, outro idioma) com o que cada um corrige. **Ela escolhe** — nunca escolher por ela.
3. Outro idioma → etapa 1b (mercados com nota) → ela escolhe o mercado.
4. Etapa 2 com a direção (caminho, público principal, regras do nicho que ela disser) → salvar de novo
   (`modelador-<data>-etapa2.json/.md`).
5. **Página original em disco** (a página e o entregável dependem disso): rodar a parte de leitura da
   `low-referencia` na URL que o Modelador leu (`url_lida`) → `pesquisa/REFERENCIA.md` + imagens da página
   (mockups, prints por dentro, folhas) em `pesquisa/referencia/imagens-origem/`.
6. Próximo: `low-validar` (validar o caminho escolhido) → depois `low-ficha-oferta`.

## Se o MineraAds falhar (fora do ar, página que ele não lê, resultado raso)
Fazer a análise à mão pela filha `metodo-spyx` (prompts SpyX de `RATO-ADS/pesquisa/spyx-prompts/`) (01 mesmo idioma · 02 outro
idioma · 03 mercado + direção escolhida), lendo a página de verdade (low-referencia), e salvar no mesmo lugar
com `origem: manual` no topo. Avisar a dona que foi manual.
