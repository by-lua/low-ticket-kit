---
name: ggcheckout-produto
description: Monta uma oferta inteira no GG Checkout (ggcheckout.app) pelo painel logado - produto, checkout com gateways, entrega e as imagens/banners - porque a API publica e bloqueada por WAF. Use quando o usuario pedir para criar produto, cadastrar oferta, montar checkout, configurar gateway, colocar link de entrega, gerar banner de produto ou pegar ID/link de checkout no GG Checkout.
allowed-tools: Bash(agent-browser:*), Bash(chromium:*), Bash(curl:*), Bash(mkdir:*), Bash(nohup:*), Bash(pgrep:*), Bash(sleep:*), Bash(pkill:*)
---

# ggcheckout-produto

> **REGRA FIXA DA DONA (repetida muitas vezes; não perguntar, não inventar alternativa):** área de membros é SEMPRE a NOSSA, externa, no site da oferta (`https://<site>/painel`). NUNCA a área de membros do checkout (Wiven, GG, Hotmart, Mundpay) nem página de obrigado genérica dele. Por isso: (1) redirect/página final pós-compra de TODA oferta e bump → `<site>/painel`; (2) link de entrega/e-mail do checkout, se existir → `<site>/painel`; (3) liberação por webhook no nosso servidor (e-mail → SKUs comprados); (4) e-mail de acesso pelo Resend da LeadGo (`no-reply@seudominio.com`) com o link do /painel e "entre com o e-mail da compra". Pronto só com venda-teste REAL provando: webhook liberou → login com o e-mail entra → e-mail chegou. Motivo: em 26/09/2026 a 1ª cliente do Mapa do Tarot BR pagou e não recebeu nada (webhook ignorava a venda, nenhum e-mail saía).

> **REGRA FIXA DA DONA (16/10/2026) — TODO produto/oferta criado entra nos DOIS webhooks NO MESMO DIA.** Vale pra toda peça: principal · **order bump** · combo · upsell/downsell · **upgrade Essencial → Completo** · produto irmão/cross · oferta de membro. Cada produto novo, na MESMA sessão do cadastro, marcado em (1) **webhook de ENTREGA** (`<site>/painel/api/webhooks/...`) e (2) **webhook de MEDIÇÃO** (Trackeador, `https://adstrackeador.leadgo.dev/api/webhooks/sale/c/<conexão>`) — "todos os produtos" OFF. Produto fora do webhook = a venda some do Trackeador/atribuição e/ou o comprador fica sem acesso, **sem erro em lugar nenhum**. Padrão/incidente (order bump "Combo Domínio Total", Jiu-Jitsu, 16/10): `wiven-checkout` §6.

Montar oferta no GG Checkout ponta a ponta. Complementa a [[browser-cloudflare]]:
lá está como abrir o browser logado, aqui o que fazer dentro do painel.

## Antes de tocar no painel: levantar o que falta

Uma oferta só fica de pé com produto + checkout + gateway + entrega + imagens.
Levante tudo ANTES de começar, e pergunte só o que não dá para deduzir do
projeto. Ordem de perguntas úteis:

| Precisa | Como descobrir sem perguntar | Pergunte se não achar |
|---|---|---|
| Nome e descrição | página de vendas, README, produto irmão no painel | sempre confirme o nome exato |
| Tipo (digital/curso/físico/assinatura) | natureza da entrega | quando houver área de membros |
| Preço | tabela de preços do projeto | sempre confirme |
| Idioma de venda | domínio/país do funil (BR = pt-BR, AR = es) | quando houver os dois |
| Gateways | padrão do usuário (abaixo) | confirme a cada oferta |
| Link de entrega | onde o cliente acessa depois de pagar | quase sempre precisa perguntar |
| Garantia e prazo de entrega | ofertas anteriores | confirme, vai no banner |

