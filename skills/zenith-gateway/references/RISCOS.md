# Zenith — custo real, prazos e risco da empresa

Apurado em 08/09/2026. Tudo aqui foi lido no painel, na doc oficial, no Reclame Aqui, na Receita Federal ou informado pelo suporte da Zenith — nada veio de material de venda.

**Atenção à distinção que atravessa o documento inteiro:** método local e cartão de crédito rodam em tabelas diferentes. Cartão é pior em taxa, reserva e prazo.

## A empresa

CNPJ **53.213.723/0001-35** — C. N PAGAMENTOS ONLINE LTDA (marca Zenith).

| | |
|---|---|
| Aberta em | 15/12/2023 |
| Capital social | **R$ 10.000,00** |
| Porte | Empresa de pequeno porte |
| CNAE | Correspondentes de instituições financeiras |
| Sede | Nossa Senhora das Graças, PR (~4 mil habitantes) |
| Sócio | Cesar Augusto de Araujo |
| Situação | Ativa |

Os próprios Termos de Uso dizem: *"A Zenith não atua como instituição financeira nem como adquirente principal"* — é gateway, orquestradora e **subcredenciadora**, rodando sobre parceiros licenciados.

Empresa com R$ 10 mil de capital retendo 15% do faturamento do seller por 180 dias. O capital não cobre nada se der errado.

## Reclame Aqui

- **C.N Pagamentos Online**: sem reputação, não verificada, 0 reclamações avaliadas. Mas os "principais problemas" já marcam **47,55% em "estorno do valor pago"**
- Reclamações soltas citando Zenith Pay existem, mas são de **comprador**, não de seller
- Cuidado ao pesquisar: "Grupo Zenith" (imobiliária) e "Zenith Financeira" são **outras empresas**

## Prazos — resolvido pelo suporte em 08/09/2026

Durante o levantamento, nenhuma fonte pública publicava prazo de saque:

| Fonte | O que diz |
|---|---|
| Docs da API | *"Eventos de payout … não pertencem ao escopo"* — fora de escopo de propósito |
| Termos de Uso (v1.0, 05/08/2026) | zero menção a saque, repasse, reserva ou prazo |
| Políticas (antifraude, compliance, riscos) | nada; a de compliance diz que procedimentos internos são restritos |
| Site zenithwld.com.br | *"Ritmo de liquidação — janelas claras"*, sem número |
| Painel | 90/180 dias em `/minhas-taxas`, D+7/D+30 em `/financeiro` |

**O suporte fechou a conta:** a contradição do painel era mistura de duas tabelas. Os 90/180 dias são **cartão de crédito**; o D+30 é **método local**. Reserva de 10% retida por 90 dias, confirmada.

Continua valendo o alerta de leitura: o site anuncia "status em tempo real", que é a **tela** atualizando, não o dinheiro chegando.

## Taxas (conta Dona De lima assis Store)

### Métodos locais — confirmado pelo suporte, 08/09/2026

Vale para PIX, boleto, SPEI, OXXO, PSE, Nequi, Yape, Plin, GCash, Maya e UPI. **Mesma taxa em todos os países.**

| | |
|---|---|
| Taxa por transação | **7,99% + R$ 5,00** |
| Fundo de reserva | **10%, retido 90 dias** |
| Liquidação padrão | **D+30** |
| Tarifa de saque | R$ 10,00 por solicitação |
| Antecipação para **D+3** | **+4,5%** sobre o valor antecipado |
| Saque em USDT | **3% sobre o montante total da operação** |

Saque mínimo R$ 100 líquido · multa por reembolso R$ 0,00.

### Cartão de crédito — do painel `/minhas-taxas`

| Método | Taxa | Reserva | Fixo | Repasse |
|---|---|---|---|---|
| Cartão | 8,99% | 15% | R$ 5,00 | 180 dias |
| Voucher/Boleto | 8,99% | 15% | R$ 5,00 | 180 dias |
| Internacional | 8,99% + câmbio 2% | 15% | R$ 5,00 | 180 dias |

Antecipação de cartão 2,50%.

Cartão é pior em tudo: taxa maior, reserva 50% maior, prazo 6× mais longo. Se o método local existe no país-alvo, use o local.

A reserva **não é taxa** — é dinheiro do seller, congelado como garantia de chargeback, e volta em 90 dias.

## Quanto sobra, por ticket (método local)

Câmbio usado: **USD 1 = R$ 5,0889** (08/09/2026). Recalcule se a data mudou.

| Venda | Custo | % da venda | Reserva (90d) | Líquido D+30 | Com reserva | D+3 (+4,5%) |
|---|---|---|---|---|---|---|
| R$ 17,90 | R$ 6,43 | **35,9%** | R$ 1,79 | R$ 9,68 (54,1%) | R$ 11,47 (64,1%) | R$ 9,24 (51,6%) |
| R$ 27,90 | R$ 7,23 | 25,9% | R$ 2,79 | R$ 17,88 (64,1%) | R$ 20,67 (74,1%) | R$ 17,08 (61,2%) |
| US$ 10 (R$ 50,89) | R$ 9,07 | 17,8% | R$ 5,09 | R$ 36,73 (72,2%) | R$ 41,82 (82,2%) | R$ 35,08 (68,9%) |
| US$ 14 (R$ 71,24) | R$ 10,69 | 15,0% | R$ 7,12 | R$ 53,43 (75,0%) | R$ 60,55 (85,0%) | R$ 51,02 (71,6%) |

