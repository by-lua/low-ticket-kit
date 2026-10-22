# Kevones YouTube: regras novas (janela 60 dias, 2026-08-07 a 2026-10-05)

Gerado em 2026-10-06. Fonte: 11 transcrições do canal @1kevones em
`~/Documentos/TRAMPO/PROJETOS-MIDIA/VIDEOS-REFERENCIA/TRACKEADOR-kevones-youtube-2026-10/`
(material de terceiro, não versionado). Transcrição automática: "Ras" = ROAS, "IC" = InitiateCheckout,
"ordebup/buffup" = order bump. Cada regra cita título + data + vídeo (id). Trechos entre aspas são
transcrição literal, não tradução de sentido.

Legenda de marcação:
- **[NOVO]** não existe nos references atuais.
- **[REFINA]** complementa regra antiga sem contradizer.
- **[CONTRADIZ]** contradiz regra antiga (citada).

Versão para analisador automático (formato SE/ENTÃO): `kevones-regras-novas-2026-10.md` na raiz do workspace TRACKEADOR-AVANÇADO.

## 1. Escala por horário e escala diária

- **[NOVO] Verba começa baixa e sobe no horário de pico.** Fonte: "LowTicket: Escalando Campanhas por Horários no Meta Ads!" (22/09/2026, bzsllO6ereY). Campanhas abriram o dia com R$ 11–30; a partir das 17h o orçamento subiu (ex.: R$ 27 → R$ 280, meta R$ 1.000). Motivo dado: "quando a gente acorda, quase nenhuma venda aconteceu". Dia 20/09: 310 vendas, gasto R$ 5.000, retorno R$ 7.258; até metade do dia o gasto não chegou à metade do orçamento.
- **[NOVO] Gap de CPA define quanto subir.** Mesma fonte. Quanto maior a distância entre o custo por compra atual e o CPA máximo, mais verba entra. Exemplo: ticket R$ 24, CPA máximo R$ 14–15, custo por compra do dia R$ 2 (5 vendas, gasto R$ 11) → "mais verba eu posso inserir".
- **[NOVO] Escala por horário é recalculada todo dia pelo horário de compra do dia anterior.** Mesma fonte: "A gente fez escala diária com base no horário de compra ontem e hoje já tá fazendo de novo". Campanha que gastou R$ 454 ontem começou hoje em R$ 150.
- **[NOVO] Escala por horário: tolera ROAS baixo se o volume de finalização existe.** Mesma fonte: "ROAS de 1,31 … podem até ficar 0 a 0, mas dão volume de finalização de compra".
- **[REFINA] Escala diária = dia de pico de venda.** "LOWTICKET: Do PREJUÍZO para 2k de LUCRO por dia!" (21/09/2026, viLhlrcJPhU): "A escala diária consiste em dias de pico de venda." Escala progressiva aparece como segunda técnica em "LowTicket Sazonal Lucrando 22k em 29 dias" (29/08/2026, SCxw6jElXio): "Basicamente eu tô aplicando escala diária e escala progressiva aqui."
- **[NOVO] Lucro crescendo em degraus (escala progressiva, 4 dias).** Mesma fonte 22/09: lucro diário R$ 252 → R$ 640 → R$ 1.600 → R$ 2.200, com volume de campanhas crescendo junto.
- **[CONTRADIZ] Aumento de verba gradual 10–30%.** Regra antiga do curso (infoproduto, aulas 125–129): "aumento de verba gradual (10-30%, nunca de uma vez)". A escala por horário do vídeo 22/09 sobe a verba diária de ~R$ 27 para ~R$ 280 no mesmo dia. Leitura de cuidado: a regra antiga vale para a verba diária da campanha; a de 22/09 é modulação intradia por horário em campanha que já vende. Não aplicar 10x em campanha sem venda no horário.
- **[REFINA] Verba: esperar 7 dias antes de aumentar um criativo.** "LOWTICKET: Do PREJUÍZO para 2k" (21/09, viLhlrcJPhU): "Deixa a campanha ficar veiculada por pelo menos 7 dias e aí sim eu vou começar a aumentar a verba desse criativo". Compatível com a janela 7d do METODO-DESTILADO.

## 2. Janela de julgamento e corte

