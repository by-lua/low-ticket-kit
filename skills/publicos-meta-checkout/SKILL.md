---
name: publicos-meta-checkout
description: Gera os 2 CSV de públicos do Meta de uma oferta (Engajados = abandono de carrinho, Compradores = vendas pagas) a partir dos exports do checkout. Use quando pedirem "atualizar engajados e compradores da oferta X", "gerar público de compradores/abandono", "lista de clientes pro Meta", ou "subir público de compradores/abandono no Meta" (subir só se pedirem explicitamente).
---

# Públicos Meta a partir do checkout

## Padrão (decisão da dona, 06/10/2026)
- **Entrega = só os 2 CSV prontos** no formato Meta: `engajados-abandono.csv` e `compradores.csv`. Caminho na resposta.
- **Não subir no Meta** por padrão. Só subir se a dona pedir explicitamente, e aí seguir a seção Meta.
- **Não tocar na Wiven pelo agente** nesse fluxo (ver bloqueio abaixo). Quem exporta é a dona, na mão.

## Definição
- **Engajados** = abandono de carrinho: iniciou o checkout e não pagou.
- **Compradores** = vendas pagas/aprovadas.

## Mapeamento oferta → checkout
Ler `OFERTAS/<slug>/STATUS.md` (tabela "Ofertas e checkouts") e o `CLAUDE.md` da oferta.
- BR, R$ → **Wiven** (`wiven-checkout`).
- PT/ES, EUR/USD → **Mundpay** (`mundpay`).
- Outros → ver STATUS da oferta.
- Só produtos da oferta no mercado pedido (principal + bumps/upsell daquele mercado). Nunca misturar PT/ES com BR.

## Bloqueio atual da Wiven (documentado 06/10/2026)
`app.wiven.com.br/panel/dashboard` devolve **403 Forbidden** nos perfis `wiven` (9254) e `wiven2` (9273).
Causa: bloqueio por IP do nosso ambiente (Cloudflare), não é a conta, e é temporário (no mesmo dia, à noite, o 9254 voltou). Não tentar contornar com outro perfil
ou relogin. Saída combinada com a dona: **a dona exporta na mão da Wiven e solta os arquivos brutos na pasta**.

## Pasta de trabalho
`OFERTAS/<slug>/trafego/publicos/<AAAA-MM-DD>/`
- Brutos (como a Wiven exportou; CSV ou XLSX): nome com `bruto` no nome, ex. `compradores-bruto.xlsx`, `engajados-abandono-bruto.csv`.
- Saída: `engajados-abandono.csv`, `compradores.csv`.
- `LOG.md` com contagens, data e o que foi feito.

## Gerar os 2 CSV (comando)
```bash
S=~/.claude/skills/publicos-meta-checkout/scripts/normaliza_meta.py
P="OFERTAS/<slug>/trafego/publicos/<AAAA-MM-DD>"
# 1) compradores primeiro (para excluir do abandono)
python3 $S "$P/compradores-bruto.xlsx" "$P/compradores.csv"
# 2) abandono, tirando quem também comprou
python3 $S "$P/engajados-abandono-bruto.csv" "$P/engajados-abandono.csv" --excluir "$P/compradores.csv"
```
Trocar os nomes pelos arquivos reais da pasta (CSV ou XLSX, qualquer um dos dois serve).
O script imprime as colunas detectadas e a contagem. Se a coluna de e-mail não for encontrada,
ele para e mostra o cabeçalho lido: ajustar o export ou renomear a coluna.

O script (`scripts/normaliza_meta.py`):
- lê CSV (detecta `,` `;` ou tab) e XLSX (primeira aba, só biblioteca padrão, sem openpyxl);
- detecta colunas por nome, sem diferenciar caixa/acento: e-mail, telefone, nome;
- telefone → DDI 55, só dígitos; nome → `fn` (primeiro nome) e `ln` (último sobrenome);
- saída: `email, phone, fn, ln, ct, st, country=br`, deduplicado por e-mail;
- `--excluir <lista>`: aceita CSV/XLSX com cabeçalho de e-mail, ou lista solta de e-mails (um por linha).

