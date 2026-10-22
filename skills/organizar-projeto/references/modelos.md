# Moldes

Troque `<...>`. Fato não confirmado = `?`. Escreva curto: CLAUDE.md entra no contexto de toda sessão.

---

## CLAUDE.md da raiz

```markdown
# <NOME> — regras do portfólio

<1 frase: o que é esta pasta.> Cada projeto em `<PROJETOS>/<slug>/` tem CLAUDE.md, STATUS.md e
memória próprios — abra o terminal dentro dele pra herdar este arquivo + o dele.

## Ao abrir
1. `STATUS.md` (painel geral) e `_memoria/estrategia.md` (foco atual).
2. Vai mexer num projeto: leia o `CLAUDE.md` + `STATUS.md` dele antes.

## Mapa da raiz
| Pasta | O que é |
|---|---|
| `<PROJETOS>/` | 1 pasta por projeto (padrão abaixo) |
| `CONHECIMENTO/` | … |
| `MODELOS/` | … |
| `_arquivo/` | backups e lixo conferido; log da reorganização |

## Padrão de pasta de projeto
<árvore curta de references/estrutura-padrao.md> — detalhe: skill `organizar-projeto`.

## Skills obrigatórias por tarefa
<tabela de references/mapa-skills.md>

## Regras do negócio
<gates, checklists obrigatórios, regras de STATUS>

## Ao terminar
STATUS.md do projeto (Atualizado em + Histórico + Pendências) e a linha dele no `STATUS.md` da raiz.
Aprendeu regra que vale sempre → `_memoria/` (negócio) ou CLAUDE.md do projeto (só dele).
```

## STATUS.md da raiz

```markdown
# STATUS — <NOME>

**Atualizado em:** AAAA-MM-DD

## Projetos
| Projeto | Fase | Mercado | No ar | Atualizado | Próximo passo |
|---|---|---|---|---|---|

## Frentes (fora dos projetos)
| Frente | Pasta | Estado |
|---|---|---|

## Histórico
- `AAAA-MM-DD` — …
```

## `_memoria/`
- `empresa.md` — quem somos, o que vende, contas e infra compartilhadas (domínio base, servidor, gateways, pixel, contas de IA). Ponteiro pra memória detalhada, não cópia.
- `estrategia.md` — foco de agora, prioridade por projeto, o que pausou e por quê. Data em tudo.
- `preferencias.md` — como a pessoa quer o trabalho: idioma, tom, nível de autonomia, o que nunca fazer.

## CLAUDE.md do projeto

```markdown
# <Nome> — <tipo de projeto>

> Herda `../../CLAUDE.md` (skills obrigatórias, gates). Aqui só o que é deste projeto.

## O que é
<1-3 linhas: produto, público, mercado/moeda, preço, fase.> Estado vivo: `STATUS.md`.

## No ar
- Página: <url | ?> · Área de membros: <url | ?> · Repo: <remote | ?> · Deploy: <como>

## Mapa da pasta
| Pasta | O que tem |
|---|---|
| `pesquisa/` | … |
| `site/` | … (repo git; editar aqui? sim/não) |

<Exceções de estrutura e symlinks legados, se houver.>

## Skills deste projeto
Além da tabela da raiz: <skills específicas, ou "nenhuma além da raiz">.

## Memória do projeto
Regras e decisões que valem só aqui (com data). Decisão nova → acrescente uma linha.
- `AAAA-MM-DD` — …
```

## STATUS.md do projeto
Use o molde já existente da pasta (ex. `MODELOS/_MODELO-STATUS.md`). A seção "Mapa da pasta"
do STATUS vira só: `Ver CLAUDE.md → Mapa da pasta.` (um lugar só pra manter).

## briefing.md de criativo (`criativos/[MERCADO/]CRIATIVO-N/`)

```markdown
# CRIATIVO-<N> — <ângulo em 3-6 palavras>
- **Formato:** vídeo 9:16 | estático | carrossel · **Mercado:** BR
- **Persona × dor/bolha:** …
- **Hook:** …
- **Skill usada:** criativo-ads → <mecânica>
- **Final:** `<arquivo>` · **Status:** rascunho | aprovado | no ar | pausado
- **Copy do anúncio:** (ou `anuncio.md`)
```
