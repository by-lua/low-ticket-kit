---
name: modelagem-escalados
description: MECÂNICA de estático/carrossel chamada pela skill `criativo-ads` (porta de entrada de todo criativo; estratégia e quantidade moram lá). Modela criativos de anúncio a partir de uma biblioteca local de 103 formatos que já estão escalando (87 estáticos, 16 vídeos, 47 categorias) — anexa a referência real no ChatGPT e adapta para a marca do usuário via pipeline de 12 prompts (brandkit, dossiê, matriz de ângulos, seleção de formato, leitura estrutural, copy, arte 1:1 1080×1080 (9:16 só se pedido), leva de headlines, reenquadramento, gate de QA, ponte para vídeo, nomenclatura). Use quando o usuário pedir criativo estático, modelar/clonar um criativo que está escalando, "modelagem de escalados", leva de anúncios, variação de headline, banco de formatos, biblioteca de anúncios, ou mencionar Antonio Ferriani, formatos escalados, antes e depois, print de WhatsApp, caixa de perguntas, Reclame Aqui, notícia, ilustração como formato de anúncio.
---

# modelagem-escalados

Produção de criativo **por modelagem**: em vez de inventar layout, você parte de um
formato que já está rodando com verba, anexa o arquivo real como referência e adapta
para a marca do usuário.

O que esta skill tem que um prompt solto não tem: **as referências estão em disco**.
103 arquivos baixados, organizados por tipo e categoria, com transcrição dos vídeos.

## DOUTRINA — o criativo valida o público (regra 2026-09-21)

**PRINCÍPIO-MÃE:** o criativo tem que SAIR como se fosse orgânico. Nada inventado
de IA, nada exagerado, **nada clean/perfeito** — acabamento de agência denuncia
que é anúncio e mata a entrega. Imperfeição real (foto de celular, luz torta,
cenário comum) vende mais que render impecável. E o caminho padrão é **partir
sempre de um MODELO VENCEDOR da biblioteca de escalados** (`scripts/buscar.sh`) —
modela o que já roda com verba, não inventa layout do zero. Da referência
vencedora → adapta pra marca → sai orgânico.

Meta usa o CRIATIVO pra achar e validar o público. Estático que não diz pra quem
é = leilão largo = CPM caro (visto na prática: R$400 → R$1200 CPM num criativo
neon lindo e vazio, sem rosto, sem dor, sem público nomeado). CPM alto quase
nunca é "público ruim" — é criativo que não comunica.

**No estático, quem valida o público é a HEADLINE + a cena.** A headline nomeia
a persona: *"Empresário, seu site tá velho e desatualizado?"*, *"Dono de
comércio sem site perde cliente todo dia."* — o leitor se reconhece. Uma leva =
várias headlines, uma por persona **e dor**; mesma arte, troca o texto (é a leva de
headlines do prompt 08). Trocar só a forma da frase com a mesma dor não conta
como variação: o Meta agrupa como o mesmo anúncio (Kevones 2026).

**O maior erro é ter cara de IA.** Facebook/Instagram são redes de ENGAJAMENTO —
o feed premia conteúdo nativo e enterra o que grita "anúncio". Criativo com
estética artificial (mockup neon, mesa gamer RGB, render 3D limpo demais) ou
"bonito/cool demais" quebra o nativo, o engajamento despenca e o **CPM dispara**.
Cenário e composição têm que parecer **post orgânico / foto real** tirada por uma
pessoa — não peça de agência, não render. Isso é o que baixa o CPM. Direção que
funciona:

- **Fundo orgânico e real:** ambiente de escritório de verdade, laptop aberto
  numa mesa comum com uma página real na tela — não render neon, não cenário
  premium-tech. A estética tem que bater com o preço (acessível, não luxo).
- **Texto com cara de Stories:** fonte tipo legenda de Story, linha fina, texto
  simples por cima da foto — não banner de oferta gigante.