## Receita Wiven (BR) — VALIDADA 06/10/2026 (Mapa do Tarot BR)
Telas: Vendas → `/panel/orders` (Histórico de transações, botão Exportar) e Clientes → `/panel/clients/abandoned-carts`
(botão "Exportar carrinhos"). Na prática o clique de exportar pela automação falhou (a aba pulava para `/panel/sales`),
então o caminho confiável é a **API interna do painel**, chamada de dentro da aba logada (`--session wiven`, 9254),
sem relogar:

```js
// agent-browser --session wiven eval "<isto>" > raw.json   (saída tem dado pessoal: salvar em arquivo, nunca imprimir)
(async()=>{async function all(u){let out=[],p=1;for(;;){const j=await (await fetch(u+'&page='+p+'&pageSize=100')).json();
const d=j.data||{};out=out.concat(d.items||[]);if(p>=(d.pagination?.totalPages||1))break;p++}return out}
return JSON.stringify({tx:await all('/api/internal/panel/transactions?period=total'),
                       ab:await all('/api/internal/panel/reports/abandoned-cart?period=total')})})()
```
- `period=total` = todo o histórico (`all` NÃO é tudo; traz só a semana).
- Transação: `status` (`COMPLETED` = pago; ignorar `PENDING`, `REFUNDED`, `FAILED`), `payerEmail`, `payerName`, `payerPhone`,
  produtos em `items[].product.name` (inclui bumps, `isBump`).
- Abandono: `client.{email,name,phone}`, produto em `checkout.product.name`, `isRecovered`.
- A conta Wiven é compartilhada entre ofertas: **filtrar pelos nomes de produto da oferta** (principal + bumps + combo).
  Tarot BR: `Mapa do Tarot`, `Leve os 3 com desconto`, `A Folha de Consulta do Tarot`,
  `80 Perguntas Poderosas para suas Tiragens de Tarot`, `Guia Flash: Arcanos Maiores`.
- Tirar e-mail de teste (`@leadgo.dev`, contendo `teste`).
- Gravar `compradores-bruto.csv` e `engajados-abandono-bruto.csv` (colunas email,nome,telefone) e rodar o normalizador acima.
- Compradores leva coluna **`value`** (pedido da dona, pro público por valor do Meta): soma de `amount` das transações
  COMPLETED da oferta por e-mail, em R$, 2 casas. O normalizador não gera essa coluna: acrescentar depois de rodar.

Se a Wiven der 403 (bloqueio por IP, ver acima): `browsers.sh wiven` de novo mais tarde; se continuar, a dona exporta na mão
pelas mesmas duas telas e solta os brutos na pasta.

## Receitas Mundpay, GGCheckout, Hotmart e Zenith
**NÃO TESTADO.** Não inventar caminho. Abrir o painel do gateway, procurar "vendas", "transações",
"abandonos"/"checkouts não finalizados" e "exportar"; registrar aqui o que for visto.

## Meta (só se pedirem para subir)
- Perfil: `meta` (porta 9225, developers.facebook.com/apps) ou o Gerenciador logado. Conferir que a conta é a da oferta.
- Conta de anúncios: sair do STATUS/trafego da oferta. Se houver dúvida, perguntar à dona antes.
- Públicos → Criar público → Público personalizado → Lista de clientes.
- Nomes: `<Oferta> <MERCADO> - Compradores` e `<Oferta> <MERCADO> - Engajados (abandono)` (ex.: `Mapa do Tarot BR - Compradores`).
- Se já existir: atualizar (adicionar/substituir clientes), não duplicar.
- Subir o CSV, mapear colunas (email, telefone, nome, cidade, estado, país), aguardar processamento e anotar as correspondências.

## Gates
- Sem export bruto = sem CSV. Não gerar lista inventada.
- Engajados nunca contém quem comprou (`--excluir`).
- Nome do público sempre com o mercado (` BR`, ` PT`, ` ES`).
- Não subir no Meta sem pedido explícito.
