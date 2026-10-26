# Histórico de regras de vídeo (movido do SKILL.md em 26/10/2026, texto original)

> **Consulta, não receita.** O que vale hoje está em `EDICAO-PADRAO.md` (edição) e `estilos-de-video.md` (modos). Aqui ficam os incidentes e regras na forma em que foram escritas, pra auditoria. Onde este arquivo contradiz `EDICAO-PADRAO.md` (velocidade, duração de corte, trilha), **vale o EDICAO-PADRAO**.


## Lições fixas da sessão de QA 2026-10-04 (mapas-visuais-eletrotecnia) — leia antes de tudo

Seis defeitos achados numa única rodada de revisão da dona, todos virando regra
permanente abaixo. Nenhum se repete.

1. **Gravação de tela de produto é SEMPRE da dona, nunca gerada pelo assistente.**
   Nunca use `agent-browser` (screenshot, pan sintético, scroll gravado) pra
   produzir a cena de tela de um criativo. Antes de qualquer correção de tela,
   procure primeiro em `criativos/MATERIAL-ENTREGAVEL/` (ou pasta equivalente)
   por gravação já entregue. Falta gravação ou o material não serve? **Peça pra
   dona gravar** — nunca gere substituto. Ver memória `nao-gravar-tela-dona-grava`.
2. **Gravação real de celular pode trazer a UI do navegador (barra de status,
   hora, URL) no topo do frame.** Antes de compositar, confira pixel a pixel se
   sobra chrome do browser — se sobrar, `crop` só essa faixa (ex.: ~130px de um
   frame 590×1280) antes de escalar pro canvas final. Nunca deixe a barra do
   Chrome visível no criativo entregue.
3. **CTA final nunca empilha objeção.** A fala de fechamento é benefício curto +
   comando direto. Nunca junte garantia + preço + condição de pagamento + termo
   legal na mesma frase — ver seção "CTA simples" mais abaixo.
4. **Tarja de marca é opt-in, não padrão** — ver seção própria mais abaixo.
5. **Toda imagem gerada (capa de carrossel, card, qualquer asset) tem que ser
   CONFERIDA visualmente contra o produto certo antes de entregar — nunca confie
   só em dimensão/contagem de arquivo.** Um worker gerou (ou puxou por engano) a
   capa de **outro produto inteiro** (Jiu-Jitsu numa oferta de eletrotécnica) e
   isso passou por todo QA automático porque dimensão e contagem bateram. Abra
   e olhe cada imagem final contra o nome/nicho do produto da oferta antes de
   declarar pronto.
