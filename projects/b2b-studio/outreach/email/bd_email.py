"""BIG DOGMA email design system: tokens, components and a renderer for outreach emails (HTML + plain-text part).

Layout: 600 px single column, dark (the brand is gold on black), table-based with inline styles so it holds up in Gmail,
Outlook, Apple Mail and phones. Web fonts are not used in the body (most clients drop them): the wordmark is an image,
text is Arial/Helvetica. Images are hosted (bigdogma.tech/email/ for brand assets, the company's private page folder
for its film thumbnails) and every image has alt text, so the email still reads with images blocked.

Usage: html, text = render(content) with content = dict(
    lang, preheader, greeting, paras=[...], films=[dict(title, meta, img, href)], cta=dict(label, href),
    note, sign=dict(name, role), optout)
Paragraph strings may contain {link} which becomes the CTA link inline.
"""
import html as _h

# ------------------------------------------------------------------ tokens
T = dict(
    bg="#0b0b0d",        # page background
    card="#141418",      # content card
    line="#26262c",      # hairlines
    fg="#f2f2f4",        # body text
    mu="#a2a2ad",        # secondary text
    gold="#f2c14e",      # accent: buttons, links, brand line
    ink="#0b0b0d",       # text on gold
    font="Arial,Helvetica,sans-serif",
    size="16px", lh="1.6",
    w=600, pad=32,
)
ASSETS = "https://bigdogma.tech/email"
E = lambda s: _h.escape(s, quote=True)


# ------------------------------------------------------------------ components
def logo(name, w, h):   # transparent lockup pair: white letters for the dark design, near-black letters for light mode
    st = f'display:block;width:{w}px;height:auto;border:0;color:{T["gold"]};font:700 16px {T["font"]}'
    return (f'<a href="https://bigdogma.tech" style="text-decoration:none"><img class="xdk" src="{ASSETS}/{name}.png" width="{w}" height="{h}" alt="BIG DOGMA · AI STUDIO | MK" style="{st}">'
            f'<!--[if !mso]><!--><div class="xlt" style="display:none;max-height:0;overflow:hidden;mso-hide:all">'
            f'<img src="{ASSETS}/{name}_light.png" width="{w}" height="{h}" alt="BIG DOGMA · AI STUDIO | MK" style="{st}"></div><!--<![endif]--></a>')


def header():   # BD mark + BIG / DOGMA + AI STUDIO | MK (as wide as DOGMA)
    return f'<tr><td class="xbg" style="padding:6px 4px 20px;background:{T["bg"]}">{logo("bd_logo_header", 220, 84)}</td></tr>'


def para(t, link=None):
    t = E(t)
    if link and "{link}" in t:
        t = t.replace("{link}", f'<a href="{E(link)}" class="xgd" style="color:{T["gold"]};text-decoration:underline">{E(link.split("://")[-1].rstrip("/"))}</a>')
    return f'<p class="xfg" style="margin:0 0 18px;font:{T["size"]}/{T["lh"]} {T["font"]};color:{T["fg"]}">{t}</p>'


def films(items):
    if not items: return ""
    cells = []
    for f in items:
        cells.append(
            f'<td class="col" width="50%" valign="top" style="padding:0 6px">'
            f'<a href="{E(f["href"])}" style="text-decoration:none"><img src="{E(f["img"])}" width="262" alt="{E(f["title"])} (видео)" '
            f'style="display:block;width:100%;height:auto;border:0;border-radius:10px"></a>'
            f'<p class="xfg" style="margin:10px 0 0;font:700 15px/1.35 {T["font"]};color:{T["fg"]}">{E(f["title"])}</p>'
            f'<p class="xmu" style="margin:2px 0 0;font:13px/1.4 {T["font"]};color:{T["mu"]}">{E(f.get("meta", ""))}</p></td>')
    return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:4px 0 22px"><tr>'
            + "".join(cells) + '</tr></table>')


def button(label, href):   # bulletproof button (VML-free; padding on the <a> works in all current clients)
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" style="margin:6px 0 24px"><tr>'
            f'<td style="border-radius:999px;background:{T["gold"]}"><a href="{E(href)}" '
            f'style="display:inline-block;padding:14px 26px;font:700 16px/1 {T["font"]};color:{T["ink"]};text-decoration:none;border-radius:999px">'
            f'{E(label)} &rarr;</a></td></tr></table>')


def note(t):
    return (f'<p class="xnote" style="margin:0 0 22px;padding:14px 16px;border-left:3px solid {T["gold"]};background:#1b1b21;'
            f'font:14px/1.55 {T["font"]};color:{T["mu"]}">{E(t)}</p>')


