---
name: depoimentos-video
description: Gera um vídeo de depoimentos — N pessoas diferentes falando do produto em câmera, uma atrás da outra, formato 9:16 com legenda queimada dentro da safe area de stories. Orquestra o pipeline (personas, falas, imagem de referência, clipe, montagem, pós) e delega a mecânica de browser para gpt-imagem-playwright (imagens no ChatGPT) e hub-video-playwright (vídeo no NinjaBR Hub, Veo 3.1 Quality). Use quando o usuário pedir vídeo de depoimento, prova social em vídeo, "gente falando do produto", UGC de cliente, testimonial, ou pedir N pessoas dando depoimento.
---

> **HUB DESATIVADO (02/10/2026, ordem da usuária):** NinjaBR Hub está SEM COTA e os perfis `hub`/`hubv2`/`hubts` foram removidos (backup em `~/.agent-profiles/_removidos-hub-2026-10-02/`). NÃO use Hub, NÃO rode `hub-livre.sh` (sai com erro), NÃO espere perfil do Hub liberar. Imagem: ChatGPT — se a cota de upload de uma conta acabar, troque de CONTA: `gpt-conta*` ↔ `gpt-conta*`. Vídeo: Google Flow (`flow-video-playwright`).


# depoimentos-video

Produz uma peça de **depoimento**: várias pessoas diferentes, cada uma falando do
produto em câmera. Não é anúncio — não tem hook, não tem oferta, não tem CTA.

**Esta skill orquestra. A mecânica de browser não mora aqui:**

| Fase | Quem executa | Invoque |
|---|---|---|
| imagem de referência | ChatGPT | `gpt-imagem-playwright` |
| clipe de vídeo | NinjaBR Hub, Veo 3.1 Quality | `hub-video-playwright` |
| regras gerais de prompt de vídeo | — | `criativo-ads-video-orq` (blocos obrigatórios, anti-morphing, dentes) |

Nunca copie seletor nem comando de browser para cá. Se um seletor mudar, corrige na
skill-filha.

---

## O erro que define esta skill: depoimento é RESULTADO, não setup

A fala de cada pessoa tem que ser **o depoimento dela sobre o produto**. Medido em
produção (AstroDicas, 01/09/2026): a primeira leva saiu com falas de *contexto*
(«eu lia horóscopo de site e nunca batia nada») e o dono cortou na hora — *"não deu
depoimento, é pra falar o depoimento"*. As oito falas tiveram que ser reescritas.

| Não é depoimento | É depoimento |
|---|---|
| «Eu lia horóscopo de site e nunca batia nada» | «Eu uso o Diário Astral faz três meses e virou a primeira coisa do meu dia» |
| «Minha filha comprou pra mim, achei que não ia entender» | «Minha filha me deu e eu não largo mais, todo santo dia» |
| «Eu achava isso tudo bobagem» | «Eu era o maior cético, mas ele me ganhou na primeira semana» |

Toda fala tem que passar num destes moldes:

- **uso + tempo:** «uso faz três meses e virou parte do meu dia»
- **resultado concreto:** «acertou o momento que eu tava vivendo»
- **o que o produto é, na boca do cliente:** «é a leitura do meu mapa mesmo»
- **recomendação:** «recomendo pra qualquer um da minha idade»

O ceticismo pode aparecer, mas **só como virada** («eu era cético, MAS…»), nunca
como a fala inteira. E o nome do produto entra na boca de pelo menos metade das
pessoas — é o que faz a peça ser sobre ele.

Objeção de preço, garantia e "não é assinatura" **não entram na fala**. Isso é
rodapé, se o usuário pedir.

---

## FASE 0 — Briefing

Levante, perguntando o que não souber:

- **Produto** e o que ele entrega, na linguagem do cliente
- **Quantas pessoas** e **duração alvo**
- **País/idioma/sotaque**, e a diversidade pedida (idade, gênero, região, etnia)
- **Onde vai rodar** (stories, site, feed)

Regra de diversidade: se o usuário pediu "pessoas diferentes", **varie idade,
gênero, região e ambiente ao mesmo tempo**. Personas do mesmo tipo convergem para
o mesmo visual mesmo com prompts distintos — ver `criativo-ads-video-orq`.

**Cada pessoa tem nome, cidade e estado** — definidos no briefing, espalhados pelo
Brasil (uma por região: NE, Sul, Sudeste, Norte/Centro-Oeste). O rótulo entra na
edição via `NOMES`, e a **cidade tem que bater com o sotaque escrito no `voice`** —
rotular de Belém quem foi gerado com sotaque de Recife denuncia a peça.

Um look por pessoa, e proíba no prompt os elementos das outras (`absolutely no
kitchen, no coffee mug` na persona da varanda). Sem isso saem quatro cozinhas.

