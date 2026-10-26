---
name: criativo-ads
description: Porta de entrada ÚNICA e ORQUESTRADORA de criativo de anúncio (Meta/TikTok) — vídeo, estático ou carrossel. Anda a TRILHA DO CRIATIVO passo a passo — Kevones (3 campanhas 1-1-10, mistura imagem/vídeo 7+3 / 5+5 / 6+4) → Rodrigo como base + nossos formatos (UGC, expert, demonstrativo, caixa de perguntas, expert respondendo, frase de impacto…) → roteiro gancho/desenvolvimento/CTA → mecânica — e roteia para as duas mecânicas, `criativo-ads-imagem` (estático/carrossel) e `criativo-ads-video-orq` (vídeo), com `modelagem-escalados` como opção extra de formatos. Use sempre que o usuário pedir criativo, anúncio, ad, leva de criativos, hook, variação, novo ângulo, criativo de vídeo/estático/carrossel, UGC, expert, demonstrativo, "estilo Rodrigo", leva 1-3-9 / 1-1-10, ou mencionar Kevones, bolhas, ângulos, gatilhos.
---

# criativo-ads

> **⚠️ CRIATIVO É O 80/20 DA OPERAÇÃO (regra da dona, 24/10/2026).** Entre tudo que se faz numa
> oferta low ticket, o criativo é o que mais pesa no resultado — raso aqui custa mais caro que
> em qualquer outra etapa. **Nenhum vídeo é "pronto" só por ter áudio+legenda+QA de boca OK** —
> passa pelo ⛔ GATE DE VÍDEO COMPLETO (hook com dor real → corpo que desenvolve MECANISMO, não só
> repete benefício → CTA sem corte seco → trilha de fundo → variedade de cena), em
> `criativo-ads-video-orq` item 11. Raso = script com só o gancho resumido do plano copiado
> direto (ver `plano-video-ganho-nao-e-roteiro-completo`). Checar o gate ANTES de declarar
> qualquer vídeo entregue, não depois.
>
> **Toda vez que for criativo novo, carrega as 3 coisas juntas, sempre (regra da dona,
> 24/10/2026):** (1) **estúdio/estratégia** — esta skill (persona, matriz, formato); (2)
> **casting** — `pesquisa/PERSONA-E-ANGULOS.md` da oferta (quem é a persona, personagens já
> fichados); (3) **mecânica** — `criativo-ads-video-orq` se for vídeo, `criativo-ads-imagem` se for imagem. Nunca carregar só a skill-porta e deixar a mecânica pra
> depois — é isso que produz vídeo com script mas sem produção completa (gate acima).
>
## 🧭 TRILHA DO CRIATIVO — um caminho só, passo a passo (regra da dona, 26/10/2026)

Pedir criativo = andar ESTA trilha, nessa ordem. Cada passo tem UMA fonte; não se inventa
regra no caminho e não se pula passo. (Antes do passo 1: `low-ticket-abrir` da oferta + GATE 0/0.1/0.2 abaixo.)

