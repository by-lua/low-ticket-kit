---
name: wiven-checkout
description: Cadastra e configura oferta na Wiven (app.wiven.com.br) pelo painel logado - criar produto/oferta, order bump, link de entrega/área de membros, pegar URL pública de checkout, e webhook pós-venda. Use quando o usuário pedir para criar produto na Wiven, checkout Wiven, order bump Wiven, link de entrega/área de membros Wiven, webhook Wiven, ou pegar link/URL de checkout Wiven.
allowed-tools: Bash(agent-browser:*), Bash(chromium:*), Bash(curl:*)
---

# wiven-checkout

> **⚠️ 403 CLOUDFLARE NÃO É BLOQUEIO DE IP — É REPUTAÇÃO DA SESSÃO/PERFIL (achado 20/10/2026, Mapa do Tarot).** Veio de fazer MUITO `fetch`/`eval` em rajada no painel (upload de capa via `window.fetch` patchado + envio em chunks por base64, repetido pros 2 produtos) — a Wiven/Cloudflare read isso como bot e trava o PERFIL/sessão naquele navegador, não a rede: **perfil novo (outra pasta de profile), mesma máquina, mesmo IP, passa direto** (testado: `wiven-leadgo-limpo` e `wiven-empresab-gabriel` logaram sem 403 enquanto `wiven-leadgo-dona` e `wiven-leadgo-dona-2` continuavam 403 minutos depois). **Dois erros reais que custaram ~1h20 nessa rodada:**
> 1. **Ficar reabrindo a MESMA aba bloqueada em loop** ("confere se já liberou") em vez de trocar de perfil na hora — 403 de sessão não passa só esperando, raramente libera sozinho rápido.
> 2. **Depois de trocar de perfil, tentar logar numa conta ERRADA** (EmpresaB/Sócio) quando a dona já tinha um perfil LeadGo logado noutra aba — sempre perguntar/confirmar qual conta antes de preencher credencial, nunca assumir "a primeira que carregar".
> **⚠️ "Oferta/Produto atualizada com sucesso" não é prova de que FICOU certo — um reenvio posterior de body capturado antes pode sobrescrever o conserto em silêncio.** Aconteceu 20/10: corrigi nome/descrição com acento quebrado (mojibake) pela UI normal, toast de sucesso apareceu — mas um save seguinte (reenvio de body canônico capturado ANTES do conserto, pra outra ação tipo ligar capa) tinha o nome velho embutido e regravou por cima. Só percebi porque recarreguei a página do zero bem depois; sem o reload teria ficado quebrado. **Regra: depois de QUALQUER fix de texto/nome, recarregar a página (não confiar no form que ficou aberto) e reconferir — e nunca reaproveitar um body de `save` capturado antes de um fix pra mandar de novo depois.**
>
> **Regra daqui pra frente:** (a) **nunca fazer rajada de `fetch`/`eval` raw no painel** — upload de capa via API (seção 1b) tudo bem, mas 1 por vez, com pausa, nunca 2 produtos em sequência imediata sem intervalo; (b) 403 nessa tela → trocar IMEDIATAMENTE pra outro perfil Wiven já cadastrado (`browsers.sh status | grep wiven`), não insistir na mesma aba; (c) perfil novo cai em `/auth/login` → confirmar com a dona QUAL conta antes de logar (LeadGo × EmpresaB/Sócio têm e-mails/senhas diferentes, `~/.claude/.credentials.env`); (d) 2FA da LeadGo vai pro hostinger-mail (`contact@seudominio.com`) — se o hostinger-mail TAMBÉM cair em desafio Cloudflare (mesmo sintoma, mesma causa — sessão flagada por uso pesado), não insistir clicando o captcha: avisar a dona e pedir o código por outro canal (celular).

> **REGRA FIXA DA DONA — código de verificação da Wiven (login):** quando a Wiven pedir código de verificação, o agente abre na caixa de e-mail (hostinger-mail) SÓ o e-mail da Wiven cujo assunto é o código de verificação, o mais recente. NUNCA abre nenhum outro e-mail da Wiven (vendas, notificações, clientes etc.) nem e-mail de outro remetente. Se não achar pelo assunto, para e pergunta.

> **REGRA FIXA DA DONA (repetida muitas vezes; não perguntar, não inventar alternativa):** área de membros é SEMPRE a NOSSA, externa, no site da oferta (`https://<site>/painel`). NUNCA a área de membros do checkout (Wiven, GG, Hotmart, Mundpay) nem página de obrigado genérica dele. Por isso: (1) redirect/página final pós-compra de TODA oferta e bump → `<site>/painel`; (2) link de entrega/e-mail do checkout, se existir → `<site>/painel`; (3) liberação por webhook no nosso servidor (e-mail → SKUs comprados); (4) e-mail de acesso pelo Resend da LeadGo (`no-reply@seudominio.com`) com o link do /painel e "entre com o e-mail da compra". Pronto só com venda-teste REAL provando: webhook liberou → login com o e-mail entra → e-mail chegou. Motivo: em 26/09/2026 a 1ª cliente do Mapa do Tarot BR pagou e não recebeu nada (webhook ignorava a venda, nenhum e-mail saía).

> **REGRA FIXA DA DONA (16/10/2026) — TODO produto/oferta criado entra nos DOIS webhooks NO MESMO DIA, sem exceção.** Vale pra **toda peça**: principal · **order bump** · **combo** · **Upsell 1/2** · **downsell** · **upgrade Essencial → Completo** · produto irmão/cross-sell · oferta de membro. Os webhooks da Wiven são **por produto** e nascem com **"Disparar para todos os produtos" OFF** — produto criado DEPOIS do webhook **não entra sozinho**. Obrigatório, na MESMA sessão do cadastro:
> 1. **Webhook da área de membros** (título `<Oferta> — área de membros`, URL `<site>/painel/api/webhooks/wiven`) → marcar o produto novo na lista de produtos.
> 2. **Webhook do Trackeador** (título `Trackeador — <oferta>`, URL `https://adstrackeador.leadgo.dev/api/webhooks/sale/c/<conexão>`) → marcar o MESMO produto (13 eventos da §6).
> 3. **Servidor da oferta** (`site/server/index.mjs`) → o produto/offer entra no `PRODUCT_SKUS`/`COMPLETO_OFFERS`/`MUNDPAY_NAME_SKUS` (nosso lado).
> **Prova:** abrir `/panel/webhooks`, editar cada um e conferir que **TODOS** os produtos da oferta estão na lista (não só o principal). **Recontar depois de cada produto novo e depois de mexer em funil.** Detalhe na §6.
> **Caso real (16/10/2026):** venda do **order bump "Combo Domínio Total"** (Jiu-Jitsu, R$ 7,32, 21:08) entrou pela área de membros e **não chegou no Trackeador** — o produto (criado 10/10, depois do webhook de 05/10) não estava marcado. Produto fora do webhook = a Wiven não dispara nada ("Nenhum log de webhook encontrado"), a venda some do Trackeador/atribuição **e/ou** o comprador fica sem acesso — sem erro em lugar nenhum.

