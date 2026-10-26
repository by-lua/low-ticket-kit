---
name: criativo-ads-video-orq
description: "MECÂNICA DE VÍDEO de anúncio, chamada pela orquestradora criativo-ads (que decide quantas peças e qual modo em cada slot). Cobre os modos de vídeo (demonstrativo, expert, UGC, caixa de perguntas/expert respondendo, imagem animada, corte TikTok, print+POV, copo azul), a EDIÇÃO PADRÃO única de todo vídeo (corte por frase, split 70/30, legenda KaraokeV2 com alinhamento forçado, velocidade 1.0, trilha contínua, card CTA, QA), geração de personagem/take com IA no Flow (imagem de referência, dentes, voz, anti-morphing, QA de clipe), b-roll (get-brolls/TikTok), gravação de tela, montagem técnica (Remotion/ffmpeg/video-use) e narração (narracao-hub-tts). Use para qualquer criativo de vídeo, UGC, expert, demonstrativo, hook, b-roll, legenda, montagem, Flow/Veo."
---

# criativo-ads-video-orq — mecânica de vídeo

> Vídeo NÃO começa aqui: começa na **TRILHA DO CRIATIVO** de `criativo-ads` (Kevones → Rodrigo + nossos
> formatos → roteiro). Esta skill é o passo 5b: produzir e montar. Hub de vídeo desativado → Flow.

**Vale pra TODO vídeo do portfólio, qualquer oferta, qualquer agente.** Não existe "legenda daquela
oferta" nem "edição desse criativo": existe UMA edição. Faltou dependência (venv da legenda, Remotion)?
Resolve a dependência — nunca troca de método.

## As 3 coisas que esta skill faz — leia só a que precisa

| Preciso de… | Arquivo | O que tem |
|---|---|---|
| **Qual vídeo é** (modo) | `references/estilos-de-video.md` — **GUIA DE VÍDEO** | cada modo: roteiro, quem fala, quais cenas entram; mapeamento de assets (Passo 0) |
| **Como editar** (igual em TODO modo) | `references/EDICAO-PADRAO.md` — **ler inteiro antes de montar** | ordem de montagem, corte, layouts, velocidade, legenda, áudio, card CTA, QA bloqueante |
| **Gerar cena com IA** (personagem/expert/UGC/take) | `references/geracao-1-conceito-e-imagem.md` → `references/geracao-2-video-e-qa-clipe.md` + `references/mecanica-flow.md` | orçamento de fala (16 palavras/8 s), imagem de referência, dentes, voz, prompt de vídeo, anti-morphing, QA de clipe, erros comuns |

Apoio, quando o passo pedir:
- `references/takes-mesa-real.md` — catálogo de takes A–O (imagem → Flow) e regras de mesa real
- `references/broll-e-tela.md` — buscar b-roll (get-brolls, TikTok, Pinterest) e gravar tela
- `references/briefing.md` — o que ler antes do roteiro; a narração fala com QUEM COMPRA
- `references/legenda.md` — spec técnica completa da KaraokeV2 e fallback
- `references/montagem-tecnica.md` — ferramentas, ffmpeg, layouts, mix, trilha, Drive
- `references/acabamento-natural-audio-cortes.md` — limpeza de áudio e cortes por fala/gesto
- `references/HISTORICO-REGRAS-VIDEO.md` — incidentes e regras na forma original (consulta; onde contradiz o EDICAO-PADRAO, vale o EDICAO-PADRAO)

## Fluxo de um vídeo

1. **Modo + `anuncio.md` na mesma passada (regra 26/10/2026, não deixar pro fim)** — achar a linha no
   GUIA DE VÍDEO (vem do plano da leva). Roteiro completo pelo
   `criativo-ads/references/ROTEIRO-POR-FORMATO.md`: hook (dor) → mecanismo → CTA (só comando) **+
   `criativo-ads/references/texto-anuncio-por-angulo.md`** pra já escrever a 1ª frase do Texto
   principal do `anuncio.md` endereçando quem compra ("Si sos...", "Si tu mamá...") — o hook do
   VÍDEO pode ser só a dor/cena; o texto de FORA (o post) sempre chama a persona, não só descreve.
2. **Assets** — Passo 0 do GUIA (gravações da dona, takes Flow, b-roll 3D, card CTA). Tela é sempre da dona.
3. **Gerar o que falta** — voz (`narracao-hub-tts`, voz fixa da leva, conferir gênero), personagem/take
   (geração 1 → 2, Flow), b-roll (`get-brolls`).
4. **Montar pelo `EDICAO-PADRAO.md`** — do §1 ao §9.
5. **Entregar** — final solto na raiz de `CRIATIVO-N/`, resto em `intermediarios/`, confere o
   `anuncio.md` já escrito no passo 1 (gate da 1ª frase), registrar no STATUS da oferta.

## Regras de execução (curtas)

- **Imagem antes do vídeo**, sempre (nunca texto→vídeo). Prompts de geração em inglês; a fala no idioma da peça.
- **O disco é a verdade:** antes de dizer "feito", abre o arquivo (data + frame). Correção em background não
  é correção até o arquivo provar.
- **Loop de leva:** você é acordado de novo via `ScheduleWakeup`, cada wakeup faz um pedaço verificável;
  dois wakeups sem arquivo novo = travou, investigue. Nunca devolver o turno "aguardando".
- **Nunca apagar** clipes-fonte (`CRIATIVO-*/VIDEO/cena-*.mp4`).
- Defeito visto no QA é defeito reportado — nunca "deixa passar".

## Skills-filhas — invoque, não reescreva

| Skill | Para quê |
|---|---|
| `gpt-imagem-playwright` | imagem de referência no ChatGPT |
| `flow-video-playwright` + `references/mecanica-flow.md` | vídeo no Flow (Veo) |
| `narracao-hub-tts` | voz off (API NinjaVoice, liberada) |
| `get-brolls` | b-roll com origem/licença |
| `video-use`, `remotion-*`, `hyperframes-*` | cortes por palavra, composição, motion |

Seletor mudou? Corrige na skill-filha, nunca aqui.
