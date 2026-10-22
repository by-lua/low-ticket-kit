# Wiven — Funil "Página final" (link de entrega) + Webhooks/API pós-venda

Perfil browser: `wiven` porta 9254 (conta LeadGo/Dona). Credenciais em `~/.claude/.credentials.env`.
App = Next.js + HeroUI + React Flow. Controlado com `agent-browser --session wiven`.

## 1. Setar LINK DE ENTREGA (redirecionamento pós-compra) — funil "Página final"

Rota: Produto → aba **Funil de vendas** (`/panel/products/<id>/funnel`). Canvas React Flow.

Fluxo que funcionou (2026-09-21, produto Mapa do Tarot `cmubqz6yu010o01pqgcgfw6j0`):

1. Pular a "Criação guiada" — o tour coach-mark ("Abra em tela cheia", 4 passos) **NÃO
   avança** por click sintético nem real no botão "Continuar". Clicar **Pular** e montar manual.
2. Botão **Adicionar etapa** → aba **Estrutura** → botão **"Adicionar Página final ao funil"**
   (é BOTÃO, adiciona o node direto; NÃO precisa drag-and-drop apesar do `.dndnode draggable`).
3. **Selecionar o node** Página final: mouse real down+up no centro dele (mouse move x y; mouse
   down; mouse up — em UM ou sequência de chamadas). Abre o painel `#editingPanel`.
4. No painel: `input[role=switch]` **"Usar página final externa"** → click liga → surge campo
   **"Link da página externa"** (`#editingPanel input[type=text]`). `fill` com a URL destino
   (ex.: `https://mapadotarot.leadgo.dev/painel`).
5. **CONECTAR** etapa inicial → página final. Drag de handle **NÃO cria edge** (nem HTML5 DnD,
   nem PointerEvent sintético, nem drag de handle-a-handle). **O que funciona = click-to-connect:**
   click real (mouse down+up) no `.react-flow__handle.source` do node inicial, DEPOIS click real
   no `.react-flow__handle.target` do node final. Cria 1 edge, some o erro "A etapa inicial
   precisa estar conectada".
6. Botão **"Criar funil"** (canto do painel Configurações do funil). Toast **"Funil criado com
   sucesso"**. Aparece dialog informativo do script de upsell (fechar, ignorar).
7. Confirmar: reload → `document.querySelectorAll('.react-flow__edge').length` = 1, 2 nodes.

Coords de handle/node: `el.getBoundingClientRect()` centro. Em fish, passar x e y como
argumentos SEPARADOS (`mouse move 1022 532`), variável única "x y" quebra ("Missing arguments").

Nota: após "Criar funil", reabrir o `#editingPanel` clicando o node ficou intermitente — mas o
estado (edge + URL externa) persiste. O valor da URL foi confirmado no campo imediatamente antes
de "Criar funil".

## 2. Webhooks pós-venda (compra aprovada → POST na nossa URL)

Rota: `/panel/webhooks` (menu Integrações → Webhooks). Docs: `/panel/docs/v1/webhooks`.

- **Já existe webhook cadastrado**: "SiteExpress Portal" → `https://siteexpress.minhaempresa.com.br/painel/api/webhooks/wiven`, token `<token no env do app, nunca em nota>`, "Todos os produtos". Ou seja, o portal SiteExpress (mesma stack do /painel leadgo.dev) JÁ recebe eventos Wiven.
  - **ERRADO (26/09/2026):** "Todos os produtos" fez a venda do Mapa do Tarot cair também no SiteExpress. Regra: todo webhook só com os produtos da própria oferta (toggle OFF). Ver seção 6 da skill `wiven-checkout`.
- Criar webhook (botão **Criar**): Título, **URL alvo do disparo** (nossa URL, POST JSON), Tipo
  (Padrão | SellFlux), **Eventos** (multiselect), toggle "Disparar para todos os produtos".
