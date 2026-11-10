---
name: low-ticket
description: Porta de entrada e orquestradora do sistema LOW-TICKET (ofertas low ticket da LeadGo). Abre a sessão (índice, métodos ativos, oferta) e diz qual etapa e qual filha usar, da escolha da oferta até a entrega pronta. Use SEMPRE no começo de qualquer trabalho low ticket — "abrir", "retomar", "onde paramos", "vou mexer na oferta X", "achei uma oferta na Biblioteca", "modelar essa oferta", página, entregável, área de membros, funil, checkout. Criativo de anúncio vai pra skill `criativo`.
---

# low-ticket — orquestradora (índice)

Esta skill só diz **a ordem e quem chamar**. Regra de execução mora na filha/skill da etapa.
Raiz: `~/Documentos/TRAMPO/PROJETOS/WORKING/PROJETOS - INTERNOS/LOW-TICKET` (fonte desta skill: `_skills/low-ticket/`).

## 1. Abrir — sempre primeiro

> **Delegação (dona, 10/11/2026):** quem delega trabalho desta pasta a outro agente (pane, worker, subagente, Codex, DeepSeek) põe no INÍCIO do prompt a ordem de abrir esta skill (`abrir.py "<oferta>" "<etapa>"`), ler o RECIBO, o `INDICE.md` e o `CLAUDE.md` da oferta antes de executar. Sem isso o worker trabalha sem as regras da casa.
```
python3 "<RAIZ>/_skills/low-ticket/scripts/abrir.py" "<oferta>" "<etapa ou tarefa>"
```
Imprime o `INDICE.md`, a chave `_memoria/METODOS-ATIVOS.md` e os arquivos da oferta. Devolva o **RECIBO** à dona antes
de agir. **Método com Ativo = não não se usa**, mesmo que a skill exista.

## 2. Passo a passo (siga na ordem; cada passo só começa com a saída do anterior)
**Como ler:** 🛑 = **pare e pergunte à dona** (texto por extenso no chat, tradução PT de todo texto estrangeiro,
depois a pergunta) e **espere a resposta**. ✅ = arquivo que prova que o passo terminou. Faltou o ✅ do passo
anterior → volte e faça, avisando a dona. Nunca pule passo, nem quando é "só levar a oferta pra outro país".
Tudo que a dona disser vai **literal** em `pesquisa/da-dona/<data>-<assunto>.md` no momento em que ela disser.

**PASSO 1 — Referência** (`low-referencia`)
- Entrada: link (Biblioteca e/ou página) + o que a dona explicou (país-alvo, se disse).
- Faço: salvo o pedido literal → crio `OFERTAS/<slug>/` → leio a página até o checkout (preço, planos, bumps,
  gateway) → baixo todas as imagens → baixo os vídeos dos anúncios (PROJETOS-MIDIA) → escrevo a referência.
- ✅ `pesquisa/REFERENCIA.md` + `pesquisa/referencia/imagens-origem/` + `pesquisa/da-dona/…`
- 🛑 Mostro o resumo (o que é, preço, funil, anunciante, dias no ar) e pergunto:
  *"Você quer **modificar** a oferta (outro produto/público/ângulo/formato) ou **só melhorar esta** e levar pro
  país X?"*

**PASSO 2 — Raio-X + SpyX** (`low-modelador`, modo LOCAL — `references/PROMPTS-MODELADOR.md`; SpyX: `metodo-spyx`)
- Sempre rodo os dois, nos dois casos:
  - **Raio-X:** 6 pilares + motor + comprador. Se ela quer **modificar** → também as **10 propostas**.
  - **SpyX:** comprador cético por etapa · notas das 4 alavancas · a mais fraca e a não tocada · furos.
- 🛑 Mostro por extenso (propostas, alavancas, furos). Se houve 10 propostas, ela **escolhe uma**; se é "só
  melhorar", ela confirma.
- ✅ `pesquisa/modelador-<data>-raiox.md` + `pesquisa/modelador-<data>-spyx.md` + escolha dela em `da-dona/`.

