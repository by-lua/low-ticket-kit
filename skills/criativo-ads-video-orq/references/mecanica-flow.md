# Mecânica: gerar no Google Flow

**Atualizado em 07/11/2026.** Toda geração no Flow (imagem ou vídeo, com ou sem
imagem de referência) é feita pela skill **`flow-mcp`** (oficial, MCP `google-flow`) — leia o SKILL.md dela.
Só se ela falhar, a reserva é a skill `flow-video-playwright` (`~/.claude/skills/flow-video-playwright/scripts/flow.sh`).

Não use `agent-browser`, perfis `flow-enovalabs-pro*`, `flow-livre.sh` nem upload por
interceptação CDP: esses caminhos tomam "atividade incomum" do reCAPTCHA do Flow.
Conteúdo antigo deste arquivo: `~/.claude/skill-backups/` (não usar).
