---
name: checkout-premium
description: Monta uma página de checkout própria com layout de alta conversão (barra de urgência full-bleed, banner colado no card, formulário mínimo só-email, order bump com foto real e checkbox pré-marcado, pagamento lado a lado adaptado ao gateway do país, prova social com fotos/nomes reais, notificação fake de compra, popup de saída) dentro de um projeto Next.js/React já existente. Use sempre que o usuário pedir "checkout premium", "checkout de alta conversão", "monta um checkout pra [produto]", pedir pra clonar/replicar um print de checkout (Hotmart ou concorrente), ou pedir para adicionar order bump / barra de urgência / prova social / notificação de compra fake a um checkout já existente. Também use quando o usuário mandar um print de checkout pedindo pra "fazer igual" ou "uma versão disso aqui".
---

# checkout-premium

Template de checkout de alta conversão, para replicar dentro de QUALQUER
projeto Next.js/React que já tenha um produto, um preço e (geralmente) um
checkout anterior. Não é um app novo — é uma peça que entra num projeto que
já existe, então o trabalho real é **descobrir o que o projeto já tem** antes
de escrever qualquer JSX.

Nasceu generalizando um checkout construído ao vivo pro projeto "El Número
Maestro" (numerologia, MX/AR) copiando o layout de um print da Hotmart. Os
erros que aconteceram nessa sessão viram as seções "Não pule isto" abaixo —
cada uma custou um retrabalho visível pro usuário.

## Regra de identidade visual: clone exato por padrão

