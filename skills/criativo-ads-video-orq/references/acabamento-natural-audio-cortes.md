# Acabamento natural: cortes, voz e clareza da oferta

Aprendizado aprovado pelo usuário na revisão do Número Mestre AR/LATAM, em 02/10/2026. Aplique a criativos de Flow/Veo, talking head e VSL. “Limpo” significa fala inteligível, volume coerente e costura natural; mantenha a aparência orgânica pedida pelo projeto.

## 1. Parta dos originais e registre as decisões

Preserve os clipes crus e faça backup do master antes de substituí-lo. Faça inventário com ffprobe: resolução, fps, codecs, áudio, duração e início/fim de cada stream. Trabalhe em <videos_dir>/edit/. Guarde hashes, transcrição por palavra, trechos mantidos, motivo do corte, velocidade, filtros, medições, legendas e limitações em edl.json/project.md. Não transforme caminhos ou números deste caso em defaults globais.

Use transcrição por palavra de fonte aceita pela skill de produção. Reutilize o cache quando o hash for igual. Não retranscreva uma fonte intacta só por mudar a montagem. Alinhe o áudio realmente pronunciado; o roteiro ajuda a detectar erro, mas não prova o que foi dito. Se a fonte de transcrição falhar, registre o fallback e suas limitações; não declare revisão auditiva quando só houver ASR, waveform e frames. Respeite a regra de motor de transcrição da skill chamadora.

## 2. Som não é fala: escolha a ocorrência correta

silencedetect/tight.py oferece candidatos, nunca a lista final de trechos. Ruído, música, respiração e roupa podem ultrapassar o threshold depois da fala. Não conserve todo evento não silencioso, nem use a última palavra de um transcript sem antes selecionar a ocorrência correta.

Leia cada clipe comparando fala e intenção. Marque: frase completa, falsa partida, palavra repetida, reinício da frase, cauda sem conteúdo e gesto tardio. Flow pode preencher os segundos restantes repetindo o começo. Corte após a primeira ocorrência completa. Se a primeira tentativa estiver incompleta, preserve o melhor trecho completo posterior. Nunca deixe “no se ve” quando a frase é “no se escoge, se calcula”. A montagem pode unir duas partes corretas do mesmo clipe, desde que fala, gesto e lip-sync funcionem juntos.

Use padding de 30–200 ms como ponto de partida; ajuste vendo e ouvindo para preservar primeira sílaba, consoante final, respiração útil e intenção. Quantize os cortes ao fps real. Não imponha aceleração ou redução de duração só porque funcionou em outro vídeo.

## 3. Corte áudio e gesto juntos

Inspecione frames e waveform perto do fim da frase e na junção renderizada. Se a personagem termina, espera, começa a levantar o braço e o corte interrompe o gesto, antecipe antes do gesto quando ele não tiver função narrativa. Se o gesto completa a ideia, mantenha-o inteiro ou use outra tomada/cutaway. Não conserve uma cauda vazia por hábito.

Preserve pausas internas que dão entendimento, ênfase e respiração. Encurte apenas as que prejudicam o ritmo. Um jump cut intencional pode funcionar; uma sílaba mordida, um braço interrompido e uma falsa partida não são estilo. Avalie a sequência em velocidade normal.

## 4. Música e ambientes

Diferencie trilha intencional de música criada na cauda do Flow. Não remova música ou gestos significativos automaticamente. Quando a preferência não estiver clara, pergunte se deve manter e suavizar ou cortar antes; a ausência de resposta não autoriza a opção dependente.

Se houver trilha intencional, prefira um bed contínuo e transições de ganho/crossfade sob a fala. Não reinicie a trilha em cada cena. Quando autorizado a remover a cauda, corte antes da entrada indesejada sem encurtar a palavra. Mantenha ambiente discreto para não alternar entre ruído e silêncio absoluto. Um fade curtíssimo evita clique, mas não resolve sozinho uma mudança grande de música ou room tone.

## 5. Limpe com moderação e meça o volume

Meça loudness, true peak e ruído antes e depois, por cena e no master. RMS/peak isolados não representam volume percebido. Ganho global sozinho mantém as diferenças entre clipes. AAC pode decodificar com overshoot acima de 0 dBFS; isso pede análise, não prova sozinho clipping irreversível.

Faça a menor correção necessária. Possível ordem: reparo de clipping/click quando diagnosticado → high-pass moderado → denoise leve → compressão moderada → normalização medida → fades → concat/mix → limiter final. Não aplique todos os filtros cegamente. Confira sibilância, consoantes, voz metálica, pumping e respiração amputada. Se o original estiver danificado, não prometa recuperação perfeita: outra tomada/regeração pode ser melhor.

Use normalização medida em duas passagens por trecho/cena quando houver diferenças de nível; escolha um alvo comum adequado ao destino. Como referência inicial para fala, cerca de -16 LUFS no master e true peak até -2 dBTP; o alvo não é uma exigência universal. Meça novamente o arquivo AAC final, pois a codificação pode aumentar true peak. Deixe headroom, sem maximizar o volume.

