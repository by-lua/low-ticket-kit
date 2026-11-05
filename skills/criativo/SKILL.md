---
name: criativo
description: Porta de entrada e orquestradora de criativo de anúncio (Meta/TikTok) do sistema LOW-TICKET — vídeo, estático ou carrossel. Diz de onde vêm as ideias (Modelador, criativos de concorrente transcritos, o que a dona trouxer), monta a ficha da leva pra dona aprovar e chama as filhas de copy, formato, edição, imagem, vídeo e revisão. Use sempre que pedirem criativo, anúncio, leva, gancho, roteiro, "faz igual o Rodrigo X", iPhone com preço, carrossel, demonstrativo, POV, UGC.
---

# criativo — orquestradora (índice)

Só a ordem e quem chamar. Regra de execução mora na filha. Raiz: `.../LOW-TICKET` (fonte: `_skills/criativo/`).
Abrir antes: `python3 "<RAIZ>/_skills/low-ticket/scripts/abrir.py" "<oferta>" criativo` → RECIBO à dona.
Métodos (Rodrigo, Kevones, SpyX, Escalados): só os com **Ativo = sim** em `_memoria/METODOS-ATIVOS.md`.

## 1. Entrada obrigatória (sem isso não começa)
- `OFERTAS/<slug>/OFERTA.md` — o que vendemos, o que NÃO é, pra quem, dor, preço. Copy que promete fora disso = errada.
  **§ Ângulo final preenchido?** Os ganchos/ganchos de criativo partem dele (molde + headline + subheadline
  aprovados na E3), não do `spyx.ganchos` cru — a página já pode ter mudado de ângulo depois da modelagem.
  Campo `?` → usa `spyx.ganchos` mesmo, mas avisa a dona que a página pode ainda não ter headline fechada.
- `OFERTAS/<slug>/pesquisa/modelador-*.json` — ganchos, roteiros, copies, estáticos e a análise dos criativos do original.
- `OFERTAS/<slug>/trafego/ANALISES.md` (se existir) — o que já funcionou ou não.
- **Oferta sem `modelador-*.json`** (todas as ativas até 01/11/2026): rodar antes o `low-modelador` no anunciante
  do `pesquisa/REFERENCIA.md` e salvar. Sem como rodar → seguir só com `OFERTA.md` + `REFERENCIA.md` e **avisar a dona**.

**Onde está cada coisa no `modelador-*.json`** (chaves reais, v3): `spyx.ganchos` · `spyx.roteiros` ·
`spyx.copies_anuncio` · `spyx.criativos_imagem` (estáticos) · `spyx.criativos_analise` (criativos dele) ·
`spyx.persona` · `spyx.posicionamento` (ele vende × nós vendemos) · `spyx.alavancas_oferta_dele` (mais fraca / não tocada).

- **Oferta já no ar que nunca passou por auditoria:** rodar `metodo-spyx` (uso dentro) antes da leva — criativo bom
  não salva oferta fraca.

## 2. Passos

### C0 — Abertura do criativo (sempre, antes do C1; ninguém pula)
🛑 = pare, mostre por extenso (tradução PT de texto estrangeiro) e espere a dona. ✅ = arquivo que prova.
1. **Conferir o histórico:** é a 1ª leva desta oferta? (`criativos/` vazio = 1ª). Dizer à dona.
2. **Mostrar o que já existe**, em 3 blocos:
   - (a) **Banco do Passo 6** (`pesquisa/modelador-*-etapa2*.md`): quantos ganchos/copies e quais ângulos;
   - (b) **Criativos do anunciante original** (`pesquisa/referencia/videos`): quantos, formatos, dias no ar;
   - (c) **Referências de outros anunciantes** (`VALIDACAO` § Referências escolhidas): quais, ou "nenhuma ainda".
3. 🛑 **Perguntar:** *"Usamos o banco que já montamos? Modelamos os criativos do original? Buscamos anunciantes novos?
   Ou uma mistura?"*
