# 《浪子回頭》（茄子蛋）人聲節奏練習頁產生器：py langzi.py → ../../pages/langzi.html
# 節奏照樂譜逐小節記下；網站公開，所以每句只顯示開頭兩個字當提示，其他字用 ● 代替，旋律也是通用音高，不是原曲旋律。
# 記法：字+長度（s=十六分 e=八分 d=附點八分 q=四分 h=二分 t=八分三連音），0=休止，-=延長（連音線），| 分小節
import sys,json;sys.path.insert(0,'.')
from common import zh_vowel
U=dict(s=3,e=6,d=9,q=12,h=24,t=4)   # 以 1/12 拍為單位
def toks(src):
    out=[]
    for tk in src.split():
        c,d=tk[0],sum(U[x] for x in tk[1:]);out.append((c,d))
    return out
def blen(src): return sum(d for _,d in toks(src))
B=dict(
 b1="一s 支s 一s 支s 一e 支s 的s 點s -d 0e 酒e",
 b2="一s 杯s 一s 杯s 一s 杯s 的s 乾s -q 0e 請s 你s",
 b3="要q 體s 諒e 我s -q 0d 我s",
 b4="酒s 量s 不s 好s 賣s 給s 我s 衝s -s 康d 0e 時s 間s",
 b5="一s 天s 一s 天s 一s 天s 的s 走s -q 0e 汗e",
 b6="一s 滴s 一s 滴s 一s 滴s 的s 流s -q 0e 有s 一s",
 b7="天q 咱s 都e 老s -q 0d 帶s",
 b8="某s 子e 逗s -s 陣d",
 b9="0q 0q 0e 浪e 子s -s 回e 頭q",
 b8v2="某s 子e 逗s -s 陣d 0q 浪t 子t 回t",
 b9v2="頭h 0q 0q",
 e1="某s 子e 逗s -e 陣e 0q 0e 帶e",
 e3="某s 子e 逗s -e 陣e 0q 0q",
 c1="親e 愛s 的s -q 可e 愛s 的s -q",
 c2="英e 俊s 的s -d 朋s 友q -q",
 c3="垃e 圾s 的s -q 沒e 品s 的s -q",
 c4="沒s 路s 用s 的s -d 朋s 友q 0d 仔s",
 c5="坎s 坷s 的s 路s 騎s 我s 兩s 光s 摩s 托e 車s -e 橫s 直s",
 c5t="坎s 坷s 的s 路s 騎s 我s 兩s 光s 摩t 托t 車t -e 橫s 直s",
 c6="我s 的s 人s 生s 甘s 哪s 狗s 屎s -q 0d 我s",
 c7="沒s 錢s 沒s 某s 沒s 子s 甘s 哪s 一s 條e 命s -e 朋s 友s",
 c7t="沒s 錢s 沒s 某s 沒s 子s 甘s 哪s 一t 條t 命t -e 朋s 友s",
 c8="阿q -q -q 逗t 陣t 來t",
 c9="搏q -q -q 0e 菸e",
)
B['e2']=B['e1']
# 句子：pick＝從上一小節尾巴進來的字；tail＝最後一小節尾巴屬於下一句的字數
L=dict(
 L1=dict(n="菸 一支一支…酒 一杯一杯…",pick="菸e",bars="b1 b2",tail=2),
 L2=dict(n="請你 要體諒我",pick="請s 你s",bars="b3",tail=1),
 L3=dict(n="我 酒量不好…",pick="我s",bars="b4",tail=2),
 L4=dict(n="時間 一天一天…",pick="時s 間s",bars="b5",tail=1),
 L5=dict(n="汗 一滴一滴…",pick="汗e",bars="b6",tail=2),
 L6=dict(n="有一天…",pick="有s 一s",bars="b7",tail=1),
 L7=dict(n="帶某子逗陣（2/4 拍）",pick="帶s",bars="b8",tail=0),
 L8=dict(n="浪子回頭（5/4 拍）",pick="",bars="b9",tail=0),
 L7b=dict(n="帶某子逗陣・浪子回頭（第二段結尾）",pick="帶s",bars="b8v2 b9v2",tail=0),
 C1=dict(n="親愛的 可愛的…",pick="",bars="c1 c2",tail=0),
 C2=dict(n="垃圾的 沒品的…",pick="",bars="c3 c4",tail=1),
 C3=dict(n="仔 坎坷的路…",pick="仔s",bars="c5 c6",tail=1),
 C4=dict(n="我 沒錢沒某…",pick="我s",bars="c7 c8 c9",tail=1),
 C3t=dict(n="仔 坎坷的路…（三連音版）",pick="仔s",bars="c5t c6",tail=1),
 C4t=dict(n="我 沒錢沒某…（三連音版）",pick="我s",bars="c7t c8 c9",tail=1),
 E1=dict(n="帶某子逗陣 ×3（結尾）",pick="帶s",bars="e1 e2 e3",tail=0),
)
def build_card(lines,names,cue=True):
    """把幾句接起來成一張卡。回傳 12 分格資料，之後再壓縮成 4 分格（沒有三連音時）。"""
    first=L[lines[0]] if lines[0] in L else None
    pick=toks(first['pick']) if first else []
    pk=sum(d for _,d in pick)
    ev=[]  # (start, dur, char, line index, kind)  kind: n=字 r=休止
    t=0
    for c,d in pick: ev.append([t,d,c,0,'n']);t+=d
    bars=[];bounds=[]
    for li,ln in enumerate(lines):
        x=L[ln];bl=x['bars'].split()
        for k,b in enumerate(bl):
            tk=toks(B[b]);bars.append((t,blen(B[b])))
            last=(k==len(bl)-1)
            nn=sum(1 for c,_ in tk if c not in '0-')
            for c,d in tk:
                if c=='-':
                    if ev and ev[-1][4]=='n':ev[-1][1]+=d
                    else: ev.append([t,d,'0',li,'r'])
                elif c=='0': ev.append([t,d,'0',li,'r'])
                else: ev.append([t,d,c,li,'n'])
                t+=d
            if last and x['tail']:
                # 尾巴的字屬於下一句；最後一句的尾巴拿掉
                idx=[i for i,e in enumerate(ev) if e[4]=='n'][-x['tail']:]
                if li==len(lines)-1:
                    for i in idx: ev[i][4]='r';ev[i][2]='0'
                else:
                    nxt=L[lines[li+1]];want=[c for c,_ in toks(nxt['pick'])]
                    got=[ev[i][2] for i in idx]
                    assert got==want,(ln,got,want)
                    for i in idx: ev[i][3]=li+1
        bounds.append(t)
    total=t
    # 判斷能不能用十六分格
    pts=[e[0] for e in ev]+[e[0]+e[1] for e in ev]+[b[0] for b in bars]
    sub=4 if all(p%3==0 for p in pts) else 12
    f=12//sub
    s=['.']*(total//f);ly=[];vw=[];lix=[];first_on={}
    hidden=[]
    for st,d,c,li,k in ev:
        if k!='n':continue
        a=st//f;s[a]='x'
        for j in range(a+1,(st+d)//f):s[j]='-'
        cnt=first_on.get(li,0)
        show=(not cue) or cnt<2 or c in '噠啦'
        first_on[li]=cnt+1
        ly.append(c if show else '●');vw.append(zh_vowel(c) if c not in '噠啦' else 'a');lix.append(li)
    bars=[(a//f,n//f) for a,n in bars]
    bounds=[b//f for b in bounds]
    pkst=pk//f
    # 接龍每一步結束時，第一句的「起拍字」能不能直接疊在最後一小節尾巴（不行就多一小節換氣）
    onsets=[(st//f,(st+d)//f,li) for st,d,c,li,k in ev if k=='n']
    breath=[]
    for k,E in enumerate(bounds):
        own_end=max([b for a,b,li in onsets if li<=k and a>=pkst] or [0])
        breath.append(1 if pkst and own_end>E-pkst else 0)
    # 鼓：每小節依拍數放踢鼓／小鼓／八分 Hi-hat
    K=['.']*len(s);S=['.']*len(s);H=['.']*len(s)
    for a,n in bars:
        nb=n//sub
        kb={2:[0],3:[0],4:[0,2],5:[0,2,4]}.get(nb,[0]);sb={2:[1],3:[1,2],4:[1,3],5:[1,3]}.get(nb,[1])
        for b in kb:K[a+b*sub]='x'
        if nb==4:K[a+2*sub-(sub//2)]='x'  # 第 2 拍反拍補一下踢鼓（Slow Soul 的味道）
        for b in sb:S[a+b*sub]='x'
        for j in range(0,n,sub//2):H[a+j]='x'
    return dict(s=''.join(s),ly=ly,vw=vw,li=lix,sub=sub,pk=pkst,bars=bars,bounds=bounds,breath=breath,
                K=''.join(K),S=''.join(S),H=''.join(H),names=names)
def count_text(c):
    sub=c['sub'];out=[]
    lab4=['','e','&','a'];lab12={0:'',3:'e',4:'三',6:'&',8:'連',9:'a'}
    def lab(i,b):
        r=i%sub;bt=b+1
        if sub==4:return str(bt)+(lab4[r] if r else '') if r==0 else lab4[r]
        return str(bt) if r==0 else lab12.get(r,'')
    s=c['s'];segs=[]
    if c['pk']:segs.append((0,c['pk'],True))
    for a,n in c['bars']:segs.append((a,n,False))
    txt=[]
    for a,n,ispk in segs:
        part=[]
        for i in range(a,a+n):
            r=(i-a) if not ispk else (i-a+ (sub*4-c['pk']))
            b=r//sub;x=s[i];L_=lab(r,b)
            if sub==12 and x!='x' and L_=='' :continue
            if sub==12 and r%sub not in (0,3,4,6,8,9) and x!='x':continue
            part.append(f'<b>{L_ or "○"}</b>' if x=='x' else ('~' if x=='-' else '·'))
        txt.append(('（起拍）' if ispk else '')+' '.join(part))
    return ' | '.join(txt)
def mk(t,g,lines,ex='',how='',bpm=62,chain=False,cue=True,ref=''):
    names=[L[x]['n'] if x in L else x for x in lines]
    c=build_card(lines,names,cue);c.update(t=t,g=g,ex=ex,how=how,bpm=bpm,chain=chain,ref=ref);c['count']=count_text(c);return c
# 節奏型示範卡用的「純節奏」小節
B.update(
 p1="噠s 啦s 噠s 啦s 噠s 啦s 噠s 啦s 噠s 啦s 噠s 啦s 噠s 啦s 噠s 啦s",
 p2="噠e 啦s 啦s 噠e 啦s 啦s 噠e 啦s 啦s 噠e 啦s 啦s",
 p3="噠s 啦e 啦s 噠s 啦e 啦s 噠s 啦e 啦s 噠s 啦e 啦s",
 p4="噠s 啦d 噠s 啦d 噠s 啦d 噠s 啦d",
 p5="噠s 啦s 噠s 啦s -q 噠s 啦s 噠s 啦s -q",
 p6="0e 噠e 0e 噠e 0e 噠s 啦s 0e 噠s 啦s",
 p7="噠q 0d 啦s 噠q 0d 啦s",
 p8="噠t 啦t 啦t 噠t 啦t 啦t 噠t 啦t 啦t 噠t 啦t 啦t",
 p9="噠d 啦s 噠d 啦s 噠h",
 b5n="一s 天s 一s 天s 一s 天s 的s 走s -q 0q",
 b7n="天q 咱s 都e 老s -q 0q",
 b4n="酒s 量s 不s 好s 賣s 給s 我s 衝s -s 康d 0e 時s 間s",
 c6n="我s 的s 人s 生s 甘s 哪s 狗s 屎s -q 0q",
 b3n="要q 體s 諒e 我s -q 0d 我s",
)
for k in 'p1 p2 p3 p4 p5 p6 p7 p8 p9'.split():L[k]=dict(n='純節奏',pick='',bars=k,tail=0)
L['C3c']=dict(n='坎坷的路…（第一次）',pick='仔s',bars='c5 c6n',tail=0)
L['C3tc']=dict(n='坎坷的路…（第二次，三連音）',pick='',bars='c5t c6n',tail=0)
L['T1s']=dict(n='一天一天一天的走',pick='',bars='b5n',tail=0)
L['T2s']=dict(n='親愛的 可愛的',pick='',bars='c1',tail=0)
L['T3s']=dict(n='天 咱都老',pick='',bars='b7n',tail=0)
L['T4s']=dict(n='一支一支一支的點',pick='',bars='b1',tail=0)
L['T5s']=dict(n='一杯一杯一杯的乾',pick='',bars='b2',tail=0)
L['T6s']=dict(n='酒量不好…時間',pick='',bars='b4n',tail=0)
L['T7s']=dict(n='要體諒我 我',pick='',bars='b3n',tail=0)
L['T8s']=dict(n='阿～ 逗陣來',pick='',bars='c8',tail=0)
L['T9s']=dict(n='英俊的 朋友',pick='',bars='c2',tail=0)
G={
 "line":{"name":"一句一句練","desc":"照樂譜一句一句切開。從上一小節尾巴進來的字（起拍）會在「先數 1 小節」的最後唱出來；循環時也會接回這句的起拍。每句只顯示開頭兩個字當提示，其他字用 ● 代替。"},
 "sec":{"name":"整段練（含 🔗 接龍練習）","desc":"把句子接成主歌、副歌、結尾。按「🔗 接龍」會先練第 1 句 2 次，再練第 1～2 句 2 次，一句一句往上加，直到整段。"},
 "type":{"name":"這首歌用到的節奏型","desc":"每張卡第 1 小節是純節奏（噠啦），第 2 小節是歌裡實際出現的地方。先聽純節奏，再聽歌裡的版本。"},
}
V1=['L1','L2','L3','L4','L5','L6','L7','L8']
PT=[]
for k in V1+['L7b']: PT.append(mk(L[k]['n'],'line',[k],how='先只聽，再按「🥁 打拍子」跟著每個字點。'))
for k in ['C1','C2','C3','C4','C3t','C4t','E1']: PT.append(mk(L[k]['n'],'line',[k],how='先只聽，再按「🥁 打拍子」跟著每個字點。'))
PT.append(mk('主歌（第一段）','sec',V1,chain=True,ex='四個十六分音符的「一支一支」貫穿整段，句尾常用連音線拖過拍子，最後用 2/4、5/4 拍收在「浪子回頭」。'))
PT.append(mk('副歌（第一次）','sec',['C1','C2','C3','C4'],chain=True,ex='前半「親愛的、可愛的」是「噠－啦啦」＋長音，留很多空間；後半「坎坷的路」突然變成一連串十六分音符，最後用三連音「逗陣來」收。'))
PT.append(mk('主歌（第二段，結尾不同）','sec',['L1','L2','L3','L4','L5','L6','L7b'],chain=True,ex='前面和第一段一樣，最後「逗陣」接一拍休止，「浪子回」改成三連音，留在 4/4 拍裡。'))
PT.append(mk('副歌（第二次，從「坎坷的路」）','sec',['C3t','C4t'],chain=True,ex='和第一次副歌後半一樣，只是「摩托車」「一條命」改成三連音，唱起來比較圓、比較拖。'))
PT.append(mk('主歌第三段＋結尾','sec',['L1','L2','L3','L4','L5','L6','E1'],chain=True,ex='最後「帶某子逗陣」重複三次，每次中間空一拍再從反拍唱「帶」。'))
T=[
 ('四個十六分「噠啦噠啦」','p1','T1s','主歌的骨幹：一支一支、一杯一杯、酒量不好、一天一天、一滴一滴，副歌後半「坎坷的路」也是。','每個字平均分在一拍的 4 格裡，唸「1 e & a」。'),
 ('八分＋兩個十六分「噠－啦啦」','p2','T2s','副歌開頭「親愛的、可愛的、英俊的、垃圾的」，主歌「一支的」。','第一個字佔半拍，後面兩個字擠在後半拍。'),
 ('十六分＋八分＋十六分「啦噠－啦」','p3','T3s','「咱都老、體諒我、某子逗、摩托車、一條命」。中間的字落在「&」上，有一點切分的感覺。','第二個字比拍子早一格進來，拉到半拍後。'),
 ('前短後長（十六分＋附點八分）','p4','T4s','「點、康、陣」這種一個字很快帶過、下一個音拉長的寫法，台語咬字很常見。','短的那格很快，長的那個要撐滿四分之三拍。'),
 ('連音拖過拍子（句尾延長）','p5','T5s','「乾～、走～、流～、老～、車～」：四個十六分唱完，最後一個字直接拖過下一拍。','拖長的那拍不要提早唱下一個字，心裡繼續數。'),
 ('從後半拍進來（反拍起句）','p6','T6s','「菸、酒、汗」從後半拍唱一個字；「請你、時間、有一、橫直」是後半拍唱兩個十六分。','拍點上先空著，在「&」才開口。'),
 ('搶在最後一格進來（0.5）','p7','T7s','「我、帶、仔」：休止四分之三拍，在最後一格才唱，直接衝進下一小節。','最後一格（a）唱出來，跟下一小節的第 1 拍連在一起。'),
 ('八分三連音','p8','T8s','「逗陣來」，第二次副歌的「摩托車、一條命」，第二段結尾的「浪子回」。一拍平均分成 3 個字。','唸「1 三 連」，三個字一樣長，不要唱成「噠－啦啦」。'),
 ('附點八分＋十六分（朋～友）','p9','T9s','副歌「英俊的 朋友」「沒路用的 朋友」：前一個字拖長，「朋」在最後一格才進來，「友」落在拍點上拉長。','「朋」要晚一點進來，跟「友」黏在一起。'),
]
for t,p,sg,ex,how in T:
    PT.append(mk(t,'type',[p,sg],ex=ex,how=how))
PT.append(mk('換拍子：2/4＋5/4（帶某子逗陣・浪子回頭）','type',['L7','L8'],ex='第一段主歌最後先縮成一小節 2 拍，再拉長成一小節 5 拍，最後才回到 4/4。歌聽起來像是停頓一下、慢慢收尾。',how='小節線（藍色粗線）間距不一樣，跟著格子數拍：2 拍、5 拍。'))
PT.append(mk('對照：摩托車 十六分 vs 三連音','type',['C3c','C3tc'],ex='第一次副歌「摩托車」是「啦噠－啦」，第二次是三連音。前 2 小節是第一次，後 2 小節是第二次。',how='聽「摩托車」三個字：第一次中間的字比較長，第二次三個字一樣長。'))
tpl=open('template_song.html',encoding='utf-8').read()
h=tpl.replace('__GROUPS__',json.dumps(G,ensure_ascii=False)).replace('__PATTERNS__',json.dumps(PT,ensure_ascii=False)).replace('__AUDIO__',open('audio.js',encoding='utf-8').read())
open('../../pages/langzi.html','w',encoding='utf-8').write(h)
print(len(PT),'cards')
for c in PT: print(c['t'],c['sub'],len(c['s']),'pk',c['pk'],'bounds',c['bounds'],'breath',c['breath'])
