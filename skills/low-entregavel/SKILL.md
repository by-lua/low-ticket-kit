---
name: low-entregavel
description: Etapa E4 do sistema LOW-TICKET — escreve e gera o entregável (produto principal, bônus, bumps) em páginas-imagem A4 com a referência visual da página original. Use para "faz o entregável", "MVP", "gera as páginas do produto", "completa a entrega", exercício, pôster, folha de atividade.
---

# low-entregavel — E4, entregável

## ⛔ Regras fixas (valem em toda página)
- **Nunca HTML, SVG, Pillow, código ou PDF cru.** Toda página é **imagem gerada no GPT, A4**, com a mesma cara
  visual (referência + paleta da oferta).
- **Item de fazer/imprimir = página própria:** exercício, pôster, folha, checklist, mapa, tabela de preencher.
  A explicação numa página, a folha na **página seguinte**. Nunca só a explicação.
- Scripts de "gerar folha por código" (`gera-worksheet.py`, `gera-printables.py`…) não se usam nem se copiam.

**Entrada:** `OFERTA.md` · página da E3 · `pesquisa/referencia/imagens-origem/` · `DESIGN-SYSTEM.md`.
**Saída:** `produto/MANIFESTO-ENTREGAVEIS.md` · `produto/texto/` · imagens em `produto/ENTREGA/` · registro vivo
`produto/ENTREGAVEIS.yaml` (skill `auditar-entregaveis-oferta`).

## Passos
1. **Manifesto:** o que a página promete, item por item (principal, bônus, bumps) = o que tem que existir.
2. **Texto inteiro primeiro** em `produto/texto/`: todas as páginas, com cada exercício/pôster descrito
   (conteúdo exato + como fica na folha + gabarito). Sem texto, o GPT gera aleatório.
3. **Primeiras páginas = imagens "por dentro" da página original** refeitas pra nossa oferta (mesma composição,
   nosso conteúdo e idioma; cor só muda se a paleta mudou) → **mostrar à dona** → ela aprova → viram a
   referência travada.
4. **MVP 40%** do principal com as aprovadas de referência → depois completo → bônus → bumps. Um item por vez.
5. **Como gerar** (mecânica, não repetir aqui): `imagens-pagina-low` § "ENTREGÁVEL — primeiras páginas" e
   "Pipeline canônico" · `gpt-imagem-playwright` § "Páginas de ENTREGÁVEL" (lote no Work mode, teste de 2) e
   § "Páginas de ATIVIDADE" (folha de imprimir: 1 por mensagem). Carta de tarô/cigano = scan real colado.
6. **Revisar cada página de imprimir:** legível impressa, espaço pra escrever, acento certo no idioma, instrução
   bate com a folha, nada cortado na margem. Contact sheet no fim.
7. Outro idioma de uma entrega existente → `traduzir-entregavel-imagem`.

Próximo: E5 (`imagens-pagina-low` — imagens da página com o MVP de referência) e E6 (área de membros:
`area-membros-netflix`, conferida com `auditar-entregaveis-oferta --registrar`).
