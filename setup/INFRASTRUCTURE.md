# Infrastructure — srv1231216 (crimson)

Live services on the Hostinger KVM 4 VPS (Ubuntu 24.04 + Docker + Traefik),
and how this repository's tooling connects to them.

Secrets are **never** stored here. Credentials live in the environment or in
each compose project's `.env` on the VPS.

## Host

| | |
|---|---|
| Host | `crimson.blaze` / `srv1231216.hstgr.cloud` |
| Plan | KVM 4 — 4 vCPU, 16 GB RAM, 200 GB disk |
| Routing | Traefik (host network), Let's Encrypt via `letsencrypt` certresolver |
| Convention | apps published at `https://<project>.srv1231216.hstgr.cloud` |

## Ollama — local inference

Container `ollama-bm3e-ollama-1`, project dir `/docker/ollama-bm3e`.

Two ways in, depending on where the client runs:

| Client location | Endpoint | Auth |
|---|---|---|
| Containers on the VPS (code-server, Letta) | `http://ollama-bm3e-ollama-1:11434` | none (private Docker network) |
| Anywhere else (desktop, external harness) | `https://ollama-bm3e.srv1231216.hstgr.cloud` | HTTP basic — user `ollama` |

The public route is defined in `docker-compose.override.yml` in the project
dir: Traefik labels (`websecure` + `letsencrypt`) plus a `basicauth`
middleware. Unauthenticated requests get `401`.

Clients that read `OLLAMA_HOST` take the URL directly; for the public route
embed the credentials: `https://ollama:<password>@ollama-bm3e.srv1231216.hstgr.cloud`.

### Models

| Model | Size | Capabilities |
|---|---|---|
| `vaultbox/qwen3.5-uncensored:4b` | 3.4 GB | completion, tools, thinking — 262K ctx |
| `hf.co/noctrex/Huihui-Qwen3-VL-4B-Instruct-abliterated-GGUF:Q4_K_M` | 3.3 GB | completion, vision — 262K ctx |
| `qwen2.5vl:3b` | 3.2 GB | vision, completion — 128K ctx |
| `phi4-mini:latest` | 2.5 GB | completion, tools — 131K ctx |
| `nomic-embed-text:latest` | 274 MB | embeddings (768-dim) |

Runtime limits: one loaded model at a time, no parallel requests, 10-minute
keep-alive, capped at 3 CPUs — sized so inference cannot starve the other
services on the box.

## Letta (letta-scy7) — agent runtime for this repo

Project dir `/docker/letta-scy7`; two containers:

- `letta-scy7-letta-1` — Letta server, published via Traefik, port 8283.
- `letta-scy7-db-1` — **pgvector/pgvector:pg16**: Postgres 16 with the
  `vector` extension, the agent store (agents, messages, archival memory
  embeddings). Volume `db_data`, healthchecked with `pg_isready`.

This instance is intentionally separate from the other Letta stacks on the
box (`letta`, `letta-6ou3`) — it starts empty and is dedicated to this
repository's agents.

`docker-compose.override.yml` wires it to Ollama: it joins the
`ollama-bm3e_default` network and sets `OLLAMA_BASE_URL`. All five Ollama
models then appear in `GET /v1/models/` alongside the OpenAI ones, so agents
can be created against the uncensored models with no further setup.

Pair a completion model with `nomic-embed-text` for embeddings to keep an
agent fully local — no request leaves the VPS.

## Reproducing

Both integrations are `docker-compose.override.yml` files beside each
project's `docker-compose.yml`. Compose merges them automatically; the
original files are untouched. Re-apply with:

```bash
cd /docker/<project> && docker compose -p <project> up -d
```

Always pass `-p <project>` — without it, compose derives the project name
from the working directory and creates a **duplicate** stack with fresh,
empty volumes instead of updating the running one.
