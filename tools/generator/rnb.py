import sys;sys.path.insert(0,'.')
from common import *
r=lambda a,b,c=1:list(range(a,b,c))
D={
 "rnb90":{"name":"90s R&B","sub":4,"k":[0,3,10,13],"s":[4,12],"h":r(0,16,2)+[11,15]},
 "njs":{"name":"New Jack Swing（16 分搖擺）","sub":6,"k":[0,9,15],"s":[6,18],"c":[6,18],"h":[0,2,3,5,6,8,9,11,12,14,15,17,18,20,21,23]},
 "neo":{"name":"Neo-Soul（鬆垮鼓）","sub":4,"k":[0,7,10],"s":[4,12],"c":[15],"h":r(0,16,2)},
 "trapsoul":{"name":"Trap Soul（慢速 Trap）","sub":6,"k":[0,15],"s":[12],"c":[12],"h":r(0,18,3)+[18,20,21,22,23],"b":[[0,9,0],[15,9,1]]},
 "soul68":{"name":"6/8（12/8）靈魂抒情","sub":3,"k":[0,7],"s":[3,9],"h":r(0,12,1)},
 "ballad":{"name":"R&B 抒情","sub":4,"k":[0,8,10],"s":[4,12],"h":r(0,16,2)}
}
G={
 "old":{"name":"90s R&B 與 New Jack Swing","desc":"Boyz II Men、TLC、Bobby Brown 的年代。十六分切分的人聲配上有彈性的鼓，New Jack Swing 更加入 16 分搖擺。"},
 "neo":{"name":"Neo-Soul","desc":"D'Angelo、Erykah Badu 開創。鼓和人聲都故意「晚一點」，鬆鬆垮垮卻很有味道。"},
 "contemp":{"name":"當代 R&B / Trap Soul","desc":"Bryson Tiller、The Weeknd、SZA。慢速 Trap 鼓配上三連音的慵懶唱法。"},
 "soul":{"name":"靈魂抒情 6/8","desc":"每拍分成三份的搖籃式律動，經典靈魂樂與 R&B 慢歌常用。"},
 "tech":{"name":"R&B 唱腔技巧","desc":"轉音（Melisma）、句尾 Ad-lib、主唱與和聲應答，是 R&B 聽起來「很 R&B」的關鍵。"}
}
PT=[
 dict(g="old",t="90s 十六分切分",dr="rnb90",sub=4,bpm=92,v="x-.x-.x---x-.x--|.x-.x-x-x-------",ly="你說的那句/還在耳邊",mel=[0,2,4,2,0,2,0,-1,0],
  ex="重音放在「e」「a」這種十六分位置，句子在拍點之間滑動，搭配踢鼓的切分，就是 90 年代 R&B 的「搖」。",how="很多字跟踢鼓錯開半格，不會同時出現。",ref="Boyz II Men、TLC、陶喆早期"),
 dict(g="old",t="New Jack Swing 跳拍",dr="njs",sub=6,bpm=104,v="x-xx-x...x-xx-x-x-----x-|x-xx-x...x-xx-----------",ly="跳起來跟著我的節奏搖/今晚不要停下來",mel=[0,2,2,4,2,0,2,2,4,5,4,2,4,4,5,4,2,0],
  ex="十六分音符長短搖擺，配上用力的小鼓和拍手。比 90s R&B 更跳、更適合跳舞。",how="Hi-hat 的長短搖擺和人聲同一個「跳」法。",ref="Bobby Brown、Michael Jackson〈Remember the Time〉"),
 dict(g="neo",t="Neo-Soul 拖拍（落在 a）",dr="neo",sub=4,bpm=78,v=".x..x..x...x.x--|...x..x..x.x----",ly="慢慢地靠近/不用說話",mel=[2,4,2,0,2,4,2,0,-1],
  ex="每個字都落在拍點之後（e 或 a），像是懶得準時。這種故意的「晚」就是 Neo-Soul 最迷人的地方。",how="人聲幾乎都夾在鼓點之間，不跟踢鼓／小鼓同時出現。",ref="D'Angelo〈Untitled〉、Erykah Badu、H.E.R."),
 dict(g="contemp",t="Trap Soul 三連音慵懶",dr="trapsoul",sub=6,bpm=66,v="x-x-x-x---x-x-x-x-------|x-x-x-x-x-x-------------",ly="凌晨三點我還醒著/螢幕還亮著光",mel=[0,0,2,4,2,2,0,-1,2,2,4,2,0,-1],
  ex="慢速 Trap 鼓上用八分三連音唱，句子一組一組地滾，然後留一大段空白給 808。慵懶、深夜感。",how="三連音的人聲對上直直的 Hi-hat，有輕微的拉扯感。",ref="Bryson Tiller、6LACK、SZA"),
 dict(g="soul",t="6/8 搖籃式抒情",dr="soul68",sub=3,bpm=56,v="x-xx--x-xx--|x-xx--x-----",ly="如果明天下雨/我會等你",mel=[0,2,4,4,5,4,2,4,2,0],
  ex="每拍分成三份，「長—短」的搖擺像搖籃。很多經典靈魂抒情與 R&B 慢歌都是這種 12/8 律動。",how="Hi-hat 每拍打三下，人聲順著這三下的節奏走。",ref="Etta James〈At Last〉、Leon Bridges、經典靈魂抒情"),
 dict(g="tech",t="轉音 Melisma（一字多音）",dr="ballad",sub=4,bpm=70,v="x-x-x-xxxxxx-x--|x-x-xxxxxx------",ly="只想愛你～～～～～呀/永遠不變～～～～",mel=[0,2,4,5,7,5,4,2,1,2,2,4,4,7,5,4,2,0],
  ex="一個字（你、變）拉成一串快速的音高變化（～），這就是 R&B 招牌的轉音。節奏上是一個字佔好幾個十六分音符。",how="～ 的部分沒有新的字，只有音高在動，每個 ～ 佔一個十六分格。",ref="Whitney Houston、Mariah Carey、方大同、A-Lin"),
 dict(g="tech",t="句尾 Ad-lib 轉音收尾",dr="ballad",sub=4,bpm=70,v="x-x-x-x-x-------|x-x-x-xxxxxx----",ly="今晚只想你/陪我到天亮～～～～",mel=[4,4,5,4,2,2,4,5,7,8,7,5,4,4],
  ex="前面正常唱，句尾最後一個字加上一串即興轉音（Ad-lib）。是 R&B 歌手展現個人味道的地方。",how="「亮」唱出後連續四個 16 分音符的轉音，然後收住。",ref="Usher、Brian McKnight、Daniel Caesar"),
 dict(g="tech",t="Call & Response 主唱與和聲應答",dr="rnb90",sub=4,bpm=92,v="x-x-x-x-..x-x---|x-x-x-x-..x-x---",ly="告訴我吧寶貝/別讓我等寶貝",mel=[0,2,4,2,7,7,0,2,4,2,7,5],
  ex="主唱唱四個字，和聲（高音）在後半小節回應兩個字，一問一答。源自福音音樂，R&B 與靈魂樂到處都是。",how="回應句從第 3 拍的「&」才進來，音高突然變高，代表另一個聲部。",ref="福音合唱、Boyz II Men、Destiny's Child")
]
build(open('template.html').read(),open('audio.js').read(),dict(title="R&B 常見節奏型・聽感練習",acc="#0c8599",groups=G,drums=D,patterns=PT,
 intro="<p>分成五組：90s R&B／New Jack Swing、Neo-Soul、當代 Trap Soul、6/8 靈魂抒情、以及 R&B 唱腔技巧（轉音、Ad-lib、和聲應答）。歌詞中的「～」代表同一個字的轉音。</p>",
 footer="<p>練習建議：R&B 的關鍵是「不在拍點上」。先開節拍器，聽清楚每個字比拍點早或晚；轉音的部分先用「啊」慢速唱準每一個音。</p>"),'../../pages/rnb.html')
