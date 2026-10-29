# Auditoria de irresistibilidade — melhorar a NOSSA oferta (não a do concorrente)

**Criado em:** 30/10/2026 (dona: "tem muitas coisas antes do criativo, com criação melhor da oferta
mais irresistível"). Diferença do resto do pacote de modelagem: `4-alavancas.md` e `virar-o-lead.md`
já existiam pra **avaliar/modelar oferta de concorrente**; isso aqui é o MESMO instrumento virado pra
**dentro** — auditar e melhorar a NOSSA oferta já publicada, antes de planejar qualquer leva de
criativo nela. Criativo bom não salva oferta fraca; esse passo vem antes.

## Quando rodar

- **Antes de qualquer leva de criativo** numa oferta que já tem página no ar (ponte com `criativo-ads`
  Gate 0 — ler a oferta inclui isso).
- Na **T11 Obra de Arte** de oferta nova, depois de montar os 8 elementos — audita o que acabou de
  nascer antes de considerar pronto (`mvt-obra-100k`).
- Quando performance cair sem explicação de criativo/tráfego (gate de diagnóstico, antes de culpar
  anúncio — às vezes é a oferta que ficou fraca, não o anúncio).

## Passo a passo

1. **Vira o lead na NOSSA própria página** (`virar-o-lead.md`, checklist de extração completo: abre a
   página de verdade, do topo ao rodapé, até o checkout — nunca de memória). Responde as 6 perguntas
   fixas (o que fisga, o que desconfia, dúvida sem resposta, objeção de desistência, o que falta pra
   confiar, momento exato de desistir) como se fosse o comprador real, cético.
2. **Nota 0-10 por alavanca** (`4-alavancas.md`) na oferta ATUAL — não na ideal, na que está no ar
   hoje. Cita o que sustenta cada nota.
3. **Aponta a alavanca mais fraca** — é o alvo. Em oferta low ticket já madura, costuma ser
   PROBABILIDADE (falta prova/garantia/demonstração) ou ESFORÇO (entregável confuso, difícil de
   começar a usar), raramente TRANSFORMAÇÃO (a promessa já existe).
4. **Melhora concreta, não genérica — e cobre o FUNIL INTEIRO, não só a página.** A auditoria aponta
   item real em qualquer peça: **produto** (entregável), **bônus**, **order bump**, **upsell/downsell**,
   não só headline/copy. Pra cada alavanca fraca, decide o item real que sobe a nota:
   - Transformação fraca → reescreve a promessa/headline; ou o **produto principal** entrega pouco
     pra promessa — mexe no entregável, não só no texto.
   - Probabilidade fraca → prova social real (nunca inventada, regra `prova-social-so-real`),
     garantia mais forte, demonstração visual do entregável; ou falta **bônus que reduz risco**
     (ex.: suporte, checklist de erro comum).
   - Tempo fraco → reduz passo até o primeiro resultado (ex.: "usa pronto" em vez de "monta você
     mesmo"), reordena a entrega; **order bump/upsell errado** pode estar adiando o resultado em vez
     de acelerar (bump que exige mais trabalho do cliente piora esta alavanca, não ajuda).
   - Esforço fraco → simplifica onboarding, MVP mais claro, reduz decisão que o cliente precisa
     tomar; **bump/upsell com overlap do principal** (mesma dor, outro nome) aumenta esforço de
     decisão sem agregar — corta ou funde (ver `PECAS-DO-FUNIL.md` § matriz anti-overlap).
   - **Pergunta de cada peça do funil, sempre:** essa peça (bônus/bump/upsell) resolve a PRÓXIMA dor
     do cliente depois da anterior, ou repete? Repetir é a falha mais comum encontrada em auditoria
     (regra já fixada em `PECAS-DO-FUNIL.md` § Regra da PRÓXIMA dor — esta auditoria é onde ela se
     aplica na prática, numa oferta já no ar).
5. **Tabela antes × depois** (mesma alavanca, nota antiga × nota proposta) — só sobe nota se a
   melhora for real e executável, nunca otimismo.
6. **Só depois disso planeja criativo.** O criativo da leva seguinte já nasce atacando a alavanca que
   subiu — não é coincidência, é o que a auditoria apontou.

## Diferença do resto do pacote (não duplicar, é outra direção)

| Ferramenta | Direção | Quando |
|---|---|---|
| `virar-o-lead.md` + `4-alavancas.md` em **concorrente** | olha pra FORA, acha brecha pra ganhar dele | mineração/modelagem (`mvt-minerar`, `mvt-modelar`) |
| **Esta auditoria** | olha pra DENTRO, melhora a NOSSA oferta | antes de leva de criativo, em T11 Obra, ou diagnóstico de queda |
| `mvt-auditar` (gate.py) | processo/trilha completos (passos pulados) | antes de Parada, retomar rodada |

## Onde isso se conecta

- `criativo-ads` Gate 0 — rodar esta auditoria ANTES do plano da leva quando a oferta já tem página
  no ar há tempo e nunca passou por isso.
- `mvt-obra-100k` — passo extra depois de montar os 8 elementos.
- Registro: `OFERTAS/<slug>/pesquisa/auditoria-irresistibilidade-<data>.md` (virar-o-lead + tabela
  antes×depois + melhorias decididas, com data).