**PASSO 3 — Validação** (`low-validar`)
- Faço: termos de busca prontos (PT/ES/EN + idioma do país-alvo), um por linha.
- 🛑 Pergunto: *"Busca manual (você) ou automática (eu)?"* — padrão dela = **manual**. Digo o que ela traz:
  tem/não tem concorrente · links dos anunciantes · quais quer de **referência de criativo/página/funil**.
- A busca responde, no idioma-alvo **e** em outros idiomas: tem demanda? · alguém já anuncia a **mesma** oferta no
  idioma-alvo (→ **mais modelagem**: volta ao Passo 2 pra diferenciar antes do Passo 4)? · ofertas parecidas em
  outros idiomas e outros anunciantes que servem de referência?
- Faço: abro os links, completo a tabela, funil dos 2-3 melhores, orgânico, veredito 🟢🟡🔴.
- 🛑 Ela decide seguir ou não.
- ✅ `pesquisa/VALIDACAO-<data>.md` (quem buscou · concorrentes · referências escolhidas · decisão).

**PASSO 4 — Ficha, valores, funil e plano da página** (`low-ficha-oferta` + regras `low-funil`)
- Checklist completo (9 itens): `low-ficha-oferta` 2a — título · copy · objeções · bônus (manter/melhorar/criar/cortar) ·
  bumps (igual/melhorar/cortar/virar upsell) · **upsell = microSaaS do produto, com a copy** (padrão: `low-upsell-app` MODO TESTE + modelo curto, escada 7,90/5,90/3,90 com 2 dias grátis) · upgrade/saída · valores e
  checkout · furos do SpyX + plano da página.
- Faço, nesta ordem: objeções do comprador (5-8) → **furos do SpyX aplicados** (tabela furo → correção → onde)
  → peças do original revisadas (manter/melhorar/cortar; acrescentar só onde sobrou objeção) → **planos e
  valores** (moeda do país) → bumps, upgrade, downsell/saída, upsell/microSaaS → **checkout** (gateway e conta
  conferidos em `_memoria/contas-e-codigos.md` · moeda · métodos de pagamento do país · modelo: checkout do
  gateway ou `checkout-premium` (padrão = visual do checkout Chave Mestra) · o que aparece nele: banner, bumps, garantia 7d BR/15d fora, timer 10 min, ícone preto+texto Privacidade/Compra segura/Conteúdo aprovado na caixa de segurança) → **plano da página** (títulos,
  seções manter/reordenar/cortar/acrescentar, popup, CTAs, desktop+mobile).
- 🛑 Mostro tudo por extenso e pergunto cada pendência (valores, checkout, garantia, bônus, título).
- ✅ `OFERTA.md` + `FUNIL.md` com "aprovada em AAAA-MM-DD" · `CLAUDE.md` + `STATUS.md` da oferta.

**PASSO 5 — Visual** (`low-pagina` § 2a · `gpt-imagem-playwright` em **chat temporário**)
- 🛑 Pergunto: *"Mantemos o visual dele ou mudamos um pouco (cor e toque leve, mesma essência)?"*
- Mudar → ofereço **3 variações de paleta** (mesmos elementos dele, fundo claro) por extenso → opção de gerar
  as 3 **em cima do mockup do plano completo dele** → 🛑 ela escolhe.
- ✅ `DESIGN-SYSTEM.md` (tokens, fontes, **imagem-guia**, "Aprovado pela dona: data").

**PASSO 6 — Copies da modelagem** (`low-modelador` etapa 2, local: prompts 2A/2B/2C)
- Só depois do Passo 4 aprovado. Direção = tudo da `OFERTA.md`/`FUNIL.md` (planos, valores, bônus, plano da página).
- Faço: oferta modelada · **página seção a seção (copy final)** · **banco de ângulos e ganchos** · copies de anúncio
  (texto principal + título) · comprador reagindo à nossa. Base: ficha/funil/plano aprovados + anúncios do original
  já lidos. **Roteiros e peças da leva NÃO saem aqui** — saem no Passo 14 (`criativo` C2), depois da página e do MVP
  (o demonstrativo precisa do produto real), com as referências de criativo escolhidas no C1.
- 🛑 Mostro por extenso, com tradução PT.
- ✅ `pesquisa/modelador-<data>-etapa2.md`.

