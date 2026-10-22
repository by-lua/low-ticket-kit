"""gflow com ANEXO de imagem na conta "agent-only" do Flow.

Por que existe: a conta do Flow (contato.minhaempresa) recebe o composer "agent-only"
(gflow issue #799). Nele o gflow 0.87 só aceita texto->imagem e texto->vídeo; qualquer
`i2i --ref`, `i2v --initial-frame` ou `r2v` sai com FlowHostMigratedError. Era por isso
que o loop POV-Bruno sempre caía no prompt-only e perdia o cenário-base.

O que faz: roda o próprio CLI do gflow (mesmo Chrome, mesmo perfil, mesma espera e
download), mas antes de enviar o comando anexa os arquivos pelo botão "+" do composer
("Enviar mídia" -> seleciona -> "Incluir no comando"), igual uma pessoa faz à mão.
Mapeado ao vivo em 22/10/2026.

Uso (sempre pelo python do gflow, via o wrapper pov-flow.sh):
    python -I gflow_ref.py image i2i --project <id> --ref a.png --ref b.png --out <dir> "<prompt>"
    python -I gflow_ref.py video i2v --project <id> --initial-frame cena.png --model omni-flash \
        --duration 8 --out-dir <dir> "<prompt>"
Qualquer outro comando passa direto pro gflow sem mudança.
"""

from __future__ import annotations

import asyncio
import mimetypes
import secrets
import sys
from pathlib import Path

from gflow_cli.api.transports import agent_only_composer as agent
from gflow_cli.api.video import Mode
from gflow_cli.errors import UiSelectorDriftError

ADD_BUTTON = (
    'button[aria-label="Adicionar elementos à caixa de comando"], '
    'button[aria-label="Add elements to the prompt box"]'
)
OVERLAY = ".cdk-overlay-pane"
INGREDIENT_BAR = "flow-ingredient-bar"
UPLOAD_WAIT_S = 90

_pending: list[Path] = []


def _log(msg: str) -> None:
    print(f"[gflow_ref] {msg}", file=sys.stderr, flush=True)


async def _ingredients(page) -> int:
    return await page.evaluate(
        "()=>{const b=document.querySelector('flow-ingredient-bar');"
        "return b?b.querySelectorAll('img').length:0}"
    )


async def _clear_ingredients(page) -> None:
    """Remove anexo que sobrou de uma rodada anterior (o Flow guarda o rascunho)."""
    for _ in range(10):
        if not await _ingredients(page):
            return
        x = page.locator(f"{INGREDIENT_BAR} button:has(mat-icon:text-is('cancel'))").first
        if not await x.count():
            x = page.locator(f"{INGREDIENT_BAR} mat-icon:text-is('cancel')").first
        await x.click(timeout=4000)
        await page.wait_for_timeout(800)
        if "movido para a lixeira" in await page.evaluate("()=>document.body.innerText"):
            undo = page.locator("button", has_text="Desfazer").first
            if await undo.count():
                await undo.click()
            raise UiSelectorDriftError(
                detail="gflow_ref: limpar anexo antigo mandou mídia pra lixeira (desfeito); nada foi enviado"
            )
    if await _ingredients(page):
        raise UiSelectorDriftError(detail="gflow_ref: não consegui limpar anexos antigos do composer")


