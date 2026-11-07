#!/usr/bin/env python3
"""Character-card generator via OpenRouter image models (default Nano Banana Pro).

Usage:
    orgen.py <ref_image> <out.png> <pose_line> [model]

One reference only. Instruction-phrased - these models have no negative-prompt field.
"""
import base64, json, mimetypes, os, sys, urllib.request

DEFAULT_MODEL = "google/gemini-3-pro-image"
SECRETS = "/a0/usr/projects/vast/.a0proj/secrets.env"

FACE = (
    "Edit this photo into a photorealistic character reference card. "
    "The person is the same individual, reimagined as a woman. Change the face to a female face: "
    "remove every trace of moustache, beard, stubble, chin and jaw shadow, and upper-lip shadow - "
    "completely smooth bare skin across the entire lower face. "
    "Give her a narrower jawline, a softer chin, a softened brow ridge, slightly fuller cheeks and lips, "
    "and a slender neck with no visible Adam's apple. "
    "Preserve her identity exactly: the same eyes, the same eye spacing, the same iris colour, "
    "the same nose shape and nostrils, the same hairline and forehead proportion, "
    "and the same small mole on the left cheek below the eye. "
    "Keep the exact same long red-and-black hair and the same black-and-red headband from the photo, unchanged. "
    "Keep her as a striking female Demon Hunter presence. "
    "She is fully dressed in a modest high-necked kimono that covers her shoulders, chest and collarbones "
    "completely - no bare skin below the neck, no bare chest. "
    "Her features must read unmistakably female and delicate: a slender tapered jaw, soft rounded cheeks, "
    "a fine brow, and a graceful feminine neck. "
    "Photorealistic portrait photograph, head and shoulders, centred, the face large and filling most of the frame, "
    "real unretouched skin with visible pores, natural soft light, 85 mm lens. "
    "Do not make it a cartoon, illustration, painting or 3D render. Do not add text, watermarks or logos."
)


def _key():
    for line in open(SECRETS):
        if line.strip().startswith('OPEN_ROUTER_API_KEY'):
            return line.split('=', 1)[1].strip().strip('"').strip("'")
    raise RuntimeError('OPEN_ROUTER_API_KEY not found')


def gen(ref, out, pose, model=DEFAULT_MODEL):
    mime = mimetypes.guess_type(ref)[0] or 'image/png'
    b64 = base64.b64encode(open(ref, 'rb').read()).decode()
    body = {
        'model': model,
        'modalities': ['image', 'text'],
        'messages': [{
            'role': 'user',
            'content': [
                {'type': 'text', 'text': FACE + ' ' + pose},
                {'type': 'image_url', 'image_url': {'url': f'data:{mime};base64,{b64}'}},
            ],
        }],
        'image_config': {'aspect_ratio': '1:1'},
    }
    import time
    req = urllib.request.Request(
        'https://openrouter.ai/api/v1/chat/completions',
        data=json.dumps(body).encode(),
        headers={'Authorization': 'Bearer ' + _key(), 'Content-Type': 'application/json'},
    )
    d = None
    for attempt in range(5):
        try:
            d = json.load(urllib.request.urlopen(req, timeout=300))
            break
        except Exception as e:
            raw = getattr(e, 'read', lambda: b'')()
            txt = raw.decode('utf-8', 'replace')
            if 'in_flight_budget_exhausted' in txt and attempt < 4:
                wait = 20 * (attempt + 1)
                print(f'  in-flight budget busy, retry in {wait}s ({attempt+1}/4)', flush=True)
                time.sleep(wait)
                continue
            print('HTTP ERR', e, txt[:400])
            return False
    if d is None:
        return False
    if 'error' in d:
        print('ERR', json.dumps(d['error'])[:500]); return False
    msg = (d.get('choices') or [{}])[0].get('message', {})
    images = msg.get('images') or []
    for im in images:
        url = (im.get('image_url') or {}).get('url', '')
        if url.startswith('data:'):
            raw = base64.b64decode(url.split(',', 1)[1])
            open(out, 'wb').write(raw)
            print('OK', out, os.path.getsize(out), 'bytes | model', model)
            print('usage', json.dumps(d.get('usage')))
            return True
    print('no image in response:', json.dumps(d)[:600])
    return False


if __name__ == '__main__':
    ref, out, pose = sys.argv[1], sys.argv[2], sys.argv[3]
    mdl = sys.argv[4] if len(sys.argv) > 4 else DEFAULT_MODEL
    sys.exit(0 if gen(ref, out, pose, mdl) else 1)
