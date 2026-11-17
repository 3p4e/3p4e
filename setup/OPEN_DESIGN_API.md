# Open Design on KVM4 — API access reference

Verified 25.10.2026 against the running daemon: Open Design 0.23.0 (daemon reports 0.22.1), container
`open-design`, stack `/opt/open-design`. Taken from the daemon source (`/app/apps/daemon/dist`:
`api-token-auth.js`, `server.js`, `origin-validation.js`, `http/*.js`, `tool-tokens.js`) and from live
requests. This file holds names only, never secret values.

## Endpoints

| | |
|---|---|
| Public URL | `https://open-design.srv1231216.hstgr.cloud`. Traefik terminates TLS and forwards to container port 7456. It adds no auth of its own. |
| Inside the container / host | `http://127.0.0.1:7456`, published only on the host loopback (`127.0.0.1:7456:7456`) |
| Token | `OD_API_TOKEN` in `/opt/open-design/.env` (also in the container env) |

## Authentication (`api-token-auth.js` + the `/api` middleware in `server.js`)

Auth is active when `OD_API_TOKEN` is non-empty **and** `OD_DISABLE_API_AUTH` is not truthy. On KVM4
the token is set and `OD_DISABLE_API_AUTH` is empty. The daemon refuses to start when bound to a
non-loopback host (`OD_BIND_HOST=0.0.0.0` here) without a token.

Every `/api/*` request must pass **one** of these:

1. **Bearer:** `Authorization: Bearer <OD_API_TOKEN>`. Matched with `/^Bearer[\t ]+(\S+)[\t ]*$/i` and a
   constant-time compare. Use this for scripts, the CLI, and automations.
2. **Basic:** `Authorization: Basic base64("open-design:<OD_API_TOKEN>")`. The username must be exactly
   `open-design` and the password is the token. Strict base64 (it must round-trip). This is what the browser uses.
3. **Loopback peer:** the TCP peer address is `127.0.0.1`/`::1`. No header is needed. This applies to
   anything running inside the container, such as `docker exec open-design node -e "fetch('http://127.0.0.1:7456/...')"`.
   `X-Forwarded-For` is ignored on purpose, so requests through Traefik always need credentials.
4. **Run-scoped tool token** (`odtt_…`, minted per agent run, 15-min default TTL): accepted only for
   `POST /api/projects/:id/export/:format`, and as a Bearer on `/api/tools/*` wrapper routes.
   The daemon removes `OD_API_TOKEN` from agent child processes, so agents only ever get `OD_TOOL_TOKEN`.
5. **Preview-asset scope:** GET of a server-minted project preview asset path works without credentials
   (sandboxed iframes). Renewing a scope requires the header `x-od-preview-scope-renewal: 1`.

Paths open without auth: `/health`, `/ready`, `/version` and their `/api/...` forms.

Failure: `401` with `WWW-Authenticate: Basic realm="OpenDesign", charset="UTF-8"` and body
`{"error":{"code":"API_TOKEN_REQUIRED","message":"Authorization: Bearer <OD_API_TOKEN> or browser Basic authentication required"}}`.
Non-API page navigations get a plain-text 401: *Use username "open-design" and OD_API_TOKEN as the password.*

Checked live from outside: `/api/health` 200, `/api/version` 200, `/api/projects` 401 with the challenge
above, `/` 401.

## Origin / CSRF guard (applies after auth, to every `/api` route)

- **No `Origin` header** (curl, scripts, the CLI): **always allowed**.
- `Origin: null` (sandboxed iframe): GET on a short read-only allowlist only, otherwise 403.
- Browser `Origin`: allowed when it equals an entry in `OD_ALLOWED_ORIGINS` (here
  `https://open-design.srv1231216.hstgr.cloud`), or is a loopback/private-LAN origin on port 7456.
  Otherwise `403 {"error":"Cross-origin requests are not allowed"}`.
  For server-side code, either send no `Origin` or send exactly the allowed origin.
- If `Origin` is absent but `Sec-Fetch-Site: same-origin` is present, the Host is checked against the same allowlist.
- Some plugin-share routes additionally require `isLocalSameOrigin`, a same-origin browser call.

## Other request headers the daemon reads

| Header | Where | Effect |
|---|---|---|
| `Content-Type: application/json` | all JSON routes | Body limit 4 MB (library ingest 128 MB, brand extract 32 MB) |
| multipart/form-data | `POST /api/projects/:id/files` (field `file`, optional `name` keeps sub-folders), `POST /api/projects/:id/upload` (multiple files) | file upload |
| `x-od-client: web\|desktop` | `POST /api/runs` | Analytics label only; otherwise the User-Agent is used (`Electron/` → desktop) |
| `x-od-workspace-id` + `x-od-workspace-member-id` | Team/workspace (collab) routes | Both or neither. One without the other → "missing" context and the request is rejected. Not needed for personal projects. |
| `x-od-workspace-runtime-client-id`, `x-od-workspace-runtime-generation` | `/api/collab/...` billing | AMR workspace runtime only |
| `x-vela-workspace-id` | `/api/vela/...` | Vela/AMR cloud agent |
| `x-od-desktop-import-token` | `POST /api/import/folder` | Required to import a host folder (desktop/CLI-minted, nonce, one use) |
| `Last-Event-ID` | `GET /api/runs/:id/events` (SSE) | Resume an event stream |
| `If-None-Match` / `If-Modified-Since` / `If-Range` | project file reads | Caching / range |

