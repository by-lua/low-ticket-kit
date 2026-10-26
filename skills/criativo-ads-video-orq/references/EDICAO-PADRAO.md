# EDIÇÃO PADRÃO — o estilo de edição de TODO vídeo de anúncio (fonte única, 26/10/2026)

> **Regra da dona (26/10/2026):** edição é UMA coisa só, separada do modo do criativo.
> UGC, expert, demonstrativo, caixa de perguntas, imagem animada — o MODO decide o que o
> roteiro diz e que cenas entram (`estilos-de-video.md`); a EDIÇÃO (este arquivo) decide como
> monta, corta, legenda, mixa e fecha — e é sempre a mesma. Ninguém precisa pedir "edita no
> estilo do demonstrativo": pediu vídeo, a edição é esta.
>
> Este arquivo **manda** sobre qualquer trecho do `SKILL.md` que diga outra coisa sobre
> velocidade, corte, legenda, trilha ou CTA. Os trechos antigos ficaram lá como histórico.
> Mudou regra de edição? Muda AQUI, nunca só no SKILL.md.

Ler inteiro antes do primeiro `ffmpeg`/`remotion`. Cada linha já custou uma versão reprovada.

---

## 1 · Ordem de montagem (nunca pula)

1. **Roteiro completo** escrito (hook → mecanismo → CTA) — vem do modo + `criativo-ads/references/ROTEIRO-POR-FORMATO.md`.
2. **Voz** gerada (`narracao-hub-tts`, voz fixa da leva; conferir gênero com `vozes.sh` — Rocha é masculina) e/ou **clipe de personagem** (Flow) com a fala.
3. **Alinhar** a voz: `scripts/legenda_align.py` → `words.json` (tempo de CADA frase).
4. **Ler frase por frase o que a fala diz** e só então escolher a cena de cada trecho.
5. **Montar** no Remotion (layouts + transições + legenda), ffmpeg só mede/normaliza/mixa.
6. **Trilha** por baixo, **card CTA** depois do fim natural da fala.
7. **QA** (seção 9) assistindo inteiro. Só então "pronto".

## 2 · Corte

- **1 clipe por frase da voz.** A cena ILUSTRA aquela frase ("nadie te mostró el movimiento" →
  cena do movimento sendo mostrado). Duração do corte = duração da frase, nunca bloco redondo de 3/4/5 s.
- **Cortes de tela/b-roll: 1,5–3 s.** Nenhuma cena passa de ~3–4 s sem corte (zoom/pan não substitui corte).
- **Clipe de personagem falando (lip-sync)** dura a fala dele — corta no fim da 1ª ocorrência completa
  (o Flow repete a frase quando sobra tempo; ler a transcrição do clipe cru, nunca pelo RMS).
- **Variedade:** usar TODAS as fontes de cena disponíveis (`criativos/ASSETS-MAPA.md`, `MATERIAL-ENTREGAVEL/`,
  `FLOW-TAKES/`, `BROLL-3D/`); nenhum take nem b-roll repete na mesma peça; peças irmãs usam b-rolls diferentes.
- **Junções:** fade de áudio 30–50 ms em toda borda; troca de layout = transição animada ~0,3 s, nunca corte seco de tamanho.
- Cortar silêncio de cabeça, cauda e pausas internas inúteis; preservar pausa que dá sentido.
- Nenhum frame de material velho vaza em transição (`startFrom` no 1º frame certo).

> Obsoleto: "≥6 s por cena" (tabela de números, 07/09) — era de outro formato; não vale mais.

## 3 · Layouts (caixa de ferramentas — o modo escolhe quais usa)

| Layout | Quando | Regra |
|---|---|---|
| **Tela cheia** | hook, CTA, ou quando 1 fonte carrega a frase sozinha | b-roll `cover` real 1080×1920 (cropdetect = 1080:1920) |
| **Split 70/30** | frase de mecanismo, material precisa ser lido | **entregável EM CIMA 70%**, b-roll/pessoa embaixo 30%, feather na costura |
| **Split 50/50** | b-roll/pessoa carrega metade do sentido | idem, entregável em cima; b-roll embaixo sempre em movimento |
| **PiP** | pessoa narrando enquanto a tela é protagonista | miniatura canto inferior 28–32% da largura, cantos arredondados |

Quem está grande é quem carrega a informação naquele segundo. Gravação de celular: cortar barra
de status/URL antes de compor. Imagem parada com Ken Burns nunca é cena de produto (usar gravação real).

## 4 · Velocidade

- **Padrão: 1.0 (ritmo natural da voz).** Nunca acelerar a timeline montada.
- Voz saiu rápida/lenta? Ajusta **na fala gerada, antes de montar** (TTS/clipe), nunca no vídeo editado.
- Acelerar só se a dona pedir naquela peça — e aí 1.05–1.1x primeiro, sempre a partir do arquivo RAW
  (conferir: duração da voz crua × vídeo mudo cru batem ±0,3 s; senão já tem aceleração embutida).

> Obsoleto: "Acelerar é padrão", "1.15x é o padrão medido", "1.35x no GATE FINAL", "1.30–1.40x sem lip-sync"
> (setembro). A dona reverteu em 24–25/10: soaram rápidos demais.

## 5 · Legenda (sempre, todo vídeo)