- **[NOVO] 48h mínimo antes de julgar anúncio novo.** Fontes: "LowTicket de R$24: R$9.147 em 7 dias no Meta Ads!" (17/09/2026, 7n2jP39qbxU): "as primeiras 24 são sempre ruins"; "LowTicket Plano prático para fazer 10k em 21 dias!" (05/09/2026, RQsTWULE0KQ): "E aí eu deixaria rodar por 48 horas".
- **[NOVO] Corte com 48h+ sem venda: olhar custo e volume de IC, não só CPA.** "LOWTICKET: Do PREJUÍZO" (21/09, viLhlrcJPhU): "Quando uma campanha passa mais do que 48 horas e não faz venda, eu ainda não mato. Mas eu analiso o custo e o volume de IC. Se o custo de IC está alto e o volume está baixo, […] não tem nenhum valor".
- **[CONTRADIZ/REFINA] Matar campanha que estourou CPA.** Regra antiga (METODO-DESTILADO, tabela "Primeiras 48h"): "gastou o CPA ou o ticket sem vender: pausar". Em 21/09 (viLhlrcJPhU) a Campanha 4 (7 vendas a R$ 17, CPA acima do ticket de R$ 24) NÃO foi morta porque o custo de finalização era parecido com o da campanha com ROAS > 2. Regra nova: CPA estourado não basta; checar IC antes de pausar.
- **[NOVO] Métrica secundária decide manter ou matar.** Mesma fonte: "Nesse caso, a métrica secundária em específico é a finalização de compra". ROAS de 1,5 é "excelente em uma oferta low ticket" (21/09).

## 3. Quantos criativos, quando, e estrutura

- **[NOVO] Estrutura 1-3 com ticket baixo: 1 campanha, 1 público (Advantage), 3 anúncios.** Fonte: "Nada supera o VOLUME de CRIATIVOS!" (29/09/2026, Vtjdg86wDxA) e 7n2jP39qbxU (17/09). Motivo dado: testar mais variáveis de criativo gastando menos que 1-1-1.
- **[CONTRADIZ] Ritmo de criativo novo.** Regra antiga (METODO-DESTILADO / CALLS, "Testar demais destrói o ROI"): "3 criativos novos por semana, não por dia" (nkRg5Xsnxis). Em "Passei +1 hora Otimizando Campanhas no Facebook Ads!" (07/08/2026, BCorw4x7q3s), o Kevones testa 3 anúncios a cada 2–3 dias; "Aí você vai subir ali de três a cinco criativos a cada dois dias" ao montar; com ecossistema de ~30 anúncios, "dois anúncios, três anúncios por semana, no máximo". Leitura: ritmo sobe na fase de montagem do ecossistema e cai para 2–3/semana quando já há volume. Atualiza a regra "por semana".
- **[NOVO] Meta de ecossistema: 20 anúncios, depois ~30.** "Fazendo +R$13.640 em 10 dias com LOW TICKET no Facebook Ads!" (11/08/2026, HdOidJJBPlE): "validar pelo menos dois desses anúncios para que a gente aumente o nosso ecossistema e chegue a 20 anúncios logo". Em 07/08 (BCorw4x7q3s) a conta já está com ~30 anúncios.
- **[NOVO] Lote de teste: 5 criativos novos, validar 2–3.** HdOidJJBPlE (11/08): "Os cinco podem muito bem não vender absolutamente nada, mas o que a gente quer é validar pelo menos três ou pelo menos dois".
- **[NOVO] Máximo 3 criativos por conjunto, 2–3 conjuntos por teste.** "LowTicket Plano prático para fazer 10k em 21 dias!" (05/09/2026, RQsTWULE0KQ): "No máximo três criativos, né? … tem muita gente que bota 10 criativos no conjunto, aí o orçamento todo vai para um criativo". Teste: "no mínimo de dois a três conjuntos, no máximo três criativos por campanha em cada um desses conjuntos". Orçamento de partida R$ 30–50/dia (mesma fonte).
- **[CONTRADIZ] Quantidade de conjuntos.** Regra antiga do curso (infoproduto, aulas 125–129): "Teste: 1 campanha, 5 conjuntos (1 Aberto + 4 de interesse)". RQsTWULE0KQ (05/09) e 7n2jP39qbxU (17/09) usam 1 conjunto com Advantage em campanhas ativas. Atualizar: 2–3 conjuntos no teste de low ticket sem rosto, com público Advantage quando há engajados/compradores configurados.
- **[NOVO] Isolamento: campanha que vende permanece como matriz.** "LowTicket de R$24" (17/09, 7n2jP39qbxU): "toda vez que eu validito um anúncio, eu não jogo o anúncio validado para uma nova campanha, eu mantenho ele na campanha atual. O que eu posso fazer é jogar as variáveis que não foram testadas em uma nova campanha."
- **[NOVO] Isolamento: 1 vencedor com CPA ok → desligar os outros.** Mesma fonte. Caso A: 3 vendas no B, 0 no C, 1 com CPA estourado no A → desligar A e C; B fica sozinho na campanha matriz (1-1-1 dentro da própria campanha).
- **[NOVO] Isolamento: 2 vencedores com CPA ok → manter os dois na disputa.** Mesma fonte. Caso B: A com 2 vendas, B com 4, ambos com CPA ok → desligar só o que não gastou (C); A e B seguem.
- **[NOVO] Anúncio que não gastou → nova campanha 1-3 com as variáveis não testadas.** Mesma fonte: "Seria interessante iniciar um novo teste de campanha com o anúncio C".
- **[NOVO] Anúncio com ROAS baixo não se mata só por ROAS.** Mesma fonte: ROAS 1,39 com 63 finalizações de compra "esse custo por compra só existe porque eu tenho outras campanhas que despertaram o interesse dessas pessoas" (ecossistema/remarketing automático do Meta 2026).

