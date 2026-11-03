# Pesquisa padrão da oferta — antes de persona, página, criativo, funil ou preço

Nasceu do Atlas AR (23/10/2026). Antes dela a persona do Atlas estava só "herdada do BR"; com ela
mudaram o termo do gancho, a unidade da peça, a cena da dor e o argumento de preço. **Toda oferta
nova, e toda oferta que vai ganhar leva de criativo, passa por isto.** Referência viva:
`OFERTAS/luciola-atlas-movimiento/pesquisa/BIBLIOTECA-AMPLIADA-2026-10-23.md` +
`DEMANDA-ORGANICA-2026-10-23.md`.

Saída: 2 arquivos datados em `OFERTAS/<slug>/pesquisa/` + `PERSONA-E-ANGULOS.md` atualizado +
`gate-persona.py` LIBERADO. Navegador **headed**, 1 perfil de sistema por pane.

## 1 · O LOOP ÚNICO (dona, 24/10/2026 — isto substitui qualquer versão anterior, ler antes de tocar em qualquer busca)

Não são "etapas separadas que ficam melhor ou pior". É **um loop só**, nesta ordem exata, que só termina
quando esgota. Pular etapa, misturar ordem, ou validar com termo "quase igual" ao que já usou (em vez de
abrir e repetir de verdade) é o motivo de toda pesquisa superficial que já aconteceu aqui (Mapa do Tarot
BR, 24/10). Rodar o loop inteiro 2x: uma vez por **keyword direto** (passo 1), outra por **keyword amplo**
(passo 7) — e as duas rodadas se repetem de novo em ES e EN (passo 11). Toda referência a "passos 1-6" ou
"1-6b" neste arquivo INCLUI o 6b — ele é parte do ciclo, não um extra que pode ficar de fora.

**Piso mínimo, sem o quê a pesquisa é rasa de novo (não é sugestão, é piso):**
- **≥3-5 concorrentes "quase idênticos"** processados pelo ciclo 1-6 (não 1 só) antes de ir pro 6b/7.
- **≥15-20 buscas no total** entre keyword direto + amplo, lendo CARD DE VERDADE (não só contador) na
  maioria delas — é o que achou "Do Tarô à Renda" no Tarot BR depois de quase perder por só contar.
- **≥5-6 vídeos** abertos no YouTube aberto (passo 8), com comentário lido, não só título/views.
- Camada "amplo" (passo 7) não é opcional por falta de tempo: sem ela, nunca aparece o formato que a
  gente não tinha pensado (é ela que acha o "curso" quando a gente só buscava "PDF").
- Abaixo desse piso, a pesquisa não está pronta pro `gate-persona.py` — mesmo que o script passe.

0. **DIVISÃO DE TRABALHO (dona, 25/10/2026, NeuroActiva AR — substitui "eu minero tudo sozinho"):**
   a Biblioteca (passos 2-7) é **mineração manual da dona**: o agente entrega **5 keywords por idioma
   (PT/ES/EN) + 1-2 de audiência + 1 frase de promessa por idioma**, a dona roda na Biblioteca, separa
   os anúncios e manda. O agente **não gasta o pane varrendo a Biblioteca em série** — enquanto a dona
   minera, o agente roda a **camada orgânica (passos 8, 9, 10, 10b)** nos 3 idiomas: YouTube (vídeo
   mais visto + comentário lido), TikTok (caption + volume), Trends e Threads. A pesquisa só fecha
   quando as duas metades voltam e são cruzadas (passo 12). Motivo: keyword de Biblioteca é decisão de
   compra (a dona vê o card e sabe na hora se é concorrente); dor/persona é leitura de comentário, e
   isso é o que o agente faz melhor sem depender de clique manual.
   **Quando a dona manda o anúncio/anunciante (27/10/2026):** o agente abre a página do anunciante,
   descreve TODOS os criativos em texto (copy, formato, como abre, o que faz, como fecha) e printa só os que vai modelar e
   agrupa por narrativa — procedimento único no Gate 0.2 passo C do `criativo-ads/SKILL.md`.