7. **Toda imagem que mostra o produto (mockup, página, tela, capa de entregável)
   leva a página/mockup REAL anexada como referência no prompt do GPT — nunca só
   descrição em texto.** Sem anexo, o modelo inventa conteúdo genérico que não
   tem nada a ver com o produto real (regra da dona, 2026-10-04: "o objetivo é
   ver o produto aparecendo"). Antes de escrever o prompt de qualquer imagem que
   precise mostrar o produto: localize a página/mockup real (entregável já
   gerado, screenshot aprovado, ou gravação de tela da dona), anexe no upload do
   ChatGPT, e no prompt descreva explicitamente "use a imagem anexada como
   referência de conteúdo/layout da tela — não invente outra página". Vale pra
   capa de carrossel, card de entregável, mockup de celular, qualquer cena que
   mostre "o que a pessoa recebe".
8. **`-stream_loop -1` num clipe mais curto que o slot necessário gera um pulo
   visível quando reinicia** (lido como "sobe e desce", "pisca", "volta do
   nada") — o loop reinicia a gravação do zero no meio da cena, sem fade nem
   aviso. Antes de usar `stream_loop` em qualquer gravação (b-roll, tela),
   **meça a duração da fonte primeiro** (`ffprobe`) e compare com os frames
   necessários da cena. Se a fonte já cobre o slot sozinha, **não use
   `stream_loop`** — use o clipe inteiro direto. Só use loop quando a fonte for
   genuinamente mais curta que o necessário, e aí prefira cortar a cena ou picar
   em outro ponto a aceitar o pulo.
9. **Dois mixes de áudio sobre a mesma narração produzem eco/cancelamento de
   fase** (soa "zuado", picotado, com pseudo-silêncios periódicos no
   `silencedetect` mesmo sem pausa real na fala). Antes de montar a mixagem
   final, garanta que existe **uma única fonte de narração** sendo usada —
   nunca misture áudio já embutido num render anterior (ex. Remotion) com uma
   segunda trilha de voz por cima. Se suspeitar de eco, gere um spectrograma
   (`ffmpeg -lavfi showspectrumpic`) do trecho suspeito: padrão de nulos
   periódicos = cancelamento de fase, não pausa de fala.
10. **O roteiro vai pro TTS COMO ESTÁ ESCRITO — roteiro sem acento gera
    narração sem acento E legenda sem acento.** Nenhum motor de TTS "corrige"
    ortografia; e a legenda karaokê lê o mesmo texto do `roteiro.json`. Em
    11/10/2026 isso derrubou os 4 vídeos de uma leva do Jiu-Jitsu de uma vez
    (`CRIATIVO-11/14/15/16`): `"O gaso acaba"`, `"Clica aqui embaixo e ve por
    dentro"`, `"Sao trinta cards, cento e vinte decisoes"` — áudios e legendas
    entregues errados, 4 peças refeitas do VO.
    **Gate, antes de chamar o TTS:** ler o texto em voz alta e conferir
    acentuação palavra por palavra — `não, são, você, está, decisão, posição,
    revisão, conexão, último, gás, dá, vê, já, é, só, técnico, sequência,
    início`. Conferir também verbo x acento (`é` ≠ `e`, `vê` ≠ `ve`, `dá` ≠
    `da`, `já` ≠ `ja`). Erro de digitação conta do mesmo jeito: `gaso` sai
    "gaso" falado, não "gás".
    **Gate de QA que pega:** abrir o `words.json` gerado e procurar palavra sem
    acento, OU extrair 2-3 frames e **olhar** a legenda renderizada. Roteiro
    revisado só no papel não basta — o defeito nasce na escrita.

11. **⛔ GATE DE VÍDEO COMPLETO — checklist obrigatório antes de marcar qualquer vídeo como
    pronto (regra da dona, 24/10/2026, caso CRIATIVO-02 Atlas). Regra permanente: toda vez que
    um ajuste pedido pela dona não estiver coberto por este gate, ele entra aqui na hora — nunca
    fica só no histórico da conversa pra "lembrar depois". A skill é o que o próximo criativo lê,
    não o chat.** **Todo criativo de vídeo tem
    hook → desenvolve mecanismo → toca a dor → CTA, sempre — a FORMA varia (expert fala tudo em
    1 clipe longo, expert fala o hook e corta pro material, 2 cenas de 8s coladas), o conteúdo
    não. Qualquer caminho serve desde que o resultado faça sentido e fique bom — monte, assista
    de novo como se fosse o cliente vendo pela 1ª vez, e só então declare pronto.** Script escrito e áudio gerado
    NÃO bastam — o roteiro do plano traz só o gancho resumido (ver `plano-video-ganho-nao-e-
    roteiro-completo`), e script completo sem estes 4 pontos ainda sai raso:
    - [ ] **Hook** nomeia a dor/pergunta real da persona (não genérico).
    - [ ] **Corpo desenvolve o MECANISMO, não só repete o benefício.** Teste: se tirar a frase do
      corpo e ela ainda disser só "o produto é bom/você vai entender", falta mecanismo. Mecanismo
      = explica O PORQUÊ funciona (ex.: "não é que você não estudou, é que decorar nome não
      mostra o movimento — com o mapa visual você vê os dois juntos"). Sem isso o criativo tem
      hook e nada depois.
    - [ ] **CTA nunca corta seco — tela final padrão fixa, usar em TODO vídeo da leva (regra da
      dona, 24/10/2026, ref. visual anexada):** fundo PRETO, **mockup COMPLETO do produto**
      centralizado no topo — este card é a ÚNICA exceção da regra "nunca mockup" (essa regra vale
      pro MEIO do vídeo, material real; o card de fechamento é peça de marca, sempre mockup
      polido) —, faixa com texto do CTA em branco sobre bloco de cor (roxo/marca) — **texto é só
      comando, NUNCA nome do produto** ("Clica aquí abajo y descubrí", nunca "Atlas Visual, mirá
      por dentro" — regra da dona 24/10/2026, vale pro texto do card E pro VO falado) —, **seta
      VERMELHA embaixo com animação simples de descida (bounce down)**, formato Stories vertical,
      tudo bem centralizado. 1-2s de sobra no fim, nunca corta na última palavra. É um card
      dedicado (asset único reusado em toda a leva), não congelamento do último frame do vídeo.
      **O card é ACRÉSCIMO depois do vídeo, nunca substituição da cena do CTA falado (regra da
      dona, 24/10/2026, caso CT2 Atlas/expert Martín — bug real: cortou a cena onde ela fala o CTA
      e pôs o card no lugar dela).** O vídeo sempre termina do jeito normal, ela falando o CTA até
      o fim (como sempre foi) — nunca encurtar essa cena pra caber o card. SÓ DEPOIS que o vídeo
      original termina é que o card (seta+mockup) entra, como um trecho A MAIS, ficando **~5s**
      com a trilha de fundo seguindo tocando. Timeline certa: `[vídeo inteiro até o fim natural da
      fala do CTA] → [+5s do card, música contínua]`. Errado: cortar o vídeo antes do fim e pôr o
      card no espaço que sobrou.
      **Legenda nunca vaza pro card (bug real, 24/10/2026):** se alguma cena do corpo for
      recortada depois dos timestamps do `words.json` já gerados, trunque a legenda pra nunca
      ultrapassar a duração real do corpo (`[w for w in words if w['end'] <= duração_do_corpo]`)
      — senão a palavra fica "pendurada" renderizada em cima do card CTA.
      **Causa já vista (CT13 Atlas, 25/10/2026): o `legenda_align.py` estica a ÚLTIMA palavra até o
      fim do áudio** — se o áudio passado inclui o silêncio/trilha do card, "dentro." fica com `end`
      no fim do vídeo e vaza em cima do card. Rode o alinhador só na trilha de VOZ e, depois, prenda
      o `end` da última palavra ao fim real da fala (silencedetect/transcrição) antes do truncamento.
      **E o Flow repete a frase do hook** quando sobra tempo no clipe de 8s (CT13: "no es tu memoria"
      2x) — cortar o hook no fim da 1ª ocorrência lendo a transcrição do clipe cru, nunca pelo RMS.
      **⛔ Legenda de OUTRO criativo (bug real, 25/10/2026, CT13 Atlas): reaproveitar a pasta
      `remotion/` de outro criativo (copiar `node_modules`/`package.json`/`KaraokeV2.jsx` pra
      economizar setup) é válido, mas o `words.json` daquela pasta é SEMPRE do criativo de
      origem — nunca copia sozinho com o resto.** Antes de rodar `npx remotion render`, imprime a
      1ª e a última linha do `words.json` que vai renderizar e compara com a 1ª/última frase do
      `roteiro*.txt` DESTE criativo — se não bater, está renderizando a legenda de outro vídeo.
      Vale também quando o `remotion/src/words.json` já existia na pasta de uma sessão anterior
      (pane interrompido, retomada): nunca assume que está certo só porque o arquivo existe —
      confere o texto antes de renderizar, sempre, mesmo em retomada.
      **Onde achar o mockup (nessa ordem):** `produto/MOCKUPS-NOSSOS/` da oferta → se não
      existir local, **a própria página de vendas no ar já tem** (ex. `/images/producto-portada.*`
      — inspecionar o HTML da página com `curl`/grep por `mockup|cover|capa|portada|producto` nos
      `src`/`srcset`) → baixar de lá antes de considerar "não existe mockup" e cair pra lâmina
      avulsa. Lâmina real só é substituto quando a página também não tiver mockup nenhum.
    - [ ] **Trilha de fundo instrumental**, -18/-22dB, do início ao fim, contínua (nunca troca no
      meio). Banco: `OFERTAS/mapa-do-tarot/criativos/BR/_ASSETS/trilhas/` (reusar entre ofertas,
      instrumental e livre de direitos).
    Vídeo que falha em qualquer um dos 4 não está pronto, mesmo com áudio+legenda+QA de boca OK.
    - [ ] **Corte sincronizado ao CONTEÚDO da fala, não por duração arbitrária (regra da dona,
      24/10/2026, caso CRIATIVO-01 — "você não está considerando a fala").** Antes de cortar
      qualquer cena, leia os timestamps reais do `words.json`/alinhamento forçado e identifique O
      QUE cada frase fala — a cena que entra naquele intervalo tem que ILUSTRAR aquela frase
      especificamente, não ser um bloco de duração redonda (3s, 4s, 5s) encaixado na ordem que
      sobrou. Ex.: a frase "es que nadie te mostró el movimiento" pede a cena que mostra o
      movimento sendo mostrado — não a cena seguinte da fila só porque "deu a vez dela". Processo
      certo: 1) gerar/alinhar o VO primeiro, 2) ler linha por linha o que cada trecho diz, 3) só
      então escolher e cortar a cena no tamanho EXATO daquele trecho (não arredondar pra 3-4s
      fixo — a duração do corte é a duração da frase).
    - [ ] **Variedade de cena, nunca segurar 1 take muito tempo (regra da dona, 24/10/2026, caso
      CRIATIVO-01).** Demonstrativo usa TODAS as gravações/takes disponíveis (ex.: 5 no total —
      3 gravações reais de tela + 2 takes Flow), nunca deixa 1-2 carregando o vídeo inteiro
      enquanto o resto fica parado no disco. **Regra prática: nenhuma cena única passa de ~3-4s
      sem corte** — segurar um take mais tempo que isso cansa, mesmo que o conteúdo mude dentro
      dele (zoom/pan não substitui corte de cena). Se há 5 takes pra um vídeo de ~25-30s, o corte
      médio é 1 a cada 5-6s — todos entram, nenhum fica de fora só porque "já deu pra mostrar".

**⛔ GATE QA FINAL — assistir o vídeo INTEIRO, não só frames em número redondo (regra da dona,
25/10/2026 — achados reais na revisão da leva Atlas AR: CT3 tinha um HOMEM contaminando um corpo
de UGC feminino no meio do vídeo — só apareceu porque o QA amostrou frames em 0/3/6/9s e pulou
bem o segundo exato onde a cena errada entrava; CT4/CT13/CT23 tinham CTA/card entrando ANTES do
corpo/legenda terminar de verdade — card sobrepondo legenda, às vezes por 1-2s, só visível
assistindo contínuo; CT12 saiu com a trilha ALTA DEMAIS, nunca medida, só "ouvida por cima";
CT13 tinha palavra repetida 2x no meio da fala. CT11/CT21 (25/10 noite) tinham ÁUDIO ERRADO
inteiro — o `src/index.jsx` do Remotion apontava pra um arquivo velho (`"final-v2.mp4"`,
sobra de uma iteração anterior) enquanto o roteiro/áudio novo só foi escrito em `"final.mp4"` —
render saiu silencioso: nenhum erro, só o áudio/roteiro antigo tocando com a legenda nova por
cima, sem bater.** Frame em número redondo (0, 3, 6, 9...) pula exatamente o segundo onde o
defeito mora. Antes de declarar QUALQUER vídeo pronto (novo ou reaproveitado de sessão anterior):
- [ ] **Confira o `src:` dentro de `src/index.jsx` contra o arquivo que você DE FATO acabou de
  escrever** — reusar uma pasta `remotion/` (própria ou de outro criativo) pode deixar o `src`
  apontando pro nome antigo (`final-v2.mp4`, `final-v3.mp4`...) enquanto você só atualiza
  `final.mp4`. `grep "src:" src/index.jsx` e compare o nome antes de rodar `npx remotion render`.
- [ ] **Transcreva o ÁUDIO DO ARQUIVO JÁ RENDERIZADO (depois do `remotion render`, não antes)**
  com Whisper (`watch` skill tem chave Groq configurada) e confira contra o roteiro palavra por
  palavra — provar o arquivo ANTES de renderizar não garante que o render usou esse mesmo arquivo.
- [ ] **Verifique CADA fonte do `list-body.txt`/lista de concat ANTES de concatenar** — abra 1
  frame de CADA arquivo `s*.mp4`/`c*.mp4` individualmente e confirme que a pessoa/conteúdo bate
  com o criativo (nunca confie em nome de arquivo nem em "já tava lá"). Clipe órfão de outra
  sessão/outro criativo entra fácil numa pasta `VIDEO/` cheia de versões.
- [ ] **Timing do card:** meça a duração EXATA do corpo (`ffprobe` do arquivo final `body-*.mp4`
  usado no concat) e confirme que o card começa EXATAMENTE nesse ponto, nunca antes — frame a
  ~0.3s antes do corte e ~0.3s depois, os dois tem que mostrar a transição limpa, sem legenda
  vazando em cima do card.
- [ ] **Áudio medido, não só ouvido:** `volumedetect` da trilha sozinha vs. da voz sozinha —
  trilha tem que estar nitidamente mais baixa (ver tabela de mix em FASE 7); nunca aceitar "parece
  ok" sem o número.
- [ ] **Palavra repetida:** ler o `words.json` renderizado inteiro (lista de texto) procurando
  qualquer palavra/frase consecutiva duplicada antes de aceitar a legenda.
- [ ] **Vídeo herdado de sessão anterior (sem intermediarios/roteiro):** não presuma que passou
  no gate só porque já estava publicado — ele pode ser de antes dessas regras existirem. Rode este
  gate nele também antes de reafirmar "pronto".

**Tool `agent-browser record` não herda sessão de login** (contexto novo, cookie
httpOnly não propaga, mesmo documentado como "preserves cookies"). Se precisar
operar página autenticada, faça login real pela UI (digitar+clicar) na MESMA
sessão onde vai trabalhar, nunca via `record` nem via `fetch()` direto na API de
login (o componente cliente não resincroniza sem reload real pós-login).

**Entrega obrigatória de copy (03/10/2026):** cada vídeo acompanha `anuncio.md`
na pasta do master, com ângulo, persona/dor, texto principal, título/headline,
descrição curta e CTA sugerido. Todos os campos seguem o ângulo e o mercado
daquele vídeo. Leia `../criativo-ads/references/texto-anuncio-por-angulo.md`.
Não concluir a entrega só com MP4. Para BR, escolha voz catalogada brasileira;
para PT, voz portuguesa. O `languageCode` não corrige sozinho o sotaque da voz.

Produção de criativo de vídeo para ads, cena a cena. **Orquestradora de vídeo**:
a estratégia (o quê, para quem, quantas peças) vem de `criativo-ads`; esta skill decide
COMO produzir e chama as mecânicas certas.


### E.0 — Modo padrão é DEMONSTRATIVO, UGC só se pedido

> ⚠️ **SUPERADO (25–26/10/2026):** o modo de cada vídeo vem do plano da leva (slots de
> `criativo-ads`: cada campanha tem expert, UGC e demonstrativo). O que continua valendo daqui:
> demonstrar com páginas REAIS e falar com quem COMPRA (ler a página antes).

Regra do usuário (2026-09-06). **Sem instrução em contrário, o criativo é
demonstrativo** — mostra o entregável por dentro, prova tangível do que o
comprador recebe — não UGC de pessoa falando. Isso é o que "fica top" por
padrão.

Receita padrão validada: ver **§E.2b** (Mapa do Tarot, 2026-09-23). Estrutura:
**hook em b-roll tela cheia → demonstração do entregável gravado → split (entregável
em cima, b-roll embaixo) → CTA em b-roll tela cheia** + VO off + legenda karaokê.

- **Pode sugerir UGC perguntando**, nunca decidir por conta próprio. Só entra
  UGC se o usuário pedir ou aceitar a sugestão.
- **Quando UGC entrar**, o tempo de vídeo tem que bater com o tempo da pessoa
  falando — nunca cortar pra alguns segundos genéricos. Quem narra o ritmo é
  a fala da pessoa; corta ou encurta as cenas de b-roll pra caber no tempo
  dela, não o contrário.
- **A demonstração usa as páginas REAIS do entregável, sempre por
  referência.** Nunca inventa conteúdo genérico — se for gravação de tela, mostra
  a navegação real; se for imagem referência, é a página de verdade (páginas reais
  do produto) como referência ao pedir a cena. O material que aparece na tela é o
  material que o comprador vai receber.
- **Antes de montar a cena, saiba onde está o entregável.** Localize os PDFs/
  imagens já gerados do produto (pasta `entregaveis/` da oferta, ou
  `estagio-N-pdf/` dentro dela) — nunca invente ou assuma que não existe
  material pra referenciar. Se o produto ainda não tiver todas as páginas
  geradas, use as que já existem; não espere o produto inteiro terminar pra
  montar o criativo.
- **Antes de escrever qualquer narração/fala, leia a página de vendas
  (`pagina/index.html`) pra confirmar quem é o comprador.** A página já
  carrega a persona certa (validada com o usuário antes de ir ao ar) — ela é
  a fonte da verdade sobre pra quem a copy fala, não o julgamento de quem
  escreve o criativo. Caso real (equilibrio-seguro-60): a narração foi escrita
  na 2ª pessoa pro idoso ("vas a recibir", "tu equilibrio") sem checar a
  página, que já usava hijo/hija/papá/mamá/cuidador — o comprador certo, não
  o usuário final. Grep rápido resolve: `grep -oE "hijo|hija|papá|mamá|
  cuidador|tu ser querido" pagina/index.html`. Se a página fala com o
  cuidador, a narração fala com o cuidador — sempre, sem exceção.


### E.0b — Expert/UGC no hook NÃO isenta o resto da receita E.2b (regra da dona, 24/10/2026)

**⛔ REPETIU 25/10/2026 (CT3 Sofi, CT22 Nico) — mesmo buraco do CRIATIVO-02, mesmo dia que a regra
foi lida inteira.** Montei o corpo em cortes full-screen sequenciais simples (`ffmpeg -f concat`
cru), sem split 70/30, sem 1-clipe-por-frase pensado, sem fade nas junções — exatamente o erro que
este item já documentava. Ler a regra não bastou; a próxima vez que montar corpo de UUGC/expert,
**abrir este item ANTES de escrever o primeiro `ffmpeg concat`**, não depois de montar errado.

**Buraco real encontrado:** CRIATIVO-02 (Atlas, expert Martín) abriu com personagem falando e,
a partir daí, o resto do vídeo foi montado "livre" — 4-5 cenas fixas, sem split, sem 1 clipe por
frase, sem acelerar a timeline. Isso é o erro: **expert/UGC no "Guia" é só a FONTE do hook, não
um modo à parte.** O resto do vídeo (do fim da fala do expert até o CTA) segue a receita **E.2b**
igualzinho a qualquer demonstrativo:

- **1 clipe por frase da VO**, não 4-5 blocos fixos pro vídeo inteiro.
- **Split 70/30 ou 50/50** (entregável em cima/b-roll embaixo) na frase de mecanismo — não corte
  sempre em tela cheia.
- **SEM aceleração por padrão (regra da dona, 24/10/2026 — revertido depois de 1.1x E 1.15x os
  dois soarem rápido demais, repetidas vezes, em criativo com personagem/narração falada).**
  Timeline no ritmo natural do VO, playbackRate 1.0. Só acelera se a dona pedir explicitamente
  pra aquela peça, e mesmo assim testa 1.05-1.1x primeiro, nunca direto 1.15x. **1.15x/1.30-1.40x
  continuam válidos só pro caso documentado da receita v10_imperatriz** (100% b-roll/tela, zero
  narração de personagem, ver tabela de velocidade mais abaixo ~linha 3478) — não é o padrão
  geral, é exceção de um formato específico.
- Trilha de fundo, CTA sem corte seco (card preto+mockup+seta vermelha, ver gate item 11) — iguais
  pra qualquer modo.
- **⛔ Antes de aplicar QUALQUER velocidade, confirme que a base é a RAW, não um render já
  acelerado (regra da dona, 24/10/2026 — bug real: #11/#21 ficaram a ~1,25x porque o `out.mp4`
  reusado já vinha com ~1,13x embutido de uma passada anterior, e o 1.1x novo somou em cima).**
  Checagem obrigatória antes de qualquer `setpts`/`atempo`: `ffprobe` a duração do áudio CRU
  (`vo.wav`/narração original) × a duração do vídeo mudo cru (`muted.mp4`/`body-visual.mp4` sem
  nenhum playbackRate) — as duas têm que bater (±0.3s). Se o arquivo que você ia acelerar já é
  mais curto que o áudio cru, ele JÁ tem velocidade aplicada — acelere a partir do raw, nunca em
  cima de um render que não é garantidamente 1:1.

**Regra de leitura da skill:** ao montar QUALQUER vídeo (1-3-9, 1-1-10, demonstrativo puro,
expert, UGC carro, qualquer um), ler E.0 → E.0b → E.2b nessa ordem ANTES de montar — a escolha de
quem fala no hook (b-roll, expert, UGC) é só um dos 4 blocos da receita, nunca motivo pra
abandonar o resto dela.

### E.0d — REGRA GERAL: quem mostra o entregável por dentro segue esta receita (dona, 25/10/2026)

> *"quando for um criativo que mostra o entregável por dentro sim, precisa ser tipo o demonstrativo —
> o demonstrativo tem muitas regras de edição e b-roll; bom ele ser mais geral do que só pro
> demonstrativo"*

**A receita do demonstrativo não é um modo entre outros: é o padrão de edição de TODA peça em que o
entregável aparece por dentro** — rotulada ou não de demonstrativo. Encaixa em: expert segurando/abrindo
o material, UGC com o produto na mão, vídeo IDA cobrindo o áudio com páginas, corte de tela, e também
estático e carrossel com página real.

**Arco obrigatório (o de §E.2b), nesta ordem:**
1. **b-roll em tela cheia** no hook (assunto/dor em movimento) — sem produto parado;
2. **entregável em tela cheia** quando a fala diz "este material";
3. **split 70/30 ou 50/50** (entregável EM CIMA) na frase de mecanismo;
4. **b-roll** no desejo até o CTA — produto parado + seta 1-2 s, nunca corte seco.

**Checklist que vale pra qualquer peça com o entregável dentro, não só a rotulada "demonstrativo"
(regra da dona, 25/10/2026 — reforçada: isso inclui legenda e velocidade, não só b-roll/split)**
(cada item já custou uma versão reprovada):
- **1 clipe/take por frase da VO**; nenhum take nem b-roll repetido na mesma peça; peças irmãs da leva
  usam b-rolls diferentes.
- **⛔ Sempre mistura fonte de cena, nunca só uma (regra da dona, 25/10/2026 — achado real: CT3
  saiu só b-roll 3D + celular, sem nenhum take Flow).** Toda peça demonstrativa combina pelo menos
  2 fontes diferentes: gravação de tela real (celular/`MATERIAL-ENTREGAVEL/`) + take Flow de mesa
  (`FLOW-TAKES/take-geral-flow.mp4`/`take-C-flow.mp4`, mandatório junto — ver §E.0c) + b-roll 3D
  quando a oferta tiver (`BROLL-3D/`). Nunca uma peça 100% só-celular nem 100% só-Flow.
- **Página real full bleed**, sem moldura e sem tarja, na sequência do início ao fim; cortar barra de
  status/URL antes de compor.
- **B-roll com o assunto no quadro**, cover 1080×1920 (cortar borda preta embutida), origem registrada
  pela `get-brolls`.
- **Legenda:** KaraokeV2 em blocos CURTOS (2-4 palavras por linha, nunca a frase inteira numa linha
  só — fica estática/lenta na tela), sincronizada palavra a palavra com o VO. Vale em TODO vídeo,
  mesmo os sem b-roll.
- **Velocidade:** timeline no ritmo natural do VO por padrão (sem acelerar); ajuste de velocidade
  só na FALA GERADA antes de montar (regra do catálogo de clipe, E.0b), nunca acelerando a edição
  já montada. Vale em TODO vídeo, independente de ter personagem, b-roll ou só gravação de tela.
- **Cortes de 1,5-3 s**, transição ~0,3 s, **sem aceleração** por padrão (playbackRate 1.0).
- **Legenda karaokê** por cima: 70% (62-64% no split), sem palavra encostando/sobrepondo; gancho em
  **até 2 frases curtas** — 3-4 frases de dor antes do produto = reprovado.
- **Vários takes do entregável**, não um take único rolando a página.
- Nunca mockup 3D, nunca "PDF" na fala, nunca tarja vermelha; trilha **-18 a -22 dB**.
- **Carrossel:** card 1 é a única arte gerada; os demais são páginas reais recortadas em sequência.
- **QA antes da dona ver:** contact sheet 1 fps, `cropdetect` em cada b-roll, frames a cada 0,5 s na
  legenda, F0 da voz antes×depois.


### E.2b — RECEITA APROVADA: demonstrativo b-roll + tela + VO (Mapa do Tarot, 2026-09-23)

Dono: "criativo top em todos os sentidos". Reuse esta estrutura para qualquer criativo
demonstrativo com VO off + gravação do entregável. Referências: `mapa-do-tarot/criativos/
CRIATIVO-1/v10_imperatriz.mp4` (final 1.15x; v8 = mesma sem acelerar) e `CRIATIVO-2/` (O Louco, mesma receita).

| Bloco (pela frase da VO) | Layout | Legenda |
|---|---|---|
| Hook (pergunta + dor) | **100% b-roll** tela cheia do assunto (ex.: mãos embaralhando cartas). SEM still/produto parado | 70% |
| "Olha esse material…" (lista do que tem) | **gravação de tela do entregável 100%** | 70% |
| "Como se conecta… pratica" (mecanismo) | **split: entregável EM CIMA 70% / b-roll EMBAIXO 30%**, feather na costura | sobe p/ ~62-64%, logo acima do b-roll (senão some) |
| "Exercícios…" até o CTA | **100% b-roll**, 1 clipe DIFERENTE por frase | 70% |

Regras que fizeram dar certo (cada uma custou uma versão):
- Tudo numa composição Remotion: layouts, transições ~0.3s, legenda `KaraokeV2` como última
  camada, `words.json` do `legenda_align.py`. ffmpeg só mede/normaliza.
- Split 50/50 com carta estática embaixo foi REJEITADO (b-roll cobria a carta); split
  30/70 com b-roll em cima também ("ficou estranho") — o aprovado é entregável em cima.
- Nenhum frame do A-roll antigo que não é mais usado (ex.: mão com a carta 0–5.34s) pode
  vazar em transição: corte seco/`startFrom` no primeiro frame da gravação.
- B-roll: objeto do nicho visível, cover real 1080×1920 (cortar borda preta embutida
  do arquivo-fonte antes), nenhum clipe repetido, e criativo irmão da mesma leva usa
  b-rolls DIFERENTES (mesma base de tela, só troca VO + b-rolls).
- ~~Final acelerado 1.15x~~ — **obsoleto**: velocidade 1.0 (`EDICAO-PADRAO.md` §4).
- QA do orquestrador antes de mostrar: contact sheet 1fps, cropdetect em cada b-roll,
  frames a cada 0.1s na troca hook→tela, karaokê mudando de palavra, F0 da voz antes×depois.

**Lições da leva ES Mapa del Tarot (dona, 05/10/2026 — v1 reprovada):**
- **Gancho no máximo 2 frases curtas** (2 linhas de legenda). Logo em seguida a fala já é
  sobre o material e a tela já MOSTRA o material. 3-4 frases de dor antes do produto = reprovado.
- **Modelo de gancho aprovado ("carta mal-entendida"):** "Acha que a carta X é só sobre Y?
  Olha esse material." → mapa da carta X em tela (significado tirado do que aparece no
  mapa, nada inventado) → exercício → outras cenas. Usado na Imperatriz (BR) e La Muerte (ES).
  Se a dona mandar vídeo filmado da carta física + tela, o criativo ABRE com ele, mas SÓ
  durante a pergunta do gancho; no "Olha esse material" já cortam as gravações de tela limpas.
- **Dona mandou várias gravações do entregável = cada criativo mostra um pouco de CADA uma.**
  Não a gravação inteira: cortes curtos (1,5-3 s) das MELHORES cenas de cada gravação,
  escolhidas para casar com a fala daquele criativo. 1-2 gravações inteiras por vídeo = reprovado.
- **Legenda com palavras sobrepostas = reprovado.** Gate obrigatório: frames a cada 0,5 s
  ao longo do vídeo inteiro, nenhuma palavra encostando/sobrepondo outra; grupo de ~3-4
  palavras, frase longa quebra em 2 linhas, gap da KaraokeV2 maior que o pop.
- Gravação de celular: cortar barra de status/URL do navegador antes de compor.

**Regra do demonstrativo (low ticket) — vale para qualquer Modo E.** O criativo
demonstrativo é feito de **b-roll + o entregável gravado por dentro em VÁRIOS takes**
(um take por parte do entregável: sumário, um módulo aberto, um exemplo, um clique
que abre uma ficha — nunca um take único rolando a página). O que segura a atenção é
o **arco dinâmico**, que vai abrindo o entregável aos poucos:

1. **Abre com b-roll** em tela cheia (hook: o assunto/dor, em movimento).
2. **Entregável em tela cheia** (o que tem dentro, "olha esse material").
3. **Split**: **meio a meio (50/50) ou 70/30** com o entregável em cima e o b-roll embaixo.
   Uma ou outra depende da fala: 70/30 quando o entregável precisa ser lido; meio a
   meio quando o b-roll carrega metade do sentido. Pode usar as duas no mesmo criativo.
4. **Fecha com b-roll** em tela cheia (resultado/desejo até o CTA).

Trocar de take/clipe a cada frase da VO; nenhum take nem b-roll se repete no mesmo
criativo. No split o b-roll é vídeo em movimento e nunca cobre a tela do entregável
(o 50/50 rejeitado abaixo foi com carta ESTÁTICA embaixo, não pelo 50/50 em si).


### GATE FINAL — obrigatório antes de chamar qualquer vídeo de "pronto"/"final"

> ⚠️ **OBSOLETO em parte (26/10/2026):** a checagem "aceleração aplicada", o 1.35x e a trilha
> `duration=first` (que corta a música no fim da fala) NÃO valem mais. O gate atual é a seção 9 de
> `references/EDICAO-PADRAO.md` (trilha contínua até o fim do card, velocidade 1.0).

Erro real (2026-09-09): 8 vídeos (calça jeans, vestido, camisola) foram entregues
e subidos pro Drive como "final" faltando voz certa, trilha e aceleração — regra
que já estava escrita acima, só não era **gate**, e por isso foi pulada sob pressa.
Descoberto só quando o usuário abriu um arquivo e notou o áudio cortado. A partir
de agora, todo `*-final.mp4` passa pelas quatro checagens abaixo antes de subir —
sem exceção, sem "depois eu ajusto":

| Checagem | Comando | Critério |
|---|---|---|
| Voz do nicho certa | ouvir/checar a voice-id usada no `narrar.sh` | feminina em moda feminina/beleza/maternidade; nunca o default `Brandon` (masculino) sem decidir |
| Trilha presente | `ffmpeg -i final.mp4 -af silencedetect=noise=-40dB:d=0.3 -f null - 2>&1 \| grep silence_` | **nenhuma linha de silêncio** — trilha contínua cobre até as pausas da narração |
| Aceleração aplicada | `ffprobe -show_entries format=duration` do final vs. soma bruta das cenas | final **mais curto** que a soma das cenas em 8s cada (não é 1:1 sem corte/aceleração) |
| Áudio completo | `silencedetect` não pode mostrar silêncio > 1s cobrindo o trecho de uma cena inteira | pega o bug do `amix duration=first` que corta no fim da 1ª fala |

Pipeline padrão pra passar as quatro de uma vez, narração off (sem lip-sync a
proteger):

1. Narração por `narrar.sh` com voz do nicho (nunca o default).
2. Concat mudo das cenas → overlay da narração (`adelay`+`amix duration=longest`
   se for por-cena, ou `-shortest` se for narração única) → **1.35x** de aceleração
   (video+áudio juntos, `setpts=PTS/1.35`+`atempo=1.35`) → mixar trilha `-20dB`
   (`duration=first`, corta a música no fim da narração).
3. Só então: `silencedetect` tem que vir **vazio**. Se aparecer qualquer
   `silence_start`, algo no pipeline não fechou — não sobe assim.


### E.4b — Sem guia, a tela carrega o criativo sozinha

Criativo 100% narração off, sem personagem em nenhuma cena: a gravação de tela
do produto **tem que aparecer em algum momento**, meio a meio ou em quadro
cheio. Sem rosto guiando, é a tela que prova que a oferta é real — só b-roll do
zero ao fim, sem nenhum trecho de tela, vira anúncio genérico e não converte.
Não precisa em toda cena, mas nenhum criativo sem guia fecha sem pelo menos um
bloco de tela.

### E.5 — O que continua valendo

Se houver personagem falante, o pipeline dele é o desta skill sem desconto:
imagem→vídeo, 16 palavras por cena no Veo, rosto em toda cena falada, bloco de
dentes literal, anti-morphing, gate de imagem e gate de clipe. O que o Modo E
elimina é a geração das cenas de **mundo** — não a do rosto.

Custo: é o modo mais barato em cota de IA e o mais caro em edição. Orce tempo de
montagem, não de geração.

### E.6 — Reaproveitar clipe existente com narração NOVA: isso é Modo E, não regravação de fala

Caso recorrente: já existe um criativo (ou clipes soltos) de uma leva anterior, a
copy/roteiro dele não vende (foi escrito sem método, ou sem ler a página de
vendas), mas o material visual é bom e dá pra reaproveitar. A tentação é trocar só
o áudio/texto por cima do vídeo pronto.

**Isso quebra se a cena tem rosto falando.** O clipe de talking-head já tem a boca
sincronizada com o roteiro velho — trocar as palavras por um texto novo (tamanho,
ritmo e conteúdo diferentes) desincroniza os lábios de forma visível. Não tem
correção de pós que resolva; é o mesmo defeito de fundo do item "Voz tocando com a
boca parada" da FASE 4, só que causado pela troca de roteiro em vez de estouro de
orçamento.

Regra de decisão, ao herdar material de uma leva anterior:

| Cena reaproveitável | Pode levar narração nova? |
|---|---|
| Rosto falando (talking-head, lip-sync gravado) | **Não** — só serve com o roteiro que já tinha, ou vira b-roll mudo cortando o áudio/lábios visíveis (evite closes de boca) |
| Mão, objeto, tela, ambiente, qualquer cena sem lábios em quadro | Sim, livre — é exatamente isso que o Modo E usa |

Na prática: quando a copy velha não presta mas o acervo tem talking-head, **não
tente salvar a cena de rosto reescrevendo o áudio por cima** — trate o projeto como
Modo E do zero. As cenas mudas do acervo antigo (mão com material, gravação de
tela, inserts) entram como b-roll pronto; as cenas de rosto ficam de fora ou viram
referência de persona para uma leva futura de talking-head genuíno (Modo A).
Narração nova, off-screen, carrega o criativo inteiro — ver E.4b.

### E.7 — Leva de N criativos em Modo E: 1 dor por célula (matriz gatilho×ângulo removida 25/10/2026)

O Modo E não tem estrutura de teste própria. Para gerar uma **leva** (não um
criativo isolado), a fonte de diversidade é a **lista de dores/ângulos reais do
banco da oferta** (`pesquisa/PERSONA-E-ANGULOS.md` — ver GATE 0.2/MATRIZ ÚNICA em
`criativo-ads`), **não** mais a matriz gatilho×ângulo do extinto Modo C:

- **Uma dor, uma célula.** Cada criativo da leva ataca uma dor/motivo de compra
  DIFERENTE do banco — nunca repete dor com roteiro reescrito (isso é a variação
  rasa que o próprio Kevones condena hoje, ver nota no Modo A).
- **A dor decide a abertura E a estrutura do roteiro** daquele criativo (história
  pessoal vs. produto+CTA vs. ensina-um-passo) — não uma célula fixa de gatilho.
- **Persona da narração é sempre quem decide a compra** (ver FASE 0/§E.4), igual
  em toda a leva — o que muda célula a célula é a dor atacada, nunca pra quem a
  narração fala.
- O corpo de mundo (b-roll + tela) pode repetir entre células de dor parecida — é
  o **roteiro e a dor** que fazem cada criativo ser um conceito distinto, não a
  obrigação de b-roll 100% exclusivo por criativo.

Preencha a lista (roteiro por célula, 1 por dor) **antes** de sair atrás de
b-roll — só então a busca de clipes por termo (E.1) sabe o que cada criativo
precisa mostrar.

**Qual material B usar depende do formato do produto, não é escolha livre por
criativo:**

- **Produto é PDF/guia estático** (o caso mais comum em low ticket): a prova é
  gravação de tela do entregável (§E.2), mostrando o material navegável. Gravação de
  tela em device mobile real é o padrão aqui — um PDF navegado num navegador lê como
  "uso real do produto", enquanto foto estática lê como "catálogo".
- **Produto é navegável** (portal, área de membros, app, catálogo com várias
  seções): aí sim entra a gravação de tela em modo mobile (§E.2) — é o único jeito
  de provar que existe uma entrega maior que um arquivo único.
- Os dois não competem dentro do mesmo criativo: escolha um pelo formato do
  produto e mantenha nas 9 células da matriz — variar isso célula a célula sem
  motivo lê como inconsistência de produção, não como diversidade.

### E.8 — UGC dentro da leva Modo E: opcional, por CÉLULA, e é edição, não geração

A leva inteira não precisa ser 100% narração off. Célula a célula, dá pra trocar a
narração off por um **personagem UGC falando** (gerado pelo pipeline normal desta
skill — imagem→vídeo, bloco de dentes, anti-morphing) e casar ele com o material
demonstrativo por **edição**, não por geração:

- **Meio a meio / Meio a meio invertido** (§E.3): metade tela com o UGC falando,
  metade com a mão+página ou b-roll. Use enquanto a fala da pessoa descreve o que
  a outra metade mostra.
- **Miniatura/PiP**: UGC pequeno no canto, o demonstrativo (mão+página, b-roll)
  ocupa o quadro cheio. Use pra trecho mais longo de prova, com a pessoa narrando
  por cima em voz off enquanto aparece reagindo/comentando no canto.

Isso é a mesma mecânica de edição do Modo E "com guia" (§E.3), só formalizando que
**dentro de uma leva majoritariamente narração-off, uma ou duas células podem ser
UGC+demonstrativo** — não precisa ser tudo-ou-nada por leva.

Regras que não mudam:

- O UGC gerado é **novo**, pipeline completo (imagem de referência, vídeo, gate) —
  nunca é o clipe de talking-head reaproveitado de uma leva anterior com áudio
  trocado (isso quebra lip-sync, ver §E.6). Se não há orçamento/cota pra gerar UGC
  novo, a célula fica 100% narração off.
- **Custo sobe** nas células com UGC: viram Modo A de verdade (imagem+vídeo no
  GPT/Hub) por dentro do Modo E — não são "grátis" como o resto da leva.
- Escolha essas células **pela dor**: dor com relato pessoal forte ("isso
  aconteceu comigo/com alguém que eu conheço") rende mais com UGC; dor mais
  técnica/direta segue bem só com narração off.
- **Default recomendado numa leva de 9-10 (matriz da MATRIZ ÚNICA):** UGC nos
  slots que já são UUGC/expert por definição (slots 1-2), o resto fica 100%
  narração off + demonstração do entregável + b-roll. Isso mantém a maioria da
  leva no custo baixo do Modo E puro e concentra a geração paga (imagem+vídeo de
  pessoa) só onde ela mais rende. Ajuste conforme orçamento, pergunte ao usuário
  antes de mudar a proporção.
- Persona do UGC segue a mesma regra de sempre (FASE 0/§E.4): fala como quem
  decide a compra (filho/cuidador), nunca como o idoso.

---



## Movido de criativo-ads/SKILL.md (26/10/2026)

> **Regras fixas da dona (29/09/2026):**
> - **Antes de qualquer criativo, carregar as skills:** esta, `criativo-ads-video-orq`
>   (edição, legenda, Modo E, gates), `get-brolls` (b-roll) e `narracao-hub-tts` (voz).
>   Todo brief de pane de criativo manda ler as quatro ANTES de mexer em arquivo.
> - **Narração/voz off = SEMPRE `narracao-hub-tts`** (API NinjaVoice do Hub: sem browser,
>   sem login, sem cota; liberada pela dona). `languageCode` do mercado (`pt-BR`, `pt-PT`…).
>   Mapa do Tarot PT usa a voz Daniela `9L8v6Oy5x46GlKUxRg6H`. O mp3/wav vai pra
>   `intermediarios/` do criativo. Não usar MiniMax nem outro TTS sem pedido.
> - **Criativo novo = do zero, material cru:** roteiro → locução → b-roll NOVO (`get-brolls`)
>   → tela do entregável gravada agora → montagem. Nunca reaproveitar criativo já montado
>   trocando só áudio e legenda. Um criativo por mercado, em `criativos/<MERCADO>/`.
> - **Legenda:** só a KaraokeV2 canônica (ver `criativo-ads-video-orq`); a "fininha" é reprovada.
>
> **Regras da dona (05/10/2026, leva ES Mapa del Tarot):**
> - **Gancho ≤ 2 frases curtas**, depois já fala do material MOSTRANDO o material.
> - **Várias gravações do entregável = cada criativo usa as melhores cenas de TODAS**, em cortes
>   curtos casando com a fala (nunca 1-2 gravações inteiras).
> - Modelo de gancho que funciona: "Acha que a carta X é só sobre Y? Olha esse material."
> - **B-roll: o pane escolhe sozinho** (Pexels/Pixabay, origem no `credits.md`), sem parar pra
>   aprovação de prévia; a dona revisa no vídeo final.
> - Detalhe e gate de legenda sobreposta: `criativo-ads-video-orq` E.2b ("Lições da leva ES").


## Acabamento aprovado — Número Mestre AR/LATAM

Para vídeo, leia também `../criativo-ads-video-orq/references/acabamento-natural-audio-cortes.md`: cortes por fala e gesto, repetição do Flow, ruído, volume, música, legenda na timeline final e verificação do master. A referência inclui clareza psicológica: benefício concreto por item, introdução curta e CTA de desejo. **Regra da dona (04/10/2026, reforçada 24/10/2026): no VÍDEO/VO, o fecho (fala e texto na tela) é só o comando curto, sem condição de compra** (garantia, preço, vitalício, termos) **e SEM NOME DO PRODUTO** — nunca "Atlas Visual, mirá por dentro", só "mirá por dentro" / "clica aquí abajo y descubrí". Nome do produto no fecho falado soa mal e é propaganda, não comando. Vale pro VO E pro texto escrito do card CTA final (gate `criativo-ads-video-orq` item 11). Condição de compra fica na página e no `anuncio.md`. **Estático e carrossel podem mostrar garantia/vitalício** (ex.: `modelagem-escalados/references/carrossel-demonstrativo-iphone.md`). Tom do fecho: curiosidade, ex.: "Clica aqui embaixo e descobre como." — ver `criativo-ads-video-orq` e `narracao-hub-tts`. Use estes princípios em novos criativos sem copiar timestamps, alegações ou filtros cegamente.

