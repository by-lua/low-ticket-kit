# Criar o PRIMEIRO conjunto de dados numa BM (e onde mora o aceite de ToS) — business.facebook.com

**Perfil / porta CDP:** `meta` / 9225
**Ferramenta padrao:** agent-browser (CDP no Chromium do SISTEMA; o empacotado trava no Cloudflare)
**Ultima validacao:** 2026-09-04
**Estado:** funciona ate o gate de aceite (o clique final e do dono da conta)

## O que isso resolve (custou uma sessao inteira)

"Va em Configuracoes do Negocio -> Fontes de dados -> Pixels e aceite os Termos
de Servico de Pixel" **nao existe como tela**. Dois motivos:

1. `/settings/pixels` esta DEPRECADA (ver `settings-pixels-tos-empresab.md`).
2. Numa BM com ZERO conjuntos de dados **nao ha banner de ToS nenhum**. O aceite
   so aparece DENTRO do fluxo de criar o primeiro conjunto de dados. Ovo e galinha.

## Pre-condicoes

- perfil no ar: `~/.claude/bin/browsers.sh meta` (`status` deve dizer ATIVA na 9225)
- login ja persistido no perfil; sem Cloudflare, sem 2FA nessa superficie da BM
  `empresab.digital`. **Nao presuma:** a MESMA URL na BM Cosmos cai em reauth por chave
  de acesso (ver `facebook.com/events-manager-criar-dataset.md`).
- `meta` divide a porta 9225 com `utmify` -> `tab new` antes de comecar, e
  `business_id` explicito na URL, senao outro pane arrasta sua pagina.

## Passos

1. `agent-browser --session meta tab new`
2. `agent-browser --session meta goto "https://business.facebook.com/latest/settings/events_dataset/?business_id=<BM_ID>"`
   -> "Conjuntos de dados e pixels"; confira o chip do topo com o nome da BM.
3. Clicar `button "Adicionar"` (o do topo direito; **ha DOIS** com esse nome
   quando a lista esta vazia — o `ref` do topo vem primeiro no snapshot):
   ```bash
   SNAP=$(agent-browser --session meta snapshot 2>/dev/null)
   REF=$(echo "$SNAP" | grep -oE 'button "Adicionar"[^]]*ref=e[0-9]+' | grep -oE 'e[0-9]+$' | head -1)
   agent-browser --session meta click "@$REF"
   ```
   -> `dialog "Criar um conjunto de dados"`.
4. Preencher o nome e (ver armadilha) DESMARCAR o checkbox da API de Conversoes:
   ```bash
   SNAP=$(agent-browser --session meta snapshot 2>/dev/null)
   NOME=$(echo "$SNAP" | grep -oE 'textbox "Nome"[^]]*ref=e[0-9]+' | grep -oE 'e[0-9]+$' | head -1)
   CBX=$(echo "$SNAP" | grep -oE 'checkbox "Adicione a API de Convers[^]]*ref=e[0-9]+' | grep -oE 'e[0-9]+$' | head -1)
   agent-browser --session meta fill "@$NOME" "<NOME EXATO>"
   agent-browser --session meta uncheck "@$CBX"
   ```
5. **PARAR.** O `button "Criar"` carrega o aceite (ver "Onde mora o aceite").
   O clique e do dono da conta.

## Seletores / ancoras estaveis

| Elemento | Ancora | Nota |
|---|---|---|
| abrir fluxo | `button "Adicionar"` | 2 ocorrencias com lista vazia; pegue a 1a |
| nome | `textbox "Nome"` | `Criar` fica `[disabled]` enquanto vazio |
| CAPI BM-wide | `checkbox "Adicione a API de Convers..."` | **`checked=true` de fabrica** |
| ToS da CAPI | `link "Ver termos"` | dentro do label do checkbox |
| ToS geral | `link "Termos das Ferramentas Comerciais da Meta."` | rodape, implicito no `Criar` |
| confirmar | `button "Criar"` | so habilita com nome preenchido |

Refs sao VOLATEIS — `snapshot` e `click` no MESMO comando, sempre.
Cuidado com o regex: a linha e `- checkbox "..." [checked=true, ref=e15]`;
ancorar `$` logo apos `ref=e[0-9]+` NAO casa (tem `]` no fim). Case `[^]]*`
antes e extraia o `e\d+` num segundo `grep -oE`.

## Onde mora o aceite de ToS (a resposta que a gente procurava)

Nao ha modal dedicado "Termos de Servico de Pixel". No dialogo de criacao ha
**dois** consentimentos:

- **Checkbox da API de Conversoes, pre-marcado**, com `Ver termos`.
- **Rodape:** "Ao continuar, voce concorda com os Termos das Ferramentas
  Comerciais da Meta." — anexado ao botao `Criar`, sem checkbox proprio.

Ou seja: **clicar `Criar` E o aceite.** Nao ha como criar o conjunto de dados
sem aceitar. Se a regra do trabalho e "aceite de termos e ato do dono", o agente
para exatamente aqui, com o formulario preenchido, e o dono da o clique.

## Armadilhas

- **O checkbox da CAPI vem `checked=true` e o escopo dele NAO e o dataset novo.**
  Texto literal: "a todos os conjuntos de dados **novos e existentes** com essa
  identificacao do Gerenciador de Negocios". Deixar ligado = mexer em config de
  CAPI da BM INTEIRA, presente e futura, por causa de um dataset de teste.
  **Desmarque** salvo pedido explicito.
- O dialogo **nao pede conta de anuncio** — bom: dataset nasce sem vinculo.
  A oferta de associar conta vem DEPOIS de criar; pule se o objetivo e isolar.
- "Selecione qualquer categoria aplicavel" e opcional; deixar vazio nao bloqueia.
- `Criar` fica `[disabled]` ate o nome existir — `disabled` aqui e falta de nome,
  nao falta de permissao. Nao confunda com bloqueio de acesso.
- Nome com em-dash (—) passa direto pelo `fill`, sem escape.

## Saida

Dataset id: so existe depois do clique em `Criar`. Ler de volta com
`GET /<BM_ID>/adspixels?fields=id,name,owner_business` e conferir
`GET /<DATASET_ID>/shared_accounts` (ou `adaccounts`) VAZIO para provar que
nenhuma conta de anuncio foi vinculada. Nao confie na tela.

## Historico

- 2026-09-04 — mapeado ate o gate de aceite na BM `empresab.digital`
  (`business_id=2099393640970892`), criando `TESTE — NAO USAR EM ANUNCIO`.
  Checkbox de CAPI desmarcado. Parado no `Criar` aguardando a dona.
