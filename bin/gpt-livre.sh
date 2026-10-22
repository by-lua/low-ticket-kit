#!/bin/bash
# Devolve um perfil ChatGPT LIVRE. Mesma razao do hub-livre.sh: perfil em uso por
# outro agente nao da erro -- so fica lento, "Algo deu errado" e imagem que nunca
# chega, e voce culpa o ChatGPT em vez da disputa.
#
# REGRA DA DONA (11/10/2026): perfil novo do GPT tem que ser CADASTRADO aqui, senao
# o gpt-livre.sh nao enxerga. A lista NAO e uma copia do registry.conf de proposito:
# e a lista de perfis GPT LOGADOS (o registry tem o gpt e o gpt-play-1, que estao sem
# login e nunca servem). Para adicionar perfil novo:
#   1. ~/.claude/bin/browsers.sh add <perfil> <porta> https://chatgpt.com
#   2. a dona loga nele
#   3. acrescentar "<conta> <perfil> <porta>" no arquivo abaixo, na conta certa
# Contas com perfis da MESMA conta dividem cota de imagem.
#
# Conta pessoal (Dona) REMOVIDA em 11/10/2026 por ordem da dona.
# Backup dos perfis: ~/.agent-profiles/_removidos-gpt-pessoal-2026-10-11/
#   pessoal    1-4 = gpt-conta, -2, -3, -4   (conta dona.assist)
#   secundaria 1-4 = gpt-conta, -2, -3, -4   (conta conta-secundaria)
#
# Uso:  S=$(~/.claude/bin/gpt-livre.sh mx)
#       GPT_CONTA=secundaria ~/.claude/bin/gpt-livre.sh mx
# Cota acabou (card "Voce atingiu o limite... Tente de novo as HH:MM"):
#       ~/.claude/bin/gpt-livre.sh --esgotou secundaria [HH:MM]
#   grava a marca; os proximos pedidos pulam essa conta ate o horario (sem HH:MM = 4h).
LANE="${1:-auto}"
MARCA_DIR="$HOME/.agent-profiles/_gpt-cota"
LISTA="$HOME/.claude/bin/gpt-contas.lst"
mkdir -p "$MARCA_DIR"

if [ "$1" = "--esgotou" ]; then
  conta="$2"; ate="$3"
  if [ -n "$ate" ]; then fim=$(date -d "$ate" +%s); [ "$fim" -le "$(date +%s)" ] && fim=$((fim+86400))
  else fim=$(date +%s); fim=$(( fim + 4*3600 )); fi
  echo "$fim" > "$MARCA_DIR/$conta"
  echo "conta $conta marcada sem cota ate $(date -d @$fim +%H:%M)" >&2; exit 0
fi

esgotada(){ local f="$MARCA_DIR/$1"; [ -f "$f" ] && [ "$(cat "$f")" -gt "$(date +%s)" ]; }

ocupado(){ # >1 aba de conversa /c/ = alguem trabalhando ali
  local n=$(curl -s "http://127.0.0.1:$1/json/list" 2>/dev/null \
   | python3 -c "import sys,json;print(sum(1 for t in json.load(sys.stdin) if t.get('type')=='page' and 'chatgpt.com/c/' in t.get('url','')))" 2>/dev/null)
  [ "${n:-0}" -gt 1 ]
}

[ -f "$LISTA" ] || { echo "FALTA $LISTA (cadastro de contas GPT) -- ver regra no topo do script" >&2; exit 2; }

# Sem agent-browser no PATH o lane.sh falha em todo perfil: o loop abria os 4 Chromium
# um a um e terminava em "SEM PERFIL" (22/10, servico systemd subindo antes do login).
# Checa antes de abrir qualquer navegador.
command -v agent-browser >/dev/null 2>&1 \
  || { echo "SEM agent-browser no PATH ($PATH) -- nao abro perfil nenhum" >&2; exit 3; }

# contas na ordem do arquivo; GPT_CONTA=<conta> comeca por ela
ORDEM=$(awk '$1 !~ /^#/ && NF>=3 {print $1}' "$LISTA" | sort -u)
if [ -n "$GPT_CONTA" ]; then ORDEM=$(printf '%s\n' "$GPT_CONTA" $ORDEM | sort -u -k1,1 --stable 2>/dev/null | awk -v p="$GPT_CONTA" 'NR==1{next}1{print}END{print p}'); fi

for conta in $ORDEM; do
  if esgotada "$conta"; then echo "pulando conta $conta (sem cota ate $(date -d @$(cat "$MARCA_DIR/$conta") +%H:%M))" >&2; continue; fi
  for par in $(awk -v c="$conta" '$1 !~ /^#/ && NF>=3 && $1==c{print $2":"$3}' "$LISTA"); do
    perfil=${par%%:*}; porta=${par##*:}
    estado=$(~/.claude/bin/browsers.sh status 2>/dev/null | awk -v p="$perfil" '$1==p{print $3}')
    [ -z "$estado" ] && continue
    if [ "$estado" = "ATIVA" ] && ocupado "$porta"; then continue; fi
    [ "$estado" = "ATIVA" ] || ~/.claude/bin/browsers.sh "$perfil" >/dev/null 2>&1
    sleep 5
    # navegador do perfil tem que responder na porta; senao o agent-browser abre um
    # Chrome headless sem login por comando (21/10: derrubou a sessao do GNOME 2x)
    curl -s --max-time 3 "http://127.0.0.1:$porta/json/version" >/dev/null 2>&1 \
      || { echo "perfil $perfil nao respondeu na porta $porta -- pulando" >&2; continue; }
    ~/.claude/bin/lane.sh take "$perfil" "$LANE" >/dev/null 2>&1 \
      || { echo "perfil $perfil: lane.sh take falhou -- pulando" >&2; continue; }
    S="$perfil-$LANE"
    agent-browser --session "$S" navigate "https://chatgpt.com/" >/dev/null 2>&1; sleep 4
    # sem login nao adianta: a conta do ChatGPT e pessoal e nao tem credencial salva
    if echo "(()=>/Entrar|Log in|Sign up/.test((document.body.innerText||'').slice(0,400))?1:0)()" \
       | agent-browser --session "$S" eval --stdin 2>/dev/null | grep -q 1; then
      echo "perfil $perfil ($conta) DESLOGADO -- pedir login a dona" >&2; continue; fi
    echo "conta: $conta | perfil: $perfil" >&2
    echo "$S"; exit 0
  done
done
echo "SEM PERFIL GPT LIVRE (contas sem cota, ocupadas ou deslogadas)" >&2; exit 1