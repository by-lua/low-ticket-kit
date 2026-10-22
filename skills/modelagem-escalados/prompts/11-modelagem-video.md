# PROMPT 11 — MODELAGEM DE VÍDEO (ponte para o pipeline de vídeo)

> Os 16 vídeos do catálogo (13 com transcrição `.txt`) não se modelam como estático.
> Aqui você extrai a **estrutura** do vídeo escalado e entrega o briefing que a skill
> `criativo-ads-video-orq` consome.

## Passo 1 — decupagem

Com o vídeo e, quando existir, a transcrição `.txt` em mãos, devolva:

| Bloco | Timestamp | Fala (literal) | O que está em quadro | Função |
|---|---|---|---|---|

Funções possíveis: hook, agitação da dor, mecanismo, prova, oferta, CTA.

Depois responda:
- **Onde está o corte de atenção?** — o segundo exato em que o vídeo compra os
  próximos 3 segundos.
- **Qual é o mecanismo do hook?** — em uma frase, o que faz parar o scroll,
  independente do produto.
- **Persona e ângulo** do original.

## Passo 2 — adaptação

Reescreva a estrutura para o meu produto, mantendo **função e ritmo** de cada bloco e
trocando integralmente conteúdo, persona e prova.

Restrições que vêm do pipeline de vídeo e não são negociáveis:
- **16 palavras por cena** no Veo 8s (22 no Grok 10s) — acima disso a voz sai robótica;
- fala **literal** no roteiro, em PT-BR;
- **rosto em quadro em toda cena falada**;
- nada de prova, número ou depoimento fora do dossiê.

## Passo 3 — entrega

Devolva o briefing no formato que a skill `criativo-ads-video-orq` espera:

```
MODO: B (hook novo sobre body existente) | A (completo)
PERSONA:
ÂNGULO:
OFERTA:
CENAS:
  1. [função] fala: "..." (n palavras) — cenário/enquadramento
  2. ...
REFERÊNCIA MODELADA: id <id> — <nome do formato>
```

A produção (imagem no GPT, vídeo no Hub, QA, montagem) é da
skill `criativo-ads-video-orq`. Esta skill entrega o briefing e para.
