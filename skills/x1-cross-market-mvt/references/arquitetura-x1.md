# X1 LATAM — concepção de oferta e arquitetura

**Países:** Argentina, México e Colômbia  
**Idioma da experiência:** espanhol neutro (`es-419`), com moeda, meios de pagamento e exemplos adaptados por país  
**Status:** concepção; este documento não autoriza nem descreve uma implementação concluída  
**Separação:** é uma operação nova. Não deve compartilhar funil, tabelas, inbox, automações, pixels ou estados com o low-ticket brasileiro.

## Recomendação executiva

O modelo mais coerente é **entregar primeiro um microproduto digital realmente útil e, só depois, pedir uma contribuição voluntária com valor mínimo**. A comunicação não deve fingir que o produto grátis é uma amostra: o item prometido já foi entregue. A contribuição sustenta o projeto, e uma faixa de contribuição claramente indicada destrava um complemento premium.

Para o primeiro MVP, a melhor combinação é:

1. começar com **Kit Express para vender por WhatsApp**, por ter custo marginal quase zero, valor facilmente demonstrável e público comercial com maior capacidade de contribuir;
2. reaproveitar o **WebWidget do Chatwoot já existente**, ligado a um fluxo determinístico no n8n/backend;
3. abrir o pagamento em uma **página/modal próprio com Zenith Elements**, fora do balão do Chatwoot;
4. usar três botões de contribuição: **mínima**, **com bônus** e **outro valor**;
5. liberar o bônus somente depois de webhook assinado e persistido.

Os pisos iniciais recomendados são **ARS 6.000**, **MXN 79** e **COP 15.000**. Eles ainda têm custo efetivo alto, mas evitam a zona em que os R$ 5 fixos praticamente consomem a contribuição. O valor preselecionado deve ser o patamar de bônus, não o mínimo: **ARS 12.000**, **MXN 149** e **COP 30.000**.

## Premissas confirmadas e ressalva de disponibilidade

- Taxa de método local da Zenith: **7,99% + R$ 5 por transação**.
- Há ainda **reserva de 10% por 90 dias**, liquidação padrão **D+30** e R$ 10 por solicitação de saque. A reserva não é taxa, mas afeta caixa.
- O navegador nunca recebe a secret da Zenith. Criação de checkout/sessão é sempre backend-to-backend.
- O valor enviado à Zenith é inteiro na menor unidade monetária. Exemplo: MXN 79,00 vira `7900`.
- A confirmação vem exclusivamente do webhook assinado. Redirect, retorno do checkout e polling não liberam bônus.
- A documentação da Zenith descreve um catálogo maior do que o routing efetivo de cada seller. A interface deve consultar `GET /integrations/payment-methods` e mostrar somente os itens devolvidos em runtime.

Na conta levantada em 08/09/2026, o routing de produção observado era:

| País | Disponível na conta | Não prometer sem reaparecer no runtime |
|---|---|---|
| Argentina | `bank-transfer` — CVU, aceitando origem CBU/CVU | QR interoperável, Mercado Pago e DEBIN constam no catálogo, mas não estavam liberados para esta conta |
| México | OXXO, SPEI e CoDi | PayCash, PayNet e cartão |
| Colômbia | PSE, Nequi e Bre-B/Llave | Cartão |

Portanto, a promessa comercial deve dizer “pague com os meios disponíveis no seu país”, e não listar Mercado Pago/QR/cartão de forma fixa. Em especial, **Argentina não deve ser lançada anunciando Mercado Pago enquanto a própria consulta da conta não o devolver**.

## 1. Concepções concretas de produto/oferta

### 1. Kit Express para vender por WhatsApp — prioridade 1

**Promessa em espanhol:** “Responde mejor, vende sin perseguir y recupera conversaciones que hoy se enfrían.”

O chat faz quatro perguntas: tipo de negócio, produto principal, perfil do cliente e objeção mais frequente. Em seguida, entrega um kit curto e personalizado:

- 10 respostas prontas para dúvidas e objeções;
- 3 mensagens de acompanhamento sem parecer insistente;
- 5 ideias de status/publicações;
- checklist de atendimento em uma página.

