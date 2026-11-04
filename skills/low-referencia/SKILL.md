---
name: low-referencia
description: Etapa E1 (porta manual) do sistema LOW-TICKET — a dona achou uma oferta na Biblioteca e manda o link + explicação. Salva tudo cru, abre a página e o checkout do anunciante, baixa as imagens da página e escreve o REFERENCIA.md. Use quando a dona mandar link de anunciante/anúncio/página pra modelar, ou "achei essa oferta".
---

# low-referencia — E1, porta manual

**Entrada:** link (Biblioteca do anunciante, anúncio ou página de vendas) + o que a dona explicou.
**Saída:** `OFERTAS/<slug>/pesquisa/da-dona/<AAAA-MM-DD>-<assunto>.md` · `pesquisa/REFERENCIA.md` ·
`pesquisa/referencia/imagens-origem/*`. Depois: `low-modelador`.

## Passos
1. **Salvar cru ANTES de pensar.** `pesquisa/da-dona/<data>-<assunto>.md`: link exato, texto da dona **literal**
   (sem resumir), data, prints que ela mandou (copiar pra mesma pasta). Nada que a dona manda se perde.
2. **Pasta da oferta.** Não existe → criar `OFERTAS/<slug>/` no padrão (skill `organizar-projeto`), slug curto
   + sufixo de mercado se precisar (`-ar`, `-us`). Oferta já ativa: não mexer em nada além de `pesquisa/`.
3. **Abrir a página até o checkout** — `agent-browser` com perfil do sistema (`~/.claude/docs/browsers.md`; nunca
   `agent-browser open` cru). Ler do topo ao rodapé; seguir quiz/VSL; abrir o checkout (preço, bumps, gateway).
4. **Baixar TODAS as imagens da página** (todo `src`, inclusive lazy) → `pesquisa/referencia/imagens-origem/`,
   nomes em ordem de aparição (`01-hero.webp`…).
5. **Escrever `pesquisa/REFERENCIA.md`:**
   - anunciante, link da Biblioteca, nº de anúncios ativos, há quantos dias roda o mais antigo, país/idioma;
   - o que é (1 frase) · entregável · bônus · garantia · preço e planos · order bumps · upsell/downsell · gateway;
   - o que protege a oferta (o que é difícil de copiar);
   - **tabela das imagens baixadas**: arquivo · o que mostra (mockup, página por dentro, mapa, pôster, folha de
     exercício, depoimento) · seção onde aparece. É a base visual da página (E3/E5) e do entregável (E4);
   - o que não deu pra ver.
6. **Vídeos dos anúncios** (se for modelar criativo): baixar em
   `~/Documentos/TRAMPO/PROJETOS-MIDIA/CRIATIVOS-CONCORRENTES/<SLUG>-<assunto>/` (mídia de terceiro não
   fica na pasta sincronizada — ver `PROJETOS/CLAUDE.md`), symlink em `pesquisa/referencia/videos`.
   Transcrição e análise: `ctv-modelar-concorrente`.
7. Devolver à dona: 5 linhas (o que é, preço, funil, quantas imagens baixadas, o que faltou) → `low-modelador`.
