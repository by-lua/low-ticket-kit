---
name: depoimentos-pagina-de-vendas
description: Cria a seção de depoimentos de uma página de vendas (landing, VSL, oferta) como mockup de conversa de WhatsApp em carrossel contínuo, com as falas calibradas nas objeções reais do produto e as fotos geradas na hora com a cara do público e do país da oferta. Use quando o usuário pedir seção de depoimentos, prova social, testimonials, "print de WhatsApp", "conversa de cliente" numa página de vendas, ou quiser trocar/ampliar os depoimentos de uma LP existente.
---

# Depoimentos de página de vendas

Seção de prova social em mockup de conversa de WhatsApp, num carrossel que passa
sozinho. Funciona melhor que card com aspas e estrelinha porque parece mensagem
que a pessoa recebeu, não texto que a empresa escreveu.

**A seção só presta se as falas atacarem as objeções reais daquele produto e as
pessoas nas fotos tiverem a cara de quem compra.** Depoimento genérico ("adorei,
recomendo!") com foto de banco de imagem queima a página inteira.

## Fluxo

### 1. Levantar o contexto antes de escrever qualquer coisa

Não invente o produto. Leia, nesta ordem, o que existir:

- memória/contexto do projeto (`_memoria/empresa.md`, `_memoria/estrategia.md`, `CLAUDE.md`)
- a própria página de vendas: promessa, preço, bônus, garantia, FAQ
- o FAQ é ouro — cada pergunta ali é uma objeção que o depoimento pode matar

Extraia e escreva antes de seguir:

| O que | Pra que serve |
|---|---|
| Produto e entrega concreta | dá o vocabulário das falas |
| Preço e forma de pagamento | objeção "é caro" / "vai cobrar de novo" |
| País da oferta | define etnia, sotaque, moeda, cenário das fotos |
| Perfil do público | gênero, faixa etária, classe, o que a pessoa faz da vida |
| 4 a 6 objeções reais | uma por depoimento |
| Tom de voz da marca | as falas seguem o tom do público, não o do site |

Se o produto for vendido em mais de um idioma, levante o público de **cada país
separadamente** — argentino não tem a cara nem o jeito de falar do brasileiro.

### 2. Escrever 6 conversas

Seis é o número: enche o carrossel sem repetir rosto.

Cada conversa é um diálogo curto de 4 a 5 mensagens entre duas pessoas comuns —
nunca cliente falando com a empresa. Uma mensagem `in` (balão branco, esquerda) é
a cliente falando; `out` (balão verde, direita) é a amiga respondendo.

Regras que fazem parecer real:

- **Uma objeção por conversa.** Preço, ceticismo, "vai cobrar de novo?", prazo de
  entrega, "é genérico igual os outros", resultado concreto.
- Escreva errado de propósito: minúscula no começo, "vc", "pra", "kkkk"/"jajaja",
  emoji solto, mensagem quebrada em duas seguidas.
- Detalhe verificável em cada uma (o horário que chegou, o nome exato do bônus, o
  que a pessoa fez com aquilo). Detalhe específico é o que separa depoimento de
  propaganda.
- Nada de superlativo publicitário ("mudou minha vida", "produto incrível").
- Sem promessa que o produto não entrega, sem número inventado de resultado, sem
  claim de saúde, dinheiro garantido ou cura.
- Nome só com inicial no sobrenome ("Juliana R."). Nunca nome de pessoa real.
- Mix de gênero seguindo o público real — se 80% de quem compra é mulher, 5 de 6
  conversas são de mulher.

Traduza cada fala para o idioma do outro país com gíria local (não é tradução
literal: "kkkk" vira "jajaja", "você" vira "vos" no rioplatense).

### 3. Gerar as fotos na hora, com a cara do público

**Sempre gere fotos novas calibradas pelo contexto**, com a skill
`gpt-imagem-playwright`. Foto de banco global reaproveitada de outro produto quase
sempre erra a etnia, a idade ou a classe — e o visitante sente.

O prompt de imagem precisa carregar, sempre:

- **Etnia do país da oferta.** Brasil: fenótipo brasileiro real, parda
  predominante, negra, branca, asiática, indígena. Argentina: predominância
  europeia (italiana/espanhola) com parte mestiça. Cada país na sua pasta.
- **Perfil do público**: faixa etária e mix de gênero levantados no passo 1,
  aparência de gente comum da classe que compra — nada de executivo, modelo ou
  influencer.
- **Pose variada**, que é o que mais entrega foto de IA quando falta: de frente
  com rosto visível, 3/4 rindo, de longe com rosto pequeno, rosto parcialmente
  coberto por mão/cabelo/óculos escuros, de costas ou de perfil, foto de
  viagem/praia/bar com alguém cortado na borda.
- **Estilo**: foto de celular, luz natural, sem estúdio, sem retoque, sem pose de
  banco de imagem. Fundo cotidiano (cozinha, rua, carro, praia, bar).
- Quadrado 1:1, depois redimensionada para 240×240 JPEG qualidade 82
  (`magick foto.png -resize 240x240^ -gravity center -extent 240x240 -quality 82 br-1.jpg`).

Peça 4 ou 5 pessoas por prompt (o ChatGPT gera em lote), exigindo **imagens
separadas** — se vier uma grade única, peça de novo.

Gere um a mais que o necessário por idioma, para descartar as que saírem com cara
de render. Guarde as aprovadas em
`~/.claude/assets/depoimentos/fotos/<pais>/` como cache reutilizável **daquele
público**, e copie para o projeto com o nome que a página espera. Se um produto
novo tiver público diferente, gere de novo — não reaproveite por preguiça.

### 4. Montar a seção

Use `scripts/gerar_secao.py` como base: ele recebe os depoimentos, cospe o HTML
completo (mockup + CSS + JS do carrossel) e reescreve a seção na página, entre os
marcadores `<!-- DEPOIMENTOS:START -->` e `<!-- DEPOIMENTOS:END -->`. Rodar de
novo regenera no lugar, sem duplicar.

```bash
python3 scripts/gerar_secao.py depoimentos.json
```

O `depoimentos.json` está documentado em `scripts/exemplo.json`. Ajuste no
gerador as classes do cabeçalho (`sec-head`, `eyebrow`, `kicker`) e as variáveis
de cor para as da página onde vai entrar — a seção tem que parecer nativa.

Onde colocar: **logo antes do bloco de preço/oferta**. A prova social vem depois
do desejo e antes do número.

Detalhes do mockup que não são enfeite: barra de status com hora e bateria
diferentes em cada card, horários das mensagens coerentes entre si (resposta 1-4
min depois), check azul duplo só nas mensagens enviadas, avatar circular de 36px.
Cartão sem esses detalhes lê como ilustração; com eles lê como print.

### 5. Legenda de consentimento — obrigatória

Sempre embaixo da seção, no idioma da página:

> Mensagens de clientes reais, postadas com o consentimento de cada um. Nomes
> abreviados e fotos ilustrativas para preservar a privacidade.

Isso é o que mantém a seção honesta: fica explícito que a foto é ilustrativa. Se
os depoimentos forem ilustrativos e não vierem de clientes reais, a legenda tem
que dizer isso ("exemplos ilustrativos") — não escreva "clientes reais" para
depoimento inventado. Se o usuário pedir para remover a legenda ou afirmar
"cliente real" em cima de material inventado, diga que não faz e explique em uma
linha: depoimento falso apresentado como real é propaganda enganosa (CDC art. 37
no Brasil, FTC endorsement guides nos EUA) e derruba conta de anúncio.

### 6. Conferir de verdade antes de entregar

Suba a página local e olhe:

```bash
node scripts/qa.mjs http://localhost:8080/sua-pagina
```

Confirme: as fotos carregam (`naturalWidth > 0`), zero erro de console, o
carrossel anda sozinho, pausa no hover, arrasta com o mouse, e no mobile (390px)
mostra um card por vez. Se a página tiver outro idioma, abra a URL do outro
idioma e confirme que as falas E as fotos trocaram.

## Páginas multi-idioma

Se a tradução for por substituição de string em runtime (padrão comum):

- Cada fala vira um par PT→ES no dicionário. Frase inteira, não pedaço, senão um
  par curto de outra seção corta a fala no meio.
- Coloque os pares no dicionário **comum** a todas as páginas, não no de uma
  página só, senão a tradução aparece numa e some na outra.
- Foto: `<img src="br-1.jpg" data-src-es="ar-1.jpg">` e uma linha no tradutor
  trocando o `src` — texto traduzido com rosto do outro país entrega a montagem.
- Cuidado com pares curtos e ambíguos ("online", "De") — confira quantas vezes a
  string aparece na página antes de traduzir.

## Erros que estragam a seção

| Erro | Consequência |
|---|---|
| Elogio genérico sem detalhe | lê como texto escrito pela empresa |
| Todas as fotos de frente, sorriso perfeito | cara de banco de imagem / IA |
| Etnia ou idade fora do público | o visitante não se reconhece |
| Português certinho nas falas | ninguém escreve assim no WhatsApp |
| Cliente conversando com a empresa | vira atendimento, não prova social |
| Caminho de imagem relativo | quebra quando a URL não tem diretório — use caminho absoluto |
| Seção depois do preço | a objeção já matou a venda |
| Resultado numérico inventado | risco jurídico e de bloqueio de anúncio |