**Contribuição com bônus:** quem atinge o patamar de bônus recebe um calendário de 30 dias, mais variações de copy e modelos editáveis.

**Por que combina com o modelo:** o ganho é imediatamente visível, o público de microempreendedores já usa WhatsApp diariamente e entende o produto como uma ajuda prática. Há uma razão natural para “apoiar para que mais kits continuem gratuitos”.

**Adaptação local:** os exemplos usam vocabulário e cenários de cada mercado, sem caricatura: entregas e CVU na Argentina; OXXO/SPEI no México; PSE/Nequi na Colômbia. O corpo da linguagem permanece `es-419`.

### 2. CV que cuenta tu valor — prioridade 2

**Promessa em espanhol:** “Convierte tu experiencia en un CV claro y una presentación que sí te represente.”

O chat pergunta objetivo profissional, experiência, competências e vaga desejada. Entrega:

- roteiro para reescrever o resumo profissional;
- modelo de CV simples e compatível com leitura automatizada;
- checklist de erros;
- mensagem curta para enviar a recrutadores.

**Contribuição com bônus:** banco de respostas para entrevista, modelo de carta de apresentação e uma segunda versão do resumo profissional.

**Por que combina:** emprego é uma dor urgente, mas o item gratuito continua útil mesmo para quem não paga. O usuário tende a contribuir por reciprocidade quando reconhece a própria história no resultado.

**Limite de promessa:** não afirmar aprovação em vaga nem “burlar ATS”; vender clareza, organização e preparação.

### 3. Plan de 7 días para ordenar tu dinero — prioridade 3

**Promessa em espanhol:** “Un plan simple para saber qué entra, qué sale y qué puedes ajustar esta semana.”

O chat coleta apenas faixas de renda, principais despesas e objetivo. Entrega:

- plano de sete dias;
- planilha/calculadora simples;
- mapa de despesas fixas, variáveis e esquecidas;
- três ações adequadas à realidade informada.

**Contribuição com bônus:** planner mensal, calendário de contas e roteiro para renegociar despesas.

**Por que combina:** resolve uma tarefa concreta e gera alívio imediato. É reutilizável nos três países sem depender de conteúdo regulatório complexo.

**Limite de promessa:** educação e organização financeira, nunca recomendação de investimento, crédito ou garantia de economia.

### 4. Menú Ahorro de 7 días

**Promessa em espanhol:** “Una semana de comidas posibles con tu presupuesto, tu tiempo y lo que ya tienes en casa.”

O chat pergunta número de pessoas, faixa de orçamento, restrições e tempo disponível. Entrega cardápio de sete dias e lista de compras agrupada.

**Contribuição com bônus:** plano de 30 dias, lista editável e tabela de substituições econômicas.

**Por que combina:** utilidade diária, resultado tangível e alto potencial de compartilhamento orgânico. Pode gerar versões locais com alimentos e medidas comuns de cada país.

**Limite de promessa:** coletar alergias/restrições e exibir aviso de que não substitui orientação médica ou nutricional.

### 5. Lectura simbólica breve

**Promessa em espanhol:** “Una pausa para mirar tu pregunta desde otro ángulo.”

O chat coleta uma pergunta, escolhe uma tiragem curta e entrega uma leitura simbólica em texto ou áudio. A experiência gratuita é completa, não um teaser interrompido.

**Contribuição com bônus:** áudio mais aprofundado, exercício de reflexão e uma leitura complementar delimitada.

**Por que combina:** alto valor emocional, custo marginal baixo e reciprocidade forte após uma entrega personalizada. É particularmente adequado a conteúdo de creator economy.

**Limite de promessa:** posicionar como entretenimento/reflexão; nunca prometer resultado, diagnóstico, cura ou certeza sobre terceiros. Este produto deve ter identidade e operação LATAM próprias, sem reutilizar o funil brasileiro.

## 2. Experiência da oferta

### Regra de ouro

O produto-base vem antes da contribuição. O bônus é a única parte condicionada ao pagamento. A copy precisa deixar isso inequívoco:

> “Esto ya es tuyo, gratis. Si te ayudó, puedes aportar desde **{piso local}** para mantener este proyecto activo. Con un aporte de **{patamar de bônus}** o más, también recibes **{bônus}**.”

