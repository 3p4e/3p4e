# BIG DOGMA outreach kit: per company (local language) cold email, LinkedIn note, WhatsApp message, two follow-ups,
# plus a tracker spreadsheet. Links are the private LTX pitch pages. H3 material is never sent by email or uploaded.
import os, json, ast, csv
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
# PRIVATE=1 writes the real private page links to S/outreach_private (never committed); the repo copy gets a placeholder.
PRIVATE = os.environ.get("PRIVATE") == "1"
OUT = f"{S}/outreach_private" if PRIVATE else "/home/user/3p4e/projects/b2b-studio/outreach"; os.makedirs(OUT, exist_ok=True)
O = json.load(open(f"{S}/cut/offers.json")); B = json.load(open(f"{S}/brand/brand.json")); TOK = json.load(open(f"{S}/cut/page_tokens.json"))
V1 = ast.parse(open(f"{S}/cut/gen_sites_v1.py").read()); NS = {}
for n in V1.body:
    if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") in ("CO", "SEC"): NS[n.targets[0].id] = eval(compile(ast.Expression(n.value), "v1", "eval"))
CO, SEC = NS["CO"], NS["SEC"]
BASE = "https://pitch.bigdogma.tech"
ROLE = {"01_zito_marketi_MK": "Marketing Director / Head of Marketing", "02_alkaloid_MK": "Corporate Communications Director; HR / Employer Branding",
        "03_replek_MK": "Marketing Manager; Export Business Development", "04_vincinni_MK": "Brand Manager Vincinni; Marketing Director (Makprogres)",
        "05_foton_MK": "Sales Director / Marketing Manager (Foton importer)", "06_beograd_na_vodi_RS": "Sales & Marketing Director",
        "07_millennium_team_RS": "Marketing & PR; Business Development", "08_nelt_RS": "Marketing / Corporate Communications Director",
        "09_gener2_AL": "Marketing Director; Sales Director", "10_concord_AL": "Sales & Marketing Manager", "11_viva_fresh_XK": "Marketing Director",
        "12_speeex_XK": "HR Director / Employer Branding Lead"}
