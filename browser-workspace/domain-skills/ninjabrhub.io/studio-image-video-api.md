# ninjabrhub.io /studio — imagem e vídeo por API (sem browser)

**Verificado por execução em 2026-09-02.** Imagem E vídeo geram por `curl`/Python
puro, sem browser depois de ter o token. Ferramenta pronta:
`Documentos/TRAMPO/.../GERADOR-AUDIO-HUB/gerar-midia.py`.

## Endpoint único
`POST https://bbwgequqwrsmbrkdmsxm.supabase.co/functions/v1/useapi-proxy`

Motor Google Flow (contas Google rotacionadas pelo backend do Hub — não precisa
de conta Google própria).

- Imagem (síncrono): `{"provider":"google-flow","action":"create_image","payload":{"prompt","model":"imagen-4","aspectRatio","count"}}`
  - aspect: `16:9 4:3 1:1 3:4 9:16 auto landscape portrait`. **NÃO** aceita `square`/`async`.
  - resposta traz `flow-content.google/image/...` assinada (expira ~6h).
- Vídeo (async): `create_video` `payload:{prompt,model:"veo-3.1-lite-low-priority",aspectRatio:"landscape",count:1,async:true}`
  → devolve `jobid` → poll `{"action":"get_video","payload":{"videoId":"<jobid>"}}`
  a cada 10s até `status:"completed"` + url `.../video/...`. ~1min, 8s, 1280×720, com áudio.

## Headers obrigatórios (4)
- `apikey`: anon key do Supabase (pública, fixa).
- `authorization: Bearer <access_token JWT>` — do login do Hub, expira 1h.
- `x-client-info: supabase-js/2.108.2; runtime=web`
- **domain guard** (senão 4xx): `x-domain-hostname: ninjabrhub.io`,
  `x-domain-timestamp: <unix>`, `x-domain-signature: HMAC_SHA256(key, "ninjabrhub.io|<unix>")`.
  Chave estática no bundle: `ninjabr-domain-guard-2024-shared`. Ofuscação, não segredo.

## Token
`access_token` expira 1h. Renova por
`POST {SUPABASE}/auth/v1/token?grant_type=refresh_token` com header `apikey` +
body `{"refresh_token":...}`. **O refresh_token ROTACIONA** a cada troca — regrave
sempre o novo. Fonte inicial do refresh: perfil `hub` logado,
`localStorage['sb-bbwgequqwrsmbrkdmsxm-auth-token'].refresh_token`.

## Como o front escolhe o modo (só relevante se for dirigir a UI)
Barra de criação: botão modo (Imagem/Vídeo, menu radix "CRIAR") + botão ferramenta
(Auto → lista de motores). Botão Enviar tem `aria-label="Enviar"`, fica
`disabled` até ter prompt. FLUX/SDXL na UI davam "Falha" (engine undefined);
Google Flow é o que funciona.
