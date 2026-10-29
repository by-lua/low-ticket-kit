---
name: mvt-obra-100k
description: MECÂNICA chamada pela skill `criacao-low-ticket-mvt` (passo 5 · T11 OBRA DE ARTE 100K e conteúdo da Parada 3). Monta a Obra de Arte 100K de cada modelagem validada: 8 elementos, valor, bônus, garantia, nível de consciência, mapa da vantagem de 10 linhas, Semáforo das Decisões (verde/amarela/vermelha), regras da Obra aprendidas na prática, checagem dos 8 erros. Use quando a orquestradora chegar em T11, quando o usuário pedir "montar a Obra", "obra de arte", "mapa da vantagem", "semáforo", ou ao preparar a Parada 3.
---

# mvt-obra-100k — passo 5 (T11)

> **Nomes de seção no texto abaixo** (`GATES TRAVADOS`, `ADENDO §x`, `passo N`, `FASE DE CONSTRUÇÃO`, `ROTEADOR`, `PASSO 0a/0b`, `PROMPT-PADRÃO`) são os da skill original, já dividida: cada um agora mora onde o `## ÍNDICE` da skill `criacao-low-ticket-mvt` aponta. O texto das regras não foi alterado.

> **IDs dos subpassos** = os de `criacao-low-ticket-mvt/references/TRILHA-CHECKLIST.yaml` (`T11.x`); evidência com nome de arquivo padronizado, conferida por `scripts/gate.py --passo T11`.

## ENTRADA EXIGIDA (conferir ANTES de começar — GATE DE PASSAGEM da orquestradora)
- T10 fechado: Parada 2 aprovada no ESTADO (data) e GATE 4 (`mvt-validar`) fechado (e etapa 2 do GATE DESTINO se cross).
Entrada ausente = passo anterior ABERTO: volte a ele pela TRILHA do modo em `criacao-low-ticket-mvt`. 
Sem `ESTADO.md` com o bloco `## ROTEADOR` gravado, esta skill não roda (chame primeiro `criacao-low-ticket-mvt`).

## 5 · OBRA DE ARTE 100K

Método: §10 (8 elementos, preço, bônus, mapa da vantagem) e o exemplo completo do Painel
do Meio Ambiente em `references/prompts-e-exemplos.md`.

Documento `OFERTAS/<id>/pesquisa/obra-de-arte.md` `[T11.1–T11.6]` (nome de arquivo FIXO — o gate procura este):
- **Concepção modelada** (9 elementos): abra o documento com a concepção em **UMA frase** e os 4 principais marcados, mais o `elemento_mudado` do passo 3 (item 3b) [YT 2hSIIWKZlBs; BOARD OBRA 100K]. Obra sem frase ou sem elemento mudado (fora a exceção cross-market declarada) = incompleta.
- **8 elementos da oferta:** promessa (= headline) · nome · o que compõe o produto principal · bônus ·
  vantagens · valor de venda · benefícios · copy base.
- **Valor:** (o preço final é gravado no ESTADO com dono+data e mudou preço = "muda em tudo", `T11.14`) dupla oferta — método começa em R$17,90 básico / R$27,90 completo.
  Se o usuário quiser outra faixa, é decisão dele; registre.
- **Bônus:** comando de 10 ideias (complementares + quebra de objeção) → escolher os
  que são coisa pronta e coerente. **Padrão da operação: ~4 bônus por oferta** (decisão do dono 25/09/2026 (revisão); o Heitor diz "de um a seis" na aula [05:54], no exemplo 4, e "de quatro a seis" no vídeo [YT 2hSIIWKZlBs]) — desvio dos ~4 só com o motivo registrado; **um deles pode ser o produto principal da referência** (no caso Salmos, "Evangelhos explicados" entrou como bônus). O ~3 dos PADRÕES abaixo é do Rodrigo (cross-market); a Obra segue o ~4 acima.
