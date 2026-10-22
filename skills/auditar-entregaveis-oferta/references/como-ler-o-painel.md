# Como o script conta as páginas

Fonte da verdade = **arquivos no disco do painel**, não o card do painel e não o STATUS.

- Raiz do conteúdo: `<painel>/conteudo/<item>/` — por padrão `OFERTAS/<slug>/site/painel/`,
  mas a oferta pode declarar outro (ver "Painel de outra oferta" abaixo)
- Conta `*.webp`, `*.jpg`, `*.png` dentro da pasta
- **Ignora** a subpasta `original/` (backup em alta resolução, não é a versão publicada)
- **Ignora** a subpasta `pdf/` (é o JPEG irmão que alimenta o download — a MESMA página)
- **Ignora** arquivos começados por `capa` (a capa não é página de conteúdo)
- `site/painel/assets/capas/` = capas dos cards; não entra na contagem

**Conta PÁGINA, não arquivo** (mudou em 15/10/2026): a chave é `(número, nome do arquivo)`,
então `.jpg` + `.webp` da mesma página contam **1** (no Tarot cada página sai nos dois: o jpg
alimenta o PDF, o webp o leitor). Antes o script contava arquivo e o Tarot dizia 92 páginas
onde havia 46 — e o Cigano dizia "38/38 COMPLETO" com uma página ainda por gerar.
`AVISO numeração ambígua` agora só aparece quando duas páginas **diferentes** disputam o mesmo
número (`pagina-01-simbologia` × `pagina-001-tensao`), que é caso de renomear, não de contagem.

## Casamento item ↔ pasta

O número do item vem da coluna **Tipo** do manifesto (`Bônus 1`, `Order bump 2`,
`Principal`), não do nome — o nome do item é o título de venda.

Os order bumps são casados pelo **assunto**, não pelo número, porque a numeração do
manifesto não bate com a pasta do painel:

| assunto no item | pasta do painel |
|---|---|
| segurança industrial | `ob-seguranca/` |
| comandos elétricos | `ob-comandos/` |
| medição e testes | `ob-medicao/` |

O caminho mais barato é a coluna **Item** ter o **mesmo nome da pasta** do painel (é o que o
Mapa do Tarot e o Cigano fazem): o primeiro passe do `casar_item()` casa por nome idêntico e
não tem heurística que erre. Se uma oferta nova tiver outro naming, ajustar `casar_item()` no
`audita.py`.

## Painel de outra oferta (oferta que mora no painel de outra)

O Baralho Cigano não tem painel próprio — vive no `/painel` do Mapa do Tarot (decisão da
dona). A oferta declara isso no manifesto e o audit passa a ler o painel certo:

```markdown
> **Painel desta auditoria:** `../mapa-do-tarot/site/painel` (moramos nele)
```

Sem a declaração o script lê `site/painel/` da oferta (no Cigano é uma cópia parada de 05/10,
com 4 páginas das 36 cartas) e diz que está tudo VAZIO.

## Escopo (o painel compartilhado tem card de outra oferta)

Quando duas ofertas dividem o mesmo `/painel`, o manifesto diz o que **não** é dele, no
parágrafo que começa com `**Escopo desta auditoria:**`:

```markdown
> **Escopo desta auditoria:** só os itens da tabela abaixo. Fora: `principal`, `completo`,
> `bonus-1` (oferta Mapa do Tarot, manifesto em `OFERTAS/mapa-do-tarot/`).
```

`cigano-*` = família inteira (prefixo); `principal` = item (exato/prefixo). O parágrafo vale
até a linha em branco — pode quebrar linha à vontade.

## Texto

`texto: ok` quando existe `produto/TEXTO/*.md` (ou `produto/TEXTO/completo/*.md`)
casado pelo mesmo critério. `ausente` = escrever/redigir o texto **antes** de gerar
imagem (ordem da casa: texto → visual → produção).

Oferta que guarda o manuscrito em OUTRO lugar declara item a item (senão a coluna mente):

```markdown
> **Texto desta auditoria:** `principal` = `produto/ENTREGA-COMPLETA-TXT.md`,
> `completo` = `—`, `guia-flash` = `produto/ORDER-BUMPS/guia-flash-arcanos-maiores/TEXTO.md`
```

`—` = **declaradamente não escrito** (é diferente de "ainda não procurei"). Item que o
manifesto não cita cai na regra antiga (`produto/TEXTO/`). O caminho pode ser arquivo, pasta
(conta `.md` dentro, recursivo) ou glob `*`.

No Tarot isso é decisivo: o manuscrito é UM arquivo (`ENTREGA-COMPLETA-TXT.md`, só o Básico,
página por página), os 3 order bumps têm `TEXTO.md` cada, e o Completo + os 4 bônus **não têm
texto escrito no repositório** (as páginas foram pra imagem sem manuscrito salvo) — antes o
script dizia "ausente" nos 9 itens, o que fazia a dona desconfiar do audit inteiro.

## Onde fica o registro

`produto/ENTREGAVEIS.yaml`, sempre reescrito pelo script. É gerado — nunca editado à mão.
Serve de estado de retomada: `publicado` é a última contagem real, `falta` é o que ainda
precisa sair.

## Quando o script não entende a oferta

Se a saída for `AUDIT-SKIP`, a tabela de `produto/MANIFESTO-ENTREGAVEIS.md` não existe ou
não tem o cabeçalho canônico (`| Item | Tipo | Plano | Promessa ... | Nº páginas
(completo) | ... |`). Aí o caminho é: escrever/ajustar o manifesto e rodar de novo — a
oferta precisa dele para saber o que promete.