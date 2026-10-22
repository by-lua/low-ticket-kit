# Crie um SaaS em 30 minutos

## Criando um SaaS em 30 minutos

**Aula:** 244

- Objetivo: criar SaaS funcional prototipo mínimo 30min (não produto final polido)
- Exemplo: SermonFlix (gerenciador sermões: login, criar, listar, visualizar, editar, deletar, relatórios, exportar)
- Hospedagem: Hostinger Premium (permite 25 sites mesma conta)
- Plano: Premium 1 mês R$45 (teste rápido) ou 12 meses R$23 mês (ganha domínio grátis)
- Domínio: gerar nome único ChatGPT (prompt fornecido) → pesquisar disponibilidade
- Exemplo nomes gerados: púlpito + tech = púlpito, verbo + logos = verbos
- Subdomínio: criar app.seudominio.com.br preferência (ao invés domínio principal)
- Bank de dados: criar manualmente (nome, usuário, senha, acesso phpMyAdmin)
- Guardar credenciais: arquivo texto com banco|usuário|senha|URL|nome-site
- Prompt ChatGPT: "Cria app PHP+SQL nome SermonFlix. Objetivos: criar/listar/visualizar sermão. Login. Usuário vê apenas seus. Design responsivo elegante. Fonte Inter. Cores azul branco, texto preto chumbo. Menu vertical"
- Chat Cloud IA: colar prompt → aguarda gerando files (SQL, config.php, style.css, header.php, footer.php, script.js, login.php, logout.php, index.php, etc)
- Upload arquivos: hostinger → cPanel → gerenciador arquivos → public_html/app → criar pasta subdomínio → novo arquivo php → colar conteúdo Cloud
- Quando Cloud trava (limite chars): pedir "refaça último arquivo" → continue
- Teste prático: access app.seudomain.com.br → login padrão admin/123456 (criar conta novo usuário)
- Funcionalidades testadas: criar sermão, listar, visualizar, editar, deletar, buscar, relatórios, exportar TXT/HTML/planilha
- Responsividade: F12 → toggle device → mobile vê corretamente
- Armazena: título, texto base, data, local, introdução, desenvolvimento, conclusão, anotações
- Contagem caracteres + estimativa tempo pregação automática
- Exportação: dados específicos ou geral múltiplos formatos

- Fonte: transcricoes/curso-id15/13-crie-um-saas-em-30-minutos/01-Criando_um_SaaS_em_30_minutos.md

## Construindo a Página de Vendas

**Aula:** 245

- Logo SaaS: Ideogram.AI (gerador imagem IA) → prompt "logotipo 'SermonFlix'" → landscape 1:1 tamanho
- Remover fundo: remove.bg upload logo → automático remove fundo → salvar PNG transparente
- Edit Windows: diminuir tamanho logo mínimo (File > Edit menu) → File > Save
- Hospedagem logo: Hostinger gerenciador arquivos → public_html → upload logo.png → copiar URL (https://seudominio/logo.png)
- Prompt página vendas: PDF fornecido com estrutura completa (3 partes: menu, benefícios, planos)
- Pontos amarelos template: troque aqui → logo URL, vídeo VSL, imagem 1-4 benefícios, preço, link checkout
- Vídeo VSL: gravar seu SaaS funcionando mostrando features (5-10 min explicação clara)
- Imagens benefícios: screenshot SaaS resize quadrado (Windows+Shift+S) → Paint → Ctrl+V → 4 imagens variadas funcionalidades
- Upload imagens: Hostinger → 1.png, 2.png, 3.png, 4.png → copiar URLs complete (https://seudominio/1.png etc)
- Garantia imagem: Ideogram prompt "imagem texto '7 dias' cor azul" → remover fundo remove.bg → salvar garantia.png
- Cloud AI: colar 3 partes prompt completo → aguarda geração HTML (pode travar parte 2/3)
- Se travar: "refaça parte dois" → copiar completo → vir arquivo anterior → colar continuação
- Estrutura HTML final: index.html com tudo (logo, menu ancoragem, vídeo, benefícios imagens, planos preço, garantia, FAQ)
- Checkout links: criar 3 ofertas Kirvano (acesso mensal, semestral, anual) → pegar links → colar em amarelo template
- Publicar: clique publish → espera → acessa dominio.com.br (sem /app) → página vendas pronta
- Responsividade mobile: F12 → toggle device → verifica layout legível celular
- Melhorias opcionais: aumentar tamanho imagens benefícios, editar cores, alterar COP conforme performance

- Fonte: transcricoes/curso-id15/13-crie-um-saas-em-30-minutos/02-Construindo_a_P_gina_de_Vendas.md

## Conheça o SaaS Build

**Aula:** 246

- SaaS Express: 2 aulas (criar SaaS 30min + página vendas) rápido validação ideia
- SaaS Build: curso completo 16 aulas profissional (projeto Sindup exemplo real início-fim)
- Diferencial SaaS Build: trata erros código, dificuldades IA, debugging prático
- Módulos SaaS Build: integração checkout (manual + automático), automação (VPS, Typebot, Evolution, N8N), microsaas, Q&A
- Integração checkout: Hotmart, Kirvano, Stripe conectar SaaS automaticamente (cancelamento automático)
- Automação: configurar Evolution bot com Typebot → assistente virtual SaaS
- Microsaas: HTML executável simples em máquina vendedor (ao invés ebook/conteúdo baixo valor)
- Duração aulas: média 10-15 min cada bem estruturado
- Comunidade WhatsApp: acesso 24h pessoas desenvolvendo SaaS, troca experiências nichos
- Desconto: quem comprou Express ganha discount entrada SaaS Build
- Valor comissão: 80% se vender estrutura produzida (templates, microsaas, automações)
- Comunidade funciona: pessoas variados nichos se ajudam, compartilham soluções
- Meta: construir negócio longo prazo (não apenas lançamento rápido)

- Fonte: transcricoes/curso-id15/13-crie-um-saas-em-30-minutos/03-Conhe_a_o_SaasBuild.md
