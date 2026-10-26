---
name: gpt-imagem-playwright
description: Gera imagens no ChatGPT usando o perfil de browser persistente já logado (sessão gpt). Aceita imagem de referência anexada para manter rosto, produto ou estilo, e gera até 10 imagens separadas por vez. Baixa os resultados direto para a pasta pedida. Use sempre que o usuário pedir para criar, gerar ou editar imagem no GPT/ChatGPT, pedir imagem de referência, mockup, cena, retrato, variação visual, ou disser "gera uma imagem".
---

# gpt-imagem-playwright

Gera imagens no ChatGPT pelo browser persistente já logado. **Execute, não explique** — o usuário conhece o fluxo.

> **Imagem que mostra O PRODUTO (mockup, página, capa de entregável, tela) SEMPRE
> leva a página/mockup REAL anexada como referência — nunca só descrição em
> texto.** Regra da dona (2026-10-04), depois de uma capa sair com conteúdo de
> outro produto inteiro: "o objetivo é ver o produto aparecendo". Antes de
> escrever o prompt, localize a página/mockup real (entregável gerado,
> screenshot aprovado, ou gravação de tela da dona), anexe-a (ver passo 2) e
> diga no prompt pra usar aquela imagem como referência de conteúdo/layout —
> nunca inventar outra tela. Sem anexo, o modelo inventa genérico sem relação
> com o produto.
>
> **Mas não é SÓ a capa (dona, 2026-10-09 — Tarô):** a referência de imagem de
> criativo é **capa + 2 a 3 páginas reais de entrega**, sempre. Anexa os 4 arquivos
> (capa + 3 páginas) e escreve no prompt que **o modelo escolhe DUAS das páginas**
> pra mostrar na cena — "nem muito, nem pouco". Anexar só a capa foi reprovado:
> "só a capa?" — a arte sai sem o produto aparecendo. As páginas visíveis na arte
> são SEMPRE arquivo real do produto; o modelo posiciona, não desenha página.

## Pegar a lane — PRIMEIRA COISA, SEMPRE

Vários Claudes usam este mesmo browser. Sem lane, todos caem na mesma aba e escrevem no mesmo chat.

```bash
~/.claude/bin/lane.sh take gpt <lane>      # ex.: lane.sh take gpt cozinha
S=gpt-<lane>                                # use $S em TODO comando daqui pra frente
```

Nome da lane = a tarefa (`cozinha`, `espanhol`, `tarot`), nunca número. Protocolo completo em `~/.claude/bin/LANES.md`.

Perfil persistente `~/.agent-profiles/gpt`, porta 9222, já logado. Nunca use `agent-browser open` (trava no Cloudflare) nem `close --all` (mata as abas das outras lanes). Ao terminar: `~/.claude/bin/lane.sh drop gpt <lane>`.

### Contas e perfis GPT (atualizado 2026-10-11, regra da dona)

**Conta PESSOAL (Dona) REMOVIDA em 11/10/2026 por ordem da dona.** Os 4 perfis
(`gpt-conta`, `-2`, `-3`, `-4` — portas 9252/9229/9240/9241) foram apagados do disco e do
`registry.conf`; backup em `~/.agent-profiles/_removidos-gpt-pessoal-2026-10-11/`. Não usar,
não recriar sem a dona mandar.

Resta **uma conta: Secundária (conta-secundaria)**, 4 perfis. Perfis da MESMA conta dividem a cota de
imagem: trocar de perfil dentro da conta não contorna limite.

| Nome | Conta | Perfil | Porta |
|---|---|---|---|
| Dona Secundária 1 | secundária (conta-secundaria) | `gpt-conta` | 9239 |
| Dona Secundária 2 | secundária | `gpt-conta` | 9243 |
| Dona Secundária 3 | secundária | `gpt-conta` | 9247 |
| Dona Secundária 4 | secundária | `gpt-conta` | 9259 |

`gpt` (9222) e `gpt-play-1` (9238) estão sem login: não usar.

**REGRA DA DONA (11/10/2026): perfil novo do GPT TEM que ser cadastrado no
`~/.claude/bin/gpt-contas.lst`, senão o `gpt-livre.sh` não enxerga e ele devolve
"SEM PERFIL GPT LIVRE" mesmo com o perfil novo funcionando.** A lista é separada do
`registry.conf` de propósito: ela é só dos perfis **logados** (o registry tem o `gpt` e o
`gpt-play-1`, que não servem). Para adicionar perfil novo:

1. `~/.claude/bin/browsers.sh add <perfil> <porta> https://chatgpt.com` e pedir login à dona
2. acrescentar a linha `<conta> <perfil> <porta>` em `~/.claude/bin/gpt-contas.lst`

**Sempre pegar perfil por `S=$(~/.claude/bin/gpt-livre.sh <lane>)`**: ele lê essa lista, pula
perfil ocupado ou deslogado e imprime no stderr qual conta/perfil pegou. **Cota acabou**
(card nativo "Você atingiu o limite… Tente de novo à(s) HH:MM", depois dos checks do item 8):

```bash
~/.claude/bin/gpt-livre.sh --esgotou secundaria 14:21
S=$(~/.claude/bin/gpt-livre.sh <lane>)   # avisa que não tem cota e para
```

Conta secundária sem cota = parar e avisar o orquestrador com o horário de reset. Perfil
deslogado = pedir à dona para logar naquela janela (não há credencial salva).

Se aparecer o desafio do Cloudflare ("Confirme que é humano"), **clique nele** — nesse Chromium ele valida normalmente. Se aparecer de novo, clique de novo.

> **⚠️ 13/10/2026 — três seletores da skill morreram na UI nova.** Medido no perfil
> `gpt-conta`; se o teu script segue o texto antigo, ele falha **em silêncio**:
> 1. **Anexo:** `input[type=file]` pega o input errado (`_r_b_`) — responde `✓ Done` e não sobe nada.
>    O do composer é o **segundo**: `input[type=file]:nth-of-type(2)` (`_r_d_`, `accept=image/*,video/*`).
> 2. **Dono do chat:** `[data-message-author-role]` não existe mais. Use **`.bg-user-message`**.
>    E o `eval` devolve a string **entre aspas** (`"MINHA"`) — compare com `| tr -d '"'`.
> 3. **`S=$(gpt-livre.sh <lane>)`** devolve `conta: … | perfil: …` **no stdout** antes do nome da
>    sessão. Sem `| tail -1` a variável fica com lixo, o `agent-browser` reclama de nome longo e o
>    sintoma é `chat nao e meu ("vazio")`.
> Referências: memória `gpt-livre-sessao-precisa-tail-1`, `gpt-imagem-playwright-seletor-arquivo-nth-2`,
> `gpt-playwright-seletor-mensagem-bg-user`.

## 🚨 ANEXO NÃO ENTRA mas a conta está "livre"? NÃO É BUG — leia isto antes de tentar outro caminho

Sintoma: `upload` responde `✓ Done`, o preview nunca aparece, o contador `backend-api` não sobe, e **nenhum** caminho funciona (nem `upload`, nem `setFileInputFiles`, nem JS). O agente costuma culpar o Playwright e ficar tentando variantes — **não faça isso**. Faça este diagnóstico de 1 minuto:

**1. Cota de UPLOAD é separada da cota de GERAÇÃO.** Banner no topo do chatgpt.com:
> "Você atingiu o limite de uploads de arquivos. Tente novamente em 20 horas."

A conta pode gerar imagem de sobra e mesmo assim **não aceitar nenhum anexo**. Sem referência não há geração — logo, conta com upload esgotado é conta inutilizável pro fluxo deste skill, mesmo com `gpt-livre.sh` dizendo que está livre. Cadastre com `gpt-livre.sh --esgotou pessoal <reset>` e pegue a outra conta.

**2. A aba pode ter caído num PROJETO do ChatGPT, não num chat.** Na lateral aparece "Fixada" / "Abrir página inicial do projeto" / "Projetos". Os `input[type=file]` dessa tela são do editor de projeto e **aceitam o comando `upload` sem erro mas não sobem arquivo nenhum** — mesma falha silenciosa. Sempre: `navigate chatgpt.com` → clicar em **"Novo chat"** (ref `e24`/`e12` da sidebar) e só então anexar.

**3. O composer pode estar em MODO WORK e não em CHAT — envio morto (medido 14/10/2026, GeriNeuro).**
O composer novo tem um par de toggle `button "Chat"` × `button "Work"`. Quando está em **Work**
o placeholder é `Trabalhe com o ChatGPT` (não `Pergunte ao ChatGPT`), o heading acima diz
`No que vamos trabalhar?`, e o `button "Enviar"` vem **`[disabled]`** se a conta está sem
créditos de Work — banner no rodapé: *"Você atingiu o limite de uso do Work por enquanto …
redefinido às HH:MM"*. Sintoma do script: anexo sobe, prompt cola (`composer_len == tamanho do
arquivo`), clique "clicou" responde ✓, mas `composer` **não zera** e `msgs_user == 0` — o lote
loga `FAIL: nao enviou` ou `FAIL: geracao falhou` 3× seguidas pra fichas diferentes (parece
rate limit, não é). Correção: clicar no toggle `Chat` **antes** de digitar/anexar — o texto já
colado e o anexo **sobrevivem** à troca de modo. Confirme o modo pelo placeholder do textbox
(`Pergunte ao ChatGPT`) antes de colar o prompt, não pelo banner (o banner de Work fica visível
mesmo em modo Chat e engana).

Ordem ao anexar, sem improvisar:
```bash
S=$(~/.claude/bin/gpt-livre.sh <lane>)
agent-browser --session $S navigate "https://chatgpt.com/" >/dev/null; sleep 4
agent-browser --session $S snapshot -i -c | grep -iE "Novo chat|Projetos|Fixada"   # confirma que é chat, não projeto
# se aparecer "Projetos/Fixada": clique em "Novo chat" e espere
```

> **⚠️ 25/10/2026 — caminho de arquivo: SEMPRE absoluto, e o diretório de trabalho NÃO pode ter
> espaço.** Dois erros medidos no Mapa del Tarot AR, os dois silenciosos:
> 1. **`upload` com caminho relativo** resolve contra o cwd do *agent-browser*, não o do shell →
>    sobe arquivo de 0 byte e o único sinal na UI é o toast vermelho **"O arquivo está vazio"**
>    (o comando responde `✓ Done` do mesmo jeito). Passe caminho absoluto.
> 2. **`gerar-imagem-gpt.sh` quebra se o caminho tiver espaço** (`PROJETOS - INTERNOS`):
>    `$P` não é citado no script (`cat $P`, `head -c 40 $P`) → `cat` falha, o `inserttext` vai
>    vazio, o script responde `FAIL dono`. Rode o script de dentro de uma pasta **sem espaço**
>    (ex.: `/tmp/<oferta>/p5`) com os anexos também em `/tmp`, e mova o resultado pro projeto
>    depois.
>
> **`gpt-livre.sh` pode devolver perfil com 1 aba `/c/` ocupada** (a checagem dele só descarta
> com >1). Sintoma: você anexa e a tela mostra outro chat, com prompt de outra oferta. Antes de
> gerar, `curl -s http://127.0.0.1:<porta>/json/list` e confirme que **nenhuma** aba está em
> `chatgpt.com/c/`; outra lane no mesmo perfil = peça de outro agente.

