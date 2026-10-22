# LowTicket em Dólar na Prática

## Low Ticket em Dólar - Introdução

**Aula:** 247

- Mercado: América Latina, EUA, Europa (milhões compradores, alto poder aquisitivo, baixa concorrência)
- Metodologia: espiar ofertas Brasil vendendo bem → modelar/adaptar culturalmente → vender em outro idioma
- Exemplo 1: oferta Brasil em espanhol → vender mercado Latam (filtro idioma espanhol)
- Exemplo 2: oferta Brasil/EUA em francês → vender países francófonos (França, Canadá, Bélgica, Suíça)
- Moeda: vender em dólar mesmo em página em português (Facebook converte automaticamente)
- Estrutura prática: conta Facebook Ads, domínio hospedagem, Hotmart, página IA, pixels, criativos, campanhas
- Foco: estrutura básica, espionagem, instalação produto, modelagem IA, configurações, criativos, campanhas ao vivo

- Fonte: transcricoes/curso-id15/12-lowticket-em-dolar-na-pratica/01-Low_ticket_em_D_lar_-_Introdu_o.md

## Estrutura Básica para Vender em Dólar

**Aula:** 248

- Hospedagem: Hostgate (hostgate.com.br) plano P (um domínio genérico)
- Domínio genérico: fórmulacursos.online/bolo, fórmulacursos.online/outro-produto (múltiplas ofertas)
- Processo: escolher plano P → continuar carrinho → nome domínio genérico (sem acento, em português ok)
- Config hospedagem: portal cliente → sites → adicionar site → selecionar domínio (propagação 72h)
- Criar site: cPanel → WordPress install (elemento disponível em lista)
- Acesso: site-name/wp-admin para gerenciar WordPress
- Se erro 404: domínio ainda em propagação, aguardar 1-2h
- Objetivo: preparar hospedagem para upload página de vendas (próxima etapa usa Bolt.new não WordPress direto)

- Fonte: transcricoes/curso-id15/12-lowticket-em-dolar-na-pratica/02-Estrutura_B_sica_para_vender_em_d_lar.md

## Espionagem de Ofertas

**Aula:** 249

- Ferramenta: Disparo Extension (pesquisar "a disparo extension" no Chrome)
- Entrada: Biblioteca de Anúncios Facebook → ativar extensão → barra amostragem aparece
- Busca: usar lista de palavras-chave por nicho (mínimo 2 anúncios, máximo 5 dias de rodagem ideal)
- Indicadores: quantidade anúncios ativos (≥6) + constância dias (3-5 dias mínimo, 5+ dias excelente)
- Plataforma alternativa: Greenads.com.br lista ofertas escaladas prontas
- Processo: carregar anúncios manualmente, filtrar quantidades, clicar artigo para detalhar
- Validação: ninguém deixa rodando oferta prejuízo 3+ dias, logo ofertas ativas = vendendo
- Ética: não copiar oferta, modelar/adaptar culturalmente

- Fonte: transcricoes/curso-id15/12-lowticket-em-dolar-na-pratica/03-Espionagem_de_Ofertas.md

## Criando e Instalando o Produto

**Aula:** 250

- Oferta escolha exemplo: 1000 esboços pregação feminino (15 anúncios, desde julho, +validada)
- Entregável: criar com Gama App (100 esboços suficiente Latam, não exagerar em 1000)
- Prompt Gama App: "Gere 100 esboços pregação feminino. Idioma espanhol. [descrição baseada oferta]"
- PDFs: copiar cada geração de ~13 docs, repetir até 100 (limite créditos), juntar PDFs externos
- Hotmart setup: produtos → criar → ebook → nome em espanhol (Digle L tradutor melhor que Google)
- Campos: nome espanhol, descrição breve, imagem 3D (usar Books Covers 3D site), idioma espanhol
- Precificação: iniciar baixo ($0.90-$5) para validação, aumentar ticket depois
- Entregável: arquivo PDF carregado em "arquivos" produto
- Checkout config: desativar boleto, deixar Pix+cartão, adicionar banner, texto oferta
- Validação: testando produto, está "vendas ativas" após aprovação 24h (ou instantânea conta antiga)
- Próximo: configurar pixels, criar página vendas IA, subir campanhas

- Fonte: transcricoes/curso-id15/12-lowticket-em-dolar-na-pratica/04-Criando_e_Instalando_o_seu_produto.md

## Modelagem com IA (Página de Vendas)

**Aula:** 251

