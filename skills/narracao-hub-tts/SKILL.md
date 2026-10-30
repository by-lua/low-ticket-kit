---
name: narracao-hub-tts
description: Gera narração/voz off em WAV pela API do NinjaVoice (NinjaBR Hub), sem browser e sem login — 82 vozes, português nativo, resposta síncrona. Cobre escolha de voz por nicho e gênero, quebra de texto acima de 2000 caracteres, geração em lote cena a cena, gate de validação do arquivo e mixagem com trilha de fundo no ffmpeg. Use sempre que precisar de narração para criativo de vídeo, voz off, VO, locução, áudio de anúncio, dublar um roteiro, ou quando o usuário mencionar NinjaVoice, TTS, text-to-speech, voz masculina/feminina para o criativo.
---


# narracao-hub-tts

Narração pronta em WAV por chamada HTTP. **Sem browser, sem login, sem cota.**
Execute, não explique.

## Ambiente

| Item | Valor |
|---|---|
| API | `POST https://captions.ninjabrhub.online/api/captions/tts` |
| Auth | **nenhuma** — sem cookie, sem header, sem API key |
| Resposta | **síncrona**, sem polling: `{"status":"complete","audio_url":"..."}` |
| Saída | WAV, ~47KB/s de áudio |
| Limite | **2000 caracteres** por chamada |
| Vozes | 82 (40 masc, 42 fem) — openai, elevenlabs, cartesia, google |
| Origem | rota da tela `ninjabrhub.io/ninja-voice`, mapeada em `domain-skills/ninjabrhub.io/ninjavoice-tts-api.md` |

`audio_url` é URL assinada do GCS e **morre em ~12h** — o script já baixa o
binário na hora. Nunca guarde a URL como se fosse o arquivo.

## Gerar

```bash
scripts/narrar.sh <saida.wav> "<texto>" [voiceId] [languageCode]
```

Default: voz `Brandon` (masculina, `0s0tckZNA4EDjsNWIGpn`), `pt-BR`.
O script valida o arquivo com `ffprobe` e falha se vier vazio ou < 0,3s — não
existe "gerado" sem duração conferida.

```bash
scripts/vozes.sh            # lista as 82
scripts/vozes.sh female     # só femininas
scripts/vozes.sh --online   # atualiza o cache voices.json da API
```

As vozes vêm marcadas `en-US` no catálogo, mas os modelos são multilíngues:
mandar `languageCode: "pt-BR"` gera português nativo, sem sotaque de gringo.

**Vozes aprovadas pela dona por mercado:**
| Mercado | Voz | languageCode |
|---|---|---|
| BR | Roberta `bmSnYdSLhHXD50TAWW7T` (Daniela soa de Portugal, não usar no BR) | `pt-BR` |
| PT | Daniela `9L8v6Oy5x46GlKUxRg6H` | `pt-PT` |
| ES neutro latino | Brittney `4wRMNoWpnF0F0r5LTRHM` (aprovada ouvindo, 05/10/2026) | `es` — a API RECUSA `es-419` e `es-MX` ("TTS generation failed") |

Worker não consegue ouvir: voz nova escolhida por metadado é provisória até a dona ouvir.

## Escolha da voz — regra de nicho

**O gênero da voz sai do nicho, não do gosto de quem edita.** Voz fora do nicho
lê como anúncio de fora, não como alguém de dentro:

| Nicho | Voz |
|---|---|
| serralheria, mecânica, obra, pesca, caminhão, agro | masculina |
| cozinha, artesanato, maternidade, beleza, decoração | feminina |
| finanças, saúde, pet, educação — público misto | teste as duas |

Público misto: teste as duas vozes em criativos **de ângulo diferente** (cada um
com a sua dor/persona), não no mesmo roteiro só trocando a voz. Desde 2026, criativo
igual com outra voz é variação rasa, que o Meta agrupa com o original (ver
`criativo/references/kevones-criativo.md`). Deixe o CPA decidir. Nunca as duas no mesmo criativo.

Escolhida a voz de um projeto, **ela não muda entre cenas.** Trocar de voz no meio
denuncia a montagem na hora.

## Roteiro longo — quebra por cena, não por caractere

Acima de 2000 chars a API recusa. Mas mesmo abaixo disso, **gere uma cena por
arquivo**, não o roteiro inteiro num WAV só: cena a cena você corta silêncio,
troca uma frase e sincroniza com o vídeo sem regerar tudo.