1. **Keyword direto — 5 por idioma (PT+EN+ES = 15 no total), correção dona 25/10/2026 (substitui
   qualquer contagem anterior deste arquivo).** Nome genérico do nicho SOZINHO não acha concorrente
   quase idêntico — é largo demais, devolve tudo e nada (ex.: "tarot" sozinho não serve). Keyword
   direto é **variação do produto/formato**: manda o site/oferta nossa pro GPT e pede literalmente
   "analisa essa oferta — o que entrega, pra quem, que problema resolve, que transformação promete —
   e me dá 5 palavras-chave em português, 5 em inglês e 5 em espanhol pra achar produtos parecidos,
   sem ficar preso ao nome/formato do nosso produto". Ele devolve variações tipo "tarot visual" /
   "mapa de tarot" / "leitura de tarot em mapa", não só "tarot". **Teste antes de aceitar uma
   keyword direta: ela sozinha, sem mais contexto, devolveria um concorrente que vende A MESMA
   COISA, ou devolve ruído do nicho inteiro?** Se é ruído, a keyword é larga demais — ainda não é
   "direto", é "amplo" disfarçado. As 15 servem pra achar os primeiros concorrentes **quase
   idênticos** (passo 2-6) nos 3 mercados de uma vez, não pra minerar volume — isso é o passo 7.
   **+ 1-2 keyword de AUDIÊNCIA, separado das 15** (dona, 25/10/2026): não é variação de produto
   nem de dor — é o substantivo que nomeia QUEM é a pessoa (papel/profissão/identidade), tipo
   "eletricista", "vendedor", "tarotista". Serve pra achar anúncio/conteúdo que fala com essa
   pessoa em QUALQUER contexto, não só o nosso nicho — outra camada de descoberta de público.
   **+ busca por PROMESSA, não só por nome (dona, 25/10/2026, exemplo real Mapa do Tarot):** além
   das 5+5+5 de produto, buscar também pela frase da promessa/benefício do nosso próprio anúncio —
   "aprenda a ler as cartas sem memorizar" / "learn tarot without memorizing" / "aprende a leer el
   tarot sin memorizar". Acha concorrente que vende a MESMA solução com nome de produto totalmente
   diferente, coisa que keyword de produto nunca pega sozinha. Gera 1 frase de promessa por idioma
   a partir do nosso próprio gancho/headline.
2. **Abre o 1º anúncio relevante** que o termo achou. Confere **"Veiculação iniciada em"** no card:
   **< 7 dias = ignora** (pode ser teste que ainda vai morrer); **≥ 7 dias = narrativa validada**
   (continuam pagando, então funciona) — só então vale a pena analisar.
3. **Transcreve/lê esse anúncio específico**: texto do card, transcrição do vídeo (ou legenda), o que
   mostra na imagem/creative — e, nessa leitura, **quem o anúncio fala**: vocabulário, cenário, objeção
   que ataca. Isso é **QUEM COMPRA DE VERDADE**, não quem a gente supôs pelo nome do nicho (lição Elétrica,
   10/10/2026: persona estudada foi "estudante", mas o anúncio que vende de verdade fala com o
   **eletricista na obra** — só a leitura do anúncio real, não o nome do nicho, mostra isso). Isso é a
   unidade de análise — não o anunciante inteiro ainda, **esse anúncio**.
4. **Abre a página do ANUNCIANTE** (clica no nome dele, não no anúncio) e repete o passo 3 pra
   **CADA outro anúncio ativo dela** — mesma transcrição, mesmo gate de 7 dias, um por um, até
   esgotar a página dela. É aqui que aparece a narrativa que ela mais repete (a espinha da oferta dela).
