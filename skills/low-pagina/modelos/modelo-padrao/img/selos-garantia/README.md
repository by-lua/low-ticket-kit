# Banco de selos de garantia (dourado, GPT, fundo transparente)

Padrão da dona (10/11/2026): medalha dourada com louros, anel preto, 5 estrelas, fita. Sempre gerado no GPT, nunca CSS/SVG.

| Arquivo | Texto |
|---|---|
| `selo-es-7.png` | GARANTÍA · 7 DÍAS · INCONDICIONAL · DEVOLUCIÓN DEL 100 % |
| `selo-es-15.png` | idem, 15 DÍAS |
| `selo-en-15.png` | GUARANTEE · 15 DAYS · UNCONDITIONAL · 100% MONEY-BACK |
| `selo-fr-15.png` | GARANTIE · 15 JOURS · INCONDITIONNELLE · SATISFAIT OU REMBOURSÉ |
| `selo-pt-7.png` | GARANTIA · 7 DIAS · INCONDICIONAL · DEVOLUÇÃO DE 100 % |

- Usar direto na página (`<img>` webp ~700px). Combinação faltando (outro idioma/prazo) = **criar seguindo o modelo**: copiar `bruto/es-15.txt`, trocar texto, `GPT_S=<sessão> GPT_TAB=<lane> ./gerar-banco.sh` (anexa `bruto/ref-padrao.jpg`), depois `./recortar-fundo.sh bruto/<id>.png selo-<id>.png`, conferir texto/acento no `contact-sheet.jpg` e acrescentar a linha acima.
- `bruto/` = saída do GPT com fundo branco (fonte para recortar de novo).
- Modelo Padrão e toda oferta nova usam este banco.