**Padrão de gateway do usuário** (atualizado 14/08/2026, reconfirme a cada oferta):
PIX em cascata — **PushInPay** primeiro, **SyncPay** segundo. Cartão no
**EfiBank** (`tokenId eMncLbtKMlNHYyO6XC03`), parcelamento até **4×**.
Era Mercado Pago no cartão até 14/08; os 17 checkouts foram migrados de uma vez.
Tokens PIX: pushinpay `4QyA1osc6n5M240h5b8t`, syncpay `XuQ3R5xziHCK7nRYi3m9`.

Dá para configurar tudo isso por API (`mcp__ggcheckout__update_checkout`), sem
browser — passe só `checkoutId` + `paymentMethods` para não mexer em preço nem
em publicação. **A API tem rate limit**: cerca de 5 updates, depois ~65s de
espera. Em lote de 17, planeje isso.

## Sessão

Portas 9222/9223 costumam estar ocupadas (perfis `gpt` e `hub`). Confira antes.

```fish
pgrep -af "remote-debugging-port" | grep -o "user-data-dir=[^ ]*" | sort -u

mkdir -p ~/.agent-profiles/gg
nohup /usr/bin/chromium --remote-debugging-port=9224 \
  --user-data-dir="$HOME/.agent-profiles/gg" \
  --no-first-run --no-default-browser-check \
  https://ggcheckout.app > /tmp/chromium-gg.log 2>&1 &

curl -s http://127.0.0.1:9224/json/version
agent-browser --session gg connect 9224
```

Login manual na primeira vez; o perfil persistente segura depois. **Todo**
comando leva `--session gg`.

## Duas pegadinhas que custam tempo

**1. `click` não abre menu.** Os menus do painel (`Novo produto`,
`Checkouts`, `Editar produto ▾`, itens da sidebar com `expanded=false`) ignoram
o clique do CDP. Só abrem por teclado:

```fish
agent-browser --session gg focus @REF
agent-browser --session gg press Enter
```

**2. Os refs mudam a cada snapshot e a cada re-render.** Snapshot e ação têm que
ser colados. Um `focus @e27` tirado de um snapshot velho já abriu a página
errada. Se a tela mudou, tire snapshot de novo antes de agir.

## Criar produto — verificado

```fish
agent-browser --session gg open https://ggcheckout.app/products-checkout-v2
agent-browser --session gg snapshot -i -c        # ache "Novo produto"
# focus + Enter no botão, depois click no tipo:
```

Tipos: **Digital** (PDF, planilha, vídeo curto, pack), **Curso** (vídeo + área de
membros), **Produto físico** (precisa envio), **Assinatura** (recorrência).
O item do menu aceita `click` normal — só o botão que abre exige teclado.

Modal "Criar produto": `Nome do produto`, editor de descrição, `Preço base`
(nasce `0,00`), imagem (PNG/JPG/WEBP/AVIF, até 5 MB).

```fish
agent-browser --session gg fill @REF_NOME "Nome"
agent-browser --session gg fill @REF_PRECO "19,90"     # vírgula, formato BR

# Descrição é contenteditable — fill NÃO funciona:
agent-browser --session gg click @REF_EDITOR
agent-browser --session gg keyboard type "Descrição."

agent-browser --session gg get value @REF_NOME         # confira antes
```

`Cancelar` fecha sem salvar — use para ensaiar. Só depois `Criar produto`.

## Criar checkout — parcialmente verificado

Na lista, menu `Checkouts` do produto (focus+Enter) → `Novo checkout`. URL:
`/products-checkout-v2/<PRODUTO_ID>/offers/new`

Assistente de 4 passos: **1 Identificação** → **2 Pagamento** → **3
Personalização** → **4 Publicar**. O rodapé mostra o progresso e o que falta.

- Passo 1: `Título do checkout` (vem preenchido com `<Produto> — Oferta`).
- Passo 2: cards `Configurar agora` / `Deixar para depois`.

O form salva rascunho: ao reabrir a URL ele pergunta *"Continuar da etapa X?"*
com `Começar do zero` / `Continuar`. Trate esse diálogo antes de qualquer
snapshot de conteúdo.

