# Geração com IA — 1: motor, conceito, orçamento de fala e imagem de referência (movido do SKILL.md em 26/10/2026)

> Ler quando o vídeo tem cena GERADA (personagem/expert/UGC no Flow). Edição não mora aqui: `EDICAO-PADRAO.md`. Hub está desativado: vídeo vai no Flow (`mecanica-flow.md` / `flow-video-playwright`); trechos que citam Hub/Grok são históricos.


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
| ~~Duração de cada corte (formato multi-cena curto)~~ **OBSOLETO 26/10 — corte = duração da frase, 1,5–3 s (`EDICAO-PADRAO.md` §2)** | ~~≥6s por cena~~ | menos que isso lê como "corte nervoso/rápido demais" mesmo com velocidade normal — usuário reclamou em 2026-09-07 (3 vídeos "Detalhe" com corte ~4s cada) |
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
8. ~~**Só Grok.**~~ Obsoleto: Hub desativado; vídeo vai no Flow (Veo).
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

