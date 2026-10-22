
## Upload de anexo falha 100% depois de esgotar cota diária (28/09/2026)

Sintoma: "Falha no upload" no chip do composer para QUALQUER arquivo, QUALQUER
formato (PNG/JPG), QUALQUER tamanho (130KB-2MB), 1 anexo ou vários, chat novo
a cada tentativa, mesmo com cooldown de 2-3min entre tentativas. Consistente
por ~30min de teste (15+ tentativas, conta gpt-conta*).

**Controle que isola a causa:** no MESMO chat, na MESMA hora:
- anexo + "describe this image" (sem gerar) → sobe liso, lê o arquivo certo.
- texto→imagem SEM nenhum anexo → gera normal.
- anexo + geração de imagem → falha sempre.

Ou seja: não é rede, não é seletor quebrado, não é cota de IMAGEM (o card
nativo de limite de imagem nunca apareceu). É cota DIÁRIA DE UPLOAD DE
ARQUIVO da conta — mesma conta tinha subido anexo de manhã sem problema.

**Não adianta:** trocar tamanho/formato do arquivo, esperar 2-3min, criar
chat novo, tentar 1 anexo em vez de vários. Nada disso muda o resultado
quando a cota diária de upload já esgotou.

**Saída (atualizado 02/10/2026):** a cota é POR CONTA — troque para a OUTRA conta de GPT
(`gpt-conta*` ↔ `gpt-conta*`, subir com `~/.claude/bin/browsers.sh <perfil>`, conferir
login em /api/auth/session). Hub NÃO é fallback: está sem cota e desativado. Antigo texto: NinjaBR Hub
(Nano Banana/GPT image) com anexo, ou GPT texto→imagem sem anexo pra peças
que não dependem de mostrar conteúdo aprovado nosso (ex.: capa sem página
interna). Peça que PRECISA de anexo (mostrar nossas páginas/cartas reais) e
nenhum motor aceita → parar e reportar, não gerar genérico.
