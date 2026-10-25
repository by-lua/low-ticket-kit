---
name: criativo-ads
description: Porta de entrada ÚNICA de criativo de anúncio (Meta/TikTok) — vídeo, imagem estática ou carrossel. Faz a estratégia (briefing, matriz persona × dor/bolha, escolha de formato, quantidade por fase da conta, regras do Kevones 2026) e depois puxa a mecânica certa — `criativo-ads-video-orq` para vídeo, `modelagem-escalados` + `gpt-imagem-playwright` para estático/carrossel, `narracao-hub-tts` para voz. Use sempre que o usuário pedir criativo, anúncio, ad, leva de criativos, hook, variação de criativo, novo ângulo, "criativo de vídeo", "criativo estático", carrossel, banner de anúncio, UGC, modelar um criativo que está escalando, "criativo estilo Rodrigo/Rodrigo Liedson", "leva 1-3-9", "leva de 9 criativos" (mix UGC carro/ambiente normal + expert + imagem clássica/impacto/antes-depois/só-texto), ou mencionar metodologia Kevones de criativo, bolhas, ângulos, gatilhos.
---

> **HUB DESATIVADO (02/10/2026, ordem da usuária):** NinjaBR Hub está SEM COTA e os perfis `hub`/`hubv2`/`hubts` foram removidos (backup em `~/.agent-profiles/_removidos-hub-2026-10-02/`). NÃO use Hub, NÃO rode `hub-livre.sh` (sai com erro), NÃO espere perfil do Hub liberar. Imagem: ChatGPT — se a cota de upload de uma conta acabar, troque de CONTA: `gpt-conta*` ↔ `gpt-conta*`. Vídeo: Google Flow (`flow-video-playwright`).


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
> fichados); (3) **mecânica** — `criativo-ads-video-orq` se for vídeo, `gpt-imagem-playwright` +
> `modelagem-escalados` se for imagem. Nunca carregar só a skill-porta e deixar a mecânica pra
> depois — é isso que produz vídeo com script mas sem produção completa (gate acima).
>
> **Regra dura (dona, 25/10/2026 — texto de peça saiu flutuante sem caixa e formato saiu 9:16
> numa peça 4:5, os dois inventados de memória em vez de copiados da regra escrita):** ninguém
> — orquestrador nem pane — escreve prompt de texto/formato pro GPT de cabeça. Antes de
> escrever QUALQUER prompt de imagem, copia e cola literalmente a definição de texto ("Texto =
> sempre texto de Stories, na fonte nativa do Instagram Stories...") e a proporção ("estático e
> carrossel = 4:5, 1080x1350") mais abaixo nesta skill. Perguntar ao usuário "que estilo você
> quer" quando a resposta já está escrita aqui é o MESMO erro — não é escolha de gosto, é regra
> fixa. Todo brief de pane de imagem cola essas linhas inteiras, não resume nem parafraseia.

## 🧭 FLUXO ÚNICO — do pedido à peça pronta (uma mecânica só, leia de cima a baixo)

Isso existe porque pedir criativo não pode virar "escrevo um roteiro solto e gero
imagem/vídeo sem pensar no resto". É UM mecanismo, com etapas que sempre acontecem
NESSA ordem — nenhuma pulada, nenhuma decidida sozinha sem olhar as outras:

1. **Quanto/quando (Kevones) — decide o volume da leva.** Em que fase a conta está
   (3-5 teste / 1-1-3 validado / rotina semanal), quantas campanhas (1-3-9 ou
   1-1-10), mix vídeo/imagem/carrossel por campanha (`Quantidade pela fase da
   conta` + `references/kevones-criativo.md`).
2. **Quem/o-quê em cada slot (Rodrigo + biblioteca) — decide o PAPEL de cada
   peça.** A tabela de 10 slots (`MATRIZ ÚNICA`) preenchida com dor real do banco
   (`PERSONA-E-ANGULOS.md`) — Rodrigo é o mínimo, não o teto: a biblioteca
   `modelagem-escalados` (103 formatos) entra pra diversificar além dele. Decide
   AQUI, antes de escrever roteiro, porque o formato muda a receita de produção.
3. **O que escrever (`references/ROTEIRO-POR-FORMATO.md`) — decide o ROTEIRO.**
   Página real → GPT → gancho+desenvolvimento+CTA por formato (UGC/expert/
   demonstrativo têm estrutura própria, nunca frase solta). Escreve no idioma que
   você entende, traduz depois.
4. **Como produzir e montar (mecânica) — decide a TÉCNICA.** Vídeo:
   `criativo-ads-video-orq` (E.2b/E.0d — split 70/30, 1 clipe/frase, fade, CTA
   card sem corte seco). Imagem/carrossel: `modelagem-escalados` (doutrina
   orgânico+headline+12 prompts, NUNCA mockup 3D — sempre lâmina real). **Mecânica
   se carrega E se aplica peça por peça, nunca só se cita no briefing** (Fluxo,
   passo 5 abaixo).
5. **Entrega** — `anuncio.md` + onde entra na conta. Tráfego/corte/escala:
   `metaads-kevones`.

As 4 primeiras etapas são camadas de UMA decisão, não 4 métodos pra escolher —
nenhuma peça nasce sem passar pelas 4.

> **🗺️ MAPA DE DECISÃO — qual seção ler, pra cada tipo de pedido (índice, 24/10/2026).** Antes de
> montar QUALQUER peça, ache a linha certa aqui e leia as seções na ordem dada — nenhuma decisão
> de formato/estrutura se toma sem passar por essas seções primeiro. Isso existe porque informação
> certa espalhada sem índice = buraco (caso real: receita E.2b já existia, não foi lida pro
> expert hook — CRIATIVO-02 Atlas, 24/10).
>
> | Pedido | Ler nesta ordem |
> |---|---|
> | "3 campanhas", 1-1-3, 1-1-10, teste em grupos | GATE 0→0.2 → `⭐ TESTE EM GRUPOS` → `🗺️ AS 3 TRILHAS` → `Como montar a matriz 1-1-3` |
> | Qualquer peça de IMAGEM (estático, carrossel, peça de preço, antes/depois) | GATE 0.1 → **`references/tipos-de-imagem.md`** (índice único, qual tipo + checklist) → `modelagem-escalados` → `gpt-imagem-playwright` |
> | Qualquer peça de VÍDEO (demonstrativo, expert, UGC, 1-3-9, caixa de perguntas) | GATE 0.1 → **`references/ROTEIRO-POR-FORMATO.md`** (como ESCREVER o roteiro: página→GPT→gancho/desenvolvimento/CTA por formato) → `criativo-ads-video-orq/references/estilos-de-video.md` (qual estilo+checklist) → E.2b/E.0d (edição, sempre, qualquer formato) |
> | "Criativo estilo Rodrigo" / leva 1-3-9 | seção `"Criativo estilo Rodrigo"` abaixo (3 tipos + catálogo de cor/cenário) → **`references/ROTEIRO-POR-FORMATO.md`** (escrever o script) → `estilos-de-video.md` linha "1-3-9" |
> | Reaproveitar formato que já escala (biblioteca) | `modelagem-escalados` (103 formatos) ou tabela de 16 vídeos escalados em `criativo-ads-video-orq` (busca ANTES de inventar corte) |
> | Vídeo "mesa real" (imagem→Flow, sem gravação de tela) | `criativo-ads-video-orq` §E.0c (catálogo de takes A-O) |
>
> **Checagem de repetição (regra da dona, 24/10/2026):** antes de fechar a leva, relistar as peças
> já feitas (tipo+ângulo+formato) e confirmar que nenhuma repete tipo+estrutura dentro da mesma
> campanha — ver `Dentro da MESMA campanha, varia o tipo` mais abaixo.

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
   e há quantos dias roda. **A narrativa que roda há mais tempo e mais se repete é a que vende** (ex.: Atlas —
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

> **Regras fixas da dona (29/09/2026):**
> - **Antes de qualquer criativo, carregar as skills:** esta, `criativo-ads-video-orq`
>   (edição, legenda, Modo E, gates), `get-brolls` (b-roll) e `narracao-hub-tts` (voz).
>   Todo brief de pane de criativo manda ler as quatro ANTES de mexer em arquivo.
> - **Narração/voz off = SEMPRE `narracao-hub-tts`** (API NinjaVoice do Hub: sem browser,
>   sem login, sem cota; liberada pela dona). `languageCode` do mercado (`pt-BR`, `pt-PT`…).
>   Mapa do Tarot PT usa a voz Daniela `9L8v6Oy5x46GlKUxRg6H`. O mp3/wav vai pra
>   `intermediarios/` do criativo. Não usar MiniMax nem outro TTS sem pedido.
> - **Criativo novo = do zero, material cru:** roteiro → locução → b-roll NOVO (`get-brolls`)
>   → tela do entregável gravada agora → montagem. Nunca reaproveitar criativo já montado
>   trocando só áudio e legenda. Um criativo por mercado, em `criativos/<MERCADO>/`.
> - **Legenda:** só a KaraokeV2 canônica (ver `criativo-ads-video-orq`); a "fininha" é reprovada.
>
> **Regras da dona (05/10/2026, leva ES Mapa del Tarot):**
> - **Gancho ≤ 2 frases curtas**, depois já fala do material MOSTRANDO o material.
> - **Várias gravações do entregável = cada criativo usa as melhores cenas de TODAS**, em cortes
>   curtos casando com a fala (nunca 1-2 gravações inteiras).
> - Modelo de gancho que funciona: "Acha que a carta X é só sobre Y? Olha esse material."
> - **B-roll: o pane escolhe sozinho** (Pexels/Pixabay, origem no `credits.md`), sem parar pra
>   aprovação de prévia; a dona revisa no vídeo final.
> - Detalhe e gate de legenda sobreposta: `criativo-ads-video-orq` E.2b ("Lições da leva ES").

> **Regras da dona (11/10/2026 — o texto da peça de imagem é do GPT, nunca overlay de código):**
> - **Estático e carrossel: o TEXTO é escrito pelo GPT DENTRO da foto.** Overlay de código
>   com faixa/barra/bloco de cor atrás é **reprovado** — o texto do GPT sai com cara de legenda
>   de Story (o que o feed premia); overlay sai "perfeito demais", cara de anúncio, e derruba o CPM.
>   Dona, ao ver o lote do Jiu-Jitsu com o texto em faixa: *"os de imagem o texto já sai pelo gpt"*.
>   No prompt: texto exato, **uma linha só e sem aspas duplas** (o `inserttext` trunca e o modelo
>   volta perguntando o texto), pedindo **flutuante, sem nenhum bloco/barra/caixa de cor atrás**, com
>   margem de ~12% no topo e ~15% embaixo e nada cortado na borda.
> - **Ortografia é QA bloqueador, não ajuste:** o gerador erra acento com frequência
>   (`VOCE`, `NAO`, `decisao`). Conferir palavra por palavra e **regenerar** o que saiu torto.
> - **A página do produto que aparece na arte é o arquivo real** — conferir lado a lado com a
>   referência (já saiu capa com produto de outra oferta assim, e passou por todo QA automático).
> - **Vídeo NÃO entra nessa regra:** legenda karaokê no Remotion, sempre. São dois caminhos distintos.

> **Regra da dona (25/10/2026 — peça documentada mas nunca gerada, Mapa del Tarot AR):** um pane
> escreveu `anuncio.md` descrevendo a capa de um carrossel ("tarotar-img-8-capa.png... headline X")
> que nunca foi salva em disco — só documentou o planejado, não verificou o resultado. Em outras 2
> peças da mesma leva, o brief pedia explicitamente "+ texto de story" e o pane entregou só a foto
> do material, sem o texto — pulou a parte difícil sob pressão de tempo/escopo.
> - **Antes do handoff, `ls` CADA arquivo citado no próprio `anuncio.md`** — documentar peça sem
>   `ls` confirmando que o arquivo existe no caminho exato é proibido. Arquivo ausente = peça NÃO
>   está pronta, não escrever como se estivesse.
> - **Todo requisito explícito do brief (ex. "+ texto de story", "+ headline") é item de checklist,
>   não detalhe opcional.** Se faltou tempo pra fazer, PARA e reporta o que ficou de fora — nunca
>   entrega menos do que foi pedido sem avisar.
> - **"Texto de story" = texto ESCRITO DENTRO DA FOTO pelo GPT (hook curto, estilo caption de story),
>   nunca a "copy do anúncio" do `anuncio.md`** (essa é a legenda de FORA, que acompanha o post — as
>   duas coisas são diferentes e sempre existem as duas).
> - **PADRÃO, não exceção: toda peça estática de imagem leva texto/gancho dentro da foto.** Não é algo
>   que só vale quando o brief escreve "+ texto de story" explicitamente — isso é óbvio, é como criativo
>   de imagem funciona (ver [[texto-estatico-imagem-nunca-overlay]]). Única exceção é quando o plano diz
>   explicitamente "só páginas" / sem gancho (ex. peça 9 do Mapa del Tarot AR, carrossel limpo de
>   páginas reais). Reincidência real (Mapa del Tarot AR, peça 5, 25/10/2026): pane escreveu copy no
>   `anuncio.md`, achou que cumpriu, entregou imagem limpa sem nada escrito na cena. Se a peça é imagem
>   e não está marcada "só páginas", ela SAI com texto na foto — conferir visualmente antes do handoff,
>   nunca só ler se o `anuncio.md` tem seção de copy.
> - Quem recebe o handoff (orquestrador) abre pelo menos 1 imagem de cada peça reportada como
>   "pronta" antes de repassar "feito" pra dona — não confiar só no texto do handoff.

> **Regras da dona (08/10/2026 — capas reprovadas, Jiu-Jitsu/Eletrotecnia):**
> - **Sem "faixa branca e azul" no criativo** — nem em imagem nem em texto de anúncio
>   (`anuncio.md`: texto principal, título, descrição curta). A página do Jiu-Jitsu foi
>   refazida sem o eyebrow "Para faixas brancas e azuis" e foi depois dela que começou a
>   vender; o criativo acompanha a página. O campo interno persona/dor pode seguir
>   citando a faixa — ele não aparece no anúncio. Vale pra peça nova e pra leva nova;
>   anúncio já no ar não é editado.
> - **Capa com cara de "inventada" reprovada** (foto de banco, título pequeno, CTA
>   fraco). Padrão aprovado de low ticket: **`references/capa-referencia-low-ticket-jj.png`**
>   (capa do CRIATIVO-7 do Jiu-Jitsu, aprovada pela dona 08/10) — título grande e
>   direto, a entrega real visível (produto na tela + material espalhado), ambiente
>   orgânico que faz sentido, CTA claro. **Todo briefing de pane de criativo cita
>   esse arquivo como referência de capa/estilo** e repete a regra do carrossel:
>   capa = a **única** arte gerada; os demais cards = **páginas reais do entregável**,
>   uma por card, **sem moldura**, recortadas **do início ao fim** (corta onde
>   precisar, um por um, começo → fim).
> - **Card de página real sem moldura** (borda branca sobre fundo escuro = feio) —
>   recorte livre pra preencher o card; regra completa em `modelagem-escalados`
>   ("Regras que não se negociam", item 12).
> - **Apresentação do entregável varia entre criativos:** pode aparecer impresso
>   (folha/página na mão, na obra), no celular, no notebook, no tablet, dois aparelhos
>   juntos ou um só — misture os formatos de peça a peça. Não repetir sempre as mesmas
>   imagens de entrega; o que importa é mostrar material real, não o mesmo mockup.
> - **Imagem de criativo: referência = CAPA + 2 a 3 PÁGINAS REAIS de entrega, sempre
>   (09/10, Tarô).** Anexar só a capa foi reprovado ("só a capa?" — o produto não
>   aparece na arte). Anexa a capa **e** 2/3 páginas reais do entregável e escreve no
>   prompt que **o modelo escolhe 2 das páginas** pra mostrar na cena — "nem muito,
>   nem pouco". As páginas visíveis na arte são SEMPRE arquivo real do produto; o
>   modelo não desenha página. Detalhe do encaixe e das refs em
>   `modelagem-escalados` (item 13) e a mecânica de anexo em `gpt-imagem-playwright`.
> - **Cor do título não precisa ser branca (09/10, Tarô):** pode ser amarelo, azul,
>   ou a cor que for da **marca** — o que for adequado. O que não vale é título
>   pequeno/fraco (regra 08/10). Na prática: define a paleta do produto (marca) e
>   manda o título nessa cor, com sombra/contorno onde a foto for clara.
> - **Vídeo de leva ABRE com o material de frente (09/10, combinado Jiu-Jitsu +
>   Elétrica):** o 1º beat é a gravação real do produto na tela (tela cheia, com
>   zoom/varredura) e o gancho fala por cima — não abrir com b-roll genérico (de obra,
>   de luta). **Proibido imagem parada com zoom (Ken Burns) como cena de produto em
>   vídeo:** onde usaria PNG estático, usa a gravação de tela real em movimento
>   (zoom/varredura/cortes). B-roll de vídeo continua valendo; imagem parada só em
>   peça de imagem (estático/carrossel), nunca em vídeo. Dona: "não quero imagem
>   parada — tenho gravações de tela aí, usa elas com zoom".
> - **Fonte única de imagem de produto em vídeo = gravações da dona (09/10, regra
>   dura):** o material visual do produto vem SEMPRE das gravações que ela mesma
>   grava e deixa em `criativos/MATERIAL-ENTREGAVEL/gravacoes-tela/` de cada oferta
>   (JJ: `OFERTAS/jiujitsu-sem-forca/criativos/MATERIAL-ENTREGAVEL/gravacoes-tela/` ·
>   Elétrica: `OFERTAS/mapas-visuais-eletrotecnia/criativos/MATERIAL-ENTREGAVEL/gravacoes-tela/`).
>   **Nunca criar/substituir com print, PNG ou imagem gerada** — "sempre vai ser a
>   minha gravação". **Se não encontrar a gravação, PERGUNTE** (volte pro Randolph/
>   orquestrador perguntando onde está) em vez de inventar material. Exceção única:
>   ela pedir explicitamente imagem parada/estática naquele momento.
> - **Imagem do entregável: 2–3 arquivos diferentes, nunca repetir a mesma (09/10):**
>   quando a cena usa imagem do material, usa 2–3 imagens DIFERENTES do produto.
>   Proibido pegar UMA imagem e repetir no celular e de novo na versão impressa.
>   Se só há uma à mão, busque mais (`produto/principal/`, `produto/MVP/`,
>   `MATERIAL-ENTREGAVEL/`); se não achar, pergunte — não duplique.
> - **Prompt de geração NUNCA solto (09/10, reprovou no Tarot):** todo prompt de
>   imagem anexa **2–3 imagens do entregável** (referência do produto real, nas
>   pastas da oferta) e traz a direção EXPLÍCITA: **estilo orgânico** (foto crua /
>   post de verdade, como a capa aprovada do JJ — nada de arte decorada inventada),
>   **título**, **estilo** e **história**. A receita (`modelagem-escalados`) é lida
>   ANTES de gerar — prompt não substitui a receita. Salva o prompt usado em
>   `intermediarios/` (prompt-*.txt) e o GPT **nunca desenha página do produto**:
>   página real entra como arquivo encaixado.
> - **Carrossel =1 arte gerada + páginas reais (09/10):** no carrossel, a **única**
>   imagem gerada é o **card 1 (capa)**; todos os cards seguintes são **páginas
>   reais do entregável**, recortadas full bleed (sem moldura), na sequência do
>   início ao fim, uma depois da outra. "Cortar onde precisar, um por um, do começo
>   ao fim" — e acabou.

## Fluxo

1. **Briefing mínimo.** Produto/oferta, ticket, público, em que fase a conta está
   (sem nada validado / já vende e quer escalar / criativo saturou), se existe
   criativo vencedor, se tem rosto/expert, verba diária. O que não estiver no
   pedido, pergunte numa mensagem só.
2. **Mapa de dores → matriz.** Liste TODAS as funcionalidades/dores que o produto
   resolve. Cada uma vira um ângulo, cada ângulo puxa uma persona. Dentro do
   público validado, cada dor é uma **bolha**. Uma célula = um criativo. Duas
   células com a mesma persona **e** a mesma dor = o mesmo anúncio, refaça.
3. **Formato de cada célula** (tabela abaixo) — **⛔ já escolhendo com a mecânica em
   mente, não só o nome do formato.** Antes de fechar o plano em texto, confira em
   `criativo-ads-video-orq`/`modelagem-escalados` o que aquele formato EXIGE pra
   sair certo (ex.: vídeo demonstrativo exige split 70/30 + 1 clipe/frase; imagem
   exige orgânico-iPhone + digital+impresso, nunca mockup 3D) — um plano que não
   sabe disso sai errado mesmo antes de produzir qualquer arquivo.
4. **Quantidade pela fase da conta** (tabela abaixo). Diga ao usuário em que fase a
   leva entra.
5. **Rotear para a mecânica — carrega E APLICA, nunca só roteia de nome.**
   ⛔ Nunca produzir sem ter aberto a skill de mecânica certa (vídeo:
   `criativo-ads-video-orq` E.2b/E.0d; imagem: `modelagem-escalados`) e checado,
   peça por peça, que o formato (quem aparece, o que a mão mostra — Rodrigo) E a
   técnica de produção (edição/split/fade pro vídeo; orgânico-iPhone/digital+
   impresso pra imagem) foram realmente seguidos — não basta ter "citado" a skill
   no briefing. Ler a regra e não aplicar na hora de montar é o erro mais caro já
   documentado aqui (`concat-cru-ignora-stack-edicao`).
6. **Entregar** com: mídia final e `anuncio.md` específico do ângulo, nome de cada peça, a dor/persona que ela carrega, formato e
   onde entra na conta (campanha nova com público validado; nunca na que já vende).
   Tráfego/corte/escala: `metaads-kevones`.

## Regras de estratégia (Kevones 2026, resumo)

Arquivo completo com fontes: `references/kevones-criativo.md`. Leia antes de
montar leva de variação ou decidir quantidade.

- **Não pode parecer anúncio.** Estrutura de trailer: entretém → problema → solução
  → produto em uso → chamada suave ("o link tá aí"). Orgânico, nada clean de agência.
- **O criativo é a segmentação.** O Meta lê o contexto do anúncio e entrega pra
  bolha certa. Criativo que não nomeia pra quem é = leilão largo, CPM caro.
- **Não fazer variação rasa do vencedor** (gancho, música, voz, tom, cor, headline
  reescrita com a mesma dor). O Meta agrupa como o mesmo anúncio. **Repete o
  formato, troca o conteúdo** (dor/persona/objeção).
- **Um ângulo, três formatos:** a mesma dor vira vídeo → carrossel → estático
  (uma frase). A leva de teste mistura formatos.
- **Remarketing** usa peça de objeção/depoimento/cupom, nunca a mesma do frio.
- **Não minta.** Benefício real do produto; nicho saúde/dinheiro/místico sem
  promessa falsa.

## Qual formato

| Situação | Formato | Mecânica |
|---|---|---|
| Produto cabe numa frase de banner | **estático direto** (produto + o que faz + CTA) | `modelagem-escalados` → `gpt-imagem-playwright` |
| Tem objeção forte ou precisa de prova | **carrossel de objeção** ou **de história** | `modelagem-escalados` (formatos + copy) → `gpt-imagem-playwright` (1 card por imagem) |
| Produto complexo/nichado, precisa demonstrar | **vídeo** TikTok/indicação/demonstrativo | `criativo-ads-video-orq` (Modos A–E) |
| Já existe um vídeo vencedor | vídeo com **hook novo e dor nova** sobre o body (B/B2/C) | `criativo-ads-video-orq` |
| Quer copiar um formato que está escalando | estático da biblioteca de 103 | `modelagem-escalados` (Modo D no vídeo) |
| Entregável digital (PDF/guia/app/ferramenta), em imagem | **carrossel demonstrativo "iPhone cru"** (promessa + mockup → benefícios + garantia/vitalício → ~4 páginas do entregável) | `modelagem-escalados` (`references/carrossel-demonstrativo-iphone.md`) → `gpt-imagem-playwright` |
| Entregável digital (PDF/guia/app) | demonstrativo: b-roll + tela + narração (Modo E) | `criativo-ads-video-orq` + `narracao-hub-tts` + `get-brolls` |
| Entregável digital (PDF/guia/app), SEM gravação de tela disponível (ou pra alternar com a de Modo E) | **demonstrativo "mesa real" por IMAGEM→VÍDEO**: gera foto realista (pessoa+aparelho+páginas reais do entregável) e anima no Flow | `criativo-ads-video-orq` §E.0c + `gpt-imagem-playwright` (imagem) + `mecanica-flow.md` (animação) |

**Tamanho:** estático e carrossel saem em **4:5 (1080×1350)** em todos os cards, por
padrão (regra da dona, 23/10/2026 — antes era 1:1). 9:16 só se o usuário pedir. Vídeo continua
9:16. No carrossel demonstrativo, as páginas do entregável são arquivos reais
encaixados no 4:5; GPT não desenha página do produto.

**Estático = foto orgânica de celular, SEMPRE (dona, 23/10/2026):** todo estático e todo carrossel é cena real
com cara de foto de iPhone, com fundo orgânico que faça sentido pra persona (academia, sala de aula, mesa de estudo,
carro). **Única exceção: fase de impacto estilo Rodrigo** (fundo branco, texto preto/vermelho), que é formato
específico — **fundo branco OU preto** (varia peça a peça; texto preto+vermelho no branco, texto
branco+vermelho no preto; regra da dona, 24/10/2026).

**⛔ Fase de impacto e carrossel tipo 2 (só lâminas) também levam estrutura
gancho→desenvolvimento→CTA, nunca frase solta de curiosidade (regra da dona,
25/10/2026).** Uma frase isolada sem desenvolvimento vira curiosidade vaga, não
intenção de compra (mesmo erro já documentado na regra de "peça de preço" acima
— vale pra TODO texto curto, não só preço):
- **Gancho/headline** — a frase de abertura, o que para o scroll.
- **Desenvolvimento/benefício** — 1 linha que entrega o porquê, o mecanismo ou o
  benefício (nunca pula direto pro CTA sem isso).
- **CTA** — comando curto. **Preço só entra se a peça É de preço** (gate "Peça de
  preço" abaixo); peça de impacto sem preço não força o valor, mas continua
  precisando das 3 partes (gancho+desenvolvimento+CTA), nunca só 1 frase.
- Vale pro carrossel tipo 2 inteiro como sequência: 1º card = gancho, cards do
  meio = desenvolvimento (as lâminas reais fazem esse papel), último card = CTA —
  nunca um carrossel de páginas soltas sem fechamento.

Caixa de perguntas também vale em imagem, e **quem responde é sempre o expert** da leva (nunca o UGC). **Texto = sempre texto de Stories**, na
fonte nativa do Instagram Stories (Classic, sans tipo SF/Helvetica, branco em caixa preta arredondada ou preto em caixa
branca), como se a pessoa tivesse digitado no story. Nunca arte de designer. **Sempre anexar as referências** (cena-modelo
+ capa + páginas reais) no GPT.

**Digital + impresso, SEMPRE (dona, 23/10/2026):** toda imagem com material (estático, foto principal de carrossel,
Henrique, cena de vídeo que mostra o produto) mostra **os dois mundos**: pelo menos 1 aparelho (celular, tablet ou
notebook) **e** folhas impressas soltas. Combinações: celular + impresso · tablet + impresso · celular + tablet +
impresso. Cada aparelho e cada folha com uma página diferente. Nunca só digital, nunca só impresso. Fora da regra:
fase de impacto (só texto) e carrossel tipo 2 (só páginas).

**Peça de preço — 2 tipos, nunca preço sozinho sem produto (regra da dona, 24/10/2026):**
1. **Impacto com produto:** fase de impacto (fundo branco, texto preto/vermelho) onde a frase
   NOMEIA o produto + o valor na mesma peça — nunca só "150 MAPAS · $10.900" solto sem dizer de
   onde é (frase solta sem marca vira curiosidade vaga, não intenção de compra). Ex.: "Atlas
   Visual: 150 mapas de anatomía y ejercicio. $10.900, acceso inmediato."
   Vale também pra ganchos de impacto que NÃO são de preço (tipo #16 "No quieras ser ese
   profesional…"): se a frase é solta sem contexto do produto, idem — adiciona nome do produto +
   valor no fecho pra não ficar só curiosidade sem intenção.
2. **Orgânico + preço:** reaproveita a MESMA composição ugly iPhone já aprovada de outra peça da
   leva (cena, aparelhos, lâminas) e troca só o texto Stories pra incluir o valor — pode ser
   **mais geral** (preço + nome do produto) ou **mais específico** (preço + a dor daquela cena).
   Varia peça a peça, já que a leva tem muitas peças pra testar. Não precisa gerar cena nova: usa
   os arquivos de `selecionados/` de uma peça já pronta como referência e só manda o prompt com o
   texto novo.

**Mix por campanha + carrossel (regra da dona, 23/10/2026):** toda campanha de teste (1-1-10 ou
1-1-3) leva **vídeo + estático + carrossel no mesmo conjunto** (metaads-kevones §21). **Proporção da
leva: 70% imagem / 30% vídeo ou 50/50 — NUNCA 70% vídeo** (dá trabalho demais) (ex.: 10 por
campanha = 6-7 imagens + 3-4 vídeos). **Sem mockup:** imagem = páginas reais do entregável em cena orgânica estilo iPhone, texto
como de story, em **vários aparelhos** (celular, tablet, notebook), nunca só impresso. **Anúncio
nunca fala "PDF"** — vendemos material organizado na área de membros; PDF não é benefício.
**Vibe das imagens (dona 23/10):** todas orgânicas estilo iPhone (derruba CPM), exceto a "fase de
impacto" (fundo branco, texto preto e vermelho). Sem moldura, sem cara de anúncio montado.
**Caixa de perguntas em story:** pergunta na imagem + alguém (de preferência o expert) respondendo
com o material na mão, orgânico.

**⛔ MÉTODO ÚNICO, 3 camadas sempre somadas — nunca escolher 1 e ignorar as outras (erro real
repetido 2x no mesmo dia, 25/10/2026: CT3/CT22 tratados como "demonstrativo OU UGC"; depois peça de
expert falando+cortando pro material sem nenhuma técnica de edição, por tratar "expert fala" como
formato que dispensa a receita).** Detalhe completo + tabela dos 10 slots: seção **🔗 MATRIZ ÚNICA**
mais abaixo. Resumo das 3 camadas, válidas em TODA peça de vídeo com pessoa:
1. **Quantidade/distribuição (Kevones)** — quanto e em que mix.
2. **Formato/papel de cada peça (Rodrigo)** — quem aparece, o que a mão/tela mostra.
3. **Técnica de edição (`criativo-ads-video-orq` E.2b/E.0b)** — split 70/30, 1 clipe por frase, fade
   nas junções, CTA sem corte seco. **É caixa de ferramenta de montagem, não um 4º "formato"** —
   usa SEMPRE, mesmo com expert/UGC falando no gancho. "Tem alguém falando" nunca dispensa isso.

**⛔ TODO UGC mostra o material SEMPRE — nunca pessoa vazia, mãos nuas, sem produto (regra da
dona, 25/10/2026 — achado real: 6/6 peças estáticas da leva Atlas AR não tinham isso, só
mesa/mockup sem rosto).** "UGC com o entregável na mão" não é peça opcional perdida no meio do
texto, é a definição do formato UGC neste portfólio (mesmo padrão do Rodrigo) — **toda** peça
UGC (comprador OU expert) mostra a pessoa **segurando o material**: impresso na mão, OU
tablet/celular "acolchoado como cartão-postal" mostrando a capa, perto do rosto/peito, olhando pra
câmera, como se desse opinião — pose "capa de livro" (ver `criativo-ads-video-orq` catálogo de
takes, letra **N**; mesma pose vale pro estático: capa visível, ou abrindo mostrando 2 páginas).

**⛔ O que vai na tela/mão: CAPA primeiro, página real só se não existir capa (regra da dona,
25/10/2026).** "Capa" aqui é a arte de capa LIMPA do produto (o mockup 3D do livro/produto
sozinho, sem grid de bônus ao redor, sem texto de oferta tipo "+7 BONOS" por cima) — não confundir
com arte de página de vendas/hero (essas costumam vir com grid de bônus e preço, não servem).
Se a oferta não tem capa própria gerada ainda, **só então** usa um print real de uma página do
entregável (área de membros, gravação de tela) como conteúdo da tela. Nunca o inverso (página real
quando a capa existe) nem o mockup-com-grid-de-bônus no lugar da capa simples.
**Nunca** a cena UGC ser só mesa/produto parado sem a pessoa segurando e reagindo — isso deixa de
ser UGC e vira peça de produto. Sem isso a leva perde o gancho de atenção do 1º frame que só
rosto+produto dá. **Checar peça por peça ao fechar o plano da leva**, não só confiar que
"variedade" cobre sozinha.

**Exceção (dona, 25/10/2026): produto "vibe"/não-material (ex.: número mestre, numerologia,
qualquer oferta que não entrega guia/PDF/manual pra segurar) pode usar UGC estilo "entrevista de
rua"** — sem segurar material, porque não tem o que segurar. A regra de SEMPRE segurar vale pro
padrão do portfólio (produto tipo guia/manual/apostila low ticket); quando o entregável não é algo
físico/visual pra mostrar na mão, o formato de entrevista/depoimento solto é válido.

**Safe area:** ou gera 2 imagens (9:16 e 4:5), ou monta a 1ª já
pensando no corte do feed 4:5 (nada importante fora da faixa central).

**⛔ Margem de segurança — TODO formato, sempre (regra da dona, 24/10/2026):** em qualquer
criativo (estático 4:5, Stories 9:16, carrossel, vídeo), nada essencial (texto, rosto, produto,
CTA) fica na faixa de cima (~top 14%) nem na de baixo (~bottom 20%) do quadro, nem muito perto das
bordas laterais — é onde o botão de seguir/curtir/compartilhar, o nome do perfil, a legenda e a
barra de progresso do Story cobrem a imagem. Vale pro texto Stories (já embutido no prompt) e
também pra cena/produto/rosto do vídeo (framing da cena, não deixar personagem cortado perto do
topo/base). Checar em TODA peça antes de fechar.
**Carrossel: mínimo 5 cards (regra da dona, 25/10/2026 — leva Atlas tinha 3, poucos).**
3 cards é raso demais; todo carrossel novo sai com **5 ou mais**, qualquer tipo abaixo.

**Dentro da MESMA campanha, varia o tipo de cada formato** — nunca 3 carrosséis iguais nem 4
vídeos do mesmo estilo. Carrossel, tipos:
1. **Imagem principal + páginas:** card 1 = a arte principal (a que já usamos/validou) e o resto =
   páginas reais do entregável (regra "1 arte gerada + páginas reais" acima).
2. **Só páginas, sem imagem principal:** todos os cards são páginas reais do entregável.
3. **Estilo Henrique:** estático por card — as páginas reais em vários aparelhos (sem mockup), a dor
   que a gente está usando, e card de CTA "mirá por dentro" (ver o produto por dentro).
- Página do entregável é A4 (1:1,414) → recorta **do topo até a altura do 4:5** (≈ 88% de cima),
  full bleed, sem moldura.
Vídeo e estático também variam (método Rodrigo abaixo): UGC com o entregável impresso na mão
mostrando/indicando, **expert reagindo/montando o material** (Flow, personagem casado com país e
nicho), antes/depois, peça com preço × sem preço, e os formatos da biblioteca `modelagem-escalados`
(caixa de perguntas, expert respondendo a caixa de perguntas, print de WhatsApp, notícia etc.).

| Expert com rosto | reels orgânicos → campanha de seguidores → conversão | `criativo-ads-video-orq` + regra em `references/kevones-criativo.md` |
| TikTok Shop / achadinho | — | `tiktok-shop` (orquestradora própria) |
| Banner de checkout / imagens da página | não é criativo de anúncio | `banner-checkout-gpt` / `imagens-pagina-low` |

Mecânica de browser sempre pela skill dela: ChatGPT → `gpt-imagem-playwright`
(perfil livre via `gpt-livre.sh`); vídeo → `hub-video-playwright` (via `hub-livre.sh`).
Nunca tocar o browser sem invocar a skill de mecânica antes.

## Quantidade pela fase da conta

| Fase | Quantas peças | Estrutura na conta |
|---|---|---|
| Oferta nova, nada validado, verba < R$ 1 mil/dia | **3 a 5**, formatos misturados | 1 campanha, 2–3 conjuntos, mesmas peças em todos |
| Público validado, quer achar novo criativo | **3** de dores diferentes | 1 campanha, 1 conjunto (público validado), 3 peças (1-1-3) |
| Já vende, construindo ecossistema | **~3 por semana**, nunca por dia | cada vencedora isolada em campanha 1-1-1 |
| Criativo saturou (CPA subindo em 14 dias) | 1+ de **ângulo novo** | campanha nova, público validado |

Meta de ecossistema: ~10 criativos validados antes de verba forte; 20 dão
constância; ele chega a 40–60. Muito teste ao mesmo tempo derruba o ROI da conta
inteira.

## Como montar a matriz 1-1-3 (regra da dona, 11/10/2026 — vale pra TODA leva)

> *"isso sempre que eu pedi 3 campanhas 1-1-3 é isso pegar o que vende e fazer isso e obviamente
> considerar a análise de persona e oferta e tais tbm"*

**1. A dor que já VENDE entra em TODAS as campanhas — uma peça em cada.** E é sempre a peça mais
forte da campanha (é a que leva a promessa no gancho/título). Campanha nova que não carrega o
ângulo que vende tá betting do zero, e não tem por que.

Variação entre as peças de spine é o **ângulo de ataque**, nunca a dor: volume (78 cartas),
bloco específico (combinações), formato (vídeo / estático / carrossel).

**2. Dentro de uma campanha NUNCA se repete a mesma dor.** As outras N−1 peças pegam dores
diferentes do banco. Mesma persona + mesma dor = o mesmo anúncio pro Meta, que agrupa e não aprende.
Os dois erros são simétricos: repetir dor demais (agrupa) ou ângulo novo demais (tábetando do zero).

Exemplo que virou padrão (Mapa do Tarot BR, 11/10): D1 "são 78 cartas, não vou decorar tudo" é a
espinha (base dos 3 vencedores, CPA R$ 8,55–13,82) e aparece em CT-33, CT-36 e CT-40 — uma em cada
campanha. As outras 6 peças pegam D4, D5, D6, D7, D8.

**3. A matriz sai da análise, não da cabeça.** Antes de escrever a matriz, obrigatoriamente:

| Fonte | O que tira |
|---|---|
| `pesquisa/PERSONA-E-ANGULOS.md` | o banco de dores e ângulos com o estado de cada um |
| `produto/MANIFESTO-ENTREGAVEIS.md` | a contraprova — a peça promete item que existe? |
| `<h1>` da landing | o anúncio promete o que a página promete? |
| `trafego/ANALISES.md` (última entrada) | **qual é a dor que vende** — é daqui que sai a espinha |

Dor sem contagem e data não entra na matriz. Duas peças com a mesma persona e mesma dor = refaça.

Plano modelo: `OFERTAS/mapa-do-tarot/criativos/PLANO-CRIATIVOS-BR-2026-10-11.md`.

## 🗺️ AS 3 TRILHAS DA LEVA — vale pro Rodrigo E pro 1-1-3/1-1-10 do Kevones (reforço 24/10/2026)

Toda leva, qualquer método de campanha, distribui as peças em **3 trilhas** — cada uma com função
própria, nenhuma substitui a outra:

| Trilha | Função | Regra fixa |
|---|---|---|
| **Imagem** | benefício + **entregável real** + preço → variações do que já validou | nunca mockup 3D, sempre lâmina/página real estilo ugly iPhone (`anuncio-sem-mockup-sem-pdf`) |
| **Vídeo** | toca na dor → **desenvolve o mecanismo** → CTA | corpo não pode só repetir a promessa — explica POR QUE funciona (ex.: "não é que você não estudou, é que decorar nome não mostra o movimento"); CTA nunca corta seco: produto parado + seta 1-2s |
| **UGC** | usuário que usou o produto, 1ª pessoa, indicando | selfie segurando o material (carro/casa/cotidiano), sem roteiro de vendedor — é relato |

Isso é o mesmo framework dos 3 tipos do Rodrigo (seção abaixo) e da matriz 1-1-3/1-1-10 do
Kevones — não são métodos concorrentes, é a mesma distribuição vista por duas portas. Ao montar
QUALQUER leva (campanha nova, 1-1-3, 1-1-10, estilo Rodrigo), checar que as 3 trilhas estão
representadas, não só 1 ou 2.

**Erro mais caro da trilha vídeo (CRIATIVO-02 Atlas, 24/10):** hook toca a dor, mas o corpo só
repete o benefício ("com mapa visual você entende") em vez de desenvolver o mecanismo. Hook sem
mecanismo no corpo = criativo incompleto mesmo com script inteiro escrito. Ver
`plano-video-ganho-nao-e-roteiro-completo`.

## ⭐ TESTE EM GRUPOS — a pergunta padrão quando a dona pede "3 campanhas" (11/10/2026)

> *"sempre que eu pedi 3 campanhas 1-1-3 é isso... separar em grupos. E pode até me perguntar:
> quer fazer o teste em grupos assim?"*

**Antes de montar qualquer matriz 1-1-3, pergunte:** *"quer fazer o teste em grupos?"*
Se sim, o agrupamento é por **PREÇO × FORMATO**, não só por dor:

| Campanha | Preço no criativo | Formatos |
|---|---|---|
| **C1** | **com valor** | peça-espinha + 2 formatos diferentes (ex.: vídeo + carrossel + estático) |
| **C2** | **sem valor** | **só vídeos** |
| **C3** | **sem valor** | **só imagens** (1 estático + 2 carrosséis) |

Cada campanha muda **UMA** variável — o que se aprender é da variável, não de peça sorteada.
Dentro de C2/C3 as 3 peças ainda são de **3 dores diferentes**.

**E cada campanha leva uma variação do criativo que JÁ VENDE** (a lógica do copo azul): mesmo
produto, mesma promessa, formato diferente conforme a campanha. **A espinha nunca some da leva.**
Sem ela na C3, a campanha vira 3× o mesmo ângulo e o Meta agrupa.

**Antes de escolher a espinha, abrir o tracker e ler a última entrada de `trafego/ANALISES.md`:**
qual anúncio está vendendo, com quantas vendas, CPA e CTR. Esse é o criativo a replicar — e o que
**não** está vendendo diz o que não repetir. Se a última análise mandar "1-1-3 de imagem com o CT 4,
criativo novo = campanha nova", a espinha é o CT 4.

**⛔ Checagem simétrica, antes de reusar QUALQUER persona/ângulo num plano novo — não só puxar o
que vende, excluir o que já falhou (regra da dona, 25/10/2026):**
1. **Nesta oferta:** abrir o `PERSONA-E-ANGULOS.md` e checar a coluna Estado do banco de ângulos —
   qualquer linha **descartado** fica de fora do plano. A fonte do descarte **não precisa ser
   tráfego pago** — mineração/pesquisa orgânica (YouTube, comentários, Trends, Biblioteca) que já
   mostrou que o recorte não faz sentido pra vender também descarta, mesmo sem `ANALISES.md` ainda
   (oferta nova, sem tráfego rodado). "Teste/minoria" não é "descartado" — mas se você já sabe, por
   fora do arquivo (precedente de portfólio, pesquisa orgânica já feita, feedback da dona), que
   aquele recorte não fecha, **registra o descartado no arquivo primeiro**, com a fonte (que tipo de
   medição, não só "a dona falou"), antes de montar o plano — nunca carrega conhecimento não escrito
   só na cabeça pra próxima sessão perder.
2. **No portfólio:** checar `recorte-precisa-dado-licao-eletrica-jiu` (memória) — recorte de
   "estudante/aprendiz" em vez do comprador real que decide já falhou 2x (Elétrica, Jiu-Jitsu).
   Oferta nova com esse mesmo padrão (estudante vs. profissional formado) entra com o recorte
   formado como principal por padrão, estudante nunca mais que peça de teste residual — a menos
   que a oferta tenha prova real em contrário.

Plano modelo: `OFERTAS/jiujitsu-sem-forca/criativos/PLANO-TESTE-GRUPOS-2026-10-11.md`.

## Acabamento aprovado — Número Mestre AR/LATAM

Para vídeo, leia também `../criativo-ads-video-orq/references/acabamento-natural-audio-cortes.md`: cortes por fala e gesto, repetição do Flow, ruído, volume, música, legenda na timeline final e verificação do master. A referência inclui clareza psicológica: benefício concreto por item, introdução curta e CTA de desejo. **Regra da dona (04/10/2026, reforçada 24/10/2026): no VÍDEO/VO, o fecho (fala e texto na tela) é só o comando curto, sem condição de compra** (garantia, preço, vitalício, termos) **e SEM NOME DO PRODUTO** — nunca "Atlas Visual, mirá por dentro", só "mirá por dentro" / "clica aquí abajo y descubrí". Nome do produto no fecho falado soa mal e é propaganda, não comando. Vale pro VO E pro texto escrito do card CTA final (gate `criativo-ads-video-orq` item 11). Condição de compra fica na página e no `anuncio.md`. **Estático e carrossel podem mostrar garantia/vitalício** (ex.: `modelagem-escalados/references/carrossel-demonstrativo-iphone.md`). Tom do fecho: curiosidade, ex.: "Clica aqui embaixo e descobre como." — ver `criativo-ads-video-orq` e `narracao-hub-tts`. Use estes princípios em novos criativos sem copiar timestamps, alegações ou filtros cegamente.

## "Criativo estilo Rodrigo" / leva 1-3-9 (método Rodrigo Liedson, saga Europa 21/10/2026)

**Nome pra pedir:** "criativo estilo Rodrigo", "leva 1-3-9", "leva de 9 nesse estilo" — qualquer um
chama esta seção. **Continua passando pelo GATE 0/0.1 do topo desta skill**: personagem, cenário,
benefício e preço de cada slot vêm da oferta REAL (`pesquisa/PERSONA-E-ANGULOS.md`,
`produto/MANIFESTO-ENTREGAVEIS.md`, preço real do checkout) — o método dá a FORMA de cada slot (que
estilo, que cor, que cenário), nunca o CONTEÚDO (isso nunca é inventado, é a oferta de verdade).

**⛔ Rodrigo é referência, não teto (regra da dona, 25/10/2026).** O catálogo dele (UGC/
expert/demonstrativo + imagem clássica/impacto/antes-depois) é o MÍNIMO, não o limite. Numa leva
grande (ex. 20-30 peças), a biblioteca `modelagem-escalados` (103 formatos: caixa de perguntas,
print de WhatsApp, notícia, Reclame Aqui etc.) está igualmente disponível — usa ela pra diversificar
além do catálogo Rodrigo, não só repetir os mesmos papéis dele em loop.
**Nunca dobrar o mesmo papel DENTRO da mesma campanha/conjunto de 10 — vale pra qualquer um dos
formatos (UGC, UGC, expert, demonstrativo, caixa de perguntas, qualquer um da biblioteca), não só
UGC.** 1 de cada papel por campanha é o teto; se ia repetir um 2º (ex. 2º UGC), troca a vaga por um
formato que ainda não apareceu nesse conjunto — **demonstrativo é o que mais costuma faltar**, dá
prioridade a ele quando sobrar vaga.

**Regra prática pro par UGC×demonstrativo (dona, 25/10/2026):** se a leva "pediria" 2 UGC, prioriza
**1 UGC em vídeo + 1 demonstrativo em vídeo**, e o 2º UGC vira peça de **imagem** (não vídeo) —
nunca 2 UGC em vídeo no mesmo conjunto. Caixa de perguntas pode ser imagem OU vídeo, conforme a vaga. **Repetir o mesmo papel ENTRE campanhas diferentes é normal**
(1 UGC na C1, 1 UGC na C2, 1 UGC na C3 — isso não é duplicar, é cada campanha tendo seu próprio
conjunto completo). Distribui largo dentro de
cada conjunto: UGC, demonstrativo, expert, caixa de perguntas, e o que mais couber da biblioteca, cada
um puxando sua própria técnica de produção (UGC = Rodrigo pose; demonstrativo = E.0d; estático de
biblioteca = `modelagem-escalados`). **Caixa de perguntas: quem responde é sempre o expert**, nunca
o UGC (regra já fixada acima, reforçada aqui porque é um dos formatos de diversificação).

### 3 tipos de criativo + fórmula gancho-corpo-CTA

Fonte: `MINERACAO/referencia-rodrigoliedson/METODO-RODRIGO-EUROPA-139-SAGA-COMPLETA.md` (4 vídeos,
transcrições completas em `CONHECIMENTO/FONTES-DE-CONHECIMENTO/RODRIGO-LIEDSON/TRANSCRICOES/`).
Técnica de CRIATIVO — a estrutura de campanha/tráfego dele ("1-3-9") **não** entra aqui, segue sempre
`metaads-kevones` (memória `trafego-segue-kevones`); só documentada na referência pra consulta.

**Leva de 9 (mix de formato × cor × função), não 9 iguais — tabela completa de slots em
`METODO-RODRIGO-EUROPA-139-SAGA-COMPLETA.md`. Só 1 peça em 9 mostra preço.**

**2 estilos de VÍDEO, nunca só 1 (correção da dona, 21/10/2026):**
- **UGC comprador comum** — pessoa fala em 1ª pessoa, relato ("isso aconteceu comigo, tal e tal").
- **Estilo "expert"** — personagem com autoridade do nicho (ex.: psicóloga explicando o mecanismo,
  não a compradora comum). Os dois precisam de personagem DIFERENTE um do outro.

**Regra de casamento do personagem (vale pros 2 estilos de vídeo e pro UGC em imagem):** a
pessoa/cena de referência tem que combinar com **(a) o país/mercado de destino do anúncio** e
**(b) o nicho/oferta anunciado** — nunca só "achar imagem bonita no Pinterest"; etnia/contexto da
pessoa tem que fazer sentido pro público daquele país, e o papel dela (comprador × expert) tem que
casar com o que o produto promete.

**Cenário por slot de UGC (correção da dona, 21/10/2026) — 3 cenários diferentes na mesma leva, não repete:**
- **UGC 1 — no carro** (pessoa dirigindo ou dentro do carro parado).
- **UGC 2 — ambiente normal/cotidiano** (casa, dia a dia, nada montado).
- **Expert — ambiente que FAZ SENTIDO com o papel dela** (ex.: psicóloga → consultório/escritório;
  nunca o mesmo cenário genérico do comprador comum — o ambiente é parte da prova de autoridade).
  **2 modos de câmera pro expert, variar entre eles:** (a) tela cheia falando, produto aparece
  depois em corte de tela; (b) **segura o entregável como capa de livro perto do rosto/peito,
  falando olhando pra câmera** (ref. UGC "segura capa", mesma pose do selfie-recomendação —
  `exemplo-criativo-demonstrativo-multipaginas` tem exemplo). O item (b) funciona pro expert E pro
  UGC comprador comum — a diferença é só ambiente+tom, não a pose.
  **Duração do clipe lip-sync define onde o mecanismo mora (24/10/2026):** clipe **8s** (padrão
  Flow i2v) só carrega o HOOK em lip-sync — mecanismo/dor desenvolvidos NÃO cabem falados por ele
  nesse tempo, então o corpo vira material/tela + VO off, cortando do rosto pro produto. Clipe
  **~12s** (se gerado mais longo) pode carregar hook+mecanismo inteiro na própria fala do
  personagem — aí o corte pro material vem só depois, pra CTA/entrega. Não force mecanismo
  inteiro dentro de 8s de lip-sync; é isso que sai raso.

**Estilos de imagem por COR (não é genérico, a cor define o estilo):**
- **"Fase de impacto"** = fundo BRANCO + texto PRETO e VERMELHO.
- **"Clássica"** = fundo PRETO + **imagem do entregável (lâmina real, estilo ugly iPhone — nunca
  mockup 3D limpo)** + headline em cima + subheadline + imagem de novo + **preço** (única peça da
  leva com valor visível). "Mockup" aqui é figura de linguagem do método — na prática é SEMPRE
  página/lâmina real, regra do portfólio (`anuncio-sem-mockup-sem-pdf`).
- **Antes/depois** = puxado direto da Biblioteca de Anúncios (referência real já rodando), não
  gerado do zero sem referência.
- **Original** = depende se a oferta já tem uma — normalmente mockup do produto ou imagem de 1
  benefício + CTA; se a referência já validou um VÍDEO de outra pessoa, modela o vídeo também, não
  só imagem.

**3 tipos (formato), usar os 3 misturados numa leva (não só um):**
1. **Imagem = variação do criativo JÁ validado** (nosso ou do concorrente modelado) — nunca do zero;
   gerador recria "imagem idêntica, só traduz/troca o texto", depois varia fundo + headline.
2. **UGC = pessoa com o produto na mão, falando** — imagem de referência de cena coerente (Pinterest:
   "mulher dirigindo" pra segurar livro no carro, por ex.) + copy curta (até 15s) gerada primeiro em
   PT e só depois traduzida/adaptada (nunca criar direto no idioma de destino que não domina).
3. **Vídeo clássico GANCHO → CORPO → CTA:**
   - Gancho (fórmula reaproveitável): *"A maior pressão não é [X esperado], é [Y real que ninguém
     fala]"* / *"Se você é [público], precisa ver isso"* / *"Veja isso antes de [ação cotidiana do
     nicho]"*.
   - Corpo = nomeia o problema de novo + apresenta a solução **gravando a TELA do entregável por
     dentro** (área de membros/app) — produto bem entregue vira o próprio corpo do criativo, sem
     precisar atuação.
   - CTA = comando curto, sem condição de compra (já é a nossa regra de fecho, seção acima).
   - **O gancho ser expert/UGC falando não isenta o corpo da receita padrão do demonstrativo** —
     `criativo-ads-video-orq` E.2b (1 clipe por frase, split 70/30, timeline inteira a 1.15x, não
     só 4-5 blocos fixos). Ver E.0b lá — buraco real encontrado no Atlas AR, 24/10/2026.

**Regra de corte — nunca corte seco no fim do CTA.** Deixa a pessoa "pensando" com a imagem do
produto parada + seta apontando pra baixo por 1-2s antes de acabar — mantém a decisão/retenção em vez
de cortar na hora do CTA.

**Produção de áudio em lote.** Em vez de gerar um áudio por criativo, cola todas as copies da leva
num texto só, gera UM áudio corrido no TTS, baixa uma vez e corta peça por peça no CapCut — mais
rápido que gerar/baixar/editar criativo por criativo.

**Não desativa criativo no dia 1 por "não vendeu".** Analogia do time de futebol: cada criativo tem
uma função (um sobe nível de consciência, outro fecha a venda) — decisão por CTR (bom a partir de
~2%) + no mínimo 3 dias rodando antes de cortar, nunca corte no 1º dia (reforça o que já está na
seção "Quantidade pela fase da conta" — aqui é o motivo).

## 🔗 MATRIZ ÚNICA — 1-1-10 do Kevones × 1-3-9 do Rodrigo (regra da dona, 25/10/2026)

> *"o 1-1-10 do Kevones tem regras, o 1-3-9 do Rodrigo fala de ângulos, formatos… um complementa o
> outro"* — e na skill não existia a junção. Esta é a junção.

**Divisão de trabalho (3 camadas, sempre juntas):** o **Kevones dá a QUANTIDADE e a DISTRIBUIÇÃO**
(10 criativos por conjunto, 1 conjunto Advantage+ por campanha, 3 campanhas; nenhuma campanha repete
a mesma dor; a dor que vende entra em todas; nada de variação rasa). O **Rodrigo dá o PAPEL de cada
slot** (que formato, que tipo, que cor, que função: UGC, expert, clássica com preço, só-texto,
antes/depois, objeção). E, **em todo slot de vídeo** (1, 2, 3 da tabela abaixo), a **técnica de
edição do demonstrativo** (`criativo-ads-video-orq` E.2b/E.0b — split 70/30, 1 clipe por frase, fade,
CTA sem corte seco) monta o corpo, **independente de quem fala no gancho** (expert/UGC/sem ninguém).
Isso não é um 4º slot — é COMO qualquer um dos 3 slots de vídeo é fisicamente montado.

### Os 10 slots de um conjunto (preenche o 1-1-10 com o repertório do 1-3-9)
| Slot | Formato | Papel | Regra que manda |
|---|---|---|---|
| 1 | vídeo | **expert** — gancho → mecanismo → CTA | corpo desenvolve o mecanismo, não repete a promessa |
| 2 | vídeo | **UGC comprador comum** — 1ª pessoa, material na mão | cenário diferente do expert |
| 3 | vídeo | **demonstrativo** — tela do entregável por dentro | é o mecanismo que segura o corpo |
| 4 | estático | **UGC** — pessoa com o material (capa ou 2 páginas) | mão nua = reprovado |
| 5 | estático | **só texto** — frase de impacto, sem produto | sobe consciência, não vende sozinha |
| 6 | estático | **original** — 1 benefício + CTA | sem história |
| 7 | estático | **fase de impacto** — fundo branco + texto preto/vermelho | só a cor define o estilo |
| 8 | estático | **clássica** — fundo preto + produto + **PREÇO** | **única peça do conjunto com preço** |
| 9 | carrossel | **objeção** — 1 card por objeção → CTA | quebra objeção, não apresenta produto |
| 10 | carrossel | **história** ou **catálogo** (escolhe 1) | história = 5-10 cards; catálogo = acervo |

**Como as 3 campanhas variam sem repetir dor:** os 10 papéis se mantêm, mas **a dor de cada slot muda**
e a **espinha (dor que vende) troca de slot** entre campanhas (C1 no slot 6, C2 no slot 8, C3 no slot 1,
por exemplo). Formato repetido é permitido; **conteúdo repetido não** (regra anti-variação-rasa).
Se a campanha tiver 9 peças em vez de 10, cai o slot 10 — os outros 9 são o 1-3-9 clássico.

**Economia de geração (confirmado /watch, método Rodrigo):** nem todo slot precisa de arquivo
novo gerado do zero — pelo menos 1 dos 9/10 pode ser **reaproveite literal** de um arquivo já
pronto da mesma leva (reposicionado noutra campanha/conjunto), contanto que o PAPEL dele na
tabela continue preenchido. Isso é diferente de repetir CONTEÚDO (dor/ângulo) — é só não gerar
2x o mesmo tipo de arquivo quando 1 já serve aos 2 lugares.

**Exceção legítima:** peça **traduzida de criativo já validado** (ex.: vencedor EN → es-AR) entra como
slot 2/6 sem contar como variação rasa — é reaproveitar validação em outro mercado, não recolorir a
mesma ideia no mesmo mercado.

**⛔ NÃO replicar gancho com o mesmo corpo trocando só o objeto** (correção da dona, 25/10/2026,
sobre a leva do Atlas): pegar o gancho vencedor e repetir o anúncio mudando só o exercício/o exemplo
é **errado** — é a mesma peça com outra etiqueta, e o Meta entrega como uma só. Peça nova = **gancho E
corpo/dor diferentes**. Reaproveitar take, gravação ou b-roll serve para montar **outro corpo**, nunca
para repetir o mesmo anúncio com outro exemplo.

**Duas regras da mesma call que fecham a matriz:**
- **Variação de hook NÃO funciona** (22/10): mexer só no texto/gancho do criativo validado, com o mesmo
  conteúdo e o mesmo "look", não sobe consciência — o Meta entrega como o mesmo anúncio. O que varia é
  **cena/ambiente e a dor** (consultório → cozinha → sala da residência → carro), nunca só a frase de
  abertura. Tradução de peça já validada para outro mercado é a única exceção.
- **A leva inteira é ponto de contato:** criativo que gera IC barato em volume fica ativo mesmo sem
  vender — é ele que sustenta a consciência dos outros. Corte só por **IC > 10% do ticket e volume
  baixo, depois de 48h**; nunca no dia 1, nunca por "não vendeu hoje".

**Cobrado pelo script:** `scripts/gate-plano-leva.py` reprova leva sem UGC (com material na mão) e sem
peça só-texto.

## Quando ler outra skill

- **`criacao-low-ticket-mvt/references/ESTRUTURA-DE-PENSAMENTO.md`** — a ordem canônica
  `persona → dor → demanda orgânica → oferta → página → criativo → peças do funil`, com a dor em
  3 camadas (**sintoma / cena / custo**). O criativo é a última ponta da cadeia: ele não inventa a
  dor, ele **traduz** a cena e o custo que a persona já mediu. Leia antes do Gate 0 se a oferta
  ainda não tem `pesquisa/PERSONA-E-ANGULOS.md`.
- `criativo-ads-video-orq`: toda produção de vídeo (imagem de referência, prompt
  Veo, QA de clipe, montagem, legenda, tarja). A estratégia da leva vem daqui.
- `modelagem-escalados`: biblioteca de 103 formatos + 12 prompts de estático
  (brandkit, dossiê, arte 9:16, leva de headlines, QA).
- `metaads-kevones`: estrutura de campanha, corte, escala, lance, e o que é novo no
  YouTube dele (`references/YOUTUBE-NOVIDADES.md`).
- `narracao-hub-tts`: voz off. `get-brolls`: b-roll com origem registrada.

## B-roll/real do TikTok — vídeos virais em inglês (regra da dona, 16/10/2026)

- **Material real = também TikTok.** Além do banco (`get-brolls`), usar **vídeos orgânicos virais em INGLÊS** do TikTok como cena real (sessão, cuidador, idoso, terapia). É o que faz o criativo parecer orgânico — os originais que modelamos **intercalam MUITA cena real** com o material do produto em cortes curtos.
- **Buscar com ~5 termos em inglês ligados ao PRODUTO.** Ex. (GeriNeuro / idoso / demência): `dementia activities` · `caregiver grandma moment` · `occupational therapy elderly` · `memory care activities` · `elderly cognitive games`. Priorizar **muitas views** (contagem no próprio TikTok).
- **⛔ REGRA DURA: o vídeo NÃO pode ter TEXTO ESCRITO / legenda queimada** — nada de caption embutida, watermark de app, ou texto em outro idioma. Só **cena limpa**; a legenda é a NOSSA (KaraokeV2). **Descarta o clipe que tiver texto.**
- **Perfil logado:** usar o perfil de browser **`tiktok`** (porta 9255). Baixar com **`yt-dlp`** (cookies do perfil quando precisar). Registrar em **`credits.md`**: termo, URL, @autor, **views**, arquivo.
- **Uso na montagem (receita dos originais):** **~15–20 cortes curtos (~2–3s)** alternando o **material do produto** (gravações de tela/fichas) com as **cenas reais** do TikTok, reforçando a fala com overlay de texto.

## Mapa do pacote (tudo linkado por aqui)

**Estratégia e produção de criativo**
- `criativo-ads` (esta) → decide o quê. `criativo-ads-video-orq` → orquestra vídeo (Hub/Flow).
- `modelagem-escalados` + `biblioteca-escalados` → estático/carrossel a partir de 103 formatos.
- `gpt-imagem-playwright` (imagem no ChatGPT) · `hub-video-playwright` (vídeo no Hub) · Flow em `criativo-ads-video-orq/references/mecanica-flow.md`.
- `narracao-hub-tts` (voz) · `get-brolls` (b-roll) · `yt-transcricao` (transcrever referência) · `metaads-kevones` (tráfego).

**Edição e composição de vídeo**
- `video-use` · `remotion-*` · `hyperframes-*` · `embedded-captions` · `captions-overlay` · `talking-head-recut` · `cut-the-curve` · `motion-doctrine` · `motion-graphics` · `seam-craft` · `media-use`.

**Orquestradoras e operacionais de nicho**
- `tiktok-shop` · `tiktok-ads` · `influenciadora-ia-instagram` · `depoimentos-video` · `depoimentos-comentarios-social` · `depoimentos-pagina-de-vendas` · `gerador-depoimentos-instagram-gpt` · `imagens-pagina-low` · `banner-checkout-gpt` · `competitive-ads-extractor` · `brandkit`.

**Infra de browser**: `agent-browser` · `browser-cloudflare` · `browser-harness` + `criativo-ads-video-orq/references/browser-setup.md`.
