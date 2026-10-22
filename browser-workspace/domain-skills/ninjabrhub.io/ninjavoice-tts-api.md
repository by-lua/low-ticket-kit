# NinjaVoice (TTS) — API direta, sem browser

Validado por execucao em 2026-09-02 (perfil `hub`).

A tela `/ninja-voice` chama UMA rota, sem auth:

    POST https://captions.ninjabrhub.online/api/captions/tts
    {"text":"...","voiceId":"0s0tckZNA4EDjsNWIGpn","languageCode":"pt-BR"}
    -> {"status":"complete","audio_url":"<GCS assinado, ~12h>","operation_id":"..."}

    GET https://captions.ninjabrhub.online/api/captions/voices  -> 82 vozes

Verificado: `curl` sem cookie/header/API key retorna 200 e WAV valido.

## Checagem de assinatura e o gate real

O gate de assinatura/cota e 100% CLIENT-SIDE, no frontend do Hub:
- `POST supabase/functions/v1/session-validate` {fingerprint, sessionToken, takeover}
  (sessao unica — automacao logada pode derrubar a sessao do humano)
- `POST supabase/rest/v1/rpc/check_generation_limit` {_user_id}
- `GET  supabase/rest/v1/quota_boosts?...`
- telemetria: `POST mind.ninjabrhub.online/api/mind/event` {tool:"ninjavoice",action:"tts_generate"}

Nada disso e exigido por `captions.ninjabrhub.online`. Chamar a rota direto
pula cota, sessao unica e telemetria. Risco: pode ganhar auth/rate limit sem aviso.

## Como captar rota nova nesse site
Hook de `window.fetch` + `XMLHttpRequest` via `agent-browser --session hub eval`,
limpar `window.__log`, clicar no botao, ler o log. O bundle
`ninjabrhub.io/assets/index-*.js` guarda so a base `captions.ninjabrhub.online/api/captions`;
os paths sao montados em runtime.

Projeto que consome isso:
`Documentos/TRAMPO/PROJETOS/WORKING/PROJETOS - INTERNOS/GERADOR-AUDIO-HUB`

## Rodar autenticado (validado 2026-09-02)

    POST supabase/auth/v1/token?grant_type=password
      apikey: <anon do bundle>   {"email","password"}
      -> access_token (1h), refresh_token, user.id

    POST supabase/rest/v1/rpc/check_generation_limit
      apikey + authorization: Bearer <access_token>   {"_user_id": user.id}
      -> {"allowed":true,"plan":"unlimited","remaining":-1,...}

anon key (publica, vem em `assets/index-*.js`):
<jwt>

NAO chame `session-validate` pela automacao: e o controle de sessao unica
(fingerprint + takeover) e pode derrubar a sessao do browser do humano.
Login por senha cria sessao Supabase separada e nao afeta o perfil `hub`.