- **Rosto humano ou alto contraste no topo** para parar o scroll.
- **Formato padrão de estático e carrossel = 1:1 (1080×1080), todos os cards** (regra
  da dona, 04/10/2026). Monte direto nesse canvas; 4:5 ou 9:16 só se o usuário pedir.
  Vídeo continua 9:16 (ver `criativo-ads-video-orq`).
- **1 público por peça.** Dois públicos na mesma arte = algoritmo não estreita = caro.
  Se o produto serve QUALQUER nicho (ex. SiteExpress), mire o **bucket largo**
  (empresário, dono de comércio, autônomo, prestador de serviço) — **não** um nicho
  específico. Fixar em "nutri"/"advogado" joga fora o resto do público que compra.
- Palette da marca atual: **azul é a identidade/paleta (IPP); laranja SÓ no CTA/botão**, não espalhado. (MinhaEmpresa — não o violeta velho.)

**"Empresário" é só um exemplo — a persona varia.** Método pra gerar as headlines
de uma leva (alimenta a matriz de ângulos do prompt 03):

1. **Liste TODA funcionalidade da entrega** — tudo que o produto faz/inclui.
   Uma linha por funcionalidade.
2. **Cada funcionalidade vira um ângulo** — o benefício/dor que resolve.
3. **Cada ângulo puxa uma persona/role** que sente aquela dor.
4. A headline = persona + ângulo. Leva = 1 headline por (persona×ângulo), mesma arte.

Assim a leva cobre vários públicos de propósito e o algoritmo valida qual role
converte — sem chutar "empresário".

**O texto do anúncio (copy primário) também valida o público** — não é só a arte.
Primeira linha do copy nomeia persona + dor, igual à headline. Copy genérico =
leilão largo. 1 persona por variação.

