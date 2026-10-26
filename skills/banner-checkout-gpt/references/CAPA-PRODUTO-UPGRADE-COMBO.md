# Capa de produto do checkout — UPGRADE, COMBO e BUMP (receita única)

> Dona, 26/10/2026 — terceira vez que corrige isto. A regra existia como frase solta (wiven-checkout
> §2b, CLAUDE.md, memória) e o agente improvisou: **recortou a faixa do título do Jiu-Jitsu e colou
> em cima de um mockup do Tarot**. Esta receita é a fonte única; os outros lugares só apontam pra cá.

## O erro que não se repete (prova real)

`LOW-TICKET/MODELOS/REFERENCIAS-VISUAIS/ERRADO-upgrade-titulo-colado-tarot.jpg` — capa do upgrade do
Tarot (16/10): faixa "UPGRADE PARA COMPLETO" **navy/vermelho do Jiu-Jitsu** recortada e colada no topo de
um mockup roxo/dourado do Tarot. Defeitos: emenda visível, paleta de outra oferta, título cobrindo as
capas de trás, e mostra só o principal (não o pacote completo).

**Proibido, sem exceção:** Pillow/ImageMagick/HTML/canvas pra pôr texto na capa; recortar título de uma
imagem e colar em outra; pegar mockup pronto e escrever por cima; reaproveitar arte de outra oferta.
**A imagem inteira nasce numa geração só do GPT**, com o título fazendo parte da composição.

## Referências aprovadas (anexar como referência de ESTILO, nunca de conteúdo)

| Tipo | Arquivo (`LOW-TICKET/MODELOS/REFERENCIAS-VISUAIS/`) | O que copiar dela |
|---|---|---|
| Upgrade | `upgrade-para-completo-exemplo-jiujitsu.png` | título enorme em 2 linhas ("UPGRADE PARA" menor / "COMPLETO" gigante) sobre pincelada amarela+vermelha, seta curva apontando pro pacote, **pacote COMPLETO inteiro** espalhado embaixo (principal no centro + todas as capas de bônus + páginas/cards abertos) |
| Combo | `combo-especial-exemplo-jiujitsu.png` | selo/emblema "COMBO ESPECIAL" (escudo + faixa) no topo, **as capas dos itens do combo em 3D**, principal maior no centro e os outros dos lados, fundo limpo |

O estilo é do Jiu-Jitsu, mas a **paleta e a tipografia são da oferta** (`OFERTAS/<slug>/DESIGN-SYSTEM.md`).
Tarot = roxo/dourado/creme, serifada clássica — nunca navy/vermelho.

## Anexos (ordem)

1. A referência de estilo da tabela acima (1 arquivo).
2. As **capas reais** de cada item que aparece (principal + bônus no upgrade; os itens do combo no combo)
   — capa oficial pronta (`produto/`, `site/painel/conteudo/<item>/pagina-01-capa.*`, `produto/ORDER-BUMPS/<item>/capa.png`).
3. Upgrade: + 2 páginas internas reais pra aparecerem abertas.
Item sem capa real ainda (ex.: bump novo sem MVP) = **gerar a capa dele antes** (capa sozinha, mesma
identidade); nunca deixar o GPT inventar capa de item no meio da composição.

## Prompt-base (sem aspas duplas no texto; acentos explícitos; idioma declarado)

**Upgrade:**
```
Crie UMA imagem quadrada 1:1, arte de produto para checkout, em português do Brasil com acentuação correta.
Use a imagem 1 SÓ como referência de composição e estilo do título — não copie cores, textos nem produtos dela.
Título integrado na arte, enorme, em duas linhas: UPGRADE PARA (menor) e COMPLETO (gigante), com pincelada/faixa
atrás do texto e uma seta curva apontando para o pacote. O título faz parte da ilustração, mesma luz e textura.
Abaixo, o pacote COMPLETO da oferta <NOME>: o livro principal no centro (capa da imagem 2) e as capas dos bônus
ao redor (imagens 3..N), em mockup 3D realista, mais 2 páginas internas abertas (imagens finais). Use as capas
exatamente como estão, sem redesenhar nem trocar texto delas. Nenhuma capa cortada pelo título.
Paleta da oferta: <tokens do DESIGN-SYSTEM>. Tipografia do título: <fonte/estilo>. Sem preço, sem selo de desconto.
CRÍTICO: não reproduza nada do jiu-jitsu da referência.
```
**Combo:**
```
Crie UMA imagem quadrada 1:1, arte de produto para checkout, em português do Brasil com acentuação correta.
Use a imagem 1 SÓ como referência de composição: emblema com o título no topo e as capas em 3D embaixo.
Emblema integrado na arte com o texto COMBO ESPECIAL (ou COMBO <NOME CURTO>), grande e legível.
Abaixo, os <N> itens do combo em mockup 3D de livro, lado a lado (o principal do combo maior, no centro), usando
exatamente as capas das imagens 2..N+1, sem redesenhar nem trocar o texto delas, nenhuma cortada.
Paleta da oferta: <tokens>. Sem preço. CRÍTICO: não reproduza nada do jiu-jitsu da referência.
```
Combo com 5+ itens: 3 na frente + 2 atrás, todos com título legível; se não couber legível, pedir 2 linhas.

## Mecânica e entrega

- Geração: skill `gpt-imagem-playwright` (`gen2.sh`), **uma imagem por chat**, prompt em arquivo.
- Tamanho final: quadrado ~1000×1000, JPEG `-strip`, **≤ 250 KB** (é imagem de produto/bump no checkout).
- Salvar em `OFERTAS/<slug>/checkout/order-bumps/<item>.jpg` (bruto do GPT em `checkout/order-bumps/_brutos/`).
- Subir na Wiven pela `wiven-checkout` §1b (API, campo `files`, um produto por vez).

## Gate antes de mostrar à dona (olhar a imagem, não o log)

1. Título integrado (sem emenda, sem faixa retangular de outra cor colada, mesma iluminação).
2. Texto do título e das capas escrito certo, com acento.
3. Paleta da oferta, nada da referência (nenhum lutador, nenhum navy/vermelho em oferta que não é).
4. Upgrade mostra o pacote completo (principal + todos os bônus); combo mostra todos os itens dele.
5. Nenhuma capa cortada ou coberta pelo título.
6. Peso ≤ 250 KB e quadrado.
Falhou um = regerar (ajustar o prompt), nunca consertar com edição por cima.