| Passo | Decide | Fonte única |
|---|---|---|
| **1 · Kevones — quantidade e mistura** | 3 campanhas 1-1-10 (com mais verba: 10× 1-1-3); diversidade de formato e narrativa; mistura **imagem/vídeo por campanha (regra da dona): C1 70/30 (7+3), C2 50/50 (5+5), C3 60/40 (6+4)**; cada peça com um **papel de consciência** declarado; dor que vende em todas; nenhuma dor repete dentro da campanha | **`references/METODO-KEVONES-LEVA.md`** + `references/kevones-criativo.md` |
| **2 · Rodrigo (base) + nossos formatos — papel de cada peça** | o método do Rodrigo vale INTEIRO como base (UGC dando a experiência, expert, gancho→desenvolvimento→CTA, cenários, regras de corte); por cima entram os formatos que a dona já fixou (caixa de perguntas, expert respondendo em imagem e vídeo, demonstrativo, frase de impacto, imagem orgânica mostrando o material). A biblioteca de escalados é **opção extra** pra diversificar. Nenhum papel repete na campanha | **`references/METODO-RODRIGO-SLOTS.md`** (Rodrigo + matriz única + 10 slots); extras em `modelagem-escalados` |
| **3 · Plano em texto** | tabela peça a peça (modo + dor + formato + papel de consciência) → `gate-plano-leva.py` → OK da dona | `references/RECEITA-LEVA-PONTA-A-PONTA.md` |
| **4 · Roteiro / texto de cada peça** | gancho → desenvolvimento (mecanismo) → CTA, pela estrutura do MODO | `references/ROTEIRO-POR-FORMATO.md` |
| **5a · Imagem** | o tipo dita visual e conteúdo; texto do GPT, páginas reais, 4:5, margens, preço | **skill `criativo-ads-imagem`** (GUIA DE IMAGEM + prompt orgânico + carrossel + gates) → `gpt-imagem-playwright`; formato da biblioteca: `modelagem-escalados` |
| **5b · Vídeo** | o modo dita roteiro e cenas; **a edição é sempre a mesma**, em qualquer modo | **skill `criativo-ads-video-orq`**: GUIA DE VÍDEO (`estilos-de-video.md`) + **`EDICAO-PADRAO.md`** (corte, legenda, velocidade, trilha, card CTA, QA) |
| **6 · Entrega** | `anuncio.md` por peça, gates finais, registrar no STATUS e em `_memoria/planos-criativos.md` | `references/texto-anuncio-por-angulo.md`, `low-ticket-salvar` |

**Quem manda em quê:** Kevones = quantidade e mistura. **Rodrigo = a base, considerada inteira** (papéis,
estrutura do texto gancho → desenvolvimento → CTA, como a pessoa conta a experiência); um complementa o
outro. Os formatos que a dona já fixou (caixa de perguntas, expert respondendo em imagem e em vídeo,
demonstrativo, frase de impacto, imagem animada…) somam-se aos dele. Biblioteca de escalados = opções a mais. **Visual = sempre o nosso:** imagem
orgânica de iPhone, texto de Stories, material impresso + digital, nunca mockup — onde Rodrigo usa
mockup ("clássica"), a nossa versão é a orgânica (com preço, se for peça de preço).

**Modo ≠ edição.** UGC, expert e demonstrativo são modos (o que se diz e o que aparece). A edição
(corte por frase, split, legenda KaraokeV2, velocidade 1.0, trilha, card CTA) é uma camada só e vale pra
todos — ninguém precisa pedir "edita no estilo do demonstrativo". Mesma lógica na imagem: o tipo muda,
as regras de texto/página/formato do GUIA DE IMAGEM não.

**Quando duas regras desta skill se contradizem, vale a mais recente (data da regra da dona)**, e a
correção vai pro arquivo-fonte do passo (GUIA DE IMAGEM, GUIA DE VÍDEO, EDICAO-PADRAO) — nunca só no histórico.
**Exceção a regra da dona só com ordem dela, com data e citação** — agente não escreve exceção pra
justificar a própria peça (caso Tarot AR, 25/10: "peça 9 sem texto").

**Checagem de repetição:** antes de fechar a leva, relistar peças feitas (modo + dor + formato) e
confirmar que nenhuma repete modo+estrutura dentro da mesma campanha.

> **🎯 "Faz os criativos da oferta X" (leva inteira, ponta a ponta):** siga
> `references/RECEITA-LEVA-PONTA-A-PONTA.md` na ordem — persona com dado → material/DESIGN-SYSTEM → plano →
> gates → peça a peça (ugly iPhone, digital + impresso 3-4 folhas + 1-2 aparelhos, nada repete, texto de
> Stories, preço do plano mais barato, REF-FORMATO anexada) → gerar (`scripts/gerar-imagem-gpt.sh`) → mostrar à
> dona → gravar. Molde de prompt: `references/PROMPT-ESTATICO-ORGANICO.md`. Exemplo vivo: Atlas AR (23/10/2026).

