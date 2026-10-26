---
name: banner-checkout-gpt
description: Gera banner de produto pro checkout (imagem via GPT/ChatGPT) sempre com título, objetivo/produto real, garantia, entrega imediata, acesso vitalício e — quando fizer sentido — mockup do produto. Sai em desktop (16:9) e mobile (1:1/retrato). Use quando o usuário pedir "banner de checkout", "banner do produto", "arte pro checkout", ou mencionar título+garantia+entrega+vitalício numa imagem. Também a CAPA DE PRODUTO de upgrade (UPGRADE PARA COMPLETO), combo (COMBO ESPECIAL) e order bump — receita em references/CAPA-PRODUTO-UPGRADE-COMBO.md.
---

# banner-checkout-gpt

Gera a arte de banner que fica no topo do checkout — a imagem em si carrega texto (não é só decoração com overlay em HTML por cima). Executa, não explica: o usuário conhece o fluxo.

**Pré-requisito de ordem (não furar):** banner só depois de ter os **mockups** da entrega — logo,
só depois do **MVP entregue**. Sem mockup do produto, não tem banner. Ordem completa da oferta em
memória `ordem-execucao-oferta`. Sair sempre organizado, os 3: **checkout desktop** (16:9), **checkout
mobile** (1:1/retrato) e **imagem do produto**.

**Capa de produto de UPGRADE, COMBO ou BUMP (imagem do item no checkout):** receita única em
`references/CAPA-PRODUTO-UPGRADE-COMBO.md` — ler antes de gerar. Imagem inteira nasce no GPT com o
título integrado; colar/recortar texto por cima é proibido (erro real Tarot 16/10, dona 26/10).

Mecânica de browser (lane, anexo, envio, download, QA) é 100% da skill `gpt-imagem-playwright` — leia ela antes de gerar qualquer imagem. Esta skill só define O QUE entra no prompt e onde salvar.

## 1. Levantar o contexto do produto — NUNCA generalizar

Antes de escrever qualquer prompt, leia o que o produto realmente é. Nunca assuma "é tipo X" (ex.: "mapa numerológico") sem confirmar no código/doc do projeto:

- `PRODUCT.md` ou README do projeto — o que o produto entrega de verdade.
- Arquivo de preço/pricing (ex.: `lib/pricing.ts`) — título oficial do produto (`PRODUCT_TITLE`), moeda, se há bump/combo/promoção que muda o preço.
- Copy real usada no checkout/página de vendas — para não inventar frase que não bate com o que a oferta entrega.

Errar isso é caro: gerar arte bonita descrevendo o produto errado (já aconteceu — "mapa numerológico" numa oferta que na verdade entrega uma "chave" + ritual). Confirme com o usuário se o entendimento do produto estiver em dúvida.

## 2. Perguntar ANTES de gerar, sempre

Sempre confirmar com o usuário (`AskUserQuestion` se ambíguo, ou direto se o padrão do projeto já está definido em memória):

- **Preço na arte? PADRÃO = NÃO queimar preço** (decisão do dono 21/09/2026). Motivo: preço queimado obriga refazer a arte toda vez que muda; deixar o preço FORA do banner (ele já aparece embaixo/no checkout) permite trocar o valor sem tocar no banner. Produto com bump/order bump/popup que muda o valor real: NUNCA queimar. Só queime preço se o dono pedir explicitamente na hora, para um produto de preço único e fixo. Na dúvida, sem preço.
- **Quantas situações/variantes?** Banner principal, banner com bump/combo, banner de popup/exit-offer — cada situação é OUTRA imagem (nunca reaproveitar o mesmo texto pra outra oferta).
- **Selos de forma de pagamento** (cartão, Mercado Pago, PIX, SPEI, OXXO etc.) são um lote SEPARADO deste banner — ícone pequeno por método, não entram no banner principal.

## 3. Texto obrigatório na arte

Todo banner de checkout leva, queimado na imagem (a não ser que o usuário peça o contrário na hora):

1. **Título** — nome real do produto/oferta.
2. **Subtítulo/objetivo** — uma linha do que o produto entrega (não genérica).
3. **Preço** — só se confirmado no passo 2.
4. **Garantia** — prazo real (ex.: "Garantía de 7 días" / "7 dias de garantia").
5. **Entrega imediata** — linha própria.
6. **Acesso vitalício** — linha própria.

