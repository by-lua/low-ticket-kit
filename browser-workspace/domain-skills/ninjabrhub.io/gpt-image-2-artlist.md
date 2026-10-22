# ninjabrhub.io — GPT Image 2 (motor Artlist) por API

**Verificado por execução em 2026-09-02.** É o motor a usar quando a imagem
**precisa ter texto correto** — capa de ebook, mockup com título, placa, rótulo.
Ferramenta: `GERADOR-AUDIO-HUB/gerar-gpt-image.py`.

## Qual GPT é qual (a confusão que custa tempo)

O Hub tem **dois** "GPT Image", e eles não são a mesma coisa:

| Onde | Modelo | Endpoint | Estado |
|---|---|---|---|
| **Artlist** | `gptimage2` | `artlist-proxy` | **funciona**, plano `unlimited` |
| Dzine | `gpt-image` | `dzine-img-proxy` | falha: `code 4712`, "unexpected error" no upstream |

E nenhum dos dois é o ChatGPT do perfil `gpt` (porta 9222) — aquele é conta
própria, com cota do Plus. O do Hub é conta do Hub, cota separada.
Na barra do Studio dá para distinguir pelo que aparece ao lado do modelo:
**Artlist** mostra `Resolução medium` + `Quantidade de imagens`;
**Dzine** mostra `Proporção` + `Resolução 2K` + `Style`.

## Chamada

```
POST https://bbwgequqwrsmbrkdmsxm.supabase.co/functions/v1/artlist-proxy
{"model":"gptimage2","prompt":"...","resolution":"medium","count":1}
  -> {"job_id":"0::01a0...","status":"generating","quota":{"plan":"unlimited"}}

GET  .../artlist-proxy?status=<job_id>   (job_id URL-encoded: "::" vira %3A%3A)
  -> quando pronto, a URL sai em cms-toolkit-artifacts.artlist.io
```

Mesmos headers do `useapi-proxy` (apikey + bearer + `x-client-info` + domain guard).
Leva ~1-2 min. `resolution`: `low` · `medium` · `high`.

**Não tem a fila de uma por vez** do google-flow/imagen-4 — o plano é ilimitado e
as gerações podem sair em sequência sem `generation_busy`.

## Texto na imagem: aqui pode pedir

Ao contrário do imagen-4 (que escreve em inglês e embaralhado), o GPT Image 2
acerta. Peça a capa escrita no prompt, palavra por palavra:

> The cover: top half solid emerald green with the words EQUILIBRIO SEGURO in
> large bold white uppercase sans-serif on two lines; bottom half white, with the
> characters 60+ very large in bold emerald green, and beneath it the single line
> 'Guías y ejercicios para prevenir caídas en casa' in small dark grey.
> Every word spelled exactly as given, in Spanish, crisp and perfectly legible.

Sai limpo e legível. Acentos: confirmar caso a caso — pedir explicitamente
("with the accented letters í exactly as written") ajuda.

## Descobrir endpoint novo do Hub

A UI resiste a clique programático (`el.click()` abre o menu em vez de enviar;
o clique real do `agent-browser click <ref>` funciona). Para achar o endpoint de
qualquer motor novo, grampeie o `fetch` e dispare uma geração pela UI:

```js
window.__cap=[];const of=window.fetch;
window.fetch=function(u,o){const url=(typeof u==='string')?u:(u&&u.url);
  if(/functions\/v1/.test(url||''))window.__cap.push({url,body:o&&String(o.body).slice(0,500)});
  return of.apply(this,arguments);};
// ... envia pela UI ...
JSON.stringify(window.__cap)
```

Aparecem o POST de criação, os `?status=` do poll e o `studio-persist` com a URL final.

## Proporção: não tem. Sai sempre 2048×2048

Testado em 2026-09-02: mandar `"aspect_ratio":"9:16"` e `"size":"1024x1792"` no body do
`artlist-proxy` **não dá erro e não muda nada** — o job volta normal e a imagem sai
quadrada, 2048×2048. `gerar-gpt-image.py` não expõe `--aspect` por isso mesmo.

Consequência para criativo 9:16: peça a foto com **composição vertical e sujeito
centralizado**, e feche o enquadramento depois. Duas saídas que funcionaram:

- recorte 9:16 do quadrado (`1152×2048`) quando o sujeito cabe na faixa central;
- quadrado 1080×1080 posicionado sobre uma cópia de si mesmo ampliada e borrada,
  com máscara de fade nas bordas — preenche o 9:16 inteiro sem cortar cabeça nem pés.

## Texto na arte: melhor não pedir, mesmo podendo

O GPT Image 2 acerta texto, mas para anúncio com preço a rota mais barata é gerar
**só a fotografia** (sem nenhuma letra, peça isso explicitamente no prompt) e compor
headline, preço e CTA por HTML/CSS renderizado em Chromium headless. Ganha-se: valor
travado sem risco de reescrita, safeline medida em px, e editar a headline depois é
mudar uma linha em vez de regerar. Papel/tela que aparece na mão do sujeito: peça
**em branco** e sobreponha o documento real por CSS.