def signature(s):   # Name, the role under it (smaller, grey), the BD lockup, then contacts
    who = (f'<p class="xfg" style="margin:0;font:700 15px/1.4 {T["font"]};color:{T["fg"]}">{E(s["name"])}</p>' if s.get("name") else "")
    if s.get("role"): who += f'<p class="xmu" style="margin:1px 0 0;font:13px/1.4 {T["font"]};color:{T["mu"]}">{E(s["role"])}</p>'
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" style="margin:8px 0 0;width:100%"><tr><td class="xln" style="padding-top:18px;border-top:1px solid {T["line"]}">'
            + (f'<div style="margin:0 0 12px">{who}</div>' if who else "")
            + logo("bd_logo_sig", 150, 58) +
            f'<p class="xmu" style="margin:10px 0 0;font:13px/1.5 {T["font"]};color:{T["mu"]}">'
            f'<a href="mailto:inf.unit@bigdogma.tech" class="xmu" style="color:{T["mu"]};text-decoration:none">inf.unit@bigdogma.tech</a> &middot; '
            f'<a href="https://bigdogma.tech" class="xmu" style="color:{T["mu"]};text-decoration:none">bigdogma.tech</a></p></td></tr></table>')


def footer(t):
    return (f'<tr><td class="xbg xft" style="padding:18px {T["pad"]}px 28px;background:{T["bg"]};font:12px/1.5 {T["font"]};color:#6e6e78;text-align:center">'
            f'{E(t)}</td></tr>')


# ------------------------------------------------------------------ page
def render(c):
    link = c["cta"]["href"]
    body = "".join(para(p, link) for p in c["paras"][:2])
    body += films(c.get("films"))
    body += button(c["cta"]["label"], link)
    body += "".join(para(p, link) for p in c["paras"][2:])
    if c.get("note"): body += note(c["note"])
    body += para(c.get("closing", "Со почит,")) + signature(c["sign"])
    pre = (f'<div style="display:none;max-height:0;overflow:hidden;opacity:0;color:transparent">{E(c["preheader"])}'
           + "&#847; &zwnj; " * 40 + '</div>')
    html = f'''<!doctype html><html lang="{c["lang"]}" xmlns="http://www.w3.org/1999/xhtml"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark"><meta name="supported-color-schemes" content="light dark">
<title>{E(c.get("subject", "BIG DOGMA"))}</title>
<style>body{{margin:0;padding:0;background:{T["bg"]}}}a{{color:{T["gold"]}}}
/* light mode (Apple Mail, iOS Mail, Outlook for Mac and others that support it): white card, dark text, the black-letter logo.
   Clients without prefers-color-scheme (Gmail) keep the dark design, where the white-letter logo is correct. */
@media (prefers-color-scheme: light){{.xbg{{background:#f3f3f5!important}}.xcard{{background:#ffffff!important;border-color:#e4e4e8!important}}
.xfg{{color:#16161a!important}}.xmu{{color:#5b5b66!important}}.xgd{{color:#9a6d0a!important}}.xft{{color:#8a8a94!important}}.xln{{border-color:#e4e4e8!important}}
.xnote{{background:#faf6ea!important;color:#4a4a52!important}}.xdk{{display:none!important}}.xlt{{display:block!important;max-height:none!important;overflow:visible!important}}}}
@media(max-width:620px){{.wrap{{width:100%!important}}.in{{padding:24px 20px!important}}.col{{display:block!important;width:100%!important;padding:0 0 16px!important}}}}</style></head>
<body class="xbg" style="margin:0;padding:0;background:{T["bg"]}">{pre}
<table role="presentation" class="xbg" width="100%" cellpadding="0" cellspacing="0" style="background:{T["bg"]}"><tr><td align="center" style="padding:24px 12px">
<table role="presentation" class="wrap" width="{T["w"]}" cellpadding="0" cellspacing="0" style="width:{T["w"]}px;max-width:100%">
{header()}
<tr><td class="in xcard" style="padding:{T["pad"]}px;background:{T["card"]};border-radius:14px;border:1px solid {T["line"]}">
{para(c["greeting"])}{body}
</td></tr>
{footer(c["optout"])}
</table></td></tr></table></body></html>'''
    # plain-text part (same words, links written out)
    tx = [c["greeting"], ""] + [p.replace("{link}", link) for p in c["paras"][:2]] + [""]
    tx += [f'- {f["title"]} ({f.get("meta", "")})' for f in c.get("films", [])] + ["", f'{c["cta"]["label"]}: {link}', ""]
    tx += [p.replace("{link}", link) for p in c["paras"][2:]] + ([c["note"]] if c.get("note") else [])
    tx += ["", c.get("closing", "Со почит,")] + [x for x in (c["sign"].get("name"), c["sign"].get("role")) if x]
    tx += ["BIG DOGMA · AI STUDIO | MK", "inf.unit@bigdogma.tech · bigdogma.tech", "", c["optout"]]
    return html, "\n".join(tx)