Opções exibidas:

- `Aporte mínimo — {piso}`;
- `Aporte con regalo — {patamar de bônus}` — preselecionado;
- `Otro monto` — validado no servidor, nunca menor que o piso.

Mensagem após confirmação:

> “¡Gracias! Tu aporte fue confirmado. Aquí tienes el contenido adicional que desbloqueaste: {enlace}.”

O uso de “aporte” é melhor que “donación” até validação jurídica/contábil. A página deve dizer que o produto-base já foi entregue e explicar objetivamente o que o valor adicional libera.

### Jornada ponta a ponta

```text
Anúncio/conteúdo orgânico
        ↓
Landing LATAM detecta/solicita país
        ↓
Chat cria sessão e faz 3–5 perguntas
        ↓
Backend gera o produto-base
        ↓
Chat entrega link/arquivo e registra delivered_at
        ↓
Chat pede contribuição e mostra 3 escolhas de valor
        ↓
Backend valida moeda + piso + teto e cria intenção imutável
        ↓
Página de pagamento cria sessão Zenith Elements
        ↓
Usuário paga pelo método local disponível em runtime
        ↓
Webhook Zenith assinado e idempotente
        ↓
paid_basic → agradecimento
paid_bonus → agradecimento + link seguro do bônus
```

O chat pode lembrar uma intenção pendente, mas não pode afirmar “pagamento aprovado” antes do webhook. OXXO e alguns fluxos bancários são assíncronos; a conversa precisa sobreviver a retorno horas ou dias depois.

## 3. Arquitetura proposta

### Componentes

| Componente | Responsabilidade |
|---|---|
| Landing LATAM | Escolher país, abrir o chat e apresentar a promessa. Rotas separadas `/ar`, `/mx`, `/co` ou subdomínios equivalentes. |
| Chatwoot WebWidget | Interface conversacional, histórico, reentrada e eventual handoff humano. |
| Orquestrador n8n/backend | Máquina de estados, perguntas, geração/seleção do produto, mensagens e integração com Chatwoot. |
| API X1 LATAM | Sessões, validação de valores, intenção de contribuição, criação de sessão Zenith, webhook e direitos de acesso. |
| Banco | Fonte de verdade para sessão, intenção, evento recebido e entitlement. Chatwoot não deve ser a única fonte de estado financeiro. |
| Zenith Elements | Coleta os campos específicos e apresenta somente os métodos liberados para país/moeda/seller. |
| Storage/CDN | Produto-base e bônus com URLs assinadas, expiráveis e regeneráveis. |
| Fila | Envia mensagem pós-pagamento e gera bônus sem atrasar o `2xx` do webhook. |

### Por que Elements no MVP

O chat não é um bom lugar para renderizar RFC, QR, voucher, CLABE, CVU, redirect e aprovação em app. O backend deve criar uma sessão do Zenith Elements já vinculada a `referenceId`, país, moeda e valor. O chat abre a página/modal de pagamento, e o Elements coleta os campos exigidos pela rota.

Vantagens:

- os campos específicos de SPEI e demais métodos ficam a cargo da Zenith;
- a secret permanece no backend;
- métodos disponíveis são filtrados pela conta;
- o valor continua totalmente dinâmico;
- o chat continua simples e não precisa imitar um checkout.

Requisitos a guardar para a implementação futura: a sessão inicial do Elements dura 15 minutos; `origin` deve ser HTTPS e corresponder exatamente a uma origem autorizada; `referenceId` não pode ser reciclado com outro valor, país, moeda, ambiente ou origem.

Se o Elements não estiver liberado na conta, o plano B é Payments API pura: consultar métodos, criar checkout e renderizar `nextAction` conforme `redirect`, `qr_code`, `voucher`, `bank_transfer` ou `app_approval`. Não deve haver lista de meios hardcoded em nenhuma das duas opções.

### Criação da contribuição

