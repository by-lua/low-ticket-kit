---
name: metaads-kevones
description: Metodologia de tráfego pago do Kevones (Seleta Comunidade) — quando decidir estrutura de campanha, teste/otimização, escala (Andrômeda 2026), empilhamento de BidCap, contenção de bloqueios, escala por horário, públicos de base, ou modelar oferta low ticket/infoproduto usando os gatilhos e ângulos do Kevones. Puxada por criacao-low-ticket-mvt e criativo-ads para a etapa de tráfego.
---

# metaads-kevones

Acesso e mapa ao curso do Kevones (Seleta Comunidade, id=15) atualizados em **2026-10-06**.
Conteúdo transcrito em texto corrido, fora do diretório de skills (é curso pago, fica em
Documentos, não versionado):

```
~/Documentos/TRAMPO/PROJETOS/WORKING/PROJETOS - INTERNOS/SKILL-KEVONES/transcricoes/
```

## Checklist de veredito — rodar ANTES de qualquer decisão de campanha

Isso é pra mim (Claude) aplicar sozinho, sem esperar a dona perguntar. Toda vez que ela mostrar
uma campanha, pedir "analisa minha operação" ou eu for sugerir subir/matar/variar algo, passo
pelas 4 perguntas abaixo primeiro — elas são os 4 erros reais que já custaram caro nesta conta
(diagnosticado 18/10/2026, Mapa do Tarot BR). Se uma bater, **eu digo isso de cara, em voz
direta** ("você está errando aqui: X. Faz Y."), não deixo enterrado em regra genérica.

1. **O orçamento de teste está proporcional ao ticket DELA, não ao do Kevones?**
   Ticket dela costuma ser R$17-27 (ou equivalente em US$/€). Orçamento de teste correto =
   **~1x o ticket mais baixo da régua** (R$15-20), nunca o R$30-50/R$100 fixo dos vídeos — esses
   são calibrados pro ticket de R$47+ dele. Orçamento alto demais pro ticket baixo = o próximo
   item (§2) quase sempre acontece. — `DECISOES.md` §1/§10.
2. **Um anúncio vendeu "empatado" (CPA perto do ticket) — a reação foi matar pelo CPA bruto?**
   **Nunca mata só pelo CPA quando vendeu.** Checa IC: IC barato + volume → mantém ligado. Só
   mata se IC caro **e** sem volume. "Vendeu empatado" é o ticket baixo funcionando, não sinal de
   fracasso — e matar um vencedor por pânico de gasto foi a causa raiz real desta conta
   (orçamento desproporcional fazia o gasto parecer alarmante antes da janela de 48h/7d fechar).
   — `DECISOES.md` §2/§7.
3. **Teste de variação (1-1-10) está com orçamento cheio por anúncio, ou diluído?**
   10 variações com orçamento total raso (ex.: R$20-30/dia pra 10 anúncios) nunca valida nada —
   morre de fome, não de mau desempenho. Cada variação precisa do orçamento de teste completo
   (item 1), não uma fração. Se não dá pra pagar 10 cheios, testa 3-5 primeiro. — `DECISOES.md` §18.
4. **Tem gap de criativo novo (>2-4 dias sem subir nada) enquanto o vencedor está envelhecendo (14+ dias)?**
   Ritmo mínimo: 3-5 criativos novos a cada 2 dias na montagem, 2-3/semana com volume — mesmo
   quando a matriz atual vai bem (seguro contra fadiga). Gap de criativo + matriz envelhecendo =
   a queda vem sem aviso e sem substituto pronto. — `DECISOES.md` §7/§8.

Essas 4 perguntas vêm antes do resto da skill porque são as que mais se repetem e mais custam —
qualquer regra nova que virar causa raiz confirmada entra aqui também, não só no corpo do
`DECISOES.md`.

## Rotina diária (o que fazer cada dia, com o Trackeador na mão)

Pedido da dona (18/10/2026): não só regra, um **framework do que fazer hoje**. Isto puxa o
Trackeador (`trackeador campanhas`/`horario`/`kevinho mentoria` — ver skill `adstrackeador`) +
o checklist acima, todo dia.

