---
name: mvt-modelar
description: MECÂNICA chamada pela skill `criacao-low-ticket-mvt` (passos 2-3 · T5 DESTRINCHAR e T7 MODELAR). Destrincha os 9 elementos (prova de leitura, raio X, mapa de personas) e modela: eliminar o que não faz sentido, funil 20→10→3, 1-3 modelagens por concepção, subnicho, princípio prova≠leilão, elemento_mudado, território, comando de decisão, descarte por método e pools evitados. Use quando a orquestradora chegar em T5/T7, quando o usuário pedir "destrinchar", "modelar", "subnichar", "achar a direção", ou ao retomar a modelagem.
---

# mvt-modelar — passos 2-3 (T5 DESTRINCHAR · T7 MODELAR)

> **Nomes de seção no texto abaixo** (`GATES TRAVADOS`, `ADENDO §x`, `passo N`, `FASE DE CONSTRUÇÃO`, `ROTEADOR`, `PASSO 0a/0b`, `PROMPT-PADRÃO`) são os da skill original, já dividida: cada um agora mora onde o `## ÍNDICE` da skill `criacao-low-ticket-mvt` aponta. O texto das regras não foi alterado.

> **IDs dos subpassos** = os de `criacao-low-ticket-mvt/references/TRILHA-CHECKLIST.yaml` (`T5.x`, `T7.x`); a evidência de cada um tem NOME DE ARQUIVO PADRONIZADO e é conferida por `scripts/gate.py --passo T5|T7`. Saída ≠ 0 = passo aberto.

## ENTRADA EXIGIDA (conferir ANTES de começar — GATE DE PASSAGEM da orquestradora)
- T5: T4 fechado — Parada 1 aprovada no ESTADO (data + lista das que seguem) e GATE 1 (`mvt-minerar`) fechado.
- T7 (mesmo mercado A/E/F-BR): T5 fechado (GATE 2 abaixo). T7 (cross): T6 classificado como OCUPADO/gap de ângulo em `mvt-cross-market` (gap puro NÃO modela elemento).
Entrada ausente = passo anterior ABERTO: volte a ele pela TRILHA do modo em `criacao-low-ticket-mvt`. 
Sem `ESTADO.md` com o bloco `## ROTEADOR` gravado, esta skill não roda (chame primeiro `criacao-low-ticket-mvt`).

> **IDEIA GERADA = só candidata [T7.30, decisão do dono 25/09/2026].** Concepção que nasce de persona-first/Comando 4/brainstorm/"gerar do zero" só vive dentro do funil 20→10→3 e exige **PROVA DE MERCADO** registrada em `modelagem-*.md` (`prova de mercado:` + URL da Biblioteca/oferta concorrente real que já anuncia/vende o desejo/formato; ou, se ninguém anuncia, demanda MEDIDA com sinal de compra — oceano azul só com demanda). Sem prova = DESCARTE/PENDENTE, nunca Obra, e nunca apresentada ao dono como oferta (tag `[HIPÓTESE …]`, regra de fala na orquestradora).

## 2 · DESTRINCHAR — os 9 elementos + raio X de 1–2 ofertas

Método: §6 e §9 passo 1 + [YT e7MDJ2OgMNE / 68Q1cwhlpYE / M57JtDR3u-4]. Para cada concepção do Hub (`concepcoes`), três blocos:

