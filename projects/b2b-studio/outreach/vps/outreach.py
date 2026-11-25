#!/usr/bin/env python3
"""BIG DOGMA outreach sender. Runs on the Mumbai VPS in /opt/outreach (chmod 700), sends as inf.unit@bigdogma.tech
through the Hostinger mailbox (SMTP 465), keeps a copy in the mailbox's Sent folder (IMAP) and stops follow-ups for
anyone who has replied.

Files in /opt/outreach:
  config.env       SENDER_NAME, FROM, SMTP/IMAP hosts, quiet hours (no secrets)
  .smtp_pass       the mailbox password, one line, chmod 600 (written by the owner, never printed)
  recipients.csv   cid,email,contact_name,greeting  (one row per company; empty email = skipped)
  emails/<cid>.json  subject + body for step 1 (day 0), 4 (day 4) and 5 (day 10), parsed from the private outreach files
  state.json       what was sent when, Message-IDs, replies (written by this script)
  outreach.log     one line per action

Commands:
  outreach.py check                      log in to SMTP and IMAP, list folders, show what is ready
  outreach.py preview <cid> [step]       print the email exactly as it would be sent
  outreach.py test <your-address> [cid]  send the day-0 email of one company to your own address (state untouched)
  outreach.py send [--only cid,cid] [--dry-run]   send the day-0 email to every recipient not contacted yet
  outreach.py followups [--dry-run]      send the day-4 / day-10 reminders that are due (skips anyone who replied)
  outreach.py status                     table of every company
  outreach.py stop <cid>                 no more emails to this company (e.g. they answered by phone)
"""
import os, sys, csv, json, time, random, ssl, smtplib, imaplib, email.utils, datetime, re
from email.message import EmailMessage
from email.header import decode_header

D = os.path.dirname(os.path.abspath(__file__))
STEPS = {"1": 0, "4": 4, "5": 10}            # outreach step -> day after the first email
SIGN = ("[Ime i prezime]", "[Име и презиме]", "[Emri dhe mbiemri]")


def cfg():
    c = {"FROM": "inf.unit@bigdogma.tech", "SENDER_NAME": "", "SMTP_HOST": "smtp.hostinger.com", "SMTP_PORT": "465",
         "IMAP_HOST": "imap.hostinger.com", "IMAP_PORT": "993", "SEND_HOURS": "9-16", "TZ": "Europe/Skopje",
         "PAUSE_MIN": "70", "PAUSE_MAX": "160", "ATTACH_PDF": "no", "PITCH_SITE": "/opt/stacks/ai-studio-pitch/site"}
    p = f"{D}/config.env"
    if os.path.exists(p):
        for line in open(p, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1); c[k.strip()] = v.strip().strip('"')
    return c


def password():
    p = f"{D}/.smtp_pass"
    if not os.path.exists(p): sys.exit("No password yet: write it to /opt/outreach/.smtp_pass (see README.md).")
    if os.stat(p).st_mode & 0o077: os.chmod(p, 0o600)
    pw = open(p, encoding="utf-8").read().strip()
    if not pw: sys.exit(".smtp_pass is empty")
    return pw


def log(msg):
    line = f"{datetime.datetime.utcnow():%Y-%m-%d %H:%M:%S}Z {msg}"
    print(line); open(f"{D}/outreach.log", "a", encoding="utf-8").write(line + "\n")


def load_state():
    p = f"{D}/state.json"
    return json.load(open(p)) if os.path.exists(p) else {}


def save_state(s):
    tmp = f"{D}/state.json.tmp"; json.dump(s, open(tmp, "w"), indent=1, ensure_ascii=False); os.replace(tmp, f"{D}/state.json")


def recipients():
    out = {}
    p = f"{D}/recipients.csv"
    for r in csv.DictReader(open(p, encoding="utf-8-sig")):
        extra = r.pop(None, None) or []          # an unquoted comma in the greeting ("Dear Ms X,") spills into extra fields
        if extra: r["greeting"] = ",".join([r.get("greeting") or ""] + extra)
        r = {k: (v or "").strip() for k, v in r.items()}
        if r.get("cid", "").startswith("#") or not r.get("cid"): continue
        out[r["cid"]] = r
    return out


def valid(addr): return bool(re.fullmatch(r"[^@\s,;<>]+@[^@\s,;<>]+\.[a-zA-Z]{2,}", addr or ""))