async def _attach(page, path: Path) -> None:
    before = await _ingredients(page)
    name = f"pov-{path.stem}-{secrets.token_hex(3)}{path.suffix.lower()}"
    stem = name.rsplit(".", 1)[0]
    await page.locator(ADD_BUTTON).first.click(timeout=8000)
    up = page.locator(f'{OVERLAY} button:has(mat-icon:text-is("upload"))').first
    await up.wait_for(state="visible", timeout=10000)
    dialogs = await page.locator("mat-dialog-container").count()
    async with page.expect_file_chooser(timeout=10000) as fc:
        await up.click()
    chooser = await fc.value
    await chooser.set_files(
        {
            "name": name,
            "mimeType": mimetypes.guess_type(path.name)[0] or "image/png",
            "buffer": await asyncio.to_thread(path.read_bytes),
        }
    )
    _log(f"enviando {path.name} como {name}")
    state = "?"
    for _ in range(int(UPLOAD_WAIT_S / 1.5)):
        await page.wait_for_timeout(1500)
        if await page.locator("mat-dialog-container").count() > dialogs:
            raise UiSelectorDriftError(
                detail=(
                    "gflow_ref: o Flow abriu um diálogo no upload (provável 'direitos de uso da "
                    "imagem', só na 1ª vez da conta). Aceite UMA vez à mão no Flow e rode de novo."
                )
            )
        if await _ingredients(page) > before:  # alguns projetos já incluem sozinho
            state = "incluido"
            break
        # Olha só o item deste upload: outro upload antigo preso em "Enviando" não pode travar.
        state = await page.evaluate(
            """(stem)=>{const o=[...document.querySelectorAll('.cdk-overlay-pane [role=option]')]
                 .find(e=>e.innerText.includes(stem));
               if(!o) return document.querySelector('.cdk-overlay-pane [role=option]') ? 'ausente' : 'sem-seletor';
               return /Enviando|Uploading/i.test(o.innerText) ? 'enviando' : 'pronto'}""",
            stem,
        )
        if state == "pronto":
            break
    else:
        raise UiSelectorDriftError(
            detail=f"gflow_ref: upload de {path.name} não terminou em {UPLOAD_WAIT_S}s (último estado: {state})"
        )
    for tentativa in range(3):
        if state == "incluido" or await _ingredients(page) > before:
            break
        if tentativa > 0:  # seletor fechou ou não incluiu: reabre e procura o item já enviado
            _log(f"anexo não entrou, tentando de novo ({tentativa})")
            if not await page.locator(f"{OVERLAY} [role=option]").count():
                await page.locator(ADD_BUTTON).first.click(timeout=8000)
                await page.wait_for_timeout(2000)
        # Dois comportamentos medidos 22/10: clicar no item já inclui no comando, OU abre a
        # prévia com o botão "Incluir no comando". Trata os dois.
        opt = page.locator(f"{OVERLAY} [role=option]", has_text=stem).first
        if not await opt.count():
            await page.wait_for_timeout(2000)
            continue
        await opt.click(timeout=8000)
        await page.wait_for_timeout(1500)
        if await _ingredients(page) == before:
            inc = page.locator(f"{OVERLAY} button", has_text="Incluir no comando").first
            if await inc.count():
                await inc.click(timeout=8000)
                await page.wait_for_timeout(1500)
    if await page.locator(f"{OVERLAY} [role=option]").count():
        await page.keyboard.press("Escape")  # fecha o seletor se ficou aberto
        await page.wait_for_timeout(600)
    after = await _ingredients(page)
    if after != before + 1:
        raise UiSelectorDriftError(
            detail=f"gflow_ref: anexo de {path.name} não entrou no composer ({before} -> {after})"
        )
    _log(f"anexado {path.name} ({after} no composer)")


# --- patches -------------------------------------------------------------------------

_orig_unported_image = agent.unported_image
_orig_unported_video = agent.unported_video
_orig_run_images = agent.run_agent_images
_orig_run_video = agent.run_agent_video
_orig_generate = agent.AgentOnlyComposer.generate


def _unported_image(request):
    if request.ref_paths and not request.refs:
        from dataclasses import replace

        return _orig_unported_image(replace(request, ref_paths=()))
    return _orig_unported_image(request)


def _unported_video(request):
    if request.mode is Mode.I2V and request.start_image is not None and request.end_image is None:
        from dataclasses import replace

        return _orig_unported_video(replace(request, mode=Mode.T2V, start_image=None))
    return _orig_unported_video(request)


async def _run_images(page, request, *, project_id):
    _pending[:] = [Path(p) for p in request.ref_paths]
    return await _orig_run_images(page, request, project_id=project_id)


