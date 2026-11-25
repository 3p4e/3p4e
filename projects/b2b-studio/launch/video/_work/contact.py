# Contact details for every asset that shows them, read from brand/brand.json. Only non-empty fields are used.
# If a value still looks like a placeholder (example.* domain or XXX digits), outputs get a _PLACEHOLDER-CONTACT suffix
# so they cannot be mistaken for publish-ready files.
import json
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
def contact():
    B = json.load(open(f"{S}/brand/brand.json", encoding="utf-8"))
    items = [str(B.get(k) or "").strip() for k in ("phone", "email", "web")]
    items = [x for x in items if x]
    placeholder = any("example." in x.lower() or "XXX" in x.upper() for x in items)
    return items, placeholder
ITEMS, PLACEHOLDER = contact()
SUFFIX = "_PLACEHOLDER-CONTACT" if PLACEHOLDER else ""