- **Garantia:** escreva prazo e texto (15 ou 30 dias: vídeo [YT 2hSIIWKZlBs] usa 30 no caso Salmos; na aula, painel Meio Ambiente, "garantia 15/30 dias" e reembolso é muito baixo); é uma das 10 linhas do mapa da vantagem.
- **Nível de consciência da Obra:** público = **fundo de funil/consciente** — quem já conhece o assunto [YT 2hSIIWKZlBs; BOARD 8 erros]. Escreva a frase que mostra que o público já está no mercado; se só serve a quem nunca ouviu falar, é vermelha (erro "nível de consciência errado").
- `[T11.5]` **Mapa da vantagem (Tarefa 03 do board):** comparar com 1–2 ofertas do mercado e preencher as **10 linhas**, cada uma com SIM/NÃO e a vantagem escrita [BOARD MAPA DA VANTAGEM; painel Tarefa 03]: produto principal · bônus · mecanismo da solução · comunicação · promessa · garantia/risco · tempo e facilidade de implementação · visual/apresentação · acesso/suporte · nome do produto. Linha em branco = Obra incompleta (o "NÃO" também precisa da justificativa).
- **Copy base = clareza sobre o produto**, sem história/descoberta/curiosidade [07:10:26] "não é sobre história. Não é sobre descoberta. Não é sobre curiosidade"; headline com uma única interpretação [07:21:01] "a headline ela precisa ser uma coisa direta que a pessoa tenha uma única interpretação". Narrativa de dor ("sua filha senta pra fazer a lição…") → refazer.
- **Nome = palavras do produto + para quem** [05:50:47] "painel educativo do dia do meio ambiente para professores"; "N coisas para X" quando houver número. Nome-marca solto ("Kit …", "Força …") não basta como identificador.
- **No mapa da vantagem, "NÃO" é normal** [06:14:04] "precisa aplicar nesses 10 pontos" [06:18:15] "eu não tenho uma vantagem aqui para a pessoa" (no exemplo dele mecanismo e tempo foram NÃO). 10/10 "SIM" sem justificativa por linha volta para refazer (a seção "onde o concorrente ganha" continua obrigatória).
- **Timebox:** ≈30 min por modelagem selecionada com o agente de oferta [05:29:03] "a gente consegue montar em 30 minutinhos"; a energia vai para escolher bem e para a vantagem [05:48:23] "gaste a sua energia nisso aqui". Passou de meio dia → você está fazendo operacional cedo.
- **Mudou mecanismo/produto/promessa → muda em tudo** [06:29:35] "você vai ter que modificar em tudo": página, criativo e mockups na mesma passada; registre no ESTADO.

