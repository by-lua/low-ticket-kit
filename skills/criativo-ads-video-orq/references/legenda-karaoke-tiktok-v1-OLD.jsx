// LEGENDA KARAOKÊ TIKTOK — CANÔNICA (padrão fixo do dono, "sempre usar ela")
// Referência aprovada: v4_imperatriz.mp4 (oferta Mapa do Tarot).
// Remotion word-by-word (hyperframes). NÃO usar ASS/drawtext.
// Compor como ÚLTIMA camada por cima do vídeo montado (chroma-key do #0000FF),
// senão o encode/concat final derruba a legenda.
//
// words.json: [{ start, end, words: [{ text, start, end }] }, ...]
//   linha = chunk de 2-3 palavras; cada word tem seu start/end.
//
// *** TIMESTAMP: NUNCA WHISPER *** (regra global do dono — nem render, nem timing).
//   Gere os start/end das palavras por: (a) TTS que devolve timing (MiniMax T2A),
//   (b) forced-alignment NÃO-whisper (aeneas), (c) reaproveitar a grade de tempos de um
//   VO gêmeo já timestampado trocando só as palavras que mudam, ou (d) distribuir por duração.
//   Proibido faster-whisper/whisperx/whisper.cpp em qualquer etapa.
//
// PARÂMETROS FIXOS (golden = v4_imperatriz.mp4):
//   fontFamily : Arial/Helvetica sans, fontWeight 900 (bold pesada)
//   fontSize   : 60 (canvas 1080x1920) — decisão do dono 2026-09-23 (v4 medido era ~72).
//   textTransform: uppercase
//   cor base   : #FFFFFF (branco puro)
//   cor ativa  : #FFD400 (amarelo forte) na palavra sendo falada, anda palavra-a-palavra
//   contorno   : WebkitTextStroke 6px #000000, paintOrder "stroke fill"
//   largura    : 94% da tela, flex-wrap, centralizado, gap 0 10px, lineHeight 1.2
//   posição    : CENTRO vertical em 70% da altura (y=1344 no 1920), via top+translateY(-50%)
//                -> centra igual com 1 ou 2 linhas. Dentro da banda 4:5, fora do rodapé. Decisão 2026-09-23.
//   fundo      : #0000FF (chave de cor pra overlay) ; fps 30 ; 1080x1920

import { Composition, useCurrentFrame, useVideoConfig, AbsoluteFill } from "remotion";
import words from "./words.json";

const FPS = 30;
const DURATION = 30.6; // ajustar à duração do vídeo

function Caption() {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const line = words.find((l) => t >= l.start && t < l.end);
  return (
    <AbsoluteFill style={{ backgroundColor: "#0000FF" }}>
      {line && <div
        style={{
          position: "absolute",
          left: "3%",
          width: "94%",
          top: 1344, // 70% de 1920
          transform: "translateY(-50%)",
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          gap: "0 10px",
          fontFamily: "Arial, Helvetica, sans-serif",
          fontWeight: 900,
          fontSize: 60,
          lineHeight: 1.2,
          textAlign: "center",
          textTransform: "uppercase",
        }}
      >
        {line.words.map((w, i) => {
          const active = t >= w.start && t < w.end;
          const color = active ? "#FFD400" : "#FFFFFF";
          return (
            <span key={i} style={{ color, WebkitTextStroke: "6px #000000", paintOrder: "stroke fill" }}>
              {w.text}
            </span>
          );
        })}
      </div>}
    </AbsoluteFill>
  );
}

export const RemotionRoot = () => (
  <Composition id="Captions" component={Caption}
    durationInFrames={Math.round(DURATION * FPS)} fps={FPS} width={1080} height={1920} />
);
