---
name: mundpay
description: Cadastra produto digital na Mundpay (login.mundpay.com) pelo painel logado - criar produto/oferta em BRL, USD ou EUR (ex.: euro de Portugal), pegar o link do checkout, ver o status de análise, e entregar pela nossa área de membros. Regra fixa: toda oferta aceita só pagamento na hora (tabela de métodos por país). Use quando o usuário pedir para criar produto na Mundpay, checkout Mundpay, vender em euro/Portugal/Europa, ou mencionar Mundpay, mycheckoutt, gateway card-first.
---

# Mundpay — produto digital + checkout

> **Regra fixa da dona (05/10/2026): toda oferta (principal, bump, popup, upsell) aceita SÓ pagamento na hora** (cartão, Apple Pay, Pix e transferência/carteira instantânea local). Boleto, OXXO, dinheiro em loja, voucher, Efecty, Rapipago, "Otros" etc. ficam DESMARCADOS. Tabela por país na seção "Tabela de métodos".
> **Regra fixa da dona (07/10/2026): PicPay e Google Pay SEMPRE DESMARCADOS**, em toda oferta, todo país — nunca deixar ativos, mesmo sendo "principal"/instantâneo.
> **Regra fixa (08/10/2026): todo checkout leva banner no idioma da oferta** (PT = pt-PT, ES = espanhol neutro) **+ contador de 15 minutos (00h15), cor de fundo vermelha `#F14254`** (aba Checkouts → Personalizar → Urgência). **Mensagem de exibição no idioma da oferta:** “Oferta por tempo limitado! Garanta o seu agora antes que o preço suba.” Traduzir/adaptar essa mensagem ao idioma da oferta. Ver skill `banner-checkout-gpt`.

> **REGRA FIXA DA DONA (16/10/2026) — TODO produto/oferta criado entra nos DOIS webhooks NO MESMO DIA.** Vale pra toda peça: principal · **order bump** · combo · upsell/downsell · **upgrade Essencial → Completo** · produto irmão/cross · oferta de membro. Cada produto novo, na MESMA sessão do cadastro, marcado em (1) **webhook de ENTREGA** (`<site>/painel/api/webhooks/mundpay`) e (2) **webhook de MEDIÇÃO** (Trackeador, `https://adstrackeador.leadgo.dev/api/webhooks/sale/c/<conexão>`) — "todos os produtos" OFF. Produto fora do webhook = a venda some do Trackeador/atribuição e/ou o comprador fica sem acesso, **sem erro em lugar nenhum**. Padrão/incidente (order bump "Combo Domínio Total", Jiu-Jitsu, 16/10): `wiven-checkout` §6.

Painel: `https://login.mundpay.com` · perfil browser **`mundpay` porta 9270** (sessão persistente, já logada; credenciais `$MUNDPAY_EMAIL`/`$MUNDPAY_PASSWORD` em `~/.claude/.credentials.env`, nunca imprimir nem literal; só pra relogar se o 9270 cair no login — perfil já logado é o único que se usa).
```bash
~/.claude/bin/browsers.sh mundpay          # sobe o perfil se estiver parado
agent-browser --session mundpay open "https://login.mundpay.com/products"
```
Nunca `agent-browser open` sem `--session`. Leia antes `~/.claude/browser-workspace/domain-skills/login.mundpay.com/criar-produto-digital.md`.

## Quando usar
Gateway **card-first**: serve Europa (PT/FR/…) onde cartão resolve; Latam tem métodos locais (lista abaixo), mas BR forte continua Zenith/XPag/Wiven. Verificar cobertura antes de migrar oferta de outro gateway.