Quando o usuário pede "checkout premium" ou manda um print pra clonar, é
**clone visual EXATO** — mesma paleta de cor, mesma tipografia, mesmo
espaçamento/formato de card, bumps, abas de pagamento, tudo igual ao print de
referência. Só troca produto/oferta/banner/texto. **Nunca adapte a paleta pro
tema/identidade visual do projeto por conta própria** — isso é uma decisão à
parte que o usuário pede explicitamente ("faz com a cor/identidade do
produto"), nunca a leitura padrão do pedido. Confirmado em sessão AstroDicas
(14/09/2026): o clone saiu no tema dark/gold do resto do site em vez do
cream/branco/laranja do print de referência, e o usuário corrigiu na hora.

## Antes de escrever código: levantar o projeto

Nunca escreva o componente sem primeiro achar isto no projeto (procure, não
pergunte tudo de cara — só pergunte o que não achar no código):

| Precisa saber | Onde costuma estar |
|---|---|
| Título e preço do produto | `lib/pricing.ts` ou equivalente — função tipo `price()`/`comparePrice()`, nunca hardcode um número |
| Se há order bump/add-on já modelado | mesmo arquivo de pricing — um SKU secundário com preço e `compareAt` |
| Copy REAL do order bump | outro componente que já vende o mesmo bump (modal de upsell, página de oferta) — nunca inventar a descrição |
| País/gateway de pagamento | lib tipo `lib/country.ts` (`isMx`, `country.gateway`) — determina os métodos de pagamento a mostrar |
| Componente de popup de saída (exit-intent) já existente | procure por "exit", "rescate", "resgate" nos componentes — REUSE, não recrie |
| Fotos/depoimentos reais já usados no site | lib tipo `lib/testimonios.ts` ou pasta `public/testimonios/` — nunca "Cliente Ejemplo" |
| Banner de produto já existente | componente tipo `BannerProducto` — pode ter largura travada pra outro contexto, ver seção 2 abaixo |

Se qualquer um destes já existir no projeto, **reaproveite** — a skill inteira
é sobre reduzir trabalho reaproveitando o que o projeto já validou (copy,
preço, popup, fotos), não sobre escrever tudo do zero com dados inventados.
Só pergunte ao usuário o que genuinamente não existe ainda (ex.: se não há
nenhum componente de exit-offer, pergunte se ele quer um).

## Anatomia do checkout

De cima pra baixo, nesta ordem:

1. **Barra de urgência full-bleed** — largura de toda a janela (fora do
   container do card), contador regressivo + texto curto. Gradiente com
   cor de urgência (vermelho tipicamente), ícone de relógio de verdade (não
   lupa/ampulheta — um `<circle>` com um ponteiro simples já resolve).
2. **Banner do produto** — imagem 16:9 colada direto no topo do card branco
   (sem gap entre banner e card: banner com `rounded-t-2xl`, card com
   `rounded-b-2xl border-t-0`, emendados). Ver seção "Não pule isto" #2 sobre
   por que não dá pra sempre reusar um componente de banner já existente.
3. **Header do card**: nome do produto em destaque — cor de marca (dourado,
   azul, o que for a paleta do projeto), NUNCA preto puro, que não chama
   atenção nenhuma. Preço à direita com comparação riscada. Selo de garantia
   (verde, com ícone de escudo) logo abaixo do nome — este selo é fácil de
   esquecer e o usuário vai notar a falta.
4. **Formulário mínimo** — só email. É a lição central do padrão Hotmart:
   nome/telefone pedem confiança antes da hora e derrubam conversão; a
   Hotmart só pede o essencial pra entregar o produto e fecha o resto depois.
   Capture o email cedo — ver seção "Não pule isto" #4.
5. **Order bump** — card com checkbox **pré-marcado** (a pessoa desmarca se
   não quiser, não o contrário), foto pequena (56×56 aprox.) do que está
   sendo oferecido, título, descrição curta, preço riscado + com desconto.
   Ver seção "Não pule isto" #1 e #5 sobre a foto e o copy.
6. **Forma de pagamento** — métodos lado a lado (`grid-cols-2`/`grid-cols-3`
   conforme quantos existirem). **Os métodos dependem do país/gateway do
   projeto** — nunca hardcode um par fixo. Ver tabela de gateways abaixo.
   **Cada tile leva imagem/ícone, sempre** — nunca só texto: gateway com
   marca reconhecida no mercado (Mercado Pago, PayPal, etc.) usa o **logo
   oficial** baixado da CDN pública da própria marca (nunca gerado por IA
   nem redesenhado — ver "Não pule isto" #7); método sem marca própria
   (transferência bancária, débito/crédito genérico) leva um ícone neutro
   desenhado (banco, cartão) + as bandeiras aceitas como texto (Visa ·
   Mastercard · Amex). Texto puro sem nenhuma imagem é o erro mais comum
   nesta seção e o usuário sempre pede pra corrigir depois.
7. **Resumo + CTA** — em desktop, coluna própria `sticky` ao lado do
   formulário (`md:grid-cols-[1fr_20rem]` é um bom ponto de partida).
   Soma produto + bumps marcados, botão "Comprar agora" no fim.
8. **Prova social** — bloco de avaliações com fotos e nomes REAIS já usados
   no projeto (nunca avatar genérico), estrelas variando entre 4 e 5 (nunca
   100% cinco estrelas — fica óbvio que é fabricado). Contador de clientes
   com número não-redondo (`700 + random(180)` por exemplo, fixado uma vez
   por sessão) — "Más de 1.000" ou "500+" lê como placeholder de template.
9. **Notificação fake de compra recente** — toast fixo no canto (superior
   direito costuma incomodar menos que inferior esquerdo, que colide com
   widgets de chat), aparecendo em ciclos de ~10-15s, nomes e cidades
   variados sem dado real de ninguém.
10. **Popup de saída (exit-intent)** — se o projeto já tem um componente pra
    isso, PLUGUE nele em vez de recriar (ver "Não pule isto" #3). Se não
    tem, pergunte antes de escrever um do zero.
11. **Selos de confiança no rodapé** — criptografia/PCI DSS, links de
    política (podem não ser funcionais num protótipo), ícone de cadeado.

## Gateways de pagamento por país — nunca hardcode

Antes de escrever os dois botões de "Forma de pago", confirme qual gateway o
projeto usa. Descobrir isso tarde (depois de já mostrar os métodos errados
pro usuário) é o erro mais caro desta lista:

| País/gateway | Métodos típicos lado a lado |
|---|---|
| México, XPag (sem cartão) | SPEI (transferência) / OXXO (efectivo) |
| Argentina, Mercado Pago | Tarjeta débito o crédito (via Mercado Pago) / Transferencia manual |
| Brasil, PIX-first | PIX / Cartão de crédito |

Leia a variável/lib de país do projeto (`isMx`, `country.gateway` etc.) e
renderize condicionalmente — nunca um par de botões fixo, mesmo que o
primeiro teste tenha sido só num país.

## Não pule isto — erros que já aconteceram

**1. Imagem gerada por IA salva com extensão errada quebra o Next Image.**
Se a imagem do order bump (ou qualquer imagem) foi gerada via
`gpt-imagem-playwright`, ela normalmente baixa como PNG. Salvar esse
arquivo como `.jpg` faz o otimizador de imagem do Next servir a resposta
com `Content-Disposition: attachment` (mismatch de tipo declarado vs real)
— o navegador nunca pinta a imagem, ela simplesmente não aparece, sem erro
visível no console. Sempre rode `file <caminho>` antes de referenciar o
arquivo no componente, e use a extensão que bate com o que `file` disse.

**2. Um componente de banner "pronto" pode ter largura travada pra outro
contexto.** Se o projeto já tem um `BannerProducto` (ou nome parecido),
olhe o CSS dele antes de reusar — pode ter um `max-w-xs`/`max-w-sm` pensado
pra ficar ao lado de um resumo em outro layout, e aqui ele prenderia o
banner inteiro na largura de mobile mesmo em desktop. Nesse caso não lute
contra o componente: monte o `<Image fill>` direto, na largura do
container deste checkout.

**3. Reuse o popup de saída existente em vez de recriar.** Se o projeto já
tem um componente de exit-offer (geralmente chamado algo como
`CheckoutExitOffer`), ele já escala sozinho com o carrinho/bump e já tem o
copy testado — plugue nele. Escrever um popup novo do zero duplica lógica
de preço que só existe corretamente num lugar do projeto.

**4. Capture o email ANTES do clique em comprar, não só no submit.** O
motivo é remarketing: se a pessoa preenche o email e fecha a aba sem
terminar, sem uma captura antecipada esse email nunca chega a lugar
nenhum. Dispare a captura no `onBlur` do campo de email (chamando uma API
que persiste o email associado ao lead, não só o `submit` do formulário) —
não trave essa chamada atrás do clique final.

**5. O copy do order bump tem que bater com o produto real, não pode ser
inventado.** Se já existe outro lugar no projeto vendendo o mesmo add-on
(um modal de upsell, uma seção de oferta), a descrição do bump no checkout
precisa contar a MESMA história — texto solto que soa bem mas não bate com
o que o produto realmente entrega é a primeira coisa que o usuário vai
pegar na revisão.

**6. Fotos e nomes de depoimento têm que ser reais e do MERCADO certo.** Se
o projeto atende mais de um país/mercado, cada mercado tem seu próprio set
de fotos/nomes (não misture uma cliente mexicana no checkout argentino) —
procure a lib de depoimentos existente e monte um set por mercado, nunca
"Cliente Ejemplo" genérico.

**7. Logo de marca conhecida (Mercado Pago, PayPal, Hotmart...) é sempre o
oficial, baixado da CDN pública da própria marca — nunca gerado por IA nem
redesenhado do zero.** Um logo gerado sai deformado e é uso indevido de
marca registrada; mas esconder a marca por completo também erra pro outro
lado — em mercados onde ela é muito reconhecida (Mercado Pago na
Argentina), NOMEAR o gateway aumenta confiança em vez de reduzir, o
oposto do que parece intuitivo. Pra achar o SVG oficial: baixe a home do
site oficial do gateway (`curl` com `-A` de browser) e grep por
`logo.*\.(svg|png)` nos assets referenciados — geralmente aparece um link
pra CDN própria da marca (ex.: `http2.mlstatic.com/.../logo-mercadopago.svg`
pro Mercado Pago). Salve em `public/checkout/` e referencie com
`next/image`. Método sem marca própria (transferência, débito/crédito
genérico) não tem esse problema: aí sim vale ícone neutro desenhado.

## Referências

- `references/exemplo-componente.md` — trecho comentado do componente que
  originou esta skill, com a estrutura completa de JSX pra copiar como
  ponto de partida (adaptar cores, textos e gateway ao projeto atual).
- Skill `gpt-imagem-playwright` — gerar a foto do order bump quando o
  projeto ainda não tiver uma pronta.
- Skill `banner-checkout-gpt` — gerar a arte do banner (16:9) quando o
  projeto ainda não tiver uma, incluindo o que precisa estar queimado na
  imagem (título, garantia, entrega, acesso).
