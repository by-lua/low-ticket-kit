# B-roll e gravação de tela — coleta (movido do SKILL.md em 26/10/2026)

> Como buscar b-roll (get-brolls, TikTok, Pinterest, banco) e como gravar a tela do produto. Como MONTAR: `EDICAO-PADRAO.md`. Gravação de tela é sempre da dona — faltou, pede.


**B-roll → skill `get-brolls`.** Sempre que o criativo pedir vídeo de apoio,
cutaway, insert, print de tela/notícia ou footage real, use a skill `get-brolls`
(busca em YouTube/IG/TikTok/Wikimedia/NASA/Pexels/Pixabay, com prévia pra revisão
e origem+licença registradas). Ela entra em DUAS fases:
- **Ao PENSAR o criativo** (concepção): buscar referência real de como o conteúdo
  orgânico daquele ângulo se parece — alimenta o conceito e mantém a estética
  nativa (não "cara de IA"). Isso é o mais importante.
- **Na PÓS-PRODUÇÃO**: sourcear os clipes de b-roll de verdade, já com licença e
  proveniência, pra montar/ilustrar.
Comandos: `/get-brolls-brief`, `/get-brolls-review`, `/get-brolls-status`.
`get-brolls` NÃO edita/renderiza o final — só coleta e entrega os trechos.

**Atualização 23/10/2026 (dona) — vale por cima do bloco abaixo:**
- **Cena com material = digital + impresso** (1 aparelho no mínimo + folhas impressas soltas, página diferente em cada). Regra completa em `criativo-ads`.
- **Idioma da busca = o que faz sentido pro contexto**, não sempre inglês: se o objeto aparece na
  cena com texto (ex.: carta de tarô), buscar no **idioma da persona** (Tarot AR → espanhol).
- **Rápido:** pega os **mais vistos sem texto**; se o texto aparece só no começo, **corta o começo**
  e usa o resto. Tira **3–4 cenas que façam sentido** e reaproveita em vários criativos; baixa mais
  só se precisar. Ordem de fonte: **TikTok > Pexels > YouTube** (YouTube costuma ser ruim).
- **Imagem da cena SEMPRE primeiro** (GPT), com prompt pensado pra não aparecer/sumir nada estranho e
  a pessoa ficar igual — só depois anima no Flow (o Flow é instável).
- **Layout do expert:** tela cheia quando fala e/ou **meio a meio com o material** em algum momento.
- **Expert no Flow:** o Flow segura no máximo **8s** e a continuação sai ruim → o expert aparece só
  nos **primeiros segundos** (ex.: lendo a caixa de perguntas em formato story) e depois entra o
  material + narração. **Voz do expert é sempre a mesma:** escolhe a voz no Flow, ou gera com
  qualquer voz e troca o áudio pela nossa voz (`narracao-hub-tts`). O prompt diz **o idioma** em
  que ela fala, pra sair claro na língua da persona.
- **CTA final (estilo Rodrigo):** nos últimos segundos, imagem do material + setinha "tocá en
  más información" rodando uns segundos.
- **Formato "imagem animada" (estilo slide do Canva):** título + elemento que se mexe e faz
  sentido (ex.: mão embaralhando o tarô) — conta como vídeo na leva.
- **Antes de gerar qualquer vídeo:** a **gravação de tela do entregável** (área de membros por
  dentro) tem que existir, e os takes no estilo Flow com as páginas em vários aparelhos/formatos
  (`§E.0c`, takes A–K). Sem isso, não começa.

