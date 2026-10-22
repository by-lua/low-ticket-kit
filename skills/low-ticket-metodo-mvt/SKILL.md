---
name: low-ticket-metodo-mvt
description: Método "O Processo" de Heitor Nogueira para produtos digitais Low Ticket MVT (Modelagem + Vantagem + Tráfego), fiel ao workshop de 11h, aos frameworks originais e aos vídeos do canal — tese, os 2 tipos de produto, as 10 características, os 8 erros, concepção × oferta × produto, fluxo de 8 passos, mineração, modelagem, Obra de Arte 100K, mapa da vantagem e Semáforo das Decisões (verde/amarela/vermelha, extra do YouTube, não da aula), página de vendas (10 blocos + 9 opcionais), produto MVP, criativo demonstrativo, configurações técnicas e estudos de caso (tráfego: skill `metaads-kevones`). Use quando o usuário pedir para criar, validar, modelar ou analisar uma oferta low ticket, perguntar o que o método diz sobre qualquer etapa, ou mencionar MVT, "O Processo", Heitor Nogueira, concepção, Obra de Arte 100K, mapa da vantagem, criativo demonstrativo, semáforo das decisões. Para executar o fluxo do zero no nosso ambiente, use junto com `criacao-low-ticket-mvt`.
---

# Low Ticket MVT — método "O Processo" (Heitor Nogueira)

**MVT = Modelagem + Vantagem + Tráfego** [MATERIAL-FRAMEWORK]. Esta skill é o
**método**, e só o método. Onde a fonte é omissa, a skill também é. A execução no
nosso ambiente (browser, Hub, panes) está em `criacao-low-ticket-mvt`.

Citações: `[aula HH:MM]` = minutagem do `aula-11h.vtt`; `[aula, cauda]` = trecho
após 09h59 (sem timestamp); `[MATERIAL-FRAMEWORK]`, `[CHECKLIST]`,
`[FRAMEWORK-TESTE-CRIATIVO]` = boards Whimsical; `[bônus …]` e `[YT …]` = aulas
extras.

## Mapa dos arquivos

| Arquivo | Conteúdo |
|---|---|
| `references/pagina-produto-criativo.md` | página (3 pilares, 10 blocos, 9 opcionais, copy, visual, stack), produto (MVP/modelo/completo), criativo demonstrativo, configurações técnicas. Ganha do YouTube: lateralização de criativo, layout do entregável, copy da página com agente; vídeo demonstrativo ≠ VSL, criativo a partir do que a persona consome, hack de imagem, crítica de página, checkout por persona |
| `references/concepcao-yt.md` | concepção do YouTube em detalhe: gerar do zero por persona/pensamento interno, teste de reescrita, Raio X, 3 mercados, oceano azul, 3 erros essenciais, prazo de 7–10 dias, mineração na prática (3 perguntas, qual comando alimenta qual palavra-chave), decisão rápida de demanda, oferta de VSL → low ticket, nicho complexo → peça específica, melhorar ≠ modelar |
| `references/prompts-e-exemplos.md` | os comandos de ChatGPT do método, na íntegra, e os exemplos trabalhados ao vivo |
| `references/estudos-de-caso.md` | Salmos (R$531k), Lanchinho Animado (R$218k), casos do YouTube (inclui Apocalipse/app, R$35.664 num dia, R$49.703, fim de semana R$5.083, R$100 a R$1.275 de lucro em 4 dias corridos, R$4.552 em ~8 dias white, rotina de um dia, 4–5 ofertas em paralelo, origem 2022/23) |
| `references/transcricoes/` | fonte bruta: aula de 11h (`aula-11h.vtt`/`.csv` + cauda), bônus, estudos de caso, YouTube. `INDICE.md` |
| `references/docs/frameworks-whimsical/*__por-painel.md` | fonte principal dos 3 boards (Material Framework, Checklist, Teste de Criativo): texto por painel + setas + cores + o que só existe como imagem, transcrito do print. Os `.txt`/`.json` são o extrato antigo/bruto. Prints em `prints/` (tiles + overview) para conferir layout e imagens |
| `references/modelo-de-pagina/` | HTML de página que já usamos (adaptação local, **não** é o template JSON do método) |

### Como ler os boards Whimsical [`*__por-painel.md`, prints]

