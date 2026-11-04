# Doutrina — o criativo valida o público e tem que parecer orgânico (movido de criativo-ads-video-orq em 26/10/2026)

> Vale pra imagem e vídeo. Cores: sempre as do `DESIGN-SYSTEM.md` da oferta.


## DOUTRINA — o criativo valida o público (regra 2026-09-21)

**PRINCÍPIO-MÃE:** o criativo tem que SAIR como se fosse orgânico. Nada inventado
de IA, nada exagerado, **nada clean/perfeito** — acabamento de agência denuncia
que é anúncio e mata a entrega. E o padrão é **partir sempre de um MODELO
VENCEDOR da biblioteca de escalados** (`modelagem-escalados`), modelar o que já
roda com verba — não inventar do zero.

Meta usa o CRIATIVO pra achar e validar o público, não só o targeting. Criativo
que não diz pra quem é = algoritmo joga num leilão largo/caro. Sintoma real:
CPM disparou (R$400 → R$1200) num criativo bonito e vazio (mockup neon, sem
rosto, sem dor, sem público nomeado). CPM alto quase nunca é "público ruim" — é
**criativo que não comunica pra quem é**.

**Em vídeo, quem valida o público é o HOOK.** O hook nomeia a persona nos
primeiros 1-2s, direto: *"Se você é dono de barbearia..."*, *"Professor que dá
aula particular, presta atenção..."*, *"Nutricionista sem site, isso é pra
você."* O criativo aponta o público pra ele mesmo se reconhecer. Uma leva =
vários hooks, um por persona (mesma matriz persona×ângulo do Kevones), body
igual. Assim cada persona valida separado e o algoritmo aprende rápido.

**O criativo tem que parecer o mais ORGÂNICO possível.** Facebook/Instagram são
redes de ENGAJAMENTO — o feed premia conteúdo nativo e enterra o que grita
"anúncio". Cara de IA / bonito-cool demais / render limpo = engajamento cai =
**CPM dispara**. Cenário e composição têm que parecer post orgânico / conteúdo
nativo tirado por uma pessoa, não peça de agência. Isso é o que baixa o CPM.
**Priorize os formatos da biblioteca de escalados** (`modelagem-escalados`) que
já imitam conteúdo orgânico — print de Stories, caixa de perguntas, vídeo de
celular na mão, screen-record — em vez de inventar arte "de anúncio". E use
**fonte estilo legenda de Story** (sans limpa, nativa). Referência de formato que
performa:

- **Cara de post de Stories:** legenda em cima do vídeo com fonte tipo Stories,
  linha fina, texto simples — não banner de oferta.
- **Legenda estilo TikTok/Reels nativo (karaokê):** palavra a palavra, texto
  **branco** que **pula pra amarelo** na palavra falada no momento (o "bounce"
  word-by-word highlight). É o padrão de legenda auto do TikTok — passa como
  conteúdo, não como ad. Montar no Remotion (ver `remotion-captions` /
  `captions-overlay`). Amarelo destaca a palavra-gancho da fala.
- Gravação de tela real, PiP falante, b-roll de banco — tudo que quebra o
  acabamento "comercial" e aproxima de UGC.
- **Cores:** sempre as do `DESIGN-SYSTEM.md` da oferta (a antiga "azul + laranja" era de outro negócio, MinhaEmpresa — não vale aqui).
- **Texto no estático/thumb: prefira o GPT colocar o texto**, não overlay de
  código — texto do GPT sai orgânico (legenda de Story), overlay de código sai
  "perfeito demais", cara de anúncio. Diga o texto exato + fonte estilo Story +
  cores no prompt do GPT. QA de ortografia obrigatório (modelo erra letra),
  regenera se torto. (Legenda karaokê de vídeo continua no Remotion.)
