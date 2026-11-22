// Renders the ABRACADABRA board to a plain, silent H.264 MP4 that any TV's USB player can play.
//
// How: it does NOT screen-record (that is jerky). It takes transparent snapshots of the live board's
// text layers (menu, promo cards, ticker, price cards) with a headless browser, then ffmpeg composes them
// over the background / wand / cinematic video clips at a steady 30 fps.
//
// usage: node render_menu_video.mjs --screen 1|2 --mode day|night [--minutes 4] [--out TV1_DAY.MP4] [--fps 30] [--size 1080|720]
// needs: Node 18+, `npm i playwright` + `npx playwright install chromium`, and ffmpeg on PATH.
import { chromium } from "playwright";
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath, pathToFileURL } from "node:url";

const arg = (k, d) => { const i = process.argv.indexOf("--" + k); return i > 0 ? process.argv[i + 1] : d; };
const SCREEN = arg("screen", "1") === "2" ? 2 : 1, MODE = String(arg("mode", "day")).toLowerCase() === "night" ? "night" : "day";
const T = Math.round(Number(arg("minutes", "4")) * 60), FPS = Number(arg("fps", "30")), SIZE = Number(arg("size", "1080"));
const OUT = path.resolve(arg("out", `TV${SCREEN}_${MODE.toUpperCase()}.MP4`));
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");           // folder with cinematic-board.html, menu-data.js, assets/
let TOPMAP = {};
try { const c = { window: {} }; vm.createContext(c); vm.runInContext(fs.readFileSync(path.join(root, "assets", "clip-map-ltx25.js"), "utf8"), c); TOPMAP = (c.window.CLIP_MAP_LTX25 || {}).top || {}; } catch {}
const V = (n) => path.join(root, "assets", "video", (TOPMAP[n] || n) + ".mp4");        // same name -> file mapping as the board
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "abra-"));
const T_ = (n) => path.join(tmp, n);
const sh = (cmd, args) => { const r = spawnSync(cmd, args, { stdio: ["ignore", "inherit", "inherit"] }); if (r.status !== 0) { console.error(`${cmd} failed`); process.exit(1); } };
if (spawnSync("ffmpeg", ["-version"]).status !== 0) { console.error("ffmpeg not found on PATH. Install it first (see the guide)."); process.exit(1); }

// ---- read the menu data exactly like the board does
const ctx = { window: {} }; vm.createContext(ctx); vm.runInContext(fs.readFileSync(path.join(root, "menu-data.js"), "utf8"), ctx);
const DATA = ctx.window.MENU_DATA;
const promos = (DATA.promos || []).filter((p) => p.price !== null && p.price !== "" && p.price !== undefined);
if (!promos.length) { console.error("No promos with a price in menu-data.js"); process.exit(1); }
const cineMin = 2, N = promos.length, SEG = 10;
const SUMMON = { wand_burger: "cine_summon_burger", wand_waffle: "cine_summon_waffle", wand_wrap: "cine_summon_wrap", fox_burger: "cine_summon_burger", fox_waffle: "cine_summon_waffle", fox_wrap: "cine_summon_wrap" };
const wandName = (p) => (p.video ? String(p.video).replace(/^fox_/, "wand_") : MODE === "night" ? "wand_idle_night" : "wand_idle_day");
const idleName = MODE === "night" ? "wand_idle_night" : "wand_idle_day";