**PASSO 7 em diante — Produção** (um por vez, mesma regra de ✅)
| Passo | O quê | ✅ | Skill |
|---|---|---|---|
| 7 (E3) | Página com o visual do Passo 5 e o plano do Passo 4 | `site/` no ar **+ `qa-layout.js` ok + `qa-performance.js` APROVADO colado no `STATUS.md`** (página sem prova de velocidade não é ✅) | `low-pagina` (9b, 9c) |
| 8 (E4) | Entregável: texto inteiro → primeiras páginas → 🛑 aprova → MVP | `produto/` | `low-entregavel` |
| 9 (E5) | Imagens da página: lote com a imagem-guia anexada | imagens plugadas | `imagens-pagina-low` |
| 10 (E6) | Área de membros | `/painel` + PDF | `area-membros-netflix` |
| 11 (E7) | Peças do funil | peças no `/painel` | `low-funil` · `low-entregavel` |
| 12 (E8) | Checkout | oferta no gateway | `low-checkout` |
| 13 (E9) | Gates no ar (eventos, **performance**, download, checkout) | prova no `STATUS.md` | `low-gates-no-ar` |
| 14 | Criativo — começa SEMPRE pelo **C0** da `criativo` (mostra banco do Passo 6 + criativos do original + refs de outros → 🛑 usar o quê / buscar novos com termos por idioma → 🛑 por anúncio: modelar o vídeo ou entender o padrão) | `criativos/FONTES-<data>.md` → leva aprovada | `criativo` |
| 15 | Tráfego | — | `metaads-kevones` |

## 2b. Classificar tudo que for salvo — NOSSO × DESCARTADO × CONCORRENTE (regra fixa, 05/11/2026)
Causa de erro real: um agente usou a capa azul (descartada, igual à da concorrente) num take porque o arquivo se chamava
`capa` e estava na pasta de uso. Nada dizia qual era a oficial. Por isso, **todo arquivo que a sessão cria, recebe ou
muda tem um dono**, e o dono fica escrito em `OFERTAS/<slug>/ATIVOS.md` (modelo: `MODELOS/_MODELO-ATIVOS.md`):
| Dono | Onde fica | Pode virar produto/referência? |
|---|---|---|
| **NOSSO** (oficial ou em teste) | pastas de uso (`produto/`, `site/`, `criativos/`…) + linha na seção 1 do `ATIVOS.md` | só se `OFICIAL` |
| **DESCARTADO** | `_descartado/AAAA-MM-DD-<motivo>/` na raiz da oferta, ou apagado — **nunca na pasta de uso** | nunca |
| **CONCORRENTE** | só `pesquisa/referencia/` ou `criativos/**/ref-original/` | só como referência de composição/ideia, nunca como arte nossa |
Regras:
1. **Antes de anexar/usar** capa, mockup, imagem-guia, persona ou página como referência: ler `ATIVOS.md`. Item fora da seção 1
   como `OFICIAL` = não usa. **Nunca escolher arquivo pelo nome** (`capa`, `guia`, `kit`, `v1`).
2. **Dona aprovou algo novo** (nova capa, persona, visual) → mesma resposta: grava na seção 1 (`OFICIAL`, data) e move o antigo
   para a seção 2 (+ `_descartado/`). Gerou e ainda não aprovou = `EM TESTE`.
3. **Dona descartou** → move/apaga na hora e registra motivo. Descartado que ficou na pasta de uso é defeito.
4. **Material do concorrente** entra na seção 3 (quem, link, o que pegamos, o que não) e nunca fora de `pesquisa/referencia/`.
5. **Criativo**: cada peça tem linha na seção 4 (modelada de qual item da seção 3, estado, arquivo final). Gerou take → registra
   `gerando`/`aprovada`/`reprovada` junto com a aprovação da dona, não depois.
6. Sem `ATIVOS.md` na oferta → o `abrir.py` avisa; criar a partir do modelo ANTES de gerar qualquer imagem do produto.
7. Imagem que mostra o produto = conferida contra o `OFICIAL` (cor, arte, texto) antes de mostrar à dona.

