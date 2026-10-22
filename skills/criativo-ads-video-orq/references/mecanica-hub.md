# Mecânica: gerar vídeo no NinjaBR Hub (Veo 3.1)

> Precisa de **assinatura própria** do NinjaBR Hub (`ninjabrhub.io/studio`). Sem ela,
> use o Flow (`mecanica-flow.md`). Setup de browser/lane: `browser-setup.md`.
> Este arquivo é o resumo operacional. **Detalhe completo, ~1.200 linhas de casos
> de falha reais: skill `hub-video-playwright`** (carregue quando algo divergir).
> O QUE gerar (roteiro, prompt, orçamento de palavras, blocos anti-morphing) vem
> deste orq; aqui só o COMO apertar os botões.

## Regras que não se negociam

1. **Sempre Imagem→Vídeo.** A imagem é o primeiro frame e trava rosto, roupa, luz e
   cenário. Texto→vídeo inventa outra pessoa e outra voz. A imagem sai do ChatGPT
   (`gpt-imagem-playwright`) e passa pelo gate de imagem antes.
2. **Motor `Veo 3.1 (Imagem→Vídeo)`, modelo `Veo 3.1 - Quality`, 9:16, 8s.** O Hub
   abre em `Auto` + `Lite` + `16:9`; reload e troca de motor **resetam** tudo, em
   silêncio. Confira as DUAS (proporção e duração) imediatamente antes de CADA envio.
   Duração errada só aparece no `ffprobe`, depois de a cota ter sido gasta.
3. **Grok Imagine é fallback** quando a cota do Veo acaba. Não use Lite/Fast em
   criativo que vai veicular.
4. **O Hub não limpa nada entre gerações** (texto e imagem ficam grudados). Ordem
   de envio, sempre: apagar texto → remover anexo (`aria-label="Remover"`) →
   conferir motor/formato/duração → anexar imagem e conferir que há exatamente 1
   anexo → colar o prompt → conferir que o texto que entrou é o do arquivo (compare
   a CAUDA, onde ficam os blocos adicionados por último) → só então `Enviar`.
5. **Prompt colado pelo setter nativo do React** (`Object.getOwnPropertyDescriptor(
   HTMLTextAreaElement.prototype,'value').set` + evento `input`), nunca digitando.
   Limite de **2500 caracteres**.
6. **NEGATIVE padrão** no prompt: legenda/texto na tela, morphing, mão dentro do
   tecido, roupa flutuando, dentes deformados (blocos exatos no SKILL.md deste orq).
7. **Cada clique conta como requisição.** Nunca retry rápido em `Enviar`. O botão é
   um ícone: ache por `aria-label`, não por texto. O widget de suporte (`gc-w-*`)
   cobre o botão: esconda antes de cada clique. Dropdown aberto trava o clique sem
   erro nenhum.
8. **Prova de envio = a barra travar** (spinner/contador subir), não o retorno do
   clique. Leia o contador antes e depois.
9. **Um envio = dois jobs no Hub** (o render do modelo e um re-roteado). Baixe o do
   modelo (`veo-3-1-i2v`), não o reroteado. Escolha o arquivo **pelo conteúdo**
   (compare com o `src` novo que apareceu), não pela posição no histórico: o
   histórico é da CONTA, não da sua aba.
10. **Baixe com `curl`**, não com `fetch` no browser (CORS mata). Nome com o prefixo
    da lane. Valide com `ffprobe` (duração, 720×1280, áudio presente) antes de
    considerar entregue.
11. **Espera:** polling curto, teto generoso; meça antes de culpar o Hub. A aba pode
    cair para `about:blank` no meio: refixe a lane DENTRO do loop de espera.
12. **"Google Flow rejeitou a geração" repetido** = saturação do backend, não o
    prompt. Pare, espere ou troque de motor (Kling 2.5 Turbo Imagem→Vídeo roda em
    pipeline separado) — ou gere no Flow direto (`mecanica-flow.md`).
13. **Contador "59/60 Gerações":** o número da ESQUERDA é o que SOBRA.
14. **Aba do Hub congela às vezes** (timeout de CDP): não é o site caindo.
    `lane.sh take hub <lane>` reabre e mantém o login.

## Gate de envio (rode antes de CADA clique em Enviar)

| Item | Esperado |
|---|---|
| Texto do textarea | igual ao arquivo do prompt (tamanho E cauda) |
| Anexos | exatamente 1, e é a imagem DESTA cena |
| Motor / modelo | Veo 3.1 (Imagem→Vídeo) / Quality |
| Proporção / duração | 9:16 / 8s |
| Contador de gerações | anotado, para conferir que subiu depois |
| Aba | a sua (lane fixada) |

## Fila em lote

`scripts/fila.sh`, `gate.sh`, `bind.sh` e `valida_img.sh` deste orq rodam a leva
cena a cena com esses gates (`PROJETO=/pasta/do/criativo` antes de chamar). Mate
fila pelo GRUPO (`kill -9 -PGID`), nunca só pelo PID do script.
