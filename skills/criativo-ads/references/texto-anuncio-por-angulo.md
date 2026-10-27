# Método de copy do criativo — imagem, vídeo e texto do anúncio

**Fonte única** de como escrever o texto de qualquer peça (o que vai NA arte, o que é FALADO no
vídeo e o `anuncio.md` de fora). As outras skills apontam pra cá.

Fontes (reescrito 27/10/2026, a pedido da dona — "pega o conceito"):
- **Rodrigo Liedson**, leva 1-3-9 da saga Europa parte 2 (`HBPMwsVGpRc`) + aulas de imagem
  (`a_GQT1ZgWtM`, `kFnDYkBoHak`) — transcrições em
  `LOW-TICKET/CONHECIMENTO/FONTES-DE-CONHECIMENTO/RODRIGO-LIEDSON/TRANSCRICOES/`, resumo em
  `LOW-TICKET/MINERACAO/referencia-rodrigoliedson/METODO-RODRIGO-EUROPA-139-SAGA-COMPLETA.md`.
- **Kevones**, live 23/10/2026 (`Fo3EFSn7LeI`) — narrativas como pontos de contato.

> **Não fazemos teste de 5 títulos / 5 textos / 5 descrições por anúncio** (dona, 27/10/2026), mesmo
> o Kevones citando isso num curso antigo. Cada peça sai com **1 copy fechada**; a variedade vem de
> peças com narrativas diferentes, não de variar título no gerenciador.

## ⛔ O criativo fala do PRODUTO, não de bônus nem de volume (dona, 27/10/2026 — já tinha dito antes)

O que a pessoa compra é **um produto só**. A copy (arte, fala e `anuncio.md`) fala **do material e do que
ele faz por ela** — nunca lista **bônus** ("+100 actividades del bonus Etapa avanzada", "4 bonus"),
**contagem/volume** ("400 fichas", "5 módulos", "1.395 páginas", "150 mapas") nem **nome de módulo/volume**
("Volumen 2", "Armador de Sesiones"). Bônus e quantidade são assunto da página de vendas, não do anúncio.
Certo: "fichas ordenadas por nivel: abrís, elegís y aplicás" · "sirve también para etapa avanzada".
Errado: "400 fichas, 5 volúmenes y 4 bonus" · "el bonus con +100 actividades".
A peça pode **mostrar** o material inteiro (páginas, aparelhos, folhas) — só não **fala** contagem nem bônus.

## 0 · De onde sai a copy (antes de escrever)

1. **Página de vendas** da oferta: `<h1>`, promessa, mecanismo, o que recebe. O Rodrigo cola a
   página no GPT e pede a copy a partir dela — a copy do criativo **promete o que a página promete**.
2. **`pesquisa/PERSONA-E-ANGULOS.md`**: a dor medida daquela peça (texto exato, com fonte e
   contagem). O código D1/D2 é ponteiro, não título.
3. **`produto/MANIFESTO-ENTREGAVEIS.md`**: o que entra como "entrega concreta" tem que existir.
4. **Papel da peça no plano** (Kevones): geral/apresentação · dor · objeção · preço/cupom · prova
   real · demonstração. *"Quanto mais ângulos você tiver, melhor"* — cada peça é um ponto de contato;
   tirar um tira consciência. A copy serve o papel: peça de objeção responde a objeção, peça geral
   mostra o que tem, peça de preço filtra curioso.

## 1 · IMAGEM (estático, card 1 do carrossel) — 3 andares

Rodrigo: *"criativo em imagem precisa ser direto e sem curiosidade"*. Estrutura que ele monta em
todas as aulas:

| Andar | O que é | Exemplo dele | Exemplo nosso |
|---|---|---|---|
| **Headline** (maior texto) | a **promessa** ou o **benefício principal**, ligado à dor medida | "Faça qualquer homem ficar obcecado por você" | "Aprenda a ler o Tarot sem decorar nenhuma carta" (AD 03, 32 vendas) |
| **Texto de baixo** (1 linha) | o **mecanismo** — COMO a promessa acontece / o que o produto faz por ela (sem contagem, sem bônus) | "princípios psicológicos que fazem ele sentir sua falta" · "5.000 esboços prontos pra pregar" | "um mapa por carta: significado, símbolos e combinações" |
| **CTA** | comando curto | "baixe agora" | "toca em saiba mais" |