def compose(c, cid, step, rcp, state):
    E = json.load(open(f"{D}/emails/{cid}.json", encoding="utf-8"))[step]
    body = E["body"]
    for s in SIGN: body = body.replace(s, c["SENDER_NAME"])
    if rcp.get("greeting"): body = rcp["greeting"] + "\n" + body.split("\n", 1)[1]
    left = re.findall(r"\[[^\]]{2,30}\]", body)
    if left: raise SystemExit(f"{cid}: placeholder left in the text: {left}")
    m = EmailMessage()
    m["From"] = email.utils.formataddr((f"{c['SENDER_NAME']} · BIG DOGMA" if c["SENDER_NAME"] else "BIG DOGMA", c["FROM"]))
    m["To"] = email.utils.formataddr((rcp.get("contact_name", ""), rcp["email"]))
    m["Subject"] = E["subject"]; m["Date"] = email.utils.formatdate(localtime=False)
    m["Message-ID"] = email.utils.make_msgid(domain="bigdogma.tech"); m["Reply-To"] = c["FROM"]
    first = state.get(cid, {}).get("sent", {}).get("1", {}).get("msgid")
    if step != "1" and first: m["In-Reply-To"] = first; m["References"] = first
    m.set_content(body)
    if step == "1" and c["ATTACH_PDF"].lower() == "yes":
        tok = json.load(open(f"{D}/page_tokens.json"))[cid]; pdf = f"{c['PITCH_SITE']}/{tok}/offer.pdf"
        m.add_attachment(open(pdf, "rb").read(), maintype="application", subtype="pdf", filename=f"BIG_DOGMA_{cid}_offer.pdf")
    return m


def smtp(c):
    s = smtplib.SMTP_SSL(c["SMTP_HOST"], int(c["SMTP_PORT"]), context=ssl.create_default_context(), timeout=60)
    s.login(c["FROM"], password()); return s


def imap(c):
    i = imaplib.IMAP4_SSL(c["IMAP_HOST"], int(c["IMAP_PORT"]), ssl_context=ssl.create_default_context())
    i.login(c["FROM"], password()); return i


def sent_folder(i):
    typ, data = i.list()
    for raw in data or []:
        line = raw.decode(errors="replace")
        if "\\Sent" in line: return line.rsplit(" ", 1)[-1].strip('"')
    for raw in data or []:
        name = raw.decode(errors="replace").rsplit(" ", 1)[-1].strip('"')
        if name.lower().endswith("sent"): return name
    return None


def keep_copy(c, m):
    try:
        i = imap(c); f = sent_folder(i)
        if f: i.append(f'"{f}"', "\\Seen", imaplib.Time2Internaldate(time.time()), m.as_bytes())
        i.logout()
    except Exception as e: log(f"WARN could not save a copy in Sent: {e}")


