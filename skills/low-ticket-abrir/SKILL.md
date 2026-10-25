---
name: low-ticket-abrir
description: >
  Abertura rápida de sessão no portfólio LOW-TICKET: lê PANORAMA+STATUS raiz e devolve um resumo
  curto (1 frase por oferta, foco atual, pendência que mais importa). Use quando a dona disser
  "abrir", "começar o dia", "/abrir", "onde paramos" sem mencionar tarefa específica ainda.
---

# /low-ticket-abrir — abertura de sessão

Atalho leve de `low-ticket-painel` FASE 0, no padrão MazyOS `/abrir`: carrega e devolve síntese
curta, sem listar o que leu. Quando a tarefa já vier definida ("gera criativo pra X"), pula direto
pra `low-ticket-painel` inteira — esta skill é só pro "abre e me diz onde estamos".

## Workflow

1. Ler `PANORAMA.md` e `STATUS.md` da raiz.
2. Devolver, em até 6-8 linhas:

```
LOW TICKET — [N] ofertas ativas.
[Oferta 1]: [fase em 4-6 palavras] — [maior pendência/bloqueio]
[Oferta 2]: [fase] — [maior pendência]
...
Foco da semana: [linha de _memoria/estrategia.md, se existir]

O que fazemos?
```

3. Não listar os arquivos lidos, não confirmar leitura.

## Regras

- Caber na tela sem rolar demais — 1 linha por oferta, não o histórico inteiro.
- Se alguma oferta tem pendência "dona"/"aprovar" nela, destacar — é o que trava o próximo passo.
- Tarefa específica dada junto do "abrir" → segue direto pra `low-ticket-painel`, não para nesta.
