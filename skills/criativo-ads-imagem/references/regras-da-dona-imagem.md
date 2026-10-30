# Regras da dona — imagem (texto original, movido de criativo-ads em 26/10/2026)

> O resumo que vale está no GUIA DE IMAGEM (`tipos-de-imagem.md`). Aqui ficam as regras na forma em que a dona deu, com os incidentes — consultar quando o GUIA não responder. Onde algo aqui contradiz o GUIA (ex.: exceção "só páginas" sem texto, "clássica" com mockup/fundo preto), **vale o GUIA** (regra mais recente).

> **Regra dura (dona, 25/10/2026 — texto de peça saiu flutuante sem caixa e formato saiu 9:16
> numa peça 4:5, os dois inventados de memória em vez de copiados da regra escrita):** ninguém
> — orquestrador nem pane — escreve prompt de texto/formato pro GPT de cabeça. Antes de
> escrever QUALQUER prompt de imagem, copia e cola literalmente a definição de texto ("Texto =
> sempre texto de Stories, na fonte nativa do Instagram Stories...") e a proporção ("estático e
> carrossel = 4:5, 1080x1350") mais abaixo nesta skill. Perguntar ao usuário "que estilo você
> quer" quando a resposta já está escrita aqui é o MESMO erro — não é escolha de gosto, é regra
> fixa. Todo brief de pane de imagem cola essas linhas inteiras, não resume nem parafraseia.


> **Regras da dona (11/10/2026 — o texto da peça de imagem é do GPT, nunca overlay de código):**
> - **Estático e carrossel: o TEXTO é escrito pelo GPT DENTRO da foto.** Overlay de código
>   com faixa/barra/bloco de cor atrás é **reprovado** — o texto do GPT sai com cara de legenda
>   de Story (o que o feed premia); overlay sai "perfeito demais", cara de anúncio, e derruba o CPM.
>   Dona, ao ver o lote do Jiu-Jitsu com o texto em faixa: *"os de imagem o texto já sai pelo gpt"*.
>   No prompt: texto exato, **uma linha só e sem aspas duplas** (o `inserttext` trunca e o modelo
>   volta perguntando o texto), pedindo **flutuante, sem nenhum bloco/barra/caixa de cor atrás**, com
>   margem de ~12% no topo e ~15% embaixo e nada cortado na borda.
> - **⛔ Primeiro confirme que o texto EXISTE, só depois confira ortografia (achado real,
>   Mapa del Tarot AR, CRIATIVO-07, 25/10/2026).** O prompt pedia 2 caixas de texto Stories com
>   texto exato — a imagem saiu **sem nenhuma das duas**, só com o preço em pill, e foi aprovada
>   assim. "QA de ortografia" sozinho não pega isso: palavra por palavra só funciona quando as
>   palavras existem. Checklist em 2 passos: (1) o texto pedido no prompt está fisicamente visível
>   na imagem? conte as caixas de texto, compare com o que o prompt pediu — se faltar 1, já reprova,
>   nem olha ortografia ainda; (2) só então confere acento palavra por palavra.
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
>   de imagem funciona (ver [[texto-estatico-imagem-nunca-overlay]]). Não existe peça de imagem sem
>   texto: até o carrossel "só páginas" tem card de gancho e card de CTA gerados (GUIA DE IMAGEM,
>   carrossel tipo 2). (A exceção "peça 9 do Tarot AR sem texto" foi escrita por um agente, não pela
>   dona — removida 26/10/2026.) Reincidência real (Mapa del Tarot AR, peça 5, 25/10/2026): pane escreveu copy no
>   `anuncio.md`, achou que cumpriu, entregou imagem limpa sem nada escrito na cena. Se a peça é imagem
>   ela SAI com texto na foto — conferir visualmente antes do handoff,
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


**Tamanho:** estático e carrossel saem em **4:5 (1080×1350)** em todos os cards, por
padrão (regra da dona, 23/10/2026 — antes era 1:1). 9:16 só se o usuário pedir. Vídeo continua
9:16. No carrossel demonstrativo, as páginas do entregável são arquivos reais
encaixados no 4:5; GPT não desenha página do produto.

> **⛔ PAGE REAL EM PAISAGEM — como virar card 4:5 sem virar slide (25/10/2026, Mapa del Tarot AR).**
> Quando o entregável tem página **horizontal** (ex.: mapa mental 1200×848), "4:5" não se resolve
> encaixando a página no card. As três tentativas erradas que um pane entregou como prontas:
> **(a)** página centralizada com **tarja branca** em cima/embaixo (= cara de PowerPoint, a dona
> reprovou); **(b)** página **crua** no card, com proporção 1200×848 dentro de um carrossel 4:5
> (o Meta corta); **(c)** **crop pequeno** de uma coluna da página ampliado (480×483 → borrado,
> cortando a carta). Certo:
> - página ocupa a **largura inteira** do card, na **resolução nativa** (texto legível) e a sobra
>   vertical é preenchida com o **próprio papel da página** (repete a faixa limpa da borda; nunca
>   espelhar conteúdo, nunca chapar branco) — é o que `criativos/scripts/montar-cards.py` faz
>   (referência viva: `OFERTAS/luciola-mapatarot-ar/criativos/scripts/montar-cards.py`);
> - ou **recorte full-bleed** que preencha o card, se a página inteira não couber — mas só quando
>   a fonte tiver resolução pra isso (nunca ampliar crop de ~480px).
> **Todos os cards da mesma peça com o MESMO tamanho** (1080×1350). Card de tamanho diferente
> reprova a peça inteira.

> **⛔ GATE DA IMAGEM FINAL — antes de dizer "pronta" (25/10/2026).** O `gate-pecas-criativo.py`
> olha o que ENTRA na cena; ele **não** olha o que sai — foi por isso que cards de 480×483 e
> página 1200×848 passaram como entregues. Rodar sempre, nos arquivos finais:
> `python3 ~/.claude/skills/criativo/scripts/gate-imagens-finais.py <finais...> --pasta CRIATIVO-N/`
> (opção `--story` pra 9:16; não existe mais dispensa de texto — impacto também tem prompt de texto, e carrossel só de páginas tem cards de gancho/CTA gerados).
> Ele cobra: proporção 4:5, largura ≥ 1080, mesmo tamanho em todos os cards e **prompt salvo em
> `intermediarios/prompt*.txt` pedindo o texto como "Instagram Stories text sticker"** — sem
> prompt salvo ninguém audita se o texto foi pedido ao modelo ou colado por cima em código, e
> colado por cima é reprovado. **BLOQUEADO = não é peça pronta**, nem entra em handoff.

**Estático = foto orgânica de celular, SEMPRE (dona, 23/10/2026):** todo estático e todo carrossel é cena real
com cara de foto de iPhone, com fundo orgânico que faça sentido pra persona (academia, sala de aula, mesa de estudo,
carro). **Única exceção: fase de impacto estilo Rodrigo** (fundo branco, texto preto/vermelho), que é formato
específico — **fundo branco OU preto** (varia peça a peça; texto preto+vermelho no branco, texto
branco+vermelho no preto; regra da dona, 24/10/2026).

**⛔ SUPERSEDE a regra de 25/10 abaixo nas peças de IMPACTO (texto puro, fundo branco/preto) —
regra da dona, 27/10/2026:** gancho→desenvolvimento→CTA em 3 blocos lê devagar, texto comprido demais
pra entender rápido rolando o feed. **Pra fase de impacto, é só 2 blocos: PRODUTO + CTA**, direto —
nome do produto + o que ele entrega (+ preço, se for peça de preço) numa frase só, e o CTA logo
embaixo. Nada de linha de desenvolvimento/benefício separada. Exemplo bom (referência aprovada):
"ATLAS VISUAL: 150 MAPAS DE ANATOMÍA Y EJERCICIO." + "$10.900, ACCESO INMEDIATO." Continua valendo
nomear o produto (não pode ser frase solta de curiosidade sem dizer o quê) — só a estrutura de 3
blocos foi derrubada. **A regra de 3 blocos (gancho→desenvolvimento→CTA) continua valendo só pro
carrossel tipo 2** (sequência de lâminas, onde cada card já é um bloco separado, não lê tudo de
uma vez).

**⛔ Fase de impacto e carrossel tipo 2 (só lâminas) também levam estrutura
gancho→desenvolvimento→CTA, nunca frase solta de curiosidade (regra da dona,
25/10/2026 — SUPERSEDIDA pra fase de impacto pela regra de 27/10 acima; continua valendo pro
carrossel tipo 2).** Uma frase isolada sem desenvolvimento vira curiosidade vaga, não
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

**⛔ Gate mecânico antes de escrever QUALQUER prompt de peça de impacto/só-texto
(regra original 25/10/2026, AJUSTADA 27/10/2026 pra 2 blocos):** o erro documentado em
25/10 (NeuroActiva AR C1-4) foi gancho de curiosidade SEM nomear o produto — isso continua
proibido. O que mudou é a estrutura: não é mais gancho+desenvolvimento+CTA (3 blocos, lento de
ler), é **PRODUTO (nomeado, com o que entrega) + CTA** (2 blocos, direto). Antes de mandar
QUALQUER prompt de texto-só pro GPT, **conte os blocos**: tem que ter exatamente 2 — (1) o nome
do produto + o que entrega (+ preço se for peça de preço) e (2) o CTA. Nunca gancho solto sem
nomear o produto, e nunca um 3º bloco de desenvolvimento separado inflando o texto.

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


**Fase de impacto é o formato PREFERIDO pra clareza direta (dona, 27/10/2026):** quando a dúvida é
"qual formato deixa mais claro o que é o produto", a resposta é fase de impacto — fundo branco (ou
preto), **texto só**, sem cena, sem material aparecendo. Continua gancho→desenvolvimento→CTA (regra
de 25/10 acima) e **preço é opcional**, não obrigatório — o que importa é nomear o produto com
clareza total ("o quê, exatamente"). Nunca trocar essa clareza por algo "mais bonito"/vago tipo
fundo colorido sem produto nomeado (a dona citou "o azul" como exemplo do que NÃO fazer: visual
bonito mas sem dizer o produto direto).

**Vibe das imagens (dona 23/10):** todas orgânicas estilo iPhone (derruba CPM), exceto a "fase de
impacto" (fundo branco, texto preto e vermelho). Sem moldura, sem cara de anúncio montado.
**Caixa de perguntas em story:** pergunta na imagem + alguém (de preferência o expert) respondendo
com o material na mão, orgânico.


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

Mecânica de browser sempre pela skill dela: ChatGPT → `gpt-imagem-playwright`
(perfil livre via `gpt-livre.sh`); vídeo → `hub-video-playwright` (via `hub-livre.sh`).
Nunca tocar o browser sem invocar a skill de mecânica antes.

