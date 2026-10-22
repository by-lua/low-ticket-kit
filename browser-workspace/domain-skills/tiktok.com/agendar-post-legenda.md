# TikTok upload/agendamento — campo de legenda

**Host:** tiktok.com / tiktokstudio.tiktok.com (Carregar → agendar)
**Conta:** @dicasdofantasminha, perfil browser `tiktokshop`

## Legenda: usar `fill`, NUNCA digitar tecla-a-tecla
O campo de legenda é contenteditable e EMBARALHA o texto quando digitado char a
char (hashtags grudam, ordem quebra). Verificado 2026-09-21.

**Certo:** `agent-browser --session tiktokshop fill <ref> "legenda #tiktokshop #modafeminina"`
(seta o valor direto no elemento, de uma vez). Funcionou 100%, hashtags juntas inclusas.
Fallback: copiar pro clipboard (xclip/wl-copy) + Ctrl+V.

## Grade de horários da conta
6 posts/dia: 11 / 13 / 15 / 17 / 19 / 21h (fuso BR). Pico 19h.
Agendador web aceita data/hora futura (dentro do limite ~10 dias).