```bash
i=1
while read -r linha; do
  scripts/narrar.sh "vo/cena-$i.wav" "$linha" "$VOZ"
  i=$((i+1))
done < roteiro.txt
```

Pontuação manda no ritmo: vírgula = respiro curto, ponto = pausa. Roteiro sem
pontuação sai atropelado. Número por extenso ("dezessete e noventa", não
"R$ 17,90") — símbolo e dígito são lidos errado.

## Montagem com trilha

Narração seca sobre gravação de tela soa como suporte técnico. Trilha sempre,
instrumental e sem letra — letra briga com a narração pelo mesmo canal.

```bash
# junta as cenas
ffmpeg -nostdin -f concat -safe 0 -i lista.txt -c copy vo/narracao.wav

# mixa com a trilha 20 dB abaixo, cortando a música no fim da narração
ffmpeg -nostdin -i vo/narracao.wav -i trilha.mp3 -filter_complex \
  "[1:a]volume=-20dB[m];[0:a][m]amix=inputs=2:duration=first:dropout_transition=0[a]" \
  -map "[a]" audio-final.wav
```

**−18 a −22 dB abaixo da voz.** Se você percebe a música, está alta demais.
Uma trilha por criativo, contínua do primeiro ao último frame — trocar de música
no meio parece emenda de dois vídeos. Trilha coerente com o gatilho: música
alegre não entra em criativo de dor. Banco livre de royalties (Pixabay Music,
Mixkit, Free Music Archive); música comercial derruba o anúncio por direitos.

Corte de silêncio antes de montar — cabeça, cauda **e pausas internas**:

```bash
ffmpeg -nostdin -i vo/cena-1.wav -af silenceremove=start_periods=1:start_threshold=-45dB:stop_periods=-1:stop_threshold=-45dB:stop_duration=0.35 vo/cena-1-tight.wav
```

## CTA falado — só o comando (regra da dona, 04/10/2026)

A última fala do VO é **uma frase de comando, curta**. Nada de condição de compra:
sem "pagamento único", "acesso vitalício", "garantia de X dias", preço, "sem
mensalidade", "dá pra imprimir", "aceita os termos" nem lista de benefício.
Empilhar condição faz parecer complicado e levanta objeção.

- Tom canônico, curiosidade (comando + o que vai descobrir): "Clica aqui embaixo e descobre como." / "Clica no link aqui embaixo e conhece o manual." / "Clica aqui embaixo e vê por dentro."
- Ruim: "Pagamento único, acesso vitalício, dá pra imprimir. Clica aqui embaixo e vê por dentro."

Isso vale pra vídeo/VO. Estático e carrossel podem mostrar garantia/vitalício
(ex.: `modelagem-escalados/references/carrossel-demonstrativo-iphone.md`).
Condição de compra no áudio fica só na página de vendas/checkout e, se precisar,
no texto do anúncio (`anuncio.md`). Ao gerar o VO, confira a última cena antes de chamar o script.

## Onde este TTS entra, e onde NÃO entra

- **Entra:** narração off (VO), criativo sem rosto, Modo E (Vitrine Guiada) da
  skill `criativo-ads-video-orq`, áudio de gravação de tela, legenda falada.
- **NÃO entra:** cena com personagem em quadro falando. Ali a voz nasce junto do
  vídeo no Veo, com lip-sync — colar TTS por cima de boca gerada nunca bate.

Regra da skill de criativo que continua valendo: **nunca misture** narração off e
personagem falando dentro do mesmo criativo.

## Risco

API não autenticada e não documentada, do fornecedor. Pode ganhar auth, rate
limit ou sumir sem aviso. Se começar a dar 4xx/5xx, é isso — não é o script.
Fallback documentado (login Supabase + `check_generation_limit`) está em
`~/.claude/browser-workspace/domain-skills/ninjabrhub.io/ninjavoice-tts-api.md`.

**Nunca chame `functions/v1/session-validate`.** É o controle de sessão única do
Hub — derruba a sessão do browser do humano.

## Referências

- `scripts/narrar.sh` — gera e valida o WAV
- `scripts/vozes.sh` — lista/atualiza as 82 vozes (`voices.json`)
- `domain-skills/ninjabrhub.io/ninjavoice-tts-api.md` — mapeamento da rota
- `PROJETOS - INTERNOS/GERADOR-AUDIO-HUB` — mesma API em workflow n8n
