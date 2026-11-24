const {chromium}=require('playwright');const fs=require('fs');const svg=fs.readFileSync(process.argv[2],'utf8');const [W,H]=svg.match(/viewBox="0 0 (\d+) (\d+)"/).slice(1).map(Number);const k=+process.argv[4];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:Math.round(W*k),height:Math.round(H*k)}});
await p.setContent(`<body style="margin:0;background:#fff"><div style="color:#000;width:${Math.round(W*k)}px;height:${Math.round(H*k)}px">${svg.replace('<svg ','<svg style="width:100%;height:100%;display:block" ')}</div></body>`);
await p.screenshot({path:process.argv[3]});await b.close();})();
