# Prompts do Modelador (extraídos de RATO-ADS/app/server/modelador.js em 2026-11-04)

Uso LOCAL (o agente faz a análise na sessão, sem MineraAds): seguir o texto e o formato JSON de cada prompt,
preenchendo os blocos (anunciante, anúncios, página, checkout) com o que foi lido de verdade na `low-referencia`.

## System prompts
### SYSTEM_RATO
```
Você é um estrategista de modelagem de ofertas low-ticket/infoproduto no Brasil. Recebe os anúncios de um anunciante na Biblioteca do Meta e o texto da página de vendas e devolve caminhos práticos para MODELAR a oferta (copiar o que funciona mudando o que dá vantagem). Seja específico, concreto, sem enrolação, em português do Brasil. Nunca invente preço: se não aparecer, escreva "não identificado". Responda SOMENTE JSON válido. Escreva TODO texto só em português do Brasil, só alfabeto latino — nunca misture caractere de outro idioma/alfabeto (chinês, coreano, cirílico etc.) em nenhum campo. NUNCA misture palavras ou fragmentos em inglês no português (ex.: Wales, unfamiliar, stimulate, cognition, activities, translated, educational, time, value, improve, participating); traduza-os para português natural antes de devolver o JSON.
```

### SYSTEM_SPYX
```
Você é um analista sênior de ofertas (estilo SpyX) que aplica o método das 4 alavancas (TRANSFORMAÇÃO, PROBABILIDADE, TEMPO, ESFORÇO) pra diagnosticar o funil de vendas de um concorrente E modelar uma oferta própria melhor.
TRANSFORMAÇÃO (elevar): quão grande e desejável é o antes→depois prometido. PROBABILIDADE (elevar): o quanto o lead acredita que vai funcionar pra ele. TEMPO (reduzir): quanto demora até o primeiro resultado. ESFORÇO (reduzir): o que o lead precisa fazer, aprender ou abrir mão.
    Leia a página de vendas inteira (e o checkout, quando fornecido) e os criativos (texto e transcrição de vídeo quando houver) antes de responder. Cite o que leu, nunca invente. Comece listando as seções que leu e o que não viu ("nao_visto"). Reaja como comprador cético em 1ª pessoa, etapa por etapa (anúncio, página, checkout). Marque "não identificado" quando faltar dado — nunca invente prova social, depoimento ou número. Nunca prometa, na oferta modelada, o que o produto não entrega — isso derruba a probabilidade. Responda SOMENTE JSON válido, em português do Brasil (exceto quando a tarefa pedir texto em outro idioma, nesse caso só os campos de texto comercial saem no idioma pedido e a análise continua em português). Nunca misture caractere de outro idioma/alfabeto (chinês, coreano, cirílico etc.) fora do que foi pedido. NUNCA misture palavras ou fragmentos em inglês dentro da análise em português; revise e traduza qualquer vazamento antes de devolver o JSON.
```

### SYSTEM_RAIOX
```
Você é um analista de ofertas low-ticket que lê uma referência e descreve, com disciplina, o que ela realmente é — sem inflar nem inventar. Separe sempre: o que foi observado na página/anúncios, o que o vendedor afirma (alegação, não fato), e sua própria leitura/interpretação. Nunca trate alcance, tempo no ar ou replicação de criativo como prova de faturamento ou resultado do anunciante — são só sinais de que o anúncio roda. Quando não conseguir confirmar algo (checkout pago, conteúdo interno do material, dado ausente na página), escreva "não consegui ver" — nunca preencha com suposição disfarçada de fato. Frases entre aspas só se estiverem escritas literalmente na página, no FAQ, em depoimento ou comentário citado pelo material — com a fonte; do contrário é leitura sua, não citação. Responda SOMENTE JSON válido, em português do Brasil, sem misturar outro idioma ou alfabeto.
```

