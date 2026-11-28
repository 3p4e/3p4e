# Outreach sender on the Mumbai VPS (`/opt/outreach`)

Sends the 12 outreach emails as **inf.unit@bigdogma.tech** through the Hostinger mailbox (SMTP), saves a copy in the
mailbox's Sent folder, and sends the day-4 and day-10 reminders automatically (weekdays 10:23 Skopje time) unless the
company has replied. Replies arrive in the normal inf.unit inbox (Hostinger webmail).

The email texts (`emails/*.json`) are built from the private outreach files with `parse_outreach.py`; they hold the real
page links, so they live only on the server, never in this repo.

## One-time setup (owner, in the server terminal)
1. Mailbox password (typed, not shown, never in the shell history):
   `read -rs -p "inf.unit password: " P && printf '%s' "$P" > /opt/outreach/.smtp_pass && chmod 600 /opt/outreach/.smtp_pass && unset P && echo`
2. Your name for the signature: `nano /opt/outreach/config.env` -> `SENDER_NAME=First Last`
3. Contacts: `nano /opt/outreach/recipients.csv` -> one email per company (`contact_name` and `greeting` optional;
   e.g. greeting `Почитувана г-ѓо Петрова,` replaces the first line "Почитувани,").
4. `python3 /opt/outreach/outreach.py check` -> both logins ok, Sent folder found, N recipients.
5. `python3 /opt/outreach/outreach.py test you@yourmail.com` -> check the test email in your inbox (and the spam folder).

## Sending
- `outreach.py preview 06_beograd_na_vodi_RS` see one email exactly
- `outreach.py send --dry-run` list what would go out
- `outreach.py send` first emails to everyone not contacted yet (Mon-Fri 9-16, 70-160 s apart; `--only <cid>,<cid>` for some)
- reminders: automatic (`systemctl list-timers outreach-followups.timer`), or by hand `outreach.py followups`
- `outreach.py status`, `outreach.py stop <cid>` (no more emails to that company), log in `outreach.log`
