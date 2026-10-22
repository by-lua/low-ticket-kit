> **ATUALIZADO 2026-10-02 (verificado):** o composer agora é `div.ProseMirror` (não existe mais `#prompt-textarea`) e o botão de envio é `button[aria-label="Enviar"]` (não "Enviar prompt"). Ele só aparece com texto no composer. Antes de digitar, foque com `document.querySelector(".ProseMirror").focus()` e use `keyboard inserttext`. Atenção: `gpt-livre.sh <lane>` devolveu `gpt-conta<lane>`, que caiu no MESMO browser 9252 já em uso por outro agente. Confira se `.ProseMirror` está vazio antes de digitar; se não estiver, o perfil está ocupado. Nesse caso, suba `-2`/`-3`/`-4`.

# chatgpt.com — gerar imagem com referência anexada

Validado por execução em 2026-08-30 (leva AstroDicas estáticos, peça 1).
Perfil `gpt` / porta 9222.

## O que quebra e por quê

1. **`[data-testid="send-button"]` NÃO EXISTE MAIS.** O botão de envio é
   `button[aria-label="Enviar prompt"]` (classe `composer-submit-btn`).
   Script que procura o testid antigo digita o prompt, tenta enviar 3x e
   falha com o campo ainda cheio — sintoma: `FAIL: nao enviou (campo=NNNN)`.

2. **Coordenada de clique: CSS px ≠ px da viewport CDP.** Nessa janela a
   escala é ~1.22 (rect y=672 → clique real em y=844). `Input.dispatchMouseEvent`
   na coordenada do `getBoundingClientRect` erra o botão em silêncio: o clique
   "funciona", nada acontece. Confirme por `Page.captureScreenshot` e leia a
   posição real na imagem antes de culpar o seletor.

3. **Anexo que não subiu tem thumbnail VAZIO.** Sinal de upload concluído é
   uma `<img>` `600x600` com src em `chatgpt.com/backend-api/...`. Só o
   `button[aria-label^="Remover ficheiro"]` existir não prova nada — ele
   aparece antes do upload terminar.

## Receita que funciona (browser-harness, CDP cru)

```python
# 1. anexar — DOM.setFileInputFiles no PRIMEIRO input[type=file]
doc = cdp("DOM.getDocument", depth=-1, pierce=True)   # kwargs, NÃO dict
# ...achar nodeId com attributes type=file, pegar o primeiro
cdp("DOM.setFileInputFiles", files=[REF], nodeId=nid)

# 2. CONFIRMAR o upload (não pule)
js("[...document.querySelectorAll('img')].some(i=>i.naturalWidth===600)")

# 3. prompt — Input.insertText, nunca fill
js("document.querySelector('#prompt-textarea').innerHTML='';document.querySelector('#prompt-textarea').focus()")
cdp("Input.insertText", text=prompt)

# 4. enviar — clique na coordenada REAL (confira por screenshot)
for ev in ("mouseMoved","mousePressed","mouseReleased"):
    cdp("Input.dispatchMouseEvent", type=ev, x=X, y=Y, button="left", clickCount=1)
# sucesso = #prompt-textarea.innerText.length == 0

# 5. baixar — fetch dentro da página, Runtime.evaluate com awaitPromise=True
#    (js() do harness não aceita await_promise)
```

Enter no textarea NÃO envia (testado, keyDown/keyUp Enter: nada).

## Tempo real medido
anexo 7s · envio 6s · **geração 40s** · download 3s. Acima de 2 min: é o seu loop.

## Saída
Imagem 9:16 sai `941x1672`. Converter pra webp: `ffmpeg -i x.png -c:v libwebp -quality 90 x.webp`
(2.0 MB → 198 KB). `cwebp` NÃO está instalado nesta máquina.
