---
name: low-pagina
description: Etapa E3 do sistema LOW-TICKET — monta a página de vendas da oferta. Padrão da casa = Modelo Padrão LeadGo (base PaginaPro do Fernando + regras da casa, em modelos/modelo-padrao/); alternativas: página da pessoa 100% ou página da pessoa + blocos do Modelo Padrão. Use para "faz a página", "página de vendas da oferta X", "Modelo Padrão", "estilo Fernando", "adapta a página dele pra nossa".
---

# low-pagina — E3, página de vendas

**Entrada:** `OFERTA.md` + `FUNIL.md` aprovados (bônus, planos e upgrade aparecem na página) · `pesquisa/REFERENCIA.md` + `imagens-origem/` · `spyx.pagina[]` do `modelador-*.json`.
**Saída:** `site/` (repo do deploy) com a página no ar em `<slug>.leadgo.dev` · `DESIGN-SYSTEM.md`.

## Passos
1. **Base = a página do original.** Estrutura e ordem das seções dele (clone pelo MineraAds `/api/clonar` ou
   `MODELOS/MODELOS-DE-PAGINA/`). Texto = `spyx.pagina[]` do Modelador, seção por seção, ajustado à `OFERTA.md`.
   Página original fraca/rasa demais pra clonar (comum em modelagem por upgrade, Raio-X com pilar trocado sem
   referência de página boa) → usa o **esqueleto padrão** abaixo em vez de inventar ordem solta.
0-. 🛑 **Pergunta obrigatória antes de montar** (dona, 04/11/2026). **Antes de perguntar, entregar as sugestões:**
   - Tabela **seções da página dela × modelo `modelo-padrao`**: o que ela tem, o que falta (dor, mecanismo, uso, pitch
     intermediário, pra quem é, o que recebe, passos de acesso…) e o que ela tem que o modelo não tem (ex.: sorteio).
   - Para cada bloco que falta: **sugiro acrescentar ou não, e por quê** (qual objeção/alavanca ele resolve).
   - Recomendação de caminho (1, 2 ou 3) com o motivo.
   Depois, os 3 caminhos, escritos por extenso (**padrão = 3, o Modelo Padrão**):
   1. **Página da pessoa 100%** — clone fiel (passo 0), muda só idioma, oferta, preços e cores do visual aprovado.
   2. **Página da pessoa + adaptações do Modelo Padrão** — clone dela como base (visual e identidade dela) + os blocos
      que faltam **copiados do Modelo Padrão** (mesma estrutura/CSS adaptados à paleta dela), só os aprovados nas sugestões.
   3. **Modelo Padrão LeadGo** (recomendado, padrão da casa desde 04/11/2026) — `_skills/low-pagina/modelos/modelo-padrao/`
      (index.html + img + build_page.py + README com todas as regras). Nasceu do PaginaPro V1 do Fernando Oliveira
      (original só pra consulta em `MODELOS/MODELOS-DE-PAGINA/fernando/`). Mudança nova aprovada pela dona numa página
      feita nele → aplicar também no modelo e anotar no README do modelo. Os modelos Flowise são legado: não usar.
   Valem nos 3: barra vermelha fixa · hero acima da dobra · planos e garantia padrão Mapa do Tarot · QA (passo 9b).
   - **Caminhos 1 e 2** → passo 0 abaixo (clone). Ordem: **o material por dentro logo depois da 1ª seção (hero)**.
   - **Template do Fernando** → `MODELOS/MODELOS-DE-PAGINA/fernando/index.html` (PaginaPro V1, HTML estático): copia,
     troca texto/cores/imagens seguindo os blocos dele (topo → dor → prévias → mecanismo → comparação → uso → pitch
     → pra quem é → o que recebe → bônus → oferta → segurança → passos de acesso → FAQ → fecho). Copy das seções:
     `CONHECIMENTO`/PaginaPro `references/arquitetura-copy.md`.
   - **Antes × depois** (nos dois): só quando a oferta pega material técnico e transforma em visual. Senão, corta.
   - **Bloco dos 2 planos** (nos dois) = padrão Mapa do Tarot (`OFERTAS/mapa-do-tarot/site/index.html`, `<!-- PLANS -->`):
     - **Básico, SEM imagem:** só o que ele tem; o que fica de fora aparece **riscado com ✗**; preço; botão
       secundário; embaixo, **no celular**: « ATENÇÃO: temos uma oferta ainda melhor para você! Olha só abaixo » + ↓↓↓ animado.
     - **Completo, COM imagem** (mockup do plano completo, **menor**: largura máx. ~300px): selo « ★ O preferido »,
       "Todos os materiais — entrega imediata", **caixa destacada com o bônus principal**, checklist do conteúdo,
       **"Bônus exclusivos:"** com 🎁, preço riscado (valor) → preço, botão principal.
