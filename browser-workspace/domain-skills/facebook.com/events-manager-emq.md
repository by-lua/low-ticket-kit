# Gerenciador de Eventos — ler EMQ e cobertura de parâmetros de um dataset

Executado e verificado em 2026-09-04, perfil `meta` (porta 9225).

## Acesso
Perfil `meta` está logado no Business (`~/.claude/bin/browsers.sh meta`).
`business.facebook.com/events_manager2/...` REDIRECIONA pra
`eventsmanager.facebook.com/...` — normal, não é erro.

```bash
agent-browser --session meta goto \
  "https://business.facebook.com/events_manager2/list/dataset/<PIXEL_ID>/overview"
sleep 12
```

⚠️ `browsers.sh status` lista `meta` e `utmify` na MESMA porta 9225. Subir um
derruba o outro — confira o `status` depois de subir.

## O que dá pra ler SEM clicar em nada (é o caminho rápido)

A tabela de eventos inteira sai em `innerText`, incluindo a nota de EMQ:

```bash
agent-browser --session meta eval "
(function(){
  var l = document.body.innerText.split('\n').map(s=>s.trim()).filter(Boolean);
  var i = l.lastIndexOf('Compra');           // ou 'PageView', 'Lead', ...
  return JSON.stringify(l.slice(i, i+10));
})()"
# -> ["Compra","Ativo","6 conjuntos de anúncios","Várias","​","7.3/10","379",...]
```

Ordem das colunas: nome, status, usado por, **integração**, ​, **EMQ**, total, recência.

`Integração: "Várias"` = MAIS DE UMA integração manda esse evento (Pixel do
browser **e** Conversions API). Pra um `Purchase` isso é o sinal de risco de
dupla contagem — o número de dedup em si fica na aba "Desduplicação de evento"
do drill-down (ver armadilha abaixo).

Também sai de graça no `innerText` da Visão geral:
- `$X investimento em publicidade afetado por baixa qualidade dos dados`
- as "Principais ações" (ex.: "Envie mais parâmetros para aumentar a qualidade
  da correspondência — Alta prioridade")
- a janela de datas vigente ("7 de ago de 2026 a 3 de set de 2026") — **confira
  sempre**, é ela que define se você está lendo o ANTES ou o DEPOIS.

## Cobertura por parâmetro (Email/IP/UA/fbp/external_id/Nome/Sobrenome/fbc)

O que ABRE o painel é **clicar na nota azul de EMQ** ("7.3/10") por
COORDENADA. Nada de seletor.

```bash
agent-browser --session meta screenshot /tmp/tabela.png   # leia a imagem, pegue x,y da nota
```
```python
# browser-harness, BU_CDP_URL=http://127.0.0.1:9225
click_at_xy(921, 643)          # a nota azul da linha desejada
time.sleep(10)
js("""(() => [...document.querySelectorAll('[role=dialog]')]
     .map(x=>x.innerText||'').filter(t=>/Medidor de cobertura/.test(t)))()""")
```
Devolve `<parâmetro> / Convertido em hash|Não convertido / NN% do total de
eventos`, mais a lista "Outros parâmetros" que o Meta recomenda enviar.

Pra saber DE QUAL evento é o painel: procure o nome no texto
("...enviaram Telefone válidas para **Purchase**..."). O painel não tem título
com o nome do evento em `innerText`.

## ⚠️ Armadilhas (custaram ~8 tentativas)

- **Clicar no NOME do evento não abre nada.** Nem por texto, nem por
  coordenada, nem subindo 0-7 níveis de `parentElement`. Só a nota de EMQ abre.
- **A tabela não usa `role=row`/`<tr>`** e os nomes de evento não são `<a>`
  nem `[role=button]` — busca por seletor semântico volta `[]`.
- **O botão "Começar" do card de ações abre o painel do evento de MAIOR
  prioridade** (no caso, `Lead`), não do que você quer. Fácil confundir os dois
  painéis: só os percentuais mudam.
- **"Ver todas as ações (3)" abre um `[role=dialog]`** que NÃO aparece em
  `document.body.innerText` — tem que consultar
  `document.querySelectorAll('[role=dialog]')` direto.
- **NÃO RESOLVIDO:** a aba "Desduplicação de evento" do drill-down do evento.
  Ela existe (aparece na lista de abas do painel do `Lead`), mas nem o chevron
  da linha nem o nome do evento abriram esse drill-down por
  `agent-browser` ou `browser-harness`. Se você achar o caminho, atualize aqui.

## EMQ demora
A nota é calculada sobre janela móvel e atualiza com atraso (~24-48h). Mudança
de código feita hoje NÃO aparece na nota hoje — anote a nota do dia da mudança
como "antes" e volte depois.
