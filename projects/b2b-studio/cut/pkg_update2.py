# ON THE MUMBAI SERVER: refresh BIG_DOGMA_LTX.zip with new offer PDFs (replace) and the RS/AL/XK explainers (add), atomic swap.
# Also writes a small BIG_DOGMA_LTX_update_<date>.zip with only those files, same layout (unzip over the existing package).
import os, zipfile, shutil, glob, datetime
DL = glob.glob("/opt/stacks/bigdogma-dl/site/_dl_*")[0]; Z = f"{DL}/BIG_DOGMA_LTX.zip"; U = "/opt/bigdogma_pkg/upd"
src = zipfile.ZipFile(Z); root = src.infolist()[0].filename.split("/", 1)[0]; tmp = Z + ".new"; n = r = a = 0
have = set(); repl = {}
for p in glob.glob(f"{U}/offers_pdf/*.pdf"): repl[f"09_offer_pdfs/{os.path.basename(p)}"] = p
add = {f"10_how_its_made/{os.path.basename(p)}": p for p in glob.glob(f"{U}/explainers/*.mp4")}
with zipfile.ZipFile(tmp, "w", zipfile.ZIP_STORED, allowZip64=True) as out:
    for info in src.infolist():
        rel = info.filename.split("/", 1)[1] if "/" in info.filename else ""; have.add(rel)
        if rel in repl: out.write(repl[rel], info.filename); r += 1
        elif rel in add: out.write(add[rel], info.filename); r += 1
        else:
            with src.open(info) as fsrc, out.open(info, "w") as fdst: shutil.copyfileobj(fsrc, fdst, 1 << 22)
        n += 1
    for rel, p in add.items():
        if rel not in have: out.write(p, f"{root}/{rel}"); a += 1
src.close(); os.replace(tmp, Z); os.chmod(Z, 0o644)
print("PKG_DONE files", n + a, "replaced", r, "added", a, "test", zipfile.ZipFile(Z).testzip(), os.path.getsize(Z))
UZ = f"{DL}/BIG_DOGMA_LTX_update_{datetime.date.today():%Y%m%d}.zip"
with zipfile.ZipFile(UZ, "w", zipfile.ZIP_STORED) as out:
    for rel, p in {**repl, **add}.items(): out.write(p, f"{root}/{rel}")
os.chmod(UZ, 0o644); print("UPDATE_ZIP", os.path.basename(UZ), os.path.getsize(UZ), len(repl) + len(add))
