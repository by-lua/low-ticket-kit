---
name: auditar-entregaveis-oferta
description: "Audita uma oferta low ticket: o que a página de vendas promete × o que existe escrito (TEXTO) × o que está publicado na área de membros (painel). Atualiza o registro vivo de entregáveis, aponta o que falta e permite gerar/redigir o que falta. Use quando disser: 'olha a área de membros e faz o que falta', 'audita a entrega da oferta', 'o que já está pronto', 'promete × entregue'."
---

# Auditar entregáveis de uma oferta

Responde sempre a mesma pergunta, sem depender de memória:
**o que a página promete × o que existe escrito × o que o cliente realmente vê logado no painel.**

Complementa (não substitui) o `PANORAMA.md` da raiz e o `STATUS.md` da oferta.
O `STATUS.md` da oferta continua sendo a fonte de verdade de fase/pendências.

## Regra da casa

Toda oferta tem UM registro vivo de entregáveis: `produto/ENTREGAVEIS.yaml`.
Ele é gerado por este script e nunca editado à mão. Fonte: contagem real de arquivos
no painel + presença do texto. Se o YAML não existe, o script cria a partir do
`produto/MANIFESTO-ENTREGAVEIS.md` (ou dos `produto/TEXTO/*.md`).

**Tabela limpa NÃO é auditoria limpa.** O veredito da oferta é o conjunto
**tabela + `BURAÇOS INVISÍVEIS`**; com qualquer buraco A–H aberto, a resposta é "falta X",
nunca "está completo". O `--registrar` agora carrega a contagem de buracos na própria linha
"Falta" e o resumo imprime `buracos: N` — leia essa linha antes de responder à dona.
Caso real (Jiu-Jitsu 20/10): o Upsell 1 estava à venda desde 16/10 e **fora do manifesto**;
a tabela dizia `15 itens · VAZIO 0 · 0 páginas a gerar` e o STATUS fechava com "Falta: nada".
O buraco A existia, mas perdido numa seção abaixo — 4 dias de item vendido com 3 de 18
páginas passaram como "tudo entregue".

**O MANIFESTO lista TODO produto vendido** — principal, bônus, order bumps (inclusive os
que viraram bônus), combo e upsells. Bump/upsell novo cadastrado na gateway entra no
MANIFESTO no mesmo dia: item vendido fora do manifesto é invisível pro audit e vira
"completo" falso por omissão (Jiu-Jitsu 14/10: 4 bumps à venda com zero registro).

Sem esse arquivo, qualquer conversa sobre "o que falta" vira reconferência manual e
gera resposta errada (já aconteceu: manifesto dizia "vazio" com 30 imagens no ar).

**O manifesto também DECLARA o que o script não tem como adivinhar** (medido 15/10/2026,
Tarot + Cigano) — sem estas 3 linhas o audit mente:

| Declaração no `MANIFESTO-ENTREGAVEIS.md` | Para quê |
|---|---|
| `> **Painel desta auditoria:** \`../mapa-do-tarot/site/painel\`` | oferta que mora no painel de OUTRA (o Cigano vive no painel do Tarot). Sem ela o script lê a cópia parada em `site/painel/` e diz que está tudo VAZIO |
| `> **Escopo desta auditoria:** ... Fora: \`principal\`, \`completo\`` | quando duas ofertas dividem o mesmo `/painel`: o card do outro não é "vendido sem registro". `x-*` = família, `x` = item |
| `> **Texto desta auditoria:** \`item\` = \`caminho\`` (`—` = não escrito) | oferta que guarda o manuscrito fora de `produto/TEXTO/` (Tarot: um arquivo único + um `TEXTO.md` por bump; Cigano: o pacote de páginas). Sem ela a coluna `txt` diz "ausente" no que já está escrito |

A contagem é de **página** (chave = número + nome do arquivo), então `.jpg` + `.webp` da
mesma página valem 1 — era o que fazia 46 páginas saírem como 92 e escondia página faltando.
Os 3 formatos estão detalhados em `references/como-ler-o-painel.md`.

## Rodar

```bash
python3 ~/.claude/skills/auditar-entregaveis-oferta/scripts/audita.py <OFERTAS/<slug>>
```

Saída: tabela item × prometido × escrito × publicado × falta × situação, e o
`produto/ENTREGAVEIS.yaml` reescrito. Opções: `--json` (machine), `--so-gap`.

