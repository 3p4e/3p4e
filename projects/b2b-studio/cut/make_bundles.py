# Sector bundles for the pitch pages: MK source (same as the studio site), translated to sr (Latin) / sq with Gemini (text only).
import json, urllib.request
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
K = open(f"{S}/.gemini_paid").read().strip(); U = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key="
MK = {
 "head": "Пакети за вашиот сектор",
 "b1": {"n": "Девелопер", "a": "€1.500–4.000", "u": "по проект", "d": "Тајмлапс на градбата од ископ до клучеви и продажен филм за станови пред изградба, во формати за огласи, мрежи и продажна канцеларија."},
 "b2": {"n": "Опремување станови", "a": "€300–800", "u": "по стан", "d": "Од празен до целосно опремен стан, направено од фотографиите на вашите станови. Пакет од 5 станови: €1.500."},
 "b4": {"n": "Тајмлапс проект", "a": "€500–2.000", "u": "по проект", "d": "Вашиот проект фаза по фаза, од почеток до готово, со вашето лого: објекти, ентериери, сончеви централи, патишта."},
 "b5": {"n": "Сезонска кампања", "a": "€2.500–6.000", "u": "по кампања", "d": "Семеен рекламен филм, филм од производството или продавницата и сезонски спотови за празници и акции."},
 "b6": {"n": "Бренд на работодавач", "a": "€1.500–3.500", "u": "по пакет", "d": "Филм за вработување, филм за вашиот тим и процес и кратки клипови за огласи за работа."},
}
txt = ("Translate this JSON from Macedonian into (a) Serbian, Latin script, ekavian and (b) Albanian, for a business pitch web page. "
       "Natural, idiomatic copywriting, same meaning, keep the euro amounts exactly as written (with the dot as thousands separator). "
       "Return JSON {\"sr\": <same structure>, \"sq\": <same structure>}.\n\n" + json.dumps(MK, ensure_ascii=False))
body = {"contents": [{"parts": [{"text": txt}]}], "generationConfig": {"responseMimeType": "application/json", "temperature": 0.2}}
r = json.loads(json.loads(urllib.request.urlopen(urllib.request.Request(U + K, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}), timeout=180).read())["candidates"][0]["content"]["parts"][0]["text"])
out = {"mk": MK, "sr": r["sr"], "sq": r["sq"]}
for L in ("sr", "sq"):
    for k in MK:
        if k != "head": assert out[L][k]["a"] == MK[k]["a"], (L, k)
json.dump(out, open(f"{S}/cut/bundles.json", "w"), ensure_ascii=False, indent=1); print("BUNDLES_OK")
print(json.dumps(out["sr"]["b1"], ensure_ascii=False)); print(json.dumps(out["sq"]["b2"], ensure_ascii=False)); print(out["sr"]["head"], "|", out["sq"]["head"])
