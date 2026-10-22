# Meta Ads 2026 (Machine learning - Andromeda)

## Como configurar sua conta de anúncios (Andromeda)

**Aula:** 239

- Contexto: pós-Andrômeda o Meta lê por sinais/dados/diversificação, não por microssegmentação; "menos é mais" (menos verba, menos conjuntos, menos otimização manual). Configurar a conta não salva oferta ruim nem criativo desconexo, mas torna distribuição e ROI mais previsíveis.
- Diagnóstico: Detalhamento → Dados demográficos → Segmentos de público. Conta não configurada só mostra "público desconhecido" (Facebook não sabe pra quem distribui, não faz remarketing nem lookalike automático).
- PASSO A PASSO — Públicos engajados (Configurações de publicidade → Público engajado → Público personalizado → fonte "Site"):
  1. Selecionar o pixel do produto.
  2. Incluir evento Page View, retenção 180 dias.
  3. Incluir mais: View Content, 180 dias.
  4. Incluir mais: Initiate Checkout, 180 dias (e Add Payment Info / Add to Cart se o pixel marcar, em e-commerce).
  5. No fim, EXCLUIR quem já comprou (evento Purchase, 180 dias) — isso isola quem viu/engajou/chegou no checkout mas não comprou. Nome sugerido: "assistiu" (ou similar).
  6. Confirmar. Repetir estrutura simplificada pra "Clientes existentes" (evento Purchase, 180 dias).
- Pré-requisito: o pixel precisa já ter marcado esses eventos; sem oferta rodando ainda, aguardar 2–3 semanas antes de configurar.
- PASSO A PASSO — Listas (mais importante que eventos de pixel, segundo a aula):
  1. Na plataforma de pagamento (ex.: Kiwify), exportar CSV de vendas aprovadas do produto e CSV de carrinhos abandonados.
  2. Público engajado → Público personalizado → Lista de clientes → subir CSV de abandono.
  3. Se a planilha tiver coluna de valor do produto, marcar "sim" (ex.: Cacto tem; outras plataformas não).
  4. Rotular o público (ex.: "leads qualificados") e nomear (ex.: "leads").
  5. Revisar o mapeamento automático de colunas ("Associado"): corrigir campos errados (ex.: documento/CPF sendo lido como telefone, ou últimos dígitos do cartão como data de nascimento) marcando "não carregar"; garantir que ficou e-mail + telefone + nome.
  6. Repetir para lista de compradores, rotulando como "clientes de alto valor" e incluindo preço base do produto quando disponível (ajuda o Facebook a mirar em tickets parecidos).
- Controle de público / posicionamento: ativar restrição geográfica só se o negócio for local; restrição de idade só se o produto exigir; restrição de marca/funcionários geralmente não se aplica a infoproduto. Posicionamento específico (ex.: só Reels/Stories) só se fizer sentido pro criativo.
- Manutenção: atualizar as listas (clientes e carrinho abandonado) a cada 30 dias, adicionando os novos registros via Públicos → editar → adicionar clientes.
- Resultado real mostrado: conta configurada, filtro "hoje" — gasto R$179, retorno R$700+, 4 vendas a R$44; 3 das 4 vendas vieram do público engajado. Custo por compra: público novo R$140 vs. público engajado R$11 (no mesmo dia). Outro exemplo: R$140 gasto em novo público retornou R$297; R$33 gasto em engajado retornou R$402.
- Conclusão: configurar pixel + listas é o primeiro passo pra qualquer escala; sem isso, só se alcança público novo caro.

- Fonte: transcricoes/curso-id15/05-meta-ads-2026-andromeda/01-Como_configurar_sua_conta_de_an_ncios_Andromeda.md
