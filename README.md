# Low Ticket Kit

Pacote completo de skills para **Claude Code** para criar e vender produto digital **low ticket**
(R$ 10–50): achar a oferta, montar a página, gerar o entregável, ligar o checkout, fazer os
criativos (imagem, vídeo, narração) e rodar o tráfego.

É independente: instala tudo que precisa (skills, plugin, scripts e dependências) e **se atualiza
sozinho**.

## Instalar

Linux ou macOS, com o [Claude Code](https://claude.com/claude-code) instalado:

```bash
git clone https://github.com/by-lua/low-ticket-kit.git
cd low-ticket-kit
./install.sh --dry-run   # mostra o que vai fazer
./install.sh
```

O instalador:

1. instala as dependências do sistema (git, curl, jq, ffmpeg, python3, Node.js/npm, Chromium, ImageMagick)
   pelo gerenciador do seu sistema (apt, pacman, dnf, zypper ou brew) — pede `sudo`;
2. instala as ferramentas: `uv`, `yt-dlp`, `youtube-transcript-api`, `gflow-cli` (Google Flow),
   `browser-harness`, `agent-browser`, `hyperframes`, `@remotion/cli`, e as libs Python Pillow, imagehash e num2words;
3. liga as skills em `~/.claude/skills`, o plugin `get-brolls` em `~/.claude/plugins/cache`, os scripts em
   `~/.claude/bin` e os mapas de site em `~/.claude/browser-workspace`;
4. cria o auto-update (veja abaixo).

Skill ou script com o mesmo nome que você já tinha vira `<nome>.bak-<data>` — nada é apagado.
Já tem as dependências? `./install.sh --no-deps`.

## Atualização automática

O repo fica em `~/.local/share/low-ticket-kit` e as skills apontam para ele. Toda vez que o Claude Code
abre, um hook (`SessionStart`) puxa a versão nova do GitHub em segundo plano (no máximo 1x a cada 6h).
Não precisa fazer nada.

- Atualizar agora: `bash ~/.local/share/low-ticket-kit/update.sh`
- Versão instalada: `cat ~/.local/share/low-ticket-kit/VERSION`
- **Não edite as skills dentro dessa pasta** — a atualização sobrescreve. Quer personalizar? Copie a skill
  para `~/.claude/skills/<outro-nome>` e edite a cópia.

## Sem hospedagem? Use a Cloudflare (grátis)

Não precisa de servidor para colocar a página de vendas e a área de membros no ar:

| O que | Onde | Custo |
|---|---|---|
| Domínio | [Cloudflare Registrar](https://dash.cloudflare.com/?to=/:account/domains/register) — preço de custo, sem taxa extra (`.com` ≈ US$ 10/ano) | barato |
| Página de vendas (HTML estático) | [Cloudflare Pages](https://pages.cloudflare.com) — conecta no GitHub e publica a cada `git push` | grátis |
| Área de membros / webhook do checkout (backend leve) | Cloudflare Pages Functions ou Workers | grátis até 100 mil requisições/dia |
| Imagens, PDFs, vídeos do produto | Cloudflare R2 | grátis até 10 GB |
| SSL (https), CDN, proteção | já vem junto | grátis |

Passo rápido: crie conta na Cloudflare → compre ou aponte o domínio → **Workers & Pages → Create →
Pages → Connect to Git** → escolha o repo da página → em **Custom domains** ligue o domínio.
Peça ao Claude: *"publica a página dessa oferta na Cloudflare Pages com o meu domínio"*.

Já tem VPS? As skills também funcionam com Coolify, Vercel, Netlify ou qualquer host estático.

## Como usar

Abra o Claude Code numa pasta vazia e peça em português:

- *"vamos criar uma oferta low ticket do zero"* → `criacao-low-ticket-mvt` (conduz o processo inteiro)
- *"minera ofertas na Biblioteca de Anúncios sobre <nicho>"* → `mvt-minerar`
- *"gera as imagens da página de vendas"* → `imagens-pagina-low`
- *"cria a área de membros estilo Netflix"* → `area-membros-netflix`
- *"o que falta entregar nessa oferta?"* → `auditar-entregaveis-oferta`
- *"cadastra o produto na Wiven/Mundpay"* → `wiven-checkout` / `mundpay`
- *"faz 3 criativos de vídeo e 3 estáticos"* → `criativo-ads`
- *"monta a campanha"* → `metaads-kevones`

## Mapa

```
criacao-low-ticket-mvt  (porta de entrada: método MVT, trilha T0–T15, gates)
 ├─ achar a oferta    → mvt-minerar · mvt-modelar · mvt-validar · mvt-obra-100k · mvt-auditar
 │                      mvt-cross-market · x1-cross-market-mvt (levar oferta pra outro país)
 ├─ funil             → mvt-funil (order bump, upsell, downsell, combo)
 ├─ página de vendas  → imagens-pagina-low · depoimentos-pagina-de-vendas · popup-saida-low-ticket
 │                      otimizacao-pagina-vendas · traduzir-entregavel-imagem
 ├─ entregável        → area-membros-netflix · auditar-entregaveis-oferta · gpt-imagem-playwright
 ├─ checkout          → wiven-checkout (BR) · mundpay (EUR/USD) · ggcheckout-produto · hotmart-produto-playwright
 │                      cooud-checkout · zenith-gateway · banner-checkout-gpt · checkout-premium · publicos-meta-checkout
 ├─ criativo          → criativo-ads (estratégia)
 │                       ├─ vídeo     → criativo-ads-video-orq → flow-video-playwright (Google Flow)
 │                       │                                     → narracao-hub-tts (voz) · get-brolls (b-roll)
 │                       │                                     → embedded-captions · captions-overlay · remotion-* · hyperframes
 │                       └─ estático  → modelagem-escalados → gpt-imagem-playwright (ChatGPT)
 ├─ orgânico          → stories-diarias-ofertas · modelar-perfil-social
 └─ tráfego           → metaads-kevones (estrutura, teste, escala, BidCap)

base: low-ticket-metodo-mvt (o método) · organizar-projeto · yt-transcricao · watch
browser: agent-browser · browser-harness · browser-cloudflare · ~/.claude/bin/browsers.sh
```

## Contas que você vai precisar

| Para | Conta |
|---|---|
| Imagens (entregável, página, criativo) | ChatGPT com geração de imagem (Plus ou superior) |
| Vídeo por IA | Google Flow (plano com créditos de vídeo) |
| Narração | NinjaBR Hub (NinjaVoice) — ou outro TTS que gere WAV |
| Checkout | uma: Wiven, Mundpay, GGCheckout, Hotmart, Cooud ou Zenith |
| Anúncios | Meta Business (Gerenciador de Anúncios + Pixel) |
| Hospedagem | Cloudflare (grátis, veja acima) ou a sua |

Os browsers ficam **logados e visíveis** (nunca headless), um perfil por conta:

```bash
~/.claude/bin/browsers.sh add gpt 9222 https://chatgpt.com
~/.claude/bin/browsers.sh gpt          # abre, você loga uma vez
~/.claude/bin/browsers.sh status
```

Coloque seus perfis do ChatGPT em `~/.claude/bin/gpt-contas.lst` (linha: `<conta> <perfil> <porta>`).
Google Flow: `gflow auth login --browser chrome --profile flow-gflow`.

## Desinstalar

```bash
for l in ~/.claude/skills/* ~/.claude/bin/* ~/.claude/browser-workspace/domain-skills/*; do
  [ -L "$l" ] && readlink "$l" | grep -q low-ticket-kit && rm "$l"
done
rm -rf ~/.claude/plugins/cache/engenheirodevideo ~/.local/share/low-ticket-kit
# e apague a linha do update.sh em "hooks" → "SessionStart" de ~/.claude/settings.json
```

## Notas

- Alguns arquivos de skill citam exemplos de ofertas reais (nomes, domínios, preços) — são exemplos do
  método; troque pelos seus.
- `modelagem-escalados` vem só com o catálogo em texto dos formatos; as imagens de referência de anúncios
  de terceiros não são distribuídas.
- Skills de terceiros incluídas para o pacote funcionar sozinho: `agent-browser` (Vercel Labs),
  `remotion-*` (Remotion), `hyperframes` (HeyGen), `get-brolls` (engenheirodevideo), `watch`.
  Cada uma mantém a licença original.
- `metaads-kevones` resume a metodologia de tráfego do Kevones (Seleta Comunidade).
