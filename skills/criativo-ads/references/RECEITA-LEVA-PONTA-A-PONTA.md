# Receita — leva de criativos de uma oferta, de ponta a ponta

Pra qualquer agente que não sabe nada do projeto. Pedido do tipo "faz os criativos da oferta X" = seguir isto
na ordem, sem pular etapa. Cada etapa tem uma prova (script ou arquivo). Sem a prova, não avança.
Referência viva (feita assim em 23/10/2026): `OFERTAS/luciola-atlas-movimiento/criativos/`.

## 0 · Carregar
Skill `low-ticket-painel` (estado do negócio) → `OFERTAS/<slug>/CLAUDE.md` + `STATUS.md` + `trafego/ANALISES.md`
(o que já vendeu ou não). Copiar os nossos vencedores (mesmo de outro idioma/nicho) já é peça de teste.

## 1 · Persona com dado → `gate-persona.py`
- Pesquisa: `~/.claude/skills/criacao-low-ticket-mvt/references/PESQUISA-PADRAO-OFERTA.md`. Começa pela página do
  anunciante modelado (narrativa que mais repete e mais dura = espinha da leva). Depois Biblioteca com 5 palavras +
  1 hashtag por idioma, YouTube/TikTok/Trends com contagem e data.
- Arquivo: `pesquisa/PERSONA-E-ANGULOS.md` no modelo `MODELOS/_MODELO-PERSONA-E-ANGULOS.md`.
- Prova: `python3 ~/.claude/skills/criacao-low-ticket-mvt/scripts/gate-persona.py OFERTAS/<slug>` = LIBERADO.
- Lição: Elétrica estudou o estudante (quem compra é o eletricista); Jiu usou "faixa branca" (só vendeu sem isso).
  Termo do gancho vem do Trends, não do nome do produto ("atlas" = 0 busca).

## 2 · Material e marca
- `DESIGN-SYSTEM.md` da oferta (cores/fonte tirados da página no ar). Sem ele a cor sai errada.
- Páginas REAIS do entregável em `criativos/PAGINAS-REAIS/` (do painel, da página no ar ou do `produto/`).
  Capa sem selo de PDF. Gravação de tela em `criativos/MATERIAL-ENTREGAVEL/` antes de qualquer vídeo.

## 3 · Plano em texto → `gate-plano-leva.py` → OK da dona
- 30 peças: 3 campanhas 1-1-10 (alternar 7 img + 3 vídeo / 6 + 4) ou 10 × 1-1-3. Toda campanha tem vídeo,
  estático e carrossel; ≥ 2 vídeos por campanha; imagem ≥ vídeo (70/30 ou 50/50, nunca 70% vídeo).
- Orçamento: oferta < R$47 = 60-65% do ticket médio por campanha (arredonda pra cima, sem centavo); ≥ R$47 = R$30-35.
- Personagens fixos: expert (combina com produto/país, ambiente de autoridade, voz fixa) + 2 UGC (carro, cotidiano).
- `criativos/PLANO-LEVA-1.md` + `criativos/CRONOGRAMA-LEVA-1.md` (peça por peça: como fica, quais páginas em qual
  aparelho/folha, texto). Variar gancho (corte YouTube / cena TikTok / material) × função (dor, objeção, narrativa,
  material) × formato. 1 peça com preço por campanha.
- Prova: `python3 ~/.claude/skills/criativo-ads/scripts/gate-plano-leva.py OFERTAS/<slug>` → mostrar pra dona →
  `- [x] OK da dona` → `--producao` = LIBERADO.

## 4 · Regras de cada imagem (o que mais erra)
- **Ugly iPhone = ESTILO da foto**, não aparelho em cena: foto feia de celular, meio torta, luz imperfeita, grão,
  sem retoque, cara de story espontâneo. Lugar real que faz sentido pra persona (academia, aula, mesa, carro).
- **Digital + impresso sempre** quando mostra o produto: **3-4 páginas impressas soltas + 1 ou 2 aparelhos**
  (celular, tablet, notebook, em qualquer combinação). **Nada repete:** o que está numa tela não aparece em outra
  tela nem nas folhas.