COUNTRY = {"MK": "North Macedonia", "RS": "Serbia", "AL": "Albania", "XK": "Kosovo"}
SIG = f"{B['name']} · {B['subline'].replace('  ', ' ')}\n" + " · ".join(x for x in (B["phone"], B["email"], B["web"]) if x)
T = {
 "mk": dict(
  subj="{c}: два кратки AI филма, направени само за вас (концепт)",
  email="""Почитувани,

Подготвивме два кратки рекламни филма за {c}: концепт само за вас, изработен со вештачка интелигенција за неколку дена, без снимање.

{hook}

Погледнете ги тука (приватна страница, 2 минути): {link}

Секој филм е готов во хоризонтален (16:9) и вертикален (9:16) формат, со глас на македонски и оригинална музика. Ништо од ова не е објавено и нема да биде без ваше писмено одобрение.

Ако ви се допаѓа насоката, би сакале за 15 минути да ви покажеме како изгледа истото со ваши вистински фотографии и производи. Пилот-филм чини од {pilot}.

Со почит,
[Име и презиме]
{sig}""",
  li="Добар ден, [Име]. Направивме два кратки AI рекламни филма за {c}, концепт само за вас, без снимање. Приватна страница: {link} Би ми било драго да го слушнам вашето мислење.",
  wa="Добар ден! Јас сум [Име] од BIG DOGMA, AI видео студио од Скопје. Подготвивме два кратки рекламни филма за {c} (концепт, необјавени): {link} Дали имате 15 минути оваа или следната недела да ви покажеме како би изгледало со ваши материјали?",
  fu1="""Почитувани,

Само кратко потсетување за концепт-филмовите за {c}: {link}

Ако не сте вистинската личност за ова, ќе ни биде драго ако нè упатите до колегата задолжен за маркетинг.

Со почит,
[Име и презиме]
{sig}""",
  fu2="""Почитувани,

Ова е нашата последна порака на оваа тема. Страницата со филмовите останува активна уште 14 дена: {link}

Ако сега не е вистинскиот момент, ќе ви се јавиме за неколку месеци.

Со почит,
[Име и презиме]
{sig}"""),
 "sr": dict(
  subj="{c}: dva kratka AI filma napravljena samo za vas (koncept)",
  email="""Poštovani,

Pripremili smo dva kratka reklamna filma za {c}: koncept samo za vas, napravljen uz pomoć veštačke inteligencije za nekoliko dana, bez snimanja.

{hook}

Pogledajte ih ovde (privatna stranica, 2 minuta): {link}

Svaki film je spreman u horizontalnom (16:9) i vertikalnom (9:16) formatu, sa glasom na srpskom i originalnom muzikom. Ništa od ovoga nije objavljeno i neće biti bez vašeg pisanog odobrenja.

Ako vam se dopada pravac, rado bismo vam za 15 minuta pokazali kako to izgleda sa vašim pravim fotografijama i proizvodima. Pilot-film košta od {pilot}.

Srdačan pozdrav,
[Ime i prezime]
{sig}""",
  li="Dobar dan, [Ime]. Napravili smo dva kratka AI reklamna filma za {c}, koncept samo za vas, bez snimanja. Privatna stranica: {link} Bilo bi mi drago da čujem vaše mišljenje.",
  wa="Dobar dan! Ja sam [Ime] iz BIG DOGMA, AI video studija iz Skoplja. Pripremili smo dva kratka reklamna filma za {c} (koncept, neobjavljeni): {link} Da li imate 15 minuta ove ili sledeće nedelje da vam pokažemo kako bi izgledalo sa vašim materijalima?",
  fu1="""Poštovani,

Samo kratak podsetnik na koncept-filmove za {c}: {link}

Ako niste prava osoba za ovo, biće nam drago ako nas uputite na kolegu zaduženog za marketing.

Srdačan pozdrav,
[Ime i prezime]
{sig}""",
  fu2="""Poštovani,

Ovo je naša poslednja poruka na ovu temu. Stranica sa filmovima ostaje aktivna još 14 dana: {link}

Ako sada nije pravi trenutak, javićemo vam se za nekoliko meseci.

Srdačan pozdrav,
[Ime i prezime]
{sig}"""),
 "sq": dict(
  subj="{c}: dy filma të shkurtër AI, të krijuar vetëm për ju (koncept)",
  email="""Të nderuar,

Kemi përgatitur dy filma të shkurtër reklamues për {c}: një koncept vetëm për ju, i krijuar me inteligjencë artificiale për pak ditë, pa xhirime.

{hook}

Shikojini këtu (faqe private, 2 minuta): {link}

Çdo film është gati në format horizontal (16:9) dhe vertikal (9:16), me zë në shqip dhe muzikë origjinale. Asgjë nga kjo nuk është publikuar dhe nuk do të publikohet pa miratimin tuaj me shkrim.

Nëse ju pëlqen drejtimi, do të na vinte mirë t'ju tregonim për 15 minuta si duket e njëjta gjë me fotot dhe produktet tuaja të vërteta. Një film pilot kushton nga {pilot}.

Me respekt,
[Emri dhe mbiemri]
{sig}""",
  li="Përshëndetje, [Emri]. Kemi krijuar dy filma të shkurtër reklamues me AI për {c}, koncept vetëm për ju, pa xhirime. Faqja private: {link} Do të më vinte mirë të dëgjoja mendimin tuaj.",
  wa="Përshëndetje! Jam [Emri] nga BIG DOGMA, studio video AI nga Shkupi. Kemi përgatitur dy filma të shkurtër reklamues për {c} (koncept, të papublikuar): {link} A keni 15 minuta këtë javë ose javën e ardhshme që t'ju tregojmë si do të dukej me materialet tuaja?",
  fu1="""Të nderuar,

Vetëm një kujtesë e shkurtër për filmat koncept për {c}: {link}

Nëse nuk jeni personi i duhur për këtë, do të na vinte mirë nëse na drejtoni te kolegu përgjegjës për marketingun.

Me respekt,
[Emri dhe mbiemri]
{sig}""",
  fu2="""Të nderuar,

Ky është mesazhi ynë i fundit për këtë temë. Faqja me filmat mbetet aktive edhe 14 ditë: {link}

Nëse tani nuk është momenti i duhur, do t'ju kontaktojmë pas disa muajsh.

Me respekt,
[Emri dhe mbiemri]
{sig}""")}
LBL = {"mk": ("Е-пошта", "LinkedIn", "WhatsApp", "Потсетник (ден 4)", "Последна порака (ден 10)", "Наслов"),
       "sr": ("E-pošta", "LinkedIn", "WhatsApp", "Podsetnik (dan 4)", "Poslednja poruka (dan 10)", "Naslov"),
       "sq": ("Email", "LinkedIn", "WhatsApp", "Kujtesë (dita 4)", "Mesazhi i fundit (dita 10)", "Subjekti")}
