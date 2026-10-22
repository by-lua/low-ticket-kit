# domain-skills — memoria de browser por site

Receitas persistentes de automacao web. **Compartilhado entre `agent-browser`
(padrao) e `browser-harness` (escalonamento CDP).** O harness le esta pasta
sozinho quando `BH_DOMAIN_SKILLS=1`; o agent-browser depende de voce ler.

    domain-skills/
      _shared/RECEITA-TEMPLATE.md   <- copie isso pra criar receita nova
      _shared/README.md             <- este arquivo
      chatgpt.com/
      ninjabrhub.io/
      ggcheckout.app/

## Protocolo — LER

Antes de qualquer trabalho num site:

    ls ~/.claude/browser-workspace/domain-skills/<host>/
    cat ~/.claude/browser-workspace/domain-skills/<host>/*.md

Achou receita do fluxo? Siga. Nao re-explore o site.
Receita marcada `quebrado` ou `Ultima validacao` velha? Siga mesmo assim como
ponto de partida, e corrija o arquivo com o que achar.

## Protocolo — GRAVAR

Grave quando qualquer uma for verdade:

- resolveu um fluxo novo num site (gerou imagem, criou produto, exportou relatorio)
- gastou mais de ~3 tentativas achando um seletor ou uma espera
- descobriu armadilha nao obvia (modal que rouba foco, cota silenciosa, iframe)
- uma receita existente quebrou e voce achou o novo caminho

Nao grave: navegacao trivial de uma tela, coisa que so vale nesta conversa.

Fluxo:

    cp _shared/RECEITA-TEMPLATE.md <host>/<fluxo>.md
    # preencher com comandos verbatim que voce executou

Atualizar receita existente > criar segunda receita do mesmo fluxo. Duas
receitas do mesmo fluxo divergindo e pior que nenhuma. Adicione linha em
`## Historico` e mexa em `Ultima validacao`.

## Regra de ouro

So entra aqui o que foi **executado e verificado**. Passo que voce nao rodou
nao vai pro arquivo — receita errada custa mais caro que arquivo vazio.

## Relacao com as skills existentes

`gpt-imagem-playwright`, `grok-video-hub-playwright`, `ggcheckout-produto` e
`video-hub` continuam sendo o playbook de alto nivel (o que fazer, em que ordem).
Estas receitas sao a camada de baixo: seletor, espera, armadilha. Quando a skill
e a receita divergirem, a receita ganha — ela foi validada por ultimo.