## 4. Volume de campanhas e criativos (ecossistema)

- **[NOVO] Volume é a alavanca principal do lucro em low ticket.** "Nada supera o VOLUME de CRIATIVOS!" (29/09, Vtjdg86wDxA): 29 dias, R$ 31.895 investidos, retorno R$ 49.803 (ROAS 1,5), 2.133 compras, 3.904 finalizações, mais de 44 mil visitas à página. Campanhas com 132–186 vendas cada. "Quando a gente começa a passar de 100 vendas em uma única campanha, o custo por compra tende a se manter".
- **[NOVO] Criativo com imagem e vídeo no mesmo ecossistema.** "Fazendo +R$13.640 em 10 dias" (11/08, HdOidJJBPlE): imagem "converte bem até pelo próprio remarketing"; combinar vídeo e imagem com ângulos diferentes.

## 5. Públicos de base (campanha própria)

- **[NOVO] Campanha "Públicos de Base" separada, sem conjunto de prospecção.** Fonte: Vtjdg86wDxA (29/09). Públicos: PageView 180d + engajamento IG/FB 7d; InitiateCheckout 7/15/30d; seguidores; envolvimento com anúncios 15d. Sempre excluir compradores 180d. "Eu vejo poucas pessoas trabalhando com os públicos de base."
- **[NOVO] Advantage com engajados + compradores substitui público de interesse.** "LowTicket de R$24" (17/09, 7n2jP39qbxU): "Toda vez que você configura os seus públicos engajados e compradores, você não precisa mais usar público de direcionamento detalhado". Campanha de remarketing automático do Meta 2026 quando engajados/compradores estão configurados.
- **[REFINA] Público validado não precisa de teste de público.** HdOidJJBPlE (11/08): "Você não tá na fase de testar público ainda porque você já tem um público validado. Então é mais fácil a gente escalar com o criativo."

## 6. Campanha de seguidores e perfil

- **[NOVO] Seguidores vindos de anúncio de conversão são sinal de oferta validada.** "Passei +1 hora Otimizando Campanhas" (07/08, BCorw4x7q3s): oferta com 200 seguidores gerados por campanha de conversão = "uma oferta que tá praticamente validada". Próximo passo recomendado: campanha de seguidores separada.
- **[NOVO] Perfil no Instagram diminui custo por compra.** BCorw4x7q3s (07/08): "preciso urgente que você estruture o perfil no Instagram, porque isso vai diminuir muito o custo por compra e suba a campanha de seguidores". Mesma linha em 7n2jP39qbxU (17/09): perfil cria ponto de confiança e torna o remarketing mais eficiente. Oferta sem rosto também precisa de perfil com stories (Vtjdg86wDxA, 29/09).

