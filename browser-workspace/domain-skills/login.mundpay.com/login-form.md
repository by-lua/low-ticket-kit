# Mundpay — Login (verificado 2026-10-02)

Painel: `https://login.mundpay.com`. Formulário com React controlado (não responde a `.value` direto).

## Técnica: click + type + Tab

Inputs têm validação onChange no React state. Preenchimento via `.value` + event falha.

Receita correta:
```javascript
// Email
const emailInput = document.querySelector('input[type="email"]');
emailInput.click();
emailInput.type('voce@exemplo.com'); // agent-browser type
// ou manualmente:
for (const char of 'voce@exemplo.com') {
  emailInput.dispatchEvent(new KeyboardEvent('keydown', { key: char, bubbles: true }));
  emailInput.value += char;
  emailInput.dispatchEvent(new KeyboardEvent('keyup', { key: char, bubbles: true }));
}
document.activeElement.dispatchEvent(new KeyboardEvent('keydown', { key: 'Tab', code: 'Tab', bubbles: true }));
// Tab pra próximo campo (desencadeia blur/onChange)

// Senha
const passInput = document.querySelectorAll('input')[1];
passInput.click();
// type senha
passInput.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', bubbles: true }));
```

**Simpler:** use `agent-browser type <text>` direto (simula teclado nativo):
```bash
agent-browser --session mundpay click input[type=email]
agent-browser --session mundpay type "voce@exemplo.com"
agent-browser --session mundpay key Tab
agent-browser --session mundpay type "$MUNDPAY_PASSWORD"
agent-browser --session mundpay key Return
```

Status: Logado quando redireciona pra `/products` (sem erros 401).
