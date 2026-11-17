#!/usr/bin/env python3
"""Nano Banana Pro (gemini-3-pro-image) character card generator.
Usage: nbgen.py <ref_image> <out.png> <pose_line>
One reference only. Instruction-phrased (no negatives - model has no negative field).
"""
import base64, json, os, sys, urllib.request

MODEL = "gemini-3-pro-image"

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
    "Photorealistic portrait photograph, head and shoulders, centred, the face large and filling most of the frame, "
    "real unretouched skin with visible pores, natural soft light, 85 mm lens. "
    "Do not make it a cartoon, illustration, painting or 3D render. Do not add text, watermarks or logos."
)

def gen(ref, out, pose):
    key = None
    for line in open('/a0/usr/projects/vast/.a0proj/secrets.env'):
        if line.strip().startswith('BN_GEMINI_API'):
            key = line.split('=', 1)[1].strip().strip('"').strip("'")
            break
    img = base64.b64encode(open(ref, 'rb').read()).decode()
    body = {
        "contents": [{"parts": [
            {"text": FACE + " " + pose},
            {"inline_data": {"mime_type": "image/png", "data": img}},
        ]}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {"aspectRatio": "1:1"},
        },
    }
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        d = json.load(urllib.request.urlopen(req, timeout=300))
    except Exception as e:
        body_txt = getattr(e, 'read', lambda: b'')()
        print('HTTP ERR', e, body_txt[:400]); return False
    if 'error' in d:
        print('ERR', json.dumps(d['error'])[:400]); return False
    for p in d['candidates'][0]['content']['parts']:
        inl = p.get('inlineData') or p.get('inline_data')
        if inl:
            open(out, 'wb').write(base64.b64decode(inl['data']))
            print('OK', out, os.path.getsize(out)); return True
    print('no image:', json.dumps(d)[:300]); return False

if __name__ == '__main__':
    sys.exit(0 if gen(sys.argv[1], sys.argv[2], sys.argv[3]) else 1)
