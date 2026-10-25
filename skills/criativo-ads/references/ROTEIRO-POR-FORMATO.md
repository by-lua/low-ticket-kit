# Como escrever o roteiro de cada formato (método Rodrigo — página → GPT → script)

> Fonte: Rodrigo Liedson, transcrições em
> `MINERACAO/referencia-rodrigoliedson/METODO-RODRIGO-EUROPA-139-SAGA-COMPLETA.md`.
> Isto é a camada que faltava entre ESTRATÉGIA (`criativo-ads` Gate 0, qual dor/ângulo)
> e EDIÇÃO (`criativo-ads-video-orq` E.2b/E.0d, como montar o corpo). Sem ela, o
> roteiro sai raso — gancho copiado do plano, sem desenvolvimento, sem CTA escrito
> (ver `plano-video-ganho-nao-e-roteiro-completo`).

## O que ele faz, na ordem (nunca pula etapa)

1. **Pega a página de vendas real** da oferta — headline, benefícios, objeções,
   garantia, preço, bônus. Nunca inventa benefício que a página não promete
   (mesma régua do Gate 0 de `criativo-ads`).
2. **Vai no GPT e PEDE o roteiro**, um prompt por FORMATO (GC, expert, demonstrativo
   — nunca um prompt genérico "faz um roteiro de anúncio"). O prompt já embute a
   estrutura de blocos daquele formato (abaixo) e a dor/ângulo real daquela peça.
3. **Monta/edita por cima** do que o GPT devolveu — ajusta fala, corta o que ficou
   cheio, mas a ESTRUTURA (gancho→desenvolvimento→CTA) já vem do prompt, não é
   inventada na montagem.
4. **Só então entra a produção** (imagem/vídeo) e a **edição** (split 70/30, 1
   clipe por frase, fade — regra universal, `criativo-ads-video-orq` E.0d).

## Estrutura do prompt por formato (o que pedir ao GPT)

Todo prompt de roteiro leva: a dor/ângulo real da peça (do `PERSONA-E-ANGULOS.md`),
o benefício/preço/garantia reais (da página), e a estrutura de blocos do formato —
nunca pede "escreve um roteiro" solto.

### GC / UGC comprador — relato em 1ª pessoa
- **Gancho:** frase de identificação ("eu também [dor]" / "isso aconteceu comigo").
- **Relato:** conta a situação, em 1ª pessoa, sem tom de vendedor.
- **Mostra o material:** aponta/segura o entregável, dizendo o que viu/usou
  (pose "capa de livro" — ver `criativo-ads` seção Rodrigo).
- **CTA:** comando curto, sem nome do produto nem condição de compra.

### Expert — autoridade que desenvolve o mecanismo
- **Gancho:** afirmação de autoridade ou contraste ("a maioria faz X, o certo é Y").
- **Desenvolve o mecanismo:** explica POR QUE funciona (não só repete o benefício —
  erro mais caro documentado, CRIATIVO-02 Atlas).
- **Mostra o material:** corta pra tela/página real enquanto explica.
- **CTA:** comando curto, mesma regra do GC.

### Demonstrativo — tela do entregável por dentro
- **Gancho:** toca a dor em b-roll, sem produto ainda.
- **Corpo:** nomeia o problema de novo → mostra a solução gravando a TELA do
  entregável por dentro (área de membros/app) — o produto bem entregue é o próprio
  corpo, sem precisar atuação.
- **CTA:** comando curto.

## Escreve no idioma que você entende, traduz depois (confirmado /watch, 25/10/2026)

Rodrigo nunca escreve o roteiro direto no idioma do mercado de destino quando não
domina esse idioma — ele pede ao GPT no idioma que ELE entende (ex. português,
vendendo em francês), lê as 5 opções, escolhe a melhor, edita, e SÓ ENTÃO traduz
(DeepL + revisão manual, às vezes traduz 2x pra limpar tradução literal estranha).
Motivo: impossível julgar qualidade de copy num idioma que você não lê bem.
Aplica aqui: roteiro de oferta ES/outro idioma nasce em PT, aprova o melhor, só
depois vai pro espanhol/francês/etc — nunca gerar direto no idioma de destino
achando que economiza um passo.