---

## FASE 1 — Orçamento: 2 cenas de 8s por pessoa

O Veo 3.1 entrega **8s** por clipe. A conta que fecha:

| Pessoas | Clipes | Bruto | Final (após corte + 1,15x) |
|---|---|---|---|
| 4 | 8 (2 por pessoa) | 64s | **~40s, ~10s por pessoa** |
| 3 | 6 | 48s | ~30s |
| 5 | 10 | 80s | ~50s |

Uma cena só por pessoa dá ~5s finais — curto demais para um depoimento respirar.
**Duas cenas por pessoa é o padrão**: a primeira apresenta o uso, a segunda dá o
detalhe concreto ou a recomendação.

**Faixa segura de fala: 11 a 16 palavras por cena.** Acima de 16 a voz acelera e
sai robótica; abaixo de 11 o Veo repete a frase para preencher o clipe. O
`gerar-prompts.py` trava nisso.

---

## FASE 2 — Roteiro em JSON

Escreva `roteiro.json` na pasta do projeto:

```json
{
  "personas": [
    {
      "char": "24-year-old Brazilian woman from Recife (Northeast Brazil), mixed Northeastern features, warm brown skin, dark curly hair tied back loosely, plain white cotton T-shirt, no makeup, natural skin",
      "scene": "sitting on the edge of a single bed in a small simple student bedroom, cold late-afternoon window light from the right, plain painted wall behind her",
      "objs": "single bed with plain bedsheet, plain painted wall — nothing else",
      "ban": "absolutely no kitchen, no coffee cup, no desk, no computer, no porch, no plants",
      "idioma": "Brazilian Portuguese",
      "voice": "VOICE: age 24, female, native Brazilian Portuguese, Recife accent. Pitch: mid register. Texture: natural, clear. Pace: 2.2 words per second, brief pauses between thoughts. Energy: casual and genuine, never bright, never salesy. Delivery: speaking to one person across from her. No echo, no reverb, no processing, no announcer tone.",
      "amb": "quiet bedroom ambience only, faint distant street sound",
      "masculino": false,
      "falas": [
        "Eu uso o Diário Astral faz três meses e virou a primeira coisa do meu dia.",
        "É a leitura do meu mapa mesmo. Parece que alguém escreveu olhando pra minha vida."
      ]
    }
  ]
}
```

`char`, `voice` e `objs` são **strings fixas da persona** — o gerador cola as três
byte a byte nas duas cenas. Reescrever entre cenas troca a pessoa e a voz.

Nacionalidade específica, nunca "Latin American": no Brasil, diga a região.

```bash
python3 ~/.claude/skills/depoimentos-video/scripts/gerar-prompts.py roteiro.json "$PROJ"
```

Ele escreve `PROMPTS/img-cena-P-K.txt`, `vid-cena-P-K.txt` e `vid-cena-P-K-short.txt`
(o `-short` é o que vai ao Veo, teto de 2500 chars), e **falha** se alguma fala sair
da faixa de palavras ou algum prompt estourar o teto.

---

## FASE 3 — Imagens (invoque `gpt-imagem-playwright`)

Duas imagens por pessoa:

- **cena 1** — plano médio, prompt do zero
- **cena 2** — mesma pessoa, enquadramento um pouco mais fechado, gerada **com a
  cena 1 anexada como referência**. Descrever a pessoa de novo por texto sorteia
  outra.

Uma cena por mensagem, chat novo a cada imagem — lote volta grid. O bloco
`MOUTH AND TEETH` vai literal (o gerador já o inclui): com a boca fechada na
referência, o Veo sorteia a dentição durante a fala.

**Gate antes de qualquer vídeo** — hash distinto por arquivo, dimensão do lote, e
olhar o contact sheet: mesma pessoa nas duas cenas, personas visualmente separadas
entre si, boca falando, nada de texto queimado.

```bash
md5sum IMG/*.png | sort | uniq -w32 -D      # qualquer saída = defeito
montage IMG/cena-*.png -tile 4x2 -geometry 260x462+3+3 -background '#111' sheet.jpg
```

Terminou as imagens? **solte a lane do gpt na hora** — o vídeo ainda vai levar meia
hora e tem gente na fila.

---

## FASE 4 — Clipes (invoque `hub-video-playwright`)

Veo 3.1 **Quality**, 9:16, 8s, Imagem→Vídeo, um clipe por vez. ~4 min por clipe;
uma leva de 8 leva ~30 min.

A fila tem que ser **idempotente**: pula o que já existe em disco e move o arquivo
para o destino final na hora. A sessão cai no meio de levas longas — o disco é o
checkpoint.

Escolha o download **por conteúdo** (frame 0 × imagem da cena, RMSE < 0,16), nunca
pelo "último vídeo da lista": o histórico do Hub é da conta inteira.


