---
name: flow-video-playwright
description: Mecânica ÚNICA do Google Flow (flow.google.com) — gera imagem e vídeo (Omni Flash/Veo, Nano Banana), inclusive com imagem de referência anexada (cenário, produto, frame inicial), pelo wrapper scripts/flow.sh (gflow-cli no Chrome real do perfil flow-gflow + anexo + ritmo compartilhado entre agentes + freio de bloqueio). Use sempre que qualquer skill ou pedido precisar gerar imagem/vídeo no Flow. NUNCA gere no Flow por agent-browser nem pelos perfis flow-enovalabs-pro* (dá "atividade incomum").
---

# Google Flow — mecânica (reescrita 22/10/2026)

> Versão antiga (fluxo agent-browser, seletores, lanes) arquivada em
> `~/.claude/skill-backups/flow-video-playwright-2026-10-22.md`. **Não use.**

## Regra única

**Todo envio ao Flow passa por `~/.claude/skills/flow-video-playwright/scripts/flow.sh`.**

- **Proibido:** `agent-browser` no Flow, perfis `flow-enovalabs-pro`, `-2/-3/-4`,
  `browsers.sh flow-*`, `flow-livre.sh`, `lane.sh take flow`. Esses rodam Chromium
  e o reCAPTCHA do Flow marca "atividade incomum" (aconteceu várias vezes em 21-22/10).
- **Proibido:** chamar `scripts/gflow_ref.py` direto ou passar `--profile` — fura a fila/ritmo
  e trava o perfil pros outros agentes (aconteceu 22/10: exit 11 "Profile locked").
- **Proibido:** chamar `gflow` puro pra gerar (fura o ritmo compartilhado e, nesta
  conta, recusa imagem de referência).
- **POV-Bruno do TikTok Shop:** nem chame o `flow.sh` direto — use
  `tiktok-shop/scripts/pov-flow.sh` (ele já chama o `flow.sh`).

## Comandos

```bash
F=~/.claude/skills/flow-video-playwright/scripts/flow.sh

$F status                                   # estado de CADA perfil: logado? resfriamento? envios? gerando?
$F check                                    # checagem REAL de login (abre o Flow em cada perfil)
$F novo-projeto                             # imprime o id (crie 1 projeto por leva/produto e reuse)
$F image t2i --project <id> --out <dir> "<prompt>"
$F image i2i --project <id> --ref a.png --ref b.png --out <dir> "<prompt>"       # até ~3 refs
$F video t2v --project <id> --model omni-flash --duration 8 --out-dir <dir> "<prompt>"
$F video i2v --project <id> --initial-frame cena.png --model omni-flash --duration 8 --out-dir <dir> "<prompt>"
```

- Imagem: Nano Banana 2.1, sai `.jpg` 768×1376 em `<dir>` (converta se precisar png).
- Vídeo: Omni Flash 720×1280, `--duration` 4/6/8/10. Sai com transfer sRGB → antes
  de usar, re-etiquete bt709:
  ```bash
  ffmpeg -i in.mp4 -vf "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv" \
    -c:v libx264 -crf 18 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 out.mp4
  ```
  (só `-color_trc` não basta no ffmpeg atual; sem isso = tela verde em player.)
- Prompt de i2i: refira-se às referências pela ordem ("the FIRST attached image…",
  "the SECOND…"). Prompt de i2v: "the attached image coming to life: …".
- Toda saída, inclusive erro com traceback, vai pro stdout do `flow.sh` — salve num log.
- **Outro perfil (perfil principal ocupado ou deslogado):** `FLOW_PROFILE=flow-gflow-2 $F ...`.
  Ritmo e fila continuam compartilhados (mesma conta); login caído e resfriamento ficam POR PERFIL
  (`login-needed-flow-gflow-2`, `cooldown-until-flow-gflow-2`). `novo-projeto` só cria no perfil
  principal: no perfil 2, reuse um `--project` existente (La Jefa Rosa: `e20d861b-d86e-485b-b90e-3503d563b944`).

## Lições de 22/10/2026 (tarde — La Jefa Rosa, 7 vídeos)

1. **Imagem da cena SEMPRE antes do vídeo**, no próprio Flow (`image i2i` com persona + quadro de
   referência da cena), depois `video i2v` dessa imagem. Vídeo com várias cenas = uma imagem por cena.
   Vídeo direto do texto, ou de imagem de outra cena, alucina.
2. **Prompt de movimento LONGO e detalhado** (o Flow é complexo):
   - câmera fixa e quem filma;
   - **em qual mão está cada objeto do começo ao fim**;
   - ação **por segundo** (0–3 s, 3–6 s, 6–8 s);
   - bloco de continuidade: objeto não some nem troca de mão, óculos não somem, 5 dedos, rosto e roupa
     iguais, fundo parado, sem fala.

   Prompt curto ("toma um gole e abaixa os óculos") fez o copo sumir da mão.
3. **Um clipe só, até 8 s.** Algo sumiu ou derreteu no fim: **cortar antes** no ffmpeg, não regerar. O QA
   olha o FIM do clipe num contact sheet de 2–4 fps.
4. **Nunca matar uma geração no meio e reenviar em seguida**: dois envios colados dão "atividade incomum"
   na hora. Pausar só no intervalo entre envios.
5. **Matar processo por PID**, nunca `pkill -f gflow_ref.py`: casa com o próprio shell (exit 144) e com a
   geração de OUTRO pane.
