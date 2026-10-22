# chatgpt.com — index

**Perfil / porta CDP:** `gpt` / 9222
**Subir:** `~/.claude/bin/browsers.sh gpt`
**Login:** persistido no perfil do Chromium do sistema. Nunca use `agent-browser open`
(Chromium empacotado nao guarda login e trava no Cloudflare).
**Playbook de alto nivel:** skill `gpt-imagem-playwright`

## Receitas

Nenhuma gravada ainda. Grave a primeira com:

    cp ../_shared/RECEITA-TEMPLATE.md gerar-imagem-com-referencia.md

Candidatas obvias, na ordem em que provavelmente vao aparecer:

- `gerar-imagem-com-referencia.md` — anexar imagem de referencia, gerar, baixar
- `gerar-lote-imagens.md` — ate 10 imagens separadas por vez
- `baixar-resultados.md` — onde os arquivos caem, como renomear

## Fatos verificados do ambiente

- Cloudflare: checkbox "Confirme que e humano" e clicavel pela automacao neste
  perfil e valida normal. Reapareceu? Clique de novo. Falhou 2x ou pediu 2FA:
  chame o usuario.
- Downloads de lane passam por `~/Downloads/PLAYWRIGHT/<lane>/`.

Nada aqui foi validado por execucao nesta sessao — o que esta acima vem da
config do ambiente, nao de um passo-a-passo rodado. Primeiro fluxo que voce
rodar, grave.
