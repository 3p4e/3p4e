import base64, json, os, sys, urllib.request, uuid
from concurrent.futures import ThreadPoolExecutor

KEY = os.environ["OPENAI_API_KEY"]
MODEL = "gpt-image-2"
SIZE = "1536x1024"

STYLE = ("2D hand-painted children's storybook illustration, soft watercolor and gouache textures with visible paper grain, "
         "warm rounded shapes, gentle soft lighting, rich but soft colors, cozy, friendly and safe mood for children aged 3-6, "
         "flat 2D picture-book look (NOT 3D, NOT glossy, NOT photorealistic), cinematic 16:9 composition. "
         "No gore, nothing scary. Absolutely no text, letters, words, numbers, captions or logos anywhere in the image "
         "unless the scene explicitly asks for specific letters.")

CHARACTERS = ("CHARACTERS (keep them identical in every picture): "
              "PROFESSOR LIDENBROCK - a cheerful, slightly clumsy older German professor of the 1860s, round glasses, "
              "big bushy grey beard, rosy nose, brown long coat with a green waistcoat, tall dark top hat outdoors. "
              "AXEL - his nephew, a boy of about 12, short blond hair, green flat cap, blue jacket, brown backpack, "
              "big curious eyes. "
              "HANS - the guide, a very tall calm strong Icelandic man, long straight blond hair, short blond beard, "
              "brown fur vest over a grey shirt, coiled rope over one shoulder, gentle face. "
              "The NOTEBOOK is a small old brown leather notebook.")


def post(path, payload=None, files=None):
    if files is None:
        req = urllib.request.Request(f"https://api.openai.com/v1/{path}", data=json.dumps(payload).encode(),
                                     headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    else:
        b = uuid.uuid4().hex
        body = b""
        for k, v in payload.items():
            body += f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
        for fn in files:
            body += (f"--{b}\r\nContent-Disposition: form-data; name=\"image[]\"; filename=\"{os.path.basename(fn)}\"\r\n"
                     f"Content-Type: image/png\r\n\r\n").encode() + open(fn, "rb").read() + b"\r\n"
        body += f"--{b}--\r\n".encode()
        req = urllib.request.Request(f"https://api.openai.com/v1/{path}", data=body,
                                     headers={"Authorization": f"Bearer {KEY}",
                                              "Content-Type": f"multipart/form-data; boundary={b}"})
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        raise RuntimeError(e.read().decode()[:500])


def save(resp, fn):
    open(fn, "wb").write(base64.b64decode(resp["data"][0]["b64_json"]))


def reference_sheet():
    fn = "ref_sheet.png"
    if os.path.exists(fn):
        return fn
    prompt = (STYLE + " " + CHARACTERS + " Make a clean character reference sheet on a soft pastel background: "
              "PROFESSOR LIDENBROCK, AXEL and HANS standing side by side, full body, front view, with a small side view of each; "
              "the old leather NOTEBOOK shown large in the corner.")
    save(post("images/generations", {"model": MODEL, "prompt": prompt, "size": SIZE, "quality": "high", "n": 1}), fn)
    return fn


def scene(item, ref):
    sid, prompt = item
    fn = f"scene_{sid}.png"
    if os.path.exists(fn):
        return fn, "cached"
    full = (STYLE + " " + CHARACTERS + " Use the attached reference sheet only for the characters' designs; "
            "do not copy its layout or background. SCENE: " + prompt)
    save(post("images/edits", {"model": MODEL, "prompt": full, "size": SIZE, "quality": "high", "n": 1}, [ref]), fn)
    return fn, "ok"


if __name__ == "__main__":
    scenes = json.load(open("scenes.json"))
    only = set(sys.argv[1:])
    ref = reference_sheet()
    print("reference:", ref, flush=True)
    items = [(s["id"], s["prompt"]) for s in scenes if not only or s["id"] in only]
    with ThreadPoolExecutor(4) as ex:
        for (sid, _), fut in zip(items, [ex.submit(scene, it, ref) for it in items]):
            try:
                print(sid, *fut.result(), flush=True)
            except Exception as e:
                print(sid, "FAILED", e, flush=True)
