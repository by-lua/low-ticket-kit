# Lições de produção de criativo — 09/10/2026 (Elétrica + Tarô)

> Tudo que a dona corrigiu ou que quebrou em produção num único dia, já com o conserto.
> Regra: **qualquer pane que for produzir criativo lê isto antes de gerar**. Onde a regra
> virou texto fixo, o ponteiro está indicado — o detalhe continua na skill que manda.

## 1. Imagem de criativo: referência = CAPA + 2 a 3 PÁGINAS REAIS, sempre

- **Errado:** anexar só a capa. Dona, 09/10 (Tarô, card 1 do CRIATIVO-21): "só a capa?" —
  a arte sai sem o produto aparecendo.
- **Certo:** anexa **1 capa + 2/3 páginas reais de entrega** e escreve no prompt que
  **o modelo escolhe DUAS** das páginas pra mostrar na cena — "nem muito, nem pouco".
  As páginas visíveis são **sempre** arquivo real; o modelo posiciona, não desenha página.
- Onde está gravado: `criativo-ads` (Regras da dona) · `modelagem-escalados` item 13 ·
  `gpt-imagem-playwright` (callout do topo).
- Prova: o card 1 gerado com capa + 3 páginas (o modelo escolheu "0 · O Louco" e
  "Como usar este mapa") passou de primeira; a versão anterior, só com a capa, foi reprovada.

## 2. Título não precisa ser branco — cor da marca

- Dona, 09/10 (Tarô): "o título não precisa ser só branco, pode ser amarelo, azul, enfim
  o que for adequado à marca".
