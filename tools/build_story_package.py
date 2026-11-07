#!/usr/bin/env python3
"""Single source of truth: canonical story JSON -> spec.md + storyboard.html.

Usage:
    python tools/build_story_package.py <data.json>

Reads one story JSON (authored first by a packaging agent) and derives:
    data/NN_<slug>_data.json            (canonical copy)
    specs/NN_<slug>_SPEC.md             (human review contract)
    storyboards/NN_<slug>_storyboard.html (visual pre-vis + machine JSON)

The JSON is the ONLY authored artifact; both outputs are DERIVED. No drift.
"""
import json, pathlib, sys, re, importlib.util

ROOT = pathlib.Path('/a0/usr/projects/vast')
DATA_DIR = ROOT/'storybook_ocr'/'data'
SPEC_DIR = ROOT/'storybook_ocr'/'specs'
SB_DIR   = ROOT/'storybook_ocr'/'storyboards'

# ---------------- validation ----------------
def validate(data):
    errs = []
    for k in ("num","title_mk","title_en","genre","logline"):
        if not data.get(k):
            errs.append(f"top-level missing/empty: {k}")
    spec = data.get("spec") or {}
    if spec.get("resolution") != "1280x720": errs.append("spec.resolution must be 1280x720")
    if spec.get("fps", 24) != 24: errs.append("spec.fps must be 24")
    if not spec.get("flf"): errs.append("spec.flf must be true (first-last-frame)")
    if spec.get("style","").lower() != "photoreal": errs.append("spec.style must be 'photoreal'")
    if spec.get("shot_floor", 0) < 40: errs.append("spec.shot_floor must be >= 40")
    if not data.get("cast"): errs.append("cast must be non-empty")
    acts = data.get("acts")
    if not acts:
        errs.append("acts must be non-empty")
    else:
        if len(acts) < 2: errs.append("need at least 2 acts")
        total = 0
        for a in acts:
            if not a.get("id") or not a.get("title") or not a.get("color"):
                errs.append(f"act missing id/title/color: {a.get('id','?')}")
            for i, s in enumerate(a.get("shots", [])):
                total += 1
                for f in ("id","size","angle","move","dur","clip_s","kf_first","kf_last"):
                    if not s.get(f):
                        errs.append(f"{a.get('id')} shot#{i} missing field: {f}")
                if "narration_mk" not in s and "dialogue_mk" not in s:
                    errs.append(f"{a.get('id')} shot {s.get('id','?')}: needs narration_mk and/or dialogue_mk key (may be empty string)")
        if total < 40:
            errs.append(f"total shots {total} < 40 (doctrine floor, need 40-60)")
    return errs

# ---------------- slug ----------------
def slugify(num, title_en):
    s = re.sub(r'[^a-z0-9]+','_', title_en.lower()).strip('_')
    return f"{num}_{s}" if s else num

# ---------------- spec.md ----------------
def esc(s):
    return (s or "").replace("|","\\|").replace("\n"," ")

