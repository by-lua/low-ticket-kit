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

1. **Keyword direto** — 1-2 termos que descrevem o NOSSO produto quase literal (ex.: "tarot para
   iniciantes"). Serve só pra achar 1-2 concorrentes **quase idênticos**, não pra minerar volume.
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
7. **Agora pensa AMPLO**: que outras palavras acham o MESMO público, mesmo sem ser o mesmo produto —
   inclusive produto totalmente diferente (curso, mentoria, app) que ataca a MESMA dor. Ex.: quem
   busca "aprender tarot sozinha" também é alcançado por "curso de autoconhecimento online" se a dor
   for a mesma. Gera essas palavras amplas e roda o **MESMO loop (passos 1-6b) com elas** — é a camada
   "nicho vizinho", nunca pulada.
8. **Depois de esgotar a Biblioteca** (direto + amplo), vai pro **YouTube com busca ABERTA** — termos
   da DOR, não os mesmos termos já usados na Biblioteca (repetir termo é confirmar o que já se sabia,
   não achar dor nova). Vê os vídeos **mais vistos**, lê **comentários**, registra contagem + data do
   comentário mais recente.
9. **Mesma lógica no Google Trends** (12 meses, país, termos candidatos a gancho, consultas
   relacionadas e em ascensão) — busca aberta pela dor, não espelho da Biblioteca.
10. **Mesma lógica no TikTok** (volume de comentários + caption; texto de comentário exige perfil
    logado, sem isso registra a limitação, nunca estima).
11. **Repete o loop INTEIRO (passos 1-6b, 7, 8, 9, 10) em ES e EN — nunca traduzindo literal.** Pra cada idioma,
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
