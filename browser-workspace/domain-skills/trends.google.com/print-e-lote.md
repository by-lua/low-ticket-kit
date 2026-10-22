# Google Trends — print confiável e lote de termos

Verificado em 2026-09-16 (movido de `gate-demanda.md`). Complementa
`ler-interesse-ao-longo-do-tempo.md`.

```bash
~/.claude/bin/browsers.sh trends
agent-browser --session trends open "https://trends.google.com/trends/explore?date=today%205-y&geo=BR&q=<URL-ENCODED>&hl=pt-BR"
sleep 22   # widget leva 15–20 s; print cedo sai branco. NÃO reabra a URL (reinicia o timer)
agent-browser --session trends screenshot <arquivo>.png
```
- O gráfico é iframe cross-origin: `eval` não lê; leia a imagem.
- Lote: `sleep 22` para carregar + `sleep 8` entre termos (9 seguidos sem 429). 429 =
  esperar e retomar, não é demanda zero.
- Recorte para ler vários: `magick full.png -crop 1080x300+60+440 -resize 55% c.png` e
  `magick c*.png -append junto.png`.
- Termo com 2–3 palavras; nome longo não renderiza → encurte mantendo o núcleo.
