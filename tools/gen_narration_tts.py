import re, os, sys, json, time, urllib.request
KEY = 'sk_4a7efb44ade8d01207d13f07d3e9339bb243ca594048d2ae'
MODEL = 'eleven_multilingual_v2'
OUT = 'media/fenrir_assets/audio/narration'
os.makedirs(OUT, exist_ok=True)

# voice casting (probed from live API)
VOICES = {
  'narrator': 'nPczCjzI2devNBz1zQrb',  # Brian - Deep, Resonant and Comforting
  'odin':     'pqHfZKP75CvOlQylNhV4',  # Bill - Wise, Mature, Balanced
  'tyr':      'SOYHLrjzK2X1ezoPC6cr',  # Harry - Fierce Warrior
  'fenrir':   'pNInz6obpgDQGcFmaJgB',  # Adam - Dominant, Firm
  'loki':     'N2lVS1w4EtoT3dr4eOWO',  # Callum - Husky Trickster (no lines in source)
  'hel':      'fVAgjfbrqAnDt9gAct91',  # Shar - The Lady of Loss (no lines in source)
}

def tts(text, voice, outpath):
    if os.path.exists(outpath) and os.path.getsize(outpath) > 1000:
        return 'skip'
    body = json.dumps({'text': text, 'model_id': MODEL,
                       'voice_settings': {'stability': 0.5, 'similarity_boost': 0.72}}).encode()
    req = urllib.request.Request(f'https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_128',
                                 data=body, headers={'xi-api-key': KEY, 'Content-Type': 'application/json'})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            open(outpath, 'wb').write(data)
            return 'ok'
        except Exception as e:
            if attempt == 3:
                return f'FAIL {e}'
            time.sleep(2)

src = open('storybook_ocr/specs/13_AUDIO_SCRIPT_MK_EN.md').read()
# parse S## blocks: capture shot number, MK line, EN line
blocks = re.findall(r'\*\*S(\d{2})[^\n]*\*\*\s*\nMK: „?(.*?)„?"?\nEN: "(.*?)"', src)
lines = {int(n): {'mk': mk.strip().strip('„”\"'), 'en': en.strip()} for n, mk, en in blocks}
print('parsed shots:', len(lines))

# dialogue-only beats for character voices (lip-sync targets S13/S27/S30)
DIALOGUE = {
 13: {'voice':'odin', 'mk':'Врзете го! Локи, можеш ти!', 'en':"Bind him! Loki, you do it!"},
 27: {'voice':'tyr',  'mk':'Да видиме дали ќе го скинеш и овој синџир.', 'en':'Let us see if you can break this chain too.'},
 30: {'voice':'fenrir','mk':'Може да ме врзеш, но стави ја раката во мојата уста. Ако не се ослободам, и ти ќе изгубиш нешто!', 'en':'You may bind me, but place your hand in my mouth. If I cannot break free, you too will lose something!'},
}

done = 0
for n in sorted(lines):
    for lang in ('mk','en'):
        r = tts(lines[n][lang], VOICES['narrator'], f'{OUT}/s{n:02d}_{lang.upper()}.mp3')
        done += 1 if r in ('ok','skip') else 0
        if r.startswith('FAIL'): print(f's{n:02d}_{lang} {r}', flush=True)
# character dialogue clips
for n, d in sorted(DIALOGUE.items()):
    for lang in ('mk','en'):
        r = tts(d[lang], VOICES[d['voice']], f'{OUT}/s{n:02d}_{lang.upper()}_char.mp3')
        done += 1 if r in ('ok','skip') else 0
        if r.startswith('FAIL'): print(f's{n:02d}_{lang}_char {r}', flush=True)
print('NARRATION_TTS_DONE generated/skipped:', done)