## REGRA: 1 produto só por mercado, o resto é OFERTA dentro dele (dona 28/09/2026)
Na Mundpay cria **só o produto principal** (ex.: "Mapa do Tarot - PT"). Todo o resto nasce **dentro dele**:
planos (Essencial/Completo), oferta de popup/down-sell, **order bumps e combo** = abas **Ofertas** e
**Order Bumps** do mesmo produto. **Nunca** criar produto novo pra plano, bump ou combo.
**Exceção — order bump:** a aba Order Bumps só aceita OUTRO produto. Então cria **um** produto "Extras <oferta> - PT" com uma oferta por bump + combo, e cada bump do produto principal aponta pra uma oferta dele. Nunca um produto por bump.
**Why:** cada produto novo entra "Em análise" e a Mundpay demora muito pra aprovar (até 24h úteis ou mais);
oferta/bump dentro do produto já aprovado não passa por nova análise.
Nomes com sufixo do mercado (" - PT", " - ES").

## Regras da oferta (memória do projeto low ticket)
Reembolso = **mínimo** (7 dias). Suporte: **support@seudominio.com** + WhatsApp **<seu-whatsapp>**. Página de vendas = URL REAL da oferta (nunca inventar domínio). Entrega = **nossa área de membros**, nunca a do gateway. Idioma do texto (nome/oferta/descrição) conforme o mercado (ex.: português de Portugal) — a Mundpay não tem campo de idioma, só moeda.

## Criar produto — wizard de 6 passos (`/products/create-products`)
1. **Produto digital**.
2. Nome, nome da oferta (aparece "Produto – Oferta" no checkout), Categoria (ex.: E-books), Descrição ≥ 40 chars, Reembolso (mín. 7), **Página de vendas COM `https://`** (sem o esquema dá "deve ser uma URL válida" e o erro só aparece aqui, o passo 6 diz apenas "1 erro(s)"), URL de agradecimento (opcional; usamos a nossa área).
3. Email + WhatsApp de suporte (+55 default).
4. **Código de 4 dígitos enviado por email ao suporte** — precisa do humano; pedir o código.
5. Tipo **Único** + moeda (**BRL/USD/EUR**) + valor; a máscara aceita dígitos: digitar `990` = 9,90.
6. Entrega **Integração Externa**: link da nossa área + e-mail de teste PADRÃO `teste@seudominio.com` (tudo liberado, igual em todo projeto) + senha de apoio para análise (senha obrigatória, ≥ ~10 caracteres; nosso painel entra só por email, então a senha é texto de apoio). **Finalizar.**
Produto nasce **"Em análise"** (toggle "Ativar para venda" só após aprovação).

## Checkout
`/products/edit-product/<uuid>/checkouts` já vem com 1 checkout ativo por oferta; link no formato `https://pay.mycheckoutt.com/<uuid>?ref=`. Abas do produto: Geral, Ofertas, Checkouts, Links, Pixels, Co-produtor, Afiliado, Parceiros, **Order Bumps**, **Upsells**.

## Editar oferta e formas de pagamento (colado do painel, 2026-09-28)
Aba Ofertas → Editar oferta: **Ativar oferta**, Nome (ex.: "Acesso vitalício"), Tipo de pagamento (**Único**), Valor + moeda (ex.: € 9,90 EUR), **Métodos de PGTO.** (contador X/64 + "Selecionar todos").
- **Principais (4, mas ver regra PicPay/Google Pay sempre desmarcado abaixo):** Cartão de Crédito, Pix, Apple Pay, Google Pay.
- **Alternativos (X/60, com busca por país):**
  - Argentina 5: Rapipago, Mercado Pago, MODO, Khipu, Otros Bancos/Billeteras
  - Brasil 2: Boleto Bancário, PicPay
  - Chile 9: Khipu, Mach, Banco de Chile, Banco Estado, Banco Falabella, Banco Santander, BCI, Fintoc, ServiPag
  - Colômbia 3: PSE, Nequi PSE, Efecty
  - Costa Rica 1: Banco Nacional
  - Equador 7: Banco Guayaquil, Banco Pichincha, Pichincha Mi Vecino, Red Activa, Mi Comisariato
  - México 17: SPEI, OXXO, Scotiabank, BBVA Bancomer, Bodega Aurrera, 7 Eleven, Circle K, Farmacias del Dr. Ahorro, Sam's Club, Superama, Banco Azteca, Soriana, Farmacias Santa Maria, Calimax, OpenPay
  - Peru 19: Banco de Crédito, Interbank, Khipu, Scotiabank, BBVA Continental, Caja Arequipa/Huancayo/Tacna/Trujillo, Ripley, Western Union, Kasnet
