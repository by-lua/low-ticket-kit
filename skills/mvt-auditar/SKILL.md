---
name: mvt-auditar
description: MECÂNICA de verificação da skill `criacao-low-ticket-mvt` — como rodar `scripts/gate.py`, como auditar uma rodada inteira (nova ou antiga) contra `references/TRILHA-CHECKLIST.yaml`, e o que fazer com cada FALTA. Use antes de toda Parada e de chamar a próxima mecânica, ao retomar rodada ("onde paramos", modo R), quando o dono perguntar "pulamos algo?", ou ao apresentar uma Parada (Verificador Haiku).
---

# mvt-auditar — verificação mecânica de passagem

Por que existe (decisão 25/09/2026): gate em texto é checklist que o orquestrador precisa LEMBRAR de rodar; nas rodadas 6 e 7 foi
esquecido (`MINERACAO/FALHAS-GATE-R6/R7`). Aqui a passagem é conferida por script. **As regras dos passos continuam nas mecânicas**;
esta skill só diz como conferir e o que fazer com o resultado. Fonte da lista de itens: `criacao-low-ticket-mvt/references/TRILHA-CHECKLIST.yaml`.

## 1 · Rodar
```fish
set G ~/.claude/skills/criacao-low-ticket-mvt/scripts/gate.py
python3 $G --rodada "…/LOW-TICKET/MINERACAO/<rodada>" --passo T7            # 1 passo
python3 $G --rodada "…/MINERACAO/<rodada>" --ate T12                        # tudo de T0 até T12
python3 $G --rodada "…/MINERACAO/<rodada>" --passo T11 --oferta <slug>      # uma oferta (OFERTAS/<slug>)
python3 $G --rodada "…/MINERACAO/<rodada>" --passo T5 --concepcao r7-A-03   # uma concepção (Hub + arquivos que a citam)
python3 $G --rodada "…/MINERACAO/<rodada>" --ate T12 --so-falta             # só as lacunas
```
- Hub: precisa do `ofertas.json` decifrado (`cd HUB-OFERTAS; set -a; source ~/.claude/.credentials.env; set +a; uv run cifrar.py --verificar`). Sem ele os itens de Hub dão FALTA e o cabeçalho avisa.
- Condições (R4 nicho, cross, modo, formato/comunicação mudou, pivô, construção) saem do bloco `## ROTEADOR` e dos arquivos; item cuja condição é falsa aparece `[N/A]` com a condição — nunca some em silêncio.
- Sem `ESTADO.md` ou sem ROTEADOR: FALTA já em T0.
- Sem oferta/concepção informada: os itens de nível `oferta` rodam em TODAS as ofertas em jogo (Hub `rodada` = a da pasta, ou pasta `OFERTAS/<slug>` citada no ESTADO) e os de `concepcao` agregam o Hub da rodada.

## 2 · Ler a saída
`[OK]` evidência achada (mostra qual) · `[FALTA]` item obrigatório sem evidência (mostra qual checagem falhou) · `[N/A]` condição não vale ·
`[DONO]` dono dispensou por escrito (linha `ABERTO-POR-DECISÃO` com o ID ou o passo no ESTADO). Última linha `RESULTADO`; **exit ≠ 0 = existe FALTA**.

## 3 · O que fazer com FALTA (fixo, sem consultar o dono)
1. O ID do item (`T7.2`) aponta a `skill_fonte` no YAML: abra a mecânica, na seção do subpasso com o mesmo ID, e EXECUTE o subpasso.
2. Grave a evidência com o NOME PADRÃO que o gate procura (`persona-<slug>.md`, `modelagem-<lote>.md`, `validacao-<lote>.md`, `demanda-<lote>.md`, `PARADA-N.md`, `OFERTAS/<slug>/pesquisa/obra-de-arte.md`, `OFERTAS/<slug>/pesquisa/checagem-mecanismo.md`, linhas `gate.py … Tn` / `Verificador Haiku Pn` no ESTADO).
3. Rode o gate de novo. Repita até exit 0. Só então avança / apresenta a Parada / libera construção.
4. **Não edite o YAML nem o script para "passar".** Só se a evidência estiver comprovadamente mal especificada — e então registre a mudança no ESTADO.
5. Evidência que o gate não consegue julgar (o arquivo existe mas está vazio de substância) → Verificador Haiku (seção 4).
6. Item que o dono quer pular: só por escrito dele → linha no ESTADO `DD/MM — dono pediu dispensar T7.2; T7.2 ABERTO-POR-DECISÃO` → o gate imprime `[DONO]`.

## 4 · Verificador Haiku (obrigatório em cada Parada — regra na orquestradora)
Subagente `model: haiku`. Prompt mínimo: o caminho do YAML, a saída de `gate.py --ate <passo>` e a ordem "para cada item OK, abra o arquivo de evidência
e diga SIM/NÃO se o CONTEÚDO cumpre o título do item (não basta o nome existir); liste furos com item, arquivo e o que falta". Furo → fecha antes da Parada.
Registre no ESTADO: `Verificador Haiku P1|P2|P3: DD/MM — n furos, fechados`.

## 6 · Auditoria de fala [decisão do dono 25/09/2026] — ANTES de mandar ao dono qualquer mensagem que cite concepções
Regra em `criacao-low-ticket-mvt` § REGRA DE FALA. Para CADA concepção/ideia/produto citado: (1) tem tag de status? (2) a tag confere com o gate — MINERADA = aparece no Hub/lote; VALIDADA = `gate.py --passo T9 --concepcao <id>`; OBRA = `--passo T11 --oferta <slug>`; LIBERADA = linha "Parada 3 LIBERADA <slug>" + `--ate T12`? (3) há HIPÓTESE apresentada como oferta (tabela com formato/dor/preço, "dá pra vender", recomendação de construir)? Qualquer resposta ruim = reescreva: troque a lista por PLANO DE MINERAÇÃO ou rebaixe a tag ao status real. Só então envie.

## 5 · Auditar uma rodada inteira (nova, antiga ou herdada)
1. `--ate T15` (ou até o passo em que a rodada está) com `--so-falta` → é a lista de dívida.
2. Agrupe por passo; a dívida mais ANTIGA (menor T) é a primeira a fechar — passo aberto trava todos os seguintes (regra do ROTEADOR).
3. Rodada antiga sem ROTEADOR: grave-o primeiro (modo R da orquestradora), depois audite.
4. Cole no ESTADO a saída resumida (`RESULTADO` + FALTA) com data e a ordem de fechamento; marque os passos afetados como ABERTO.
5. Pivô detectado (`T7.13`, `T9.8`, `T10.4` em oferta com Obra): a Obra fica `PAUSADA`; a concepção re-entra em T7 (regra do PIVÔ na orquestradora).
