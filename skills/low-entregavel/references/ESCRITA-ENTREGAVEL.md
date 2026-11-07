# Escrita do entregável — método (06/11/2026)

O entregável é o que o cliente pagou. Texto errado gera reembolso e reclamação. Texto raso gera "não aprendi nada".

Casos reais que motivaram este método:
- **Auriculoterapia:** pontos no lugar errado. Um cliente da oferta apontou o erro.
- **Costura:** conteúdo raso, pouco técnico.
- **Jiu-jitsu:** termo inventado ("guarda de gancho"), instrução perigosa (escapar de heel hook girando)
  e cards criados só para bater o número "120 decisões" da página.

São dois defeitos diferentes:
- **ERRADO:** fato escrito de memória (ponto, termo, medida, técnica).
- **RASO:** conselho genérico, sem número, sem passo físico, sem material.

Este método ataca os dois. Ordem fixa: **pensar como especialista → pesquisar → escrever → revisar**.
Nenhum texto vira imagem sem passar pelos passos 0 a 6.

## Vale para qualquer oferta

O método é o mesmo em todo tipo de oferta. O que muda por tipo é o especialista, a fonte e o "fato" que
precisa estar certo:

| Tipo (exemplos do portfólio) | Especialista | Fonte de autoridade | Fato que não pode errar |
|---|---|---|---|
| Técnico com risco (mapas elétricos, eletrotécnica) | eletricista/engenheiro | norma do país (NBR 5410 no BR, norma local fora) e fabricante | bitola, disjuntor, ligação, aterramento, segurança |
| Saúde e terapia (auriculoterapia, kinesiologia, neuroactiva, gerineuro, atlas movimiento) | terapeuta da área, fisioterapeuta, TO, neuropsicólogo | livro-texto, associação profissional, artigo científico | ponto/músculo/exercício certo, faixa de idade, contraindicação, sem promessa de cura |
| Esporte (jiu-jitsu) | professor faixa preta | federação (IBJJF), livro técnico | nome da técnica, passos, regra por graduação |
| Ofício manual (costura) | profissional do ofício com ateliê | manual técnico, curso de especialista | medida, material, ordem de montagem |
| Idioma (atividades de espanhol) | professor nativo do idioma | RAE, Cervantes, livro didático | gramática, acento, gabarito, nível (A1–C2) |
| Esotérico (tarô, cigano, numerologia, calendário mágico) | taróloga/numeróloga da tradição escolhida | livros clássicos da tradição (ex.: Lenormand, Rider-Waite) | significado da carta/número segundo a tradição escolhida, tiragem, cálculo |

No esotérico, "fato" = o que a tradição diz. Escolha uma tradição, declare qual é e não invente significado.
Em qualquer tipo, cálculo e gabarito são conferidos à mão pelo revisor.

---

## 0. Pensar como especialista, antes de tudo: `produto/texto/ESPECIALISTA.md`

Antes de pesquisar e antes de escrever, quem escreve **vira o especialista** do nicho e planeja o produto
com a cabeça dele. Escreva este arquivo:

1. **Quem é o especialista:** formação, anos de prática, onde atua (exemplo: "acupunturista com formação em
   auriculoterapia chinesa, 15 anos de consultório"). Esse especialista é o autor de todo o texto.
2. **Quem é o leitor:** nível e o que ele já sabe.
3. **O que o especialista ensinaria** e um leigo esqueceria: os fundamentos que vêm primeiro, a ordem certa,
   os detalhes que separam quem sabe de quem não sabe.
4. **Erros de iniciante** que o especialista vê toda semana, e como ele corrige cada um.
5. **O que um profissional do nicho conferiria** ao abrir o produto e que geraria reclamação se estivesse
   errado (exemplo: localização de cada ponto, margem de costura, regra de graduação).
6. **Riscos e contraindicações** que o especialista nunca deixaria de citar.
7. **Perguntas técnicas a pesquisar:** a lista de tudo que precisa de fonte. Esta lista é a pauta do passo 1.

Plano sem a visão do especialista = texto genérico. Não pule este passo.

## 1. Pesquisa antes de escrever: `produto/texto/FONTES.md`

Escreva este arquivo antes de qualquer página. **A pesquisa é obrigatória**: cada pergunta do
`ESPECIALISTA.md` precisa de resposta com fonte. Use `WebSearch` com várias buscas, em `mode: "extended"` para
fato técnico de nicho, busque também no idioma de origem da técnica e leia a fonte (`ctx_fetch_and_index`);
nunca responda pelo resumo da busca. Pergunta sem resposta com fonte fica `[SEM FONTE]`.

- **De 3 a 5 fontes reais, em ordem de autoridade:**
  1. norma, órgão, federação ou associação profissional;
  2. livro ou manual técnico de autor reconhecido;
  3. curso ou aula de especialista, com transcrição (`PROJETOS-MIDIA/CURSOS/`, skill `yt-transcricao`);
  4. produto do concorrente, **só para estrutura, nunca como fonte de fato**.
  
  Para cada fonte, registre título, autor, link ou caminho e o que a fonte cobre.
- **Glossário:** `termo — definição — fonte`. Termo técnico fora do glossário não entra no texto.
- **Tabela de dados técnicos:** cada fato atômico com a fonte dele. Exemplos: ponto e localização, medida em cm,
  número da agulha, temperatura, tempo, regra de graduação. A escrita **copia da tabela**. Nunca escreva fato
  técnico de memória.
- **Escolas divergentes:** exemplo, auriculoterapia chinesa × francesa (Nogier), que têm mapas diferentes.
  Escolha **uma** escola. Declare a escola no `FONTES.md` e no texto ("mapa segundo ..."). Nunca misture escolas.
- **Fato sem fonte:** não escreva. Marque `[SEM FONTE]` e avise a dona.

## 2. Ficha de profundidade do nicho

Antes do texto, liste no `FONTES.md` os campos que um profissional do nicho espera ver numa página técnica.
Toda página técnica precisa ter esses campos. Página sem os campos está rasa: reescreva.

Exemplos:
- **Costura:** tecido, agulha (número), linha, ponto da máquina, comprimento do ponto, margem de costura em cm,
  ordem de montagem, acabamento, erro comum e correção.
- **Auriculoterapia:** nome do ponto (nomenclatura da escola escolhida), região anatômica da orelha (hélix,
  anti-hélix, concha cimba/cava, trago, antitrago, lóbulo, fossa triangular, escafa), indicação, material
  (semente, cristal, agulha), tempo de permanência, forma de estímulo, contraindicação.
- **Jiu-jitsu:** posição de partida, pegadas, base, passos em sequência, sinal do oponente, regra de graduação
  (IBJJF) quando houver finalização.

## 3. Escrever na voz do especialista

Escreva como o especialista do `ESPECIALISTA.md` explicaria ao vivo para aquele leitor. Siga a ordem dos
fundamentos do passo 0, cubra os erros de iniciante e os riscos listados lá. Cada fato técnico vem da tabela
do `FONTES.md`.

## 4. Molde de página técnica

1. **Objetivo:** o que o leitor consegue fazer ao terminar a página.
2. **Material ou pré-requisito.**
3. **Passo a passo numerado.** Cada passo tem uma ação física concreta e um número, quando o número existe.
4. **Como saber que deu certo.**
5. **Erro comum e correção.**
6. **Segurança e contraindicação**, quando o nicho tiver.
7. **Ação:** exercício ou folha `w` (`PAGINAS-DE-ATIVIDADE.md`).

## 5. Proibido

- Frase que repete o título ou a decisão com outras palavras.
- Conselho vago sem o "como" ("use a técnica certa", "mantenha a calma", "jogue de estrutura").
- Inventar nome de técnica, ponto, termo ou estatística.
- Item criado só para bater número da página. Se a página promete 120 e existem 60 conteúdos distintos de
  verdade, avise a dona. Nunca encha.
- Promessa de cura ou resultado garantido em saúde.
- Vícios de texto de IA: "não é X, é Y", travessão em excesso, trio de adjetivos. Passe a skill `humanizer` no fim.

## 6. Exemplo ruim × bom (Card 03, jiu-jitsu)

**Ruim (como saiu):**
> Oponente está mais pesado e mais forte. Decisão: CEDER o jogo de força e RESISTIR só nos pontos de estrutura
> (frame, base, ângulo). Detalhe-chave: contra quem é mais forte, jogue de estrutura.

O leitor não sabe onde põe o braço nem o que faz em seguida.

**Bom:**
> Você está por baixo, no 100 kg, contra alguém 20 kg mais pesado.
> Erro comum: empurrar o peito dele com os braços esticados, como num supino. O braço cansa em 20 segundos.
> 1. Antebraço de dentro no pescoço/ombro dele, antebraço de fora no quadril dele. Os antebraços **seguram**
>    a distância; não empurram.
> 2. Pés no chão, faça a fuga de quadril para o lado oposto ao dele, abrindo espaço entre vocês.
> 3. Coloque o joelho de dentro nesse espaço.
> 4. Recupere a guarda.
> Deu certo quando: o seu joelho fica entre vocês dois e o peso dele sai do seu peito.

## 7. A imagem também erra

Texto certo não garante imagem certa. O GPT inventa posição de ponto e desenha diagrama errado.

- Página com diagrama técnico (mapa de pontos, molde, posição do corpo): anexe ao GPT um **mapa ou molde real da
  fonte** como referência, e cite no prompt cada localização da tabela de dados.
- O GPT errou o diagrama 2 vezes: o diagrama vem da fonte (scan ou ilustração real, mesma regra da carta de
  tarô/cigano) e o GPT faz o resto da página.
- Depois de gerar, confira cada diagrama contra a tabela de dados (passo 8).

## 8. Revisão técnica obrigatória (gate)

**Antes de gerar imagem.** Quem revisa é outro pane, nunca quem escreveu, no papel de especialista sênior
do nicho. O revisor recebe `FONTES.md` e o texto. A saída é `produto/texto/REVISAO-TECNICA.md`:

| Página | Fato | Fonte | Veredito (OK / ERRADO / SEM FONTE) | Correção |
|---|---|---|---|---|

O revisor também confere:
- campos da ficha de profundidade presentes em cada página;
- segurança e contraindicação;
- repetição entre itens (principal, bônus, bumps);
- lista do passo 5.

**Aprovado** = zero ERRADO, zero SEM FONTE e todas as páginas com a ficha completa. Reprovado volta para a escrita.

**Depois de gerar:** a mesma revisão confere a imagem contra a tabela de dados (ponto no lugar, medida
legível, termo escrito certo). Registre o resultado no mesmo `REVISAO-TECNICA.md`.
