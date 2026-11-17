/* J-POP 頁：DiffSinger AI 歌聲（音檔由 GitHub Actions 預先產生在 assets/jpop/） */
window.AIV=(function(){
const DIR="../assets/jpop/";let on=true;try{on=localStorage.getItem("aiVoice")!=="off"}catch(e){}
const raw={},buf={};let srcs=[],decoding=null;
fetch(DIR+"index.json").then(r=>r.json()).then(ix=>Promise.all(Object.entries(ix).map(([i,f])=>fetch(DIR+f).then(r=>r.arrayBuffer()).then(a=>{raw[i]=a})))).catch(()=>{});
function decodeAll(){if(typeof initAudio==="function")initAudio();if(!ctx)return;
 Object.keys(raw).forEach(i=>{if(buf[i]||raw[i]==null)return;const a=raw[i];raw[i]=null;ctx.decodeAudioData(a,b=>{buf[i]=b},()=>{})})}
document.addEventListener("click",decodeAll,true);
const bar=document.querySelector(".bar .in");if(bar){const l=document.createElement("label");
 l.innerHTML='人聲 <select id="aisel"><option value="on">AI 歌聲（DiffSinger）</option><option value="off">母音合成</option></select>';
 bar.insertBefore(l,bar.children[1]||null);const s=l.querySelector("select");s.value=on?"on":"off";s.onchange=()=>{on=s.value==="on";try{localStorage.setItem("aiVoice",on?"on":"off")}catch(e){}}}
function slowOK(){const e=document.getElementById("spd");return !e||e.value>=50}
return{
 has:i=>on&&!!buf[i]&&slowOK(),
 start(i,t,rate){decodeAll();if(!on||!buf[i]||!slowOK())return;const s=ctx.createBufferSource();s.buffer=buf[i];s.playbackRate.value=rate||1;const g=ctx.createGain();g.gain.value=1.1;s.connect(g);g.connect(master);s.start(t);srcs.push(s)},
 stop(){srcs.forEach(s=>{try{s.stop()}catch(e){}});srcs=[]}
}})();
