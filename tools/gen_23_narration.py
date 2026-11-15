#!/usr/bin/env python3
"""
#23 Perseus & Medusa — bilingual narration/dialogue TTS pipeline (MK + EN).

Reads   : storybook_ocr/specs/23_AUDIO_SCRIPT_MK_EN.md   (single-line blocks)
Outputs : media/perseus_assets/audio/narration/s{NN}_{MK,EN}.wav  (48 kHz PCM16 mono)
          media/perseus_assets/audio/narration/manifest.json      (per-line metadata)

Script line grammar (hex-verified):
    **S04** P: „MK text..." / "EN text..."
  - MK wrapped in low-9 quotes „ ... " (straight-quote close, LITERAL backslash absent)
  - EN wrapped in plain ASCII quotes " ... "; languages separated by exactly one ' / '
  - character codes: N (narrator), P (Perseus), M (Medusa), A (Andromeda), ATH (Athena), H (Hermes)
  NOTE: this differs from the Fenrir script (multi-line MK:/EN: blocks) — the Fenrir
  regex parses ZERO lines here. This parser targets the #23 grammar only.

Modes:
  default                DRY RUN — parse, validate continuity, write manifest with
                         status "pending", zero API spend.
  --generate             Call ElevenLabs eleven_multilingual_v2, save 48k WAV stems.
                         Requires every cast character to have a voice_id (see CAST).
  --script PATH          Override script path (default storybook_ocr/specs/23_AUDIO_SCRIPT_MK_EN.md)
  --only S,S,S           Restrict to these shot numbers (e.g. --only 1,6,8 dry-runs 3 lines)

Spend discipline (VAST operating rules): generation runs only after the director's
explicit spend GO; every run is its own ledger; duration metadata is measured, not
estimated. ElevenLabs has no native 48 kHz output — raw pcm_44100 is resampled with
ffmpeg, so a generation run requires ffmpeg on PATH.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request

KEY = 'sk_4a7efb44ade8d01207d13f07d3e9339bb243ca594048d2ae'          # injected by framework; resolves in-process
MODEL = 'eleven_multilingual_v2'              # one model handles MK + EN natively
EL_FMT = 'pcm_44100'                          # raw s16le mono @44.1k; resampled to 48k below
OUT = 'media/perseus_assets/audio/narration'
SCRIPT = 'storybook_ocr/specs/23_AUDIO_SCRIPT_MK_EN.md'
SAMPLE_RATE = 48000                           # doctrine: WAV stems at 48 kHz
SETTINGS = {'stability': 0.5, 'similarity_boost': 0.72}   # proven Fenrir voice settings

# ---------------------------------------------------------------- casting
# Narrator / Athena / Hermes reuse the Fenrir-probed, proven voice IDs (Bill = the
# "wise-male" class the script asks Athena to mirror; Callum = the "wry/husky" class
# the script asks Hermes to mirror).
# Perseus / Medusa / Andromeda are marked "new cast" in the script footer — the
# casting probe must fill these before any --generate run; left None on purpose so
# an incomplete cast fails loudly instead of mis-casting.
CAST = {
    'narrator':  {'who': 'Narrator',  'voice_id': 'nPczCjzI2devNBz1zQrb', 'ref': 'Brian  — deep, resonant (proven Fenrir narrator)'},
    'perseus':   {'who': 'Perseus',   'voice_id': None,                   'ref': 'young-hero: steady, low   (NEW CAST — probe required)'},
    'medusa':    {'who': 'Medusa',    'voice_id': None,                   'ref': 'dark-female: tired menace, not shrieky (NEW CAST — probe required)'},
    'andromeda': {'who': 'Andromeda', 'voice_id': None,                   'ref': 'noble-female: restrained grief (NEW CAST — probe required)'},
    'athena':    {'who': 'Athena',    'voice_id': 'pqHfZKP75CvOlQylNhV4', 'ref': 'Bill — wise, mature (proven; script asks for Fenrir-Odin class)'},
    'hermes':    {'who': 'Hermes',    'voice_id': 'N2lVS1w4EtoT3dr4eOWO', 'ref': 'Callum — husky trickster (proven; script asks for Fenrir-Loki class)'},
}
CODE2CHAR = {'N': 'narrator', 'P': 'perseus', 'M': 'medusa', 'A': 'andromeda', 'ATH': 'athena', 'H': 'hermes'}

# ---------------------------------------------------------------- parsing
# Script grammar (dry-run verified): dialogue lines are quoted
#   **S04** P: „MK..." / "EN..."
# but narration lines are BARE text with no quote wrappers:
#   **S01** N: MK text... / EN text...
# So the wrappers are optional — split on the separator and strip incidental quotes.
# Verified: exactly one ' / ' per line across the corpus (awk NF>2 -> none), so the
# last-occurrence split is unambiguous.
LINE_RE = re.compile(
    r'^\*\*S(\d{1,3})\*\*\s+([A-Z]{1,3}):\s+'   # **S04** P:
    r'(.+?)\s+/\s+(.+?)\s*$',                     # MK / EN (wrappers optional)
)
STRIP_CHARS = ' \t„“”"'                            # all quote/space variants seen in the corpus


def parse_script(path):
    """Return (entries, warnings). entries: [{'shot', 'code', 'character', 'mk', 'en'}]."""
    raw = open(path, encoding='utf-8').read().splitlines()
    entries, warnings = [], []
    seen = {}
    for ln, line in enumerate(raw, 1):
        m = LINE_RE.match(line.strip())
        if not m:
            if re.match(r'^\*\*S\d', line.strip()):          # a shot line that failed grammar
                warnings.append(f'L{ln}: SHOT LINE FAILED GRAMMAR: {line.strip()[:90]}')
            continue
        shot, code, mk, en = int(m.group(1)), m.group(2), m.group(3), m.group(4)
        if code not in CODE2CHAR:
            warnings.append(f'L{ln}: S{shot:02d} unknown character code {code!r} (skipped)')
            continue
        if shot in seen:
            warnings.append(f'L{ln}: duplicate shot S{shot:02d} (first at L{seen[shot]}), keeping first')
            continue
        seen[shot] = ln
        entries.append({
            'shot': shot, 'code': code, 'character': CODE2CHAR[code],
            'mk': mk.strip(STRIP_CHARS), 'en': en.strip(STRIP_CHARS),
        })
    entries.sort(key=lambda e: e['shot'])
    return entries, warnings


def validate(entries, warnings):
    """Continuity + sanity gates. Returns list of issue strings (empty == clean)."""
    issues = list(warnings)
    shots = [e['shot'] for e in entries]
    if not entries:
        return ['no parseable shot lines at all — grammar mismatch?']
    missing = [n for n in range(1, max(shots) + 1) if n not in shots]
    if missing:
        issues.append(f'non-continuous shots (gaps at S{", S".join(f"{n:02d}" for n in missing)})')
    if shots[0] != 1:
        issues.append(f'script starts at S{shots[0]:02d}, expected S01')
    for e in entries:
        for lang in ('mk', 'en'):
            t = e[lang]
            if not t:
                issues.append(f'S{e["shot"]:02d} empty {lang.upper()} text')
            if ' / ' in t:
                issues.append(f'S{e["shot"]:02d} {lang.upper()} contains " / " — separator is ambiguous')
            if t.startswith('„') or t.endswith('"') or t.startswith('"'):
                issues.append(f'S{e["shot"]:02d} {lang.upper()} quote residue after strip: {t[:30]!r}')
    return issues


# ---------------------------------------------------------------- tts

def tts_raw_pcm(text, voice_id):
    """One ElevenLabs call; returns raw s16le bytes. Raises on final failure."""
    body = json.dumps({'text': text, 'model_id': MODEL, 'voice_settings': SETTINGS}).encode()
    url = f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format={EL_FMT}'
    req = urllib.request.Request(url, data=body,
                                 headers={'xi-api-key': KEY, 'Content-Type': 'application/json'})
    last = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except Exception as e:
            last = e
            if attempt < 3:
                time.sleep(2 * (attempt + 1))
    raise RuntimeError(f'ElevenLabs TTS failed after 4 attempts: {last}')


def pcm_to_wav_48k(raw, outpath):
    """Resample raw s16le mono 44.1k -> 48k 16-bit WAV via ffmpeg."""
    p = subprocess.run(
        ['ffmpeg', '-y', '-loglevel', 'error',
         '-f', 's16le', '-ar', '44100', '-ac', '1', '-i', 'pipe:0',
         '-ar', str(SAMPLE_RATE), '-ac', '1', '-c:a', 'pcm_s16le', outpath],
        input=raw, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(f'ffmpeg resample failed: {p.stderr.decode()[:200]}')


def wav_duration(path):
    p = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                        '-of', 'default=nw=1:nk=1', path], capture_output=True, text=True)
    return round(float(p.stdout.strip()), 3)


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--generate', action='store_true', help='actually call ElevenLabs (needs spend GO)')
    ap.add_argument('--script', default=SCRIPT)
    ap.add_argument('--only', default=None, help='comma shot list, e.g. "1,6,8" (dry-run subset)')
    args = ap.parse_args()

    os.makedirs(OUT, exist_ok=True)
    entries, warnings = parse_script(args.script)
    issues = validate(entries, warnings)

    if args.only:
        keep = {int(x) for x in args.only.split(',')}
        entries = [e for e in entries if e['shot'] in keep]
        print(f'--only filter applied: {len(entries)} shots selected')

    print(f'parsed shots: {len(entries)}  (script: {args.script})')
    char_count = {}
    for e in entries:
        char_count[e["character"]] = char_count.get(e["character"], 0) + 1
    print('lines per character:', json.dumps(char_count, sort_keys=True))

    unclean = [i for i in issues if not i.startswith(('L', 'non-continuous'))]
    for i in issues:
        print('  ! ' + i)

    manifest = {
        'film': '#23 Perseus & Medusa',
        'script': args.script,
        'model': MODEL,
        'sample_rate': SAMPLE_RATE,
        'settings': SETTINGS,
        'cast': {k: {'who': v['who'], 'voice_id': v['voice_id'], 'ref': v['ref']} for k, v in CAST.items()},
        'mode': 'generate' if args.generate else 'dry-run',
        'issues': issues,
        'lines': [],
    }

    uncast = sorted({e['character'] for e in entries if CAST[e['character']]['voice_id'] is None})

    if not args.generate:
        for e in entries:
            for lang in ('mk', 'en'):
                manifest['lines'].append({
                    'shot': e['shot'], 'language': lang, 'character': e['character'],
                    'text': e[lang],
                    'output': f'{OUT}/s{e["shot"]:02d}_{lang.upper()}.wav',
                    'duration': None, 'status': 'pending',
                })
        manifest_path = os.path.join(OUT, 'manifest.json')
        json.dump(manifest, open(manifest_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        print(f'DRY RUN complete — manifest written: {manifest_path}')
        print(f'total pending stems: {len(manifest["lines"])} ({len(entries)} shots x 2 languages)')
        if unclean:
            print(f'PARSER WARNINGS: {len(unclean)} (see manifest.issues)')
        if uncast:
            print('UNCAST CHARACTERS (block --generate until probed): ' + ', '.join(uncast))
        print('no ElevenLabs calls made (zero spend)')
        return

    # ---------------------------------------------------- generation path
    if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):
        sys.exit('ffmpeg/ffprobe not on PATH — required for 48 kHz WAV stems')
    if unclean:
        sys.exit(f'refusing to spend: {len(unclean)} parser warning(s) unresolved (see dry run)')
    if uncast:
        sys.exit('refusing to spend: uncast characters ' + ', '.join(uncast) +
                 ' — run the casting probe and fill CAST voice_ids first')

    done = failed = 0
    for e in entries:
        voice_id = CAST[e['character']]['voice_id']
        for lang in ('mk', 'en'):
            out = f'{OUT}/s{e["shot"]:02d}_{lang.upper()}.wav'
            rec = {'shot': e['shot'], 'language': lang, 'character': e['character'],
                   'text': e[lang], 'output': out}
            if os.path.exists(out) and os.path.getsize(out) > 1000:
                rec['status'] = 'skip'
                rec['duration'] = wav_duration(out)
                done += 1
            else:
                try:
                    raw = tts_raw_pcm(e[lang], voice_id)
                    pcm_to_wav_48k(raw, out)
                    rec['status'] = 'ok'
                    rec['duration'] = wav_duration(out)
                    done += 1
                except Exception as ex:
                    rec['status'] = 'fail'
                    rec['error'] = str(ex)[:200]
                    failed += 1
                    print(f'  FAIL s{e["shot"]:02d}_{lang.upper()}: {rec["error"]}', flush=True)
            manifest['lines'].append(rec)
            print(f"s{e['shot']:02d}_{lang.upper():2} {e['character']:<10} "
                  f"{rec['status']:<4} {rec.get('duration') or '-'}s", flush=True)
        json.dump(manifest, open(os.path.join(OUT, 'manifest.json'), 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=2)   # checkpoint after every shot

    print(f'NARRATION_TTS_23_DONE ok/skip={done} failed={failed} -> {OUT}')


if __name__ == '__main__':
    main()
