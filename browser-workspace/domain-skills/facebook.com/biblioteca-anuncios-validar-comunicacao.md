# Biblioteca de Anúncios — validar se uma comunicação já existe

Executado e verificado em 2026-08-31, perfis `adslib`..`adslib4` (portas 9232, 9235-9237).

## Acesso
Abre sem login. O "Entrar" do topo é falso positivo de detector de login.
Perfis paralelos: `~/.claude/bin/browsers.sh adslib adslib2 adslib3 adslib4`.
4 varreduras simultâneas rodam sem rate limit — 48 queries levaram ~2 min.

## URL direta (não preencher formulário)
```
https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=BR&q=<URLENCODED>&search_type=keyword_unordered&media_type=all
```

## Extração (eval, após `sleep 6`)
```js
(function(){
  var m=document.body.innerText.match(/~?[\d.,]+\s*resultados/i);
  var ids=[...new Set([...document.body.innerHTML.matchAll(/Identifica..o da biblioteca:\s*(\d+)/g)].map(x=>x[1]))];
  var t=document.body.innerText.split("\n").filter(l=>l.length>45).slice(0,10).map(l=>l.slice(0,150));
  return JSON.stringify({total:m&&m[0],n:ids.length,ids:ids.slice(0,6),amostra:t});
})()
```
`total` ausente + texto "Nenhum anúncio corresponde" = zero real.
`n` (ids no DOM) é só o que carregou no 1º viewport — use `total`, não `n`.

## ⚠️ Armadilha: query longa devolve ZERO fácil
`keyword_unordered` NÃO é OR — quanto mais palavras, mais restritivo.
"estampas de motociclista para camiseta uso comercial" → 0
"estampas para camiseta" → 1.200

**Sempre rode o teste de controle antes de confiar num zero.** Uma query de 6
palavras num território sabidamente populado tem que voltar populada:
`atividades de alfabetização para imprimir professora` → ~290. Se der zero, o
motor está quebrado, não o mercado.

## Método de 2 camadas (o que dá leitura confiável)
1. **Camada específica** — a comunicação exata que você quer usar (6-8 palavras).
   Zero aqui = a vaga da SUA comunicação está livre.
2. **Camada de território** — o núcleo em 3-4 palavras.
   Mede se existe mercado ao redor.

Cruzamento:
| específica | território | leitura |
|---|---|---|
| 0 | alto | **VAGA BOA** — mercado existe, ninguém falou assim |
| 0 | 0 | **DESERTO** — ninguém anuncia nada; ou nicho morto, ou oportunidade cega |
| >0 | alto | **OCUPADO** — trocar direção |

Um zero na camada 1 sozinho não prova nada.

## ⚠️ UI em inglês gera zero falso (2026-09-16)
Perfis adslib3/adslib4 ficaram com a Biblioteca em inglês ("~380 results"). O contador
que casa só `resultados` devolve 0 pra tudo — inclusive o controle. Regex tem que ser
`/~?[\d.,]+\s*(resultados|results)/i` e esperar ~7s após o `open` (1s dava zero).
`MINERACAO/scripts/validar.sh` já corrigido. Controle zerado = motor quebrado, sempre.
