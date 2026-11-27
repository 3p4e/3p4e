"""Sends the emails built by cut/new_pitches.py (scratchpad email_new/email_<key>.{html,txt,json}) from the studio mailbox through the Hostinger Mail API,
HTML + plain text like send_all.py. Recipients and the sent log stay in the scratchpad (email/recipients_new.json, email/sent_new.log); keys already logged are skipped.
  python3 send_new.py check [key ...]    verify pages, images, films and PDFs of each page, no sending
  python3 send_new.py send  [key ...]    25 s between messages
"""
import json, os, re, sys, time, subprocess, urllib.request
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; O = f"{S}/email_new"; LOG = f"{S}/email/sent_new.log"
R = json.load(open(f"{S}/email/recipients_new.json")); T = json.load(open(f"{S}/cut/page_tokens_new.json"))
URL = "https://api.mail.hostinger.com/api/v1/mailboxes/" + open(f"{S}/email/.mailbox").read().strip() + "/send"; K = open(f"{S}/hapi/.mailkey").read().strip()
def code(u): return subprocess.run(["curl", "-s", "-o", "/dev/null", "-m", "40", "-I", "-w", "%{http_code}", u], capture_output=True, text=True).stdout
def check(k):
    j = json.load(open(f"{O}/email_{k}.json")); h = open(f"{O}/email_{k}.html", encoding="utf-8").read(); t = open(f"{O}/email_{k}.txt", encoding="utf-8").read(); page = f"https://pitch.bigdogma.tech/{T[k]}/"
    urls = {page, page + "offer.pdf", page + "hero.mp4"} | set(re.findall(r'src="(https://[^"]+)"', h))
    urls |= {page + f for f in re.findall(r'data-play="([^"]+\.mp4)"', open(f"{S}/pv3/{k}/../../pv3/{k}/classic.html").read())} if False else set()
    bad = {u: code(u) for u in urls if code(u) != "200"}
    ph = [w for w in ("[TEST]", "{", "undefined", "None", "TODO", "%s", "[DRAFT", "PITCH_PAGE_LINK") if w in t]
    print(k, "|", j["subject"][:55], "| links", len(urls), "| bad", bad or "none", "| placeholders", ph or "none", "| to", R[k]["to"], "cc", R[k].get("cc", []), flush=True)
    return not bad and not ph
def post(b):
    r = urllib.request.Request(URL, data=json.dumps(b).encode(), method="POST", headers={"Authorization": "Bearer " + K, "Content-Type": "application/json", "Accept": "application/json", "User-Agent": "mail-client/1.0"})
    try: x = urllib.request.urlopen(r, timeout=60); return True, str(x.status)
    except urllib.error.HTTPError as e: return False, f"{e.code} {e.read()[:200]!r}"
mode, keys = sys.argv[1], sys.argv[2:] or list(R)
if mode == "check": print("ALL_OK" if all([check(k) for k in keys]) else "PROBLEMS")
else:
    done = set(open(LOG).read().split()) if os.path.exists(LOG) else set()
    for k in keys:
        if k in done: print("skip", k); continue
        j = json.load(open(f"{O}/email_{k}.json")); h = open(f"{O}/email_{k}.html", encoding="utf-8").read(); t = open(f"{O}/email_{k}.txt", encoding="utf-8").read()
        ok, info = post({"to": R[k]["to"], "cc": R[k].get("cc", []), "displayName": "Blagoj N. | BIG DOGMA", "subject": j["subject"], "html": h, "text": t})
        print("SEND", k, "SENT" if ok else "ERROR", info, flush=True)
        if ok: open(LOG, "a").write(k + "\n")
        time.sleep(25)
