# chatgpt.com — upload input[type=file] quebrado, fix = paste sintético

Validado 2026-09-27 (oferta mapas-visuais-eletrotecnia, perfis gpt-conta,
-2, -3, todos os 3 reproduziram).

## Sintoma
`agent-browser upload "input[type=file]" arquivo.ext` — o chip aparece mas
sempre "Falha no upload" (vermelho), reproduzível até com .txt de 10 bytes,
**zero requisição de rede** a `/backend-api/files` (client rejeita antes de
qualquer fetch/XHR). Acontece em Chat mode E Work mode, em qualquer conta,
mesmo perfil recém-aberto sem histórico. Não é cota, não é tamanho de arquivo,
não é caminho em /tmp.

## Fix: ClipboardEvent('paste') sintético com DataTransfer
CDP `DOM.setFileInputFiles` (o que `upload` usa por baixo) está sendo
rejeitado por essa build do ChatGPT. Um evento de paste sintético com
DataTransfer contendo File objects FUNCIONA — dá 200 em
`/backend-api/files`, PUT em blob storage, `process_upload_stream` 200.

```js
(async () => {
  const items = [{name, mime, b64}, ...]; // ler cada arquivo local em Python/bash, base64
  const el = document.querySelector('#prompt-textarea, [contenteditable=true]');
  function b64ToBlob(b64, mime) {
    const bin = atob(b64);
    const arr = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i);
    return new Blob([arr], {type: mime});
  }
  const dt = new DataTransfer();
  for (const it of items) {
    const file = new File([b64ToBlob(it.b64, it.mime)], it.name, {type: it.mime});
    dt.items.add(file);
  }
  const evt = new ClipboardEvent('paste', {bubbles: true, cancelable: true, clipboardData: dt});
  el.dispatchEvent(evt);
})()
```

Envie via `cat script.js | agent-browser --session <S> eval --stdin` (não como
arg — payload base64 de várias imagens facilmente passa de 1-5MB de texto).
Testado com lote de 10 imagens (~300-500KB jpg cada) + html + md = 12 arquivos
num só paste, sem falha.

## Gerador usado (Python)
Ler cada arquivo do disco, base64, montar lista `{name, mime, b64}`, injetar
no template JS acima via `json.dumps`, escrever em arquivo `.js`, mandar por
stdin. `mime`: image/jpeg pra .jpg, text/html pra .html, text/markdown pra .md.

## Ordem de diagnóstico que levou até aqui
1. upload direto (`input[type=file]`) com arquivo em `/tmp` → falha, 0 network.
2. Mesmo arquivo movido pra dentro do projeto (fora de /tmp) → falha igual.
3. Trocado de conta/perfil (3 contas diferentes, uma delas nunca usada nesta
   sessão) → falha igual em todas. Não é conta, é o método de upload.
4. `paste` sintético com ClipboardEvent + DataTransfer → funcionou de cara.