> **⛔ GATE DE PERSONA MECÂNICO (dona, 23/10/2026 — erro que não se repete):** antes de página, criativo,
> peça do funil ou preço, rodar `python3 ~/.claude/skills/criacao-low-ticket-mvt/scripts/gate-persona.py OFERTAS/<slug>`. **BLOQUEADO = não começa**; completa o
> `pesquisa/PERSONA-E-ANGULOS.md` no modelo `MODELOS/_MODELO-PERSONA-E-ANGULOS.md` (MERCADO na Biblioteca ≥5 anúncios,
> QUEM COMPRA DE VERDADE, dores com contagem+data, RECORTES com "por que está na oferta"). Casos: Elétrica estudou o
> estudante (comprador = eletricista na obra); Jiu usou "faixa branca/azul" (só vendeu quando tirou da página).
> **Pesquisa que alimenta (lição Atlas 23/10):** `criacao-low-ticket-mvt/references/PESQUISA-PADRAO-OFERTA.md` —
> Biblioteca 5 palavras + hashtag por idioma, YouTube/TikTok/Trends com contagem. O gate também cobra TERMOS DE
> BUSCA (nome do produto quase nunca é termo: "atlas" = 0 no Trends AR), unidade da peça, cena da dor,
> NARRATIVAS QUE RODAM (dias no ar) e ÂNCORA DE PREÇO.
>
> **⛔ GATES DA LEVA (dona, 23/10/2026):**
> 1. Plano em texto → `python3 ~/.claude/skills/criativo-ads/scripts/gate-plano-leva.py OFERTAS/<slug>` antes de
>    mostrar pra dona; com `--producao` antes de gerar qualquer peça (exige `- [x] OK da dona`). Cobra: persona
>    LIBERADA, **DESIGN-SYSTEM.md** (cor/fonte — sem ele a cor sai errada), 3 formatos e ≥2 vídeos por campanha,
>    imagem ≥ vídeo, alternar 7+3/6+4, zero "PDF"/"mockup", ângulo existe no banco, personagens com voz,
>    orçamento, 4:5, gravação de tela antes de vídeo.
> 2. **Preço no criativo = SEMPRE o plano mais barato** quando a página tem 2 planos (linha
>    `**Preço no criativo:**` no plano; popup/saída/bump não contam).
> 3. **Cada peça:** takes de vídeo + imagens que entram (capa + páginas) em `CRIATIVO-N/selecionados/`, separados
>    de `intermediarios/`. **Nada repete:** PC, celular, tablet e folha solta mostram cada um uma página
>    DIFERENTE (capa + 3-5 páginas distintas). Prova: `python3 ~/.claude/skills/criativo-ads/scripts/gate-pecas-criativo.py <pasta do criativo>`
>    antes de gerar a cena no GPT/Flow.

## ⛔ GATE 0 — leia a oferta ANTES de propor qualquer ângulo [regra da dona 10/10/2026]

> **A ordem canônica completa** (persona → dor → demanda orgânica → oferta → página → criativo →
> peças do funil, com as contraprovas e a regra de dor-fora-do-escopo) está em
> `~/.claude/skills/criacao-low-ticket-mvt/references/ESTRUTURA-DE-PENSAMENTO.md`. Este Gate é a
> versão dela na porta do criativo.

**Não existe criativo sem ler a oferta.** Ângulo inventado a partir do nome da pasta é
o buraco mais caro deste fluxo: produz peça que promete outra coisa e só descobre isso
depois de gastar a verba.

**Ordem obrigatória, nessa sequência:**

1. `OFERTAS/<slug>/CLAUDE.md` + `STATUS.md`
2. `OFERTAS/<slug>/pesquisa/PERSONA-E-ANGULOS.md` — **a obra de arte da oferta**: quem vendemos,
   as dores medidas, **as dores fora do escopo do produto (matéria-prima de bump/upsell)** e o
   banco de ângulos com o estado de cada um (feito/na fila/descartado+por quê). É o arquivo que
   responde "minha oferta é essa, o que eu tenho que atacar?". Se não existir na oferta, ele é
   **obrigatório criar** a partir de `MINERACAO/` + `pesquisa/` antes de continuar.