> **DE ONDE VEM AS PEÇAS (09/10/2026):** o que vai em bump, Upsell 1, Upsell 2, downsell e qual
> **ferramenta/microSaaS** vende junto é decidido ANTES, na mecânica **`mvt-funil`** (regras em
> `criacao-low-ticket-mvt/references/PECAS-DO-FUNIL.md`) — aqui só se monta o que já está no `FUNIL.md`
> da oferta (gate T13.24), com preço na tabela da dona 08/10.

Mecânica pra montar oferta na Wiven (app.wiven.com.br) no nosso ambiente. Complementa
[[browser-cloudflare]]. Receitas cruas (fonte de verdade, mais detalhe que aqui) em
`~/.claude/browser-workspace/domain-skills/app.wiven.com.br/*.md`.

## Acesso

Perfil browser do sistema **`wiven`**, porta **9254**, conta **LeadGo**. Credenciais
`$WIVEN_EMAIL`/`$WIVEN_PASSWORD` em `~/.claude/.credentials.env` — nunca literal.
Sempre headed (não headless). Todo comando: `agent-browser --session wiven ...`.

**Perfil JÁ LOGADO = o único que se usa (regra da dona, 29/09).** Perfil é EXCLUSIVO da Wiven: nenhum pane usa o 9254 pra conferir site/painel (sequestra a aba de quem está na Wiven). Antes de qualquer
ação: `curl -s localhost:9254/json` → deve ter aba em `app.wiven.com.br/panel/...`.
Se tem, anexa nessa aba e segue. PROIBIDO: abrir perfil/sessão/Chromium novo, logar
à toa, pedir código de 2FA pra dona.
**Relogin sozinho (dona 29/09):** só quando o perfil estiver de fato em `/login` (conferido
no curl). Loga NO MESMO perfil (9254/9273) com `$WIVEN_EMAIL`/`$WIVEN_PASSWORD`
(`~/.claude/.credentials.env`, sempre por variável). Quando a Wiven pedir o código de
verificação: `agent-browser --session hostinger-mail` (porta 9274, webmail de
contact@seudominio.com, já logado) → recarrega a INBOX → abre o e-mail mais recente da Wiven →
copia o código → cola na Wiven. Nunca repassar o código pra dona. Só se o e-mail não chegar em
~2 min (recarregando), ou o hostinger-mail cair em login, para e avisa o orquestrador.
**Segundo perfil `wiven2`, porta 9273** (mesma conta, logado pela dona 29/09): se o 9254 estiver
ocupado (aba de outro pane ou da dona no /panel), use `--session wiven2` na 9273. Um perfil por
pane; mesmas regras (relogin só se cair em /login, código pelo hostinger-mail).
**Terceiro perfil `wiven3`, porta 9275** (mesma conta, logado 29/09 pelo orquestrador via
hostinger-mail): terceiro pane Wiven simultâneo. Conferir os três com `curl -s localhost:<porta>/json`
(9254, 9273, 9275) e pegar o que NÃO tem aba de outro pane no /panel. Dois panes no mesmo perfil =
mesma aba ativa (agent-browser segue a aba ativa) → um mexe no produto do outro. Nunca.
Perfil caído/novo sobe com `~/.claude/bin/browsers.sh <nome>` (registro em `~/.agent-profiles/registry.conf`).
**Receita do login (testada 29/09, wiven3):** `open /auth/login` → `snapshot -i` → `fill` textbox
"Email*" e "Senha*" com as variáveis → clicar "Entrar" → esperar ~10s (botão fica "Loading") →
cai em `/panel/dashboard` com heading "Autenticação de 2 fatores" e um textbox único → no
`hostinger-mail`: `open https://mail.hostinger.com/0/mailboxes/INBOX` (recarrega), clicar o 1º
link "Wiven Seu código de verificação", conferir a hora (`Set 29, HH:MM` = agora), o código é o
StaticText de 6 dígitos logo após "Use o código abaixo para continuar:" → `fill` no textbox do 2FA
(valida sozinho, sem botão) → alerta "Autenticação de dois fatores validada com sucesso". Depois
voltar o hostinger-mail pra INBOX.
Se o 9254 estiver **parado** (curl não conecta; `browsers.sh status` = parada), subir o
MESMO perfil com `~/.claude/bin/browsers.sh wiven` — é o perfil persistente logado, não
perfil novo. Orquestrador: dona usando a janela na mão = nenhum pane toca no 9254 até
ela liberar; enquanto isso, pane prepara arquivos (banner/imagens) e enfileira.

Builder de funil (canvas) é **hostil a automação** — React Flow + HeroUI, refs de
snapshot embaralham a cada re-render, click sintético simples não funciona em vários
lugares. Quando `agent-browser` travar 2x no mesmo passo, escalar pra
`browser-harness`/CDP cru (ver `~/.claude/skills/browser-harness`). Botões React em
geral só disparam com sequência pointerdown→pointerup→click real, nunca click simples.

## 1. Criar produto + oferta

> **REGRA FIXA (dona, 10/10/2026): o NOME da oferta/produto na Wiven NÃO leva preço.** Nem
> "Oferta 17,90", nem "Upsell R$ 9,90", nem nada com valor. O preço vai **só no campo de
> valor** da oferta.
>
> **Por que (não é vaidade):** o comprador **lê o nome** no checkout. Se o nome diz "17,90"
> e a página promete "9,90", ele percebe a divergência e **fecha a aba** — a venda morre
> ali, na tela do checkout. Nome com preço congelado denuncia toda reprecificação futura
> (área de membros mais barata que o checkout, promoção, teste de preço) e ainda deixa o
> painel e os relatórios mostrando o valor velho.
>
> Nome descreve a **peça** ("Upsell 1 — Mapas Visuais", "Combo Bumps", "Bump Comandos"),
> nunca o dinheiro. Sufixo de mercado (`- PT`, `- ES`) continua valendo no nome.
>
> **Gate antes de salvar:** (a) nome sem `R$` e sem número que pareça preço; (b) nome,
> descrição, valor cobrado e o que a página promete **concordam**; (c) reprecificar é
> reprecificar **o valor** — nunca editar o nome pra "compensar".

Produtos → Criar. Modal com inputs reais: `input[name="name"]`, `input[name="salesPage"]`
(campo visível de topo é "Buscar" — não usar). tipo/categoria/garantia são comboboxes
custom: abrir clicando o botão pelo texto ("Selecione o tipo/categoria/reembolso"),
clicar `[role=option]` pelo texto exato.

Depois de criar: aba **Informações** (descrição `textarea[name="description"]`, Salvar) →
aba **Ofertas** → Adicionar oferta: **preço vive aqui**, `input[type=number]` com ponto
decimal (ex `"21.91"`), selects Moeda=Real / Idioma=Português (BR) / tipo=Nacional → Adicionar.

### 1b. Capa do produto — SÓ por API (verificado 13/10/2026, conta EmpresaB/Sócio)

> ⚠ **A skill dizia `input[type=file]` na aba Informações — ERRADO neste painel.** Conferido
> campo por campo em `/edit`, aba Informações, aba Ofertas, modal "Adicionar oferta" e
> `/checkout`: **não existe NENHUM `input[type=file]` nem `label` de upload de produto.**
> Clicar na imagem quebrada não abre seletor. Logo a capa **não se resolve por UI** — é por
> `fetch` dentro da página logada:

1. **Upload** — `POST /api/internal/upload/producer/product`, `FormData`:
   - ⚠ **o campo é `files`, NÃO `file`** (com `file` a API responde `200 {"urls":[]}` e não
     devolve nada — falha silenciosa, é o que mais engana).
   - segundo campo: `productId` = id do produto **na conta destino** (sem ele: 400
     "ID do produto é obrigatório").
   - resposta: `{"success":true,"data":{"urls":["{\"path\":\"<owner>/product-photo/<id>/<uuid>\",\"token\":\"...\",\"blurHash\":\"...\"}"]}}`
2. **Montar a URL** exatamente como a LeadGo guarda:
   `https://app.wiven.com.br/files/<path>#blurHash=<blurHash>`
3. **Salvar** — server action `save` (id em `run.js` → `ACT.save`) em
   `POST /panel/products/<id>/edit`, body `[id, {name, description, category, photos:[url],
   salesPage, supportEmail, supportContact, warranty, invoiceName, width:0, height:0,
   length:0, weight:0, deliveryFile:''}]`.
   - `photos` é **array de STRING de URL** (não objeto, não JSON duplo).
   - ⚠ Não passar `{name:null}` nem campo vazio no lugar do nome — teste com `name:null`
     deu **500**. Sempre mandar o nome real.
   - **Body canônico sem adivinhar (15/10/2026, conta LeadGo):** um patch ÚNICO em
     `window.fetch` que grava o body de todo POST `*/edit`, clique em "Salvar alterações"
     (salva sem mudança = inofensivo), pegar o **maior** body capturado (o 1º clique
     costuma vir `[]`/preflight) e reenviar pelo `__a` trocando só `photos` — os campos
     vêm exatamente como o painel os manda (nome, descrição, `category` em código tipo
     `spirituality`, etc). ⚠ **Nunca empilhar 2 patches do fetch** (o 2º captura o 1º e
     recursa em "Maximum call stack size exceeded"; pra desfazer, `location.reload()` —
     o fetch nativo volta sozinho).
4. **Prova**: `Page.navigate` em `/panel/products`, `scrollTo` o fim da lista 3-4×,
   `img.loading='eager'`, sleep 5 e contar `img` com `naturalWidth===0`. Esperado **0**
   quebradas. Antes de "subir tudo", rolar a página — sem isso as linhas de baixo ainda
   estão lazy e a contagem mente (já/accountou `{}`/`%7B%7D` como quebrada em produto já
   corrigido).
- Fonte pronta: `_wiven-migration/fotos/<leadgoId>.jpg`; mapeamento LeadGo→EmpresaB em
  `_wiven-migration/empresab-mapa.json` + `leadgo-eletrica-jiu.json` (match por **nome**,
  o mais antigo quando há duplicata).
- Foto que não existe na origem não se inventa: puxar da conta LeadGo (perfil 9296,
  `/edit` → `img` com `naturalWidth>0` → `fetch` → base64 → `fotos/<id>.jpg`) ou pedir capa
  nova à dona. Descobrir que a **LeadGo também não tem** (`photos: []`) = gap de origem,
  não falha de migração.

> **REGRA (dona, 09/10/2026): nunca criar produto/oferta de BÔNUS na Wiven.** Bônus é **parte do
> produto** — liberado pelo webhook quando a oferta do **COMPLETO** é paga (`PRODUCT_SKUS` +
> `COMPLETO_OFFERS`); o básico libera só `principal`. Produtos próprios só para **order bump,
> upsell, downsell, combo e oferta de membro**. Caso real que motivou a regra: 30/09/2026 foram
> criados 4 produtos de bônus (R$12,90) e o webhook não os reconhecia → pagamento sem entrega
> (`OFERTAS/mapa-do-tarot/produto/UPSELL-CIGANO/TABELA-CHECKOUTS-MEMBROS.md`).
> Regra cheia: `criacao-low-ticket-mvt` › `## REGRA DO BÔNUS × PLANO × BUMP`.

Inputs controlados React (não aceitam `fill` puro): setar valor via
`Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set` + dispatch
`input`+`change`. Ver receita de dropdown abaixo pra mesma lógica em selects custom.

Página de produtos às vezes mostra "carregamento demorando" — é erro de widget, tabela
e edição continuam funcionando.

## 2. Order bump

Order bump = produto separado + vínculo no checkout do principal. Não existe atalho.

1. **Criar o bump como produto** — mesmo fluxo da seção 1 (Produtos → Criar → Informações
   → Ofertas).
2. **Vincular no principal** — abrir produto PRINCIPAL → **Personalizar checkout** →
   **Order Bumps** → "Criar primeiro order bump"/"Adicionar order bump". Form: SELECT
   Produto (escolhe o bump), Título, Descrição, Ancoragem (`input[number]` = preço "de"
   riscado), SELECT "Para todas as ofertas". Adicionar por bump.
3. **Ativar o switch "Mostrar order bumps"** (nasce OFF) e Salvar — sem isso o bump não
   aparece no checkout, mesmo já vinculado.
4. **Cada bump é um produto com funil próprio** — não basta vincular no principal: abrir
   `/panel/products/<idDoBump>/funnel` e repetir seção 3 (página final externa →
   `<site>/painel` + conectar aresta + "Salvar funil"). Sem a aresta, pós-compra do bump
   não cai no /painel. Checklist: 5 funis (principal + 4 bumps) = 5 arestas + 5 URLs
   externas.

> ⚠ **Order bump NÃO persiste por `fetch` (verificado 13/10/2026).** POST direto em
> `/panel/products/<id>/checkout?action=order_bump` (ou via server action) responde **200** e
> **não grava** — a lista volta com 0 bumps. Só o fluxo completo de UI persiste. Receita que
> funciona (rodada EmpresaB, 10 bumps em 2 produtos):
> aba Order Bumps → clicar "Criar primeiro order bump"/"Adicionar order bump" → **esperar o
> `<select>` aparecer** (o form só monta depois, ~5-8s; preencher cedo faz nada) →
> select Produto (**escolher pelo `data-key` = id do produto**, nunca pela posição, nomes se
> repetem) + select Oferta → `input[type=text]` = título → `textarea` = descrição →
> `input[type=number]` = ancoragem → clicar **"Adicionar"** — o do **MODAL**, não "Adicionar
> oferta ao pedido" — → **Salvar**. Remover: `button[aria-label="Remover order bump"]` + Salvar
> (funciona). Receita crua: `_wiven-migration/add-bump-ui.js` / `run-bumps.sh`.

## 2c. Opções de pagamento (padrão, regra da dona, 14/10/2026)

Toda oferta nova: Produto → **Personalizar checkout** → aba **Pagamento** → deixar assim, sem
perguntar de novo:

- **Aceitar pagamentos via:** CPF (nunca CNPJ).
- **Métodos aceitos:** PIX + Cartão de crédito (boleto e pagamento na entrega ficam OFF).
- **Método de pagamento padrão:** PIX.
- **Envio de endereço obrigatório / cupom no checkout:** OFF (ambos).
- **Carteiras digitais (Google Pay / Apple Pay):** deixar como vier (depende da adquirente).
- **Descontos (cartão/boleto/PIX):** 0% nos três.
- **Cartão de crédito:** limite de parcelas **3x**, parcela pré-selecionada **3**, taxa
  extra **1%**.
