# Vela — Brand design workspace

Local React + FastAPI + Blender MVP. See docs/PRD.md for the source requirements and docs/DEMO.md for the prepared fixture.

## Run

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
npm install
npm run build
.venv/bin/uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000. For frontend development, run `npm run dev` alongside the backend.

Blender defaults to `/Applications/Blender.app/Contents/MacOS/Blender`; override BLENDER_PATH if needed. Set OPENAI_API_KEY and the exact available OPENAI_MODEL in the server environment for live extraction, planning and visual review. `.env.example` is documentation; the server does not automatically load `.env` files. Never put API keys in the frontend.

## Workflow

Approve editable Vela rules → approve dimensions and rationale → generate a fresh concept or diagnostic scene → run deterministic review → preview a suggested fix → approve → rerender and verify → compare or restore versions.

State is stored in data/workspace.sqlite. Versioned .blend files, measurements, renders and worker logs are in outputs/demo. The local service is single-user and binds only to loopback. Do not expose it to the public internet.

## Boundaries

The generator supports a bounded speaker template, not arbitrary product geometry. Only shell material, ring accent, and ring thickness are auto-fixable. Logo checking currently measures origin height; studio checking measures light power. Visual interpretation stays REVIEW. Live AI requires configured credentials and has not been validated without them. Frontend source compilation and backend tests do not substitute for product-designer evaluation.

API implementation reference: https://developers.openai.com/api/docs/guides/structured-outputs

## Blender MCP execution (working route)

The backend now prefers Blender MCP on `127.0.0.1:9876` and runs the checked-in worker inside the open Blender GUI. This avoids the observed background Metal initialization crash. No arbitrary Python execution endpoint is exposed by the web app.

Installed here: `blender-mcp==1.9.1`, matching Blender addon in the Blender 5.0 user scripts directory, and `[mcp_servers.blender]` in the existing Codex config. Existing MCP entries were preserved. Telemetry is disabled. The package is invoked directly from this project's virtual environment; uvx is not required for this installation.

Keep Blender open with its MCP server running. If reconnecting after restart, use the Blender MCP sidebar's connection button. The wording may say “Connect to Claude,” but the connection also works with Codex. The web header indicates whether the local socket is reachable.

The backend uses the official MCP Python client and the server's `execute_blender_code` tool to invoke only `blender/scene.py` with backend-generated versioned requests. Every GUI run backs up the previously open scene before loading or generating geometry. Selection uses the same MCP transport; the older selection_bridge.py is no longer needed when MCP is connected.

`outputs/MCP Verification.json` records the local generation/revision test and is not committed. The original and revised test scenes are demo fixtures, not human-approved product revisions.

Sources: https://github.com/ahujasid/blender-mcp and https://learn.chatgpt.com/docs/extend/mcp?surface=cli

## Team collaboration

See [CONTRIBUTING.md](CONTRIBUTING.md) for branch and document review workflow.
