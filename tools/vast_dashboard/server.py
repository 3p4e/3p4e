#!/usr/bin/env python3
"""Vast.ai live dashboard — zero-dependency backend with an auth gate.

Serves a single-page UI and proxies Vast.ai calls so the API key never leaves
this process. Every route (UI and API) is protected by VAST_DASH_TOKEN when it
is set; destructive actions additionally require an explicit `confirm` flag.

Safety: if no token is configured the server refuses to bind a non-loopback
address unless --insecure is passed. Do not run this publicly without a token.

Usage:
  python3 server.py --port 8090 [--host 0.0.0.0] [--token SECRET]

Environment:
  VASTAI_API        Vast.ai API key (required)
  VAST_DASH_TOKEN   dashboard login token (strongly recommended)
  VAST_DASH_HOST    bind host (default 0.0.0.0)
  VAST_DASH_PORT    bind port (default 8090)
"""
import argparse
import hmac
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from hashlib import sha256
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BASE = "https://console.vast.ai/api/v0"
PROJ = "/a0/usr/projects/vast"
HERE = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(HERE, "index.html")
COOKIE_NAME = "vd_auth"

API_KEY = None
AUTH_TOKEN = None
_FAILS = {}  # ip -> [timestamps]


# ---------------------------------------------------------------- key loading
def load_key():
    if os.environ.get("VASTAI_API", "").strip():
        return os.environ["VASTAI_API"].strip()
    env_file = os.path.join(PROJ, ".a0proj", "secrets.env")
    if os.path.exists(env_file):
        m = re.search(r"(?m)^VASTAI_API=\s*(.+?)\s*$", open(env_file).read())
        if m:
            return m.group(1).strip().strip('"').strip("'")
    return None


# ------------------------------------------------------------------ vast calls
def req(method, path, body=None, timeout=40):
    headers = {"Authorization": "Bearer " + (API_KEY or ""), "Content-Type": "application/json"}
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            raw = resp.read().decode()
            try:
                return resp.status, json.loads(raw)
            except json.JSONDecodeError:
                return resp.status, {"raw": raw[:2000]}
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode() or "{}")
        except Exception:
            return e.code, {"error": "HTTP %s" % e.code}
    except Exception as e:  # noqa: BLE001
        return 0, {"error": str(e)}


def enrich_instance(x):
    ports = x.get("ports") or {}
    ssh = (ports.get("22/tcp") or [{}])[0] or {}
    now = time.time()
    start = x.get("start_date") or x.get("created_at")
    try:
        start_f = float(start) if start else None
    except (TypeError, ValueError):
        start_f = None
    uptime_s = None
    if start_f and start_f > 1e9:
        uptime_s = int(now - start_f / 1000)
    elif start_f and start_f > 1e6:
        uptime_s = int(now - start_f)
    return {
        "id": x.get("id"),
        "label": x.get("label"),
        "actual_status": x.get("actual_status"),
        "cur_state": x.get("cur_state"),
        "status_msg": x.get("status_msg"),
        "dph_total": round(float(x.get("dph_total") or 0), 3),
        "gpu_name": x.get("gpu_name"),
        "gpu_ram_mb": x.get("gpu_ram"),
        "cpu_ram_mb": x.get("cpu_ram"),
        "cpu_cores": x.get("cpu_cores_effective") or x.get("cpu_cores"),
        "disk_gb": x.get("disk_space"),
        "public_ip": x.get("public_ipaddr"),
        "ssh_host": x.get("ssh_host"),
        "ssh_port": x.get("ssh_port") or ssh.get("HostPort"),
        "geolocation": x.get("geolocation"),
        "uptime_s": uptime_s,
        "is_bid": x.get("is_bid"),
        "image_uuid": x.get("image_uuid"),
        "ports": ports,
    }


def get_instances():
    st, d = req("GET", "/instances/")
    if st != 200:
        return st, d
    return st, [enrich_instance(x) for x in d.get("instances", [])]


def get_summary():
    out = {"ok": False, "ts": int(time.time())}
    st_c, user = req("GET", "/users/current/")
    st_i, insts = get_instances()
    credit = None
    if st_c == 200:
        credit = round(float(user.get("credit") or 0.0), 3)
        for k in ("balance", "total_spend", "autobill_threshold", "balance_threshold",
                  "balance_threshold_enabled", "autobill_amount", "email", "username", "tfa_status"):
            if k in user:
                out[k] = user[k]
    else:
        out["user_error"] = user
    if st_i == 200:
        out["instances"] = insts
    else:
        out["instances_error"] = insts
    if credit is not None:
        out["credit"] = credit
        running = [i for i in insts if i["actual_status"] in
                   ("running", "loading", "openport", "pending")] if isinstance(insts, list) else []
        out["running"] = len(running)
        out["total_dph"] = round(sum(i["dph_total"] for i in running), 3)
        out["burn_hours"] = round(credit / out["total_dph"], 1) if out["total_dph"] > 0 else None
    out["ok"] = out.get("credit") is not None
    return out