**Gate de upload: conte QUALQUER preview, não só `backend-api`.** A UI mudou — o preview no composer hoje é `data:image/...;base64` (upload local), e o servidor só devolve `backend-api` DEPOIS que o prompt é enviado. Contar só `backend-api` dá falso negativo: o anexo está lá e o agente acha que falhou, joga fora uma referência boa e entra em loop de retentativa.

Gate confiável (serve nos dois casos):
```bash
CNT="(()=>[...document.querySelectorAll('img')].filter(i=>i.src.startsWith('data:image')||i.src.includes('backend-api')).length)()"
N0=$(echo "$CNT" | agent-browser --session $S eval --stdin | tr -dc '0-9')
agent-browser --session $S upload 'input[type=file]:nth-of-type(2)' "$REF"
for k in $(seq 1 40); do
  n=$(echo "$CNT" | agent-browser --session $S eval --stdin | tr -dc '0-9')
  [ "${n:-0}" -gt "${N0:-0}" ] && break; sleep 3
done
[ "${n:-0}" -gt "${N0:-0}" ] || { echo "FAIL: anexo nao subiu"; exit 1; }
```
Sinal extra, o mais direto de todos: o botão de remover mostra o nome do arquivo **renomeado pelo ChatGPT** (ex.: `Remover 01-capa(20261008-232320).png`). Se esse botão apareceu com o nome entre parênteses, o upload CONCLUÍU — não é o botão "Remover ficheiro N" cru, que aparece antes de o upload terminar.
CNT="(()=>[...document.querySelectorAll('img')].filter(i=>i.src.includes('backend-api')).length)()"
N0=$(echo "$CNT" | agent-browser --session $S eval --stdin | tr -dc '0-9')
agent-browser --session $S upload 'input[type=file]:nth-of-type(2)' "$REF"
# esperar contador subir; se NÃO subir em ~40s: ou é cota de upload, ou é aba de projeto. Não tente outro caminho — refaça o diagnóstico.
```
Último recurso de prova: screenshot da tela. Banner de cota e miniatura do anexo são visíveis lá e resolvem em 1 olhar.

Se aparecer botão "Entrar", a conta caiu: peça ao usuário para logar naquela janela (a conta do ChatGPT é pessoal e não tem credencial salva).

## Fluxo

### 1. Novo chat DENTRO da lane

Comece sempre num chat limpo — contexto de imagem anterior contamina o resultado. Navegue direto; **nunca clique numa conversa do histórico**, pode ser de outra lane.

```bash
agent-browser --session $S tab <lane>                    # re-fixar a aba
agent-browser --session $S navigate "https://chatgpt.com/"
sleep 3
agent-browser --session $S snapshot -i -c        # pegar o ref do textbox
```

### 2. Anexar referência (quando houver)

> **Referência acima de ~1 MB FALHA no upload — "Falha no upload" não é cota de conta (11/10/2026).**
> Medido no Jiu-Jitsu: PNG de 1,5 MB deu `FAIL upload` três vezes seguidas na mesma conta que
> depois gerou imagem sem problema. JPG de 150–270 KB passa. Converta as referências antes de anexar
> (mesma pasta `_refs/`, um JPG por referência):
> ```bash
> convert "$orig" -resize 1000x -quality 84 "_refs/$(basename "$orig" .png).jpg"
> ```
> Se o upload falhar **e** a conta não estiver com banner de cota: cheque o **tamanho** antes de
> trocar de conta.

```bash
agent-browser --session $S upload 'input[type=file]:nth-of-type(2)' /caminho/referencia.png
```

**`"Remover ficheiro 1: ..."` no snapshot NÃO prova que o anexo subiu.** Esse
botão aparece assim que o arquivo entra no input, antes do upload terminar. Se
você enviar nessa janela, o prompt vai **sem a referência** — e o sintoma é
silencioso: a miniatura no chat fica um quadrado vazio e a imagem sai sem
nenhuma herança visual da referência.

O sinal de upload concluído é o **preview**: uma `<img>` com src em
`chatgpt.com/backend-api/` **ou** `data:image/...;base64` (upload local — é o
que a UI mostra hoje, já que o servidor só responde depois do prompt ser
enviado). O jeito certo de esperar é **contar antes de anexar e esperar o
contador subir** — sem depender de dimensão nem de peso:

```bash
CNT="(()=>[...document.querySelectorAll('img')].filter(i=>i.src.startsWith('data:image')||i.src.includes('backend-api')).length)()"
N0=$(echo "$CNT" | agent-browser --session $S eval --stdin | tr -dc '0-9')

agent-browser --session $S upload 'input[type=file]:nth-of-type(2)' "$REF"

for k in $(seq 1 40); do
  n=$(echo "$CNT" | agent-browser --session $S eval --stdin | tr -dc '0-9')
  [ "${n:-0}" -gt "${N0:-0}" ] && break; sleep 3
done
[ "${n:-0}" -gt "${N0:-0}" ] || { echo "FAIL: anexo nao subiu"; exit 1; }
```

**Nunca trave numa dimensão fixa.** Errei isso: usei `naturalWidth===600` depois
de ver o preview da primeira referência em `600x600`, e as três referências
seguintes falharam todas no gate. O preview **mantém a proporção da referência**
— a segunda ref veio `338x600`. 600 é só o lado maior. Peso também não serve:
o teto de tempo tem que cobrir a maior ref do lote (a de 627 KB estourou 36s e
passou com 120s), então dê folga em vez de calibrar.

Contador é o sinal certo porque não assume nada sobre o arquivo — vale pra
qualquer referência, qualquer proporção, qualquer tamanho.

Medido: ~7s numa ref de 220 KB, ~40s numa de 627 KB.

### 3. Enviar o prompt

> **Pegue o `@ref` do textbox pelo snapshot — `focus "div#prompt-textarea"` NÃO funciona.**
> Esse seletor não existe nesse DOM (medido 11/10/2026, Jiu-Jitsu). Do jeito certo:
> ```bash
> TB=$(agent-browser --session $S snapshot -i -c 2>/dev/null \
>      | grep -oiP '(textbox|textarea)[^\]]*\[ref=\K[^\]]+' | head -1)
> agent-browser --session $S focus "@$TB"
> ```
> E **confirme o envio pelo `innerText.length` do composer**, nunca por "clicou" — clique
> sem enviar deixa o prompt parado no campo.

> **Hífen/underscore no texto do prompt QUEBRA o envio.** Pedir a ortografia com marcação tipo
> `V-O-C-E-ACENTUADO` fez o ChatGPT responder *"o que gostaria que eu criasse?"* — o prompt não
> chegou. Escreva as palavras normalmente e peça o acento **por extenso** ("com o acento
> circunflexo no O de VOCE"), sem separadores.
>
> **⚠️ Isso NÃO significa tirar o acento do texto do prompt (confundido 25/10/2026, Mapa do
> Tarot BR — 7 peças saíram sem acentuação e tiveram que ser regeradas).** O bug é só o
> hífen-pra-soletrar; escrever a palavra inteira **com acento normal** (`será`, `só`, `não`,
> `é`) no meio da frase passa numa boa. Se o prompt tirar o acento pra "evitar problema", a
> imagem sai **sem acento** — não evita nada, só produz peça errada. **Declare o idioma e peça
> acento explicitamente**: `written in correct Brazilian Portuguese WITH proper accent marks,
> render the accent marks (á, ó, ã, ê...) clearly and correctly` (PT) ou `texto en español con
> tildes correctas: é, á, í, ó, ú, ñ` (ES). Confira sempre com crop da área do texto em
> full-res antes de aprovar — ver memória `acentuacao-espanhol-declarar-prompt`.

> **Declare o IDIOMA do texto explicitamente no prompt, sempre** (dona, 25/10/2026 — Mapa del Tarot
> AR). Nunca assumir que o modelo acerta acento sozinho fora do português: peça "texto en español
> rioplatense con tildes correctas (á, é, í, ó, ú, ñ)" / "texto in English" explicitamente, mesmo
> quando o resto do prompt já está no idioma certo. Confira palavra por palavra antes de aceitar a
> peça — acento errado é QA bloqueador, regenera.

> **O texto que VOCÊ escreve dentro do prompt (o texto que vai aparecer na imagem/anúncio) tem que
> sair já com acentuação correta no idioma certo — o modelo reproduz fielmente o que você digitou,
> inclusive o erro** (dona, 25/10/2026). Bug real: prompt escrito "Diagnostico"/"Medico"/"Tarjeta
> Rapida"/"linea" (sem acento) saiu assim na imagem, sem nenhum defeito do GPT — a imagem só copiou
> o texto exatamente como foi mandado. Antes de enviar qualquer prompt com texto em espanhol/
> português/francês etc dentro de aspas, releia cada palavra com acento (á, é, í, ó, ú, ñ, ã, ê, ç)
> e corrija no PRÓPRIO arquivo do prompt — não deixe pra corrigir só depois de ver a imagem errada.

Escreva o prompt num arquivo e use `keyboard inserttext` — `fill` quebra com texto longo e caractere especial.

> **`inserttext` trunca na primeira quebra de linha/aspas (medido 2026-10-09, Tarô).**
> Um prompt de 10 linhas chegou ao modelo cortado na **primeira linha** — o modelo
> respondeu perguntando o texto do título e a geração foi perdida. Faça o prompt
> **uma linha só, sem aspas duplas** (`"` vira quebra), e confirme o envio pelo
> começo da mensagem que aparece no chat ("Você disse: …"): se ali só tem a
> primeira frase, o prompt truncou — reenvie inteiro antes de esperar imagem.

```bash
agent-browser --session $S focus @eN
agent-browser --session $S keyboard inserttext "$(cat prompt.txt)"
agent-browser --session $S click @eENVIAR      # button "Enviar prompt"
```

**O countdown do seu gate vai ACENDER com as PRÓPRIAS REFERÊNCIAS (medido
12/10/2026).** As referências anexadas entram no DOM como `img` com
`naturalWidth` 1000-ish e o filtro `naturalWidth>700` as conta como se fossem a
geração. Resultado: o monitor dispara "PRONTO" na hora, ~8 min antes, e o
`fetch` do blob devolve `null` (`b64` vazio → `AttributeError` no decode).

**Gate que não dá falso positivo** — a geração tem `src` `blob:` e **mede
1155×1491** (a ref é 1000×1250):

```js
(()=>{const g=[...document.querySelectorAll('img')].filter(i=>i.naturalWidth>700);
 const nova=g.filter(i=>!i.src.startsWith('data:image/jpeg'));
 return nova.length+" "+JSON.stringify(g.map(i=>i.naturalWidth+'x'+i.naturalHeight));})()
```

Esperar `nova.length >= 1`, ou casar `1155` no JSON de dimensões.

**"A geração de imagens falhou" costuma ser FALTA DE REFERÊNCIA, não cota.**
Sintoma medido 12/10: chat novo ("Novo chat"), prompt enviado sem anexar nada, o
modelo responde *"Envie as três imagens de referência de estilo"* e para — sem
banner de cota nenhum. Com os anexos no composer antes de enviar, funciona
normalmente. Se a resposta do modelo pedir as referências, é isso — reanexar e
reenviar no MESMO chat, não abrir outro.

