# Mundpay — criar produto digital (verificado 2026-09-25)
Perfil `mundpay` porta 9270, `agent-browser --session mundpay`. Rota: /products → "Criar produto" → /products/create-products (wizard 6 passos).
1 Produto digital · 2 nome, oferta, categoria (select role=option), descrição ≥40, reembolso (mín 7), Página de vendas, URL obrigado ·
3 email + WhatsApp de suporte (+55 default) · 4 código de 4 dígitos ENVIADO POR EMAIL ao suporte (precisa humano) ·
5 tipo Único + moeda (BRL/USD/EUR) + valor (máscara: digitar 990 = 9,90) · 6 entrega (Integração Externa = link da nossa área + email/senha demonstrativos p/ análise; senha obrigatória, ≥ ~10 chars).
ARMADILHAS: Página de vendas exige URL COM https:// (sem = "deve ser uma URL válida"; o erro só aparece no passo 2, no passo 6 só diz "1 erro(s)"). Voltar até o passo 2 pra ver o campo vermelho.
Selects = eval com PointerEvent pointerdown/up + click (igual receita Wiven). Produto nasce "Em análise". Moeda/idioma: não há campo de idioma, só moeda.