1. **Todo anúncio novo, dia 0-1 (24h):** não decide nada ainda (§2). Só confere se o funil básico
   está vivo: tem clique, tem LPV. Se **CTR < ~1% e custo por LPV caro (perto do CPA-alvo)** já no
   dia 1, mata — não é cedo demais, é sinal de que não tem futuro (filtro de CTR/LPV, §2).
2. **48h:** decide por anúncio (não campanha inteira). IC barato + volume → mantém mesmo com CPA
   acima do ticket. IC caro + sem volume → mata. Gastou o CPA-alvo sem vender e sem IC → mata.
3. **7 dias:** só continua o que sobreviveu 48h com potencial. 2+ vendas no CPA-alvo → validado,
   isola (checklist item 2: não mata validado pelo CPA bruto depois disso).
4. **Todo dia, independente do que validou ou não:** confere se o ritmo de criativo novo está em
   dia (3-5 a cada 2 dias na montagem, 2-3/semana com volume — checklist item 4). Esse item roda
   em paralelo aos outros 3, nunca para porque "a matriz atual está bem".
5. **Pelo menos 1x/semana:** roda `kevinho mentoria` + `horario` no dashboard de cada oferta —
   fadiga (CPA subindo 14+ dias no mesmo criativo), pico de horário mudando, veredito por
   campanha. Compara com a semana anterior antes de decidir subir volume.

## Estrutura de teste atual (22/10/2026, supera o número antigo do checklist)

Volume mínimo de teste por oferta nova: **30 criativos**, em uma das duas formas (`DECISOES.md`
§21): **3 campanhas 1-1-10** (pouca verba, ~R$100-105 total) ou **10 campanhas 1-1-3** (mais
verba, ~R$300-350/dia). Mix vídeo+estático+carrossel no mesmo conjunto. Decide só depois de 48h,
só pelo IC (≤10% do ticket). Isolamento: 1-1-1 só quando um único criativo indiscutivelmente
mantém o CPA — se mais de um mantém, fica 1-1-N (matar os que ainda geram IC quebra ponto de
contato, pode derrubar até o "vencedor"). Ler §21 inteiro antes de montar teste novo.

## Como usar

1. **Campanha em análise → `references/DECISOES.md` primeiro.** Regras SE→ENTÃO por
   situação (oferta nova, 48h, 7 dias, validou, escalar, horário, CPA subindo, fadiga,
   público de base, ticket baixo, bloqueio). Cada regra tem número, fonte e data. Quando
   fontes divergem, vale a mais recente; a divergência vem marcada com ⚠️. As 32 regras
   de vídeo com id estão em `references/YOUTUBE-REGRAS-NOVAS-2026-10.md`. Seções 13–16 do
   DECISOES são regras do Trackeador (produto novo, pausada, densidade, gargalo), não do Kevones.
2. **Caso contínuo de ticket R$ 24 (set/2026) → `references/ESTUDO-DE-CASO-24-REAIS.md`**:
   linha do tempo, escala por horário, públicos de base, decisões com gatilho.
3. **Índices por tipo** (cada item tem resumo de 2 a 4 linhas e link para a transcrição):
   - `references/INDICE.md`: hub, aponta para os demais e lista o curso com links.
   - `references/INDICE-CURSO-RESUMOS.md`: 112 aulas do curso id=15.
   - `references/INDICE-CALLS.md`: calls e lives do curso.
   - `references/INDICE-CLOSE-FRIENDS.md`: curso Close Friends (id=13).
   - `references/INDICE-YOUTUBE.md`: 165 vídeos e lives do @1kevones.
4. **Só então a transcrição** da aula ou vídeo (pelo link do índice). Mapa auditável:
   `references/mapa-curso.json`.
5. **Metodologia por texto corrido:** `references/METODO-DESTILADO.md` (régua de decisão
   com as mesmas regras, mais o histórico das divergências) e `references/aulas/<modulo>.md`
   (resumo detalhado por módulo).