1. O navegador envia apenas `session_id`, escolha de valor e país já vinculado à sessão.
2. O servidor ignora qualquer moeda/piso vindo do navegador e carrega a configuração vigente do país.
3. O servidor normaliza o valor digitado, verifica piso, teto e limites retornados pela Zenith.
4. Cria `contribution_intent` com valor, piso e patamar de bônus congelados naquele momento.
5. Gera `reference_id` e chave idempotente únicos para aquela intenção.
6. Cria a sessão Elements ou checkout via backend.
7. Devolve ao navegador apenas token/sessão efêmera e dados públicos de apresentação.

Um retry técnico reutiliza a mesma intenção e o mesmo payload. Uma nova escolha de valor cria nova intenção e invalida/cancela a anterior quando for seguro fazê-lo.

### Estado mínimo de domínio

```text
chat_state:
  started
  product_generating
  product_delivered
  contribution_offered
  payment_pending
  paid_basic
  paid_bonus

payment_status:
  created | pending | succeeded | failed | canceled | refunded | chargeback

entitlement:
  base_access = true depois da entrega, independentemente de pagamento
  contribution_tier = none | basic | bonus
  bonus_access = true somente após evento definitivo válido
```

Não é recomendável definir “acima do piso” como literalmente um centavo acima. Isso permite destravar o bônus por uma diferença irrelevante e confunde a oferta. Devem existir dois valores:

- `minimum_amount`: menor contribuição aceita;
- `bonus_threshold`: valor público a partir do qual o bônus é liberado, inicialmente cerca de 2× o mínimo.

Assim, `paid_basic` significa `minimum_amount ≤ paid_amount < bonus_threshold`, e `paid_bonus` significa `paid_amount ≥ bonus_threshold`. A copy deve dizer “a partir de X libera o bônus”, sem ambiguidade.

### Schema conceitual simples

| Entidade | Campos essenciais |
|---|---|
| `x1_session` | `id`, `country`, `currency`, `locale`, `product_id`, `chatwoot_account_id`, `inbox_id`, `conversation_id`, `contact_id`, `state`, `delivered_at`, `created_at` |
| `contribution_intent` | `id`, `session_id`, `reference_id` único, `zenith_checkout_id`, `idempotency_key` único, `amount_minor`, `minimum_minor_snapshot`, `bonus_threshold_minor_snapshot`, `pricing_version`, `payment_method`, `status`, `expires_at`, timestamps |
| `webhook_event` | `zenith_event_id` único, `event_type`, `checkout_id`, `received_at`, `payload_hash`, `processed_at` |
| `entitlement` | `session_id`, `product_id`, `base_access_at`, `tier`, `source_intent_id`, `bonus_access_at`, `revoked_at` |
| `country_pricing` | `country`, `currency`, `minimum_minor`, `bonus_threshold_minor`, `suggested_minor`, `version`, `active_from` |

Os snapshots na intenção impedem que uma mudança futura de preço altere retroativamente a classificação de uma contribuição já criada.

### Webhook e liberação do bônus

1. Receber o **corpo bruto**.
2. Exigir `X-Zenith-Timestamp`, `X-Zenith-Signature`, `X-Zenith-Event-Id` e tipo do evento.
3. Rejeitar timestamp com diferença superior a 300 segundos.
4. Calcular HMAC SHA-256 sobre `timestamp + "." + rawBody` e comparar em tempo constante.
5. Inserir `X-Zenith-Event-Id` em tabela com restrição única.
6. Dentro de transação, localizar a intenção e aplicar a transição de estado.
7. Responder `2xx` somente depois de o evento estar persistido.
8. Disparar geração/envio do bônus em fila, com chave idempotente própria.

Tratamento dos eventos:

| Evento | Ação |
|---|---|
| `payment.captured` / `checkout.succeeded` | Marcar `succeeded`; calcular tier pelo snapshot; criar/atualizar entitlement uma única vez. Como os dois podem chegar para a mesma intenção, o efeito precisa ser idempotente. |
| `payment.failed` | Marcar falha; manter produto-base; oferecer nova tentativa sem reutilizar referência incompatível. |
| `payment.refunded` | Marcar reembolso; manter o produto-base gratuito; revogar somente o bônus quando a política da oferta exigir. |
| `payment.chargeback` | Marcar chargeback, revogar bônus e sinalizar risco; não repetir efeitos em reentregas. |

