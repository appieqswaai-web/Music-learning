import json,re
from pypinyin import pinyin,Style
def zh_vowel(ch):
    f=pinyin(ch,style=Style.FINALS,strict=False)[0][0]
    for v in "aoe":
        if v in f: return v
    if f.endswith('i'): return 'i'
    if f and f[-1] in 'uvü': return 'u'
    if f=='' : return 'e'
    return 'i' if 'i' in f else 'u'
K="あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ"
R="a i u e o ka ki ku ke ko sa shi su se so ta chi tsu te to na ni nu ne no ha hi fu he ho ma mi mu me mo ya yu yo ra ri ru re ro wa wo n ga gi gu ge go za ji zu ze zo da ji zu de do ba bi bu be bo pa pi pu pe po".split()
KR=dict(zip(K,R))
def kana_rm(tok):
    t=''.join(chr(ord(c)-0x60) if 'ァ'<=c<='ヶ' else c for c in tok)
    out='';i=0
    while i<len(t):
        c=t[i];nx=t[i+1] if i+1<len(t) else ''
        if nx in 'ゃゅょ' and nx:
            base=KR[c];y={'ゃ':'a','ゅ':'u','ょ':'o'}[nx]
            out+=(base[:-1] if base in('shi','chi','ji') else base[:-1]+'y')+y;i+=2;continue
        if c=='っ': out+="'";i+=1;continue
        if c=='ー': out+='-';i+=1;continue
        out+=KR[c];i+=1
    return out
def kana_vowel(tok):
    rm=kana_rm(tok); vs=[c for c in rm if c in 'aiueo']
    return vs[-1] if vs else 'u'
def build(tpl,audio,cfg,out):
    P=[]
    for p in cfg['patterns']:
        q=dict(p)
        if q.get('jp'):
            toks=q['ly'].split(); bars=q['ly'].split('/')
            b1=len(bars[0].split()); toks=[x for x in toks if x!='/']
            q['rm']=[kana_rm(t) for t in toks]; q['vw']=[kana_vowel(t) for t in toks]; q['ly']=toks; q['b1']=b1
        else:
            s=q['ly'].replace(' ',''); b1=s.index('/') if '/' in s else len(s); chars=list(s.replace('/',''))
            vw=[];cont=[]
            for c in chars:
                if c=='～': vw.append(vw[-1]); cont.append(True)
                else: vw.append(zh_vowel(c)); cont.append(False)
            q['ly']=chars;q['vw']=vw;q['b1']=b1
            if any(cont): q['cont']=cont
        n=q['v'].replace('|','').count('x'); L=len(q['v'].replace('|',''))
        if n!=len(q['ly']) or L!=q['sub']*8: print('MISMATCH',q['t'],'onsets',n,'lyrics',len(q['ly']),'len',L,'need',q['sub']*8)
        if 'mel' in q and len(q['mel'])<len(q['ly']): print('short mel',q['t'])
        P.append(q)
    for k,d in cfg['drums'].items():
        n=d['sub']*4
        for r in 'kschob':
            for x in d.get(r,[]):
                pos=x[0] if isinstance(x,list) else x
                if pos>=n: print('drum pos out',k,r,pos)
    h=tpl.replace('__TITLE__',cfg['title']).replace('__INTRO__',cfg['intro']).replace('__FOOTER__',cfg['footer']).replace('__ACC__',cfg['acc'])
    h=h.replace('__GROUPS__',json.dumps(cfg['groups'],ensure_ascii=False)).replace('__DRUMS__',json.dumps(cfg['drums'],ensure_ascii=False)).replace('__PATTERNS__',json.dumps(P,ensure_ascii=False)).replace('__AUDIO__',audio)
    open(out,'w').write(h)