def build_spec_md(data):
    spec = data["spec"]
    acts = data["acts"]
    total = sum(len(a["shots"]) for a in acts)
    total_dur = round(sum(s["dur"] for a in acts for s in a["shots"]),1)
    total_clip = round(sum(s.get("clip_s",5.0) for a in acts for s in a["shots"]),1)
    L = []
    a = L.append
    a(f"# {data['num']} — {data['title_mk']} ({data['title_en']})")
    a("")
    a("> DEFINE deliverable. Zero cost — authoring only. Doctrine-compliant per `24_CRITIQUE_REANALYSIS_REPORT.md`.")
    a(f"> Photoreal · FLF (start+end) · 1280×720 · 24 fps · Macedonian audio · **{total} shots** (floor 40).")
    a("")
    a("---")
    a("")
    a("## 0. Concept")
    a("")
    a(f"**{esc(data['title_mk'])}** — {esc(data['logline'])}")
    a("")
    a(f"*Genre:* {esc(data['genre'])}")
    a("")
    a("---")
    a("")
    a("## 1. Render contract (non-negotiable)")
    a("")
    a("| Field | Value |")
    a("|---|---|")
    a(f"| resolution / aspect | {esc(spec.get('resolution','1280x720'))} / {esc(spec.get('aspect','16:9'))} |")
    a(f"| fps | {spec.get('fps',24)} |")
    a(f"| model | {esc(spec.get('model','SkyReels-V3-identity'))} |")
    a(f"| style | {esc(spec.get('style','photoreal'))} |")
    a(f"| FLF | {'start+end keyframes' if spec.get('flf') else 'single-ref (REJECTED)'} |")
    a(f"| language | {esc(spec.get('language','mk'))} |")
    a(f"| shot floor–max | {spec.get('shot_floor',40)}–{spec.get('shot_max',60)} |")
    a(f"| seed policy | {esc(spec.get('seed_policy','fixed-per-shot'))} |")
    a(f"| style anchor | {esc(' · '.join(spec.get('style_anchor',[])))} |")
    a("")
    a("**Negative prompt:**")
    a("")
    a(f"```\n{esc(spec.get('negative_prompt',''))}\n```")
    a("")
    a("---")
    a("")
    a("## 2. Cast")
    a("")
    a("| Role | Trait | Source | Face-lock |")
    a("|---|---|---|---|")
    for c in data["cast"]:
        a(f"| {esc(c['role'])} | {esc(c.get('trait',''))} | {esc(c.get('source','story-suggested'))} | {esc(c.get('face_lock','AI-default'))} |")
    a("")
    a("> Characters remain **AI-default / story-suggested** at this stage. No real face is applied (external casting is a later, separately-approved step).")
    a("")
    a("---")
    a("")
    a("## 3. Acts & shot list (FLF)")
    a("")
    a(f"**{total} shots · ~{total_dur}s runtime · {total_clip}s rendered @ ~5s/clip.** Full KF·A/KF·B keyframe prompts, continuity and motion live in the machine layer (`data/*_data.json` + embedded JSON in the storyboard HTML).")
    for ai, act in enumerate(acts):
        a("")
        a(f"### {act['num']} — {esc(act['title'])}")
        a("")
        a(f"*{esc(act.get('synopsis',''))}*")
        a("")
        a("| # | Size | Angle | Move | t | cue |")
        a("|---|---|---|---|---|---|")
        for s in act["shots"]:
            cue = "DLG" if s.get("dialogue_mk") else ("NAR" if s.get("narration_mk") else "—")
            a(f"| {esc(s['id'])} | {esc(s['size'])} | {esc(s['angle'])} | {esc(s['move'])} | {s['dur']}s | {cue} |")
    a("")
    a("---")
    a("")
    a("## 4. Narration & dialogue (Macedonian, adapted — never verbatim)")
    a("")
    a("Narration is **filler**; the visual carries more than the voice. Only what earns its place is spoken.")
    a("")
    found = False
    for act in acts:
        for s in act["shots"]:
            n = s.get("narration_mk","")
            d = s.get("dialogue_mk","")
            if n:
                found = True
                a(f"- `{esc(s['id'])}` **NAR** — {esc(n)}")
            if d:
                found = True
                a(f"- `{esc(s['id'])}` **DLG** — {esc(d)}")
    if not found:
        a("(no dialogue/narration authored)")
    a("")
    a("---")
    a("")
    a("## 5. Acceptance criteria (testable)")
    a("")
    checks = [
        f"Shot count = {total} (≥40), durations ≥2.5s averaging ~3s → ≥2:00 runtime.",
        "References per shot ≥ 2 (start + end FLF); single-reference jobs rejected at build.",
        "Camera grammar present in every shot (size + angle + move).",
        "Motion floor via frame-difference — no held stills.",
        "Narration/dialogue split, adapted not verbatim; narration is filler.",
        "Visual-first — mute audio, the story still reads.",
        "Audio — spatial SFX + restrained score; Macedonian-only voices.",
        "Style: photoreal, validated against external references only (no self-made benchmark).",
    ]
    for i, c in enumerate(checks, 1):
        a(f"{i}. {c}")
    a("")
    a("---")
    a("")
    a("## 6. Pipeline note")
    a("")
    a("```")
    a("P0 RESEARCH    source text read + cinematic language researched")
    a("P1 ENHANCE     beat spine authored into shot list")
    a("P2 SPLIT       narration != dialogue (Macedonian)")
    a("P3 SCRIPT      shot list + cues (this spec)")
    a("P4 STORYBOARD  every shot = START + END keyframe (FLF)")
    a("P5 PROMPTS     Qwen-Image keyframes + Wan FLF video prompts")
    a("P6 PRICE CHECK live Vast scan + itemized estimate + per-run approval")
    a("P7 PROOF       1 scene (3-4 FLF shots) for user judgement")
    a("P8 FULL RUN    approved shots -> copy+sha256+ffprobe -> assembly -> teardown")
    a("```")
    a("")
    a("*DEFINE-ONLY. No GPU rented; nothing spends until P6 is approved per run.*")
    return "\n".join(L) + "\n"

# ---------------- main ----------------
def main():
    if len(sys.argv) != 2:
        print("usage: build_story_package.py <data.json>"); sys.exit(2)
    src = pathlib.Path(sys.argv[1]).resolve()
    data = json.loads(src.read_text(encoding='utf-8'))
    errs = validate(data)
    if errs:
        print("VALIDATION FAILED:")
        for e in errs: print("  -", e)
        sys.exit(1)
    slug = slugify(data["num"], data["title_en"])
    for d in (DATA_DIR, SPEC_DIR, SB_DIR):
        d.mkdir(parents=True, exist_ok=True)
    # canonical copy
    (DATA_DIR/f"{slug}_data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    # spec.md
    spec_path = SPEC_DIR/f"{slug}_SPEC.md"
    spec_path.write_text(build_spec_md(data), encoding='utf-8')
    # storyboard.html via existing generator
    sb_mod_path = ROOT/'tools'/'build_storyboard_html.py'
    sp_mod = importlib.util.spec_from_file_location('build_sb', sb_mod_path)
    sb = importlib.util.module_from_spec(sp_mod); sp_mod.loader.exec_module(sb)
    html = sb.build(data)
    html_path = SB_DIR/f"{slug}_storyboard.html"
    html_path.write_text(html, encoding='utf-8')
    # verify embedded machine layer
    m = re.search(r'<script type="application/json" id="storyboard-spec">(.*?)</script>', html, re.S)
    import html as H
    payload = json.loads(H.unescape(m.group(1))) if m else {}
    n = sum(len(a['shots']) for a in payload.get('acts',[]))
    print(f"PACKAGE OK: {data['num']} {data['title_mk']}")
    print(f"  data      -> {DATA_DIR/f'{slug}_data.json'}")
    print(f"  spec.md   -> {spec_path}")
    print(f"  storyboard-> {html_path}")
    print(f"  shots={n} | section-sign bytes={html_path.read_bytes().count(b'\xc2\xa7')} | CLEAN={html_path.read_bytes().count(b'\xc2\xa7')==0}")

if __name__ == "__main__":
    main()