- **Variante "dor em cima"** (Rodrigo, sermões): headline = a dor do público ("dificuldade pra
  preparar o sermão toda semana"), texto de baixo = o que resolve ("5.000 esboços prontos pra
  pregar"). Usar quando a dor da peça está **medida** no PERSONA-E-ANGULOS.
- **Clássica com preço** (só 1 peça da leva): headline + subheadline + produto + **preço** + texto
  de apoio embaixo. Preço = plano mais barato. *"Coloca o preço de cara porque não quer curioso."*
- **Só texto** (consciência, sem produto, sem preço): uma frase de impacto que nomeia a dor — é a
  única peça que não precisa mostrar o que vende.
- **Gate de 1 segundo:** olhando a peça, dá pra saber **o que é, pra quem é e o que entrega**?
  Curiosidade pode abrir, nunca esconder o produto.
- **No nosso visual** (orgânico iPhone, `PROMPT-ESTATICO-ORGANICO.md`): headline = 1ª caixa de texto
  de Stories, texto de baixo = 2ª caixa. Mesmos 3 andares, só a estética muda.

**Reprovado — rótulo de seção sozinho** (erro real, Tarot AR leva 9, 26/10): "Lado luz y lado
sombra", "Cada símbolo, explicado", "Amor, trabajo y dinero en una página", "400 fichas. Una por
hoja.". Isso é o andar do meio sem o andar de cima: diz uma parte do material, não promete nada nem
toca dor. O `gate-imagens-finais.py` lê o Título do `anuncio.md` e reprova (FALHA "título-rótulo").

## 2 · VÍDEO — gancho na dor → mecanismo → CTA

Rodrigo: *"toca na dor no primeiro momento, depois desenvolve o mecanismo, depois chama pra ação"*.
Exemplo literal dele (15 s):

> **Gancho (dor):** "Quer saber como fazer ele sentir sua falta sem ficar correndo atrás?"
> **Mecanismo:** "Existe uma forma de criar um espaço emocional que faz ele perceber sua ausência
> e começar a valorizar sua presença."
> **Ponte pro produto + CTA:** "Eu descobri nesse livro. Clique pra conhecer."

- **Mecanismo = "existe uma forma de [X] que faz [Y]"** — explica POR QUE funciona, nunca repete a
  promessa com outras palavras (erro mais caro documentado, CRIATIVO-02 Atlas).
- **Headline fixa no topo** do vídeo com a **promessa** ("Descubra como fazer ele sentir sua falta").
- **Fórmulas de gancho:** "A maior pressão não é [X esperado], é [Y real]" · "Se você é [público],
  precisa ver isso" · "Veja isso antes de [ação do dia a dia do nicho]".
- **UGC:** relato em 1ª pessoa ("isso aconteceu comigo… foi o que aprendi nesse material"),
  até 15 s. Roteiro por formato e edição: `ROTEIRO-POR-FORMATO.md` + `EDICAO-PADRAO.md`.
- CTA final = só comando (memória `cta-video-so-comando`).

## 3 · Texto do anúncio (`anuncio.md`) — o que vai fora da arte

> **⛔ GATE BLOQUEADOR (dona, 26/10/2026 — NeuroActiva AR):** a **primeira frase** do Texto
> principal chama quem compra, nunca descreve o produto. "400 fichas, 5 volúmenes..." descreve;
> "Si coordinás sesiones para adultos mayores..." chama. ("Si sos...", "Si tu mamá...",
> "¿Trabajás con...?").

- **Texto principal:** 1ª frase endereça a persona/situação → mesmo ângulo da peça (dor ou objeção)
  → mecanismo em 1 frase → convite. Curto.
- **Título:** a headline da peça (promessa/benefício) ou a dor em frase. Mesmas regras do §1.
- **Descrição:** o que o produto faz pela pessoa, sem repetir o título (sem contagem, sem bônus).
- **1 copy por peça** — sem lista de 5 variações.

```markdown
# Anúncio — [nome do criativo]
Mercado: [BR / PT / ES] · Formato: [vídeo / imagem / carrossel]
Papel: [geral / dor / objeção / preço / prova / demonstração]
Persona/dor: [texto da dor medida + fonte]
Arquivo: [nome exato da mídia]

## Texto principal
[1ª frase chama a persona → ângulo → mecanismo → convite]

## Título / headline
[promessa ou dor em frase — nunca rótulo]

## Descrição curta
[o que o produto faz — sem contagem nem bônus]

## CTA sugerido
Saiba mais
```

## 4 · Exemplos reais com resultado — Mapa do Tarot BR

| Peça | Copy | Resultado |
|---|---|---|
| AD 03 (imagem) | "Aprenda a Ler o Tarot Sem Decorar Nenhuma Carta" | **32 vendas**, ROAS 1,85–1,97 |
| AD 04 IMG | "Aprenda a ler Tarot de forma visual e prática" + página real | **22 vendas**, CPA R$ 8,55–14,22 |
| CT 12 IMG | sem texto, mesa com páginas reais | 19 vendas |
| CT 34 V (vídeo) | combinações — abre na tela do produto, promessa direta | 3 vendas, ROAS 1,68–2,03 |
| CT 10 (imagem) | "A carta sozinha não diz nada" — dor como frase solta, sem promessa | desligado, 0 venda |
| CAOS-1/2/3 (vídeo) | caos/dor antes do produto | CTR alto, CPA R$ 29–42 — pior do painel |

**Leitura:** o que vende é **promessa direta contra a dor + produto real visível**. Dor sozinha
(sem promessa e sem o que entrega) não vendeu em imagem. A dor das combinações é medida
(YouTube 26 mil views + Biblioteca + 3 vendas) e vendeu em **vídeo**, onde dá pra desenvolver o
mecanismo.

## 5 · Conferência antes de dar a copy por pronta

1. A headline **promete** (ou nomeia uma dor medida) — não é rótulo de seção?
2. O texto de baixo diz **como** ou **o que recebe**, e isso existe no MANIFESTO?
3. Gate de 1 s: o que é, pra quem, o que entrega.
4. Vídeo: o corpo tem **mecanismo** ("existe uma forma de…"), não só a promessa repetida?
5. `anuncio.md`: 1ª frase chama a persona; idioma/sotaque do mercado (BR brasileiro, PT europeu,
   AR voseo); nada de previsão certa, dom ou resultado garantido; nunca "PDF".
6. Cada peça da leva com **papel** diferente — o mesmo texto com outra cor é a mesma peça.