Eventos fora de ordem devem obedecer precedência de estado: reembolso/chargeback não podem ser revertidos por um `checkout.succeeded` atrasado. A página de retorno pode consultar o estado para mostrar “aguardando confirmação”, mas não concede acesso.

## 4. Chatwoot existente ou chatbot próprio?

### O que foi confirmado na máquina

- Existe Chatwoot ativo em **`https://atendimento.empresa-b.com.br`**; o domínio antigo `chatwoot.empresa-b.com.br` está morto.
- A conta EmpresaB já está integrada ao n8n e há automações de atendimento em produção.
- Outro projeto da máquina, Aura Mystica, já usou **Channel::WebWidget** em site, ligado a bot e workflow. Portanto, reaproveitamento não é hipótese: o padrão já foi usado.
- Os projetos registram estados, etiquetas e atributos no Chatwoot a partir de fatos do workflow, padrão útil para `produto-entregue`, `pagamento-pendente`, `pagou-basico` e `pagou-bonus`.

### Recomendação: reutilizar no MVP, com isolamento

Criar uma conta Chatwoot dedicada `X1 LATAM` ou, no mínimo, três inboxes WebWidget separados (`X1 AR`, `X1 MX`, `X1 CO`). Não usar as inboxes comerciais atuais da EmpresaB. Cada sessão do site grava `conversation_id` no banco, permitindo que o webhook mande a mensagem de bônus à conversa correta via API.

Configuração recomendada:

- `locale: "es"`/espanhol suportado pelo Chatwoot, validado na versão instalada;
- `pre_chat_form_enabled: false` para não adicionar fricção antes da entrega;
- `enable_email_collect: false` no widget; nome completo/e-mail reais são coletados no momento do pagamento pelo Elements;
- país fixado pela rota da landing, não perguntado repetidamente;
- agente/bot 24/7 e mensagem de disponibilidade revisada;
- etiquetas e atributos como espelho operacional, nunca como fonte financeira de verdade.

Armadilhas já observadas em outro projeto:

- locale inválido no snippet do site faz o widget cair para inglês;
- o Agent Bot não conta como agente humano “online”, então o widget pode dizer “Estamos ausentes” mesmo respondendo automaticamente;
- pré-chat e coleta automática de e-mail podem criar um bloqueio desnecessário;
- editar/importar workflow n8n pode desativá-lo e exigir reativação/restart para registrar o trigger;
- o host antigo do Chatwoot em credenciais ou nós hardcoded deixa o fluxo mudo.

### Limite do reaproveitamento

O Chatwoot deve ser a **casca conversacional**, não o checkout nem a máquina de estados financeira. Se tentarmos colocar seletor de valor, validação monetária e todos os `nextAction` dentro do balão, o MVP ficará frágil. O botão do chat deve abrir `/aportar/{token}` em modal ou nova página, mantendo o vínculo com a conversa.

Um chatbot próprio passa a compensar apenas se testes mostrarem que:

- abrir a página de pagamento derruba muito a conversão;
- é indispensável mostrar os botões de valor dentro da própria conversa;
- o visual do WebWidget prejudica confiança ou marca;
- o volume torna o histórico/automação do Chatwoot um custo ou gargalo.

Mesmo nesse cenário, o backend, schema, Zenith e webhook permanecem iguais; troca-se apenas a interface. Isso preserva a opção de migrar sem reescrever a camada financeira.

## 5. Piso mínimo por país

### Método de cálculo

Usando a PTAX de fechamento do Banco Central do Brasil de **08/09/2026** como referência de planejamento:

| Moeda | Cotação aproximada em BRL | R$ 5 equivalem a | Break-even matemático¹ |
|---|---:|---:|---:|
| ARS | R$ 0,003370 por ARS | ARS 1.484 | ARS 1.612 |
| MXN | R$ 0,3005 por MXN | MXN 16,64 | MXN 18,08 |
| COP | R$ 0,001628 por COP | COP 3.071 | COP 3.338 |

¹ Valor bruto que apenas cobre `7,99% + R$ 5`: `piso = R$ 5 / (1 - 0,0799)`, convertido para moeda local. Esse ponto não gera contribuição útil e não deve ser o piso comercial.