# ------------------------------------------------------------------------ auth
def cookie_value():
    return hmac.new(AUTH_TOKEN.encode(), b"vast-dash-v1", sha256).hexdigest()


def login_page(error=""):
    msg = f'<p class="err">{html.escape(error)}</p>' if error else ""
    return f"""<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>VAST · sign in</title>
<style>body{{margin:0;height:100vh;display:grid;place-items:center;background:#0c0e13;color:#e6e9f0;
font:14px/1.5 -apple-system,Segoe UI,Roboto,sans-serif}}form{{background:#141821;border:1px solid #242b3a;
border-radius:14px;padding:26px;width:320px;box-shadow:0 20px 60px rgba(0,0,0,.5)}}h1{{font-size:17px;margin:0 0 4px}}
p{{color:#8b93a7;margin:0 0 16px;font-size:12px}}input{{width:100%;box-sizing:border-box;background:#1a1f2b;
border:1px solid #242b3a;border-radius:9px;padding:10px 12px;color:#e6e9f0;font:inherit;margin-bottom:12px}}
button{{width:100%;padding:10px;border-radius:9px;border:1px solid #4f8cff;background:#4f8cff;color:#fff;
font:inherit;font-weight:600;cursor:pointer}}.err{{color:#f87171;font-size:12px}}</style></head>
<body><form method="POST" action="/login"><h1>VAST dashboard</h1>
<p>Enter the dashboard token to continue.</p>{msg}
<input type="password" name="token" placeholder="Dashboard token" autofocus autocomplete="current-password">
<button type="submit">Sign in</button></form></body></html>"""