**`gpt-livre.sh` escolhia conta errada por causa de comentário no cadastro.**
O `awk '{print $1}'` da lista de contas tratava linha começando em `#` como nome
de conta. Corrigido em 12/10/2026 para `awk '$1 !~ /^#/ && NF>=3 {print $1}'` nos
dois pontos (`ORDEM` e o laço de perfis). Se o script escolher perfil errado
depois de editar `gpt-contas.lst`, é essa linha — confira o filtro. **E: nunca
comece um comentário em `gpt-contas.lst` com o nome de uma conta**, senão o bug
reaparece.

**O botão de envio não tem mais `data-testid="send-button"`.** Verificado em
2026-08-30: é `button[aria-label="Enviar prompt"]`, classe `composer-submit-btn`.
**ATUALIZADO 12/10/2026: hoje é `button[aria-label="Enviar"]`** — SEM a palavra
"prompt". A skill antiga quebrava aqui: o seletor antigo devolve `null` e o script
morre achando que não existe botão. Use sempre o fallback com os dois:

```js
document.querySelector('button[aria-label="Enviar"]')
  || document.querySelector('button[aria-label="Enviar prompt"]')
  || document.querySelector('.composer-submit-btn')
```

**O composer também mudou:** não existe mais `#prompt-textarea`. É
`div.ProseMirror` (sem id). Para conferir que colou, compare o `innerText` do
composer com o `wc -c` do arquivo.

**Enter no `#prompt-textarea` NÃO envia** (testado com `Input.dispatchKeyEvent`
keyDown/keyUp Enter: nada acontece). O caminho é o clique.

## Quanto tempo UMA imagem leva — 60 a 70 segundos, não minutos

Medido em produção (leva de 9 imagens 9:16, 2026-08-30), etapa por etapa:

| Etapa | Tempo |
|---|---|
| navegar + composer aparecer | 6s |
| digitar o prompt | 3s |
| enviar + confirmar que enviou | 6s |
| **ChatGPT gerando** | **~50s** |
| baixar + validar dimensão | 5s |
| **total** | **~63s** |

**Se uma imagem está levando minutos, o problema é o SEU loop de espera, não o
ChatGPT.** Na mesma leva, um polling com `sleep 15` e teto de 60 iterações produziu
imagens levando 9, 20 e 21 minutos, e uma abortada por timeout — enquanto a geração
real levava 50 segundos. Duas causas somadas:

- **`sleep 15` desperdiça até 15s por imagem** e, pior, faz parecer que o serviço
  está lento quando o lento é o loop.
- **Teto curto aborta cedo.** 60 × 15s parece 15 min, mas cada iteração ainda soma o
  tempo do `eval`; o loop estourava antes de imagens que teriam saído.

Use **`sleep 5` e teto de 120 iterações** (10 min reais de margem). Um `eval` custa
~157ms, então polling curto é barato — medido, não estimado:

```bash
for i in 1 2 3; do a=$(date +%s%N)
  echo '(()=>1)()' | agent-browser --session $S eval --stdin >/dev/null 2>&1
  b=$(date +%s%N); echo "eval $(( (b-a)/1000000 ))ms"; done
```

**Instrumente o script com timestamps por etapa** antes de culpar a ferramenta. Sem
isso você reporta ao usuário que "o ChatGPT está engasgando" quando o gargalo é seu:

```bash
T0=$(date +%s); ts(){ echo "  [$(( $(date +%s)-T0 ))s] $1"; }
```

Régua: **acima de ~2 min numa imagem, suspeite do seu código primeiro.**

## Paralelizar: uma aba por imagem, no máximo 4 a 5

A serialização obrigatória é **uma cena por mensagem** (lote volta grid) — ela não
obriga a gerar uma imagem por vez. Com aba própria por imagem, N imagens saem no
tempo de uma.

Vale a partir de ~5 imagens: 9 imagens seriais levam ~10 min; em 4 abas, ~3 min.
Abaixo disso não compensa o modo de falha.

**Teto de 4 a 5 abas.** Mais que isso satura o browser e aumenta a colisão.

**O risco é real e silencioso:** abas concorrentes trocam imagem entre criativos, e o
arquivo sai com dimensão certa e conteúdo alheio — passa por `ffprobe`, por hash e
por contagem de arquivos. A trava é a **verificação de dono por conteúdo**,
obrigatória em cada aba antes de baixar:

```bash
SIG=$(head -c 40 "$PROMPT" | tr -d '\n')
cat <<EOF | agent-browser --session $S eval --stdin
(()=>{const m=document.querySelectorAll('.bg-user-message');
 if(!m.length) return 'vazio';
 return (m[0].innerText||'').indexOf("$SIG")===0 ? 'MINHA':'ALHEIA';})()
EOF
```

`ALHEIA` = descarte aquela aba e refaça a imagem. Nunca baixe.

Em série, mantenha a checagem de aba vazia (`msgs == 0`) antes de enviar; em
paralelo, as duas — vazia antes, e "MINHA" depois.

### 4. Esperar

> **⛔ 26/10/2026 — causa raiz das "imagens sem texto" (Tarot AR, 25–26/10): o GPT gera em DUAS
> passadas.** A foto aparece primeiro (já com `naturalWidth > 1020`, `blob:`), e o texto de Stories é
> escrito DEPOIS, numa segunda renderização da mesma imagem. Script que baixa quando a 1ª imagem
> aparece salva a versão SEM TEXTO — e ela passa em dimensão, hash e contagem. **Só baixe quando a
> geração TERMINOU:** botão `Parar` / `stop-button` sumiu do composer; aí espere ~6 s e pegue a última
> imagem grande. Já aplicado em `criativo-ads-imagem/scripts/gerar-imagem-gpt.sh`. Sintoma pra
> reconhecer: imagem perfeita, sem nenhuma caixa de texto, e o chat ainda com o botão "Parar".

```bash
bash -c "sleep 8; for i in \$(seq 1 120); do
  > **Espera pela imagem pronta, não pelo "Parar de responder" (11/10/2026).** Esse botão não existe
> no estado "Pensando" — o loop acima roda os 90s inteiros esperando um texto que nunca vem, e às vezes
> baixa antes da imagem existir. Espere a **contagem de blobs** crescer:
> ```bash
> for i in $(seq 1 90); do
>   n=$(echo "(()=>[...document.querySelectorAll('img')].filter(x=>x.naturalWidth>700&&x.src.startsWith('blob:')).length)()" \
>       | agent-browser --session $S eval --stdin | tr -dc '0-9')
>   [ "${n:-0}" -gt "$NB" ] && break; sleep 8
> done
> ```
> E pegue a **última** imagem do filtro (o modelo às vezes devolve duas). Antes de aceitar o arquivo,
> compare o `md5` contra as referências anexadas e contra os irmãos do lote — já baixou a própria
> referência por engano duas vezes com dimensão e peso perfeitos.

```bash
  if ! agent-browser --session $S snapshot -i -c 2>/dev/null | grep -q 'Parar de responder'; then echo DONE; break; fi
  sleep 5
done"
```

### O clique por `ref` FALHA de vez em quando — use eventos de mouse (2026-09-05)

Medido em produção: numa leva de 12 imagens, **todos** os envios falharam com o
campo cheio (`FAIL: nao enviou (campo=1330)`), com o botão **presente, habilitado
e não coberto** — `elementFromPoint` no centro devolvia o próprio botão. Só o
`agent-browser click @ref` é que não disparava o handler do React.

Trocar o clique por ref pelo **disparo completo de eventos** resolveu na hora.
Faça disso o padrão, não o fallback:

```bash
cat <<'JS' | agent-browser --session $S eval --stdin
(()=>{const el=document.querySelector('button[aria-label="Enviar prompt"]')
       ||document.querySelector('.composer-submit-btn');
if(!el||el.disabled) return 'sem botao';
const r=el.getBoundingClientRect();
const o={bubbles:true,cancelable:true,view:window,clientX:r.left+r.width/2,clientY:r.top+r.height/2,pointerId:1,isPrimary:true,button:0};
['pointerover','mouseover','pointermove'].forEach(t=>el.dispatchEvent(new (t.startsWith('pointer')?PointerEvent:MouseEvent)(t,o)));
el.dispatchEvent(new PointerEvent('pointerdown',o)); el.dispatchEvent(new MouseEvent('mousedown',o));
el.dispatchEvent(new PointerEvent('pointerup',o)); el.dispatchEvent(new MouseEvent('mouseup',o));
el.dispatchEvent(new MouseEvent('click',o)); return 'clicou';})()
JS
```

E confirme pelo campo zerar — `clicou` não prova envio.

### Baixar: DIFF de `src`, não marcação no DOM

Marcar as imagens existentes com `dataset` antes de enviar **não funciona**: o
React recria os nós e a marca some, e todas voltam a parecer novas.

O que funciona é capturar a lista de `src` **antes** do envio e ficar com a
diferença depois:

```bash
srcs(){ echo '(()=>[...new Set([...document.querySelectorAll("img")]
  .filter(i=>i.naturalWidth>800 && i.naturalHeight/i.naturalWidth>1.5)
  .map(i=>i.src))].join("|"))()' | agent-browser --session $S eval --stdin | tr '|' '\n'; }
srcs > /tmp/pre.txt          # ANTES de enviar
# ... envio e espera ...
NEW=$(srcs | grep -vxF -f /tmp/pre.txt | tail -1)
```

**Com várias referências anexadas isso é obrigatório.** O filtro por dimensão
sozinho pega o *preview da própria referência* — uma imagem-mãe 941×1672 tem
exatamente o formato do lote e passa como se fosse geração nova.

> **⚠️ Logo APÓS o envio, o anexo da referência aparece no DOM como um `blob:` NOVO
> (medido 14/10/2026, GeriNeuro — 9 downloads errados seguidos).** No composer o preview
> é `data:`/`blob:`; depois de enviar, a mensagem re-renderiza o anexo como um `blob:`
> com outro UUID. Como o `pre.txt` foi capturado antes disso, esse `blob:` da referência
> **conta como "imagem nova"** e o `tail -1` do diff escolhe *ele* — o gate de hash
> detecta (`md5` bate com o `.jpg` da referência) e o lote aborta inteiro com
> `FAIL: repetiu referencia/irmao` pra toda ficha, mesmo com a geração certa pronta
> ao lado. Não é imagem repetida, é o gate pegando o anexo.
> **Trava:** o `blob:` da *geração* é sempre **mais largo que o da referência** —
> filtre o diff por `naturalWidth > 1020` (a geração mede 1024–1060; a ref de
> 1000px mede 1000). E o `eval` do `agent-browser` devolve a string **entre aspas**:
> passe `tr -d '"'` antes de usar o `src` numa etapa seguinte, senão o `fetch("…")`
> herda aspas e morre com `SyntaxError: missing ) after argument list`.

### Baixou e falhou? A geração fica no chat — recupere, não regenere (14/10/2026)

Se o envio passou e a imagem gerou, ela **permanece no chat** mesmo depois que o download
falha ou o script aborta. Regenerar gasta cota à toa. Recuperar: navegue cada `/c/<uuid>`
do histórico e baixe de lá.

**Pegue os links pelo DOM, e não assuma a ordem.** A sidebar do perfil é **compartilhada
por todas as lanes** — os 3 primeiros `/c/` podem ser de outra lane (Tarot apareceu no meio
da fila do GeriNeuro). Nunca baixe por posição; identifique cada chat pelo conteúdo:

```bash
cat <<'JS' | agent-browser --session $S eval --stdin
(()=>[...new Set([...document.querySelectorAll('a[href*="/c/"]')].map(a=>a.getAttribute('href')))].slice(0,20))()
JS
# por chat: navegue, espere, e identifique pelo NÚMERO/PALAVRA-CHAVE da cena no 1º prompt
agent-browser --session $S navigate "https://chatgpt.com$H" >/dev/null 2>&1; sleep 6
cat <<'JS' | agent-browser --session $S eval --stdin
(()=>{const m=document.querySelector('.bg-user-message');
 if(!m)return '';const x=(m.innerText||'').match(/CARD (\d{3})/);return x?x[1]:'000';})()