## O mesmo roteiro base flexiona entre UGC e expert (confirmado /watch)

A copy "descobri isso neste livro" (relato de quem comprou/usou) e a copy "estudei
5 anos o assunto, descobri os gatilhos, coloquei tudo neste livro" (autoridade) são
o MESMO gancho+mecanismo, só reescritos na voz de quem fala. Confirma: escrever o
roteiro UMA vez por dor/ângulo e depois adaptar a voz pros 2-3 formatos (UGC,
expert) é válido e mais rápido que escrever do zero pra cada um — desde que a voz
mude de verdade (1ª pessoa relato vs. autoridade que explica o mecanismo), não só
troque o pronome.

## Detalhes de produção confirmados numa 2ª leitura completa do /watch (25/10/2026)

- **Não copia a página inteira pro prompt do GPT.** Copia só o trecho denso em
  benefício/promessa ("até aqui") — depoimento, garantia, FAQ ficam de fora. Um
  prompt de roteiro carrega só a matéria-prima relevante, não a página completa.
- **Já manda a duração alvo dentro do prompt** ("roteiro de até 15s") — o
  rascunho do GPT já nasce no tamanho certo. Nunca escrever livre e cortar depois
  pra caber no tempo; pedir o tamanho na hora economiza retrabalho.
- **Tradução com contraprova (back-translation):** depois de traduzir e editar,
  traduz a versão final DE VOLTA pro idioma original e lê — se o sentido mudou ou
  ficou estranho na volta, ajusta antes de fechar. Não é só "traduzir 2x pra
  limpar", é uma checagem de fidelidade de sentido.
- **Sintaxe exata de prompt pra geração de vídeo com fala:** `"<ação da cena>":
  "<fala exata entre aspas>"` — ex. `woman holding the book and speaking: "<fala>"`.
  Usar esse padrão literal (ação + dois-pontos + fala entre aspas) nos nossos
  prompts de imagem→vídeo (Flow), não frase solta sem separação clara.
- **Gera a imagem de referência em 1:1 (quadrado) de propósito**, mesmo sabendo
  que vai rodar em 9:16/4:5 depois — assunto centralizado aguenta o corte
  automático por posicionamento sem perder enquadramento. Isso é a MESMA lógica
  da nossa margem de segurança (`criativo-ads`), só que aplicada já na hora de
  GERAR a imagem, não só na hora de montar — vale testar como padrão de geração.
- **Overlay de texto muda por formato, não é o mesmo tratamento pra tudo:**
  - **UGC/testemunho:** texto pequeno e discreto no topo (estilo caption nativa
    de Story) — a intenção é DISFARÇAR de post real, não parecer anúncio.
  - **Vídeo gancho→mecanismo→CTA:** headline grande com a promessa por cima
    ("descubra como…") — aqui o overlay É o argumento de venda, não disfarce.
  - Escolher o estilo de overlay pelo PAPEL da peça (disfarçar vs. vender
    explicitamente), nunca aplicar o mesmo texto-padrão em toda peça de vídeo.
- **O respiro antes da pessoa pegar o material NÃO é descartado.** Ele suaviza
  esse início com um efeito de transição leve, tratando aquele instante como
  parte do próprio hook (a pessoa ainda não mostrou o produto = ainda é gancho de
  atenção) — nunca cortar esse trecho achando que é sobra; é cortar que chega
  tarde demais que é o erro (ver regra "gancho ≤2 frases, já mostra o material").

## Velocidade da fala: ajusta na FALA gerada, antes de montar (não é regra de edição)