- **Boleto:** dias para vencimento **3** (campo fica mesmo com boleto OFF).
- **Pix:** tempo de expiração **15 minutos**.

Isso é o padrão de TODA oferta — só muda se a dona pedir explicitamente outra config.

## 2b. Oferta de upgrade de tier (Essencial → Completo, área de membros)

Quando a oferta tem Essencial/básico e Completo (bônus 1-N): quem comprou só o Essencial
precisa de uma oferta própria pra subir pro Completo direto da área de membros, sem recomprar
o principal.

- **Preço fixo R$5,90, SEMPRE (regra da dona, 13/10/2026)** — nunca o cálculo de 50-60% off
  do produto irmão (esse cálculo vale só pra bump/combo/upsell, nunca pro upgrade de tier).
  Mesmo gate de nome sem preço da seção 1, **mas o nome DIZ DE QUAL PRODUTO é** (dona,
  16/10/2026): `Upgrade <Produto> Essencial → Completo - Área de Membros - Idioma Português (BR)`
  — ex.: `Upgrade Manual do Jiu-Jitsu Sem Força Essencial → Completo - Área de Membros - Idioma
  Português (BR)`. Nunca o genérico "Upgrade Essencial → Completo …" sozinho — na lista de
  produtos ninguém sabe de que oferta é. Sufixo de mercado quando aplicável; preço só no campo
  de valor.
- **Capa do produto de upgrade (dona, 16/10/2026, corrigido 24/10/2026):** leva uma arte "**UPGRADE
  PARA COMPLETO**" — mockup do pacote **COMPLETO** (4 capas de bônus + cards + manual + páginas
  internas) com faixa vermelho/amarela "UPGRADE PARA COMPLETO" no topo e seta amarela, no navy da
  oferta. **Gerar do ZERO no GPT** (anexar as capas/mockups reais dos itens do Completo como
  referência de conteúdo + pedir o título "UPGRADE PARA COMPLETO" já nascendo integrado na arte) —
  **nunca pegar o mockup do Completo já pronto e colar/recortar o texto por cima** (ficou errado
  assim no Jiu-Jitsu; a dona corrigiu). Referência aprovada (texto bem integrado, do jeito certo):
  `LOW-TICKET/MODELOS/REFERENCIAS-VISUAIS/upgrade-para-completo-exemplo-jiujitsu.png` (combo: `combo-especial-exemplo-jiujitsu.png`) — receita completa em `banner-checkout-gpt/references/CAPA-PRODUTO-UPGRADE-COMBO.md`. Subir a capa pelo fluxo da seção 1b
  (só por API de `fetch`, campo `files`, montar `photos` no `save`).
- **Mesmo fluxo da seção 2** (produto próprio + funil com página final externa `<site>/painel`
  + webhook) — a oferta precisa entrar no mapeamento do webhook que libera o Completo
  (`COMPLETO_OFFERS`/equivalente), senão paga e não libera.