5. **Abre o site/página de vendas dela** pra entender a oferta por dentro (preço, estrutura, bônus) —
   sem isso o passo 4 fica incompleto, porque o anúncio só mostra o gancho, não o produto.
   **Escreve o mecanismo real em 1 frase (30/10/2026):** o que ela REALMENTE vende, além do objeto —
   ex. "não vende PDF, vende redução do trabalho de preparar atividades". É essa frase, não o nome
   do produto, que decide se o concorrente é narrativa forte ou só mais um PDF genérico.
   **Registra "Limitações" explicitamente (30/10/2026):** qualquer trecho do funil que não abriu até
   o fim (tela de pagamento externa, método de pagamento, confirmação de transação) e qualquer dado
   de prova social da página (nº de vendas, nota, depoimento) — escreve como **"alegação da própria
   página, não verificada"**, nunca como fato. Isso não é opcional nem preguiça: é o que distingue
   "li a página" de "copiei o que a página afirma sobre si mesma".
6. **Volta pro passo 1-5 pra CADA um dos "quase idênticos" achados** (repetir o ciclo completo por
   concorrente, não só no primeiro). Isso fecha a camada "produto direto".
6b. **Mapeia as PORTAS dentro do mesmo nicho** (dona, 24/10/2026): nicho largo puxa anúncio em
   vários sub-temas — não existe lista fixa, cada nicho tem as suas (não é sempre "amor/dinheiro",
   é achar QUAIS são no mercado real). Agrupa os anúncios achados nos passos 2-6 por sub-tema e conta
   qual puxa MAIS anúncio (volume) e narrativa mais repetida. O sub-tema que mais puxa é a porta onde
   a demanda concentra DENTRO do nicho — mais específico que o nicho largo.
   **Dor forte achada aqui é só POSSIBILIDADE de bônus/upsell/reforço de copy, nunca regra automática**
   — é uma leitura a mais, não conclusão. **⚠️ Guarda-corpo:** achar um sub-tema popular (anúncio forte
   falando de dinheiro, de amor, do que for) NÃO vira ângulo nosso sozinho — passa pelo GATE 0 de
   sempre ("o que vendemos / não é / isso é item do MANIFESTO?") antes de propor qualquer coisa a
   partir daqui. O erro a não repetir é o mesmo da Elétrica/Jiu: ver um anúncio popular com tema X e
   querer fazer "nossa oferta com ângulo X" sem checar se X cabe no que a gente realmente entrega.
   Registra tabela sub-tema × nº de anúncios × dias no ar em `BIBLIOTECA-AMPLIADA-<data>.md` como
   leitura de mercado — a decisão de usar (bônus, copy, ou nada) é sempre posterior e conferida.
7. **Agora pensa AMPLO** — que outras palavras acham o MESMO público, mesmo sem ser o mesmo
   produto — inclusive produto totalmente diferente (curso, mentoria, app) que ataca a MESMA dor.
   Ex.: quem busca "aprender tarot sozinha" também é alcançado por "curso de autoconhecimento
   online" se a dor for a mesma. É a mesma pergunta que a dona faz ao GPT depois de já ter achado
   os concorrentes diretos: "agora me dá palavras mais abertas pra eu entender esse público, achar
   outros produtos/dores do mesmo nicho". Gera essas palavras amplas (sem teto fixo — o quanto
   esgotar fizer sentido) e roda o **MESMO loop (passos 1-6b) com elas** — é a camada "nicho
   vizinho", nunca pulada. **Resumo do mix completo de keyword: 5 diretas por idioma (passo 1,
   acham concorrente quase idêntico) + 1-2 de audiência (passo 1, quem é a pessoa: profissão/papel)
   + N amplas (passo 7, dor/público maior)** — nunca só um tipo.
8. **Depois de esgotar a Biblioteca** (direto + amplo), vai pro **YouTube com busca ABERTA** — termos
   da DOR, não os mesmos termos já usados na Biblioteca (repetir termo é confirmar o que já se sabia,
   não achar dor nova). Vê os vídeos **mais vistos**, lê **comentários**, registra contagem + data do
   comentário mais recente.
   **Ficha padrão por vídeo (30/10/2026, espelha o dado estruturado que o SpyX dá pra anúncio —
   orgânico merece o mesmo rigor, não prosa solta):** canal · título · views · data de publicação ·
   dias desde publicação · nº de comentários · data do comentário mais recente · formato (tutorial/
   vlog/shorts/review) · trecho de dor literal mais repetido nos comentários, com contagem de quantos
   comentários dizem a mesma coisa. Um vídeo sem essa ficha completa não conta pro piso de ≥5-6.
