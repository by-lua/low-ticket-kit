# ChatGPT: sinais de DOM que mudaram (verificado 02/10/2026, conta gpt-conta)

Script completo e testado: `OFERTAS/mapa-do-taro/pagina-mundpay/scripts/traduzir-pagina-es.sh`
(anexa imagem, manda prompt, espera, baixa pelo navegador, valida com PIL, só grava se válido).

- **Anexo pronto:** a prévia NÃO é mais `<img src=backend-api>`. É `blob:` com `alt="Anexo do usuário"`.
  Sinal confiável: existe `[aria-label="Remover <nome-do-arquivo>"]`, depois espere ~6s.
- **Imagem gerada:** `img` com `alt` "Imagem 1 gerada" (UI pt-BR), src `blob:`. Filtre por
  `/gerada|generated|generada/i.test(img.alt)`. NUNCA pegue "a maior img nova": o anexo do usuário
  também é img grande e entra no diff (já baixamos a referência achando que era o resultado).
- **Gerando:** texto "Quase pronto" + percentual ("88%") no main. Pronto = img gerada presente e sem esse texto.
- **Enviar:** o botão fica desabilitado alguns segundos depois do anexo; tente o clique em loop (até ~60s).
- **Download:** `fetch(blobSrc)` dentro da página → base64 via eval → decodificar e validar com PIL.
  Nunca gravar sem validar: um download quebrado já sobrescreveu página boa com `{"error": "Invalid URL"}`.
- Cota de upload é por conta: esgotou em gpt-conta, use gpt-conta (e vice-versa). Hub desativado.
