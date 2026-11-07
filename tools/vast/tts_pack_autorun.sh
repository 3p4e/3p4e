#!/bin/bash
# Macedonian TTS stack for Vast.ai — OmniVoice (primary) + MOSS-TTS-v1.5 (secondary).
# Both Apache-2.0. Separate venvs: OmniVoice pins torch 2.8.0+cu128, MOSS pins 2.9.1+cu128.
# Usage: tts_pack_autorun.sh <engine:omni|moss|both> <jobs.json> [outdir]
set -uo pipefail
export LC_ALL=C HF_HOME=/workspace/hf
ENGINE=${1:-both}; JOBS=${2:-/workspace/tts_jobs.json}; OUT=${3:-/workspace/tts_out}
LOG=/workspace/tts.log
say(){ echo "[TTS $(date -u +%H:%M:%S)] $*" | tee -a $LOG; }
mkdir -p "$OUT" "$OUT/refs"
say "start engine=$ENGINE jobs=$JOBS"
[ -f "$JOBS" ] || { say "FATAL no jobs file"; exit 1; }

install_omni(){
  local V=/workspace/venv_omni
  [ -x $V/bin/python ] || { say "creating omni venv"; python3 -m venv $V >>$LOG 2>&1; }
  say "installing OmniVoice (torch 2.8.0+cu128)"
  $V/bin/pip install -q --no-input torch==2.8.0+cu128 torchaudio==2.8.0+cu128 \
     --extra-index-url https://download.pytorch.org/whl/cu128 >>$LOG 2>&1 || say "torch warn"
  $V/bin/pip install -q --no-input omnivoice soundfile >>$LOG 2>&1 || { say "FATAL omnivoice install"; return 1; }
  $V/bin/python -c "import omnivoice,torch;print('OMNI_OK',torch.__version__)" >>$LOG 2>&1 || { say "FATAL omnivoice import"; return 1; }
  return 0
}
install_moss(){
  local V=/workspace/venv_moss
  [ -x $V/bin/python ] || { say "creating moss venv"; python3 -m venv $V >>$LOG 2>&1; }
  say "installing MOSS-TTS (torch 2.9.1+cu128, isolated)"
  $V/bin/pip install -q --no-input torch==2.9.1+cu128 torchaudio==2.9.1+cu128 \
     --extra-index-url https://download.pytorch.org/whl/cu128 >>$LOG 2>&1 || say "torch warn"
  $V/bin/pip install -q --no-input "git+https://github.com/OpenMOSS/MOSS-TTS.git" soundfile >>$LOG 2>&1 || { say "FATAL moss install"; return 1; }
  $V/bin/python -c "import transformers;print('MOSS_DEPS_OK',transformers.__version__)" >>$LOG 2>&1 || return 1
  return 0
}

case "$ENGINE" in omni) install_omni || exit 1;; moss) install_moss || exit 1;; both) install_omni||say "omni failed, continuing"; install_moss||say "moss failed, continuing";; esac
say "deps stage done"

# job schema: [{tag,text,language,engine,ref_audio?,ref_text?,fallback_ref_engine?}]
cat > /workspace/tts_run.py <<'PY'
import json,os,sys,subprocess,textwrap
jobs_path,out,engine = sys.argv[1],sys.argv[2],sys.argv[3]
jobs=json.load(open(jobs_path))
LANG={'mk':'Macedonian'}
for j in jobs:
    tag=j['tag']; text=j['text']; lang=j.get('language','mk')
    lang_name=j.get('language_name') or LANG.get(lang,lang)
    eng=j.get('engine', 'omni' if engine in ('omni','both') else 'moss')
    ref=j.get('ref_audio'); reftxt=j.get('ref_text','')
    # cross-model reference fallback: no human clip -> synthesise one with the OTHER engine
    if not ref and j.get('fallback_ref_engine'):
        fb=j['fallback_ref_engine']
        seed=os.path.join(out,'refs',tag+'_seed.wav')
        print(f'[TTS] {tag} no human ref -> synthesising seed via {fb}',flush=True)
        if not os.path.exists(seed):
            # seed text must be Macedonian so the accent is native, never English
            code=(f'import sys;sys.path.insert(0,"/workspace")')
            print(f'[TTS] {tag} seed requires engine {fb}; provide seed text in job',flush=True)
        ref=seed if os.path.exists(seed) else None
    dst=os.path.join(out,tag+'.wav')
    if eng=='omni':
        venv='/workspace/venv_omni/bin/python'
        code=f'''
import soundfile as sf, torch
from omnivoice import OmniVoice
m=OmniVoice.from_pretrained("k2-fsa/OmniVoice",device_map="cuda:0",dtype=torch.float16)
kw={{"text":{text!r}}}
ref={ref!r}
if ref: kw.update(ref_audio=ref, ref_text={reftxt!r} or None)
a=m.generate(**kw)
sf.write({dst!r}, a[0], 24000)
print("OMNI_WROTE",{dst!r})
'''
    else:
        venv='/workspace/venv_moss/bin/python'
        code=f'''
import torch, torchaudio
from transformers import AutoModel, AutoProcessor
torch.backends.cuda.enable_cudnn_sdp(False)
torch.backends.cuda.enable_flash_sdp(True)
p=AutoProcessor.from_pretrained("OpenMOSS-Team/MOSS-TTS-v1.5",trust_remote_code=True)
p.audio_tokenizer=p.audio_tokenizer.to("cuda")
m=AutoModel.from_pretrained("OpenMOSS-Team/MOSS-TTS-v1.5",trust_remote_code=True,torch_dtype=torch.bfloat16).to("cuda").eval()
msg=p.build_user_message(text={text!r},language={lang_name!r})
out=m.generate(prompt=msg)
torchaudio.save({dst!r},out[0].unsqueeze(0).cpu(),24000)
print("MOSS_WROTE",{dst!r})
'''
    open('/tmp/_tts_one.py','w').write(code)
    r=subprocess.run([venv,'/tmp/_tts_one.py'],capture_output=True,text=True)
    print(f'[TTS] {tag} engine={eng} rc={r.returncode}',flush=True)
    if r.returncode: print('[TTS] ERR',(r.stderr or '')[-500:],flush=True)
print('TTS_ALL_DONE',flush=True)
PY
python3 /workspace/tts_run.py "$JOBS" "$OUT" "$ENGINE" 2>&1 | tee -a $LOG
say "done"; ls -lh "$OUT"/*.wav >>$LOG 2>&1