def replied(c, rcp, state, cid):
    """True if the mailbox has a message from the recipient's address (or, for a company domain, from that domain)
    received after the first email."""
    first = state.get(cid, {}).get("sent", {}).get("1", {}).get("at")
    if not first: return False
    since = datetime.datetime.fromisoformat(first).strftime("%d-%b-%Y")
    addr = rcp["email"].lower(); dom = addr.split("@")[1]
    free = dom in ("gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "live.com", "icloud.com", "t-home.mk", "yandex.com")
    i = imap(c)
    try:
        typ, data = i.list(); folders = []
        for raw in data or []:
            line = raw.decode(errors="replace"); name = line.rsplit(" ", 1)[-1].strip('"')
            if "\\Noselect" in line or "\\Sent" in line or "\\Drafts" in line or "\\Trash" in line or name.lower().endswith(("sent", "drafts", "trash")): continue
            folders.append(name)
        for f in folders or ["INBOX"]:
            if i.select(f'"{f}"', readonly=True)[0] != "OK": continue
            typ, hits = i.search(None, "SINCE", since, "FROM", f'"{addr if free else "@" + dom}"')
            if typ == "OK" and hits and hits[0].split(): return True
        return False
    finally:
        try: i.logout()
        except Exception: pass


def in_hours(c):
    try:
        from zoneinfo import ZoneInfo
        now = datetime.datetime.now(ZoneInfo(c["TZ"]))
    except Exception: now = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    a, b = (int(x) for x in c["SEND_HOURS"].split("-"))
    return now.weekday() < 5 and a <= now.hour < b


def deliver(c, cid, step, rcp, state, dry):
    m = compose(c, cid, step, rcp, state)
    if dry: log(f"DRY {cid} step {step} -> {rcp['email']} | {m['Subject']}"); return
    s = smtp(c); s.send_message(m); s.quit(); keep_copy(c, m)
    st = state.setdefault(cid, {}); st.setdefault("sent", {})[step] = {"at": datetime.datetime.utcnow().isoformat(timespec="seconds"),
                                                                       "to": rcp["email"], "msgid": m["Message-ID"]}
    save_state(state); log(f"SENT {cid} step {step} -> {rcp['email']} | {m['Subject']}")


def pause(c):
    t = random.randint(int(c["PAUSE_MIN"]), int(c["PAUSE_MAX"])); log(f"wait {t}s"); time.sleep(t)


def main(a):
    c = cfg(); cmd = a[0] if a else "status"; dry = "--dry-run" in a
    only = None
    if "--only" in a: only = set(a[a.index("--only") + 1].split(","))
    if cmd == "check":
        pw = password(); print("password file: ok (", len(pw), "characters )")
        s = smtp(c); print("SMTP login ok:", c["SMTP_HOST"]); s.quit()
        i = imap(c); print("IMAP login ok:", c["IMAP_HOST"], "| Sent folder:", sent_folder(i)); i.logout()
        print("sender name:", c["SENDER_NAME"] or "(MISSING: set SENDER_NAME in config.env)")
        R = recipients(); ok = [k for k, r in R.items() if valid(r.get("email"))]
        print(f"recipients with a valid email: {len(ok)} of {len(R)}", ", ".join(ok))
        bad = [k for k, r in R.items() if r.get("email") and not valid(r["email"])]
        if bad: print("INVALID email in recipients.csv:", bad)
        return
    if cmd == "preview":
        cid = a[1]; step = a[2] if len(a) > 2 else "1"; R = recipients()
        rcp = R.get(cid) or {"email": "someone@example.com"}
        if not rcp.get("email"): rcp = dict(rcp, email="someone@example.com")
        print(compose(c, cid, step, rcp, load_state()).as_string()); return
    if cmd == "test":
        to = a[1]; cid = a[2] if len(a) > 2 else "01_zito_marketi_MK"
        if not c["SENDER_NAME"]: sys.exit("Set SENDER_NAME in config.env first.")
        m = compose(c, cid, "1", {"email": to, "contact_name": ""}, {})
        m.replace_header("Subject", "[TEST] " + m["Subject"])
        s = smtp(c); s.send_message(m); s.quit(); log(f"TEST {cid} -> {to}"); return
    if cmd == "status":
        st = load_state(); R = recipients()
        for cid in sorted(R):
            x = st.get(cid, {}); sent = x.get("sent", {})
            print(f"{cid:24s} {R[cid].get('email') or '-':34s} " + " ".join(f"{k}:{v['at'][:10]}" for k, v in sorted(sent.items())) +
                  (" REPLIED" if x.get("replied") else "") + (" STOPPED" if x.get("stopped") else ""))
        return
    if cmd == "stop":
        st = load_state(); st.setdefault(a[1], {})["stopped"] = True; save_state(st); log(f"STOP {a[1]}"); return
    if cmd in ("send", "followups"):
        if not c["SENDER_NAME"]: sys.exit("Set SENDER_NAME in config.env first (it replaces [Name] in the signature).")
        if not dry and not in_hours(c) and "--now" not in a:
            log(f"outside sending hours ({c['SEND_HOURS']} {c['TZ']}, Mon-Fri): nothing sent (add --now to override)"); return
        st = load_state(); R = recipients(); todo = []
        for cid, r in sorted(R.items()):
            if only and cid not in only: continue
            if not valid(r.get("email")) or st.get(cid, {}).get("stopped") or st.get(cid, {}).get("replied"): continue
            sent = st.get(cid, {}).get("sent", {})
            if cmd == "send":
                if "1" not in sent: todo.append((cid, "1", r))
            else:
                if "1" not in sent: continue
                day0 = datetime.datetime.fromisoformat(sent["1"]["at"])
                for step in ("4", "5"):
                    if step in sent: continue
                    if datetime.datetime.utcnow() >= day0 + datetime.timedelta(days=STEPS[step]): todo.append((cid, step, r))
                    break
        if cmd == "followups":
            keep = []
            for cid, step, r in todo:
                if replied(c, r, st, cid):
                    st.setdefault(cid, {})["replied"] = True; save_state(st); log(f"REPLIED {cid}: no more reminders")
                else: keep.append((cid, step, r))
            todo = keep
        if not todo: log(f"{cmd}: nothing due"); return
        for n, (cid, step, r) in enumerate(todo):
            if n and not dry: pause(c)
            deliver(c, cid, step, r, st, dry)
        return
    print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