- **Eventos disponíveis**: Transação criada, **Transação paga** (=compra aprovada), cancelada,
  estornada, contestada, Chargeback recebido/atualizado, MED recebido/atualizado, Transferência
  criada/concluída/falhou, Sessão criada/atualizada, **Dados do comprador atualizados**, Carrinho
  abandonado.
- **Token de validação**: cada webhook tem token pra autenticar o disparo (campo `token` no payload).

### Payload (HTTP POST JSON) — campos-chave
```
event: "TRANSACTION_CREATED" | (paga/etc)   // status real em transaction.status: "COMPLETED"
token, offerCode, checkoutUrl
client: { id, name, EMAIL, phone, cpf, cnpj, address{...} }   // client.email = email do comprador
transaction: {
  id, status ("COMPLETED"), paymentMethod, amount, currency, installments,
  createdAt, payedAt,
  trackProps: { utm_*, fbc, fbp, ip, ... }
}
orderItems: [ { id, price, product: { id, name, externalId } } ]   // RAIZ do payload, NÃO dentro de transaction (verificado 26/09/2026 em venda real; event = TRANSACTION_PAID; também orderId, orderUrl, subscription)
```

**Pra liberar /painel automático:** webhook evento "Transação paga" → POST na nossa URL →
validar `token` + ler `client.email` + `transaction.status=COMPLETED` → liberar acesso ao email.
Já há endpoint recebendo (SiteExpress portal). Também há **API** completa (`/panel/docs/v1`,
seção Autenticação) com GET Buscar transação, POST Criar checkout etc., como alternativa a polling.

### Área de Membros nativa
Integrações → **Área de Membros**: Astron Members, Curseduca, Member Kit (ativos), Cademi,
The Members (em breve) — plataformas de membros que a Wiven libera acesso automático na compra.
Não há área de membros própria da Wiven pra site externo arbitrário; pro /painel custom o caminho
é webhook.

## 3. Checkout público
URL pública da oferta em `/panel/products/<id>/links` (Links de divulgação):
`https://checkout.wiven.com.br/checkout/<checkoutId>?offer=<OFFERCODE>`.
Ex. Mapa do Tarot / Completo R$27,90: `https://checkout.wiven.com.br/checkout/cmubqz6yy010p01pqilaiahqe?offer=I38JADD`.

## 4 ofertas de checkout — Mapa do Tarot (produto cmubqz6yu010o01pqgcgfw6j0, 2026-09-21)
Base checkout id: cmubqz6yy010p01pqilaiahqe
- Completo R$27,90 → offer=I38JADD
- Completa com Desconto R$22,90 → offer=IIUQ8EW
- Exit R$15,90 → offer=7FJCQSC
- Básica R$17,90 → offer=Q2J6TBK
URLs: https://checkout.wiven.com.br/checkout/cmubqz6yy010p01pqilaiahqe?offer=<CODE>

## Reabrir o painel da Página final numa conferência (2026-09-24, verificado)
Tour "Criação guiada" reaparece ao abrir /funnel: fechar com mouse real down+up em **Pular**, depois recolher "Adicionar etapa" (chevron). Clicar no corpo do nó NÃO abre o painel; clicar no **ícone de engrenagem** dentro do nó (canto direito) abre `#editingPanel`. Ler `input[role=switch]` (checked) e `input[type=text]` (URL).

## Log de webhooks / payload real (2026-09-26)
`/panel/webhooks` → ícone de link da linha → `/panel/webhooks/<id>/logs`. Coluna "Dados enviados" → botão **Ver** abre `[role=dialog]` com o JSON exato (`eval 'document.querySelector("[role=dialog]").innerText'`). Não há botão reenviar visível; reenvio = POST do JSON copiado (contém `token`) no endpoint.
Bug real: handler lendo `tx.orderItems` ignorava toda venda (`no-known-product`).

## 5. EDITAR um webhook (marcar/desmarcar produto) — receita verificada 16/10/2026

