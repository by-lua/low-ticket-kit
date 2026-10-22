"""Helpers persistentes do browser-harness.

Carregado automaticamente pelo browser-harness (BH_AGENT_WORKSPACE aponta pra ca).
Helpers do core ja vem pre-importados; aqui so entra o que e especifico das
tarefas deste ambiente.

REGRA: helper so entra aqui depois de rodar e funcionar de verdade. E a
contraparte em codigo das receitas em domain-skills/ — a receita explica o
fluxo, o helper executa o pedaco chato.

Perfis / portas CDP (BU_CDP_URL=http://127.0.0.1:<porta>):
    gpt -> 9222   chatgpt.com
    hub -> 9223   ninjabrhub.io/studio
    gg  -> 9224   ggcheckout.app
"""

PROFILE_PORTS = {"gpt": 9222, "hub": 9223, "gg": 9224}


def profile_cdp_url(profile: str) -> str:
    """Endpoint CDP HTTP de um perfil persistente. Exporte como BU_CDP_URL."""
    try:
        return f"http://127.0.0.1:{PROFILE_PORTS[profile]}"
    except KeyError:
        raise ValueError(
            f"perfil desconhecido: {profile!r}. Conhecidos: {sorted(PROFILE_PORTS)}"
        ) from None
