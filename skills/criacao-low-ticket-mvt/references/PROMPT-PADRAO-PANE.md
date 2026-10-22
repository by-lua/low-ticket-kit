# PROMPT-PADRÃO DE PANE — blocos obrigatórios (browser / mineração / medição)

Referência ÚNICA, citada por `criacao-low-ticket-mvt`, `mvt-minerar`, `mvt-cross-market` e `mvt-validar`. Conteúdo original, intacto (era a seção `## PROMPT-PADRÃO DE PANE` da skill antes da divisão de 24/09/2026).

Todo `pane_spawn` de pane que toca browser, minera ou mede **carrega TODOS os blocos abaixo, copiados
no prompt** (não "veja a skill"). Prompt sem um bloco = não despacho. Antes de despachar, releio o
prompt contra a lista.

> **Pane que GASTA (imagem/vídeo/app/página/checkout/tráfego) [decisão do dono 25/09/2026]:** o prompt carrega `[GATE DE GASTO] Só execute se o ESTADO tiver a saída colada de gate.py --ate T12 --oferta <slug> = OK e a linha "Parada 3 LIBERADA <slug>" + T13.19 ≤48h. Senão PARE e reporte. Regra: CONSTRUCAO-GATES.md §0b.`

```text
[PERFIL] Use SOMENTE o perfil <perfil>. Nenhum outro. Tabela pane→perfil vigente: <colar do ESTADO>.
  Antes de abrir: `pane_list` — se há pane órfão/duplicado nesse perfil, NÃO abra; reporte.
  Sintoma de perfil disputado ("a URL da aba mudou sozinha entre duas leituras", resultado que não
  é da sua query): PARE, não navegue mais, reporte. Não use pkill em perfil alheio.
[CONCORRÊNCIA] Máx. 1-2 panes simultâneos na Biblioteca por IP; ~30 queries por perfil e depois
  INTERVALO. O throttle é por volume acumulado no IP. Bloqueou → pare e reporte quantas fez.
[NAVEGADOR] Visível, nunca headless. Proibido script, nohup, lote paralelo, qualquer coisa que
  meça sozinha. Se o ritmo virar problema, REPORTE queries/hora; não mude de método.
[COTA = PARADA] Bateu ~6 concepções no termo → PARA e vai pro próximo. Termo seco: ~150 cards
  sem chegar na cota → registre quantas deu e siga. 30 cards seguidos sem nova = saturado.
[SEGUIDORES NA VARREDURA] Para cada anunciante: card → clicar no NOME → aba "Sobre" → "Páginas e
  contas" → ícone INSTAGRAM (@handle + seguidores). NUNCA o número do Facebook. Sem IG: "sem IG" +
  nº do Facebook, marcar PENDENTE. Nada de passe separado depois.
[2 LINKS] Toda concepção: `facebook.com/ads/library/?id=<ID>` + página de vendas (decodificar `u=`
  do l.php do bloco do PRÓPRIO ID). Página fora do ar = "fora do ar (data)".
[LINK NÃO BLOQUEIA] Não achou o link da página (WhatsApp, sem l.php, fora do ar): grave
  `pagina_vendas: PENDENTE (motivo, data)`, mantenha o link da Biblioteca e SIGA. Nunca pule nem
  reprove concepção por falta de link, preço, seguidor ou print — anote PENDENTE e continue.
[CHECKLIST 100K] Cada concepção: CABE / CABE COM RECORTE (qual) / NAO CABE (por quê) + nível de
  consciência. Preço nunca é critério de descarte.
[FALSO-ZERO / CONTROLE] Antes de aceitar zero: confira que a busca ACONTECEU (campo q preenchido,
  regex aceita `resultados` e `results`); zero só após 4 tentativas limpas (grave `tentativas`);
  query de controle a cada ~12 buscas; controle zerou = descarte tudo desde o último controle bom.
[MODELO/REFERÊNCIA] Pane Sonnet executa (claude-sonnet-5; Haiku só verificação/edição mecânica). O
  orquestrador abre a referência real ANTES de despachar e anexa no prompt; auto-relato de pane não
  conta — o orquestrador confere o artefato. Reporte só em marcos (início → 50% → 100% com caminho).
[FALSO-POSITIVO] Número idêntico ao do controle logo antes = contaminação; remedir.
[REPORTE POR EVENTO] Avise só: (1) fim do lote com resumo (quantas mediu/zerou/número alto);
  (2) controle falhou ou q voltou vazio — diga em qual ID parou; (3) precisa de decisão; (4) perfil
  disputado / IP bloqueado. Nada de reporte por item; "mais um zero" não é evento.
[FECHAR] Terminou sua parte → feche o perfil (`pkill -f "user-data-dir=$HOME/.agent-profiles/<perfil>"`
  só do SEU perfil) e AVISE que liberou. O orquestrador fecha o PANE no handoff (`pane_close`) e
  confere o resultado antes de repassar "pronto".
[GRAVAÇÃO] Registre no Hub/arquivo da rodada durante o trabalho, não só no fim.
```