Caso de uso: produto novo da oferta precisa entrar nos **DOIS** webhooks (área de membros + Trackeador)
— ver skill `wiven-checkout` §6 e `_memoria/preferencias.md`. **A API é o caminho limpo** (não briga com
o multiselect).

### 5a. Abrir o modal de edição (o clique sintético NÃO funciona)
O `/panel/webhooks` é React (HeroUI `data-react-aria-pressable`). `agent-browser click eNN` no ícone
lápis da linha (**Ações**: `<>`=logs · funil=testar · **lápis=editar** · lixeira) retorna "Done" e **não
abre nada**. Funciona: **sequência pointer real** (`mouse move` → `down` → `up`) **ou** dispatch por
`eval` — `dispatchEvent(new PointerEvent('pointerdown',opt))` + `MouseEvent('mousedown'/'mouseup'/'click')`
no próprio botão (idem para "Salvar"/"Cancelar"). O modal lista os produtos **SELECIONADOS** como chips
(cada um com `×`); as outras opções abrem no dropdown do campo.

### 5b. Editar pela API (recomendado) — `PUT /api/internal/panel/webhooks`
1. Abrir o modal (5a); patch de `window.fetch` para capturar o body do **Salvar**:
   `window.__cap=[]; const of=fetch; window.fetch=(...a)=>{const o=a[1]||a[0]; if(/post|put|patch/i.test(o?.method||'')&&o?.body) window.__cap.push({url:a[0],method:o.method,body:String(o.body)}); return of(...a);}; window.__patched=1;`
2. Clicar **Salvar** (sem mudar nada) → `window.__cap` traz:
   `PUT /api/internal/panel/webhooks` · body `{"webhookId":"<id>","webhookData":{"isApi":false,"allProducts":false,"productsIds":[…],"type":"DEFAULT","title":"…","targetUrl":"…","events":[…]}}`
3. Reenviar o MESMO request trocando **só** `productsIds`:
   `fetch('/api/internal/panel/webhooks',{method:'PUT',headers:{'content-type':'application/json'},body:JSON.stringify(payload)})`
   → **200** `{"success":true,"message":"Webhook atualizado com sucesso","webhook":{…}}`.
   ⚠ preservar `title`/`targetUrl`/`events` **exatamente** como capturado — só `productsIds` muda.
4. Confirmar: reabrir o webhook (5a) e ler os chips.

### 5c. Ids dos webhooks (conta LeadGo, 16/10/2026)
| Oferta | Área de membros (`/painel/api/webhooks/wiven`) | Trackeador (`adstrackeador…/sale/c/…`) |
|---|---|---|
| Jiu-Jitsu | `cmun53usdd27c01o80k46e2xs` | `cmuw2hayr4xku01ohsehumpue` |
| Mapas/Eletrotécnica | `cmuls9zym1nb901pv5yfmlkgt` | `cmuxeltfk1wvl01oilqc783o2` |
| Mapa do Tarot (+ Cigano) | `cmuh1hebg1oqg01ooeg8q9qe9` | `cmuixpo5o49z201oiibel7xut` (v2) |
| AstroDicas | `cmv1an7ev0j1e01pu5iqq8459` | `cmv2lsd6a1lz901pqzff86sxt` |

**Regras:** 1 webhook por destino, **"Disparar para todos os produtos" OFF**, só os produtos da oferta.
**Produto novo entra nos DOIS** (regra da dona 16/10). ⚠ **Upgrades de ofertas diferentes têm nomes quase
iguais** (`Upgrade <Produto> Essencial → Completo - Área de Membros …`) — conferir o nome **EXATO** antes
de marcar (16/10: o webhook do JJ ficou com o upgrade da **Elétrica** e sem o dele → CD do JJ não disparava).

### 5d. Não bater no painel em rajada
Reloads/navegações rápidos em `app.wiven.com.br` derrubam a aba com **403** (Cloudflare) e a sessão cai.
Uma navegação por vez, ~5–8 s entre elas. Perfil morto volta com `~/.claude/bin/browsers.sh wiven-leadgo-dona`.
