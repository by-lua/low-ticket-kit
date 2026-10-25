---
name: low-ticket-atualizar
description: >
  Varre o portfólio LOW-TICKET (ou uma oferta específica) e compara o que os arquivos de memória
  dizem contra o estado real do workspace (arquivos, pastas, datas). Aponta divergência: inventário
  de material desatualizado, STATUS.md defasado, skill com regra que não bate mais com o produto
  real. Use quando o usuário disser "atualiza", "/atualizar", "varre o projeto/a oferta",
  "confere se a memória tá certa", ou sempre que uma correção da dona sugerir que algo no contexto
  mudou e não foi registrado.
---

# /low-ticket-atualizar — varredura memória × realidade

Adaptado do padrão MazyOS `/atualizar`. Não inventa fato — só aponta divergência com evidência do
disco, e deixa a dona decidir o que aplicar.

## Workflow

### Passo 1 — Escopo

Pergunta implícita: oferta específica (mais comum, mais barato) ou portfólio inteiro (raro, só
quando pedido "varre tudo"). Oferta específica: só mexe nos arquivos dela + linha dela no STATUS
raiz. Portfólio inteiro: repete o passo 2 pra cada oferta em `OFERTAS/`.

### Passo 2 — Levantamento (por oferta)

- `find criativos/ -maxdepth 2 -newermt "<N dias atrás>"` — material/criativo novo na pasta.
- `find criativos/*/INVENTARIO.md criativos/*/README.md -mtime +7` cruzado com os arquivos de
  mídia da mesma pasta — inventário mais velho que o material = defasado.
- `grep -c "^- \[ \]" STATUS.md` — pendências em aberto, comparar com o que já foi resolvido na
  conversa/sessão atual.
- Data de "Atualizado em" do `STATUS.md` vs. data de hoje — mais de ~7 dias sem tocar numa oferta
  ativa é sinal de alerta, não necessariamente erro.
- `pesquisa/PERSONA-E-ANGULOS.md` existe e bate com a página no ar (preço, bônus, nome do produto)?

### Passo 3 — Comparação

Para cada arquivo de memória da oferta (`CLAUDE.md`, `STATUS.md`, `criativos/*/INVENTARIO.md`,
`_memoria/` central), perguntar: **o que ele afirma ainda é verdade no disco?** Ex.: "STATUS diz
0/30 peças, mas tem 15 pastas `CRIATIVO-N` com arquivo final" · "INVENTARIO lista 9 fontes mas a
pasta `PC/` foi arquivada — inventário mentindo" · "CLAUDE.md da oferta não menciona a regra de GC
nova que a dona deu, mas já apareceu em 2 peças dessa oferta".

### Passo 4 — Proposta

```
Encontrei [N] coisas desatualizadas em <oferta>:

1. criativos/MATERIAL-ENTREGAVEL/INVENTARIO.md — lista PC/ mas a pasta foi arquivada em 25/10
2. STATUS.md diz "0/30 peças" mas 15 pastas CRIATIVO-N já têm arquivo final
3. CLAUDE.md da oferta não tem a regra de GC "pessoa segura material sempre" (criativo-ads já tem)

Aplico todas, só algumas, ou nenhuma?
```

### Passo 5 — Aplicação

Edição cirúrgica (só a linha/trecho relevante, nunca reescreve o arquivo inteiro). Depois de
aplicar, roda a FASE 3 de `low-ticket-painel` normalmente (Hub, STATUS raiz) se algo relevante
mudou.

## Regras

- Nunca inventa fato — só o que tem evidência no disco (`ls`/`ffprobe`/`grep`/data de modificação).
- Evidência ambígua (ex.: pasta vazia, arquivo com nome genérico) → pergunta antes de registrar.
- Nunca apaga conteúdo de memória, só atualiza/adiciona.
- Nada pra atualizar → responde "Tá tudo coerente, nada pra atualizar" e para.
- Regra de produção (CTA, corte, b-roll) encontrada desatualizada na skill de mecânica
  (`criativo-ads`, `criativo-ads-video-orq`) é corrigida **lá**, nunca copiada pro CLAUDE.md da
  oferta — fonte única por tópico (ver `_memoria/` do portfólio).
