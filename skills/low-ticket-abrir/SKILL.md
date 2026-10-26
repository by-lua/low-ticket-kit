---
name: low-ticket-abrir
description: >
  /abrir do portfólio LOW-TICKET (padrão MazyOS): carrega a memória INTEIRA que importa pra
  tarefa — negócio, oferta, regras da dona, memória de sessões, gates e skills obrigatórias — por
  um script, e devolve o RECIBO antes de qualquer ação. Use SEMPRE no começo de qualquer trabalho
  low ticket e ao retomar: "abrir", "/abrir", "retomar", "onde paramos", "começar o dia", "vou
  mexer na oferta X", "vamos fazer criativo/página/checkout/entrega de X". Nada começa sem o recibo.
---

# /low-ticket-abrir — abertura de sessão (padrão MazyOS)

O MazyOS nunca se desvia porque a memória dele cabe inteira no contexto (3 arquivos, < 1 KB).
A nossa não cabe: CLAUDE.md 25 KB, `_memoria/` 225 KB, STATUS de oferta até 265 KB. Agente que
"lê tudo" passa o olho e pula — foi assim que o Tarot AR saiu com carrossel sem texto (25/10).
Por isso aqui **quem lê é o script**: ele junta o recorte certo (negócio + oferta + tipo de
tarefa), roda os gates e manda as skills. O agente só obedece o que sai.

## Como chamar

```
/low-ticket-abrir                                  → onde paramos (negócio inteiro)
/low-ticket-abrir <oferta>                         → estado da oferta
/low-ticket-abrir <oferta> — <tarefa>              → estado + rota da tarefa (o normal)
```
Oferta aceita apelido ("tarot ar", "jiu", "atlas"). Ambíguo → o script lista e para.

## Workflow (sem pular passo)

1. **Rodar o script** — a saída É a leitura; não substitua por leitura própria:
   ```bash
   python3 ~/.claude/skills/low-ticket-abrir/scripts/abrir.py "<oferta>" "<tarefa>"
   ```
   Saída grande? Ler INTEIRA mesmo assim (é o recorte, não o arquivo todo). Se truncar, ler o
   arquivo salvo por partes. `--ofertas` lista os slugs.

2. **Carregar TODAS as skills** da seção "SKILLS OBRIGATÓRIAS" pelo Skill tool, uma por uma,
   antes de abrir qualquer arquivo de produção. A lista sai da tabela do `CLAUDE.md` da raiz
   (fonte única). Skill com `?` = invocar pelo ID mesmo assim.

3. **Gates:** o script já rodou. `GATE BLOQUEADO` = a tarefa não começa; dizer à dona o que falta.
   "plano com pendência" = pode corrigir peça, mas avisar.

4. **Devolver o RECIBO** (bloco do fim da saída) preenchido, curto, em português, pra dona.
   Ele é a prova de que leu: fase, o que vendemos / o que NÃO é, 3-5 regras da dona que valem
   aqui **com o arquivo de origem**, última análise de tráfego, gates, skills carregadas, avisos
   e próximo passo. Sem recibo, não age.

5. **Avisos** (oferta sem CLAUDE.md, arquivo faltando, STATUS velho) entram no recibo e viram
   pendência — não se ignora aviso.

6. **SUGESTÃO DE ALTERAÇÃO** (bloco que o script imprime em oferta já existente): ficha com
   exercício/pôster/folha de imprimir cujo texto não traz a página `w`, ou página `w` feita por
   código (Pillow/HTML). Levar ao recibo como sugestão e **oferecer** a correção à dona (texto da
   `w` primeiro, depois imagem GPT 1 por mensagem). Não corrigir sem OK. Oferta nova já nasce
   certa pela regra de `criacao-low-ticket-mvt/references/PAGINAS-DE-ATIVIDADE.md`.

## Durante e depois (o resto do ciclo MazyOS)

- Correção da dona ("na verdade é assim", "não faz mais isso", "sempre que…") → perguntar
  **"quer que eu salve isso pra não precisar repetir?"** e salvar no lugar certo
  (negócio → `_memoria/`, oferta → "Memória da oferta" do CLAUDE.md dela, mecânica → a skill).
- **Agente nunca escreve exceção a regra da dona numa skill pra justificar a própria peça**
  (caso Tarot AR 25/10: exceção "peça 9 sem texto" + `--sem-texto` no gate). Exceção só com
  ordem explícita da dona, com data e citação.
- Ao terminar: `low-ticket-salvar` (STATUS da oferta + linha da raiz + memória). Varredura
  geral quando houver dúvida: `low-ticket-atualizar`.

## Manutenção do script

- Tipo de tarefa novo, palavra-chave, arquivo extra ou gate por tipo → `TIPOS` / `EXTRAS` em
  `scripts/abrir.py`. Skills por tarefa NÃO moram aqui: editar a tabela do `CLAUDE.md` da raiz.
- Teste rápido depois de mexer: `abrir.py luciola-mapatarot-ar "refazer carrossel 9"` e
  `abrir.py jiujitsu "checkout bump"` — saída entre 20 e 60 KB, sem erro de Python.