Layout sugerido: título+subtítulo num canto (ou topo, se for quadrado), as 3-4 linhas curtas empilhadas como lista com ícone, e o elemento visual/mockup do produto ocupando o espaço livre — nunca sobrepondo texto. Sempre `no text` para QUALQUER outro texto fora dessa lista (nada de letras soltas, marca d'água, legenda).

## 4. Mockup do produto — só quando fizer sentido

Se o produto é um artefato digital com "capa" (PDF, e-book, painel, relatório): pode mostrar um mockup do documento/tela como elemento visual.

Se o produto é mais abstrato (uma leitura, uma chave, um ritual, uma sessão): usar um objeto simbólico central e bem descrito em vez de mockup de tela — mais honesto e evita "promessa de tela" que a oferta não cumpre (ver doutrina de telas/PDF mockup na skill `gpt-imagem-playwright`: se aparecer tela, o conteúdo dela tem que ser descrito, ligada, no idioma certo).

Nunca personas/rosto de pessoa no banner de produto — isso é papel de criativo de anúncio, não do banner de checkout.

**Régua de arte boa × feia** (produto visível e legível, cena coerente, paleta da marca, sem preço queimado, webp leve): `imagens-pagina-low` › "Imagem de PRODUTO/oferta (capa de checkout, card e banner da área) — boa × feia".

### ⚠️ REGRA CRÍTICA: Mockup do banner = SEMPRE identidade NOSSA, NUNCA arte do concorrente

**Ordem correta:** (1) entregável pronto → (2) construir os NOSSOS mockups (nossa identidade/idioma) → (3) SUBSTITUIR na página de vendas os mockups do concorrente pelos nossos adaptados → (4) só então fazer o banner, usando os NOSSOS mockups já publicados na página. Banner nunca nasce antes desse passo 3.

**O mockup visual do produto no banner SÓ pode ser gerado a partir de nossas PRÓPRIAS páginas-base (já traduzidas, já recoloridas na nossa paleta, já em PT-BR).** Nunca copiar ou "modelar em cima" de uma IMAGEM DE MOCKUP do concorrente e colar direto no banner. Modelar = editar cor+idioma, mas o resultado final TEM QUE SAI 100% nossa identidade. **O critério é a arte ser do concorrente — não o idioma.**

Sintoma possível de erro (não é a causa, é só indício): banner sai com texto em ESPANHOL, cores do concorrente, ou visual/design que não é o nosso. Reprovar e regerar sempre que a peça usar mockup/arte do concorrente ou deixar asset dele sem substituir — sempre anexar as nossas imagens de referência (geradas em `imagens-pagina-low`, salvas em `IDENTIDADE-REF/`), nunca a imagem-mockup do concorrente.

**Método completo:** passar a identidade visual extraída (cores hex + fontes + estilo) explícita no prompt e, se precisar de referência, anexar print da nossa página — ver skill `imagens-pagina-low` seção "Passar SEMPRE a nossa identidade visual pro GPT".

## 5. Tamanhos e nomes de arquivo

Convenção usada no componente React que consome (`BannerProducto.tsx` ou equivalente): dois recortes do MESMO conceito visual, texto adaptado ao formato.

- **Desktop**: 16:9, `Generate ONE single standalone image, horizontal 16:9 landscape format, full-bleed...`
- **Mobile**: 1:1 ou retrato, `Generate ONE single standalone image, square 1:1 format, full-bleed...` com o texto reorganizado em coluna (título no topo, elemento visual no meio, linhas curtas embaixo).

Nome de arquivo segue o padrão do componente que já existe no projeto — confira antes (ex.: `banner-<pais>-<desktop|mobile><-combo>.jpg`). Salvar em `public/checkout/` (ou equivalente do projeto).

## 6. Gerar — uma imagem por chat, sempre

Siga a doutrina de `gpt-imagem-playwright`: **nunca peça desktop+mobile na mesma mensagem** (sempre volta grid/colagem, testado repetidas vezes). Chat novo por imagem. Baixe pelo `img.src` COMPLETO (não truncar — a URL do ChatGPT carrega parâmetros de assinatura `p`/`ts`; cortar a string derruba o download com JSON de erro em vez da imagem).

Depois de baixar: confira dimensão (`ffprobe`), abra a imagem e confirme que todo o texto obrigatório está lá, correto e sem sobreposição, antes de copiar pra pasta do projeto.

## 7. Variar por situação/país sem reescrever do zero

Uma variante (combo/bump, outro país, outra promoção) é o MESMO prompt-base com:
- a persona/idioma trocado (ex.: voseo AR vs "tú" MX — nunca misturar),
- uma frase extra se for combo (ex.: "Con la Herencia de Familia incluida"),
- preço/moeda do país certo, se preço entrar (ver passo 2).

Nunca reaproveitar arte de um país pro outro sem trocar o texto — ver regra de país-nunca-se-cruza se o projeto tiver personas por mercado.
