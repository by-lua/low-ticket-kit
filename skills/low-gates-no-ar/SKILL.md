---
name: low-gates-no-ar
description: Etapa E9 do sistema LOW-TICKET — prova no ar que a oferta está pronta pra tráfego: eventos do pixel, download do PDF na área de membros e checkout (preço, banner, webhooks). Use antes de liberar tráfego e depois de qualquer mudança em página, painel, servidor, preço, SKU ou webhook.
---

# low-gates-no-ar — E9, prova no ar

> **REGRA FIXA DA DONA (reforçada 10/11/2026) — IC SÓ QUANDO A PESSOA VAI PRO CHECKOUT, no PIXEL META E no TRACKEADOR.** Gate obrigatório antes de dar o pixel/tracking como entregue, em toda oferta.
> - Botão do Básico que só **abre o popup** de upgrade pro Completo mais barato: **0 IC** (nem `fbq`, nem `/api/track`).
> - Dentro do popup: o clique em "quero o Completo mais barato" **ou** em "sigo com o Básico" leva ao checkout: **1 IC** com o valor daquele botão.
> - Na página: clicar no Completo ou no botão da oferta de saída que leva ao checkout: **1 IC**. O popup de saída **aparecer** = 0 IC.
> - Conferir os DOIS lados em cada clique: request `facebook.com/tr` (ev=InitiateCheckout) **e** envio do Trackeador (`/api/track`/`/api/collect`). Um lado certo e o outro disparando no botão do popup = reprovado.
> - Prova: `node scripts/audit-eventos-pagina.cjs` (Gate 1) com contagem por botão colada no `STATUS.md`. Sem essa prova, não se diz "pixel entregue".

Nada vai pra tráfego sem os gates (eventos, página leve, download, checkout) com **prova colada** no `STATUS.md` da oferta. Nunca "deve estar funcionando".

## Gate 0 — Domínio autorizado no pixel Meta (antes de liberar tráfego)
Aprendido com a dona em 06/11/2026, na primeira operação do Calendrier Magique FR. Vale para toda oferta nova e depois de trocar domínio/pixel.

- Abrir o **conjunto de dados correto**, conferir seu ID contra o pixel instalado e acessar **Configurações → Permissões de tráfego — Sites**. Conferir também o **Diagnóstico**, especialmente “Confirme o domínio que pertence a você”.
- Confirmar o domínio público exato da oferta na lista de permissão. Reabrir/recarregar e comprovar que ficou salvo. Havendo outros domínios legítimos do mesmo funil, conferir cada um antes de restringir a lista: tudo que ficar fora será bloqueado. Nunca autorizar o domínio compartilhado inteiro (`pages.dev`) para resolver um aviso de um único projeto.
- `localhost`, `127.0.0.1` e URLs temporárias de desenvolvimento **não são o domínio público da oferta**. Um evento listado com essa origem é evidência de um envio anterior, não prova de que o site esteja hospedado localmente. Não autorizar essas origens no pixel de produção; investigar o registro sem inventar a causa.
- Esta confirmação de **permissão de tráfego do conjunto de dados** é diferente da verificação de propriedade por DNS no portfólio empresarial. Não afirmar que uma substitui a outra, nem presumir que o aviso sozinho prove bloqueio de todos os eventos anteriores.
- Registrar no `STATUS.md`: ID do conjunto, domínio autorizado, data e evidência da configuração persistida. Sem conferir esse gate, não declarar a oferta pronta para tráfego.

## Gate 1 — Eventos (página)
**`trackeador verificar-site` sozinho NÃO prova o lado Meta** (06/11/2026). Ele bloqueia o `fbevents.js`, não vê nenhum
evento do fbq e mesmo assim responde "Sem falhas" (correção em andamento: PR fix/verificar-site-ve-fbq). Até o PR entrar,
a prova é um navegador real que deixa o `fbevents.js` CARREGAR e só captura e aborta `facebook.com/tr`,
`/api/track`, `/api/collect` e a navegação ao gateway. Script pronto (nada chega ao Meta nem ao servidor), na raiz LOW-TICKET:
`node scripts/audit-eventos-pagina.cjs <url> '<botão direto ao checkout>' '<botão que só abre popup>' '<botão dentro do popup>'`
(iPhone; cenários com UTM, só com `fbclid` e popup). Esperado: PageView e ViewContent na carga; 0 IC no botão do popup;
1 IC com `value`/`currency` e `eid` em cada botão que navega; e a URL do gateway com `utm_*` + id da visita.
Colar no `STATUS.md` a linha de cada evento.
**Página não dispara IC/ViewContent/AddToCart próprio** quando o Trackeador já cuida do botão. Duplicata vista no Tarot FR
(06/11/2026): 2 ViewContent por carga.

Antes de abrir a página para QA, interceptar/bloquear os envios ao Meta (`facebook.com/tr`, Graph/CAPI), `/api/track` e `/api/collect`, inclusive beacons/noscript. Capturar o request bloqueado comprova geração, **não** aceite/atribuição pelo Meta. Para provar ingestão, usar somente o dataset de teste dedicado conforme a skill `trackeador`; `test_event_code` não isola um evento do dataset de produção. Nunca testar o pixel de produção em `localhost`.

Capturar requests `facebook.com/tr` no ar (headed + rede, skill `trackeador`):
- PageView ao carregar · cada etapa do quiz (se tiver) · outros eventos da página;
- **InitiateCheckout só quando a pessoa é MANDADA pro checkout** (dona, 05/11/2026), com `value` e `currency` certos do
  mercado. Testar clicando de verdade, um fluxo por vez, e contar os IC:
  · botão que só ABRE popup (Básico → upgrade) → **0 IC** (popup abre, URL não muda);
  · cada botão do popup que navega (upgrade / "non merci, sigo com o básico") → **1 IC**, com o valor do próprio botão;
  · botão do plano caro que vai direto → **1 IC**;
  · popup de saída: APARECER = 0 IC; o clique no botão dele que navega = 1 IC;
  · back/scroll/modal = 0 IC.
