# Stripe — MCP e CLI por conta

Revisado em 10/11/2026. Fonte de conta/organização: `SKILL.md` e `_memoria/contas-e-codigos.md`. Os nomes de variáveis abaixo identificam a conta, nunca contêm segredos.

## MCP oficial (preferido)

Endpoint oficial remoto: `https://mcp.stripe.com`. Preferir OAuth; não instalar servidor local antigo `@stripe/mcp`. Em Codex:

```bash
codex mcp add stripe --url https://mcp.stripe.com
# Se o add não iniciou OAuth, ou numa retomada:
codex mcp login stripe --no-browser
```

Em Claude Code:

```bash
claude mcp add --transport http stripe https://mcp.stripe.com/
# Depois abrir /mcp e concluir OAuth.
```

Abrir o consentimento no perfil persistente do navegador reservado à Stripe. Selecionar a organização e a conta da oferta (conferir o `acct_...` esperado); nunca a conta de outra oferta. Conceder só o acesso necessário. Separar teste/live. Não concluir consentimento de conta errada.

Registrar MCP não injeta ferramentas em uma conversa já iniciada: pode ser necessário iniciar nova sessão. Quando presentes, usar `get_stripe_account_info` antes das operações, `stripe_api_search`/`stripe_api_details` para consultar o contrato, e `stripe_api_read`/`stripe_api_write` para a operação. Conferir a resposta efetiva. Não executar um agente novo apenas para contornar ferramentas ausentes.

Se OAuth não estiver disponível, a documentação atual prevê **agent API key** com escopo mínimo no bearer, fornecida por variável de ambiente do host. Nunca gravar a chave em TOML versionado, argumento de processo, prompt ou chat. Documentação avisa da mudança de aceitação de chaves em dezembro/2026; conferir de novo antes de usar esse caminho. Preferir OAuth.

### Estado por conta
Contas autorizadas, perfis da CLI, escopos e histórico de login desta máquina: `_memoria/contas-e-codigos.md` → "Stripe — estado de MCP/CLI por conta".

## CLI oficial (alternativa operacional)

CLI instalada e validada: **v1.55.10** (10/11/2026), via pacote oficial `@stripe/cli`. Comando efetivo `~/.local/bin/stripe` aponta para `~/.npm-global/bin/stripe`; binário antigo ficou em `~/.local/bin/stripe-v1.25.0-backup`. Conferir `command -v stripe`, `stripe --version` e `stripe <recurso> --help`.

A dona pediu atualizar após o aviso de incompatibilidade do login antigo, com prazo 08/02/2027:

```bash
npm i -g @stripe/cli@latest
stripe --version
stripe login --non-interactive --project-name <perfil-da-conta> --device-name low-ticket
```

Na v1.55.10, o login não interativo imprime `browser_url`, `verification_code` e `next_step`; executar imediatamente o `next_step` com o mesmo perfil para aguardar a autorização (`stripe login --complete-device --project-name <perfil-da-conta>`). Abrir `browser_url` no perfil do navegador reservado à Stripe, confirmar o código igual ao terminal, escolher a organização → a conta da oferta → o ambiente (teste ou produção) e concluir o consentimento. `stripe login list --project-name <perfil-da-conta>` comprova conta/ambiente ativos. Não iniciar `--new-session` nem fazer logout por rotina. Se pedir 2FA, a dona responde; não inventar código.

Credenciais OAuth são administradas pelo CLI, nunca copiadas para a oferta, logs ou chat. Instalação npm nesta máquina teve postinstall bloqueado, mas o pacote opcional Linux já trouxe o binário: `stripe --version` e chamadas autenticadas funcionaram sem liberar scripts de instalação.

Todo comando leva `--project-name <perfil-da-conta>`. Não presumir o ambiente pelo padrão da CLI: conferir `stripe login list` e conta/ambiente efetivos; esta sessão OAuth autorizou produção. `--live` só quando a tarefa já autoriza a operação real. Testes de pagamento exigem autenticar sandbox/teste separado, não usar a conta live. Criar catálogo de uma oferta real conforme pedido direto não autoriza criar cobranças de teste em clientes reais, mudar preços existentes ou publicar checkout sem validação.

```bash
stripe get /v1/account --project-name <perfil-da-conta>
stripe products list --limit 100 --project-name <perfil-da-conta>
# Somente após confirmar a conta e o ambiente:
stripe products create --name 'Les 78 Cartes Mentales du Tarot' \
  --project-name <perfil-da-conta>
```

Antes de criar, procurar o produto existente por nome/metadata e consultar todas as páginas quando necessário. Para código, usar metadata `offer_slug`, `role`, `locale`, `currency` e idempotência estável. Prices são identificados por `lookup_key`, moeda, valor e recorrência. Nunca reutilizar `prod_`/`price_` de outra conta ou ambiente.

## Evidência de conclusão

Salvar IDs não secretos, conta, ambiente, moeda e operação realizada na oferta. Depois da escrita, ler o recurso e conferir valores. Criar catálogo não ativa pagamentos nem conecta o site. Se o acesso bloquear, registrar a etapa exata (2FA/OAuth/conta), sem inventar que o cadastro terminou.

## Fontes oficiais

- [Stripe MCP](https://docs.stripe.com/mcp)
- [Stripe CLI e login](https://docs.stripe.com/stripe-cli)
- [Checkout Sessions e componentes](https://docs.stripe.com/payments/quickstart)
- [PayPal e países de empresa elegíveis](https://docs.stripe.com/payments/paypal)
- [Métodos aceitos no Brasil](https://support.stripe.com/questions/accepted-payment-methods-in-brazil)