### Passo 2 em detalhe — os gateways

`Configurar agora` já vem selecionado. **Clique em `Avançar →` com ref recém
tirado** — é ele que revela a tela "Métodos de pagamento". Se parecer travado
ali, o ref envelheceu: tire snapshot de novo e clique outra vez.

```fish
# ref sempre fresco, na mesma linha do clique
set R (agent-browser --session gg snapshot -i -c | grep -oE 'button "Avançar[^"]*" \[ref=e[0-9]+' | grep -oE 'e[0-9]+$' | head -1)
agent-browser --session gg click @$R
```

Depois aparecem os checkboxes `PIX` e `Cartão de crédito`. Marque os métodos
(`click` funciona aqui) e cada um abre sua própria configuração:

**Cascata PIX** — "quando um gateway recusa, tenta o próximo. Mínimo 1, máximo
5". É onde entra a ordem de preferência. `+ Adicionar gateway` cria um slot;
cada slot tem `Arrastar para reordenar`, o combobox e `Remover`. Um gateway já
escolhido some da lista dos outros slots.

O combobox de gateway é **custom, não `<select>`** — `select` não funciona,
tem que ser `focus` + `Enter` para abrir e `click` na option:

```fish
agent-browser --session gg click @REF_ADICIONAR_GATEWAY
set S (agent-browser --session gg snapshot -i -c | grep -oE 'combobox "Selecione um gateway" \[expanded=false, ref=e[0-9]+' | grep -oE 'e[0-9]+$' | head -1)
agent-browser --session gg focus @$S
agent-browser --session gg press Enter
agent-browser --session gg snapshot -i -c | grep 'option "'   # pegue o ref
agent-browser --session gg click @REF_DA_OPCAO
```

**Cartão de crédito** — combobox `Gateway` (mesma mecânica) + `Parcelamento
máximo` (À vista até 12×) + switch "Mostrar valor parcelado junto do preço".
Só gateways que suportam cartão aparecem aqui (SyncPay é só PIX, então não
aparece).

Ainda no passo 2: `Método primário (destaque visual)`, `Oferecer desconto pra
quem paga via PIX` e `Envio de comprovante`.

Confirme lendo os comboboxes antes de avançar — o rótulo passa a mostrar a
escolha (`combobox "Selecione um gateway: PushInPay"`).

### Passo 3 — Personalização (opcional)

Abas `Banner`, `Modelo`, `Visual`. O banner aceita `Upload` ou `Link`.

### Imagens do checkout: o que renderiza e o que não

Medido em 14/08/2026, com a página aberta no browser:

- **`bannerUrl` (update_checkout) FUNCIONA por URL externa.** O GG baixa a arte e
  re-hospeda no storage dele, convertendo para AVIF — o valor gravado vira
  `/api/r2-proxy/uploads/<owner>/<ano>/<mês>/<uuid>.avif`. Aparece na página.
- **`image` (a arte quadrada ao lado do título da oferta) NÃO funciona por URL
  externa.** O campo aceita e grava a URL, o `get_checkout` devolve ela
  bonitinha, e a página continua com um placeholder cinza (src fixo em
  `/images/skeleton/default-product-file.svg`, não é onerror fallback).
  Confirmado com cache-bust.

  **Fix correto: upload via aba Geral do PRODUTO pai** (não do checkout):
  1. Navegar para `https://ggcheckout.app/products-checkout-v2/<PRODUTO_ID>`
  2. Aba **Geral** → campo "Foto do produto" → botão **"Escolher arquivo"**
  3. Upload do arquivo (PNG/JPG/WEBP/AVIF, até 5 MB)
  4. Aguardar "Salvar alterações" habilitar → clicar

  Via browser automation:
  ```fish
  agent-browser --session gg open https://ggcheckout.app/products-checkout-v2/<PRODUTO_ID>
  agent-browser --session gg snapshot -i -c   # ache o botão "Escolher arquivo"
  agent-browser --session gg upload @<REF_ESCOLHER_ARQUIVO> /caminho/para/imagem.png
  # aguardar "Salvar alterações" habilitar
  set R (agent-browser --session gg snapshot -i -c | grep -oE 'button "Salvar alterações" \[ref=e[0-9]+' | grep -oE 'e[0-9]+$')
  agent-browser --session gg click @$R
  ```

  O GG processa e re-hospeda como AVIF em `/api/r2-proxy/uploads/…`. Todos
  os checkouts daquele produto refletem o campo `image` automaticamente.
  Um produto pode ter vários checkouts — o upload no produto corrige todos de
  uma vez.

