---
name: criativo-ads-video-orq
description: "Mecânica de produção e edição de anúncios em vídeo, chamada por criativo-ads. Use para criativo de vídeo, UGC, hook novo, variação de vencedor, modelagem de escalados, Veo/Flow, cenas com imagem de referência, b-roll, gravação de tela, PiP, narração ou trilha. Cobre briefing, persona/ângulo/oferta, orçamento de palavras, prompts de continuidade/voz/lip-sync, QA de imagem e clipe, montagem, cortes por palavra e gesto, repetição, limpeza de áudio, volume, legendas e entrega. Modos: do zero, hook+body, bodies variados, modelagem Kevones e Vitrine Guiada. Delega geração às skills de browser; usa video-use para cortes, Remotion para composição/legenda, Hyperframes para motion e ffmpeg para medição/normalização/mix. A estratégia da leva vem de criativo-ads; motor e restrições seguem as regras atuais do corpo desta skill."
---

> **HUB DESATIVADO (02/10/2026, ordem da usuária):** NinjaBR Hub está SEM COTA e os perfis `hub`/`hubv2`/`hubts` foram removidos (backup em `~/.agent-profiles/_removidos-hub-2026-10-02/`). NÃO use Hub, NÃO rode `hub-livre.sh` (sai com erro), NÃO espere perfil do Hub liberar. Imagem: ChatGPT — se a cota de upload de uma conta acabar, troque de CONTA: `gpt-conta*` ↔ `gpt-conta*`. Vídeo: Google Flow (`flow-video-playwright`).



> **Leva inteira de uma oferta:** antes dos vídeos, seguir `criativo-ads/references/RECEITA-LEVA-PONTA-A-PONTA.md` (persona → plano → gates → estáticos → vídeos).

# criativo-ads-video-orq

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
CT13 tinha palavra repetida 2x no meio da fala.** Frame em número redondo (0, 3, 6, 9...) pula
exatamente o segundo onde o defeito mora. Antes de declarar QUALQUER vídeo pronto (novo ou
reaproveitado de sessão anterior):
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

## Onde cada coisa é gerada (escolha o motor de vídeo primeiro)

| Etapa | Ferramenta | Mecânica (leia ANTES de tocar o browser) |
|---|---|---|
| Imagem de referência da cena | **ChatGPT** (`chatgpt.com`, perfil logado) | skill `gpt-imagem-playwright` |
| Vídeo, opção A | **NinjaBR Hub** (Veo 3.1 Quality, Imagem→Vídeo, com voz) — exige assinatura do Hub | `references/mecanica-hub.md` (resumo) → skill `hub-video-playwright` (detalhe) |
| Vídeo, opção B | **Google Flow** (Veo 3.x, Frames to Video) — exige conta Google com créditos | `references/mecanica-flow.md` (**não validado**: rode o protocolo de descoberta 1x) |
| Browser, perfis e lanes | Chromium persistente + `agent-browser` | `references/browser-setup.md` |

**Regra de escolha:** **NinjaBR Hub está PROIBIDO enquanto a assinatura não estiver paga (memória `ninjabr-hub-nao-usar`) → vídeo vai no Flow.** Só volte ao Hub quando o dono confirmar que pagou. Os blocos de prompt (CANON_VOICE, anti-morphing, dentes,
lip-sync, orçamento de palavras) e os gates de QA são os mesmos nos dois; só muda o
teclado. **Nunca dois motores na mesma cena.**

**Narração/voz off (VO):** skill `narracao-hub-tts` (API NinjaVoice do Hub). Essa API NÃO usa login nem perfil de browser: continua valendo mesmo com o Hub de imagem/vídeo desativado. Voz padrão dos criativos: Rocha `GTfQlFazcVAZK9iGyXN3`. NUNCA espeak, edge-tts ou voz neural sem a dona pedir; se a API falhar, pare e avise em vez de trocar de motor. `languageCode` do mercado; o áudio vai pra `intermediarios/` do criativo.

Montagem, legenda e motion: ver **Stack de edição** logo abaixo. B-roll de apoio (fonte literal, notícia, print de tela) busca com a skill `get-brolls` — ela só busca/entrega, não edita. Edição manual em timeline, OpenCut é opção externa (`~/Projetos/opencut-classic`, `bun dev:web` → localhost:3000).

## Stack de edição (qual ferramenta pra quê) — revisado 2026-09-23

