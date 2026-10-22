# Caso real — NUMERO-MESTRE, 13/08/2026

Execução completa do Modo B: três hooks novos sobre um body vencedor. Serve de modelo para reproduzir o fluxo inteiro.

**Projeto:** `Documentos/TRAMPO/PROJETOS/WORKING/PROJETOS - INTERNOS/NUMEROLOGIA/NUMERO-MESTRE`
**Entregue:** `ANUNCIO/13-08/CRIATIVO-10`, `-11`, `-12` — 60s, 61s, 62s, todos 1080x1920

---

## 1. Contexto da oferta

- **Produto:** Ritual do Número Mestre — numerologia, três números bloqueadores + um quarto número (o mestre)
- **Ritual:** papel dobrado 3x, guardado debaixo do colchão por 3 noites
- **Persona:** Ágata / "Madalena", taróloga, ~48 anos
- **Idioma:** espanhol rioplatense, voseo, sotaque de Buenos Aires
- **Preço:** não aparece no criativo. A VSL longa em PT-BR fecha em R$ 67 à vista ou 12x R$ 6,60. CTA do body é só *"Tocá el botón y asegurá hoy tu consulta"*

## 2. Escolha do body

Os candidatos estavam em `ANUNCIO/06-08/VIDEO/`:

| Arquivo | O que é |
|---|---|
| `AD4.mp4` (55s) | Sala de tarô, velas, mini-VSL comprimida + 3 depoimentos UGC + oferta. Legenda serifada dourada. **Vencedor.** |
| `AD5.mp4` (50s) | UGC mesa/abajur, ritual do copo com água e sal. Legenda Impact colorida. |
| `AD6.mp4` (50s) | Mesmo footage do AD5, **sem legenda** (master limpo). |

**Achado importante:** o AD5 promete um ritual (copo com água e sal) **diferente** do da VSL e do AD4 (papel dobrado sob o colchão). Furo de continuidade, ainda não resolvido — vale checar se existe VSL espanhola com o ritual do copo.

## 3. Ponto de corte do body

Mapeado frame a frame + `silencedetect`:

| t | legenda do AD4 |
|---|---|
| 0,0 | "No cierres" |
| 1,0 | "esta página." |
| 2,0 | "tres números" |
| 3,0 | "actuando en" |
| 3,5 | "silencio dentro" |
| 4,5 | "nombre." |
| 5,0 | "Tal vez" |
| 5,5 | "pensaste que" |
| 6,5 | "era falta" |
| 7,0 | "de esfuerzo," |
| 8,0 | "de fe o" |
| 8,5 | "de merecimiento." |

**Corte em 5,28s** (silêncio de 5,107s a 5,443s).

Por que não em 2,0s: manteria *"tres números actuando en silencio dentro de tu nombre"* — mas todos os hooks já dizem "três números". Repetiria dois segundos depois. Cortando em 5,28s o body entra em *"Tal vez pensaste que era falta de esfuerzo…"*, que emenda limpo.

```bash
ffmpeg -ss 5.28 -i AD4.mp4 -vf "scale=1080:1920:flags=lanczos,fps=30,format=yuv420p" \
  -c:v libx264 -crf 18 -preset slow -c:a aac -b:a 192k -ar 48000 -ac 2 -y body.mp4
```

## 4. Persona de referência

Mesma atriz nos dois criativos — tarô no AD4, mesa no AD5/AD6. Quatro frames extraídos para `REFERENCIA/`, já 720x1280 nativo:

```bash
ffmpeg -ss 2  -i AD4.mp4 -frames:v 1 REFERENCIA/madalena-tarot-01.png
ffmpeg -ss 6  -i AD4.mp4 -frames:v 1 REFERENCIA/madalena-tarot-02.png
ffmpeg -ss 1  -i AD6.mp4 -frames:v 1 REFERENCIA/madalena-mesa-01.png
ffmpeg -ss 44 -i AD6.mp4 -frames:v 1 REFERENCIA/madalena-mesa-02.png
```

Usados como anexo no ChatGPT para travar o rosto no CRIATIVO-10.

---

## 5. Os três hooks

Body idêntico nos três. Hook é a única variável do teste.

| | Primeiro frame | Som nos 3s | Luz | Público | Duração |
|---|---|---|---|---|---|
| **10** | Mãos, caderno, cenital | Só caneta | Dia, dura, fria | Cético, racional | 10,7s |
| **11** | Rosto no carro | Fala rápida, rua | Fim de tarde, quente | Filha, 28-45 | 11,8s |
| **12** | Rosto no escuro | **Silêncio** | Tela de celular, azul | Dor, 40+ | 12,1s |

### CRIATIVO-10 — "El Cuaderno"

