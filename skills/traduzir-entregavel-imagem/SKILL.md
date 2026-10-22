---
name: traduzir-entregavel-imagem
description: Traduz imagens de oferta low ticket — entregável (módulos, e-books, PDFs de área de membros) E imagens da página de vendas (capas, mockups, bônus, depoimentos, selos, banners) — para outro idioma ou variante (pt-BR, pt-PT, espanhol, inglês, francês), nos dois sentidos (Brasil→fora e fora→Brasil), SEM regenerar a imagem — apaga o texto original dentro da própria arte e reescreve o texto traduzido no mesmo lugar, por script (Pillow), com a ilustração intacta. Inclui geometria por página, gate de resíduo do idioma original, contact sheet antes|depois e publicação no painel. Use quando o usuário pedir para traduzir módulo, bônus, e-book, páginas da área de membros ou imagens da página de vendas, levar oferta para outro país (ou trazer oferta de fora para o Brasil), adaptar pt-BR para pt-PT, ou revisar imagens que ficaram no idioma antigo.
---

# Traduzir e adaptar imagens da oferta sem regenerar

**Decisão da dona (05/10/2026):** este é o método padrão para traduzir entregável. Não regenerar a
página no GPT: o GPT redesenha e mexe na ilustração (fere a regra de carta/arte original) e gasta cota.
Rota GPT (`traduzir-pagina-es.sh`) só se a dona pedir ou se a página não tiver área de texto apagável.
**Exceção — imagens da página de vendas inteira:** padrão é GPT Work mode só com o link (seção abaixo).

Referência viva: `OFERTAS/mapa-do-tarot/site/scripts/traduz-principal-es.py` (46 páginas, commit b4192c2)
+ `scripts/es-overrides.json`. Copie dele as funções em vez de reescrever.

## Escopo (decisão da dona 05/10/2026)
Vale para **toda oferta low ticket que muda de mercado**, nos dois sentidos:
- **Brasil → fora** (ES latino, PT de Portugal, EN, FR) e **fora → Brasil** (oferta gringa modelada).
- **Entregável:** páginas-imagem dos módulos, bônus, capas dos módulos no painel.
- **Página de vendas:** capa/mockup do produto, mockups dos bônus, "por dentro", print de depoimento,
  selo de garantia, banner de checkout, imagem de order bump.
- **Variante do mesmo idioma também conta:** pt-BR → pt-PT não é só ortografia. Trocar o que soa
  brasileiro: gerúndio ("Ativando" → "A ativar"), "pra" → "para", "jeito" → "forma", "dicas" → "conselhos",
  "você" → tratamento de Portugal, gíria de depoimento ("certinho", "amei" → "recebi tudo direitinho"
  só se soar natural lá; na dúvida, frase neutra).

Oferta de fora modelada: a regra de `imagens-pagina-low` › Cross-market continua (identidade dele
predominante, peça ADAPTADA, nunca crua). Quando a mudança é **só de idioma**, use esta técnica. Quando
precisa **trocar cores também**, a rota é o GPT Work Mode de `imagens-pagina-low`, ou esta técnica para o
texto + recolorir por script se o fundo for liso.

## Adaptar culturalmente, não só traduzir (regra da dona 05/10/2026)
O texto final tem que soar escrito por alguém DE LÁ. Tradução literal reprova.
- **Espanhol neutro latino** (todos os países hispânicos da América ao mesmo tempo): `tú` (nunca
  `vosotros`, nunca `vos`); sem regionalismo (`che`, `güey`, `chévere`, `plata`, `chamba`, `pibe`); vocabulário
  comum a todos: `celular`, `computadora`, `descargar`, `correo`, `dinero`, `pareja`. Exemplos, nomes de
  pessoas em depoimento e situações do dia a dia de lá (nome latino, não brasileiro). Moeda e preço
  seguem a regra de `PRECO-MOEDA-LOCAL.md`.
- **Português de Portugal** (pt-PT, AO90): trato por `tu` ou impessoal (o `você` brasileiro soa distante
  ou estranho); sem gerúndio (`a ativar`, não `ativando`); `para`, nunca `pra`; vocabulário de lá:
  `telemóvel`, `ecrã`, `ficheiro`, `descarregar`, `registo`, `equipa`, `pequeno-almoço`, `casa de banho`,
  `facto`, `contacto`; expressões (`dicas` → `conselhos`, `jeito` → `forma`, `legal` → `fixe`/`ótimo`, `amei` →
  `adorei`). Nomes em depoimento de Portugal (Inês, Joana, Rita, Tiago).
- **Fora → Brasil:** mesmo cuidado ao contrário: português do Brasil coloquial do nicho, R$, nomes e
  referências brasileiras.
- Termo técnico do nicho no padrão do mercado (tarot ES: `Arcanos Mayores`, `El Loco`, `Bastos/Copas/
  Espadas/Oros`, `Sota/Caballero/Reina/Rey`; tarot PT-PT segue o BR nos nomes das cartas).
- Antes de rodar o script, a tabela origem → texto adaptado é revisada inteira contra esta lista.