Depois de gerar o clipe falado (i2v/lip-sync), se a voz saiu rápida/apressada,
Rodrigo ajusta a **velocidade do próprio clipe de fala** (ferramenta de geração,
ex. slider de speed) ANTES de entrar na montagem — não é a mesma coisa que acelerar
a timeline editada (isso é proibido por padrão, ver `criativo-ads-video-orq` E.0b).
Checar a naturalidade da fala logo depois de gerar o clipe, ainda na ferramenta de
imagem→vídeo, é um passo a mais no catálogo de QA de clipe (`criativo-ads-video-orq`
QA de clipes) — antes de levar o clipe pra montagem.

## Depois do roteiro: a edição é camada separada, sempre a mesma

Qual dos 3 formatos acima o roteiro seguiu NÃO muda a receita de montagem — todo
vídeo com entregável aparecendo por dentro usa `criativo-ads-video-orq` E.0d/E.2b
(split 70/30, 1 clipe por frase, fade, CTA sem corte seco), **independente do
formato do roteiro**. Formato = O QUE o roteiro diz; edição = COMO a tela monta
o que o roteiro diz. Nunca confundir os dois nem pular a edição achando que o
roteiro de GC/expert "já basta".

## Imagem NÃO usa o banco de 5 copies do GPT — texto é curto e tem 2 fontes só (confirmado /watch)

Diferente de vídeo/UGC (que nasce do prompt "5 copies com hook/desenvolvimento/
mecanismo/CTA"), o texto de imagem no método Rodrigo vem de só 2 lugares, sempre
curto (headline + no máximo 1 subheadline/bottom-text, nunca um roteiro):

1. **Clona o texto do criativo JÁ VALIDADO** (nosso ou modelado) — manda a imagem
   de referência pro gerador com o prompt "cria uma imagem IDÊNTICA, só traduz o
   texto". O texto não é reescrito, é tradução literal do que já vende. Essa é a
   variação mais simples e mais usada (2 das 6 imagens da leva dele foram assim).
2. **Variação com headline/subheadline escritas na hora**, direto no prompt
   ("fundo branco + headline: '<promessa>' + texto de baixo: '<fragmento de
   mecanismo/benefício>'"). **Correção (leitura completa do transcript):** o tipo
   "clássica" (fundo preto/branco + mockup + preço) leva ATÉ 4 elementos de texto —
   headline, subheadline, preço, e um texto de apoio extra embaixo — não é só
   headline+1 linha; varia pelo tipo (antes/depois e só-texto ficam mais curtos,
   clássica carrega mais texto porque tem o preço visível). CTA nunca entra dentro
   da arte, fica no botão do anúncio.

**No nosso portfólio isso bate com `tipos-de-imagem.md` + GATE 0.1 (capa+páginas
reais anexadas)** — a diferença é que aqui o texto Stories que escrevemos
(regra "texto é do GPT dentro da foto") deve seguir essa mesma régua de tamanho:
1 headline + no máximo 1 linha de apoio, nunca texto longo tipo legenda de post.

**Variedade de formato de imagem confirmada no vídeo (mapeia 1:1 com nossos slots):**
antes/depois (mostra o antes, depois o depois, aponta pro produto) · clássica
(headline + subheadline + mockup + preço + texto de apoio) · só-texto (frase
isolada, sem produto) — os 3 já existem na nossa tabela de slots, confirmados.

## Imagem segue o mesmo caminho de produção (não é exclusivo de vídeo)

Peça estática também nasce de roteiro curto (texto de Stories) escrito a partir da
página real + a mesma lógica de formato (GC mostra material, impacto só frase,
clássica com preço) — ver `criativo-ads` seção "Estático = foto orgânica de celular"
e `references/PROMPT-ESTATICO-ORGANICO.md`. A cena SEMPRE orgânica estilo iPhone,
material em 2 formatos (digital+impresso) — isso é regra de produção da imagem,
equivalente à edição do vídeo: aplica em QUALQUER formato de imagem, não é um
formato a mais.
