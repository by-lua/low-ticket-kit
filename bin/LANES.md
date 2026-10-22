# Lanes — vários Claudes no mesmo browser logado

Problema: o login é do **perfil** (`gpt`, `hub`, `gg`) e o perfil é único — clonar
diretório de perfil derruba a sessão e o Cloudflare volta. Mas sem isolamento
dois Claudes escrevem no **mesmo chat**: todo comando `agent-browser` cai na
última aba criada, então quem abre uma aba rouba o ponteiro de quem já estava lá.

Solução: **uma lane por Claude**, dentro do mesmo perfil.

| Camada | Valor | Por quê |
|---|---|---|
| Perfil / porta CDP | `gpt` 9222, `hub` 9223, `gg` 9224 | onde mora o login — nunca duplicar |
| Sessão agent-browser | `<perfil>-<lane>` | cada sessão guarda o próprio ponteiro de aba |
| Aba | label `<lane>` | labels e ids `t<N>` são namespace **por sessão** |
| Staging de download | `~/Downloads/<AREA>/<lane>/` | `~/Downloads` é global e as lanes se sobrescrevem |

**Áreas de staging.** A área separa ferramentas que não têm nada a ver uma com
a outra, e entra por `LANE_AREA`:

| Área | Para quê | Pasta |
|---|---|---|
| `PLAYWRIGHT` (padrão) | geração por browser: ChatGPT, bancos de imagem | `~/Downloads/PLAYWRIGHT/<lane>/` |
| `HUB` | NinjaBR Hub: vídeo, criativo, transcrição | `~/Downloads/HUB/<lane>/` |

```bash
export LANE_AREA=HUB
lane.sh dir minhalane        # ~/Downloads/HUB/minhalane
lane.sh collect minhalane <destino>
```

Um fluxo que usa as duas (o criativo de vídeo: imagens no ChatGPT, clipes no
Hub) exporta a variável na fase certa. Misturar faz um `collect` levar arquivo
de uma fase para a pasta da outra.

## Pegar a lane (primeira coisa, sempre)

```bash
~/.claude/bin/lane.sh take gpt cozinha     # sobe o perfil, cria/fixa a aba, cria o staging
```

Imprime a sessão a usar. A partir daí **todo** comando leva essa sessão:

```bash
S=gpt-cozinha
agent-browser --session $S snapshot -i -c
```

Escolha o nome da lane pelo trabalho, não por número: `cozinha`, `espanhol`,
`tarot`. Dois Claudes na mesma tarefa = mesma lane de propósito; tarefas
diferentes = lanes diferentes, sempre.

## Re-fixar a aba antes de cada bloco

```bash
agent-browser --session $S tab cozinha
```

Barato e obrigatório: se outra lane abriu aba no meio do caminho, o ponteiro
pode ter saltado. `lane.sh take` refaz isso e é idempotente — pode rodar de novo
a qualquer momento.

## Chat/aba limpa

- **ChatGPT:** a lane começa em `https://chatgpt.com/`. Para novo chat dentro da
  lane, `navigate https://chatgpt.com/` — nunca clique em conversa do histórico,
  ela pode ser de outra lane.
- **Hub:** cada aba tem a própria barra de criação; o estado (imagem anexada,
  prompt) é por aba. Mesmo assim limpe o textarea antes de cada geração.

## Downloads

Nomeie o arquivo com o prefixo da lane no `a.download`:

```js
a.download = `cozinha-cena-1.mp4`;
```

Depois recolha e mande pro projeto:

```bash
~/.claude/bin/lane.sh collect cozinha /caminho/do/projeto/assets
```

Sem prefixo, duas lanes gerando `cena-1.mp4` se sobrescrevem em `~/Downloads`.

## Outros comandos

```bash
~/.claude/bin/lane.sh list             # lanes ativas + URL de cada aba
~/.claude/bin/lane.sh dir cozinha      # caminho do staging
~/.claude/bin/lane.sh drop gpt cozinha # fecha a aba e libera a lane (faça ao terminar)
```

## Regras que não mudam

- Nunca `agent-browser open` nem `press Escape` — derrubam para o Chromium
  empacotado, sem login, com Cloudflare que não passa.
- Nunca `agent-browser close --all` — mata as abas das outras lanes.
- Feche só a sua: `lane.sh drop <perfil> <lane>`.