rows = []
for c in O["companies"]:
    L = c["lang"]; t = T[L]; sec = CO[c["id"]][0]; hook = SEC[(sec, L)][0]; link = f"{BASE}/{TOK[c['id']]}/" if PRIVATE else "[PITCH_PAGE_LINK]"
    pilot = O["prices"][L]["pilot"].split("–")[0]
    f = dict(c=c["name"], hook=hook, link=link, pilot=pilot, sig=SIG)
    msg = {k: v.format(**f) for k, v in t.items()}
    assert len(msg["li"]) <= 300, (c["id"], len(msg["li"]))
    l = LBL[L]
    md = f"""# {c['name']} · outreach ({L.upper()})

- Country: {COUNTRY[c['id'][-2:]]} · Sector: {sec} · Language: {L}
- Who to contact: **{ROLE[c['id']]}**
- Private page (LTX films only): {link}
- Offer PDF: on the page (button), or attach `offers_pdf/{c['id']}_offer.pdf`
- Films: {", ".join(lbl for _, lbl in c['films'])}

## 1. {l[0]} (day 0)
**{l[5]}:** {msg['subj']}

```
{msg['email']}
```

## 2. {l[1]} (day 0, connection note, {len(msg['li'])} characters)
```
{msg['li']}
```

## 3. {l[2]} (only if you already have the number from a business card, website or referral)
```
{msg['wa']}
```

## 4. {l[3]}
**{l[5]}:** Re: {msg['subj']}

```
{msg['fu1']}
```

## 5. {l[4]}
**{l[5]}:** Re: {msg['subj']}

```
{msg['fu2']}
```
"""
    open(f"{OUT}/{c['id']}.md", "w").write(md)
    rows.append([c["id"][:2], c["name"], COUNTRY[c["id"][-2:]], L, sec, ROLE[c["id"]], link, msg["subj"]])
# tracker
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.datavalidation import DataValidation
wb = Workbook(); ws = wb.active; ws.title = "Tracker"
hdr = ["#", "Company", "Country", "Lang", "Sector", "Who to contact (role)", "Contact name", "Email", "LinkedIn URL", "Phone",
       "Pitch page", "Email subject", "Day 0 sent", "Follow-up 1 due", "Follow-up 2 due", "Status", "Meeting date", "Notes"]
ws.append(hdr)
for i, r in enumerate(rows, start=2):
    ws.append(r[:6] + ["", "", "", ""] + [r[6], r[7], None, f'=IF(M{i}="","",M{i}+4)', f'=IF(M{i}="","",M{i}+10)', "Not contacted", None, ""])
    for col in ("M", "N", "O", "Q"): ws[f"{col}{i}"].number_format = "yyyy-mm-dd"
    ws[f"K{i}"].hyperlink = r[6]; ws[f"K{i}"].font = Font(color="0563C1", underline="single")
dv = DataValidation(type="list", formula1='"Not contacted,Sent,Follow-up 1 sent,Follow-up 2 sent,Replied,Meeting booked,Proposal sent,Won,Lost,Later"', allow_blank=True)
ws.add_data_validation(dv); dv.add(f"P2:P{len(rows)+1}")
for c in ws[1]: c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor="0D0D0F"); c.alignment = Alignment(vertical="center", wrap_text=True)
widths = [4, 22, 14, 6, 12, 34, 22, 26, 30, 16, 44, 46, 12, 14, 14, 18, 13, 30]
for i, w in enumerate(widths): ws.column_dimensions[chr(65 + i)].width = w
ws.freeze_panes = "C2"; ws.auto_filter.ref = f"A1:R{len(rows)+1}"
wb.save(f"{OUT}/outreach_tracker.xlsx")
with open(f"{OUT}/outreach_tracker.csv", "w", newline="") as fh: csv.writer(fh).writerows([hdr[:6] + ["Pitch page", "Email subject"]] + [r for r in rows])
print("OUTREACH_DONE", len(rows))
