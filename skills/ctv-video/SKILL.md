---
name: ctv-video
description: Produz criativo de vídeo do sistema LOW-TICKET a partir da ficha da leva aprovada — cenas (Flow), narração (VoiceStudio local / LoveVoice / Speechma), gravações de tela do entregável, b-roll — e entrega pra edição. Use para gerar vídeo demonstrativo, UGC, expert, caixinha, POV.
---

# ctv-video — vídeo

> **Regra da dona (09/11/2026) — adaptar = refazer cena a cena com o NOSSO material:** cada cena/take do original vira referência de composição e é refeita com o nosso produto oficial do mercado (ATIVOS.md) e texto no idioma do mercado; vídeo = imagem do take no GPT → clipe no Flow com o mesmo movimento; fala, legenda e anuncio.md adaptados; pessoa nova. Nunca reaproveitar cena com produto/texto de outro idioma ou oferta. Texto completo: skill `criativo` § 3.

**Entrada:** linha aprovada da `FICHA-LEVA` com o **roteiro completo** (gancho + desenvolvimento + CTA) ·
`OFERTA.md` · material do entregável (`criativos/MATERIAL-ENTREGAVEL/`, gravações de tela).
**Saída:** `criativos/<MERCADO>/CRIATIVO-N/` — vídeo final 9:16 + `anuncio.md`; intermediários em `intermediarios/`.

## Passos
1. **Mapear todos os assets** da oferta antes de montar (gravações, takes, b-roll): cada vídeo usa um pouco de cada.
2. **Cenas de pessoa** (UGC, expert, POV): Flow (`flow-mcp`; reserva `flow-video-playwright`) — pessoa segurando o material real,
   criada a partir de referência real do país (regra abaixo).
3. **Cenas de mesa/demonstração:** 1-2 aparelhos + 3-4 folhas impressas, página diferente em cada; zoom de câmera
   orgânico (aproximação lenta), gesto padrão = apontar.
4. **Voz:** VoiceStudio local → senão LoveVoice/Speechma (regra `ctv-edicao` › EDICAO-PADRAO § Voz), voz fixa da leva;
   **conferir o gênero** da voz antes de gravar.
5. **B-roll — cenas reais orgânicas do TikTok primeiro** (muito melhores que Pexels/banco):
   - **3-4 termos em inglês** da cena de cada frase (ex. idosos: "dementia activities", "memory care", "ot elderly",
     "cognitive games"; tarô: "learning tarot beginner", "tarot cards on table");
   - rodar `python3 scripts/broll-tiktok.py --out <PROJETOS-MIDIA>/VIDEOS-REFERENCIA/<SLUG>-broll-tiktok "termo 1" …`
     (~1 min por termo: busca no perfil `tiktok2`, filtra ≥50 mil views e ≤90 s, baixa em paralelo, folha de contato
     de 4 quadros + `ORIGEM.md`) e criar o symlink em `criativos/`;
   - escolher olhando as `.sheet.jpg`: **sem texto queimado** na parte usada (ou recortar fora dele);
   - `get-brolls` só pra fonte que o script não cobre (YouTube, Wikimedia, NASA, print de notícia) — é lento.
6. **Montar:** regras da `ctv-edicao` (todas). Mecânica de render: `criativo-ads-video-orq`.

**Pessoa em cena (UGC, expert, POV, foto com gente) — PROTOCOLO FIXO, 4 passos, nenhum pulável (dona,
01/11/2026, reescrito explícito 05/11/2026 depois de repetir a explicação várias vezes — ler isto inteiro
antes de gerar qualquer persona, não decidir por conta):**

**Passo 1 — referência da pessoa (SEMPRE obrigatório, nunca pula).** Uma foto real de alguém, usada só
como referência de ESTILO (pele, cabelo, roupa, idade, vibe do país) — nunca a pessoa final, nunca o rosto
final. Três formas de conseguir, qualquer uma serve:
  - **(a) Eu busco no Pinterest** (perfil `pinterest`, porta 9246: `~/.claude/bin/browsers.sh pinterest` →
    `agent-browser --session pinterest`) com termo do país/cena: "mulher brasileira dirigindo carro",
    "mujer argentina en la cocina", "american woman 50s kitchen". Baixo 2-3 fotos em
    `PROJETOS-MIDIA/CRIATIVOS-CONCORRENTES/<SLUG>-pessoas-ref/`.
  - **(b) A dona manda a foto** (print, link, Pinterest, qualquer imagem de uma pessoa real).
  - **(c) A dona pede pra eu achar** — mesma busca do (a), mas ela escolhe entre as opções antes de eu usar.
  Sem foto de referência não se gera persona nenhuma — perguntar à dona antes de inventar do zero.

