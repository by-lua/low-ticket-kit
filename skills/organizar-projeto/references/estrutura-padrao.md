# Estrutura padrão

Ideia (MazyOS): a pasta-raiz é a "empresa" — memória, regras e status geral. Cada projeto
(oferta, cliente, produto) é uma "empresa dentro da empresa" — com contexto, status e memória
próprios. O agente que abre o terminal numa subpasta herda o CLAUDE.md da raiz e o do projeto.

## Raiz

```
<RAIZ>/
  CLAUDE.md          regras do portfólio · mapa da raiz · tabela "tarefa → skill obrigatória"
  STATUS.md          painel geral: 1 linha por projeto (fase, mercado, link, atualizado) + frentes
  _memoria/
    empresa.md       quem somos, o que vendemos, contas/infra que todo projeto usa
    estrategia.md    foco atual, prioridades, o que está pausado
    preferencias.md  como a dona/dono quer o trabalho (tom, formato, o que evitar)
  <PROJETOS>/        1 pasta por projeto (OFERTAS/, CLIENTES/, PRODUTOS/ — nome do negócio)
    <slug>/          (estrutura do projeto, abaixo)
  CONHECIMENTO/      método, cursos transcritos, fontes, perfis de referência
  MODELOS/           moldes reutilizáveis (página, checkout, STATUS), referências visuais
  <FRENTES>/         ferramentas/sistemas internos com vida própria (cada um com README/CLAUDE.md)
  _arquivo/          backups, versões velhas, lixo conferido, log da reorganização
```

## Projeto

```
<slug>/
  CLAUDE.md          o que é · links no ar · mapa da pasta · skills · Memória do projeto
  STATUS.md          estado vivo: fase, checkouts, tracking, pendências, decisões, histórico
  DESIGN-SYSTEM.md   (se tiver identidade visual própria)
  pesquisa/          mineração, obra de arte, checagens, oferta/briefing, concorrência,
                     referencia/, CLONE-ORIGINAL (symlink pra mídia de terceiro), prints/ da pesquisa,
                     anuncios-concorrentes/, criativos-referencia/
  produto/           o que o cliente recebe: texto/, ENTREGA/, PDF/, MOCKUPS-NOSSOS/, prompts/
  site/              página de vendas + área de membros (painel/). Normalmente é o repo git do deploy
  site-<idioma>/     variação por mercado quando é app separado
  checkout/          banners/, order-bumps/, upsell/, downsell/, CONFIG-<gateway>.md
  criativos/
    [<MERCADO>/]     BR/ PT/ ES/… quando a oferta roda em mais de um mercado
      CRIATIVO-<N>[-slug]/
        briefing.md | roteiro-*.md | anuncio.md   (copy, ângulo, decisão)
        <final>.mp4|.png                          (final SOLTO na raiz do criativo)
        intermediarios/                           (frames, raw, b-roll usado, renders de teste)
    MATERIAL-ENTREGAVEL/   gravações de tela/fotos do produto — fonte de todos os criativos
    _broll/                b-roll compartilhado
  instagram/         conteúdo orgânico da oferta (stories, posts, depoimento) — o que a gente posta
  trafego/           campanhas, relatórios, testes, decisões de escala
  prints/            QA e prova de gate (página no ar, checkout, painel) — por propósito
  _arquivo/          versão velha, revogado, lixo conferido
```

Só cria pasta quando tem conteúdo. Nome é fixo: não inventar `anuncios/`, `ANUNCIO/`, `pagina-v2/`,
`banners-checkout/` — vai pra pasta do padrão.

## Onde vai cada coisa (decisão rápida)

| Coisa | Destino |
|---|---|
| obra de arte, checagem, pesquisa de demanda/concorrência, oferta.md | `pesquisa/` |
| print de anúncio/página de concorrente, clone da página original | `pesquisa/` (mídia pesada → PROJETOS-MIDIA + symlink) |
| texto do entregável, PDFs, imagens dos módulos, prompts do produto | `produto/` |
| index.html, painel, Dockerfile, repo git | `site/` |
| banner do checkout, capa de order bump, upsell | `checkout/` |
| story/post orgânico da oferta (depoimento, bastidor) | `instagram/` |
| vídeo/imagem/carrossel de anúncio | `criativos/[MERCADO/]CRIATIVO-N/` |
| gravação de tela do produto pra usar em criativo | `criativos/MATERIAL-ENTREGAVEL/` |
| print de QA / gate de eventos | `prints/` |
| versão descartada, backup, .zip exportado, `.lixo` | `_arquivo/` |

## Exceções aceitas (documentar no CLAUDE.md do projeto)
- Pipeline que copia arquivo por caminho fixo (ex. `deploy.sh` copia `index.html` da raiz pro repo):
  deixar onde está e anotar "fonte da página = X, deploy = Y".
- Fonte editável separada do build (`pagina/` = fonte, `site/` = build gerado): manter as duas, anotar qual editar.
- Pastas ocultas de ferramenta (`.claude`, `.codex`, `.overclock-app`): nunca mover.