Ou seja: **API respondendo certo não prova tela certa.** Depois de mexer em
imagem de checkout, abra a página e olhe — foi assim que o placeholder apareceu,
depois de a auditoria por API ter dado tudo verde.

**Alternativa quando o MCP não está disponível**: fazer fetch direto dentro
do browser logado. O Chromium já tem as cookies HttpOnly da sessão e as inclui
automaticamente em requests same-origin:

```fish
agent-browser --session gg eval "
(async()=>{
  const d = await fetch('/api/checkouts/CHECKOUT_ID',{credentials:'include'}).then(r=>r.json());
  const r2 = await fetch('/api/checkouts/CHECKOUT_ID',{
    method:'PATCH', credentials:'include',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({title:d.title, uuidOwner:d.uuidOwner, id:d.id,
      price:d.price, paymentMethods:d.paymentMethods, bannerUrl:'URL_DO_BANNER'})
  });
  const vr = await fetch('/api/checkouts/CHECKOUT_ID',{credentials:'include'}).then(r=>r.json());
  return JSON.stringify({status:r2.status, bannerUrl:vr.bannerUrl, published:vr.published});
})()
"
```

Rate limit da API: ~5 calls → espera ~65s. Um por vez com pausa evita 429.

**Spec do banner: mínimo 1280 × 400 px, proporção 16:5, até 8 MB**
(JPG, PNG, WEBP, GIF, AVIF ou BMP). Use exatamente isso ao gerar a arte.

Pode ser pulado — o padrão do painel já entrega um checkout apresentável.

### Passo 4 — Publicar

Mostra `Checklist final` (título preenchido, ao menos 1 método com gateway) e
uma prévia com nome e preço. `Publicar checkout` deixa disponível pros clientes
e o painel confirma com "Checkout publicado com sucesso".

Depois de publicar, o checkout aparece no menu `Checkouts` do produto marcado
como `PUBLICADA`, e a URL do painel revela o uid:
`/products-checkout-v2/checkout/<CHECKOUT_UID>`.

Link público para divulgar: `ggcheckout.app/checkout/<CHECKOUT_UID>`
(redireciona para `/checkout/v2/<uid>`).

**Validar o link só funciona pelo browser.** `curl` na URL pública responde
**403** — é o WAF, não erro do checkout. Abra no browser da sessão e confirme
que a página carrega com produto, preço e formas de pagamento.

## Gateways — verificado

`Ferramentas → Gateways` (`/settings/gateways`). Duas famílias, com taxa
diferente e isso importa na escolha:

- **Split automático** — 3% por transação, retida no ato. Amplopay, EfiBank,
  Mercado Pago, Payevo, PushInPay.
- **Sob Demanda (Billing)** — R$ 0,49 + 3% sobre o total, acumulada e cobrada a
  cada 7 dias. SyncPay e a maioria dos outros.

Atenção real do painel: não pagar a taxa no fim do ciclo **bloqueia a conta e
despublica checkouts e loja**.

Conectados nesta conta (13/08/2026): Amplopay, Mercado Pago, PushInPay, SyncPay
(SyncPay é **só PIX**). Cada card mostra `Conectado`/`Disponível` e as bandeiras
de método (PIX, Cartão, Assinatura).

## Entrega — verificado