| Etapa | Ferramenta padrão | Fallback |
|---|---|---|
| B-roll de apoio: cutaway, insert, footage real, print de tela/notícia, "corte do X falando Y" | **get-brolls** (`/get-brolls-brief` → `/get-brolls-review` → entrega com origem/licença). Só coleta, NÃO edita: o trecho entregue entra na montagem pelas linhas abaixo | Pexels/Pixabay/Pinterest à mão (seção Vitrine Guiada) |
| Corte de cabeça/cauda/pausas, fim da fala, repetição do Veo | **video-use** (`~/.claude/skills/video-use`): `helpers/transcribe.py` (ElevenLabs Scribe, palavra a palavra, NÃO é whisper) → `edl.json` → `helpers/render.py` (corta em fronteira de palavra, fade de 30ms em toda junção, preserva fps nativo) | `scripts/tight.py` + `scripts/montar.sh` (silencedetect) |
| Legenda karaokê de fala | **`scripts/legenda_align.py`** (tempo por alinhamento forçado roteiro+áudio) → **Remotion** `references/legenda-karaoke-tiktok-CANONICA.jsx` (KaraokeV2, vídeo+legenda na mesma composição) | ffmpeg `subtitles` estilo VSL2-MARTA (só VSL sem Remotion) |
| Split meio a meio, PiP, tarja, call-out, transição de escala | **Remotion** (composição React sobre as cenas uniformes) | Hyperframes |
| Motion/legenda animada elaborada, cards gráficos, transição com velocidade casada | **Hyperframes** (`hyperframes-*`, `talking-head-recut` pra cards sobre fala, `cut-the-curve` pra costuras) | Remotion |
| Medir (ffprobe, silencedetect, volumedetect, mpdecimate), extrair frame, normalizar resolução, concat, mix narração+trilha | **ffmpeg** — é a ferramenta certa aqui, não troca | — |
| Ajuste fino à mão pelo dono (timeline visual) | **OpenCut classic** (`~/Projetos/opencut-classic`, http://localhost:3000) — ferramenta externa, não é passo automático | — |

Regras que valem pra qualquer ferramenta da tabela:

- **Timestamp de palavra NUNCA sai de whisper** (regra do dono, ver cabeçalho do `.jsx` canônico). Isso exclui `faster-whisper`, `whisper.cpp`, `@remotion/install-whisper-cpp` (o que a skill `remotion-captions` ensina) e `hyperframes transcribe` (motor `auto` cai em whisper no Linux; `parakeet-mlx` é só Mac). As skills `talking-head-recut` e `embedded-captions` chamam `hyperframes transcribe` (whisper) no passo de transcrição: pule esse passo e entregue o `transcript.json` pronto (array plano `[{text,start,end}]`) gerado de uma fonte aceita. Fontes aceitas: Scribe via video-use, timing devolvido pelo TTS, forced-alignment não-whisper, grade de um VO gêmeo, ou distribuir por duração.
- **video-use precisa de `ELEVENLABS_API_KEY`** (env ou `.env` na raiz de `~/Developer/video-use`). Em 2026-09-23 a key **não está configurada**: sem ela, use o fallback da tabela e não trave o loop pedindo key. Scribe é pago por minuto de áudio; o transcript fica em cache em `<videos_dir>/edit/transcripts/`, nunca transcreva de novo o mesmo arquivo.
- Do video-use aqui se usam **os helpers**, não o fluxo conversacional dele (entrevista + confirmação de estratégia): a estratégia já saiu da FASE 0/1 desta skill.
- Legenda sempre é a ÚLTIMA camada, em qualquer ferramenta.

Jeito antigo (ffmpeg pra tudo): ver `references/SKILL-ffmpeg-OLD-2026-09-23.md` (cópia integral do SKILL.md antes desta revisão).

## DOUTRINA — o criativo valida o público (regra 2026-09-21)

**PRINCÍPIO-MÃE:** o criativo tem que SAIR como se fosse orgânico. Nada inventado
de IA, nada exagerado, **nada clean/perfeito** — acabamento de agência denuncia
que é anúncio e mata a entrega. E o padrão é **partir sempre de um MODELO
VENCEDOR da biblioteca de escalados** (`modelagem-escalados`), modelar o que já
roda com verba — não inventar do zero.

Meta usa o CRIATIVO pra achar e validar o público, não só o targeting. Criativo
que não diz pra quem é = algoritmo joga num leilão largo/caro. Sintoma real:
CPM disparou (R$400 → R$1200) num criativo bonito e vazio (mockup neon, sem
rosto, sem dor, sem público nomeado). CPM alto quase nunca é "público ruim" — é
**criativo que não comunica pra quem é**.

**Em vídeo, quem valida o público é o HOOK.** O hook nomeia a persona nos
primeiros 1-2s, direto: *"Se você é dono de barbearia..."*, *"Professor que dá
aula particular, presta atenção..."*, *"Nutricionista sem site, isso é pra
você."* O criativo aponta o público pra ele mesmo se reconhecer. Uma leva =
vários hooks, um por persona (mesma matriz persona×ângulo do Kevones), body
igual. Assim cada persona valida separado e o algoritmo aprende rápido.

**O criativo tem que parecer o mais ORGÂNICO possível.** Facebook/Instagram são
redes de ENGAJAMENTO — o feed premia conteúdo nativo e enterra o que grita
"anúncio". Cara de IA / bonito-cool demais / render limpo = engajamento cai =
**CPM dispara**. Cenário e composição têm que parecer post orgânico / conteúdo
nativo tirado por uma pessoa, não peça de agência. Isso é o que baixa o CPM.
**Priorize os formatos da biblioteca de escalados** (`modelagem-escalados`) que
já imitam conteúdo orgânico — print de Stories, caixa de perguntas, vídeo de
celular na mão, screen-record — em vez de inventar arte "de anúncio". E use
**fonte estilo legenda de Story** (sans limpa, nativa). Referência de formato que
performa:

- **Cara de post de Stories:** legenda em cima do vídeo com fonte tipo Stories,
  linha fina, texto simples — não banner de oferta.
- **Legenda estilo TikTok/Reels nativo (karaokê):** palavra a palavra, texto
  **branco** que **pula pra amarelo** na palavra falada no momento (o "bounce"
  word-by-word highlight). É o padrão de legenda auto do TikTok — passa como
  conteúdo, não como ad. Montar no Remotion (ver `remotion-captions` /
  `captions-overlay`). Amarelo destaca a palavra-gancho da fala.
- Gravação de tela real, PiP falante, b-roll de banco — tudo que quebra o
  acabamento "comercial" e aproxima de UGC.
- **Palette da marca:** azul é a identidade/paleta (IPP); laranja SÓ no CTA/botão,
  não espalhado. (MinhaEmpresa — não o violeta velho.)
- **Texto no estático/thumb: prefira o GPT colocar o texto**, não overlay de
  código — texto do GPT sai orgânico (legenda de Story), overlay de código sai
  "perfeito demais", cara de anúncio. Diga o texto exato + fonte estilo Story +
  cores no prompt do GPT. QA de ortografia obrigatório (modelo erra letra),
  regenera se torto. (Legenda karaokê de vídeo continua no Remotion.)
- **TODA imagem de criativo/ad sai com FILTRO ORGÂNICO "foto feia de celular", SEMPRE.**
  Diferente do entregável/mockup (esses são limpos, na identidade do `DESIGN-SYSTEM.md`):
  a imagem de anúncio tem que parecer foto real tirada no iPhone e postada no Stories —
  não render de IA, não estúdio. No prompt do GPT peça explícito: foto de celular amador,
  levemente torta/desalinhada, luz natural/ambiente imperfeita, leve grão/ruído e blur de
  câmera de celular, sem retoque, enquadramento de story vertical, "shot on iPhone", cara de
  UGC/postagem espontânea. Nada de perfeição comercial. **Isso derruba muito o CPM** — é o
  que faz passar como conteúdo nativo, não como ad. Regra de vida, todo criativo. Memória
  `criativo-imagem-organica-iphone`.
- **Mockup/entregável DENTRO do criativo = foto orgânica de "eu imprimi e usei".** Quando o
  criativo mostra o produto (mockup, capa, página de entrega), NÃO cole o mockup limpo do
  DESIGN-SYSTEM na arte — peça ao GPT uma FOTO amadora de iPhone do material **impresso em papel
  espalhado numa mesa de casa real** + **tablet/celular mostrando a capa**, com props do dia a dia
  (xícara de café, óculos, caneta, luz de janela), leve grão e enquadramento torto, legenda de
  Story por cima. Parece que a pessoa comprou, imprimiu e fotografou — não render de catálogo.
  Refs reais em `references/organico-iphone/` (ref-entregavel-impresso-mesa.png,
  ref-mockup-tablet-mesa.png — tutorial nicolasmoreirafe, "criativos em imagem totalmente
  orgânicos"). Anexe essas refs no GPT + a capa/página real do produto como conteúdo.

### §E.0c — Demonstrativo "mesa real" animada (imagem→vídeo, validado 20/10/2026)

Complemento ao Modo E de gravação de tela: em vez de só b-roll + tela gravada,
gera uma FOTO orgânica realista da pessoa com o aparelho/páginas reais na mesa e anima ela
direto no Flow (imagem vira 1º frame do vídeo). **Não é alternativa — é mandatório em TODO vídeo
da leva, junto com a tela gravada (regra da dona, 24/10/2026): cada peça monta os DOIS,
gravação de tela real do entregável + take mesa real do Flow.** Vídeo só com um dos dois está
incompleto.

**Antes de gerar qualquer imagem desse tipo, pense (não invente):**
- **Cenário**: mesa de casa real, luz de janela, props do dia a dia — nunca estúdio.
- **Quem aparece**: a persona da oferta (gênero, idade, como ela é de verdade — ver
  `pesquisa/PERSONA-E-ANGULOS.md` da oferta). Nunca genérico.
- **Páginas do entregável**: SEMPRE arquivo real anexado (`produto/ENTREGA/`), nunca a página
  inventada pelo modelo — mesma regra do Gate 0.1 de `criativo-ads`.

**Receita (2 ferramentas, nessa ordem):**
1. `gpt-imagem-playwright` — gera a foto-base (1 cena por mensagem, chat novo, referências reais
   anexadas: capa + 2-3 páginas do entregável + identidade visual). 9:16, sem texto/legenda
   queimada (a legenda final é sempre Remotion KaraokeV2 depois). Composição = uma das letras
   do CATÁLOGO abaixo.
2. `mecanica-flow.md` — anima a foto aprovada: upload por interceptação CDP
   (`Page.setInterceptFileChooserDialog` + `DOM.setFileInputFiles`, NUNCA o fallback
   prompt-only, que perde a imagem exata), 9:16, prompt só do MOVIMENTO (câmera/mão/dedo —
   a composição já está na imagem, não repete a cena inteira em texto).

#### Catálogo de takes — como pedir

Pra pedir, basta dizer **a letra** ("quero a take B desse criativo") ou **descrever a cena** em
1 frase ("quero uma de notebook" → cai na C). Quem gera cruza com `PERSONA-E-ANGULOS.md` pra
decidir QUEM aparece (gênero/idade) e quais páginas reais mostrar — nunca pede confirmação óbvia,
só avisa a escolha.

**Sem letra ("produz as takes dessa oferta", "faz o demonstrativo mesa real") = escolha
automática.** Não pergunte qual letra — espalhe sozinho **2-3 letras bem diferentes** entre si
(ex.: uma com pessoa + uma só-mão/sem-rosto + uma 100% papel, nunca duas parecidas), busque as
páginas reais certas pra cada cena (`produto/ENTREGA/`, 2 a 5 páginas conforme a cena pedir — nunca
só a capa) e produza as 2-3 até vídeo final, avisando no fim quais letras saíram e por quê.

| Take | Composição | Movimento no Flow |
|---|---|---|
| **A** | Multi-aparelho: notebook+tablet+celular na mesa, cada tela uma página diferente, pessoa aparece e aponta pra um detalhe numa das telas. | Só o dedo e leve drift de câmera. |
| **B** | Só a MÃO (sem rosto/corpo) + 1 tablet na mesa + páginas impressas soltas ao redor. | Dedo apontando + drift leve. |
| **C** | Notebook como peça central (tela com 1 página), páginas reais espalhadas do lado, pessoa aparece. | Dedo/mão + drift leve. |
| **D** | Páginas FÍSICAS impressas empilhadas/meio-fanned na mesa, SEM tela nenhuma, 100% papel. | Só drift de câmera (ninguém mexe, parece que vai folhear). |
| **E** | Tablet + caneta tipo Apple Pencil apontando/riscando um detalhe na tela, zoom — estilo "apresentador". *(pendente de gerar)* | Caneta se movendo + zoom. |
| **F** | Tablet E celular PARADOS lado a lado na mesa (cada um com uma página), SEM mão mexendo/rolando nada — a cena é estática. | **Movimento de câmera NATURAL/cinematográfico** (drift/pan leve, como mão segurando o celular gravando) aproximando das telas — **nunca zoom de lente puro/mecânico que corre reto até o ponto** (regra da dona, 20/10 + reforçada 24/10: "zoom até o ponto e para" parece automação; o certo é câmera se aproximando devagar, orgânico). Imagem de referência aprovada: `~/Downloads/ar-takeF.png`. |
| **G** | Tablet segurado BEM DE PERTO pela pessoa (close-up na mão/peito, não na mesa), página real na tela, enquadramento fechado. | **Zoom de câmera** aproximando mais ainda, sem a pessoa mexer o braço. |
| **H** | POV: a PRÓPRIA mão da pessoa segura o tablet lendo (ângulo em primeira pessoa, como quem fotografa o próprio colo), 1 página real na tela. | Dedo ou caneta mexendo/rolando a tela + leve drift. |
| **I** | Flat-lay limpo: 2 páginas IMPRESSAS reais levemente sobrepostas, vista de cima, mesa de madeira, caderno fechado + caneta do lado — SEM mão, SEM device, SEM pessoa. | Só zoom/drift bem sutil de câmera (cena estática de propósito). |

| **J** | TV grande em primeiro plano com a página real cheia (tela, não papel), caneta apontando pra ela; tablet + notebook menores e desfocados ao fundo/embaixo, de apoio. | Caneta risca diagonal, do canto superior até embaixo da tela, **câmera dá zoom junto** (não fica parada) — os dois movimentos simultâneos, não um depois do outro. |

| **K** | Over-the-shoulder: câmera ATRÁS da pessoa (só cabelo/ombro em quadro, rosto nunca aparece), tablet na mão dela de frente mostrando a página real, dedo tocando a tela. | Dedo tocando um ponto + zoom de câmera aproximando por trás do ombro. |

| **M** | Mesa com VÁRIAS páginas físicas espalhadas (5+, diferentes cartas), a mão folheia/desliza uma por cima da outra revelando cada página em sequência — câmera PASSEIA pela mesa acompanhando (pan), não fica parada num ponto só. Mostra volume e variedade, não uma pilha estática. Referência: vídeos de concorrente analisados 20/10 (`pesquisa/referencia-vsl` style, folheando cartas uma a uma). | Mão folheando + câmera em pan contínuo acompanhando o movimento — mais dinâmico que a D (que é só drift sutil numa pilha parada). |
| **L** | Close-up na tela de um celular mostrando página real. Dois dedos (polegar+indicador) visíveis fazendo o gesto físico de pinça (pinch-to-zoom) sobre a tela — igual quem dá zoom numa foto no próprio celular. Resto do corpo fora de quadro. | Os dois dedos abrindo em pinça, tela ampliando o detalhe em sincronia com o gesto (zoom = ação da mão, não só drift de câmera). |
| **N** | Mão segurando o material como um LIVRO fechado (capa do entregável bem visível, como produto físico) e depois abrindo em livro, mostrando 2 páginas reais abertas lado a lado. Ou só a capa sendo exibida pra câmera, sem abrir — o que fizer sentido pro criativo. | Mão abre o "livro" revelando as 2 páginas + leve drift de câmera; ou só sustenta a capa com leve drift, sem mecânica de abrir. |
| **O** | 100% papel: VÁRIAS páginas reais impressas espalhadas/semi-empilhadas na mesa (como M), e por CIMA delas a mão segura a CAPA do entregável virada pra câmera — as páginas de baixo ficam parcialmente visíveis/espiando pelas bordas, mostrando que tem conteúdo por trás da capa. Referência: `~/.overclock-app/dropped/1792854006010-pasted-image.png`. | Só drift/zoom cinematográfico leve de câmera, mão parada segurando a capa (sem abrir/folhear) — variação mais estática que N, serve pra diversificar a leva. |

### Regras fixas 24/10/2026 (dona) — valem em toda take, novas e antigas

- **Combinação obrigatória de material em cena:** sempre **1-2 aparelhos digitais** (celular/tablet/notebook,
  qualquer combinação) **+ 3-4 páginas impressas soltas**. Nunca só papel, nunca só tela — a combinação é
  o padrão, salvo a take ser deliberadamente 100% papel (D, I) ou servir de variação proposital.
- **Nada repete, em lugar nenhum da cena:** o que está numa tela não aparece em outra tela nem numa folha
  impressa; cada folha impressa mostra uma página diferente das outras folhas e das telas. Dispositivo e
  folha = sempre conteúdo exclusivo.
- **Zoom corrigido 24/10 (2ª rodada):** o zoom que a dona quer é o de CÂMERA, só que **cinematográfico/
  orgânico** — câmera se aproximando devagar como se uma pessoa estivesse filmando/segurando o aparelho,
  NUNCA o zoom mecânico que corre reto até o ponto e para ("zoom de lente", tipo motion graphics). A
  diferença é o movimento: orgânico tem leve imperfeição/drift, não é uma trajetória perfeita e previsível.
  **Gesto da mão é, por padrão, APONTAR** (dedo indicando o trecho, como M/K), não pinça. **Pinça
  (pinch-to-zoom, extensão/expansão) é EXTRA opcional**, só quando a cena pedir (ex.: tablet no colo/na
  mão, dá pra ela "esticar" uma parte com os dedos) — se não couber na cena, não force, use só o apontar
  + o zoom de câmera orgânico.
- **Folha impressa sempre proporção A4:** retrato (~1:1.414) na maioria dos casos; se a página do
  entregável for deitada, a folha é A4 **landscape** (~1.414:1), nunca uma proporção fora disso tipo
  "mini-folha" quadrada ou esticada — fica torto/feio e denuncia que não é impressão real.
- **Capa é bem-vinda:** incluir 1 página/plano com a CAPA do entregável (como produto físico) é um reforço
  bom em qualquer take — soma-se às 3-4 páginas de conteúdo, não substitui.
- **Prop tipo "livro":** segurar o material fechado como livro (capa visível) ou aberto mostrando 2 páginas
  reais lado a lado (take N) é uma composição válida sempre que fizer sentido pro criativo — não é
  obrigatória, é mais uma ferramenta do catálogo.
- **O mesmo acabamento orgânico do estático vale no vídeo:** cara de foto/filmagem real de iPhone, sem
  legenda queimada na cena (a legenda final é sempre Remotion depois) — não é um visual separado, é a
  MESMA regra de `criativo-imagem-organica-iphone` aplicada ao frame de vídeo.
- **Expert pensado ANTES, não genérico:** rosto/idade/gênero/figurino do expert tem que combinar com a
  oferta e com quem exerce aquele papel na vida real — ex.: oferta pra cuidador de idoso → expert com cara,
  idade e roupa de cuidador profissional de verdade (não qualquer adulto de jaleco). Decidir isso lendo
  `pesquisa/PERSONA-E-ANGULOS.md` da oferta ANTES de gerar a imagem-base, igual se faz pro estático.
- **Voz: gerar primeiro para acertar a boca, trocar depois.** Pode gerar a cena no Flow com qualquer voz
  (inclusive a nativa do Flow, mesmo sendo ruim) só pra garantir que o lip-sync/movimento de boca saia bom;
  o áudio final da fala é sempre trocado pela nossa voz fixa (`narracao-hub-tts`, Rocha) antes de entregar —
  nunca a voz do Flow fica no criativo final.

**⛔ UGC não usa take genérico do banco compartilhado (regra da dona, 25/10/2026, caso CT22
Atlas/Nico).** `FLOW-TAKES/take-geral`/`take-C` (§E.0c, "reaproveitáveis em todos os 10 vídeos")
servem pro **demonstrativo** (mão anônima, sem persona — mesa real sem rosto). Peça rotulada
**UGC/UGC** é outra coisa: é recomendação de UMA pessoa específica — o corpo tem que mostrar ESSA
pessoa segurando o material, cena gerada só pra ela (imagem GPT da persona segurando o produto +
Flow i2v), nunca o clipe de mão genérica do banco. Usar o take compartilhado numa peça UGC quebra
o formato: hook mostra rosto, corpo vira mão anônima sem conexão — lê como demonstrativo, não
recomendação. Sinal de que errou: a mesma mão/mesa aparece em UGC de personas diferentes na leva.

**Preferência padrão: pessoa de COSTAS/over-the-shoulder, não de frente (regra da dona,
20/10/2026).** Quando a take tiver pessoa (A, C, G, K…), o padrão é rosto NÃO aparecer — só
cabelo/ombro/mão, como a K. Rosto de frente só entra se o criativo realmente precisar (ex.:
reação, expressão). Motivo dela: fica mais orgânico, "menos cara de IA" (rosto gerado de frente
entrega mais o giveaway de IA que o corpo de costas). Aplicar isso como padrão em qualquer take
nova que incluir pessoa, a menos que a cena peça expressão facial.

**Diversifique IMPRESSO × DIGITAL na mesma leva** — não repita só tela (regra da dona, 20/10):
D e I são 100% papel; A/B/C/F/G/H têm tela. Uma leva boa mistura os dois tipos, não só variações
de "gente com tablet".

**Regra fixa em TODA take (já embutida no prompt do Flow, não é opcional):** dentro de UM clipe
os elementos nunca mudam do início ao fim — nada aparece, some ou pisca (`nothing ever flickers
or changes content`, `no jumping, no cuts`). Composição pode variar LIVRE de take pra take (A
vira G sem problema); dentro da MESMA take é sempre a mesma cena, só com o movimento pedido.

Toda letra nova que não existir ainda: criar seguindo o mesmo gate (cenário real + persona pensada
+ páginas reais anexadas) e **acrescentar linha nesta tabela** depois de validada — é o catálogo
vivo, não lista fechada.

Depois do clipe cru: segue o acabamento normal (KaraokeV2, `narracao-hub-tts`, gate de
`acabamento-natural-audio-cortes.md`) igual qualquer outro take. Pasta: `criativos/<MERCADO>/
CRIATIVO-N/take-<letra>/`.

**"Empresário" é só um exemplo — a persona varia.** Não fixe numa role. O método
pra gerar as personas/hooks de uma leva:

1. **Liste TODA funcionalidade da entrega** — tudo que o produto faz/inclui.
   (Ex. SiteExpress: site em 72h, alteração inclusa todo mês, hospedagem inclusa,
   link da bio, botão WhatsApp, mapa, aparece no Google, sem fidelidade, painel
   próprio, domínio .com.br...) Uma linha por funcionalidade.
2. **Cada funcionalidade vira um ângulo** — o benefício/dor que ela resolve.
3. **Cada ângulo puxa uma persona/role** que sente aquela dor. Uma funcionalidade
   pode servir várias personas; escolha a que mais dói pra cada uma.
4. O hook = persona + ângulo. Leva = 1 hook por (persona×ângulo), body igual.

Assim a leva cobre vários públicos de propósito e o algoritmo valida qual role
converte, sem você chutar "empresário". É a matriz persona×ângulo do Kevones,
alimentada pela lista de funcionalidades da entrega.

**O texto do anúncio (copy primário/legenda) também valida o público.** Não é só
imagem/vídeo. A primeira linha do copy nomeia a persona e a dor, igual ao hook —
o Meta lê o texto pra entregar. Copy genérico = leilão largo. Mesma regra: 1
persona por variação, primeira linha = persona + dor.

**Palavras que inflam o CPM — evite.** Certos termos derrubam o quality/engagement
ranking e disparam o CPM (ou reprovam o anúncio):
- **Atributo pessoal na 2ª pessoa** ("você está endividado", "você é gordo",
  "você tem mais de 50") — política de atributos pessoais do Meta, penaliza forte.
  Reescreva impessoal: "quem tá endividado", "pra quem passou dos 50".
- **Promessa/sensacionalismo** ("garantido", "100%", "ganhe dinheiro fácil",
  "milagroso", "urgente!!!", CAIXA ALTA excessiva, excesso de emoji/!!!).
- **Termos de nicho sensível** (saúde, dinheiro, relacionamento, emagrecimento)
  ditos como afirmação sobre a pessoa.
Prefira dor + prova + benefício concreto, em 2ª pessoa neutra ou 3ª pessoa.

**B-roll → skill `get-brolls`.** Sempre que o criativo pedir vídeo de apoio,
cutaway, insert, print de tela/notícia ou footage real, use a skill `get-brolls`
(busca em YouTube/IG/TikTok/Wikimedia/NASA/Pexels/Pixabay, com prévia pra revisão
e origem+licença registradas). Ela entra em DUAS fases:
- **Ao PENSAR o criativo** (concepção): buscar referência real de como o conteúdo
  orgânico daquele ângulo se parece — alimenta o conceito e mantém a estética
  nativa (não "cara de IA"). Isso é o mais importante.
- **Na PÓS-PRODUÇÃO**: sourcear os clipes de b-roll de verdade, já com licença e
  proveniência, pra montar/ilustrar.
Comandos: `/get-brolls-brief`, `/get-brolls-review`, `/get-brolls-status`.
`get-brolls` NÃO edita/renderiza o final — só coleta e entrega os trechos.

**Atualização 23/10/2026 (dona) — vale por cima do bloco abaixo:**
- **Cena com material = digital + impresso** (1 aparelho no mínimo + folhas impressas soltas, página diferente em cada). Regra completa em `criativo-ads`.
- **Idioma da busca = o que faz sentido pro contexto**, não sempre inglês: se o objeto aparece na
  cena com texto (ex.: carta de tarô), buscar no **idioma da persona** (Tarot AR → espanhol).
- **Rápido:** pega os **mais vistos sem texto**; se o texto aparece só no começo, **corta o começo**
  e usa o resto. Tira **3–4 cenas que façam sentido** e reaproveita em vários criativos; baixa mais
  só se precisar. Ordem de fonte: **TikTok > Pexels > YouTube** (YouTube costuma ser ruim).
- **Imagem da cena SEMPRE primeiro** (GPT), com prompt pensado pra não aparecer/sumir nada estranho e
  a pessoa ficar igual — só depois anima no Flow (o Flow é instável).
- **Layout do expert:** tela cheia quando fala e/ou **meio a meio com o material** em algum momento.
- **Expert no Flow:** o Flow segura no máximo **8s** e a continuação sai ruim → o expert aparece só
  nos **primeiros segundos** (ex.: lendo a caixa de perguntas em formato story) e depois entra o
  material + narração. **Voz do expert é sempre a mesma:** escolhe a voz no Flow, ou gera com
  qualquer voz e troca o áudio pela nossa voz (`narracao-hub-tts`). O prompt diz **o idioma** em
  que ela fala, pra sair claro na língua da persona.
- **CTA final (estilo Rodrigo):** nos últimos segundos, imagem do material + setinha "tocá en
  más información" rodando uns segundos.
- **Formato "imagem animada" (estilo slide do Canva):** título + elemento que se mexe e faz
  sentido (ex.: mão embaralhando o tarô) — conta como vídeo na leva.
- **Antes de gerar qualquer vídeo:** a **gravação de tela do entregável** (área de membros por
  dentro) tem que existir, e os takes no estilo Flow com as páginas em vários aparelhos/formatos
  (`§E.0c`, takes A–K). Sem isso, não começa.

**TikTok — vídeos virais em INGLÊS (regra da dona, 16/10/2026).** Além do stock, usar **vídeos orgânicos que
já viralizaram** no TikTok como b-roll (é o que parece nativo — os originais que modelamos intercalam MUITA
cena real com o material). Buscar no perfil logado **`tiktok`** (porta 9255) com **~5 termos em inglês ligados
ao produto** (ex.: `dementia activities`, `caregiver grandma moment`, `occupational therapy elderly`,
`memory care activities`, `elderly cognitive games`), priorizando **muitas views**. ⛔ **O clipe NÃO pode ter
texto/legenda queimada** (nem caption, nem watermark, nem outro idioma) — a legenda é a NOSSA (KaraokeV2).
Baixar pela rota do **`get-brolls`** (`gb.py resolve --url <url> --shot <beat>` → `fetch`) pra sair com
origem/licença; `yt-dlp` como fallback, **sempre registrando `credits.md`** (termo, URL, @autor, views).
Montar intercalando **~15–20 cortes curtos (~2–3s)** do material do produto + as cenas reais.

**UM criativo serve feed E stories** — não renderize dois. Monte no canvas 9:16
(1080×1920), mas mantenha TODO texto/legenda/CTA/logo dentro da **banda central
4:5 (1080×1350)** — os ~285px de cima e ~285px de baixo são só fundo/vídeo. Assim
o corte do feed não come legenda. Vale pra estático e pra legenda de vídeo.

Gate: antes de subir, o criativo passa no **teste de 1 segundo** — estranho olha
1s e sabe (a) PRA QUEM é e (b) a DOR. Não passou, não sobe.

## Este pipeline roda em LOOP — regra genérica, vale pra qualquer projeto/produto/nicho

Diferente de um loop-kit por projeto (que carrega estado exclusivo de uma oferta),
este é o comportamento padrão desta skill em QUALQUER uso dela — sem cópia por
produto, sem pasta própria. A regra existe porque, em produção, a execução
travava sozinha no meio de uma etapa (imagem gerando, clipe gerando, gate
rodando) e devolvia o controle achando que alguém ia avisar quando terminasse.
**Ninguém avisa.** Só quem está olhando a tela/arquivo sabe.

- O loop é **você, o modelo, sendo acordado de novo via `ScheduleWakeup`** (o
  `/loop` dinâmico do harness), não um script `.sh`/`.py` com `sleep` que roda
  sozinho em background esperando ser avisado. Se cair nesse padrão, pare —
  volte a checar você mesmo, um passo de cada vez.
- Nunca devolva o turno com frases tipo "aguardando a geração terminar" ou
  "aguardando notificação" sem ter chamado `ScheduleWakeup` antes — isso é
  abandonar a leva no meio.
- Cada wakeup faz um pedaço real e verificável de trabalho (nova imagem, novo
  clipe, gate passou, cena montada) — nunca "vou esperar mais um pouco" sem
  checar nada novo.
- **Trava contra loop fantasma:** se dois wakeups seguidos não mudaram nenhum
  arquivo, isso é TRAVAMENTO REAL (browser caiu, lane perdida, Cloudflare,
  fila zumbi — ver `hub-video-playwright`/`gpt-imagem-playwright`). Investigue
  a causa antes de reagendar de novo; não insista cego.
- Só termina o loop (`ScheduleWakeup stop:true`) quando a leva inteira passou
  no gate (`gate.sh`), foi montada e entregue — ou quando travou de verdade e
  precisa do usuário pra destravar (ex: pedir 2FA, decisão de produto).
- Delegou pra um agente em background paralelo? Você continua sendo a rede de
  segurança: acorda, confere arquivo real (nunca confia no relato do agente
  sem olhar), cutuca se ele estiver parado.

## Números que quebram criativo — decore estes

Todos medidos em produção, todos invisíveis ao `ffprobe`. Errar qualquer um custa
regeração.

| Regra | Valor | O que acontece se errar |
|---|---|---|
| **Bloco de dentes em cena falada** | sempre | dente some, fica prateado, amarelo ou torto **durante** a fala |
| **Bloco de dentes COPIADO LITERAL** | sempre | parafrasear falhou em **7 de 28** frames (boca fechada) — leva AR 26/08 |
| **Prompt sem contradição interna** | sempre | descrição concreta vence regra genérica: `face-down` matou a tela ligada |
| **Palavras por cena (Veo 8s)** | **16** | acima disso o Veo acelera a fala e **a voz sai robótica** |
| Palavras por cena (Grok 10s) | 22 | idem, e a fala pode ser cortada no fim |
| **Tamanho do prompt (Veo/Kling/Runway)** | **< 2500 chars** | falha com "Serviço temporariamente indisponível" |
| **fps na montagem** | **o nativo do motor** (Veo = 24) | forçar 30 duplica frames → travadinho |
| **Concat** | filtro `concat`, nunca `-c copy` | áudio picotado nas junções |
| **Ordem do histórico do Hub** | **crescente** (índice 0 = mais antigo) | criativo montado de trás pra frente |
| Proporção | 9:16 | trocar de motor reseta pra 16:9 sem avisar |
| **Rosto em quadro em toda cena falada** | sempre | cena sem rosto sorteia **outra voz** — o criativo se denuncia |
| **Contagem do prop no prompt** | `exactly ONE ... stays in X` | o prop da imagem **duplica** na mesa |
| **Superfície escrita** | prop fixo + nunca "lê em voz alta" | o modelo **reescreve o papel** com a fala |
| **Imagem da cena de ação** | a variante do prop, nunca a base | o Veo **inventa cenário, figurino e óculos novos** na cena |
| **Acessório no CHARACTER** | só o que está na imagem | o objeto **brota no meio do criativo** e fica |
| **Corte de silêncio** | cabeça, cauda **e pausas internas** | sobra respiração; o criativo arrasta |
| **`ffmpeg` em laço** | `-nostdin` | come o stdin e corrompe os cortes em silêncio |
| **Duração de cada corte (formato multi-cena curto)** | **≥6s por cena**, não trim agressivo pra caber na VO | menos que isso lê como "corte nervoso/rápido demais" mesmo com velocidade normal — usuário reclamou em 2026-09-07 (3 vídeos "Detalhe" com corte ~4s cada) |
| **Mão manuseando roupa no prompt** | negar clipping e flutuação | sem isso a mão **entra dentro** do tecido ou a peça **flutua sem apoio** — adicionar `hand clipping through fabric, fingers penetrating garment, garment floating unsupported, garment defying gravity` no NEGATIVE |

Antes de aceitar um clipe, confirme que **sobrou respiro**: se
`silencedetect` não achar nenhum silêncio no fim, o texto estourou o tempo.

E antes de dizer que algo está pronto ou corrigido: **abra o arquivo.** Data de
modificação e um frame extraído. A falha mais cara do dia não foi de modelo — foi
reportar como feita uma correção que um script em background nunca executou.

## Regras que não se negociam

1. **Imagem sempre antes do vídeo.** Nunca texto→vídeo. Sempre Imagem→Vídeo.
2. **Todos os prompts em inglês** — GPT e Grok. Só a fala do personagem fica no idioma do criativo.
3. **Story 9:16 vertical** desde a imagem.
4. **Prompt de vídeo muito descritivo.** Cena vaga = vídeo genérico.
5. **A fala vai literal no prompt.** Sem o texto exato, a boca não bate com o áudio.
6. **Bloco anti-morphing em todo prompt de vídeo.** Sem ele nascem objetos do nada e dedos a mais.
6b. **Movimento sempre natural, e nada nascendo do nada.** Todo prompt de vídeo,
   sem exceção, leva as duas metades: no `ACTION`, micro-movimento humano
   contínuo (piscar, respirar, peso do corpo, ombros e cabeça acompanhando a
   fala, dedos com peso e atrito nas cenas de mão); no `CONTINUITY` + `NEGATIVE`,
   a lista fechada de objetos e a proibição de qualquer coisa surgir, sumir,
   duplicar, derreter ou deformar. Cena parada demais lê como boneco falante;
   cena com objeto brotando lê como IA. As duas queimam o criativo do mesmo jeito.
7. **Sem legenda na geração.** Legenda é pós-produção — queimada pelo modelo fica horrível.
8. **Só Grok.** É ilimitado na assinatura do Hub; os outros modelos consomem o pool geral.
9. **Orçamento de tempo antes de escrever as cenas.** Nunca some no fim.
10. **O Hub NÃO limpa o prompt nem a imagem entre gerações.** O texto da cena anterior fica no campo e a próxima cena sai gerada com ele, sem aviso nenhum. Limpe à mão e **confirme que zerou** antes de digitar — a sequência canônica está em `hub-video-playwright`.
11. **A cena de ação usa a imagem do estado que a fala dela descreve.** Gerar as
   imagens de prop e deixar toda cena apontando para a base é o mesmo que não
   tê-las gerado. Prove o vínculo com `bind.sh` (md5 da imagem da cena bate com
   uma imagem aprovada do próprio criativo) — inspeção a olho não conta.
12. **Só entra no CHARACTER o que está na IMAGEM.** Acessório escrito no prompt e
   ausente da foto (colar, brinco, terço) aparece do nada no meio do criativo.
13. **`gate.sh` antes de concatenar, e ele é bloqueante.** Três checagens por cena:
   RMSE frame 0 × imagem da cena < 0,16; rosto × mediana das outras cenas < 0,20
   (pega troca de set/figurino); `silencedetect` achou respiro no fim. Falhou
   qualquer uma, regera a cena — não monta.
14. **Nunca apague `CRIATIVO-*/VIDEO/cena-*.mp4`.** Sem os clipes-fonte, um defeito
   numa cena obriga a refazer o criativo inteiro.

---

## FASE 0 — Briefing

**Antes de decidir modo, cena ou fala: entenda o produto e quem compra.** Nunca
escreva a primeira linha de prompt de imagem, vídeo ou narração sem antes ler:

1. **A página de vendas** (`pagina/index.html` da oferta) — ela já carrega
   promessa, ângulo e **para quem fala** (comprador, não necessariamente usuário
   final), validados com o usuário antes de ir ao ar. É a fonte da verdade do
   projeto, não um detalhe a inferir depois.
2. **O entregável** (PDFs/imagens já gerados) — o que o comprador de fato recebe,
   pra demonstração usar conteúdo real (ver §E.0 mais abaixo).

Pular esse passo já custou caro: um criativo saiu com a narração falando
diretamente com o idoso ("vas a recibir", "tu equilibrio") num produto cujo
comprador real é o filho/cuidador — a própria página já usava
hijo/hija/papá/mamá, e ninguém checou antes de escrever. Ver §E.4 para a regra
completa de "a quem a narração se dirige".

**Se você é o orquestrador delegando essa skill pra um pane/subagente, o
prompt de spawn É o briefing.** Aconteceu de novo (2026-09-07): um pane
recebeu só caminho de arquivos de referência + "monte 1 criativo demonstrativo"
e produziu vídeo/imagem tecnicamente corretos mas sem ângulo de venda nenhum
— nunca soube produto, persona ou proposta, porque isso nunca chegou no
prompt de spawn. Passar arquivos não é briefing. Todo spawn pra essa skill
precisa incluir explicitamente: nome do produto, promessa/proposta real,
persona (pra quem fala), preço real, e a instrução de invocar esta skill
desde a FASE 0 — nunca pular direto pra "gere a cena X".

Só depois disso, decida o modo. Se não estiver claro no pedido, **pergunte**:

**Modo A — Criativo completo do zero.** Todas as cenas são geradas: hook, corpo,
oferta e CTA. **É o modo padrão desde 25/10/2026** (B/B2/C removidos — ver nota
abaixo). Toda dor/ângulo novo vira peça nova do zero, nunca reaproveitando body
de vencedor com variação de superfície.

> **⛔ Modo B, B2 e C REMOVIDOS (regra da dona, 25/10/2026).** Os três dependiam
> de reaproveitar o body de um vencedor trocando só o hook/gancho (matriz
> gatilho×ângulo do Kevones, ou "v2" com body variado). Confirmado em
> `criativo-ads/references/kevones-criativo.md` linhas 11-38: **o próprio Kevones
> abandonou essa lógica depois da Andrômeda** (out/2025) — o Meta passou a agrupar
> por IDEIA/CONTEXTO, não por superfície, então trocar gancho/voz/cor/matriz de
> abertura sobre o mesmo body é a variação rasa que ele hoje condena. O que ele
> ensina agora é **"um anúncio por dor/benefício"**: lista as dores do produto,
> 1 peça nova (gerada do zero, Modo A) por dor — é exatamente o que GATE 0.2 /
> MATRIZ ÚNICA de `criativo-ads` já fazem. A única variação de vencedor que ele
> ainda autoriza é o **"copo azul"** (mesmo produto+copy, troca quem/onde —
> `copo-azul-variacao-vencedor`), que é uma peça nova mesmo assim, não corte de
> hook sobre body velho.
>
> Se encontrar `HOOK/`, `CRIATIVO-N` com body reaproveitado, ou qualquer menção a
> "Modo B/C" em oferta antiga: é legado, não reproduzir o padrão numa leva nova.

**Modo D — Modelagem de escalados.** A leva não nasce de briefing nem de vencedor
próprio: nasce de um **formato que já está escalando na conta de outra pessoa**, com o
arquivo real anexado como referência. Existe uma biblioteca local de 103 formatos
(87 estáticos, 16 vídeos, 47 categorias) em `~/.claude/biblioteca-escalados`.

Quem conduz esse modo é a skill **`modelagem-escalados`** — leia-a antes de qualquer
coisa. A divisão é:

| | `modelagem-escalados` | esta skill |
|---|---|---|
| Estático | pipeline inteiro (01→12) | não entra |
| Vídeo | decupa o formato e devolve o briefing (prompt `11`) | produz: imagem → vídeo → QA → montagem |

Fluxo de vídeo no Modo D:

1. `scripts/buscar.sh --tipo video` na skill `modelagem-escalados` lista os 16 formatos;
   13 têm transcrição `.txt` ao lado do arquivo.
2. Prompt `11` decupa o vídeo escalado em blocos (hook / agitação / mecanismo / prova /
   oferta / CTA), acha o corte de atenção e nomeia o mecanismo do hook.
3. O briefing que sai dali entra aqui como **Modo A**, já com persona, ângulo e
   falas por cena. Todas as regras desta skill continuam valendo — 16 palavras por cena
   no Veo, rosto em quadro, bloco de dentes, anti-morphing.

Regra que não muda no Modo D: **modela-se o mecanismo, não o produto.** Pessoa, marca,
logo, prova e número da referência não sobrevivem à adaptação. Sem depoimento real no
briefing, formato de prova social não entra.

**Modo E — Vitrine Guiada (b-roll de banco + demonstração do entregável + guia
falante, MISTURADOS no mesmo criativo).** Nenhuma cena de mundo real é gerada por
IA. O criativo é montado com quatro fontes que já existem ou já foram geradas
antes (imagem do entregável, ver FASE 0/§E.0), e a única coisa que pode ser gerada
agora é a pessoa que fala (ou nem ela, quando é só narração).

⚠️ **PADRÃO VALIDADO (Receita Aprovada Tarot, 2026-09-23):** O modo demonstrativo
segue o padrão **b-roll + gravação de tela/entregável + VO + legenda karaokê,
SEM tarja vermelha, SEM geração de pessoa por IA**. Ver seção **E.2b** para receita
completa e detalhes de estrutura, layout, regras que funcionaram.

| Camada | Fonte | Para que serve |
|---|---|---|
| **B-roll** | banco público (Pexels, Pixabay, Coverr, Mixkit) e Pinterest | contexto e dor: cenas do mundo do comprador que o acervo próprio não tem |
| **Demonstração do entregável** | gravação de tela ou mão apontando página real (§E.2 ou §E.0) — o material físico/mockup do produto | prova principal em produto PDF/guia: mostra exatamente o que o comprador recebe |
| **Tela** | gravação do próprio produto em modo mobile no DevTools (§E.2) | prova em produto navegável (portal, app, área de membros) — alternativa à demonstração acima, não soma com ela no mesmo criativo salvo casos específicos |
| **Guia** | personagem falante (imagem→vídeo, pipeline normal desta skill, ou UGC de leva anterior — nunca com áudio trocado, ver §E.6) ou só narração off | conduz, promete e chama pra ação; editado com as outras camadas via Meio a meio ou PiP (§E.3) |

**As quatro camadas não são modos separados — são um kit.** Um único criativo pode
abrir com b-roll (dor), passar pra demonstração do entregável (prova via gravação
de tela ou visual), voltar pro b-roll (contexto), e fechar com o guia falando em
PiP ou VO sobre a demonstração (CTA). A composição cena a cena decide qual camada
entra onde — não existe regra de "este criativo é só b-roll" ou "este é só
demonstração"; cada cena usa a fonte que prova melhor aquela frase do roteiro.

Use quando: o produto é **digital e navegável** (site, área de membros, catálogo,
app) — a tela real vende mais que qualquer cena inventada; ou quando o b-roll do
nicho existe pronto em banco e gerar aquilo por IA seria pagar caro por pior; ou
quando o produto é um PDF/guia e a prova mais forte é ele mesmo, físico, na mão.

**Inspiração de estrutura vem da biblioteca de escalados também — sempre olhe
antes de inventar o corte.** `~/.claude/skills/modelagem-escalados/scripts/buscar.sh
--tipo video` lista os 16 formatos de vídeo já escalados, por categoria:

| Categoria | Qtd | Corresponde a |
|---|---|---|
| UGC (verde, tela dividida, expert reagindo) | 7 | Meio a meio / Miniatura-PiP |
| Tela dividida | 2 | Meio a meio |
| Antes e depois (com tela dividida) | 2 | Meio a meio |
| Tela verde | 1 | Miniatura-PiP (fundo composto) |
| POV em Vídeo | 1 | Print + POV + Meme, sem meme físico — só POV+prova |
| Identificação | 1 | Tela cheia |
| Animação 3D | 1 | fora do escopo do Modo E |
| Estilo stories | 1 | Tela cheia, ritmo de story nativo |

Não é o Modo D (que decupa um vencedor específico e vira briefing formal): aqui
é consulta rápida de referência validada, e entra em **dois momentos, não só
um**:

1. **Antes de pensar em como vai ser o criativo** — primeiro passo, antes de
   decidir estrutura, persona ou ângulo. Busca referência validada primeiro,
   inventa depois em cima do que já funciona; nunca o inverso.
2. **Antes de montar** (FASE 7, já com os clipes/imagens prontos) — confere se
   o layout escolhido pra edição (Meio a meio, PiP, Tela cheia, Print+POV+Meme)
   ainda bate com o formato de referência, porque decisão de montagem muda
   depois de ver o material pronto: às vezes o corte planejado não sobra tempo
   pro layout que virou referência, e é melhor trocar de layout do que forçar.

Rode a busca **de qualquer ponto do processo**, sempre que o corte ou a
montagem do criativo estiver em dúvida — nenhum arquivo da biblioteca entra na
peça final, é referência de estrutura, não material.

**Cuidado ao ler a referência: o que é edição não vira prompt de vídeo.** O
formato escalado mostra o resultado **já montado** (split, PiP, faixa, corte).
Isso é decisão de pós-produção — mesma regra do começo desta seção (## Regra de
voz/rosto, "Modos de edição"). Ao escrever o roteiro a partir de uma referência,
separe sempre os dois: o que o **guia fala e faz** (vira prompt de vídeo,
gerado em quadro cheio, normal) e o **layout que a referência usa** (vira nota
de edição, aplicado depois no clipe pronto). Copiar a montagem da referência
pro prompt do Veo ("cena dividida ao meio", "tela no canto") é o erro que gera
clipe quebrado — o modelo tenta desenhar a divisão dentro da própria imagem.

### E.0 — Modo padrão é DEMONSTRATIVO, UGC só se pedido

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

**Checklist que vale pra qualquer peça com o entregável dentro** (cada item já custou uma versão
reprovada):
- **1 clipe/take por frase da VO**; nenhum take nem b-roll repetido na mesma peça; peças irmãs da leva
  usam b-rolls diferentes.
- **Página real full bleed**, sem moldura e sem tarja, na sequência do início ao fim; cortar barra de
  status/URL antes de compor.
- **B-roll com o assunto no quadro**, cover 1080×1920 (cortar borda preta embutida), origem registrada
  pela `get-brolls`.
- **Cortes de 1,5-3 s**, transição ~0,3 s, **sem aceleração** por padrão (playbackRate 1.0).
- **Legenda karaokê** por cima: 70% (62-64% no split), sem palavra encostando/sobrepondo; gancho em
  **até 2 frases curtas** — 3-4 frases de dor antes do produto = reprovado.
- **Vários takes do entregável**, não um take único rolando a página.
- Nunca mockup 3D, nunca "PDF" na fala, nunca tarja vermelha; trilha **-18 a -22 dB**.
- **Carrossel:** card 1 é a única arte gerada; os demais são páginas reais recortadas em sequência.
- **QA antes da dona ver:** contact sheet 1 fps, `cropdetect` em cada b-roll, frames a cada 0,5 s na
  legenda, F0 da voz antes×depois.

### E.1 — Coleta do b-roll

**Todo b-roll mostra o ASSUNTO do produto no quadro — e só entra clipe ENTREGUE pela
`get-brolls`.** Erro real (Mapa do Tarot, 2026-09-23): o projeto get-brolls só rodou
`search`, nunca review/entrega; um pane baixou clipes à mão com queries genéricas
("hand writing journal", "book pages flipping") e o criativo saiu com pessoa escrevendo
numa poltrona e livro abrindo em leque — nenhuma carta de tarô. Dono: "não tem nada a
ver com o assunto". Regras:
- Toda query e todo `target` do BRIEF carregam o objeto do nicho explícito
  (`tarot cards spread on table hands`, não `hand writing journal`). Palavra genérica
  (book, journal, writing, pages) sem o objeto do nicho = clipe genérico garantido.
- No review, rejeite candidato em que o objeto do nicho não aparece no quadro.
- Pasta `raw/` baixada fora da skill não entra na montagem sem passar por review e
  registro de origem/licença. Delegou? Escreva isso no prompt do pane.
- B-roll em tela cheia = `object-fit: cover` real no 1080×1920. Clipe horizontal
  encaixado sem cover vira letterbox com barra preta (v7 Imperatriz: conteúdo só em
  y 440–1480). QA: `ffmpeg -vf cropdetect` em cada bloco de b-roll tem que dar 1080:1920.
- Nenhum clipe (nem outro trecho do mesmo clipe) aparece duas vezes no criativo. Faltou
  clipe: alonga o anterior ou busca outro.
- B-roll sempre `muted` no Remotion — o único áudio é a VO. (Louco v7: áudio original do
  clipe vazou por baixo da narração.)
- Clipe tem que ter duração útil ≥ slot. Mais curto, o Remotion segura o último frame e a
  cena "trava" (Louco v7, 25.8–27.1s e 27.5s–fim). QA: `ffmpeg -vf
  "freezedetect=n=0.003:d=0.4" -f null -` no final = zero freeze.

**Os termos de busca saem do que você entendeu do produto e da persona na FASE
0, não de achismo na hora de buscar.** Se o comprador é o filho/cuidador de um
idoso (ver FASE 0/§E.4), o b-roll certo mostra a cena pela ótica dele — um
adulto cuidando/visitando um idoso, não só "elderly exercising" genérico.
Releia a página de vendas antes de montar a lista de termos; ela já diz qual é
a dor e o contexto visual que vende.

Busca **sempre em inglês**, mesmo pra nicho brasileiro: o acervo indexado em
português é uma fração do inglês. `rural blacksmith welding`, não `ferreiro
soldando`. Baixe 3–4 clipes que fazem sentido pro roteiro, não os 3–4 primeiros
bonitos.

- Perfil de browser dedicado: **`pinterest`** (`~/.agent-profiles/pinterest`,
  registrado em `registry.conf`). Pinterest exige login pra ver vídeo; sem perfil
  persistente cai no muro de cadastro a cada sessão.
- Prefira o banco público ao Pinterest quando o clipe existir nos dois: licença
  limpa (Pexels/Pixabay/Mixkit/Coverr liberam uso comercial sem atribuição).
  Pinterest é **descoberta**, não fonte — o pin quase sempre reaponta pra origem;
  baixe da origem.
- **Correção (dona, 25/10/2026): Pinterest É fonte direta válida, não só descoberta, quando o
  conteúdo é ESTILIZADO/3D** (render 3D de exercício/anatomia, animação, ilustração) — é onde o
  banco público costuma faltar (ver `OFERTAS/luciola-atlas-movimiento/STATUS.md`, "B-roll externo
  resolvido 12/10": os 5 clipes 3D do Atlas vieram de busca direta no Pinterest em inglês, não de
  banco público). **Divisão de fonte por tipo de conteúdo:** Pinterest = 3D/estilizado/render;
  TikTok = orgânico/viral (cena real, não encenada); YouTube = secundário (geralmente pior
  qualidade/mais clichê que os outros dois, usar só quando os outros não têm). Buscar sempre em
  inglês nos três.
- Nunca use clipe com marca, logo, rosto reconhecível de celebridade ou legenda
  queimada. Corta o anúncio no review da Meta.
- **TikTok também é fonte — dupla função (buraco fechado 2026-09-09).**
  1. **Sinal de demanda:** vídeo viral sobre o tema/dor da oferta é a mesma
     leitura que "comentário recente no YouTube" (complemento de demanda do método, ver `low-ticket-metodo-mvt` mineração) — visualização e comentário alto e recente = gente
     querendo aquilo agora. Busque pelo termo da persona/dor antes de decidir
     que "não tem demanda".
  2. **Fonte de b-roll:** cena TikTok que faz sentido pro roteiro (mesma regra
     de nunca usar marca/logo/rosto de celebridade/legenda queimada — corte
     esse trecho ou descarte o clipe) pode virar b-roll, do mesmo jeito que
     Pinterest é descoberta e você baixa da origem quando possível.
  3. **Download:** `yt-dlp` baixa TikTok direto por URL, sem precisar de perfil
     logado pra vídeo público (`yt-dlp <url> -o saida.mp4`). Só precisa de
     conta/perfil de browser dedicado se o conteúdo estiver atrás de
     idade/restrição — nesse caso, mesma lógica dos outros perfis persistentes
     do projeto (criar um perfil dedicado, não usar conta pessoal).
  4. Padronize igual aos outros: 9:16 (já nasce assim na maioria), sem áudio
     original, cortar qualquer selo/UI do TikTok (relógio, @usuário, ícones de
     like/comentário) antes de usar — nunca deixa a chrome do app original
     visível no criativo final.
- Padronize antes de montar: 9:16, mesmo fps do resto, sem áudio original
  (`-an`) — a trilha e a narração são únicas pro criativo todo.
- **Se achar fácil, cena de gente usando algo parecido com o produto ajuda**
  (mão folheando papel numa mesa, gente manuseando peça, cliente recebendo
  objeto) — o comprador se vê fazendo aquilo, mais forte que ambiente vazio.
  Mas é ganho oportunista, não meta: não trave a busca de b-roll tentando achar
  esse tipo específico. Cena de ambiente/ferramenta parada (banco tem de sobra)
  resolve o criativo sozinha na maioria das vezes.

### E.2 — Gravação de tela em modo mobile

O produto navegado por dentro, gravado com o DevTools em device emulation
(iPhone/Android, 9:16 nativo), não o desktop redimensionado — barra de rolagem e
hover de mouse denunciam desktop e quebram a leitura de "isso é o app no meu
celular".

**Comando (`agent-browser`) — nunca gravar sem setar o device antes, senão sai
em resolução de desktop:**

```bash
agent-browser --session <sessao> set device "iPhone 16 Pro"   # NÃO --device (isso é o provider iOS)
agent-browser --session <sessao> navigate "<url do produto>"
agent-browser --session <sessao> record start "<saida.webm>"
# ... ações reais: scroll, clique em link/card/botão real da UI ...
agent-browser --session <sessao> record stop
```

Sai em ~1080×2340 (3x DPR do device), não exatamente 9:16 — normalize na
montagem: `scale=1080:-1,crop=1080:1920:0:0` (ou pad, se preferir não cortar).

#### Demonstração obrigatória do entregável digital

Quando o produto tiver portal, área de membros ou arquivos navegáveis, a gravação
precisa provar a entrega real — não basta rolar a landing page:

1. Mostre rapidamente a tela de login e a entrada pelo e-mail da compra.
2. Nunca deixe um e-mail completo legível. Use uma conta fictícia e mantenha o campo
   desfocado, coberto ou mascarado com asteriscos; na área logada, exiba algo como
   `cl******@dominio.com`.
3. Passe pela visão geral do produto e por **cada seção entregue**, incluindo todos os
   bônus. Mostre pelo menos um detalhe interno de cada seção, não apenas o cartão/capa.
4. Faça cliques reais: abra um material, mostre seu conteúdo, volte ao portal e siga
   para o próximo. O corte final pode acelerar transições, mas cada seção precisa ser
   reconhecível em quadro.
5. Grave em device mobile real e enquadre para o texto importante continuar legível
   depois do crop 9:16. Sem cursor de desktop, hover ou rolagem horizontal.

Gate antes da montagem: revise quadro a quadro procurando e-mail, nome, token, pedido
ou dado pessoal completo. Se aparecer, masque na interface ou na pós antes de exportar.

**Grave clicando de verdade, não só rolando.** `viewport <w> <h>` muda só o
tamanho da janela — continua desktop, sem media query mobile, sem toque. Só
`set device` ativa o user-agent e o layout mobile reais. Uma gravação que só
rola a página sem nenhum clique prova menos que uma que abre uma ficha/card de
verdade — o produto sendo *usado*, não só *visto*, é a prova que o Modo E
promete.

- Movimento **lento e intencional**: rolagem contínua, pausa em cima do que
  importa, um clique por bloco. Rolagem nervosa é o erro mais comum e ilegível em
  quadro pequeno.
- Grave mais do que precisa e corte depois; regravar sincronizado com a narração
  custa mais que cortar.
- Zero dado pessoal, e-mail, token ou nome real de cliente em quadro.

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
- Final acelerado 1.15x no Remotion (ver "Acelerar é padrão").
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

### E.3 — Edição: os dois arranjos

Os dois arranjos existem no mesmo criativo, alternando. É essa alternância que
segura a atenção.

**Meio a meio (split 9:16).** Tela em cima, pessoa embaixo (ou o inverso). Use
enquanto a fala **descreve o que a tela mostra** — os dois canais dizem a mesma
coisa ao mesmo tempo e a prova entra sem interromper a fala.

**Foco alternado (PiP).** A pessoa começa em quadro cheio falando. Quando a fala
vira "olha aqui dentro", ela **encolhe pra miniatura no canto** e a tela toma o
quadro rolando por dentro. No CTA ela **volta ao foco** em quadro cheio.

Regra do arranjo: **quem está em quadro cheio é quem está carregando a
informação naquele segundo.** Personagem grande enquanto a tela mostra o que
importa é desperdício dos dois lados. A transição entre arranjos é escala
animada em ~0,3s, nunca corte seco — corte seco na troca de tamanho lê como bug.

Miniatura: canto inferior, ~28–32% da largura, cantos arredondados, sem borda
grossa. Menor que isso o rosto some no feed; maior, briga com a tela.

**Onde montar:** composição **Remotion** — cada cena/gravação é um `<OffthreadVideo>`
dentro de `<Sequence>`; a troca quadro cheio → miniatura é `interpolate`/`spring`
de escala e posição em ~0,3s (9 frames a 30fps, 7 a 24fps); a borda esfumaçada do
meio a meio é `maskImage: linear-gradient(...)` na camada de cima. Ver
`remotion-best-practices` / `remotion-multimedia`. Hyperframes serve igual
(`hyperframes-*`), quando o criativo já vai ter motion elaborado lá. O fps da
composição é o nativo do motor (ver FASE 7), não 30 por hábito. Não testado ainda
como template pronto desta skill: o primeiro criativo que usar, salve a composição
em `references/` pra reaproveitar.

**Referências reais de composição, 4 exemplos salvos** (2026-09-09) em
`references/composicao-tela-dividida/` — cobrem a variação que existe na
prática, além do que já ia descrito acima:

| Arquivo | Arranjo | Leitura |
|---|---|---|
| `exemplo-1-hook-meio-a-meio-blur.png` | Meio a meio, pessoa em cima, tela embaixo | Corte **NÃO é linha reta** — borda entre as duas camadas é esfumaçada/borrada (gradiente), não um corte seco de pixel. Legenda em destaque ("GREW UP" em vermelho) sentada bem na costura. |
| `exemplo-2-meio-a-meio-pessoa-baixo.png` | Meio a meio invertido, tela em cima, pessoa embaixo | Mesma borda esfumaçada; prova que a ordem (pessoa cima/baixo) é livre — decide pelo que a fala está descrevendo naquele segundo, não por regra fixa de posição. |
| `exemplo-3-split-corte-seco-play.png` | Split 50/50, linha reta (corte seco) | Ao contrário do E.3 acima: **corte seco na linha do split TAMBÉM é válido** quando o estilo é "demonstração de app/tela" — ícone de play sobreposto reforça que aquela metade é conteúdo navegável, não B-roll comum. Use linha reta quando quiser deixar claro "isto é uma tela", esfumaçado quando quiser fusão mais orgânica (b-roll/produto físico). |
| `exemplo-4-miniatura-pip-canto.png` | Miniatura/PiP, mas SEM o círculo perfeito da regra acima | Rosto pequeno com ícone de play ao lado — variação do PiP que sinaliza "isso é um vídeo dentro do vídeo", útil quando a demonstração em si parece um card/resultado de busca (ex: catálogo, feed).

**Ordem não é fixa.** Nenhuma regra obriga "hook em quadro cheio → split → CTA
em quadro cheio" como sequência única. O hook pode nascer já em split (exemplo
1/2) se a informação da tela já for a prova do hook; guarde o quadro cheio pra
quando a pessoa precisa carregar sozinha a atenção (identificação, CTA).

**Legenda nos exemplos:** texto bold, branco/amarelo claro, com 1 palavra-chave
em vermelho/destaque, tamanho médio (nunca ocupando mais que ~2 linhas curtas),
sentada na costura do split quando existe, ou no terço inferior quando é
quadro cheio/PiP. Isso é a MESMA regra da legenda de fala (branca, caixa viva
960×1270) — a diferença é que aqui é call-out/manchete, não transcrição da fala.

### E.4 — Narração e trilha

**A quem a narração se dirige sai de QUEM COMPRA, não de quem USA o produto.**
Caso real (equilibrio-seguro-60): a narração falava na segunda pessoa como se o
próprio idoso estivesse comprando ("vas a recibir", "tu equilibrio") — mas em
nicho de idosos/terceira idade, saúde do idoso, cuidados especiais, quem decide
e paga quase sempre é o filho/filha ou cuidador, não o idoso. Falar como se o
idoso fosse o comprador erra o alvo da dor: o gatilho de quem cuida é
preocupação/culpa/responsabilidade pelo bem-estar de outra pessoa, não
autocuidado.

Antes de escrever a narração de qualquer criativo, pergunte **quem decide a
compra**, não só quem usa o produto:

| Nicho | Quem usa | Quem decide/paga | Narração fala com |
|---|---|---|---|
| Guias/produtos pra idosos | o idoso | filho(a), cuidador(a) | o cuidador — "para tu papá/mamá", nunca "para ti" no idoso |
| Material infantil/escolar | a criança | pai/mãe | o responsável |
| Produto pet | o pet | o dono | o dono |
| Produto B2B de uso técnico | o operador | quem compra na empresa | quem decide a compra, se for diferente de quem usa |

Regra prática: se usuário final e comprador são pessoas diferentes, a narração
(e a matriz persona×ângulo×oferta da FASE 1) é escrita **para o comprador**,
descrevendo o benefício pela ótica dele ("dá tranquilidade pra você saber que
ele está seguro"), não pela ótica de quem usa.

**Gênero da voz sai do nicho, não do gosto.** Nicho tocado majoritariamente por
homens (serralheria, mecânica, pesca, obra) → voz masculina. Nicho majoritariamente
feminino (cozinha, artesanato, maternidade, beleza) → voz feminina. Voz fora do
nicho lê como anúncio de fora, não como alguém de dentro. Na dúvida, teste as duas
como variação — teste as duas em peças diferentes da leva.

A narração é gerada pela skill **`narracao-hub-tts`** (API do NinjaVoice, sem
browser, 82 vozes, pt-BR nativo, WAV síncrono). Invoque-a, não reescreva a
mecânica aqui. Escolhida a voz do projeto, ela não muda entre cenas.

### GATE FINAL — obrigatório antes de chamar qualquer vídeo de "pronto"/"final"

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

### Upload pro Drive: só o arquivo final, e nunca sem a pasta Kalodata

- **Só sobe o `*-final.mp4`** pra pasta `1 - FEED (postar)/` — nunca clipe de cena
  solto, TMP, ou intermediário sem trilha/aceleração.
- **Toda pasta datada de produto leva a pasta `0 - Pesquisa Kalodata/`** com
  `kalodata-metricas.png` + `link-kalodata.txt` daquele produto (já existem em
  `PRODUTOS/<produto>/` — copie de lá, nunca esqueça ao criar pasta nova no Drive).
- **Padrão fixo desde 09/09/2026: além da métrica, sempe inclua o print da
  TELA DE DETALHE DO PRODUTO no Kalodata** (`/product/detail?id=...`, a página
  que mostra foto, preço, categoria, avaliação e "Principais métricas" —
  não o card de ranking da busca). É esse print + o link dessa URL de detalhe
  (não o link genérico `/product` de busca) que o usuário usa pra se afiliar.
  Nomeie `"<Produto> - detalhe produto Kalodata.png"` e salve junto do
  `metricas Kalodata.png` na mesma pasta `0 - Pesquisa Kalodata/`.
  **Como achar o link de detalhe certo:** Hub -> `/tools` -> busca "kalodata"
  -> clica no card -> escolhe a conta certa (abre aba nova autenticada,
  `kalodata2.*`=Conta 1, `kalodata3.*`=Conta 2) -> aba `Produto` -> busca pelo
  nome exato do produto (da `ficha.md`) -> clica no resultado que bate (nome +
  preço + `id` batendo com o Cover CDN salvo em `link-kalodata.txt`) -> a URL
  vira `/product/detail?id=<id>&...` — é essa que entra no `link-kalodata.txt`
  e no `links-kalodata.txt` consolidado do Drive, substituindo qualquer link
  genérico de busca/ranking que estava lá antes.

**Trilha sempre.** Narração seca sobre gravação de tela soa como tutorial de
suporte técnico. Regras da trilha:

- Instrumental, sem letra — letra briga com a narração pelo mesmo canal.
- Coerente com o nicho e com o gatilho: rural/oficina pede algo seco e ritmado,
  não épico de trailer; e trilha alegre não entra em criativo de dor.
- **−18 a −22 dB abaixo da voz.** Se você percebe a música, está alta demais.
- Uma trilha por criativo, contínua do primeiro ao último frame — trocar de
  música no meio parece emenda de dois vídeos.
- Banco livre de royalties (Pixabay Music, Mixkit, Free Music Archive).
  Nunca música comercial: derruba o anúncio por direitos.

### Baixar a trilha do Pixabay Music — `WebFetch` NÃO pega o link de áudio

O player do Pixabay Music carrega a faixa via JS só depois do clique em play; a
página estática (o que `WebFetch` lê) não tem nenhum `<audio>`/`.mp3` no HTML.
Testado: `WebFetch` na página de busca devolveu "nenhum link .mp3 encontrado"
mesmo com dezenas de faixas listadas visualmente.

Correção — abra num browser real, clique o overlay de play da faixa, e o
`<audio>` aparece no DOM com o `src` direto do CDN (`cdn.pixabay.com/audio/...`),
baixável por `curl` sem sessão/cookie:

```bash
~/.claude/bin/browsers.sh gratuito                     # ou qualquer perfil livre
agent-browser --session gratuito navigate "https://pixabay.com/music/search/genre/pop/"
agent-browser --session gratuito eval "(() => {
  const btns = Array.from(document.querySelectorAll('button'));
  const play = btns.find(b => b.className.toLowerCase().includes('play'));
  play.click(); return 'clicked';
})()"
sleep 2
agent-browser --session gratuito eval "(() => Array.from(document.querySelectorAll('audio,source')).map(a=>a.src||a.currentSrc).filter(Boolean))()"
# -> ["https://cdn.pixabay.com/audio/2026/06/04/audio_xxxxxxxxxx.mp3"]
curl -sL "<url>" -o trilha.mp3
```

Troque `/genre/pop/` pelo gênero/mood do nicho (`/search/mood/calm/`,
`/genre/cinematic/` etc.) — a mecânica do clique é a mesma.

**Baixe um BANCO de faixas variadas, não uma só.** Usar a mesma trilha em todo
criativo da leva é o mesmo erro de "todos os hooks abrem igual" (ver FASE 1,
teste de similaridade) — só que no áudio. Navegue por **vários gêneros
diferentes** (`pop`, `corporate`, `acoustic`, `lofi`, `rnb`, `cinematic`...),
uma faixa de cada, e salve num banco reusável por nicho:

```
<PROJETO>/_ASSETS/trilhas/<genero>.mp3
```

**Cada `navigate` pede sleep de ~3s antes do clique** — o Pixabay é SPA e o
componente do player pode não ter re-renderizado ainda; clicar cedo demais
retorna o `src` da faixa anterior sem erro nenhum (parece ter funcionado, mas
é a mesma URL de antes). Confirme que a URL mudou antes de seguir pro próximo
gênero — se repetiu, aumente o sleep e tente de novo.

Na montagem, **sorteie/alterne a faixa por criativo** (ex.: `pop` no provador,
`corporate` no detalhe, `acoustic` no pov) — nunca a mesma faixa em todos os
formatos do mesmo produto, e nunca repita a mesma faixa em produtos vizinhos
da mesma leva.

### Nível real do mix — meça, não chute

(Mix narração+trilha continua no ffmpeg de propósito: os ganhos abaixo foram
calibrados de ouvido em produção. Se a trilha for pra dentro de uma composição
Remotion/Hyperframes, leve os MESMOS ganhos (`volume` do `<Audio>` / `data-volume`)
e confira com o `volumedetect` do mesmo jeito. Não use `hyperframes normalize-audio`
aqui: ele IGUALA a loudness da trilha à da narração, o oposto do que o mix pede.)

`-18 a -22dB` como ponto de partida genérico **não bate** com o que soa bem na
prática: testado em produção e ainda saiu alto demais / narração baixa demais.
O que funcionou depois de calibrar por ouvido:

```bash
ffmpeg -i vo.mp4 -i trilha.mp3 -filter_complex \
  "[0:a]volume=2.2[v0];[1:a]volume=-38dB[m];[v0][m]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[aout]" \
  -map 0:v -map "[aout]" -c:v copy -c:a aac final.mp4
```

- **`normalize=0` é obrigatório no `amix`.** Sem isso o filtro reduz os dois
  canais pela metade automaticamente, e o resultado depende de quantos inputs
  existem — o `-20dB` de um teste não soa igual ao `-20dB` de outro. Com
  `normalize=0`, os ganhos (`volume=`) são os únicos que decidem o nível.
- **Narração ganha `volume=2.2`** (sobe ~+7dB) antes de mixar — sem isso ela
  fica baixa demais perto da trilha mesmo com a trilha atenuada.
- **Trilha em `-38dB`**, bem mais baixo que o `-18/-22dB` da orientação
  genérica — meça de ouvido a cada leva nova, o valor certo varia com a
  loudness da faixa escolhida (uma faixa mais "cheia" precisa de mais corte).
- **Confirme com `volumedetect`, não só de ouvido:** compare o `mean_volume`
  do vídeo final contra o da narração sozinha — se subiu muito (>2-3dB), a
  trilha está competindo.

```bash
ffmpeg -i narracao.wav -af volumedetect -f null - 2>&1 | grep mean_volume
ffmpeg -i final.mp4 -af volumedetect -f null - 2>&1 | grep mean_volume
```

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

## FASE 1 — Conceito e orçamento de tempo

### Conceito = PERSONA × ÂNGULO × OFERTA

A Meta hoje não persegue o público que você definiu: ela **lê o criativo**,
interpreta a mensagem e vai buscar o público a partir dela. Consequência direta
para quem cria: **volume de criativos não é diversidade criativa**. Cem anúncios
dizendo a mesma coisa alcançam o mesmo bolsão, o alcance incremental cai e o
funil colapsa.

Um **conceito** é a junção de três variáveis. Mudou uma, é conceito novo e
desbloqueia um bolsão diferente:

| Variável | O que muda de verdade |
|---|---|
| **Persona** | quem fala e para quem — idade, sexo, papel (a própria pessoa, a filha, o marido, o cético) |
| **Ângulo** | a ideia central — dor pura, prova social, desmistificação, curiosidade mecânica, comparação social, urgência |
| **Oferta** | a promessa e o formato — que dor resolve, teste grátis vs. diagnóstico vs. consulta, preço, garantia |

Antes de escrever qualquer prompt, monte a **matriz de conceitos** da leva: uma
linha por criativo, com persona, ângulo e oferta preenchidos. Se duas linhas só
diferem no `look`, elas são o **mesmo conceito** com roupa diferente — corte uma.

### Teste de similaridade — faça ANTES de gerar, não depois

Escreva as falas dos hooks lado a lado e conte:

- **Território semântico:** no máximo **1 a 2 criativos** por território. Se
  metade dos hooks aterrissa na mesma ideia central (por mais diferentes que sejam
  as cenas), são vários anúncios que a Meta lê como um só.
- **Palavra-chave repetida:** se a mesma expressão central aparece em quase todos
  os hooks, a mensagem é a mesma por mais diferentes que sejam as cenas.
- **Promessa:** quantas promessas distintas existem na leva? Se é uma só, a leva
  inteira é um conceito.

```bash
# conta a repetição da ideia central nas falas dos hooks da leva
grep -h "exact words\|says exactly" */HOOK/PROMPTS/*.txt | tr A-Z a-z | grep -c "<palavra-central>"
```

### Ficha de cada criativo

- **Persona, ângulo e oferta** — os três, explícitos
- **Público** — quem exatamente
- **Look** — ambiente, paleta, tipo de luz, hora do dia. Visualmente diferente dos outros e do body.
- **Primeiro frame** — o que aparece no segundo zero. Se dois criativos abrem igual, um deles está sobrando.

### Ao ler resultado: não mate criativo por ROAS isolado

A Meta faz remarketing automático — mostra mais de um anúncio seu para a mesma
pessoa até converter. Por isso é comum o criativo que **abre caminho** (primeiro
contato) ficar com ROAS feio enquanto alimenta os que fecham. Pausar ele por
métrica isolada derruba a campanha inteira. Avalie por resultado de campanha e
alcance incremental, não anúncio a anúncio.

### Orçamento de tempo — faça ANTES de escrever as cenas

O Grok só entrega **6s ou 10s** por clipe, e o corte de silêncio come 20-30% de cada um. Planeje com o líquido:

| Motor | Clipe | Líquido após cortar silêncio | Palavras (2,5 pal/s) |
|---|---|---|---|
| **Veo 3.1** (padrão) | **8s** | ~6 a 7s | **até 20** |
| Veo 3.1 | 6s | ~4 a 5s | até 15 |
| Grok (fallback) | 10s | ~7 a 8s | até 25 |
| Grok (fallback) | 6s | ~3 a 4s | até 15 |

No fluxo padrão (Veo, 8s por cena), **escreva cada fala com no máximo 20 palavras**.
Um criativo de **4 a 5 cenas** fecha em ~28 a 35s de líquido — 5 cenas quando o
território precisa de um bloco extra de prova ou objeção antes do CTA; não force
a 5ª cena só para preencher tempo.

Combinações prontas:

- Hook de **8-10s** → um clipe de 8s no Veo
- Hook de **12-14s** → 8s + 6s
- Hook de **16s** → 8s + 8s
- Criativo completo de **~30s** → 4 clipes de 8s (o padrão desta skill)

Depois distribua a **fala** dentro do orçamento: **~2,5 palavras por segundo de líquido**. Se o texto não couber, corte o texto — nunca estique o clipe.

### Conte as palavras de CADA cena antes de gerar — é gate, não sugestão

Fala que não cabe no clipe **não** faz o modelo acelerar a voz. Ele deixa o áudio
correr além da animação, e o resultado é **a boca parada com a voz tocando por
cima** — defeito que só aparece assistindo, e que não tem conserto na pós.

Orçamento real, contando o `Pace` que você escreveu no `VOICE`:

| Clipe | Pace 2.5 pal/s | Pace 2.2 pal/s |
|---|---|---|
| 6s | ~15 palavras | ~13 palavras |
| 10s | ~25 palavras | ~22 palavras |

```bash
# conta as palavras da fala de todas as cenas de uma vez
for f in PROMPTS/vid-cena-*.txt; do
  w=$(grep -oP 'exact words: "\K[^"]+|says exactly: "\K[^"]+' "$f" | wc -w)
  printf "%s: %s palavras%s\n" "$f" "$w" "$([ "$w" -gt 25 ] && echo '  <-- ESTOURA')"
done
```

**Se estourou, corte o texto. Nunca estique o clipe.**

Atenção especial ao **último bloco**: é onde se empilha oferta, preço, brinde e
garantia, e é por isso que ele estoura. Numa leva real, 7 de 9 criativos tinham a
cena 4 acima do teto (uma com 34 palavras para 22 de orçamento) — todos escritos
sem contar. Corte a repetição antes de cortar conteúdo: "na primeira compra",
"em PDF", e dizer "sem renovação automática" logo depois de "não renova sozinho"
são gordura que sai sem perder argumento.

### CTA no corpo do roteiro: o "é grátis" abre a frase, não fecha

Esta seção vale para a objeção dentro do corpo (cena de prova, oferta). **No fecho
final a regra é outra: só o comando, sem condição** (ver a seção abaixo). A
objeção que trava o clique é **preço**. Se ela só cai no fim, o espectador já
decidiu sair antes de descobrir que não custa nada. Derrube a objeção primeiro
no corpo, depois mande a ação.

```
Es gratis: tocá el botón acá abajo y descubrí tu número maestro ahora.
```

Não:

```
Tocá el botón, descubrí el tuyo, es gratis.        ← grátis chega tarde demais
```

Padrão: **`<é grátis> : <comando> <benefício>`**. O resto do CTA (urgência, "pode
sair do ar") vem depois, nunca antes do grátis.

### CTA simples — só o comando, zero condição (regra da dona, 2026-10-04)

O fechamento do vídeo (fala da última cena, texto na tela do fecho E o campo CTA
do `anuncio.md`) é **uma frase de comando, curta**. **Nenhuma condição de compra
no áudio nem no vídeo**: nada de garantia, preço, "pagamento único", "acesso
vitalício", "sem mensalidade", "dá pra imprimir", "aceita os termos" ou lista de
benefício técnico. Empilhar condição faz o fecho parecer complicado e levanta
objeção que não existia ("preciso aceitar uma lei?").

Condição de compra fica só na página de vendas/checkout e, se precisar, no texto
do anúncio (`anuncio.md`). Não é exceção nem quando o produto é grátis: o "é
grátis" não vai no fecho.

**Escopo: isso vale pra vídeo/VO. Estático e carrossel podem mostrar garantia/vitalício** (ex.: `modelagem-escalados/references/carrossel-demonstrativo-iphone.md`).

Tom canônico: CURIOSIDADE, o comando + o que a pessoa vai descobrir.

```
Clica aqui embaixo e descobre como.
Clica no link aqui embaixo e conhece o manual.
Clica aqui embaixo e vê por dentro.
```

Não:

```
Pagamento único, acesso vitalício, dá pra imprimir. Clica aqui embaixo e vê por dentro.   ← condição no fecho
Clica no botão, aceita os termos, garanta sua compra com 7 dias de garantia
e pagamento seguro, e acesse agora.                                          ← empilhado, burocrático
```

### DENTES — bloco obrigatório em TODA cena de rosto falando

O defeito de dentes é o mais recorrente do Veo em talking head, e tem **quatro
variantes**. Proibir uma não protege das outras — todas apareceram em produção, no
mesmo projeto:

| Variante | Como aparece |
|---|---|
| **faltando** | buraco escuro na arcada, a pessoa fica banguela em parte do clipe |
| **prateado / metálico** | um dente vira coroa de prata, cinza ou ouro — lê como dentadura barata |
| **amarelado** | esmalte encardido que não combina com a persona |
| **torto** | arcada desalinhada, dente virado, tamanho irregular |

Nenhuma aparece na imagem de referência nem no primeiro frame: **nascem no
movimento da fala**. Só se pegam amostrando a boca ao longo da duração.

**Bloco canônico — cole no `CONTINUITY` de toda cena com rosto falando:**

```
Her teeth stay natural and consistent for the entire clip: a complete upper and
lower row, off-white natural enamel, matte, evenly aligned, age-appropriate for a
65-year-old, with no changes while she speaks. No missing teeth, no gaps, no dark
holes in the mouth. No metallic, silver, grey or gold tooth, no crown, no cap, no
braces, no shiny reflective surface. No yellow, stained or discoloured teeth. No
crooked, twisted, overlapping or irregularly sized teeth. No denture look.
```

**`NEGATIVE`:**

```
missing teeth, gaps between teeth, toothless mouth, black holes in the mouth,
silver tooth, metallic teeth, grey metal tooth, gold tooth, dental crown, metal cap,
shiny reflective teeth, yellow teeth, stained teeth, discoloured teeth, crooked teeth,
twisted teeth, overlapping teeth, uneven tooth size, denture look, deformed teeth,
distorted dental anatomy
```

**Cheque assim, sempre — recorte a BOCA, não o rosto inteiro:**

```bash
# a boca fica em ~0.21-0.41 da altura; recortar mais abaixo pega só o pescoço
for t in 1.5 2.5 3.5 5 6; do
  ffmpeg -v error -ss $t -i cena-N.mp4 -frames:v 1 \
    -vf "crop=iw*0.5:ih*0.20:iw*0.25:ih*0.21,scale=230:-1" /tmp/b$t.jpg -y
done
montage /tmp/b*.jpg -tile 5x1 -geometry 230x+2+2 -background '#111' /tmp/boca.jpg
```

Um único frame não basta: o dente muda **durante** a fala. Cinco tempos é o mínimo.

**Cuidado com o teto de 2500 chars.** O bloco completo é longo e estoura o
`-short` (medido: 2812). Corte na ordem descrita em `hub-video-playwright` — `NEGATIVE` enxuto,
`CONTINUITY` resumido, cauda do `VOICE`. Nunca a fala nem a linha de lip-sync.
Versão comprimida que cabe:

```
Teeth stay natural the whole clip: complete rows, off-white matte enamel, aligned,
no missing, metallic, silver, gold, yellow, stained or crooked teeth, no crown, no cap.
```

### Dentes: o Veo apaga dentes em boca falando — proíba explicitamente

Em plano médio com a pessoa falando, é comum a arcada superior aparecer com
**buracos escuros ou dentes faltando** — a pessoa fica banguela em parte do clipe.
Não aparece no primeiro frame nem na imagem de referência: nasce no movimento da
fala, então só se pega amostrando a boca ao longo da duração.

```bash
# recorte da boca em vários tempos
for t in 1.5 2.5 3.5 4.5 5.5; do
  ffmpeg -v error -ss $t -i cena-N.mp4 -frames:v 1 \
    -vf "crop=iw*0.5:ih*0.22:iw*0.25:ih*0.22,scale=260:-1" /tmp/b$t.jpg -y
done
montage /tmp/b*.jpg -tile 5x1 -geometry 260x+3+3 -background '#111' /tmp/boca.jpg
```

No `CONTINUITY`:

```
Her mouth keeps complete, natural, even teeth for the entire clip — a full upper
and lower row, no gaps, no missing teeth, no dark holes in the mouth while she speaks.
```

No `NEGATIVE`: `missing teeth, gaps between teeth, toothless mouth, black holes in
the mouth, deformed teeth, distorted dental anatomy`.

**Segunda variante do mesmo defeito: dente PRATEADO.** Além de apagar dentes, o Veo
às vezes entrega um dente metálico — prata, cinza, azulado ou dourado, como coroa ou capa.
Numa senhora de 65 anos isso lê como dentadura barata e estraga o close. Proibir
"missing teeth" não cobre: o dente está lá, só é de metal.

**Acontece mesmo com a imagem de referência correta (dentes visíveis, boca
entreaberta).** Confirmado em produção (VSL Rosa, 2026-09-12): as 5 imagens de
setup mostravam a boca entreaberta com dentes naturais, exatamente como manda a
FASE 3 — e mesmo assim a cena 1 saiu com um dente nitidamente azul/metálico por
~1 frame em torno de 5,5s, no meio da fala. Ou seja, referência boa reduz a
frequência do defeito mas **não elimina**: é defeito de invenção durante a
ANIMAÇÃO, não de falta de informação na imagem. Conclusão prática: o bloco de
dentes no `CONTINUITY`+`NEGATIVE` é obrigatório em toda cena falada mesmo
quando a imagem de referência já está perfeita — nunca pule por achar que "a
foto já resolve".

Acrescente no `CONTINUITY`:

```
Teeth are natural off-white enamel, matte, slightly uneven and age-appropriate:
no metallic, silver, grey or gold tooth, no crown, no cap, no shiny reflective surface.
```

E no `NEGATIVE`: `silver tooth, metallic teeth, grey metal tooth, gold tooth,
dental crown, metal cap, shiny reflective teeth`.

Os dois blocos de dentes juntos estouram os 2500 chars do `-short` com facilidade —
ao aplicar deu 2812. Corte na ordem descrita em `hub-video-playwright`: `NEGATIVE` enxuto, `CONTINUITY`
resumido, cauda do `VOICE`. **Nunca** corte a fala nem a linha de lip-sync.

Vale para **toda** cena de rosto falando, não só close.

### Ficha de cada cena

- **Look** — ambiente, paleta, luz, hora
- **Personagem** — idade, nacionalidade/etnia, roupa, cabelo, expressão
- **Enquadramento** — close / médio / cenital, altura da câmera
- **Ação** — o que acontece nos 6-10s, em uma frase
- **Fala** — texto exato, idioma e sotaque
- **Voz** — timbre, ritmo, emoção
- **Áudio ambiente** — silêncio, rua, madrugada

---

## FASE 2 — Browsers e lane

**Escolha a lane do criativo antes de tudo** — um nome curto que identifique este trabalho (`tarot`, `espanhol`, `cozinha`). Vários Claudes usam os mesmos browsers logados; sem lane todos caem na mesma aba e no mesmo chat, e um sobrescreve o material do outro.

```bash
LANE=<nome-do-criativo>
~/.claude/bin/lane.sh take gpt $LANE     # imagens
~/.claude/bin/lane.sh take hub $LANE     # vídeos
G=gpt-$LANE ; H=hub-$LANE                # use $G e $H em TODO comando
```

Protocolo completo em `~/.claude/bin/LANES.md`. Regras que valem sempre:

- **Refixe a aba** (`lane.sh take ...`, idempotente) no começo de cada fase e sempre que algo parecer fora de lugar.
- **Nunca** `agent-browser close --all` — mata as abas dos outros Claudes. Ao terminar o criativo: `lane.sh drop gpt $LANE` e `lane.sh drop hub $LANE`.
- **Todo download leva o prefixo da lane** no nome (`$LANE-cena-1.mp4`) e passa pela pasta de staging da lane antes de ir pro projeto.
- **A área do staging depende da ferramenta.** `export LANE_AREA=HUB` quando o arquivo vem do Hub (vídeo, criativo, transcrição) — vai para `~/Downloads/HUB/$LANE/`. A área padrão, `PLAYWRIGHT`, é a da geração por browser (imagens do ChatGPT), e fica em `~/Downloads/PLAYWRIGHT/$LANE/`. Este criativo usa **as duas**: as imagens de cena saem do ChatGPT (PLAYWRIGHT) e os clipes saem do Hub (HUB). Exporte a variável na fase certa; misturar faz um `collect` levar arquivo de uma fase para a pasta da outra.

`lane.sh take` sobe (ou reaproveita) os Chromium persistentes e conecta o agent-browser. `browsers.sh status` mostra o que está de pé, em que URL, e avisa se tem Chromium empacotado (perfil em `/tmp`) rodando — esse não guarda login e trava no Cloudflare.

Portas fixas por perfil, registradas em `~/.agent-profiles/registry.conf`. Nunca invente porta nova nem suba Chromium à mão fora do script: perfil errado = login perdido.

**Nunca use `agent-browser open`** — o Chromium empacotado dele trava no Cloudflare. Ver skill `browser-cloudflare`.

Os perfis em `~/.agent-profiles/` são persistentes, então normalmente já abrem logados.

Se o login cair: as credenciais estão em `~/.claude/.credentials.env` (permissão 600) — `set -a; source ~/.claude/.credentials.env; set +a`, e preencha pela variável, nunca com o valor literal. **O checkbox do Cloudflare pode ser clicado** — nesse Chromium ele valida normalmente. Só chame o usuário se falhar duas vezes seguidas ou se pedir 2FA.

Passe `--session $G` (ChatGPT) ou `--session $H` (Hub) em **todo** comando. Sessão sem lane (`--session gpt`) é bug: vai parar no chat de outro Claude.

---
## FASE 3 — Imagens de referência (lane gpt)

### PRINCÍPIO CENTRAL: o que não estiver definido na IMAGEM, o modelo inventa

Toda decisão desta fase sai daqui. O Veo copia o que enxerga na imagem de
referência e **inventa tudo o que ela não mostra** — e o que ele inventa muda
durante o clipe, porque não tem de onde copiar.

Foi assim que apareceram, todos no mesmo projeto:

| O que faltava na imagem | O que o modelo inventou |
|---|---|
| boca fechada, dentes não visíveis | dente faltando, prateado, amarelo, torto — mudando durante a fala |
| nenhum rosto em quadro (insert de mãos) | **outra mulher** e outra voz |
| prop mencionado no prompt mas ausente da foto | o objeto brotando na mesa |
| papel com texto que o prompt mandava "ler em voz alta" | a fala impressa no papel, truncada |

A conclusão prática: **resolva na imagem, não no prompt.** Uma lista de proibições
no `NEGATIVE` é a segunda linha de defesa; a primeira é a foto já mostrar a coisa
certa. Custa uma imagem no ChatGPT (barato, rápido) e evita uma geração de vídeo
perdida (cara, com cota).

### Gere a imagem com a BOCA LEVEMENTE ABERTA, mostrando os dentes

O caso mais rentável desse princípio. Com a boca fechada na referência, o modelo
não tem arcada de onde copiar e sorteia a dentição a cada frame. Com os dentes
visíveis, ele copia.

```
MOUTH AND TEETH: her mouth is slightly open, caught mid-sentence as if she has just
started speaking, and her upper teeth are clearly and naturally visible. A complete,
even upper row of natural off-white enamel, matte, age-appropriate, slightly imperfect
but healthy. This is NOT a smile: no wide grin, no raised cheeks, no squinting — just
a relaxed talking mouth with the teeth showing.
```

O "NOT a smile" não é detalhe: sorriso largo na foto vira careta ao animar, porque o
modelo parte de um extremo. Boca entreaberta de quem vai falar é o ponto certo.

Com isso na imagem, **remova as travas de dente do prompt de vídeo** — elas deixam de
ser necessárias e liberam ~200 chars do teto de 2500.

**Copie o bloco acima LITERALMENTE. Parafrasear reprova.** Medido na leva AR de
26/08/2026: quem escreveu os prompts trocou por "lips slightly parted in a natural
relaxed expression, upper teeth partly visible" e **falhou em 7 de 28 frames**
(boca fechada). A versão fraca perde porque descreve uma EXPRESSÃO parada, e as
pistas de expressão vizinhas — "calm", "composed", "quiet certainty", "expression
in repose" — puxam boca fechada com mais força.

O que faz o bloco funcionar são três coisas, e as três somem na paráfrase:

1. Descreve **AÇÃO** (`caught mid-sentence`, `has just started speaking`), não
   estado. Boca aberta é consequência de estar falando.
2. Diz explicitamente o que NÃO é (`This is NOT a smile`).
3. Vai acompanhado, na lista negativa, de `closed mouth, sealed lips, teeth hidden,
   teeth not visible, lips pressed together, posed static smile`.

Se a cena pede expressão contida ou séria, **não remova o bloco**: mantenha e ajuste
a frase da expressão para incluir a fala — `calm and composed, speaking`, e não
`calm and composed`.

### A imagem NASCE do roteiro — uma por cena onde o estado visual muda

A ordem é: escrever o roteiro → ler cena a cena → **para cada cena, perguntar se o
que está em quadro mudou** → se mudou, essa cena tem imagem própria.

O caminho inverso é o que produz descasamento: gerar um punhado de imagens
"genéricas" do criativo (uma base, uma com o prop na mão, um close) e **depois**
distribuir pelas cenas. Feito assim, o prompt de vídeo de uma cena acaba descrevendo
o que estava na imagem de outra — e o modelo tenta conciliar movendo objeto,
inventando prop ou trocando a pessoa. Numa leva de 6 criativos isso custou 4
regerações.

Monte a tabela junto com o roteiro, antes de abrir o ChatGPT:

| cena | fala | estado em quadro | imagem |
|---|---|---|---|
| 1 | "agarrá sal y un vaso con agua" | mesa com bacia, papel dentro | `A` |
| 2 | "quien hace esto ve la plata" | idem, nada mudou | `A` |
| 3 | "escribí tu número en un papel" | ela **segura** o papel | `B` |
| 4 | "ponelo en el vaso" | papel **entrando** na água | `C` |
| 5 | "tiene que ser el correcto" | volta ao repouso | `A` |

Cenas que repetem o mesmo estado **compartilham** a imagem — isso é normal e
desejável. O que não pode é uma cena usar imagem de um estado que a fala dela não
descreve.

**Os dois extremos estão errados, e os dois foram cometidos na mesma leva:**

- **Imagem demais / variada demais** — insert de mãos, close de prop, cenital.
  Cada enquadramento sem rosto é uma chance de o modelo inventar pessoa e voz.
- **Imagem de menos** — uma única foto para o criativo inteiro, inclusive nas
  cenas em que ela pega o papel ou põe algo no copo. Aí o `ACTION` pede uma ação
  que a imagem não sustenta, e o objeto salta para a mão sozinho.

O critério que separa os dois:

> **Muda o que está em quadro? Nova imagem — sempre com o rosto dela em quadro.**
> **Só a fala muda? Mesma imagem.**

Na prática, num criativo de 6 cenas isso costuma dar **2 ou 3 imagens**: a de
repouso (usada em 3-4 cenas), a dela segurando o objeto à altura do peito, e a da
ação (pondo o papel no copo) — esta última em plano médio, com o rosto visível,
nunca só as mãos.

Nos criativos que funcionaram, a proporção era **1 imagem por cena** (4 cenas,
4 imagens), com variação mínima entre elas — mesmo plano frontal, no máximo um
enquadramento um pouco mais fechado. Nunca insert de mãos, nunca close de objeto
isolado.



A imagem é o **primeiro frame** do vídeo e o contrato que o vídeo vai seguir. Ela trava personagem, roupa, luz e ambiente.

**O GPT gera até 10 imagens por vez.** Lote é o modo certo de trabalhar — não caia
para "uma por requisição" ao ver um grid. O grid é falha de **redação do pedido**,
não limite do modelo.
### ⛔ MECÂNICA DO CHATGPT — invoque `gpt-imagem-playwright` ANTES de tocar no browser

<EXTREMELY-IMPORTANT>
Nesta fase você **tem que** invocar a skill `gpt-imagem-playwright` pelo tool
`Skill` antes do primeiro comando de browser. Ela é a fonte única da mecânica:
lane, chat novo, anexo de referência, envio pelo `data-testid`, verificação de
dono da aba, espera, download filtrado por proporção, validação do arquivo salvo
e distribuição por hash.

**Não improvise seletor, não copie comando de memória e não use `agent-browser
open`.** Os seletores do ChatGPT mudam; esta skill guarda as *regras criativas*
(o que a imagem precisa mostrar), a outra guarda *como operar* — e é ela que é
mantida atualizada.
</EXTREMELY-IMPORTANT>

Regras desta skill que a mecânica **não** substitui, e que valem sempre:

- **UMA cena por mensagem, chat novo a cada imagem.** Lote de cenas volta grid —
  testado quatro vezes com redações cada vez mais explícitas, e nenhuma funcionou.
  Um grid 3×1 sai em 9:16 e passa por qualquer checagem de dimensão; cada cena
  dentro dele fica com ~941×557 e não serve de primeiro frame. Recortar não salva.
- **Automatize em vez de negociar com o modelo:**
  `for n in 31 32 33; do ./one.sh prompt-$n.txt cena-$n; done`
- **Lote só para cenas independentes.** A cena 2 de um hook nunca entra no mesmo
  lote da cena 1 — ela é gerada depois, com a cena 1 aprovada anexada.
- **Consistência de personagem:** anexe um frame real e peça "same woman, same
  face, same age". Nunca descreva a pessoa do zero de novo.

```bash
# extrair frame de referência de um criativo existente
ffmpeg -ss <seg> -i vencedor.mp4 -frames:v 1 REFERENCIA/persona-01.png
```

### Regras do prompt de imagem (inglês)

- Frame **parado**, não ação em curso
- `vertical 9:16 story format`
- Lente e luz: `shot on 35mm, natural window light, shallow depth of field`
- Proibir texto: `no text, no captions, no watermark, no UI overlay`
- Look UGC: `amateur phone footage look, slight grain, no studio lighting`
- **Liste e feche os objetos:** `only these objects on the table: X, Y, Z — nothing else`. Objeto ambíguo aqui vira objeto brotando no vídeo.
- **Realismo ancorado:** `grounded documentary realism, real ordinary objects, natural imperfections, no surreal elements, no decorative clutter`
- **Feche a foto em repouso:** `still frame, subject at rest, not mid-gesture`. Sem
  isso a imagem sai no meio de um movimento e o vídeo anima a partir de um extremo —
  o gesto "completa" sozinho e vira morphing. Vem dos criativos que funcionaram
- **Proíba o que pode vazar da referência.** Se a foto de referência tem vela e cristal e a cena nova é uma cozinha, escreva `absolutely no candles, no crystals, no tarot cards, no mystical objects`.
### Duas personas parecidas na mesma leva CONVERGEM para o mesmo visual

Ao gerar vários corpos de uma vez, personas do mesmo "tipo" (duas mulheres de
meia-idade em ambiente doméstico à noite, por exemplo) saem **visualmente idênticas**
mesmo com prompts diferentes — mesmo cabelo, mesma roupa, mesma luz. Dois corpos
gêmeos destroem o objetivo da leva: a Meta lê os dois como um conceito só.

Idade diferente **não** basta ("mulher 45" vs "mulher 38" convergiu). Force contraste
em eixos concretos e **proíba explicitamente os elementos do outro**:

| Eixo | Corpo A | Corpo B |
|---|---|---|
| cabelo | liso e solto | ondulado |
| cor da roupa | verde escuro | cinza |
| móvel | sofá + estante | cama + criado-mudo |
| luz | teto neutra, fria | abajur quente |

E na descrição de um: `absolutely no bed, no table lamp, no bedside table`.

Cheque isso **no gate**, montando os corpos lado a lado. Dois que se parecem custam
uma imagem para corrigir agora e a leva inteira se passarem.

### Peça longa (VSL): NÃO gere uma imagem por cena — gere por SETUP

Numa peça de 2 minutos são ~17 cenas de 8s. Gerar 17 imagens é desperdício e, pior,
**instabilidade**: cada imagem nova é outro sorteio de rosto, e ao longo de 17 cenas
a persona escorrega mesmo com referência anexada.

A mesma imagem serve de primeiro frame para **várias falas diferentes**. Agrupe por
**setup visual**, não por cena:

| Imagem | Setup | Cenas que usam |
|---|---|---|
| A | plano médio, mesa, mãos na mesa | 1, 2, 5, 6, 10, 13 |
| B | close no rosto | 3, 4, 8, 9, 16, 17 |
| C | médio + objeto da fala (caderno) | 7 |
| D | médio + objeto da fala (papel e caneta) | 11 |
| E | insert cenital de mãos, sem rosto | 12 |
| F | médio + objeto da oferta (dossiê aberto) | 14, 15 |

**6 imagens para 17 cenas.** Menos geração, e a persona fica idêntica do começo ao
fim porque quase tudo nasce do mesmo frame.

Regra de alternância: **nunca deixe o mesmo enquadramento por mais de ~20s**. Médio
e close alternados, e pelo menos um **insert sem rosto** no meio — é o que quebra a
monotonia do busto falante numa peça longa.

### Decupagem: escreva a peça já em cenas de 8s

Não escreva o roteiro corrido e fatie depois. Escreva **direto na grade do motor**:
uma linha por cena, com a fala e a contagem de palavras ao lado.

```
| # | Fala | pal | Enquadramento |
|---|------|-----|---------------|
| 1 | Esos tres números que acabás de descubrir no se quedan quietos. | 11 | médio |
| 2 | Actúan en silencio, tirando todo para atrás. Conocerlos no alcanza. | 16 | médio |
```

Assim o teto de 16 palavras deixa de ser algo a conferir no fim e passa a ser a
própria unidade de escrita. E a coluna de enquadramento já vira o mapa de quais
imagens gerar.

Conta de tempo: **8s por cena, ~6,5-7s líquidos** após cortar silêncio e somar o
respiro de 0,75s. Uma peça de 2min = ~17 cenas faladas.

### Regerar cena de personagem existente: anexe a referência, não redescreva

Toda regeração de uma cena cujo criativo já tem a persona definida usa **imagem
aprovada anexada**, nunca descrição textual da pessoa. Vale para conserto de
defeito, troca de pose, mudança de enquadramento — qualquer motivo.

Numa leva real a cena 1 precisou ser refeita: foi descrita do zero com a mesma
idade, cabelo, roupa, parede e luz, e voltou **outra mulher**, enquanto as cenas 2,
3 e 4 seguiam com a original. Descrição textual sorteia; referência anexada fixa.

Peça também **uma única imagem**, explicitamente — o modelo entrega colagem de 4
poses com facilidade, e a colagem tem as dimensões corretas (9:16), então passa por
qualquer checagem que não seja **abrir o arquivo**. Aconteceu no mesmo criativo: a
imagem da cena 1 era um grid de quatro fotos empilhadas, virou clipe, e só apareceu
quando o dono assistiu.

### A cena tem que fazer sentido na vida real — teste antes de escrever o prompt

Antes de descrever qualquer cena, pergunte: **uma pessoa de verdade faria isso,
nesse lugar, desse jeito?** Se a resposta é não, o defeito não nasce no modelo:
nasce no roteiro, e nenhum bloco anti-morphing conserta.

O caso que originou esta regra: "homem no banco do motorista com o celular apoiado
no volante". Ninguém apoia celular no volante — não tem onde firmar. O modelo não
sabe onde fixar o objeto e ele **desgruda e flutua** no meio do clipe. Foram três
regerações tentando corrigir com prompt, até a correção certa aparecer: **tirar o
celular da cena.** Ele fala de memória, mãos no volante; a leitura aconteceu antes
de entrar no carro.

Checagem, cena por cena:

- **Todo objeto tem apoio físico?** Na mão fechada, sobre a mesa, no bolso. Objeto
  "apoiado" onde não se apoia é morphing garantido.
- **A ação é possível ali?** Dirigindo não se lê tela. Cozinhando não se segura
  telefone com as duas mãos. Deitado não se digita de frente pra câmera.
- **O objeto precisa mesmo estar em cena?** Se a fala já entrega a informação, cortar
  o objeto é sempre melhor que domar o objeto. Menos coisa em cena, menos invenção.
- **A pessoa está vestida e posicionada como aquele ambiente pede?** Roupa de praia
  numa cena de escritório de manhã lê como IA — e pode atrair o público errado.
- **A hora do dia bate com a luz e com a fala?** "Chega no e-mail de manhã" com
  janela noturna ao fundo se contradiz.

Regra prática: **remover é mais barato que corrigir.** Cada objeto a mais é uma
chance de o modelo inventar. Se a cena funciona sem o objeto, tire.

### Tela, papel, placa: TODA superfície que mostra conteúdo é obrigatória no prompt

Se a cena tem celular, laptop, tablet, papel escrito, cartaz ou placa, o conteúdo
dessa superfície **tem que ser descrito explicitamente**. Deixar implícito produz
três defeitos, todos já vistos em produção:

- **Tela preta / aparelho desligado.** O modelo entrega o objeto sem conteúdo. Em
  imagem parece só sóbrio; virando vídeo é a cena inteira com uma tela apagada, e
  num criativo de mecanismo isso mata o anúncio — a tela É o produto.
- **Aparelho virado de costas.** "Resolve" o problema de texto errado escondendo a
  tela, e entrega uma cena que não mostra nada.
- **Idioma errado.** Sai em inglês por padrão. Um anúncio brasileiro exibindo o
  próprio produto em inglês (e com data de outro ano) não sobe.

Escreva sempre os quatro itens: **ligada, o que aparece, em que idioma, com que
aparência**. Modelo para tela de app de leitura em PT-BR:

```
the phone screen is ON and clearly visible, displaying a reading app in Portuguese:
a short title line, a date line, and three or four paragraphs of body text in
Brazilian Portuguese, dark background with warm off-white text, calm editorial
layout, no app chrome, no message bubbles, no chat interface, no green color,
no English text, text slightly soft so individual words are not sharply readable
```

O "slightly soft" é deliberado: resolve a tensão entre precisar de conteúdo
plausível e não poder exibir texto inventado. Texto nítido na tela de um produto
real é mockup falso — pode prometer o que a oferta não promete, e reprova.

**Nunca:** balão de mensagem, layout de chat, qualquer tom esverdeado (lê como
WhatsApp), tela preta, aparelho de costas, texto em inglês.

E confira **abrindo a imagem** antes de mandar pro vídeo. Tela errada na imagem é
tela errada no clipe — e clipe custa cota.

### Descrição concreta VENCE regra genérica — não deixe o prompt se contradizer

Aconteceu **duas vezes na mesma leva** (AR, 26/08/2026), e as duas custaram
regeração:

| O que o prompt dizia | O que saiu |
|---|---|
| negativa com `no lit screen` (escrita pensando em "sem UI") | celular **desligado** na cena |
| corpo do prompt: `the phone face-down beside her` | celular de tela pra baixo, produto invisível |

Nos dois casos existia, no mesmo arquivo, uma regra genérica mandando o contrário
("a tela tem que estar ligada"). **O modelo obedeceu à descrição concreta e ignorou
a regra.** Objeto descrito no corpo do prompt pesa mais que instrução abstrata no
fim.

Duas consequências práticas:

- Ao corrigir um prompt, **releia o corpo inteiro** procurando a descrição que
  contradiz a correção. Acrescentar a regra certa sem remover a frase errada não
  corrige nada — só cria um prompt esquizofrênico.
- Nunca escreva `no lit screen` querendo dizer "sem interface". A negativa correta
  para cena com celular é `phone screen off, black screen, phone face down` — que é
  o oposto do que aquela frase pedia.

### Marca de terceiro em cena: proíba logo, permita o genérico

Documento, cartão, embalagem ou tela em cena podem vir com **marca real legível** —
na leva AR saiu um cartão **VISA** nítido em cima de um resumo de fatura. Bandeira
de cartão identificável em criativo de tráfego pago é briga com o Meta de graça.

Na lista negativa de todo prompt de imagem:

```
brand names, brand logos, credit card brand marks, VISA, Mastercard,
legible printed text, readable document text
```

**Mas não confunda marca com cenário.** Um papel escrito `ESTADO DE CUENTA DE
TARJETA DE CRÉDITO`, sem bandeira, sem número de cartão e com o corpo ilegível,
está **aprovado** — é cenário genérico, ajuda a contar a história e não imita
instituição real. O que se proíbe é a marca identificável e o documento que passe
por real. Regerar cenário genérico é queimar geração para piorar a cena.

### Nacionalidade: seja específico, "Latin American" não basta

"Latin American" faz o modelo cair no padrão mexicano/andino. Se o criativo fala com um país, o rosto tem que ler como daquele país — senão o público não se reconhece.

- **Argentina / Uruguai:** `Argentine woman from Buenos Aires, of Italian and Spanish descent, European-Mediterranean features, fair to light olive skin`
- **Brasil:** especifique a região — Sul, Sudeste e Nordeste têm fenótipos bem diferentes
- **México / América Central:** `Mexican woman, mestiza features, warm olive skin`
- **Colômbia / Venezuela caribenha:** `Caribbean Colombian woman`

Combine sempre com a idade e o tipo de cabelo. E confira na imagem gerada antes de mandar pro vídeo — corrigir aqui custa uma imagem, corrigir depois custa o clipe inteiro.

### Rosto: natural, exposição correta, expressão em repouso

A imagem é o ponto de partida da animação. Rosto estourado ou expressão exagerada na foto vira careta esquisita no vídeo — o modelo anima *a partir* daquele extremo e não tem pra onde ir.

Sempre inclua:

```
natural evenly exposed face, no blown-out highlights on the skin, no overexposure,
soft natural skin tones, visible pores and fine lines, natural skin texture,
relaxed neutral expression, mouth closed or barely open, no exaggerated
expression, no wide grin, no raised eyebrows, no squinting, no forced pose,
candid unposed look
```

E proíba o acabamento de banco de imagem: `no beauty retouching, no skin smoothing, no plastic skin, no airbrushing, no stock photo look, no perfect studio lighting`.

**Deixe a emoção para o prompt de vídeo, não para a imagem.** Se a cena pede alguém rindo ou falando rápido, gere a imagem com o rosto em repouso e descreva a emoção no `ACTION` do vídeo. Partir do repouso dá movimento natural; partir do exagero dá deformação.
### A imagem manda; o prompt de vídeo se ADAPTA a ela

Depois de aprovar a imagem, releia o `CONTINUITY` das cenas que a usam e confirme
que ele descreve **o que está na imagem**, não o que você imaginou ao escrever.

Caso real: a imagem voltou com o papel do número **sobre a mesa, na frente do
copo**; os seis prompts do criativo diziam que ele estava **submerso no mel dentro
do copo**. Nada disso é erro isolado — junto, é instrução para o modelo *mover* o
papel durante o clipe, que é exatamente como nasce objeto flutuando. Foram 10
arquivos de prompt corrigidos antes de gerar; se tivesse gerado, seriam 6 clipes
perdidos.

Regra: **imagem aprovada é a fonte da verdade.** O prompt descreve a imagem, nunca
o contrário.

**O gatilho mais perigoso é REMAPEAR.** Trocar qual imagem uma cena usa — por
defeito, por decisão de formato, por qualquer motivo — e **não** reescrever o
`CONTINUITY` daquela cena. O caminho fica certo, o `valida_img.sh` passa, e o
prompt continua descrevendo a imagem antiga.

Encontrados numa única revisão, todos por esse motivo:

| prompt dizia | imagem nova tinha | o clipe faria |
|---|---|---|
| "um celular sobre a toalha" | **mesa vazia** | celular brotando do nada |
| "as mãos escrevendo na fatura" | faturas paradas, mãos na mesa | mão indo ao objeto sozinha |
| "ela segura a folha de louro" | folha **na mesa** | folha saltando para a mão |

Checklist ao remapear qualquer cena — os três, sempre:

1. copiar a imagem nova para `CRIATIVO-N/IMG/cena-i.png` e validar por hash
2. **reescrever o `CONTINUITY`** listando o que está na imagem nova, com contagem
   (`exactly ONE …`) e onde cada coisa fica
3. reescrever o `ACTION` para o novo enquadramento — e, em plano fixo, incluir
   `she does not pick anything up` para que nenhum objeto salte para a mão
## FASE 3.5 — QA das imagens: GATE obrigatório antes de qualquer vídeo

Nenhum clipe é gerado enquanto TODAS as imagens da leva não passarem por aqui.

Motivo, medido em produção: vídeo é o recurso escasso (o Grok tem teto por dia no
Hub). Imagem errada que vira vídeo custa **duas** gerações — a perdida e a
regeração. Uma leva inteira já queimou a cota assim.

**Ordem de trabalho da leva, sem exceção:**

1. Um worker só. Nunca vários no mesmo browser — abas compartilhadas trocam imagem
   entre criativos sem avisar.
2. Gerar **todas** as imagens, de todos os criativos.
3. **Este gate.** Quem revisa não é quem gerou.
4. Só então vídeo, **um criativo por vez**, fechado antes do próximo.

### O gate

```bash
# imagem duplicada: o mesmo PNG salvo como cenas diferentes
md5sum CRIATIVO-*/IMG/*.png | sort | uniq -w32 -D     # qualquer saída = defeito

# contact sheet por criativo
montage CRIATIVO-N/IMG/cena-{1,2,3,4}.png -tile 4x1 \
  -geometry 220x391+4+4 -background '#111' sheet-N.jpg
```

Abrir o sheet e verificar, por cena:

| Checagem | Falha já vista |
|---|---|
| Hashes todos distintos | 3 cenas eram o mesmo PNG; o vídeo saiu com 3 cenas idênticas |
| Persona e ambiente batem com o roteiro | cena-4 de um criativo era imagem de outro |
| Mesma pessoa, roupa e cabelo em todas as cenas | troca de atriz no meio do criativo |
| Toda tela ligada, com conteúdo, no idioma certo | 4 imagens com tela preta ou celular de costas |
| Sem texto queimado, marca d'água, objeto proibido | legenda escrita pelo modelo dentro da cena |
| Serve como primeiro frame: rosto em repouso, objeto na posição inicial | expressão exagerada virou careta ao animar |

**Contar arquivos não é QA.** Só hash e olho detectam esses defeitos — todos eles
passaram por relatório de worker dizendo "verificado".

Imagem reprovada volta pra FASE 3. Só depois de a leva inteira passar é que a
FASE 4 começa.

## FASE 4 — Prompt de vídeo

### Antes de escrever a primeira linha de qualquer prompt de vídeo

Estas decisões são tomadas **enquanto você escreve**, não conferidas depois. Cada
uma existe porque o defeito correspondente já queimou clipe em produção, e nenhum
deles tem conserto na pós — o único remédio é regerar, gastando cota.

**1. A fala cabe no clipe?** Escreva a fala e conte na hora. 10s = 25 palavras
(22 se o `VOICE` pedir 2.2 pal/s); 6s = 15. Se não cabe, **corte o texto agora** —
esticar o clipe não é opção. Texto que estoura faz o áudio correr além da animação:
a boca para e a voz continua.

**2. Tem objeto na mão?** Então gere em **6s**, não 10s — a degradação cresce com a
duração. E antes disso pergunte se o objeto precisa mesmo existir na cena: se a fala
já entrega a informação, **tirar o objeto é sempre melhor que domar o objeto**.

**3. O objeto tem apoio físico real?** Mão fechada, mesa, bolso. Se está "apoiado"
onde ninguém apoia (celular no volante), o modelo não sabe onde fixar e ele desgruda
e flutua. Isso é defeito de roteiro: volte e mude a cena, não o prompt.

**4. `CHARACTER` e `VOICE` são strings fixas.** Escreva uma vez por criativo e cole
byte a byte em todas as cenas. Resumir, reescrever ou trocar por "same woman as in
the reference" muda a pessoa e a voz.

**5. Nenhuma instrução meta no texto.** Nada de "same as scene 1", "keep consistent",
"do not paraphrase". O Grok lê isso como conteúdo da cena.

**6. A lista de objetos é fechada e nomeada.** Tudo que está em quadro, nada além.

**7. Nunca peça legenda.** `no subtitles, no burned-in text` no NEGATIVE, sempre.
   Mas saiba que o NEGATIVE **não basta sozinho**: numa cena real com o bloco
   completo de proibições (`captions, subtitles, burned-in text, on-screen text,
   closed captions`) a legenda apareceu mesmo assim — porque a fala tinha 29
   palavras para um clipe de 10s. Texto que não cabe faz o modelo "ajudar"
   imprimindo a frase na tela. A mesma cena, com a fala encurtada, saiu limpa.
   **Legenda queimada é quase sempre sintoma de fala longa demais** — trate pelo
   item 1, não por mais proibição.

**8. Papel, placa ou tela EM QUADRO: trave o conteúdo como prop fixo.** Se a cena
   tem uma superfície escrita e o personagem fala, o modelo **reescreve a
   superfície com a fala**. Não é legenda na tela: ele imprime o texto falado no
   próprio objeto, com a caligrafia da cena, e o resultado sai truncado e sem
   sentido.

   Caso real: cena de uma senhora segurando um papel com sete palavras e o número
   63. O `ACTION` dizia que ela **lia as palavras em voz alta**. O clipe voltou com
   o papel reescrito — `"Yo soy bendición, yo soy sod, properidad, yonfección,
   Repetilo antes Repetilo de dormir."` — enquanto as duas cenas irmãs, com o
   mesmo papel e sem "lê em voz alta", saíram intactas.

   Duas travas, as duas necessárias:

   - **Nunca escreva que o personagem lê o conteúdo em voz alta.** Troque
     `reads the words out loud to the lens` por `speaks to the lens`. É essa frase
     que convida o modelo a sincronizar objeto e fala.
   - **Declare a superfície como prop imutável** no `CONTINUITY`:

   ```
   The sheet of paper is a fixed prop: it shows exactly the same seven handwritten
   Spanish words and the number 63 as in the reference image, completely unchanged
   for the whole clip. No new words are written on it, no text on it changes,
   nothing is added or erased.
   ```

   E no `NEGATIVE`: `text changing on the paper, new handwriting appearing, words
   being written during the clip, altered handwriting, spoken words printed on the
   paper`.

   Vale para **toda** cena com superfície escrita em quadro, mesmo as que já saíram
   certas uma vez — o defeito é sorteado, não determinístico. Ao adicionar o bloco
   na versão `-short`, confira o limite de 2500 chars: no caso real os três
   prompts passaram para 2588 e tiveram que perder a cauda do `VOICE`.

**9. Prop que aparece na imagem DUPLICA na mesa — conte-o no prompt.** Se a imagem
   de referência tem um objeto pequeno em posição específica (um papelzinho dentro
   de uma tigela, uma moeda no copo), o Veo cria uma **segunda cópia** dele no
   quadro, tipicamente sobre a mesa, em cenas onde a mão não está mexendo em nada.

   Caso real: bacia com água e um papel "11" submerso. Em **4 de 8 cenas** do mesmo
   criativo nasceu um segundo papel "11" na mesa, na frente da bacia. A imagem de
   referência estava correta e o bloco anti-morphing padrão estava no prompt — não
   bastou, porque ele proíbe "objetos aparecerem" de forma genérica e não diz
   **quantos** existem.

   Escreva a contagem e o lugar, explicitamente:

   ```
   There is exactly ONE small white paper slip in the entire scene and it stays
   submerged inside the glass bowl for the whole clip. No second paper slip exists,
   none appears on the table, none is duplicated.
   ```

   `NEGATIVE`: `duplicated paper slip, second piece of paper appearing on the table,
   paper multiplying`.

   Regra geral: **todo prop pequeno e destacado leva numeral por extenso
   (`exactly ONE`) e o lugar onde fica.** "Only these objects: X, Y" não impede a
   duplicação de X — só impede a entrada de um Z.

Passe pelos nove **para cada cena**. Cinco minutos escrevendo evitam uma regeração
que custa cota e meia hora.

O Grok recebe **imagem + texto**. O texto descreve movimento, ação e fala. A aparência já está na imagem, mas o personagem precisa ser reafirmado para a voz sair certa.

### Estrutura (inglês)

```
CHARACTER: <idade, nacionalidade, aparência resumida, "must stay the same for the whole clip">
CAMERA: locked-off static <plano>, no camera movement, no zoom, no pan
ACTION: <o que acontece, em ordem, nos N segundos — UMA ação só>
  + <micro-movimento natural contínuo: piscar, respirar, peso do corpo,
     ombros e cabeça acompanhando a fala, mão que se ajusta>
DIALOGUE: she speaks on camera, in <idioma/sotaque>. Her lips must be accurately
  synced to these exact words: "<texto exato>"
  Her mouth moves visibly and continuously for the ENTIRE spoken line, from the first
  syllable to the last. The audio must never play while her mouth is closed or still.
  She finishes speaking before the clip ends.
VOICE: <idade, timbre, ritmo, emoção, "natural conversational pace">
AUDIO: <ambiente> only. No background music, no score, no sound effects, no subtitles.
CONTINUITY AND PHYSICS: <bloco abaixo>
NEGATIVE: <lista abaixo>
```

**As três linhas extras do `DIALOGUE` não são enfeite.** Sem elas o Grok trata a
fala como faixa de áudio independente da animação: quando o texto é longo, ele
mantém a voz tocando com o rosto parado. Escrever que a boca se move do primeiro ao
último sílabo, e que o áudio nunca toca com a boca fechada, amarra as duas coisas.

Isso **não substitui** o gate de contagem de palavras da FASE 1 — é a segunda
trava. Texto muito acima do orçamento estoura mesmo com a instrução; a instrução
segura a margem, a contagem segura o caso grosseiro.

### Cena SEM ROSTO sorteia outra voz — evite b-roll falado

O Veo deriva o timbre **do rosto que está no frame**. Numa cena de b-roll (só
mãos, só objeto) não há rosto, então ele sorteia uma voz nova — e o `VOICE`
idêntico, copiado byte a byte, **não segura**. O espectador ouve outra pessoa no
meio do criativo e a montagem se denuncia na hora.

Caso real: criativo de 8 cenas, sete com a senhora em quadro e uma de b-roll
(mãos com sal, sem rosto). Só essa saiu com voz diferente. O dono percebeu antes
de qualquer análise técnica: *"a voz não é a mesma"*.

**A saída é uma só: reenquadre para incluir o rosto.** Não existe insert de mãos
falado que funcione — o modelo inventa a pessoa. Se o objeto precisa aparecer, ela
o segura à altura do peito, com o rosto em quadro.

**Regra: toda cena falada tem rosto em quadro.**

Sobra b-roll de verdade? Então ele é **mudo**, e a fala fica na cena anterior ou
seguinte. Nunca gere b-roll com narração esperando que combine com o resto.

Ponha também no `NEGATIVE` das cenas faladas: `off-screen narrator, voice-over,
different voice`.

Para narração fora de quadro — só quando o criativo inteiro é narrado e nenhuma
cena tem rosto — troque o DIALOGUE por:

```
DIALOGUE: an off-screen female narrator speaks in <idioma/sotaque>, no one is
  visible speaking on camera. She says exactly: "<texto exato>"
  The narration starts within the first second and finishes before the clip ends,
  at a natural pace, without rushing and without trailing silence.
```

### `CHARACTER` e `VOICE` são texto FIXO — copie igual, nunca "same as reference"

O erro mais fácil de cometer e o mais caro: escrever a descrição completa na cena
1 (`35-year-old woman from Buenos Aires, of Spanish descent, fair skin, straight
dark brown hair…`) e, na cena 2, resumir para `same woman as in the reference
image, same face, same top`. Parece equivalente — **não é**. Texto diferente muda
o que o modelo sorteia: a personagem sai levemente diferente **e a voz junto**.

Regra: o bloco `CHARACTER` e o bloco `VOICE` são **strings fixas do criativo**.
Escreva uma vez, cole **byte a byte igual** em todas as cenas. A única coisa que
varia entre cenas é `CAMERA`, `ACTION`, `DIALOGUE` e a lista de objetos do
`CONTINUITY`.

O mesmo vale para o sotaque: `Argentine Spanish with Buenos Aires accent` numa
cena e `Argentine woman, Buenos Aires accent` na outra já é variação suficiente
para o sotaque escorregar. Uma frase, sempre a mesma.

Verificação antes de gerar:

```bash
diff <(grep '^CHARACTER' v-cena-1.txt) <(grep '^CHARACTER' v-cena-2.txt)   # tem que ser vazio
diff <(grep '^VOICE'     v-cena-1.txt) <(grep '^VOICE'     v-cena-2.txt)   # tem que ser vazio
```

### A imagem da cena 2 sai da cena 1, não do zero

Gerar as duas imagens do mesmo hook em paralelo, a partir da mesma descrição
textual, dá duas pessoas parecidas — não a mesma. Gere a cena 1, aprove, e então
gere a cena 2 **anexando a imagem da cena 1 como referência**, pedindo só a
mudança de enquadramento e o que ela tem nas mãos. Consistência de rosto, roupa,
luz e cenário sai de graça.

### Cena de "verso"/folhear página: o verso sai EM BRANCO se nenhuma imagem mostra o conteúdo dele

Caso real (equilibrio-seguro-60, cena de mão virando página): o verso da folha saiu
em branco. Causa raiz — a mesma regra de sempre desta skill, "o que não está na
imagem, o modelo inventa (ou deixa vazio)": a imagem de referência mostrava só a
FRENTE da folha, com o texto e a ilustração daquele lado. Ao animar o giro, o Veo
não tem nenhum pixel de onde copiar o que fica atrás — e sem isso ele não inventa
conteúdo plausível, ele apaga: o verso vira uma folha branca lisa.

É um defeito diferente (e mais comum) do que a mistura de páginas — ver abaixo. Um
é falta total de informação (verso branco); o outro é informação demais e ambígua
(duas folhas soltas, o modelo mistura). O remédio dos dois é o mesmo: **decidir na
imagem, não no prompt de vídeo.**

Correção: gerar uma imagem própria já mostrando o estado do verso — outra página
real do PDF, foto separada — e usar essa imagem como referência daquela cena
específica (ou como frame final, se o motor aceitar). Nunca escrever no prompt de
vídeo "a hand turns the page revealing the back" esperando que o modelo desenhe um
verso plausível sozinho: sem imagem de origem, ele não tem o que desenhar.

**Melhor ainda: não anime a virada, corte entre dois clipes estáticos.** Girar a
página fisicamente dentro de um único clipe é a parte mais frágil do pedido — pede
ao modelo física de papel (dobra, sombra, ângulo) E o conteúdo do verso ao mesmo
tempo, dois problemas somados. Como o Grok Imagine é **ilimitado** no plano do Hub
(regra 8 desta skill), sai mais barato e mais confiável gerar **dois clipes
separados, cada um de uma imagem de referência diferente** — um em repouso com a
frente da página, outro em repouso já com o verso — e resolver a "virada" na
**montagem** (corte seco ou crossfade curto no ffmpeg), não na geração. Zero física
de papel pro Veo/Grok errar, zero conteúdo inventado: cada clipe só precisa
sustentar o que já está na própria imagem.

Use a virada animada apenas quando o movimento em si for o ponto de venda da cena
(ex.: mostrar o material é grosso, várias páginas). Quando o objetivo é só mostrar
duas páginas de conteúdo, dois clipes estáticos + corte é mais barato e mais seguro
que uma virada animada.

**A regra generaliza pra qualquer plano do modo demonstrativo, não só folhear.**
Folha deitada na mesa, folha em pé/segurada, pilha de folhas desfocada com uma em
foco, tela de notebook/celular mostrando a página — cada um desses é um **estado
visual diferente**, e cada um vira **uma imagem própria**, gerada no GPT com a(s)
página(s) real(is) certa(s) anexada(s) como referência daquele estado específico.

Isso vale mesmo quando a composição da imagem tem **várias folhas espalhadas** de
propósito (dá volume, mostra "são 60 guias"): não tem problema nenhum ter 3-4
folhas na mesma foto — o que quebra o vídeo é a folha ENTRAR EM MOVIMENTO sem
imagem de origem pra aquele exato enquadramento. Pra pilha espalhada funcionar:

- Ao montar o prompt de imagem, anexe as páginas reais que vão aparecer legíveis
  naquela composição (a que estiver em foco, pelo menos) — nunca peça "várias
  páginas do guia" sem anexar quais.
- A cena de vídeo gerada a partir dessa imagem é **estática** (repouso, só
  micro-movimento) — não peça ação que mude qual folha está em foco ou que
  reorganize a pilha; isso volta a ser "movimento sem imagem de origem".
- Precisa de outro enquadramento da mesma pilha (outra folha em foco, ângulo
  diferente)? É outra imagem, gerada e aprovada separadamente — mesmo raciocínio
  do verso: o que muda de estado visual pede referência própria.

Segundo defeito possível na mesma cena, causa oposta: o modelo misturou um pouco de
cada página, como se houvesse 2-3 folhas soltas em quadro, ou focou em uma e borrou
o resto. A causa mais provável é a imagem de referência mostrar mais de uma folha
solta, ou a folha entrando em ângulo/dobra que expõe uma segunda superfície — o Veo
não sabe qual delas é o "verso" e tenta desenhar as duas ao mesmo tempo, ou soma
texto de ambas.

Antes de gerar a cena de folhear:

- **A imagem de referência mostra exatamente UMA folha**, plana ou com dobra
  mínima — nunca duas ou três páginas soltas na mesma foto, mesmo que a intenção
  seja mostrar "o material tem várias páginas".
- **Se a cena precisa mostrar o verso**, gere uma imagem própria só pra esse
  estado — a folha já virada, mostrando o conteúdo de trás, foco único e nítido
  — em vez de esperar o vídeo criar esse estado a partir de uma folha vista de
  frente.
- No prompt de vídeo, declare no `CONTINUITY`: `there is exactly ONE sheet of
  paper in frame, single, flat or with a single natural fold — never two or
  three loose sheets, never a blurred mix of two pages`. E no `NEGATIVE`:
  `multiple loose sheets, blended pages, two pages overlapping, out-of-focus
  second page`.
- Se sair errado mesmo assim, não tente "consertar" no vídeo — regere a IMAGEM
  primeiro (fonte da verdade, ver seção seguinte), garantindo folha única em
  foco antes de gastar cota de vídeo de novo.

### Bloco CANON_VOICE — a voz TEM que ser a mesma nas duas cenas

O Grok sorteia uma voz nova a cada clipe. Duas cenas do mesmo criativo com
descrições de voz diferentes — ou vagas — saem com **pessoas diferentes falando**,
e o hook morre: o espectador percebe na hora que é montagem.

Escreva a voz **uma vez**, como um bloco fixo, e cole **literalmente igual, palavra
por palavra**, em todas as cenas daquele criativo. Não reescreva, não resuma, não
"melhore" na cena 2 — qualquer variação de texto muda a voz sorteada.

O bloco precisa fechar seis eixos. Vago em qualquer um deles = voz solta:

```
VOICE: age <idade numérica>, <sexo>, native <idioma + sotaque regional>.
  Pitch: <registro — ex. low chest register, no head voice>.
  Texture: <textura — ex. slightly husky, dry, faint vocal fry at sentence ends>.
  Pace: <ritmo em palavras por segundo + pausas>.
  Energy: <energia — ex. contained and matter-of-fact, never bright, never salesy>.
  Delivery: <entrega — ex. speaking to one person across a table>.
  No echo, no reverb, no processing, no announcer tone.
```

> **NUNCA escreva instrução meta dentro do prompt.** Nada de
> `(identical in every scene of this creative — do not paraphrase)`,
> `same as scene 1`, `keep consistent with the other clip` ou qualquer nota de
> processo. O Grok não tem memória entre gerações: ele lê isso como **texto da
> cena** e a qualidade cai — no caso real que originou esta regra, o clipe saiu com
> a **voz tocando sobre o rosto parado**, e só depois a boca entrava em sincronia.
> A consistência se obtém **copiando o mesmo texto descritivo**, em silêncio.
> Escreva sempre como se aquele clipe fosse o único que existe.

Regras que fazem o bloco valer:

- **Idade numérica**, não "meia-idade". O modelo trata `48` e `40s` como vozes diferentes.
- **Registro e textura explícitos** (`low chest register`, `slightly husky`) — sem
  isso a cena 2 volta ao padrão claro e jovem do modelo.
- **Ritmo em palavras por segundo**, não "natural". "Natural" oscila entre clipes.
- **Sotaque no bloco de voz também**, mesmo já estando no `DIALOGUE`.
- **A mesma imagem de referência de pessoa** nas duas cenas: o Grok deriva timbre
  do rosto. Roupa, luz e idade diferentes na imagem puxam a voz junto.
- **Nunca** descreva emoção diferente entre cenas do mesmo hook (`calm` na 1 e
  `emotional` na 2 vira outra atriz). Se a emoção precisa evoluir, ponha a evolução
  no `ACTION` e mantenha o `VOICE` intacto.

Confira sempre ouvindo as duas cenas em sequência antes de montar. Se destoou,
**regere a cena** — não tem conserto na pós.

### Bloco anti-morphing — obrigatório

Sem isso o modelo faz coisa brotar do nada: objeto aparecendo na mesa, dedo extra, mão virando outra mão, roupa mudando no meio do clipe, fundo se reorganizando. É o defeito que mais queima criativo.

```
CONTINUITY AND PHYSICS: Everything must stay physically consistent and natural
for the entire clip. The scene contains ONLY the objects visible in the reference
image: <liste-os>. No new objects appear, nothing materializes, grows, multiplies
or fades in. Objects keep their exact shape, size, color and position unless the
described action moves them. Hands keep exactly five fingers, correct anatomy,
natural skin, no extra limbs, no fusing, no melting. The face keeps the same
identity, same age, same features throughout — no morphing, no drifting, no face
swap. Clothing, hair and jewelry stay exactly as in the reference image. The
background stays static and stable, no warping, no shifting walls, no sliding
furniture. Real-world physics, natural gravity, natural human motion. Grounded
documentary realism. Vertical 9:16.
NEGATIVE: morphing, warping, melting, extra fingers, extra limbs, deformed hands,
objects appearing out of nowhere, floating objects, duplicated objects, identity
change, face swap, distorted anatomy, surreal artifacts, dreamlike transitions,
glitch, flicker, text overlay, captions, subtitles, watermark, logo, camera whip,
unnatural zoom, background music, unsynced lips.
```

Reforços que valem mais que o bloco em si:

- **Micro-movimento é obrigatório no `ACTION`.** Sem ele o Grok anima só a boca e
  o resto congela — lê como boneco falante e queima o criativo. Uma frase de ação
  principal + uma frase de movimento contínuo. Para cenas de mãos: dedos com peso
  e atrito, pequenas hesitações, punho que se ajusta. Ponha também
  `frozen mannequin stillness, static doll-like body` no `NEGATIVE`.
- **Câmera travada.** `locked-off static camera`. Quanto mais a câmera anda, mais cenário o modelo inventa.
- **Nomear e fechar a lista de objetos** em cena.
- **Preferir 6s quando tem objeto na mão.** A degradação cresce com a duração.
- **Texto escrito em quadro oscila.** Nome ou número manuscrito treme entre frames. Mantenha pequeno, fora do centro, ou mascare na pós.

---

## Disciplina de execução — as cinco falhas que mais custam

Não são bugs de ferramenta. São jeitos de trabalhar que produziram, num único dia,
uma correção que nunca aconteceu, um defeito entregue ao cliente, um lote perdido
numa queda de sessão e um browser preso enquanto outro agente esperava.

### 1. Correção em background não é correção — verifique o ARQUIVO

Um script foi posto em background para regerar uma cena defeituosa "assim que o
lote anterior terminasse". Ele esperou, destravou, e mandou ao Hub o **prompt
antigo**. O relatório da sessão dizia que a correção estava na fila; o arquivo em
disco continuava com data e conteúdo velhos. O dono descobriu abrindo o vídeo.

Regras:

- **Nunca reporte "corrigido" ou "na fila" sem olhar o arquivo.** `ls -la` na data
  de modificação e um frame extraído. Intenção não é resultado.
- **Correção pontual roda em primeiro plano**, acompanhando cada passo. Background
  serve para lote longo e repetitivo, não para conserto.
- Encadear scripts com `while pgrep ...; do sleep; done` é frágil: quando destrava,
  o estado da página já é outro. Prefira rodar em sequência explícita.

```bash
# antes de dizer que trocou:
ls -la VIDEO/cena-8.mp4                       # data tem que ser de agora
ffmpeg -ss 4 -i VIDEO/cena-8.mp4 -frames:v 1 /tmp/check.jpg && <abrir e olhar>
```

### 2. A sessão pode cair — o estado da verdade é o DISCO, não a memória

Uma leva longa atravessa quedas de sessão. Quando isso acontece, **todo job em
background morre sem aviso** e as notificações que você esperava nunca chegam: elas
voltam depois marcadas como `stopped`, sem dizer o que ficou pronto.

Retomar é sempre o mesmo procedimento, na ordem:

```bash
# 1. o que já está montado
for c in $CRIATIVOS; do [ -f "CRIATIVO-$c/CRIATIVO-$c.mp4" ] && \
  echo "$c $(ffprobe -v error -show_entries format=duration -of csv=p=0 CRIATIVO-$c/CRIATIVO-$c.mp4)"; done
# 2. o que tem clipe mas não foi montado
ls CRIATIVO-*/VIDEO/cena-*.mp4 | wc -l
# 3. o que tem imagem mas não tem clipe   (cobertura cena a cena)
# 4. só então decidir o que falta gerar
```

Duas armadilhas na retomada:

- **Arquivo existir não é arquivo certo.** Depois de uma queda, um `.png` no lugar
  esperado pode ser a versão **reprovada** que nunca foi substituída. Confira o
  conteúdo, não o caminho — foi assim que uma imagem descartada quase virou clipe.
- **O browser persiste, a sessão não.** A barra do Hub costuma sobreviver com motor,
  Quality e 9:16 intactos. Confirme com o gate em vez de reconfigurar às cegas.

### 3. Leva longa roda em FILA IDEMPOTENTE — o disco é o checkpoint

Uma leva de 36 cenas leva horas e **vai** atravessar queda de sessão. Aconteceu
duas vezes no mesmo dia. O que decide se você perde o trabalho é como a fila foi
escrita, não a sorte.

Duas propriedades, as duas obrigatórias:

**1. Pule o que já existe.** A fila checa o destino final antes de gerar. Relançar
o mesmo comando depois de uma queda retoma na cena exata, sem regerar nada e sem
gastar cota:

```bash
[ -f "$P/CRIATIVO-$n/VIDEO/cena-$i.mp4" ] && { echo "cena $i ja existe"; continue; }
```

**2. Mova o arquivo para o destino NA HORA.** Nada de acumular em `~/Downloads`
para organizar depois — "depois" é justamente quando a sessão cai, e aí o clipe
existe mas a fila não sabe:

```bash
STAGING="$(LANE_AREA=HUB ~/.claude/bin/lane.sh dir "$LANE")"
/tmp/gen.sh ... && mv "$STAGING/$LANE-$n-$i.mp4" "$P/CRIATIVO-$n/VIDEO/cena-$i.mp4"
```

Com as duas, a recuperação vira uma linha: `scripts/fila.sh`. Sem elas, é
inventário manual do que sobreviveu — e o risco de regerar o que já estava pronto.

A fila também para no primeiro criativo que não fechar as 6 cenas, em vez de
seguir queimando cota contra um teto ou um bloqueio.

Modelo pronto em `scripts/fila.sh`.

### 4. Solte a lane assim que terminar — tem gente na fila

Os browsers são compartilhados entre Claudes. Terminou de gerar imagem? Solte a lane
do `gpt` na hora, mesmo que o vídeo ainda vá levar horas no `hub`:

```bash
~/.claude/bin/lane.sh drop gpt $LANE
~/.claude/bin/browsers.sh status     # confirme que o perfil sumiu da lista
```

Segurar uma lane ociosa é o que produz o roubo de aba do outro lado. E ao pedirem o
browser de volta, **cheque antes se você ainda precisa dele**: numa ocasião a
resposta era "não preciso de nenhuma imagem nova", e o que faltava era só copiar
arquivo já gerado — trabalho de disco, zero navegador.

### 5. Defeito visto no QA é defeito reportado — nunca "deixa passar por cota"

No QA de um criativo apareceu um papel duplicado (um dentro da tigela, outro
brotando na mesa) em 4 de 8 cenas. A decisão foi seguir em frente para poupar
cota, **sem avisar**. O dono achou o mesmo defeito minutos depois, e a regeração
teve que ser feita de qualquer jeito — com a diferença de que agora havia um
criativo montado em cima do material errado.

- Defeito percebido, **fala**. A decisão de aceitar ou regerar é de quem paga a
  veiculação, não de quem monta.
- Economizar cota escondendo defeito **não economiza nada**: o retrabalho vem
  depois, maior, e com a confiança quebrada.
- Nenhum criativo é montado sobre cena reprovada. Corrige antes.
## FASE 5 — Gerar o vídeo

### ⛔ MECÂNICA DO HUB — invoque `hub-video-playwright` ANTES de tocar no browser

<EXTREMELY-IMPORTANT>
Nesta fase você **tem que** invocar a skill `hub-video-playwright` pelo tool
`Skill` antes do primeiro comando de browser. Ela é a fonte única da mecânica:
lane, scroll até a barra, escolha de motor e nível (**Veo 3.1 Quality**, nunca
Lite), proporção 9:16, duração, sequência canônica de envio (apagar texto E
imagem antes de tudo), prompt pelo setter nativo do React, gate de envio, gate de
imagem por hash, rate limit do botão Enviar, Cloudflare, download por conteúdo e
leitura do contador de cota.

**Não improvise seletor e não faça retry rápido no Enviar** — cada clique conta
como requisição e derruba a sessão por um minuto.
</EXTREMELY-IMPORTANT>

O que **esta** skill decide, e a outra apenas executa:

| Decisão | Onde está |
|---|---|
| quantas cenas, que fala, quantas palavras | FASE 1 |
| que imagem cada cena usa | FASE 3 |
| o texto do prompt de vídeo, com os blocos obrigatórios | FASE 4 |
| se o clipe voltou aceitável | QA de clipes, abaixo |
| como emendar e montar | FASE 7 |

Regra de ouro que atravessa as duas: **um criativo por vez, fechado antes do
próximo.** Vídeo é o recurso escasso — a cota do Veo repõe por geração, 24h depois
de cada uma.

## QA de clipes — diagnóstico e gate antes de montar


### 1. Voz tocando com a boca parada (dessincronia por fala longa)

Causa quase sempre a mesma: **o texto não cabia no clipe**. O Grok não acelera a
fala — deixa o áudio correr além da animação. Ver o gate de contagem de palavras na
FASE 1; se você pulou, é aqui que a conta chega.

```bash
# quanto do clipe é fala: se ocupa ~100% da duração, o texto estourou
ffmpeg -i cena-N.mp4 -af silencedetect=noise=-32dB:d=0.3 -f null - 2>&1 | grep silence_
ffprobe -v error -show_entries format=duration -of csv=p=0 cena-N.mp4
```

Fala terminando junto com o último frame, sem respiro no fim, é sinal forte. Confirme
assistindo os últimos 2 segundos. **Não tem conserto na pós: corte o texto e regere.**

Causa secundária, se o texto cabia: **instrução meta dentro do prompt** — ver FASE 4.

### 1b. Corte automático por RMS pega respiração/eco, não o fim real da palavra

Defeito oposto do anterior, e mais traiçoeiro porque **passa despercebido no
QA de imagem e no ffprobe** — só aparece assistindo a transição entre cenas.

O corte de silêncio por RMS (usado pra achar onde a fala de uma cena termina)
mede energia de áudio, não fala. Numa pessoa que "esvai" a voz aos
poucos em vez de calar abruptamente, o resíduo de respiração/eco continua
acima do limiar por 1-2s **depois** que ela já parou de falar e já está
sorrindo de boca fechada. O corte então:

1. inclui esse trecho de sorriso estático antes da transição (parece "sobra
   estranha" no fim do hook);
2. e ao mesmo tempo o corpo (cena seguinte) começa achando que o hook terminou
   ali — quando na verdade a **última palavra da fala nem chegou a ser dita**,
   porque o corte foi medido pelo fim do ÁUDIO alto, não pelo fim da FALA.

Caso real (leva 08-09-MONJE-V2, `CT69/70/71-AR`): o corte automático deu
`[0.30, 7.68]` (7.38s) pro hook de CT69, quando a fala real ("...esconde.")
terminava em torno de **5.75s** — 1.9s de respiração/sorriso incluídos, e a
palavra final cortada no meio porque o corpo já tinha começado antes dela sair.

**Não confie no `silencedetect`/RMS sozinho pra cena de hook curta com fala
terminando perto do fim do clipe.** Depois do corte automático:

```bash
# contact sheet da boca nos últimos 2-3s do hook, pra ver onde a fala PARA de verdade
for t in $(seq 4.5 0.3 7.5); do
  ffmpeg -v error -ss $t -i cena-1.mp4 -frames:v 1 -vf scale=300:-1 /tmp/m$t.jpg -y
done
montage /tmp/m*.jpg -tile 3x3 -geometry 300x+3+3 -background '#111' /tmp/sheet.jpg
```

Olhe o sheet: ache o último frame com boca ainda em movimento de fala (não
sorriso), some ~0.1-0.2s de folga, e use isso como fim do corte manual —
ignore onde o RMS achou que a energia caiu.

### 2. Morphing (objeto duplicando, flutuando, desgrudando)

Frame estático não pega. Amostre ao longo do clipe e olhe a sequência:

```bash
for k in 1 2 3 4 5 6; do
  ffmpeg -v error -ss $(awk -v k=$k 'BEGIN{print k*1.4}') -i cena-N.mp4 -frames:v 1 f$k.jpg
done
montage f?.jpg -tile 6x1 -geometry 180x320+3+3 sheet.jpg
```

Se o objeto muda de posição sem a mão levar, ou aparece um segundo, é morphing. E se
o objeto está "apoiado" onde não se apoia, o defeito é do roteiro — ver a regra de
verossimilhança na FASE 3.

### 3. Clipe de outro criativo

Com vários itens no histórico da conta, é fácil baixar o vídeo errado. Confira a
**pessoa e o ambiente** do frame contra o roteiro daquela cena, não só o prompt
exibido na página.

### O gate de clipes — um sheet por criativo, dois tempos por cena

Olhar "um frame de cada cena" não pega os defeitos que apareceram hoje: papel
duplicado, texto reescrito e degradação de fim de clipe **só existem em parte da
duração**. Amostre no mínimo dois tempos por cena — um no meio e um perto do fim,
que é onde o Veo degrada.

```bash
# faixa inferior (mesa/props) de cada cena, aos 3s e aos 6,8s
for i in $(seq 1 $N); do
  for t in 3 6.8; do
    ffmpeg -v error -ss $t -i cena-$i.mp4 -frames:v 1 \
      -vf "crop=iw:ih*0.45:0:ih*0.55,scale=200:-1" /tmp/z$i-$t.jpg -y
  done
done
montage /tmp/z*.jpg -tile 4x2 -geometry 200x+3+3 -background '#111' /tmp/qa.jpg
```

Recortar a **faixa inferior** é o truque: é onde ficam mesa, props e mãos, e é
onde nascem os objetos duplicados. No quadro inteiro o papelzinho extra some no
meio da imagem.

| Checagem | Como | Defeito real que ela pega |
|---|---|---|
| prop único | sheet da faixa inferior, 2 tempos | 2º papel "11" brotando na mesa |
| superfície escrita intacta | frame do meio, ler o texto | fala impressa no papel |
| fim do clipe limpo | frame a ~0,3s do fim | papel desbotando, roupa mudando |
| mesma voz | **ouvir** as cenas em sequência | b-roll sem rosto com voz sorteada |
| respiro sobrando | `tight.py` em cada cena | pausas de respiração |
| cena é do criativo certo | RMSE frame 0 × imagem de origem | clipe de outro job |

**O tamanho do arquivo é um sinal grátis.** Numa leva de 8 cenas, sete tinham
~4,7 MB e uma tinha 2,3 MB — era justamente a de b-roll sem rosto, a que saiu com
voz diferente. Clipe muito fora da média dos irmãos merece um olhar:

```bash
ls -la cena-*.mp4 | awk '{print $NF, $5}'
```

### Checklist antes de montar

- [ ] Palavras da fala dentro do orçamento (contadas ANTES de gerar)
- [ ] Boca acompanha a fala até o fim, com respiro no final
- [ ] Sem objeto duplicando, flutuando ou desgrudando
- [ ] Sem legenda ou texto queimado na imagem
- [ ] Mesma pessoa, roupa e cabelo das outras cenas do criativo
- [ ] Pessoa e ambiente batem com o roteiro desta cena
- [ ] `r_frame_rate` igual ao dos outros segmentos
- [ ] Superfície escrita em quadro continua com o texto da imagem de referência
- [ ] Cortes revisados por fala e gesto: sem falsa partida ou cauda inútil; pausas com função preservadas. `tight.py` só propõe candidatos.

## FASE 6 — Registrar

Para cada cena, salve `PROMPTS/cena-N.md` com prompt de imagem, prompt de vídeo, duração, modelo e data. Sem isso não dá para reproduzir nem iterar uma cena que ficou quase boa.

---

## FASE 7 — Montagem

**Antes de cortar ou normalizar**, leia [Acabamento natural: áudio, cortes e clareza](references/acabamento-natural-audio-cortes.md). A revisão aprovada do Número Mestre AR/LATAM é o guia para falsas partidas, gestos tardios, ruído, música e diferenças de volume. `tight.py` é detector de candidatos, não aprovação de cortes; preserve pausas com função e confira o master.

### Cortar silêncio — cabeça, cauda E pausas internas

**O motor entrega ar demais.** Cada clipe de 8s do Veo chega com 0,8 a 1,6s de
silêncio sobrando só nas pontas, mais as pausas de respiração no meio da fala.
Num criativo de 11 cenas isso somou **9 segundos de nada** — o dono assistiu e a
primeira coisa que apontou foi "as pausas de respiração ainda aparecem".

Aparar só a cauda **não resolve**: as pausas internas são a maior parte do
problema. Numa medição real, o mesmo criativo tinha **20 silêncios** com
`d=0.35` depois de aparado só nas pontas, e **3** depois do corte completo.

**Padrão (quando houver `ELEVENLABS_API_KEY`): corte por palavra no video-use.**
`silencedetect` mede "onde há som", e o Veo enche o fim do clipe de som que não é
fala (ver "Fim da fala" abaixo). O transcript Scribe dá a fronteira de cada palavra,
então o corte nunca come sílaba nem deixa sorriso sobrando:

```bash
VU=~/Developer/video-use; PY=$VU/.venv/bin/python
# 1. transcreve cada cena (cacheado em VIDEO/edit/transcripts/<cena>.json)
for i in $(seq 1 $N); do $PY $VU/helpers/transcribe.py VIDEO/cena-$i.mp4 --language pt; done
$PY $VU/helpers/pack_transcripts.py --edit-dir VIDEO/edit     # -> VIDEO/edit/takes_packed.md
# 2. monte VIDEO/edit/edl.json: um range por trecho falado, borda na palavra
#    (padding 30–200 ms, calibrado por fala e gesto; não use cauda fixa de 0,30 s)
# 3. renderiza: corta por trecho, fade de 30ms em cada junção, concat, fps nativo
$PY $VU/helpers/render.py VIDEO/edit/edl.json -o VIDEO/edit/preview.mp4 --preview --no-subtitles
$PY $VU/helpers/render.py VIDEO/edit/edl.json -o FINAL-sem-legenda.mp4 --no-subtitles --no-loudnorm
```

`edl.json` (formato do video-use):

```json
{"version": 1,
 "sources": {"cena-1": "/abs/VIDEO/cena-1.mp4", "cena-2": "/abs/VIDEO/cena-2.mp4"},
 "ranges": [
   {"source": "cena-1", "start": 0.26, "end": 2.90, "beat": "HOOK", "quote": "...", "reason": "..."},
   {"source": "cena-1", "start": 3.05, "end": 6.95, "beat": "HOOK", "quote": "...", "reason": "pausa interna cortada"},
   {"source": "cena-2", "start": 0.18, "end": 5.40, "beat": "BODY", "quote": "...", "reason": "..."}]}
```

- `--no-subtitles`: a legenda é a camada final no Remotion (canônica), não o SRT/ASS do video-use.
- `--no-loudnorm`: o render.py normaliza pra -14 LUFS por padrão; aqui o nível
  final sai do mix calibrado (E.4), então desligue e deixe o mix decidir.
- Não passe `--fps`: sem ele o render preserva o fps da fonte (Veo = 24), que é a regra.
- Uma cena que veio em resolução diferente continua precisando da normalização
  1080×1920 **antes** (seção "ANTES do concat" abaixo) — não testado se o render.py
  cobre isso sozinho.
- Os mesmos transcripts servem pro "Fim da fala" e pra caça de repetição do Veo,
  mais abaixo — uma transcrição por cena, nunca duas.

Status: helpers conferidos (`--help`) em 2026-09-23; o fluxo inteiro ainda **não
rodou num criativo real** desta skill. No primeiro uso, compare o resultado com o
`montar.sh` no mesmo material antes de trocar de vez.

**Fallback (sem key, ou se o video-use falhar): `scripts/tight.py`** — ele lê o
`silencedetect` e devolve candidatos. Revise fala, repetição, música e gesto antes de aprovar qualquer trecho:

```bash
python3 scripts/tight.py cena-1.mp4
# 0.360 2.747
# 3.111 6.653
# 7.218 7.712
```

Parâmetros no topo do arquivo, calibrados em produção:

| Constante | Valor | O que faz |
|---|---|---|
| `HEAD_PAD` | 0.10 | respiro antes da primeira sílaba |
| `TAIL_PAD` | 0.30 | respiro depois da última |
| `MINGAP` | 0.30 | pausa acima disso é cortada |
| `MAXGAP` | 0.16 | o que sobra da pausa cortada |

Trechos com menos de 0,35s são descartados — clipe de 0,1s quebra o encode e o
erro que aparece é enganoso (reclama do `-ss` da linha seguinte).

**O jump cut aqui é a estética, não um defeito.** Os criativos-modelo deste nicho
são cortados assim; ritmo frouxo é que destoa. Só preserve a pausa quando ela for
dramática de propósito.

`scripts/montar.sh <dir-criativo> <n-cenas> <saida.mp4>` faz tudo: corta, faz
upscale para 1080x1920, normaliza no fps nativo e concatena pelo filtro.
(Fallback. Atenção: o `montar.sh` fixa `-r 24` — em cena de outro motor, ajuste.)

### `ffmpeg` come o stdin do loop — sempre `-nostdin`

Bug que corrompe a montagem **em silêncio** e é dificílimo de ler pelo erro.
Dentro de `while read ... done < <(...)`, o `ffmpeg` lê o mesmo stdin e engole as
linhas restantes. A primeira cena sai certa e da segunda em diante os tempos
chegam truncados ou vazios:

```
Invalid duration for option ss: .360      # o "0" sumiu — linha meio consumida
Invalid duration for option to:           # linha inteira consumida
```

O erro aponta para o valor, então se perde tempo procurando bug de formatação
numérica ou de locale. A causa é o stdin.

```bash
ffmpeg -nostdin -v error -ss "$a" -to "$b" -i cena-$i.mp4 ...
```

Regra: **todo `ffmpeg` dentro de laço que lê linhas leva `-nostdin`.**

### Upscale + normalização

```bash
VF="scale=1080:1920:flags=lanczos,unsharp=5:5:0.7:5:5:0.0,fps=30,format=yuv420p"
ffmpeg -ss <ini> -to <fim> -i cena-N.mp4 -vf "$VF" \
  -c:v libx264 -crf 18 -preset slow -c:a aac -b:a 192k -ar 48000 -ac 2 -y s<N>.mp4
```

Acelerar uma cena arrastada (vídeo e voz juntos, sem subir o tom):

```bash
ffmpeg -i cena.mp4 -vf "setpts=PTS/1.3,$VF" -af "atempo=1.3" ... -y saida.mp4
```

Se a cena não tem boca em quadro, dá para acelerar só o vídeo e deixar a voz no ritmo natural.

### Voz robótica = fala longa demais. O teto do Veo é 16 palavras.

Quando o texto não cabe no clipe, o Veo **não corta a fala: ele acelera**. O
resultado soa sintético, "robótico do nada", e nenhuma métrica técnica acusa — o
arquivo fica perfeito, só a voz é que está comprimida.

Medido em produção, no mesmo criativo:

| Fala | Ritmo resultante | Resultado |
|---|---|---|
| 20 palavras | 2,82 pal/s | robótica |
| 18 palavras | 2,56 pal/s | robótica |
| 18 palavras (ocupa os 8s) | 2,25 pal/s | **cortada no fim**, sem respiro |
| 17 palavras | 2,29 pal/s | natural |

**O Veo fala mais devagar que o Grok** — ~2,2 pal/s contra 2,5. Não reaproveite a
régua de um motor no outro.

| Motor | Clipe | Teto real |
|---|---|---|
| **Veo 3.1** | 8s | **16 palavras** |
| Grok | 10s | 22 palavras |
| Grok | 6s | 13 palavras |

Depois de gerar, confirme que a fala terminou **antes** do fim do clipe:

```bash
# tem que sobrar respiro: fim da fala < duracao - 0.5s
ffmpeg -i clipe.mp4 -af silencedetect=noise=-34dB:d=0.35 -f null - 2>&1 | grep -oP 'silence_start: \K[0-9.]+' | tail -1
ffprobe -v error -show_entries format=duration -of csv=p=0 clipe.mp4
```

Se não houver nenhum `silence_start`, a fala foi até o último frame: **o texto
estourou**. Encurte e regere — a montagem não conserta.

**Antes de condenar o clipe, repita a -28dB.** O Veo entrega ruído de sala audível,
e a -34dB esse room tone conta como som: o `silencedetect` não acha silêncio nenhum
e o clipe parece estourado quando não está. Num clipe real, `-34dB` não devolveu uma
linha sequer, e `-28dB:d=0.2` mostrou a fala terminando em **6,0s de 8,0s**, com
1,9s de respiro.

```bash
# checagem primária
ffmpeg -i clipe.mp4 -af silencedetect=noise=-34dB:d=0.35 -f null - 2>&1 | grep silence_
# se vier VAZIO, confirme antes de regerar:
ffmpeg -i clipe.mp4 -af silencedetect=noise=-28dB:d=0.2 -f null - 2>&1 | grep silence_
```

Só é estouro de verdade quando **as duas** passagens não acham silêncio no fim.
Regerar por leitura errada do limiar gasta cota à toa.

### O Veo degrada DEPOIS que a fala acaba — corte ali, não regere

Quando a fala termina antes dos 8s, o modelo precisa preencher o resto e é aí que
ele inventa: a pessoa baixa o objeto, o texto escrito desbota, a roupa muda, um
microfone de lapela aparece. O miolo do clipe está perfeito.

Caso real: cena regerada saiu com o papel correto e, a partir de ~6,3s — depois do
fim da fala em 6,75s — as primeiras linhas do papel começaram a apagar e o suéter
mudou de textura. Regerar de novo custaria cota e provavelmente repetiria o
padrão, porque a causa é estrutural.

**A correção é o corte, não a regeração:**

```bash
# 1. onde a fala termina de fato
ffmpeg -i clipe.mp4 -af silencedetect=noise=-28dB:d=0.12 -f null - 2>&1 | grep -oP 'silence_start: \K[0-9.]+' | tail -1
# 2. corte logo depois disso
ffmpeg -nostdin -v error -ss 0 -to 6.80 -i clipe.mp4 -c:v libx264 -crf 18 -preset slow -r 24 \
  -c:a aac -b:a 192k -ar 48000 -ac 2 -y cena-N.mp4
```

Antes de condenar um clipe, **amostre o fim** (`-ss <dur-1.5>`, `-ss <dur-0.3>`).
Se o defeito só existe depois da última sílaba, é corte de 10 segundos — não uma
geração nova.

### NUNCA force fps — respeite o nativo do motor

O Veo entrega **24fps**. Forçar `fps=30` na normalização **duplica frames de forma
irregular** e o clipe fica com travadinho (judder) perceptível, sobretudo em
movimento de mão e cabeça. Nenhum `ffprobe` acusa: o arquivo fica 30fps certinho.

```bash
# descobre o fps nativo ANTES de normalizar
ffprobe -v error -select_streams v -show_entries stream=r_frame_rate -of csv=p=0 clipe.mp4
```

Normalize mantendo o nativo — sem `fps=` no filtro, e `-r` igual ao de origem:

```bash
ffmpeg -ss 0 -to $end -i clipe.mp4 \
  -vf "scale=1080:1920:flags=lanczos,format=yuv420p" \
  -c:v libx264 -crf 18 -preset slow -r 24 \
  -c:a aac -b:a 192k -ar 48000 -ac 2 -y sN.mp4
```

### Concat de cenas com fps diferente: o fps do CRIATIVO é o do motor, o resto se adapta

Cenas geradas em motores diferentes (Veo 24fps, outra fonte 30fps) dentro do
mesmo criativo. Uma tem que ceder, e a escolha não é opinião — se mede:

```bash
# para cada candidato: total de frames vs frames únicos
tot=$(ffprobe -v error -select_streams v -show_entries stream=nb_frames -of csv=p=0 x.mp4)
uni=$(ffmpeg -i x.mp4 -vf mpdecimate -f null - 2>&1 | grep -oP 'frame=\s*\K[0-9]+' | tail -1)
```

Medido num hook real de 8s:

| Caminho | Hook | Veredito |
|---|---|---|
| forçar tudo a **30** (converte o hook 24→30) | 240 total / **173 únicos** = **67 frames duplicados** | judder |
| manter **24** (converte o body 30→24) | 192 total / 173 únicos, nativo | limpo |

O detalhe que fecha a questão: o hook tem **173 frames únicos nas duas versões**. Subir
para 30 não acrescenta informação nenhuma, só duplica — e a duplicação cai justamente
no hook, que é a parte que segura a atenção no feed.

Portanto: **o criativo inteiro sai no fps do motor (Veo = 24), e o body é reamostrado
para esse fps.** O body perde frames numa conversão real de taxa, que é bem menos
visível que padrão de duplicação. Nunca o contrário.

Todos os clipes do mesmo criativo precisam do **mesmo** fps antes do concat — mas
esse fps é o do motor, não 30 por hábito. Verifique que não sobrou frame duplicado:

```bash
# frames unicos tem que bater com o total
ffmpeg -i FINAL.mp4 -vf mpdecimate -f null - 2>&1 | grep -oP 'frame=\s*\K[0-9]+' | tail -1
ffprobe -v error -select_streams v -show_entries stream=nb_frames -of csv=p=0 FINAL.mp4
```

### ANTES do concat: normalize TODA cena pra 1080x1920 — cenas de resoluções diferentes DISTORCEM o vídeo inteiro

Erro real (2026-09-09): um vídeo saiu com a pessoa **esticada horizontalmente**,
tipo espelho deformado — não era morphing do Veo, era montagem. Cada cena de um
mesmo criativo pode voltar do Hub numa resolução diferente (720×1280, 1080×1920,
e às vezes até **1920×1080 paisagem** por engano de engine/fallback) — motores e
fallbacks diferentes entregam tamanhos diferentes, e nada nisso aparece no
`ffprobe` de forma óbvia se você só olhar duração.

**Concatenar cenas com resolução diferente sem normalizar produz um vídeo final
com o canvas do PRIMEIRO clipe, e as cenas seguintes espremidas/estiradas para
caber ali** — silenciosamente, sem erro no ffmpeg. Uma cena paisagem (1920×1080)
misturada com cenas retrato (1080×1920) é o caso mais visível, mas **duas cenas
retrato de tamanhos diferentes** (720×1280 vs 1080×1920) já basta pra distorcer.

Confira as dimensões de TODAS as cenas antes de montar:

```bash
for i in 1 2 3; do ffprobe -v error -show_entries stream=width,height -of csv=p=0 VIDEO/cena-$i.mp4; done
```

Se não bater 100% entre todas, normalize cada cena **antes** do concat — nunca
confie que "todas são 9:16" só porque a proporção parece certa em cada uma:

```bash
VF="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1"
ffmpeg -y -i cena-N.mp4 -vf "$VF" -c:v libx264 -crf 18 -preset fast normN.mp4
```

`force_original_aspect_ratio=increase` + `crop` cobre o quadro inteiro e recorta
a sobra (nunca deixa barra preta) — funciona tanto pra ajustar 720×1280→1080×1920
quanto pra "salvar" uma cena que veio paisagem por engano, recortando pro centro
em vez de esticar. Rode isso **sempre**, mesmo quando as cenas parecem OK —
o defeito só aparece assistindo o vídeo final, não em nenhum comando de checagem
rápida.

### Concat: use o FILTRO, não `-c copy`

`-c copy` emenda os arquivos sem realinhar os frames de áudio. O vídeo fica certo e
**o áudio sai picotado nas junções** — estalo audível a cada troca de cena. Só se
percebe ouvindo; nenhum `ffprobe` acusa.

```bash
ffmpeg -i q1.mp4 -i q2.mp4 -i q3.mp4 -i q4.mp4 \
 -filter_complex "[0:v][0:a][1:v][1:a][2:v][2:a][3:v][3:a]concat=n=4:v=1:a=1[v][a]" \
 -map "[v]" -map "[a]" -c:v libx264 -crf 18 -preset slow \
 -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart -y FINAL.mp4
```

Reencoda, mas é o único jeito de emendar áudio limpo. Confira depois:

```bash
# só devem sobrar as pausas naturais entre cenas, nenhum estalo
ffmpeg -i FINAL.mp4 -af silencedetect=noise=-40dB:d=0.25 -f null - 2>&1 | grep silence_
```

### A ordem do histórico do Hub é CRESCENTE — não inverta

`document.querySelectorAll('video')[0]` é o clipe MAIS ANTIGO, não o mais novo.
Inverter a lista monta o criativo de trás para frente, e isso passa por qualquer
checagem técnica: resolução, fps e duração ficam corretos, as cenas é que estão
trocadas.

**Confirme por conteúdo, não por posição.** Cada clipe começa na imagem que o
gerou, então casar frame 0 contra as imagens de referência resolve:

```bash
for n in 1 2 3 4; do ffmpeg -v error -ss 0.1 -i clipe-$n.mp4 -frames:v 1 -vf scale=200:-1 /tmp/v$n.png; done
for n in 1 2 3 4; do magick IMG/cena-$n.png -resize 200x /tmp/i$n.png; done
for v in 1 2 3 4; do for i in 1 2 3 4; do
  echo "v$v vs i$i: $(magick compare -metric RMSE /tmp/v$v.png /tmp/i$i.png null: 2>&1 | grep -oP '^[0-9.]+')"
done; done
# menor RMSE de cada linha = a cena daquele clipe
```

### Concat

Todos os trechos precisam ter mesma resolução, fps, codec e taxa de áudio — normalize antes.

```bash
printf "file '%s'\nfile '%s'\n" /abs/s1.mp4 /abs/s2.mp4 > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy -y HOOK-1.mp4
```


### Fim da fala: use a ÚLTIMA PALAVRA (transcript), não `silencedetect`

`silencedetect` responde "onde há som", não "onde há fala". No Veo os dois divergem
sempre, porque o modelo **preenche o resto do clipe depois que a fala acaba** — e o
que ele põe ali (respiração, riso, um "hmm", roupa roçando) é som audível.

Medido num hook real de 8s: a última palavra terminava em **4,94s**, e o
`silencedetect` apontava o último início de silêncio em **6,92s**. Cortar por ele
deixava **2 segundos de sorriso** no fim do hook — exatamente o trecho que o corte
existia para remover.

Com o transcript Scribe da cena (o mesmo do corte, ver FASE 7 acima), o fim da
fala sai de graça — whisper está proibido (regra do dono):

```bash
VU=~/Developer/video-use
$VU/.venv/bin/python $VU/helpers/transcribe.py "$CLIP" --language pt   # cacheado
T=$(dirname "$CLIP")/edit/transcripts/$(basename "$CLIP" .mp4).json
END=$(python3 -c "import json,sys;w=[x for x in json.load(open(sys.argv[1]))['words'] if x.get('type','word')=='word'];print(round(w[-1]['end'],2))" "$T")
CUT=$(awk -v e="$END" 'BEGIN{print e+0.15}')               # ponto de partida; valide fala/gesto
```

O mesmo vale para o **início**: `start` da primeira palavra `- 0.15` apara a cabeça
sem cortar a primeira sílaba. Sem key do ElevenLabs, volte ao `silencedetect` a
`-28dB` e **amostre o fim no olho** (frames em `END`, `END+0.5`, `END+1`) antes de cortar.

Jeito antigo (faster-whisper local): ver `references/SKILL-ffmpeg-OLD-2026-09-23.md`
§"Fim da fala: use a ÚLTIMA PALAVRA (whisper)".

`silencedetect` continua útil para o que ele de fato mede: detectar que a fala
**estourou** o clipe (nenhum silêncio no fim = texto longo demais, regere) e cortar
pausas internas na montagem.


### Fala CURTA demais: o Veo REPETE a frase para preencher o clipe

O teto de 16 palavras protege contra fala longa (voz acelerada, boca parada, legenda
queimada). Mas existe o defeito oposto, e ele é mais difícil de ver: **fala curta
demais num clipe de 8s faz o Veo repetir a frase inteira.**

Caso real (leva 29-08): fala de 13 palavras, `"Si todos los meses terminás en la misma
cuenta, esto es para vos."` O clipe voltou com:

```
Si todos los meses terminás en la misma cuenta, esto es para vos, esto es para vos.
```

A repetição começou em 5,86s e a primeira ocorrência terminava em **4,82s**. Nada no
`ffprobe` acusa: 8,00s, áudio normal, lip-sync correto — o modelo dubla a repetição
direitinho. E o QA por frames não pega, porque a imagem está perfeita. **Só se pega
lendo a transcrição**, e o dono do anúncio pegou antes de mim.

Pior: o corte pela última palavra (a regra da seção anterior) **mantém as duas** —
ele corta em 6,82s, que é o fim da repetição.

**Faixa segura de fala para o Veo em 8s: 11 a 16 palavras.** Abaixo de ~11 o risco de
repetição sobe; acima de 16 a voz acelera. Escreva dentro da faixa.

**No QA, procure repetição na transcrição** — não em frames. `words` = as palavras
do transcript Scribe da cena (`[x for x in json['words'] if x.get('type','word')=='word']`,
chaves `text`/`start`/`end`):

```python
norm = [re.sub(r"[^\w]", "", x["text"]).lower() for x in words]
for L in range(min(8, len(words)//2), 2, -1):
    for i in range(len(norm) - 2*L + 1):
        if norm[i:i+L] == norm[i+L:i+2*L] and norm[i]:
            fim = words[i+L-1]["end"]    # corta no fim da PRIMEIRA ocorrencia
```

Achou repetição? **Não regere** — corte no fim da primeira ocorrência. O trecho até
ali está perfeito, e a regeração pode repetir o padrão, porque a causa é estrutural:
sobra tempo no clipe.

Deixe o aviso visível no log da montagem. Defeito silencioso que ninguém vê é defeito
que chega ao cliente.

### Toda cena é a MESMA pessoa em quadro falando — não peça edição ao modelo

Não peça ao Veo variação de enquadramento, insert de mãos, close de prop ou
qualquer "dinâmica de edição". Cena a cena, sempre o mesmo plano: a pessoa sentada
de frente, falando. É o formato que sai limpo.

Medido numa leva de 6 criativos: as cenas com enquadramento diferente (mãos na
carteira, mãos escrevendo, close do celular) trocaram a personagem ou a voz em
**4 criativos**. As cenas de plano fixo com rosto não deram um defeito.

Split, PiP, corte seco, tarja — tudo isso é **pós-produção** no Remotion (ou
Hyperframes, se o criativo já tem motion lá; ver E.3), aplicada sobre cenas uniformes. Não é coisa que se pede na geração.

### Legenda, motion, trilha — Remotion (legenda), Hyperframes (motion), ffmpeg (mix)

O Grok já entrega voz, então música é opcional e fica baixa. Legenda queimada só na pós, casando com o estilo do criativo vencedor. Ver skills `remotion-create`, `remotion-captions` (**menos** a parte de transcrição: ela usa whisper.cpp, proibido — os timestamps vêm do Scribe/TTS, ver Stack de edição), `remotion-render`.

Legenda **animada** além do karaokê (palavra que entra com motion, destaque que
cresce, texto que interage com o sujeito): Hyperframes — skills `embedded-captions`
+ `captions-overlay` (doutrina: legenda é overlay por cima, nunca faixa reservada).
Mesma regra de timestamp: entregue o `transcript.json` pronto, não rode o
`hyperframes transcribe` delas.

#### ⭐ LEGENDA KARAOKÊ TIKTOK — CANÔNICA v2 (padrão fixo do dono, 2026-09-23)

Por que v2: a v1 (`references/legenda-karaoke-tiktok-v1-OLD.jsx`) tinha três defeitos
que o dono apontou: (1) **não acompanhava a fala** — timestamps de whisper/distribuição
por duração, grudados um no outro, legenda ficava na tela nas pausas; (2) **borda
grotesca** — `WebkitTextStroke` fica centrado na borda da letra, come o desenho e
serrilha as quinas, e o chroma-key do fundo `#0000FF` deixava halo; (3) **pequena e
chapada**, sem profundidade. Aprovado visualmente em `mapa-do-tarot/criativos/v4_imperatriz_KARAOKE-V2.mp4`.

**Passo 1 — tempo de cada palavra: `scripts/legenda_align.py` (alinhamento forçado, NÃO whisper).**
A gente sempre tem o texto falado (roteiro/prompt do Veo/texto do TTS). O alinhador
(wav2vec2/MMS via `ctc-forced-aligner`, local, grátis, CPU ~45s pra 30s de áudio)
só descobre ONDE cada palavra do roteiro cai no áudio — não adivinha palavra, então
não erra texto nem deriva no tempo. Venv pronta em `~/Developer/legenda-karaoke`:

```bash
~/Developer/legenda-karaoke/.venv/bin/python ~/.claude/skills/criativo-ads-video-orq/scripts/legenda_align.py \
  final_sem_legenda.mp4 roteiro.txt -o src/words.json        # --lang por (padrão)
```

- `roteiro.txt` = EXATAMENTE o que é falado, na ordem, com pontuação (pontuação quebra linha).
  Se o Veo improvisou/trocou palavra, corrija o roteiro pro que foi dito de fato.
- Números viram extenso só pro alinhamento ("78" alinha como "setenta e oito"), exibição fica "78".
- Saída: linhas de 1-3 palavras, quebra em pontuação e em pausa >0,30s; linha só existe
  enquanto é falada (+0,15s); **nas pausas a tela fica limpa**. Palavra ativa não pisca
  em gap <0,30s.
- Rodar no vídeo **montado final** (tempo da saída), não nos clipes soltos.
- Ele imprime palavras de confiança baixa: confira essas no vídeo.
- Alternativa paga equivalente: Scribe do video-use (precisa `ELEVENLABS_API_KEY`).
- Proibido: `hyperframes transcribe` (whisper `small.en`, só inglês), faster-whisper, whisper.cpp,
  `remotion-captions` com install-whisper-cpp, e "distribuir por duração".

**Passo 2 — render: `references/legenda-karaoke-tiktok-CANONICA.jsx` (componente `KaraokeV2`).**
Vídeo e legenda na MESMA composição Remotion (`<OffthreadVideo>` + legenda por cima) —
**sem fundo #0000FF, sem chroma-key, sem overlay ffmpeg**. Composição com o fps nativo
do vídeo (Veo = 24, montado pode ser 25) e 1080×1920. Precisa `@remotion/google-fonts`
na mesma versão do `remotion`. Projeto de referência pronto:
`mapa-do-tarot/criativos/BR/CRIATIVO-1/intermediarios/remotion-cap` (composição `KaraokeV2`,
vídeo em `public/`).

| Parâmetro | Valor |
|---|---|
| Fonte | **Montserrat 900** (`@remotion/google-fonts/Montserrat`), caixa alta, `letterSpacing 0.5px` |
| `fontSize` | **60** (canvas 1080×1920) |
| Posição | **centro vertical em 70% da altura** (`top: height*0.70`, `translateY(-50%)`) — centra igual com 1 ou 2 linhas, dentro da banda 4:5, fora do rodapé |
| Largura | `left 4%`, `width 92%`, flex-wrap centralizado, `gap 0 26px`, `lineHeight 1.25` |
| Cor base / ativa | `#FFFFFF` / `#FFD400` — SÓ a palavra sendo falada fica amarela |
| Contorno | **anel de 24 `text-shadow` de 5px, preto** — redondo, todo por FORA da letra (nunca `WebkitTextStroke`) |
| Profundidade | `0 7px 0 #000` (extrusão) + `0 10px 14px rgba(0,0,0,.55)` (sombra) |
| Pop | palavra ativa escala ~1,05 com `spring` (damping 12, stiffness 220) — o gap 26px absorve; não aumente o pop sem aumentar o gap (senão as palavras grudam: "IMPERATRIZSÓ") |
| Chunk | 1-3 palavras, vem pronto do `legenda_align.py` |

`words.json`: `[{ start, end, words: [{ text, start, end }] }, ...]`.

Jeito antigo (v1: Arial + WebkitTextStroke + chroma `#0000FF`, tamanhos 34/72): ver
`references/legenda-karaoke-tiktok-v1-OLD.jsx` e `references/SKILL-ffmpeg-OLD-2026-09-23.md`.

QA obrigatório: extrair frames em tempos de fala e provar que existe UMA palavra
`#FFD400` E que a posição do amarelo MUDA entre frames (karaokê real, não amarelo
fixo). Amarelo ausente ou estático = FAIL.

#### Fallback — legenda sem Remotion (ffmpeg puro): padrão validado da VSL2-MARTA

Só fallback: o padrão é o karaokê canônico acima. (O `render.py --build-subtitles`
do video-use cai nesta mesma classe — SRT/ASS queimado — e serve só aqui.)
Quando não há pipeline Remotion montado pro projeto (caso comum de VSL gerada
via `hub-video-playwright` + montagem própria em ffmpeg), reproduza o estilo
aprovado da VSL2-MARTA em vez de inventar um novo:

- **Fonte Inter Bold, sem itálico.** Itálico fino (ex. Georgia) foi tentado numa
  VSL e reprovado pelo usuário — pareceu fraco/errado comparado ao padrão.
- **Amarelo `#FFD21E`** (ASS: `&H001ED2FF`), contorno preto fino, sem fundo.
- **Fonte fina + linha larga, não fonte grande + linha curta.** São duas
  variáveis independentes e fáceis de confundir: "tá grosso/enorme" pede
  `FontSize`/`Outline` menores; "não preenche o espaço, fica um bloco
  centralizado sobrando lateral" pede `MAXCH` maior e `MarginL`/`MarginR`
  menores. Valores validados no monge (VSL-MONGE, 2026-09-08), depois de
  passar por "grosso demais" (FontSize=17) e "fino demais, pouca largura"
  (FontSize=12 com MAXCH=34):

  ```python
  MAXCH = 56  # char por linha antes de quebrar
  style = (
      "FontName=Inter,FontSize=10,Bold=1,Italic=0,"
      "PrimaryColour=&H001ED2FF,OutlineColour=&H00000000,BackColour=&H00000000,"
      "BorderStyle=1,Outline=1.0,Shadow=0.4,Alignment=2,MarginV=100,MarginL=15,MarginR=15,WrapStyle=0"
  )
  ```

  2 linhas por cue, tempos distribuídos proporcionalmente por caractere dentro
  da janela de fala da cena. Isso é ponto de partida, não valor fixo — confirme
  sempre extraindo um frame antes de aceitar como pronto (ver abaixo).
- **Posição embaixo, nunca no meio nem cobrindo boca/rosto.** Em 1080×1920 via
  filtro `subtitles` do ffmpeg: `MarginV≈100` (distância da base), dentro da
  faixa "que não corta" descrita abaixo.
- Implementação de referência (gera SRT chunked + queima via
  `ffmpeg -vf subtitles=...:force_style=...`, sem precisar de Remotion):
  `PERSONAGENS/MONGE/VSL-MONGE/TOOLS/gen_captions2.py` no projeto NUMERO-MESTRE.
  Copie e adapte (troca só o dict de falas e a lista de durações por cena) em
  vez de reescrever o estilo do zero.
- **Sempre compare contra um frame do vídeo de referência aprovado** (ex.:
  `PERSONAGENS/MARTA/VSL2-MARTA/VIDEO/VSL2-MARTA-legenda.mp4`) antes de dar como
  pronta — a primeira tentativa raramente bate no tamanho/posição certos de
  primeira, e o usuário nota na hora se destoar do padrão já validado.

#### Legenda mora na área que não corta — regra fixa

Todo vídeo final é 1080 × 1920. A legenda **nunca** encosta nas faixas que a
plataforma cobre ou corta:

- **Topo: 290 px livres.** Nome de perfil e notificações no Stories; corte no feed.
- **Base: 360 px livres.** Legenda da plataforma, nome do áudio, botões, "seguir".
- **Laterais: 60 px**, atenção redobrada à direita (botões de interação).

Isso deixa a legenda dentro de uma **caixa viva de 960 × 1270 px centralizada** — a
mesma do prompt 07 da skill `modelagem-escalados`, porque o feed recorta um 9:16
para 1080 × 1350 centralizado. Na prática: a linha de legenda assenta com a base
entre ~1300 px e ~1560 px do topo, nunca abaixo disso.

Duas armadilhas medidas em produção:

1. **Legenda de duas linhas cresce para cima, não para baixo.** Ancore a caixa pela
   base, senão a segunda linha invade a faixa dos 360 px.
2. **Legenda que "não pula"** — largura fixa e base fixa. Legenda que muda de altura
   a cada frase denuncia automação e cansa o olho. Ver a memória de pós-produção do
   projeto AstroDicas (1.15x, corte de respiração, legenda dourada estável).

#### Acelerar é padrão, não opcional

**Todo criativo final acelera na pós-produção — sempre, em todos os modos.** É o
que faz a fala soar mais rápida e a peça não arrastar; sem isso o ritmo fica de
vídeo institucional, não de anúncio. Acelere o pré-final inteiro (vídeo + áudio
juntos, `setpts`+`atempo`, nunca só um dos dois — descasa lip-sync). Confirme a
legenda depois de acelerar: tempo de cena muda, ponto de troca de frase muda
junto.

- **Com personagem falando em quadro (lip-sync gerado no Veo): 1.10x a 1.20x.**
  Acima disso a boca visivelmente descasa da voz.
- **100% narração off / b-roll / gravação de tela (sem boca sincronizada pra
  proteger): 1.30x a 1.40x.** Testado em produção — 1.20x ficou lento demais
  pro ritmo de criativo demonstrativo; sem lip-sync, o teto sobe.
  Exceção aprovada: VO de TTS já em ritmo de anúncio (MiniMax, Mapa do Tarot) →
  **1.15x** é o ponto (dono, 2026-09-23: 1.25x ficou rápido demais). Acelere NO REMOTION: composição
  que roda o render final via `<OffthreadVideo playbackRate={1.15}>`,
  `durationInFrames = ceil(dur*fps/1.15)` — vídeo, voz e karaokê queimado andam juntos,
  pitch preservado (confira F0 antes×depois; tem que ficar ~igual, não +15%).

#### Tarja de marca — OPT-IN, não é mais padrão (regra da dona, 2026-10-04)

⚠️ **Mudança 2026-10-04: a tarja deixou de ser automática em qualquer modo.**
Antes desta data era obrigatória nos Modos A-D; a dona reportou que toda
entrega está saindo com a faixa vermelha sem ter sido pedida e não quer isso
por padrão. **A tarja só entra se o brief daquele criativo pedir
explicitamente.** Sem pedido explícito, nenhum criativo (A, B, C, D ou E) leva
tarja — e isso vale também pro Modo E, que já não usava por outro motivo (ver
§E.2b).

Quando o usuário pede ("quero a faixa com o nome do produto", "bota tarja"),
siga as regras abaixo. Fora isso, pule esta seção inteira.

Toda peça **que pedir tarja** leva uma **tarja sólida vermelha, letra branca, com o nome do
produto**, fixa na área que não corta (topo ou base da caixa viva de
960 × 1270 px, nunca dentro dela por cima da legenda de fala — são duas coisas
diferentes, não competem pelo mesmo espaço).

- **Onde:** topo (abaixo dos 290px livres) OU base (acima dos 360px livres) —
  escolha um lado e mantenha em todo o criativo, nunca alterna.
- **O quê:** nome do produto/oferta, curto — não é headline nem CTA, é
  identificação de marca visível o tempo todo.
- **Cor:** fundo vermelho sólido, texto branco, alto contraste — não é a legenda
  de fala (essa segue o estilo do criativo vencedor); a tarja é elemento fixo,
  a legenda de fala é dinâmica por frase.
- **Presença:** do primeiro ao último frame, ou pelo menos do fim do hook até o
  CTA — nunca só num flash de 1-2s, senão ninguém lê.

**Referência canônica (validada, print salvo em produção):** faixa vermelha com
borda rasgada (efeito "papel picado"), texto branco em caixa alta, 2-3 linhas,
sentada exatamente **na costura do Meio a meio** — onde o bloco de cima (tela:
planilha, dashboard, gravação) encontra o bloco de baixo (pessoa em quadro
falando). No bloco de cima ainda cabe uma **miniatura pequena no canto superior
direito** (a mesma pessoa, reagindo) — três camadas visuais ao mesmo tempo:
tela grande, rosto pequeno reagindo, faixa de manchete no meio, pessoa falando
embaixo com legenda própria (branca, sem fundo, separada da faixa). A frase da
faixa é a manchete que para o scroll ("não entra em X antes desse vídeo"), não
o CTA nem o preço — isso fica na fala. Quando o layout é Meio a meio, a faixa
**pode** sentar na costura em vez do topo/base da caixa viva; nos outros
layouts (Tela cheia, Miniatura/PiP) ela volta pro topo ou base, fora da área
que corta.

---

## Modos de edição — só DEPOIS do pré-final

**Ordem obrigatória. Editar antes de fechar o pré-final é retrabalho garantido:**
qualquer corte de silêncio ou mudança de ritmo depois desloca todos os pontos de
troca de layout, e a peça inteira precisa ser remontada.

1. **Pré-final** — concatenar as cenas aprovadas no gate. É um vídeo assistível,
   com a fala inteira, sem nenhuma edição de layout.
2. **Pós-produção base** — acelerar (1.15x é o padrão medido), cortar respiração e
   fala repetida, queimar legenda dentro da caixa viva. Só aqui o **tempo final de
   cada fala** existe de verdade.
3. **Modos de edição** — agora sim, com os segundos reais em mãos.

### O material B: gravação de tela OU b-roll de banco

O que entra na outra metade depende do que o criativo precisa provar:

- **Produto digital** (portal, app, dashboard): gravação de tela em modo mobile,
  navegada como um usuário novo. Ver Modo E (Vitrine Guiada).
- **Produto físico ou serviço** (coleira de pet artesanal, marcenaria, estética):
  cenas de banco público e Pinterest, montadas na ordem da fala. Um plano por
  ideia, nunca um plano genérico "de enfeite".
- **Com ou sem narração:** a fala da personagem pode continuar por cima, ou o
  trecho vira narração pela skill `narracao-hub-tts` com a voz da peça.

A regra de enquadramento é a mesma para os dois: material vertical entra em
moldura deitada com **zoom e foco próprios**, senão a metade fica com sobra morta
e a peça parece dois vídeos empilhados.

### O menu — escolha UM por criativo

Os quatro layouts são linguagens diferentes, não um combo. Três trocas de
linguagem em dez segundos viram mostruário: sinalizam edição automática e
queimam a atenção que o hook comprou. **A peça abre na pessoa, usa UM estilo no
miolo para provar o que ela disse, e volta pra ela no fecho.**

| Estilo | Serve pra | Uso típico |
|---|---|---|
| **Meio a meio** (B em cima, ela embaixo) | provar o que ela acabou de afirmar | uma inserção, na fala do mecanismo |
| **Meio a meio invertido** (ela em cima, B embaixo) | devolver o peso pra ela sem soltar o B | quando a fala volta a ser pessoal |
| **Miniatura / PiP** (B em foco, ela no canto) | demonstração longa em que o B é protagonista | trecho de 4-8s, voz off narrando |
| **Tela cheia dela** | hook e fecho | sempre começo e fim |
| **Print + POV + Meme** | prova social/resultado sem rosto nenhum em quadro | ver abaixo |

### Print + POV + Meme — o único layout sem rosto real

Três zonas empilhadas, fundo preto sólido, sem faixa colorida:

1. **Topo — print de prova.** Screenshot real (chat, dashboard, resultado,
   métrica) — ROAS, ROI, conversa, o que for a prova daquele criativo.
2. **Meio — texto POV.** Amarelo, itálico, negrito, fundo preto. Sempre começa
   com "POV:" e conta a situação em 1-2 linhas — é a piada/gancho, não a oferta.
3. **Base — personagem meme recortado.** PNG com fundo removido (Shrek, Doge,
   etc.), reagindo à situação do POV. É a assinatura visual do formato — sem
   ele vira só um print com legenda.

Sem narração, sem b-roll, sem gravação de tela em movimento — é 100% estático
em composição, o "vídeo" é só o efeito de entrada de cada zona (fade/slide
curto) e som de fundo opcional. Cabe no Modo E como variante estática dele, ou
no Modo D pela biblioteca de escalados (categoria "meme"/"ilustração"). Nunca
misture com faixa vermelha do layout Meio a meio — são dois vocabulários visuais
diferentes.

Implementação de referência (Remotion, com os quatro layouts e o menu de estilos
já escritos): `marketing/anuncios/2026-09-02-BR-gratis/editor/` no projeto
AstroDicas — `src/layouts.ts` (retângulo + zoom + foco de cada layout),
`src/estilos.ts` (o menu), `src/MeioAMeio.tsx` (a viagem entre layouts).

A troca **não é fade**: os dois vídeos viajam entre os retângulos, então a pessoa
encolhe de verdade enquanto o B cresce. Fade entre dois layouts lê como corte de
software; a viagem lê como decisão de edição.

## Estrutura de pastas

```
<PROJETO>/ANUNCIO/<DD-MM>/
  REFERENCIA/                frames de referência (persona, look)
  CRIATIVO-<N>/
    IMG/     cena-1.png ...
    VIDEO/   cena-1.mp4 ...
    PROMPTS/ cena-1.md  ...
    CRIATIVO-<N>.mp4         entregável final
```

**Numeração: continue a série do projeto, não recomece do 1.** Antes de criar as pastas, veja até que número os anúncios já chegaram e siga daí. Se o projeto já tem AD1…AD9, os novos são CRIATIVO-10, 11, 12. Recomeçar do 1 gera colisão de nome no gerenciador de anúncios e some com o histórico de qual criativo é qual.

```bash
ls <PROJETO>/ANUNCIO/*/ | grep -oE "(AD|CRIATIVO-)[0-9]+" | sort -uV | tail -3
```

---

## Erros comuns

| Sintoma | Causa | Correção |
|---|---|---|
| Boca não bate com o áudio | Fala não foi literal no prompt | `lips accurately synced to these exact words: "<texto>"` |
| Pessoa muda de rosto entre cenas | Cada imagem gerada do zero | Anexe frame de `REFERENCIA/` e peça "same woman, same face" |
| Objeto brotando na cena | Falta bloco de continuidade | Cole o bloco anti-morphing e feche a lista de objetos |
| Mão deformada, dedo a mais | Idem, pior em clipe longo | Bloco anti-morphing + prefira 6s com objeto na mão |
| Fundo se reorganizando | Câmera com movimento demais | `locked-off static camera` |
| Elemento místico vazando pra cena nova | Referência tinha vela/cristal | Proíba explicitamente no prompt de imagem |
| Sotaque neutro em vez do regional | Sotaque não especificado | `Argentine Spanish, voseo, Buenos Aires accent` |
| Fala cortada no fim | Texto longo demais | 6s ≈ 15 palavras, 10s ≈ 25 |
| **Frase repetida no clipe ("esto es para vos, esto es para vos")** | fala CURTA demais para os 8s | faixa segura 11-16 palavras; corte no fim da 1a ocorrencia, nao regere |
| **Voz tocando com a boca parada** | **Texto estourou o orçamento do clipe** | **Conte as palavras ANTES (FASE 1). Corte o texto e regere — não tem conserto na pós** |
| Trilha indesejada | Grok adiciona por padrão | `no background music, ambient sound only` |
| Legenda queimada no clipe | Não foi proibido | `no subtitles, no burned-in text` |
| Vídeo horizontal | Formato não travado na imagem | `vertical 9:16 story format` desde o GPT |
| Total do hook estourou o alvo | Cenas escritas soltas e somadas no fim | Orçamento de tempo na FASE 1 |
| Cena gerada com o prompt da cena anterior | Hub não limpa o textarea | sequência canônica de envio em `hub-video-playwright` |
| Loop de espera trava para sempre | src do `<video>` vira `blob:` | ver `hub-video-playwright` |
| Rosto vira careta ao animar | Imagem de origem estourada ou com expressão exagerada | Gere o rosto em repouso e exposição correta; a emoção vai no `ACTION` do vídeo |
| Clique em `Enviar` responde OK e nada acontece | Crisp por cima, ou ref expirado | ver `hub-video-playwright` |
| Loop de espera estoura sem clipe novo | Verificação de Segurança na tela | ver `hub-video-playwright` |
| Cena parada, boca mexendo e corpo congelado | `ACTION` sem micro-movimento | Descreva piscar, respirar, peso do corpo, mão que se ajusta |
| Imagens do GPT chegam fora de ordem | ordem do DOM ≠ ordem das cenas | ver `gpt-imagem-playwright` |
| Só 2 de N imagens baixam do GPT | downloads em rajada bloqueados | ver `gpt-imagem-playwright` |
| "Muitas requisições em pouco tempo" | cada clique em Enviar é requisição | ver `hub-video-playwright` |
| **Clipe gerado da imagem reprovada** | regerou a imagem mas não redistribuiu às cenas | `valida_img.sh` por hash antes de cada envio |
| Imagem baixada é miniatura (416x681) | filtro de download frouxo | valide dimensão com `ffprobe`; tamanho fora da média dos irmãos = lixo |
| Cena sem imagem descoberta só na hora de gerar | distribuição rodou antes de a imagem existir | cobertura **cena a cena**, não contagem total |
| Objeto flutuando apesar do bloco anti-morphing | prompt descreve o prop em lugar diferente da imagem | imagem aprovada é a fonte da verdade; adapte o prompt a ela |
| Lote reporta sucesso com item faltando | falha de envio no meio não para o loop | reconcilie pedido × disco no fim do lote |
| **Dente prateado/metálico** | Veo põe coroa ou capa de metal | bloco de esmalte natural no `CONTINUITY` + negativo de metal |
| **Banguela — dentes somem enquanto fala** | Veo apaga dentes no movimento da boca | bloco de dentes no `CONTINUITY` + `NEGATIVE`; amostre a boca em 5 tempos |
| **Personagem TROCADA numa cena** | `DIALOGUE` (fala em quadro) usado em imagem sem rosto — o modelo inventa a pessoa | declare narração explícita + `no new character`, ou reenquadre com rosto |
| **Voz muda no meio do criativo** | cena de b-roll sem rosto em quadro | Toda cena falada mostra o rosto; b-roll é mudo — ver "Cena SEM ROSTO sorteia outra voz" |
| **Prop pequeno duplicado (2 papéis, 2 moedas)** | prompt não disse QUANTOS existem | `exactly ONE ... stays inside the bowl` + negativo de duplicação — item 9 da FASE 4 |
| **Papel/tela reescrito com a fala** | `ACTION` dizia que ela lê em voz alta | Trave a superfície como prop fixo no `CONTINUITY` + `NEGATIVE` — ver item 8 da FASE 4 |
| **Respiração e pausas sobrando no final** | montagem conservou cauda inútil | corte por palavra + gesto (FASE 7); sem key, revise candidatos do `tight.py`, preservando pausas úteis |
| Tempos de corte truncados/vazios da 2ª cena em diante | `ffmpeg` comeu o stdin do `while read` | `ffmpeg -nostdin` |
| Cloudflare travando | Chromium empacotado | skill `browser-cloudflare`; `~/.claude/bin/browsers.sh status` |
| Sessão errada / conta trocada | Faltou `--session` | Passe sempre |

## Skills-filhas — invoque, não reescreva

Esta skill é o orquestrador. A mecânica de browser vive nas duas skills abaixo, e
elas são a **única** fonte de verdade sobre seletores e operação. Copiar comando
delas para cá cria segunda verdade — foi assim que a antiga `grok-video-hub-playwright`
ficou dizendo que o motor padrão era o Grok enquanto o fluxo real já era Veo 3.1.

| Skill | Cobre | Invocada na |
|---|---|---|
| `gpt-imagem-playwright` | imagem no ChatGPT: lane, chat novo, anexo, envio, download, validação do arquivo | FASE 3 |
| `hub-video-playwright` | vídeo no NinjaBR Hub: motor Veo 3.1 Quality, 9:16, envio, gates, cota, download | FASE 5 |
| `narracao-hub-tts` | narração off em WAV pelo NinjaVoice: escolha de voz por nicho, lote cena a cena, mixagem com trilha | Modo E |

Se um seletor mudar, corrija **na skill-filha**. Nunca aqui.

## Referências

- `scripts/browsers.sh` — sobe e conecta os dois browsers persistentes
- `references/caso-numero-mestre.md` — caso real histórico (projeto NUMERO-MESTRE, extinto Modo B): consulta de erro antigo, não reproduzir o mecanismo
- Skill `browser-cloudflare` — detalhe de por que o Chromium do sistema
- Skills `remotion-create`, `remotion-captions`, `remotion-render` — montagem final e legenda canônica
- Skill `video-use` (`~/Developer/video-use`) — transcript Scribe por palavra, EDL, corte/concat com fade (FASE 7)
- Skills `hyperframes-*`, `embedded-captions`, `captions-overlay`, `talking-head-recut`, `cut-the-curve` — motion, legenda animada, cards e costuras
- `references/SKILL-ffmpeg-OLD-2026-09-23.md` — SKILL.md como era antes da revisão da stack de edição (tudo em ffmpeg + whisper)