## Situações

| Situação | Significado |
|---|---|
| `VAZIO` | nada no painel — buraco crítico se já vendido |
| `MVP` | tem páginas publicadas, abaixo do completo |
| `COMPLETO` | publicadas as páginas prometidas |
| `AGREGADOR` | item sem página própria (combo que "lê os 3 itens", upsell, **ferramenta/web app publicado no `/painel`** que não é módulo de páginas) — **não é VAZIO**, é o card que vende o pacote; entra na tabela com `0` páginas |
| `SOBRA_PAGINA` | painel tem páginas a mais que a promessa (informativo) |

## Checagem: instrução SEM a folha de fazer (dona, 18/10/2026)

Atividade que pede material físico/imprimível (caça-palavra, labirinto, sequência, recibo,
cartões para recortar, pôster, tabuleiro, ligar-colunas, relógio, rostos) precisa de **duas
páginas**: a que ensina (`pagina-NNN`) **e** a que a pessoa imprime e faz (`pagina-NNNw`).
Se o texto do card tem "hand the person…", "show a grid…", "lay out coins…", "show picture
cards…", "poster…" e **não existe a `w` correspondente**, o item está incompleto mesmo com o
número de páginas batendo — o cliente paga por um exercício que não consegue aplicar.
Caso real: GeriNeuro US 18/10 ("Printable Word Search" só com a ilustração, sem a grade).

Ao auditar: grep dos gatilhos no `produto/texto/` × existência de `conteudo/<sku>/pagina-NNNw.*`;
reportar como buraco **"instrução sem folha"** (não é VAZIO — tem páginas). Regra e gerador em
`criacao-low-ticket-mvt/references/PAGINAS-DE-ATIVIDADE.md`.

### Como o script conta (importante antes de discutir número)

`pub` = **quantos arquivos de página existem** em `site/painel/conteudo/<módulo>/` —
é o mesmo número que o menu (`sync-menu.sh`) e o PDF (`modulo-pdf.mjs`) usam. Três
armadilhas que já incursionaram:

| Armadilha | Sintoma | Como o script trata |
|---|---|---|
| `pdf/` tem um jpg por página | contagem **dobra** (93 vira 186) | `pdf/` e `original/` são ignorados |
| duas famílias de numeração (`pagina-01-x` e `pagina-001-y`) | contagem por número **subestima** (93 vira 87) — mas são páginas diferentes, todas no ar | conta arquivos e imprime `AVISO numeração ambígua` |
| página servida em **jpg + webp** (Tarot: `pagina-01-capa.jpg` e `.webp` são a MESMA página) | contagem **dobra** (46 vira 92) — situação continua correta, só o número infla | imprime `AVISO numeração ambígua`; leia `pub` como arquivos, não páginas (92 = 46 páginas) |
| página no disco e fora do menu | script diz que existe, cliente não vê | não é do script: rode `produto/PROMPTS/sync-menu.sh` da oferta |
| página no disco e **fora do git** (untracked) | `pub` conta como "publicado", mas o deploy não tem o arquivo — cliente não vê | checagem **E** acusa (gerar ≠ publicar); commit do menu **e** do conteúdo |
| manifesto chama o bump de "Bônus N (OB)" | bump VAZIO sai COMPLETO contando as páginas do **bônus** (Jiu-Jitsu 14/10: auditoria dizia 11/11 e o cliente via "em atualização") | item com OB/bump no tipo só casa pasta `bump*`/`ob-*`, nunca `bonus-N`; bumps numerados no manifesto (`Order bump 1..6`) |
| o diretório de texto se chama `texto/` (minúsculo) | `texto: ausente` em todos os itens (Linux é case-sensitive) | aceita `TEXTO/` ou `texto/`; arquivo de bump casa `bump-N*.md` |
| **duas pastas `ob-*` disputam o mesmo assunto** (`ob-seguranca` × `ob-manual-seguranca`) | item de bump casa a pasta ERRADA e sai **VAZIO com as páginas no ar** (Eletrotecnia 15/10: `+60 Mapas de Segurança Industrial` dizia 0/60 e tinha 10 publicadas; a pasta do bump novo vinha antes na ordem alfabética) | entre as pastas candidatas, escolhe a **mais específica** (proporção das palavras do nome da pasta que aparecem no item) |
| a coluna **Estado** do MANIFESTO tem número | promessa **inventada** e item VAZIO por falso alarme (Eletrotecnia 15/10: "publicado **12**/10" → Calculadora com 12 páginas a gerar; "lê os **4** SKUs" → Kit com 4) | o fallback só lê colunas de contagem; célula com data (`\d{1,2}/\d{1,2}`) ou texto de Estado (publicado/agregador/lê os N SKUs) é ignorada — item sem número vira `AGREGADOR`, não `VAZIO` |