- Buscar: página concorrente → print cada sessão (ou copiar texto se permitido)
- ChatGPT prompt: "Quero página vendas espanhol. Cópia: [texto]. Traduza para espanhol. Imagens: [prints]"
- Detalhes prompt: sessão Hero = capa logo abaixo subhline (link imagem fornecido), botão = checkout link
- Primeira oferta card = bônus area, segunda = oferta completa checkout
- Preço: valor promo (ex R$17 por apenas R$9,90), descontos vistos, ticket médio subir
- Plataforma: Bolt.new (gera código) vs Lovable (mais pronto) vs ChatGPT raw
- Bolt.new: copiar prompt + enviar 5 prints máximo + instrução "imagens para inspirar + traduzir textos"
- Saída Bolt.new: código HTML/React pronto, editar via interface (buscar texto → control F → achar → editar)
- Movimentar elementos: selecionar componente → code view → buscar e apagar linhas botões indesejados
- Tamanhos texto: class name (ex "4xl" = grande, "2xl" = pequeno) → modificar valores
- Publicar: botão Publish → gera URL Bolt automática (gratuita)
- Host pessoal: download ZIP → extrair em hospedagem → editar index.html para adicionar slug caminho (ex "/bosquejos-mujeres/")
- Teste: acessar domínio/bosquejos-mujeres → página deve funcionar responsiva
- Configuração: adicionar pixel checkout, setup de rastreamento próxima aula

- Fonte: transcricoes/curso-id15/12-lowticket-em-dolar-na-pratica/05-Modelagem_com_IA_P_gina_de_vendas.md

## Configurações Gerais (Pixels, Fan Page, UTM)

**Aula:** 252

- Fan page: criar página Facebook temática (ex "Predicadora Eloquente. Cristianos Activos" nicho cristão)
- Capa página: imagem relacionada nicho, sem necessidade postar/aquecer/Instagram
- Pixel Facebook: criar conjunto dados → gerenciador eventos → adicionar pixel novo → ID + token
- Hotmart integração: ferramentas → pixel rastreamento → Facebook → adicionar ID pixel → selecionar eventos (compra)
- Gerar token: gerenciador eventos → gerar token → copiar → colar Hotmart
- Página HTML pixel: editar index.html (antes de </head>) → adicionar script Meta pixel + script Datafy (Hotmart)
- Verificação: Meta Pixel Helper (extensão Chrome) → reload página → confirma pixel ativo + eventos
- UTM (Ultimy): configurar tracking códigos UTM em Hotmart para rastrear campanhas
- Resultado: pixel ativo, eventos trackando, pronto para campanhas e análise ROI

- Fonte: transcricoes/curso-id15/12-lowticket-em-dolar-na-pratica/06-Configura_es_Gerais_Pixels_fun_page_utm.md

## Fazendo os Criativos

**Aula:** 253

- Estrutura padrão testada: promessa (headline) + capa produto + preço (tachado + promo) + CTA
- Variação: destacar benefício principal no meio (ex "1000 esboços")
- Ferramentas: Canva, Figma, IA (Win Ads, Ideogram) + post-edição
- Estilo mercado Latam: "simples bem feito funciona + feio converte" → caseiro melhor que profissional demais
- Headline: copiar conteúdo página vendas → jogar ChatGPT → pedir 10 variações headlines persuasivas
- Fundo: cores caseiras (amarelo, cores neutras), não muito design elaborado
- Elementos: fundo cor + capa produto + headline + preço (valor cheio taxado, valor promo em destaque) + "Clique"
- Idioma: espanhol ("Haga Click aqui" exemplo)
- Formatos testados: imagem estática, vídeo IA, split-screen TikTok+IA (todos funcionam)
- Mínimo testar: 4-5 criativos variados estrutura/cores/headlines
- Dica extra: mercado França/Bélgica/Suíça também funciona, mesma metodologia só muda idioma francês

- Fonte: transcricoes/curso-id15/12-lowticket-em-dolar-na-pratica/07-Fazendo_os_Criativos.md

## Subindo Campanha de Vendas Internacional

**Aula:** 254

- Estrutura: 1 campanha por produto, 1 pixel, público + criativo por conjunto
- Setup campanha: nome produto → testar 5 criativos inicialmente → orçamento R$30-35 ou metade ticket
- Objetivo: conversão (compra) → pixel já rastreando
- Início: "começar dia seguinte" meia-noite
- Público: limitar mais alcance → idioma (espanhol) → direcionamento detalhado (pastor/pregador)
- Gênero: mulheres (oferta feminina) → não usar como sugestão
- Localizações: mundo todo → excluir (África, Venezuela, Bolívia, Guiana, Guiana Francesa, Brasil)
- Idade: deixar automática ou 25-55
- Criativo: imagem + título (benefício) + descrição (call) → um criativo por conjunto (A1, A2, A3...)
- Duplicar campanha: para testar 5 criativos = 5 campanhas duplicadas mudando apenas criativo
- Observação: primeira validação é só produto entrada (sem order bumps, sem upsells ainda)
- Dica: esperar otimização Facebook (3-7 dias aprendizado), não parar campanha por poucos dias sem venda

- Fonte: transcricoes/curso-id15/12-lowticket-em-dolar-na-pratica/08-Subindo_a_Campanha_de_vendas_internacional.md
