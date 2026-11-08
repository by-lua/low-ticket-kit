---
name: ctv-imagem
description: Produz criativo de imagem (estático e carrossel) do sistema LOW-TICKET a partir da ficha da leva aprovada — gera no GPT com as regras de cara orgânica, páginas reais, texto dentro da foto e 4:5. Use para gerar estático, carrossel, ugly iPhone, frase direta, antes e depois, caixinha em imagem.
---

# ctv-imagem — estático e carrossel

**Entrada:** linha aprovada da `FICHA-LEVA` · páginas reais do entregável (`produto/ENTREGA/`) · `OFERTA.md`.
**Saída:** `criativos/<MERCADO>/CRIATIVO-N/` com a arte final + `anuncio.md` (texto, título, descrição, CTA).

## Regras de toda imagem
- **4:5, 1080×1350** (estático e todo card do carrossel).
- **Cara orgânica:** foto amadora de iPhone, levemente torta, luz natural, grão — nunca render de IA nem estúdio.
- **Texto escrito pelo agente** (copy da ficha) e **desenhado pelo GPT dentro da foto** (cara de legenda de Story),
  nunca faixa/overlay por código. **Exceção: formato 14 Imagem animada** — selo de preço, botão CTA e seta são a camada de animação por código (`ctv-formatos/formatos/imagem-animada.md`); a foto-base continua sem esses elementos.
  Ortografia e acento conferidos palavra por palavra; errou → regerar.
- **Páginas reais do entregável**, nunca mockup nem folha falsa. Cena com produto = 1-2 aparelhos + 3-4 folhas
  impressas, **cada um mostrando uma página diferente**.
- **Margem:** nada essencial no topo ~14% nem na base ~20%.
- Preço só do plano mais barato e sempre junto do nome do produto. **Carrossel nunca tem preço**, ≥ 5 cards.
- Nunca "PDF", bônus, volume ou contagem na arte.

- **Peça com pessoa** (caixinha, antes e depois, iPhone com gente): mesma regra de referência real do país da
  `ctv-video` (Pinterest → pessoa NOVA no GPT, nunca o rosto da foto).

## Como gerar
Mecânica: `criativo-ads-imagem` (prompts e tipos) + `gpt-imagem-playwright` (perfil livre, download).
Carrossel de páginas: recortar a página A4 do topo até fechar 4:5. Formato da peça: `ctv-formatos`.
Fecho: tudo da leva pronto → `ctv-revisor`.

**Imagem validada (aprovada ou que vendeu) → animar:** gerar a versão animada como peça nova com `ctv-formatos/scripts/animar-imagem/animar-imagem.sh` (formato 14). Também dá pra gerar já animada: foto-base limpa + camada por código.