0. **Clone primeiro, sempre** (erro de 04/11/2026, Calendrier: página escrita do zero com layout próprio — a dona
   perguntou "por que não está parecido com a original, melhorada?"). Base = DOM renderizado + CSS da página dele
   (Elementor costuma ser 1 bloco HTML com `<style>` próprio: extrair esse bloco). Troca só texto, variáveis de cor,
   fontes e `src`; depois aplica o Plano da página (cortar/acrescentar/reordenar seções) usando as MESMAS classes
   dele. O esqueleto 1a só quando a original é fraca demais pra clonar.
0b. **Preferências fixas da dona (04/11/2026):**
   - **Hero centralizado:** barra → headline → **mockup no meio** → texto curto/bullets organizados → botão.
     Nada de hero em 2 colunas (texto de um lado, imagem do outro), nem no desktop.
   - **Hero organizado como o do Fernando** (dona, 04/11/2026): subheadline → **bullets com ✓ em círculo** → **pílula com o
     preço do plano mais barato logo acima do botão** → botão → linha de confiança (✓ acesso imediato · ✓ garantia · ✓ pagamento
     seguro). Nada de cards espalhados nem parágrafos empilhados.
   - **A 1ª seção cabe na tela até o botão, sem rolar**, no celular (até 360×740) e no PC (1366×768): mockup com
     `max-height` em vh, h1 menor em tela baixa, 3º bullet some se precisar. Provar com o QA (9b).
   - **Barra de urgência sempre VERMELHA** (fundo vermelho, texto branco), qualquer paleta, **fixa no topo** (`position:sticky;top:0`)
     e **fina: ~30px, 1 linha** em qualquer tela (no celular, encurtar o texto).
   - **Mockup é o protagonista do hero:** grande (~44vh celular / 46vh PC) e texto pequeno ao redor.
1a. **Esqueleto padrão (fallback, 1 função comercial por bloco, nesta ordem):**
   barra de urgência (só se for real) + hero → dor/agitação (título "[atividade central] não precisa ser
   [dor do dia a dia]", 6 chips de situação, ponte fixa pro mecanismo) → prova do produto (mostra antes de
   explicar) → mecanismo único (a unidade real + 4 passos numerados) → antes×depois (condicional, só com fonte
   legítima) → demonstração de uso (condicional, 4+ cenas reais) → pitch intermediário (mockup diferente do
   hero + CTA) → pra quem é (6 situações no molde situação→ganho: 4 do público majoritário + até 2 de
   secundário, nunca característica do produto como se fosse avatar) → produto completo/benefícios (8 itens
   curtos, sem repetir o mesmo benefício reformulado) → bônus → oferta/value stack → prova social (só com prova
   real — sem prova, corta sem deixar buraco) → garantia → passos pós-compra (condicional) → FAQ (perguntas
   que matam objeção real, nunca genérica) → fecho emocional (condicional) → rodapé.
   Teste de toda frase central: `recurso → ação facilitada → ganho → custo evitado` — se não converte nisso, é
   adjetivo vazio, refaz.
1b. **Headline/subheadline/bullets do hero — regra fixa, qualquer oferta:**
   - **Headline** vende o resultado final que o avatar quer no fundo, nunca um degrau no meio do caminho
     (formato, organização, quantidade pura). Teste: se trocar o nome do produto e a frase continuar servindo
     pra qualquer coisa, tá genérica — refaz.
   - Gera 3 variações, moldes diferentes, e escolhe a mais forte (ou mostra as 3 pra dona decidir):
     **Inventário** (`[número] [item] prontos para [uso]` — quando o forte é a coleção contável e pronta) ·
     **Domínio** (`Domine [assunto] e [consequência concreta na vida]` — quando o produto fecha um corpo de
     conhecimento) · **Descoberta** (`Descubra [mecanismo] que [resultado], sem [objeção]` — quando o
     diferencial é o método).
   - **Subheadline** é a ponte entre o desejo da headline e o caminho real: mecanismo/quantidade real → ação
     simplificada → ganho funcional observável (reconhecer, memorizar, aplicar, localizar, decidir) → atrito
     removido. Teste: escondendo a headline, a sub ainda explica o que a oferta ajuda a fazer e por que é mais
     fácil? Se não, refaz. Nunca feche a frase só em "no celular", "em poucas horas", "tudo em um só lugar" sem
     ligar isso a um ganho concreto.
   - **3 bullets do hero**, um por frase, no molde `[verbo] + [ganho] + [cena concreta]`: (1) ganho apesar da
     principal restrição de rotina do avatar, (2) a unidade/mecanismo do produto visível, (3) uso real ou
     flexibilidade no momento que importa. Nunca liste característica pura ("vem em PDF") como bullet.
   - Proibido: número de velocidade/resultado sem prova (`5x mais rápido`), garantia de resultado que depende
     do comprador (`garante aprovação`), adjetivo sem mecanismo atrás (`completo`, `inovador`, `transformador`,
     `prático e fácil`).
   - **Headline aprovada → grava em `OFERTA.md` § Ângulo final** (molde + headline + subheadline). O `criativo`
     lê esse campo antes de usar `spyx.ganchos` do modelador — se o molde escolhido aqui divergir do ângulo que
     o SpyX chutou na modelagem, o ângulo final manda; avisa a dona que os ganchos antigos podem não bater mais.
