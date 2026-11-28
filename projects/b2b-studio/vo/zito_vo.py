import sys,json,base64,subprocess,shutil
src=open("gen_vo3.py").read().split("def words")[0].replace("from vo_extra import VO","")
exec(src)
tests=[("zito_5","Kore","Жито маркети. Свежината започнува тука."),("b2_zito_opening_film_4","Charon","Жито маркети. Тим што ве пречекува со насмевка.")]
for name,voice,line in tests:
    for a in range(6):
        r=call("gemini-3.8-flash-tts",{"contents":[{"parts":[{"text":line}]}],"generationConfig":{"responseModalities":["AUDIO"],"speechConfig":{"voiceConfig":{"prebuiltVoiceConfig":{"voiceName":voice}}}}})
        try: raw=base64.b64decode(r["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]); break
        except KeyError: time.sleep(10)
    out=f"lines/{name}.wav"; tr=f"trim/{name}.wav"
    if raw[:4]!=b"RIFF":
        open("t.pcm","wb").write(raw); subprocess.run(["ffmpeg","-v","error","-y","-f","s16le","-ar","24000","-ac","1","-i","t.pcm",out],check=True)
    else: open(out,"wb").write(raw)
    subprocess.run(["ffmpeg","-v","error","-y","-i",out,"-af","silenceremove=start_periods=1:start_threshold=-35dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-35dB:start_silence=0.2,areverse",tr],check=True)
    t=call("gemini-2.5-flash",{"contents":[{"parts":[{"text":"Transcribe exactly every word spoken in this audio in its original language and script. Output only the transcript."},{"inline_data":{"mime_type":"audio/wav","data":base64.b64encode(open(tr,"rb").read()).decode()}}]}]},120)["candidates"][0]["content"]["parts"][0]["text"]
    print(name,"|",line,"|",t.strip())
for i in range(1,5): shutil.copy(f"trim/kam_{i}.wav",f"trim/zito_{i}.wav")
for i in range(1,4): shutil.copy(f"trim/b2_kam_opening_film_{i}.wav",f"trim/b2_zito_opening_film_{i}.wav")
