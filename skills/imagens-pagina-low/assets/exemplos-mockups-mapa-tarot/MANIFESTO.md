# Manifesto de Mockups — Mapa do Tarô

Mapeamento das 10 imagens que serão substituídas pelas nossas versões design.

---

## Tabela de referência

| Arquivo | Seção da página | Alt atual | Dimensão aprox | O que a NOSSA versão deve mostrar |
|---------|------------------|-----------|-----------------|----------------------------------|
| `producto-basico.webp` | OPENING / VALUE (linha 146) · PLAN CARD — básico (linha 339) | "Mapa Completo del Tarot — guía visual en tablet" | 899×543px | Mockup em tablet/iPad mostrando a página-diagrama completa do produto básico. Fundo índigo `#1B1035`, moldura decorativa dourada `#C9A24B` nos 4 cantos, mapa visual de 1 arcano com layout: título + ilustração central + caixas de significado/símbolos/palavras-chave/luz-sombra/combinações em torno (conforme ESTRUTURA). |
| `producto-bundle.webp` | OFFER + PRICING — ITEM 01 (linha 271) · PLAN CARD — completo (linha 357) | "Mapa Completo del Tarot — con todos los materiales y bonos" | 1000×860px | Mockup em tablet/iPad mostrando o produto COMPLETO: capa do mapa + 1 página-diagrama visível + stack das 4 capas de bônus ao lado/abaixo. Paleta índigo/dourado, moldura decorativa. Comunica "set completo" — visibilidade dos 4 bônus. |
| `map-fool.webp` | METHOD / SOLUTION — PEEK INSIDE (linha 208) | "El mapa visual — El Loco (Arcano Mayor)" | 880×619px | Página-diagrama do Arcano 0 "El Loco" (Arcano Maior). Identidade: título + número + ilustração central + 5 caixas (Significado geral / Símbolos e elementos / Palavras-chave / Luz × Sombra / Combinações comuns) ligadas por setas douradas. Fundo índigo, moldura decorativa. |
| `map-knight.webp` | METHOD / SOLUTION — PEEK INSIDE (linha 209) | "El mapa visual — Caballero de Espadas (Arcano Menor)" | 880×619px | Página-diagrama de 1 Arcano Menor (Caballero de Espadas recomendado). Mesmo layout que map-fool (página-diagrama), mas visualmente distinto (palo de espadas). Paleta e moldura identidade. |
| `practice-fool.webp` | METHOD / SOLUTION — PEEK INSIDE (linha 215) | "La página de práctica — El Loco (Arcano Mayor)" | 880×618px | Página-exercício do Arcano 0 "El Loco". Identidade: título do arcano + 5 seções com linhas para preencher (Primeiras impressões / Símbolos que vejo / Associação pessoal / Pergunta pra tiragem / Notas / Resumo em 1 frase). Caderno (workbook), não mapa. Moldura dourada. |
| `practice-knight.webp` | METHOD / SOLUTION — PEEK INSIDE (linha 216) | "La página de práctica — Caballero de Espadas (Arcano Menor)" | 880×618px | Página-exercício do Caballero de Espadas (Arcano Menor). Mesmo layout caderno que practice-fool. Identidade: seções em branco com linhas para anotações. Moldura índigo/dourado. |
| `b1.webp` | BONUS SHOWCASE (linha 306) | "Bono 2 — Libro de las Tiradas" | 551×343px | Capa do Bônus 2 "Libro de las Tiradas" — 6 tiradas ilustradas. Design: título + ilustrações das 6 disposições (1 carta, 3 cartas, cruz, ferradura, relação, ano) em grid/showcase. Paleta identidade (índigo + dourado + creme). Moldura decorativa. |
| `b2.webp` | BONUS SHOWCASE (linha 322) | "Bono 4 — Guía Paso a Paso: Mi Primera Tirada" | 551×343px | Capa do Bônus 4 "Guía Paso a Paso: Mi Primera Tirada" — guia passo-a-passo para 1ª leitura. Design: título + 3–4 passos visuais (ex: baralho, gesto de tirada, interpretação). Paleta identidade. |
| `b3.webp` | BONUS SHOWCASE (linha 298) | "Bono 1 — Guía de Interpretación Intuitiva" | 551×343px | Capa do Bônus 1 "Guía de Interpretación Intuitiva" — símbolos, intuição, clareza de leitura. Design: título + ilustrações de símbolos-chave (copa, espada, ouro, vareta) ou figura em meditação. Paleta identidade (índigo + dourado + violeta `#6D4AA0`). |
| `b4.webp` | BONUS SHOWCASE (linha 314) | "Bono 3 — Cuidado y Conexión con tu Tarot" | 551×343px | Capa do Bônus 3 "Cuidado y Conexión con tu Tarot" — limpeza, proteção, conexão com baraja. Design: título + imagens de manuseio ritual (cristal, sal, vela, baralho). Paleta identidade com ênfase em dourado (sagrado). |

---

## Notas de design

### Identidade visual (ESTRUTURA-ENTREGAVEL)
- **Paleta:** Índigo profundo `#1B1035`, ameixa `#2E1A47`, violeta `#6D4AA0`, dourado `#C9A24B`, creme `#F5EFE6`
- **Moldura:** Decorativa dourada nos 4 cantos — presente em TODAS as páginas (coesão de workbook)
- **Tipografia:** Título serifada elegante (dourado), corpo sem serifa (creme sobre índigo)
- **Número de página:** Rodapé central em todas as páginas

### Tipos de página
1. **Página-diagrama (mapa visual):** 1 arcano, layout em estrela/caixa com setas douradas, significados conectados. Produto básico + páginas-diagrama no completo.
2. **Página-exercício (caderno):** 1 arcano, seções com linhas para anotações — prática e memorização ativa.
3. **Capas de bônus:** Cada bônus tem capa própria, mesma identidade, 4 estilos diferentes conforme conteúdo.

### Ordem de geração (recomendado)
1. Capa + 1 página-diagrama (El Loco) + 1 página-exercício → validar identidade
2. Bônus 1, 2, 3, 4 (capas)
3. Mockups de tablet (producto-basico, producto-bundle)
4. Gerar os 22 Arcanos Maiores em lote (2 páginas cada = 44 pags)

---

## Entrega
- Pasta: `/MOCKUPS-TROCAR/` (este diretório)
- Formato: PNG ou WEBP (otimizado, mesma qualidade do original)
- Destino final: `pagina-clone/assets/webp/`