- Tempo: **`scripts/legenda_align.py`** (alinhamento forçado roteiro+áudio; venv `~/Developer/legenda-karaoke/.venv`
  — conferir que existe antes de instalar outra). **Nunca whisper/proporcional/distribuir por duração.**
- Render: **Remotion KaraokeV2 do projeto aprovado** `OFERTAS/mapa-do-tarot/criativos/BR/CRIATIVO-1/intermediarios/remotion-cap`
  (copiar o projeto; nunca reimplementar de cabeça, nunca ffmpeg/ASS se existe Remotion).
- Spec (só pra CONFERIR, a fonte é o `.jsx`): Montserrat 900 caixa alta, 60 px, branco com a palavra falada `#FFD400`,
  contorno de text-shadow preto, centro em **70% da altura** (**62–64% no split**), blocos curtos de 1–3 palavras
  como o `legenda_align.py` gera (nunca a frase inteira numa linha). Tela limpa nas pausas.
- Roteiro com acento certo ANTES do TTS (TTS e legenda leem o mesmo texto). Ortografia palavra por palavra.
- Alinhar só a trilha de VOZ e prender o `end` da última palavra ao fim real da fala — senão a última
  palavra vaza em cima do card. Truncar: `[w for w in words if w['end'] <= duração_do_corpo]`.
- `words.json` copiado de outro criativo = legenda errada: conferir 1ª e última frase contra o roteiro DESTE vídeo.
- Legenda é a ÚLTIMA camada. Clipe com texto queimado (TikTok, caption, watermark) é descartado.

## 6 · Áudio

- **Uma única fonte de voz** (nunca voz embutida de render anterior + voz nova = eco/fase).
- Voz final sempre a NOSSA (`narracao-hub-tts`), mesmo que o clipe do Flow tenha saído com voz dele.
- **Trilha instrumental contínua -18 a -22 dB**, do 1º frame até o fim do card (não troca no meio, não corta no fim da fala).
  Banco: `OFERTAS/mapa-do-tarot/criativos/BR/_ASSETS/trilhas/`.
- Medir, não ouvir: `volumedetect` voz sozinha × trilha sozinha; master ~-16 LUFS, true peak ≤ -2 dBTP.
- B-roll sempre mudo (`-an` / `muted` no Remotion).
- Detalhe de limpeza (high-pass, denoise leve, normalização por trecho): `acabamento-natural-audio-cortes.md`.

## 7 · Fecho e CTA

- **Fala do CTA = só o comando curto**, sem nome do produto, sem preço/garantia/vitalício ("Clicá acá abajo y descubrí").
- **O vídeo termina natural** (a fala do CTA inteira) e **DEPOIS entra o card, +~5 s** com a trilha seguindo.
  Nunca cortar a cena do CTA pra caber o card.
- **Card CTA (asset único da leva, reusado):** fundo preto · mockup COMPLETO do produto no topo (única exceção
  do "nunca mockup") · faixa com o comando em branco sobre a cor da marca · **seta vermelha com bounce pra baixo**.
  Mockup: `produto/MOCKUPS-NOSSOS/` → página de vendas no ar (curl no HTML) → lâmina real só se não houver nenhum.
  Outra peça da leva já montou o card? Reusa o arquivo.
- Sem tarja de marca (só se o brief pedir).

## 8 · Formato e técnica

- 1080×1920, fps nativo do motor (Veo = 24), concat por **filtro** (nunca `-c copy`), normalizar toda cena
  pra 1080×1920 antes do concat, `ffmpeg -nostdin` em laço, sem `-stream_loop` quando a fonte já cobre o slot.
- **Margem de segurança:** nada essencial no topo ~14% nem na base ~20%, nem colado nas laterais.
- Pasta: final solto na raiz de `CRIATIVO-N/`, o resto em `intermediarios/`. Nunca apagar clipes-fonte.
- Toda peça sai com `anuncio.md` (`criativo-ads/references/texto-anuncio-por-angulo.md`).

## 9 · QA antes de "pronto" (bloqueante — assistir inteiro, não frames redondos)

- [ ] Hook nomeia a dor real · corpo desenvolve o MECANISMO (não repete benefício) · CTA só comando.
- [ ] Cada corte casa com a frase falada; nenhuma cena > ~3–4 s; todas as fontes usadas; nada repetido.
- [ ] `grep "src:" src/index.jsx` aponta pro arquivo que você ACABOU de gerar (não `final-v2.mp4` velho).
- [ ] Transcrever o áudio do arquivo JÁ renderizado e conferir com o roteiro (palavra repetida, faltando, sem acento).
- [ ] Abrir 1 frame de CADA fonte da lista de concat (clipe de outro criativo/pessoa errada entra fácil).
- [ ] Card começa exatamente no fim do corpo (frame ~0,3 s antes e depois), sem legenda vazando.
- [ ] Karaokê: 1 palavra amarela por frame e ela MUDA entre frames; nada sobreposto (frames a cada 0,5 s).
- [ ] Trilha presente do início ao fim e mais baixa que a voz (números do `volumedetect`).
- [ ] `cropdetect` 1080:1920 em cada b-roll; `freezedetect` zero; sem barra do navegador.
- [ ] Assistir como cliente vendo pela 1ª vez: faz sentido? fica bom? Só então "pronto".