### Cada clipe aparece DUAS vezes no histórico — é normal

Um envio vira **dois jobs**: o Hub re-roteia o pedido do Veo para o backend
`google-flow`, então o histórico mostra o mesmo prompt em dois cards
(`Veo 3.1 (Imagem→Vídeo)` e `google-flow · create_video`). Não é reenvio da
automação — duplo clique produziria dois cards do MESMO motor.

Consequência prática: **cada clipe custa 2 gerações de cota e ~o dobro do tempo**.
Uma peça de 8 clipes consome 16. Dimensione a leva por isso.

Antes de acusar regeração, conte por par:

```bash
# no /studio: quantas vezes cada fala aparece, por motor
echo '(()=>{const c={};for(const a of document.querySelectorAll("article")){
 const m=a.textContent.match(/exact words: "([^"]{0,30})/); if(!m) continue;
 const k=m[1]+" | "+a.textContent.slice(0,30).split("·")[0].trim(); c[k]=(c[k]||0)+1;}
 return JSON.stringify(c);})()' | agent-browser --session $S eval --stdin
```

`1 Veo + 1 google-flow` por fala = correto. Mais que isso = envio repetido de
verdade — tipicamente uma fila que foi interrompida e relançada sem checar o disco.


### Browser disputado: um perfil de vídeo por leva

Se outro agente já está gerando no perfil `hub`, **não dispute** — a aba compartilhada
come o anexo e o contador de vídeos sobe pelas gerações do outro, então o loop de
espera baixa nada e reporta "sem clipe novo". Medido em 01/09/2026: três cenas
seguidas falharam assim enquanto uma leva argentina rodava no mesmo perfil.

```bash
curl -s http://127.0.0.1:9223/json/list | python3 -c "
import sys,json
for t in json.load(sys.stdin):
    if t.get('type')=='page': print(t['url'][:70])"      # duas abas /studio = disputa
```

Sinal no histórico: o topo mostra um `CHARACTER:` que não é o seu. Nesse caso mude
para `hubv2` (segundo perfil de vídeo, porta 9231) e **solte a lane do `hub`**. O
`hubv2` costuma estar deslogado — logue com as credenciais do env, o Cloudflare
dessa tela valida normalmente.

---

## FASE 5 — QA dos clipes

Antes de montar, por cena:

- **fala é a certa?** transcreva ou ouça — é aqui que se pega fala que não é
  depoimento, e frase repetida pelo Veo
- **boca acompanha até o fim**, com respiro sobrando
- **dentes** ao longo da fala (recorte a boca em 5 tempos, não um frame só)
- **mesma pessoa e mesmo ambiente** nas duas cenas dela
- **tamanho do arquivo** dentro da média dos irmãos

Defeito visto é defeito reportado ao dono. Nunca monte sobre cena reprovada.

---

## FASE 6 — Montagem e legenda

Ordem: pessoa 1 cena 1, pessoa 1 cena 2, pessoa 2 cena 1… Concat pelo **filtro**
(`-c copy` picota o áudio nas junções) e no **fps nativo do motor** (Veo = 24).

```bash
bash ~/.claude/skills/depoimentos-video/scripts/montar.sh "$PROJ" "$PROJ/DEPOIMENTOS.mp4"
```

A legenda e o título são pós-produção, nunca pedidos na geração:

```bash
TITULO="O que dizem sobre nós" NOMES="$(cat nomes.json)" \
  python3 ~/.claude/skills/depoimentos-video/scripts/pos-producao.py DEPOIMENTOS.mp4
# -> DEPOIMENTOS-v2.mp4
```

`nomes.json` identifica cada depoente **na edição** (texto queimado, nunca falado),
em tempos do vídeo **montado, antes do corte** — o script remapeia sozinho para a
timeline final:

```json
[{"t": 0, "e": 16, "txt": "Mariana, Recife - PE"},
 {"t": 16, "e": 32, "txt": "Rogério, Curitiba - PR"}]
```

Com 2 cenas de 8s por pessoa, a pessoa `i` ocupa `[16*(i-1), 16*i)`.

**As duas faixas de texto ficam fora do que os stories cortam**, e é por isso que
elas têm margens diferentes:

| Faixa | Estilo | Posição | Por quê |
|---|---|---|---|
| **título** (`TITULO`, opcional) | Jost bold 62, dourado, caixa alta | `alignment 8`, **MarginV 300 do topo** | abaixo do header/avatar dos stories |
| **nome + cidade/UF** (`NOMES`, opcional) | Jost bold 46, branca | `alignment 2`, **MarginV 600 do rodapé** | logo acima da legenda, sem colidir |
| **legenda** | Jost bold 74, branca, palavra ativa dourada | `alignment 2`, **MarginV 470 do rodapé** | acima da barra de resposta e do swipe |