Quando o gate no ar (nº de págs do PDF) e o `pub` do script divergirem, a fonte da
verdade é o **PDF baixado**, não o script.

## Checagens A–H — os buracos que a contagem não enxerga

Contar página nunca acha o buraco que mais custa dinheiro. A mesma rodada compara o
`/painel` (`index.html`: `MODULES` + `BUMPS`) com o MANIFESTO, com o servidor
(`site/server/index.mjs`) e **com o git** (o que foi deployado), e imprime a seção
`BURAÇOS INVISÍVEIS`:

| | O que procura | Já pegou |
|---|---|---|
| **A · SEM-MANIFESTO** | card no `/painel` que não casa com nenhum item do MANIFESTO — **item vendido fora de todo registro** | Jiu-Jitsu: 4 bumps à venda desde 10/10 invisíveis pro audit; Eletrotecnia: 4 cards fora |
| **B · QUEBRADA / ÓRFÃ** | `pages[]` do card × arquivo no disco: aponta pra arquivo que não existe, ou está publicado e fora do menu (cliente nunca vê). A órfã cobre **também o principal** (menu por `PRINCIPAL_CATEGORIES`, não por `pages:`) | Eletrotecnia 16/10: página nova do principal commitada e fora do menu — o publicador ligava só bônus/bumps |
| **C · SEM-ENTREGA** | sku do card que o servidor **nem cita** — webhook responde `no-known-product` e o comprador fica sem acesso | Eletrotecnia: `ob-kit-eletricista` |
| **D · ENTREGA-SÓ** | sku que o webhook concede e que nenhum card/item cobre — comprador antigo com acesso que ninguém vê | Jiu-Jitsu: `combo-bumps` legado |
| **E · NÃO-DEPLOYADA** | arquivo de página **no disco/painel mas fora do git** (untracked, não ignorado) — **gerar ≠ publicar**: contava como "publicado" e nunca subia | Eletrotecnia 16/10: o publicador só fazia `git add painel/index.html`; a página nova ficava no disco e o menu no ar apontava pra webp inexistente |
| **F · MENU-CORROMPIDO** | `pages:` do card com `[object Object]` ou o mesmo `.map()` repetido — lista de páginas cruzada mais de uma vez | Eletrotecnia 16/10: `wire-bump-pages.py` não-idempotente colou `.map` a cada publicação → `conteudo/<mod>/[object Object].webp`, **4 módulos quebrados no ar** (leitor sem imagem, PDF 404) |
| **G · INSTRUÇÃO≠EXERCÍCIO** | card que **promete** uma folha imprimível (`hand the person a … worksheet`, `printable`, `maze`, `word search`) e **não existe a página do exercício** no painel — item `COMPLETO` na contagem que não entrega **o que fazer**, só o "como fazer" | GeriNeuro US 18/10/2026: V5 "Attention & Everyday Thinking" (*+ printable worksheets*) tem **8 cards `Printable …`** e **nenhuma folha** — ver §G abaixo |
| **H · PARCIAL FALSO** | card com `partial:true` num módulo **já completo** (`publicado >= prometido`): o leitor mostra "conteúdo inicial · mais em breve" e fecha com "Em atualização" num módulo inteiro que o cliente pagou | Jiu-Jitsu 20/10/2026: `bonus-1..4` com 5/4 páginas e `partial:true` desde o MVP — badge de "em construção" nos 4 bônus completos |

As 8 saem também no `ENTREGAVEIS.yaml` (seção `buracos:`) e no bloco que o
`--registrar` escreve no STATUS. **Nenhum achado é "deixa pra depois": ou vira item no
MANIFESTO, ou vira correção no servidor, ou é registrado como decisão da dona.**

