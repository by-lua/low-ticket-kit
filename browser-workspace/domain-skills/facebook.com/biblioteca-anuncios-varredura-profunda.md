# Biblioteca de Anúncios — varredura profunda (extrair card a card)

Executado e verificado em 2026-09-04, perfis `adslib`..`adslib4`, país MX.
Complementa `biblioteca-anuncios-validar-comunicacao.md` (que só conta resultados).

## Comando é `open`, não `nav`
`agent-browser --session adslib open "<url>"` — `nav` não existe.

## País: trocar só `country=` na URL
`...&country=MX&...` / `country=AR`. Mesma URL, sem mexer em formulário.
4 perfis em paralelo, 12 queries em ~2min, sem rate limit.

## Extrair os cards (após open + sleep 8 + 15× scroll down 2500 com sleep 2.5)
```js
(function(){
 var nodes=[...document.querySelectorAll('div')].filter(function(d){
   var t=d.innerText||'';
   return /Identifica..o da biblioteca:/.test(t) &&
          !/Identifica..o da biblioteca:[\s\S]*Identifica..o da biblioteca:/.test(t);
 });
 var seen={},out=[];
 nodes.forEach(function(d){
   var t=d.innerText||'';
   var id=(t.match(/Identifica..o da biblioteca:\s*(\d+)/)||[])[1];
   if(!id||seen[id])return; seen[id]=1;
   out.push(t.replace(/\n{2,}/g,'\n').slice(0,1400));
 });
 return JSON.stringify(out);
})()
```
O filtro "tem UM id e não dois" isola o card exato na árvore de divs aninhadas.
~25-28 cards com 6 scrolls (medido 09-04); 15 scrolls com "Ver mais" passaram de 150 (16-09). Anote quantos cards reais vieram. Rende uns 20-25KB.

## ⚠️ `eval` devolve JSON DUPLAMENTE codificado
`json.loads()` volta uma **string**. Rodar `json.loads` de novo:
```python
d=json.loads(open(f).read().strip())
if isinstance(d,str): d=json.loads(d)
```
E abrir/gravar com `errors='surrogatepass'` — copy com bold matemático
(𝗧𝗲𝘅𝘁𝗼) traz surrogates que quebram o encoder UTF-8 padrão.

## Campos que dá pra tirar do texto do card (UI em pt-BR)
| Campo | Regex |
|---|---|
| id | `biblioteca:\s*(\d+)` |
| data início | `iniciada em (\d+) de (\w+)\.? de (\d{4})` (mês abreviado pt: jan..dez) |
| **variações** | `(\d+)\s*an.ncios usam esse` — só aparece se >1; `Esse anúncio tem várias versões` = ≥2 sem número |
| anunciante | `(?:Ver detalhes do an.ncio\|Ver resumo)\n(.+?)\nPatrocinado` |
| formato vídeo | presença de `0:00 / 0:00` no card |

Card com múltiplas versões usa **`Ver resumo`** em vez de `Ver detalhes do anúncio`,
e o bloco começa com o cabeçalho cru (`Ativo / Identificação... / Plataformas`) —
por isso o regex de anunciante precisa das duas alternativas.

## Leitura técnica de spend: ≥30 dias no ar E ≥2 variações
> Não é critério do método MVT: o Heitor diz que nº de anúncios ativos e tempo rodando
> "não dizem nada" para escolher concepção [aula 02:15]. Serve só para ler o mercado.
Ordenar por variações primeiro, dias depois. Variações altas (6-14) são o sinal
mais forte de spend — mais que idade sozinha (ad velho e único pode ser só
esquecido ligado).

## Screenshot de um anúncio específico
`https://www.facebook.com/ads/library/?id=<library_id>` + sleep 7 + `screenshot <path>`.

## Sem login, sem Cloudflare
Abre limpo nos perfis adslib. O "Entrar" do topo é falso positivo.

## Diagnóstico de paginação — BR / setembro de 2026

Na UI atual, a primeira renderização pode parar em 24–30 cards e exibir o botão
**"Ver mais"** no rodapé. `agent-browser scroll down 2500` chega ao rodapé, mas não
aciona essa paginação; `window.focus()` + `window.scrollTo(0, document.body.scrollHeight)`
também não. Esse foi o motivo das coletas falsas de 26–42 cards.

Para cada um dos 15 scrolls, conte IDs únicos de `Identificação da biblioteca`.
Se a contagem não crescer: aguarde 4 s (e spinner, se existir), confirme/focalize a
janela, rode o scroll nativo até o fim e conte de novo. Persistindo sem incremento,
use `agent-browser --session <perfil> find text 'Ver mais' click`, espere 4 s e
reconte. Se a contagem parar em ~30, é paginação travada, não fim dos resultados.
Em 16 set 2026, isso entregou: ebook 168, planilha 174, kit 180, moldes 172 e
apostila 170 no perfil `adslib2`.

## ⚠️ Zero intermitente (2026-09-16)
Mesma URL no mesmo perfil alterna entre "~26.000 resultados" e "Nenhum anúncio corresponde"
minutos depois (`ebook`, `direito de revenda`, `revenda autorizada`). Zero NÃO é confiável:
recarregue até 3× com sleep 15 e teste em outro perfil adslib antes de concluir vazio.
Perfil muito usado no dia tende a devolver zeros — alterne perfis.
