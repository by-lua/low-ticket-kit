# Tráfego Para E-commerce e Outras Aulas

## Tráfego Para E-commerce

### Mensurando os dados

**Aula:** 145

- Primeiro passo pra campanha de e-commerce: Pixel instalado e marcando TODOS os eventos (page view, view content, add to cart, initiate checkout, purchase) ANTES de gastar qualquer verba.
- Passo a passo de instalação: Gerenciador de negócios → Fonte de dados → Conjunto de dados (nome atual de "Pixel") → compartilhar/conectar na BM → Gerenciador de eventos → Adicionar eventos → Adicionar nova integração → escolher entre "Pixel do Meta" (código HTML, colar no `<head>` da plataforma) ou API de conversão (mais eficaz, pega mais dados). Cada plataforma de e-commerce (Shopify, Nuvem Shop, etc.) tem tutorial próprio — pesquisar no YouTube "como instalar Pixel Facebook [nome da plataforma]".
- Verificação: extensão Chrome "Meta Pixel Helper" confirma se o Pixel está disparando no site. Depois, usar "Eventos de teste" no gerenciador (colar a URL, abrir o site, navegar) pra confirmar cada evento disparando em sequência: Page View → View Content → Add to Cart → Initiate Checkout → Purchase.
- Ponto crítico: o CHECKOUT geralmente é uma plataforma EXTERNA à loja (CartPanda, AppMax, Yampi etc.) — o Pixel precisa ser instalado SEPARADAMENTE nessa plataforma de checkout, senão "Initiate Checkout" e "Purchase" nunca disparam mesmo com o Pixel do site funcionando perfeitamente.

- Fonte: transcricoes/curso-id15/19-trafego-para-ecommerce/01-Mensurando_os_dados.md

### Estética e Confiabilidade

**Aula:** 146

- 2ª etapa de análise pré-campanha (depois do Pixel): avaliar Estética (site organizado, padrão visual, boa descrição de produto), Confiabilidade (reviews/avaliações reais — "não dá pra subir um site sem review", pedir pra família/amigos avaliarem se não tiver nenhum ainda) e Oferta (preço + condição precisam ser atrativos pro nicho — ex. real: "compre 2, leve 4" + personalização de nome/número na camisa).
- Regra de negócio pro gestor: recusar fechar contrato com cliente cujo site não tenha esses 3 fatores (estética + confiança + oferta boa) — "a culpa de não performar vai cair em você, não na estrutura ruim do cliente".

- Fonte: transcricoes/curso-id15/19-trafego-para-ecommerce/02-Est_tica_e_Confiabilidade.md

### Campanhas de compra de dados

**Aula:** 147

- Conceito: toda campanha subida já é "compra de dados" (o Facebook aprende com cada impressão/clique quem é o público certo) — não ter dados é a causa #1 de campanha nova não vender, não necessariamente produto/criativo ruins.
- Se o cliente JÁ vendia antes: usar públicos QUENTES (quem já engajou/comprou/iniciou checkout) desde o início.
- Se NUNCA vendeu (começando do zero): sequência de 4 campanhas simultâneas, todas rodando ao mesmo tempo, pra "aquecer" o Pixel e gerar dados:
  1. **Engajamento no Instagram** (campanha de seguidores) — gera branding; case citado: perfil de 700 pra quase 100.000 seguidores, vídeos orgânicos de 1,5 milhão de views.
  2. **Tráfego pro site** — objetivo explícito NÃO é vender, é levar gente pro site pra "comprar dados" (aquecer Pixel, dar credibilidade pro Google). Recomendação: deixar essa campanha sempre ativa, eterna, só trocando criativo.
  3. **Adicionar ao carrinho** (campanha de conversão, objetivo = add to cart).
  4. **Iniciar finalização de compra** (campanha de conversão, objetivo = initiate checkout).
- Orçamento sugerido com pouca verba (intercalando em vez de rodar tudo com verba alta ao mesmo tempo): engajamento Instagram ~R$2-20/dia; tráfego ~R$2-45/dia (mais barato); adicionar ao carrinho ~R$2-45/dia; iniciar checkout ~R$45+/dia. Regra geral se tiver mais verba: R$45-60/dia por campanha.