2. **Visual = o da E2d, já aprovado.** Antes do passo 1, conferir `DESIGN-SYSTEM.md` com a linha
   `Aprovado pela dona: <data>`. Não existe → **parar e fazer a E2d** (abaixo). Nunca copiar a paleta do original
   em silêncio.
2a. **E2d — Visual (pergunta obrigatória, regra da dona 04/11/2026).** Antes de montar a página, perguntar:
   *"Mantemos o visual dele ou mudamos um pouco (cores, fundo, elementos, capa)?"* — mostrando o que ela já
   comentou (ex.: "fundo mais limpo", "desktop mal resolvido").
   - **Objetivo padrão da dona = diferenciar sem fugir do que vende.** Mantém a **pegada/vibe** do original (o
     estilo que bate no público — ex.: grimório vintage no Calendrier), mesma composição e tipo de peça; muda
     **as cores e alguns elementos**, um pouco — o bastante pra que, se outro modelar a mesma oferta nesse idioma,
     a nossa não fique igual à dele. Dois erros já cometidos (Calendrier, 04/11): (1) trocar só a cena e manter
     cores/elementos = "ficou praticamente igual"; (2) trocar o estilo inteiro (Art Nouveau) = foge do que vende.
     Os 3 oferecidos são **variações de paleta dentro da mesma vibe** + um toque leve de visual (detalhe de moldura,
     tipografia do título), **mantendo todos os elementos** dele (trocar coruja/gato/tarô por outra coisa inventa
     produto — dona, 04/11: "mudar só a cor e um pouco do visual sem perder a essência"). Fundo da cena claro.
   - **Oferecer 3 variações** escritas por extenso (paleta · elementos trocados · por que serve pro mercado), com
     recomendação, e a opção **"gerar os 3 pra comparar"** (uma imagem-guia de cada). Ela escolhe.
   - **Gerar EM CIMA do mockup completo do original** quando a página dele tiver: anexar o kit completo dele
     como BASE (mesma composição e itens) e pedir só a troca de identidade (paleta, estilo, elementos, idioma).
     É a base visual de tudo; sem ele, montar a cena a partir da capa + páginas + bônus dele.
   - **Manter** → tokens hex + fontes da página original → `DESIGN-SYSTEM.md`.
   - **Mudar** → gerar **uma imagem-guia** com `gpt-imagem-playwright` descrevendo a mudança (cores, fundo, elementos).
     **A imagem-guia é o mockup do PLANO COMPLETO** (regra da dona, 04/11/2026): capa do principal + páginas de
     dentro + capas dos bônus, tudo numa cena — é a que mais carrega identidade (capas, páginas, elementos) e serve
     de referência pra todo o resto. Anexar: o mockup do kit completo dele (se a página tiver) + capa + 2 páginas
     reais de dentro + mockups dos bônus. A página dele não tem mockup completo → montar a cena completa a partir
     da capa, das páginas e dos bônus dele. Mostrar → dona aprova
     ou pede ajuste → tirar a paleta da imagem aprovada (fundo clareado se ela pediu fundo limpo).
   - Gravar em `DESIGN-SYSTEM.md`: tokens hex, fontes, **caminho da imagem-guia**, o que a dona pediu (literal)
     e `Aprovado pela dona: <data>`. Daqui pra frente a imagem-guia é a âncora: página (E3), entregável (E4) e
     lote de imagens (E5) seguem ela, não o visual do concorrente.
   - Página sempre com **desktop e mobile** resolvidos (página clonada costuma ser só mobile).
3. **Imagens:** placeholders agora; geração na E5 (`imagens-pagina-low`, ordem nova: mockups da página primeiro).
4. **Preço:** botões com o preço da `OFERTA.md`. Oferta multi-país → preço em moeda local
   (`low-ticket/references/PRECO-MOEDA-LOCAL.md`).