Tabela pane→perfil e nº de panes ativos na Biblioteca ficam no `ESTADO.md`; atualizar a cada
despacho e a cada handoff.

---

## PRM-CONSTRUCAO — blocos obrigatórios de todo `pane_spawn` de CONSTRUÇÃO (T13–T15) e de pane de app  [buraco 2 · 25/09/2026]

Vale para pane que gera página, entregável (imagens/app), mockup, banner, checkout, criativo ou código de app. Copiados NO prompt (nunca "veja a skill"); prompt sem bloco = não despacho; o orquestrador junta a referência ANTES de delegar (memória `orquestrador-junta-referencia-antes-de-delegar`) e delega a pane Sonnet/Haiku, não executa (memórias `delegar-sempre-sonnet-haiku`, `delegar-tudo-fechar-pane`).
```text
[OFERTA-PRIMEIRO] Antes de escrever QUALQUER briefing ou ângulo, abra nesta ordem e grave as 4 linhas no handoff:
  1) OFERTAS/<slug>/CLAUDE.md + STATUS.md   2) produto/MANIFESTO-ENTREGAVEIS.md  3) a página de vendas (h1/headline/meta)  4) criativos/ (inventário + o que já foi descartado e por quê).
  O QUE VENDEMOS: <o que o cliente recebe na mão, em uma frase>
  NÃO É: <o que esta peça NÃO pode parecer que seja>
  PERSONA: <quem é + a dor de hoje>
  DOR ATACADA: <dor + onde foi medida>
  Contraprova: "se o cliente comprar isso, o que ele recebe?" → tem que ser um item do MANIFESTO. Se não for, PARA e reporta — ângulo errado é melhor que peça pronta errada.
  Alinhamento com a landing: o que o anúncio promete é LITERALMENTE o que o <h1> promete? CTR alto + IC baixo = promessa errada (a pessoa clica, vê que não tem a ver com aquilo, sai).
  Gate do dono (10/10/2026): ângulo inventado a partir do nome da pasta já custou 2 peças prontas (Mapas Visuais Eletrotecnia, CRIATIVO-9 e CRIATIVO-10). Não repita.
[OBRA-DE-ARTE] A persona NÃO é só criativo: as dores que o produto principal NÃO endereça são a matéria-prima de bônus/order bump/upsell. Regra da dona (10/10/2026) — o filtro é SÓ "é dor da persona?" + "tem demanda?". Concorrente NÃO impede: bump/upsell vende pra quem já comprou, com confiança estabelecida, público diferente do frio do concorrente — o dado do concorrente é PREÇO/posicionamento, não bloqueio. O FORMATO é livre: visual, PDF, curso, ou a pasta ainda vazia que vira o bump depois. Simples = bump barato; complexo = upsell mais caro. ⛔ só para dor que não é da persona (ex.: faturamento/preço do serviço numa oferta de produto).
[BRIEFING] produto · persona · ângulo · preço (do ESTADO, com dono+data) · garantia (dias) · suporte · o que NÃO prometer (área sensível).
[DESIGN-SYSTEM] DESIGN-SYSTEM.md da oferta ANEXADO + tokens de cor/fonte escritos no prompt. Nada de cor/fonte própria.
[REFERÊNCIA REAL] a referência (print/arquivo do concorrente só como estudo, nunca como arte) e a identidade (IDENTIDADE-REF) ANEXADAS pelo orquestrador.
[FIM] Faça a lista toda num turno só. Handoff só no final, `done` com as provas. `blocked` só para impedimento real (login caído sem conseguir relogar, cota de todas as contas esgotada). Modal que não carregou, token "fora do ambiente", passo difícil por mouse: tente outro caminho (reload, outro perfil, CDP, env do Coolify) e siga. Esperar geração/deploy = Monitor dentro do turno, nunca encerrar o turno nem mandar handoff por página.
[ENTREGA] conteúdo = 1 IMAGEM por página (ilustrada), MVP conforme manifesto; app = trilha K-APP (SPEC→REVISÃO→TESTES→DEPLOY→ACESSO), nunca PDF/texto cru salvo pedido do dono.
[CRIATIVO] imagem = orgânica (foto "eu imprimi"/filtro iPhone/Story), mockup limpo NÃO; legenda de vídeo = Remotion/Hyperframes.
[ANTI-ARTE] nenhuma arte, texto ou depoimento do concorrente CRU (cross-market: páginas/imagens/mockups/entregável dele ADAPTADOS em idioma+cor é o método); PROVA SOCIAL só real (decisão do dono 25/09/2026) — sem depoimento/foto/contador inventado.
[PERFIL LIVRE] `S=$(~/.claude/bin/gpt-livre.sh <lane>)` / `hub-livre.sh <lane>` antes de gerar; nunca fixar perfil.
[EVIDÊNCIA] gravar o arquivo de evidência do item (nome fixo em `references/CONSTRUCAO-GATES.md`) e reportar só em marcos.
[FECHAR] terminou → handoff_submit e o orquestrador fecha o pane (`pane_close`).
```