4. **Se buscar novos** (ou se a busca ainda não foi feita): entregar os **termos por idioma** (idioma-alvo + PT/ES/EN),
   um por linha, prontos pra copiar → 🛑 padrão = **busca manual da dona**: ela devolve a **lista de anúncios** (links).
5. 🛑 **Pra cada anúncio da lista, decidir com ela:** modelar **um vídeo específico** (refazer aquele criativo) ou
   **entender o que o anunciante faz** (padrão de formato, ângulo, gancho, oferta) e aplicar.
6. ✅ `criativos/FONTES-<data>.md`: o que vem do banco · quais criativos do original · quais anúncios novos (link +
   "modelar este vídeo" / "entender o padrão") · leva padrão (3 vídeos: demonstrativo, expert, UGC + 4 imagens).
   Só então C1.


| # | Passo | Saída que prova | Filha |
|---|---|---|---|
| C1 | **Juntar ideias** — **antes, perguntar à dona de onde modelar** (regra 04/11/2026): (1) os criativos do **anunciante original** · (2) os de **outros anunciantes** (seção *Referências escolhidas pela dona* da `VALIDACAO`) · (3) **os dois**. Mostrar o que existe de cada lado (quantos, formatos, dias no ar). Depois: (a) Modelador · (b) os criativos escolhidos: transcrever, entender o formato (POV, demonstração, expert, UGC) e o porquê, refazer pra nossa oferta · (c) o que a dona trouxer | `criativos/IDEIAS-<data>.md` com a fonte de cada ideia | `ctv-modelar-concorrente` |
| C1b | **Clone 1:1** — quando a dona aponta UM criativo específico (nosso ou de terceiro, imagem ou vídeo) e pede "modela esse aqui 100%" (não ideia solta, reprodução fiel, inclusive pra nicho/produto diferente do original) | peça clonada ou storyboard cena a cena | `ctv-clonar-referencia` |
| C2 | **Ficha da leva** — **leva padrão de teste da dona (04/11/2026): 3 vídeos (1 demonstrativo · 1 expert · 1 UGC) + 4 imagens**, salvo ordem diferente. 1 linha por peça: formato, **bolha** (pra quem é: 1 dor/persona — o criativo é a segmentação, `references/METODO-KEVONES-LEVA.md`), gancho, texto na imagem/fala, título, descrição. **Cada peça nomeia a bolha; 2 peças na mesma bolha só se o formato for diferente** (nunca variação rasa). Campanha: país aberto + idioma (Rodrigo); conjuntos aberto/segmentado/idade com os mesmos criativos (Kevones). Ganchos e copies partem do **banco do Passo 6** (`modelador-*-etapa2.md`) + criativos escolhidos no C1 | `criativos/FICHA-LEVA-<data>.md` **aprovada pela dona** | `ctv-estudo-leva` |
| C3 | **Copy** — gancho → desenvolvimento → CTA, pelo formato | copy de cada peça na ficha | `ctv-copy` |
| C4 | **Formato** — receita do formato pedido (expert Rodrigo, demonstrativo, POV, UGC, impacto direto, antes e depois, iPhone com/sem preço, carrossel de páginas, orgânico feio) | briefing da peça | `ctv-formatos` |
| C5 | **Produzir** — imagem (GPT) ou vídeo (Flow, narração, b-roll) | arquivos em `criativos/CRIATIVO-N/` | `ctv-imagem` / `ctv-video` |
| C6 | **Edição** (vídeo) — legenda, b-roll, cortes, layouts, áudio, fecho padrão (card preto + mockup/compilação + CTA mudo alguns segundos), QA | vídeo final | `ctv-edicao` |
| C7 | **Revisão** — copy e peça revisadas num pane limpo contra `OFERTA.md` e a ficha | aprovado/reprovado por peça | `ctv-revisor` |

Depois: subir e rodar → `metaads-kevones` (tráfego) · `meta-ads-mcp`.

Referências herdadas das skills antigas (detalhe que as filhas citam): `references/` e `scripts/` desta skill.

