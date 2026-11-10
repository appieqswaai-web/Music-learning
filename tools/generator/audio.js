/* ---------- 音訊 ---------- */
let ctx,master,noiseBuf;
function initAudio(){if(ctx)return;ctx=new (window.AudioContext||window.webkitAudioContext)();master=ctx.createGain();master.gain.value=.8;
 const comp=ctx.createDynamicsCompressor();master.connect(comp);comp.connect(ctx.destination);
 noiseBuf=ctx.createBuffer(1,ctx.sampleRate,ctx.sampleRate);const d=noiseBuf.getChannelData(0);for(let i=0;i<d.length;i++)d[i]=Math.random()*2-1}
function kick(t){const o=ctx.createOscillator(),g=ctx.createGain();o.frequency.setValueAtTime(140,t);o.frequency.exponentialRampToValueAtTime(45,t+.12);g.gain.setValueAtTime(.9,t);g.gain.exponentialRampToValueAtTime(.001,t+.35);o.connect(g);g.connect(master);o.start(t);o.stop(t+.4)}
function noise(t,dur,type,freq,vol){const s=ctx.createBufferSource();s.buffer=noiseBuf;const f=ctx.createBiquadFilter();f.type=type;f.frequency.value=freq;const g=ctx.createGain();g.gain.setValueAtTime(vol,t);g.gain.exponentialRampToValueAtTime(.001,t+dur);s.connect(f);f.connect(g);g.connect(master);s.start(t);s.stop(t+dur+.02)}
function snare(t){noise(t,.18,"bandpass",1800,.5);const o=ctx.createOscillator(),g=ctx.createGain();o.frequency.value=190;g.gain.setValueAtTime(.3,t);g.gain.exponentialRampToValueAtTime(.001,t+.1);o.connect(g);g.connect(master);o.start(t);o.stop(t+.12)}
function hat(t,acc){noise(t,.04,"highpass",8000,acc?.22:.13)}
function clickS(t,hi){const o=ctx.createOscillator(),g=ctx.createGain();o.frequency.value=hi?1600:1100;g.gain.setValueAtTime(.35,t);g.gain.exponentialRampToValueAtTime(.001,t+.05);o.connect(g);g.connect(master);o.start(t);o.stop(t+.06)}
const SCALE=[0,2,4,5,7,9,11];function deg2midi(d){const o=Math.floor(d/7),r=((d%7)+7)%7;return 64+o*12+SCALE[r]}
const FORM={a:[[800,1],[1150,.5],[2900,.12]],e:[[480,1],[1700,.35],[2500,.12]],i:[[300,1],[2300,.3],[3000,.15]],o:[[460,1],[800,.6],[2800,.06]],u:[[330,1],[700,.35],[2500,.05]]};
function voice(t,dur,deg,acc,vow,cons){const f=440*Math.pow(2,(deg2midi(deg)-69)/12);const end=t+Math.max(.07,dur*.92);
 const o1=ctx.createOscillator(),o2=ctx.createOscillator();o1.type="sawtooth";o2.type="sawtooth";
 o1.frequency.setValueAtTime(f*.97,t);o1.frequency.exponentialRampToValueAtTime(f,t+.05);o2.frequency.setValueAtTime(f*.97*1.004,t);o2.frequency.exponentialRampToValueAtTime(f*1.004,t+.05);
 const vib=ctx.createOscillator(),vg=ctx.createGain();vib.frequency.value=5.2;vg.gain.setValueAtTime(0,t);if(dur>.3)vg.gain.linearRampToValueAtTime(f*.012,t+Math.min(dur*.6,.5));vib.connect(vg);vg.connect(o1.frequency);vg.connect(o2.frequency);
 const src=ctx.createGain();src.gain.value=.5;o1.connect(src);o2.connect(src);
 const out=ctx.createGain();const pk=(acc?1:.78)*({a:1.1,e:1.25,i:.52,o:1,u:.35}[vow]||1);out.gain.setValueAtTime(0,t);out.gain.linearRampToValueAtTime(pk,t+.025);out.gain.setValueAtTime(pk*.85,Math.max(t+.03,end-.05));out.gain.linearRampToValueAtTime(0,end);
 (FORM[vow]||FORM.a).forEach(([fr,amp])=>{const bp=ctx.createBiquadFilter();bp.type="bandpass";bp.frequency.value=fr;bp.Q.value=fr<1000?6:10;const g=ctx.createGain();g.gain.value=amp*1.6;src.connect(bp);bp.connect(g);g.connect(out)});
 out.connect(master);
 if(cons!==false)noise(t,.025,"bandpass",3500,acc?.12:.08);
 [o1,o2,vib].forEach(o=>{o.start(t);o.stop(end+.05)})}

/* ---------- 排程 ---------- */