## PRM-VERIFICADOR — blocos obrigatórios de todo pane que CONFERE trabalho de outro  [10/10/2026]

Nasceu da troca de order bumps de Elétrica + Jiu-Jitsu: um Haiku devolveu "5/5 PASSA, no ar" sem
ter aberto o browser (e errou um item de arquivo); dois verificadores marcaram falha falsa por não
conhecerem a regra do gateway; o relatório longo chegou cortado no orquestrador.

```
[SÓ CONFERE] Não edita, não commita, não mexe em gateway, não conserta. Achou erro → reporta.
[SKILL DO ASSUNTO] Carregue a MESMA skill que o worker usou (ex.: `wiven-checkout`, `trackeador`,
  `area-membros-netflix`) antes de conferir. As pegadinhas do assunto moram nela.
[MODELO] Conferência com browser (checkout público, painel logado, pixel) = Sonnet. Haiku só pra
  conferência de arquivo/código/git, nunca pra item que precisa abrir página.
[3 ESTADOS] Cada item = PASSA / FALHA / NÃO CONFERIDO + valor lido + caminho do print. O resumo do
  handoff conta os TRÊS ("7 passa, 1 falha, 3 não conferido"). Proibido resumir "tudo passou" com
  item não conferido. Não conseguiu abrir = NÃO CONFERIDO + erro exato, nunca "deve estar ok".
[FALHA TEM QUE SER REPRODUZIDA] Antes de marcar FALHA, descartar a causa boba do assunto (bump da
  Wiven só aparece após escolher pagamento; curl em checkout = 403 sempre). Dizer o passo exato.
[RELATÓRIO EM ARQUIVO] Gravar o relatório completo em `prints/verificacao-<data>/RELATORIO.md` da
  oferta (única escrita permitida) e mandar no handoff só o resumo + o caminho. Handoff longo chega
  truncado no orquestrador.
[HOST COMPARTILHADO] Gateway/Biblioteca com limite por IP: conferir por último, uma página por vez,
  e nunca enquanto outro pane está no mesmo host. Bloqueou → para, registra, não contorna.
```

Do lado do ORQUESTRADOR:
- "Mover" no brief = escrever `mv` e mandar provar que a origem ficou vazia. Worker tende a copiar.
- Conferir no relatório o que o verificador NÃO abriu antes de repassar "verificado" pra dona.
- Verificador também erra (deu "STATUS não atualizado" com o STATUS atualizado): item que decide
  retrabalho, o orquestrador confere com 1 grep/1 print antes de despachar correção.
- Duas ofertas no mesmo gateway na mesma noite: executar em paralelo pode, **provar** em fila.

## Pane que falha, trava ou some — regra do lado do ORQUESTRADOR  [buraco 14 · 25/09/2026]
- No despacho, o ESTADO grava `hora do despacho + prazo esperado` por pane; o prompt exige **ponto de retomada** (último item feito) no `.jsonl` a cada ~10 itens.
- Prazo vencido sem handoff: **1** `pane_read` (única leitura permitida) → fechar o pane → `pane_list` limpo → reabrir a partir do último ponto de retomada no MESMO perfil. Nunca re-despachar o mesmo lote em perfil ainda ocupado (colisão R6 #11).
- Retomada após reinício do app: rodar modo R + `pane_list` + fechar órfãos ANTES de qualquer spawn; reconciliar a tabela pane→perfil.

## IP bloqueado na Biblioteca  [buraco 32 · 25/09/2026]
Bloqueou → parar TUDO nesse IP, gravar ponto de retomada, esperar **≥50 min** e retomar com controle bom (`emagrecer`); concepção semi-medida = "não medido", nunca preenchida. Trocar de rede/VPN/proxy = decisão do dono. Nunca "contornar" trocando de perfil.