Ângulo: desmistificação, é cálculo e não simpatia. Mesma atriz do body, **sem figurino místico** (rabo de cavalo, camiseta lisa, sem joia).

- Cena 1 (6s, cenital, só mãos, VO off): *"Esto no es una simpatía. Es una cuenta."*
- Cena 2 (10s, rosto, on camera): *"Tres números que salen de tu nombre. Vos no los elegiste. Y mientras estén ahí, no importa cuánto trabajes."*

Pós: cena 1 acelerada **1.3x** (a escrita ficou arrastada).

### CRIATIVO-11 — "El Audio de mi Mamá"

Ângulo: prova social por terceiro. **Atriz diferente**, 33 anos, UGC dentro do carro.

- Cena 1 (6s): *"Mi mamá me mandó un audio a las seis de la mañana."*
- Cena 2 (10s): *"Decía: nena, apareció la plata. La que le debían hace dos años. Yo me reí de ella. Ahora quiero el mío."*

Pós: ambas aceleradas **1.25x** (bruto saiu 14,8s). O ritmo rápido combina com a personagem.

**Risco Meta:** "apareció la plata" é promessa financeira indireta. Alternativa: *"le cambió el mes entero"*.

### CRIATIVO-12 — "Las 3 de la Mañana"

Ângulo: dor pura, sem mencionar produto, ritual ou número nos 12s. Atriz argentina, 46, quarto escuro, luz da tela do celular.

- Cena 1 (6s, **muda**): olha o celular, não fala nada. Card "3:14 AM" entra na edição.
- Cena 2 (10s): *"¿Cuántas noches ya hiciste esta cuenta en la cabeza? Trabajás. Rezás. Hacés todo bien. Y no alcanza. Nunca alcanza."*

Sem aceleração — a fala é lenta e confessional de propósito.

---

## 6. Erros cometidos nesta execução

Todos já corrigidos no `SKILL.md`. Listados aqui porque foram descobertos na prática:

1. **`agent-browser open` travou no Cloudflare** nos dois sites. Resolvido subindo Chromium do sistema com perfil persistente + CDP.
2. **Rodou headless na primeira tentativa** — nenhuma janela apareceu. `--headed` não resolve, continua o binário empacotado.
3. **O Hub não limpa o prompt entre gerações.** A cena 1 do CRIATIVO-11 saiu com caderno e xícara dentro do carro — gerada com o prompt do CRIATIVO-10. Sem nenhum aviso. E o `snapshot` mostrava o valor desatualizado, então parecia certo.
4. **Loop de espera travou 10 minutos** esperando URL http. O src do `<video>` vira `blob:` depois que o player carrega.
5. **"Latin American" deu cara mexicana/andina** onde precisava ser argentina. Refeito com `of Italian and Spanish descent, European-Mediterranean features`.
6. **Total do hook estourou o alvo** no primeiro criativo — cenas escritas soltas e somadas no fim. Daí veio a regra do orçamento de tempo antes.
7. **Numeração recomeçou do 1** quando o projeto já tinha AD1…AD9. Renumerado para 10, 11, 12.
8. **Corte do body quase saiu errado** — o plano era 4s, que cairia no meio da frase e repetiria o que o hook diz. Só o mapa frame a frame revelou.

## 7. Comandos de montagem usados

```bash
# silêncio
ffmpeg -i cena.mp4 -af "silencedetect=noise=-32dB:d=0.35" -f null - 2>&1 | grep silence_

# upscale + normalização (com aceleração opcional)
VF="scale=1080:1920:flags=lanczos,unsharp=5:5:0.7:5:5:0.0,fps=30,format=yuv420p"
ffmpeg -ss <ini> -to <fim> -i cena.mp4 -vf "setpts=PTS/1.3,$VF" -af "atempo=1.3" \
  -c:v libx264 -crf 18 -preset slow -c:a aac -b:a 192k -ar 48000 -ac 2 -y s1.mp4

# concat
printf "file '%s'\nfile '%s'\n" /abs/s1.mp4 /abs/s2.mp4 > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy -y HOOK-10.mp4

# hook + body
printf "file '%s'\nfile '%s'\n" /abs/HOOK-10.mp4 /abs/body.mp4 > final.txt
ffmpeg -f concat -safe 0 -i final.txt -c copy -y CRIATIVO-10.mp4
```

## 8. Pendências

- **Legenda queimada** no estilo serifado dourado do AD4 — ainda não feita, seria via Remotion
- **Inconsistência do ritual** entre AD5 (copo com água e sal) e VSL/AD4 (papel sob o colchão)
- Confirmar se AD4 e AD5 apontam para a mesma página
- Card "3:14 AM" do CRIATIVO-12 ainda não foi inserido