## 3. Regras que valem em toda etapa (só estas; o resto mora na filha)
- **Fatos antes de cadastrar:** gateway, conta, código, webhook, domínio e **organização do Trackeador** — conferir no
  índice (seção Fatos). Nunca de cabeça. Todo comando `trackeador` que cria algo leva `--org` explícito.
  Incidente Calendrier FR (04-06/11/2026): a oferta nasceu na Leadgo, não na WINX, e a venda chegou órfã.
- **Webhook de medição (Trackeador) com TODOS os eventos, em qualquer checkout** (Hotmart, Wiven, Mundpay, Zenith,
  GG, próprio): aprovada, recusada/cancelada, expirada, boleto/aguardando, atrasada, abandono, reembolso, chargeback.
  Só "aprovada" = tentativas somem do Trackeador. Regra da dona 09/11/2026. Entrega (`/painel`) segue só o que libera/tira acesso.
- **IC só quando vai pro checkout, no pixel Meta e no Trackeador (dona, 10/11/2026):** botão que só abre o popup Básico→Completo = 0 IC; clique que leva ao checkout (Completo barato ou Básico no popup, Completo ou saída na página) = 1 IC. Gate obrigatório antes de entregar pixel: `low-gates-no-ar` › regra fixa do topo + Gate 1.
- **Funil de upsell e order bump em TODA oferta de entrada (dona, 10/11/2026):** Básico, **Completo, Upgrade e Saída/popup** (e combos) têm cada um **funil de vendas ATIVO** (entrada → upsell → downsell → obrigado) e os **mesmos order bumps** no checkout, **inclusive a oferta de Saída**. O funil serve **cartão, PayPal, Apple Pay e Google Pay** (boleto/Pix desligados). Antes do tráfego e todo dia de tráfego: conferir pela API/tela da Hotmart (status do funil, bumps no checkout de cada `off=`, planos do app). Procedimento e script: `_skills/low-upsell-app/references/CHECKLIST-UPSELL-QUALQUER-OFERTA.md` § « Verificação POR OFERTA DE ENTRADA ». Caso: Calendrier FR, funil do Complet achado desligado em 10/11.
- **Checkout (dona, 10/11/2026) — depende do tipo, nova ou existente:**
  - **Checkout PRÓPRIO / premium** (a oferta usa `checkout-premium`): sai pronto no modelo `MODELOS/checkout-base/index.html` (cópia da Chave Mestra) — timer 10 min regressivo que reinicia a cada entrada · selos "acesso imediato por e-mail" (cinza, esquerda) + garantia (verde: BR 7 dias, internacional 15) · seta pequena no rodapé do banner · confiança em ícone preto + texto · fluxo e-mail → bumps → forma de pagamento → botão de compra · total recalcula ao marcar bump · **pedido/cobrança criado UMA vez, só no clique em comprar**.
  - **Checkout de gateway** (Hotmart, Wiven, Mundpay, Cooud, Zenith, GG, Cakto, Stripe): NÃO é o modelo premium. Aplica o que o gateway permitir do mesmo padrão (timer 10 min que reinicia, texto do timer, garantia 7/15, acesso imediato por e-mail, banner) seguindo o bloco "Padrão de checkout da casa" da skill do gateway; o que o gateway não deixar configurar, avisar a dona. Azul de confiança é só Hotmart.
- **Tráfego só depois do `low-gates-no-ar` inteiro**, inclusive o aviso de venda 2xx nos 2 destinos e o link
  do checkout levando a sessão. "Configurei" não é prova.
- **Entregável nunca é HTML/código:** sempre imagem A4 do GPT com a referência visual. Item de fazer/imprimir
  (exercício, pôster, folha, checklist) = **página própria** depois da explicação.
- **Ofertas já ativas:** não migrar pro fluxo novo sem a dona mandar.
- **Fecho de toda sessão:** `low-ticket-salvar` — `STATUS.md` da oferta, ficha e índice atualizados. Regra nova
  da dona → arquivo certo + linha no `INDICE.md`. Esta skill só guarda o passo a passo; detalhe vai na filha.

Plano completo e mapa do que vem de onde: `CONHECIMENTO/PLANO-SKILLS-LOW-TICKET-V2.md`.
