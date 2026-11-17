/* 鼓聲風格切換：覆寫頁面上的 kick/snare/hat/clap/ohat，所有練習頁共用 */
(function(){
const ORIG={kick:window.kick,snare:window.snare,hat:window.hat,clap:window.clap,ohat:window.ohat};
function nz(t,dur,type,freq,vol,q){const s=ctx.createBufferSource();s.buffer=noiseBuf;const f=ctx.createBiquadFilter();f.type=type;f.frequency.value=freq;if(q)f.Q.value=q;const g=ctx.createGain();g.gain.setValueAtTime(vol,t);g.gain.exponentialRampToValueAtTime(.001,t+dur);s.connect(f);f.connect(g);g.connect(master);s.start(t);s.stop(t+dur+.02)}
function tone(t,f0,f1,dropT,dur,vol,type,sat){const o=ctx.createOscillator(),g=ctx.createGain();o.type=type||"sine";o.frequency.setValueAtTime(f0,t);o.frequency.exponentialRampToValueAtTime(f1,t+dropT);g.gain.setValueAtTime(vol,t);g.gain.exponentialRampToValueAtTime(.001,t+dur);
 let n=o;if(sat){const sh=ctx.createWaveShaper(),c=new Float32Array(256);for(let i=0;i<256;i++){const x=i/128-1;c[i]=Math.tanh(sat*x)}sh.curve=c;o.connect(sh);n=sh}n.connect(g);g.connect(master);o.start(t);o.stop(t+dur+.05)}
const KITS={
 classic:{name:"原本",...ORIG},
 modern:{name:"現代 808",
  kick:t=>{tone(t,130,46,.07,.75,1,"sine",2.2)},
  snare:t=>{[0,.011,.022].forEach((d,i)=>nz(t+d,i<2?.02:.17,"bandpass",1500,.5));nz(t,.05,"highpass",5000,.2)},
  hat:(t,acc)=>nz(t,.025,"highpass",9500,acc?.17:.1),
  clap:t=>{[0,.011,.022].forEach((d,i)=>nz(t+d,i<2?.02:.15,"bandpass",1400,.45))},
  ohat:t=>nz(t,.18,"highpass",8500,.13)},
 lofi:{name:"Lo-fi 柔和",
  kick:t=>tone(t,95,48,.06,.3,.75),
  snare:t=>{nz(t,.16,"lowpass",2600,.32);tone(t,210,170,.05,.09,.12,"triangle")},
  hat:(t,acc)=>nz(t,.03,"bandpass",6000,acc?.07:.045,1.5),
  clap:t=>nz(t,.12,"bandpass",1100,.25),
  ohat:t=>nz(t,.14,"bandpass",6500,.06,1.5)},
 rock:{name:"樂團原聲鼓",
  kick:t=>{tone(t,150,55,.04,.28,1,"sine",1.5);nz(t,.012,"highpass",3000,.25)},
  snare:t=>{nz(t,.22,"bandpass",2200,.55,.8);tone(t,240,180,.04,.12,.35,"triangle")},
  hat:(t,acc)=>nz(t,.06,"highpass",7000,acc?.2:.13),
  clap:t=>nz(t,.08,"highpass",3500,.3),
  ohat:t=>nz(t,.35,"highpass",6500,.16)}
};
let cur="modern";try{cur=localStorage.getItem("drumKit")||cur}catch(e){}
if(!KITS[cur])cur="modern";
["kick","snare","hat","clap","ohat"].forEach(fn=>{if(typeof window[fn]!=="function")return;window[fn]=function(t,a){const k=KITS[cur],f=k[fn]||ORIG[fn];return f(t,a)}});
const bar=document.querySelector(".bar .in");if(bar){const s=document.createElement("label");
 s.innerHTML='鼓聲 <select id="kitsel">'+Object.entries(KITS).map(([k,v])=>`<option value="${k}"${k===cur?" selected":""}>${v.name}</option>`).join("")+'</select>';
 bar.insertBefore(s,bar.children[1]||null);s.querySelector("select").onchange=e=>{cur=e.target.value;try{localStorage.setItem("drumKit",cur)}catch(_){}}}
})();