**TikTok — vídeos virais em INGLÊS (regra da dona, 16/10/2026).** Além do stock, usar **vídeos orgânicos que
já viralizaram** no TikTok como b-roll (é o que parece nativo — os originais que modelamos intercalam MUITA
cena real com o material). Buscar no perfil logado **`tiktok`** (porta 9255) com **~5 termos em inglês ligados
ao produto** (ex.: `dementia activities`, `caregiver grandma moment`, `occupational therapy elderly`,
`memory care activities`, `elderly cognitive games`), priorizando **muitas views**. ⛔ **O clipe NÃO pode ter
texto/legenda queimada** (nem caption, nem watermark, nem outro idioma) — a legenda é a NOSSA (KaraokeV2).
Baixar pela rota do **`get-brolls`** (`gb.py resolve --url <url> --shot <beat>` → `fetch`) pra sair com
origem/licença; `yt-dlp` como fallback, **sempre registrando `credits.md`** (termo, URL, @autor, views).
Montar intercalando **~15–20 cortes curtos (~2–3s)** do material do produto + as cenas reais.


### E.1 — Coleta do b-roll

**Todo b-roll mostra o ASSUNTO do produto no quadro — e só entra clipe ENTREGUE pela
`get-brolls`.** Erro real (Mapa do Tarot, 2026-09-23): o projeto get-brolls só rodou
`search`, nunca review/entrega; um pane baixou clipes à mão com queries genéricas
("hand writing journal", "book pages flipping") e o criativo saiu com pessoa escrevendo
numa poltrona e livro abrindo em leque — nenhuma carta de tarô. Dono: "não tem nada a
ver com o assunto". Regras:
- Toda query e todo `target` do BRIEF carregam o objeto do nicho explícito
  (`tarot cards spread on table hands`, não `hand writing journal`). Palavra genérica
  (book, journal, writing, pages) sem o objeto do nicho = clipe genérico garantido.
- No review, rejeite candidato em que o objeto do nicho não aparece no quadro.
- Pasta `raw/` baixada fora da skill não entra na montagem sem passar por review e
  registro de origem/licença. Delegou? Escreva isso no prompt do pane.
- B-roll em tela cheia = `object-fit: cover` real no 1080×1920. Clipe horizontal
  encaixado sem cover vira letterbox com barra preta (v7 Imperatriz: conteúdo só em
  y 440–1480). QA: `ffmpeg -vf cropdetect` em cada bloco de b-roll tem que dar 1080:1920.
- Nenhum clipe (nem outro trecho do mesmo clipe) aparece duas vezes no criativo. Faltou
  clipe: alonga o anterior ou busca outro.
- B-roll sempre `muted` no Remotion — o único áudio é a VO. (Louco v7: áudio original do
  clipe vazou por baixo da narração.)
- Clipe tem que ter duração útil ≥ slot. Mais curto, o Remotion segura o último frame e a
  cena "trava" (Louco v7, 25.8–27.1s e 27.5s–fim). QA: `ffmpeg -vf
  "freezedetect=n=0.003:d=0.4" -f null -` no final = zero freeze.

**Os termos de busca saem do que você entendeu do produto e da persona na FASE
0, não de achismo na hora de buscar.** Se o comprador é o filho/cuidador de um
idoso (ver FASE 0/§E.4), o b-roll certo mostra a cena pela ótica dele — um
adulto cuidando/visitando um idoso, não só "elderly exercising" genérico.
Releia a página de vendas antes de montar a lista de termos; ela já diz qual é
a dor e o contexto visual que vende.

Busca **sempre em inglês**, mesmo pra nicho brasileiro: o acervo indexado em
português é uma fração do inglês. `rural blacksmith welding`, não `ferreiro
soldando`. Baixe 3–4 clipes que fazem sentido pro roteiro, não os 3–4 primeiros
bonitos.

- Perfil de browser dedicado: **`pinterest`** (`~/.agent-profiles/pinterest`,
  registrado em `registry.conf`). Pinterest exige login pra ver vídeo; sem perfil
  persistente cai no muro de cadastro a cada sessão.
- Prefira o banco público ao Pinterest quando o clipe existir nos dois: licença
  limpa (Pexels/Pixabay/Mixkit/Coverr liberam uso comercial sem atribuição).
  Pinterest é **descoberta**, não fonte — o pin quase sempre reaponta pra origem;
  baixe da origem.