- Fonte: transcricoes/curso-id15/19-trafego-para-ecommerce/03-Campanhas_de_compra_de_dados.md

### Qual criativo você deve usar?

**Aula:** 148

- Loja NICHADA (ex. camisas de time específico): criativo fala da LOJA e da oferta geral (não de um produto específico) — ex. "essa loja incrível, super promoção, compre 2 leve 4, há 5 anos no mercado".
- Loja GENÉRICA (multi-categoria): criativo de PRODUTO específico, estilo anúncio de venda, mas com objetivo ainda de tráfego/add-to-cart (não venda direta) nessa fase de compra de dados.

- Fonte: transcricoes/curso-id15/19-trafego-para-ecommerce/04-Qual_criativo_voc_deve_usar.md

### Campanhas de Conversão

**Aula:** 149

- Depois de ter dados suficientes: subir campanha de COMPRA (conversão/vendas). Orçamento R$45-65 a nível de campanha (CBO).
- Públicos a testar: Aberto; público de interesses (relacionado ao nicho); "visitantes da página +1%" lookalike; "adicionou ao carrinho +1%" lookalike; "iniciou checkout +1%" lookalike; "ao Insta + ao Face" (quem engajou nas redes, se já movimentadas). Mínimo 2-3 criativos, ideal 3-5, repetidos em todos os conjuntos.
- Resultado real mostrado (loja "Invictos", camisas de time): campanha em teste — 794 visualizações de página a R$0,63 cada; 551 adições ao carrinho a <R$1,88; 65 finalizações de compra a <R$8; 10 compras a CPA de R$48; gasto R$482 → retorno R$2.521 (ROAS 5,23, com nota de que o Facebook não estava marcando ~R$1.000 de vendas reais adicionais). Público "visitantes +1%" gerou 5 compras com ROAS 3,83; público de interesse (Pixel já aquecido) teve CPA menor (R$35) que o de "visitantes" nesse caso específico — reforça que não existe público "sempre vencedor", depende do aquecimento do Pixel.
- Prática de consolidação: em vez de criar campanha nova pra cada público que já vende, ADICIONAR o público novo na MESMA campanha de conversão que já está performando (em vez de pulverizar em várias campanhas pequenas) — mantém o histórico/aprendizado da campanha.

- Fonte: transcricoes/curso-id15/19-trafego-para-ecommerce/05-Campanhas_de_Convers_o.md

### Otimizando na Prática

**Aula:** 150

- Ordem de otimização: CRIATIVO primeiro → CONJUNTO depois → CAMPANHA por último.
- A nível de criativo: filtrar por compras — quem não vendeu E não teve nem finalização de compra iniciada (métrica secundária efetiva), matar. Quem teve adição ao carrinho/finalização mas ainda não vendeu, manter (ainda "desenvolvendo potencial").
- A nível de conjunto: mesma lógica — manter só quem tem finalização de compra iniciada ou vendas; o que só gastou pouco (ex. 24 centavos) sem nenhum sinal, não matar ainda (não deu tempo de desenvolver).
- A nível de campanha: não olhar só o CPA isolado — olhar CPA junto com VOLUME. Exemplo real: conjunto "Flamengo" (interesse) com CPA R$81 e baixo volume → matado; outro conjunto com CPA R$52 mas volume alto → mantido, porque gerou mais "grana no bolso" absoluta (R$700) que um conjunto com ROAS maior (11,19x) mas volume baixo (só R$382 de lucro). Regra: ROAS alto com volume baixo pode perder pra ROAS menor com volume alto em lucro absoluto.
- Resultado da otimização ao vivo: CPA médio da campanha caiu de R$50 para R$42 só desativando os piores criativos e conjuntos.

- Fonte: transcricoes/curso-id15/19-trafego-para-ecommerce/06-Otimizando_na_Pr_tica.md

### Públicos quente e Remarketing

**Aula:** 151

