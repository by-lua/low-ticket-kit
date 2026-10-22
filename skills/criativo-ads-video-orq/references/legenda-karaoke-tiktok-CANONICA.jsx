// LEGENDA KARAOKÊ TIKTOK v2 — CANÔNICA (2026-09-23)
// words.json vem de ~/Developer/legenda-karaoke/align.py (alinhamento forçado roteiro+áudio, NÃO whisper).
// Vídeo e legenda na MESMA composição: sem fundo #0000FF, sem chroma-key (o chroma deixava halo nas bordas).
import { AbsoluteFill, OffthreadVideo, staticFile, useCurrentFrame, useVideoConfig, spring } from "remotion";
import { loadFont } from "@remotion/google-fonts/Montserrat";

const { fontFamily } = loadFont("normal", { weights: ["900"], subsets: ["latin", "latin-ext"] });

const FONT_SIZE = 60;
const CENTRO_Y = 0.70;        // centro vertical da linha = 70% da altura
const CONTORNO = 5;           // px, contorno redondo por fora da letra
const AMARELO = "#FFD400";

// contorno redondo feito de sombras em anel: fica todo por FORA da letra (não come o desenho,
// sem quina serrilhada) + sombra projetada embaixo pra dar profundidade
const anel = Array.from({ length: 24 }, (_, i) => {
  const a = (i / 24) * 2 * Math.PI;
  return `${(Math.cos(a) * CONTORNO).toFixed(2)}px ${(Math.sin(a) * CONTORNO).toFixed(2)}px 0 #000`;
});
const SOMBRA = [...anel, "0 7px 0 #000", "0 10px 14px rgba(0,0,0,0.55)"].join(", ");

export const KaraokeV2 = ({ src, words }) => {
  const frame = useCurrentFrame();
  const { fps, height } = useVideoConfig();
  const t = frame / fps;
  // linha só existe enquanto é falada; nas pausas a tela fica limpa
  const line = words.find((l) => t >= l.start && t < l.end);
  return (
    <AbsoluteFill>
      <OffthreadVideo src={staticFile(src)} />
      {line && (
        <div
          style={{
            position: "absolute",
            left: "4%",
            width: "92%",
            top: height * CENTRO_Y,
            transform: "translateY(-50%)",
            display: "flex",
            flexWrap: "wrap",
            justifyContent: "center",
            gap: "0 26px",
            fontFamily,
            fontWeight: 900,
            fontSize: FONT_SIZE,
            lineHeight: 1.25,
            textAlign: "center",
            textTransform: "uppercase",
            letterSpacing: "0.5px",
          }}
        >
          {line.words.map((w, i) => {
            const active = t >= w.start && t < w.end;
            // pop curto quando a palavra entra (escala 1.0 -> ~1.07 -> 1.05; gap 26px absorve)
            const pop = active
              ? 1 + 0.05 * spring({ frame: frame - Math.round(w.start * fps), fps, config: { damping: 12, stiffness: 220 } })
              : 1;
            return (
              <span
                key={i}
                style={{
                  color: active ? AMARELO : "#FFFFFF",
                  textShadow: SOMBRA,
                  display: "inline-block",
                  transform: `scale(${pop})`,
                }}
              >
                {w.text}
              </span>
            );
          })}
        </div>
      )}
    </AbsoluteFill>
  );
};
