# Pesquisa padrão da oferta — antes de persona, página, criativo, funil ou preço

Nasceu do Atlas AR (23/10/2026). Antes dela a persona do Atlas estava só "herdada do BR"; com ela
mudaram o termo do gancho, a unidade da peça, a cena da dor e o argumento de preço. **Toda oferta
nova, e toda oferta que vai ganhar leva de criativo, passa por isto.** Referência viva:
`OFERTAS/luciola-atlas-movimiento/pesquisa/BIBLIOTECA-AMPLIADA-2026-10-23.md` +
`DEMANDA-ORGANICA-2026-10-23.md`.

Saída: 2 arquivos datados em `OFERTAS/<slug>/pesquisa/` + `PERSONA-E-ANGULOS.md` atualizado +
`gate-persona.py` LIBERADO. Navegador **headed**, 1 perfil de sistema por pane.

## 1 · Biblioteca de Anúncios → `pesquisa/BIBLIOTECA-AMPLIADA-<data>.md`
1. **Começa pelo anunciante modelado** (link da página dele): conta narrativas por repetição e dias
   no ar. A que mais repete e mais dura é a espinha da leva (Atlas: N1 = 23 de 26 vídeos).
2. **5 palavras-chave + 1 hashtag por idioma** (idioma do mercado + PT + EN, mais o que fizer
   sentido), `active_status=active`, `country=ALL`. Palavras = **o que a pessoa procura**, não o
   nome do produto.
3. Falso-zero: conferir `q` não-vazio e ler o contador aceitando `resultados`/`results`.
4. Tabela de **anunciantes relevantes** (país, link, dias ativo, nº de anúncios, preço, pra quem
   vende, formato/gancho) + descartados com motivo.
5. Tabela **narrativas × quem repete × dias** — o que roda há mais tempo em vários anunciantes.
6. Tabela **âncora de preço**: quanto os vizinhos cobram e por quanto (unidades). Decide se o preço
   muda ou se muda só o argumento.
7. Seguidores (aba Sobre), referências visuais salvas em `PROJETOS-MIDIA/CRIATIVOS-CONCORRENTES/`.
8. **"O que a varredura mudou"**: antes × agora. Se nada mudou, escrever que nada mudou.

## 2 · Demanda orgânica → `pesquisa/DEMANDA-ORGANICA-<data>.md`
1. **YouTube:** vídeos mais vistos nas palavras da dor (views + data) e comentários baixados
   (`yt-dlp`), com **contagem por dor e data do comentário mais recente**. Amostras literais.
2. **Comentário com intenção de compra** ("pasa link", "onde compro", "dónde los consigo") é dor
   contada à parte: prova que o público já procura o material.
3. **TikTok:** volume de comentários + caption. Texto de comentário precisa de perfil logado; se
   não der, escrever a limitação (não estimar).
4. **Google Trends do país (12 meses):** índice de cada termo candidato a gancho, consultas
   relacionadas, **em ascensão**. "Dados insuficientes" = termo NÃO vai pro gancho.
5. **Conclusões** em tabela: achado · dado · consequência prática. Pendências honestas no fim.

## 3 · O que tem que sair escrito no PERSONA-E-ANGULOS (o gate confere)
- `## TERMOS DE BUSCA`: termo · fonte (Trends/YouTube/Biblioteca) · índice/contagem · veredito
  (**gancho** / só nome do produto / descartado). **Nome do produto quase nunca é termo de busca**
  (Atlas: "atlas" = dados insuficientes; o gancho virou "kinesiología" / "qué músculos trabajan").
- `## NARRATIVAS QUE RODAM`: narrativa · quem repete · dias no ar · como vira peça.
- `## ÂNCORA DE PREÇO`: vizinhos com preço e unidade + decisão (mantém/muda preço ou argumento).
- **Unidade da peça**: o menor pedaço que a pessoa busca (Atlas: 1 exercício por peça, escolhido
  pelo que sobe no Trends). Catálogo inteiro numa peça só perde pra peça de 1 unidade.
- **Cena da dor**: onde a dor acontece, tirada do comentário com mais contagem (Atlas: sala, prova,
  oral, além da academia). É a imagem do criativo.
- Recorte sem dado (ninguém do mercado fala com ele) fica fora da headline, só ângulo de teste.
- **Prova social do concorrente não se copia** antes da 1ª venda nossa.

## 4 · Depois da pesquisa
`gate-persona.py` → LIBERADO → plano de leva em texto → `gate-plano-leva.py` → OK da dona → produção.
