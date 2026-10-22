# Configurações do Negócio → Pixels: URL deprecada + duas BMs "EmpresaB"

Executado e verificado em 2026-09-04, perfil `meta` (porta 9225), BM `empresab.digital`
(`business_id=2099393640970892`).

## `/settings/pixels` NÃO é mais a tela de pixels

```
https://business.facebook.com/settings/pixels?business_id=<BM_ID>
```
redireciona pra `/latest/settings/pixels/` e mostra só um card de migração:
"Os pixels de <BM> têm uma nova localização" + link **"Ver conjuntos de dados"**.
A tela real é:
```
https://business.facebook.com/latest/settings/events_dataset/?business_id=<BM_ID>
```
Vá direto nessa — pula o card de migração.

**Sem gate de 2FA nessa BM.** (Contrasta com `events-manager-criar-dataset.md`,
onde a mesma URL em Cosmos caiu em reauth por chave de acesso — o gate é por
BM/superfície, não universal. Não presuma nenhum dos dois: teste.)

## ⚠️ "Ver conjuntos de dados" é `link`, não `button`

Grep de `button "Ver conjuntos de dados"` volta vazio e o comando morre com
exit 1. A árvore tem `- link "Ver conjuntos de dados" [ref=e80]`.
Snapshot + click no MESMO comando (refs são voláteis):

```bash
SNAP=$(agent-browser --session meta snapshot 2>/dev/null)
REF=$(echo "$SNAP" | grep -oE 'link "Ver conjuntos de dados"[^]]*ref=e[0-9]+' | grep -oE 'e[0-9]+$' | head -1)
agent-browser --session meta click "@$REF"
```

## ⚠️ DUAS BMs com nome quase igual — escolher errada estraga o passo

`https://business.facebook.com/select/` lista os portfólios sem clicar em nada
(NÃO clique num item: trocar o portfólio ativo arrasta o contexto de outros panes):

| Nome exibido | Perfil |
|---|---|
| **`empresab.digital`** (minúscula, com ponto) | 1 conta de anúncios · 1 Página · 3 pessoas — **é a viva**, `business_id=2099393640970892` |
| `EmpresaB Digital` (capitalizada, com espaço) | 0 contas de anúncios · 0 Páginas · 1 pessoa — casca |

Outras homônimas no mesmo seletor: `EmpresaB - Bm Bdm -One Stream`,
`EmpresaB - Clubinho Kids`, `EmpresaB W OFF - Daiane Lima...`.
Confira sempre o chip do topo (`empresab.digital / Portfólio empresarial`) antes de agir.

## Estado achado: `empresab.digital` tem ZERO conjuntos de dados

"Nenhum conjunto de dados adicionado". Como não há pixel na BM, **não existe
banner de Termos de Serviço de Pixel pra aceitar nessa tela** — grep de
`termo|aceit|contrat` no `innerText` volta vazio. O ToS provavelmente só aparece
depois de "+ Adicionar" (criar/compartilhar dataset). Não criar dataset por conta
própria: nasce no portfólio do seletor e já custou caro uma vez.

## `tab close` / `tab select` exigem id `tN`, não inteiro

`agent-browser --session meta tab close 4` → `✗ ... positional integers are not
accepted`. Use `tab close t4`, `tab select t3`. `tab select` por LABEL falha se
a aba já foi fechada — liste com `tab list` (a seta `→` marca a ativa).