## Core calls (all with `Authorization: Bearer $OD_API_TOKEN`)

```
GET  /api/agents                      # agent detection: available, path, models, diagnostics
GET  /api/projects                    # list
POST /api/projects                    # {id:<uuid>, name, skillId?, designSystemId?, metadata?, skipDiscoveryBrief?} → {project, conversationId}
POST /api/projects/:id/files          # multipart: file=@x, name=assets/x.png
GET  /api/projects/:id/files          # list (name, size, kind, artifactManifest)
POST /api/runs                        # {projectId, conversationId?, agentId, model?, message, byokProvider?} → 202 {runId, conversationId, assistantMessageId}
GET  /api/runs/:id                    # status: queued|running|succeeded|failed|cancelled, error, failureCategory
GET  /api/runs/:id/events             # SSE event log
POST /api/runs/:id/cancel
POST /api/projects/:id/export/{html|pdf|image|pptx}
```

`agentId: "byok-opencode"` needs `byokProvider: {protocol: anthropic|openai|azure|google|ollama|senseaudio|aihubmix, apiKey, baseUrl?}`
plus a `model`, otherwise you get `400 VALIDATION_FAILED`.

## How to reach it from a Claude Code cloud session

SSH is not reachable. Use the kvm4-runner: `POST $RUNNER_URL/shell` with `Authorization: Bearer $RUNNER_TOKEN`
(`KVM4_RUNNER_TOKEN` is stale). From there, run `docker exec open-design node -e "…"` against
`http://127.0.0.1:7456`. Read `process.env.OD_API_TOKEN` inside the container, so the token never leaves the server.
Helpers used in practice: `rsh.py` (runner shell), `rput.py` (chunked `/file/write` with sha256 check),
`odjs.py` (runs a JS file inside the container).

## Agent providers (state after the 25.10.2026 fix)

Backup of the pre-fix config: `/opt/open-design/backups/20261025-193947-provider-fix/`.

- Agent home is persistent: `/opt/open-design/home` → `/home/open-design` (was tmpfs, which wiped CLI logins on every restart).
- Daemon heap: `NODE_OPTIONS=--max-old-space-size=1024` (was 256).
- DeepSeek: wrapper `/home/open-design/.local/bin/deepseek` (moves `--model` before `exec` for codewhale), set via `DEEPSEEK_BIN`. ✅
- OpenCode: default model is now NVIDIA NIM (see "NVIDIA NIM" below); DeepSeek stays available as a provider. ✅
- Codex: logged in with `OPENAI_API_KEY`. The OpenAI account has no credits; top up billing.
- Kimi: Moonshot provider for now. For the Kimi For Coding (Allegretto) plan, put that key in `.env` as
  `KIMI_API_KEY`, recreate the container, then run `sh /opt/open-design/kimi-code-setup.sh`.
- Claude Code: the binary under `/root` is unreadable for uid 1001, and the Anthropic key returns 401. Needs a valid key or login.
- Gemini: `GEMINI_API_KEY` is empty.

## NVIDIA NIM (configured 17.11.2026)

NVIDIA NIM is OpenAI-compatible at `https://integrate.api.nvidia.com/v1`. The key is `NVIDIA_API_KEY` in
`/opt/open-design/.env`, passed through `docker-compose.yml` into the container. No value is recorded here.
Backup of the previous config: `/opt/open-design/backups/20261117-130833-nvidia-nim/`.

| Function in Open Design | Model |
|---|---|
| Default design/code agent (`agentId=opencode`, app-config) and memory extractor | `nvidia/nemotron-3-ultra-550b-a55b` |
| OpenCode small/background model (titles, summaries) | `nvidia/nemotron-3.5-bolt-e4b` |
| Fast code edits (selectable) | `poolside/laguna-xs-2.1` |
| Long, hard tasks (selectable) | `mistralai/mistral-large-4-1t-a52b` |
| Reasoning (selectable) | `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` |
| Vision / image input (selectable) | `google/gemma-4-31b-it`, `nvidia/nemotron-3.5-super-vl-120b-a12b` |

How it is wired:

- OpenCode: provider `nvidia-nim` in `/opt/open-design/home/.config/opencode/opencode.json` (npm `@ai-sdk/openai-compatible`,
  `apiKey` read from `{env:NVIDIA_API_KEY}`).
- Default agent: `PUT /api/app-config` with a partial body (`agentId`, `agentModels`).
- Memory extraction: `PATCH /api/memory/config {extraction:{provider,baseUrl,model}}`. Leave `apiKey` out to keep the stored one.

Lessons:

- Memory extraction has a 30 s timeout and asks for `response_format: json_object`. Gemma 4 31B took 32.6 s on long input and
  timed out; Nemotron 3 Ultra answered in 5.2 s. Pick the extractor for latency, not size.
- The first run on a NIM model after a restart can fail without a message (cold start). Retry once.
- Not covered: Open Design's media providers (openai, grok, nanobanana, openrouter, fal, minimax, elevenlabs) have no NIM
  equivalent, and NIM embeddings do not fit the 1536-dim Open Brain column. Image and video generation stay with Higgsfield.
- Server disk was 100% full at the time (about 800 MB free). `/opt/open-design/home` held 1.9 GB, mostly caches
  (puppeteer 1.2 GB, npm 492 MB). Clear those before the next large upload.
