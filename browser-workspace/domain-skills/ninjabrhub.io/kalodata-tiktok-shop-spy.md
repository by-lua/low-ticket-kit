# Kalodata (o real) via NinjaBR Hub

**Kalodata é ferramenta separada de terceiros**, acessada via SSO a partir do
Hub. NÃO é NinjaSpy → Catálogo TikTok Shop (essa é outra ferramenta do Hub,
proxy `fastmoss-proxy`/`ninjaspy-proxy`, e trava — ver seção no fim).

## Caminho certo (verificado 2026-09-08)

1. `agent-browser open https://ninjabrhub.io/tools`
2. Preencher o campo de busca "Buscar entre todas as ferramentas..." com
   `kalodata`.
3. Aparece card **"Kalodata 2 contas · SPY & INTELIGÊNCIA"**, categoria
   "Spy & Inteligência". Clicar nele (clique nativo `agent-browser click @ref`
   funciona, mesmo sendo item que abre nova aba).
4. Abre modal com 2 opções de conta ("Kalodata 2 (GLOBAL) Conta 1", "Kalodata 3
   (GLOBAL) Conta 2"). Clicar em qualquer uma.
5. Abre **nova aba** (`agent-browser tab` mostra a nova) em
   `https://kalodata2.ninjabrhub.online/` (ou similar), já autenticado via SSO
   — sem pedir login. Cair na home é normal (parece página de marketing); o
   login real só aparece ao navegar pra uma seção como **Product**.
6. Clicar no menu **Produto** (`/product`) — aí carrega o dashboard de
   verdade, com filtros funcionando (Datas, Categorias, Receita, Comissão,
   Avaliação, etc).

## Filtro por categoria (moda feminina)

Painel esquerdo → **Categorias** → busca ou navega na árvore → categoria
**"Roupas femininas e roupas íntimas femininas"** é o nó de moda feminina
geral (tem subcategorias: peças superior/inferior, vestidos, roupas íntimas,
etc). Clicar no **texto do checkbox item** (não a linha inteira) marca de
fato — testado: clicar na linha (`ref` do `menuitemcheckbox`) às vezes não
marca, clicar no elemento filho (ícone/checkbox) dentro dele marca certo.
Depois clicar **Aplicar** (dentro do popover) e depois **Enviar** (botão do
painel de filtros, fica `disabled` até aplicar pelo menos 1 filtro).

## Tabela de resultado

Ordenável por Receita, Itens Vendidos, Taxa de crescimento, Avaliação, Comissão
etc (clicar no cabeçalho da coluna). Paginação embaixo (ex: 17.507 produtos na
categoria moda feminina BR, 10/página por padrão).

**Scroll**: a tabela é um container interno com scroll próprio, `scroll down`
normal do agent-browser NÃO rola ela. Usar JS:
```js
const el = [...document.querySelectorAll('div')].find(d => d.scrollHeight > d.clientHeight + 200 && d.clientHeight > 300);
el.scrollTop += 900;
```
(pega o primeiro `div` grande com overflow — funcionou, mas é heurística
frágil; se a página mudar de layout, pode pegar o container errado.)

## Dados que a tabela mostra por produto

Preço médio por unidade, Taxa de comissão (%), Receita 30d, Contagem de
criadores publicando, Taxa de conversão do criador, Avaliação do produto,
Data de lançamento, tendência de receita (gráfico), thumbnails dos vídeos
com maior receita daquele produto. Cobre praticamente todo critério do
Jhonatas (comissão, avaliação, volume/vendas, preço) numa tela só.

---

## NÃO confundir com: NinjaSpy → Catálogo TikTok Shop (trava)

Essa é outra ferramenta dentro do Hub (menu lateral NinjaSpy → "Catálogo
TikTok Shop", rótulo "TikTok Shop Spy"), sem sair do domínio `ninjabrhub.io`.
Parece o Kalodata (mesma proposta) mas usa proxy próprio
(`fastmoss-proxy`/`ninjaspy-proxy` via função Supabase) — medido 2x, minutos
de diferença, perfis diferentes: a chamada de rede fica **pendente pra
sempre**, sem erro nem sucesso, dashboard e busca ficam eternamente em
skeleton cinza. Não é Cloudflare, não é login, não é seletor errado — é
backend do provedor (FastMoss) fora do ar ou proxy quebrado.

**Se alguém pedir "abre o Kalodata": é o caminho do topo deste arquivo
(`/tools` → busca → card Kalodata → conta → `kalodata2.ninjabrhub.online`),
nunca o NinjaSpy.**
