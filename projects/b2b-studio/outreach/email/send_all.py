"""Sends the built pitch emails (build_all.py output) from inf.unit@bigdogma.tech through the Hostinger Mail API.
Recipients live only in the scratchpad (email/recipients.json, chmod 600: {key: {"to": [...], "cc": [...]}}), never in the repo.
  test:  TEST_TO=<address> python3 send_all.py test [key ...]   -> each listed email (default: Foton) to TEST_TO, subject prefixed [TEST]
  real:  python3 send_all.py send [key ...]                     -> each company to its own recipients; keys already in sent.log are
                                                                   skipped, so a re-run never sends twice. 25 s between messages.
"""
import json, os, sys, time, urllib.request
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
O = f"{S}/email/out_all"; LOG = f"{S}/email/sent.log"
URL = "https://api.mail.hostinger.com/api/v1/mailboxes/" + open(f"{S}/email/.mailbox").read().strip() + "/send"   # mailbox id kept out of the repo
K = open(f"{S}/hapi/.mailkey").read().strip()
FROM = os.environ.get("FROM_NAME", "Blagoj N. | BIG DOGMA")

def post(body):
    r = urllib.request.Request(URL, data=json.dumps(body).encode(), method="POST",
                               headers={"Authorization": "Bearer " + K, "Content-Type": "application/json", "Accept": "application/json", "User-Agent": "mail-client/1.0"})
    try:
        x = urllib.request.urlopen(r, timeout=60); return True, f"{x.status} {x.read()[:200].decode(errors='replace')}"
    except urllib.error.HTTPError as e:
        return False, f"{e.code} {e.read()[:300].decode(errors='replace')}"

def msg(key):
    j = json.load(open(f"{O}/{key}.json"))
    return j, open(f"{O}/{key}.html").read(), open(f"{O}/{key}.txt").read()

mode, keys = sys.argv[1], sys.argv[2:]
if mode == "test":
    to = os.environ.get("TEST_TO", "").strip()
    if not to: sys.exit("set TEST_TO first")
    for k in keys or ["05_foton_MK"]:
        j, h, t = msg(k)
        ok, info = post({"to": [to], "displayName": FROM, "subject": "[TEST] " + j["subject"], "html": h, "text": t})
        print("TEST", k, "SENT" if ok else "ERROR", info[:160]); time.sleep(3)
elif mode == "send":
    R = json.load(open(f"{S}/email/recipients.json"))
    done = set(open(LOG).read().split()) if os.path.exists(LOG) else set()
    for i, k in enumerate(keys or sorted(R)):
        if k in done: print("skip (already sent)", k); continue
        rc = R[k]; j, h, t = msg(k)
        body = {"to": rc["to"], "displayName": FROM, "subject": j["subject"], "html": h, "text": t}
        if rc.get("cc"): body["cc"] = rc["cc"]
        ok, info = post(body)
        print("SEND", k, "->", len(rc["to"]), "to,", len(rc.get("cc", [])), "cc:", "SENT" if ok else "ERROR", info[:160], flush=True)
        if ok: open(LOG, "a").write(k + "\n")
        if i < len(keys or R) - 1: time.sleep(25)
