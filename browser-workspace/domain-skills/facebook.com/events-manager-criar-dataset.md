# Gerenciador de Eventos — o que a UI dá e o que ela NÃO dá

Tentado em 2026-09-04, perfil `meta` (porta 9225), portfólio Cosmos Astrología
(`business_id=2835296186826870`). **A UI não cede — e não precisa: crie o dataset
pela Marketing API.** Ver `skills/trackeador/references/abrir-mercado-novo.md`
§ "Dataset no Meta — CRIE PELA API". Este doc fica pro que SÓ existe na UI
(lista de permissão de domínios, token da CAPI) e pras armadilhas de automação.

## O gate de 2FA — real, mas contornável por API

Dataset novo, PELA UI, se cria em **Configurações da Empresa → Fontes de dados →
Conjuntos de dados → Adicionar**:

```
https://business.facebook.com/settings/pixels?business_id=<BM_ID>
```

Essa URL redireciona pra `/latest/settings/pixels/` e cai em
**reauth 2FA por chave de acesso** (`/security/twofactor/reauth/`), com o texto
"Confirme que é você com sua chave de acesso". A sessão do perfil `meta`
continua logada pro resto do Business — o gate é só dessa superfície.

Não dá pra passar por automação — a chave de acesso é credencial física do
dono. **Mas não escale por isso:** `POST /{business_id}/adspixels` da Marketing
API cria o dataset sem tocar nessa tela, com o token que o Trackeador já tem
(validado 04/09/2026). Escale só o que SÓ existe aqui: a lista de permissão de
domínios e a geração do token da CAPI.

## O que NÃO funciona (não repita)

`eventsmanager.facebook.com` tem os botões, mas eles não abrem o fluxo:

| Alvo | Resultado |
|---|---|
| `button "Conectar dados"` (nav esquerda) | clique aceito, **URL não muda** |
| `button "Conjuntos de dados"` (nav esquerda) | idem |
| `combobox "Fonte de dados"` | clique aceito, dropdown não expande no DOM |
| `.../events_manager2/list/?business_id=X` | redireciona pro ÚLTIMO dataset aberto, não pra lista |

A nav lateral colapsada é decorativa pra automação — a navegação real é por URL.

## ⚠️ Refs do `snapshot` são VOLÁTEIS — invalidam a cada snapshot

Foi o que fez 3 cliques "✓ Done" não fazerem nada. `agent-browser snapshot`
renumera os refs a cada chamada (`e143` numa, `e158` na seguinte, para o MESMO
botão). Snapshot num comando e clique no comando seguinte = ref podre, e o
clique cai em outro elemento (ou em nada) **sem erro**.

Sempre no MESMO comando:

```bash
SNAP=$(agent-browser --session meta snapshot 2>/dev/null)
REF=$(echo "$SNAP" | grep -oE 'button "Conectar dados"[^]]*ref=e[0-9]+' | grep -oE 'e[0-9]+$')
agent-browser --session meta click "@$REF"
```

Cuidado com o regex: a linha é `- combobox "…" [expanded=false, ref=e24]: …` —
âncora `$` depois de `ref=e[0-9]+` NÃO casa (tem `]:` no fim). Case o `[^]]*`
antes e extraia o `e\d+` num segundo `grep -oE`.

## ⚠️ Perfil `meta` é COMPARTILHADO entre panes — isole em aba

`meta` e `utmify` dividem a porta 9225 (mesma instância de Chromium). Com dois
panes trabalhando, um arrasta a página do outro no meio da operação — aconteceu:
a aba pulou de `EmpresaB N MESTRE`/Cosmos pra `ASTRODICAS AR`/portfólio Lucas Leis
entre dois comandos meus.

**Risco concreto:** criar dataset no portfólio errado (o dataset nasce no
portfólio que estiver no seletor do topo). Já custou caro uma vez.

Isolamento que funciona:

```bash
agent-browser --session meta tab new
agent-browser --session meta goto "<url com business_id pinado>"
agent-browser --session meta tab list   # confirma qual aba é sua
```

`tab new` + `business_id` explícito na URL segurou o contexto em Cosmos
enquanto o outro pane mexia na aba 1.

## Verificação obrigatória depois de criar (não presuma)

Dataset criado → abrir `.../list/dataset/<ID>/settings?business_id=<BM_ID>` e
conferir no `innerText` o bloco **Proprietário**:

```bash
agent-browser --session meta eval "
JSON.stringify((document.body.innerText.match(/Propriet.rio\n([^\n]+)\n(\d+)/)||[]).slice(1,3))"
# esperado: ["Cosmos Astrología","2835296186826870"]
```

Se voltar outro portfólio, o dataset nasceu no lugar errado — some do seletor de
campanha e a campanha trava. Corrigir na hora, não depois.

## Fatos colhidos no caminho (úteis)

- Dataset AR do Número Mestre: **EmpresaB N MESTRE**, ID `2812114902493745`,
  proprietário Cosmos Astrología, criado por Lucas Leis em 02/08/2026.
  O nome **não tem sufixo de mercado** — ao criar o do México, use um nome
  inequívoco (`EmpresaB N MESTRE MX`) e renomeie o AR pra `EmpresaB N MESTRE AR`.
- A aba **Configurações** do dataset tem *Lista de permissão de domínios*:
  "Somente os domínios adicionados à lista de permissão podem enviar eventos".
  Domínio novo (México) precisa entrar lá, senão o pixel carrega e não entrega.