**Passo 2 — gerar a PERSONAGEM NOVA (Imagem 1), sem material, uma vez só por leva.**
  GPT image, 1 anexo (a ref do Passo 1): pedir pessoa NOVA, mesmo jeito real (pele, cabelo, roupa, luz,
  cenário) da ref, mas rosto e traços DIFERENTES — nunca a mesma pessoa da foto. Mãos livres, nada na mão.
  Salvar em `nossa/persona/personagem-base.png`. Essa imagem é a personagem fixa da leva inteira — gerada
  uma vez, reusada em toda cena nova dela.

**Passo 3 — personagem segurando O NOSSO material (Imagem 2), uma vez por cena/CT.**
  GPT image, 2 anexos: Imagem 1 (`personagem-base.png`, pra manter a mesma pessoa) + a capa/mockup REAL do
  nosso produto (livro, caderno, tablet, postal — o que fizer sentido pra cena). Pedir a MESMA pessoa da
  Imagem 1, agora segurando/mostrando o material real na pose da cena (abrindo, exibindo a capa pra câmera
  etc). Nunca volta a usar a foto do Pinterest aqui — só a Imagem 1. Aprovar visual com a dona antes de
  seguir. Salvar em `nossa/persona/cena-<nome-da-cena>-<idioma>-aprovada.png`.

**Passo 4 — Flow: imagem da cena (Passo 3) + A FALA EXATA no prompt, numa chamada só.**
  `flow-mcp` (`flow_generate_video` com a Imagem 2 do Passo 3 em `reference_images`; reserva `flow-video-playwright` `video i2v --initial-frame`). O prompt de movimento TEM que
  incluir a fala exata que a pessoa vai dizer, entre aspas, no idioma certo — o Flow já sincroniza boca e
  gera a voz sozinho, não precisa de narração em cima depois. Nunca manda o Flow sem a fala: sem isso ele
  inventa uma fala genérica por conta própria (já aconteceu, fala saiu errada/fora do roteiro). Pegar a fala
  do roteiro aprovado (`FICHA-LEVA` ou plano da peça), nunca inventar.
  Exemplo de prompt: `"<pessoa e pose>, talking directly to camera, lips synced saying in <idioma>: \"<fala
  exata>\". <resto da cena>."`

Isso é tudo — 1 ref, personagem, personagem+material, Flow com a fala. Repetir o Passo 3+4 pra cada cena nova
da mesma personagem (reusando `personagem-base.png` do Passo 2, sem regerar a pessoa).
Objetivo: gente com cara de gente daquele país, não de IA.

Formato e roteiro: `ctv-formatos` + `ctv-copy`. Fecho: → `ctv-revisor`.

**Levar take que já existe pra outro mercado/idioma/produto (regra da dona, 07/11/2026) — 3 passos, nada mais:**
1. Pegar o **frame/imagem da cena do take original** (ex.: `FLOW-TAKES/<take>/frame.png`). Não montar cena do zero.
2. **GPT image** (`gpt-imagem-playwright`), anexo = esse frame. O prompt diz SÓ o que muda: idioma (traduzir todo
   texto pra X)? produto (anexar a capa/página real do produto novo)? preço (anexar/escrever o preço novo)? O resto
   fica igual. Anexo extra só quando muda produto ou preço; mesmo produto em outro idioma = só o frame.
3. **Flow** (`flow-mcp`): anima essa imagem nova com o mesmo prompt de movimento do take original.
**Passo 3 no Flow (regra da dona, 07/11):** `flow_generate_video` com `reference_images` reenvia o arquivo a cada
tentativa e falha com `REFERENCE_NOT_ATTACHED`, deixando cópias duplicadas no projeto (4 do mesmo frame). Fazer
assim: (a) subir o frame UMA vez (a 1ª chamada já sobe, mesmo falhando); (b) `flow_project_open` pra limpar o
composer; (c) `flow_inspect` clicar no "+" do composer → escolher o asset já enviado na lista → "Incluir no
comando" → esperar o seletor fechar; (d) só então `flow_generate_video` **sem** `reference_images`, só o prompt
(preview `auto_confirm=false`, depois `true`). Nunca reenviar o mesmo arquivo. Antes de subir, olhar a lista de
recentes: se o asset já existe, usa ele. Sem a imagem anexada no composer, não gera.
Mostrar a imagem do passo 2 à dona antes do passo 3. Erro real (07/11, Tarot FR→AR): mandei 5 anexos (páginas AR +
capa) direto no Flow pra "recriar" a cena — ruído, composer travou. Imagem é no GPT, não no Flow.

**Catálogo de takes de demonstração:** antes de inventar uma composição, consultar `criativo-ads-video-orq/references/takes-mesa-real.md` (catálogo A–O). Take J = TV com página inteira e caneta apontando + zoom orgânico; pode variar mão pela direita/esquerda e usar outra página REAL. Impresso = D/I/O. Não rolar para inventar conteúdo: regra `flow-video-playwright` § Conteúdo de tela fechado.