- Cobertura é **Latam + cartão/carteiras**; **não há método local europeu** (sem SEPA, Multibanco, MB Way, iDEAL, Bancontact). Em EUR/Portugal a venda depende de cartão + Apple Pay (Google Pay nunca).
- Exemplo do estado colado: 8/64 marcados (4 principais + 4 alternativos: Brasil 2, Chile 1, México 1).
- **Moedas:** principais = **EUR, USD, BRL**. Segundo o Lua, o checkout converte para a moeda do comprador (informado por ele, **não verificado** no checkout: conferir taxa/IOF e o valor final cobrado antes de prometer preço em moeda local).
- **API:** nenhuma documentação de API/webhook foi fornecida ainda; só o painel foi validado. Não presumir endpoints.

### Tabela de métodos: só pagamento na hora (regra fixa, dona 05/10/2026)
Método no painel: deixar tudo marcado e DESMARCAR só o que não cai na hora, país por país. Fonte de classificação: oferta Básico - ES (`OFERTAS/mapa-do-tarot/site/es/CHECKOUT-MUNDPAY-ES.md`). Método sem certeza de ser instantâneo: DESMARCAR e marcar **(dúvida)**.

**Principais: MANTER** Cartão de Crédito, Pix, Apple Pay. **DESMARCAR SEMPRE** Google Pay e PicPay (regra fixa dona 07/10/2026, todo país, mesmo sendo "principal"/instantâneo).

| País | MANTER | DESMARCAR |
|---|---|---|
| **AR** Argentina | Mercado Pago, MODO, Khipu | Rapipago, Otros Bancos/Billeteras |
| **BR** Brasil | — | Boleto Bancário, PicPay |
| **CL** Chile | Khipu, Mach, Banco de Chile, Banco Estado, Banco Falabella, Banco Santander, BCI, Fintoc | ServiPag |
| **CO** Colômbia | PSE, Nequi PSE | Efecty |
| **CR** Costa Rica | Banco Nacional | — |
| **EC** Equador | Banco Guayaquil, Banco Pichincha | Pichincha Mi Vecino, Red Activa, Mi Comisariato |
| **MX** México | SPEI, Scotiabank, BBVA Bancomer (dúvida) | OXXO, Bodega Aurrera, 7 Eleven, Circle K, Farmacias del Dr. Ahorro, Sam's Club, Superama, Soriana, Farmacias Santa Maria, Calimax, Banco Azteca (dúvida), OpenPay (dúvida) |
| **PE** Peru | Banco de Crédito, Interbank, Khipu, Scotiabank, BBVA Continental | Caja Arequipa, Caja Huancayo, Caja Tacna, Caja Trujillo, Ripley, Western Union, Kasnet |

Nota: outros países da lista do seletor (sem método local) = só principais (cartão, Apple Pay; Pix só BR). Google Pay e PicPay nunca, em nenhum país. Nada além disso.

**Checklist ao criar/editar oferta (passo obrigatório):**
1. Marcar os principais (Cartão, Pix, Apple Pay); **desmarcar Google Pay e PicPay sempre**.
2. Abrir Métodos de PGTO, **desmarcar métodos não instantâneos (tabela acima)**; dúvida = desmarcado.
3. Conferir o contador e registrar no status o que ficou marcado.
4. Aba Checkouts → "⋮" na linha do checkout → **Personalizar** → **banner no idioma da oferta** (PT=pt-PT, ES=espanhol neutro, ver skill `banner-checkout-gpt`) + **contador de 15 minutos (HH=00, MM=15), fundo `#F14254` e mensagem de exibição no idioma da oferta**: “Oferta por tempo limitado! Garanta o seu agora antes que o preço suba.” Traduzir/adaptar ao idioma da oferta.
5. **Releia o painel depois de salvar** (reabrir a oferta/checkout) — não confiar só no toast de sucesso.