9. **Mesma lógica no Google Trends** (12 meses, país, termos candidatos a gancho, consultas
   relacionadas e em ascensão) — busca aberta pela dor, não espelho da Biblioteca.
10. **Mesma lógica no TikTok** (volume de comentários + caption; texto de comentário exige perfil
    logado, sem isso registra a limitação, nunca estima). **Mesma ficha padrão do passo 8**
    (criador · caption · views/curtidas · data · dias desde publicação · nº comentários · data do
    mais recente · trecho de dor literal + contagem).
10b. **Mesma lógica no Threads (dona, 25/10/2026, nova fonte)** — busca aberta pela dor, vê posts
    com engajamento, lê os comentários/respostas (texto nativo, direto, sem filtro de algoritmo de
    vídeo) — costuma expor objeção e pergunta crua que YouTube/TikTok não mostram tão literal.
    Exige perfil logado pra ver resposta; sem isso registra a limitação. **Mesma ficha padrão**
    (autor · texto do post · data · nº respostas · trecho de dor literal + contagem).
11. **Repete o loop INTEIRO (passos 1-6b, 7, 8, 9, 10, 10b) em ES e EN — nunca traduzindo literal.** Pra cada idioma,
    PENSA de novo nas 3 camadas de keyword (passo 1 e 7) **como o nativo fala aquilo**, não a tradução
    da palavra PT: gíria, termo de mercado, sinônimo que só existe naquela língua. Ex.: "aprender tarot
    sozinha" em espanhol vira "no entiendo el tarot" (frase de dor crua, não tradução de "sozinha"); em
    inglês o termo real pode ser "tarot for beginners" ou "how to read tarot", nunca a tradução palavra
    por palavra de "aprender". Gera a lista de keyword NOVA em cada idioma (passo 1 direto + passo 7
    amplo), roda o loop com ELA. Produto que já vende fácil fora do Brasil tem
    narrativa testada em mercado maior — mais barato importar a que já validou lá do que descobrir do
    zero aqui. Não é traduzir keyword: é abrir a Biblioteca/YouTube/Trends/TikTok de lá e rodar o
    mesmo processo.
12. **Cruza tudo**: a narrativa que aparece validada em VÁRIOS concorrentes (passo 4), em VÁRIOS
    idiomas (passo 11) e tem sinal orgânico (passo 8-10) é a base do ângulo. Só um sinal sozinho =
    hipótese, nunca gancho fechado. Narrativa importada sem NENHUM eco orgânico no mercado de destino
    também fica como hipótese, não gancho.

**Falso-zero** (Biblioteca): confere `q` não-vazio no campo de busca antes de aceitar zero; aceita
contador em `resultados`/`results`.
**Preço** sempre lido abrindo a LANDING do anunciante (passo 5), nunca só do texto do card — o card
às vezes omite ou mostra preço antigo.
**Saídas obrigatórias em disco:** `pesquisa/BIBLIOTECA-AMPLIADA-<data>.md` (tabela por anunciante:
país · link · dias ativo · nº de anúncios · preço · pra quem vende · formato/gancho; separar
concorrência direta × vertical adjacente × "só modelo de formato/copy"; + tabela narrativas × quem
repete × dias; + tabela âncora de preço; + seguidores da aba Sobre; + "o que a varredura mudou")
e `pesquisa/DEMANDA-ORGANICA-<data>.md` (YouTube/TikTok/Trends com contagem, comentário com intenção
de compra registrado à parte, conclusões em tabela). Ambos existem mesmo quando a seção MERCADO do
`PERSONA-E-ANGULOS.md` já tem link ≥5 — o gate mecânico confere a contagem, não se o concorrente foi
lido de verdade; essa leitura é responsabilidade de quem pesquisa.

## 2 · O que tem que sair escrito no PERSONA-E-ANGULOS (o gate confere)
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

## 3 · Depois da pesquisa
`gate-persona.py` → LIBERADO → plano de leva em texto → `gate-plano-leva.py` → OK da dona → produção.