6. Módulos-chave por situação (curso):
   - **Já tem oferta, não escala** → `05-meta-ads-2026-andromeda` → `08-metodologia-de-escala` → `09-empilhamento-de-bidcap`.
   - **Não sabe se a oferta converte** → `06-sua-oferta-converte`.
   - **Testar e diagnosticar gargalo** → `07-teste-otimizacao-validacao`.
   - **Criar oferta nova / vender em dólar** → `12-lowticket-em-dolar-na-pratica`.
   - **Criativos** → `15-masterclass-criativos-milionarios`.
   - **Bloqueio/restrição no Meta Ads** → `18-masterclass-contencao`.
   - **Iniciante absoluto** → `03-curso-trafego-do-zero`.
   - **Infoproduto do zero** → `04-criando-infoproduto` + `16-desafio-do-infoproduto`.
   - **Gestão de tráfego pra cliente** → `17-curso-agencia-milionaria`.
   - **E-commerce/delivery** → `19-trafego-para-ecommerce`.

## YouTube do Kevones (@1kevones): mais novo que o curso

165 transcrições (vídeos e lives, set/2023 a out/2026). Pasta:
`~/Documentos/TRAMPO/PROJETOS/WORKING/PROJETOS - INTERNOS/SKILL-KEVONES/transcricoes/youtube-1kevones/`
(`videos/`, `lives/`; arquivo `AAAA-MM-DD Título [id].txt`). Análise em `analise/`:
`RELATORIO.md` e `notas-A..E.md` (vídeo a vídeo).

**Leia `references/YOUTUBE-NOVIDADES.md`** para o que só existe no YouTube e o que ele
atualizou em relação ao curso. Quando curso e YouTube divergirem, vale o vídeo mais recente.
Pontos principais:
- escala por horário (set/2026, `bzsllO6ereY`);
- volume de campanhas com ROAS 1,5 (`viLhlrcJPhU`, `Vtjdg86wDxA`);
- públicos de base em campanha própria, exclusão de compradores em 180 dias;
- meta de custo empilhada no lugar de BidCap sozinho;
- estrutura 1-1-3;
- um criativo por dor, método das bolhas;
- empilhamento de order bump, oferta de janela;
- imposto de 2026 e ticket mínimo de R$ 47.

## Estado (18/10/2026)

- **Curso principal (id=15):** 112 aulas mapeadas; 110 com transcrição. **Reconferido 18/10/2026
  aula a aula (login Membriz + diff id a id contra `mapa-curso.json`): 112 = 112, sem aula nova.**
  Exceções confirmadas: aula 164 (sem player no Membriz) e aula 158 (vídeo de 5 s, sem fala). Aula
  332 foi removida do Membriz em 2026-10-02 (texto histórico em `calls-lives/11-aaaaa.md`).
  Resumo por aula: `INDICE-CURSO-RESUMOS.md`.
- **Calls e lives (curso):** 11 arquivos em `transcricoes/calls-lives/`; duas são
  exceções (164 e 332, sem transcrição útil). Índice: `INDICE-CALLS.md`.
- **Close Friends (id=13):** 5 aulas (ids 66, 67, 68, 69, 72) com transcrição. Índice:
  `INDICE-CLOSE-FRIENDS.md`.
- **YouTube @1kevones:** 169 transcrições (163 vídeos + 6 lives), atualizado 23/10/2026.
  Fechados os pendentes de 18/10 (`myAmzdSfkmg`, `hM2qQA1B6NY`) + novo `Fo3EFSn7LeI` (23/10,
  "Você só precisa de 1hr pra ESCALAR" — metodologia completa, `DECISOES.md` §21). Ver
  `YOUTUBE-NOVIDADES.md`.
- **Caso contínuo de set/2026** (`viLhlrcJPhU` 21/09, `bzsllO6ereY` 22/09, `Vtjdg86wDxA`
  29/09): playbook em `ESTUDO-DE-CASO-24-REAIS.md`, regras em `DECISOES.md`.
- **Lacunas de resumo:** 30 vídeos do YouTube têm resumo automático (início da transcrição),
  porque não há nota em `analise/`. Calls e Close Friends também têm resumo automático, não
  revisado linha a linha. Vídeos sem fala (2025-06-19 `JGs4W7rwOnc`, 5 s) ficam sem resumo.
- Versão anterior (ago/2025, ~24 módulos) arquivada em `~/Documentos/1-Pessoal/cursos/SELETA-COMUNIDADE-TRAFEGO/Kevones-ANTIGO-2025-archive/` — **não usar como referência**.

Acesso ao curso e remapeamento: ver `references/LOCAL-ACESSO.md` (arquivo local, não versionado).
