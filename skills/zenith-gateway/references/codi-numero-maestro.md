# Receita ponta a ponta: CoDi no Número Maestro (MX)

Integração real, feita em 09/09/2026 e no ar em `elnumeromaestro.leadgo.dev`.
Serve como molde para qualquer método da Zenith que devolva `nextAction`.

O contexto: o checkout mexicano já rodava na XPag (SPEI + OXXO). CoDi é **o
único método que a XPag não tem** — QR interoperável lido pelo app do banco,
acredita em segundos. A decisão foi **só CoDi na Zenith, o resto fica na XPag**:
duas gateways convivendo, cada uma com o que sabe fazer. Não migre o que já
funciona só para consolidar fornecedor; migrar SPEI/OXXO seria risco sobre
dinheiro que já entra, em troca de nada.

## Ordem que funciona

1. **Credencial** — `/integracoes-zenith`, com o código do autenticador em mãos.
2. **Conferir o método no catálogo da conta** antes de escrever código.
3. **Código** — cliente, webhook, ramo no checkout, botão na tela.
4. **Registrar o endpoint de webhook** (só depois de ter o secret escolhido).
5. **Env no host + deploy**.

Inverter 4 e 5 registra eventos apontando para um domínio que ainda não sabe
validar assinatura — todo evento vira 401 no log e a Zenith conta como falha de
entrega.

## 1. A credencial sai atrás de 2FA

Em `/integracoes-zenith`, "Criar nova chave" aparece **desabilitado**, com
"Configuração pendente / Conclua os itens indicados abaixo" no topo e **nenhum
item marcado como pendente**. Sem tooltip, sem `title`, sem texto ao lado.
Selecionar produto, país e método não muda nada.

O que destrava é o **código de 6 dígitos do autenticador**, que o painel pede
num modal ("AÇÃO PROTEGIDA — Confirmação de segurança"), válido por cinco
minutos e só para essa ação. Não é bloqueio de conta, não precisa de chamado.

A secret aparece **uma vez só**. Capture direto para o arquivo de credenciais,
sem imprimir no terminal.

## 2. Conferir o catálogo antes de codar

```bash
curl -H "X-API-Key: $ZENITH_PUBLIC_KEY" -H "X-API-Secret: $ZENITH_SECRET_KEY" \
  "https://api.zenithworld.com.br/integrations/payment-methods?country=MX&currency=MXN"
```

Devolveu, nesta conta: `oxxo`, `spei`, `codi`. O CoDi vem como
`{"flows":["qr_code"],"category":"instant","capabilities":{"asynchronous":true}}`.

**Cartão não aparece em nenhum dos seis países.** Quem chegar aqui procurando
cartão para o México não vai achar na Zenith.

### Sandbox não existe por padrão

```
HTTP 403  {"code":"ENVIRONMENT_NOT_ALLOWED",
           "message":"Environment is not allowed for this product"}
```

Verificado para MX/MXN, referência de suporte `ZEN-AQESSPMK`. O seletor de
ambiente do painel também só lista `production:*` nos seis países — o "Sandbox"
que aparece no card do produto é rótulo estático, não ambiente disponível.

Consequência prática: **a primeira cobrança é com dinheiro real**. Faça uma, de
valor baixo, antes de ligar tráfego. É a mesma situação do voucher OXXO na XPag,
que também nunca foi testável em sandbox.

## 3. O código

Quatro arquivos, no molde que já existia para a XPag:

| Arquivo | Papel |
|---|---|
| `src/lib/zenith.ts` | Cliente `server-only`. Cria a cobrança, consulta estado, verifica assinatura |
| `src/lib/zenith-config.ts` | `codiEnabled()` — flag client-safe, sem `server-only` |
| `src/app/api/webhook/zenith/route.ts` | Recebe e valida o evento assinado |
| `/api/checkout` + `CheckoutMx.tsx` | Ramo do método novo e o botão |

### Decisões que valem repetir

**Valor em unidade minoritária.** `Math.round(pesos * 100)`. MX$ 199,00 vira
`19900`. Errar isso cobra 199 centavos e a API aceita numa boa — o mínimo dela é
MX$ 0,01, então não há validação que salve.

**QR desenhado no servidor.** `qrcode` → data URI, entregue pronto para a tela.
O público chega pelo WebView do Facebook/Instagram; carregar uma lib de QR no
cliente e torcer para renderizar igual em todo WebView é aposta desnecessária.

**Nada de copiar e colar no CoDi.** Foi a primeira decisão, e estava errada —
ver "CoDi não tem copiar e colar" mais abaixo. O payload não entra em campo
nenhum de app bancário.

**`Idempotency-Key` é por INTENÇÃO, não por pedido.** Chave nova a cada tentativa
de pagamento do mesmo pedido; reusar a antiga com payload diferente devolve
`409 IDEMPOTENCY_KEY_CONFLICT`. `referenceId` é que identifica o pedido.

