# TikTok — busca de vídeos (perfil logado)

Verificado em 2026-09-16 (movido de `gate-demanda.md`). Não faz parte do método MVT;
é ferramenta opcional de leitura de mercado.

- Perfil `tiktok` (porta 9255), já logado. Sem login dá erro de servidor/bot detection.
- `agent-browser --session tiktok open "https://www.tiktok.com/search/video?q=<URL-ENCODED>"`
  → `sleep 14` → screenshot.
- Captcha/checkbox: clicar; falhou 2× → marcar inconclusivo.
- Pane Codex falhou 2× nessa tarefa (render/sessão): preferir rodar no orquestrador.