## Raio-X (6 pilares + 10 propostas)
```js
function buildRaioxPrompt(oferta, landing, preco, pesquisaComercial) {
  const pilar = '{"pilar":"","como_aparece_na_referencia":"","preservar_ou_explorar_troca":""}';
  const classificacaoPilar = '{"pilar":"","status":"trocado|adaptado|mantido"}';
  const fonte = `{"ranking":0,"fonte":"","tipo":"estrutural|upgrade|cultural","pergunta_respondida":"","proposta":{"titulo":"","o_que_muda":"a decisão principal trocada","entrega":"","publico":"","mercado":"só preenche quando fonte=outro_mercado ou tipo=cultural: país destino","idioma_alvo":"só junto com mercado: idioma desse país","demanda":"alta|media|baixa","dificuldade":"baixa|media|alta","por_que":""},"pilares":[${classificacaoPilar},${classificacaoPilar},${classificacaoPilar},${classificacaoPilar},${classificacaoPilar},${classificacaoPilar}],"filtro_comercial":{"comprador_identificavel":true,"necessidade_especifica_ou_desejo_forte":true,"cena_de_uso_descritivel":true,"trabalho_principal_ja_feito_pelo_produtor":true,"diferencial_visivel_ao_abrir_uma_unidade":true,"motivo_pra_pagar_mesmo_com_alternativa_gratis":true,"producao_viavel_pro_preco":true}}`;
  return `ANUNCIANTE: ${oferta.nome}${oferta.anuncios ? ` · ${oferta.anuncios} anúncios ativos · o mais antigo roda há ${oferta.dias_rodando} dias` : ' (link direto da página de vendas, sem leitura dos anúncios)'}
${oferta.criativos.length ? `ANÚNCIOS (numerados; use como evidência, nunca como prova de resultado):\n${oferta.criativos.map((c, i) => `[${i + 1}] ${JSON.stringify(c)}`).join('\n')}\n` : ''}
PREÇOS ENCONTRADOS NA PÁGINA: ${preco || 'nenhum'}
${landingBlock(landing)}
${pesquisaComercialBlock(pesquisaComercial)}
Faça a leitura em duas partes.

PARTE 1 — RAIO-X CURTO: monte um quadro compacto da oferta real (nome e promessa central, nicho e subnicho, público ideal, entregável principal e a unidade que ele conta — ex.: "40 projetos", "12 fichas" —, preço e planos quando informados, bônus e adicionais relevantes, evidências disponíveis e o que não deu pra confirmar). Não confunda quantidade de página com quantidade de item entregue, nem deduza o conteúdo só pela capa. Depois mapeie os 6 pilares nesta ordem — PÚBLICO (quem compra, quem aplica, quem recebe o benefício, podem ser pessoas diferentes), RESULTADO (a tarefa/necessidade concreta que o produto resolve — não confundir com o assunto/domínio), CONTEÚDO (os assuntos e componentes entregues), MECANISMO (o que a pessoa faz com o material na situação real de uso — não confundir com o formato do arquivo), FORMATO (PDF, fichas, planilha, cartões, mapa etc. — é só o suporte, não o mecanismo), MERCADO (país, idioma, contexto) — dizendo como cada pilar aparece na referência e se vale preservar ou vale trocar. Resuma o motor da oferta (formato + mecanismo + tipo de nome) em uma frase. Descreva o comprador em até 4 linhas na voz dele (a cena concreta, a dor/desejo, com o que ele se vira hoje sem o produto, a objeção que o faria desistir) — frase entre aspas só quando estiver escrita de fato na página/FAQ/depoimento, com a fonte indicada.

PARTE 2 — EXATAMENTE 10 NOVAS PROPOSTAS: priorize a modelagem estrutural (trocar UM pilar principal por vez, preservando o resto do motor), usando como fontes — conteúdo complementar/bônus que ganharia peso como produto próprio, público vizinho com a mesma necessidade, outro resultado concreto do mesmo comprador, outro mecanismo pro mesmo resultado, outro formato pro mesmo conteúdo, outro mercado/idioma diferente da referência, e nome/enquadramento diferente para o mesmo motor. Também aceite, quando fizer mais sentido que uma troca estrutural, no máximo 1-2 propostas do tipo "upgrade" (mesma ideia central, melhoria visível de cobertura/aplicação/facilidade — nunca só aumentar quantidade com item repetido) e no máximo 1-2 do tipo "cultural" (mesma ideia, outro idioma/contexto, com adaptação real da cultura local, não só tradução). Cada proposta parte da REFERÊNCIA ORIGINAL, nunca acumula a troca de uma proposta anterior. Em cada proposta, classifique os 6 pilares como "trocado" (a decisão principal, 1 ou 2 pilares no máximo), "adaptado" (ajuste que a troca obrigou) ou "mantido" (preservado da referência) — nunca use "adaptado" pra esconder outra troca independente. Antes de incluir uma proposta, confira o filtro comercial (comprador identificável, necessidade específica/desejo forte, cena de uso descritível, trabalho principal já feito pelo produtor, diferencial visível ao abrir uma unidade do material, motivo pra pagar mesmo com alternativa grátis, produção viável pro preço) — descarte e substitua qualquer ideia abstrata, formulário vazio que exige o comprador pesquisar/construir tudo, mudança só de capa/nome/headline, ou quantidade inflada com duplicação sem unidade nova de verdade. Toda proposta de fonte "outro_mercado" ou tipo "cultural" tem que preencher "proposta.mercado" (país) e "proposta.idioma_alvo" — sem isso a troca de mercado não dá pra aprofundar depois. Distribua as 10 entre as fontes/tipos (pode repetir), e ranqueie de 1 (melhor) a 10 por demanda estimada × facilidade de produzir.

