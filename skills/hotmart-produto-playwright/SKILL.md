---
name: hotmart-produto-playwright
description: Cadastra produto, precificação, checkout e webhook na Hotmart pelo browser, usando o perfil persistente `hotmart`. Use sempre que o usuário pedir para criar produto na Hotmart, configurar checkout, ativar/desativar forma de pagamento, pegar link de checkout, ou cadastrar webhook/HOTTOK da Hotmart.
---

# hotmart-produto-playwright

Automação de browser pra cadastro e configuração de produto na Hotmart (`app.hotmart.com`), usando o perfil persistente do sistema (não o Chromium empacotado do agent-browser, que trava no Cloudflare).

> **REGRA FIXA DA DONA (16/10/2026) — TODO produto/oferta criado entra nos DOIS webhooks NO MESMO DIA.** Vale pra toda peça: principal · **order bump** · combo · upsell/downsell · **upgrade Essencial → Completo** · produto irmão/cross · oferta de membro. Cada produto novo, na MESMA sessão do cadastro, marcado em (1) **webhook de ENTREGA** (`<site>/painel/api/webhooks/hotmart`) e (2) **webhook de MEDIÇÃO** (Trackeador, `https://adstrackeador.leadgo.dev/api/webhooks/sale/c/<conexão>`) — "todos os produtos" OFF. Produto fora do webhook = a venda some do Trackeador/atribuição e/ou o comprador fica sem acesso, **sem erro em lugar nenhum**. Padrão/incidente (order bump "Combo Domínio Total", Jiu-Jitsu, 16/10): `wiven-checkout` §6.

## Perfil

Perfil `hotmart` registrado em `~/.agent-profiles/registry.conf`, porta fixa. Se não existir:

```bash
echo "hotmart <porta_livre> https://app-vlc.hotmart.com/login" >> ~/.agent-profiles/registry.conf
~/.claude/bin/browsers.sh hotmart
```

Credenciais em `~/.claude/.credentials.env` (`HOTMART_ACCOUNT`, `HOTMART_URL`, `HOTMART_EMAIL`, `HOTMART_PASSWORD`, `HOTMART_HOTTOK`). Login pede 2FA por email — o humano digita o código na janela, você só confirma que a sessão avançou.

```bash
agent-browser --session hotmart snapshot -i -c   # confere se logou
```

## Regra geral de clique — a Hotmart usa web components custom

Muitos elementos da Hotmart são custom elements (`hot-select-option`, switches Radix-like) que **não respondem a `agent-browser click @ref`** nem a `.click()` simples. Padrão que funciona sempre: pegar o elemento por `elementFromPoint` ou busca de texto, e disparar a sequência completa de eventos de mouse:

```js
(()=>{
  const el = document.elementFromPoint(x, y); // ou busca por texto
  const r = el.getBoundingClientRect();
  const o = {bubbles:true,cancelable:true,view:window,clientX:r.left+r.width/2,clientY:r.top+r.height/2,pointerId:1,isPrimary:true,button:0};
  ['pointerover','mouseover','pointermove'].forEach(t=>el.dispatchEvent(new (t.startsWith('pointer')?PointerEvent:MouseEvent)(t,o)));
  el.dispatchEvent(new PointerEvent('pointerdown',o)); el.dispatchEvent(new MouseEvent('mousedown',o));
  el.dispatchEvent(new PointerEvent('pointerup',o)); el.dispatchEvent(new MouseEvent('mouseup',o));
  el.dispatchEvent(new MouseEvent('click',o));
})()
```

Tire screenshot (`agent-browser --session hotmart screenshot /tmp/x.png` + Read) sempre que o snapshot de acessibilidade não mostrar a lista de opções — muitos dropdowns/listas só aparecem no DOM visual, não no `snapshot -i -c`.

### Toggle "desligado" pode estar ligado e travado

Um `<button role="switch">` pode ter `disabled` (visual cinza, parece off) mas `aria-checked="true"` — significa **ligado e obrigatório**, não desligado. Antes de clicar de novo achando que está off, confira via DOM:

```js
document.querySelector('button[role="switch"]').getAttribute('aria-checked')
```

Aconteceu com "Cartão de crédito" no checkout: sempre trava ligado (não dá pra desligar), o cinza é só o estilo `disabled`.

### Fechar modal (X) — clique no botão, não no ícone svg filho