Fica **dentro do produto**, não no checkout. O menu `Editar produto ▾` da lista
só tem Duplicar/Apagar — para editar, **clique no nome do produto**:
`/products-checkout-v2/<PRODUTO_ID>`.

Abas do produto: `Geral` · `Checkouts` · `Área de membros` ·
**`Entrega & Estoque`** · `Configurações`. Cada uma mostra
`Configurado` / `Não configurado`, o que serve de checklist da oferta.

Em `Entrega & Estoque`:

- Upload de entregável (até 64 MB; PDF, DOC, DOCX, XLS…)
- Aba **`Email só link`** — `Link entregável (Email)`: a URL que o cliente
  recebe. É aqui que entra o link do produto (ex.: o painel do assinante).
- Aba `WhatsApp link + arquivo` e aba `Estoque`
- Switch **`Entrego este produto por fora`** — para entrega manual; desliga o
  e-mail de entrega e dispensa entregável
- Switch `Enviar dados de acesso no e-mail` — login/senha inicial para área de
  membros externa

Em `Geral` ainda ficam nome, `Valor`, descrição, imagem e **`Moeda do produto`**
(R$ por padrão) — a moeda importa nas ofertas em espanhol.

`Salvar alterações` nasce desabilitado e só habilita quando algo muda.

## Imagens e banners

Geradas no **ChatGPT logado** (perfil `gpt`, porta 9222 — ver
[[browser-cloudflare]]). Regras que vêm da prática do usuário:

- Até **10 imagens** por vez.
- **Prompt em inglês**, mas o texto que aparece na arte no **idioma de venda**:
  diga explicitamente "the text in the image must be in Brazilian Portuguese"
  (ou "in Spanish"). Português e espanhol são os dois idiomas em uso.
- Diga que as imagens são **separadas**, uma por arquivo — sem isso ele devolve
  tudo numa imagem só.
- Peça o tamanho exato do slot. São dois, e o painel exige o mínimo:

| Slot | Mínimo | Proporção | Formatos | Onde aparece |
|---|---|---|---|---|
| Imagem do produto | 1080 × 1080 px | 1:1 | PNG, JPG, WEBP, AVIF · 5 MB | card da loja e e-mail de entrega |
| Banner do checkout | 1280 × 400 px | 16:5 | JPG, PNG, WEBP, GIF, AVIF, BMP · 8 MB | topo do checkout |

  O painel recomenda para a imagem do produto: **quadrada, fundo neutro**.

- Salve em `produtos/imagens/<slug-do-produto>/` dentro do projeto, e reaproveite
  em vez de regerar.

**Todo banner precisa ter, sem exceção:**

1. O que a oferta entrega em **uma frase** ("250 dinâmicas e 100 atividades")
2. **Mockup** do produto
3. **Preço**
4. **Entrega rápida**
5. **Garantia**

Sobre texto em imagem gerada por IA: revise a arte antes de subir. Modelo de
imagem erra letra com frequência, e banner com palavra torta vai para a página
de venda. Se o texto sair errado, regere em vez de publicar.

## Pegar ID e link de checkout

O rótulo do botão na lista já traz o ID — dá para ler sem clicar:

```fish
agent-browser --session gg snapshot -i -c | grep "Copiar ID"
```

O ID é o mesmo da URL: `ggcheckout.app/checkout/<uid>` (uid real responde 307;
inexistente responde 200 — ver [[gg-checkout-url-por-uid]]).

## Confirmar antes de publicar

Criar produto, publicar checkout e mexer em gateway aparecem na conta que recebe
dinheiro do usuário. Antes do clique final, mostre nome, tipo, preço, gateways e
link de entrega e peça o OK. Para ensaiar sem efeito, use `Cancelar` no modal ou
`Deixar para depois` no passo 2 (salva rascunho).

## Fechar

A porta CDP fica aberta em loopback **sem autenticação**, com a conta de
pagamento logada. Feche ao terminar:

```fish
agent-browser --session gg close
pkill -f "user-data-dir=$HOME/.agent-profiles/gg"
```