- Conferir a identidade nos dois lados: ID Meta correto no request e pixel correto no payload do Trackeador. Instalar o loader com `?pixel=<UUID cadastrado no Trackeador>` para não depender de encontrar o `fbq('init')` em uma fila que o SDK já pode ter consumido. Testar também o SDK Meta carregando antes do loader.
- **Correspondência do Purchase/CAPI:** conferir preservação de `fbclid`, `_fbc`, `_fbp` e o vínculo da sessão até o webhook do gateway (na Hotmart, SCK com mapeamento compatível). Conferir que o envio recupera IP e agente **do comprador**, nunca do servidor/gateway, e os demais dados disponíveis. Em venda real já existente, conferir os nomes em `matching_fields` no log e a qualidade no Meta sem reenviar só para testar. Sem venda real, validar o encadeamento isoladamente e usar somente o dataset de teste para ingestão. Aceite HTTP 200 não comprova atribuição; ausência de `fbc` em acesso sem clique Meta pode ser legítima. Não inventar identificadores, telefone ou dados pessoais para preencher recomendações.
- Sem `facebook.com/tr`: conferir carregamento do SDK, `fbq`, bloqueios de rede e a instalação; apenas trocar a ordem dos scripts não prova a correção. Botão que só abre popup
  não leva `data-tk-*`, `data-plan` nem href de checkout (`href="#upgradepopup" role="button"`; `qa-layout.js` confere).
  Página não manda IC próprio.

## Gate 1b — Página leve (performance) — roda o script, não "olhar a olho"
- `node _skills/low-pagina/scripts/qa-performance.js <url-no-ar> --meta-id=<id do pixel>` → tem que dar **APROVADO**.
  Cola o bloco RESULTADO no `STATUS.md`. Limites e o que reprova: `_skills/low-pagina/SKILL.md` passo 9c.
- Lighthouse mobile (comando em `otimizacao-pagina-vendas`) é complemento: colar score, LCP, TBT e peso total.
- Todo vídeo em player com `preload="none"` (ou fachada que carrega no clique); nenhum vídeo baixando no carregamento.
- Otimizar não pode quebrar o pixel: o próprio script confere pixel Meta + Trackeador; rodar o Gate 1 de novo depois.
- **Funil mostra queda entre Cliques e "Vis. Página"?** (aprendido 06/11/2026) Antes de culpar a página: (1) rodar este
  gate; (2) trocar o toggle do funil de **Meta** para **Trackeador** e comparar; (3) só concluir com ≥ 100 cliques
  (23 cliques não é amostra). "Vis. Página" do Meta só conta se o `fbevents.js` carregar antes de a pessoa sair.

## Gate 2 — Download (área de membros)
- `node scripts/check-download-pdf.mjs <url-da-oferta> <email-de-teste> [--lang=es]` (na raiz LOW-TICKET),
  **depois** do deploy terminar (~1 min no Coolify). Tem que sair OK em todo módulo com conteúdo.
  AVISO (404) = módulo sem páginas — conferir se é esperado; módulo COM páginas dando 404 = rota faltando.
- **Botão no leitor:** `grep -i pdf site/painel/index.html` acha o handler e o `pdfBottomButton`. Logar com a
  conta de teste, abrir um módulo e clicar.
- Bloco de dados do `painel/index.html` (de `PRINCIPAL_CATEGORIES` até `LOCK_SVG`) = só dado puro (helper/DOM
  ali derruba todos os PDFs com 500).

## Gate 3 — Checkout
- **Formato dos identificadores de origem:** conferir os limites documentados do gateway e o retorno pelo webhook. Hotmart documenta códigos UTM/SRC/SCK com até **30 caracteres** e sem underscore. UUID de 36 caracteres não pode ser considerado validado só porque apareceu no link. Usar representação compatível com resolução para a sessão original no Track; nunca apenas cortar o ID. Fonte: [Hotmart — códigos de origem](https://suportehotmart.zendesk.com/hc/pt-br/articles/216441797-Como-identificar-a-origem-das-minhas-vendas-na-Hotmart).
- Abrir o checkout público: cobra exatamente o que o botão (e o popup/downsell) promete.
- Banner e imagem leves (≤ ~400 KB / ≤ ~250 KB).
- `/panel/webhooks` reaberto com **todos** os produtos da oferta nos 2 webhooks.
- **Aviso de venda aceito nos 2 destinos** (incidente Calendrier, 06/11/2026: Trackeador e área de membros devolveram 401).
  Prova: um evento real (abandono de carrinho serve) com 2xx no servidor de entrega e "último aviso OK" na conexão do
  Trackeador (`trackeador doctor --host <host>`), sem `secret_invalido`. Colar no `STATUS.md`.
- **Link de checkout no ar leva a sessão:** clique de verdade num botão e confira na URL do gateway as `utm_*` e o id
  da visita (Hotmart: `sck` ≤ 30 caracteres, sem `_`). Teste também a visita **só com `fbclid`** (volta pelo app do Facebook):
  sem UTM, a venda só casa se o id da visita chegar ao webhook.
- Acesso liberado no `/painel` pelo modo teste oficial do gateway/Trackeador — nunca venda de teste no webhook
  de produção do Trackeador.

Fecho: prova de todos no `STATUS.md` → oferta pronta → `criativo` e `metaads-kevones`.
