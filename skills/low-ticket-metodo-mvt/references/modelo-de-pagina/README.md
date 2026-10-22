# Modelos de página de vendas — Low Ticket

> **Atenção:** estes HTML são adaptações locais de uma página Flowise. O template do
> método é o JSON de Elementor entregue no bônus do workshop (não está nesta pasta).
> A ordem de blocos do método é a de `../pagina-produto-criativo.md` §1 — este modelo
> cobre só parte dela e traz peças que não são do método (countdown, notificação,
> autoridade fixa, upsells).

| Arquivo | O que é | Quando usar |
|---|---|---|
| `MODELO-PAGINA-LOW-MVT.html` | **Modelo de trabalho.** É o Flowise adaptado: mesmo visual e mesmos componentes, com **50 `{{PLACEHOLDERS}}`**, tudo em pt-BR (varrido em 02/09/2026 — não sobrou espanhol) e barra de urgência com countdown de 15 min. | Base HTML disponível localmente quando não se usa WordPress/Elementor. |
| `MODELO-PAGINA-LOW-FLOWISE-ES.html` | Página real do Flowise em **espanhol** (nicho de prevenção de quedas em idosos), exportada de page builder. Referência visual e de copy. | Consultar exemplo pronto: carrossel, depoimentos WhatsApp, countdown, VSL. |
| `MODELO-PAGINA-LOW-FLOWISE-PT.html` | Mesma página **traduzida para pt-BR** (copy, depoimentos, bônus, upsells e preços em R$). | Referência de copy quando a oferta for em português. |
| `MODELO-PAGINA-LOW-FLOWISE.original.html` | Cópia intocada do Flowise, antes de qualquer edição. | Restaurar se o outro for alterado por engano. |

## O que o modelo já tem

barra de urgência (countdown 15 min) · hero com VSL ou mockup · carrossel
demonstrativo · depoimentos WhatsApp · bônus · **dupla oferta com "o que você
perde"** · autoridade · FAQ · rodapé.

## Placeholders (50)

```
NOME_DA_MARCA NOME_DO_PRODUTO HEADLINE_PARTE_1 HEADLINE_PARTE_2 SUBHEADLINE
CTA_PRINCIPAL TITULO_DEMONSTRATIVO TITULO_DEPOIMENTOS
OLHO_BONUS TITULO_BONUS SUB_BONUS NOME_BONUS_1..3 DESC_BONUS_1..3
TITULO_PLANOS AVISO_DESCONTO ENTREGAVEL_BASICO ENTREGAVEL_COMPLETO
PRECO_DE_BASICO PRECO_BASICO PRECO_DE_COMPLETO PRECO_COMPLETO
CTA_PLANO_BASICO CTA_PLANO_COMPLETO
NOME_AUTORIDADE BIO_AUTORIDADE_1 BIO_AUTORIDADE_2 CREDENCIAL_1 CREDENCIAL_2
PERGUNTA_1..5 RESPOSTA_1..5
UPSELL_1_HEADLINE UPSELL_1_DESC UPSELL_1_PRECO
UPSELL_2_HEADLINE UPSELL_2_DESC UPSELL_2_PRECO UPSELL_PRECO_DE
ANO
```

**Nunca troque preço por replace de texto plano** (`$27` aparecia nos dois planos —
era o bug do `montar.py` da oferta ferreiro-rural). Use os 4 placeholders de preço.

## O que o modelo NÃO tem placeholder (edição manual)

- **Depoimentos de WhatsApp** (12 conversas, nomes e falas) — texto pt-BR de exemplo,
  reescreva na voz do comprador e troque os nomes.
- **Notificação de venda** no canto — troque nomes e cidades pro público da oferta.
- **Cards de bônus: só 3.** O método pede 4 a 6 — duplique o card do bônus 3 quando
  precisar de mais, copiando o bloco inteiro.

## O que criar quando a oferta pedir

O modelo cobre 6 dos 10 blocos obrigatórios do MVT. Estes 4 não existem nele e
devem ser montados copiando o estilo dos blocos vizinhos:

| Bloco | O que é | Onde entra |
|---|---|---|
| Benefícios | resultados, não características | depois do demonstrativo |
| Headline de urgência + botão | CTA no meio da página | antes dos planos |
| Ideal para você que… | segmenta, gera identificação | antes do produto principal |
| Tudo o que você vai receber | mockup + tópicos do principal | antes dos bônus |

## Barra de urgência

Countdown regressivo de **15 minutos por visitante**, guardado em `sessionStorage`:
recarregar a página não reinicia o relógio; nova sessão começa do zero. Ao zerar,
o texto vira "Últimas unidades disponíveis" em vez de ficar negativo.
Para mudar a janela, edite `MINUTOS` no script da barra.

## Regras que não mudam

- Copy sem persuasão, sem gatilho, sem história. Clareza e especificidade.
- Headline sobre o produto, com uma única interpretação possível.
- Botão do bloco 1 vai para os planos, nunca direto ao checkout.
- Plano básico é âncora de preço. Nunca R$10.
- Order bump é no checkout, montado no 2º dia da oferta no ar.
