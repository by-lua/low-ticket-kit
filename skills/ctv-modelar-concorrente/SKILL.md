---
name: ctv-modelar-concorrente
description: Modela criativos de concorrente (ou de oferta vizinha) pra nossa oferta no sistema LOW-TICKET — transcreve os vídeos, identifica o formato (POV, demonstração, expert, UGC…), entende por que converte e refaz trocando só a oferta. Também analisa criativos que a dona trouxer. Use para "modela os criativos dele", "transcreve os vídeos do anunciante", "olha esse anúncio e faz o nosso".
---

# ctv-modelar-concorrente — ideias a partir de criativo dos outros

**Entrada:** link da Biblioteca do anunciante (o original ou uma oferta vizinha — ex.: atividades pra idosos →
nossa de Alzheimer), ou vídeos/imagens que a dona mandou. `OFERTA.md` da nossa oferta.
**Saída:** seção "Do concorrente" em `criativos/IDEIAS-<AAAA-MM-DD>.md`.

## Passos
0. **Fontes de concorrente:** o original (Modelador) + os anunciantes **validados** da `pesquisa/VALIDACAO-*.md`
   (diretos e ofertas vizinhas, achados pelos termos PT/ES/EN).
1. **Já tem análise?** `criativos_analise` do `modelador-*.json` cobre os criativos do original — partir dela.
2. **Baixar** os vídeos/imagens em `/home/lua/Documentos/TRAMPO/PROJETOS-MIDIA/CRIATIVOS-CONCORRENTES/<SLUG>-<assunto>/`
   (mídia de terceiro fora da pasta sincronizada) + symlink em `pesquisa/referencia/`. Material da dona: salvar
   cru em `pesquisa/da-dona/` primeiro.
3. **Transcrever** cada vídeo: `yt-transcricao` (YouTube) ou whisper local (`watch` faz frames + transcrição).
4. **Por criativo, uma linha:** link · dias no ar · formato (catálogo `ctv-formatos`) · gancho literal ·
   desenvolvimento (mecanismo) · prova · CTA · cena (quem aparece, o que faz, gesto, cenário) · por que converte.
5. **Nossa versão:** mesmo formato e estrutura, trocando só a oferta (nosso produto, público e dor da `OFERTA.md`),
   no idioma do nosso mercado. Oferta muito parecida → modelagem quase 1 pra 1 da estrutura.
6. Imagem que a dona trouxe pra modelar: anexar a referência no GPT e refazer pra nossa oferta (mecânica:
   `modelagem-escalados` se o método Escalados estiver ativo; senão `criativo-ads-imagem`).

As ideias seguem pra `ctv-estudo-leva`.
