---
name: low-validar
description: Etapa E2b do sistema LOW-TICKET — valida o caminho de modelagem que a dona escolheu ANTES de virar ficha e página. Gera os termos de busca em português, espanhol e inglês, acha na Biblioteca de Anúncios os concorrentes com oferta parecida (validados pelo tempo no ar), mede a demanda orgânica (YouTube + Google Trends) e dá o veredito verde/amarelo/vermelho. Use depois da escolha no low-modelador, ou quando a dona pedir "valida essa ideia", "acha concorrentes", "termos de busca", "tem demanda?".
---

# low-validar — E2b, validar o caminho escolhido

**Entrada:** `pesquisa/modelador-<data>-etapa2.json` (ou a ideia escolhida: `direcao.ideia`) · mercado escolhido.
**Saída:** `OFERTAS/<slug>/pesquisa/VALIDACAO-<AAAA-MM-DD>.md` com veredito **e a decisão da dona**.
**Sem esse arquivo a `low-ficha-oferta` não começa.**

## Passos (nenhum se pula)
1. **Termos de busca — 3 idiomas sempre**, mesmo se o mercado for um só (concorrente bom pode estar em outro idioma
   e vira modelo de página e criativo):
   - 5 termos em **português**, 5 em **espanhol**, 5 em **inglês**;
   - misturar: nome do entregável ("mapa mental", "cuaderno de actividades"), dor/resultado ("memória idoso"),
     público ("jiu jitsu 40 anos") e mecanismo;
   - outro idioma: somar os `mercado.termos_biblioteca` do Modelador.
   - **Mostrar a lista à dona** — ela corta ou soma termos antes da busca.
   - **Perguntar como fazer a busca** (regra da dona, 04/11/2026): *automática* (eu rodo os termos na
     Biblioteca/MineraAds e trago a tabela) **ou** *manual* (ela pesquisa e me dá o retorno). **Padrão dela =
     manual**: entregar os termos prontos pra copiar (um por linha, por idioma) e sugerir manual primeiro. Manual → registrar o
     retorno dela **literal** no `VALIDACAO-<data>.md` como fonte, e seguir pros passos que ela não cobriu
     (orgânico, funil dos concorrentes). Nunca rodar a busca sem essa resposta.
   - **Na pergunta, já dizer o que ela tem que trazer se escolher manual** (quem faz o quê fica escrito):
     | Quem | O quê |
     |---|---|
     | **Dona** (manual) | 1) termos que usou · 2) por idioma: **tem ou não tem** concorrente · 3) **link de cada anúncio/anunciante** que achou (Biblioteca) · 4) **quais ela quer como referência** — de criativo, de página ou de funil · 5) qualquer print/observação |
     | **Eu** | registrar o retorno literal · abrir cada link e preencher a tabela (dias no ar, nº de anúncios, preço, validado?) · baixar os criativos marcados como referência (`PROJETOS-MIDIA/CRIATIVOS-CONCORRENTES/`) · funil dos 2-3 melhores · orgânico · veredito |
     Ela disse só "não tem" sem link → perguntar se achou algo parecido que queira usar como referência
     (anúncio vizinho, outro idioma); "nenhum" também fica escrito. Os links marcados como referência vão
     pra seção **Referências escolhidas pela dona** do `VALIDACAO-<data>.md` — é de lá que `criativo` /
     `ctv-modelar-concorrente` e `low-pagina` puxam.
2. **Biblioteca — concorrentes parecidos.** Cada termo: `mineraads mine "<termo>"` (ou Biblioteca pelo
   `agent-browser` com perfil do sistema, todos os países). Tabela por anunciante: nome · link da Biblioteca ·
   idioma/país · dias no ar · nº de anúncios ativos · o que vende · preço (se visível) · **validado?**
   - **Validado** = anúncio com **≥ 30 dias no ar** OU **≥ 3 criativos com ≥ 7 dias** cada.
   - Separar: **mesmo produto** (concorrente direto) · **oferta vizinha** (mesmo público, outro produto — serve
     pra criativo e funil).
3. **Demanda orgânica** no mercado escolhido: tela do Modelador → "Validar demanda" (YouTube + Google Trends,
   rota `POST /api/modelador/validar-demanda`, sessão logada) ou `yt-dlp` à mão. Registrar: vídeos e views,
   comentários por janela (≤3 meses · 3-12 · >12), Trends subindo/estável/caindo e **5-10 frases reais do público**
   (vão pra Dor da `OFERTA.md` e pros ganchos).
4. **Funil dos concorrentes validados:** abrir a página e o checkout dos 2-3 melhores → bônus, order bump,
   upsell, downsell e preço de cada um. Alimenta o funil da ficha (E2).
4b. **O que a busca tem que responder (dona, 04/11/2026)** — no idioma-alvo **e** nos outros idiomas:
   - **Tem demanda?** (anúncios validados + orgânico)
   - **Alguém já anuncia a MESMA oferta no idioma-alvo?** → sim = **aplicar mais modelagem antes da ficha**:
     voltar ao Passo 2 (Raio-X/SpyX) e diferenciar (ângulo, bônus, visual, preço) dos anunciantes achados; a
     `VALIDACAO` lista o que eles fazem pra gente não ficar igual.
   - **Ofertas parecidas em outros idiomas?** → referência de página, funil e criativo (e sinal de que o modelo
     roda fora do país de origem).
   - **Outros anunciantes que já têm isso** (mesmo produto ou vizinho) → entram em *Referências escolhidas pela dona*.
5. **Veredito:**
   - 🟢 **verde** — ≥ 2 concorrentes validados no mercado-alvo **e** orgânico com comentários nos últimos 3 meses;
   - 🟡 **amarelo** — só um dos dois; dizer o risco;
   - 🔴 **vermelho** — nenhum concorrente validado e orgânico frio → voltar ao `low-modelador` e escolher outro
     caminho (top 3).
   **A dona decide** seguir ou não; a decisão vai escrita no fim do arquivo, com data.
6. Termos que acharam concorrente bom → sugerir à dona incluir no Swipe automático diário do MineraAds.
7. **Referência de criativo (sempre, mesmo sem concorrente no mercado-alvo):** procurar também quem anuncia
   **parecido** (mesmo formato de anúncio, oferta vizinha, outro idioma) só pra inspirar criativo, e perguntar à
   dona quais entram. Vai pra *Referências escolhidas pela dona* (link + "criativo"). A `criativo` (C1) lê daqui e
   pergunta de novo: modelar os do original, os desses, ou os dois.

## O arquivo `VALIDACAO-<data>.md`
Termos (PT/ES/EN, marcando os que acharam algo) · **quem fez a busca (eu/dona)** · tabela de concorrentes · **Referências escolhidas pela dona** (link + pra quê: criativo/página/funil) · orgânico + frases reais · funil dos
concorrentes · veredito · **decisão da dona**.

Quem usa depois: `low-ficha-oferta` (dor, funil, preço), `low-pagina` (concorrente com página melhor = referência
extra), `ctv-modelar-concorrente` (anunciantes validados = fonte de criativo).

Próximo: `low-ficha-oferta`.