Ainda faltam, em cima disso: **R$ 10,00 por saque** e, se sacar em USDT, **3% sobre o montante**.

### Como o fixo de R$ 5,00 dilui

| Ticket | Custo % |
|---|---|
| US$ 10 | 17,8% |
| US$ 15 | 14,5% |
| US$ 20 | 12,9% |
| US$ 30 | 11,3% |
| US$ 50 | 10,0% |

O fixo é o assassino do low ticket. Em R$ 17,90 ele sozinho come 28% da venda. Sem renegociar para ≤ R$ 1,00, ticket baixo não fecha — a operação só respira acima de ~US$ 30.

### O que a nova tabela mudou

Comparado ao que o painel mostrava para cartão, método local ficou **melhor**: US$ 10 sai de 64,2% líquido em 180 dias para **72,2% em 30 dias**. Continua caro, mas o prazo deixou de ser inviável e virou apenas ruim.

## Comparação com as alternativas

| | Zenith (método local) | Stripe (conta BR) | Cartpanda Pay Global |
|---|---|---|---|
| US$ 10 líquido | R$ 36,73 | **R$ 46,43** | R$ 39,26 |
| US$ 14 líquido | R$ 53,43 | **R$ 65,16** | R$ 55,57 |
| Custo efetivo | 15,0–17,8% | **8,5–8,8%** | 12,0–12,8% |
| Reserva | 10% por 90d | **nenhuma** | 10% por 90d |
| Repasse | D+30, ou D+3 por +4,5% | 5d (cartão intl) | 14d padrão, **2d** sob aprovação |
| Métodos locais fora do BR | **sim, 7 países** | não | não |
| Bandeiras | conforme rota | Visa, Master | Visa, Master, Amex, JCB, UnionPay, Discover, Diners, CB |
| Moedas | por país | 135+ | 130+ |

### Stripe com CNPJ brasileiro — o que trava

- Só habilita **boleto** e **Pix** (este por convite), e só para comprador **brasileiro**. OXXO, UPI, Konbini, iDEAL exigem sede em outro país
- Aceita só **Visa e Mastercard**
- O cartão do comprador precisa estar habilitado para **compra internacional** — cartão só-nacional é recusado. É a maior fonte de queda de aprovação em público de baixa renda
- Repasse: cartão internacional **5 dias**, cartão nacional 30 dias, Pix/boleto 2 dias
- Liquidação em BRL (Brasil é país de controle cambial)
- **Adaptive Pricing** (preço na moeda local automático, cliente paga 2–4% do câmbio) só funciona no Stripe Checkout e Payment Links — **não funciona com Elements/Payment Intents**, ou seja, não funciona em checkout próprio. E exige preço-base numa settlement currency, que para conta BR é BRL

### Cartpanda Pay Global — quando o D+2 é inegociável

- 130+ moedas, comprador vê na moeda dele, seller recebe em BRL
- 8 bandeiras, incluindo Amex, JCB e UnionPay — público que a Stripe BR não atende
- Taxa internacional 9,9% + R$ 1,50 (Light) até 8,5% + R$ 1,50 (Advanced)
- Reserva **10% presa por 90 dias**, independente do prazo escolhido
- Padrão **D+14**; D+2 só mediante aprovação (30+ dias de operação, rastreio em dia, chargeback baixo) — **não dá para começar no D+2**
- Bloqueia Argentina, Rússia, Cuba, Irã, Coreia do Norte, Síria; Alemanha sob análise
- Saque em conta BR ou Payoneer
- Os 3 dias a menos custam ~R$ 7,17 por venda de US$ 10 frente à Stripe

## O que ainda falta exigir por escrito

Respondido pelo suporte em 08/09/2026:
- ~~Prazo de liberação da reserva~~ → **90 dias**
- ~~90/180 dias ou D+7/D+30?~~ → **D+30 para método local**; 90/180 era cartão
- ~~Existe antecipação?~~ → **D+3 por +4,5%**

Ainda em aberto:
1. **Fixo por transação renegociado** — R$ 5,00 inviabiliza qualquer ticket abaixo de US$ 30. É a única negociação que muda o jogo
2. SLA do saque em si: de "Solicitado" a "Pago", quantas horas ou dias após o D+30
3. Liberação das **Integrações Zenith** na conta — sem isso não sai API key
4. Se a reserva de 10% também vale para cartão ou se lá continuam os 15%

Nada disso está em documento público — foi dito em atendimento. Peça por escrito antes de operar volume.

## Estado da conta levantada

- KYC **aprovado**, contrato assinado em 07/09/2026
- `/integracoes-zenith`: **"Nenhum produto de integração foi liberado para esta conta"** — sem isso não sai `zp_pub_`/`zp_sec_`, e nem Payments API nem Elements funcionam. Precisa pedir liberação
- Menu tem link **Super Admin** visível
- Zero vendas, saldos zerados — nada dá para medir na prática ainda

## Veredito

O gargalo de uma operação low ticket não é a taxa, é a **aprovação**. 8,8% num checkout que aprova 40% perde para 20% num que aprova 80%.

A Zenith só se justifica quando o público-alvo paga em método local fora do Brasil e não tem cartão internacional. Fora desse caso, Stripe ganha por larga margem. E mesmo no caso favorável, compare antes com um gateway local do país-alvo — a combinação de capital de R$ 10 mil, 15% retido e prazo não publicado é risco de crédito, não custo de operação.