- **Cor** (Material Framework): faixa **dourada** = título de seção · **verde-escuro/teal**
  = definição ou passo certo · **carmesim/vermelho** = erro ou anti-exemplo ("NÃO É UM
  LOWTICKET MVT QUE EU VENDO") · **roxo** = "SUA OFERTA", raiz das 10 características.
  Cor sozinha não prova; confirme no contexto. Cada board muda um pouco: no Checklist,
  amarelo = fase, verde-escuro = etapa, cinza = tarefas (sem vermelho); no Teste de
  Criativo, vermelho também marca fase/alerta/**alternativa** (estrutura simplificada),
  não só erro.
- **Material Framework** é uma faixa de 7 colunas: 1 informações do workshop · 2
  cronograma do dia, "o jogo é dominar o jogo" e resultados de abril (prints do
  Utmify) · 3 o que é um Low Ticket MVT, exemplos, o que NÃO é, as 10 características
  · 4 os 8 erros · 5 concepção × oferta × produto · 6 mineração/Biblioteca, mapa da
  modelagem, vantagem · 7 blocos da página (obrigatórios/opcionais, onde inserir) e
  criativos demonstrativos.

Em dúvida sobre o que o Heitor disse: `grep` na transcrição, não na memória.

---

## 1. A tese

- **O jogo é a concepção.** "O jogo não é sobre ferramenta de IA, não é sobre
  estrutura de campanha, não é sobre Facebook, não é sobre edição de vídeo… o jogo é
  minerar, entender a concepção, saber modelar da forma correta e preparar sua obra
  de arte" [aula 01:42]. A execução estratégica é "o 90/10 do resultado"
  [MATERIAL-FRAMEWORK; aula 00:09].
- **Dominar princípios**, não copiar. O mercado ensina "encontra um produto que já
  está vendendo com muitos anúncios ativos, copia a estrutura, faz algumas melhorias
  e sobe" — "95% das pessoas vão te ensinar isso" [aula 00:15].
- **Vender algo que as pessoas QUEREM, que tem DEMANDA e que NÃO TEM NINGUÉM
  VENDENDO** — a "direção de ouro" [aula 00:18; MATERIAL-FRAMEWORK]. Querer ≠
  precisar: "precisar é uma coisa que eu deixo para depois" [aula 00:57].
- **Seguir 100% um fluxo.** "Depois que você entende os princípios e o fluxo de
  execução, a única coisa que você precisa fazer é lançar concepções até acertar"
  [MATERIAL-FRAMEWORK; aula 01:06]. Testar 10 ofertas com a mesma metodologia é
  diferente de testar 10 ofertas cada uma de um jeito [aula 01:15].
- **O jogo do mercado × o meu jogo** [MATERIAL-FRAMEWORK, painel 15]. Mercado (vermelho):
  acha produto que já vende com muitos anúncios ativos → copia a estrutura (página,
  criativo, produto) e faz melhorias → sobe campanhas para ver se funciona. Meu jogo
  "desde 2023 com low ticket" (verde): domino os princípios e a lógica de cada
  movimento → modelo e crio ofertas do zero com marketing de vantagem → vendo algo que
  as pessoas querem, tem demanda e ninguém vende → sigo 100% um fluxo com etapas
  definidas → faço o fluxo ser repetitivo.
- Todas as ofertas lançadas no ano "eram ofertas novas que não tinha ninguém
  vendendo" — ou criadas do zero dominando os princípios, ou modeladas [aula 00:18].

## 2. Os dois únicos tipos de produto [aula 00:27–00:45]

1. **Transformar algo difícil em algo de fácil entendimento — visual, explicativo e
   organizado.** Não é guia cheio de texto. Ex.: 150 Salmos explicados versículo por
   versículo, calendário da Semana Santa para crianças, mapas mentais de português,
   Catecismo parágrafo por parágrafo.
2. **Entregar uma coisa pronta para baixar e usar — organizada, economiza tempo,
   rápida.** Formato "**número + coisas + para tal resultado**". Ex.: 60 modelos de
   luminárias CNC, 300 capas de caderno no Canva, 100 encontros de catequese prontos.

**O que não se vende:** transformação completa, curso completo/longo barato,
"aprenda do zero", metodologia, "módulo 1, 2, 3…", "conquiste o resultado X em X dias
com X minutos por dia", algo complexo de entender [aula 00:39–00:42;
MATERIAL-FRAMEWORK].

- Não é sobre o preço: "vai ter oferta que você vai botar 10 reais e não vai vender"
  [aula 00:39].
- Ebook ainda vende; o número de páginas não importa (produto de 2.500 páginas
  rodando) — importa a concepção e ser visual [aula 00:45].
- Fazer um dos dois tipos **aumenta a chance**, não garante: precisa ainda do tipo de
  página, criativo e estrutura de campanha [aula 00:39, 00:48].

## 3. As 10 características do Low Ticket MVT [MATERIAL-FRAMEWORK; aula 01:36–01:42]

"Ou o produto cumpre os requisitos, ou ele não é um Low Ticket MVT de verdade."

| # | Característica | Definição do framework |
|---|---|---|
| 1 | Específico | resolve uma dor ou desejo bem definido, sem abraçar o mundo |
| 2 | Melhoria | entrega um resultado imediato, ainda que pequeno, mas perceptível |
| 3 | Prático | fácil de aplicar, sem conhecimento avançado ou materiais difíceis |
| 4 | Organizado | tira a confusão da cabeça e coloca num formato simples e estruturado |
| 5 | Visual | atrativo aos olhos, design que passa clareza e valor imediato |
| 6 | Economiza tempo | atalho pronto que evita horas quebrando a cabeça |
| 7 | Rápido de consumir | entende e aplica em minutos, não em semanas |
| 8 | Ferramental | pode ser usado de forma repetida, como ferramenta |
| 9 | Fácil entendimento | não exige explicação complexa |
| 10 | Tangível | mesmo digital, passa sensação de algo real e palpável |

No board é uma cadeia: raiz roxa "SUA OFERTA" → 10 caixas empilhadas em sequência (na
ordem da tabela); cada uma tem definição (amarelo) e exemplo (azul), ex.: Melhoria =
"planilha que mostra onde cortar gastos hoje" · Ferramental = "planilha de controle de
anúncios" · Tangível = "mockup de e-book com capa profissional". Caixa vermelha final:
"se faltar uma dessas peças, o produto perde força"; ao lado, "OFERTA XYZ" (scripts
para venda de imóveis) como oferta que falha nelas [MATERIAL-FRAMEWORK, painel 22].

Exemplo passado característica por característica ao vivo: "140 exercícios de
cinesiologia para fisioterapeutas" [aula 01:36–01:42].

## 4. Os 8 erros [MATERIAL-FRAMEWORK; aula 00:54–01:09]

**Erros de execução**
1. **Concepção:** vender mais do mesmo · vender o que as pessoas só *precisam* ·
   vender algo cético ("acabe com a ansiedade", "10 mensagens para o ex voltar",
   "perca 10 kg em 4 semanas") [aula 00:57].
2. **Características:** vender transformação completa, curso longo barato, algo
   complexo [aula 01:00].
3. **Nível de consciência errado:** vender para quem não está pronto para comprar
   (curso do zero de confeitaria → "20 receitas de bolo de pote para quem já é
   confeiteira") [aula 01:00].
4. **Comunicação:** não é específica para quem compra; o criativo fala A e a página
   fala B ("10 modelos de currículo para engenharia mecânica" no criativo e "50 para
   todas as profissões" na página) [aula 01:03].
5. **Não seguir a metodologia:** recebe template, modelo de criativo e estrutura de
   tráfego e faz diferente [aula 01:03].

**Erros pessoais**
6. **Falta de execução:** demora para cumprir demandas e subir a oferta, demora para
   decidir, procrastina olhando o resultado dos outros [aula 01:03–01:06].
7. **Falta de organização:** não segue o fluxo, não sabe o que fazer em cada momento,
   quer fazer tudo ao mesmo tempo [aula 01:06].
8. **Falta de constância:** cada hora consome conteúdo de alguém e aplica coisa
   diferente; testou a primeira concepção e já quer desistir [aula 01:06].

"Se você errar nessa concepção, nada adianta você fazer isso aqui: página, produto,
criativo, configuração técnica, tráfego" [aula 01:00].

## 5. Princípios iniciais [MATERIAL-FRAMEWORK; aula 01:45, 04:27]

Antes da prática, dominar: **modelo de vendas** (vende em página de vendas) ·
**nível de consciência** (para quem já está no mercado) · **as 10 características** ·
**formatos escaláveis** (ebook/PDF, app, flashcard…) · **precificação lucrativa**
(dupla oferta R$17,90 / R$27,90) · **concepção × oferta ×
produto** · **mapa da modelagem** · **mapa da vantagem** · **ser um executor**
[aula, cauda].

## 6. Concepção × Oferta × Produto [aula 01:15–01:48; MATERIAL-FRAMEWORK]

"Para construir o seu low ticket, antes mesmo da página, criativo e anúncios, você
precisa definir os elementos da concepção, a oferta e o produto."

| | O que é | Elementos |
|---|---|---|
| **Concepção** | a ideia: o que vendo, para quem e por que é valioso — "duas linhas" | **9:** nicho · subnicho · persona · dor · desejo · pensamento interno · resultado final · mecanismo da solução · formato |
| **Oferta** | como apresento ao mercado | **8:** promessa · nome do produto principal · o que compõe o produto principal · bônus · vantagem · valor de venda · benefícios · copy |
| **Produto** | o que entrego | conteúdo · visual · experiência de consumo · entrega |

**Os 4 elementos principais da concepção** (os usados na modelagem) [aula 01:21]:
1. **Comunicação** (persona, dor, desejo) — para quem
2. **Formato** — como entrego
3. **Mecanismo** — o que entrego para resolver
4. **Nicho/subnicho** — onde a oferta está inserida

Exemplo: "140 exercícios de cinesiologia para profissionais de educação física" →
comunicação: prof. de ed. física · formato: ebook/PDF · mecanismo: 140 exercícios
de cinesiologia · nicho: saúde/educação física [aula 01:21–01:24].

"Se você fizer 20 vezes isso, você domina a concepção" [aula 01:21].

No board [MATERIAL-FRAMEWORK, painel 5] cada bloco (9 elementos da concepção · 8 da oferta ·
4 do produto: conteúdo, visual, experiência de consumo, entrega) termina numa caixa vermelha
**"CHECKLIST DE VALIDAÇÃO"** ligada por seta. O board só traz a caixa, sem critério escrito;
o único checklist com texto é o checklist 100k da concepção (§8). O bloco de concepção tem dois
ramos: "encontrar um lowticket já no mercado" (minerar) e "criar do zero" (ideia própria), com a
entrada "não tenho nada / estou no zero" caindo em Mineração.

## 7. Fluxo de execução — 8 passos [CHECKLIST; aula 01:42, 02:15]

```
EXECUÇÃO ESTRATÉGICA (o 90/10)          EXECUÇÃO OPERACIONAL (se repete igual)
1. Mineração                           4. Página de vendas (técnica → blocos+copy → visual)
2. Modelagem                           5. Produto (MVP / modelo / completo)
3. Obra de Arte 100K com vantagem      6. Criativos (3 a 5 demonstrativos)
                                       7. Configurações técnicas gerais
                                       8. Tráfego pago
```

**Fluxo real do board** [CHECKLIST, print]: a estratégica é uma **cadeia com setas**,
Mineração → Modelagem → Obra 100K com vantagem, cada caixa ligada ao seu quadro de
tarefas. A operacional são **7 caixas em lista vertical, sem setas entre elas** (ordem
só de cima para baixo, não fluxo obrigatório): Página 01 · Página 02 · Produto ·
Página 03 · Criativos · Configurações técnicas · Tráfego pago. Os "8 passos" acima
agrupam as 3 páginas num passo só. Só as Configurações técnicas abrem um quadro grande
(Protectify, plataforma de vendas, Facebook Ads, UTMify). O cronograma do dia
[MATERIAL-FRAMEWORK, painel 14] desenha setas Página → Produto, Página → Criativos,
Criativos → Configurações e Criativos → Tráfego.

Checklist completo do board [CHECKLIST]:

- **Mineração:** montar planilha de mineração · separar palavras-chave (comando GPT)
  · abrir Biblioteca de Anúncios · pesquisar 10–50 concepções e salvar (passando no
  checklist 100k).
- **Modelagem:** entender e definir os 9 elementos (4 principais) de cada concepção
  · modificar um ou mais elementos (mapa da modelagem) · completar a modelagem de
  todas as concepções da planilha · selecionar 3 a 5 modelagens.
- **Obra 100K:** definir os 8 elementos da oferta · aplicar os 10 pontos de vantagem
  · selecionar 3 a 5 obras 100k para a fase operacional.
- **Página 01** (técnica): hospedagem (Hostgator) · domínio · WordPress · Elementor ·
  upload do modelo de página. **Página 02:** definir blocos (obrigatórios +
  opcionais) · criar a copy · implementar a copy. **Página 03** (visual): cores ·
  demonstrativo do produto · mockups · imagens · ícones.
- **Produto:** entregável MVP · entregável MODELO.
- **Criativos:** gravação de takes (tela, impresso, takes de rede social) · narração
  (sua voz ou IA) · edição (takes, narração, cortes, legenda, áudio) · exportar ·
  armazenar no Google Drive.
- **Configurações:** Protectify · plataforma de vendas (cadastrar produto, subir
  conteúdo, formas de pagamento, link de checkout nos botões, pixel na plataforma) ·
  Facebook Ads (BM, conta, pagamento, pixel, script do pixel na página) · UTMify
  (config + script de UTM na página).
- **Tráfego:** skill `metaads-kevones`.

**Ritmo** [aula 04:09–04:15; aula, cauda]:
```
Dia 1   → minerar (recomendado 50 concepções)
Dia 2   → entender (destrinchar os elementos) de todas
Dia 2/3 → modelar 1 a 3 direções por concepção
Dia 3/4 → selecionar e montar 3 a 5 Obras de Arte 100K
```
- "Um dia para cada fluxo, para fazer com qualidade." Nos 5 primeiros dias saem 3 a
  6 ofertas prontas; página + produto + criativo levam ~2 dias por oferta; a 1ª
  concepção vai ao ar com ~7 dias; depois a tendência é 3–5 dias por concepção
  [aula, cauda]. Operação dele: 1–2 dias [aula 00:06].
- Com 5 obras e 1 lançamento por semana = 5 semanas só de trabalho operacional
  [aula 04:15].
- Erro: "gasta 10 minutos pegando uma ideia e fica 2, 3 dias criando as coisas —
  tinha que ser o contrário" [aula 04:15]. "Se você ficar uma semana só criando obras
  de arte sem botar nada para rodar, isso não é perda de tempo" — perda é uma semana
  para uma só [aula 06:24].
- "É muito melhor você ter assertividade do que velocidade" [aula, cauda].

---

## 8. MINERAÇÃO — encontrar referência de concepção

Detalhe e prompts: `references/prompts-e-exemplos.md`.

**Onde:** Biblioteca de Anúncios do Facebook [MATERIAL-FRAMEWORK]. Há dois caminhos
para chegar numa concepção: a ideia surge no dia a dia, ou você vai atrás dela na
Biblioteca — no workshop foi a segunda [aula 02:24].

**Planilha (4 colunas):** URL da Biblioteca · página de vendas · concepção principal
· elementos da concepção [aula 02:15]. "Com quatro colunas você vira craque."
- **Não precisa** anotar quantidade de anúncios ativos nem tempo rodando [aula 02:15].
- Oferta vendida só no WhatsApp também serve — marca X na página de vendas.

**Ele não abre a página de vendas do concorrente ao minerar** (só na coleta; ao *entender*, no
dia 2, ele cola página/VSL/post/texto do anúncio no agente [aula 04:16:30]) [aula 01:22:16]: "Eu *não quero
saber o que a pessoa está entregando, não quero saber a página de vendas, nada*. Concepção eu
faço exatamente assim." E depois de modelar [01:35:29]: "eu não olhei a página de vendas, eu não
vi como que a pessoa tá vendendo e **eu não olhei os bônus, não olhei nada** — por isso que eu
falo, a biblioteca de anúncio é o ouro." Consequência prática: nada de análise de concorrente
na mineração, e **preço do concorrente não é olhado** — o preço já vem fixo do método
(R$17,90/R$27,90). A coluna "página de vendas" da planilha é registro, não etapa de estudo.

**Palavras-chave** [aula 02:27; MATERIAL-FRAMEWORK]:
- Tipos: nicho/subnicho, persona, **oferta** e **formato**. Use as de **oferta e
  formato**: amplas, trazem coisas diferentes. "O jogo da mineração não é você ficar
  olhando para onde está todo mundo olhando" — nada de receita, bolo de pote, pudim.
- Exemplos usados: `ebook`, `download imediato`, `acesso vitalício`, `oferta
  limitada` [aula 01:21, 02:30, 02:51].
- Gerar com o **Comando 1** (formato + valor/oferta + nicho) no ChatGPT.
- **Não fixar nicho no início:** "nicho só vai te confundir" [aula 02:06, 02:27].
- Oferta em **português, espanhol ou inglês** serve [aula 02:51].

**Checklist 100k — crivo rápido antes de salvar** [aula 02:33–02:48]:
consigo vender numa página de vendas? · vendo para quem já está no mercado (nível de
consciência)? · encaixa nas 10 características? · consigo um formato escalável? ·
consigo vender por R$17,90/R$27,90? · consigo transformar em algo que as pessoas
**querem**? · consigo aplicar modelagem? · consigo aplicar vantagem?

- "Esse checklist **não significa que a concepção que eu encontrei tem que cumprir
  tudo**. Significa que eu tenho que tentar **trazer ela** para esses objetivos"
  [aula 02:39]. Ex.: curso de bordado industrial → "20 modelos prontos de bordado
  comercial".
- O item "mais de 5 anúncios ativos, rodando há 2 dias" existia no checklist e ele
  **tirou ao vivo**: "isso aqui não é algo que vai entrar no nosso crivo mais… confunde
  mais as pessoas do que ajuda; não precisa ter anúncio ativo" [aula 02:48:30].
- Modelar oferta escalada ou não: "tanto faz… o jogo é a concepção"; dá para pegar
  até um **curso** e transformar em low ticket MVT [aula 02:15, 05:36].

**Do YouTube — detalhe em `references/concepcao-yt.md`:**
- **Gerar concepção do zero** (rota alternativa à Biblioteca): nicho+subnicho+persona →
  ChatGPT lista pensamentos internos de dor/desejo (amplos e técnicos) e os **mais
  urgentes** → persona detalhada → 10 ideias low ticket → fechar 1 e minerar/modelar.
  Não urgente é descartado; o GPT lista, o senso crítico é seu [YT xbWpBqDt8Ow]. Variante:
  partir do que o dono já sabe (ex.: checklist do 1º cliente em < 7 dias) [YT IcyJyf7X08k].
  *[Nota operacional, decisão do dono 25/09/2026 — não altera o método]:* na nossa operação, a ideia gerada por essa rota é só CANDIDATA (T7) e exige prova de mercado (alguém anunciando/vendendo, ou demanda medida) antes de seguir; nunca é apresentada ao dono como oferta. Ver `criacao-low-ticket-mvt` § REGRA DE FALA.
- **3 mercados macro:** dinheiro, saúde, relacionamento (com Deus e pessoas); nicho →
  subnicho → persona → pensamento interno. "Não é sobre nicho" [YT 68Q1cwhlpYE].
- **Sem concorrente na Biblioteca = oceano azul, se houver demanda** ("quando não tem
  ninguém rodando, eu adoro"); precisa de mercado pronto para comprar, não gente que nem
  sabe que a solução existe [YT eZNmYHP4uPc].
- **Raio X da oferta:** tabela por oferta concorrente (mercado, nicho, subnicho, persona,
  mecanismo, promessa, formato, tempo de acesso, suporte, garantia, bônus, order bump,
  preço) para ver o que têm em comum/diferente [YT M57JtDR3u-4]. Não contradiz o "não abro a
  página" acima: são dois momentos (coleta sem página; *entender* no dia 2 com página, VSL, post
  ou texto do anúncio [aula 04:16:30]). `concepcao-yt.md` §3.
- **Tempo do zero ao 1º teste de criativo:** 7 a 10 dias (máx. 12 para iniciante); ajuste
  de oferta que já vende: 2–3 dias [YT jgsK9kyWQn8].
- **Mineração = 3 perguntas (o quê, onde, como)** e mapa de qual comando de ChatGPT alimenta
  qual família de palavra-chave (nicho/subnicho → 2 e 3; persona → 4; oferta+formato → 1);
  ideia também nasce do dia a dia. Achar a **concepção**, não a oferta: vale oferta vendida no
  WhatsApp e concepção boa com produto ruim [YT -UTDJP5eSrc; `concepcao-yt.md` §8–9].
- **Decisão rápida de demanda e urgência**, 5 perguntas (cabe no low ticket, anúncio ativo, roda
  há 2–3 dias, aplico modelagem e vantagem, "dentre 1.000 pessoas, pelo menos uma compraria?")
  [YT -UTDJP5eSrc]. Nuance sobre "anúncio ativo/dias": ver §12.
- **Oferta de VSL também rende concepção** (extrai desejo e mecanismo, reformata em planilha/
  protocolo); **nicho complexo** vira peça específica de quem já faz (checklist, planilha),
  nunca curso do zero [YT uRmw73oj-tA; `concepcao-yt.md` §10].
- **Melhorar ≠ modelar:** manter persona, mecanismo e formato e só trocar palavras, bônus e página
  é "clonar com melhorias", não modelagem nem vantagem [YT uRmw73oj-tA; `concepcao-yt.md` §11].

**Separar coleta de análise:** "aqui eu não estou modelando, eu só estou coletando
ideias… se você for coletar e já quiser preparar a oferta, vai se embananar"
[aula 02:42]. Rendimento ao vivo: 6 concepções de UM termo (`download imediato`) [aula 02:53:01]
e 7 no total em < 30 min [aula 02:54]. Nos shorts ele fala em "uma, duas, três concepções para
cada palavra-chave" [YT cpmkuup83VY]; na aula o ritmo foi ~6 por termo.
- **Ideia solta** ("será que X vende?") ele não mede: pede a concepção — "50 tal coisas para tal
  coisa" — e "me fala os quatro elementos dessa concepção" [aula, cauda].

---

## 9. MODELAGEM — apontar para uma nova direção (o coração)

**Definição:** "identificar uma concepção/oferta que está ativa no mercado e (vende)
para usá-la como base e criar a sua própria versão. **Não é copiar.** É aprender com
o que funciona e reconstruir com originalidade" [MATERIAL-FRAMEWORK].
"Modelar é entender o que já dá certo e aplicar do seu jeito, pro seu público, com a
sua identidade."

**Por que modelar:** parte de algo com prova de venda · reduz o risco de errar na
concepção · ganha clareza sobre estrutura, comunicação e formato · coloca a oferta no
ar mais rápido · diferencia do mercado [MATERIAL-FRAMEWORK; aula 04:27].

**Passo 1 — entender e definir os elementos de cada concepção minerada** [aula
04:06–04:24]: manual (4 elementos) ou com o agente de concepção (9 elementos,
alimentado com texto da página, VSL, post ou texto do anúncio). "Muitas vezes vocês
nem analisam o que o ChatGPT trouxe… se você não entender o que está sendo vendido,
vai ter dificuldade na copy, no criativo e no produto" [aula 04:21]. "Uma das piores coisas
que você pode ter é estou vendendo algo e eu não sei o que tô vendendo" [aula 04:23:25]. Marca os
4 principais ("esse aqui seria o ponto número um" [aula 04:18:46]). **Teste de que entendeu:** só
com os elementos já dá para escrever a página — headline = produto + formato, subheadline =
desejo, bullets = resultado [aula 04:19:13].

**Passo 2 — modificar um ou mais dos 4 elementos** (mapa da modelagem). Na
modelagem você muda **pelo menos um** [MATERIAL-FRAMEWORK]:

| Elemento | Exemplo do framework | Ressalva do framework |
|---|---|---|
| Comunicação | "Guia da Dieta Low Carb para Mulheres" → "…para Homens acima dos 40" | busque personas que também **querem** a solução, não só precisam |
| Formato | "Ebook com 50 Receitas Detox" → "Planilha Interativa de Receitas Detox + Lista de Compras Automática" | só se a persona **realmente usa** o novo formato |
| Mecanismo | "Guia: organizar rotina espiritual com devocionais" → "Desafio de 7 Dias com Tarefas Gamificadas" | mecanismos mais atrativos, rápidos, fáceis, práticos, desejados |
| Nicho/subnicho | "Ebook Receitas de Pães" → "Receitas Lucrativas de Pipoca Gourmet" | posicionar em oceano azul, sem concorrência |
| Mais de um | "Ebook: exercícios para dor nas costas" → "Protocolo de exercícios para eliminar dores na coluna em 5 min/dia, ideal para idosos" (formato + comunicação) | — |

Nicho/subnicho "é onde a gente encontra as maiores possibilidades" [aula 04:36].
Curso grande → tirar uma peça de dentro e mudar o formato (ex.: "20 modelos de
placa-mãe e seus esquemas elétricos") [aula 04:33–04:36].

**Do YouTube — detalhe em `references/concepcao-yt.md`:**
- **Teste de reescrita:** tira "aprenda/domine/passo a passo" e põe "N coisas prontas"
  — a transformação sai implícita. "25 tipos de carne em mapa visual"; "10 estratégias
  para dobrar o lucro do Uber no fim do mês" (para quem já é motorista); "checklist para
  a horta produzir 2x"; "10 músicas prontas com partitura para casamento/culto";
  "20 projetos de caixa redonda" [YT t-BlrY5jVUw]. Nichar não basta.
- **3 erros essenciais:** concepção ruim (precisam, não querem) · oferta sem vantagem
  (mais do mesmo) · não entender a própria oferta (criativo/página/produto sem relação)
  [YT eZNmYHP4uPc].
- **Vantagem em < 10 min** numa oferta de mercado (fornecedores plus size: 200 → 250,
  bônus, garantia 7 → 90 dias, visual) [YT t-BlrY5jVUw].

**Cópia × modelagem** [YT 2hSIIWKZlBs]: a concepção é **uma frase** ("todos os 150 Salmos
explicados versículo por versículo"), com os 4 pontos principais. Anunciar a mesma concepção sem
modificar **pelo menos um** dos 4 (às vezes dois) é copiar — "mesmo trocando de cor, colocando mais
volume, isso é uma copiagem"; copia-se quando se tenta melhorar sem mudar a concepção.
**Expandir o campo de visão:** para um mecanismo, olha ~20 opções, vai a fundo em ~10 e define
**rodar 3**; o filtro é querem · demanda · ninguém vendendo (nem todo mecanismo tem demanda; Daniel
pode não ter). Pesquisa demanda no YouTube e no Uber Suggest (Salmos = livro mais buscado). Antes
de escolher, **entender o que a coisa é** ("o que é, para que serve, de onde surgiu": Salmos são
cânticos → "Salmos em música"). Ele descreve o "20, 30 anúncios ativos, rodando há X dias = oferta validada" como o
que o mercado ensina: "pode até dar algumas vendas", sem longo prazo nem escala. Na oferta do caso: 6 bônus, um deles o produto principal de outra oferta (Evangelhos
explicados), garantia de 30 dias, R$17,90/27,90.

**Passo que evita Frankenstein — primeiro elimine o que não faz sentido modelar**
[aula 04:39–04:45]. Painel dos Povos Indígenas: persona só faz sentido professor →
não modela; formato tem que ser PDF para imprimir → não modela; sobram mecanismo e
nicho/subnicho. "Se você modifica um elemento e o negócio não faz sentido, o negócio
piora." Isso é senso crítico, não precisa de ChatGPT.

**Explorar direções** conversando com o ChatGPT sempre a partir de uma ideia sua, e
pedindo "que tem demanda, que as pessoas querem comprar e que não tem ninguém
vendendo" [aula 04:48–04:57]. "Não tem problema fugir da concepção inicial — ela é o
ponto de partida", desde que continue dentro dos princípios [aula 04:57]. Modelar é pensar em
conversa, não em lote: "eu vou evitar usar o chat gpt para poder fazer vocês pensarem" [aula
04:52:32]; "não tem que fazer com velocidade, tem que fazer com qualidade" [aula 04:50:40].
**1 a 3 modelagens por concepção**, não 10: "eu não recomendo que você crie dez modelagens para
cada oferta" (7 concepções → ~21 modeladas) [aula 04:12:03]. As 10 ideias do comando de decisão
são para escolher, não para virar 10 ofertas. Eixos que ele usa além dos 4: **data/ocasião**
("as 5 datas com maiores demandas de compra" [aula 04:49:25]) e **pergunta de demanda antes de
modelar** ("eu poderia ter feito isso antes da modelagem" [aula 01:52:20]).

**Decidir** — Comando de decisão (10 ideias → as 3 que as pessoas mais querem comprar,
têm demanda e ninguém vende, com o porquê) [aula 01:51–01:54]. Exemplo de saída:
"biomecânica — a pessoa não acorda querendo biomecânica" [aula 01:54].

**Validar a direção escolhida** — "a última coisa que eu faria era vir na biblioteca
e verificar se encontro essa concepção" [aula 01:54]. Encontrou muita coisa vendendo
→ "eu não dou seguimento, aquele mercado já está populado"; troca de direção
[aula 05:03]. O framework lista, para "verificar se a sua nova concepção tem demanda,
as pessoas querem": **ofertas sobre a nova concepção na Biblioteca · Google Trends ·
YouTube + comentários (tá tendo comentário recente?)** [MATERIAL-FRAMEWORK]. Demanda
também se lê por senso crítico ("num grupo de mil pessoas eu encontro esse tipo de
pessoa querendo comprar isso?") e pelo ChatGPT [aula 01:12].

**Sinal de parada:** travou, opções "mais ou menos", concepção complexa, criativo
demonstrativo difícil → descarta. Ao vivo: "500 skills para Claude" descartada
[aula 05:03–05:12]: "essa oferta aqui é uma oferta que eu não seguiria" [05:11:28], senão "você
vai criar um frankstein" [05:12:29]. "Aquilo que você já bate o olho e consegue modelar
geralmente vai ser o caminho de mais resultado" [aula 05:12]. **Pools que ele evita:** IA/marketing
digital ("eu não gosto muito de trabalhar com esses nichos de inteligência artificial", métricas
mais caras [aula 05:04:58]); "N prompts de ChatGPT para tal coisa" ("já está saturado" [aula
05:06:42]); cético/emocional só vira produto para o **profissional** ("material para outros
hipnoterapeutas… se tiver muita gente rodando, não vai"; "são coisas mais céticas") [aula, cauda].

**Decisão tomada:** "Tomou a decisão, a decisão está tomada." Se seguiu o processo e
errou, "coloca o peso na metodologia, não em você" [aula 02:00].

**Lateralização:** acertou uma concepção → modela a própria oferta. Catálogo CNC →
luminárias (acertou) → 400 modelos cristãos → 140 relógios → 100 jogos educativos;
mesma página, mesma estrutura [aula 05:24–05:27].

---

## 10. OBRA DE ARTE 100K — modelagem + vantagem (o coração do low ticket)

"A obra de arte sem cá é o resumo da nossa oferta, da nossa concepção" [aula 06:21].
Documento = concepção modelada + 8 elementos da oferta + vantagens
[MATERIAL-FRAMEWORK]. Diagrama: oferta do mercado (vermelho) → oferta modelada
(laranja) → + vantagem = Obra 100K (verde) [aula 05:45].

**Os 8 elementos da oferta** [aula 05:48–06:06]: muitos já saem da concepção
(promessa ≈ desejo; nome = uma linha com as palavras-chave do produto; valor já
definido). O nome é o produto, sem inventar: "você não precisa inventar a roda" → "painel
educativo do dia do meio ambiente para professores" [aula 05:50:47]. A Obra é rápida ("a gente
consegue montar em 30 minutinhos" [aula 05:29:03]) e é onde se gasta energia ("gaste a sua
energia nisso aqui" [aula 05:48:23]). O que exige trabalho são **bônus e vantagem**. Existe um agente de oferta
que gera os elementos a partir da concepção — "o que o agente cospe é o que você vai
colocar na página" [aula 05:51–05:54].

**Valor de venda** [aula 02:24, 05:30, 05:48]: começa sempre em **dupla oferta**:
plano básico **R$17,90** (só o produto principal) e plano completo **R$27,90**
(principal + bônus). "Eu não vendo low ticket de R$10." O plano 1 é **âncora de
preço** que faz o plano 2 parecer muito mais vantajoso [MATERIAL-FRAMEWORK]. Existe
um framework de precificação com testes de preço na mentoria, não mostrado no
workshop [aula, cauda]. Caso real: completo convertendo > 85% → subiu para R$37,90 e
manteve a conversão [YT 4].

**Bônus** [aula 05:54–06:06; MATERIAL-FRAMEWORK]:
- "Geralmente eu boto de um a seis"; no exemplo, 4 [aula 05:54]. Em [YT 2hSIIWKZlBs]: "geralmente a gente coloca de quatro a seis bônus" (o caso Salmos teve 6).
- São **coisas complementares** ou **quebras de objeção**, e também são **coisa
  pronta**, nunca método.
- Critérios: quantidade (mais bônus relevantes) · qualidade (aceleram o resultado
  principal) · coerência (fazem sentido para o produto, não só para encher).
- "Não ache que a pessoa vai comprar por causa dos bônus… bônus não salva concepção
  ruim."
- **Não guarde o ouro para o order bump:** "o que vende é aquilo que a pessoa vê
  primeiro" [aula 06:00]. Order bump entra no checkout, geralmente no 2º dia, e não
  precisa esperar validar [aula 05:36; aula, cauda].

### Mapa da Vantagem — 10 pontos [MATERIAL-FRAMEWORK; aula 06:09–06:21]

**Definição:** comparar 1 a 2 ofertas já existentes no mercado e criar uma terceira
opção superior/mais vantajosa. A oferta deve gerar a sensação "estou ganhando ao
comprar isso" e "isso está melhor do que as outras ofertas".

- "A vantagem é invisível, mas perceptível: *não sei por quê, mas gostei mais desse
  aqui*."
- "No cérebro do cliente, comprar é decisão emocional — e a emoção que mais converte
  no low ticket é *estou ganhando algo bom*."
- Por que aplicar: o cliente compara o tempo todo · o mercado está saturado de mais
  do mesmo · vantagem gera sensação de ganho · o público sente a diferença mesmo sem
  saber explicar.

**Tarefa 03:** a partir da oferta modelada + mapa, passar pelas 10 categorias,
**marcar SIM ou NÃO** e escrever a vantagem. Não precisa aplicar nos 10.

| # | Ponto | Como aplicar (framework) | Exemplo |
|---|---|---|---|
| 1 | Produto principal | mais prático, clareza do resultado, ferramentas internas, melhor estrutura | guia teórico → guia prático com planilhas e modelos de copy |
| 2 | Bônus | quantidade, qualidade, coerência | 3 bônus genéricos → 6 complementares que somam R$300 |
| 3 | Mecanismo da solução | simplificar processo, alterar método, diferencial lógico | "rotina de 30 dias" → "desafio de 7 dias com plano diário" |
| 4 | Comunicação | persona mais específica, linguagem simples, "feito pra mim" | "para mulheres" → "para mães acima dos 40 sem tempo de treinar" |
| 5 | Promessa | resultado + tempo + facilidade; tirar exagero; evidência | "aprenda inglês rápido" → "200 frases essenciais em 10 dias" |
| 6 | Garantia/risco | reduzir medo; garantia como diferencial | "Teste 15 dias; se não gostar devolvo e você fica com o material" |
| 7 | Tempo e facilidade | acelerar, sem equipamento, mostrar economia | "7 dias" > "30 dias" |
| 8 | Visual/apresentação | design profissional, mockups, organização | concorrente "feito no Word" |
| 9 | Acesso/suporte | vitalício, suporte humano, grupo opcional | "o concorrente vende e some" |
| 10 | Nome do produto | fácil de lembrar, específico, benefício, identidade | "Planilha Financeira" → "Mapa da Liberdade Financeira Cristã" |

Aplicado ao vivo (Povos Indígenas → Painel do Meio Ambiente) [aula 06:15–06:21]:
produto SIM (material visual superior) · bônus SIM (concorrente não tinha nenhum) ·
mecanismo NÃO (só trocou a data) · comunicação SIM (mais específica) · promessa SIM
(mais direta) · garantia SIM (15/30 dias; "reembolso é muito baixo") · tempo NÃO ·
visual SIM · suporte SIM (**e-mail no início**, nada de WhatsApp nem recuperação de
venda de R$17,90) · nome SIM. Muitas vantagens já saem aplicadas do processo anterior
[aula 06:27].

**Selecionar 3 a 5 obras** para a fase operacional [CHECKLIST; aula 06:24]. **Na aula a
seleção é sem cor**: 3 a 5 modelagens → Obras → "de todas aquelas, selecionamos de 3 a 5 obras
de arte" + "uma ordem de execução" [aula 04:12:50; 06:25:55; 06:07:50] (0 ocorrências de
"semáforo" na aula de 11h e na cauda). O Semáforo abaixo é **outra fonte** (extra do YouTube).

### Semáforo das Decisões — filtro das Obras antes de rodar [YT 10; board MOD 04 "Execução Estratégica"]

**Não vem da aula de 11h.** Conteúdo da mentoria, publicado no YouTube (vídeo `M4cT8gIfilo`, transcrição
`transcricoes/08-youtube-extras/10-semaforo-das-decisoes-avaliar-antes-de-testar.txt`).
Print do board: `references/docs/boards-mentoria/semaforo-das-decisoes-MOD04.png`.
**Quando:** só DEPOIS de minerar tudo, modelar tudo e montar todas as Obras de Arte
— "somente depois que você tiver as suas obras de arte prontas, você vai passar pelo
semáforo". Pergunta que ele responde: *"essa obra de arte está pronta para eu colocar
dinheiro, energia e execução nela?"* — não "a ideia é boa ou ruim".

| | 🟢 VERDE — vamos rodar | 🟡 AMARELA — precisa de ajuste | 🔴 VERMELHA — não vamos rodar agora |
|---|---|---|---|
| Objetivo | rodar agora: dinheiro, energia, execução | descobrir o que falta para virar verde | identificar o que está fora da metodologia |
| Sinal principal | **Fator UAU** — "caraca, isso aqui é diferente" | "tá legal, mas falta algo" (sem fator UAU) | **mais do mesmo**, sem diferencial claro |
| Tipo de produto (§2) | entrega pronta OU complexo → simples | cumpre parcialmente | fora da metodologia |
| 10 mandamentos (§3) | cumpre todos | cumpre a maioria (ou até todos) | não cumpre (basta falhar um) |
| Demanda | forte, comprovada | existe, mas é mais "precisam" que "querem" | sem demanda definida / ninguém procura |
| Intenção de compra | as pessoas **querem** comprar | as pessoas **precisam** | precisam, mas não querem comprar agora (sem urgência) |
| Concorrência | ninguém vendendo daquela forma | já tem algo parecido | mercado saturado, mais do mesmo |

- **Verde** = passou pelos 3 critérios (tipo de produto MVT · 10 mandamentos ·
  direção de ouro "querem comprar + tem demanda + ninguém vendendo") **E** gera o
  fator UAU. "Muitas concepções verdes têm esse tempero na comunicação."
- **Amarela** — 3 ajustes que costumam virar verde (nem toda amarela vira):
  1. **Mais específica** — "não é nichar, é colocar mais detalhes na comunicação":
     "100 modelos de mouse" → "+100 modelos de mouse para programadores e
     desenvolvedores que querem aumentar a produtividade".
  2. **Detalhar a transformação** — resultado explícito, antes/depois da solução
     (não transformação completa; deixar mais tangível).
  3. **Reposicionar a comunicação** — mudar a frase, a direção ou o recorte (nicho,
     subnicho, formato, mecanismo, persona). Trabalhou e não melhorou → vira vermelha.
- **Vermelha** — 3 causas que aparecem rápido: (1) fora da metodologia (não cumpre
  os 10 mandamentos ou os 2 tipos de entregável); (2) sem demanda real (ninguém
  procura/fala do assunto); (3) precisam mas não compram (falta urgência/intenção).
  Também: "encaixa, as pessoas querem, mas já tem muita gente vendendo" ou "ninguém
  vende, mas as pessoas também não querem".

**Ordem prática:** (1) mata as vermelhas primeiro — de ~20 obras, analisando com
rigor, **30–50% saem vermelhas** ("numa lista de 10 ideias, 5–6 vão ser
vermelhas"); (2) puxa as verdes — "quais são as mais diferentes?"; (3) o que sobra é
amarela → aplica os 3 ajustes. Depois: **lista de prioridades** (próxima aula da
mentoria, não publicada). Pode mandar a tabela + concepção pro agente de concepção
ajudar a validar, "mas não vá só pela validação do ChatGPT".

**Exemplos reais dele:**
- 🟢 "+200 folhas de exercícios bilaterais para desenvolver coordenação motora
  infantil" (nicho concorrido de atividade infantil, mas mecanismo e comunicação
  novos; ninguém vendendo) · "+100 pixel arts imprimíveis para colorir e desenvolver
  foco, concentração e raciocínio lógico" (colorir → pixel art; "não era tirar da
  tela, era desenvolver foco"; primeiros a lançar) · "exercícios de fortalecimento
  para corredores — melhorar desempenho e reduzir risco de lesão", depois
  **lateralizado para ciclistas**.
- 🟡 "50 receitas de airfryer para quem mora sozinho" · "30 atividades para mães
  diminuírem o tempo das crianças no celular" · "+100 prompts de ChatGPT para
  corretores de imóveis" — encaixam, mas cheiram a mais do mesmo.
- 🔴 ebook de receitas para emagrecer (genérico, saturado) · guia de finanças
  pessoais (saturado) · "desenvolva mentalidade vencedora" (jornada/transformação,
  foge do MVT) · pack de arte editável para barbearia (é MVT, mas muita gente
  vendendo) · kit de currículo pronto (precisam mais do que querem).

**Verde não garante venda** — "traz paz pro coração e te mantém no processo";
testar só vermelha é que garante não ter resultado. Exercício sugerido: passar
ofertas antigas que não venderam pelo semáforo.

Mudou algo depois (mecanismo, produto)? "Você vai ter que modificar em tudo" —
página e criativo não podem falar coisas diferentes [aula 06:27].

---

## 11. Execução operacional — resumo

"Essa é a parte operacional, que não muda. Ela se repete para todas as ofertas. Os
mesmos modelos, as mesmas tarefas, as mesmas estruturas, as mesmas configurações"
[MATERIAL-FRAMEWORK]. Detalhe completo em `references/pagina-produto-criativo.md`.

- **Página:** 3 pilares (comunicação, estrutura, visual) · 10 blocos obrigatórios em
  ordem fixa · 9 opcionais só quando necessário · copy de **clareza e
  especificidade, sem persuasão, sem gatilho, sem história, sem curiosidade** ·
  headline sobre o produto, uma única interpretação · a copy sai da Obra de Arte ·
  template no WordPress + Elementor, não IA gerando página [aula 06:45–07:27].
- **Produto:** "se você não entende o que está vendendo, não consegue criar o
  produto" · MVP (não perder 30 dias criando) → modelo (páginas diagramadas para
  criativo e página) → completo · ChatGPT, Canva, bibliotecas gratuitas, PLR com
  revenda [aula 08:15–08:54; aula, cauda].
- **Criativo demonstrativo:** 3 a 5 · "se a pessoa precisa imaginar o produto, o
  criativo está errado" · 4 componentes: copy, visual (takes), narração, edição ·
  copy em 3 partes (início = headline da página; meio = subheadline + benefícios;
  fim = "clique em saiba mais") · o criativo de 2023 e o de 2026 têm a mesma
  estrutura [aula 00:21–00:24, 07:45–08:00].
- **Configurações técnicas:** Protectify · plataforma de vendas (Hotmart) · Facebook
  Ads · UTMify [aula 08:42–09:15].
- **Tráfego:** skill `metaads-kevones`. (Do Heitor fica só: "tráfego não faz milagre; o que faz milagre é a concepção".)

---

## 12. Regras rápidas do próprio Heitor

- Dois tipos de produto; nada de curso/transformação/cético.
- Querem + demanda + ninguém vendendo + dentro dos princípios.
- Não focar nicho no início; minerar por palavra de formato/oferta.
- Quantidade de anúncios e tempo rodando **não entram no crivo da coleta** [02:19, 02:48:30,
  05:36]; sobre o nº de anúncios ele diz "isso daí é crença" [05:35:43] e "isso daí não diz nada"
  [05:37:20] — leitura neutra na aula. O que o método trata como erro é a **concepção populada**
  ("mais do mesmo", erro nº1 dos 8; "muitos anúncios ativos" em caixa vermelha na coluna "O QUE O
  MERCADO TE ENSINA" do board = o jogo de copiar), não o nº de anúncios em si. Na *decisão/validação
  da direção* ele faz leitura solta: [01:56:40] "37 anúncios, tá vendendo… é um cara que tá tendo
  resultado"; em [YT -UTDJP5eSrc] "passou de 10 já é OK" e "2, 3, 7 dias". Nunca formaliza como
  regra: na coleta, ignore; na validação, no máximo leitura solta, nunca crivo.
- Concepção achada não precisa cumprir o checklist — o trabalho é trazê-la para ele.
- Primeiro elimine o que não faz sentido modelar; travou → descarta.
- Dupla oferta R$17,90/R$27,90; nunca R$10.
- Bônus 1–6, complementares ou quebra de objeção, coisa pronta.
- Página: 10 blocos na ordem, copy sem persuasão, headline de produto; sem VSL (no
  máximo vídeo de 1–2 min demonstrando o material, opcional) [aula 06:30].
- Produto sem expert: "entrego uma coisa pronta, não vai precisar de autoridade"
  [aula 04:00].
- Suporte só por e-mail no início [aula 06:21].
- Criativo demonstrativo, congruente com a página.
- Capital inicial: ~R$1.000 [aula, cauda].
- Insistir numa concepção: decisão em 3–7 dias, não 2–3 semanas [aula 03:57–04:00].
- Empilhar ofertas (depois de acertar a primeira); nunca depender de uma só [YT 9].
- Iniciante: "começa com **uma** oferta, foca em uma" [YT uRmw73oj-tA]; a conta dele roda 4–5
  projetos em fases diferentes [YT 3tBWZ76Du04].
- Recuperação de vendas pendentes só depois de a oferta acertar e com volume alto; no início não
  [YT uRmw73oj-tA]. Só Brasil: ele hoje não faz oferta Latam nem para fora [YT J9X4FCcgb30;
  YT uRmw73oj-tA]; a linha "português, espanhol ou inglês serve" é da coleta [aula 02:51].
- Prazo: no workshop a 1ª concepção sobe com ~7 dias; em [YT jgsK9kyWQn8] ele fala em
  7 a 10 dias até o teste de criativo (máx. 12 para iniciante) e 2–3 dias para ajustar
  oferta que já vende.