## 7. Ticket médio, order bumps e CPA

- **[NOVO] 2 a 3 order bumps no máximo.** "LowTicket Plano prático para fazer 10k em 21 dias!" (05/09, RQsTWULE0KQ): "Cara, no máximo ali, no máximo três order bumps, mínimo dois". Ticket médio citado: "Ticket média dele subiu para mais de R$ 100".
- **[REFINA] Bumps a partir de R$ 9,90.** BCorw4x7q3s (07/08): "Orderbup de R$9,90 para cima, irmão, você tem que aumentar o ticket médio." Complementa a regra de R$ 21–28 do YOUTUBE-NOVIDADES (que descreve o caso mais alto, não o piso).
- **[NOVO] Ticket de front baixo estoura CPA sem bump.** BCorw4x7q3s (07/08): "com esse ticket do front é um pouco difícil. Porque estoura muito rápido o CPA aí quando a pessoa não pega OrdeBup."
- **[NOVO] Dobrar o ticket médio via bumps (oferta sazonal).** "LowTicket Sazonal Lucrando 22k em 29 dias" (29/08, SCxw6jElXio): front R$ 27 + combo de bumps R$ 37; "a gente precisa aumentar em pelo menos duas vezes o preço do produto principal através das estratégias dos nossos buffups". Com ticket médio mais alto, CPA mais alto ainda deixa a campanha ligada "porque elas nutrem o meu ecossistema".
- **[NOVO] CPA pode subir se ROI e IC continuam.** BCorw4x7q3s (07/08): "O CPA sobe, o custo por compra sobe, ele ainda tá no ROI. Ele gera IC, ele gera finalização de compra barata e ele gera volume."
- **[NOVO] Teto de CPA definido por conta.** Ticket R$ 24, CPA máximo citado R$ 14–15 (bzsllO6ereY, 22/09). Como o teto é calculado: não explicado na fonte.

## 8. Oferta sazonal / janela

- **[NOVO] Evento externo com data pública + produto pronto.** SCxw6jElXio (29/08): "Ele não compete com curso, ele compete com o calendário do comprador." Ticket R$ 27 com entrega pronta; a dor não é falta de informação.

## 9. Fora de escopo nesta janela

- Vídeos 2026-08-21 (Porsche, pessoal), 2026-09-03 (disparos WhatsApp, "100 mil por dia"): não trazem regra de Meta Ads de conversão; WhatsApp fica para a regra existente (CALLS/curso, aula 109).
- "Agente de IA + Vídeos virais" (05/10/2026, fbjnXiN1RJY): ideias de produto com base em vídeos de YouTube (filtro > 100 mil views). Sem regra de tráfego.
- Não há nesta janela vídeo tratando diretamente de "teste aberto em que o criativo direciona o público" nem de "variações por ângulo" com números: o tema aparece só no 11/08 (imagem/vídeo, ângulos diferentes) e no bloco "um criativo por dor" de abril/2026 (cJ_dFlCyM60, fora da janela). Lacuna registrada.

## 10. Métricas secundárias (ordem de leitura, reforço)

- **[REFINA] Visualização da página de destino.** RQsTWULE0KQ (05/09): "Às vezes a página tá demorando carregar, a pessoa sai da página, então ela não visualiza." Página lenta = problema antes do criativo.
- **[REFINA] CTR baixo.** BCorw4x7q3s (07/08): diagnóstico de criativo sempre batendo na dor; "o CTR eu tô achando baixo". Sem número de corte novo nesta janela (o limiar >2% do METODO-DESTILADO permanece).
- **[REFINA] Custo de IC como sinal de decisão.** Fontes: viLhlrcJPhU (21/09) e HdOidJJBPlE (11/08: 553 IC em 10 dias como prova de demanda gerada pelo ecossistema).

## 11. Divergências em aberto (não resolvidas pela fonte)

- Escala por horário sobe verba em campanha que já vende; não diz o limiar de venda para liberar o aumento. A regra da dona ("<48h só se vendeu hoje") fica como controle.
- Não há limiar numérico de "pico" nos 11 vídeos. Memória da dona (pico com 15 vendas) é regra própria, não do Kevones.
- Autor não fala de BidCap nesta janela; o gerenciamento de lance segue a decisão de 06/10 ("Só Escala Diária e Horário").
