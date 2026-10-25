---
name: low-ticket-salvar
description: >
  Salva manualmente o estado atual no portfólio LOW-TICKET, fora do fluxo de uma tarefa — dispara
  a FASE 3 (grava o estado) de `low-ticket-painel` sozinha, sem precisar terminar nenhuma produção.
  Use quando a dona disser "salva", "salva e sai", "grava o que a gente conversou", "/salvar", ou
  quiser registrar uma correção/decisão sem seguir executando mais nada agora.
---

# /low-ticket-salvar — salvar estado avulso

LOW-TICKET não é repositório git (sincroniza por Syncthing) — "salvar" aqui não é commit, é
garantir que tudo que mudou na conversa virou arquivo em disco antes de fechar a sessão.

## Workflow

1. Revisar a conversa desde a última gravação (ou desde o início da sessão): o que foi decidido,
   corrigido, produzido, descoberto?
2. Pra cada item, aplicar a FASE 3 de `low-ticket-painel` que for pertinente:
   - Entrega/quantidade → `auditar-entregaveis-oferta --registrar`.
   - Fase/pendência/bloqueio → `STATUS.md` da oferta + "Atualizado em".
   - Linha no `STATUS.md` raiz.
   - `PANORAMA.md` raiz, só se mudou o quadro geral.
   - Regra nova (correção da dona sobre skill/mecânica) → **na skill certa**, nunca só na
     conversa — ver bloco "Memória nunca se perde" do `CLAUDE.md` raiz.
   - Inventário de material/take → `INVENTARIO.md` da pasta certa.
   - `_memoria/preferencias.md` ou `MEMORY.md` se for regra de portfólio.
3. Rodar o Hub (sincroniza-ofertas → cifrar → verificar) se algum STATUS mudou.
4. Responder curto: o que foi salvo, em que arquivo, 1 linha cada — nunca reformatar os arquivos
   inteiros, só mostrar o que foi adicionado/editado.

## Regras

- Nunca inventa o que não foi dito/decidido na conversa.
- Dúvida sobre se algo já estava salvo ou não → rodar `low-ticket-atualizar` no lugar de arriscar
  duplicar.
- Se nada mudou desde a última gravação: responder "já tava tudo salvo, nada novo" e parar.