## Página de vendas inteira → GPT Work mode só com o LINK (decisão da dona 05/10/2026)
Para adaptar TODAS as imagens da página de vendas, o caminho rápido é o ChatGPT em WORK MODE, sem
anexar nada: ele mesmo baixa as imagens da página e devolve um ZIP. Mecânica (perfil, work mode,
download): `gpt-imagem-playwright` + `domain-skills/chatgpt.com/work-mode-lote-entrega.md`; navegador visível.
Mensagem (uma só, trocar link e mercado):
> "Esta é a minha página de vendas: <URL> — está em português do Brasil. Baixa todas as imagens da
> página e adapta todas para <português de Portugal / espanhol neutro latino>, mantendo exatamente o
> mesmo visual, layout, cores e fontes — muda só o texto, incluindo o texto pequeno dos mockups. Não
> redesenhes as cartas. Mantém o nome original de cada arquivo. No fim, entrega tudo num ZIP."
Baixar o ZIP em `site/<mercado>/assets/` (pasta separada, ex.: `webp-gpt/`), revisar BR × novo lado a
lado (reprovar layout mudado, carta redesenhada, idioma antigo, texto borrado) e só então trocar os src.
O script (seções abaixo) fica pra entregável/painel e pra retoque pontual. Por que: nas folhas em
perspectiva dos mockups o script saiu borrado e com fonte errada (05/10); o GPT refaz o mockup inteiro.

## Casos especiais da página de vendas
- **Mockup em perspectiva** (tablet, folhas inclinadas): o texto está distorcido. Primeiro tentar
  apagar e escrever com transformação de perspectiva (`Image.transform` com os 4 cantos da página).
  Ficou ruim → remontar o mockup a partir das páginas JÁ traduzidas (mesma composição).
- **Print de depoimento** (comentário de rede social): reescrever o texto no mesmo balão, fonte de
  sistema (sans), mesmo tamanho; nome e foto continuam borrados como no original.
- **Selo** ("7 DIAS"/"7 DÍAS"/"7 DAYS"): texto curvo; refazer o selo inteiro só se o apagamento falhar.
- Imagem de página de vendas por mercado mora na pasta do mercado (ex.: `site/es/assets/`), nunca
  sobrescreve a do outro mercado.

## Técnica
1. **Inventário:** listar as páginas do idioma de origem (`painel/conteudo/<sku>/`). Agrupar por
   layout (capa, abertura, página de carta, exercício, lista…). Uma família de layout = uma geometria.
2. **Ler o texto original olhando a imagem** (abrir cada página). Escrever a tradução no script:
   ADAPTADO ao mercado (seção acima: ES neutro latino; PT de Portugal), mesmo sentido, sem
   acrescentar promessa nem cortar conteúdo, nomes canônicos (ex.: arcanos em espanhol: El Loco, El Mago…).
   `**negrito**` dentro da string vira bold.
3. **Geometria:** retângulo `[x0,y0,x1,y1]` de cada bloco de texto, medido sobre uma grade de
   coordenadas desenhada na página. Família no JSON, ajuste fino por página em `overrides`.
4. **Apagar (`inpaint`):** preencher o retângulo interpolando na horizontal os pixels limpos das bordas.
   Funciona em fundo liso/papel/gradiente suave. Nunca apagar dentro da ilustração; só a faixa
   do nome no rodapé da carta, se tiver texto.
5. **Reescrever:** cor da tinta amostrada do texto original (`ink_color`), fonte parecida
   (Cormorant Garamond com `features=["lnum"]` para algarismos; título com serif bold; letra
   cursiva = serif inclinada com `shear_text`), mesmo alinhamento, tamanho ajustado à caixa
   (`fit_blocks`/`fit_single`). Texto maior que a caixa: reduzir fonte, nunca transbordar.
6. **Gate de resíduo:** depois de escrever, procurar traço escuro do texto antigo dentro de cada
   retângulo apagado fora das caixas novas (`residual_dark`, limite `GATE_MAX_RESIDUAL`). Reprovou =
   NÃO copia para o destino; ajusta a geometria e roda de novo.
7. **Contact sheet** `origem | traduzida` em `_prints/<idioma>-<sku>/` e **olhar todas** as páginas:
   sobra de letra antiga, texto cortado, acento faltando, sobreposição em ornamento.
8. **Publicar:** destino `painel/conteudo-<idioma>/<sku>/` com o MESMO nome de arquivo da origem;
   `scripts/otimiza-painel-webp.sh`; conferir o array `pages` do painel do idioma (mesma lista e
   ordem do painel de origem); o PDF do módulo sai do mesmo array.
9. **Conferir no ar** com conta teste: manifest lista as páginas, imagem 200, leitor abre, PDF baixa.

## Regras
- Uma pasta/sku por worker. Dois workers nunca editam o mesmo script ou JSON.
- Defeito aceito e registrado: ornamento pequeno grudado no texto pode falhar no apagamento.
  Defeito NÃO aceito: qualquer palavra do idioma antigo visível.
- Registrar no STATUS da oferta: quantas páginas, commit, defeitos conhecidos.

## Ficha de instrução plana (ícone abstrato) — NÃO traduzir/copiar, refazer ilustrada (regra da dona, 22/10/2026)
Ficha de instrução cuja arte é ícone abstrato (arco-íris, círculos, pontos, folha) em caixa vazia + bloco de NOTAS não se traduz nem se copia (nem por Pillow, nem no GPT). Refazer a FICHA INTEIRA no GPT como imagem ilustrativa real, com uma ficha nossa aprovada como referência e o prompt explicando o exercício + texto exato do módulo. Nunca card de código com foto colada. Regra completa: `criacao-low-ticket-mvt/references/PAGINAS-DE-ATIVIDADE.md` › "Ficha de instrução SEMPRE com imagem ilustrativa".
