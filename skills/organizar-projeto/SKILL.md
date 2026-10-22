---
name: organizar-projeto
description: Organiza uma pasta grande de trabalho no padrão "sistema operacional" (inspirado no MazyOS) — raiz com CLAUDE.md, STATUS.md geral e _memoria/; cada projeto/oferta/cliente com CLAUDE.md próprio, STATUS.md, memória e pastas fixas (pesquisa, produto, site, checkout, criativos/CRIATIVO-N, trafego, prints, _arquivo); e uma tabela "tarefa → skill obrigatória" pra todo agente que entrar ali. Inventaria, propõe o mapa de movimentação, move com symlink onde algo depende do caminho velho, conserta referências em skills/memórias e escreve os docs. Use quando o usuário pedir "organiza essa pasta/esse projeto", "deixa no padrão", "estrutura igual o low ticket/MazyOS", "cada projeto com seu CLAUDE/status/memória", "documenta as skills que tem que usar", ou criar projeto/oferta nova já no padrão.
---

# organizar-projeto

Transforma uma pasta bagunçada num sistema: o agente que abrir qualquer subpasta sabe
**o que é, em que pé está, onde guardar cada coisa e qual skill é obrigatória pra cada tarefa**.

Referência viva já aplicada: `~/Documentos/TRAMPO/PROJETOS/WORKING/PROJETOS - INTERNOS/LOW-TICKET/`
(leia o `CLAUDE.md` dela quando estiver em dúvida de como fica pronto).

Arquivos desta skill:
- `references/estrutura-padrao.md` — árvore da raiz e do projeto, o que vai em cada pasta, regras
- `references/modelos.md` — moldes de CLAUDE.md (raiz e projeto), STATUS.md (raiz e projeto), `_memoria/`, briefing de criativo
- `references/mapa-skills.md` — como montar a tabela "tarefa → skill obrigatória" + catálogo base
- `scripts/inventario.sh <pasta>` — raio-x: árvore, repos git, symlinks, arquivos soltos, tamanhos, quem referencia a pasta
- `scripts/mover.sh <base> <plano.tsv>` — executa o plano (mv + symlink opcional + log), idempotente

## Fluxo

### 1 · Inventário (não mexe em nada)
```bash
bash ~/.claude/skills/organizar-projeto/scripts/inventario.sh "<pasta-raiz>"
```
Leia também: CLAUDE.md/AGENTS.md existentes, STATUS/README de cada projeto, e as memórias do
projeto (`~/.claude/projects/<slug-da-pasta>/memory/` e as do Overclock). **Convenção que já existe
em memória ganha da genérica** — estenda, não contradiga.

Cheque também:
- Repos git (`site/`, `pagina/`…) e scripts com caminho relativo (`deploy.sh`, `*.sh`, `build.mjs`):
  `grep -rn '\.\./' --include='*.sh' --include='*.mjs' --include='*.py'`
- Referências externas à pasta: skills (`~/.claude/skills`), memórias, docs (`~/.claude/docs`)
  — o inventário lista. Script que valida caminho (gate) precisa de fallback ou update.
- Panes/agentes ativos com cwd dentro da pasta (Overclock: `pane_list`). Running = não mova o que ele usa.

### 2 · Plano (uma pergunta ao usuário, só o que ele precisa decidir)
Monte `plano.tsv` (`origem<TAB>destino<TAB>link`) seguindo `references/estrutura-padrao.md`.
Pergunte com AskUserQuestion só o que for decisão dele:
- mover + symlink (recomendado) × mover limpo × só documentar
- juntar projetos duplicados (mesma oferta em 2 pastas)
Não pergunte o óbvio (onde vai obra-de-arte, prints etc. — o padrão decide).

**Regras de symlink** (link=1): repo git movido, pasta usada por script/deploy, pasta citada
por skill/memória, cwd de pane vivo, projeto renomeado/fundido. Arquivo solto de doc: sem link
— conserte a referência. Nunca symlink dentro de repo git.

**Nunca mover:** `.git`, `.claude`, `.codex`, `.overclock-app`, `node_modules`, `.data`; arquivos que
um script de deploy copia por caminho fixo (documente a exceção no CLAUDE.md do projeto).
Mídia de terceiros em pasta sincronizada → regra do CLAUDE.md da pasta-mãe (ex. PROJETOS-MIDIA + symlink).

### 3 · Executar
```bash
bash ~/.claude/skills/organizar-projeto/scripts/mover.sh "<base>" plano.tsv
```
Log vai em `<raiz>/_arquivo/REORGANIZACAO-<data>.log`. Depois confira:
- `find -L <raiz> -maxdepth 4 -type l` → nenhum symlink quebrado
- `git -C <repo> status --short` → nada novo além do que já estava sujo antes
- script com `../caminho` atualizado (sed) e testado

### 4 · Consertar referências
`grep -rn` nas skills, memórias, docs e .md da pasta pelo caminho velho → `sed` pro novo.
Validador/gate que procura arquivo em caminho fixo → fallback que aceita o novo e o velho.

### 5 · Escrever os docs (moldes em `references/modelos.md`)
1. **Raiz:** `CLAUDE.md` (regras do portfólio + mapa da raiz + **tabela de skills obrigatórias**),
   `STATUS.md` (1 linha por projeto + frentes), `_memoria/{empresa,estrategia,preferencias}.md`.
   Índice antigo (ex. `OFERTAS.md`) vira symlink pro `STATUS.md`.
2. **Cada projeto:** `CLAUDE.md` (o que é, links no ar, mapa da pasta com o que tem HOJE,
   skills específicas, exceções de estrutura, **Memória do projeto**), `STATUS.md` atualizado
   (Atualizado em + Histórico + seção "Mapa da pasta" apontando pro CLAUDE.md).
3. Fato que você não confirmou = `?` — nunca invente domínio, preço, checkout.

### 6 · Memória e relatório
- Atualize/crie a memória de convenção de pastas do projeto (uma só, sem duplicar).
- Relatório final curto: o que moveu (contagem + log), symlinks criados, refs consertadas,
  docs escritos, pendências (STATUS desatualizado, coisa que não deu pra classificar).

## Projeto novo dentro de pasta já organizada
Crie `<PROJETOS>/<slug>/` com `CLAUDE.md` + `STATUS.md` (moldes) e **só as pastas que a primeira
tarefa usa** — o resto nasce quando precisar, sempre com o nome do padrão. Linha nova no STATUS da raiz.

## Regras
- Raiz e raiz de projeto = só `.md` + pastas. Nada de imagem/zip/print solto.
- Criativo = pasta própria: `criativos/[<MERCADO>/]CRIATIVO-<N>[-slug]/` com briefing/roteiro, final solto e `intermediarios/`. Tudo daquele criativo dentro dele.
- Nunca deletar: o que parece lixo vai pra `_arquivo/`.
- Nunca commitar/pushar repo durante a reorganização.
