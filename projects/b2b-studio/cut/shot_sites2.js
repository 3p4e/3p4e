const {chromium}=require('playwright');const fs=require('fs');const S=process.argv[2];const T=JSON.parse(fs.readFileSync(S+'/cut/page_tokens.json'));
(async()=>{const b=await chromium.launch();
 const p=await b.newPage({viewport:{width:1440,height:900}});   // preloader frame
 await p.goto('file://'+S+'/pitch_site/site/'+T['05_foton_MK']+'/index.html');await p.waitForTimeout(3300);await p.screenshot({path:S+'/qc/v2_pre.png'});
 for(const id of ['05_foton_MK','06_beograd_na_vodi_RS','02_alkaloid_MK','12_speeex_XK']){
  const q=await b.newPage({viewport:{width:1440,height:900}});await q.addInitScript(()=>sessionStorage.setItem('dogma_pre','1'));
  await q.goto('file://'+S+'/pitch_site/site/'+T[id]+'/index.html');await q.waitForTimeout(4200);await q.screenshot({path:`${S}/qc/v2_${id}_hero.png`});
  await q.evaluate(()=>document.querySelectorAll('.rv').forEach(e=>e.classList.add('in')));
  for(const [sel,tag] of [['.marq','stats'],['#ai','ai']]){await q.evaluate(s=>document.querySelector(s).scrollIntoView(),sel);await q.waitForTimeout(2600);await q.screenshot({path:`${S}/qc/v2_${id}_${tag}.png`});}
  await q.close();}
 const m=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:1});await m.addInitScript(()=>sessionStorage.setItem('dogma_pre','1'));
 await m.goto('file://'+S+'/pitch_site/site/'+T['01_zito_marketi_MK']+'/index.html');await m.waitForTimeout(3000);await m.screenshot({path:S+'/qc/v2_mobile.png'});
 await b.close();})();