### Onde cada coisa se configura — mapa das 3 telas (07/10/2026)
São **3 telas diferentes**, não confundir:
- **Aba Ofertas → Editar oferta**: Métodos de PGTO. completo (principais + alternativos por país, a tabela desta skill). Aqui é onde PicPay/Google Pay e a tabela de países se aplicam.
- **Aba Checkouts → "⋮" → Personalizar → aba Urgência**: cronômetro (switch, horas, **minutos** — são 2 comboboxes HH e MM, nessa ordem; **15 min = deixar HH=00, MM=15**) + **cor de fundo `#F14254`** + mensagem de exibição **no idioma da oferta**: “Oferta por tempo limitado! Garanta o seu agora antes que o preço suba.” Traduzir/adaptar ao idioma da oferta.
- **Aba Checkouts → "⋮" → Personalizar → abas Banners Desktop / Banners Mobile**: upload do banner (switch "Banner superior" liga primeiro, só depois aparece o campo de arquivo). Desktop recomenda 1032×264px (tira larga), Mobile 343×120px (tira fina) — nosso banner 16:9/1:1 entra redimensionado e funciona, mas não é o formato nativo do slot.
- **Aba Checkouts → "⋮" → Personalizar → aba Pagamentos**: isso é só o **método padrão pré-selecionado** no checkout (qual ícone já vem marcado pro cliente), não duplica a lista de métodos habilitados — não precisa mexer aqui depois do passo 1-2.
- **1 checkout por oferta**, nasce junto quando a oferta é criada; **Personalizar** cobre cada checkout individualmente (não existe personalização em lote).

### Mecânica de browser do Personalizar (verificado 07/10/2026, flaky — ler antes de automatizar)
- O **seletor de cor** é uma caixa de saturação arrastável (não um `<input type=color>` nem Radix select): dirigir por `PointerEvent`/`MouseEvent` (`pointerdown`→`pointermove`→`pointerup` em sequência, com `sleep` entre cada um) **direto na caixa de saturação e na barra de matiz** (classes `[class*=saturation]`, barra de matiz é o 13º `<div>` descendente — `querySelectorAll('div')[12]`). **Digitar no campo hex (`input[name="hex"]`) NÃO comita** o valor pro estado React mesmo com `input`/`change`/`blur` disparados — only o arraste funciona. A cor de fundo exigida é **`#F14254`**: ajustar matiz/saturação até obter esse hex e conferir o valor persistido ao reabrir. Não substituir por um vermelho aproximado; se o controle impedir a configuração exata, informar a limitação.
- O **combobox de minutos do cronômetro** é um Radix select comum (`[role=combobox]` dentro do `[role=tabpanel]`, 2 instâncias: índice 0 = horas, índice 1 = minutos) — dirigir com a mesma técnica de PointerEvent da Wiven/Mundpay (não `agent-browser click`, que falha silenciosamente nesses).
- O **botão "⋮"** de cada linha (oferta/checkout) é um ícone SVG `lucide-ellipsis`, não um `<button>` de verdade — clicar com `elementFromPoint` + dispatch de PointerEvent, não ref direto.
- **"Salvar oferta"/"Salvar"**: `agent-browser click @ref` e `dispatchEvent` sintético falham silenciosamente às vezes (o modal fecha mas nada foi persistido — sem toast de erro, sem request de rede). O que funciona de forma confiável é `button.click()` nativo via `eval` **pegando o botão fresco na hora** (nunca reusar uma referência de uma chamada eval anterior).
- **A tela inteira ("Personalizar checkout") trava num spinner global** de vez em quando (10-40s), não só a tabela — não é bug do nosso script; espere e tire screenshot antes de concluir falha. Recarregar `/checkouts` ou navegar pra `/dashboard` e voltar destrava.
- Depois de qualquer upload de banner, **o campo "Escolher arquivo" continua mostrando "Nenhum arquivo escolhido"** mesmo com o arquivo certo carregado — o preview do celular/desktop à direita é a prova real, não o texto do campo.

