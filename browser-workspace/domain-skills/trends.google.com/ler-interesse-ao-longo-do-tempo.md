# Google Trends — ler "Interesse ao longo do tempo"

Verificado em 2026-08-30.

## O problema

Trends devolve **429 Too Many Requests** para qualquer perfil deslogado, em
qualquer porta. Não é rate limit de sessão — é por IP + ausência de conta. Trocar
de perfil anônimo não resolve; testado em `adslib`, `ferriani` e `trends` novo.

Os atores do Apify também não resolvem:
- `apify/google-trends-scraper` → roda 8+ min, termina SUCCEEDED com **0 itens**
  (log: `Failed to handle embed widget RELATED_QUERIES: TimeoutError`).
- `data_xplorer/google-trends-fast-scraper` → só entrega *trending searches* do
  dia (geo US), não série histórica. Ator errado para esse fim.

## A solução: perfil logado

Qualquer perfil com conta Google logada abre o Trends normalmente. O perfil
`gcloud` (porta 9228) já está logado.

Para não brigar pelo `gcloud`, clone-o:

```bash
pkill -f "agent-profiles/trends"
rm -rf ~/.agent-profiles/trends && mkdir -p ~/.agent-profiles/trends
rsync -a --exclude='*Cache*' --exclude='Code Cache' --exclude='GPUCache' \
      --exclude='Service Worker/CacheStorage' --exclude='Singleton*' \
      ~/.agent-profiles/gcloud/ ~/.agent-profiles/trends/
~/.claude/bin/browsers.sh trends          # porta 9234
```

333M → 145M sem os caches. O login vem junto e sobrevive a reboot.

## Ler o valor

A página é Angular e monta o widget depois do load — **eval imediato volta
vazio**. Faça polling até o texto conter `Média`.

```bash
URL="https://trends.google.com/trends/explore?date=today%205-y&geo=BR&q=t1,t2,t3&hl=pt-BR"
agent-browser --session trends open "$URL"
# repita até casar "Média":
agent-browser --session trends eval '
  var t=document.body.innerText.replace(/\s+/g," ");
  var i=t.indexOf("Interesse ao longo do tempo");
  i<0?"":t.slice(i,i+280)'
```

Retorno útil: `... Média x1 <termo1> <termo2> <termo3> Média <v1> <v2> <v3> ...`

Script pronto (até 3 termos por chamada): ver `trends.sh` nesta pasta.

## Armadilha de interpretação

Os valores são **relativos dentro de cada comparação**, escala 0-100 normalizada
pelo maior termo daquela consulta. Comparar número entre consultas diferentes é
inválido. Para comparar listas grandes, repita um **termo âncora** em todas as
consultas e normalize por ele.

Máximo de 5 termos por comparação (o script usa 3 para caber na leitura de texto).