Como não gerar falso positivo (medido em 15/10 — alarme que não é buraco mata a skill):
- **jpg + webp da mesma página** (Tarot): comparação de órfã é **sem extensão**.
- **Card sem `pages:`** não é card de conteúdo desta oferta (link/cross-sell) → A/B/C pulam.
- **A liberação pode passar por outro mapa**: no Tarot os bônus e o `completo` saem do
  `COMPLETO_OFFERS` (offer code), não do `PRODUCT_SKUS` — a C procura o sku **em qualquer
  lugar** do servidor.
- **Painel hospedando outra oferta**: declare no MANIFESTO
  `> **Escopo desta auditoria:** ... Fora: \`cigano-\*\` (oferta própria).`
  (Tarot hospeda o Cigano; sem a linha são 16 alarmes falsos).
- **E durante geração**: a fila grava no disco e publica em lote — enquanto ela roda,
  E acusa a página recém-gerada ainda não commitada. Isso é a **verdade** (não subiu); some
  no próximo `pos-fila`. Não é falso positivo, é o sinal chegando cedo.
- **E sem git**: `site/` que não é repositório git devolve `E · SEM-CHECAGEM` (não some a
  checagem em silêncio).

### G · INSTRUÇÃO ≠ EXERCÍCIO — o card promete a folha e não entrega a folha (conteúdo)