## Países do checkout (lido em 2026-09-28)
Fonte: seletor de país do checkout público `pay.mycheckoutt.com/<uuid>` (abrir combobox Radix por PointerEvent, ler `[role=option]`, fechar a aba depois). **250 entradas** (inclui territórios e "European Union"), padrão Brasil.
- **Moeda local (converte pra moeda do comprador, além de cartão): só os países da lista de métodos alternativos acima** (AR, BR, CL, CO, CR, EC, MX, PE), segundo o Lua. **Todo o resto = só cartão** (mais Apple Pay; Google Pay nunca).
- Cuidado: a lista inclui países sancionados (Cuba, Irã, Coreia do Norte, Síria, Rússia, Belarus); estar no seletor **não garante** que a Mundpay aprove a venda. Não prometer cobertura sem teste.
- Lista completa: Afghanistan; Albania; Algeria; American Samoa; Andorra; Angola; Anguilla; Antarctica; Antigua And Barbuda; Argentina; Armenia; Aruba; Ascension Island; Australia; Austria; Azerbaijan; Bahamas; Bahrain; Bangladesh; Barbados; Belarus; Belgium; Belize; Benin; Bermuda; Bhutan; Bolivia, Plurinational State Of; Bonaire, Sint Eustatius And Saba; Bosnia & Herzegovina; Botswana; Brazil; British Indian Ocean Territory; Brunei Darussalam; Bulgaria; Burkina Faso; Burundi; Cabo Verde; Cambodia; Cameroon; Canada; Cayman Islands; Central African Republic; Chad; Chile; China; Christmas Island; Cocos (Keeling) Islands; Colombia; Comoros; Cook Islands; Costa Rica; Croatia; Cuba; Curacao; Cyprus; Czech Republic; Côte d'Ivoire; Democratic Republic Of Congo; Denmark; Djibouti; Dominica; Dominican Republic; Ecuador; Egypt; El Salvador; Equatorial Guinea; Eritrea; Estonia; Eswatini; Ethiopia; European Union; Falkland Islands; Faroe Islands; Fiji; Finland; France; French Guiana; French Polynesia; Gabon; Gambia; Georgia; Germany; Ghana; Gibraltar; Greece; Greenland; Grenada; Guadeloupe; Guam; Guatemala; Guernsey; Guinea; Guinea-bissau; Guyana; Haiti; Honduras; Hong Kong; Hungary; Iceland; India; Indonesia; Iran, Islamic Republic Of; Iraq; Ireland; Isle Of Man; Israel; Italy; Jamaica; Japan; Jersey; Jordan; Kazakhstan; Kenya; Kiribati; Korea, Democratic People's Republic Of; Korea, Republic Of; Kosovo; Kuwait; Kyrgyzstan; Lao People's Democratic Republic; Latvia; Lebanon; Lesotho; Liberia; Libya; Liechtenstein; Lithuania; Luxembourg; Macao; Madagascar; Malawi; Malaysia; Maldives; Mali; Malta; Marshall Islands; Martinique; Mauritania; Mauritius; Mayotte; Mexico; Micronesia, Federated States Of; Moldova; Monaco; Mongolia; Montenegro; Montserrat; Morocco; Mozambique; Myanmar; Namibia; Nauru; Nepal; Netherlands; New Caledonia; New Zealand; Nicaragua; Niger; Nigeria; Niue; Norfolk Island; North Macedonia; Northern Mariana Islands; Norway; Oman; Pakistan; Palau; Palestinian Territory, Occupied; Panama; Papua New Guinea; Paraguay; Peru; Philippines; Pitcairn; Poland; Portugal; Puerto Rico; Qatar; Republic Of Congo; Reunion; Romania; Russia; Rwanda; Saint Barthélemy; Saint Helena, Ascension And Tristan Da Cunha; Saint Kitts And Nevis; Saint Lucia; Saint Martin; Saint Pierre And Miquelon; Saint Vincent And The Grenadines; Samoa; San Marino; Sao Tome and Principe; Saudi Arabia; Senegal; Serbia; Seychelles; Sierra Leone; Singapore; Sint Maarten; Slovakia; Slovenia; Solomon Islands; Somalia; South Africa; South Georgia And The South Sandwich Islands; South Sudan; Spain; Sri Lanka; Sudan; Suriname; Svalbard And Jan Mayen; Sweden; Switzerland; Syrian Arab Republic; Taiwan; Tajikistan; Tanzania, United Republic Of; Thailand; Timor-Leste, Democratic Republic of; Togo; Tokelau; Tonga; Trinidad And Tobago; Tristan de Cunha; Tunisia; Turkey; Turkmenistan; Turks And Caicos Islands; Tuvalu; Uganda; Ukraine; United Arab Emirates; United Kingdom; United States; United States Minor Outlying Islands; Uruguay; Uzbekistan; Vanuatu; Vatican City State; Venezuela, Bolivarian Republic Of; VietNam; Virgin Islands (British); Virgin Islands (US); Wallis And Futuna; Western Sahara; Yemen; Zambia; Zimbabwe; Åland Islands.