Devolva JSON exatamente neste formato:
{"raiox":{"nome":"","promessa":"","nicho":"","subnicho":"","publico":"","entregavel":"","unidade_contada":"","preco":"${preco ? '' : 'não identificado'}","bonus":"","evidencias_e_limites":"","nao_consegui_ver":["itens que não deu pra confirmar"]},
"pilares":[${pilar},${pilar},${pilar},${pilar},${pilar},${pilar}],
"motor":"frase: formato + mecanismo + tipo de nome",
"comprador":{"cena":"","dor_e_desejo":"","alternativa_atual":"","objecao_que_faria_desistir":""},
"citacoes":[{"texto":"só se estiver escrito literal na referência","fonte":"onde apareceu (página, FAQ, depoimento, comentário)"}],
"propostas":[${fonte},${fonte},${fonte},${fonte},${fonte},${fonte},${fonte},${fonte},${fonte},${fonte}],
"ressalvas":["o que não foi possível confirmar nesta leitura"]}
"pilares": um item por pilar, nesta ordem exata — publico, resultado, conteudo, mecanismo, formato, mercado. "propostas": exatamente 10, "ranking" de 1 a 10 sem repetir, "fonte" um dos sete tipos (conteudo_complementar, publico_vizinho, outro_resultado, outro_mecanismo, outro_formato, outro_mercado, outro_nome) quando "tipo":"estrutural" — "fonte" pode ficar vazia quando "tipo" for "upgrade" ou "cultural". Cada "proposta.pilares" tem exatamente 6 itens, mesma ordem dos pilares, com "status" trocado/adaptado/mantido. "filtro_comercial": todos os 7 campos true antes de incluir a proposta no JSON — se algum ficar false, substitua a proposta por outra que passe no filtro.`;
}
```

## Saneamento do Raio-X
```js
function sanearRaiox(raioxOut) {
  const propostas = raioxOut?.propostas;
  if (!Array.isArray(propostas) || !propostas.length) return;
  const vistos = new Set();
  let reordenou = false;
  propostas.forEach((p) => {
    if (typeof p.ranking !== 'number' || vistos.has(p.ranking)) reordenou = true;
    else vistos.add(p.ranking);
    const f = p.filtro_comercial;
    if (!f || typeof f !== 'object') { p.filtro_comercial = {}; }
    for (const k of ['comprador_identificavel', 'necessidade_especifica_ou_desejo_forte', 'cena_de_uso_descritivel', 'trabalho_principal_ja_feito_pelo_produtor', 'diferencial_visivel_ao_abrir_uma_unidade', 'motivo_pra_pagar_mesmo_com_alternativa_gratis', 'producao_viavel_pro_preco']) {
      if (typeof p.filtro_comercial[k] !== 'boolean') p.filtro_comercial[k] = true;
    }
    if (!Array.isArray(p.pilares) || p.pilares.length !== 6) console.warn('[modelador] raio-x: proposta sem os 6 pilares classificados', JSON.stringify({ titulo: p.proposta?.titulo, pilares: (p.pilares || []).length }));
  });
  if (reordenou) {
    console.warn('[modelador] raio-x: ranking vindo do LLM com duplicata/faltando, renumerando por ordem de chegada');
    propostas.forEach((p, i) => { p.ranking = i + 1; });
  }
}
```

## SpyX — diagnóstico (alavancas, persona, fraquezas)
```js
function buildSpyxDiagnosticoPrompt(oferta, landing, pesquisaComercial) {
  return `ANUNCIANTE: ${oferta.nome}${oferta.anuncios ? ` · ${oferta.anuncios} anúncios ativos · o mais antigo roda há ${oferta.dias_rodando} dias` : ' (link direto da página de vendas, sem leitura dos anúncios)'}
