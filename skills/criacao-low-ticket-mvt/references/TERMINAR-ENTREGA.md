# TERMINAR A ENTREGA — receita (dona, 07/10/2026)

Gatilho: "termina/terminar a entrega", "completar o entregável", "o que falta na área de membros",
"ver o que prometemos × o que tem". Receita provada nos Mapas Elétricos 07/10 (OB1 e OB2 do zero → no ar
no mesmo dia). Repetir os 6 passos em ordem, sem pular. Orquestrador CONFERE e DELEGA; não gera.

## 1. Mapear (orquestrador, antes de qualquer pane)
Ler `OFERTAS/<slug>/CLAUDE.md` + `STATUS.md`. Cruzar 4 fontes e CONTAR (nunca confiar em manifesto velho):
- **Promessa:** página de vendas (`pagina/index.html` ou `site/index.html`) — nº de itens por produto ("+150 mapas", "30+ cenários"), bônus por plano, order bumps do checkout.
- **Painel:** `site/painel/index.html` (array de módulos: `pages`, `mvp`, `soon`) + `site/painel/conteudo/<sku>/` (ls/contagem).
- **Texto:** `produto/TEXTO*/` — contar entradas escritas por item (grep do padrão `**Ficha N`, `### Mapa N`…).
- **Imagens prontas:** `produto/<item>/` ou `produto/MVP/<item>/`.
Saída: `produto/MAPA-GAPS-<data>.md` = tabela item | plano/preço | promessa | texto | no painel | falta gerar | falta p/ MVP 40%,
+ ordem de execução + referências visuais por formato. Mostrar a tabela à dona (resumo) e seguir.

## 2. Escrever o que falta de texto
Item sem texto integral → escrever ANTES de gerar (todas as páginas, não só MVP). Texto pronto = segue.
**Texto pronto inclui a composição:** ficha que pede material (exercício, pôster, cartão, tabuleiro,
folha pra imprimir) tem a página `w` escrita junto, com conteúdo exato + composição + gabarito
(`PAGINAS-DE-ATIVIDADE.md`). Ficha só com a explicação = texto incompleto, volta e escreve.
No mapa (passo 1), contar as `w` que o texto pede × as que existem no painel.
A `w` também é imagem GPT 1×1 (passo 4), **nunca HTML/Pillow**.

## 3. Ordem
1º item que entrega ZERO e é vendido (bump/bônus vazio) → MVP 10 págs + capa → publica.
Depois: principal até MVP 40% → bônus → resto dos bumps → completar tudo.

## 4. Gerar no GPT — 1×1 no CHAT (sem Work mode)
Skill `gpt-imagem-playwright`. Worker Sonnet (`claude-sonnet-5`), 1 pane por conta, máx 2 panes, cada pane num item/pasta diferente:
- **Conta:** Pessoal `gpt-conta*` e Secundária `gpt-conta*` (via `gpt-livre.sh`). Cada worker fica na SUA conta; perfil com aba de outro trabalho → sobe outro perfil da mesma conta (`-2/-3/-4`). Headed sempre.
- **1 imagem por mensagem.** Toda mensagem anexa **2–3 páginas NOSSAS já prontas** do mesmo formato (depois da 1ª página aprovada do item, ela entra como referência) e diz:
  "A referência visual é esta (anexos). Cada página é uma imagem. A página que quero agora é esta:" + TEXTO INTEGRAL da página + tokens do `DESIGN-SYSTEM.md` + "CRITICAL: use o texto abaixo, não copie o texto da referência; mesmo formato/proporção das referências" + "sem brasão/logo de órgão público, sem marca/logo de fabricante".
- Salva cada imagem assim que sai (`pagina-NN-<slug>.png`, `capa.png`), abre e confere (é a do SEU prompt? texto pt certo? conteúdo técnico bate com o texto?). Errou → regera (máx 2×), anota em `QA.md`.
- Worker NÃO mexe em `site/`/painel. Reporta só em marco (item fechado) ou bloqueio real — nunca "trabalhando".
- **Cota:** "too many requests" = espera 2-3 min. Upload falha / card de limite = cota real da CONTA → anota hora e para o pane daquela conta (não usa a conta do outro worker); o item fica na fila da outra conta ou espera o reset. Chat antigo sem nossas refs ≠ saída; nunca gerar genérico.
- **Travou sem erro** (gpt-livre/`browsers.sh status` pendurado): ver `ps -o stat` do chromium — estado `T` = processo parado → `kill -CONT <pid>`.

## 5. Conferir (orquestrador) a cada item fechado
Contact sheet (`montage … -tile 4x2`) e olhar: layout igual às refs, texto, sem marca/brasão. Problema leve = anota e segue; grave = regera.

## 6. Publicar (pane publicador, 1 por item, fecha ao fim)
Mesmo padrão do item anterior já publicado (citar o commit de exemplo): webp em `site/painel/conteudo/<sku>/` + `original/`, `pages` + `mvp:true` no módulo, combo inclui o bump, commit + push (Coolify), conferir NO AR com a conta teste `teste@seudominio.com` (leitor + Baixar PDF, 390px e desktop), prints `prints/painel-<sku>-*.png`. Orquestrador abre 1 print antes de dar como feito. Print full-page do leitor mostra páginas em branco por lazy-load: prova = print da viewport na ÚLTIMA página (`*-leitor-mobile-ultima.png`) + todas as webp 200 na rede.
Atualizar `MAPA-GAPS`, `STATUS.md` da oferta (Histórico) e linha no STATUS da raiz. Tirar aviso "em atualização" do /painel só quando o último item prometido para o dia subir.