**`referenceId` com sufixo do método** (`<orden>:codi`). A ordem pode ter tentado
SPEI antes; id pelado colidiria entre os dois cobros.

**Sem QR, não mostre nada.** Se `nextAction.type !== "qr_code"` ou faltar
`code`, falhe e caia no fallback (SPEI/OXXO) com a ordem preservada. A doc avisa
que a rota operacional pode estar fora mesmo com o método no catálogo — QR vazio
é pior que método ausente.

**Nome e e-mail reais.** `422 CUSTOMER_NAME_INVALID` / `CUSTOMER_EMAIL_INVALID`
em dado fictício, e a doc avisa que insistir leva a **bloqueio permanente da
conta** após análise de conformidade. Não invente comprador nem para testar.

## A tela do comprador: o que só aparece montando

Esta parte custou várias rodadas de correção. Nada aqui está na doc da Zenith.

### `nextAction.instructions` é texto para PROGRAMADOR — nunca exiba cru

A API devolve `instructions.steps` em espanhol e parece copy pronta. Não é. O
passo 2 do CoDi vem assim:

> "Escanea el QR generado con el valor de nextAction.code."

Isso foi parar na tela de uma compradora real. Os passos falam de campos da API,
não do que ela vê. **Escreva os seus.** Se um dia servirem, reescreva — nunca
repasse.

### CoDi não tem copiar e colar

Copiar o payload é reflexo de quem vem do PIX. No CoDi **não existe**: nenhum app
bancário mexicano tem campo para colar código. O `nextAction.code` é um JSON
(`{"TYP":20,"CRY":...,"v":{"DEV":...},"ic":{"SER":...}}`) feito para ser
**codificado em QR**, não digitado. O fluxo é câmera, só.

Onde copiar serve de verdade:

| Método | Copiar? | Por quê |
|---|---|---|
| CoDi | **não** | só câmera; o JSON não vai em campo nenhum |
| SPEI | sim | ela digita a CLABE no app do banco |
| OXXO | sim | ela dita a referência no caixa |
| Valor | sim | em todos: o monto tem que ser exato |

Mostrar o JSON truncado (`{"TYP":20,"CR…`) com um botão Copiar ao lado é ruído
que não serve para nada e ocupa a dobra inteira.

### O QR se desenha no servidor

`qrcode` → data URI pronto, entregue no payload. Carregar uma lib de QR no
cliente é apostar que ela renderiza igual em todo WebView — e esse público chega
pelo navegador embutido do Facebook/Instagram. `errorCorrectionLevel: "M"`,
`margin: 1`, `width: 512`, exibido a 256 com fundo branco e padding: QR precisa
de zona clara em volta, sem ela a câmera não engata.

### `min-width: auto` explode o layout com o payload do CoDi

O JSON tem ~400 caracteres numa `<p>` monoespaçada. Mesmo com `truncate`, a
caixa foi para **6411px** de largura e empurrou a página inteira: item de grid e
de flex nasce com `min-width: auto` e cresce com o conteúdo, ignorando o
`minmax(0,1fr)` da track.

`truncate` no texto não resolve — **quem cresce são os pais**. Ponha `min-w-0`
em cada nível da corrente: coluna → painel do método → caixa do dado. Um só
ancestral sem ele já basta para o defeito voltar.

O sintoma antes disso: a coluna da direita ("Tu pedido") aparecia **por cima**
do conteúdo da esquerda entre ~800 e ~950px de janela. Parecia z-index; era
transbordo.

### Restos de tema escuro

`bg-black/30`, `text-bone`, `text-mist`, `text-gold` sem fundo — em tela clara
viram uma caixa preta com um botão dourado flutuando, que lê como elemento
sobreposto. Confira a paleta do componente contra os cartões vizinhos antes de
culpar o layout.

### Ordem dos métodos e hierarquia visual

CoDi primeiro (digital imediato), depois SPEI, depois OXXO — é o que a própria
doc pede. **Um só destaque:** se CoDi e SPEI ficarem os dois dourados, nenhum
destaca. Com CoDi ligado, SPEI cai para o neutro do OXXO.

### Duas saídas que faltavam, em pastilhas pequenas

- **"Cambiar forma de pago"** — sem isso a primeira escolha era definitiva: quem
  não tem app do banco ficava preso na CLABE sem volta. Não cancele a cobrança
  anterior: o método vai dentro do `referenceId` (`<orden>:codi`), as duas
  coexistem, e se ela pagar a primeira o webhook reconhece.
- **"Ya pagué y no me llegó nada"** — abre o envio de comprovante. O webhook
  pode atrasar; com OXXO ficar pendente por horas é normal, e sem isso ela não
  distingue demora de defeito.

Pequenas e sem cor de ação, de propósito: grandes, empurram para o caminho
manual, que obriga alguém a conferir comprovante à mão.

## Erros que a API devolve e o que significam de verdade

