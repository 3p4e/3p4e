const {chromium}=require('playwright');const fs=require('fs');const S=process.argv[2];
const T=JSON.parse(fs.readFileSync(S+'/cut/page_tokens.json'));
(async()=>{const b=await chromium.launch();
for(const id of ['06_beograd_na_vodi_RS','05_foton_MK','01_zito_marketi_MK','02_alkaloid_MK','12_speeex_XK','07_millennium_team_RS']){
 for(const [w,h,tag] of [[1366,900,'d'],[390,844,'m']]){const p=await b.newPage({viewport:{width:w,height:h}});
  await p.goto('file://'+S+'/pitch_site/site/'+T[id]+'/index.html');await p.waitForTimeout(800);
  await p.evaluate(()=>document.querySelectorAll('.rv').forEach(e=>e.classList.add("in")));await p.waitForTimeout(1200);
  await p.screenshot({path:`${S}/qc/site_${id}_${tag}.png`,fullPage:true});await p.close();}}
await b.close();})();