3. `OFERTAS/<slug>/produto/MANIFESTO-ENTREGAVEIS.md` — **o que o cliente recebe**
4. **A página de vendas** (`pagina/` ou `site/`): headline, `<h1>`, meta description
5. `criativos/` — inventário das peças que já existem e o que **já foi descartado e por quê**

**Antes de escrever qualquer briefing, Grave e responda em voz alta:**

```
O QUE VENDEMOS: <o produto, em uma frase, no que o cliente realmente recebe>
NÃO É:         <o que este criativo NÃO pode parecer que seja>
PERSONA:       <quem é, e a dor que ele tem hoje>
DOR ATACADA:   <dor, e onde ela foi medida>
```

Sem essas quatro linhas, **para**. Se `NÃO É` não estiver claro, o briefing está errado.

**Contraprova obrigatória:** pegue o ângulo e responda *"se o cliente comprar isso, o
que ele recebe na mão?"*. Se a resposta não for um item do `MANIFESTO-ENTREGAVEIS.md`,
o ângulo está errado — mesmo que o ângulo pareça bom.

**Rubrica fixa + objeção medida (regra nova, 20/10/2026):** antes de montar a matriz dor×persona,
rodar `criacao-low-ticket-mvt/references/4-alavancas.md` (nota 0-10 Transformação/Probabilidade/
Tempo/Esforço na NOSSA oferta, aponta a mais fraca) e, quando houver concorrente modelado,
`criacao-low-ticket-mvt/references/virar-o-lead.md` (simulação 1ª pessoa por etapa do funil dele —
a objeção real vira matéria-prima do gancho, nunca objeção chutada). Cada gancho da leva cita qual
alavanca ataca.

**Contraprova de alinhamento com a landing (mesma regra, vista pelo lado do dado):** o
anúncio promete uma coisa e a página entrega outra? A pessoa clica, chega e **"não tem nada
a ver com aquilo"** — e sai sem comprar. Sinais: **CTR alto + IC zerado ou muito baixo**. Isso
é **desalinhamento criativo↔página**, não criativo ruim: CTR ruim é problema do anúncio, IC
ruim com CTR bom é problema da **promessa**.

Pergunta que fecha: **"o que o anúncio promete é literalmente o que o `<h1>` da página
promete?"** Se o anúncio fala em "facilitar o orçamento" e a página vende "+150 mapas
visuais de eletricidade e eletrotécnica", o anúncio está vendendo outro produto — mesmo que
CTR alto, ele só entrega clique caro.

⚠️ **Erro que já aconteceu (10/10/2026, Mapas Visuais Eletrotecnia):** ângulo "serviço
igual, preço diferente" e "cobra mais quem entende o diagrama" foram gerados a partir
do nome do nicho, sem ler a oferta. A oferta **não é serviço** — é um sistema visual de
consulta. As duas peças (CRIATIVO-9 e CRIATIVO-10) foram descartadas na hora, depois de
já estarem prontas. Não repita.

Quem delega **também** cumpre este gate antes de escrever o briefing do pane —
o orquestrador junta a referência e a leitura da oferta (ver `PROMPT-PADRAO-PANE.md`,
bloco `[OFERTA-PRIMEIRO]`).

## ⛔ GATE 0.1 — SEM REFERÊNCIA REAL NÃO EXISTE CRIATIVO [regra da dona 10/10/2026]

**Nenhum criativo começa sem antes material de verdade da oferta na mão.** Este gate vem
logo depois do Gate 0 e vale tanto pra peça feita aqui quanto pra pane delegado.

O que tem que estar **anexado** (arquivo, não descrição) antes de escrever o primeiro prompt:

| Peça | Referência mínima obrigatória |
|---|---|
| Estático | capa do produto + **2 ou 3 páginas reais** do entregável |
| Carrossel | idem, mais a página de cada card do carrossel |
| Vídeo | idem + **frames de tela do produto** gravados (`MATERIAL-ENTREGAVEL/gravacoes-tela/`) |

