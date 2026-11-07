# Vast.ai live dashboard

Zero-dependency Vast.ai telemetry and instance control, packaged as a Docker
container. The API key stays server-side; the browser never sees it.

```
Dockerfile            python:3.12-alpine, non-root, healthcheck
 docker-compose.yml    restart, read-only rootfs, cap_drop ALL, mem/cpu caps
deploy_kvm4.sh        build + start / logs / stop
server.py             stdlib backend + auth gate
index.html            single-page UI
.env.example          template for VASTAI_API + VAST_DASH_TOKEN
```

Total image payload: **~30 KB** of source (image itself ~55 MB, it is Alpine).

## Deploy on KVM4

```bash
scp -r tools/vast_dashboard kvm4:/opt/vast-dashboard
ssh kvm4
cd /opt/vast-dashboard
cp .env.example .env
nano .env          # set VASTAI_API and VAST_DASH_TOKEN (openssl rand -hex 24)
./deploy_kvm4.sh   # docker compose up -d --build
```

Then open `http://<kvm4>:8090/` and enter the token.

## Security

| Control | Detail |
| --- | --- |
| Auth gate | `VAST_DASH_TOKEN`; HttpOnly + SameSite=Strict signed cookie, or `Authorization: Bearer` |
| Fail throttle | 10 failed logins per IP / 5 min |
| Refuses unsafe bind | Won't bind a public address without a token unless `--insecure` |
| Confirm gate | `stop`/`start`/`destroy` require `confirm: true` in the body |
| Key isolation | Read from env inside the container; never serialised to the UI |
| Container | Non-root user, read-only rootfs, all capabilities dropped, 128 MB / 0.5 CPU |

**Do not expose `DASH_BIND=0.0.0.0` to the open internet.** Bind to
`127.0.0.1` and reach it through an SSH tunnel (`ssh -L 8090:127.0.0.1:8090 kvm4`)
or put it behind a TLS reverse proxy (Caddy/nginx). The token is the only
credential in front of instance destruction.

## Local (no Docker)

```bash
VASTAI_API=... VAST_DASH_TOKEN=... python3 server.py --host 127.0.0.1 --port 8090
```

Without `VAST_DASH_TOKEN` it will only bind loopback.

## API

| Route | Method | Purpose |
| --- | --- | --- |
| `/` | GET | UI (login page when unauthenticated) |
| `/login` | POST | form token -> signed cookie |
| `/api/summary` | GET | credit, burn rate, instances |
| `/api/instances` | GET | enriched instance list |
| `/api/offers` | GET | cheapest verified on-demand offers |
| `/api/logs?id=N` | GET | last log lines for an instance |
| `/api/action` | POST | `{action, id, confirm:true}` |
| `/healthz` | GET | liveness (unauthenticated, no data) |
