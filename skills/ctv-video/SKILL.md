---
name: ctv-video
description: Produz criativo de vídeo do sistema LOW-TICKET a partir da ficha da leva aprovada — cenas (Flow), narração (NinjaVoice), gravações de tela do entregável, b-roll — e entrega pra edição. Use para gerar vídeo demonstrativo, UGC, expert, caixinha, POV.
---

# ctv-video — vídeo

**Entrada:** linha aprovada da `FICHA-LEVA` com o **roteiro completo** (gancho + desenvolvimento + CTA) ·
`OFERTA.md` · material do entregável (`criativos/MATERIAL-ENTREGAVEL/`, gravações de tela).
**Saída:** `criativos/<MERCADO>/CRIATIVO-N/` — vídeo final 9:16 + `anuncio.md`; intermediários em `intermediarios/`.

## Passos
1. **Mapear todos os assets** da oferta antes de montar (gravações, takes, b-roll): cada vídeo usa um pouco de cada.
2. **Cenas de pessoa** (UGC, expert, POV): Flow (`flow-video-playwright`) — pessoa segurando o material real,
   criada a partir de referência real do país (regra abaixo).
3. **Cenas de mesa/demonstração:** 1-2 aparelhos + 3-4 folhas impressas, página diferente em cada; zoom de câmera
   orgânico (aproximação lenta), gesto padrão = apontar.
4. **Voz:** `narracao-hub-tts`, voz fixa da leva; **conferir o gênero** com `vozes.sh` antes de gravar
   (Rocha é masculina).
5. **B-roll — cenas reais orgânicas do TikTok primeiro** (muito melhores que Pexels/banco):
   - **3-4 termos em inglês** da cena de cada frase (ex. idosos: "dementia activities", "memory care", "ot elderly",
     "cognitive games"; tarô: "learning tarot beginner", "tarot cards on table");
   - rodar `python3 scripts/broll-tiktok.py --out <PROJETOS-MIDIA>/VIDEOS-REFERENCIA/<SLUG>-broll-tiktok "termo 1" …`
     (~1 min por termo: busca no perfil `tiktok2`, filtra ≥50 mil views e ≤90 s, baixa em paralelo, folha de contato
     de 4 quadros + `ORIGEM.md`) e criar o symlink em `criativos/`;
   - escolher olhando as `.sheet.jpg`: **sem texto queimado** na parte usada (ou recortar fora dele);
   - `get-brolls` só pra fonte que o script não cobre (YouTube, Wikimedia, NASA, print de notícia) — é lento.
6. **Montar:** regras da `ctv-edicao` (todas). Mecânica de render: `criativo-ads-video-orq`.

**Pessoa em cena (UGC, expert, POV, foto com gente) — referência real do país (dona, 01/11/2026):**
1. Buscar no **Pinterest** (perfil `pinterest`, porta 9246: `~/.claude/bin/browsers.sh pinterest` → `agent-browser --session pinterest`) a cena + o país/idioma do mercado: "mulher brasileira
   dirigindo carro", "mujer argentina en la cocina", "psicóloga brasileira consultório", "american woman 50s kitchen".
2. Baixar 2-3 fotos reais que batem com a persona da `OFERTA.md` (idade, classe, cenário) em
   `PROJETOS-MIDIA/CRIATIVOS-CONCORRENTES/<SLUG>-pessoas-ref/` (mídia de terceiro, fora da pasta sincronizada).
3. Anexar no GPT como **referência de estilo, não de rosto**: pedir uma **pessoa NOVA** com o mesmo jeito real
   (pele, cabelo, roupa, casa/carro, luz de celular) daquele país, **segurando o nosso material** (capa real anexada).
   Nunca reproduzir o rosto da pessoa da foto.
4. Essa foto aprovada vira o quadro inicial do vídeo no Flow (imagem → vídeo) e a mesma pessoa segue a leva toda.
Objetivo: gente com cara de gente daquele país, não de IA.

Formato e roteiro: `ctv-formatos` + `ctv-copy`. Fecho: → `ctv-revisor`.

**Catálogo de takes de demonstração:** antes de inventar uma composição, consultar `criativo-ads-video-orq/references/takes-mesa-real.md` (catálogo A–O). Take J = TV com página inteira e caneta apontando + zoom orgânico; pode variar mão pela direita/esquerda e usar outra página REAL. Impresso = D/I/O. Não rolar para inventar conteúdo: regra `flow-video-playwright` § Conteúdo de tela fechado.