4b. **3 destinos de CTA, só isso — independe da página clonada, sempre assim:**
   - **CTA do hero** → **sempre a seção "o que você recebe"** (`id="recebe"`, ex.: « Tout ce qu'il faut pour vivre
     2027 ») — dona, 04/11/2026. Nunca pula direto pro preço.
   - **Todo CTA do meio da página** (dor, pitch intermediário, benefícios, fecho emocional) → `id="oferta"`
     (a seção de planos/preço), nunca checkout externo direto.
   - **Só o botão DENTRO do card de preço** → URL do checkout. Centraliza essa URL em 1 campo só
     (`checkoutUrl`), nunca repete em outro componente. Checkout ainda não cadastrado → placeholder explícito
     na pendência, nunca URL inventada, nunca todos os botões indo pro checkout.
   - **2 planos na seção de oferta:** ver passo 0- (padrão Mapa do Tarot).
   - **No mobile, entre os 2 planos:** aviso "ATENÇÃO: temos uma oferta ainda melhor para você! Olha só abaixo"
     + 3 setas (↓↓↓) com animação de bounce, apontando pro plano completo logo abaixo.
4c. **Sincronia de bônus — regra fixa:** o bônus já vem decidido do `FUNIL.md` (cada um matando uma objeção
   específica — ver `low-funil` § bônus mata objeção). Na página só exibe, sem inventar nem resumir:
   - **Badge da oferta** no molde `✦ [quantidade real] [unidade principal] + [N] BÔNUS` — número sempre
     contado pela lista real do `FUNIL.md`, nunca estimado.
   - **1 card por bônus real**, nome oficial do bônus (nunca "bônus 1, bônus 2" genérico nem resumir vários
     bônus numa linha só).
   - Mudou quantidade/nome de bônus no `FUNIL.md` depois? Sincroniza em TODO lugar que cita o número: badge,
     cards, lista do plano, soma do value stack, FAQ, texto de liberação — nenhum resquício do número antigo.
5. **Rastreio no `<head>`:** bloco fbq inline ANTES do loader do Trackeador (skill `trackeador`). Todo botão
   de checkout com `data-tk-value` + `data-tk-currency`; página não manda IC próprio.
6. **Os 2 popups, SEMPRE** (dona, 04/11/2026: "eu sempre uso essas coisas"), padrão Mapa do Tarot (código no modelo
   `modelos/modelo-padrao/`):
   - **Upgrade no clique do Básico** (`#downsell`): « leve tudo por quase o mesmo preço » — Completo num preço
     intermediário (ex.: básico 5,90 → **upgrade 7,90** → completo 12,90). Sim → checkout do upgrade; "não, continuar
     com o básico" → checkout do básico.
   - **Saída** (`#exitpopup`): básico com desconto (ex.: 4,90). Regras e textos: skill `popup-saida-low-ticket`.
   O QA (9b) acusa se faltar algum dos dois.
6b. **Página leve e otimizada — obrigatório, toda página** (skill `otimizacao-pagina-vendas`, sem quebrar o clone):
   - **toda imagem** em WebP, no dobro da largura exibida, ~80 KB cada, `width`/`height`, lazy abaixo da dobra,
     a imagem principal (LCP) pré-carregada;
   - **todo vídeo dentro de player e leve**: MP4 comprimido (720p, alvo ≤ ~4 MB) com `controls preload="none"` e
     poster WebP, ou player externo que só carrega no clique. Nunca vídeo pesado baixando no carregamento;
   - fontes só com os pesos usados, pixel e Trackeador `async` (nunca removidos);
   - medir no Lighthouse mobile antes e depois — a prova vai pro gate da E9.
7. **Rodapé:** BR → só "LeadGo" (sem CNPJ nem nome da dona); fora do BR mantém dados legais. Termos e
   privacidade. Favicon na página e no `/painel`. Suporte: e-mail e WhatsApp de `_memoria/empresa.md`.
9b. **QA de layout antes de publicar (obrigatório):** `scripts/qa-layout.js` em 360×740, 375×667, 390×844, 1366×768 e
   1920×1080 (`agent-browser --session S set viewport W H` → `eval --stdin < qa-layout.js`). Tem que dar `ok` em todos:
   botão do hero acima da dobra, sem rolagem lateral, nenhum texto vazando da caixa, nenhum texto estourando botão,
   todo botão aguentando texto +45% (tradução automática do navegador — a compradora pode traduzir a página),
   nenhuma imagem coberta ou cortada por outro elemento ou caixa (precisa sobrar espaço embaixo), e favicon presente.
   Depois, olhar print do hero (celular e PC) e do bloco de planos.
8. Deploy: repo em `github.com/leadgodev/`, Coolify auto-deploy (fatos em `_memoria/empresa.md`).
9. Trocou a página de uma oferta que já roda anúncio → `adstrackeador pagina comparar <atual> <nova>` antes.

Gates no ar (eventos) ficam na `low-gates-no-ar`. Próximo: `low-entregavel`.
