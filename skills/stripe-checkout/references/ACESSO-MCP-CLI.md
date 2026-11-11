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

### Estado confirmado nesta máquina (10/11/2026)
- Codex `codex-acc-2`: MCP `stripe` registrado e **OAuth concluído**, confirmação `Successfully logged in to MCP server stripe`.
- Conta: produção **Calendrier Magique / Winx**, `acct_1UaIGiABfkUzod1X`. Escrita somente Products/Prices. Leitura Account Features/Accounts/Events/Payment Method Configurations/Payment Method Domains; demais permissões nenhum. Credenciais OAuth administradas pelo Codex, sem copiar tokens ou secret keys para a oferta.
- Esse escopo serve ao cadastro de catálogo desta etapa. Checkout/cobrança/webhook exigirão ampliar apenas os escopos necessários em etapa posterior autorizada, sem trocar de conta. As ferramentas não apareceram nesta conversa que já estava aberta; iniciar nova sessão para carregá-las.
- CLI **atualizada de 1.25.0 para 1.55.10 e autenticada via OAuth** na mesma conta de produção. `stripe login list --project-name winx-calendrier` confirma uma única conta ativa; `GET /v1/account --live` confirma ID/BR e charges_enabled/payouts_enabled/details_submitted=true. O fluxo antigo exigiu 2FA e expirou; o novo login foi concluído sem código adicional da dona. CLI usa o papel da dona nesta conta (tela: Super Administrator); o escopo restrito de catálogo descrito acima é do MCP, não da CLI.

### Retomada posterior em 10/11/2026
- MCP **apareceu nesta sessão e funciona**: `list_available_accounts_or_orgs` retornou somente `Calendrier Magique`, contexto `acct_1UaIGiABfkUzod1X`, `livemode=true`. `GetProductsId` e `GetPricesPrice` confirmaram o produto Guide Tarot ativo e o preço avulso EUR 790. Não inferir disso autorização para cobrar, publicar ou mudar outro recurso.
- CLI continua na versão **1.55.10**, porém `stripe login list --project-name winx-calendrier` retornou **401, OAuth token expired**. O login concluído anteriormente é fato histórico; o estado atual requer novo login antes de qualquer leitura/escrita autenticada pela CLI. MCP segue utilizável. Não substituir por credencial de outra conta.

### Recuperação em 11/11/2026
- A tentativa normal `stripe login --non-interactive --project-name winx-calendrier` abriu **reauthorization**, mas o botão `Autorizar` ficou desabilitado porque não havia mudança de contas/permissões. O token da CLI seguia expirado. `stripe login --non-interactive --new-session --project-name winx-calendrier --device-name low-ticket` criou um fluxo de **device login** novo sem sair do perfil persistente do navegador.
- No perfil `stripe`, foi selecionado **Winx → Calendrier Magique → Conta de produção** (a tela também oferecia Modo de teste e outras organizações, que não foram selecionados). `stripe login --complete-device --project-name winx-calendrier` concluiu: `Done! ... Calendrier Magique · live (acct_1UaIGiABfkUzod1X)`.
- Prova posterior: `stripe login list --project-name winx-calendrier` = **uma conta**, `Calendrier Magique acct_1UaIGiABfkUzod1X live active`. Perfil do navegador fechado normalmente; nenhuma chave impressa ou copiada. Usar `--new-session` **só para recuperar token expirado** quando a tela de reautorização não permitir autorizar, nunca como rotina.
- **Perfil separado para testes, criado em 11/11:** `stripe login --non-interactive --project-name winx-calendrier-test --device-name low-ticket-test` → no mesmo perfil persistente do navegador, escolher **Winx → Calendrier Magique → Modo de teste** (a tela também mostra produção e área restrita) → `stripe login --complete-device --project-name winx-calendrier-test`. Prova: `stripe login list --project-name winx-calendrier-test` = **uma conta**, `acct_1UaIGiABfkUzod1X sandbox active`; o perfil `winx-calendrier` permanece **live active**. Todo comando de teste leva `--project-name winx-calendrier-test`; todo comando live leva `--project-name winx-calendrier`. Confirmar o modo mostrado pela CLI antes de escrita. Nenhuma cobrança de teste foi criada nesta configuração.

## CLI oficial (alternativa operacional)

CLI instalada e validada: **v1.55.10** (10/11/2026), via pacote oficial `@stripe/cli`. Comando efetivo `~/.local/bin/stripe` aponta para `~/.npm-global/bin/stripe`; binário antigo ficou em `~/.local/bin/stripe-v1.25.0-backup`. Conferir `command -v stripe`, `stripe --version` e `stripe <recurso> --help`.

A dona pediu atualizar após o aviso de incompatibilidade do login antigo, com prazo 08/02/2027:

```bash
npm i -g @stripe/cli@latest
stripe --version
stripe login --non-interactive --project-name winx-calendrier --device-name low-ticket
```

Na v1.55.10, o login não interativo imprime `browser_url`, `verification_code` e `next_step`; executar imediatamente o `next_step` com o mesmo perfil para aguardar a autorização (nesta máquina: `stripe login --complete-device --project-name winx-calendrier`). Abrir `browser_url` no perfil `stripe`, confirmar o código igual ao terminal, escolher Winx → Calendrier Magique → Produção e concluir o consentimento. `stripe login list --project-name winx-calendrier` comprova conta/ambiente ativos. Não iniciar `--new-session` nem fazer logout por rotina. Se pedir 2FA, a dona responde; não inventar código.

Credenciais OAuth são administradas pelo CLI, nunca copiadas para a oferta, logs ou chat. Instalação npm nesta máquina teve postinstall bloqueado, mas o pacote opcional Linux já trouxe o binário: `stripe --version` e chamadas autenticadas funcionaram sem liberar scripts de instalação.

Todo comando leva `--project-name winx-calendrier`. Não presumir o ambiente pelo padrão da CLI: conferir `stripe login list` e conta/ambiente efetivos; esta sessão OAuth autorizou produção. `--live` só quando a tarefa já autoriza a operação real. Testes de pagamento exigem autenticar sandbox/teste separado, não usar a conta live. Criar catálogo de uma oferta real conforme pedido direto não autoriza criar cobranças de teste em clientes reais, mudar preços existentes ou publicar checkout sem validação.

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
