# Offer PDFs for the pages built by new_pitches.py: writes <token>/offer.html per company, then renders it to offer.pdf with Node Playwright.
#   python3 offer_pdf.py [key ...]  (default: all in page_tokens_new.json)      needs: NODE_PATH=$(npm root -g) TMPDIR=/dev/shm
import json, os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import new_pitches as N
def render(keys=None):
    T = json.load(open(f"{N.S}/cut/page_tokens_new.json")); keys = keys or list(T)
    JS = "const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({args:['--disable-dev-shm-usage']});for(const f of process.argv.slice(1)){const p=await b.newPage();await p.goto('file://'+f);await p.pdf({path:f.replace('offer.html','offer.pdf'),format:'A4',printBackground:true});}await b.close()})()"
    files = []
    for k in keys:
        c = N.CO[k]; d = f"/dev/shm/pub/{T[k]}"
        h = (f'<html lang="{c["lang"]}"><meta charset="utf-8"><style>body{{font:15px/1.5 system-ui,sans-serif;margin:40px;color:#111}}h1{{font-size:28px}}.price{{display:flex;gap:14px;flex-wrap:wrap;margin:10px 0}}'
             f'.card{{border:1px solid #ccc;border-radius:12px;padding:14px;flex:1;min-width:200px}}.amt{{font-size:22px;font-weight:700}}.tag{{font-size:11px;background:#f2c14e;padding:2px 8px;border-radius:99px}}'
             f'.eyebrow{{display:none}}.terms{{font-size:12px;color:#555}}.u{{font-size:12px;color:#555}}</style><body><h1>BIG DOGMA · AI STUDIO | MK</h1><p>{c["name"]}</p>{N.offer_section(c)}<p class="terms">inf.unit@bigdogma.tech · bigdogma.tech</p></body></html>')
        open(f"{d}/offer.html", "w", encoding="utf-8").write(h); files.append(f"{d}/offer.html")
    subprocess.run(["node", "-e", JS] + files, check=True, env=dict(os.environ, NODE_PATH=subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip(), TMPDIR="/dev/shm"))
    for f in files: os.remove(f)
    print("pdf", len(files))


if __name__ == "__main__":
    render(sys.argv[1:] or None)