**Palavras que inflam o CPM — evite:**
- Atributo pessoal na 2ª pessoa ("você está endividado", "você é gordo", "você
  tem mais de 50") → política de atributos pessoais do Meta, penaliza. Reescreva
  impessoal: "quem tá...", "pra quem passou dos...".
- Sensacionalismo/promessa ("garantido", "100%", "ganhe dinheiro fácil", CAIXA
  ALTA excessiva, excesso de !!! e emoji).
- Nicho sensível (saúde/dinheiro/emagrecimento) dito como afirmação sobre a pessoa.
Prefira dor + prova + benefício concreto, 2ª pessoa neutra ou 3ª pessoa.

**Ponto de partida de teste de criativo:** a primeira peça de uma leva junta
**DOR + PÚBLICO LARGO**. Uma boa **PERGUNTA** (que faz a persona parar e pensar
"isso sou eu") e um bom **COMEÇO/abertura** já são um ótimo começo de teste —
antes de abrir novas dores, valide se dor+público comunicam.

**Regras de criativo do Kevones que valem para estático (YouTube 2025/26):**
- **Imagem vende quando o produto cabe numa frase de banner.** Produto complexo ou
  muito de nicho pede vídeo (prompt 11 → `criativo-ads-video-orq`). [tTJNpAVAs5I]
- **O estático direto** (produto + o que faz + CTA, sem história) é o mais fácil e
  o que mais vende no produto dele. Variante "cara de tweet". [xmaToxt7OiE, aUYGsoHUb2w]
- **O carrossel também é criativo de teste:** carrossel de objeção ("Será que X vale
  a pena?" → um card por objeção → CTA) e carrossel de história (problema →
  produto → final feliz).
- **Carrossel demonstrativo "iPhone cru"** (imagem crua de celular + mockup + benefícios/garantia + ~4 páginas reais do entregável): receita em `references/carrossel-demonstrativo-iphone.md`. Está dando muito certo.
- **Um ângulo, três formatos:** a mesma dor vira vídeo, carrossel e estático (uma
  frase). A leva de teste mistura formatos.
- **Quantidade:** teste de low ticket com 3 a 5 peças no máximo; depois de validar,
  ~3 peças novas por semana, cada uma com dor nova. Não suba 10 de uma vez numa
  conta que já vende.
- **Remarketing** usa peça de objeção, depoimento ou cupom, nunca a mesma peça do
  público frio.
Detalhe e fontes: `criativo-ads` (`references/kevones-criativo.md`) e `metaads-kevones`.

**Quem coloca o texto: prefira o próprio GPT (texto orgânico), não overlay de
código.** Peça pro GPT já gerar a imagem COM o texto — headline/CTA — no estilo
**legenda de Story do Instagram** (fonte sans nativa de Story, do jeito que uma
pessoa escreveria num Story), com as cores da marca (azul + gancho/CTA laranja).
Texto colocado pelo GPT sai com cara de post orgânico; overlay de código sai
"perfeito demais", com cara de anúncio. No prompt do GPT, diga o texto exato, a
fonte estilo Story, as cores e a banda segura. **QA de ortografia obrigatório:**
modelo de imagem erra letra/acentuação — confira palavra por palavra e regenere
se saiu torto. Só cai pra overlay de código se o GPT insistir em errar o texto.

**Receita que funcionou (referência AD06 SiteExpress):** cena de mesa/home-office
**sem pessoa**, laptop aberto mostrando um **site profissional de verdade na tela**
(a tela é a prova visual — mostra o produto), café + caderno, luz de janela. Texto
embutido pelo GPT em **fonte handwritten estilo legenda de Story** (não sans dura),
gancho e CTA em laranja sobre madeira/fundo escuro. Saiu orgânico, legível,
ortografia certa. Guardado em `ofertas/assinatura-site-mensal/criativos/AD06-organic.png`.
Use como molde de novas peças/levas.

**Receita vencedora 2 — Story nativo (referência AD07 SiteExpress, modelado do
formato "Estilo Stories #3" da biblioteca):** print de Story PATROCINADO do
Instagram, o mais orgânico do banco. Estrutura:
- Foto POV tela cheia, cara de foto de celular real: cenário do público (ex.
  balcão de comércio de bairro, maquininha, caderno, plaquinha escrita à mão).
- Chrome de Story NATIVO por cima: barra de status do iPhone (hora/wifi/bateria),
  barra de progresso, seta voltar, @perfil pequeno + "Patrocinado", curtir/comentar,
  card "Saiba mais" azul no rodapé, nav do IG embaixo.
- Headline com REALCE AZUL (fundo azul claro, texto azul): pergunta/relato-gancho.
- Caixa PRETA texto branco: o relato em 1ª pessoa (dor → virou o jogo com o
  produto → CTA "Toca em Saiba mais").
- Texto TODO embutido pelo GPT (anexa a referência #19), QA de ortografia.
Passa como Story real, não anúncio → engajamento alto, CPM baixo. Molde em
`ofertas/assinatura-site-mensal/criativos/AD07-story-nativo.png`. Referência do
banco: `biblioteca/formatos/estatico/estilos-stories/19-estilo-stories-3.webp`.

**Legibilidade do texto sobre foto:** texto sobre foto SEMPRE com contraste —
stroke escuro ou sombra/drop-shadow por baixo. A palavra em laranja só se lê
sobre fundo ESCURO; laranja some sobre área clara (tela de laptop acesa, parede
clara, céu). Se o gancho cai numa zona clara, ou escurece o fundo atrás dele, ou
troca a cor de destaque ali. Sem logo/marca desnecessária poluindo a peça.

Gate: **teste de 1 segundo** — estranho olha 1s e sabe (a) PRA QUEM é e (b) a
DOR. Não passou, não sobe. Passa nesse gate no prompt 10 (QA) antes de gerar.

## Onde está tudo

```
biblioteca/                     → ~/.claude/biblioteca-escalados (symlink)
├── CATALOGO.md                 103 formatos, agrupados por tipo e categoria
├── catalogo.json               metadados (id, tipo, categoria, título, transcrição)
├── formatos/estatico/<cat>/    87 imagens
├── formatos/video/<cat>/       16 vídeos + 13 .txt de transcrição
└── prompt-etapa1-produto.md    os 2 prompts originais, preservados como estão
    prompt-etapa2-referencias.md
prompts/01..12                  o pipeline desta skill
scripts/buscar.sh               busca no catálogo
```

Buscar:

```bash
scripts/buscar.sh                    # categorias com contagem
scripts/buscar.sh whatsapp           # por termo
scripts/buscar.sh --tipo video       # só os 16 vídeos
```

## O pipeline — 12 prompts

Os 2 prompts originais do Ferriani viraram 12. O que ganhou: brandkit separado
(rodado uma vez por marca, não recolado a cada peça), matriz de ângulos antes da arte,
copy travada antes de gastar geração, gate de QA, e ponte para vídeo.

| # | Prompt | Roda | Sai com |
|---|---|---|---|
| 01 | `brandkit` | 1× por **marca** | design system em ficha + parágrafo colável |
| 02 | `dossie-produto` | 1× por **oferta** | dores/desejos + **bloco canônico de oferta/preço/garantia** |
| 03 | `angulos` | 1× por **leva** | matriz persona × dor × promessa × objeção |
| 04 | `selecao-formatos` | você, não o GPT | tabela ângulo × formato × arquivo |
| 05 | `leitura-referencia` | com refs anexadas | 13 eixos + mecanismo de cada formato |
| 06 | `adaptacao-copy` | antes de gerar | copy por peça, aprovada por você |
| 07 | `arte-stories` | gera | 1:1 1080×1080 (9:16 1080×1920 só se a dona pedir Stories/Reels) |
| 08 | `leva-headlines` | pós-vencedor | N headlines na mesma arte, **cada uma com outra dor/persona** |
| 09 | `feed-e-outras-proporcoes` | **sempre** | 1:1 1080×1080 (padrão de estático/carrossel); 4:5 se pedido |
| 10 | `gate-qa` | você, não o GPT | aprovada / reprovada / refazer copy |
| 11 | `modelagem-video` | formatos de vídeo | briefing p/ `criativo-ads-video-orq` |
| 12 | `nomenclatura-entrega` | fim | nomes + `leva.md` + conferência |

Leia o arquivo do prompt antes de usar — eles têm regra, não só template.

## Execução

**Mecânica de browser:** delegue para a skill `gpt-imagem-playwright` (perfil `gpt`,
já logado). Esta skill decide **o quê** anexar e **o que** pedir; aquela sabe clicar.

Ordem mínima de uma leva do zero:

1. `01` uma vez → salve `brandkit.md` na pasta do projeto
2. `02` → confira o que voltou como `NÃO INFORMADO` antes de seguir
3. `03` → N ângulos
4. `04` → escolha os N formatos no catálogo (**abra as imagens**, não escolha pelo nome)
5. Nova conversa no ChatGPT: cole `02` + brandkit, anexe capa/mockup/logo
6. Anexe as N referências + cole `05` → leitura estrutural
7. `06` → aprove a copy
8. `07` → **anexe a referência de novo** e gera as artes
9. `10` → gate. Reprovada volta pro 06 ou 07, não sobe "pra testar"
10. `09` → confirma formatos: 1:1 padrão; 9:16 extra só se pedido
11. `12` → nomeia e entrega

## Regras que não se negociam

1. **Copie a peça, troque o contexto.** Layout, grade, hierarquia, tipografia, cor
   e acabamento da referência ficam **como estão** — a peça nova tem que ser
   reconhecível como a mesma arte com outro produto dentro. O que se substitui é
   copy, produto/mockup, fotos e fundo, e toda identidade de terceiro (rosto, logo,
   marca, embalagem). Redesenhar em "estilo da marca" é perder o que o escalado já
   provou. O brandkit governa assinatura e vocabulário — **não a cor de destaque nem
   a composição**, nem quando a referência parece neutra. Cor de acento (verde,
   vermelho, dourado etc.) da referência entra como está; trocar por verde da marca
   por padrão foi erro registrado (correção do usuário, 2026-09-10): "vc fez mudando
   as coisa mano so pega a ref e coloca o texto". Só recolora se o usuário pedir.
   Ao trocar o produto/objeto por um equivalente do que está sendo vendido, mantenha
   o mesmo tratamento fotográfico da referência (mesma luz de estúdio, mesmo ângulo,
   mesma composição de reflexo/sombra) e peça explicitamente **realismo de produto
   real** — sem UI cartunizada, sem proporção distorcida, sem "cara de IA". Uma tela
   (laptop, celular) em cena precisa mostrar conteúdo plausível e legível na
   composição (headline curta, nav bar, blocos), não texto placeholder óbvio.
2. **Prova não se fabrica.** Sem depoimento real no dossiê, não entram os formatos
   Depoimento em direct, Reclame Aqui, Email recebido nem número de aluno. Isso não é
   preferência estética.
3. **Nenhuma identidade de terceiro sobrevive.** Nome, rosto, logo ou perfil que
   aparecem na referência saem da peça final.
4. **Safelines são medidas, não aproximação.** 250 px topo, 350-400 px base, 50 px
   laterais. CTA nunca na base.
5. **Abra o arquivo.** Antes de escolher a referência e antes de aprovar a peça.
   Avaliar pela descrição que o modelo deu da própria imagem é como o erro entra.
6. **Copy antes de arte.** Gerar imagem com copy não aprovada é queimar geração.
7. **Oferta, preço e garantia são texto travado.** Saem do bloco canônico do 02 e
   atravessam 06, 07 e 09 sem uma vírgula mudada. Valor errado na arte é verba
   queimada e risco de reprovação na Meta. Onde o preço não pode aparecer, o campo
   diz `OMITIR` — nunca vira "investimento acessível".
8. **A referência vai anexada também no 07.** O 05 lê, o 07 gera; gerar sem o arquivo
   à vista faz a peça escorrer para template genérico.
9. **Estático e carrossel saem em 1:1 (1080×1080) por padrão, todos os cards.** 9:16
   só entra como formato extra quando o usuário pedir. Carrossel demonstrativo: as
   páginas do entregável são arquivos reais encaixados no 1:1; GPT nunca desenha
   página do produto (ver `references/carrossel-demonstrativo-iphone.md`).
   **Só o card 1 (capa) é arte gerada** — os demais cards são só páginas reais do
   entregável, recortadas full bleed em sequência do início ao fim (dona, 09/10).
   E todo prompt de geração anexa **2–3 imagens do entregável** como referência e
   declara estilo orgânico + título + estilo + história — sem isso, a arte sai
   "inventada" (reprovou no Tarot, 09/10). Capa-referência aprovada de low ticket:
   `criativo-ads/references/capa-referencia-low-ticket-jj.png` (dona, 08/10).
10. **Um formato por ângulo, no máximo 2 peças por categoria.** Duas peças com a mesma
   persona e a mesma dor são um anúncio só — e a Meta lê assim.
11. **Entregável em PDF/guia: use a composição de mesa validada.** Tablet/celular em
   pé mostrando a capa, cercado de 3-5 páginas reais espalhadas (nunca empilhadas
   retas) + props do nicho, nunca fundo vazio — é a fartura de objetos que vende
   "material completo" sem precisar dizer isso em texto. Referência completa e os
   arquivos reais na skill `criativo-ads-video-orq`, §E.0b — pasta global
   `references/composicao-mesa-entregavel/` dentro dela (9 `ref-demonstrativo-*.png`
   + mockups tablet+folhas). Vale tanto pra estático (aqui) quanto pra vídeo (lá) —
   é a mesma composição. **Variação livre (dona, 08/10):** nem toda peça usa a
   composição de mesa — o entregável pode aparecer impresso, no celular, no notebook,
   no tablet, dois aparelhos ou um só; misture os formatos entre peças. O proibido é
   repetir sempre as mesmas imagens de entrega.
12. **Card de página real: sem moldura — preenche o card.** A página/parte real entra
   de ponta a ponta (full bleed); página centralizada "com respiro" e borda branca
   sobre fundo escuro foi reprovada pela dona ("borda feia", 08/10). Recorte é livre:
   pode cortar um pedaço da imagem, inclusive o fim de uma fonte longa/PDF — o que
   importa é o conteúdo aparecer do início ao fim, card a card. Detalhe do encaixe em
   `references/carrossel-demonstrativo-iphone.md`.
13. **Imagem gerada do produto: anexa CAPA + 2/3 PÁGINAS REAIS, e o modelo escolhe 2
    (dona, 09/10).** Anexar só a capa reprovou ("só a capa?" — a arte sai sem o
    produto aparecendo). No `gpt-imagem-playwright`: 1 capa + 2/3 páginas reais do
    entregável (`refs/`, `produto/PDF/` ou as páginas já cortadas daquele criativo) e
    no prompt manda o modelo **escolher DUAS** das páginas pra mostrar impressas/na
    tela — "nem muito, nem pouco". As páginas visíveis são arquivo real; o modelo só
    posiciona. Encaixe das páginas no card = item 12.

## Vídeo

Os 16 formatos de vídeo **não** se modelam aqui. Rode o prompt `11` para decupar e
adaptar a estrutura; o briefing que sai dele é consumido pela skill
`criativo-ads-video-orq`, que faz imagem → vídeo → QA → montagem.

## Atualizar a biblioteca

A fonte é `sistema.antonioferriani.com/modelos-de-criativos` (perfil de browser
`ferriani`, porta 9233, opt-in já feito). Para pegar formatos novos:

```bash
~/.claude/bin/browsers.sh ferriani
agent-browser --session ferriani navigate 'https://sistema.antonioferriani.com/modelos-de-criativos'
agent-browser --session ferriani state save /tmp/auth.json   # cookie criativos_lead
```

Cada card é um `<article>` com `data-id`, `data-tipo`, `data-categoria`, `data-nome`.
Download: `GET /api/criativos/download?id=<id>&formato=arquivo` (ou `formato=txt` para
a transcrição), com o cookie, seguindo o 302 para o Supabase. Os links assinados
expiram em ~60s — baixe na hora.

### Sync automático — roda sozinho, sem sessão de Claude aberta

`scripts/sync.sh` faz o diff acima sozinho: lê os cards do site, compara `id`
contra `catalogo.json` local e baixa **só o que é novo** — nunca rebaixa os 103
já no disco. Atualiza `catalogo.json` no fim; `CATALOGO.md` (o índice legível)
não é regravado automaticamente — rode `buscar.sh` pra conferir o que entrou e
atualize o `.md` a mão se for citar os novos formatos em algum lugar.

Agendado por **systemd user timer** (não é cron do Claude — roda mesmo com a
sessão fechada):

```bash
systemctl --user list-timers escalados-sync.timer   # próxima execução
journalctl --user -u escalados-sync.service -n 30   # log da última rodada
cat ~/.claude/skills/modelagem-escalados/scripts/sync.log
```

Unidades em `~/.config/systemd/user/escalados-sync.{service,timer}`, dispara
todo dia às 06:17. Depende do perfil de browser `ferriani` (porta 9233) estar
com login válido — se o cookie expirar, o sync loga a falha e não quebra nada,
só não acha cards novos até alguém relogar.