- **O MESMO produto entra TAMBÉM como order bump no checkout do Básico** (regra da dona,
  13/10/2026: "coloca esse upgrade como order bump da básica") **e é SEMPRE o 1º order bump da
  lista** (dona, 16/10/2026: "na order o bump de upgrade é sempre o primeiro"). O produto de
  upgrade pertence **só à oferta dele** — nunca cruzar com outra oferta. **Escopo do bump: só a
  oferta BÁSICA** — no form do order bump, o SELECT de oferta = a **Básica** (nunca "todas as
  ofertas"): quem escolhe o **Completo** NÃO vê o upgrade (dona, 16/10/2026: "só a oferta básica
  aparece, não aparece no completo").
- **Capa do upgrade = arte regerada no GPT, nunca mockup pronto + texto colado por cima** (dona,
  16/10/2026, corrigido 24/10/2026) — a arte do pacote completo (4 bônus + cards + manual + páginas)
  com a faixa vermelho/amarela "UPGRADE PARA COMPLETO" e a seta, gerada inteira de novo no GPT com os
  mockups reais anexados como referência. Ref. aprovada:
  `LOW-TICKET/MODELOS/REFERENCIAS-VISUAIS/upgrade-para-completo-exemplo-jiujitsu.png` (combo: `combo-especial-exemplo-jiujitsu.png`) — receita completa em `banner-checkout-gpt/references/CAPA-PRODUTO-UPGRADE-COMBO.md`. Não é produto duplicado —
  é o mesmo produto/oferta usado em dois lugares: order bump no checkout (ancoragem = preço
  normal do Completo, ex. R$27,90) E link de upgrade nos cards bloqueados da área de membros.
  Vincular em Personalizar checkout do produto PRINCIPAL → Order Bumps → Adicionar order bump
  → Produto = o upgrade (seção 2, passo 2). **Cuidado:** se já existir outra oferta com o
  MESMO nome em outro produto (padrão comum, já que o nome do upgrade é fixo em toda oferta),
  o dropdown de Produto mostra as duas — confirmar pelo `data-key` do `<li role=option>`
  (id do produto, bate com o que a seção 1 devolveu ao criar) antes de clicar, nunca pela
  posição na lista.
- **Painel:** TODO card do Completo bloqueado (card Completo, bônus 1-N, qualquer módulo
  "só no Completo") lê o preço de uma tabela única (`PRECOS_AREA`) e linka pra essa MESMA
  oferta — nunca preço calculado card a card, nunca "Incluso no Completo" sem link. Badge/CTA
  dizem **"Upgrade com desconto"**, nunca "incluso/somente no Completo". Detalhe:
  `area-membros-netflix` › "Ofertas de membro — preço de quem já é cliente".
- **Oferta nova (mercado sem ela ainda):** cadastrar do mesmo jeito, 1 por mercado/moeda
  (BR R$5,90; outro mercado usa o cálculo de 50-60% off até ganhar oferta fixa própria).
- Exemplo real cadastrado: Mapa do Tarot BR, offer `G8MYTZF`,
  `https://checkout.wiven.com.br/checkout/cmubqz6yy010p01pqilaiahqe?offer=G8MYTZF`.

## 3. Link de entrega / área de membros (externa)

Área de membros = SEMPRE a nossa externa, `<site>/painel` (regra no topo). Na Wiven isso são
DUAS coisas, as duas obrigatórias: (1) **página final externa** no funil de cada produto
(principal E cada order bump) → `<site>/painel`, e (2) **webhook** só com os produtos da oferta
(seção 6) liberando o e-mail no nosso servidor. Só redirect sem webhook = cliente cai no
painel e o login recusa; só webhook sem redirect = cliente não sabe onde entrar.

### 3b. Arquivo de entrega (PDF de entrega) — Entregas → Arquivos (dona, 16/10/2026)

Além do redirect + webhook, o produto **PRINCIPAL** entrega um **arquivo**: a Wiven
(**Entregas → Arquivos**) **só aceita PDF ou ZIP ≤ 30 MB** e obriga um arquivo na entrega.

- **Só o produto principal.** Bump/upsell/downsell **não** leva.
- **Conteúdo:** agradecimento pela compra + **botão com o link da área de membros** +
  "entre com o e-mail que você usou na compra" + suporte. Uma página A4, com a identidade visual
  da oferta. **Tudo clicável:** o botão, o endereço escrito embaixo e o e-mail de suporte
  (`mailto:support@seudominio.com`).
- **Nome do arquivo = o nome exato do produto** (`<Produto>.pdf`), nunca genérico tipo
  `Guia-de-Acesso-…`.
- Modelo/gerador: `LOW-TICKET/MODELOS/PDF-DE-ENTREGA/` — `python3 build.py [slug|alias]`
  (HTML A4 self-contained → Chromium headless `--print-to-pdf`, que cria o link clicável →
  gate PyMuPDF: 1 página + link). Saída em `OFERTAS/<slug>/produto/PDF-DE-ENTREGA/`. Adicionar
  oferta = bloco novo em `ofertas.json` (cores/fontes do `DESIGN-SYSTEM.md`; rodapé só `LeadGo`).
- ⚠ A Wiven guarda o arquivo como **UUID** (`content-disposition: attachment` **sem** filename) —
  o nome do nosso arquivo não aparece no download de lá; o padrão de nome vale pro nosso lado.
- Vale só pra oferta **Wiven**. GGCheckout e Cooud têm outro mecanismo.

Rota: Produto → aba **Funil de vendas** (`/panel/products/<id>/funnel`). Canvas React Flow.
⚠ `/checkout` **NÃO** é o editor de funil — é personalização de checkout (Aparência/Pagamento/
Order Bumps/Upsell-Downsell/Gatilhos); as rotas trocam de conteúdo por render atrasado,
conferir sempre `location.pathname`. Parte automation-hostile do fluxo — ver receita completa em
`funil-pagina-final-e-webhooks.md`.

### 3a. Funil inteiro por POST (13/10/2026) — burla o canvas, ~2 s por produto

> **Não briga com o React Flow.** Toda a receita manual de cliques-aresta-handle (tour,
> drawer, `visibility:hidden`, mouse real) existe só porque ninguém achou a chamada de rede.
> Ela é uma server action. Achada e testada — 21 produtos de uma vez, todos gravados.

`POST /panel/products/<id>/funnel` · headers `content-type: text/plain;charset=UTF-8`,
`accept: text/x-component`, **`next-action: 78489f0c1c08d43a0f84a1bffd6c73ab23e0e8409a`**
(esse id é a `saveFunnelSettings`; **cria o funil se não existir** — responde
`"Funil criado com sucesso"` ou `"Funil atualizado com sucesso"`).

Body = **JSON de 4 argumentos** `[productId, nodes, edges, settings]` (o 3º e 4º podem ser
`[]` e `{}`; o 1º é obrigatório):

```js
const front='a1b2c3d4e5', fin='f6g7h8i9j0';           // ids de 10 chars, aleatórios
const nodes=[
 {id:front,data:{name:'',stepType:'FRONT',productId:id},position:{x:0,y:0}},
 {id:fin,  data:{name:'Página final',
                 settings:{offer:{code:'',name:''},isExternal:true,externalPageUrl:'<site>/painel'},
                 stepType:'THANKYOU',productId:''},position:{x:640,y:0}}];
const edges=[{id:`xy-edge__${front}next-upsell${fin}previous-upsell`,
              source:front,target:fin,sourceHandle:'next-upsell',targetHandle:'previous-upsell'}];
```

- `stepType:'FRONT'` = etapa inicial; `'THANKYOU'` = página final; `isExternal:true` +
  `externalPageUrl` = link externo (`<site>/painel`, regra da dona).
- O **id da aresta é literalmente** `xy-edge__<idInicial>next-upsell<idFinal>previous-upsell`.
- Erros que a action devolve (200 com RSC, ler `1:{...}` no corpo): `"Funil não encontrado"`
  = assinatura errada ou mandando pela `saveFunnelThankYouPage`; `"Invalid data type"` = arg
  no lugar errado.
- **Ações irmãs** (mesmo chunk `2q66w2k1kk37j.js`, nomes via `createServerReference(...,"nome")`):
  `saveFunnelThankYouPage = 60009f2ea82c64a7ad3092bbf0b46de9be940b01e4`,
  `resetFunnelConfiguration = 405da4a659a04ee52944165d037eee4b3e40577150`. ⚠ os ids têm
  **42 caracteres** — regex de 40 corta e devolve 400 "Invalid Server Action request".
- **Prova**: `fetch` do RSC da própria rota e conferir que a URL externa está no corpo +
  `.react-flow__edge`.length === 1 na UI. Script pronto: `_wiven-migration/funil-all.js`
  (lê `_wiven-migration/funil-urls.json` e grava `funil-all-log.json`).
- ⚠ Chamar de novo **sobrescreve** o funil (nodes/edges vão no body). Se o funil já tem
  upsell/downsell, ler o atual pelo RSC e mesclar antes — nunca sobrescrever às cegas.

Passos verificados (quando for mesmo por UI):

1. Pular a "Criação guiada" (tour coach-mark não avança por click sintético) — clicar
   **Pular** e montar manual.
2. **Adicionar etapa** → aba **Estrutura** → **"Adicionar Página final ao funil"** (é
   botão, adiciona o node direto — não precisa drag-and-drop apesar do `.dndnode`).
3. Selecionar o node: mouse real down+up no centro dele → abre painel `#editingPanel`.
4. No painel: switch `input[role=switch]` **"Usar página final externa"** ON → campo
   **"Link da página externa"** (`#editingPanel input[type=text]`) → preencher com a URL
   destino (ex. `.../painel`).
5. **Conectar** etapa inicial → página final: drag NÃO cria edge (nenhuma variante).
   Único jeito: **click-to-connect** — click real no `.react-flow__handle.source` do node
   inicial, depois click real no `.react-flow__handle.target` do node final.
6. **"Criar funil"** → toast "Funil criado com sucesso".
7. Confirmar: reload → `document.querySelectorAll('.react-flow__edge').length` = 1.

Se um passo travar 2x, ver receita crua ou escalar pra `browser-harness`.

### Conectar + salvar + validar (aprendido 01/10 — causa raiz de quase toda demora)

Receita crua completa: `funil-conectar-salvar-e-validar.md`. Os 5 pontos que travam:

1. **Medição inicial é sempre 0 falso** — ao abrir `/funnel`, nós nascem
   `visibility:hidden` com texto vazio e `.react-flow__edge` = 0 MESMO com aresta salva.
   Contagem de edge só vale DEPOIS do ciclo de aba: click tab "Desempenho" → sleep 3 →
   click "Editor do funil" → sleep 5 → aí medir. Sem isso, acredita em "não persistiu" e
   refaz à toa (risco de edge duplicado no estado).
2. **Pra poder clicar, forçar antes** (JS): `visibility='visible'` nos nós,
   `pointerEvents='all'` em todo handle (o **source nasce com `pointer-events:none`
   computed** — sem o force, `mousedown` não chega e o React Flow não inicia conexão) e
   `display:none` nos overlays `aside.w-96` (drawer "Adicionar etapa") e `#editingPanel`,
   que cobrem os handles direitos. Zoom Out não resolve sozinho — o drawer acompanha.
   ✗ Dispatch sintético de PointerEvent no handle não funciona; só mouse real CDP
   (`move` → `down` → `up` no source, sleep, idem no target), com coords medidas na hora
   (zoom muda tudo; coords velhas = clique no vazio).
3. **Salvar = botão "Salvar funil"** → POST `/panel/products/<id>/funnel`
   `[productId, nodes, edges, settings]` → toast "Funil atualizado com sucesso".
   ⚠ Neste canvas **estado ≠ DOM**: a aresta pode estar no payload do POST com
   `.react-flow__edge` = 0 na tela. Pra depurar, hook de fetch e olhar `__cap[2]` (edges)
   em vez da DOM.
4. **Conferir a URL externa ANTES de salvar** — o save persiste o rascunho do
   `#editingPanel` (engrenagem do nó final via dispatch sintético `pointerdown→pointerup→
   →click` funciona); se a página trocou de produto, grava URL do produto errado.
5. **Validação obrigatória**: `open` de novo no `/funnel` → sleep 13 → ciclo de aba →
   edges = 1, id `xy-edge__<front>next-upsell-<thankyou>previous-upsell`. Voltou 0 →
   repetir o ciclo de aba (render atrasado) antes de reconectar.

**Upsell no funil (verificado 29/09):** Adicionar etapa → Produtos → buscar → "+" (nó tipo Upsell).
Oferta do upsell PRECISA ter nome (oferta "Sem nome" = validação "Existem etapas sem oferta
selecionada" mesmo com o código gravado) — nomear em Ofertas do produto e recarregar o /funnel.
Ligações: inicial `next-upsell` → upsell `previous-upsell`; upsell `next-upsell` (aceitou) e
`next-downsell` (recusou) → Página final `previous-upsell`. Engrenagem do nó só aparece em hover.
Snippet 1 clique = "Script do botão" em Configurações do funil (iframe + product-funnel.js, único
por funil); só carregar com params `OCB_*` na URL (senão dá alert). Receita:
`funil-etapa-upsell-oferta-select.md`.

## 4. Banner de checkout (mídias)

**LIMITE DE PESO (regra da dona 10/10/2026): banner ≤ ~400 KB.** Banner de 1–2 MB faz o checkout
parecer quebrado no1º segundo (auditoria 09/10: banners de 0,9–2,0 MB onde havia carrinho
abandonado). Antes de subir comprimir: `magick in.png -auto-orient -strip -resize '1680x1680>' -quality 82 out.jpg`
(desktop; mobile `'1254x1254>'`), baixando qualidade até caber no limite.

**GATE: máximo 1 desktop + 1 mobile por produto. Listar mídias antes de adicionar, substituir se já existe, recontar depois de salvar (esperado 2). Nunca duplicar — detalhes na receita.**

Produto → Personalizar checkout → aba **Gatilhos** → toggle **Mídias** ON → **Adicionar
mídia**. Slots: Acima/Lateral/Abaixo do checkout. Banner topo desktop e mobile = 2 mídias
separadas (Acima+Desktop, Acima+Mobile).

Dropdowns são HeroUI Select — refs de snapshot embaralham a cada re-render, popovers de
multiselect não fecham direito. Ver receita `banner-checkout-midias.md` pro script de
eval que dirige por evento real e confere no `<select>` escondido.

## 5. URL pública de checkout

Em `/panel/products/<id>/links` (Links de divulgação):

```
https://checkout.wiven.com.br/checkout/<checkoutId>?offer=<offerCode>
```

**`checkoutId` ≠ ID do produto** (erro real 29/09: Cigano produto `cmulz3f9a020701...`
× checkout `cmulz3f9d020801...` — quase iguais, o do produto dá "Checkout não encontrado").
Sempre copiar o link de Links de divulgação, nunca montar com o ID da URL do produto.
Conferir abrindo no navegador (sessão separada, nunca 9254): `curl` no checkout dá 403
(Cloudflare), não serve de prova.

## 5b. Pacote de todo checkout (principal E produto irmão/upsell)

Todo checkout da oferta sai igual ao principal, não só o do produto principal:
banner desktop+mobile (seção 4 — **banner ≤ ~400 KB**), **imagem do produto/item** (miniatura do resumo do
pedido, mockup nosso quadrado; **≤ ~250 KB**, ~900–1000px, JPEG `-strip` — mesmo motivo do banner:
tudo que o checkout carrega tem que pintar rápido), **contagem regressiva** copiada do checkout principal
(Personalizar checkout; no Mapa do Tarot: 15 min, vermelho, "Oferta por tempo limitado!
Garanta o seu agora antes que o preço suba."), e **imagem em cada order bump**, inclusive
o combo. Checkout de upsell/irmão (ex. Cigano) nasce com os 4, não depois.

**Combo E Upgrade de tier também são produto próprio — levam imagem igual a qualquer bump**
(regra da dona, 14/10/2026). Não é só order bump "normal": todo produto que aparece no
checkout (combo de bumps, upgrade Essencial→Completo da seção 2b) precisa da foto do item
cadastrada nele (seção 1b), senão aparece sem imagem na listagem/resumo do pedido mesmo com
preço e nome certos. Checklist de "todo checkout do pacote completo" cobre esses dois também.

Imagem do combo de bumps: capas NOSSAS dos itens, proporção original (nunca espremer),
nenhum título cortado por sobreposição, capas preenchendo ~85% do quadro, mesmo formato
das imagens dos outros bumps do checkout. Faixa fina no meio com fundo vazio vira borrão
na miniatura.

Order bumps só aparecem no checkout DEPOIS de escolher a forma de pagamento — "sem bump
no checkout" antes disso é falso alarme.

## 5d. Conferir o checkout público sem tomar bloqueio (aprendido 10/10/2026)

Caso real (Elétrica + Jiu-Jitsu, troca de order bumps): 2 workers e 3 verificadores abriram
`checkout.wiven.com.br` em sequência rápida e o **IP inteiro tomou 403** — no browser também,
não só no `curl`. Durou mais de 15 min e deixou preço de membro, banner e bumps sem prova.
Dois verificadores ainda marcaram "bump não aparece = FALHA" com print tirado **antes** de
escolher o pagamento (regra da seção 5b) — falso alarme que custou uma rodada de correção.

Protocolo de prova pública (worker E verificador):

1. **Quem confere carrega esta skill.** Verificador sem `wiven-checkout` carregada não sabe da
   regra do pagamento nem do 403 e devolve falha falsa.
2. **Uma abertura por oferta**, no browser, ~20–30 s entre uma e outra. Sem `curl` (403 de
   Cloudflare sempre, não prova nada — nem "confirma" bloqueio), sem reload, sem lote paralelo.
3. Em cada abertura, antes do print: **marcar Pix** → rolar até o fim → print de página
   inteira. **Não precisa preencher dados pessoais** (dona, 10/10/2026: "pra testar order bump
   é só marcar Pix") — só a forma de pagamento faz o bump aparecer. É esse print que prova
   bump, imagem do bump, preço e banner de uma vez. Print sem pagamento marcado não prova bump.
4. **Nunca dois panes no checkout público ao mesmo tempo.** Worker tira a prova dele; o
   verificador só abre o checkout depois que o worker fechou. Duas ofertas em paralelo = as
   provas públicas vão em fila, não juntas.
5. **Deu 403 no browser:** parar todo mundo nesse IP, não repetir (cada tentativa pode renovar
   o bloqueio), sem proxy/VPN. Registrar "NÃO CONFERIDO — 403 no IP" com horário. O painel
   (`app.wiven.com.br`) é outro host e continua funcionando: configuração segue, só a prova
   pública espera. Comprador de fora não é afetado.
6. Enquanto o IP não libera, a dona confere pelo celular com dados móveis (IP diferente):
   mandar o link do básico + 1 link de membro avulso + o do combo.

Padrão de preço de bump com oferta de membro: cada produto de bump tem **2 ofertas** — a
normal (vai no checkout principal) e a de membro (vai no `CHECKOUT_URL` do `/painel`). A lista
de produtos da Wiven mostra só o menor preço + "+ 1 oferta": ler as duas ofertas no produto
antes de ligar, e ligar a certa em cada lugar.

## 5c. API pública (`app.wiven.com.br/api/v1`) — o que dá e o que não dá (29/09/2026)

Índice completo lido (26 endpoints). Auth `x-public-key` + `x-secret-key`. Resumo em
`OFERTAS/mapa-do-tarot/produto/wiven-api/WIVEN-API.md` (LOW-TICKET).
- **Dá:** `POST /gateway/checkout` cria produto+oferta+link (preço, métodos, cores,
  thankYouPage, fotos); buscar UMA transação; webhooks.
- **NÃO dá (GUI-only):** editar preço/nome de oferta existente, order bump, imagem
  isolada, banner, contagem regressiva, funil/upsell/link 1 clique, listar vendas.
A doc fica atrás de Cloudflare: `curl` = 403, abrir no navegador do sistema.

## 6. Webhook pós-venda

Rota: `/panel/webhooks` (Integrações → Webhooks). Docs: `/panel/docs/v1/webhooks`.

- **Segredo da conexão Wiven = o TOKEN que a Wiven mostra no webhook criado** (campo `token`). Cole esse token como secret da conexão; não gere outro. Token diferente = `secret_invalido:campo=token` e nenhuma venda entra.
### Regra do Trackeador: eventos a marcar em TODO checkout Wiven (06/10/2026, pedido da dona)
Webhook do Trackeador (URL `https://adstrackeador.leadgo.dev/api/webhooks/sale/c/<conexão>`) com **13 eventos**:
- **Transação:** Transação criada, Transação paga, Transação cancelada, Transação estornada, Transação contestada. (venda e o que acontece com ela)
- **Chargeback e MED:** Chargeback recebido, Chargeback atualizado, MED recebido, MED atualizado. (disputa; o Trackeador trata como chargeback, nunca como venda paga)
- **Sessão:** Sessão criada, Sessão atualizada, Dados do comprador atualizados, Carrinho abandonado. (liga o checkout ao clique pelo `_tkid` em `utm_medium` e mostra onde a pessoa desistiu, inclusive PIX gerado e não pago)
- **NÃO marcar:** Transferência criada/concluída/falhou (saque da Wiven, não é venda; podia virar venda falsa) e os 6 de assinatura, salvo se o produto for assinatura.
- Toggle "Disparar para todos os produtos" **desligado** e produtos da oferta (principal, bumps, upsells) marcados. Ligado só se a conta tiver uma oferta.

### Regra: 1 webhook por oferta, SÓ com os produtos dela (nunca "todos os produtos")
Os webhooks da Wiven são da CONTA. Com o toggle **"Disparar para todos os produtos"** ligado,
venda de QUALQUER produto vai pra aquela URL. Em 26/09/2026 o webhook "SiteExpress Portal"
estava em "Todos os produtos" e recebeu a venda do Mapa do Tarot (log: `18:07:55 · Sucesso ·
TRANSACTION_PAID · siteexpress.minhaempresa.com.br`). Produto diferente no webhook errado.
- Ao criar webhook de oferta nova: toggle "Disparar para todos os produtos" **OFF** e marcar
  só o produto principal + os order bumps daquela oferta.
- Ao criar oferta nova, **revisar TODOS os webhooks existentes**: nenhum pode estar em
  "Todos os produtos". Se estiver, restringir aos produtos dele (não apagar).
- Mesmo assim, o handler do nosso servidor deve IGNORAR productId que não é dele
  (`no-known-product`) sem efeito colateral: defesa em profundidade.
- Token de validação: cada webhook tem o seu (campo `token` no payload). Guardar só no env
  do app (Coolify), nunca em skill, nota ou transcript.

### Regra: TODO produto vendido entra nos DOIS webhooks, na mesma hora em que é criado (05/10 + 16/10/2026)
Cada oferta tem **DOIS** webhooks: o da **área de membros** (`<site>/painel/api/webhooks/wiven`, título
`<Oferta> — área de membros`) e o do **Trackeador** (`https://adstrackeador.leadgo.dev/api/webhooks/sale/c/<conexão>`,
título `Trackeador — <oferta>`). Produto novo da oferta — **principal, order bump, combo, upsell/downsell do
funil, upgrade Essencial → Completo, produto irmão/cross, oferta de membro** — vai marcado nos **DOIS**,
na mesma hora em que é criado. Checklist ao criar QUALQUER produto (não dar por pronto sem os 6):
1. produto criado ✓ · 2. oferta nomeada (sem preço) ✓ · 3. **marcado no webhook da área de membros** ✓ ·
4. **marcado no webhook do Trackeador** (13 eventos, "todos os produtos" OFF) ✓ ·
5. `PRODUCT_SKUS`/`COMPLETO_OFFERS` (+`COMPLETO_OFFERS` no upgrade) do servidor ✓ ·
6. `/panel/webhooks` reaberto mostrando **TODOS** os produtos da oferta nos dois ✓ — **recontar depois de cada produto novo e depois de mexer em funil**. Produto fora do
webhook = a Wiven não dispara nada (pedido mostra "Nenhum log de webhook encontrado"): a venda
some do Trackeador e o cliente fica sem acesso, sem erro em lugar nenhum.
Caso real: upsell "Mapa do Baralho Cigano" (oferta AQNS7ED) foi criado em 29/09 sem entrar no
webhook do Trackeador; venda de R$ 27,90 em 05/10 nunca chegou. Conferir depois de mexer em
funil: abrir `/panel/webhooks`, editar o do Trackeador e ver se todos os produtos da oferta estão
na lista. O combobox de produtos só persiste se o Salvar for do modal certo (com 2 modais
abertos, o Salvar do anterior grava o webhook errado): recarregue a página entre edições.

### Editar um webhook (marcar produto novo) — API, receita 16/10/2026
Marcar/desmarcar produto num webhook já criado = **`PUT /api/internal/panel/webhooks`** com
`{webhookId, webhookData:{isApi:false, allProducts:false, productsIds:[…], type:'DEFAULT', title, targetUrl, events:[…]}}`
→ 200 `"Webhook atualizado com sucesso"`. Para pegar o body: abrir o webhook (`/panel/webhooks`, ícone lápis
da linha — clique sintético não abre; usar sequência pointer real), patch de `window.fetch`, clicar Salvar
sem mudar nada, e reenviar trocando **só** `productsIds`. Ids dos webhooks, armadilha dos **upgrades com
nome parecido** e o "não bater no painel em rajada (403)" estão na receita
`~/.claude/browser-workspace/domain-skills/app.wiven.com.br/funil-pagina-final-e-webhooks.md` §5.

### Criar
Botão Criar: Título (`<Oferta> — área de membros`), URL alvo `https://<site>/painel/api/webhooks/wiven`
(POST JSON), Tipo **Padrão**, Eventos: pelo menos **"Transação paga"** (+ reembolso/chargeback
se o servidor revoga acesso), toggle "todos os produtos" OFF + produtos marcados.

### Payload (POST JSON) — campos-chave (conferido em venda real 26/09/2026)
```
event: "TRANSACTION_PAID" | "TRANSACTION_CREATED" | ...
token, offerCode, checkoutUrl
client: { id, name, email, phone, cpf, ... }
orderItems: [ { id, price, product: { id, name, externalId } } ]   // NA RAIZ
transaction: { id, status, paymentMethod, amount, currency, createdAt, payedAt, trackProps{utm_*, fbc, fbp, ip} }
```
**`orderItems` vem na RAIZ do payload, NÃO dentro de `transaction`.** Ler
`payload.orderItems || payload.transaction.orderItems`. Ler só de `transaction` faz TODA venda
real ser ignorada (`no-known-product`) respondendo HTTP 200 — o log da Wiven mostra "Sucesso"
e ninguém percebe (bug do Mapa do Tarot, 26/09/2026: 1ª cliente pagou e ficou sem acesso).
`offerCode` diz qual oferta (ex.: básico × completo) para liberar os SKUs certos.

### Liberar acesso (servidor da oferta)
webhook "Transação paga" → validar `token` → evento pago → `client.email` minúsculo →
productId de `orderItems` → SKUs → gravar e-mail→SKUs (volume persistente) → idempotente por
`transaction.id` → mandar e-mail de acesso (Resend LeadGo, `no-reply@seudominio.com`, link
`<site>/painel`, "entre com o e-mail da compra") → responder 200. Erro no e-mail não derruba o
webhook. A Wiven NÃO tem botão de reenviar e-mail no pedido: o e-mail de acesso é nosso.

**Produto com vários planos (05/10/2026):** o `product.id` do payload NÃO é o id da URL de checkout. Plano sai do `offerCode`: mapear TODOS (plano, popup de saída, oferta de membro) num mapa `OFFERS = {CODE: [sku]}` e conferir contra a lista de ofertas do produto no painel Wiven (produto > Ofertas). Order bump é produto próprio: mapear pelo `product.id` dele. O token do webhook mora na env do app no Coolify: leia de lá para simular, sem imprimir.

**Order bump vinculado ≠ order bump aparecendo:** depois de salvar, abrir a URL pública de CADA oferta (`?offer=<code>`) e conferir que os bumps aparecem com imagem e preço. O switch "Mostrar order bumps" salvo não basta.

### Prova obrigatória antes de ligar tráfego
1. Venda-teste REAL (PIX de menor valor) → log de webhooks da Wiven mostra entrega na URL
   da oferta e SÓ nela.
2. Corpo da resposta NÃO é `ignored` (conferir o corpo, não só o "Sucesso"/200).
3. `POST <site>/painel/api/login` com o e-mail da compra → 200 com os SKUs certos.
4. E-mail de acesso entregue (Resend `GET /emails/{id}` = delivered/sent).
5. Pós-compra cai em `<site>/painel` (seção 3).

Alternativa a webhook/polling: **API completa** em `/panel/docs/v1` (Autenticação,
GET Buscar transação, POST Criar checkout etc.) — útil pra reprocessar venda perdida.

Integrações → **Área de Membros** oferece liberação automática só pra plataformas de
terceiro (Astron Members, Curseduca, Member Kit; Cademi, The Members em breve) — NÃO usar:
a área de membros é sempre a NOSSA externa (regra no topo).

Webhook → liberação de acesso na área de membros própria: sempre conferir contra o
checklist "SEMPRE verificar" em [[area-membros-netflix]] antes de dar a oferta por pronta.

---

## PARADAS DE MIGRAÇÃO — os pontos onde a oferta PARA e alguém tem que decidir

Toda migração de oferta na Wiven (mudar preço, trocar oferta/página, mover bumps, entrar
nela noutro gateway) passa por estas paradas. Cada uma já custou retrabalho — pule uma e
o webhook responde 200 "Sucesso" com o comprador **sem acesso**.

| # | Parada | Regra | Memória |
|---|---|---|---|
| 1 | **Reaproveitar oferta existente, não criar outra** | Antes de editar gateway, listar as ofertas já cadastradas (principal, downsell, exit/popup). Trocar preço = editar a existente; produto novo = oferta nova só se a análise pedir | [[mundpay-reaproveitar-oferta-existente]] |
| 2 | **Nome com sufixo de mercado** | ` - BR` / ` - PT` / ` - ES`, ES sempre depois. Sem sufixo, oferta de mercado se confunde com a outra | [[sufixo-mercado-nos-cadastros]] |
| 3 | **Order bump é produto NOVO + vinculado** | Personalizar checkout → Order Bumps → ativar switch. Bump nunca sai do nada; bump ocupado por concorrente **não bloqueia** a oferta | [[wiven-order-bump-cadastro]] |
| 4 | **Bump/upell só da oferta da leva** | Banner "todos" = só os banners das ofertas daquela leva, nunca produto de outra | [[banner-escopo-oferta]] |
| 5 | **Máx 1 banner desktop + 1 mobile** | Listar antes, reccontar depois de salvar — salvar duas vezes duplica | [[banner-checkout-sem-duplicata]] |
| 6 | **`salesPage` = URL real da oferta** | Nunca URL inventada; reler o campo DEPOIS de cadastrar | [[link-pagina-vendas-real-no-checkout]] |
| 7 | **Preço local é o da página** | Abrir o checkout público e conferir que cobra exatamente o que o botão promete (popup de saída e downsell também) | — |
| 8 | **Mídia leve** | Banner ≤ ~400 KB, foto do produto ≤ ~250 KB (redimensionar + JPEG). Página que demora a pintar onde tem carrinho abandonado vira mais abandono | [[banner-checkout-sem-duplicata]] |
| 9 | **Webhook: 1 por oferta/destino, SÓ com os produtos dela** | Oferta fora do mapa (`OFFERS`/`COMPLETO_OFFERS`) → webhook responde `no-known-*`, HTTP 200, log "Sucesso", **comprador sem acesso**. **Todos os produtos da oferta (principal, bump, combo, upsell, downsell, upgrade) marcados nos DOIS webhooks** (área de membros E Trackeador) — produto criado DEPOIS do webhook não entra sozinho (caso "Combo Domínio Total", 16/10) | [[acesso-pos-compra-verificar]] |
| 10 | **Todo checkout do pacote completo** | Principal E upsell com banner d+m, imagem do item, contagem, imagem em **todo** bump | [[checkout-pacote-completo]] |
| 11 | **Pós-compa fora da Wiven** | `/painel` externo + e-mail Resend `support@seudominio.com`, WhatsApp <seu-whatsapp>, reembolso no menor prazo que o gateway permitir | [[area-membros-externa-painel]] |

**A parada que mais engana: o webhook responder 200 e dizer "Sucesso" não é prova de
entrega.** Prova é a venda-teste (item "Prova obrigatória" acima).