- Depois de validar os melhores conjuntos: criar uma campanha NOVA dedicada aos públicos vencedores (verba maior), mantendo a campanha de teste original ativa (ela continua vendendo, não desativar).
- Campanha de REMARKETING: diferença-chave é NÃO usar lookalike/semelhantes — só os públicos reais (quem adicionou ao carrinho, quem iniciou checkout, quem comprou — exclui compradores — quem engajou no Instagram, seguidores). Criativo de remarketing precisa ter OFERTA/copy que reconhece que a pessoa já viu (ex. "vi que você iniciou a compra, finalize agora e ganhe 10% de desconto").
- Modelo mental do "ciclo infinito": compra de dados → campanha de vendas com os dados → se não converteu, cai no remarketing → remarketing não convertido cai em outro remarketing mais agressivo → e assim por diante, com a verba subindo conforme a entrada de receita permite comprar mais dados.

- Fonte: transcricoes/curso-id15/19-trafego-para-ecommerce/07-P_blicos_quente_e_Remarketing.md

## Outras Aulas (catálogo de aulas legadas/duplicadas que o Membriz mantém soltas fora dos módulos principais)

### Modelos de Contratos

**Aula:** 158

- Exceção — vídeo tem 5 segundos (yt-dlp: duration=5, availability=unlisted), sem conteúdo substancial e com legenda desativada. Verificado em 2026-10-03. Nada a resumir.

- Fonte: transcricoes/curso-id15/19-trafego-para-ecommerce/18-Modelos_de_Contratos.md

### Como as Campanhas funcionam na Prática! / Como definir seu Objetivo de Campanha! / Tudo sobre Conjuntos de Anúncios / Orçamento! (CBO, ABO, Diário e Vitalício) / Entendendo os Anúncios / Criando uma Campanha na Prática

**Aulas:** 230, 231, 232, 233, 234, 235

- Conteúdo IDÊNTICO, palavra por palavra (confirmado por diff), às aulas 305, 306, 307, 308, 309, 310 do módulo "Curso de Tráfego do Zero" — ver resumo completo em `skill/references/aulas/03-curso-trafego-do-zero.md`. São a mesma gravação listada duas vezes no Membriz sob ids antigos.

- Fontes: transcricoes/curso-id15/19-trafego-para-ecommerce/08 a 13 (mesmo conteúdo de transcricoes/curso-id15/03-curso-trafego-do-zero/07 a 12)

### Comece aqui! Tudo que você irá aprender! (módulo Delivery)

**Aula:** 135

- Abertura do sub-módulo "campanhas para Delivery". Case de prova: cliente delivery, R$3.500 investidos (abr-ago) → R$49.000+ retornados, ROAS 13,9, lucro ~R$46.000.

- Fonte: transcricoes/curso-id15/19-trafego-para-ecommerce/14-Comece_aqui_Tudo_que_voc_ir_aprender.md

### O objetivo certo para Campanhas de Delivery

**Aula:** 136

- Melhor tipo de campanha pra delivery: CONVERSÃO (não tráfego, não WhatsApp) levando pra um CARDÁPIO DIGITAL com Pixel instalado — nunca campanha de engajamento pro WhatsApp, porque esta não dá métrica confiável (CPA, ROAS) e 90% dos clientes não reportam vendas reais do WhatsApp de volta.
- Plataformas de cardápio digital recomendadas com integração de Pixel: Goomer, Menudino, Nemo (pesquisar e se cadastrar). Se o cliente não tiver cardápio digital, vender esse serviço adicional (aumenta o ticket do contrato).
- Resultado real mostrado: campanha de conversão pra cardápio digital, últimos 30 dias, R$1.000 investidos → R$11.000 retornados, lucro líquido ~R$9.000.

- Fonte: transcricoes/curso-id15/19-trafego-para-ecommerce/17-O_objetivo_certo_para_Campanhas_de_Delivery.md

### Orçamento de Campanhas para Delivery!

**Aula:** 137

- Delivery precisa de programação por HORÁRIO e DIA DA SEMANA (só funciona dentro do expediente do estabelecimento) — isso só é possível com orçamento TOTAL/vitalício (orçamento diário não libera a opção de "programação de anúncios" por horário).
- Passo a passo: orçamento total (não diário) → ativar "vincular anúncios de acordo com uma programação" → no nível de CONJUNTO, arrastar os dias/horários de funcionamento (pode variar por dia, ex. sábado com horário diferente).
- Verba recomendada: R$20-30/dia mínimo, multiplicado por 7 (duração mínima de teste) = orçamento total de R$140-210 pra uma semana de teste.

