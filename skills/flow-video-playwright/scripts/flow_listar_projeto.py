# Lista a mídia de um projeto do Flow (para recuperar vídeo quando o flow.sh sai com exit 25 e a geração continua).
# uso: flock ~/.cache/pov-flow/<perfil>.lock env DISPLAY=:1 ~/.local/share/uv/tools/gflow-cli/bin/python flow_listar_projeto.py <perfil> <project_id>  -> bodies.json no cwd
import asyncio, json, sys
from gflow_cli._cli_helpers import _make_provider_dir
from gflow_cli.api.client import FlowApiClient
PID=sys.argv[2]
async def main():
    async with FlowApiClient(profile_dir=_make_provider_dir(sys.argv[1]), headless=False) as c:
        page = await c._context.new_page()
        bodies=[]
        async def on_resp(r):
            if "flow.google.com" in r.url and r.request.resource_type in ("fetch","xhr"):
                try: bodies.append({"url":r.url[:200],"body":await r.text()})
                except Exception as e: pass
        page.on("response", lambda r: asyncio.ensure_future(on_resp(r)))
        await page.goto(f"https://flow.google.com/project/{PID}", wait_until="domcontentloaded")
        await page.wait_for_timeout(15000)
        print("url", page.url)
        try:
            d = await c.fetch_project_listing(PID); bodies.append({"url":"api","body":json.dumps(d)})
        except Exception as e: print("api fail", type(e).__name__)
        json.dump(bodies, open("bodies.json","w"))
        print(len(bodies), [b["url"][:90] for b in bodies])
asyncio.run(main())
