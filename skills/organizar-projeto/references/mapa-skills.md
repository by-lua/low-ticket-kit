# Tabela "tarefa → skill obrigatória"

Vai no `CLAUDE.md` da raiz (vale pra todos os projetos). O CLAUDE.md do projeto só acrescenta
o que é específico dele (ex. gateway próprio, skill de nicho).

## Como montar
1. Liste as skills instaladas: `ls ~/.claude/skills` + as do projeto (`.claude/skills/`) + plugins.
2. Leia a `description` das que tocam o tipo de trabalho da pasta.
3. Pra cada tipo de tarefa recorrente do negócio, escolha **a porta de entrada** (a skill que
   orquestra) e liste as mecânicas que ela puxa. Porta única quando existir — o agente chama a
   porta, a porta chama o resto.
4. Escreva como regra: "Vai fazer X → carregue `skill-y` ANTES de começar. Sem exceção."
5. Inclua as memórias-regra que mudam a escolha (ex. "imagem = GPT pelo browser, nunca Hub").

## Formato

```markdown
## Skills obrigatórias por tarefa

Antes de começar a tarefa, carregue a skill da linha (Skill tool). Sem ela, não comece.

| Vai fazer… | Skill obrigatória (porta) | Ela puxa / usar junto |
|---|---|---|
| criativo de anúncio (vídeo, estático, carrossel) | `criativo-ads` | `criativo-ads-video-orq`, `modelagem-escalados`, `gpt-imagem-playwright`, `narracao-hub-tts`, `get-brolls` |
| … | … | … |
```

## Catálogo base (low ticket / infoproduto / tráfego) — ajuste pro negócio

| Tarefa | Porta | Junto |
|---|---|---|
| oferta nova, minerar, retomar "onde paramos" | `criacao-low-ticket-mvt` | `mvt-minerar`, `mvt-modelar`, `mvt-validar`, `mvt-obra-100k`, `mvt-cross-market`, `mvt-auditar` |
| dúvida de método (MVT, obra 100K, semáforo) | `low-ticket-metodo-mvt` | — |
| página de vendas | `criacao-low-ticket-mvt` (construção) | `imagens-pagina-low`, `depoimentos-pagina-de-vendas`, `popup-saida-low-ticket`, `otimizacao-pagina-vendas`, `frontend-design` |
| produto / entregável / área de membros | `criacao-low-ticket-mvt` (construção) | `gpt-imagem-playwright`, `area-membros-netflix` |
| checkout e gateway | gateway: `wiven-checkout` · `mundpay` · `ggcheckout-produto` · `hotmart-produto-playwright` · `zenith-gateway` | `banner-checkout-gpt`, `checkout-premium` |
| criativo de anúncio | `criativo-ads` | `criativo-ads-video-orq`, `modelagem-escalados`, `gpt-imagem-playwright`, `narracao-hub-tts`, `get-brolls`, `depoimentos-video` |
| imagem avulsa | `gpt-imagem-playwright` | — |
| vídeo por IA | `flow-video-playwright` | — |
| pixel, eventos, venda × campanha | `trackeador` | — |
| tráfego (estrutura, teste, escala) | `metaads-kevones` | `paid-ads` |
| transcrever vídeo/aula | `yt-transcricao` | — |
| organizar pasta / projeto novo | `organizar-projeto` | — |
