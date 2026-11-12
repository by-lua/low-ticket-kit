# Formato 14 — Imagem animada (4:5)

**O que é:** imagem de feed 1080×1350 que vira um `.mp4` de 7,2 s, sem som, com movimento leve por código:
zoom lento (1→1,05) · **selo de preço verde pulsando** ("Desde $7.900") · **seta vermelha pulando** apontando o botão ·
**botão CTA vermelho pulsando com mãozinha** (ou anel pulsando em volta do botão que já está na arte).
Referência de origem: CTV 6/7/8 do <Oferta Exemplo> FR (`<slug-da-oferta>/criativos/CTV-06…08`).
Primeira aplicação AR: CT19 (CT11 animado), CT20 (UGC com o Mapa), CT21 (mãos com páginas), em `<slug-da-oferta>/criativos/ES/`.

## Dois modos
1. **Animar uma imagem JÁ VALIDADA** (regra da dona 07/11/2026): imagem estática aprovada/que vendeu → gerar a versão animada **como peça nova**
   (nunca substitui a estática; as duas rodam). A arte base é a própria imagem 4:5; o botão que já está nela ganha o anel
   (`layout: ring`) ou, se a arte não tem botão, o botão vermelho entra por cima (`layout: pill`).
   ```bash
   ~/.claude/skills/ctv-formatos/scripts/animar-imagem/animar-imagem.sh <arte-4x5.png> <CTnn-IMG-es-v1-animado.mp4> exemplo-props-ring.json
   ```
2. **Nasce animada, do zero:** gerar no GPT uma **foto-base limpa, sem texto de CTA, sem selo, sem seta** (pessoa/UGC segurando o material,
   ou mãos com as páginas reais; mesma composição de uma referência que roda) em 4:5, e a camada animada entra por código
   (`layout: pill`; `band` opcional = faixa amarela de headline no topo, estilo CTV8).
   O que vira overlay (preço, CTA, seta, headline) NÃO é desenhado pelo GPT.

## Regras
- **4:5, 1080×1350 obrigatório** (o script recusa outra medida). GPT devolve 3:4 (1092×1440) ou 1122×1402: escalar a 1080 de largura e cortar a altura até 1350 (≈30 px topo) **antes** de animar; conferir que nada do texto da arte foi cortado.
- Peça NOVA = número novo de CT (`CTnn-IMG-fr-<origem>-anim-ar/`), final solto `CTnn-IMG-es-v1-animado.mp4` + `anuncio.md` (mesmo texto da peça de origem).
- **Preço no selo = o do plano mais barato** (AR: $7.900). Peça que na ficha é "sem preço" (carrossel) não ganha selo: `"price":""`.
- CTA do botão em espanhol: "RECIBIR AHORA". Headline da faixa (`band`) só no modo 2 quando a referência tem faixa.
- Pessoa: persona nossa (rosto novo, regra de pessoa de referência); material em cena = produto oficial de `ATIVOS.md`; papel impresso A4.
- Margem de segurança: botão e selo dentro de ~45 px das bordas; nada essencial no topo 14% / base 20% além do que a referência já faz.
- Sem som. Duração 7,2 s (`sec` ajusta).
- Registrar em `ATIVOS.md` §4 com "modelada de" = a imagem/CT de origem.

## Props (`props.json`, todos opcionais)
`price` · `cta` · `band` · `arrow` · `arrowX/arrowY` · `sec` · `badgePos` (`bl`|`tr`) · `layout` (`pill`|`ring`) · `ring{left,top,width,height}`.
Exemplos: `scripts/animar-imagem/exemplo-props-ring.json`, `exemplo-props-pill.json`.
