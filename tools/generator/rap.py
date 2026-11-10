import sys;sys.path.insert(0,'.')
from common import *
r=lambda a,b,c=1:list(range(a,b,c))
D={
 "old":{"name":"Old School（Funk 碎拍）","sub":4,"k":[0,7,8],"s":[4,12],"c":[4,12],"h":r(0,16,2)},
 "boom":{"name":"Boom Bap","sub":4,"k":[0,7,10,11],"s":[4,12],"h":r(0,16,2),"o":[14]},
 "trap":{"name":"Trap（半速＋Hi-hat 連打）","sub":6,"k":[0,15],"s":[12],"c":[12],"h":r(0,18,3)+r(18,24,1),"b":[[0,9,0],[15,9,0]]},
 "trap4":{"name":"Trap（16 分格）","sub":4,"k":[0,10],"s":[8],"c":[8],"h":r(0,12,2)+[12,13,14,15],"b":[[0,7,0],[10,6,1]]},
 "chop":{"name":"快嘴 16 Beat","sub":4,"k":[0,3,8,10],"s":[4,12],"h":r(0,16,1)},
 "drill":{"name":"Drill（滑音 808＋三連 Hi-hat）","sub":6,"k":[0],"s":[12,21],"h":[0,2,4,6,9,10,12,14,16,18,20,22],"b":[[0,6,0],[8,4,1],[15,6,1]]},
 "jazz":{"name":"Jazz Rap（慵懶鼓）","sub":4,"k":[0,10],"s":[4,12],"c":[15],"h":[0,3,4,6,8,11,12,14]}
}
G={
 "old":{"name":"Old School 老派饒舌","desc":"1980 年代起源，節奏「正」、字跟著拍點走，句尾押韻，像在帶動現場氣氛。"},
 "boom":{"name":"Boom Bap","desc":"90 年代東岸，鼓「咚—啪」很重，人聲用 16 分切分和內韻（句子中間也押韻），講究技巧與歌詞。"},
 "trap":{"name":"Trap","desc":"2010 年代主流，半速鼓＋Hi-hat 連打＋808 低音。招牌是三連音 Flow 和短句留白。"},
 "mel":{"name":"Melodic Rap 旋律饒舌","desc":"半唱半唸，有旋律線、常配 Auto-tune，句子較短，尾音拉長。"},
 "chop":{"name":"快嘴 Chopper / Fast Rap","desc":"比誰快、誰穩。一拍塞 4 個字以上，靠呼吸與咬字控制。"},
 "drill":{"name":"Drill","desc":"源自芝加哥、英國，陰暗、壓迫。三連音 Hi-hat、滑音 808、小鼓不在正拍上，人聲從反拍進來、帶點三連彈跳。"},
 "jazz":{"name":"Jazz Rap / Lo-fi","desc":"爵士取樣、鼓很鬆。人聲故意晚一點點（behind the beat），像在聊天。"}
}
PT=[
 dict(g="old",t="八分平均・句尾押韻",dr="old",sub=4,bpm=100,rap=1,v="x-x-x-x-x-x-x---|x-x-x-x-x-x-x---",ly="麥克風握在手中/節奏響起往前衝",
  ex="一個字一個八分音符，句尾停在第 4 拍並押韻（中、衝）。這是最早期饒舌的骨架，簡單、好跟、適合帶動現場。",how="每句結尾空出半拍，下一句準時在第 1 拍進來。",ref="Run-DMC、Sugarhill Gang 這類 80 年代老派饒舌"),
 dict(g="old",t="正拍喊句・Call 現場",dr="old",sub=4,bpm=100,rap=1,v="x---x---x-x-x---|x---x---x-x-x---",ly="大家一起來/舉起你的手",
  ex="前兩個字踩四分音符，後面三個字變八分加速，像 MC 在喊口號。重點是「正」：每個重音都在拍點上。",how="「大、家」跟小鼓／踢鼓同時打，聽起來很有力。",ref="老派派對饒舌、現場 Hype 段落"),
 dict(g="boom",t="十六分切分・內韻",dr="boom",sub=4,bpm=90,rap=1,v="x-xx-x-xx-x-x---|.xx-x-xx-x-xx---",ly="老派的鼓點在耳邊/一字一句都是經驗",
  ex="字落在「e」「a」的十六分位置，不再乖乖踩拍點。句子裡面就有押韻（點、邊／句、驗），這是 Boom Bap 技術派的味道。",how="第二小節從第 1 拍的「e」才進來，比第一小節晚一格。",ref="Nas、Mos Def、台灣的大支、熱狗早期作品"),
 dict(g="boom",t="跨小節句・連押",dr="boom",sub=4,bpm=90,rap=1,v="....x-x-x-xx-x-x|x-x---x-xx-x----",ly="說的每一個字都/有份量不浪費",
  ex="句子從第 2 拍才開始，一路講到下一小節中間才停，「句子」和「小節」故意不對齊。這讓 Flow 聽起來像在說話，而不是在數拍子。",how="小節線那一刻人聲沒有停，第二小節第 1 拍正好落在句子中間。",ref="Biggie、MC HotDog 敘事型段落"),
 dict(g="trap",t="三連音 Flow",dr="trap",sub=6,bpm=140,rap=1,v="x-x-x-x-x-x-x-x-x-x-x-x-|x-x-x-x-x-x-x-x-x-------",ly="每一天都在拚不回頭往前看/數著錢數著夢數不完",
  ex="每拍三個字（八分三連音），「噠噠噠 噠噠噠」像在滾動。跟直直的 Hi-hat 形成 3 對 2 的拉扯，是 Trap 最具代表性的 Flow。",how="每三個字為一組，組頭剛好落在每一拍上。",ref="Migos〈Versace〉、Travis Scott、許多華語 Trap"),
 dict(g="trap",t="短句＋留白",dr="trap",sub=6,bpm=140,rap=1,v="x-x-x-......x-x-x-......|x-x-x-...x-x-x-x-x------",ly="不停歇往前走/嘿嘿嘿停不下來了",
  ex="三個字一組，然後故意空出半小節給 808 和 Hi-hat。留白讓 Ad-lib（嘿、Yeah）可以塞進去，也讓節奏更有「氣勢」。",how="人聲停下來的地方，正好聽得到 Hi-hat 連打。",ref="21 Savage、Future 這類低調冷靜的 Trap"),
 dict(g="mel",t="半唱半唸",dr="trap4",sub=4,bpm=140,v="x-x-x---x-x-x---|..x-x-x-x-------",ly="夜很深燈很亮/我還沒睡",mel=[2,2,4,2,2,0,-1,0,2,0],
  ex="三個字一組、有旋律起伏，第二小節從反拍進來並拉長尾音。介於唱和唸之間，是現在最流行的饒舌唱法。",how="尾音拉長時底下是 808 的低音在撐。",ref="Post Malone、Juice WRLD、華語的 Melodic Rap"),
 dict(g="mel",t="Auto-tune 長尾音",dr="trap4",sub=4,bpm=140,v="x-x-x-x-x-------|x-x-x-x-x-------",ly="我不想再等/讓風帶我走",mel=[4,4,5,4,2,4,4,5,7,5],
  ex="四個短字＋一個超長尾音，兩句完全同節奏。重點在尾音的旋律，像用唱的在饒舌。",how="長音拉滿兩拍半，下一句準時在小節頭進來。",ref="Travis Scott、Lil Uzi Vert 抒情段"),
 dict(g="chop",t="十六分連發",dr="chop",sub=4,bpm=92,rap=1,v="xxxxxxxxxxxxxxxx|xxxxxxxxxxxx----",ly="我要一口氣說完這一整段話都不換氣啊/不能停下來因為節拍在追",
  ex="整整一小節每格一個字，第二小節最後才喘一口氣。考驗的是「每個字一樣長」，不能越唸越快。",how="每一個字對一下 16 分 Hi-hat。",ref="Eminem〈Rap God〉快段、Twista、Busta Rhymes"),
 dict(g="chop",t="機關槍（四連＋休止）",dr="chop",sub=4,bpm=92,rap=1,v="xxxx.xxxx.xxxx.x|xxxx.xxxx.xx----",ly="一二三四五六七八九十十一十二/再來一次快快快快快",
  ex="四個字一串、停一格、再四個字，像機關槍一陣一陣地掃射。休止的位置每次往後移一格，製造錯位感。",how="每串的第一個字不一定在拍點上，要靠 Hi-hat 對位。",ref="Busta Rhymes、Logic 的快嘴段落"),
 dict(g="drill",t="反拍進場＋三連彈跳",dr="drill",sub=6,bpm=142,rap=1,v="..x-x-x---x-x-x---x-x---|..x-x-x---x-x-x-x-------",ly="在街角低著頭別問/我是誰我從哪來",
  ex="每句都晚一點（從拍點後的三連音位置）才進來，三個字一組彈跳。配上不在正拍的小鼓和滑音 808，就是 Drill 的壓迫感。",how="第 1 拍讓給 808，人聲從後面插進來。",ref="Pop Smoke、UK Drill（Headie One 等）"),
 dict(g="jazz",t="慵懶後拍（Behind the beat）",dr="jazz",sub=4,bpm=86,rap=1,v=".x..x..x..x.x---|.x..x.x...x.x---",ly="咖啡還溫著/書翻到一半",
  ex="每個字都比拍點晚一格（落在 e 或 a），像懶洋洋地講話。這種「晚一點點」就是 Jazz Rap、Lo-fi 那種放鬆的味道。",how="人聲幾乎都不跟踢鼓／小鼓同時出現。",ref="A Tribe Called Quest、Nujabes 合作的饒舌、蛋堡")
]
build(open('template.html').read(),open('audio.js').read(),dict(title="饒舌流派節奏型・聽感練習",acc="#7048e8",groups=G,drums=D,patterns=PT,
 intro="<p>依流派分組：Old School、Boom Bap、Trap、Melodic Rap、快嘴、Drill、Jazz Rap。每個流派列出它最有代表性的人聲節奏和鼓組，先聽、試著跟著唸，再揭曉格子譜。</p>",
 footer="<p>練習建議：先用「只鼓」聽出流派（鼓最能辨認流派），再開「人聲＋鼓」跟著唸。Trap／Drill 的三連音最難，先把速度倍率調到 70%。</p>"),'../../pages/rap.html')
