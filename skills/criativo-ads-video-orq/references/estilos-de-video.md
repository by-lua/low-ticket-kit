# GUIA DE VÍDEO — modos de criativo (índice único, revisado 26/10/2026)

Os modos vêm do método do Rodrigo (a base, vale inteiro: UGC contando a experiência, expert,
demonstrativo) somado ao que a dona já fixou (caixa de perguntas, expert respondendo, imagem
animada…); a biblioteca de escalados é opção extra. Rodrigo ensina a estrutura do texto;
visual e edição seguem as NOSSAS regras.

Todo vídeo da leva é UM modo desta tabela. **O modo decide O QUE:** o roteiro, quem fala e
quais cenas entram. **A edição é sempre a mesma** — `EDICAO-PADRAO.md` (corte por frase,
layouts, legenda KaraokeV2, velocidade 1.0, trilha, card CTA, QA). Nenhum modo tem edição
própria e nenhum dispensa a edição padrão. Ninguém precisa dizer "edita no estilo X".

Onde cada coisa mora:
- **Roteiro de cada modo** → `criativo/references/ROTEIRO-POR-FORMATO.md`
- **Edição de todos** → `EDICAO-PADRAO.md`
- **Gerar personagem/take no Flow** (imagem → vídeo, dentes, voz, anti-morphing) → `SKILL.md` FASE 3–5 + `mecanica-flow.md`
- **Takes "mesa real" (catálogo A–O)** → `SKILL.md` §E.0c

## Os modos

| Modo | O que é | Roteiro | Cenas que entram (arco) | Quem fala | Não confundir |
|---|---|---|---|---|---|
| **Demonstrativo** | mostra o entregável por dentro | gancho um nível mais fundo → corpo ecoa a palavra do gancho → CTA | b-roll do assunto (hook) → entregável tela cheia ("olha esse material") → split 70/30 no mecanismo → b-roll até o CTA. Fontes misturadas: gravação de tela real + take mesa real (Flow) + b-roll | voz off | gancho ≤ 2 frases curtas, já mostrando o material |
| **Expert** | autoridade do nicho explica o mecanismo | dor ou contraste → mecanismo (POR QUE funciona) + frase de autoridade ("estudei X anos… coloquei tudo aqui") → CTA | expert **segurando o material aberto (livro/apostila encadernada) e falando a copy inteira em quadro**, ambiente de autoridade; 2 clipes de 8 s da mesma pessoa quando não couber em 1; corte curto pro material por dentro é opcional | o próprio expert (lip-sync) | nunca "rosto só no gancho + voz off em cima da tela" (erro Atlas 24-25/10) |
| **UGC comprador** | 1 pessoa comum dá relato em 1ª pessoa | identificação ("eu também…") → "existe um jeito" → prova pessoal → gatilho → CTA | a pessoa com o material **em quadro falando a copy inteira** — apresentação varia: segurando como livro (fechado/aberto), pegando da estante, impresso na mão, tablet/celular com a capa — em cenário cotidiano (carro / casa), cenas geradas SÓ pra ela + cortes de b-roll do contexto | a própria pessoa | **NÃO mostra o entregável por dentro** (isso é expert/demonstrativo); nunca take genérico de mão do banco; mão nua = reprovado; cenário diferente do expert |
| **Caixa de perguntas / expert respondendo** | pergunta de story + expert responde | pergunta real (dor/objeção) → resposta com mecanismo → CTA | caixa de pergunta estilo story → expert respondendo com material na mão → material | sempre o **expert** (nunca UGC) | — |
| **Imagem animada** | slide estilo Canva que se mexe | título-gancho + desenvolvimento + CTA | título + elemento que se move e faz sentido (mão embaralhando, carta virando) → páginas | voz off ou só texto | conta como vídeo na leva |
| **Corte TikTok / b-roll viral** | abre com cena orgânica real que já viralizou | gancho falado por cima da cena → material → CTA | 15–20 cortes curtos alternando cena real (TikTok, sem texto queimado) e material | voz off | origem em `credits.md` |
| **Print + POV + Meme** | prova/resultado sem rosto | POV em 1–2 linhas | print real (topo) + texto POV (meio) + meme recortado (base), fundo preto | sem voz (som opcional) | só com print REAL (prova não se fabrica) |
| **Copo azul (variação do vencedor)** | mesmo produto + copy do vencedor, troca quem/onde | o do vencedor | o do modo do vencedor, com outra pessoa/ambiente | idem | peça nova, campanha nova; nunca só trocar gancho |

**Variante opcional do demonstrativo — headline fixa (dona, 26/10/2026: só como teste, quando ela pedir):**
uma linha curta e fixa com a promessa do produto (nunca contagem nem bônus — dona 27/10) durante o vídeo, dentro da
área segura e sem brigar com a legenda KaraokeV2. Não é o padrão; o demonstrativo que funciona continua sem ela.

Produto "vibe"/não-material (ex.: número mestre): UGC pode ser "entrevista de rua", sem segurar material.

## Passo 0 — mapear TODOS os assets antes de montar

Toda oferta com criativo em produção mantém `criativos/ASSETS-MAPA.md` (o que existe em
`MATERIAL-ENTREGAVEL/`, `FLOW-TAKES/`, `BROLL-3D/`, card CTA pronto, trilha). Ler primeiro e
atualizar na hora. Se não existir, criar antes do 1º vídeo (exemplo: `OFERTAS/luciola-atlas-movimiento/criativos/ASSETS-MAPA.md`).

```bash
find criativos/MATERIAL-ENTREGAVEL -iname "*.mp4"   # gravações reais de tela (sempre a 1ª parada, usar TODAS)
find criativos/FLOW-TAKES -iname "*.mp4"             # takes mesa real já gerados (reusar antes de gerar)
find criativos/BROLL-3D -iname "*.mp4"               # b-roll 3D (o clipe que casa com o roteiro)
find criativos/*/VIDEO -iname "cta-card*.mp4"         # card CTA de outra peça da leva (reusar)
```
Gravação de tela é SEMPRE da dona — faltou, pede; nunca gerar substituto.

## Checklist por vídeo

1. Nomear o modo (linha da tabela) antes de começar.
2. `pesquisa/PERSONA-E-ANGULOS.md`: quem fala, que dor, que ângulo, personagem fichado.
3. Roteiro completo (hook → mecanismo → CTA) pelo `ROTEIRO-POR-FORMATO.md` — nunca só a frase do plano.
4. Gerar o que o modo pede (voz, clipe de personagem, take) — mecânica no `SKILL.md`.
5. **Montar pelo `EDICAO-PADRAO.md`, do 1 ao 9.**