${oferta.criativos.length ? `CRIATIVOS (texto do anúncio + transcrição do vídeo quando capturada; numerados):\n${oferta.criativos.map((c, i) => `[${i + 1}] ${JSON.stringify(c)}`).join('\n')}\n` : ''}
${landingBlock(landing)}
${pesquisaComercialBlock(pesquisaComercial)}

Isto é só a ETAPA 1 (diagnóstico) — NÃO modele a oferta ainda. Siga esta ordem: (1) liste as seções que leu de verdade, (2) extraia os dados do funil, (3) vire o lead e reaja etapa a etapa, (4) dê nota nas 4 alavancas, (5) aponte fraquezas exploráveis, (6) escreva o posicionamento dele × o nosso, (7) analise cada criativo diferente.
Devolva JSON exatamente neste formato:
{"secoes_lidas":["seções que você realmente leu, em ordem"],"nao_visto":["o que não deu pra ver: checkout, quiz, bônus etc."],
"extracao":{"promessa":"","mecanismo":"","entregavel":"","bonus":"","garantia":"","preco_parcelamento":"","order_bumps":"","upsell_downsell":"","plataforma_checkout":"","prova_social":""},
"persona":{"descricao":"2 linhas: idade, rotina, dor, quanto gasta online",
  "etapas":[{"etapa":"anuncio","fisgou":"","desconfiou":"","duvida":"","objecao":"","faltou_ver":"","desistiria_em":""},{"etapa":"pagina","fisgou":"","desconfiou":"","duvida":"","objecao":"","faltou_ver":"","desistiria_em":""},{"etapa":"checkout","fisgou":"","desconfiou":"","duvida":"","objecao":"","faltou_ver":"","desistiria_em":""}],
  "compraria":"sim|nao|talvez","por_que":"",
  "reacao_anuncio":"= etapas[0] resumida em 1ª pessoa","reacao_pagina":"= etapas[1] resumida em 1ª pessoa","objecao_principal":"","duvida_sem_resposta":"","momento_que_desistiria":""},
"alavancas_oferta_dele":{"transformacao":{"nota":0,"por_que":""},"probabilidade":{"nota":0,"por_que":""},"tempo":{"nota":0,"por_que":""},"esforco":{"nota":0,"por_que":""},"mais_fraca":"","nao_tocada":""},
"fraquezas":[{"problema":"","alavanca":"","como_eu_corrijo":""}],
"posicionamento":{"ele_vende":"frase curta","nos_vendemos":"frase curta","frase":"a diferenciação em 1 frase"},
"criativos_analise":[{"n":1,"formato":"","gancho":"","angulo":"","prova":"","cta":"","por_que_converte":"","nossa_versao":""}],
"ressalvas":["o que não foi possível confirmar"]}
"criativos_analise": 1 item por criativo diferente (texto e/ou transcrição), até 10, "n" = número do criativo na lista acima.
"fraquezas": use as objeções/desconfianças da persona como principal fonte, citando a qual alavanca cada uma pertence.
Preencha também os campos antigos (reacao_anuncio, reacao_pagina, objecao_principal, duvida_sem_resposta, momento_que_desistiria) dentro de "persona" — são resumos dos campos novos, nunca deixe em branco.`;
}
```

## Mercado / outro idioma
```js
function buildMercadoPrompt(oferta, landing, diagnostico) {
  return `Já diagnostiquei esta oferta pelas 4 alavancas (etapa 1):
${JSON.stringify(diagnostico)}

ANUNCIANTE: ${oferta.nome} (${oferta.pais_origem || 'país de busca: Todos'})
${landingBlock(landing)}

