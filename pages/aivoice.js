/* DiffSinger AI 歌聲（音檔由 GitHub Actions 預先產生在 assets/<頁>/）
   J-POP：<script src="aivoice.js">（預設 ../assets/jpop/，速度倍率 #spd）
   流行樂：<script src="aivoice.js" data-dir="../assets/pop/">（每張卡有 70/90/120 BPM 版本，依 #bpm 挑最接近的） */
window.AIV=(function(){
const me=document.currentScript,DIR=(me&&me.dataset.dir)||"../assets/jpop/";let on=true;try{on=localStorage.getItem("aiVoice")!=="off"}catch(e){}
const raw={},buf={};let srcs=[],bpms=null;
fetch(DIR+"index.json").then(r=>r.json()).then(ix=>{let files=ix;if(ix.files){files=ix.files;bpms=ix.bpms}
 return Promise.all(Object.entries(files).map(([k,f])=>fetch(DIR+f).then(r=>r.arrayBuffer()).then(a=>{raw[k]=a})))}).catch(()=>{});
function decodeAll(){if(typeof initAudio==="function")initAudio();if(!ctx)return;
 Object.keys(raw).forEach(i=>{if(buf[i]||raw[i]==null)return;const a=raw[i];raw[i]=null;ctx.decodeAudioData(a,b=>{buf[i]=b},()=>{})})}
document.addEventListener("click",decodeAll,true);
const bar=document.querySelector(".bar .in");if(bar){const l=document.createElement("label");
 l.innerHTML='人聲 <select id="aisel"><option value="on">AI 歌聲（DiffSinger）</option><option value="off">母音合成</option></select>';
 bar.insertBefore(l,bar.children[1]||null);const s=l.querySelector("select");s.value=on?"on":"off";s.onchange=()=>{on=s.value==="on";try{localStorage.setItem("aiVoice",on?"on":"off")}catch(e){}}}
/* 挑音檔：回傳 [key, playbackRate]，不適合就回傳 null（改用母音合成） */
function pick(i,rate){
 if(bpms){const el=document.getElementById("bpm"),b=el?+el.value:90;let best=bpms[0];bpms.forEach(x=>{if(Math.abs(x-b)<Math.abs(best-b))best=x});
  const r=b/best,k=i+"_"+best;return buf[k]&&r>=.83&&r<=1.2?[k,r]:null}  /* 超過約 ±3 個半音就換回合成聲 */
 const e=document.getElementById("spd");if(e&&e.value<50)return null;return buf[i]?[i,rate||1]:null}
return{
 has:i=>on&&!!pick(i),
 start(i,t,rate){decodeAll();if(!on)return;const k=pick(i,rate);if(!k)return;const s=ctx.createBufferSource();s.buffer=buf[k[0]];s.playbackRate.value=k[1];const g=ctx.createGain();g.gain.value=1.1;s.connect(g);g.connect(master);s.start(t);srcs.push(s)},
 stop(){srcs.forEach(s=>{try{s.stop()}catch(e){}});srcs=[]}
}})();
