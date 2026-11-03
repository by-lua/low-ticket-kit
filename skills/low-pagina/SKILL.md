---
name: low-pagina
description: Etapa E3 do sistema LOW-TICKET — monta a página de vendas da oferta modelando a página do original: mesma estrutura e cores, troca a oferta, o texto e o idioma. Use para "faz a página", "página de vendas da oferta X", "adapta a página dele pra nossa".
---

# low-pagina — E3, página de vendas

**Entrada:** `OFERTA.md` + `FUNIL.md` aprovados (bônus, planos e upgrade aparecem na página) · `pesquisa/REFERENCIA.md` + `imagens-origem/` · `spyx.pagina[]` do `modelador-*.json`.
**Saída:** `site/` (repo do deploy) com a página no ar em `<slug>.leadgo.dev` · `DESIGN-SYSTEM.md`.

## Passos
1. **Base = a página do original.** Estrutura e ordem das seções dele (clone pelo MineraAds `/api/clonar` ou
   `MODELOS/MODELOS-DE-PAGINA/`). Texto = `spyx.pagina[]` do Modelador, seção por seção, ajustado à `OFERTA.md`.
   Página original fraca/rasa demais pra clonar (comum em modelagem por upgrade, Raio-X com pilar trocado sem
   referência de página boa) → usa o **esqueleto padrão** abaixo em vez de inventar ordem solta.
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
2. **Paleta e fontes = as da página original**, gravadas em `DESIGN-SYSTEM.md` (tokens hex + fontes).
   Outra paleta só se a dona pedir pra essa oferta.
3. **Imagens:** placeholders agora; geração na E5 (`imagens-pagina-low`, ordem nova: mockups da página primeiro).
4. **Preço:** botões com o preço da `OFERTA.md`. Oferta multi-país → preço em moeda local
   (`low-ticket/references/PRECO-MOEDA-LOCAL.md`).
4b. **3 destinos de CTA, só isso — independe da página clonada, sempre assim:**
   - **CTA do hero** → âncora de prévia/galeria do material (`id="previas"` ou a seção "recebe hoje"/bônus se
     não tiver prévia separada). Nunca pula direto pro preço.
   - **Todo CTA do meio da página** (dor, pitch intermediário, benefícios, fecho emocional) → `id="oferta"`
     (a seção de planos/preço), nunca checkout externo direto.
   - **Só o botão DENTRO do card de preço** → URL do checkout. Centraliza essa URL em 1 campo só
     (`checkoutUrl`), nunca repete em outro componente. Checkout ainda não cadastrado → placeholder explícito
     na pendência, nunca URL inventada, nunca todos os botões indo pro checkout.
   - **2 planos na seção de oferta:** básico sem imagem, completo com imagem (mockup do produto).
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
6. **Popup de saída:** skill `popup-saida-low-ticket`.
6b. **Página leve e otimizada — obrigatório, toda página** (skill `otimizacao-pagina-vendas`, sem quebrar o clone):
   - **toda imagem** em WebP, no dobro da largura exibida, ~80 KB cada, `width`/`height`, lazy abaixo da dobra,
     a imagem principal (LCP) pré-carregada;
   - **todo vídeo dentro de player e leve**: MP4 comprimido (720p, alvo ≤ ~4 MB) com `controls preload="none"` e
     poster WebP, ou player externo que só carrega no clique. Nunca vídeo pesado baixando no carregamento;
   - fontes só com os pesos usados, pixel e Trackeador `async` (nunca removidos);
   - medir no Lighthouse mobile antes e depois — a prova vai pro gate da E9.
7. **Rodapé:** BR → só "LeadGo" (sem CNPJ nem nome da dona); fora do BR mantém dados legais. Termos e
   privacidade. Favicon na página e no `/painel`. Suporte: e-mail e WhatsApp de `_memoria/empresa.md`.
8. Deploy: repo em `github.com/leadgodev/`, Coolify auto-deploy (fatos em `_memoria/empresa.md`).
9. Trocou a página de uma oferta que já roda anúncio → `adstrackeador pagina comparar <atual> <nova>` antes.

Gates no ar (eventos) ficam na `low-gates-no-ar`. Próximo: `low-entregavel`.
