# Modelador Automático — método puro (RatoAds/MineraAds), pra fazer na mão

Formato exato usado pela ferramenta (`server/modelador.js` do MineraAds, clone do
RatoAds) quando não quiser/puder rodar o Modelador Automático. Serve pra modelar
qualquer anunciante escalado manualmente, com a mesma estrutura.

## Passo a passo manual

1. Abra a Biblioteca de Anúncios do Facebook, ache o anunciante escalado, clique
   no NOME dele e copie o link (precisa ter `view_all_page_id=` na URL).
2. Leia os anúncios ativos (o máximo que der, 10-40) e anote por criativo:
   `titulo`, `cta`, `copy` (corpo do anúncio, até ~700 caracteres).
3. Ache o link de destino (landing/checkout) num dos anúncios, abra e leia o
   texto da página (ignora imagem/script). Puxe preço se aparecer (`R$ XX,XX`).
4. Calcule dias rodando = hoje − data do anúncio mais antigo. Ativo há mais
   dias = mais validado.
5. Preencha o **DIAGNÓSTICO** (o que é a oferta):
   - `produto`, `publico`, `promessa`, `mecanismo`, `formato`, `preco`,
     `por_que_funciona` (por que essa oferta escala — a dor específica que
     ataca e o atrito que remove).
6. Gere ideias nas **6 famílias de modelagem** (2 a 4 ideias cada, evidência
   sempre apoiada em algo que apareceu nos anúncios/página, nunca invenção):
   - **subnichar** — recorta o público/problema pra um pedaço mais específico
     do mesmo nicho (ex.: "saídas de emergência" dentro de Jiu-Jitsu geral).
   - **trocar_angulo** — mesmo produto/público, muda a dor/motivação que puxa
     a venda (ex.: de "medo de apanhar" pra "economizar energia no treino").
   - **trocar_publico** — mesmo mecanismo, público diferente com mais poder
     aquisitivo ou dor mais aguda (ex.: mesmo manual, público 40+ em vez de
     geral).
   - **trocar_roupagem** — mesmo conteúdo, empacotamento/formato de entrega
     diferente (ex.: manual em PDF → baralho de flashcard → fluxograma).
   - **trocar_nicho** — mesmo mecanismo estrutural, nicho totalmente diferente
     que tem o mesmo gargalo (ex.: "cards de decisão rápida" de Jiu-Jitsu →
     xadrez, plantão médico, defesa pessoal).
   - **trocar_formato** — muda o meio de entrega/consumo (PDF → app web → Anki
     → áudio).
   Cada ideia leva: `titulo`, `entrega` (o que o lead recebe, concreto),
   `descricao` (o que muda em relação ao original e por quê), `demanda`
   (alta/media/baixa), `dificuldade` (baixa/media/alta — baixa = fácil de
   produzir), `publico` (pra quem), `por_que` (por que funciona).
7. Escolha o **TOP 3** entre todas as ideias geradas (título, tipo,
   justificativa, evidência — trecho/fato dos anúncios ou da página que apoia)
   e dentro desses o **TOP 1 disparado** com um plano de 3 passos concretos
   pra executar.
8. Feche com **ressalvas**: o que não deu pra confirmar (faturamento real,
   conversão, se o formato funciona no público novo, etc.) — nunca inventar.

## Regra de ouro
Toda ideia nasce de EVIDÊNCIA real dos anúncios/página (nunca "achismo" do
que funcionaria) — é o mesmo princípio de prova de mercado da skill
`mvt-modelar` (ver `[[modelador-manual-borba]]` cruzado lá: elemento mudado
sempre com evidência, nunca hipótese sem prova).

## Exemplo real (Manual do Jiu-Jitsu, RatoAds, 27/09/2026)
Ver `RATO-ADS/pesquisa/EXEMPLO-MODELADOR-JIUJITSU.md` — modelagem completa
rodada pela ferramenta num anunciante escalado (9 anúncios, 53 dias no ar),
com as 6 famílias preenchidas, top3, top1 disparado e ressalvas. Use como
referência de nível de detalhe esperado por ideia.