O título entra como um evento ASS do primeiro ao último frame — sem segundo
encode, e sem risco de sair do lugar. Vazio (padrão) = sem título.

**Legenda não pode pular.** Só a COR da palavra ativa muda; escala fica em 100.
Destacar com `\fscx104` muda a largura da linha e o bloco re-centraliza a cada
palavra.

**fps: o nativo do motor.** O script lê o `r_frame_rate` da entrada e usa ele —
forçar 30 num material 24 do Veo duplica frames e dá judder que nenhum `ffprobe`
acusa.

**Dinheiro na legenda sai por extenso, sempre.** O whisper normaliza a fala para
dígitos — a pessoa diz "vinte e sete e noventa" e a legenda escreve `R$ 27,90`,
que lê como preço impresso e destoa do resto da frase. A pós converte de volta
(`R$ 27,90` → "vinte e sete reais e noventa centavos"), dividindo o intervalo do
token original entre as palavras novas, então o destaque palavra a palavra
continua batendo. Cobre `R$`, `US$`, `€`, `$` e o padrão `14.900 pesos`. Número
que não é moeda (`às 27 horas`) não é tocado.

**Chiado do Veo.** O motor entrega room tone audível — um chiadinho constante que,
somado a 8 clipes, vira ruído contínuo na peça. A pós trata por padrão
(`highpass=f=70,afftdn=nr=12,dynaudnorm`): o highpass tira o rumble, o `afftdn`
tira o ruído de fundo, e o `dynaudnorm` iguala o volume entre pessoas gravadas em
ambientes diferentes. `DENOISE=0` desliga.

Não passe de `nr=18`: acima disso a voz fica metálica, que é pior que o chiado.
Meça em vez de confiar no ouvido no primeiro take:

```bash
ffmpeg -i entrada.mp4 -af astats=metadata=1 -f null - 2>&1 | grep -i "Noise floor dB"
```

O `pos-producao.py` faz, nesta ordem: whisper com word timestamps → corta
silêncio/respiração acima de 0,32s → dropa **frase** repetida pelo Veo (por frase,
nunca por bloco de fala) → denoise do áudio → 1,15x em vídeo e áudio → queima
título, nomes e legenda.

---

## Estrutura de pastas

Depoimento **não é anúncio** — não vai para `anuncios/`, e não recebe numeração de
criativo. Dito explicitamente pelo dono na leva de 01/09/2026.

```
<PROJETO>/marketing/depoimentos/<AAAA-MM-DD>-<PAIS>/
  roteiro.json
  ROTEIRO.md          personas, falas e contagem de palavras
  IMG/     cena-1-1.png cena-1-2.png cena-2-1.png ...
  VIDEO/   cena-1-1.mp4 ...
  PROMPTS/ img-cena-1-1.txt  vid-cena-1-1.txt  vid-cena-1-1-short.txt ...
  DEPOIMENTOS.mp4     bruto montado
  DEPOIMENTOS-v2.mp4  entregável (cortado, acelerado, legendado)
```

Nunca apague `VIDEO/cena-*.mp4`: sem os clipes-fonte, um defeito numa pessoa obriga
a refazer a peça inteira.

---

## Erros comuns

| Sintoma | Causa | Correção |
|---|---|---|
| «isso não é depoimento» | fala de contexto/objeção em vez de resultado | os moldes do topo desta skill |
| pessoa fala e não cita o produto | nome do produto só no roteiro | nome na boca de metade das pessoas |
| quatro personas parecidas | mesmo tipo de pessoa e ambiente | varie idade/gênero/região **e** proíba o cenário das outras |
| voz muda entre as duas cenas da mesma pessoa | `VOICE` reescrito | string fixa, colada byte a byte |
| voz robótica | fala acima de 16 palavras | corte o texto, não estique o clipe |
| frase repetida no clipe | fala abaixo de 11 palavras | faixa 11-16; ou corte no fim da 1ª ocorrência |
| legenda pula no vídeo | destaque mudando a escala | só a cor muda |
| peça foi parar em `anuncios/` | tratada como criativo | `marketing/depoimentos/` |
| mesmo prompt 2x no histórico | Hub re-roteia Veo -> google-flow, 1 envio = 2 jobs | normal; conte por par antes de suspeitar |
| "barra não configurada" / "sem chip motor" em toda cena | a sessão do Hub caiu para `/auth` — o script lê a tela de login como barra ausente | cheque `get url` antes de culpar seletor; relogue e relance a fila (ela pula o que já existe) |
| "sem clipe novo" repetido, anexo some | outro agente no mesmo perfil de browser | migre para `hubv2` e solte o `hub` |