- **Correção (dona, 25/10/2026): Pinterest É fonte direta válida, não só descoberta, quando o
  conteúdo é ESTILIZADO/3D** (render 3D de exercício/anatomia, animação, ilustração) — é onde o
  banco público costuma faltar (ver `OFERTAS/luciola-atlas-movimiento/STATUS.md`, "B-roll externo
  resolvido 12/10": os 5 clipes 3D do Atlas vieram de busca direta no Pinterest em inglês, não de
  banco público). **Divisão de fonte por tipo de conteúdo:** Pinterest = 3D/estilizado/render;
  TikTok = orgânico/viral (cena real, não encenada); YouTube = secundário (geralmente pior
  qualidade/mais clichê que os outros dois, usar só quando os outros não têm). Buscar sempre em
  inglês nos três.
- Nunca use clipe com marca, logo, rosto reconhecível de celebridade ou legenda
  queimada. Corta o anúncio no review da Meta.
- **TikTok também é fonte — dupla função (buraco fechado 2026-09-09).**
  1. **Sinal de demanda:** vídeo viral sobre o tema/dor da oferta é a mesma
     leitura que "comentário recente no YouTube" (complemento de demanda do método, ver `low-ticket-metodo-mvt` mineração) — visualização e comentário alto e recente = gente
     querendo aquilo agora. Busque pelo termo da persona/dor antes de decidir
     que "não tem demanda".
  2. **Fonte de b-roll:** cena TikTok que faz sentido pro roteiro (mesma regra
     de nunca usar marca/logo/rosto de celebridade/legenda queimada — corte
     esse trecho ou descarte o clipe) pode virar b-roll, do mesmo jeito que
     Pinterest é descoberta e você baixa da origem quando possível.
  3. **Download:** `yt-dlp` baixa TikTok direto por URL, sem precisar de perfil
     logado pra vídeo público (`yt-dlp <url> -o saida.mp4`). Só precisa de
     conta/perfil de browser dedicado se o conteúdo estiver atrás de
     idade/restrição — nesse caso, mesma lógica dos outros perfis persistentes
     do projeto (criar um perfil dedicado, não usar conta pessoal).
  4. Padronize igual aos outros: 9:16 (já nasce assim na maioria), sem áudio
     original, cortar qualquer selo/UI do TikTok (relógio, @usuário, ícones de
     like/comentário) antes de usar — nunca deixa a chrome do app original
     visível no criativo final.
- Padronize antes de montar: 9:16, mesmo fps do resto, sem áudio original
  (`-an`) — a trilha e a narração são únicas pro criativo todo.
- **Se achar fácil, cena de gente usando algo parecido com o produto ajuda**
  (mão folheando papel numa mesa, gente manuseando peça, cliente recebendo
  objeto) — o comprador se vê fazendo aquilo, mais forte que ambiente vazio.
  Mas é ganho oportunista, não meta: não trave a busca de b-roll tentando achar
  esse tipo específico. Cena de ambiente/ferramenta parada (banco tem de sobra)
  resolve o criativo sozinha na maioria das vezes.

### E.2 — Gravação de tela em modo mobile

O produto navegado por dentro, gravado com o DevTools em device emulation
(iPhone/Android, 9:16 nativo), não o desktop redimensionado — barra de rolagem e
hover de mouse denunciam desktop e quebram a leitura de "isso é o app no meu
celular".

**Comando (`agent-browser`) — nunca gravar sem setar o device antes, senão sai
em resolução de desktop:**

```bash
agent-browser --session <sessao> set device "iPhone 16 Pro"   # NÃO --device (isso é o provider iOS)
agent-browser --session <sessao> navigate "<url do produto>"
agent-browser --session <sessao> record start "<saida.webm>"
# ... ações reais: scroll, clique em link/card/botão real da UI ...
agent-browser --session <sessao> record stop
```