- Fonte: transcricoes/curso-id15/19-trafego-para-ecommerce/19-Or_amento_de_Campanhas_para_Delivery.md

### Quais Públicos você deve utilizar!

**Aula:** 138

- Estrutura de 3-4 conjuntos pra delivery: (1) **Aberto**, segmentado SÓ pela cidade de atuação (nunca estado/país — delivery é hiperlocal); (2) **"ao Insta +seguidores 180 dias"** — todo mundo que engajou/visitou/comentou/enviou mensagem/salvou publicação no Instagram do estabelecimento nos últimos 180 dias, MAIS todos os seguidores (sem lookalike, pra não vazar pra fora da região); (3) **Interesses/direcionamento detalhado** — mínimo 5 interesses relacionados ao nicho (ex. pizza, delivery, fast food, pedido online); (4, só depois de ter dados) **Lookalike 1% de quem comprou + quem iniciou checkout** (compradores últimos 180 dias).
- Aviso: NÃO usar lookalike sobre o público de Instagram "ao Insta" se o Instagram tiver alcance nacional — o lookalike pode trazer gente de fora da cidade de entrega.

- Fonte: transcricoes/curso-id15/19-trafego-para-ecommerce/21-Quais_P_blicos_voc_deve_utilizar.md

### Criativos Vencedores para Delivery!

**Aula:** 139

- Regra central do criativo de delivery: precisa gerar DESEJO (comida parecendo deliciosa, realista — não "super editada"/fake) e ser SACIÁVEL — informar a localização do estabelecimento no próprio criativo, pra deixar claro que é um pedido real "a um clique de distância" (ex.: "picanha saborosa, aqui em Açailândia, peça agora" com CTA direto pro cardápio digital).
- Banco de imagens/vídeo recomendado: Pexels, Canva, Pinterest.
- Mínimo 3-5 criativos, intercalando foto e vídeo, com variações do mesmo prato (ex. "picanha 2", "picanha 4") — case real: uma variação gerou 31 vendas, outra variação do mesmo prato só 7, mostrando que pequenas mudanças de criativo têm impacto grande mesmo dentro do mesmo produto.

- Fonte: transcricoes/curso-id15/19-trafego-para-ecommerce/24-Criativos_Vencedores_para_Delivery.md

### Otimização! e Escala! (Delivery)

**Aula:** 140

- "Otimização inversível" (nome dado pelo Kevones, aplica-se a qualquer campanha, não só delivery): ordem CRIATIVO → CONJUNTO → CAMPANHA, pausando em cada nível quem estourou o CPA (vendendo caro demais) ou gastou o CPA máximo sem nenhuma venda.
- Case real: campanha com 1 criativo fraco (ROAS baixo, "grana no bolso" só R$7) desativado, mantendo só o criativo forte (12 vendas/30 dias, CPA R$9,15, ROAS 7,42, lucro R$700+) e outro "Feijoada 2" com 42 vendas a CPA R$3 (gasto R$125 → retorno ~R$2.500).
- Escala: 3 formas combinadas — (1) criar campanhas novas com públicos validados + variações de criativo parecidas às vencedoras; (2) duplicar as melhores campanhas; (3) aumentar a verba da campanha que já vende todo dia (dobrar/triplicar o orçamento vitalício inicial, ex. de R$210/semana pra 2-5x isso). Preferência pessoal do Kevones no exemplo: aumentar verba da campanha já validada em vez de criar novas (nova campanha entra em fase de aprendizado e demora pra estabilizar).
- Resultado citado: cliente com verba limitada (~R$900-1.000/mês), campanha única acumulada gastando R$2.000+ retornando R$37.000+.

- Fonte: transcricoes/curso-id15/19-trafego-para-ecommerce/25-Otimiza_o_e_Escala.md

## Domine os Infoprodutos no Meta Ads (sub-módulo)

### Domine os Infoprodutos no Meta Ads

**Aula:** 125

