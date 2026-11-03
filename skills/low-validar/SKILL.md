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
5. **Veredito:**
   - 🟢 **verde** — ≥ 2 concorrentes validados no mercado-alvo **e** orgânico com comentários nos últimos 3 meses;
   - 🟡 **amarelo** — só um dos dois; dizer o risco;
   - 🔴 **vermelho** — nenhum concorrente validado e orgânico frio → voltar ao `low-modelador` e escolher outro
     caminho (top 3).
   **A dona decide** seguir ou não; a decisão vai escrita no fim do arquivo, com data.
6. Termos que acharam concorrente bom → sugerir à dona incluir no Swipe automático diário do MineraAds.

## O arquivo `VALIDACAO-<data>.md`
Termos (PT/ES/EN, marcando os que acharam algo) · tabela de concorrentes · orgânico + frases reais · funil dos
concorrentes · veredito · **decisão da dona**.

Quem usa depois: `low-ficha-oferta` (dor, funil, preço), `low-pagina` (concorrente com página melhor = referência
extra), `ctv-modelar-concorrente` (anunciantes validados = fonte de criativo).

Próximo: `low-ficha-oferta`.