Agora avalie se vale a pena levar esta oferta pra fora do mercado de origem. Siga esta ordem: (1) a dor/desejo é universal ou local (cultura, religião, sistema escolar, datas, leis, moeda, referências locais)? (2) cada alavanca se sustenta fora (prova social local, prazo/forma de entrega, idioma, pagamento)? (3) dê nota 0-10 pra cada mercado candidato (nunca escolha automaticamente o país de origem); (4) o que não se traduz e os riscos; (5) estime se alguém já levou essa oferta pra fora e dê 5 termos de busca por mercado.
Devolva JSON exatamente neste formato:
{"dor_universal_ou_local":{"veredito":"universal|local|mista","por_que":""},
"alavancas_fora":{"transformacao":{"nota":0,"sustenta_fora":""},"probabilidade":{"nota":0,"sustenta_fora":""},"tempo":{"nota":0,"sustenta_fora":""},"esforco":{"nota":0,"sustenta_fora":""}},
"mercados":[{"pais":"","idioma":"","nota":0,"quente":true,"por_que":""}],
"nao_traduz":["o que não se traduz / precisa adaptar"],"riscos":["concorrência, nicho saturado, políticas de anúncio da Meta etc."],
"termos_biblioteca":[{"mercado":"","termos":["5 termos no idioma do mercado"]}],
"ja_levaram_pra_fora":"estimativa com o motivo",
"recomendacao":"manter mercado original, mudar só posicionamento, mudar de país, ou mudar de país e idioma — e por quê"}
"mercados": avalie no mínimo Latam em espanhol (México, Colômbia, Peru, Chile, Argentina), Estados Unidos em inglês e Portugal, além de outros mercados relevantes pro nicho. Marque "quente":true nos de potencial forte.`;
}
```

## Bloco de direção (etapa 2)
```js
function direcaoBlock(direcao, mercado) {
  // "Mesmo idioma" = modelar pra ONDE A DONA VENDE (Brasil, português), nunca no idioma da página
  // original lida — senão uma página espanhola/inglesa vazava pro texto comercial da oferta modelada.
  // `mercado` é o diagnóstico inteiro ({mercados:[{pais,idioma,...}]}), não tem campo .idioma direto —
  // acha o idioma pelo país escolhido em direcao.mercado (é o que o CLI/tela mandam, sem idioma_alvo).
  const paisEscolhido = mercado?.mercados?.find((m) => m.pais?.toLowerCase() === direcao.mercado?.toLowerCase());
  const idiomaAlvo = direcao.idioma === 'outro' ? (direcao.idioma_alvo || paisEscolhido?.idioma || 'a definir') : 'português do Brasil';
  const ideiaBlock = direcao.ideia ? `IDEIA ESCOLHIDA (modele ESTE caminho, não invente outro):
- Título: ${direcao.ideia.titulo || ''}
- Família: ${direcao.ideia.tipo || ''}
- O lead recebe: ${direcao.ideia.entrega || ''}
- Descrição: ${direcao.ideia.descricao || ''}
- Público da ideia: ${direcao.ideia.publico || '(nenhum — use a persona do diagnóstico)'}
- Por quê: ${direcao.ideia.por_que || ''}
- Resolve (fraqueza/alavanca que esta ideia corrige): ${direcao.ideia.resolve || ''}
- Evidência: ${direcao.ideia.evidencia || ''}
` : '';
  return `${ideiaBlock}DIREÇÃO ESCOLHIDA PELA DONA:
- Mercado/idioma: ${direcao.idioma === 'outro' ? `LEVAR PRA OUTRO IDIOMA — mercado "${direcao.mercado || mercado?.pais || 'a definir'}", idioma "${idiomaAlvo}"` : 'MESMO IDIOMA/MERCADO da oferta original'}
- Caminho/ângulo escolhido: ${direcao.caminho || '(nenhum texto livre — siga a ideia escolhida acima, se houver; senão decida com base no diagnóstico)'}
- Público principal (não misture públicos; sobrepõe o público da ideia se vier preenchido): ${direcao.publico_principal || '(não informado — use o público da ideia, ou a persona do diagnóstico)'}
- Regras obrigatórias do nicho: ${direcao.regras_nicho || '(nenhuma regra extra informada)'}
IDIOMA DE SAÍDA: todo texto comercial (oferta, página, ganchos, roteiros, copies) sai em "${idiomaAlvo}", natural do mercado — nunca tradução literal. A análise (alavancas_comparacao, diferenciacao) continua em português do Brasil.`;
}
```

## Caminhos 1-4
```js
function buildCaminhosPromptA(oferta, landing, preco, spyx) {
  const fams = FAMILIAS_CAMINHOS.slice(0, 4);
  return `Já diagnostiquei esta oferta pelo método das 4 alavancas (etapa 1 SpyX):
${JSON.stringify(spyx)}

