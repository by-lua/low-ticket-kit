# ninjabrhub.io — relogar e regravar o refresh_token

**Verificado por execução em 2026-09-02** (projeto LOW-TICKET, criativos do
Catálogo do Ferreiro Rural).

Complementa `imagem-lote-serializado.md`, que descreve o sintoma
(`refresh_token_already_used`) mas não o conserto executado.

## Sintoma

```
[erro] refresh falhou 400: {"code":400,"error_code":"refresh_token_already_used",
"msg":"Invalid Refresh Token: Already Used"}
```

Não adianta repetir. O `.hub-creds.json` está com um refresh_token já queimado —
outra sessão o usou (ele rotaciona a cada uso) ou a sessão do perfil expirou.

## Conserto, na ordem

```bash
~/.claude/bin/lane.sh take hub <lane>
agent-browser --session hub-<lane> get url        # caiu em /auth? entao deslogou
```

Deslogado, o `localStorage` do Supabase volta `null` — o eval devolve `SEM TOKEN`,
não um erro. Não confunda com problema de seletor.

```bash
set -a; . ~/.claude/.credentials.env; set +a     # NINJABR_EMAIL / NINJABR_PASSWORD
agent-browser --session hub-<lane> snapshot -i -c   # pega os refs
agent-browser --session hub-<lane> focus @<ref EMAIL>
agent-browser --session hub-<lane> keyboard inserttext "$NINJABR_EMAIL"
agent-browser --session hub-<lane> focus @<ref SENHA>
agent-browser --session hub-<lane> keyboard inserttext "$NINJABR_PASSWORD"
```

**Confirme o preenchimento contando caracteres, nunca imprimindo valor:**

```bash
echo "(()=>[...document.querySelectorAll('input')].map(x=>x.type+':'+(x.value?x.value.length:0)).join(' '))()" \
  | agent-browser --session hub-<lane> eval --stdin
# email:27 password:12 hidden:773 file:0 text:0
```

O `hidden:773` é o **token do Cloudflare já resolvido**. Nesse perfil o desafio
valida sozinho: se o hidden tem centenas de chars, não clique no widget, só envie.
Hidden em 0 = o desafio ainda não passou; aí sim clique no checkbox.

Botão `ENTRAR` → em ~8s a URL vira `/inicio` e o token aparece.

```bash
RT=$(echo "(()=>JSON.parse(localStorage.getItem('sb-bbwgequqwrsmbrkdmsxm-auth-token')).refresh_token)()" \
  | agent-browser --session hub-<lane> eval --stdin | tr -d '"' | tail -1)
# regravar SÓ a chave refresh_token, preservando anon
python3 -c "import json,sys;p='.hub-creds.json';c=json.load(open(p));c['refresh_token']=sys.argv[1];json.dump(c,open(p,'w'),indent=1)" "$RT"
chmod 600 .hub-creds.json
```

Arquivo: `GERADOR-AUDIO-HUB/.hub-creds.json`, chaves `anon` e `refresh_token`.

## Um dono por vez

O refresh_token rotaciona a cada uso: **dois agentes usando o mesmo
`.hub-creds.json` se derrubam mutuamente**. Quem renovar avisa os outros para não
relogarem. Rodando um pane em paralelo, mande-o usar o `artlist-proxy`
(GPT Image 2), que além de não ter a fila do google-flow não disputa nada.

## imagen-4 COM pessoa descrita: funciona

`imagem-lote-serializado.md` registra "prompt com pessoa identificada por idade e
nacionalidade volta vazio". **Não se confirmou aqui.** Um prompt com
`a 45-year-old Brazilian man from rural Minas Gerais, sun-weathered tanned skin,
short dark hair, thick moustache, brown leather blacksmith apron` gerou normalmente,
768×1376 em `--aspect 9:16`, rosto coerente e sem marca d'água.

Provável causa do caso antigo: era `generation_busy` (a fila) lido como resposta
vazia — exatamente o modo de falha que aquela mesma receita descreve. Antes de
concluir que o filtro barrou a pessoa, imprima a resposta crua e procure
`_errorCode`.

## Dimensão de saída

`--aspect 9:16` devolve **768×1376**, não 1080×1920. Serve como primeiro frame de
vídeo; o upscale para 1080×1920 é na montagem, com lanczos.
