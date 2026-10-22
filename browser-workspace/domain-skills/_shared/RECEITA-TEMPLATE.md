# <fluxo> — <host>

<!--
COMO USAR ESTE TEMPLATE

Um arquivo por FLUXO, nao por site. Nome do arquivo em kebab-case:
  domain-skills/chatgpt.com/gerar-imagem-com-referencia.md
  domain-skills/ninjabrhub.io/imagem-para-video-veo.md

Regra: gravou uma receita = proxima sessao nao re-explora o site.
So grave o que voce EXECUTOU e viu funcionar. Nada de suposicao.
-->

**Perfil / porta CDP:** `hub` / 9223
**Ferramenta padrao:** agent-browser | browser-harness (diga qual, e por que)
**Ultima validacao:** AAAA-MM-DD
**Estado:** funciona | fragil | quebrado

## Pre-condicoes

- perfil no ar: `~/.claude/bin/browsers.sh <perfil>`
- login: ja persistido no perfil / precisa `$VAR_DE_SENHA` do `~/.claude/.credentials.env`
- qualquer coisa que precise estar aberta/selecionada antes

## Passos

1. `<comando exato>` → `<o que aparece>`
2. ...

Comandos verbatim. Seletores/refs reais. Sem "clique no botao de enviar" —
escreva o seletor ou o texto exato do elemento.

## Seletores / ancoras estaveis

| Elemento | Ancora | Nota |
|---|---|---|
| botao enviar | `[data-testid="send-button"]` | muda de `aria-label` entre releases |

Prefira: `data-testid` > texto acessivel > aria-label > CSS estrutural.
Nunca grave XPath posicional (`div[3]/div[2]`) — quebra na semana seguinte.

## Esperas

O que sinalizar fim de cada passo (elemento que aparece/some), nunca sleep fixo.

## Armadilhas

- Cloudflare: clicar no checkbox funciona nesses perfis; 2x falha = chamar usuario
- rate limit / cota: como o site avisa, e qual o fallback
- estados que parecem sucesso mas nao sao

## Saida

Onde o resultado cai (path de download, texto na tela, request de rede a ler).

## Helper

Se virou funcao Python: nome dela em `~/.claude/browser-workspace/agent_helpers.py`.

## Historico

- AAAA-MM-DD: criado
