# HANDOFF — como outra pessoa monta, testa e publica um checkout a partir deste modelo

## Quem faz o quê
| Quem | Faz |
|---|---|
| **Dono da oferta** | decide preços, moedas, mercados, textos e imagens; cria a conta Stripe da oferta; confirma a conta PayPal que recebe; verifica a empresa na Stripe; autoriza o live; fornece depoimentos reais e páginas legais |
| **Quem monta (pessoa + agente: Codex, Claude Code...)** | copia o modelo, adapta catálogo/traduções/imagens, roda os testes, sobe em teste, prova os fluxos, prepara o go-live |
| **Agente** | segue `AGENTS.md`: pergunta onde hospedar, nunca usa chave live sem ordem, nunca inventa prova social |

## Antes de começar (o dono entrega)
1. Conta **Stripe** da oferta criada (organização/empresa certa) e acesso de teste (chaves `pk_test` e `sk_test`). Conta verificada só é necessária para o live.
2. Conta **PayPal Business** que vai receber + um app de desenvolvedor (client id e secret **sandbox**).
3. Hospedagem escolhida: **Cloudflare** (conta do cliente) ou **Coolify/Node**.
4. Tabela de SKUs com preço por moeda aprovado (plano básico, completo, upgrade aditivo, bumps), garantia (dias) e mercados.
5. Banner, capa, miniaturas dos bumps e favicon da oferta; textos do produto e dos bumps.

## Passo a passo
1. **Copiar** o modelo para o projeto da oferta (sem `node_modules`, `data/`, `.dev.vars`) e `npm install`.
2. **Adaptar:** `catalog.mjs`, `public/i18n.js`, `public/assets/img/` e favicon, `OFFER_SLUG`/`OFFER_DESCRIPTION`/`BRAND` (veja `AGENTS.md` §4).
3. **Testar local:** `npm test` e depois o checkout de ponta a ponta com chaves de teste (veja `AGENTS.md` §5).
4. **Provar** e anotar (arquivo de status da oferta): cartão aprovado e recusado, 3D Secure, reembolso, webhook duplicado, valor adulterado, PayPal sandbox com captura, troca de país/idioma/moeda, celular e Safari.
5. **Hospedar em teste** (Cloudflare ou Coolify) com HTTPS e domínio; registrar o domínio na Stripe (Apple/Google Pay); cadastrar o webhook de teste.
6. **Go-live** (só com ordem do dono): conta live verificada; chaves live nos segredos; `ALLOW_LIVE=1`; criar Product/Prices live; webhook de produção; app live do PayPal e seu webhook; entrega real; rastreamento/pixel; IVA tratado; páginas legais e cookies; depoimentos reais; teste real com valor baixo e reembolso.
7. **Só então** trocar os links públicos da página de vendas para o novo checkout.

## Definição de pronto (checklist)
- [ ] `npm test` passa; testes de ponta a ponta da seção 4 anotados
- [ ] Preço sempre calculado no servidor; adulterar valor retorna 400
- [ ] Entrega só por webhook/captura; reembolso revoga
- [ ] Idioma e moeda mudam pelo país; telas conferidas em fr/en/es/pt (ou nos idiomas da oferta)
- [ ] Sem notificação de compra falsa e sem depoimento/contador inventado em produção
- [ ] Favicon, banner e imagens da oferta; sem placeholders
- [ ] Segredos fora do repositório; chaves live só nos segredos do ambiente
- [ ] Teste real em produção com reembolso

## Como integrar com Codex / outros agentes
O arquivo `AGENTS.md` na raiz é lido automaticamente pelo Codex (e por outros agentes que seguem esse padrão); o `CLAUDE.md` aponta para ele no Claude Code. Peça ao agente: "monte o checkout internacional deste modelo para a oferta X" e ele deve **perguntar onde hospedar** antes de qualquer coisa. Se o agente tiver skills próprias (ex.: Stripe, PayPal, Cloudflare), elas complementam; as regras do `AGENTS.md` prevalecem.