- **Texto = texto de Stories** digitado (caixinhas brancas com texto preto ou o inverso, fonte do IG). Nunca arte
  de designer, nunca botão "Saiba mais", nunca interface do Instagram.
- **Preço = sempre o plano mais barato.** Nunca "PDF", nunca mockup, nunca prova social inventada.
- **Caixinha de pergunta:** quem responde é sempre o expert.
- **Impacto** (exceção, só texto): fundo branco, texto preto + vermelho.
- Feed 4:5 (1080×1350); story 9:16 com safe area.

## 5 · Montar cada peça → `gate-pecas-criativo.py`
Pasta `criativos/CRIATIVO-NN-<slug>/`:
- `selecionados/` = SÓ o que entra: páginas reais (uma por aparelho/folha) + capa se aparece + **REF-FORMATO-***
  (referência de estilo/formato, obrigatória):
  - cena orgânica: `~/.claude/skills/criativo-ads-video-orq/references/organico-iphone/ref-recorte-impresso-mesa.jpg` e `ref-recorte-tablet-mesa.jpg`
  - caixinha: `~/.claude/biblioteca-escalados/formatos/estatico/caixa-de-perguntas/70-*.jpg` e `90-*.png`
  - impacto: `organico-iphone/ref-impacto-layout-texto.jpg` (inverter pra branco/preto/vermelho)
  - outros formatos: `~/.claude/biblioteca-escalados/CATALOGO.md` (recortar a UI do print antes)
- `intermediarios/prompt-vN.txt` no molde `PROMPT-ESTATICO-ORGANICO.md` (inglês, uma linha, sem aspas).
- Prova: `python3 ~/.claude/skills/criativo-ads/scripts/gate-pecas-criativo.py <pasta>` = LIBERADO.

## 6 · Gerar
- Sessão: `S=$(~/.claude/bin/gpt-livre.sh <lane> | tail -1)` → `agent-browser --session $S navigate https://chatgpt.com/`
- `bash ~/.claude/skills/criativo-ads/scripts/gerar-imagem-gpt.sh $S prompt.txt saida.png <páginas...> <REF-FORMATO...>`
  (1 imagem por chat novo; confere anexo, envio, dono do chat e baixa). Várias peças = fila em série (ver
  `OFERTAS/luciola-atlas-movimiento/criativos/_fila/fila-estaticos.sh`), parando se a cota acabar.
- Cota acabou ("limite de criação de imagens") = `gpt-livre.sh --esgotou secundaria HH:MM` e agendar pra depois.
- Personagem: a 1ª imagem aprovada do expert vira referência de rosto das próximas (mesma pessoa sempre).

## 7 · Conferir e entregar
Olhar cada imagem em tamanho cheio: texto e acentos certos, páginas reais (não redesenhadas), nada repetido,
digital + impresso, sem botão/UI. Recortar pra 4:5. Final na raiz da pasta da peça. **Mostrar toda peça pronta
pra dona**; a 1ª de cada etapa (estático, caixinha, impacto, carrossel, vídeo) é aprovada antes do resto.

## 8 · Gravar
Progresso no `PLANO-LEVA-1.md` + `_memoria/planos-criativos.md` + `STATUS.md` da oferta e da raiz; hub
(`HUB-OFERTAS/sincroniza-ofertas.py` → `uv run cifrar.py` → push).

## Vídeo (depois dos estáticos)
Skill `criativo-ads-video-orq`: imagem da cena no GPT primeiro → Flow ≤ 8s → expert só no começo (tela cheia ou
meio a meio com o material) → material + VO (voz fixa, idioma dito no prompt) → CTA com seta "toca en más
información" segurada uns segundos. B-roll: TikTok > Pexels > YouTube, no idioma da persona, mais visto sem texto.
Toda campanha com ≥ 2 vídeos, 1-2 com b-roll 3D quando a oferta tiver.