- Abertura do sub-módulo "campanhas para infoprodutos" (independente de nicho). Sem conteúdo técnico novo (aula de introdução/motivacional).

- Fonte: transcricoes/curso-id15/19-trafego-para-ecommerce/15-Domine_os_Infoprodutos_no_Meta_Ads.md

### Como Testar Públicos na Prática

**Aula:** 126

- Reforça o conceito "toda campanha é compra de dados" (você não paga pra usar redes sociais — você É o produto; como anunciante, você inverte isso comprando dados de quem já é usuário).
- Tipo de orçamento por volume de verba: POUCA verba → CBO (nível de campanha, deixa o Facebook decidir onde gastar, mas é "menos eficaz" porque o Facebook pode favorecer um conjunto bom e nunca testar os outros igualmente). MAIOR volume de verba → ABO (nível de conjunto) é MAIS eficaz pra validar/excluir públicos rápido, porque força gasto garantido em cada conjunto.
- Orçamento mínimo: baseado na recomendação oficial do próprio Meta Ads ("US$4 mínimo para objetivo de vendas") — multiplicar por 2-3x pra compensar a conversão BRL/USD (sugestão: ~R$8, ou R$48-70 por campanha completa). Meta também recomenda deixar a campanha ativa NO MÍNIMO 7 dias antes de julgar.
- Estrutura de teste de público recomendada: 1 campanha, 5 conjuntos — 1 Aberto + 4 com direcionamento detalhado (interesses relacionados ao produto, achados via palavra-chave principal + "sugestões" do próprio Facebook pra achar interesses parecidos).

- Fonte: transcricoes/curso-id15/19-trafego-para-ecommerce/16-Como_Testar_P_blicos_na_Pr_tica.md

### Teste de Criativos para Infoprodutos

**Aula:** 127

- Regra absoluta: NUNCA subir campanha com um criativo só. Estrutura de teste: 5 a 10 criativos (variações de estrutura/formato), repetidos nos MESMOS conjuntos (não criar criativo diferente por conjunto — isso isolaria a variável errada). Formatos recomendados: direto, estilo TikTok, de dica (detalhado no módulo de criativos avançados).
- Estrutura da copy: 5 variações de texto principal + 5 de título + 5 de descrição, cada uma podendo abordar uma dor diferente do público — maximiza a chance de achar a combinação vencedora de público + criativo + copy ao mesmo tempo.

- Fonte: transcricoes/curso-id15/19-trafego-para-ecommerce/20-Teste_de_Criativos_para_Infoprodutos.md

### Otimização para Infoprodutos

**Aula:** 128

- Métrica PRIMÁRIA (única): CPA (custo por aquisição/compra) — dentro do limite definido, mantém; estourou, mata (a nível de criativo, conjunto e campanha, nessa ordem).
- Métricas SECUNDÁRIAS de apoio (quando ainda não há venda suficiente pra julgar pelo CPA): custo por visualização da página de destino, initiate checkout, adição ao carrinho (se e-commerce) — exemplo real: campanha com custo de visualização R$2 e zero vendas (desligada) vs. outra com custo de visualização R$0,79 e 4 vendas a CPA R$6,81 (mantida) — a métrica secundária já indicava a diferença de performance antes mesmo de comparar CPA final.

- Fonte: transcricoes/curso-id15/19-trafego-para-ecommerce/22-Otimiza_o_para_Infoprodutos.md

### Escala de Infoprodutos no Meta Ads

**Aula:** 129

- 3 formas de escalar infoproduto, usadas em combinação: (1) **Lookalike** dos melhores públicos (quem comprou, iniciou checkout, visitou, engajou no Instagram) — método preferido atual do Kevones; (2) **Aumento de verba gradual** (10-20-30% por vez, nunca duplicar de uma vez — aumento abrupto faz o Facebook "testar" público mais caro e o CPA sobe); (3) **Duplicação** das melhores campanhas/conjuntos — usar com cautela, pode inflar o CPA das campanhas originais por sobreposição de público.

- Fonte: transcricoes/curso-id15/19-trafego-para-ecommerce/23-Escala_de_Infoprodutos_no_Meta_Ads.md
