/* 打拍子練習：跟著人聲節奏點下面的大按鈕，網頁即時判斷早或晚（扣掉節拍器校準存的延遲） */
window.TAP=(function(){
const NAMES={speaker:"手機喇叭",wired:"有線耳機",bt:"藍牙耳機"};
function calib(){try{return JSON.parse(localStorage.getItem("tapCalib")||"{}")}catch(e){return{}}}
let card=-1,exp=[],marks=[],loopN=0,stats=null,iv=null,out=calib().current||"speaker";
const css=document.createElement("style");css.textContent=`
#tapp{position:fixed;left:0;right:0;bottom:0;z-index:50;background:var(--card);border-top:2px solid var(--acc);box-shadow:0 -6px 20px rgba(0,0,0,.15);padding:10px 12px calc(10px + env(safe-area-inset-bottom));display:none;-webkit-user-select:none;user-select:none}
#tapp.on{display:block}body.tapping{padding-bottom:50vh}
#tapp .tr{display:flex;flex-wrap:wrap;gap:8px;align-items:center;font-size:.86rem;max-width:920px;margin:0 auto}
#tapp .tr b.t{flex:1;min-width:120px}
#tappad{max-width:920px;margin:8px auto;height:20vh;min-height:110px;border-radius:18px;border:2px dashed var(--acc);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:1.2rem;color:var(--acc);touch-action:manipulation;cursor:pointer;background:color-mix(in srgb,var(--acc) 6%,var(--card))}
#tappad.hit{background:color-mix(in srgb,var(--acc) 25%,var(--card))}
#tapfb{font-size:1.6rem;font-weight:800;text-align:center;min-height:2rem}
#tapcv{display:block;width:100%;max-width:920px;height:64px;margin:0 auto}
#tapst{text-align:center;font-size:.86rem;color:var(--mute);max-width:920px;margin:2px auto 0}
.btn.tapb{margin-left:4px}`;document.head.appendChild(css);
const box=document.createElement("div");box.id="tapp";box.innerHTML=`
<div class="tr"><b class="t" id="tapt"></b>
<label>輸出 <select id="tapout">${Object.entries(NAMES).map(([k,v])=>`<option value="${k}">${v}</option>`).join("")}</select></label><span id="tapcal"></span>
<button class="btn" id="tapx">✕ 結束</button></div>
<div id="tappad">跟著「人聲節奏」在這裡點</div>
<div id="tapfb"></div><canvas id="tapcv"></canvas><div id="tapst"></div>`;
document.body.appendChild(box);
const $t=id=>document.getElementById(id);
function calMs(){const c=calib()[out];return c?c.ms:0}
function showCal(){$t("tapout").value=out;const c=calib()[out];$t("tapcal").innerHTML=c?`校準 ${c.ms>0?"+":""}${c.ms} ms`:`<a href="metronome.html" target="_top" onclick="parent.location.hash='metro';return false">尚未校準 ⏱️</a>`}
$t("tapout").onchange=e=>{out=e.target.value;const all=calib();all.current=out;try{localStorage.setItem("tapCalib",JSON.stringify(all))}catch(_){}showCal()};
function win(p){const sd=60/bpmOf(p)/p.sub;return Math.min(.15,Math.max(.06,sd*1.2))}
function open(i){stop();card=i;exp=[];marks=[];loopN=0;stats={n:0,ok:0,good:0,miss:0,sum:0};
 $t("tapt").textContent="🥁 #"+(i+1)+" "+P[i].t;$t("tapfb").textContent="";showCal();box.classList.add("on");document.body.classList.add("tapping");
 document.getElementById("c"+i).scrollIntoView({behavior:"smooth",block:"start"});
 if(cur!==i)toggle(i);iv=setInterval(tick,60);draw();stat()}
function close(){box.classList.remove("on");document.body.classList.remove("tapping");clearInterval(iv);if(card>=0&&cur===card)stop();card=-1}
$t("tapx").onclick=close;
function expect(t,j,s){if(card<0||cur!==card)return;const p=P[card];if(s===p.notes[0].st&&exp.length){loopN++;marks=[]}exp.push({t,s,j,hit:false,miss:false});if(exp.length>64)exp.splice(0,exp.length-64)}
function grade(d){const a=Math.abs(d);return a<=35?["準！","var(--ok,#2f9e44)",2]:a<=75?[(d<0?"稍早 ":"稍晚 "),d<0?"#1c7ed6":"#e8590c",1]:[(d<0?"太早 ":"太晚 "),d<0?"#1c7ed6":"#e8590c",0]}
function tap(e){if(e.cancelable)e.preventDefault();if(card<0)return;if(cur!==card){toggle(card);return}
 const p=P[card],lag=Math.max(0,(performance.now()-(e.timeStamp||performance.now()))/1000),t=ctx.currentTime-lag-calMs()/1000,w=win(p);
 let best=null;for(const x of exp){if(x.hit||x.miss)continue;if(Math.abs(t-x.t)<=w*1.6&&(!best||Math.abs(t-x.t)<Math.abs(t-best.t)))best=x}
 const pad=$t("tappad");pad.classList.add("hit");setTimeout(()=>pad.classList.remove("hit"),80);
 const fb=$t("tapfb");
 if(!best){fb.textContent="多點了一下";fb.style.color="var(--mute)";return}
 best.hit=true;const d=(t-best.t)*1000,[txt,col,sc]=grade(d);
 fb.textContent=txt+(sc===2?"":Math.round(Math.abs(d))+" ms");fb.style.color=col;
 stats.n++;stats.sum+=d;if(sc===2)stats.ok++;else if(sc===1)stats.good++;
 marks.push({s:best.s,d,col});draw();stat()}
function tick(){if(card<0)return;if(cur!==card)return;
 const p=P[card],now=ctx.currentTime-calMs()/1000,w=win(p)*1.6;let ch=false;
 for(const x of exp){if(!x.hit&&!x.miss&&now>x.t+w){x.miss=true;stats.miss++;marks.push({s:x.s,miss:true});ch=true}}if(ch){draw();stat()}}
function stat(){const s=stats,tot=s.ok+s.good+(s.n-s.ok-s.good)+s.miss;if(!tot){$t("tapst").textContent="先數一小節，然後跟著人聲的每個字點一下。";return}
 const avg=s.n?Math.round(s.sum/s.n):0;$t("tapst").textContent=`第 ${loopN+1} 輪 ・ 準 ${s.ok}　稍偏 ${s.good}　偏太多 ${s.n-s.ok-s.good}　漏掉 ${s.miss} ・ 平均${avg<0?"早":"晚"} ${Math.abs(avg)} ms`}
function draw(){const c=$t("tapcv");if(card<0||!c)return;const p=P[card],dpr=devicePixelRatio||1,W=c.clientWidth,H=c.clientHeight;c.width=W*dpr;c.height=H*dpr;const g=c.getContext("2d");g.scale(dpr,dpr);
 const cs=getComputedStyle(document.documentElement),ink=cs.getPropertyValue("--mute")||"#888",x=s=>6+(W-12)*s/p.steps,sd=60/bpmOf(p)/p.sub;
 for(let s=0;s<=p.steps;s+=p.sub){g.fillStyle=ink;g.globalAlpha=s%(p.sub*4)===0?.8:.35;g.fillRect(x(s),4,s%(p.sub*4)===0?2:1,H-8)}g.globalAlpha=1;
 p.notes.forEach(n=>{g.fillStyle=cs.getPropertyValue("--acc")||"#d9480f";g.globalAlpha=.35;g.fillRect(x(n.st),H/2-7,Math.max(3,x(n.st+n.len)-x(n.st)-2),14);g.globalAlpha=1;g.fillRect(x(n.st),H/2-10,2,20)});
 marks.forEach(m=>{if(m.miss){g.strokeStyle="#e03131";g.lineWidth=2;const X=x(m.s);g.beginPath();g.moveTo(X-5,H/2-5);g.lineTo(X+5,H/2+5);g.moveTo(X+5,H/2-5);g.lineTo(X-5,H/2+5);g.stroke();return}
  g.fillStyle=m.col;g.beginPath();g.arc(x(m.s+m.d/1000/sd),H/2,6,0,7);g.fill()})}
$t("tappad").addEventListener("pointerdown",tap);
document.addEventListener("keydown",e=>{if(card>=0&&(e.code==="KeyJ"||e.code==="KeyF"||e.code==="Enter")){tap(e)}});
addEventListener("resize",draw);
document.querySelectorAll(".card").forEach(c=>{const i=+c.id.slice(1),b=document.createElement("button");b.className="btn tapb";b.textContent="🥁 打拍子";b.onclick=()=>open(i);c.querySelector(".play").after(b)});
return{expect,open,close}})();