## Mecânica de browser
Selects = componentes Radix: dirigir por eval com `PointerEvent('pointerdown'/'pointerup')` + `.click()` no trigger e depois na `[role=option]` pelo texto exato (mesma técnica da Wiven). Conferir o valor lido depois de cada passo. Screenshot só pra confirmar visual.

## Webhook Genérico (verificado 29/09/2026)
Rota: `/integrations/configurations` → Webhook Genérico → Conectar integração.
Campos: título, URL de postback, produto, eventos e formas de pagamento. Para
venda/CAPI, marcar **Pago**, **Reembolsado** e **Chargeback**; Aguardando
pagamento é opcional. O painel aceita query string na URL, então o
AdsTrackeador usa `/api/webhooks/sale/c/<id>?token=<secret>` (nunca registrar o
valor do token em transcript/docs).

Payload oficial: `{event,data:{transaction_id,status,amount,currency,
payment_method,customer,product,tracking,created_at}}`; `amount` em centavos.
O botão **Testar** do painel enviou também um shape achatado
`{id,event_type,status,amount,currency,customer,offers}`. O preset Mundpay do
Trackeador aceita os dois. Idempotência: `transaction_id`/`id`.

Segurança: a Central oficial menciona HMAC-SHA256 no header
`X-Mundpay-Signature`, mas não informa como obter a chave nem o manifest
assinado, e o formulário atual não exibe chave. Não inventar validação HMAC;
usar o token aleatório da URL até a especificação completa existir.

Tracking: o bundle do checkout lê `utm_source`, `utm_medium`, `utm_campaign`,
`utm_content`, `utm_term`, `src` e qualquer parâmetro extra, colocando-os no
objeto `tracking`. Ele exclui explicitamente `ref`, `mund_lang`, `mndpay` e
`uh`. Portanto passe o tracking id em **`_tkid`**, nunca em `ref`.

Order bump/upsell na Mundpay continua não testado com venda real.

## Estado conhecido (2026-09-25)
Conta LeadGo/Dona. Produto "Mapa do Tarot" € 9,90 criado, **em análise**. Dois produtos antigos "La chave mestra" aparecem **Bloqueado** (causa desconhecida — checar suporte se afetar aprovação).

