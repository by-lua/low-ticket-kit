# PROMPT 12 — NOMENCLATURA E ENTREGA

> Última etapa. Peça sem nome rastreável não sobrevive à primeira semana de teste.

## Nomenclatura

```
<marca>_<oferta>_<formato>_<angulo>_<proporcao>_v<n>.<ext>
```

Exemplo: `dietabiblica_ebook_antesdepois_a03_9x16_v2.png`

- `formato` = a categoria do catálogo, sem acento e sem espaço
- `angulo` = o número da matriz do prompt 03
- `v<n>` = versão da headline (prompt 08), não versão de arquivo

## Manifesto da leva

Entregue junto um `leva.md`:

| Arquivo | Formato (id da referência) | Ângulo | Persona | Headline | Oferta na peça | Proporção | Status QA |
|---|---|---|---|---|---|---|---|

Na coluna **Oferta na peça**: `selo` / `rodapé` / `linha do CTA` / `não cabe`.

E o resumo:
- quantas peças, quantas categorias distintas;
- distribuição por grau de agressividade;
- o que **não** foi produzido e por quê (formato sem prova disponível, ângulo cortado);
- quais peças são teste de headline de uma arte vencedora e qual é a arte-mãe.

## Antes de declarar entregue

- [ ] Todo arquivo abre e tem a dimensão que diz ter (`identify` / `ffprobe`)
- [ ] Nenhum arquivo com 0 byte ou thumbnail salvo no lugar da arte
- [ ] Todas as peças passaram pelo gate 10
- [ ] O `leva.md` bate com o que está na pasta — conte os arquivos
- [ ] Cada peça aprovada tem os **dois** arquivos: `_9x16` e `_4x5`
- [ ] Preço e garantia renderizados batem, caractere por caractere, com o bloco
      canônico do 02
