---
name: low-ticket
description: Porta de entrada e orquestradora do sistema LOW-TICKET (ofertas low ticket da LeadGo). Abre a sessão (índice, métodos ativos, oferta) e diz qual etapa e qual filha usar, da escolha da oferta até a entrega pronta. Use SEMPRE no começo de qualquer trabalho low ticket — "abrir", "retomar", "onde paramos", "vou mexer na oferta X", "achei uma oferta na Biblioteca", "modelar essa oferta", página, entregável, área de membros, funil, checkout. Criativo de anúncio vai pra skill `criativo`.
---

# low-ticket — orquestradora (índice)

Esta skill só diz **a ordem e quem chamar**. Regra de execução mora na filha/skill da etapa.
Raiz: `~/Documentos/TRAMPO/PROJETOS/WORKING/PROJETOS - INTERNOS/LOW-TICKET` (fonte desta skill: `_skills/low-ticket/`).

## 1. Abrir — sempre primeiro
```
python3 "<RAIZ>/_skills/low-ticket/scripts/abrir.py" "<oferta>" "<etapa ou tarefa>"
```
Imprime o `INDICE.md`, a chave `_memoria/METODOS-ATIVOS.md` e os arquivos da oferta. Devolva o **RECIBO** à dona antes
de agir. **Método com Ativo = não não se usa**, mesmo que a skill exista.

## 2. Etapas (uma por vez; cada uma só começa com a saída da anterior)
**Nenhuma etapa se pula.** Antes de começar uma, conferir que o arquivo da anterior existe; faltou → fazer a anterior
primeiro e avisar a dona. Pontos em que a dona aprova: E2a, E2b, E2c, **E2d (visual)**, primeiras páginas e MVP (E4), ficha da leva.

| # | Etapa | Saída que prova | Filha |
|---|---|---|---|
| E1 | **Escolher a oferta** — (a) a dona manda link da Biblioteca + explica · (b) Modelador do MineraAds, **padrão Raio-X+SpyX** (5 modos disponíveis, ver `low-modelador`) · (c) mineração MVT (**desligada**) | `OFERTAS/<slug>/pesquisa/REFERENCIA.md` + material cru em `pesquisa/da-dona/` + imagens da página original em `pesquisa/referencia/imagens-origem/` | (a) `low-referencia` · (b) `low-modelador` · Biblioteca: `agent-browser` + perfis do sistema |
| E2a | **Direção** — Raio-X traz 10 propostas ranqueadas, **a dona escolhe uma** → SpyX/Combinado aprofunda nessa proposta | `pesquisa/modelador-<data>-etapa2.md` + `.json` | `low-modelador` (etapa 2) |
| E2b | **Validar o caminho** — termos PT/ES/EN → concorrentes parecidos na Biblioteca (validados por dias no ar) → demanda orgânica → funil dos concorrentes → veredito 🟢🟡🔴 → **dona decide** | `pesquisa/VALIDACAO-<data>.md` com a decisão | `low-validar` |
| E2c | **Ficha + funil** — o que vendemos, pra quem, dor, preço **e o funil inteiro** (bônus, bump, upsell, downsell, upgrade, combo) **antes da página** | **`OFERTA.md`** + **`FUNIL.md`** aprovados · pasta no padrão | `low-ficha-oferta` (regras de funil: `low-funil`) · `organizar-projeto` |
| E2d | **Visual** — **perguntar à dona**: manter o visual do original ou mudar (cores, fundo, elementos, capa)? Mudar → gerar 1 **imagem-guia = mockup do plano COMPLETO** (capa + páginas + capas dos bônus, paleta nova; refs: kit completo dele + páginas reais) → dona aprova → travar tokens + imagem-guia. Manter → tokens do original | `DESIGN-SYSTEM.md` (tokens + caminho da imagem-guia) **aprovado** | `low-pagina` § Visual · `gpt-imagem-playwright` |
| E3 | **Página** — página do original modelada **com o visual da E2d**, troca oferta e idioma; desktop e mobile bem resolvidos | `site/` | `low-pagina` |
| E4 | **Entregável** — texto inteiro → primeiras páginas das imagens de dentro da original → **dona aprova** → MVP | `produto/` texto + imagens A4 | `low-entregavel` |
| E5 | **Imagens da página** (mockups refeitos das dele, prints de dentro do nosso MVP) — lote anexa a **imagem-guia da E2d** | imagens plugadas na página | `imagens-pagina-low` · `depoimentos-pagina-de-vendas` |
| E6 | **Área de membros** | `/painel` com módulos + PDF baixando | `area-membros-netflix` · `auditar-entregaveis-oferta` |
| E7 | **Peças do funil** — produzir o entregável de cada peça do `FUNIL.md` (desenhado na E2c) | peças no `/painel` | `low-funil` · `low-entregavel` |
| E8 | **Checkout** — gateway, banner, capa, PDF de entrega, 2 webhooks, registro do código | produto/oferta no gateway | `low-checkout` |
| E9 | **Gates no ar** — eventos, página leve (imagens, vídeos em player, Lighthouse), download do PDF + botão no leitor, checkout (preço, banner leve, webhooks) | prova colada no `STATUS.md` | `low-gates-no-ar` |

Depois da E9: criativo → skill **`criativo`**. Tráfego → `metaads-kevones`.

## 3. Regras que valem em toda etapa (só estas; o resto mora na filha)
- **Fatos antes de cadastrar:** gateway, conta, código, webhook, domínio — conferir no índice (seção Fatos). Nunca de cabeça.
- **Entregável nunca é HTML/código:** sempre imagem A4 do GPT com a referência visual. Item de fazer/imprimir
  (exercício, pôster, folha, checklist) = **página própria** depois da explicação.
- **Ofertas já ativas:** não migrar pro fluxo novo sem a dona mandar.
- **Fecho de toda sessão:** `low-ticket-salvar` — `STATUS.md` da oferta, ficha e índice atualizados. Regra nova
  da dona → arquivo certo + linha no `INDICE.md`. Esta skill não cresce.

Plano completo e mapa do que vem de onde: `CONHECIMENTO/PLANO-SKILLS-LOW-TICKET-V2.md`.