JS
```

O **owner check pelo texto do prompt é obrigatório** aqui, mais ainda que no fluxo normal:
caso `000`/sem match = chat de outra lane, **pule**. Depois baixe a imagem `blob:` (ou
`https`) com `naturalWidth > 1020`, valide `md5` contra a referência e os irmãos, e renomeie
pelo número lido no chat. Recuperando assim, **9 de 9** fichas que o gate tinha recusado
foram salvas sem nenhuma regeneração.

### Rejeite o download que for igual a uma referência ou a um irmão do lote

Duas gerações do mesmo lote voltaram com **hash idêntico** — o modelo devolveu a
mesma imagem duas vezes, e o arquivo passou por dimensão, por peso e por
contagem. Compare o md5 do que baixou contra as referências anexadas e contra os
arquivos já salvos daquele lote; se bater, é lixo, apague e refaça:

```bash
NEW=$(md5sum < "$F")
for R in "$@"; do [ "$(md5sum < "$R")" = "$NEW" ] && { echo "baixou a REFERENCIA"; exit 1; }; done
for O in "$(dirname "$F")"/*.png; do [ "$O" != "$F" ] && [ "$(md5sum < "$O")" = "$NEW" ] && { echo "repetida"; exit 1; }; done
```

### Formato paisagem (16:9) — o filtro padrão descarta

O filtro de download é `naturalHeight/naturalWidth > 1.5`, que é retrato. Para
banner 16:9 inverta o critério (`naturalWidth/naturalHeight > 1.3`) e valide a
dimensão como "largura maior que altura", não contra um valor fixo. Saída típica
de banner: **1672×941**.

### Foto de referência com pele pode fazer a geração falhar

Um banner de shorts falhou **duas vezes seguidas** com "Something went wrong. If
this issue persists please contact us…" — não é o aviso transitório em português,
é erro real, e persistiu os 10 minutos de espera. A referência era a foto do
produto vestido, com as pernas da modelo à mostra.

**Recortar só a peça** (sem pele) e reenviar passou de primeira. Para roupa curta
— shorts, biquíni, lingerie — anexe o recorte da peça, nunca a foto com corpo.

### Enviou, chat criado, e NENHUMA resposta = engasgo, refaça

Distinga pelos **contadores**, não pela aparência:

| Sinal | Significado | Conduta |
|---|---|---|
| `msgs == 1` (só a sua) | o assistente nunca respondeu | **refaça a cena** |
| "Algo deu errado / Repetir" em PT | aviso transitório | **espere**, a imagem vem |
| "Something went wrong… help center" em EN, persistente | erro real | troque a referência |

```bash
echo "(()=>document.querySelectorAll('.bg-user-message').length)()" \
  | agent-browser --session $S eval --stdin
```

### Clicar em `Enviar prompt` não garante que enviou — confirme

O clique responde `✓ Done` mesmo quando o ref já expirou (digitar re-renderiza a
barra) e nada é enviado. Você só descobre 10 minutos depois, esperando uma imagem
que nunca foi pedida — e o usuário acaba tendo que clicar à mão.

Pegue o ref **no instante do clique** e confirme por **dois** sinais antes de
entrar no loop de espera:

```bash
S=$(agent-browser --session $S snapshot -i -c | grep -oP 'button "Enviar prompt" \[ref=\K[^\]]+' | head -1)
agent-browser --session $S click @$S
sleep 8
# 1) o campo do prompt zerou  2) a página diz que está gerando
echo "(()=>'prompt='+(document.querySelector('#prompt-textarea')?.innerText.length||0)+' | '+document.body.innerText.slice(-160).replace(/\s+/g,' '))()" \
  | agent-browser --session $S eval --stdin
```

Campo com o texto ainda lá = **não enviou**. Re-snapshot e clique de novo.

### Cloudflare que não passa NUNCA = você não está no browser logado

Antes de culpar o Cloudflare, confirme em que browser você está. O
`agent-browser` sobe um **Chromium empacotado próprio**, com perfil em
`/tmp/agent-browser-chrome-*` — sem login, sem cookie — e nesse browser o
"Confirme que é humano" **nunca** valida, por mais que você clique.

```bash
# em que perfil eu estou?
pgrep -af chromium | grep -oP 'user-data-dir=\K[^ ]+' | sort -u
# /tmp/agent-browser-chrome-...  -> ERRADO, descartável, sem login
# ~/.agent-profiles/gpt          -> certo
```

A correção é uma linha — **não** clicar no checkbox, **não** abrir aba nova:

```bash
agent-browser --session $S connect 9222     # ancora a sessão no browser logado
agent-browser --session $S get url          # confirme que respondeu
```

Sintoma que identifica o caso na hora: o usuário olha a tela e diz que **não tem
Cloudflare nenhum** enquanto o seu `snapshot` insiste que tem. São dois browsers
diferentes — o dele é o logado, o seu é o descartável. Custou uma sessão inteira
de cliques inúteis para descobrir isso; `connect 9222` resolveu em 2 segundos.

Vale também quando a aba da lane morre no meio (`No tab with label`): reconecte e
navegue direto para a URL da conversa, que o ChatGPT preserva o chat e as imagens
já geradas.

### Perdeu a aba, ou caiu no Cloudflare: escalone pro browser-harness

Duas falhas que **não** se resolvem insistindo no `agent-browser`:

- **A aba da lane morreu no meio.** `tab <lane>` responde `No tab with label`,
  `eval` retorna `about:blank`, `snapshot` diz `(no interactive elements)`. A
  lane perdeu o ponteiro, mas **as outras abas do Chromium continuam vivas e
  logadas**.
- **Cloudflare que não valida.** Ao reabrir, a aba nova pode cair no
  "Confirme que é humano" e o checkbox não passar nem em 3 cliques — enquanto
  outra aba do mesmo browser está logada e livre.

Antes de chamar o usuário, **veja o que mais existe no browser** — o
`agent-browser` só enxerga a aba dele:

```bash
curl -s http://127.0.0.1:9222/json/list | python3 -c "
import sys,json
for t in json.load(sys.stdin):
    if t.get('type')=='page': print(t['id'][:8],'|',t['url'][:60],'|',t['title'][:40])"
```

Achou aba viva em `chatgpt.com`? Trabalhe nela por CDP cru:

```bash
set -x BU_CDP_URL http://127.0.0.1:9222
browser-harness <<'PY'
ensure_real_tab()
print(page_info())
PY
```

Três pegadinhas do harness, todas custaram tentativa:

- `cdp()` recebe **kwargs, não dict**: `cdp("DOM.getDocument", depth=-1, pierce=True)`.
  Passar dict devolve `Message may have string 'sessionId' property`.
- `js()` **não aceita** `await_promise`. Para `fetch`/promise use
  `cdp("Runtime.evaluate", expression=..., awaitPromise=True, returnByValue=True)`.
- `shot()` não existe; screenshot é `cdp("Page.captureScreenshot", format="png")`
  e decodificar o base64.

Anexar por CDP (o `input[type=file]` certo é o **SEGUNDO** dos 4 — `:nth-of-type(2)`, id `_r_d_`):

```python
doc = cdp("DOM.getDocument", depth=-1, pierce=True)
# percorra children + shadowRoots atrás de INPUT com attribute type=file
cdp("DOM.setFileInputFiles", files=[REF], nodeId=nid)
```

**Coordenada de clique: CSS px ≠ px da viewport CDP.** Nessa janela a escala é
~1.22 — `getBoundingClientRect` deu y=672 e o botão real estava em y=844.
`Input.dispatchMouseEvent` na coordenada do rect **erra em silêncio**: o comando
retorna ok, o campo continua cheio, e você culpa o seletor. Tire um
`Page.captureScreenshot`, leia a posição real na imagem, clique nela. Sucesso =
`#prompt-textarea.innerText.length === 0`.

### Ao baixar, filtre pela proporção — o DOM tem imagens de outros chats

`naturalWidth > 800` sozinho pega miniaturas da barra lateral e imagens de
conversas antigas, e você acaba salvando foto aleatória no lugar da cena. Para
material 9:16, filtre também pela razão:

```js
[...new Set(Array.from(document.querySelectorAll('img'))
  .filter(i => i.naturalWidth > 800 && i.naturalHeight / i.naturalWidth > 1.6)
  .map(i => i.src))]
```

Confira sempre as dimensões do que baixou (`ffprobe`): se vier quadrada onde devia
ser 9:16, é imagem de outro chat.

**"Algo deu errado. Tente novamente." NÃO é falha — é só esperar.** O ChatGPT
mostra esse aviso com o botão `Repetir` enquanto ainda está gerando; a imagem
aparece depois, sozinha. Nunca clique em `Repetir`, não reenvie o prompt e não
abra chat novo — cada uma dessas coisas enfileira outra geração e embaralha qual
imagem é de qual cena.

Conte imagens, não leia o texto da página. O sinal de pronto é o número de `<img>`
com `naturalWidth > 400` subir:

```bash
bash -c "ALVO=<n_atual+1>; for i in \$(seq 1 120); do
  n=\$(echo '(()=>Array.from(document.querySelectorAll(\"img\")).filter(i=>i.naturalWidth>400).length)()' | agent-browser --session $S eval --stdin | tr -dc '0-9')
  [ \"\$n\" -ge \"\$ALVO\" ] && { echo READY; break; }
  sleep 5
done"
```

Só é falha de verdade se o contador não subir depois de ~10 min.

### 5. Baixar

Pegue os ids das imagens geradas:

```bash
cat <<'EOF' | agent-browser --session $S eval --stdin
Array.from(document.querySelectorAll('img')).map(i=>i.src)
  .filter((s,i,a)=>a.indexOf(s)===i)
  .map(s=>{const m=s.match(/id=(file_[a-z0-9]+)/);return m?m[1]:null}).filter(Boolean);
EOF
```

O primeiro id costuma ser a referência que você anexou — confira a ordem antes de baixar.

Depois baixe. **Prefixe o nome com a lane** — sem isso duas lanes se sobrescrevem em `~/Downloads`:

```bash
cat <<'EOF' | agent-browser --session $S eval --stdin
(async () => {
  const ids = ["file_XXX","file_YYY"];
  const srcs = Array.from(document.querySelectorAll('img')).map(i=>i.src);
  for (let k=0;k<ids.length;k++){
    const url = srcs.find(s=>s.includes(ids[k]));
    const r = await fetch(url); const b = await r.blob();
    const a = document.createElement('a');
    a.href = URL.createObjectURL(b); a.download = `<lane>-img-${k+1}.png`;
    document.body.appendChild(a); a.click(); a.remove();
  }
  return 'ok';
})()
EOF
sleep 3
~/.claude/bin/lane.sh collect <lane>                              # ~/Downloads/<lane>-* → ~/Downloads/PLAYWRIGHT/<lane>/
~/.claude/bin/lane.sh collect <lane> /caminho/do/projeto/assets   # e JÁ de cara pro destino final do projeto
```

**Collect é parte do download, não um passo depois — rode os dois `lane.sh collect` na mesma
chamada, logo após o `sleep 3` (regra da dona, 24/10/2026: "não pode ficar na Downloads, tem que
cair na pasta do projeto").** Sem o 2º `collect` (com o caminho do projeto), o arquivo fica preso em
`~/Downloads/PLAYWRIGHT/<lane>/` e vira exatamente o erro que mais acontece: imagem baixada mas
nunca entregue na pasta certa. **Nunca espere "aprovação" pra mover** — mova pro destino do
projeto assim que validar o arquivo (seção 6 logo abaixo); se depois for reprovada, apaga de lá
mesmo. `ls ~/Downloads/*.png ~/Downloads/*.webp 2>/dev/null` antes de dar a tarefa por pronta — se
aparecer algo, é um `collect` que faltou.

**Pediram webp?** `cwebp` **não está instalado** nesta máquina — use o ffmpeg,
que está. Entregue os dois arquivos, o PNG é o master:

```bash
ffmpeg -y -loglevel error -i saida.png -c:v libwebp -quality 90 saida.webp
```

Medido: 941×1672, 2.0 MB de PNG → 198 KB de webp.

### 6. VALIDE O ARQUIVO SALVO — o download mente de três jeitos

Baixar não é ter. Cada uma destas falhas já entregou arquivo que *parecia* certo:

| Falha | Como o arquivo aparece | Como pega |
|---|---|---|
| **miniatura** do DOM | 416×681 em vez de 941×1672 | dimensão via `ffprobe` |
| imagem de **outro chat** (aba roubada) | dimensão correta, conteúdo alheio | abrir e olhar / 1ª msg do chat |
| **envio que falhou** | arquivo antigo permanece no lugar | data de modificação |

Rode sempre os três, logo depois de salvar:

```bash
# 1) dimensão exata do lote — qualquer coisa diferente é lixo
for f in <lane>-*.png; do
  d=$(ffprobe -v error -show_entries stream=width,height -of csv=p=0 "$f")
  [ "$d" = "941,1672" ] || echo "REPROVA $f = $d"
done
# 2) tamanho fora da média dos irmãos denuncia miniatura
ls -la <lane>-*.png | awk '{print $NF, $5}'
# 3) reconcilie pedido × disco: o lote não para quando um envio falha
for n in $LISTA; do [ -f "<lane>-$n.png" ] || echo "FALTA $n"; done
```

Um arquivo de **455 KB** no meio de arquivos de 2 MB é miniatura — foi exatamente
assim que uma imagem de 416×681 entrou numa leva e quase virou vídeo.

### 7. Congele a imagem aprovada e distribua por HASH

Depois do QA, a imagem aprovada vira **fonte da verdade**. O erro que fecha o ciclo:
a imagem foi reprovada, regerada e salva na pasta de origem — mas as cópias já
distribuídas para as cenas continuaram sendo a **versão velha**. Cinco cenas foram
gerar vídeo a partir da imagem descartada; ninguém notou porque o caminho do arquivo
estava certo.

**Caminho certo não prova conteúdo certo.** Toda vez que uma imagem for regerada,
redistribua e compare hash:

```bash
md5sum _IMG/numes-51-base.png CRIATIVO-51/IMG/cena-1.png   # têm que bater
```

E antes de consumir a imagem em qualquer etapa seguinte, valide que ela é
byte-idêntica a alguma imagem aprovada **daquele mesmo criativo** — ver
`scripts/valida_img.sh` na skill `video-hub`.

## Páginas de ENTREGÁVEL (produto/bônus/OB) = WORK MODE, não chat
A regra "uma cena por mensagem" abaixo vale pro CHAT (criativo/cena). Páginas de entregável low
ticket vão no **Work mode**: lote inteiro do item num pedido (até ~90 imagens), com a nossa página de
referência + capa anexadas, contexto e texto página a página. Receita:
`~/.claude/browser-workspace/domain-skills/chatgpt.com/work-mode-lote-entrega.md`. Ordem e ciclo de
panes em `criacao-low-ticket-mvt/references/CONSTRUCAO.md` passo 2(f).

### Página com carta real (tarô/cigano): SLOT VAZIO + scan colado (05/10/2026)
O GPT redesenha a carta mesmo com o scan anexado (o Sol saiu desenhado na capa da Intuitiva do Cigano). Jeito que funciona:
1. Prompt pede a página com um **quadro vazio no tamanho da carta** (moldura, sem nada dentro): `leave the card frame EMPTY, plain paper inside, no illustration`.
2. Cola o **scan real** no quadro por script (Pillow), recortado SEM fundo branco, com borda fina e sombra leve. Retângulo branco por cima da arte = colagem malfeita: refazer.
3. Auditoria: contact sheet de todas as páginas. Toda carta que aparece (inclusive nas mãos de alguém, numa mesa, na rotina) tem que ser scan real ou mostrar só o verso. Frente inventada = refazer a página (c-003 e c-009 do Cigano).

### Prompt-modelo OBRIGATÓRIO do lote de entregável (Work mode)
Copiar e preencher. Nunca mandar lote sem estas linhas (cada uma cobre um erro que já aconteceu):
```
Gere {N} IMAGENS INDIVIDUAIS — uma imagem separada por página, cada uma um arquivo de imagem
próprio, usando o GERADOR DE IMAGENS. NÃO junte páginas numa imagem, NÃO faça grid/colagem,
NÃO renderize com HTML/SVG/Python/código, NÃO gere PDF.
As imagens anexas são a REFERÊNCIA DE ESTILO: copie exatamente moldura, fundo, fonte, caixas e
setas; troque só a ilustração e o texto. NÃO devolva a referência. NÃO reproduza a página anexa.
Ilustração = {ex.: gravura Rider-Waite clássica completa e colorida da carta} — nunca ícone,
silhueta ou placeholder.
Tokens: fundo {hex}, tinta {hex}, ornamento {hex}; cabeçalho "{nome exato do produto}".
Orientação: {paisagem/retrato por tipo de página}.
Imagem 1 = {página} — texto: ...
Imagem 2 = {página} — texto: ...
```
Checklist antes de aceitar o lote:
1. **Teste com 2 páginas primeiro**; lote só se as 2 saírem no nível da referência.
2. **Desenhou por código** (formas chapadas, placeholder, fonte de sistema) → reprovar, repetir
   a 1ª linha; se insistir, modo Chat (uma página por mensagem).
3. **Devolveu a referência** (re-encodada, md5 diferente): comparar cada download contra as
   refs e contra o lote — hash exato + olhar; bateu → apagar e regerar (6 casos em 27/09).
4. **Grid / várias páginas numa imagem** → reprovar.
5. **Nome do produto trocado no cabeçalho** (ex.: "Tarô" × "Tarot") → padronizar com as páginas já publicadas.
6. Fim: md5sum sem duplicatas + contact sheet (`montage`) olhando página por página.
7. **Página com ILUSTRAÇÃO fiel (gravura Rider-Waite, retrato, produto real) → MODO CHAT, não Work.**
   27/09: o Work mode entregou 36 páginas do principal do Mapa do Tarot com carta em ícone
   simplificado, mesmo com o prompt-modelo. Chat (uma página por mensagem + referência do mesmo
   tipo) entregou as 31 dos Menores certas no mesmo dia. Work mode só serve pra página de texto/
   diagrama sem ilustração fiel — e ainda assim testar 2 antes.
8. **Cota esgotada:** bloqueio de imagem NÃO é cota até descartar com prova (dono 28/09): (a) rate limit por pedido rápido demais ("too many requests" ≠ cota — esperar 2-3 min, 1 pedido por vez); (b) aba fechada/errada; (c) modo errado — conferir seletor em Chat no chat novo; (d) perfil antigo sem login (`gpt` 9222, `gpt-play-1`) em vez de `gpt-conta*`. Se os 4 checks passarem e aparecer o card nativo "Você atingiu o limite de imagens… Tente de novo à(s) HH:MM", é cota real do Plus e vale em Chat E Work (provado 28/09 com prints, Mapas Elétricos). Os perfis `gpt-conta*` são a MESMA conta (Dona) e outros panes (ex.: tarot) gastam a mesma cota: aí é esperar o horário e retomar sozinho.

## Regras de prompt

- **Sempre em inglês.**
- **UMA cena por mensagem, chat novo a cada imagem.** Pedir N cenas numa mensagem faz o modelo devolver **uma imagem contendo as N** — ver a seção "Lote SEMPRE volta grid" abaixo. Nenhuma redação testada mudou isso.
- **Formato:** diga explicitamente. `vertical 9:16 story format`, `square 1:1`, `horizontal 16:9`.
- **Sem texto:** `no text, no captions, no watermark, no UI overlay` — o modelo erra letras.
- **Feche a lista de objetos:** `only these objects: X, Y, Z — nothing else`. Objeto ambíguo vira lixo na cena.
- **Realismo:** `grounded documentary realism, real ordinary objects, natural imperfections, no surreal elements, no decorative clutter`
- **Look UGC:** `amateur phone footage look, slight grain, no studio lighting`

### Regerar cena de personagem que já existe: SEMPRE anexar a referência

Se o criativo já tem uma cena aprovada com aquela pessoa, **nunca redescreva a
persona por texto** para gerar outra cena dela. Anexe uma imagem aprovada e peça a
MESMA pessoa; mude só a pose e o enquadramento.

```
Using the attached photo as the reference: generate ONE single standalone photograph
of the SAME woman — same face, same bone structure, same age, same hair, same shirt,
same wall, same light. Change only the pose: <nova pose>.
```

Descrição textual, por mais detalhada que seja, sorteia outra pessoa. Aconteceu numa
leva real: a cena 1 precisou ser refeita, foi descrita do zero com idade, cabelo,
roupa e ambiente idênticos, e voltou com outra mulher — enquanto as cenas 2, 3 e 4
seguiam com a original. Um criativo com duas atrizes não sobe.

Vale para qualquer regeração: correção de defeito, troca de pose, mudança de
enquadramento. **Existe cena aprovada com a persona? Anexa.**

E peça **UMA imagem**, explicitamente: `ONE single frame only. Not a grid, not a
collage, not a contact sheet, not multiple panels` mais `no grid, no collage, no
split screen, no multiple images, no repeated person, no duplicate figure` no
negativo — o modelo entrega colagem de 4 poses com facilidade, e a colagem passa
pelo teste de dimensão (fica 9:16 certinho), então só se pega **abrindo a imagem**.

### A cena tem que fazer sentido na vida real

Antes de escrever o prompt: **uma pessoa de verdade faria isso, nesse lugar, desse
jeito?** Se não, o defeito é do roteiro, não do modelo — e vai reaparecer por mais
que você reforce o prompt.

- **Todo objeto precisa de apoio físico:** na mão fechada, sobre a mesa, no bolso.
  Objeto "apoiado" onde não se apoia (celular em cima do volante, xícara no braço do
  sofá) o modelo não sabe onde fixar — na imagem sai torto, e se virar vídeo desgruda
  e flutua.
- **A ação tem que ser possível ali:** dirigindo não se lê tela; cozinhando não se
  segura telefone com as duas mãos.
- **Objeto que não precisa estar em cena, tire.** Cada objeto a mais é uma chance de
  invenção. Remover é mais barato que domar.
- **Roupa, luz e hora coerentes com o ambiente e com o que se fala.**

### Telas e superfícies com conteúdo

Se a cena tem celular, laptop, tablet, papel escrito, cartaz ou placa, **descreva o
conteúdo explicitamente**. Sem isso o modelo entrega tela preta, aparelho virado de
costas, ou texto em inglês por padrão — os três já quebraram criativo em produção.

Escreva sempre os quatro itens: **ligada, o que aparece, em que idioma, com que
aparência.**

```
the phone screen is ON and clearly visible, displaying a reading app in Portuguese:
a short title line, a date line, and three or four paragraphs of body text in
Brazilian Portuguese, dark background with warm off-white text, calm editorial
layout, no app chrome, no message bubbles, no chat interface, no green color,
no English text, text slightly soft so individual words are not sharply readable
```

`text slightly soft` é deliberado: dá conteúdo plausível sem exibir texto inventado
nítido. Texto legível na tela de um produto real é mockup falso — pode prometer o
que a oferta não promete.

**Proíba a traseira explicitamente.** Pedir "tela ligada" não basta: o modelo
satisfaz a instrução **virando o aparelho de costas** — aí não há tela acesa para
contradizer o prompt. Num criativo cujo mecanismo é a tela, isso entrega uma cena
vazia. Aconteceu quatro vezes seguidas no mesmo criativo até a proibição entrar:

```
the phone is face UP with the screen visible and ON, the back of the phone is never
shown, no camera module visible, the hand holds the phone from the side or below
without covering the screen
```

E no NEGATIVE: `phone face down, back of phone, camera module, hand covering the screen`.

Regra geral que isso ilustra: **quando o modelo insiste num desvio, proíba o desvio
pelo nome** em vez de reforçar o pedido original.

**Nunca:** tela preta, aparelho de costas, texto em inglês num criativo PT-BR, balão
de mensagem, layout de chat, qualquer tom esverdeado (lê como WhatsApp).

Isso é exceção à regra `no text` acima: ali o texto proibido é legenda/marca d'água
sobre a imagem. Conteúdo DENTRO de uma tela em cena é obrigatório quando a tela
aparece.

## Conferir os controles ANTES de cada envio

Vale para qualquer painel de geração (ChatGPT, Hub, etc): **trocar de modelo reseta
os controles** — proporção, duração e o anexo voltam ao padrão do motor novo, sem
aviso. Um "tentar com outro motor" depois de falha faz isso silenciosamente.

Antes de todo envio, confirme por `eval` (não por screenshot, que engana):

- **modelo** é o que você escolheu, não `Auto`
- **proporção** é a do formato pedido — 9:16 para story, nunca o 16:9 padrão
- **duração** é a planejada
- **imagem de referência** continua anexada — anexo perdido vira texto→imagem e
  entrega outra pessoa
- **tamanho do prompt** dentro do limite do motor

Enviar sem conferir gasta cota e devolve material inútil. Foi assim que uma leva
inteira saiu em 16:9 e 5s quando o pedido era 9:16 e 10s.

## QA das imagens — gate antes de virar vídeo

Vídeo custa cota e é o recurso escasso. Imagem errada que vira vídeo custa duas
vezes: a geração perdida e a regeração. Rode este gate em TODAS as imagens antes de
liberar qualquer clipe.

**Rode a checagem de hash DEPOIS DE CADA DOWNLOAD, não só no fim do lote.** Baixar
a mesma imagem duas vezes com nomes de cenas diferentes é o defeito mais frequente
deste fluxo — em uma única leva aconteceu em três criativos distintos (um com três
arquivos iguais). O DOM não garante que a imagem nova é a última: se o download
pegar o `src` errado, você leva a anterior de novo e não percebe.

```bash
# 1. imagem duplicada — o mesmo PNG salvo com nomes de cenas diferentes
md5sum IMG/*.png | sort | uniq -w32 -D        # qualquer saída = defeito

# 2. contact sheet pra olhar tudo de uma vez
montage IMG/cena-*.png -tile 4x1 -geometry 220x391+4+4 -background '#111' sheet.jpg
```

**Tela em cena não se valida pelo contact sheet.** Reduzida, toda tela parece
"levemente suave"; no arquivo original o texto costuma estar nítido e quotável.
Crope a área da tela em full-res e olhe:

```bash
magick IMG/cena-N.png -crop 45%x18%+180+330 +repage -resize 800x /tmp/tela.jpg
```

Se der pra ler título, data ou uma frase inteira, **reprove** — mesmo que na
miniatura parecesse borrado.

Depois **abra o sheet** e confira, imagem por imagem:

- **Persona e ambiente** batem com o roteiro daquela cena? Imagem de outro criativo
  vaza com facilidade quando há mais de uma aba aberta.
- **É a mesma pessoa** em todas as cenas do mesmo criativo? Roupa, cabelo e idade
  iguais?
- **Toda tela em cena está ligada, com conteúdo, no idioma certo?**
- Tem texto queimado, marca d'água ou objeto proibido pela marca?
- A imagem serve como **primeiro frame** do vídeo que ela vai gerar? Rosto em
  repouso, exposição correta, objeto na posição em que a ação começa?

Contar arquivos não é QA. Hash e olho, sempre.

### Pessoas

- **Nacionalidade específica.** "Latin American" cai no padrão mexicano/andino. Use `Argentine from Buenos Aires, of Italian and Spanish descent, European-Mediterranean features`, `Mexican, mestiza features`, `Caribbean Colombian`, e no Brasil especifique a região.
- **Rosto natural, exposição correta:** `natural evenly exposed face, no blown-out highlights, no overexposure, visible pores and fine lines, natural skin texture`
- **Sem acabamento de banco de imagem:** `no beauty retouching, no skin smoothing, no plastic skin, no airbrushing, no stock photo look`
- **Expressão em repouso** se a imagem vai virar vídeo: `relaxed neutral expression, mouth closed, no exaggerated expression, no forced pose, candid unposed`. Emoção exagerada na imagem vira careta ao animar.
- **Mesma pessoa em várias imagens:** anexe um frame real e escreva `the SAME person as in the attached reference photo — same face, same bone structure, same age`. Não redescreva do zero — sai outra pessoa.
- **Proíba o que pode vazar da referência.** Se a referência tem vela e cristal e a cena nova é uma cozinha: `absolutely no candles, no crystals, no mystical objects`.

## Erros comuns

| Sintoma | Correção |
|---|---|
| Veio um grid em vez de imagens separadas | Pediu mais de uma cena na mesma mensagem. UMA cena por mensagem, chat novo — proibição de layout não resolve |
| Voltaram variações da cena anterior | Chat reusado ancora no assunto do turno anterior — abra chat novo |
| Envio falhou no meio do lote e ninguém viu | Reconcilie pedido × disco no fim (`[ -f ... ] || echo FALTA`) |
| Baixou imagem de outro projeto | Aba roubada por outra lane — verifique dono do chat antes de baixar |
| Pessoa diferente entre imagens | Anexe referência + "same face, same bone structure" |
| Etnia errada | Especifique país e ascendência, não continente |
| Rosto estourado | `no blown-out highlights, no overexposure` |
| Cena poluída de objeto | Feche a lista: `only these objects: … nothing else` |
| Pede login | Peça ao usuário para logar na janela do perfil `gpt` |
| Prompt caiu no chat de outro Claude | Você não fixou a aba. `lane.sh take gpt <lane>` de novo antes do bloco |
| Imagem sumiu / veio a de outra tarefa | Download sem prefixo de lane sobrescreveu em `~/Downloads`. Use `<lane>-img-N.png` |

Para gerar vídeo a partir das imagens, ver skill `grok-video-hub-playwright`. Para o pipeline completo de criativo de anúncio, ver `video-hub`.

---

# Mecânica migrada do antigo `video-hub` (2026-08-23)

Estas seções vieram do monolito `video-hub` ao ser dividido em
`criativo-ads-video-orq` (orquestrador) + `gpt-imagem-playwright` (esta) +
`hub-video-playwright`. **Esta skill é a fonte única da mecânica do ChatGPT** —
se um seletor mudar, corrija aqui, nunca no orquestrador.

### O pedido do lote tem que ser cirúrgico — senão volta grid

Dizer "imagens separadas, uma por cena" **não basta**. Numa leva real, um pedido de
4 cenas com essa frase devolveu: duas variações da cena 1, um **grid 2×2 com as
quatro cenas coladas**, e só uma cena solta correta. O grid sai em 9:16, então passa
por qualquer checagem de dimensão — só abrindo o arquivo se descobre.

Abra o pedido **exatamente assim**, antes de qualquer descrição de cena:

```
Generate N images and return them as N SEPARATE image attachments — one attachment
per scene, N files in total.

Do NOT merge them into one picture. No grid, no 2x2, no collage, no contact sheet,
no mosaic, no side-by-side, no before/after, no panel layout, no single image
containing more than one scene. Each scene is its own standalone photograph, each
one full-bleed vertical 9:16, each one filling its entire frame edge to edge with
a single scene.

Do not generate variations or alternate takes of any scene. Exactly one image per
scene, N images, no more and no fewer.

===== IMAGE 1 =====
<descrição da cena 1>

===== IMAGE 2 =====
<descrição da cena 2>
...
```

As três travas que fazem esse texto funcionar, e por que cada uma existe:

- **"N SEPARATE image attachments … N files in total"** — o modelo entende "anexo",
  não "imagem separada"; sem contar os arquivos ele entrega um só.
- **A lista fechada de layouts proibidos** (grid, 2x2, collage, contact sheet,
  mosaic, side-by-side, panel) — proibir só "grid" deixa "collage" liberado.
- **"full-bleed … filling its entire frame edge to edge with a single scene"** — é
  o que impede o modelo de "resolver" o 9:16 empilhando cenas dentro do quadro.
- **"Do not generate variations or alternate takes"** — sem isso ele gasta o lote
  entregando duas versões da mesma cena e nenhuma das outras.

Confira **contando os arquivos e abrindo cada um**. Contar não basta: no caso acima
o total batia e um dos arquivos era o grid.

### Declare o STYLE UMA vez para o lote inteiro — repetir por cena mata o lote

Segundo defeito da mesma leva, e o mais caro: um pedido de **10 cenas** voltou com
**duas variações da cena 1 e mais nada**. As outras nove foram simplesmente
ignoradas, sem erro e sem aviso.

Causa: o bloco `STYLE` (~900 chars) estava colado dentro de cada uma das 10
descrições. Prompt final: **18 mil caracteres**, 9 mil deles pura repetição. Acima
de uns poucos milhares de caracteres o modelo atende só a primeira cena.

Estrutura certa — o compartilhado sai do laço:

```
<abertura com a contagem e a lista de layouts proibidos>

STYLE — apply this identically to all N images: <bloco de estilo, UMA vez>

IMAGE 1 — <personagem, ambiente, enquadramento, objetos fechados, luz>
IMAGE 2 — <idem, compacto>
...
```

Cada cena vira ~350 chars em vez de ~1800, e o pedido de 9 cenas fecha em **~6k
chars** em vez de 18k. Acrescente também **"Render ALL NINE scenes, not just the
first one"** — barato e ataca exatamente o modo de falha.

Régua: se o pedido do lote passa de **~8k caracteres**, tem repetição para tirar.
Fatie em dois lotes antes de aceitar um prompt gigante.

### CONCLUSÃO: UMA cena por mensagem. Lote de cenas SEMPRE volta grid.

Testado quatro vezes na mesma leva, com a redação ficando mais explícita a cada
tentativa. O resultado não melhorou:

| Pedido | Voltou |
|---|---|
| 4 cenas | grid 2×2 + 2 variações da cena 1 + 1 cena solta |
| 10 cenas | 2 variações da cena 1, mais nada |
| 9 cenas | grid 3×3 com as nove + 3 variações da cena anterior |
| 3 cenas, chat novo, cada layout proibido pelo nome | **grid 3×1** |
| **1 cena** | **1 imagem standalone, 941×1672** ✓ |

Pedir N cenas numa mensagem faz o modelo entregar **uma imagem contendo as N**.
Nenhuma redação testada mudou isso — proibir "grid, 2x2, collage, contact sheet,
mosaic, side-by-side, panel", exigir "N separate image attachments, N files in
total", exigir "full-bleed, one scene filling the entire frame": tudo ignorado.

Detalhe que engana: **as cenas dentro do grid saem individualmente perfeitas** —
personagem, luz, objetos, tudo conforme descrito. Dá a sensação de que faltou pouco.
Não faltou: num grid 3×1 cada cena fica com ~941×557 e não serve de primeiro frame
de vídeo. Recortar não salva.

**Portanto: uma cena por mensagem, sempre.** É mais lento e é o único que funciona.
Automatize em vez de negociar com o modelo:

```bash
for n in 31 32 33 34 35; do ./one.sh prompt-$n.txt cena-$n; done
```

Cada rodada: chat novo → colar o prompt de UMA cena → esperar 1 imagem → baixar →
conferir `941x1672` no `ffprobe`.

### Por que chat novo a cada imagem

Medido na mesma leva, com o prompt já enxuto e com todas as proibições de layout:

| Pedido | Voltou |
|---|---|
| 4 cenas | 2 variações da cena 1, **1 grid 2×2**, 1 cena solta correta |
| 10 cenas | 2 variações da cena 1, mais nada |
| 9 cenas | 3 variações da cena 1 do turno anterior, **1 grid 3×3** com as nove |

Dois comportamentos, os dois independentes da redação:

- **Teto de ~3-4 imagens por turno.** Pedir mais não aumenta a entrega: o modelo
  desiste das cenas extras ou as empilha num grid. Peça **no máximo 3-4 por vez** e
  feche o lote antes do próximo.
- **A conversa ancora na última cena.** Num chat que já gerou imagens, o turno
  seguinte volta cheio de **variações do assunto anterior** em vez das cenas novas.
  Por isso: **um chat novo (`https://chatgpt.com/`) por lote.** Não é higiene, é o
  que faz o lote seguinte obedecer.

Sinal de que o grid está vindo: as cenas descritas aparecem todas **corretas** lá
dentro. A descrição não é o problema — o formato de entrega é. Não reescreva as
cenas; refaça o pedido em chat novo, com 3.

**Lote só para cenas independentes.** Cena 2 de um hook nunca entra no lote junto
com a cena 1 dele — ela é gerada depois, com a cena 1 aprovada anexada como
referência (ver adiante). Lote é para cenas de criativos diferentes, que não
precisam de consistência entre si.

**Consistência de personagem:** anexe um frame real da pessoa e peça "same woman, same face, same age". Não descreva a pessoa do zero em cada cena — sai outra pessoa. Para extrair frames de um vídeo existente:

```bash
ffmpeg -ss <seg> -i vencedor.mp4 -frames:v 1 REFERENCIA/persona-01.png
```
### O botão de enviar do ChatGPT também é ícone — e o campo NÃO se limpa sozinho

Mesmo defeito do Hub, e ele aparece nas duas pontas do fluxo (com e sem anexo):
`agent-browser click @ref` no botão de enviar responde `✓ Done` e **não envia**. O
prompt fica no campo, o loop espera uma geração que nunca foi pedida e estoura em
timeout — que se parece muito com bloqueio de Cloudflare ou cota esgotada.

Envie sempre pelo `data-testid` com a sequência completa de eventos:

```bash
cat <<'EOF' | agent-browser --session $G eval --stdin
(()=>{const el=document.querySelector('[data-testid="send-button"]');
if(!el||el.disabled) return 'sem botao';
const r=el.getBoundingClientRect(); const o={bubbles:true,cancelable:true,view:window,clientX:r.left+r.width/2,clientY:r.top+r.height/2,pointerId:1,isPrimary:true,button:0};
['pointerover','mouseover','pointermove'].forEach(t=>el.dispatchEvent(new (t.startsWith('pointer')?PointerEvent:MouseEvent)(t,o)));
el.dispatchEvent(new PointerEvent('pointerdown',o)); el.dispatchEvent(new MouseEvent('mousedown',o));
el.dispatchEvent(new PointerEvent('pointerup',o)); el.dispatchEvent(new MouseEvent('mouseup',o));
el.dispatchEvent(new MouseEvent('click',o)); return 'clicou';})()
EOF
```

**E limpe o campo antes de digitar.** `keyboard inserttext` **acrescenta** ao que já
está lá. Com o envio falhando em silêncio, cada nova tentativa empilha outro prompt:
num caso real o campo chegou a **6.523 caracteres** — mais de quatro prompts colados.
Se um desses tivesse sido enviado, teria gerado uma imagem sem sentido.

```bash
echo "(()=>{const t=document.querySelector('#prompt-textarea'); t.innerHTML=''; t.dispatchEvent(new Event('input',{bubbles:true})); t.focus(); return 1;})()" | agent-browser --session $G eval --stdin
```

### A ABA PODE SER ROUBADA NO MEIO — confirme que a conversa é SUA antes de baixar

O defeito mais caro do ChatGPT, e o mais difícil de perceber: **outro Claude no mesmo
browser abre uma aba e rouba o ponteiro da sua sessão**. Seus comandos passam a cair
no chat dele. Você envia seu prompt para o vazio e baixa **a imagem que ele gerou**.

Como aparece na prática: pedi a personagem de uma VSL (senhora à mesa de tarô) e
baixei, em duas tentativas seguidas, um copo com moedas e depois um celular marcando
11:11 — imagens de outro projeto. Nada no script deu erro. O arquivo tinha 941×1672,
o log dizia `OK`.

**Fixar a lane não basta.** `lane.sh take` corrige o ponteiro no instante em que roda,
mas a outra lane pode abrir aba um segundo depois. Aconteceu mesmo com lane nova e
exclusiva.

A única defesa é **verificação de dono**, em duas etapas:

```bash
# 1) ANTES de enviar: a aba tem que estar num chat VAZIO
m=$(echo "(()=>document.querySelectorAll('.bg-user-message').length)()" \
  | agent-browser --session $G eval --stdin | tr -dc '0-9')
[ "$m" = "0" ] || { echo "aba tomada por outra lane (msgs=$m)"; }   # descarte e refaça

# 2) DEPOIS de enviar: a primeira mensagem tem que ser O SEU PROMPT
SIG=$(head -c 40 prompt.txt | tr -d '\n')
cat <<EOF | agent-browser --session $G eval --stdin
(()=>{const m=document.querySelectorAll('.bg-user-message');
 if(!m.length) return 'vazio';
 return (m[0].innerText||'').indexOf("$SIG")===0 ? 'MINHA':'ALHEIA';})()
EOF
```

`ALHEIA` = **não baixe nada**, refixe a lane e recomece aquela imagem. Envolva em
2-3 tentativas.

É o mesmo princípio da validação por conteúdo do Hub (frame 0 × imagem de origem):
**em ferramenta de conta compartilhada, nunca confie em posição — confirme por
conteúdo.** No Hub essa trava pegou oito clipes trocados; no ChatGPT a ausência dela
deixou duas imagens erradas passarem.

### Um perfil por conta é regra — não tente clonar para isolar

A saída intuitiva ("cada Claude num perfil próprio com o mesmo login") **não
funciona**: o login pertence ao perfil, e duplicar o diretório derruba a sessão e
traz o Cloudflare de volta. Está em `~/.claude/bin/LANES.md`. O isolamento possível
é por **lane** (aba + ponteiro + staging de download), e ele é frágil por natureza.

Duas regras que reduzem a colisão:

- **Nome de lane por TAREFA, nunca por projeto.** Reusar a lane de ontem
  (`mestre20`) numa tarefa nova é convite a colisão. VSL nova = lane nova
  (`martavsl`).
- **Refixe a lane antes de CADA geração**, não uma vez por lote. `lane.sh take` é
  idempotente e barato; vinte gerações seguidas sem refixar é onde o ponteiro salta.

E quando souber que outro Claude está usando o mesmo browser, **peça para o usuário
pausá-lo**. Cada colisão custa uma tentativa e alguns minutos; não dá para resolver
sozinho do lado de cá.

### Detecte o composer por `eval`, não por snapshot — e saiba que sem login ele não existe

`grep 'textbox ...'` no snapshot falha de forma intermitente com a página ainda
carregando. Espere pelo elemento real:

```bash
for k in $(seq 1 8); do
  v=$(echo "(()=>document.querySelector('#prompt-textarea')?1:0)()" | agent-browser --session $G eval --stdin | tr -dc '01')
  [ "$v" = "1" ] && break; sleep 6
done
```

Se ele nunca aparecer, **a sessão provavelmente caiu** — deslogado o ChatGPT não
renderiza o composer, e isso se disfarça de "página lenta". Cheque o login antes de
aumentar timeout.

### Geração que não responde: é engasgo, não cota

Sintoma: mensagem enviada (campo zerou, a conversa existe), `busy=0`, **nenhuma
imagem** e **nenhuma resposta do assistente** — a conversa fica só com a sua
mensagem. Não há aviso de limite.

Isso é travamento pontual do ChatGPT. Confirme contando as mensagens:

```bash
echo "(()=>document.querySelectorAll('.bg-user-message').length)()" | agent-browser --session $G eval --stdin
```

`1` = só a sua, o assistente nunca respondeu. **Refaça aquela cena**; não conclua que
a cota acabou. Numa leva real uma cena travou assim e as duas seguintes saíram
normalmente — espaçar as gerações teria sido perda de tempo.
### Operação

```bash
agent-browser --session $G upload "input[type=file]" /caminho/REFERENCIA/persona-01.png
agent-browser --session $G snapshot -i -c          # achar o ref do textbox
agent-browser --session $G focus @eN
agent-browser --session $G keyboard inserttext "$(cat prompt.txt)"
agent-browser --session $G click @eENVIAR
```

Use `keyboard inserttext` com heredoc em arquivo — `fill` quebra com prompt longo e caractere especial.

Esperar terminar:

```bash
bash -c 'for i in $(seq 1 120); do if ! agent-browser --session $G snapshot -i -c 2>/dev/null | grep -q "Parar de responder"; then echo DONE; break; fi; sleep 5; done'
```

### Confirme que a geração COMEÇOU — clicar em `Enviar prompt` não basta

O clique responde `✓ Done` mesmo com o ref expirado (digitar no campo re-renderiza
a barra) e nada é enviado. O sintoma é cruel: você entra no loop de espera e
descobre 10 minutos depois que nunca pediu nada — ou o usuário clica à mão por você.

Pegue o ref no instante do clique e valide **dois** sinais antes de esperar:

```bash
S=$(agent-browser --session $G snapshot -i -c | grep -oP 'button "Enviar prompt" \[ref=\K[^\]]+' | head -1)
agent-browser --session $G click @$S
sleep 8
echo "(()=>'prompt='+(document.querySelector('#prompt-textarea')?.innerText.length||0)+' | '+document.body.innerText.slice(-160).replace(/\s+/g,' '))()" \
  | agent-browser --session $G eval --stdin
```

Campo do prompt zerado **e** a página dizendo "Gerando uma imagem…" = enviou.
Texto ainda no campo = não enviou; re-snapshot e clique de novo.

### VALIDE A DIMENSÃO DO ARQUIVO BAIXADO — o filtro sozinho deixa passar miniatura

O filtro no `querySelectorAll` é a primeira barreira, não a última. Num lote real
uma imagem baixou com **416×681** — uma miniatura — porque o script de então usava
`naturalWidth > 400` e a razão 1,63 passou no teste de proporção. O log disse
`baixou`, o arquivo existia, e o defeito só apareceu horas depois, na hora de
distribuir as imagens pelas cenas.

Dois sinais que pegam isso em um segundo:

```bash
# 1) dimensão: tudo que não for a resolução do lote é lixo
for f in numes-*.png; do
  d=$(ffprobe -v error -show_entries stream=width,height -of csv=p=0 "$f")
  [ "$d" = "941,1672" ] || echo "  $f = $d   <-- REPROVA"
done
# 2) tamanho: um arquivo muito menor que os irmãos é miniatura ou erro
ls -la numes-*.png | awk '{print $NF, $5}'
```

Na leva onde isso aconteceu, o arquivo ruim tinha **455 KB** contra ~2 MB dos
outros — a mesma assinatura de um clipe de vídeo defeituoso que tinha 2,3 MB entre
irmãos de 4,7 MB. **Discrepância de tamanho entre irmãos é o detector mais barato
que existe**; rode-o em imagem e em vídeo.

### Falha de envio no meio do lote NÃO para o lote — reconcilie no fim

Num lote de 9 imagens, uma falhou com `FAIL: nao enviou (campo=1567)` — resíduo de
prompt no composer impediu o envio. O loop registrou a falha, **seguiu para a
próxima** e terminou reportando sucesso geral. A imagem faltante só apareceu quando
as cenas foram distribuídas e quatro ficaram sem arquivo.

Feche todo lote com uma reconciliação explícita entre o que foi pedido e o que
existe em disco:

```bash
for n in $LISTA; do [ -f "$DIR/numes-$n.png" ] || echo "FALTA $n"; done
```

E, antes de gerar qualquer vídeo, confirme a **cobertura cena a cena** — não a
contagem total:

```bash
for n in 51 52 53 54 55 56; do for i in $(seq 1 6); do
  [ -f "CRIATIVO-$n/IMG/cena-$i.png" ] || echo "FALTA $n/cena-$i"
done; done
```

Contar arquivos na pasta de origem não prova que cada cena recebeu o seu: numa leva
real o total batia e um criativo inteiro estava com 4 cenas descobertas, porque a
distribuição rodou antes de uma imagem existir.
### Baixe filtrando pela proporção, não só pelo tamanho

`naturalWidth > 800` pega miniatura de barra lateral e imagem de conversa antiga —
já aconteceu de baixar 4 fotos aleatórias de outro chat achando que eram as cenas.
Para 9:16, filtre também pela razão e confira com `ffprobe`:

```js
[...new Set(Array.from(document.querySelectorAll('img'))
  .filter(i => i.naturalWidth > 800 && i.naturalHeight / i.naturalWidth > 1.6)
  .map(i => i.src))]
```

Imagem quadrada onde devia ser 9:16 = veio de outro chat, descarte.

Lotes grandes falham mais: **peça 4 a 6 imagens por vez**, não 10, e espere cada
lote terminar antes do próximo.

### "Algo deu errado. Tente novamente." NÃO é falha — espere

O ChatGPT mostra esse aviso com o botão `Repetir` **enquanto ainda está gerando a
imagem**. A imagem aparece depois, sozinha, sem você clicar em nada. Tratar isso
como erro é o caminho para desperdiçar meia hora reenviando prompt e concluir
errado que a cota de imagens acabou.

Portanto:

- **Não clique em `Repetir`** ao ver a mensagem. Clicar enfileira uma segunda
  geração e embaralha qual imagem é de qual cena.
- **Não reenvie o prompt.** Não abra chat novo. Não troque de modelo.
- **Espere e continue contando imagens**, não lendo o texto da página. O sinal de
  pronto é o número de `<img>` com `naturalWidth > 400` subir:

```bash
bash -c 'ALVO=<n_atual+1>; for i in $(seq 1 120); do n=$(echo "(()=>Array.from(document.querySelectorAll(\"img\")).filter(i=>i.naturalWidth>400).length)()" | agent-browser --session $G eval --stdin | tr -dc "0-9"); [ "$n" -ge "$ALVO" ] && { echo READY; break; }; sleep 5; done'
```

Só considere falha real se o contador não subir depois de ~10 minutos.

Baixar as imagens geradas (fetch na própria página). **Nome sempre prefixado com a lane** — sem isso outra lane sobrescreve seu arquivo em `~/Downloads`:

```bash
cat <<'EOF' | agent-browser --session $G eval --stdin
(async () => {
  const ids = ["file_XXX","file_YYY"];                       // ids das imagens geradas
  const srcs = Array.from(document.querySelectorAll('img')).map(i=>i.src);
  for (let k=0;k<ids.length;k++){
    const url = srcs.find(s=>s.includes(ids[k]));
    const r = await fetch(url); const b = await r.blob();
    const a = document.createElement('a');
    a.href = URL.createObjectURL(b); a.download = `${LANE}-cena-${k+1}.png`;   // substitua ${LANE} pelo nome da lane
    document.body.appendChild(a); a.click(); a.remove();
  }
  return 'ok';
})()
EOF
sleep 3
~/.claude/bin/lane.sh collect $LANE $PROJETO/IMG    # ~/Downloads/$LANE-* → staging → projeto, SEMPRE com destino — nunca só `collect $LANE` sozinho
```

Para descobrir os ids: `document.querySelectorAll('img')` filtrando por `naturalWidth > 200`.

**Baixe uma imagem por vez.** Um `eval` que dispara 8-10 downloads em rajada faz o
Chromium bloquear tudo depois do segundo — sem erro, você só descobre contando os
ficheiros. Um `eval` por imagem, `sleep 2` entre eles, e confira o total no fim.

**A ordem do DOM não é a ordem das cenas.** Num lote de 10 as imagens vêm
embaralhadas. Antes de mandar qualquer uma pro vídeo, monte um contact sheet e
remapeie pelo conteúdo:

```bash
ffmpeg -pattern_type glob -i "lote-*.png" -vf "scale=200:-1,tile=5x2" -frames:v 1 sheet.jpg
```

Aproveite o mesmo sheet para checar **consistência entre as duas cenas do mesmo
hook** — roupa, cabelo e ambiente têm que bater. Se não baterem, regere **uma**
imagem anexando a outra como referência; sai mais barato que refazer o clipe.

Mova para `HOOK/IMG/cena-N.png` (ou `IMG/cena-N.png` no Modo A).

---

## Páginas de ATIVIDADE (folha "w" — worksheet imprimível) de entregável low ticket

Entregável com fichas de atividade (NeuroActiva e o mesmo padrão em qualquer oferta do gênero)
tem DOIS arquivos por ficha: `pagina-NNN` (card de instrução pro profissional, foto real — já
é gerado no GPT) e `pagina-NNNw` (a folha que a PESSOA imprime pra FAZER a atividade — sopa de
letras, labirinto, sequência, cálculo, ordenar passos). O "w" **nunca** pode ser código/Pillow
desenhado (regra da dona, 23/10/2026 — ficou com ícone de arco-íris chapado, "psicodélico") —
tem que ser gerado no GPT no mesmo padrão visual navy/dourado das fichas.

**Referência de qualidade pra sopa de letras / word search e similares:** quando faltar um bom
modelo visual pra um tipo de exercício, procurar referência no Pinterest (busca de imagem) ou
nos materiais do mineirador/concorrente que já foi modelado pra oferta (a dona cita "o Kim" como
exemplo de modelador que já teve exercícios assim — ver `pesquisa/` da oferta ou a mineração
registrada). Nunca inventar o layout do zero sem referência quando o tipo de exercício for
visualmente específico (grade de letras, labirinto com caminho).

### Lote de página-de-atividade NÃO escala como lote de capa — confirmado em produção, use 1 por vez

Capas de produto (mesmo layout, só troca título/cor) saíram 9-10 de 9-10 numa mensagem só. Página
de atividade (cada uma com layout e conteúdo DIFERENTE — grid, linhas de resposta, tabela) **não
tem o mesmo comportamento**, testado repetidas vezes em produção (NeuroActiva V5, 23/10/2026):

- Pedido de 8 atividades diferentes numa mensagem só → devolveu **1**.
- "Continua as outras" no mesmo chat → só mais **1** (às vezes REPETIU/variou a mesma ficha em
  vez de avançar).
- Prompt reforçado com densidade visual + "6 SEPARATE image attachments" explícito, pedindo 6 de
  uma vez → de novo só **1-2** novas, resto repetição.
- Pedido de 3 com o TEXTO COMPLETO E EXATO de cada uma (título exato, instrução exata, valores
  exatos) em chat novo → também só **1** de cada vez, mas cada uma saiu perfeita.

**Conclusão fechada: não tem prompt mágico que faça o lote de atividade funcionar. O fluxo
confirmado e que SEMPRE funciona é 1 imagem por mensagem, pedindo explicitamente a próxima pelo
número**, mesmo que o primeiro pedido descreva todas as N (não atrapalha, só a 1ª sai). Nunca
prometa "N de uma vez" pro usuário nessa tarefa — avise que é 1-por-1, ~1-2min cada.

Fluxo:
1. Chat novo no projeto, anexa 1-2 referências de estilo (card aprovado + 1 atividade já aprovada).
2. Manda o pedido com a descrição completa de todas as N fichas (serve de contexto pro resto do
   chat, mesmo que só a 1ª saia).
3. A cada resposta: baixa, confere `md5` contra os já baixados (pega repetição disfarçada de
   nome novo), e manda "HOJA 00X foi perfeita, agora gera HOJA 00Y" citando sempre o número exato
   que falta — nunca "continua"/"as outras" genérico, isso é o que mais repete.
4. **Atenção especial:** a resposta pode vir como "documento"/canvas em vez de `<img>` solto — a
   skill `gpt-imagem-playwright` detecta isso quando o filtro de `querySelectorAll('img')` não
   cresce mas a UI mostra "NeuroActiva_Hoja_00X.png" com botão "Baixar arquivo"/"Abrir prévia" em
   vez do preview inline. Quando acontecer, peça pro próprio modelo "resend exactly those as
   plain standalone PNG image attachments using the image generator, not a document or canvas" —
   resolve, mas conta como mais 1 rodada "1 por vez".
5. Reporte ao usuário em marcos (a cada 5-8 prontas), nunca uma por uma — mas publique/commite
   em lotes menores pra não acumular risco.

Essa é uma tarefa de MUITAS gerações (um módulo de 32 fichas = ~32 rodadas de "próxima"). Avise o
usuário do volume real antes de começar.

---