**A) `[T5.1–T5.4]` Os 9 elementos** (marcando os **4 principais**: comunicação, formato, mecanismo, nicho/subnicho): nicho · **subnicho** · persona · dor · desejo · pensamento interno · resultado final · mecanismo da solução · formato.
Fonte: texto da página de vendas, VSL, post ou texto do anúncio → ChatGPT (equivalente ao agente de concepção). **Leia e entenda** o que voltou [aula 04:22:43] — sem isso a copy, o criativo e o produto saem ruins — e corrija à mão. Preencha a 4ª coluna do método ("elementos") → no nosso ambiente: Hub `concepcoes` nos campos listados em "Onde registrar".
**Prova de leitura (2 min por concepção que avançar):** só a partir dos 9 elementos, escreva headline (produto + formato), subheadline (desejo) e 3 bullets (resultado final) — [04:19:13] "só com essa informação aqui, eu já tenho tudo que eu preciso para criar uma cópia de uma página de vendas". Se não sai, o entendimento está errado: refaça antes de modelar ([04:23:25] "uma das piores coisas que você pode ter é estou vendendo algo e eu não sei o que tô vendendo"). Marque ★ nos 4 principais [04:18:46] "esse aqui seria o ponto número um" e grave a prova no registro (`prova_leitura`).
Qualidade exigida (antes saía 1 linha por elemento):
- **Pensamento interno em duas camadas:** *amplo* (a pessoa consigo mesma: "estou envelhecendo mais rápido") e *técnico* (sobre o material: "se eu tivesse apostilas prontas ganharia horas do meu dia"). Mínimo 2 de cada nas concepções que avançarem [YT xbWpBqDt8Ow; M57JtDR3u-4].
- **Marque a dor/desejo mais URGENTE.** Não urgente = registrar e deixar de lado ("a desvalorização da profissão me desmotiva… não é urgente") [YT xbWpBqDt8Ow]. Teste do pneu furado × para-brisa ruim [YT e7MDJ2OgMNE].
- **Querem × precisam:** 1 linha — a persona QUER isso ou só PRECISA? [aula 02:36:23]
- **Nível de consciência:** já está no mercado / precisa ser convencida.

**B) `[T7.10]` Raio X** (→ Hub: objeto `raio_x` na concepção; feito na MODELAGEM, de 1–2 ofertas por concepção escolhida [YT M57JtDR3u-4], não de todas no destrinchar; 1 tabela por oferta): mercado (dinheiro/saúde/relacionamento) · nicho · subnicho · persona (faixa etária, dor, desejo) · promessa · mecanismo · produto principal · bônus · order bump · valor · formato · tempo de acesso · suporte · garantia · pontos que chamam atenção. "É um raio X da oferta para identificar o que têm em comum, o que têm diferente" [YT M57JtDR3u-4]. Primeiro só coleta, depois organiza. (Preço aqui é informação registrada, nunca filtro.)

**Antes de montar o raio X, rodar `references/virar-o-lead.md`** (checklist de extração do funil
até o checkout + simulação de objeção 1ª pessoa por etapa) e marcar nota 0-10 por alavanca
(`references/4-alavancas.md`) — vira evidência MEDIDA pro campo "pontos que chamam atenção" e pro
"o que não se traduz" do cross-market, em vez de opinião solta. Se der pra ver o criativo de
anúncio dele (print/transcrição — nunca inventar sem material), analisar junto: formato (imagem/
vídeo/carrossel/story-ads), ângulo, como mostra a entrega (produto na tela, blur, mockup, print de
depoimento) — cruzar com `modelagem-escalados` (biblioteca de formatos) e, se a oferta estiver no
MineraAds/RatoAds, puxar de lá os anúncios já indexados do mesmo anunciante em vez de catar na mão.

**C) `[T5.5]` Subnicho — mapa de personas** (→ Hub: `mapa_personas`, 1 entrada por subnicho): quando 2+ ofertas caem no mesmo subnicho, liste **para qual persona cada uma fala** e qual mecanismo repetem ("mesmo mecanismo, personas diferentes" [YT lSEfqS7Jm44]). O espaço vazio do mapa é candidato a modelagem.

**N1–N5 (referência usada nos campos abaixo):** N1 = concepção em 1 frase (`concepcao_frase`) · N2 = `elemento_mudado` · N3 = `evidencia_formato` · N4 = lateralização (`modelado_de` — lote lateral de oferta `venceu`, regra "Modelar a própria concepção vencedora", item 3 das práticas abaixo) · N5 = `funil_subnicho`.

**Onde registrar:** Hub, `concepcoes` (não há planilha). Já existem `nicho`, `formato`, `checklist_100k`, `preco`, `pagina_vendas`. **Campos a criar quando o Hub for atualizado** (esquema completo no `HUB-OFERTAS/README.md`; ainda não existem em `ofertas.json`): `subnicho`, `persona`, `dor`, `desejo`, `pensamento_interno_amplo`, `pensamento_interno_tecnico`, `resultado_final`, `mecanismo`, `urgencia` (a mais urgente), `nivel_consciencia`, `querem_precisam`, `elementos_principais`; raio X em `raio_x` (objeto); mapa de personas em `mapa_personas`; N1–N5: `concepcao_frase`, `elemento_mudado`, `evidencia_formato`, `origem_referencia`, `funil_subnicho`; E3/E5: `gate_origem` (+ motivo), `prova_leitura`.