// ---- 1. transparent snapshots of the live board's text layers
console.log("Taking layer snapshots ...");
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined, args: ["--allow-file-access-from-files", "--hide-scrollbars"] });
const base = pathToFileURL(path.join(root, "cinematic-board.html")).href + `?screen=${SCREEN}&mode=${MODE}&cine=0`;
const HIDE = `html,body,#stage{background:transparent!important}.bg-plane,#bgv,.beams,.rays,.shade,#fx,#fxv,.flashfx,#cine,.grain,.letterbox,#mv,img.mascot{display:none!important}*{animation:none!important;transition:none!important}`;
async function open(extraPromos) {
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  if (extraPromos) await page.route("**/menu-data.js", async (route) => {
    const body = fs.readFileSync(path.join(root, "menu-data.js"), "utf8");
    await route.fulfill({ contentType: "text/javascript", body: body + `\n;window.MENU_DATA.promos=${JSON.stringify([extraPromos[0], extraPromos[0], extraPromos[0]])};window.MENU_DATA.refreshMinutes=9999;` });
  });
  await page.goto(base);
  await page.waitForSelector("#promo .portal", { timeout: 60000 });   // screen 2 has more content and takes longer to lay out
  await page.waitForTimeout(4000);
  await page.addStyleTag({ content: HIDE });
  return page;
}
// base layer: header + menu + ticker frame (promo panel and ticker text hidden)
{
  const page = await open();
  await page.addStyleTag({ content: `aside{visibility:hidden!important}#ticktrack{visibility:hidden!important}` });
  await page.screenshot({ path: T_("ui_base.png"), omitBackground: true });
  // ticker text, captured in 1798 px chunks and stitched (it is wider than the screen)
  await page.addStyleTag({ content: `aside{display:none!important}#menu,header,.ticker{visibility:hidden!important}#ticktrack{visibility:visible!important}footer{background:none!important;border:none!important;box-shadow:none!important;overflow:visible!important}.ticker{overflow:visible!important;visibility:visible!important}` });
  const geo = await page.evaluate(() => { const t = document.getElementById("ticktrack").getBoundingClientRect(); const f = document.querySelector("footer").getBoundingClientRect(); return { x0: t.x, w: t.width, fx: f.x, fy: f.y, fw: f.width, fh: f.height }; });
  const chunks = Math.ceil((geo.w + 1798) / 1798);
  for (let k = 0; k < chunks; k++) {
    await page.evaluate(([dx]) => { document.getElementById("ticktrack").style.transform = `translateX(${dx}px)`; }, [(geo.fx - geo.x0) - k * geo.fw]);
    await page.screenshot({ path: T_(`tk${k}.png`), omitBackground: true, clip: { x: geo.fx, y: geo.fy, width: geo.fw, height: geo.fh } });
  }
  fs.writeFileSync(T_("tick.json"), JSON.stringify({ ...geo, chunks, half: geo.w / 2 }));
  await page.close();
}
// promo panels, one per promo
const aside = { x: 1295, y: 167, w: 577, h: 799 };
for (let k = 0; k < N; k++) {
  const page = await open([promos[k]]);
  await page.addStyleTag({ content: `header,#menu,footer{visibility:hidden!important}` });
  const box = await page.evaluate(() => { const b = document.querySelector("aside").getBoundingClientRect(); return [b.x, b.y, b.width, b.height]; });
  Object.assign(aside, { x: Math.floor(box[0]) - 40, y: Math.floor(box[1]) - 40, w: Math.ceil(box[2]) + 80, h: Math.ceil(box[3]) + 80 });
  await page.screenshot({ path: T_(`promo${k}.png`), omitBackground: true, clip: { x: aside.x, y: aside.y, width: aside.w, height: aside.h } });
  const portal = await page.evaluate(() => { const b = document.querySelector(".portal").getBoundingClientRect(); return [b.x, b.y, b.width, b.height]; });
  fs.writeFileSync(T_("portal.json"), JSON.stringify(portal));
  await page.close();
}
// price cards for the summon cinematics
const summonable = promos.filter((p) => SUMMON[p.video]);
for (let k = 0; k < summonable.length; k++) {
  const page = await open();
  await page.addStyleTag({ content: `header,#menu,aside,footer{display:none!important}#cine{display:block!important;opacity:1!important;background:transparent!important}#cine::after,#cv{display:none!important}.cine-card{opacity:1!important;transform:translate(-50%,0)!important}` });
  await page.evaluate((p) => { const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])); document.getElementById("cineCard").innerHTML = `<h4>${esc(p.title)}</h4><div class="price">${esc(p.price)}<small>ден</small></div>`; }, summonable[k]);
  await page.screenshot({ path: T_(`card${k}.png`), omitBackground: true });
  await page.close();
}
await browser.close();
const tick = JSON.parse(fs.readFileSync(T_("tick.json")));
const portal = JSON.parse(fs.readFileSync(T_("portal.json")));
const chunkList = Array.from({ length: tick.chunks }, (_, k) => T_(`tk${k}.png`));
sh("ffmpeg", ["-y", "-v", "error", ...chunkList.flatMap((c) => ["-i", c]), "-filter_complex", `${chunkList.map((_, i) => `[${i}:v]`).join("")}hstack=inputs=${tick.chunks}`, "-frames:v", "1", T_("ticker.png")]);

