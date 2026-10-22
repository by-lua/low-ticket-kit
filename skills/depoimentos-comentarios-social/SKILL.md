---
name: depoimentos-comentarios-social
description: Gera prova social como mockup de comentário/DM do Instagram ou Facebook — comentários empilhados em bolha de chat, estilo feed. Use como alternativa/complemento ao carrossel de depoimento em WhatsApp da página de vendas, quando o usuário pedir "depoimento tipo comentário de Instagram/Facebook", "DM de comprador", ou mencionar prova social em formato de rede social.
---

# Depoimentos como comentário/DM de rede social

Gera prova social em imagem única (mockup), não HTML: comentários de
compradores empilhados como um feed de Instagram ou Facebook — avatar
redondo, nome, texto do comentário, timestamp, reações (like/coração),
"Responder". Referência real: mapadeltaro.online, ver memória
`[[modelo-pagina-mx-tarot]]` e `[[licao-entregavel-mockups]]`.

## Quando usar

Alternativa ao carrossel de depoimento em conversa de WhatsApp (padrão do modelo de página). Use este formato quando:
- a página de vendas já usa Instagram/Facebook como prova de tráfego/canal;
- o usuário pedir explicitamente esse formato;
- quiser variar a prova social pra não repetir o mesmo bloco em toda oferta.

## Padrão visual (Instagram/Facebook)

Cada comentário é um card de bolha branca arredondada, empilhado
verticalmente, sobre fundo neutro (bege claro/branco):

- **Avatar** — círculo pequeno à esquerda, foto de perfil ou iniciais.
- **Nome** — parcialmente mascarado (barra colorida por cima, cor
  aleatória por comentário) ou só primeiro nome — nunca nome completo
  real, é comentário fictício.
- **Texto do comentário** — 1 a 3 linhas, tom espontâneo de comprador
  satisfeito: menciona ter comprado, recebido, gostado do material.
  Emoji de mão/coração/aplauso ocasional, não em todo comentário.
- **Metadados** — tempo relativo ("14 s", "4 h", "1 sem"), "Responder",
  e no padrão Facebook também "Me encantó"/reação + contador + "Mensaje"
  + "Ocultar"; no Instagram, coração de curtida à direita.
- Variação de estilo entre comentários: alguns mais informais/curtos,
  outros mais elaborados — não repetir o mesmo formato em todos.

## Como gerar

Pede como imagem ao ChatGPT (skill `gpt-imagem-playwright`, mecânica de
envio/download/QA está lá — siga as regras dela). Um prompt por leva de
comentários (3-5 comentários empilhados numa imagem só, formato vertical),
descrevendo:
- a rede social (Instagram ou Facebook — layout muda: Facebook tem "Me
  encantó"/"Mensaje"/"Ocultar", Instagram é mais limpo, só coração);
  screenshot/UI real da rede, com componentes de UI corretos daquela rede
  (não misturar elementos das duas);
- os textos exatos dos comentários (escreva você o conteúdo, curto,
  crível, coerente com o produto — nunca invente número/promessa que a
  oferta não faz);
- **nomes mascarados ou só primeiro nome**, nunca nome completo de pessoa
  real;
- avatares genéricos ou iniciais coloridas — se pedir foto de rosto,
  aplicar a mesma regra de "mesma pessoa, mesmo avatar" da skill
  `gpt-imagem-playwright` (nunca gerar rosto novo por comentário sem
  necessidade).

## QA antes de subir

- Conferir que nenhum comentário promete número/resultado que o produto
  não entrega (prova social não promete o que o produto não entrega).
- Conferir que a UI da rede social está coerente (não misturar elemento
  de Instagram com texto de Facebook).
- Texto sem erro de espanhol/português conforme o idioma da oferta —
  rodar pelo mesmo tipo de checagem do `gate-idioma.py` se a oferta usar
  esse gate.
