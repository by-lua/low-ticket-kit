# Teste, otimização e Validação (Meta 2026)

## Estrutura de Campanhas (Atualizado)

**Aula:** 237

- Meta 2026: qual melhor estrutura campanhas? CBO ou ABO? Quantos públicos/criativos?
- CONFIGURAÇÃO 1 (MENOS VERBA, MAIS TESTES):
  - 1 campanha, 3 públicos DIFERENTES, 3 criativos repetidos
  - Pública 1: aberto (recomendação Facebook 100%)
  - Público 2: segmentado por interesses/comportamento
  - Público 3: segmentado idade/gênero/localização
  - Criativos: C1 em P1, P2, P3 / C2 em P1, P2, P3 / C3 em P1, P2, P3
  - NÃO cria 9 criativos = usa 3 repetidos nos 3 públicos
  - Orçamento: nível campanha (distribui entre públicos)
  - Verba: R$45-70 (objetivo = coletar dados, não ganhar dinheiro)
  - Vantagem: testa múltiplas públicos + criativos gastando menos
  - Desvantagem: mais tempo para validar, verba pulverizada
- CONFIGURAÇÃO 2 (MAIS VERBA, MENOS TESTES):
  - 1 campanha, 1 público, 1 criativo
  - Injeta 100% verba em um combo P+C
  - Não há competição verba entre públicos/criativos
  - Mais caro (precisa múltiplas campanhas para testar)
  - Vantagem: testa rápido, dados concentrados
  - Desvantagem: gasta mais dinheiro com menos testes
- CONFIGURAÇÃO HÍBRIDA (RECOMENDADO):
  - 1 campanha, 2 públicos, 3 criativos variados
  - Testa públicos + criativos ao mesmo tempo
  - Menos pulverização que config 1, menos caro que config 2
  - Orçamento: nível campanha
- VERBA IDEAL:
  - Low ticket (R$29-47): mínimo R$30/dia
  - Ticket maior (R$97+): pode começar R$45-70
  - Abaixo R$30: muito lento testar, gasta mais no longo prazo
  - Acima R$200: pode começar R$100+ (se já validado)
- O QUE KEVIN USA:
  - Config 1 primeiro (testar públicos/criativos desconhecidos)
  - Encontra P3 validado? Para testar criativos, muda para config 2
  - Nessa agora: P3 + variações criativos em campanhas isoladas
  - Resultado: escala rápido após descobrir público validado
- CASE REAL (SAS financeiro):
  - Mês 1: Config 1 (teste) = R$1.557 investido → R$3.873 retorno = R$2.316 lucro
  - Campanhas vencedoras isoladas = 3, 9, 18 vendas (mantêm CPA)
  - Mês 2: Config 2 (escala) = R$700 → R$3.995 = R$3.295 lucro
  - Prova: após validar, escala mais rápido
- ESTRUTURA NÃO PRECISA SER ROBUSTA:
  - Muita gente complica
  - Simples funciona: 1 campanha, públicos diferentes, máximo 3 criativos
  - Conforme vai testando = vai aprendendo = vai escalando

- Fonte: transcricoes/curso-id15/07-teste-otimizacao-validacao/01-Estrutura_de_Campanhas_Atualizado.md

## Métricas e Otimização na Prática

**Aula:** 238

- Muita gente perde dinheiro aqui porque confunde métricas (mata boa campanha, mantém ruim)
- MÉTRICAS PRINCIPAIS:
  1. CTR (todos) > 2% = anúncio gerando cliques
  2. Visualização página destino: R$2-3 ideal (até R$5 se ticket alto)
  3. Finalização compra < 10% ticket (R$47 produto = máx R$4.70 finalização)
  4. CPA (custo por aquisição/venda) < 60% ticket (R$47 produto = máx R$28)
  5. ROAS > 2.0 (ganhar dobro do investimento)
- ORDEM ANÁLISE (FUNIL):
  1. CTR baixo (< 2%)? Criativo ruim (não chama atenção)
  2. CTR bom, visualização cara (> R$5 em low ticket)? Criativo não convence ir pra página
  3. Visualização ok, finalização cara (> 10% ticket)? Página/copy/oferta ruim
  4. Finalização ok, zero vendas? Página não converte
  5. Vendas caras (> 60% ticket)? Público errado ou campanha saturada
- MODO MONGE (DECISÃO CRÍTICA):
  - NÃO olha hoje, olha período máximo rodado
  - Campanha boa que parou vendendo? Filtra máximo período
  - Se mantém CPA filtrando máximo = mantém ativa (dia ruim é normal)
  - Se estourou CPA no máximo? Mata (realmente ruim)
- EXEMPLO REAL KEVIN (campanha 1º ao dia 31):
  - Dia 1: 2 vendas R$16 CPA, faturou R$108 (ROI 3x)
  - Dia 2: 1 venda, ROI 1.7 (pior, topo funil em pânico mataria)
  - Dia 3: 1 venda, CPA subiu (pânico aumenta)
  - Dia 4: zero venda, gastou R$38 (desespero máximo)
  - Dia 5: 1 venda R$32
  - Dias 3-7: filtrando MÁXIMO = CPA R$57 (estourado)
  - Dia 8: 5 vendas, ROI 7x = R$400 lucro EM UM DIA
  - DO DIA 3 AO 7: R$53 prejuízo (bem visto)
  - MAS: filtrando máximo (dia 1 ao dia 7) = mantém CPA < 60 ticket = mantém
  - Se tivesse matado dia 3? Teria perdido R$3.580 de lucro mês inteiro
- CAMPANHA BOAS TEM OSCILAÇÃO:
  - Há dias que ganha, há dias que perde
  - Período máximo que diz se campanha é boa
  - Modo monge = paciência = lucro
- EXEMPLO 2 CAMPANHA PÉSSIMA:
  - CTR 1.4% (baixo) = não funciona
  - Se baixo sempre = mata logo
  - Mas se variava? Filtrar máximo antes de matar
- SETUP MÉTRICAS NO GERENCIADOR:
  - Personalizar colunas > Adicionar: CTR, Visualização página, Finalização, CPA, ROAS
  - Criar métrica personalizada: valor conversão - valor gasto = lucro real
  - Salvar e pronto, usa sempre esse template
- TAKEAWAY:
  - Nunca mata por dia ruim (modo monge = filtra máximo)
  - Mata por período máximo estourado (aí realmente ruim)
  - Múltiplas campanhas distribuem risco (uma ruim, outras boas = lucro geral)
  - Respeita CPA < 60% ticket = operação saudável

- Fonte: transcricoes/curso-id15/07-teste-otimizacao-validacao/02-Metr_cas_e_Otimiza_o_na_Pr_tica.md