**Virar o lead na Obra — prática recomendada antes do Semáforo (dona, 30/10/2026, "melhor dos dois
mundos": mapa da vantagem é comparativo SIM/NÃO, falta a simulação de objeção em 1ª pessoa).**
Depois do mapa da vantagem, roda `criacao-low-ticket-mvt/references/virar-o-lead.md` NA PRÓPRIA
Obra (promessa + 8 elementos + preço, mesmo sem página pronta ainda): na pele do comprador, por
etapa prevista (anúncio→promessa→oferta→preço), as 6 perguntas fixas (o que fisga, o que desconfia,
dúvida sem resposta, objeção de desistência, o que falta pra confiar, momento exato de desistir).
Objeção encontrada que o mapa da vantagem não cobriu vira ajuste ANTES de montar o Semáforo — não é
gate bloqueante no `gate.py` ainda (recomendação de prática, registra no `obra-de-arte.md` numa
seção "Virei o lead" se rodou).

**`[T11.7]` Semáforo das Decisões — obrigatório antes de selecionar (regra NOSSA, vinda do extra YT `M4cT8gIfilo`; não está na aula)** (método §10, "Semáforo das Decisões";
YT `M4cT8gIfilo`). **Origem: não é da aula** (0 ocorrências nas 11h43); vem do YT `M4cT8gIfilo`. Na aula a seleção é sem cor: 3-5 modelagens → Obras → 3-5 Obras + ordem de execução [04:12:50] "vai montar aqui de umas três a cinco obras de arte" [06:25:55] "de todas aquelas, selecionamos de 3 a 5 obras de arte" [06:07:50] "você vai definir uma ordem de execução". O semáforo roda só sobre as Obras JÁ MONTADAS (as modelagens selecionadas, ~10-20), nunca sobre a leva inteira de 55-60 concepções. Classificar cada uma em 🟢/🟡/🔴
pela tabela do método (tipo de produto · 10 mandamentos · demanda · intenção querem×precisam ·
concorrência · fator UAU), nesta ordem: **mata as vermelhas primeiro** (espere 30–50%) → puxa as
verdes ("quais as mais diferentes?") → o resto é amarela → aplica os 3 ajustes (mais específica ·
detalhar transformação · reposicionar comunicação) e reclassifica; não virou → vermelha com motivo.
Registrar no Hub em `semaforo` (`VERDE|AMARELA|VERMELHA`) + `semaforo_motivo` (1 linha). Vermelha
aqui não é apagada: vai pra `proximas-levas` com o motivo, igual regra geral de descarte.
Mapeamento com os nossos dados do passo 4: demanda = fontes orgânicas (YouTube/Trends/TikTok);
intenção "querem" = `sinal_de_compra` > 0; concorrência "ninguém vendendo" = comunicação livre na
Biblioteca. Fator UAU é julgamento — escreva a frase que gera o "caraca, isso é diferente"; se não
conseguir escrever, não é verde.

**Cor = só VERDE ou não-verde. "VERDE com condição/ressalva" NÃO existe como cor:** condição pendente (tabela, teste, checagem nossa) = AMARELA. Se o dono decidir liberar com condição, o ESTADO ganha `CONDIÇÃO → <id> · responsável · prazo · evidência` e a condição vira item BLOQUEANTE de T13 antes de vender (`T11.11`, conferido pelo gate; buraco 8, 25/09/2026).

**PROIBIDO no texto do semáforo/Obra: critério condicional fora do método** — "sobe a verde se o teste der X", "vira verde se…", "verde condicionada a…", "se o teste passar". O semáforo é 🟢/🟡/🔴 pela tabela do método + 3 ajustes + reclassificação; teste/checagem pendente se FAZ ANTES (T11.8) e a cor é dada com o resultado. "Verde com ressalva" só como ressalva do texto, nunca como condição de subida. O `gate.py` (T11.7) procura esse padrão no texto da Obra e acusa (`não sobe a verde` não conta; tudo que faça a cor depender de resultado futuro conta).

Selecione 3 a 5 obras **verdes** para a fase operacional (método) e defina a ordem de lançamento.

### Regras da Obra aprendidas na prática (18/09/2026)

**1. Mapa da vantagem: 10/10 é sinal de alerta, não de força.** Se a Obra ganha em tudo, ou o
concorrente é fraco de verdade (então diga POR QUE — na R3 um "10/10" era contra uma planilha
grátis usada como isca de SaaS, o que muda a leitura do território inteiro), ou ninguém procurou
direito. Exija a seção **"onde o concorrente ganha"** escrita, com a resposta da copy. Exemplos
reais: concorrente a R$10 contra nós a R$17,90 (preço é vantagem dele para professora de escola
pública); concorrente a R$167 com marca e produção visual consolidadas ("a copy não disputa
produção — disputa especificidade").

**2. Ticket acima da faixa se justifica pelo CUSTO DO PROBLEMA, não pelo preço do concorrente.**
Padrão que funcionou no Kit Aprovação Solar: "uma reprovação na distribuidora custa semanas de
retrabalho, deslocamento e risco de perder o cliente — R$500 a R$2.000. R$37,90 é menos que 2h de
trabalho do integrador." Escreva a conta em `sustenta_preco`.

**3. Ticket ABAIXO do mercado também precisa de resposta.** Nicho de commodity visual (figurinhas,
artes) pratica R$3,99-R$5,99; a faixa do método fica 4x acima. A pergunta "por que isso custa 4x
o do outro?" mata a conversão se não for respondida na oferta.

**4. Áreas sensíveis: posicione como PREPARO/estimativa.** Sempre que o tema for jurídico,
previdenciário, trabalhista, de saúde, de treino ou cálculo regulado, a oferta não promete
resultado regulado. **O produto NUNCA manda o cliente contratar/consultar outra pessoa** (revisor,
engenheiro, contador, advogado, "consulte um profissional") nem traz "não substitui ART/laudo" —
não faz sentido num low ticket (decisão do dono 25/09/2026 (revisão)); a validação dos dados é
feita POR NÓS com fonte pública + casos de teste nossos (T13.11-T13.12). O que funcionou:
- INSS → "organize seus documentos, saiba o que esperar", nunca "garanta seu benefício" ou "sem
  advogado" (promessa que não podemos cumprir). Público vulnerável (pessoa doente, afastada, sem renda) — nada de urgência artificial.
- Cálculo trabalhista → ferramenta de **conferência e estimativa**; a promessa fala do que a ferramenta faz, sem parecer e sem indicar terceiro.
- Treino → planilha/programa geral com ressalva, nunca prescrição individualizada.
- Dado que muda (norma de concessionária, versão de ferramenta de IA) → data de atualização
  visível, compromisso de revisão, e a fonte oficial declarada. Prometa "não ser reprovado por
  documentação", nunca "aprovação garantida".
Escreva na Obra, em uma linha, que a escolha foi deliberada — senão parece timidez de copy.

**5. Em território enorme, a vantagem vem do ÂNGULO.** `extensão de cílios` tem 12.000 anúncios e
todos vendem TÉCNICA; a vaga estava em **processo de atendimento** (o roteiro do primeiro
atendimento). Mercado grande não é mercado fechado — é mercado com um ângulo livre.

**6. Território vago é risco, não oportunidade.** `guia passo a passo prático` (3.400) serve para
qualquer coisa: comunicação genérica não conecta com dor e o criativo fica sem o que mostrar.
Quando as comunicações livres apontarem para públicos diferentes, escolha UMA e construa a oferta
inteira nela.

**7. Mapa da vantagem (SIM/NÃO) e virar-o-lead (1ª pessoa) respondem perguntas diferentes — rodar os
dois, nunca só um (30/10/2026).** O mapa mostra ONDE a Obra ganha/perde do concorrente; virar o lead
mostra ONDE o comprador desconfia mesmo numa linha "SIM" do mapa (ex.: garantia existe = SIM no
mapa, mas o lead simulado ainda pergunta "e se não funcionar pra mim especificamente?" — a resposta
a isso é texto, não aparece na tabela). Nicho sensível (regra #4 acima) é onde essa dupla checagem
mais compensa: a objeção de credibilidade clínica/jurídica raramente aparece como "NÃO" no mapa.

### `[T11.8]` Checagem de CONCORRENTE POR MECANISMO — RE-CONFERÊNCIA antes da Parada 3 (a checagem primária é `concorrencia-<id>.md` em T9.13, `mvt-validar`, antes da Parada 2; aqui reabre e atualiza; frescor ≤48h = T13.19) [decisão do dono 25/09/2026]

**"Ninguém vende" não se prova pelo termo de busca — prova-se pelo MECANISMO: o que o concorrente ENTREGA.** Erro real R7 #5: liberamos com a premissa "ninguém vende" e só depois vimos Automação JC / Ajuda Eletricista entregando o mesmo (app que calcula material+MO+lucro+PDF com marca), com termos de busca completamente diferentes. Para cada Obra, escreva `OFERTAS/<slug>/pesquisa/checagem-mecanismo.md`:
1. A **frase do mecanismo** da Obra (o que o comprador RECEBE/FAZ: "digita X, recebe Y").
2. Busca por **mecanismo e entrega**, não só pelo termo do território: descrições do que faz ("app/planilha/gerador que calcula…"), Biblioteca (anúncios sem o termo mas com a mesma promessa), Google/Play Store/YouTube ("app de…"), lojas de nicho. ≥3 formulações distintas do mecanismo.
3. Para cada concorrente achado: **página ABERTA** (URL + data de acesso + print em `prints/`) e a linha **"entrega:"** (o que o comprador recebe, preço, formato). Concorrente que entrega o mesmo mecanismo = a vantagem da Obra NÃO pode ser "ninguém vende": refaça o mapa da vantagem (`onde o concorrente ganha`) e a cor do semáforo.
4. Conclusão em 1 linha: `mecanismo livre | mecanismo ocupado por <X> (entrega igual/parcial)`.
Evidência para o gate: arquivo `checagem-mecanismo*.md` contendo `mecanismo` e ao menos uma URL `https://`.

## ⏸ Parada 3 — conteúdo (o formato e a regra de paradas estão na orquestradora)

Apresente a tabela do semáforo (obra · cor · motivo · ajuste tentado) e a(s) Obra(s) verde(s) inteira(s). **Antes de liberar, cada Obra verde leva 1 linha OK/NÃO por erro de concepção do board "8 erros"** [BOARD 8 erros]: mais do mesmo (já tem milhares rodando) · só PRECISAM, não querem · cético (difícil de acreditar) · transformação completa · curso longo barato · complexo de entender · nível de consciência errado · comunicação não específica. Um NÃO = volta ao passo 3 ou vai pra `proximas-levas`; não libera. (Os erros de execução/organização/constância são do executor: ver Condução.) Pergunte se libera a parte operacional. Liberou →
toque até o criativo sem nova parada, só volte se algo bloquear — **os GATES 6 e 7 seguem valendo**. Formato: `FORMATO DAS PARADAS`.

---

## GATE DE SAÍDA — GATE 5 · OBRA DE ARTE 100K → Parada 3

### GATE 5 · OBRA DE ARTE 100K → Parada 3
- [ ] `T11.1` `test -f OFERTAS/<id>/pesquisa/obra-de-arte.md` (contador `obra sem arquivo: 0`).
- [ ] `T11.1 · T11.2 · T11.3 · T11.6` Obra abre com a frase da concepção + 4 principais + `elemento_mudado`; 8 elementos; garantia com prazo+texto; bônus (faixa registrada); `sustenta_preco`.
- [ ] `T11.4` Nível de consciência da Obra (frase que mostra público já no mercado) · copy base = clareza sobre o produto, sem história/curiosidade · nome = palavras do produto + para quem.
- [ ] `T11.5` Mapa da vantagem: 10 linhas SIM/NÃO com justificativa + seção "onde o concorrente ganha".
- [ ] Mudou mecanismo/produto/promessa depois da Obra → muda em página, criativo e mockups na mesma passada (registrado no ESTADO).
- [ ] `T11.7` Semáforo em `semaforo` + `semaforo_motivo` (vermelhas primeiro).
- [ ] `T11.9` Parada 3: 1 linha OK/NÃO por erro do board "8 erros" em cada Obra verde. Um NÃO = não libera.
- [ ] `T11.8` `OFERTAS/<slug>/pesquisa/checagem-mecanismo*.md` — concorrente checado por MECANISMO, página aberta (seção acima).
- [ ] **Pivô:** Obra de concepção que apareceu depois do T7 só existe se a concepção passou por T7→T9→Parada 2 (`T7.13`, `T9.8`, `T10.4`); senão a Obra é rascunho `PAUSADA`, não vai à Parada 3.
- [ ] **Antes da Parada 3:** `gate.py --ate T11` exit 0 + Verificador Haiku (regra: orquestradora, GATE DE PASSAGEM).
- [ ] `T11.10` **Área sensível (jurídico/saúde/treino/cálculo regulado/norma):** a Obra traz a linha `área sensível: SIM|NÃO`; SIM exige posicionamento como PREPARO/estimativa (sem prometer resultado regulado) + fonte pública (oficial/fabricante) + data de atualização; **sem revisor/RT/freelancer e sem "consulte um profissional"** (regra #4 acima passa a ser item do gate).
- [ ] `T11.11` Semáforo VERDE sem "com condição/ressalva"; condição liberada pelo dono = linha `CONDIÇÃO →` no ESTADO (acima).
- [ ] `T11.12` `formato_entrega` + `evidencia_uso` (o público usa app/ferramenta digital?) escritos na Obra, sempre — não só quando o formato muda. `T11.13` classe do entregável declarada na Obra (Rápido/Ferramenta/Completo; teto padrão Rápido+Ferramenta, `Completo` só se o dono disser).
- [ ] `T11.14` Preço final (básico/completo/bumps/downsell) gravado no ESTADO com dono+data e igual à Obra.
