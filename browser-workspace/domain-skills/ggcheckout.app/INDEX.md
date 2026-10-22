# ggcheckout.app — index

**Perfil / porta CDP:** `ggcheckoutpnzdona` / 9224
**Subir:** `~/.claude/bin/browsers.sh ggcheckoutpnzdona`
**Playbook de alto nivel:** skill `ggcheckout-produto`

## Por que browser aqui

A API publica do GG Checkout e bloqueada por WAF. Todo o trabalho (produto,
checkout, gateway, entrega, banners) sai pelo painel logado. Existe tambem um
servidor MCP `ggcheckout` com centenas de tools — **tente o MCP primeiro**;
so va de browser quando o MCP nao cobrir a operacao.

## Receitas

Nenhuma gravada ainda.

    cp ../_shared/RECEITA-TEMPLATE.md criar-produto.md

Candidatas:

- `criar-produto.md`
- `configurar-checkout-gateway.md`
- `link-de-entrega.md`
- `upload-banner.md` — upload de arquivo e o caso classico de escalonar
  pro browser-harness se o agent-browser travar

## Fatos verificados do ambiente

- Cloudflare: mesma regra do `_shared/README.md`.

Nada aqui foi validado por execucao nesta sessao. Grave o primeiro fluxo que rodar.
