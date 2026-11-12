---
name: low-modelador
description: Etapas E1/E2 do sistema LOW-TICKET pelo MineraAds — roda o Modelador combinado (SpyX + Rato) num anunciante ou página, mostra os caminhos pra dona escolher, roda a modelagem do caminho escolhido e salva o relatório na oferta. Use quando a dona disser "roda o modelador", "modela essa oferta", "joga no MineraAds", ou depois do low-referencia.
---

# low-modelador — E1/E2 pelo MineraAds

> **⚠️ PADRÃO DESDE 04/11/2026 = MODO LOCAL** (ordem da dona: "parar de fazer pelo MineraAds e fazer aqui, usando as
> skills de modelagem, é mais rápido"). O agente faz na sessão, lendo a página e os anúncios de verdade
> (`low-referencia`), seguindo os mesmos prompts e formatos do app: `references/PROMPTS-MODELADOR.md`
> (Raio-X 6 pilares + 10 propostas · SpyX diagnóstico/alavancas → `metodo-spyx` · etapa 2 A/B/C: oferta, página,
> ganchos, roteiros, copies, lead reagindo). Mesma ordem de etapas e mesmas saídas (`pesquisa/modelador-<data>-*.md`,
> com `origem: local` no topo). A API do MineraAds abaixo só roda se a dona pedir.
> Demanda na web (que o app fazia no Gemini): no local, WebSearch na sessão, citando fonte.

O Modelador (SpyX + Rato) monta a oferta: extração do que o original tem (bônus, bump, upsell, downsell,
checkout), buracos, lead reagindo, alavancas, caminhos de modelagem, e — depois da escolha — oferta nossa,
funil, página seção por seção e criativo (ganchos, roteiros, copies, estáticos).

**Entrada:** link da Biblioteca do anunciante (`view_all_page_id`) ou da página de vendas.
**Saída:** `OFERTAS/<slug>/pesquisa/modelador-<AAAA-MM-DD>.md` + `.json`. **Rodou e não salvou = não feito.**

**Se a dona mandar os dois links (Biblioteca de Anúncios do Facebook + página de vendas): usar a URL da
Biblioteca como `url` na chamada** — só ela aciona `scrapeLibrary` (lê anúncios reais, `dias_rodando`,
criativos). Mandar a URL da página de vendas no lugar da URL da Biblioteca faz o Modelador cair no fallback
"link direto, sem leitura dos anúncios" (`anuncios:0`, `criativos:[]`) mesmo com a página de vendas lida —
parece bug, mas é a URL errada entrando. A página de vendas entra depois, no passo 5 (`low-referencia`).

**Antes de rodar, checar se o MineraAds está disponível** (token `MINERAADS_EXT_KEY` setado, API responde).
Sem acesso: não perguntar à dona "você tem MineraAds?" — ir direto pro fallback manual (seção "Se o MineraAds
falhar" abaixo), avisando que foi manual.

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
Token: `MINERAADS_EXT_KEY` (`set -a; source <COFRE-DE-CREDENCIAIS>; set +a`). Base: `$MINERAADS_URL`
(padrão `https://<subdominio>.<seu-dominio>`). Contrato: `RATO-ADS/API-CONTRATO.md` § CLI.
- Comando (quando instalado, spec v3): `mineraads modelador analisar|caminhos|mercado|modelar|salvar`.
- Sem o comando: rotas com `Authorization: Bearer $MINERAADS_EXT_KEY`:
  1. **Fluxo padrão (Raio-X+SpyX), 3 chamadas em sequência — nenhuma pula a próxima:**
     a. `POST /api/cli/modelador` `{"url":"<link>","modo":"raiox"}` → guardar `page_id` e as 10 `propostas`.
        Mostrar à dona **o texto inteiro de cada proposta na mensagem** (ver "Como mostrar" abaixo), ela escolhe uma pelo `ranking`.
     b. `POST /api/cli/modelador` de novo, mesma `url`, `{"modo":"combinado","refazer":true}` (sobrescreve o
        resultado salvo — esperado). Isso só dá o diagnóstico SpyX + caminhos do Rato, **ainda não gera
        página/ganchos/roteiros/copies**.
     c. **Obrigatório, não pula — mas só DEPOIS da E2c aprovada** (dona, 04/11/2026: "o SpyX faz as copies, por isso
        a gente define a modelagem inteira antes"). A etapa 2 escreve página, ganchos, roteiros e copies; rodar antes
        de fechar ficha + funil + plano da página gera copy com preço/planos/bônus errados. Ordem: (a) Raio-X → dona
        escolhe → (b) Combinado (diagnóstico + alavancas, mostrar) → E2b → E2c aprovada → **(c)** com `direcao`
        completa (planos, bônus, bumps, garantia, plano da página, regras do nicho tirados de `OFERTA.md`/`FUNIL.md`).
        Rodou antes (<Oferta Exemplo>, 04/11)? Rodar de novo depois da E2c.
        `POST /api/cli/modelador/modelar` `{"page_id":…,"direcao":{"ideia":{"titulo":…,
        "entrega":…,"publico":…},"publico_principal":…,"regras_nicho":…}}` montando `direcao.ideia` a partir da
        proposta do Raio-X escolhida em (a) — só essa chamada roda a etapa 2B de verdade (`pagina[]`, 5
        `ganchos`, 3 `roteiros`, 4 `copies_anuncio`, `diferenciacao`, `checklist_lancamento`). Sem (c), a E2a
        não tem saída real — vira só diagnóstico sem direção.
  2. Outro modo: `POST /api/cli/modelador` `{"url":"<link>","modo":"rato"|"spyx"|"combinado"}` → etapa 1
     (2-4 min; timeout ≥ 6 min). Guardar `oferta.page_id`.
  3. `POST /api/cli/modelador/mercado` `{"page_id":…}` → só se o caminho for outro idioma/mercado.
  4. `POST /api/cli/modelador/modelar` `{"page_id":…,"direcao":{…}}` → etapa 2 (v3: `direcao.ideia_id`).
     **`page_id` aqui é o ID normalizado** (`oferta.page_id` da resposta da etapa 1, ex. `1173579039169074`),
     **nunca a URL completa** — mandar a URL dá `{"error":"Rode a análise SpyX primeiro."}` mesmo já tendo
     rodado etapa 1 (o registro existe, só não casa pela chave errada).
  5. `GET /api/cli/modelador/<page_id>/markdown` → relatório inteiro.
- A dona já rodou na tela? Não rodar de novo: buscar pelo `page_id` (fica salvo no MineraAds).
- Ela não disser o modo? Roda o **padrão (Raio-X+SpyX)**. Só usa outro modo se ela pedir explicitamente.
- **Rodando via `ctx_execute` (sandbox)**: cada chamada pode virar task em background com sandbox própria —
  um arquivo salvo em `/tmp` numa chamada pode não existir mais na próxima (sandbox efêmera, não é o mesmo
  disco do host). Pra não perder o resultado: fazer curl + leitura/validação do JSON **na mesma chamada**
  (um só bloco de código que salva e já imprime o que precisa), nunca dividir "salva num `ctx_execute`" e
  "lê noutro". Se precisar do arquivo depois (Read tool, cp pra OFERTAS/), copiar pra fora do sandbox ainda
  dentro da mesma chamada que gerou — ou aceitar que só o que foi impresso no momento sobrevive.

## Passos
1. Etapa 1 → salvar `.json` (resposta bruta) e `.md` na oferta.
2. **Como mostrar (regra da dona, 04/11/2026):** as propostas vão **escritas por extenso na mensagem do chat**,
   nunca só como opção resumida de pergunta (AskUserQuestion) nem só "salvei no arquivo". Para cada proposta:
   título · tipo/pilar trocado · o que muda · entrega · público · mercado (se houver) · demanda/dificuldade · por quê.
   Se ela pedir "as N primeiras", mostra essas N por extenso e o resto em 1 linha cada (título — o que muda).
   Salvar também em `pesquisa/modelador-<data>-raiox.md`. Só depois perguntar qual ela escolhe.
   Avisar quando a pesquisa de demanda veio vazia (`pesquisa_comercial` nulo ou com `erro`) — as propostas ficam sem prova de demanda.
3. **Mostrar à dona (Combinado/SpyX):** o que o original vende · alavanca mais fraca e a que ele nem tocou · 3-5 buracos ·
   os caminhos (top 1, top 3 e as famílias: mesma oferta melhorada, subnicho, público, ângulo, roupagem, formato,
   nicho, outro idioma) com o que cada um corrige. **Ela escolhe** — nunca escolher por ela.
   **Depois da etapa 2 (sempre — inclusive quando a direção é "o original igual, em outro país"):** mostrar por
   extenso a análise de alavancas: notas das 4 alavancas dele (`alavancas_oferta_dele`) · a mais fraca e a não
   tocada · fraquezas → como corrigimos (`fraquezas`) · dele × nossa (`alavancas_comparacao`) · o comprador cético
   reagindo à NOSSA oferta (`lead_oferta_nova`: o que ainda trava, "compraria?"). Modelar pra outro país não pula
   isso (erro de 04/11/2026, <Oferta Exemplo>: rodou e não foi mostrado). Esse material alimenta a `low-ficha-oferta` 2b.
4. Outro idioma → etapa 1b (mercados com nota) → ela escolhe o mercado.
5. Etapa 2 com a direção (caminho, público principal, regras do nicho que ela disser) → salvar de novo
   (`modelador-<data>-etapa2.json/.md`).
6. **Página original em disco** (a página e o entregável dependem disso): rodar a parte de leitura da
   `low-referencia` na URL que o Modelador leu (`url_lida`) → `pesquisa/REFERENCIA.md` + imagens da página
   (mockups, prints por dentro, folhas) em `pesquisa/referencia/imagens-origem/`.
7. Próximo: `low-validar` (validar o caminho escolhido) → depois `low-ficha-oferta`.

## Demanda vs. concorrência — dois tipos, nunca misturar
Decisão 2026-11-03, baseada no método do Fernando Oliveira Pro (canal, vídeo "Como Minerar e Modelar
Produtos Low Ticket") — transcrição em `PROJETOS-MIDIA/PERFIS-E-CANAIS/LOW-TICKET-fernandooliveira/`:
- **Demanda orgânica+comercial (existe mercado pra isso?):** busca web real (Gemini com grounding,
  `pesquisaComercialReal` em `modelador.js`) por quem já vende produto parecido na internet em geral,
  com preço — **automático dentro do raiox e do SpyX/combinado**, não é botão. Roda 2x: na etapa 1
  (produto original) e de novo depois que a dona ESCOLHE a modelagem (`pesquisaComercialModelagem`,
  gera o campo `demanda_modelagem` — equivalente ao momento em que o Fernando acha "a Rúbio já vende
  isso por R$213" depois de já ter a concepção, não antes).
- **Concorrência ativa (alguém tá pagando anúncio ESSA oferta ESSE ângulo agora?):** botão separado
  "Validar demanda real antes de escolher" na tela do Modelador → `validarMercado`
  (validacaoMercado.js) → lê de verdade a Biblioteca de Anúncios do Facebook (+YouTube+Trends). Só
  roda DEPOIS que a dona escolhe 1 idioma específico — nunca antes.
Não dá pra confundir as duas: a primeira diz se o mercado existe, a segunda diz se já tem anúncio
pago validando aquele ângulo específico.

**Checkbox "modelar pra fora" (tela do Modelador, antes de rodar):** se marcada, a dona escolhe
quais idiomas quer cobrir — espanhol (Latam), inglês, francês, italiano, alemão, português de
Portugal (chips, `es/en/fr/it/de/pt`) — e a pesquisa de demanda da etapa 1 já cobre esses idiomas
de cara (`internacional`+`idiomasAlvo` no corpo de `POST /api/modelador` e `/api/cli/modelador`).
Isso só afeta a busca de DEMANDA; a concorrência na Biblioteca continua esperando a escolha de 1
idioma específico mais na frente.

## Se o MineraAds falhar (fora do ar, página que ele não lê, resultado raso)
Fazer a análise à mão pela filha `metodo-spyx` (prompts SpyX de `RATO-ADS/pesquisa/spyx-prompts/`) (01 mesmo idioma · 02 outro
idioma · 03 mercado + direção escolhida), lendo a página de verdade (low-referencia), e salvar no mesmo lugar
com `origem: manual` no topo. Avisar a dona que foi manual.