### `422 CUSTOMER_NAME_INVALID`

> "customerName deve conter nome e sobrenome reais. Sequências repetidas,
> iniciais isoladas e dados fictícios não são aceitos."

Dispara com qualquer coisa que cheire a teste — um lead chamado "Ana Ruiz
**Demo**" foi recusado. E-mail com `demo`/`teste` cai no equivalente
`CUSTOMER_EMAIL_INVALID`.

Não é bug e não adianta contornar: a doc avisa que uso repetido de dado
fictício leva a **bloqueio permanente da conta** após análise de conformidade.
Para testar, use uma pessoa real — sem sandbox, é dinheiro de verdade de
qualquer jeito.

### `403 error code: 1010` (não é da Zenith)

Cloudflare recusando o cliente HTTP. `urllib` do Python leva 1010; `curl` passa.
Vale para a API inteira.

### Nunca deixe o método "escorregar"

Bug que escrevi e quase subiu: o ramo do CoDi exigia as chaves da Zenith e, sem
elas, **caía no ramo da XPag** — onde tudo que não é `oxxo` vira `spei`. Quem
pedia QR recebia uma CLABE, cobrada por outro trilho, sem aviso nenhum.

Método indisponível tem que **falhar explícito** e a tela oferecer os outros. Um
gateway a menos é problema; cobrar pelo método errado é outro tamanho de
problema.

### Webhook não alcança `localhost`

Em dev dá para gerar o QR e até pagar, mas o pedido **não vira aprovado**: a
Zenith precisa alcançar o endpoint de fora. A confirmação automática só se
valida no domínio publicado. Planeje o teste sabendo disso.

## 4. Webhook

Diferente da XPag (que não assina nada), aqui o callback **é assinado**. Mas
assinatura prova a origem, não o número dentro: o valor pago vem de
`GET /integrations/checkouts/:id`, e pagamento parcial não aprova.

```
HMAC SHA-256 de: timestamp + "." + corpo CRU
janela: 300s
comparação: timingSafeEqual
libera pedido: só payment.captured e checkout.succeeded
```

O corpo tem que ser o texto exato recebido. Reserializar o JSON muda um espaço,
muda o hash, e **toda venda passa a ser recusada** — em Next.js isso significa
`await request.text()` antes de qualquer `.json()`.

### Registrar o endpoint

```bash
curl -X POST https://api.zenithworld.com.br/integrations/webhooks/endpoints \
  -H "X-API-Key: $ZENITH_PUBLIC_KEY" -H "X-API-Secret: $ZENITH_SECRET_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"...\",\"url\":\"https://SEU_DOMINIO/api/webhook/zenith\",
       \"secret\":\"$ZENITH_WEBHOOK_SECRET\",
       \"events\":[\"payment.captured\",\"checkout.succeeded\",\"payment.failed\",
                   \"payment.refunded\",\"payment.chargeback\"]}"
```

`201` devolve `{"endpoint":{"id":"...","hasSecret":true,"secretLast4":"...",
"isActive":true,"deliveryFailures":0}}`. O secret é **seu**, escolhido por você
— não é emitido pela Zenith.

O endpoint do Número Maestro é `cmtu34l9q027nzmy1y3ijme7a`.

## 5. Env e deploy

```
ZENITH_PUBLIC_KEY=zp_pub_...     # runtime
ZENITH_SECRET_KEY=zp_sec_...     # runtime, NUNCA no cliente
ZENITH_WEBHOOK_SECRET=...        # runtime
NEXT_PUBLIC_ZENITH_CODI=1        # build-time — exige rebuild para mudar
```

No Coolify (`coolify app env create <uuid> --key K --value V`) as duas
disponibilidades vêm ligadas por padrão, que é o certo para as `NEXT_PUBLIC_*`.
`env update` respondeu `422 Validation failed` tanto por chave quanto por uuid —
para corrigir uma variável, apague e recrie.

App do Número Maestro MX: contexto `empresab`, uuid `rdb7cs7wsgj0p2irrwgkpjyv`,
repo `leadgodev/projeto-chavemestra-es`, **branch `mx`** (a `main` é a Argentina).

## Armadilha de automação: o login do painel

O Chromium empacotado do `agent-browser` **não passa** no Turnstile do login:
`Falha no Turnstile (600010)`, três tentativas, com desafio novo entre elas. Não
é senha errada — as credenciais nem chegam a ser testadas, e a mensagem não diz
isso.

Use o perfil persistente do sistema:

```bash
~/.claude/bin/browsers.sh zenith    # porta 9251, sessão já logada
agent-browser --session zenith ...
```

Se `/integracoes-zenith` devolver `Unauthorized`, a sessão caiu — suba o perfil
de novo, não tente relogar pelo browser empacotado.

A API, essa, não tem Turnstile — mas rejeita `urllib` do Python com
`403 error code: 1010` (Cloudflare). Use `curl`.