Caso aprovado: high-pass 85 Hz, redução de ruído leve (afftdn nr=8/nf=-45), compressão ratio=2, normalização por trecho -18 LUFS e ganho final 2 dB com limiter. Fades de 50 ms em todas as bordas. Esses valores são ponto de comparação; calibração por material é obrigatória. A medição final foi -15,90 LUFS / -1,69 dBTP / LRA 1,90, sem pico acima de full scale no master.

## 6. Monte e legende na timeline final

Renderize segmentos com parâmetros compatíveis antes do concat. Mantenha áudio e vídeo com a mesma duração de trecho. Confira frames, sample rate, canais, PTS e padding/priming do AAC: atrasos pequenos repetidos podem acumular dessincronização. A legenda usa o tempo após cortes e mudanças de velocidade, nunca o tempo da fonte.

Aplique fades de áudio de pelo menos 30 ms em cada borda; 50 ms funcionou neste caso. Escolha crossfade mais longo só quando necessário e confira se não mistura palavras. Faça mix/limiter final sem estourar. Preserve fps nativo, salvo requisito explícito. Legenda é a última camada; mantenha a canônica do projeto, sem trocar VSL existente por estilo de anúncio arbitrário.

## 7. Verifique o master, não só os clipes

- Confira toda fala/CTA e os pontos corrigidos no transcript final; procure duplicação, falsa partida, palavra faltando e preço antigo em todas as versões de mercado.
- Inspecione cada junção renderizada em janela de cerca de ±1,5 s com frames e waveform; ouça quando houver acesso à reprodução. Confira flash, gesto interrompido, estalo, trilha quebrada, salto de volume e lip-sync.
- Amostre início, fim e miolo; valide legibilidade/sincronia das legendas e ausência de overlays sobre elas.
- Meça loudness/true peak final; execute ffprobe/decode e compare duração real com EDL e endpoints dos streams. Não acumule drift entre cenas.
- Guarde backup, EDL, métricas e evidência de revisão. Ao substituir asset web, versione a URL para evitar cache antigo; teste que o dev carrega o arquivo novo. Commit e publicação são etapas distintas; respeite o pedido atual do usuário.

## 8. Clareza psicológica que acompanha o criativo

A sequência aprovada foi identificação da situação → interpretação compreensível → mecanismo → entregável visível → benefício pessoal → oferta/garantia real. Aplique conforme o público e a peça, sem forçar uma VSL inteira num hook curto.

Traduza cada item do produto em uso concreto: “três números” precisa explicar em que situações ajuda a reconhecer padrões no trabalho, relações ou dinheiro. “Guia digital” ganha sentido quando pode ser consultado ao repetir uma dificuldade. Use nome/contexto quando disponíveis e autorizados, sem expor detalhes técnicos do quiz ao comprador nem inventar personalização.

Mantenha o quiz introdutório curto; a pessoa veio pelo Número Mestre, não por uma explicação de engenharia do cálculo. Não mostre blocos como “você escolheu X, as respostas orientam a leitura” se não ajudam a decisão. CTA expressa desejo: “Quiero mi número maestro”, em vez de “Ver mi lectura y el precio”. Preço e condições ficam na página de vendas e no `anuncio.md`, nunca na fala do CTA nem na tela do fecho; o CTA fica só no comando curto.

Preserve voseo AR e espanhol neutro LATAM. Dê destaque ao valor na moeda local quando a conversão estiver disponível e identifique estimativas; dólar secundário no LATAM. Não invente agenda limitada, urgência, ancoragens ou promessa de ganho/cura. Numerologia é interpretação simbólica, sem garantia de mudança material na vida. Não anuncie entrega, bônus ou garantia diferentes do produto real.

## Caso de referência e critérios de reaplicação

No LATAM, cena 6 tinha “No se escoge” e depois uma falsa partida; foram unidos os trechos corretos “No se escoge / se calcula”. Cena 13 terminou na primeira ocorrência completa de “resolver”. Cena 20 (“Los ciclos de tu vida y en cuál estás ahora”) terminou antes de ruído e gesto de braço tardio. As pausas naturais foram preservadas. O master passou de ~122,29 para ~126,42 s: priorizou-se fala completa e costura natural, não a menor duração.

Na AR foi removida a cena inteira que dizia o preço antigo, mantendo entrada/saída naturais e CTA. A checagem LATAM não encontrou preço falado. Nunca transplante esses timestamps para outra fonte: use hashes, transcript e inspeção do material atual.

Cenários para checar se estas instruções foram compreendidas:
1. Fala termina em 5,4 s; ruído em 7,5 s supera threshold e braço começa a subir. Resultado esperado: fim perto da fala com padding validado, sem conservar a ilha de ruído ou interromper o braço.
2. Primeira tentativa correta, falsa partida, segunda parte correta e repetição no fim. Resultado esperado: selecionar partes completas necessárias, conservar significado, suavizar junção e verificar o master.
3. Cenas de voz com volumes diferentes e trilha nas caudas. Resultado esperado: medir/igualar loudness, reduzir ruído sem destruir timbre, tratar preferência da música explicitamente, medir o AAC final e recalcular legendas após cortes.