ANUNCIANTE: ${oferta.nome}${oferta.anuncios ? ` · ${oferta.anuncios} anúncios ativos · o mais antigo roda há ${oferta.dias_rodando} dias` : ' (link direto da página de vendas, sem leitura dos anúncios)'}
PREÇOS ENCONTRADOS NA PÁGINA: ${preco || 'nenhum'}
${landingBlock(landing)}

Agora, em cima desse diagnóstico (não do zero), abra caminhos práticos de modelagem nestas 4 famílias: ${fams.join(', ')}.
Cada ideia tem que citar, em "resolve", qual fraqueza, buraco ou alavanca fraca do diagnóstico ela corrige — não é genérico, é em cima do que já foi lido. "mesma_oferta_melhorada" = só corrige os buracos já identificados, sem trocar público/ângulo/nicho (1 ideia só). "demanda_palpite" é chute, nunca invente número. Preço na moeda da oferta original, nunca R$ fixo se a oferta não for brasileira. Não prometa o que o produto não entrega.
Devolva JSON exatamente neste formato:
{"diagnostico":{"produto":"","publico":"","promessa":"","mecanismo":"","formato":"","preco":"","por_que_funciona":""},
"modelagens":[{"tipo":"mesma_oferta_melhorada","ideias":[${IDEIA_SHAPE}]},{"tipo":"subnichar","ideias":[${IDEIA_SHAPE},${IDEIA_SHAPE}]},{"tipo":"trocar_publico","ideias":[${IDEIA_SHAPE},${IDEIA_SHAPE}]},{"tipo":"trocar_angulo","ideias":[${IDEIA_SHAPE},${IDEIA_SHAPE}]}]}
"diagnostico": preencha a partir do que já está no SpyX (extracao, persona), sem reler nada.`;
}
```

## Caminhos 5-8 + ranking
```js
function buildCaminhosPromptB(oferta, landing, preco, spyx, modelagensA) {
  const fams = FAMILIAS_CAMINHOS.slice(4);
  return `Já diagnostiquei esta oferta (etapa 1 SpyX) e já abri as 4 primeiras famílias de caminhos (etapa 1c-A):
DIAGNÓSTICO SPYX: ${JSON.stringify(spyx)}
CAMINHOS JÁ ABERTOS (famílias ${FAMILIAS_CAMINHOS.slice(0, 4).join(', ')}): ${JSON.stringify(modelagensA)}

ANUNCIANTE: ${oferta.nome}
PREÇOS ENCONTRADOS NA PÁGINA: ${preco || 'nenhum'}
${landingBlock(landing)}

Agora abra as 4 famílias restantes: ${fams.join(', ')}. "outro_idioma": 1-2 ideias, cada uma com "mercado" preenchido (país+idioma sugerido), usando a lógica de dor universal/local de forma resumida (não precisa repetir o diagnóstico de mercado completo). "trocar_nicho": a extração/mecanismo do original serve de referência de MECANISMO, nunca de público.
Depois, olhando as 8 famílias inteiras (as 4 já abertas + estas 4), escolha o top3 e o top1 geral, citando "resolve" em cada um.
Devolva JSON exatamente neste formato:
{"modelagens":[{"tipo":"trocar_roupagem","ideias":[${IDEIA_SHAPE},${IDEIA_SHAPE}]},{"tipo":"trocar_formato","ideias":[${IDEIA_SHAPE},${IDEIA_SHAPE}]},{"tipo":"trocar_nicho","ideias":[${IDEIA_SHAPE},${IDEIA_SHAPE}]},{"tipo":"outro_idioma","ideias":[${IDEIA_SHAPE},${IDEIA_SHAPE}]}],
"top3":[{"titulo":"","tipo":"uma das 8 famílias","justificativa":"","evidencia":"","resolve":""}],
"top1":{"titulo":"","tipo":"","justificativa":"","plano":["passo 1","passo 2","passo 3"],"resolve":""},
"ressalvas":["o que não foi possível confirmar"]}
"top3": exatamente 3 itens, de qualquer família (não só as últimas 4).`;
}
```

## Etapa 2A — oferta modelada + alavancas dele × nossa
```js
function buildModelarPromptA(oferta, landing, diagnostico, direcao, mercado, pesquisaModelagem) {
  return `Já diagnostiquei esta oferta pelas 4 alavancas (etapa 1):
${JSON.stringify(diagnostico)}
${mercado ? `\nDIAGNÓSTICO DE MERCADO (etapa 1b):\n${JSON.stringify(mercado)}\n` : ''}
ANUNCIANTE: ${oferta.nome}
${landingBlock(landing)}