// ---- 2. wand layer: one 10 s segment per promo (its summon clip, then the idle loop), cycled for the whole timeline
console.log("Building wand layer ...");
const wh = Math.round(portal[3]), wy = Math.round(portal[1]), wcx = Math.round(portal[0] + portal[2] / 2);
const wandIn = []; const wandF = [];
promos.forEach((p, k) => {
  const nm = wandName(p), idle = nm === idleName;
  const a = wandIn.length; wandIn.push(V(nm)); wandIn.push(V(idleName));
  const ww = Math.round(wh * 0.75 / 2) * 2;
  const clip = idle ? 0 : 8;
  wandF.push(`[${a}:v]trim=0:${idle ? SEG : clip},setpts=PTS-STARTPTS,scale=${ww}:${wh}[c${k}]`);
  wandF.push(idle ? `[c${k}]null[s${k}]` : `[${a + 1}:v]trim=0:${SEG - clip},setpts=PTS-STARTPTS,scale=${ww}:${wh}[i${k}];[c${k}][i${k}]concat=n=2:v=1[s${k}]`);
});
const MASK = `format=gbrp,geq=r='r(X,Y)*clip((1-hypot((X/W-0.5)*2,(Y/H-0.5)*2))/0.34,0,1)':g='g(X,Y)*clip((1-hypot((X/W-0.5)*2,(Y/H-0.5)*2))/0.34,0,1)':b='b(X,Y)*clip((1-hypot((X/W-0.5)*2,(Y/H-0.5)*2))/0.34,0,1)'`;   // soft edge like the board's CSS mask, so the clip's dark box disappears under the screen blend
const cyc = `${promos.map((_, k) => `[s${k}]`).join("")}concat=n=${N}:v=1,fps=${FPS},${MASK},pad=1920:1080:${wcx - Math.round(wh * 0.75 / 2)}:${wy}:black,format=yuv420p[w]`;
sh("ffmpeg", ["-y", "-v", "error", ...wandIn.flatMap((f) => ["-i", f]), "-filter_complex", [...wandF, cyc].join(";"), "-map", "[w]", "-an", "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", T_("wand_cycle.mp4")]);

// ---- 3. timeline events
const slashAt = []; for (let k = 1; k * SEG < T; k++) if (k % 4 === (SCREEN === 2 ? 2 : 0)) slashAt.push(k * SEG);
// full-screen cinematics: one ambient scene, then each food summoned once (burger, waffle, wrap), 60 s apart
const cineAt = []; {
  const seen = new Set(), list = [];
  promos.forEach((p, i) => { const nm = SUMMON[p.video]; if (nm && !seen.has(nm)) { seen.add(nm); list.push({ name: nm, card: summonable.indexOf(p) }); } });
  const seq = [{ name: MODE === "night" ? "cine_neon_night" : "cine_awakening_day", card: null }, ...list];
  let t = 20 + (SCREEN === 2 ? 30 : 0);
  for (const c of seq) { if (t + 10 <= T) cineAt.push({ t, ...c }); t += 60; }
}
console.log(`Slashes at ${slashAt.join(", ") || "-"} s; cinematics at ${cineAt.map((c) => c.t + "s(" + c.name + ")").join(", ") || "-"}`);

// ---- 4. final composition
console.log("Composing the video (this takes a few minutes) ...");
const inputs = []; const F = []; let nx = 0;
const add = (args) => { inputs.push(...args); return nx++; };
const bgName = MODE === "night" ? "bg_night" : "bg_day";
sh("ffmpeg", ["-y", "-v", "error", "-i", V(bgName), "-an", "-filter_complex", "[0:v]split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1[v]", "-map", "[v]", "-c:v", "libx264", "-crf", "14", "-preset", "veryfast", T_("bg_loop.mp4")]);
const ibg = add(["-stream_loop", "-1", "-i", T_("bg_loop.mp4")]);
const iui = add(["-loop", "1", "-framerate", String(FPS), "-i", T_("ui_base.png")]);
const ipr = promos.map((_, k) => add(["-loop", "1", "-framerate", String(FPS), "-i", T_(`promo${k}.png`)]));
const iwd = add(["-stream_loop", "-1", "-i", T_("wand_cycle.mp4")]);
const itk = add(["-loop", "1", "-framerate", String(FPS), "-i", T_("ticker.png")]);
const ifx = slashAt.map(() => add(["-i", V("fx_slash")]));
const icn = cineAt.map((c) => add(["-i", V(c.name)]));
const icd = cineAt.map((c) => (c.card !== null ? add(["-loop", "1", "-framerate", String(FPS), "-i", T_(`card${c.card}.png`)]) : -1));