6. **Perfil novo:** copiar o diretório do perfil dura ~25 min (depois o Google pede "Confirme que é você").
   Perfil durável = `DISPLAY=:1 gflow auth login --profile <nome> --browser chrome`, com a usuária
   confirmando. **Nunca abra o perfil do gflow num Chrome comum/CDP**: os cookies são regravados com outro
   chaveiro e o gflow cai em `flow.google.com/about`.
7. **Subir VÍDEO no Flow** (Omni Flash editando vídeo, troca de personagem) abre "Direitos de uso deste
   vídeo". Vídeo de terceiro: **não aceitar em nome da usuária**. Pra vídeo nosso, script pronto em
   `~/.claude/skills/modelar-perfil-social/scripts/flow_swap.py`.
8. Lote de vídeos modelados (imagem → clipe → montagem com música do original + texto de story), já pelo
   `flow.sh`: `~/.claude/skills/modelar-perfil-social/scripts/lote_flow.py`.

## O que o `flow.sh` faz por você

| Proteção | Como |
|---|---|
| Rodízio de perfis (igual `gpt-livre.sh`) | perfis = todo `~/.local/share/gflow-cli/profile_*` (hoje `flow-gflow` e `flow-gflow-2`, mesma conta `contato.minhaempresa` → projetos valem pros dois). Cada envio pega o perfil logado, fora de resfriamento, livre e com menos envios. **Não passe `--profile`.** Perfil novo: `gflow auth login --browser chrome --profile flow-gflow-N` e pronto |
| Login checado de verdade | `gflow auth status` ERRA (diz deslogado com sessão boa). `flow.sh check` abre o Flow: caiu em `/about` = deslogado (marca e pula o perfil). Perfil que cai no meio de um envio é marcado e o envio repete no próximo |
| Fila entre agentes | `flock` por perfil (`~/.cache/pov-flow/<perfil>.lock`): 1 envio por vez em cada perfil; com 2 perfis, 2 agentes geram em paralelo |
| Ritmo humano por perfil | 45–120s entre envios e máx. 8 por 30 min por perfil (`~/.cache/pov-flow/<perfil>.sends`) |
| Freio de bloqueio | "atividade incomum"/exit 10 → 45 min de resfriamento só naquele perfil; não reenvia automático |
| Retry seguro | falha antes do envio (exit 23, sem gasto) → 1 nova tentativa |
| Anexo de imagem | `gflow_ref.py`: a conta recebe o composer "agent-only" (gflow #799), onde o gflow puro recusa `--ref`/`--initial-frame`; o driver anexa pelo "+" → Enviar mídia → item → (Incluir no comando) e confere pela contagem de anexos |

## Códigos de saída

| exit | significa | o que fazer |
|---|---|---|
| 0 | ok | — |
| 10 | Flow bloqueou (atividade incomum) | **parar**; avisar a usuária o horário de volta |
| 76 | nenhum perfil disponível (todos deslogados/em resfriamento) | `flow.sh status`; pedir à usuária o login do perfil indicado; depois `flow.sh check` |
| 23 | tela/anexo mudou (já tentou 2x) | 1 print do incidente (`~/.local/share/gflow-cli/incidents/`), avisar; não chutar seletor |
| 25 | o agente do Flow respondeu diferente (ex.: "4 vídeos na fila onde pediu 1", "Algo deu errado") | conferir o projeto no Flow antes de reenviar (pode já ter gerado) |
| outro | ver traceback no log | — |

Login caiu: `flow.sh check` diz qual perfil; a usuária roda
`gflow auth login --browser chrome --profile <perfil>` (janela do Chrome, "Confirme que é você"),
depois `flow.sh check` libera o perfil.

## Armadilhas já tratadas no driver (não reimplemente)

1. Upload vira tile na grade → o anexo é feito antes do gflow medir a linha de base.
2. O Flow às vezes abre o visualizador da mídia enviada ("O que você quer mudar?");
   o driver fecha e só envia no campo "O que você quer criar?".
3. O seletor de mídia varia por projeto (clicar já inclui OU abre prévia com
   "Incluir no comando"); tratado, com retry.
4. Espera do upload olha só o item enviado.
5. Limpar anexo antigo nunca manda mídia pra lixeira (se aparecer, clica "Desfazer" e para).
6. `gflow project create` cria id que o flow.google.com não acha → `flow.sh novo-projeto`
   cria pelo botão "Novo projeto" do site.

## Recuperar vídeo quando o envio sai com exit 25 (22/10/2026)

O agente do Flow às vezes pede **"Aprovar"** antes do vídeo e o driver sai com exit 25, mas **a geração continua**
no projeto. Não reenvie. Espere ~3 min e:
1. `cd <tmp>; flock ~/.cache/pov-flow/<perfil>.lock env DISPLAY=:1 ~/.local/share/uv/tools/gflow-cli/bin/python ~/.claude/skills/flow-video-playwright/scripts/flow_listar_projeto.py <perfil> <project_id>`
   (abre o projeto em flow.google.com e salva as respostas em `bodies.json`; o `fetch_project_listing` do gflow dá
   `AuthExpiredError` porque o host migrou). O media id é o UUID cuja legenda = o prompt de movimento enviado.
2. `flock ~/.cache/pov-flow/<perfil>.lock env DISPLAY=:1 gflow video upscale <media_id> --scale 720p --project <id> --profile <perfil> --out <dir>`
   (720p = baixar o original, sem custo). Depois renomeie pra `clip.mp4` e rode o lote de novo (só monta).