${direcaoBlock(direcao, mercado)}
${pesquisaComercialBlock(pesquisaModelagem)}
Modelar, não clonar: mude 10-30% (nome, headline, números, bônus) mas mantenha o que já valida e vende. Mexa primeiro na alavanca mais fraca do diagnóstico. Nunca prometa o que o produto não entrega. Nunca invente prova/depoimento/números.
Monte a ETAPA 2A — a oferta modelada. Devolva JSON exatamente neste formato:
{"oferta_modelada":{"nomes":["5 opções de nome, no idioma de saída"],"nome":"o nome escolhido","promessa":"","mecanismo":"","entregavel":"MVP rápido de produzir",
  "bonus":[{"nome":"","conteudo":"","alavanca":""}],"garantia":"",
  "preco_sugerido":"","ancora":"","moeda":"código/símbolo da moeda do mercado escolhido",
  "funil":{"entrada":"oferta de entrada, preço baixo","popup":"pop-up/upgrade pro kit completo, se fizer sentido","order_bump":"","upsell":"","downsell":""},
  "order_bump":"= funil.order_bump (campo antigo, mantido)","upsell":"= funil.upsell (campo antigo, mantido)",
  "alavanca_por_item":[{"item":"nome do bônus/order bump/upsell","alavanca":""}]},
"alavancas_comparacao":{"transformacao":{"dele":0,"minha":0,"por_que":""},"probabilidade":{"dele":0,"minha":0,"por_que":""},"tempo":{"dele":0,"minha":0,"por_que":""},"esforco":{"dele":0,"minha":0,"por_que":""}},
"demanda_modelagem":{"existe_prova":true,"evidencia":"cite a pesquisa comercial real acima quando houver, ou diga que não achou prova","risco":"se não achou prova, diga o risco de seguir sem validação"}}
Preço: moeda local (ou dólar com âncora, se o mercado pedir), isca de preço baixo no anúncio + pop-up do kit completo quando fizer sentido pro funil.`;
}
```

## Etapa 2B — página, ganchos, roteiros, copies
```js
function buildModelarPromptB(oferta, landing, diagnostico, direcao, mercado, ofertaModelada) {
  return `Já diagnostiquei esta oferta (etapa 1) e modelei a oferta nova (etapa 2A):
DIAGNÓSTICO: ${JSON.stringify(diagnostico)}
OFERTA MODELADA: ${JSON.stringify(ofertaModelada)}

ANUNCIANTE ORIGINAL: ${oferta.nome}
${landingBlock(landing)}

${direcaoBlock(direcao, mercado)}

Agora monte a ETAPA 2B a partir da oferta modelada acima: a página de vendas seção por seção, 5 ganchos, 3 roteiros de criativo, 4 copies de anúncio, a diferenciação frente ao concorrente e o checklist de lançamento. Nunca invente prova/depoimento/números: onde não houver prova real, sugira como construir credibilidade com demonstração do material.
HEADLINE PADRÃO (vale pra "pagina.headline" e pro "titulo" de cada copy de anúncio — mesmo molde nos dois, nunca ângulos diferentes entre página e anúncio): escolha o molde que melhor serve o motor da oferta — Inventário ("[número] [item] prontos para [uso]", quando o forte é a coleção contável e pronta), Domínio ("Domine [assunto] e [consequência concreta na vida]", quando o produto fecha um corpo de conhecimento) ou Descoberta ("Descubra [mecanismo] que [resultado], sem [objeção]", quando o diferencial é o método). A headline vende o resultado final que o avatar quer, nunca um degrau intermediário (formato, organização, quantidade pura) — teste: se trocar o nome do produto e a frase continuar servindo pra qualquer coisa, tá genérica, refaça. Devolva JSON exatamente neste formato:
{"pagina":[{"secao":"headline","texto":"","molde":"inventario|dominio|descoberta"},{"secao":"subheadline","texto":""},{"secao":"dor","texto":""},{"secao":"identificacao","texto":""},{"secao":"solucao","texto":""},{"secao":"mecanismo","texto":""},{"secao":"demonstracao","texto":""},{"secao":"incluido","texto":""},{"secao":"beneficios","texto":""},{"secao":"bonus","texto":""},{"secao":"prova","texto":""},{"secao":"oferta","texto":""},{"secao":"garantia","texto":""},{"secao":"faq","texto":""},{"secao":"cta","texto":""}],
"ganchos":[{"texto":"","angulo":"","dor":"","alavanca":""}],
"roteiros":[{"tipo":"ugc","gancho":"","desenvolvimento":"","demonstracao":"","cta":""},{"tipo":"demonstracao","gancho":"","desenvolvimento":"","demonstracao":"","cta":""},{"tipo":"dor_solucao","gancho":"","desenvolvimento":"","demonstracao":"","cta":""}],
"copies_anuncio":[{"angulo":"","titulo":"","molde":"inventario|dominio|descoberta","texto":""}],
"diferenciacao":"comparação textual: público, promessa, mecanismo, entregável, esforço, valor percebido, preço, diferencial — por que ganhamos dele",
"checklist_lancamento":["itens práticos: marca/Instagram no idioma, criativos, página, demonstrações reais, checkout na moeda certa, meios de pagamento locais, order bump, upsell, entrega automática, atendimento, revisão de políticas Meta"]}
"ganchos": exatamente 5, cada um atacando uma alavanca (pode repetir alavanca). "roteiros": exatamente 3, nessa ordem. "copies_anuncio": exatamente 4, com ângulos diferentes mas podendo repetir molde de headline quando fizer sentido. Textos de página/ganchos/roteiros/copies no idioma de saída definido acima.`;
}
```

