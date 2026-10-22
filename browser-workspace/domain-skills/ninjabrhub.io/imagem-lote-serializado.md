# ninjabrhub.io — gerar VÁRIAS imagens (a fila de uma por vez)

**Verificado por execução em 2026-09-02.** Complementa `studio-image-video-api.md`,
que cobre uma geração isolada. Esta receita é sobre gerar um lote.

## O que morde

O backend aceita **uma geração por vez, por conta**. A segunda chamada volta:

```json
{"error":"Você já tem uma geração em andamento. Aguarde a conclusão antes de iniciar outra.",
 "_upstreamStatus":429,"_errorCode":"generation_busy","activeJob":null}
```

`activeJob` vem `null` mesmo com o lock ativo — não dá para consultar o que está
rodando, só esperar. O `gerar-midia.py` mostra isso como **"[erro] nenhuma imagem
retornada"**, que parece falha de conteúdo e não é. O sintoma característico:
**a primeira chamada funciona, todas as seguintes falham**, inclusive prompts
triviais que acabaram de funcionar. Se isso acontecer, é fila, não prompt.

Antes de culpar o prompt, imprima a resposta crua e procure `_errorCode`.

## Solução: retentar com espera

Ferramenta em `/tmp/hubimg.py` (recriável): mesma chamada, mas se vier
`generation_busy` dorme 20s e tenta de novo, até 30 vezes. O lock costuma
liberar em ~1-2 min. Gere **em série**, nunca em paralelo — panes concorrentes
disputando a mesma conta só se bloqueiam.

```python
r = call(access, anon, {"provider":"google-flow","action":"create_image",
     "payload":{"prompt":P,"model":"imagen-4","aspectRatio":"1:1","count":1}})
if r.get("_errorCode") == "generation_busy":
    time.sleep(20); continue
```

## Token: o passo que sempre falta

`refresh_token` **rotaciona a cada uso**. Se o `.hub-creds.json` ficou parado,
o refresh volta `400 refresh_token_already_used`. Aí não adianta insistir:

1. `~/.claude/bin/browsers.sh hub`
2. Se cair em `/auth`, logar com `$NINJABR_EMAIL` / `$NINJABR_PASSWORD`
   (o Cloudflare desse perfil já valida sozinho)
3. `agent-browser --session hub eval "JSON.parse(localStorage.getItem('sb-bbwgequqwrsmbrkdmsxm-auth-token')).refresh_token"`
4. Regravar em `GERADOR-AUDIO-HUB/.hub-creds.json`

## Texto na imagem: não peça

O `imagen-4` renderiza texto **em inglês e embaralhado**, mesmo com o prompt
pedindo outro idioma. Numa oferta em espanhol saiu "WELLNESS GUIDE" e
"PUBLISHED BY VITALITY INC." com letras deformadas.

Regra: **peça as capas em branco** ("completely blank, no text, no letters, no
typography, no logos") e escreva o título depois com PIL. Mesma lógica do desenho
técnico com cota — o que precisa estar correto não sai de IA generativa.

## Pessoas: evite descrever

Prompt com pessoa identificada por idade e nacionalidade ("Mexican woman around
70 years old") volta vazio. Não confirmei se é filtro ou coincidência de fila —
mas capa abstrata resolve e não depende da resposta.

## Aspect ratio

`16:9 4:3 1:1 3:4 9:16 auto landscape portrait`. **Não** aceita `square`.
