---
name: ctv-edicao
description: Regras de edição de vídeo de anúncio do sistema LOW-TICKET — fonte única pra todo formato (demonstrativo, UGC, expert, caixinha, POV…): ordem de montagem, corte, layouts, velocidade, legenda, texto no topo, áudio, fecho com card CTA mudo, margem e QA. Use sempre que for montar ou revisar um vídeo de criativo.
---

# ctv-edicao — edição (fonte única)

**Vale pra TODO vídeo, de qualquer tipo** — inclusive o cru/orgânico ("feio" de celular): legenda, áudio,
fecho com card CTA e QA sempre entram; o que muda por formato é só o layout e o texto do topo.

**Todo formato com edição puxa daqui. Nenhum formato reescreve regra de edição** — formato só escolhe quais
blocos usa (tabela da `ctv-formatos`). Detalhe completo, com exemplos e porquês: `references/EDICAO-PADRAO.md`.

## Blocos
1. **Ordem de montagem (nunca pula):** roteiro completo → voz (VoiceStudio local → senão NaturalReader; ver `references/EDICAO-PADRAO.md` § Voz; conferir gênero da voz) e/ou
   clipe de personagem → alinhar a voz (tempo de cada frase) → escolher a cena de cada frase → montar no
   Remotion → trilha + card CTA → QA.
2. **Corte:** 1 clipe por frase da voz, a cena ilustra a frase · cortes de tela/b-roll 1,5–3 s · usar TODAS as
   gravações/fontes, cada vídeo um pouco de cada · gancho ≤ 2 frases e o material na tela até a 3ª frase ·
   a fala não promete o que a cena não mostra · gravação de tela limpa (sem barra, URL, selo "em breve").
3. **Layouts:** tela cheia · tela dividida 70/30 (entregável em cima, b-roll embaixo) · mesa real (1-2 aparelhos +
   3-4 folhas, página diferente em cada) · transição animada ~0,3 s na troca de layout, nunca corte seco de tamanho.
4. **Velocidade:** 1.0, ritmo natural da voz. Ajuste de ritmo é na fala gerada, nunca na timeline.
5. **Legenda:** sempre, igual em todo formato — karaokê v2 (Remotion, Montserrat 900).
6. **Texto no topo:** UGC = pequeno, estilo legenda de Story · expert/demonstrativo/caixinha = headline da promessa.
7. **Áudio:** uma fonte de voz só · trilha instrumental contínua −18 a −22 dB · fade 30–50 ms em toda junção.
8. **Fecho padrão (todo vídeo):** fala do CTA = só o comando curto ("Clica aqui embaixo e descobre") → o vídeo
   termina natural → **card ~5 s em silêncio**: fundo preto, mockup do plano Completo parado, seta pra baixo,
   CTA escrito.
9. **Formato:** 9:16 · margem de segurança: nada essencial no topo ~14%, na base ~20% nem colado nas laterais.
10. **QA (bloqueante):** assistir o vídeo inteiro (não frames soltos): voz sem eco, legenda casando, nenhuma cena
    repetida, nada cortado na margem, card no fim, acento certo.

## Bloco F — frame rate (regra fixa, 07/11/2026 — vídeo "travadinha" no CT18; confirma `EDICAO-PADRAO.md` §8)
- **Montar a 24 fps, o fps nativo do Flow/Veo.** O clipe do Flow entra **como veio**: sem `fps=30`, sem `minterpolate`,
  sem reencodar, sem mexer em quadro. Composição do Remotion `fps={24}`; o clipe toca 1 quadro por quadro.
- **Proibido** converter take de 24 fps para 30 (duplica quadro, trava) **e proibido interpolar** (suja o movimento).
- Gravação de celular/tela (VFR/30) e b-roll de banco entram na composição de 24 fps; o Remotion amostra, é o lado que perde menos.
- `startFrom` e durações do Remotion são em quadros da composição (24/s). Voz/legenda em segundos.
- **Gate do QA (bloco 10):** assistir a parte do clipe do Flow; medir quadro a quadro contra o arquivo original
  (cada quadro do render = quadro i do clipe, sem repetir nem voltar). Usar `OffthreadVideo` no Remotion (exato por quadro).

## Bloco E — só formato 13 (Explicador de mecanismo), 🧪 PILOTO desde 01/11/2026
Vem do estudo `CONHECIMENTO/ESTUDOS/2026-11-01-edicao-drive.md`. **Não vale pros outros formatos** até a dona aprovar
o piloto. Blocos 1-10 continuam valendo inteiros (legenda, áudio, produto cedo, card final).
- **E1 · Mapa de cenas antes de montar:** `cenas.json` com `de`, `ate`, `tipo`, `asset`, `frase`, `palavra_chave`,
  `layout`, `fonte`. O Remotion lê o mapa; trocar cena = editar o mapa, não o JSX.
- **E2 · Tipo de cena pela frase:** concreto/ação → cena real (gravação do entregável ou b-roll) · mecanismo
  invisível/causa → animação · vínculo/autoridade → pessoa.
- **E3 · Animações reaproveitáveis:** pulso, fluxo, antes/depois, barra, lista/check, seta — componentes com tema
  (cores do `DESIGN-SYSTEM.md` da oferta); fazer só as que a peça usa.
- **E4 · Enquadres da pessoa:** 2-3 crops aprovados do mesmo clipe, alternados nas voltas + push-in leve.
- **E5 · SFX com respiro:** só na entrada de animação/cena real, 4-5 sons em rodízio, ~1 em 4 cortes sem som,
  nenhum na volta à pessoa, baixo (abaixo da voz); card final continua mudo.
- **E6 · Rascunho + folha por cena:** render leve → 1 quadro do meio de cada cena numa folha numerada → corrigir →
  render final → QA do bloco 10 (assistir inteiro).

Regra nova de edição → entra aqui (e no `references/EDICAO-PADRAO.md`), em nenhum outro lugar.