O X de fechar é um `<button>` com `<svg>` dentro. Clicar direto na coordenada do ícone às vezes pega o svg (sem handler). Ache o botão pela posição (`top<160 && left>790` tipicamente) em vez do ícone.

### Scroll dentro de modal

`element.scrollTop = element.scrollHeight` às vezes não dispara re-render. Use `scrollBy(0, N)` em vez de setar `scrollTop` direto, e sempre re-screenshot pra confirmar.

## Fluxo: criar produto

1. `Produtos → Meus produtos → Criar produto` (ou link "Criar produto" se não tiver nenhum ainda)
2. Escolher tipo (Curso Online é o padrão seguro pra produto digital com entrega/redirect externo, mesmo se a área de membros real for fora da Hotmart)
3. **Informações básicas**: nome, descrição (mínimo 200 caracteres — a Hotmart valida e mostra erro embaixo do textarea), idioma (dropdown custom, ver truque de clique acima), **país principal para vendas** — é single-select **sem filtro por digitação**, lista alfabética fixa, tem que rolar/scrollIntoView até achar o país. Não existe opção "todos os países" — o campo é só o país âncora do catálogo, não trava quem pode comprar.
4. **Categoria do produto** (chips clicáveis)
5. **Precificação**: moeda (USD converte automático pra moeda local do comprador no checkout — não calcule conversão própria na sua página, vai descasar com o câmbio que a Hotmart usa), prazo de reembolso, forma de pagamento (à vista / parcelado — trava depois de criado), valor.

## Fluxo: configurar checkout (formas de pagamento)

Em `Precificação e ofertas → Configurar checkout → Editar manualmente` (evite "Tudo pronto em 1 clique", não dá controle fino):

1. Tela "dados essenciais" — Nome+Email obrigatório, ligar "Número do celular" se quiser recuperação de venda
2. Tela "formas de pagamento" — dois cards editáveis por lápis: **Principais formas de pagamento** (Hotmart, cartão, débito, Pix, Apple Pay, etc) e **Formas de pagamento parceiras** (PayPal, Mercado Pago, Nequi, Bancolombia, MACH, MB Way, Servipag, Yape, Pay By Bank...). Cada um abre modal com lista scrollável de toggles.
   - Se o pedido for "sem boleto/dinheiro físico, só o que recebe na hora": desligar **Boleto bancário** e **Boleto bancário (Dispositivo Móvel)** nas principais, e qualquer rede de pagamento físico tipo **Servipag** nas parceiras — o resto (Pix, cartão, débito, wallets como Nequi/MACH/MB Way/Yape) é instantâneo, mantém ligado.
   - Cuidado: clicar no ícone de lápis (editar) em vez do toggle abre uma sub-config (ex: dias de vencimento do boleto) em vez de ligar/desligar — sempre mire a coordenada do toggle, não do lápis.
3. Telas seguintes (ferramentas extras, suporte, dados pós-venda) são opcionais — pode clicar Continuar direto se não houver pedido específico.
4. **"Escolha onde seu cliente irá finalizar a compra"** — aqui fica a página de obrigado. Se a entrega é uma área de membros **externa** (fora da Hotmart Club), clique **"Adicionar página externa"** e preencha "URL para compras aprovadas" com a URL de obrigado do seu domínio.
5. Tela final de revisão → **Concluir e fechar**.

## Pegar o link de checkout

`Links de divulgação` (menu lateral do produto) → aba "Links principais":
- **Página de Vendas** (`go.hotmart.com/...`) — landing page da própria Hotmart, não é o link direto de compra.
- **Página de pagamento** (`pay.hotmart.com/...`) — **esse é o link de checkout direto**, o que embeda no seu site/anúncio.

Ambos aparecem só depois de um `sleep 2` (carregam via skeleton assíncrono).

## Cadastrar Webhook e pegar HOTTOK

Webhook **não fica dentro do produto** — é ferramenta de conta, em `Ferramentas` (ícone de chave inglesa na sidebar principal) → busca "webhook" → **Webhook (API e notificações)**.

1. `Cadastrar Webhook`: nome, selecionar o produto (checkbox numa lista dropdown — não é multi-select nativo, é lista com checkbox por item), URL de envio de dados (seu endpoint, ex `https://seudominio/api/webhook/hotmart`), versão 2.0.0 (recomendado), eventos (mínimo **"Compra aprovada"** pra liberar acesso), marcar checkbox de conformidade LGPD/dados, Salvar.
2. Depois de salvo, vai pra aba **Autenticação** da mesma tela de Webhook pra pegar o **Hottok de verificação** — é o segredo que valida a assinatura do POST recebido (equivalente a webhook secret). Fica mascarado por padrão; clique "Mostrar hottok" e extraia via DOM (não print/screenshot, é credencial):

