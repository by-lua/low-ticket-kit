# Método da leva — Kevones (quantidade, mistura, matriz, teste em grupos) — movido do SKILL.md em 26/10/2026

> Passo 1 da TRILHA DO CRIATIVO. Atualizado com a aula do Kevones de 23/10/2026 (`Fo3EFSn7LeI`, estudo em
> `CONHECIMENTO/ESTUDOS/2026-10-26-delta-criativo-kevones.md`):
> - **Estrutura pela verba:** pouca verba → 3 campanhas 1-1-10 (padrão da casa); mais verba e teste mais rápido → 10 campanhas 1-1-3.
> - **Mistura imagem/vídeo C1 7+3, C2 5+5, C3 6+4 = regra da DONA (26/10/2026)**; o Kevones só exige diversidade de formato e de narrativa ("não faz sentido subir 30 criativos iguais").
> - **Cada peça cumpre um papel de consciência** (apresentação/mecanismo, dor, objeção, prova real, oferta/preço, demonstração) — o plano registra qual; 30 peças diferentes no visual mas com o mesmo papel são redundantes. Prova/feedback só com material real.
> - **Depois do teste (48 h):** IC até 10% do ticket é o veredito. IC caro → olhar CTR e custo de LPV: CTR < 2% e LPV caro (> ~R$1,30) = corrigir o criativo na próxima leva; CTR e LPV bons com IC caro = gargalo na página/oferta, não no criativo. Nunca matar no dia 1. Detalhe de tráfego: `metaads-kevones`.
> - **Peça de preço é PRÉ-QUALIFICAÇÃO** (Rodrigo, estudo `CONHECIMENTO/ESTUDOS/2026-10-26-delta-criativo-rodrigo.md`): tende a ter CTR menor e conversão maior, porque quem clica já sabe o preço. CTR baixo sozinho não reprova a peça de preço — olhar IC/compra.

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


**Mix por campanha + carrossel (regra da dona, 23/10/2026):** toda campanha de teste (1-1-10 ou
1-1-3) leva **vídeo + estático + carrossel no mesmo conjunto** (metaads-kevones §21). **Proporção por
campanha (dona, 26/10/2026): C1 70/30 (7 imagens + 3 vídeos), C2 50/50 (5+5), C3 60/40 (6+4) —
imagem nunca menos que vídeo** (vídeo dá trabalho demais). **Sem mockup:** imagem = páginas reais do entregável em cena orgânica estilo iPhone, texto
como de story, em **vários aparelhos** (celular, tablet, notebook), nunca só impresso. **Anúncio
nunca fala "PDF"** — vendemos material organizado na área de membros; PDF não é benefício.

**⛔ MÉTODO ÚNICO, 3 camadas sempre somadas — nunca escolher 1 e ignorar as outras (erro real
repetido 2x no mesmo dia, 25/10/2026: CT3/CT22 tratados como "demonstrativo OU UGC"; depois peça de
expert falando+cortando pro material sem nenhuma técnica de edição, por tratar "expert fala" como
formato que dispensa a receita).** Detalhe completo + tabela dos 10 slots: seção **🔗 MATRIZ ÚNICA**
mais abaixo. Resumo das 3 camadas, válidas em TODA peça de vídeo com pessoa:
1. **Quantidade/distribuição (Kevones)** — quanto e em que mix.
2. **Formato/papel de cada peça (Rodrigo)** — quem aparece, o que a mão/tela mostra.
3. **Técnica de edição (`criativo-ads-video-orq/references/EDICAO-PADRAO.md`)** — split 70/30, 1 clipe por frase, fade
   nas junções, CTA sem corte seco. **É caixa de ferramenta de montagem, não um 4º "formato"** —
   usa SEMPRE, mesmo com expert/UGC falando no gancho. "Tem alguém falando" nunca dispensa isso.


(caixa de perguntas, expert respondendo a caixa de perguntas, print de WhatsApp, notícia etc.).

| Expert com rosto | reels orgânicos → campanha de seguidores → conversão | `criativo-ads-video-orq` + regra em `references/kevones-criativo.md` |
| TikTok Shop / achadinho | — | `tiktok-shop` (orquestradora própria) |
| Banner de checkout / imagens da página | não é criativo de anúncio | `banner-checkout-gpt` / `imagens-pagina-low` |


## Quantidade pela fase da conta

| Fase | Quantas peças | Estrutura na conta |
|---|---|---|
| Oferta nova, nada validado, verba < R$ 1 mil/dia | **3 a 5**, formatos misturados | 1 campanha, 2–3 conjuntos, mesmas peças em todos |
| Público validado, quer achar novo criativo | **3** de dores diferentes | 1 campanha, 1 conjunto (público validado), 3 peças (1-1-3) |
| Já vende, construindo ecossistema | **conforme o ecossistema pede** (2–3/semana é exemplo conservador, não teto — Kevones 23/10/2026) | cada vencedora isolada em campanha 1-1-1 |
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
| **Vídeo** | toca na dor → **desenvolve o mecanismo** → CTA | corpo não pode só repetir a promessa — explica POR QUE funciona (ex.: "não é que você não estudou, é que decorar nome não mostra o movimento"); CTA nunca corta seco: card com produto + seta ~5 s (`EDICAO-PADRAO.md` §7) |
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