### GATE DE SAÍDA — GATE 2 · DESTRINCHAR (todas as que seguem)

### GATE 2 · DESTRINCHAR (todas as que seguem)
- [ ] `T5.1` 9 elementos + ★ nos 4 principais em 100% — evidência: nº com `elementos` preenchido == nº que segue.
- [ ] `T5.2` `prova_leitura` (headline + subheadline + 3 bullets) gravada nas que avançam para modelar.
- [ ] `T5.3 · T5.4` Pensamento interno amplo ≥2 + técnico ≥2, dor/desejo mais urgente marcada, querem×precisam, nível de consciência — nas que avançam.

---

## Padrão COMBO (conteúdo + ferramenta) — modelagem de mecanismo

**O padrão COMBO é o mais interessante dos dois:** pegar o formato que já está vendendo
(mapa mental, checklist, planilha, pack) e **acoplar a ferramenta que o faz funcionar**. O conteúdo
dá a prova de que vende; a ferramenta dá a vantagem que ninguém tem. Exemplos:

| Já vende | Combo com ferramenta |
|---|---|
| mapa mental de concurso | mapa + **simulado** que sorteia questões do tema e mostra desempenho |
| planilha de precificação | planilha + **calculadora** que devolve preço e margem preenchendo 3 campos |
| documentos de SST prontos | pacote + **gerador** que preenche os dados da empresa e exporta o PGR |
| planilha de treino | planilha + **acompanhamento** com progressão de carga |
| checklist de perícia INSS | checklist + **quiz de diagnóstico** que diz qual benefício se aplica |

É modelagem de MECANISMO no vocabulário do método — mesmo conteúdo, mecanismo mais atrativo
("use mecanismos mais atrativos, mais rápidos, mais fáceis, mais práticos, mais desejados"
[MATERIAL-FRAMEWORK]). E sustenta ticket acima da faixa base, registrado em `sustenta_preco`
na etapa 5.

Efeito prático: escolhido "ferramenta" ou "completo", entram na leva concepções cujo valor está em
CALCULAR, PREENCHER, ACOMPANHAR ou GERAR — que no modo rápido seriam recortadas para caber em PDF
e perderiam o melhor delas. O registro do porquê vai em `sustenta_preco` na etapa 5.

---

## 3 · MODELAR — apontar para uma nova direção

Método: §9 e `references/prompts-e-exemplos.md` (seção Modelagem).

Para cada concepção:
1. `[T7.1]` **Eliminar primeiro** os elementos que não fazem sentido modelar (senso crítico:
   "faria sentido vender isso para X? entregar nesse formato?").
2. `[T7.11 · T7.4]` **Explorar** os elementos que sobraram conversando com o ChatGPT a partir de ideias
   suas, sempre pedindo "que têm demanda, que as pessoas querem comprar e que não tem
   ninguém vendendo". **Modelar é pensar em conversa, não lote:** [04:52:32] "eu vou evitar usar o chat gpt para poder fazer vocês pensarem"; [04:50:40] "não tem que fazer com velocidade tem que fazer com qualidade". Worker pode rascunhar; a escolha (item 5) é do orquestrador com o dono, nunca de um lote de workers.
   Eixos que ele usa e vale perguntar: **data/ocasião** ("as 5 datas com maiores demandas de compra" [04:49:25] "faça uma lista das 5 datas com maiores demandas de compra"; a demanda tem prazo, [02:39:27] "a pessoa começa a vender 30 dias antes") · **coleção/curso gigante → uma pecinha** [06:31:38] "olha para ela como um todo e tira uma pecinha ali de dentro" · **pergunta de demanda ANTES de modelar** ("além de X, quais 5 áreas têm mais demanda?", [01:52:20] "eu poderia ter feito isso antes da modelagem").