De onde sai a referência, nesta ordem:

1. `produto/MVP/<item>/` — as páginas aprovadas da peça.
2. `site/painel/conteudo/<item>/` — o que já está publicado pra o cliente ver.
3. `produto/MOCKUPS-NOSSOS/` — mockup nosso (nunca o do concorrente cru).
4. `site/` — página de vendas no ar (banner/capa).

Checklist de gate (responde tudo **sim** ou não começa):

- [ ] Abri os arquivos de referência e **vi** as páginas (não só li o nome do arquivo).
- [ ] As imagens anexadas são **da nossa oferta**, não do concorrente.
- [ ] Pelo menos uma referência é **página de dentro** do entregável, não só a capa.
- [ ] O prompt leva **identidade visual explícita** (hex + fonte) — senão o GPT copia o
      estilo da referência (`gpt-clona-referencia-prompt`).
- [ ] No briefing está escrito **qual arquivo** é a referência de cada card/cena.

Sem referência o GPT inventa uma página que a oferta não tem — e o criativo vende
material que o cliente nunca vai receber. É o modo de erro que mais caro já custou aqui.

> **Quem delega também cumpre este gate.** Se você é o orquestrador e vai spawnar um
> pane de criativo: junte você mesmo as imagens/paths de referência e **cite os caminhos no
> briefing**. Não mande o pane "descobrir a referência" — delegar cego é o mesmo defeito.

## ⛔ GATE 0.2 — LEVA EM VOLUME: PERSONA EM DIA + BIBLIOTECA ANTES [regra da dona 23/10/2026]

Antes de planejar qualquer leva (ex.: 30 do teste 3× 1-1-10):
1. **Persona atualizada e conferida:** `PERSONA-E-ANGULOS.md` da oferta bate com a página no ar
   (o que vende / não é / preços / bônus) e as dores têm medida. Resumo da oferta errado = para aqui.
2a. **Começa pelo anunciante MODELADO (a página da Biblioteca que a dona passou):** é a oferta que já
   vende. Listar todos os anúncios dele e, pra cada **narrativa**, contar em quantos anúncios ela se repete
   e há quantos dias roda. **A narrativa que roda há mais tempo e mais se repete é a que vende** — e entre as que vendem, escolher a que dá pra **modelar com o que a gente TEM** (sem rosto proprietário, prova inventada ou material que a oferta não tem; Rodrigo, estudo `CONHECIMENTO/ESTUDOS/2026-10-26-delta-criativo-rodrigo.md`) (ex.: Atlas —
   "recém-formado começando como personal / no consultório" repetida em vários anúncios) → vira peça da
   leva em imagem E em vídeo. Dissecar como foi feito: visual, ângulo, gancho, sequência, personagem.
   Ela também diz **quem compra de verdade** (entra no PERSONA-E-ANGULOS, seção QUEM COMPRA/MERCADO).
   Registro: `OFERTAS/<slug>/pesquisa/BIBLIOTECA-<data>.md` (anúncio · narrativa · repetições · dias · formato).
2. **Biblioteca de Anúncios + demanda orgânica = o LOOP ÚNICO de
   `criacao-low-ticket-mvt/references/PESQUISA-PADRAO-OFERTA.md`**, mesma régua, nunca uma pesquisa
   à parte, nunca resumido aqui de novo — ler aquele arquivo inteiro antes de buscar. Rodar o loop
   com a dor da PERSONA ampla ("iniciante trava em quê"), nunca só o ângulo já sugerido na conversa
   — pesquisa estreita confirma o que já se queria achar, não descobre dor nova (lição 24/10/2026,
   Mapa do Tarot BR). Registra em `OFERTAS/<slug>/pesquisa/BIBLIOTECA-AMPLIADA-<data>.md` +
   `DEMANDA-ORGANICA-<data>.md` e usa como referência real da leva (Gate 0.1). Mecânica de browser:
   `mvt-minerar` (falso-zero, perfis, headed).