## Etapa 2C — lead reagindo à oferta nova
```js
function buildModelarPromptC(oferta, diagnostico, direcao, mercado, ofertaModelada, pagina) {
  return `Já diagnostiquei esta oferta (etapa 1), modelei a oferta nova (etapa 2A) e escrevi a página (etapa 2B):
DIAGNÓSTICO: ${JSON.stringify(diagnostico)}
OFERTA MODELADA: ${JSON.stringify(ofertaModelada)}
PÁGINA NOVA: ${JSON.stringify(pagina)}

ANUNCIANTE ORIGINAL: ${oferta.nome}
${direcaoBlock(direcao, mercado)}

Agora monte a ETAPA 2C: 5 criativos de imagem (estático/carrossel, pelo menos 1 carrossel) pra Meta Ads, e a MESMA persona da etapa 1 reagindo à OFERTA NOVA (não à do concorrente), cética, etapa por etapa.
Regras dos estáticos: preço = sempre o plano/entrada mais barato; nunca cite bônus nem contagem de módulos na imagem; o texto vai ESCRITO dentro da arte (texto_na_imagem), nunca como overlay solto; a cena é orgânica (foto de celular, uso real), nunca mockup de produto nem print de PDF.
Devolva JSON exatamente neste formato:
{"criativos_imagem":[{"tipo":"estatico","angulo":"","dor":"","alavanca":"","texto_na_imagem":"frase curta no idioma de saída","cena":"o que aparece na foto/arte","titulo":"","texto":"legenda do anúncio"},{"tipo":"estatico","angulo":"","dor":"","alavanca":"","texto_na_imagem":"","cena":"","titulo":"","texto":""},{"tipo":"estatico","angulo":"","dor":"","alavanca":"","texto_na_imagem":"","cena":"","titulo":"","texto":""},{"tipo":"carrossel","angulo":"","dor":"","alavanca":"","texto_na_imagem":"","cena":"","slides":["texto slide 1","texto slide 2","texto slide 3"],"titulo":"","texto":""},{"tipo":"carrossel","angulo":"","dor":"","alavanca":"","texto_na_imagem":"","cena":"","slides":["","",""],"titulo":"","texto":""}],
"lead_oferta_nova":{"etapas":[{"etapa":"anuncio","fisgou":"","desconfiou":"","duvida":"","objecao":"","faltou_ver":"","desistiria_em":""},{"etapa":"pagina","fisgou":"","desconfiou":"","duvida":"","objecao":"","faltou_ver":"","desistiria_em":""},{"etapa":"checkout","fisgou":"","desconfiou":"","duvida":"","objecao":"","faltou_ver":"","desistiria_em":""}],"compraria":"sim|nao|talvez","por_que":"","ainda_falta":["o que ajustar na oferta/página antes de lançar"]}}
"criativos_imagem": exatamente 5 itens nessa ordem (3 estático + 2 carrossel). Texto no idioma de saída definido acima; "lead_oferta_nova" em português do Brasil.`;
}
```