Sai em ~1080×2340 (3x DPR do device), não exatamente 9:16 — normalize na
montagem: `scale=1080:-1,crop=1080:1920:0:0` (ou pad, se preferir não cortar).

#### Demonstração obrigatória do entregável digital

Quando o produto tiver portal, área de membros ou arquivos navegáveis, a gravação
precisa provar a entrega real — não basta rolar a landing page:

1. Mostre rapidamente a tela de login e a entrada pelo e-mail da compra.
2. Nunca deixe um e-mail completo legível. Use uma conta fictícia e mantenha o campo
   desfocado, coberto ou mascarado com asteriscos; na área logada, exiba algo como
   `cl******@dominio.com`.
3. Passe pela visão geral do produto e por **cada seção entregue**, incluindo todos os
   bônus. Mostre pelo menos um detalhe interno de cada seção, não apenas o cartão/capa.
4. Faça cliques reais: abra um material, mostre seu conteúdo, volte ao portal e siga
   para o próximo. O corte final pode acelerar transições, mas cada seção precisa ser
   reconhecível em quadro.
5. Grave em device mobile real e enquadre para o texto importante continuar legível
   depois do crop 9:16. Sem cursor de desktop, hover ou rolagem horizontal.

Gate antes da montagem: revise quadro a quadro procurando e-mail, nome, token, pedido
ou dado pessoal completo. Se aparecer, masque na interface ou na pós antes de exportar.

**Grave clicando de verdade, não só rolando.** `viewport <w> <h>` muda só o
tamanho da janela — continua desktop, sem media query mobile, sem toque. Só
`set device` ativa o user-agent e o layout mobile reais. Uma gravação que só
rola a página sem nenhum clique prova menos que uma que abre uma ficha/card de
verdade — o produto sendo *usado*, não só *visto*, é a prova que o Modo E
promete.

- Movimento **lento e intencional**: rolagem contínua, pausa em cima do que
  importa, um clique por bloco. Rolagem nervosa é o erro mais comum e ilegível em
  quadro pequeno.
- Grave mais do que precisa e corte depois; regravar sincronizado com a narração
  custa mais que cortar.
- Zero dado pessoal, e-mail, token ou nome real de cliente em quadro.



## Movido de criativo-ads/SKILL.md (26/10/2026)

## B-roll/real do TikTok — vídeos virais em inglês (regra da dona, 16/10/2026)

- **Material real = também TikTok.** Além do banco (`get-brolls`), usar **vídeos orgânicos virais em INGLÊS** do TikTok como cena real (sessão, cuidador, idoso, terapia). É o que faz o criativo parecer orgânico — os originais que modelamos **intercalam MUITA cena real** com o material do produto em cortes curtos.
- **Buscar com ~5 termos em inglês ligados ao PRODUTO.** Ex. (GeriNeuro / idoso / demência): `dementia activities` · `caregiver grandma moment` · `occupational therapy elderly` · `memory care activities` · `elderly cognitive games`. Priorizar **muitas views** (contagem no próprio TikTok).
- **⛔ REGRA DURA: o vídeo NÃO pode ter TEXTO ESCRITO / legenda queimada** — nada de caption embutida, watermark de app, ou texto em outro idioma. Só **cena limpa**; a legenda é a NOSSA (KaraokeV2). **Descarta o clipe que tiver texto.**
- **Perfil logado:** usar o perfil de browser **`tiktok`** (porta 9255). Baixar com **`yt-dlp`** (cookies do perfil quando precisar). Registrar em **`credits.md`**: termo, URL, @autor, **views**, arquivo.
- **Uso na montagem (receita dos originais):** **~15–20 cortes curtos (~2–3s)** alternando o **material do produto** (gravações de tela/fichas) com as **cenas reais** do TikTok, reforçando a fala com overlay de texto.