3b. **Primeiro o que JÁ vence pra gente:** olha os vencedores das nossas ofertas (mesmo idioma ou outro,
   mesmo nicho ou outro ângulo — ex.: Atlas AR modela a oferta BR) e entende POR QUE funcionou. Muitas
   vezes copiar e adaptar o vencedor já é uma peça da leva (já é um teste); o planejamento vai pras outras.
4. **Plano em texto primeiro, dona aprova, só então produz:** plano da leva peça a peça + ficha de
   cada personagem (expert: quem é, gênero, idade, visual, ambiente, voz — casado com o produto e o
   país). Nada é gerado antes do OK.
3. **Leva com variedade máxima:** formatos e ângulos o mais variados possível; nenhum tipo se
   repete dentro da mesma campanha. Variar em 3 eixos, em vídeo E imagem:
   - **origem do gancho:** corte de vídeo do YouTube · cena orgânica estilo TikTok · o material
     direto na tela;
   - **função da peça:** mostra o material · ataca a dor/ângulo · **quebra de objeção** ·
     **narrativa/história** · combinação delas;
   - **formato** (vídeo/estático/carrossel e seus tipos).
   Porquê: a pessoa vê o ecossistema inteiro — um compra na quebra de objeção, outro (pra quem a
   objeção não faz sentido) compra numa peça específica. Cada peça é ponto de contato (§21).

## Texto do anúncio acompanha toda peça — regra da dona (03/10/2026)

Todo criativo de vídeo, imagem ou carrossel deve ser entregue com `anuncio.md`
na mesma pasta do arquivo final. Inclua: ângulo, persona/dor, texto principal,
título/headline, descrição curta e CTA sugerido. Escreva cada campo para o
ângulo daquela peça; não repita uma copy genérica na leva. Adapte texto e voz
ao mercado: BR = pt-BR, PT = pt-PT, ES = espanhol do mercado. Leia
`references/texto-anuncio-por-angulo.md` antes de escrever ou revisar a copy.
O arquivo de mídia sozinho não conclui a entrega. Ao criar uma nova leva,
confira também as peças existentes citadas pelo usuário e acrescente a copy
que estiver faltando, sem alterar suas mídias.

Uma porta só. **Esta skill decide O QUE fazer; as outras sabem COMO produzir.**
A estratégia mora aqui e em `references/kevones-criativo.md`. As skills de
mecânica não repetem regra de estratégia. Se alguma divergir desta, vale esta.


## Mapa do pacote

| Camada | Skill / arquivo |
|---|---|
| Orquestradora (esta) | TRILHA + gates; método em `references/METODO-KEVONES-LEVA.md`, `references/METODO-RODRIGO-SLOTS.md`, `references/kevones-criativo.md`, `references/ROTEIRO-POR-FORMATO.md`, `references/RECEITA-LEVA-PONTA-A-PONTA.md`, `references/DOUTRINA-ORGANICO.md`, `references/texto-anuncio-por-angulo.md` |
| Mecânica de imagem | `criativo-ads-imagem` (GUIA DE IMAGEM, prompt orgânico, carrossel, gates de imagem) → `gpt-imagem-playwright` |
| Mecânica de vídeo | `criativo-ads-video-orq` (GUIA DE VÍDEO, EDICAO-PADRAO, geração no Flow) → `flow-video-playwright`, `narracao-hub-tts`, `get-brolls` |
| Opção extra | `modelagem-escalados` (formatos da biblioteca: print de WhatsApp, notícia, story nativo, antes/depois…) |
| Depois | `metaads-kevones` (tráfego), `low-ticket-salvar` (registrar) |
| Estrutura de pensamento | `criacao-low-ticket-mvt/references/ESTRUTURA-DE-PENSAMENTO.md` (persona → dor → demanda → oferta → página → criativo → funil) |

Histórico do fluxo antigo: `references/HISTORICO-ORQ.md`. Backup completo pré-remodelagem: `~/.claude/skills/_backup-criativo-2026-10-26/`.