F.push(`[${ibg}:v]fps=${FPS},scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1,format=yuv420p[bg]`);
F.push(`[bg][${iui}:v]overlay=0:0:format=auto[a0]`);
let cur = "a0";
ipr.forEach((ix, k) => {
  F.push(`[${ix}:v]format=rgba[pr${k}]`);
  F.push(`[${cur}][pr${k}]overlay=${aside.x}:${aside.y}:format=auto:enable='lt(mod(t\\,${N * SEG})\\,${(k + 1) * SEG})*gte(mod(t\\,${N * SEG})\\,${k * SEG})'[p${k}]`);
  cur = `p${k}`;
});
F.push(`[${cur}]format=gbrp[bw]`);
F.push(`[${iwd}:v]fps=${FPS},format=gbrp[wd]`);
F.push(`[bw][wd]blend=all_mode=screen[wb]`);
F.push(`[${itk}:v]format=rgba,crop=${tick.fw}:${tick.fh}:x='mod(t*${(tick.half / 46).toFixed(4)}\\,${tick.half.toFixed(2)})':y=0[tk]`);
F.push(`[wb]format=yuv420p[wb2]`);
F.push(`[wb2][tk]overlay=${Math.round(tick.fx)}:${Math.round(tick.fy)}:format=auto[t0]`);
cur = "t0";
slashAt.forEach((t, i) => {
  F.push(`[${ifx[i]}:v]fps=${FPS},scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setpts=PTS-STARTPTS+${t}/TB,format=gbrp[fx${i}]`);
  F.push(`[${cur}]format=gbrp[b${i}];[b${i}][fx${i}]blend=all_mode=screen:enable='between(t\\,${t}\\,${t + 5})':eof_action=pass,format=yuv420p[f${i}]`);
  cur = `f${i}`;
});
cineAt.forEach((c, i) => {
  F.push(`[${icn[i]}:v]fps=${FPS},scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setpts=PTS-STARTPTS+${c.t}/TB,format=yuva420p,fade=in:st=${c.t}:d=0.8:alpha=1,fade=out:st=${c.t + 9.2}:d=0.8:alpha=1[cn${i}]`);
  F.push(`[${cur}][cn${i}]overlay=0:0:format=auto:enable='between(t\\,${c.t}\\,${c.t + 10})':eof_action=pass[c${i}]`);
  cur = `c${i}`;
  if (icd[i] >= 0) {
    F.push(`[${icd[i]}:v]format=rgba[cd${i}]`);
    F.push(`[${cur}][cd${i}]overlay=0:0:format=auto:enable='between(t\\,${c.t + 6.4}\\,${c.t + 9.4})'[d${i}]`);
    cur = `d${i}`;
  }
});
const scale = SIZE === 720 ? `,scale=1280:720:flags=lanczos` : "";
F.push(`[${cur}]format=yuv420p${scale}[out]`);
// Old TV players are picky: H.264 Main profile, constant 30 fps, plus a silent audio track (some players refuse video-only files)
sh("ffmpeg", ["-y", "-v", "error", "-stats", "-stats_period", "15", ...inputs, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-filter_complex", F.join(";"), "-map", "[out]", "-map", `${nx}:a`, "-t", String(T), "-r", String(FPS),
  "-c:v", "libx264", "-profile:v", "main", "-level", "4.0", "-crf", "28", "-maxrate", "9M", "-bufsize", "18M", "-g", String(FPS * 2), "-preset", "medium", "-pix_fmt", "yuv420p",
  "-c:a", "aac", "-b:a", "64k", "-ar", "48000", "-shortest", "-movflags", "+faststart", OUT]);
fs.rmSync(tmp, { recursive: true, force: true });
console.log(`Done: ${OUT} (${(fs.statSync(OUT).size / 1e6).toFixed(0)} MB, ${T} s)`);
