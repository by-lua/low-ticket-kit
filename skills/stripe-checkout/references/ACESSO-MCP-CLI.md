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

Abrir o consentimento no perfil persistente `stripe`, porta 9299. Selecionar **Winx → Calendrier Magique**, conferir `acct_1UaIGiABfkUzod1X`; não AdsTrackeador nem LeadGo. Conceder somente o acesso necessário à tarefa. Separar teste/live. Não concluir consentimento de conta errada. O pedido de usar o acesso não autoriza reembolsar, cobrar clientes reais ou alterar dados bancários.

Registrar MCP não injeta ferramentas em uma conversa já iniciada: pode ser necessário iniciar nova sessão. Quando presentes, usar `get_stripe_account_info` antes das operações, `stripe_api_search`/`stripe_api_details` para consultar o contrato, e `stripe_api_read`/`stripe_api_write` para a operação. Conferir a resposta efetiva. Não executar um agente novo apenas para contornar ferramentas ausentes.

Se OAuth não estiver disponível, a documentação atual prevê **agent API key** com escopo mínimo no bearer, fornecida por variável de ambiente do host. Nunca gravar a chave em TOML versionado, argumento de processo, prompt ou chat. Documentação avisa da mudança de aceitação de chaves em dezembro/2026; conferir de novo antes de usar esse caminho. Preferir OAuth.

## CLI oficial (alternativa operacional)

CLI já instalada: `stripe`. Conferir `stripe --version` e `stripe <recurso> --help`; o ambiente tinha v1.25.0 em 10/11/2026 e comandos de documentos novos podem não existir nessa versão. Não atualizar nem substituir silenciosamente uma instalação compartilhada.

```bash
stripe login --project-name winx-calendrier --device-name low-ticket
```

Abrir a URL de pareamento no mesmo perfil `stripe`, conferir o código exibido e selecionar a conta. O CLI salva credenciais em `~/.config/stripe/config.toml`; arquivo privado, nunca imprimir `stripe config --list` nem colocar no Git. 2FA do autenticador é da dona; se aparecer, pedir a ela. Nunca usar chaves de AdsTrackeador para tentar operar Winx.

Todo comando leva `--project-name winx-calendrier`. O ambiente padrão é teste; `--live` só quando a tarefa já autoriza a operação real. Criar catálogo de uma oferta real conforme pedido direto não autoriza criar cobranças de teste em clientes reais, mudar preços existentes ou publicar checkout sem validação.

```bash
stripe get /v1/account --project-name winx-calendrier
stripe products list --limit 100 --project-name winx-calendrier
# Somente após confirmar a conta e o ambiente:
stripe products create --name 'Les 78 Cartes Mentales du Tarot' \
  --project-name winx-calendrier
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