- Prática: define a paleta do produto (ex.: Tarô = roxo #4B2E83 sobre creme) e manda o
  título nessa cor, com sombra/contorno onde a foto for clara. Continua valendo a regra
  08/10: **título grande e direto** (título pequeno/fraco continua reprovado).
- Gravado em `criativo-ads` (Regras da dona).

## 3. Vídeo de leva ABRE com o produto na tela — e nada de imagem parada

- Regra 09/10 (JJ + Elétrica): beat 1 = **gravação real** do produto (tela cheia, com
  zoom/varredura), gancho falando por cima. Nada de b-roll genérico na abertura.
- **Proibido PNG/Ken Burns como cena de produto em vídeo** — onde usaria PNG, usa a
  gravação real em movimento.
- Fonte única de imagem do produto em vídeo = **gravações da dona** em
  `criativos/MATERIAL-ENTREGAVEL/gravacoes-tela/`. Sem print, sem PNG, sem imagem gerada.
  **Não achar a gravação → PERGUNTE**, não invente.

## 4. Gancho: rever ANTES de produzir (os ângulos v3 falharam)

- Elétrica: o gancho "dominar teoria" leu como peça de estudo; dona 09/10: "não gostei do
  ângulo do vídeo, é mais sobre estudo do que profissional". Falas 2 e 3 reescritas pra
  **serviço/renda/respeito** ("o que o serviço exige", "resolve na frente do cliente,
  sem depender de ninguém").
- Sempre: confere as análises de tráfego (`trafego/ANALISES.md`) da oferta **antes** de
  escrever o gancho, e não reusa dor que já morreu em vídeo. Confere também
  **`LOW-TICKET/KEVONES/MUDANCAS.md`** (preço, página/headline, público e **troca de anúncio**):
  o que "parou de vender" às vezes é mudança da dona, não criativo morto.

## 5. BUG DE MONTAGEM: `adelay` espera MILISSEGUNDOS

- Em `montar*.sh`, os offsets das cenas saem em **segundos** (soma das durações). Passar
  eles direto pro filtro `adelay` (= ms) empilha **todas as falas em ~0s**: frases
  sobrepostas no começo + **mudo do meio pro fim**. Parece "áudio duplicado".
- Conserto: `ms() { awk -v v="$1" 'BEGIN{printf "%d", v*1000+0.5}'; }` e usar `$(ms ${OFFS[i]})`.
- **O GATE do `fechar.sh` NÃO pega esse defeito** (os gates de aceleração/última-fala leem
  o `words.json`, que é estático — não medem onde a fala caiu). Confira sempre a **envoltória**:
  ```
  ffmpeg -i VIDEO.mp4 -ac 1 -ar 16000 -f f32le - > /tmp/a.raw
  # numpy: RMS por 0.5s — a fala tem que estar espalhada por TODA a duração
  ```
  E correlacione o final com a VO bruta: pico em **lag 0** = 1 cópia (ok); pico em outro
  lag = eco; resíduo grande = outra coisa (música com voz, por exemplo).
- Achado em 09/10 no CRIATIVO-10 da Elétrica e conferido nos outros: C1/C2/C3 da Elétrica
  e os 5 vídeos do Ji-Jitsu estão com a fala espalhada (ok). Corrigido e registrado no
  `montar-c10.sh` + STATUS da oferta.

## 6. Toda peça entrega com `anuncio.md` — inclusive peça antiga

- 09/10: 6 peças do Tarô BR (CRIATIVO-13 a 18) estavam só com PNG, sem copy — regra da
  dona ("o arquivo de mídia sozinho não conclui a entrega"). Todos os 6 foram escritos,
  cada um com **ângulo próprio** (nunca copy repetida na mesma leva).
- Checklist de saída de qualquer pasta de criativo: `arquivo final` + `intermediarios/` +
  `anuncio.md` (ângulo, persona/dor, texto principal, título, descrição curta, CTA).

## 7. Envio de prompt no ChatGPT: SEM aspas duplas

- `keyboard inserttext` **trunca o prompt na primeira quebra de linha/aspas**. Custo real:
  o modelo recebeu só a primeira linha e voltou perguntando o texto do título — geração
  perdida e pista falsa de "cota".
- Faça o prompt **numa linha só, sem `"`,** e confirme o envio pelo começo da mensagem que
  aparece no chat ("Você disse: …"). Se ali só tem a primeira frase, reenvie inteiro.
- Gravado em `gpt-imagem-playwright`.

## 8. B-roll: o slug do Pexels só aparece DEPOIS do download

- Dois clipes escolhidos por busca ("painel elétrico") eram na verdade **ambulância**
  (`paramedic-entering-an-ambulance`, `ambulance-driver-flipping-switches`). Só se vê
  abrindo o `.json`/baixando. **Confira o slug e os frames de todo clipe novo** antes de
  entrar no corte, mesmo que a busca tenha parecido certa.

## 9. Trilha: a régua genérica (−38 dB) nem sempre serve

- No C10 da Elétrica, −38 dB deixou a trilha **40,5 dB abaixo da voz** (fora da faixa
  12–40 do gate) e sem leito nas pausas. Subiu pra −30 dB e fechou (32,8 dB abaixo).
  Mesmo caso registrado no C1 (−28 dB). **Meça, não herde o número.**

## 10. Peça entregue ≠ peça pronta: confira o que existe na pasta

- Padrão que apareceu 3× em 09/10: pasta com `anuncio.md` + `refs/` mas **sem a arte**,
  ou com cards 2–5 e **sem a capa**. Antes de produzir, olhe a pasta: se faltar arte ou
  copy, é isso que falta — não invente outro item.

## 11. Legenda karaokê: a "segura" da linha não pode invadir a próxima

- No gerador da `.ass` (padrão karaoke v2: um evento por palavra, mostrando a linha inteira),
  a última palavra de cada linha costuma ganhar um `+0.15s` de respiro. Se esse respiro passar
  do início da **próxima linha**, as duas linhas são desenhadas juntas no mesmo `\pos` — o
  vídeo sai com **legenda "duplicada"** em toda transição (dona, 09/10, ES).
- Conserto: `fim = min(line["end"] + 0.15, proxima["start"])`.
- Depois de queimar legenda, **confere uma transição** (2-3 frames em torno da troca de linha):
  tem que haver **uma** legenda por frame.
- E nunca deixe `.ass`/`.srt` solto na pasta do mp4 final: player (mpv, VLC com autoplay de
  legendas) carrega como faixa extra e "duplica" mesmo. Intermediário vai pra `intermediarios/`.

## 12. B-roll do Pexels vem mudo (e `-map` só de vídeo mata o áudio)

- Quase todo clipe do Pexels traz pista de áudio **digitalmente muda** (-91dB) — medir, não
  assumir. Se a cena de b-roll for a última do vídeo, o silêncio aparece como "fim mudo".
- Ao usar `-map 0:v` num comando ffmpeg, o áudio **não é mapeado por padrão**: sem `-map 0:a`
  a cena sai sem pista e o concat/ mix quebram em silêncio. Fonte muda → `anullsrc` (pista muda
  explícita) pra concat funcionar; fonte com som → `-map 0:a`.
- Gravações de produto em celular costumam trazer **status bar + barra do navegador**; a barra
  vaza a URL do portal. Corte padrão: **130px** do topo (não 44px).

## 13. Variação do vencedor = "o copo azul" (`YT:Hwu1hmmM4_Q`, 08/10/2026)

Regra nova do Kevones, dita por ele no vídeo do R$ 47. Vale para **imagem e vídeo**:

- **Não muda:** o **produto** e a **copy**.
- **Muda:** **quem** e **onde**. Ele validou "Copo azul. Compre agora." e a partir daí fez
  o Isaque segurando o copo, o copo na mesa, o copo na cadeira, o Kevones de óculos na praia —
  **sempre o mesmo copo azul, sempre a mesma copy**.
- Aplicando: **vídeo vencedor → imagem e carrossel com a mesma copy**; **estático vencedor →
  designs novos, mesma copy e mesma cor**. (Na Elétrica: variação do CT 04.)
- ⚠️ **Não é** a variação rasa de 2025 que ele derrubou (aquela trocava gancho/música/cor do
  conteúdo). E continua valendo: variação entra em **campanha nova**, nunca adicionada na
  campanha que está rodando, e **nunca** duplicando campanha idêntica (duplicar em 2026 é o
  que trava o ROI em 1,3).

Regra completa e fontes em `criativo-ads/references/kevones-criativo.md` (§ "A variação que
ele AUTORIZA") e em `metaads-kevones/references/DECISOES.md` §18.
