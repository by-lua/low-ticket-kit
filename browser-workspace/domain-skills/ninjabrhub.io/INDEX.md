# ninjabrhub.io — index

**Perfil / porta CDP:** `hub` / 9223
**URL de trabalho:** https://ninjabrhub.io/studio
**Subir:** `~/.claude/bin/browsers.sh hub`
**Login:** persistido no perfil. Senha em `$NINJABR_PASSWORD`
(`~/.claude/.credentials.env`, chmod 600) — carregue com
`set -a; source ~/.claude/.credentials.env; set +a` e use sempre a variavel,
nunca o valor literal.
**Playbooks de alto nivel:** skills `grok-video-hub-playwright`, `video-hub`

## Receitas

- `ninjavoice-tts-api.md` — TTS por HTTP puro, sem browser e sem auth.
- `studio-image-video-api.md` — imagem (imagen-4) e video (veo-3.1) por API, sem browser (tem auth). VERIFICADO.
- `gpt-image-2-artlist.md` — GPT Image 2 (motor Artlist) por API: o motor a usar quando a imagem PRECISA ter texto correto. Plano ilimitado, sem fila. VERIFICADO.
- `imagem-lote-serializado.md` — gerar VARIAS imagens: fila de uma por vez (`generation_busy` 429), token rotacionado, e por que nao pedir texto na imagem. VERIFICADO.
- `login-e-token.md` — relogar o perfil e regravar o refresh_token quando vier `refresh_token_already_used`; um dono por vez. VERIFICADO.
- `kalodata-tiktok-shop-spy.md` — Kalodata = NinjaSpy → Catálogo TikTok Shop (proxy `fastmoss-proxy`, não `ninjaspy-proxy`); caminho de navegação certo e travamento conhecido de backend (pedido fica pendente sem erro). VERIFICADO.

    cp ../_shared/RECEITA-TEMPLATE.md imagem-para-video.md

Candidatas:

- `imagem-para-video.md` — modo Imagem→Video, clipe 6s/10s com voz e ambiente
- `veo-3-1.md` — motor padrao do pipeline de criativo
- `fallback-grok-imagine.md` — quando a cota do Veo acaba
- `cota-e-limites.md` — como o site sinaliza cota estourada

## Fatos verificados do ambiente

- Motores disponiveis no hub: Grok Imagine, Veo, Seedance.
- Pipeline de criativo (`video-hub`): Veo 3.1 e o padrao, Grok Imagine e fallback.
- Cloudflare: mesma regra do `_shared/README.md`.

Nada aqui foi validado por execucao nesta sessao. Grave o primeiro fluxo que rodar.
