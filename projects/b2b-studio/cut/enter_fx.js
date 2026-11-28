/* enter transitions (owner 2026-11-28): five effects, one picked at random on every load. Each: 220 ms fade to black, switch to the content, ~1 s reveal. */
var bc=$('#burst'),b=bc.getContext('2d'),FXI=/[?&]fx=[0-4]/.test(location.search)?+location.search.match(/fx=([0-4])/)[1]:Math.floor(Math.random()*5);
function burst(done){var D=Math.min(2,devicePixelRatio||1),W=bc.width=innerWidth*D,H=bc.height=innerHeight*D,cx=W/2,cy=H/2,R=Math.hypot(W,H)/2,t0=performance.now(),sw=false,GOLD='242,193,78';
 var tiles=[],n=16,m=Math.ceil(n*H/W);for(var y=0;y<m;y++)for(var x=0;x<n;x++)tiles.push([x,y,(x+y)/(n+m)*.7+Math.random()*.15]);
 function ease(t){return t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2}
 var FX=[
  function(q){var r=R*1.08*ease(q);b.fillStyle='#000';b.beginPath();b.rect(0,0,W,H);b.arc(cx,cy,r,0,6.283,true);b.fill();
   b.strokeStyle='rgba('+GOLD+','+(1-q)+')';b.lineWidth=W/240*(1-q*.6);b.beginPath();b.arc(cx,cy,r,0,6.283);b.stroke();
   b.strokeStyle='rgba(255,240,205,'+(.6*(1-q))+')';b.lineWidth=W/900;b.beginPath();b.arc(cx,cy,r*.94,0,6.283);b.stroke()},
  function(q){var e=ease(q),h=W/2*(1-e);b.fillStyle='#000';b.fillRect(0,0,h,H);b.fillRect(W-h,0,h,H);
   var g=b.createLinearGradient(h-W/60,0,h+W/60,0);g.addColorStop(0,'rgba('+GOLD+',0)');g.addColorStop(.5,'rgba('+GOLD+','+(1-q*.7)+')');g.addColorStop(1,'rgba('+GOLD+',0)');b.fillStyle=g;b.fillRect(h-W/60,0,W/30,H);
   g=b.createLinearGradient(W-h-W/60,0,W-h+W/60,0);g.addColorStop(0,'rgba('+GOLD+',0)');g.addColorStop(.5,'rgba('+GOLD+','+(1-q*.7)+')');g.addColorStop(1,'rgba('+GOLD+',0)');b.fillStyle=g;b.fillRect(W-h-W/60,0,W/30,H)},
  function(q){var k=12,sh=H/k;for(var i=0;i<k;i++){var d=Math.max(0,Math.min(1,(q*1.6-i/k*.6))),e=ease(d),hh=sh*(1-e);b.fillStyle='#000';b.fillRect(0,i*sh+(sh-hh)/2,W,hh);
   if(d>0&&d<1){b.fillStyle='rgba('+GOLD+','+(1-d)*.9+')';b.fillRect(0,i*sh+(sh-hh)/2,W,Math.max(1,W/1600));b.fillRect(0,i*sh+(sh+hh)/2,W,Math.max(1,W/1600))}}},
  function(q){var tw=W/n,th=H/m;tiles.forEach(function(t){var d=Math.max(0,Math.min(1,(q-t[2])/.3)),s=1-ease(d);if(s>0){b.fillStyle='#000';b.fillRect(t[0]*tw+tw*(1-s)/2,t[1]*th+th*(1-s)/2,tw*s+.5,th*s+.5)}
   if(d>0&&d<1){b.fillStyle='rgba('+GOLD+','+(1-d)*.8+')';b.fillRect(t[0]*tw+tw/2-1,t[1]*th+th/2-1,W/700,W/700)}})},
  function(q){var e=ease(q),span=W+H,p=-H*.3+span*1.3*e;b.save();b.translate(0,0);b.fillStyle='#000';b.beginPath();b.moveTo(p,0);b.lineTo(W*2,0);b.lineTo(W*2,H);b.lineTo(p-H*.6,H);b.closePath();b.fill();
   var g=b.createLinearGradient(p-W*.12,0,p+W*.02,H*.1);g.addColorStop(0,'rgba('+GOLD+',0)');g.addColorStop(.75,'rgba(255,236,190,'+(.85*(1-q*.5))+')');g.addColorStop(1,'rgba('+GOLD+',0)');
   b.fillStyle=g;b.beginPath();b.moveTo(p-W*.12,0);b.lineTo(p+W*.02,0);b.lineTo(p+W*.02-H*.6,H);b.lineTo(p-W*.12-H*.6,H);b.closePath();b.fill();b.restore()}];
 (function f(now){var t=now-t0;b.clearRect(0,0,W,H);
  if(t<220){b.fillStyle='rgba(0,0,0,'+(t/220)+')';b.fillRect(0,0,W,H)}
  else{if(!sw){sw=true;try{sp.style.transition="none"}catch(e){}done()}var q=Math.min(1,(t-220)/1050);FX[FXI](q);if(q>=1){b.clearRect(0,0,W,H);return}}
  requestAnimationFrame(f)})(t0)}