## Aprovação Mundpay: o que a página de vendas TEM que ter (pendência real 2026-09-25, Mapa do Tarot)
A Mundpay reprova ("Falta pouco para aprovar") se faltar qualquer item; retorno em até 24h úteis após salvar. Checklist antes de enviar para análise:
1. **Produto claro**: a página diz exatamente o que o cliente compra (formato, conteúdo, entrega).
2. **Rodapé completo**: identificação do responsável (Razão Social + CNPJ, ou Nome + CPF), Termos de Uso, Política de Privacidade, canal de suporte (email + WhatsApp). Nosso padrão: 49.265.147 DONA DE LIMA ASSIS, CNPJ 49.265.147/0001-00, support@seudominio.com, WhatsApp <seu-whatsapp>. Termos/Privacidade = páginas reais no mesmo domínio (`/termos`, `/privacidade`).
3. **Domínio próprio** (não subdomínio de plataforma alheia).
4. **Todos os botões de compra = checkout OFICIAL Mundpay** `https://pay.mycheckoutt.com/<uuid>?ref=` (uuid em `/products/edit-product/<produto>/checkouts`). Link Hotmart/Wiven/GG na página = reprovação ("link de checkout não direciona para o checkout da Mundpay"). Conferir com curl: zero hotmart/wiven, todos os botões no mesmo link.
5. **Campo "Página de vendas" do produto** = URL real publicada, com `https://`.
6. **Acesso de análise**: painel/área de membros no ar + usuário teste PADRÃO `teste@seudominio.com` (senha de apoio ≥10 caracteres) cadastrado em Entrega → Integração Externa, para o analista testar sem comprar.
7. Idioma da página conforme mercado (ex.: `/pt` em português neutro, `lang="pt"`); sem prova social inventada.
Verificar sempre a página AO VIVO (curl) depois do deploy: o auto-relato do worker não basta.
Suporte para dúvida: risco@mundpay.com; produtor: help@mundpay.com.

### Receita executada (Mapa do Tarot)
Página = `OFERTAS/mapa-do-tarot/site/` (cópia de `pagina-clone`, original intacta), rota `/pt`, `termos.html`, `privacidade.html`, `/painel` (+ `/pt/painel`). Publicada em https://mapadotarot.leadgo.dev/pt. Checkout Mundpay uuid 01a0d98a-e909-7239-b459-75d58aff0365.

### Termos e Privacidade (exigidos no rodapé)
Páginas reais e completas, mesmo domínio, rotas limpas `/termos` e `/privacidade` (e `/pt/termos`, `/pt/privacidade`), linkadas no rodapé de todas as versões. Duas linhas não bastam (1,4 KB foi raso). Termos: produto digital e entrega, preço, reembolso 7 dias, licença pessoal, limite de responsabilidade, foro, contato. Privacidade: dados coletados (email; pagamento tratado pela Mundpay), finalidade, cookies/pixels (só citar o que a página realmente usa), compartilhamento, retenção, direitos do titular (LGPD), contato. Ambas com Razão Social + CNPJ + suporte. Conferir 200 com curl.

### Resultado real (Mapa do Tarot, 2026-09-25) — ao vivo, verificado por curl
- Página de vendas: https://mapadotarot.leadgo.dev/pt (campo "Página de vendas" da Mundpay). Todos os botões = `pay.mycheckoutt.com/01a0d98a-e909-7239-b459-75d58aff0365?ref=`.
- Termos/Privacidade completas em `/termos`, `/privacidade`, `/pt/termos`, `/pt/privacidade` (200, ~4,7/5,3 KB).
- Acesso de análise: https://mapadotarot.leadgo.dev/pt/painel, login demo `teste@seudominio.com` (senha demo salva na Mundpay em Entrega; login testado por API: certa=200, errada=401). Usuário demo no `server/index.mjs` (`DEMO_USERS`, hash), acesso completo sem compra.
- Armadilha: deploy no Coolify demora; curl logo após publicar pode ver a versão antiga (parecia 404/tamanho antigo). Rechecar com `cache-control: no-cache` e `?x=$RANDOM` antes de concluir que falhou.