- **TODA imagem de criativo/ad sai com FILTRO ORGÂNICO "foto feia de celular", SEMPRE.**
  Diferente do entregável/mockup (esses são limpos, na identidade do `DESIGN-SYSTEM.md`):
  a imagem de anúncio tem que parecer foto real tirada no iPhone e postada no Stories —
  não render de IA, não estúdio. No prompt do GPT peça explícito: foto de celular amador,
  levemente torta/desalinhada, luz natural/ambiente imperfeita, leve grão/ruído e blur de
  câmera de celular, sem retoque, enquadramento de story vertical, "shot on iPhone", cara de
  UGC/postagem espontânea. Nada de perfeição comercial. **Isso derruba muito o CPM** — é o
  que faz passar como conteúdo nativo, não como ad. Regra de vida, todo criativo. Memória
  `criativo-imagem-organica-iphone`.
- **Mockup/entregável DENTRO do criativo = foto orgânica de "eu imprimi e usei".** Quando o
  criativo mostra o produto (mockup, capa, página de entrega), NÃO cole o mockup limpo do
  DESIGN-SYSTEM na arte — peça ao GPT uma FOTO amadora de iPhone do material **impresso em papel
  espalhado numa mesa de casa real** + **tablet/celular mostrando a capa**, com props do dia a dia
  (xícara de café, óculos, caneta, luz de janela), leve grão e enquadramento torto, legenda de
  Story por cima. Parece que a pessoa comprou, imprimiu e fotografou — não render de catálogo.
  Refs reais em `references/organico-iphone/` (ref-entregavel-impresso-mesa.png,
  ref-mockup-tablet-mesa.png — tutorial nicolasmoreirafe, "criativos em imagem totalmente
  orgânicos"). Anexe essas refs no GPT + a capa/página real do produto como conteúdo.


**"Empresário" é só um exemplo — a persona varia.** Não fixe numa role. O método
pra gerar as personas/hooks de uma leva:

1. **Liste TODA funcionalidade da entrega** — tudo que o produto faz/inclui.
   (Ex. SiteExpress: site em 72h, alteração inclusa todo mês, hospedagem inclusa,
   link da bio, botão WhatsApp, mapa, aparece no Google, sem fidelidade, painel
   próprio, domínio .com.br...) Uma linha por funcionalidade.
2. **Cada funcionalidade vira um ângulo** — o benefício/dor que ela resolve.
3. **Cada ângulo puxa uma persona/role** que sente aquela dor. Uma funcionalidade
   pode servir várias personas; escolha a que mais dói pra cada uma.
4. O hook = persona + ângulo. Leva = 1 hook por (persona×ângulo), body igual.

Assim a leva cobre vários públicos de propósito e o algoritmo valida qual role
converte, sem você chutar "empresário". É a matriz persona×ângulo do Kevones,
alimentada pela lista de funcionalidades da entrega.

**O texto do anúncio (copy primário/legenda) também valida o público.** Não é só
imagem/vídeo. A primeira linha do copy nomeia a persona e a dor, igual ao hook —
o Meta lê o texto pra entregar. Copy genérico = leilão largo. Mesma regra: 1
persona por variação, primeira linha = persona + dor.

**Palavras que inflam o CPM — evite.** Certos termos derrubam o quality/engagement
ranking e disparam o CPM (ou reprovam o anúncio):
- **Atributo pessoal na 2ª pessoa** ("você está endividado", "você é gordo",
  "você tem mais de 50") — política de atributos pessoais do Meta, penaliza forte.
  Reescreva impessoal: "quem tá endividado", "pra quem passou dos 50".
- **Promessa/sensacionalismo** ("garantido", "100%", "ganhe dinheiro fácil",
  "milagroso", "urgente!!!", CAIXA ALTA excessiva, excesso de emoji/!!!).
- **Termos de nicho sensível** (saúde, dinheiro, relacionamento, emagrecimento)
  ditos como afirmação sobre a pessoa.
Prefira dor + prova + benefício concreto, em 2ª pessoa neutra ou 3ª pessoa.


**UM criativo serve feed E stories** — não renderize dois. Monte no canvas 9:16
(1080×1920), mas mantenha TODO texto/legenda/CTA/logo dentro da **banda central
4:5 (1080×1350)** — os ~285px de cima e ~285px de baixo são só fundo/vídeo. Assim
o corte do feed não come legenda. Vale pra estático e pra legenda de vídeo.

Gate: antes de subir, o criativo passa no **teste de 1 segundo** — estranho olha
1s e sabe (a) PRA QUEM é e (b) a DOR. Não passou, não sobe.