async def _run_video(page, request, **kw):
    _pending[:] = [Path(request.start_image)] if request.start_image else []
    return await _orig_run_video(page, request, **kw)


async def _generate(self, page, directive, **kw):
    # Anexa ANTES do gflow medir a linha de base: o upload vira um tile novo na grade e,
    # se entrasse depois, o gflow contaria como resultado extra e abortaria.
    await _clear_ingredients(page)
    for p in list(_pending):
        await _attach(page, p)
    _pending.clear()
    await _ensure_create_view(page)
    return await _orig_generate(self, page, directive, **kw)


CREATE_EDITOR = 'div.ProseMirror[aria-label="O que você quer criar?"], div.ProseMirror[aria-label="What do you want to create?"]'


async def _ensure_create_view(page) -> None:
    """O Flow às vezes abre o visualizador da mídia recém-enviada ('O que você quer mudar?').
    Se o comando for digitado ali, vira EDIÇÃO da foto e nenhuma imagem nova sai (22/10/2026).
    Fecha o visualizador e só segue se o último editor da página for o de criação."""
    for _ in range(4):
        last = page.locator("div.ProseMirror").last
        label = (await last.get_attribute("aria-label")) if await last.count() else None
        if label and label in ("O que você quer criar?", "What do you want to create?"):
            return
        _log(f"visualizador aberto (editor='{label}'), fechando")
        back = page.locator("button:has(mat-icon:text-is('arrow_back'))").first
        if await back.count():
            await back.click(timeout=4000)
        else:
            await page.keyboard.press("Escape")
        await page.wait_for_timeout(1500)
    raise UiSelectorDriftError(
        detail="gflow_ref: o campo de criação não voltou depois do anexo; nada foi enviado"
    )


agent.unported_image = _unported_image
agent.unported_video = _unported_video
agent.run_agent_images = _run_images
agent.run_agent_video = _run_video
agent.AgentOnlyComposer.generate = _generate

def _profile_dir() -> Path:
    import os

    return Path.home() / f".local/share/gflow-cli/profile_{os.environ.get('FLOW_PROFILE', 'flow-gflow')}"


async def _probe() -> str:
    """Checagem REAL de login (o `gflow auth status` erra: diz deslogado com sessão boa).
    Deslogado = o Flow manda pra página pública /about."""
    from gflow_cli.api.client import FlowApiClient

    async with FlowApiClient(_profile_dir()) as c:
        page = c.page
        await page.goto("https://flow.google.com/", wait_until="domcontentloaded", timeout=45000)
        await page.wait_for_timeout(8000)
        return "deslogado" if "/about" in page.url else "ok"


async def _new_project() -> str:
    """Cria projeto pelo botão "Novo projeto" do flow.google.com (o `gflow project create`
    cria um id que o host novo responde 'Projeto não encontrado' — medido 22/10/2026)."""
    import re

    from gflow_cli.api.client import FlowApiClient

    async with FlowApiClient(_profile_dir()) as c:
        page = c.page
        await page.goto("https://flow.google.com/", wait_until="domcontentloaded", timeout=45000)
        btn = page.locator("button", has_text=re.compile(r"Novo projeto|New project"))
        await btn.first.wait_for(state="visible", timeout=30000)
        await page.wait_for_timeout(1500)
        await btn.first.click()
        await page.wait_for_url(re.compile(r"/project/[0-9a-f-]{36}"), timeout=30000)
        return re.search(r"/project/([0-9a-f-]{36})", page.url).group(1)


if __name__ == "__main__":
    if sys.argv[1:2] == ["probe"]:
        print(asyncio.run(_probe()))
        sys.exit(0)
    if sys.argv[1:2] == ["novo-projeto"]:
        print(asyncio.run(_new_project()))
        sys.exit(0)
    from gflow_cli.cli import main

    sys.argv[0] = "gflow"
    sys.exit(main())