```js
Array.from(document.querySelectorAll('input')).filter(i=>i.type==='text' && i.value.length>10).pop().value
```

Salve em `~/.claude/.credentials.env` como `HOTMART_HOTTOK` — nunca em texto solto na conversa nem em screenshot.

## Checklist de produto pronto pra vender

- [ ] Informações básicas completas (nome, descrição 200+, idioma, país, categoria, imagem)
- [ ] Preço e forma de pagamento
- [ ] Checkout configurado (dados essenciais, formas de pagamento revisadas, sem boleto se pedido)
- [ ] Página de obrigado (Hotmart nativa ou externa) configurada
- [ ] Link de checkout (`pay.hotmart.com/...`) extraído e repassado pro time de código/tráfego
- [ ] Webhook cadastrado + HOTTOK salvo em credenciais
- [ ] Produto ainda fica "Rascunho" até enviar pra análise (`Finalizar cadastro` no painel) — avisar o usuário antes de enviar, é passo irreversível de revisão

## Rotas reais do painel de produto (mapeadas em 2026-09-15)

Não existe `/pricing`: essa URL carrega o menu e deixa o painel direito **vazio**,
sem nem disparar request. Perde-se muito tempo achando que é bug de browser. As
rotas que abrem de fato:

| O que | Rota |
|---|---|
| Preços e ofertas | `/products/manage/{id}/offers` |
| Config. de checkout (pagamento, obrigado, dados, formas) | `/products/manage/{id}/tools/checkout/settings` |
| Área de membros / entrega | `/products/manage/{id}/content/add` |
| Ferramentas (Aparência, etc.) | `/products/manage/{id}/tools` |
| Builder do checkout | `custom-checkout.hotmart.com/{id}` → card "Publicado" → `Editar aparência` → `/builder/{pageId}` |
| Histórico de vendas | `app.hotmart.com/sales` (NÃO `/tools/sales/history`, dá 404) |

### Clique no menu do produto

Os itens do menu lateral do produto (`Precificação e ofertas`, `Área de membros`…)
são `<button>` simples. O que funciona:

```js
[...document.querySelectorAll('button')].find(e=>/^Área de membros$/.test(e.textContent.trim())).click()
```

Já as **abas** (`Pagamento` / `Página de Obrigado`) e os **lápis de editar** dentro
do modal de checkout NÃO respondem a `.click()` nem a `dispatchEvent`; tem que
pegar por índice em `querySelectorAll('button,a')` e clicar. Dumpe índice +
`getBoundingClientRect()` antes, e **nunca clique por coordenada solta**: num teste
o clique caiu em `builder-row-down` e mexeu a ordem do bloco, e outro caiu na
sidebar e jogou pra "Central de Colaboradores".

### Formas de pagamento ficam em DOIS grupos

`tools/checkout/settings` → lápis de "Formas de pagamento e cupom" → dois cards:

- **Principais formas de pagamento** — Hotmart, Cartão de crédito, Débito, Pix,
  Pix automático, Apple/Google Pay, NuPay, Boleto (móvel e normal).
- **Formas de pagamento parceiras** — PayPal, Mercado Pago, Débito virtual Caixa,
  Klarna, SOFORT, **Nequi** (CO), **Bancolombia**, **MACH** (CL), MB Way,
  **Servipag** (CL), **Yape** (PE), Pay By Bank.

Ler o estado de todos de uma vez:

```js
[...document.querySelectorAll('input[type=checkbox],[role=switch]')].map((s,i)=>{let p=s,l='';for(let k=0;k<6&&p;k++){p=p.parentElement;if(p&&p.textContent.trim().length>2&&p.textContent.trim().length<60){l=p.textContent.trim();break}}return i+':'+l+'='+(s.checked??s.getAttribute('aria-checked'))})
```

**"Pago en efectivo"** (CO/PE/CL) não tem toggle próprio — vem embutido no provedor
"Hotmart" e só sai desligando o Hotmart inteiro (o que mataria o cartão). Se a
regra do cliente é "só método com confirmação rápida", o que dá pra desligar é
Servipag, SOFORT e os boletos.