## 3. Regras que valem em toda peça (só estas; o resto mora na filha)
- Ficha aprovada antes de gerar qualquer imagem ou vídeo.
- Todo formato que tem edição puxa de `ctv-edicao`; nenhum formato reescreve regra de edição.
- Fecho da sessão: `low-ticket-salvar` (ficha, peças feitas, `STATUS.md`).
- **Pessoa de referência (regra fixa, 05/11/2026):** toda imagem de pessoa real que a dona manda como
  referência (Pinterest, print, foto) é só inspiração de estilo — nunca gera a mesma pessoa. Cria persona
  NOVA parecida (tom de pele, cor/tipo de cabelo, vibe), rosto diferente da referência. Vale pra qualquer
  geração de persona (GPT imagem, Flow) em qualquer formato. Não precisa a dona repetir a cada pedido.
- **Print/frame de criativo como referência de POSE (regra fixa, 05/11/2026):** quando a dona manda
  print/frame de um criativo ("faz assim", "igual essa", "esse take aqui"), ANEXA o print e pede pra
  REPLICAR aquela composição exata (ângulo, enquadramento, posição da mão, posição do objeto), trocando
  só a pessoa pela nossa persona e o produto pelo nosso. Nunca escreve descrição de cena do zero a partir
  do que entendeu olhando o print — perde fidelidade. Referência de pose é material de composição pro
  gerador, não é pra ler e reinterpretar. Vale pra qualquer formato/ferramenta de geração.
- **Mostrar cada imagem antes da próxima (regra fixa, 05/11/2026):** gera 1 peça/take, baixa, mostra a
  imagem pra dona, espera aprovação ou correção — só então gera a próxima. Vale mesmo quando o pedido já
  veio com várias poses/cenas definidas de uma vez (a lista é o que fazer, não autorização pra rodar tudo
  sem mostrar nada no meio).
- **Todo material impresso em cena é A4 (regra fixa, 05/11/2026):** calendário, agenda, caderno, livro, livreto,
  folha, capa — qualquer papel/impresso que o produto mostre numa imagem ou take tem tamanho **A4** (21 × 29,7 cm,
  proporção ~1 : 1,41, retrato). Sem isso o GPT escolhe o tamanho que acha bom (pequeno, esticado, enorme). No prompt:
  escreva `A4 size (21 x 29.7 cm, portrait, proportion about 1 to 1.41), real-world scale: a little larger than a
  woman's two hands side by side, about the width of her shoulders`, e proíba `postcard size, pocket size, tiny, oversized,
  stretched, square`. Vale pra capa na mão, folha na mesa, prancheta, caderno aberto. Ao conferir a imagem, compare a
  proporção do objeto com as mãos/mesa; fora de A4 = regera.
- **Produto em cena = só o produto oficial da oferta (regra fixa, 05/11/2026):** antes de anexar capa/mockup/página como
  referência, leia `OFERTAS/<slug>/ATIVOS.md` (seções 1 e 2: o que é OFICIAL e o que foi DESCARTADO; regra em `low-ticket` § 2b). **Nunca escolha capa pelo nome do arquivo** (`capa`, `guia`, `kit`): o agente do Calendrier Magique pegou
  `guia-v1-capa.png` (azul descartada, igual à da concorrente) por causa do nome. Arquivo em lista de descartado, com
  `descartado` no nome, ou de cor/arte diferente da capa oficial = não usar. Sem ponteiro de capa oficial no
  `CLAUDE.md` da oferta → criar o ponteiro antes de gerar. Depois de gerar, **confira a imagem contra a capa oficial**
  (cor, musa/arte, texto) antes de mostrar. Oferta que descarta um visual apaga o arquivo (ou move pra `_arquivo/`),
  nunca deixa na pasta de uso.
- **Registrar cada peça em `ATIVOS.md` seção 4 (regra fixa, 05/11/2026):** peça gerada = linha com estado `gerando`; dona aprovou = `aprovada`
  e o arquivo final; dona reprovou = `reprovada` + motivo, e o arquivo reprovado sai da pasta de uso (`_descartado/` ou apagado).
  Cada peça diz de qual referência de concorrente foi modelada (seção 3). Registrar junto com a resposta da dona, não no fim da sessão.