class Handler(BaseHTTPRequestHandler):
    server_version = "VastDash/1.1"

    def log_message(self, fmt, *args):
        pass

    # ------------------------------------------------------------- plumbing
    def _send(self, code, obj, ctype="application/json", cookie=None, location=None):
        body = obj if isinstance(obj, (bytes, str)) else json.dumps(obj)
        if isinstance(body, str):
            body = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        if cookie:
            self.send_header("Set-Cookie",
                             f"{COOKIE_NAME}={cookie}; Path=/; HttpOnly; SameSite=Strict; Max-Age=604800")
        if location:
            self.send_header("Location", location)
        self.end_headers()
        self.wfile.write(body)

    def _read_raw(self):
        n = int(self.headers.get("Content-Length") or 0)
        return self.rfile.read(n) if n else b""

    def _read_json(self):
        try:
            return json.loads(self._read_raw().decode() or "{}")
        except Exception:  # noqa: BLE001
            return {}

    def _client_ip(self):
        return self.client_address[0] if self.client_address else "?"

    # ----------------------------------------------------------------- auth
    def _authed(self):
        if not AUTH_TOKEN:
            return True
        hdr = self.headers.get("Authorization") or ""
        if hdr.startswith("Bearer ") and hmac.compare_digest(hdr[7:].strip(), AUTH_TOKEN):
            return True
        raw = self.headers.get("Cookie") or ""
        for part in raw.split(";"):
            k, _, v = part.strip().partition("=")
            if k == COOKIE_NAME and hmac.compare_digest(v.strip(), cookie_value()):
                return True
        return False

    def _too_many_fails(self):
        ip = self._client_ip()
        now = time.time()
        hits = [t for t in _FAILS.get(ip, []) if now - t < 300]
        _FAILS[ip] = hits
        return len(hits) >= 10

    def _note_fail(self):
        _FAILS.setdefault(self._client_ip(), []).append(time.time())

    # ------------------------------------------------------------------ GET
    def do_GET(self):
        path = self.path.split("?", 1)[0]
        qs = urllib.parse.parse_qs(self.path.split("?", 1)[1]) if "?" in self.path else {}

        if path == "/healthz":
            self._send(200, {"ok": True})
            return

        # one-shot token login via ?token=...
        if AUTH_TOKEN and "token" in qs and path in ("/", "/index.html"):
            if hmac.compare_digest(qs["token"][0], AUTH_TOKEN):
                self._send(302, b"", "text/plain", cookie=cookie_value(), location="/")
            else:
                self._note_fail()
                self._send(401, login_page("Invalid token."), "text/html")
            return

        if not self._authed():
            if path in ("/", "/index.html"):
                self._send(401, login_page(), "text/html")
            else:
                self._send(401, {"error": "unauthorized"})
            return

        if path in ("/", "/index.html"):
            try:
                self._send(200, open(INDEX, "rb").read(), "text/html")
            except FileNotFoundError:
                self._send(404, {"error": "index.html missing"})
            return
        if path == "/api/summary":
            self._send(200, get_summary())
            return
        if path == "/api/instances":
            st, d = get_instances()
            self._send(200 if st == 200 else 502, d)
            return
        if path == "/api/offers":
            try:
                limit = min(int(qs.get("limit", ["60"])[0]), 200)
            except ValueError:
                limit = 60
            body = {"type": "ondemand", "rentable": {"eq": True}, "verified": {"eq": True},
                    "order": [["dph_total", "asc"]], "limit": limit}
            st, d = req("POST", "/bundles/", body=body)
            offs = d.get("offers", []) if isinstance(d, dict) else []
            self._send(200, {"offers": offs[:limit]})
            return
        if path == "/api/logs":
            iid = qs.get("id", [""])[0]
            if not iid.isdigit():
                self._send(400, {"error": "id required"})
                return
            st, d = req("PUT", f"/instances/request_logs/{iid}/", body={"tail": "100"})
            if st != 200 or not isinstance(d, dict) or not d.get("temp_download_url"):
                self._send(502, d if isinstance(d, dict) else {"error": "logs unavailable"})
                return
            time.sleep(3)
            try:
                with urllib.request.urlopen(d["temp_download_url"], timeout=60) as resp:
                    txt = resp.read().decode(errors="replace")
                self._send(200, {"logs": txt[-12000:]})
            except Exception as e:  # noqa: BLE001
                self._send(502, {"error": str(e)})
            return
        self._send(404, {"error": "not found"})

    # ----------------------------------------------------------------- POST
    def do_POST(self):
        path = self.path.split("?", 1)[0]

        if path == "/login":
            if not AUTH_TOKEN:
                self._send(302, b"", "text/plain", location="/")
                return
            if self._too_many_fails():
                self._send(429, login_page("Too many attempts, wait 5 minutes."), "text/html")
                return
            form = urllib.parse.parse_qs(self._read_raw().decode(errors="replace"))
            supplied = (form.get("token") or [""])[0]
            if supplied and hmac.compare_digest(supplied, AUTH_TOKEN):
                self._send(302, b"", "text/plain", cookie=cookie_value(), location="/")
            else:
                self._note_fail()
                self._send(401, login_page("Invalid token."), "text/html")
            return

        if not self._authed():
            self._send(401, {"error": "unauthorized"})
            return

        if path != "/api/action":
            self._send(404, {"error": "not found"})
            return

        b = self._read_json()
        action, iid = b.get("action"), b.get("id")
        confirm = b.get("confirm") is True
        if action not in ("stop", "start", "destroy") or not iid:
            self._send(400, {"error": "invalid action or id"})
            return
        if not confirm:
            self._send(409, {"error": "confirm required", "need_confirm": True})
            return
        if action in ("stop", "start"):
            st, d = req("PUT", f"/instances/{iid}/",
                        body={"state": "stopped" if action == "stop" else "running"})
        else:
            st, d = req("DELETE", f"/instances/{iid}/")
        self._send(200, {"status": st, "action": action, "id": iid, "result": d})


# ------------------------------------------------------------------------ main
def main():
    global API_KEY, AUTH_TOKEN
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default=os.environ.get("VAST_DASH_HOST", "0.0.0.0"))
    ap.add_argument("--port", type=int, default=int(os.environ.get("VAST_DASH_PORT", "8090")))
    ap.add_argument("--key", default=None)
    ap.add_argument("--token", default=os.environ.get("VAST_DASH_TOKEN"))
    ap.add_argument("--insecure", action="store_true",
                    help="allow binding a public address with no dashboard token")
    a = ap.parse_args()

    API_KEY = a.key or load_key()
    if not API_KEY:
        sys.exit("no VASTAI_API key found (use --key, env, or .a0proj/secrets.env)")
    AUTH_TOKEN = (a.token or "").strip() or None

    loopback = a.host in ("127.0.0.1", "localhost", "::1")
    if not AUTH_TOKEN and not loopback and not a.insecure:
        sys.exit("refusing to bind %s without VAST_DASH_TOKEN "
                 "(set a token, bind 127.0.0.1, or pass --insecure)" % a.host)

    srv = ThreadingHTTPServer((a.host, a.port), Handler)
    print(f"Vast.ai dashboard -> http://{a.host}:{a.port}")
    print(f"  api key: {len(API_KEY)} chars (server-side only)")
    print(f"  auth: {'ON (token required)' if AUTH_TOKEN else 'OFF — localhost only'}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.server_close()


if __name__ == "__main__":
    main()