Medido GeriNeuro US, 18/10/2026 (a dona viu antes do audit: *"só vejo o idoso apontando, cadê
a página do exercício pra imprimir?"*).

Um item pode estar **`COMPLETO` na contagem** e mesmo assim **não entregar o exercício**. O
card traz "Objective / Instruction / What the older adult does" + uma foto, e a instrução diz
*"Hand the person a word search worksheet with 8 object names hidden in a letter grid"* — mas a
**folha do caça-palavras não existe**. O comprador recebe o **"como fazer"**, não **"o que
fazer"** (o grid, o labirinto, a sequência, o *spot the difference*). A contagem de página não
vê o buraco: a página do card existe e conta.

**Checagem:** varrer `produto/texto/*.md` + o MANIFESTO por marcadores de folha imprimível —
`worksheet`, `printable`, `maze`, `word search`, `spot the difference`, `sequence worksheet`,
`Hand the person`, `pairs with a printable` — e confirmar que existe a **página do exercício**
correspondente no painel (não só o card de instrução). Ex.: GeriNeuro V5 (subtítulo *"+ printable
worksheets"*) tem **8 cards `Printable …`** e nenhuma folha.

**Correção — texto primeiro, depois imagem GPT (nunca código; regra da dona 23/10/2026):**
1. Faltou a página `w` no **texto** (`produto/texto/`)? Escrever antes: conteúdo exato + composição +
   gabarito, modelo em `criacao-low-ticket-mvt/references/PAGINAS-DE-ATIVIDADE.md` § "A composição
   nasce no TEXTO". Ficha só com explicação = texto incompleto.
2. Gerar a `w` no GPT, 1 por mensagem (`gpt-imagem-playwright` § "Páginas de ATIVIDADE"), conferir o
   conteúdo exato contra o gabarito, publicar como página nova logo depois do card (checagens B/E valem).
**Proibido HTML/SVG/Pillow/HTML→PDF** — reprovado ("psicodélico"). `gera-worksheet.py`,
`gera-atividades.py`, `gera-printables.py` estão obsoletos: só inventário, não gerador. Página `w`
feita por código já publicada conta como **pendente**. Título deixa claro o que é: `WORKSHEET` +
nome do exercício, e a página é **só o exercício** (sem a explicação, que fica no card).

## Publicação — gerar ≠ publicar (medido Eletrotecnia, 16/10/2026)

A contagem mede **o disco**. O cliente vê o que está **commitado e deployado**. Lições que
já custaram entrega (as checagens B/E/F pegam — mas evite-as na origem):

1. **Publicar = ligar TODOS os módulos, não só alguns.** Cada módulo tem seu menu em lugar
   diferente: o **principal** sai de `PRINCIPAL_CATEGORIES` (por categoria — no padrão da
   Eletrotecnia, reconstruído do disco pelo `sync-menu.sh`); **bônus** de `BONUSn_PAGES`;
   **bumps** de `pages:[...]` no card. Um publicador que liga só bônus/bumps (o
   `wire-bump-pages.py` da Eletrotecnia) deixa a página nova do **principal** commitada e
   **fora do menu** — órfã, o cliente nunca vê (achado 16/10/2026). Publique rodando TODOS os
   wires, ou a checagem **B** acusa.
2. **O publicador commita MENU + CONTEÚDO.** Se o script de publicação faz só
   `git add painel/index.html`, toda página NOVA (untracked) fica no disco e **nunca sobe**.
   Regra: `git add painel/index.html painel/conteudo` e gate por `git diff --cached`
   (não `git diff -- painel/index.html`).
3. **O "wire" (ligar páginas no menu) tem que ser idempotente.** Um gerador que casa só
   `pages:[...]` e deixa o `.map(...)` anterior colado adiciona um `.map` a cada rodada; o
   segundo `.map` recebe objetos e produz `[object Object].webp`. A regex deve **consumir a
   run inteira** do sufixo e reescrever UMA só. Teste: rodar `--apply` duas vezes e conferir
   que não muda (idempotente).
4. **A fila longa roda como serviço, não solta.** Geração de centenas de páginas leva horas:
   um processo destacado com `setsid` morre no fim do turno (o harness mata o grupo órfão).
   Suba como serviço de usuário (`systemd-run --user ... -p Restart=on-failure`, com
   `Linger=yes`) e controle por `systemctl --user status`.
5. **O vigia de publicação não pode expirar antes da geração.** Um "espera e publica" com
   limite de tempo menor que a geração morre sem publicar (Eletrotecnia 16/10: o vigia de
   10h morreu às 20:17 e os bumps só fecharam depois — a entrega saiu na mão). Ou o limite
   cobre a geração inteira, ou o supervisor **republica periodicamente** enquanto a fila
   não termina.
6. **Gate logo após o push mente.** O Coolify leva ~1 min de rollout: durante ele o gate
   devolve 500/504/404 falsos. **Rodar o gate de novo depois do deploy assentar** antes de
   declarar OK ou FALHA.

## Retomada — o motivo da skill existir

Toda entrega **trava** no meio: os tokens do GPT acabam, a cota de upload bloqueia, a
conta cai, a sessão morre. A doña volta depois e diz "olha a área de membros e faz o que
faltou". O estado da produção precisa sobreviver a isso — é o `ENTREGAVEIS.yaml`.

```bash
python3 ~/.claude/skills/auditar-entregaveis-oferta/scripts/audita.py OFERTAS/<slug> --retomar
```

Imprime, por item, a **próxima faixa exata** de páginas a produzir (número inicial e
final), o arquivo de texto que manda, o destino no painel e as referências visuais.
Não é plano — é a próxima mensagem pra executar.

Fluxo canônico de retomada:

1. Página de vendas → listar tudo que é prometido (todo item, todo bônus, todo bump).
2. **Texto integral primeiro** — `produto/TEXTO/completo/`. Sem texto, sem imagem.
3. Módulos → capas → referências visuais → geração (GPT, 1 página por mensagem).
4. Publicar no painel → rodar o script de novo → o YAML vira o novo estado.
5. Recomeça no passo 1 com o próximo item.

## Passo a passo COMPLETO — "olha a área de membros e faz o que falta"

A dona fala uma frase e o resto é com a skill. Ninguém repete passo a passo: **os 8
passos abaixo são o trabalho inteiro**, do diagnóstico à prova no ar.

1. **Diagnóstico** — `audita.py OFERTAS/<slug>` (tabela) e `--retomar` (próxima faixa
   exata de páginas). Ler junto o `MANIFESTO-ENTREGAVEIS.md` e `produto/texto/INDICE.md`.
2. **Feche os `BURAÇOS INVISÍVEIS` (A–H) ANTES de gerar imagem** — um card fora do
   manifesto ou um sku sem entrega no servidor anula tudo que você produzir depois.
3. **Texto** (`texto: ausente`) — escrever seguindo o arquivo vizinho como modelo
   (mesma estrutura, mesmo nº de cards, mesma voz). Sem texto não existe imagem.
4. **Imagem** — 1 página por mensagem no GPT (`gpt-imagem-playwright`), com 2–3 páginas
   nossas já aprovadas como referência + tokens do `DESIGN-SYSTEM.md`. Padrão de entrega:
   `01-capa` + `NN-cards-XX-YY` (2 cards por folha), **webp ≤ 146 KB**, mesmo visual do módulo vizinho.
5. **Publicar — menu E conteúdo** — jogar em `site/painel/conteudo/<sku>/`, **listar as
   páginas novas no `pages[]` do card** no `site/painel/index.html` e tirar o `soon:true`
   (wire **idempotente**: rodar 2× tem que dar o mesmo). Depois **commitar os dois**:
   `git add painel/index.html painel/conteudo` — página publicada e fora do `pages[]` o
   cliente não vê (checagem B), e página nova **fora do git** também não sobe no deploy
   (checagem E). Só entra página com **webp E `pdf/<nome>.jpg`**. Commitar só o
   `index.html` é o bug clássico: menu no ar apontando pra arquivo que não existe no servidor.
6. **Recontar** — `audita.py OFERTAS/<slug>` de novo: tem que sair `COMPLETO` e com a
   seção de buracos (A–H) limpa. O `ENTREGAVEIS.yaml` é regravado sozinho.
7. **Deploy + gate** — commit só do que é seu (`git add <caminho>`), push, esperar o
   Coolify (~1 min) e **provar no ar**:
   `node scripts/check-download-pdf.mjs <url> <e-mail-de-teste>` tem que sair **OK** em
   todo módulo com conteúdo (404 só em card "em atualização"). **O gate roda de novo DEPOIS
   do rollout assentar** — durante o deploy ele devolve 500/504/404 falsos. Mudou
   preço/SKU/webhook → conferir também o checkout público e o clique do card bloqueado.
8. **Registrar (Fase 3)** — `audita.py OFERTAS/<slug> --registrar` (escreve no STATUS da
   oferta **e** na linha da raiz) + entrada datada no `STATUS.md` da oferta (números, o
   que mudou, o que ficou pendente) + `PANORAMA.md` se o maior buraco mudou.
   O `--registrar` **não sobrescreve mais a data do topo** de uma entrada antiga (isso
   criava "2026-10-20 (incidente de 16/10)"): ele insere uma linha nova
   `**Atualizado em:** <hoje> — auditoria de entregáveis`, idempotente no mesmo dia, e
   preserva o texto que estava lá.

Rodou os 8, a resposta pra "olha e faz o que falta" está **terminada** — não "quase".

Ordem de prioridade dentro dos passos 3 e 4:

1. **Item `VAZIO` que já é vendido** → capa + 10 páginas primeiro (regra MVP 40%).
2. **`MVP` incompleto** → subir até o prometido, em ordem de página.
3. **Texto faltando** (`texto: ausente`) → escrever/redigir o texto antes de gerar imagem
   (ordem da casa: texto → visual → produção). Nunca gerar imagem sem texto.
4. **`AGREGADOR` (combo)** → não gera nada próprio; confere que os SKUs dele estão
   mapeados no servidor (checagens C e D).

Regras que continuam valendo (ver CLAUDE.md da oferta):
- Todo entregável é **imagem**, nunca PDF cru.
- Texto primeiro; MVP 40% antes de completo.
- Manda o texto pro GPT com referência visual (2–3 páginas nossas) + identidade do
  `DESIGN-SYSTEM.md`.
- Promessa fora da realidade (norma estrangeira, "contrate profissional") se adapta
  ao Brasil.

- **Nunca afirmar "está no ar" sem a saída do `check-download-pdf.mjs` e o clique real.**

## Rodar em todas as ofertas

```bash
for d in OFERTAS/*/; do echo "== $d"; python3 ~/.claude/skills/auditar-entregaveis-oferta/scripts/audita.py "$d" --so-gap; done
```

Sem MANIFESTO-ENTREGAVEIS.md a oferta sai como `AUDIT-SKIP` — aí não existe registro e
qualquer resposta sobre "o que falta" é chute. **Criar o manifesto antes** (a partir dos
`produto/TEXTO/*.md` + o que o `/painel` já mostra) e rodar de novo.

## Referências

- `references/como-ler-o-painel.md` — como o script conta as páginas (nomes de pasta do painel).
- `references/exemplo-eletrotecnia.md` — exemplo real de YAML gerado.

## Gate visual: ficha sem imagem = não entregue (regra da dona, 22/10/2026)
Ao auditar o painel, abrir contact sheet de cada módulo. Ficha de instrução com ícone abstrato (arco-íris, círculos, pontos) em caixa vazia, sem imagem da cena, conta como **pendente**, não como entregue. Ficha montada em código com foto colada também é pendente. Correção (ficha inteira no GPT com a nossa como referência): `criacao-low-ticket-mvt/references/PAGINAS-DE-ATIVIDADE.md` › "Ficha de instrução SEMPRE com imagem ilustrativa".
