# YouTube — busca e comentários recentes sem browser

Verificado em 2026-09-16 (movido de `criacao-low-ticket-mvt/references/gate-demanda.md`).
Uso no método MVT: framework lista "youtube + comentários (tá tendo comentário
recente?)" para verificar se uma concepção nova tem demanda.

## Por que sem browser
Nos perfis `adslib`/`adslib2` o YouTube renderizou vazio (innerText ""). Ler direto.

## Busca (id, título, views, data)
```bash
python3 "…/LOW-TICKET/MINERACAO/scripts/yt-busca.py" "COD|termo de busca" "COD2|outro termo"
```
Lê `ytInitialData` de `youtube.com/results?search_query=`. Filtro de recentes na URL:
`&sp=CAI%253D`.

## Comentários mais recentes
```bash
yt-dlp -q --skip-download --write-comments \
  --extractor-args "youtube:comment_sort=new;max_comments=40,all,0" \
  -o cm/COD -- <videoId>
```
Filtre `timestamp` dos últimos ~90 dias no `.info.json`.

## Leitura
- Termo como o comprador digita (2–3 palavras), não a headline.
- Comentário recente pedindo/perguntando/elogiando o tema = sinal. Vídeo de 3+ anos,
  poucas views e nenhum comentário recente = sinal fraco.
- Cite 1–2 comentários literais com data; não invente número.
