# Sector bundles on the pitch pages: which bundles fit each company, and the HTML/CSS for the offer section.
import json, html
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
BUND = json.load(open(f"{S}/cut/bundles.json"))
FIT = {"01_zito_marketi_MK": ["b5", "b6"], "02_alkaloid_MK": ["b6"], "03_replek_MK": ["b6"], "04_vincinni_MK": ["b5"], "05_foton_MK": [],
       "06_beograd_na_vodi_RS": ["b1", "b2"], "07_millennium_team_RS": ["b4", "b6"], "08_nelt_RS": ["b6"], "09_gener2_AL": ["b1", "b2"],
       "10_concord_AL": ["b1", "b2"], "11_viva_fresh_XK": ["b5", "b6"], "12_speeex_XK": ["b6"], "13_telekom_MK": ["b5", "b6"]}
CSS = ".bh{font-size:clamp(22px,2.4vw,30px);margin:56px 0 0} .price.bund{margin-top:22px} @media(min-width:900px){.price.bund{grid-template-columns:repeat(auto-fit,minmax(300px,1fr))}} .price.bund .u{display:block;font-size:13px;color:var(--mu);margin-top:4px}"
def block(cid, lang):
    ks = FIT.get(cid, [])
    if not ks: return ""
    b = BUND[lang]; E = html.escape
    cards = "".join(f'<div class="card rv"><h3>{E(b[k]["n"])}</h3><div class="amt">{E(b[k]["a"])}</div><span class="u">{E(b[k]["u"])}</span><p>{E(b[k]["d"])}</p></div>' for k in ks)
    return f'<h3 class="bh rv">{E(b["head"])}</h3><div class="price bund">{cards}</div>'