2b. `[T7.2 · T7.9]` **Se o elemento modificado for a COMUNICAÇÃO (persona/dor/desejo)** — evidência: `persona-<slug>.md` (o mesmo arquivo do 2c) com a seção `Comando 4` — o caso mais comum — não pare em string de busca. O Heitor faz assim [YT M57JtDR3u-4]:
   1. GPT: "sugira ideias de personas para <mecanismo>". Cada persona = uma oferta diferente (pilates: home office, 50+, atleta, mulher que parou).
   2. GPT: "dentre essas, qual tem a dor/desejo mais urgente para a minha solução?" — escolha a persona (aqui entra *querem × precisam*).
   3. **Comando 4** com a persona escolhida + subnicho: dores e desejos, pensamentos internos **amplos e técnicos**, ~10 de cada, **os mais urgentes**. NÃO reaproveite as dores do concorrente ("vamos mudar o público").
   4. Persona detalhada em cima da dor mais urgente (nome, idade, situação) — vira o tom da página e do criativo.
   5. Só então a **promessa** e as 3 comunicações.
2c. `[T7.2 · T7.3]` **Persona-first (inverso) — SUBPASSO OBRIGATÓRIO quando R4 tem nicho/persona** (não é "técnica opcional"; dono, 25/09/2026, R7 #1-2): para cada persona-alvo, pergunte "para essa persona, que outra concepção?" [YT QcJxRCX-YN8] e rode o **Comando 4 COMPLETO** (dores, desejos, pensamentos internos amplos + técnicos, ~10 de cada, MAIS URGENTES marcados) → ~20 concepções a partir das dores/desejos urgentes (não só dos anúncios minerados) → funil 20→10→3. Evidência PADRÃO: `MINERACAO/<rodada>/persona-<slug>.md` com as seções `Comando 4`, `dores`, `desejos`, `pensamentos internos amplos`, `pensamentos internos técnicos`, `urgentes`, `persona-first` e a tabela `20 → 10 → 3`. O `gate.py` procura esses termos; sem eles = T7.2/T7.3 FALTA. Rodada sem nicho (R4 amplo): item N/A. As 3 escolhidas entram na MESMA validação das mineradas (T9).
3. `[T7.4]` Rascunhar até ~10 ideias (comunicação, formato, mecanismo, nicho/subnicho — qual dos 4 mudou) **só para chegar a 1 a 3 modelagens por concepção** [04:12:03] "eu não recomendo que você crie dez modelagens para cada oferta" (de 7 concepções saem ~21 [04:12:18] "de sete no mínimo a gente vai ter aqui vinte e uma concepções modeladas"). Registre no Hub e meça na Biblioteca **só as 1-3 escolhidas**; as ~10 ideias ficam em rascunho, não viram registro nem query.
3b. `[T7.6 · T7.8]` **Registro obrigatório de cada modelagem escolhida (Tarefa 01 do board)** — evidência: `modelagem-<lote>.md` com os rótulos literais `concepcao_frase`, `elemento_mudado`, `evidencia_formato` (quando formato mudou):
   - **Concepção em UMA frase** (→ Hub `concepcao_frase`) — "Todos os 150 Salmos explicados versículo por versículo" (comunicação = estudante/pastor · formato = ebook · mecanismo = Salmos · nicho = materiais bíblicos) [YT 2hSIIWKZlBs; BOARD MODELAR]. Sem a frase escrita a variação não é mensurável nem comparável.
   - **Elemento mudado — Sim/Não nos 4** (→ Hub `concepcoes.elemento_mudado`) (comunicação · formato · mecanismo · nicho/subnicho) [BOARD Tarefa 01 · MODELAR]. **Nenhum Sim = CÓPIA** (trocar cor, volume, mockup ou palavras não conta) e a variação não sai do passo 3 [YT 2hSIIWKZlBs]. Única exceção: cross-market, onde só o mercado muda — entra escrita como `elemento_mudado: nenhum — mercado (divergência declarada, ver bloco abaixo)`, nunca como "modelada".
   - Se o Sim for **formato**, escreva a evidência de que a persona já usa o novo formato (Biblioteca/comentários) → Hub `evidencia_formato` — "o formato é modelado caso sua persona realmente utilize o novo formato" [BOARD Exemplo 2; YT 2hSIIWKZlBs].
4. `[T7.7]` **Toda modelagem sai com TERRITÓRIO, não só com as 3 comunicações** (cada uma com o pensamento interno de que nasceu). O território é o núcleo
   do mercado em 3-4 palavras, escrito como o comprador escreveria. Sem ele a concepção não é
   mensurável e fica invisível em qualquer ranking depois. Erro real 18/09/2026: os lotes de
   modelagem 01-14 saíram só com as comunicações; 90 concepções ficaram sem termo de território,
   nunca foram medidas e não competiram na seleção. Território é campo obrigatório da saída da
   etapa 3, junto com as comunicações.
5. `[T7.11 · T7.14]` Rodar o **comando de decisão** e gravar `decisao-<lote>.md` (prompt + saída + porquê de cada corte; a lista de finalistas com motivo vai ao dono ANTES de gastar medição cara) (as ~10 ideias rascunhadas → as 1-3 que as pessoas mais querem comprar,
   têm demanda e ninguém vende, com o porquê).
6. `[T7.1 · T7.15]` **Descarte × `proximas-levas` (binário, cada linha cita a regra):** pool evitado/recorte futuro = `proximas-levas`; violação de método (Frankenstein, travou, cópia) = `DESCARTADA`. Todo descarte vai numa tabela mostrada ao dono na Parada 2 (concepção · regra citada · trecho). **Descarte por método é regra, não exceção**, e é **definitivo no Hub** (`validacao: DESCARTADA` + `nota_descarte`; não volta para `proximas-levas`). Descarte na hora: travou, complexo/Frankenstein [05:12:29] "você vai criar um frankstein", opções "mais ou menos", criativo demonstrativo difícil, mercado saturado depois de modelar ([05:03:36] "Cara, eu não dou segmento"), ou pool evitado (6b). Exemplo dele: 500 skills para Claude [05:11:28] "essa oferta aqui é uma oferta que eu não seguiria". Erro nosso (R3): ≥12 concepções que os workers marcaram "descartada por completo" (R3-021, 023, 030, 031, 037, 040, 065, 067, 069, 070, 133, 171) continuaram vivas no Hub com `CABE`. Registre o motivo.
6b. **Pools que ele evita** (não entram na leva; vão para `proximas-levas` com o motivo e só saem com recorte que TIRE a concepção do pool — "prompts para professor" NÃO tira, é o mesmo pool): IA/marketing digital [05:04:58] "eu não gosto muito de trabalhar com esses nichos de inteligência artificial" (motivo: métricas mais caras [05:05:10]); "N prompts prontos" [05:06:42] "500 prompts de chat gpt para tal coisa isso aqui já está saturado"; cético/emocional ("curar ansiedade") — só vira produto para o PROFISSIONAL ("materiais para hipnoterapeutas", [cauda ≈11:27] "são coisas mais céticas" · [cauda ≈11:29] "hipnoterapeuta").

Funil do método: de cada concepção, 1 a 3 modelagens; ao fim, 3 a 5 seguem para a Obra.

**Três práticas do Heitor que entram no MODELAR** (YT `2hSIIWKZlBs`, "Modelagem não é cópia"):

1. **Abrir o campo de visão — funil 20 → 10 → 3.** Escolhido o elemento a modelar, não pare nas
   primeiras ideias: liste **~20 opções** daquele elemento (ex.: 20 mecanismos), pesquise a fundo até
   sobrarem **10**, e defina **3 pra rodar**. "Tira o tapa-olho do burro da carroça." As ~10 ideias
   rascunhadas do item 3 acima são o meio desse funil, não o começo (o "3 pra rodar" aqui é o teto de 1-3 modelagens; não vira 10 registros). Pergunta-chave em cada opção: querem · tem
   demanda · ninguém vende? Ex.: referência "4 Evangelhos explicados versículo por versículo" → a
   Bíblia tem 66 livros, sobram 58 → pesquisa no YouTube/Ubersuggest → **Salmos** era o mais buscado e
   ninguém vendia → "150 Salmos explicados versículo por versículo" (R$500k+).
   **Registre** `[T7.4]` no `modelagem-<lote>.md`, por concepção que avança: tabela com as ~20 opções · as 10 que sobraram · as 3 escolhidas, o critério de cada corte e, por opção, a resposta a "alguém já vende?" (Biblioteca) e a fonte de demanda (YouTube/Uber Suggest) [YT 2hSIIWKZlBs]. Concepção que entra no passo 4 sem essa tabela = passo 3 aberto. Validação por "20-30 anúncios ativos há X dias" **não** substitui a tabela — ele a rejeita no mesmo vídeo.
2. **Pesquisar a fundo O QUE a coisa é, pra achar a troca de formato.** Entender de onde vem e pra que
   serve o produto revela o formato certo: Salmos são **cânticos** (louvor, clamor, adoração) → a
   maioria é de **Davi** → Davi tocava **harpa** → modelagem de FORMATO: ebook → **"Salmos em música"**,
   mesma comunicação e nicho, e de novo ninguém vendendo. **Registre** `[T7.5]` a linha `o que é` (origem · para que serve · quem criou/usa · pistas de formato) antes de escolher formato ou mecanismo [YT 2hSIIWKZlBs]. Trocar formato só quando serve ao público
   (ver ressalva app × ebook no passo 1), nunca "pra ficar mais bonito".
3. **Modelar a própria concepção vencedora.** Acertou uma concepção → ela vira referência nova:
   Salmos → Cartas de Paulo, Apocalipse, Provérbios, Daniel, Profetas, Pentateuco; Evangelhos → 30
   milagres de Jesus, parábolas. "De uma concepção eu tiro umas 10 ofertas — problema de oferta nunca
   mais." Referência também pode vir da **experiência do dia a dia**, não só da Biblioteca.
   **Gate:** oferta que vira `venceu` no Hub abre um lote de modelagem lateral — mesmos 3 elementos, mecanismo novo, ≥10 opções rascunhadas pelo funil 20 → 10 → 3 acima (saem 1-3 modelagens) — com `modelado_de` apontando para ela [YT 2hSIIWKZlBs].

Regra de fronteira (dele): **copiar = rodar a mesma concepção sem trocar nenhum dos 4 elementos**
(comunicação, formato, mecanismo, nicho/subnicho) — mesmo trocando cor, mockup ou dobrando volume.
Modelar = trocar pelo menos 1 (às vezes 2). Exceção declarada NOSSA: cross-market (abaixo).

**Sub-nicho é modelagem de primeira classe** (Comando 2 do método, nicho→subnicho). O coração do
MVT é "o que dá pra fazer EM CIMA do que já vende" — e sub-nichar é a forma mais direta: pega o
público VALIDADO de um território/oferta que escala e estreita pra **fatia com dor mais aguda e
latente**, criando produto só pra ela (ex: `250 dinâmicas cristãs` → `500 dinâmicas pra catequese`,
só catequista). Bidirecional: oferta nichada demais → ampliar pra fatia maior. Vale em TODOS os
modos (não só Biblioteca-BR). É uma das ideias rascunhadas do passo 3, mas medida em camadas barato→caro
no passo 4 e só avança quem passa a anterior:
1. Território do subnicho na Biblioteca **> 0** (tem gente — não sub-nichou até o deserto).
2. Comunicação livre = **vaga PROVISÓRIA** (ninguém vendendo aquela porta NA BUSCA; só confirma depois de `concorrencia-<id>.md`, T9.13 — 1 busca não prova "ninguém vende"). Ocupado → subnicho vizinho.
3. Demanda orgânica (4b) + `sinal_de_compra` > 0.
Termo-NÚCLEO mede o teto de demanda; termo-SUBNICHO acha a porta vazia — duas medições, não se
contradizem. Sub-nichar até zerar a audiência é o risco: a camada 1 barra.

**Sub-nicho fundo vale SE a demanda foi MEDIDA — profundidade não é o problema, profundidade CEGA é
(22/09/2026, confirmado transcrição Ed Borba `Do_0_ao_R_1.000.000...GwKEMxzTSjg`).** Estreitar é achar
fatia com dor mais aguda; o corte não é a distância, é ter território. Ex do próprio Borba: `1000
atividades pra idoso` → `atividades pra idoso com Alzheimer/demência` foi FUNDO e funcionou — porque ele
MEDIU antes (7,4M de americanos 65+ com Alzheimer, mercado enorme, já tem gente gastando). O erro é
aprofundar SEM medir e cair num recorte sem gente (camada 1 barra). Regra: mediu e tem demanda → fundo é
ótimo (comunica mais direto com a dor); não mediu → não aprofunda no escuro.

**Como ACHAR o subnicho (não só estreitar)** [Heitor]: (a) **Comando 2** gera nicho→subnicho→dor única→formato→título; (b) pesquise DENTRO do nicho (o exemplo Salmos, acima, é isso: 66 livros → 58 → YouTube + Uber Suggest); (c) leia o **mapa de personas do subnicho** (passo 2-C) — o buraco do mapa é o subnicho candidato [YT lSEfqS7Jm44]; (d) só aprofunda se a demanda foi MEDIDA. Registre a lista ~20 → 10 → 3 com o critério de cada corte (funil das "Três práticas") → Hub `funil_subnicho` (`candidatos_20`, `finalistas_10`, `escolhidos_3`, `criterio_corte`).

**Sub-nicho (público) e troca de MECANISMO/ÂNGULO são alavancas DIFERENTES — escolher pela causa.**
Diagnóstico primeiro: o que está saturado, o público ou o mecanismo? A resposta escolhe a alavanca.
- **Público saturado, dor com demanda** → sub-nicha (estreita o público; ver bloco acima). Só se mediu.
- **MECANISMO/formato saturado** (ex: "atividades", "dinâmicas", "exercícios pra idoso" — todo mundo
  vende) → NÃO estreita público, muda o **ângulo/benefício pro MESMO público**: mesma ideia-raiz, outra
  porta de entrada. Ex real (dono): exercício pra idoso já lotado no México → foram pra **prevenção de
  quedas em idosos** — adjacente ao exercício, mesma raiz, mas a promessa/apresentação pro público é
  outra, escapa do formato saturado. Pode também trocar o veículo de entrega (microSaaS/ferramenta, mapa
  mental, checklist, planilha, quiz). É o eixo "ângulo/mecanismo/formato" do princípio prova≠leilão logo
  abaixo. A chave é: **mesma audiência validada, entrada NOVA** — não a mesma "dinâmica" de sempre.

**Ler o FUNIL/formato vencedor do nicho no destino, não só a oferta solta (22/09/2026).** Antes de
decidir mecanismo, buscar o NICHO na Biblioteca do destino (termo traduzido — não-literal, como o
nativo fala) e ver **o que os anunciantes com MUITOS anúncios estão usando de FUNIL/formato**. Ex:
`1000 exercícios pra idoso` no BR é página de vendas; olhando o nicho na gringa, quem escala usa
**quiz**. Então o movimento é trocar página→quiz (ou VSL, microSaaS, mapa mental — o que o nicho lá
premia). O mecanismo vencedor não se adivinha: **lê-se do nicho no mercado-destino**. Entrega segue
nosso padrão (visual, área de membros), mas o FUNIL de entrada copia o que já converte lá.

**Princípio "prova ≠ leilão"** (estende "modelar não é copiar"). Oferta com muitos anúncios é PROVA
de escala, nunca convite pra rodar igual — copiar o público+ângulo+mercado dela = disputar o MESMO
leilão, CPM sobe, você perde pro pixel maduro dele. Toda modelagem em cima de oferta escalada tem
que **sair do leilão por pelo menos um eixo**: outro mercado (cross-market), outro público
(sub-nicho), outro ângulo/mecanismo, ou outro formato. É o que transforma "achei algo que vende" em
oferta nossa. Combinar eixos é mais forte.


**Paralelização (forma de executar, não de pular passo):** modelagem de concepções diferentes é independente — dá para
dividir em lotes e abrir panes (`pane_spawn({ prompt })`, uma tarefa por pane, saída em
`MINERACAO/<rodada>/modelagem-<lote>.md` + `handoff_submit`). No prompt do worker:
ler `low-ticket-metodo-mvt/SKILL.md` §9 e não usar browser (a validação da etapa 4 é
do orquestrador). Pane com `agent: 'codex'` exige `model` explícito do catálogo dele.
O orquestrador escolhe as modelagens (item 5) e confere o `modelagem-<lote>.md` contra o GATE 3 antes de aceitar. Despachou → encerre o turno e espere o handoff.

---

## Princípio prova≠leilão — lado das fontes  [ex-ADENDO §A]

## A · Princípio "prova ≠ leilão" e sub-nicho → agora no CORPO (passo 3 MODELAR)
Os dois viraram método (não são mais só referência): a regra "prova de escala ≠ disputar leilão,
sair por um eixo — mercado/público/ângulo/formato" e "sub-nicho é modelagem de primeira classe"
estão no **passo 3 · MODELAR**. Aqui fica só o que apoia isso do lado das fontes.
Prova de que é oferta viva de verdade (pra valer o esforço): nº de anúncios ativos estável ou
subindo **+ anunciante testando coisa nova** (criativos novos, order bump mudando) = está lucrando.
15 anúncios recém-subidos = ainda testando, não modela ainda.
Régua do Borba (referência, NÃO substitui o nosso piso de 7 d): sinal de vida = mesmo nº de ads ativos ou subindo + testando criativos/order bump novos [BORBA-GA iIOMI4OOCXA]. Divergência declarada no passo 3.

## Sub-nicho  [ex-ADENDO §C]

## C · Sub-nicho → agora no CORPO (passo 3 MODELAR)
Promovido a modelagem de primeira classe — ver passo 3. Aqui só o gancho: o modo E da abertura
aponta pra cá, mas a mecânica (camadas núcleo/subnicho, bidirecional) mora no MODELAR.

---

## GATE DE SAÍDA — GATE 3 · MODELAR

### GATE 3 · MODELAR
- [ ] `T7.6` `sem modelagem (p2-3): 0` (exceto DUPLICATA/DESCARTADA com motivo).
- [ ] `T7.6 · T7.7 · T7.8` Por modelagem escolhida: `concepcao_frase` · `elemento_mudado` (Sim/Não nos 4; nenhum Sim = CÓPIA, salvo cross-market declarado) · **território (3-4 palavras)** · 3 comunicações com pensamento interno · `evidencia_formato` se formato mudou.
- [ ] `T7.4 · T7.5` Tabela 20 → 10 → 3 + linha `o que é` em `modelagem-<lote>.md` para cada concepção que entra no passo 4 (sem ela = passo 3 ABERTO).
- [ ] `T7.2 · T7.3` **PERSONA-FIRST (2c) obrigatório quando a rodada tem nicho/persona (R4 ≠ amplo)** (subpasso 2c acima; mesmo arquivo `persona-<slug>.md`) — dono, 25/09/2026 ("pulamos algo?"): Comando 4 COMPLETO por persona-alvo (dores, desejos, pensamentos internos amplos+técnicos, ~10 palavras cada, marcando os MAIS URGENTES) → ~20 concepções a partir das dores/desejos urgentes (não só dos anúncios minerados) → funil 20→10→3 → as 3 entram na mesma validação das mineradas. Evidência: `persona-<nome>.md` com Comando 4 + tabela 20→10→3. Sem isso o passo 3 está ABERTO: as modelagens só enxergam o que já é anunciado. Erro real R7: dimensionador elétrico escolhido sem persona-first; dono perguntou "tem certeza que é a melhor concepção?".
- [ ] `T7.9` Elemento mudado = comunicação → persona escolhida + Comando 4 (dores/desejos/pensamentos internos amplos e técnicos, os mais urgentes) registrados; NÃO reaproveitar dores do concorrente.
- [ ] `T7.10` Raio X (`raio_x`) de 1-2 ofertas por concepção escolhida; `mapa_personas` quando 2+ ofertas caem no mesmo subnicho.
- [ ] `T7.1 · T7.11` Comando de decisão rodado; descarte por método com `nota_descarte` (definitivo, não volta p/ `proximas-levas`).
- [ ] `T7.13` **PIVÔ:** concepção/mecanismo que surgiu DEPOIS do T7 (concorrente derruba premissa, "e se…") passa por ESTE gate inteiro como concepção nova — persona-first/Comando 4, 20→10→3, `elemento_mudado`, território — antes de qualquer Obra. Regra do pivô: `criacao-low-ticket-mvt` (GATE DE PASSAGEM).
- [ ] **Antes de devolver:** `python3 ~/.claude/skills/criacao-low-ticket-mvt/scripts/gate.py --rodada <rodada> --passo T5` e `--passo T7` exit 0 (saída colada no ESTADO pela orquestradora).
- [ ] `T7.14` `decisao-<lote>.md` (prompt + saída + porquê de cada corte). `T7.15` tabela de descartes com regra citada, mostrada na Parada 2. `T5.6` dedupe contra `concepcoes`+`ofertas`+`proximas-levas` de TODAS as rodadas (`dup-check: N novas` no ESTADO ou `dup-check*.md`).