## Cronômetro do checkout: tipo "Quantidade de tempo" é por visitante

No builder, componente **Contagem Regressiva** tem dois tipos. `Quantidade de tempo`
(`00:HH:MM`) é **por visitante**, com texto separado pra contagem ativa e pra
contagem zerada.

**Pegadinha que já gerou diagnóstico errado:** o navegador que já visitou o
checkout vê `00 : 00 : 00` + o texto de "oferta finalizada" para sempre — a janela
é gravada por visitante. Isso NÃO significa que o cronômetro venceu pra todo mundo.
**Sempre confira num perfil de browser virgem** (`~/.claude/bin/browsers.sh <outro>`)
antes de concluir que o contador está quebrado.

## Order bump herda moeda/idioma da página do builder, não do país

O bloco "Aproveite e compre junto" é renderizado pelo builder: se a página foi
montada em PT/BRL, o bump aparece com rótulos em **português** e valor em **R$**
dentro do checkout mexicano, mesmo com o produto principal em MXN e o addon com
preço base em US$. Os textos ("Aproveite e compre junto:", "Adicionar produto",
"Cupom de desconto") saem do builder — traduza lá. Checar sempre trocando país no
seletor "Cambiar país" do checkout publicado.

## Área de membros: EXTERNA não é o default

`/{id}/content/add` mostra a área vinculada. Se aparecer um card do Club com
`Link de acesso ao produto: https://hotmart.com/PT_BR/club/{conta}/products/{id}`,
o produto está entregando pela **Área de Membros da Hotmart**, não pela sua.

Quando a entrega é o seu sistema (webhook `PURCHASE_APPROVED` → seu app libera
acesso e manda e-mail), esse vínculo com o Club é ruído: o comprador recebe um
acesso a mais, vazio, e em `PT_BR`. Desvincular é pelo menu `⋮` do card — **mas
confirme com o usuário antes**, porque a Hotmart usa a existência de conteúdo/área
no critério de aprovação do produto, e produto já aprovado pode cair em revisão.

Checklist de entrega externa:
- [ ] Webhook cadastrado com `PURCHASE_APPROVED` (+ cancelado/reembolso/chargeback)
- [ ] HOTTOK salvo e verificado no endpoint
- [ ] `Página de Obrigado` apontando pra sua `/gracias`, não pra nativa da Hotmart
- [ ] Área de membros da Hotmart desvinculada **ou** conscientemente mantida
- [ ] Casamento da ordem: se o checkout é link hospedado, a Hotmart não devolve
      `external_reference` — o único vínculo é o **e-mail do comprador**, e ele pode
      digitar um e-mail diferente do que deu no seu funil. Prever fallback manual.

## Trocar para área de membros externa (fluxo real, testado 2026-09-16)

`/{id}/content/add` → menu `⋮` do card (é `querySelectorAll('button')[17]` nessa
tela) → **"Trocar para área de membros externa"** → modal de aviso → **"Usar área
de membros externa"** → abre um questionário (Memberkit/Kajabi/Astron/Cademi/Outra)
que pode ser **Fechado sem responder** → o formulário real fica atrás dele:

- `https://` → URL de login da sua área (ex.: `https://dominio/entrar`)
- `Digite um nome para aluno` + `Digite a senha do aluno` + `Reescreva a senha`
  → credencial de um **aluno de teste real** pra revisão da Hotmart

Depois `Salvar`. Confirme recarregando `/content/add`: se o `Link de acesso ao
produto: https://hotmart.com/PT_BR/club/...` desapareceu, desvinculou.

**Os inputs são React controlados.** `el.value = x` NÃO funciona (o botão Salvar
continua inerte). Use o setter nativo do protótipo:

```js
function S(el,v){const d=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value');
  d.set.call(el,v);['input','change','blur'].forEach(t=>el.dispatchEvent(new Event(t,{bubbles:true})))}
```

Mesma regra vale pros switches (`[role=switch]`, Radix): só viram com a sequência
`pointerdown → mousedown → pointerup → mouseup → click` disparada no próprio
switch. `Salvar alterações` também.

Aluno de teste, quando a área é própria com login por e-mail/senha: criar o
usuário direto no banco com o mesmo esquema de hash do app (aqui
`scrypt$<salt hex>$<derived hex>`, 64 bytes, `password.normalize('NFKC')`) e
validar com `POST /api/session` antes de entregar a credencial pra Hotmart.