Fonte cambial: [Banco Central do Brasil — cotações de todas as moedas em 08/09/2026](https://ptax.bcb.gov.br/ptax_internet/consultarTodasAsMoedas.do?method=consultaTodasMoedas).

### Valores recomendados para lançamento

| País | Piso mínimo | Patamar do bônus | Equivalente BRL aproximado do piso | Taxa Zenith no piso | Disponível D+30 após taxa + reserva² |
|---|---:|---:|---:|---:|---:|
| Argentina | **ARS 6.000** | **ARS 12.000** | R$ 20,22 | R$ 6,62 | R$ 11,58 |
| México | **MXN 79** | **MXN 149** | R$ 23,74 | R$ 6,90 | R$ 14,47 |
| Colômbia | **COP 15.000** | **COP 30.000** | R$ 24,42 | R$ 6,95 | R$ 15,03 |

² Antes da tarifa agregada de saque e sem antecipação. A reserva de 10% volta após 90 dias; não é perda definitiva.

Esses valores são um **compromisso de conversão**, não uma economia ideal. No piso, o custo efetivo continua pesado. Se a oferta depender de tráfego pago, o piso não sustenta CAC; a operação precisará de contribuição média próxima ou acima do patamar de bônus, tráfego orgânico/remarketing barato ou outra monetização posterior.

### Regra operacional de atualização

- Guardar pisos em moeda local, com versão e data de vigência.
- Monitorar semanalmente o equivalente em BRL, mas não mudar o preço todos os dias.
- Revisar quando o piso sair da faixa de aproximadamente **R$ 20–25 brutos** ou o câmbio variar mais de 10% desde a versão vigente.
- Congelar `minimum` e `bonus_threshold` dentro de cada intenção.
- Conferir também o câmbio efetivamente aplicado pela Zenith no repasse; PTAX é referência de planejamento, não garantia de liquidação.

## 6. Regras de negócio e métricas do piloto

### Regras que não devem ficar na mão de IA

- país, moeda, piso e threshold;
- criação de intenção e idempotência;
- método de pagamento liberado;
- interpretação do webhook;
- tier e liberação/revogação de bônus;
- número máximo de lembretes.

Um LLM pode personalizar perguntas e redigir o produto, mas o workflow determinístico decide estado e pagamento.

### Métricas mínimas

- início do chat → produto entregue;
- produto entregue → oferta de contribuição vista;
- oferta vista → checkout criado;
- checkout criado → pagamento confirmado, por método e país;
- contribuição média e mediana;
- proporção `paid_basic` versus `paid_bonus`;
- tempo até confirmação, especialmente OXXO;
- margem líquida após taxa, reserva, saque e custo de geração;
- reembolso/chargeback;
- taxa de retorno para buscar o bônus.

Não medir apenas conversão em pagamento: o indicador central é **contribuição líquida por produto entregue**.

## 7. Decisões antes da implementação

1. Escolher um único produto para o piloto; recomendação: **Kit Express para vender por WhatsApp**.
2. Definir o bônus exato e deixá-lo pronto antes de levar tráfego.
3. Confirmar em runtime o routing de produção dos três países, especialmente Argentina.
4. Confirmar que Payments API e Elements estão liberados na conta e que as origens HTTPS estão autorizadas.
5. Criar isolamento Chatwoot/n8n/banco para X1 LATAM.
6. Validar a expressão jurídica/contábil “aporte” versus venda de conteúdo bônus.
7. Fazer microtestes com dinheiro real, pois a documentação local registra que sandbox não vem habilitado por padrão.
8. Só depois escolher piso definitivo por país com base em checkout-to-paid e contribuição média, não apenas em câmbio.

## Veredito

O formato é viável quando tratado como **produto grátis + apoio voluntário + bônus por faixa**, não como “qualquer valor”. O piso precisa existir e o valor de bônus deve ser explícito. A infraestrutura já existente favorece Chatwoot no MVP, mas o pagamento deve morar numa superfície própria com Zenith Elements e backend idempotente. O principal risco técnico não é o chat: é prometer meios que o seller não tem, liberar bônus por retorno do navegador e deixar o custo fixo de R$ 5 corroer contribuições pequenas.
