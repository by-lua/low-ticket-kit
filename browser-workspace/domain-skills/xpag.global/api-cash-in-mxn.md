# XPag — API de cash-in MXN (SPEI + OXXO)

Verificado em 2026-09-04 contra `https://api.xpag.net` com as credenciais de sandbox.
Perfil de browser: `xpag` (porta 9245). Docs em `https://xpag.global/pt/docs/`
(o `xpag.net/docs/` redireciona pra lá). Não existe `llms.txt`.

## Autenticação
Headers `X-Client-Id` / `X-Client-Secret`. Cash-in NÃO exige IP na allowlist
(só o cash-out exige). Sandbox tem credencial pública documentada:
`xpagsandbox_00000000` / `202620262026202620262026`.

## Cobrança SPEI (funciona no sandbox)
`POST /cashin` com `{"currency":"MXN","amount":199,"external_id":"...","webhook_url":"..."}`
→ devolve `clabe` (18 díg.), `bank_name`, `beneficiary`, `transaction_id`,
`request_number`, `e2e`, `fee`, `expire_minutes: 30`.

Com `amount` = CLABE dinâmica daquele pagamento. **Sem** `amount` = CLABE de
valor aberto (a pessoa transfere qualquer valor) — não usar em venda.

## ARMADILHA: o sandbox ignora `method: "OXXO"`
Mandar `{"currency":"MXN","method":"OXXO","generateCheckout":false,...}` no
sandbox devolve **uma CLABE de SPEI**, sem `payee_data` e sem `barcode`.
O trilho OXXO não é testável em sandbox — a primeira validação tem que ser
com credencial de produção e dinheiro real. Faixa OXXO: 10 a 10.000 MXN,
valor exato.

## ARMADILHA: o webhook NÃO é assinado
Não há HMAC, nem header de assinatura, nem segredo no protocolo. O payload
confirmado é:
```json
{"type":"cashin","origin":"dynamic","status":"confirmed","amount":199,"fee":14.95,
 "currency":"MXN","request_number":"sbx_...","transaction_id":"SBX-...",
 "external_id":"PEDIDO-1","e2e":"E...","provider":"XPag"}
```
Qualquer um que descubra a URL forja isso. **Nunca liberar produto a partir do
corpo do POST.** Tratar como aviso e reconsultar:
`GET /consult-transaction?transaction_id=...` (aceita também `external_id`,
`e2e`, `request_number`; por `external_id`/`clabe` pode voltar LISTA em
`payments[]`). Conferir também o `amount` contra o valor do pedido.

## Taxa
199 MXN → `fee` 14,95 (≈7,5%). Entra no cálculo de margem.

## Loop de teste no sandbox (validado ponta a ponta)
1. `POST /cashin` → guarda `transaction_id`
2. `GET /consult-transaction?transaction_id=...` → `pending`
3. `POST /sandbox/simulate {"transaction_id":"...","outcome":"paid"}` → dispara
   o webhook de verdade e devolve o payload + `http_status` da entrega
4. `GET /consult-transaction` → `confirmed`

`outcome` aceita `paid` · `failed` · `expired`.

## Erros
JSON `{"ok":false,"error":"...","error_code":"..."}` + header `X-App-Error-Code`.
Tratar por `error_code`, nunca pela mensagem. Retentáveis (com o MESMO
`external_id`): `provider_unavailable`, `rate_limited`. Todo o resto é
definitivo.

Usado em: NUMERO-MESTRE/app (`src/lib/xpag.ts`, `src/app/api/webhook/xpag/route.ts`).
