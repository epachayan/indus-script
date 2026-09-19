import csv, collections, json, numpy as np
exec(open('../scripts/numerals.py').read().split('seen=set(); T=[]')[0])
m=json.load(open('meta.json'))
MERGE={}
pairs=[(f'G{a}',f'G{b}') for a,b in m['sim']]+[('G235','G240'),('G390','G407'),('G705','G706')]
for a,b in pairs:                       # union variant signs (never merge numerals)
    if a in VAL or b in VAL: continue
    ra,rb=MERGE.get(a,a),MERGE.get(b,b); root=min(ra,rb)
    for k,v in list(MERGE.items())+[(a,ra),(b,rb)]:
        if v in (ra,rb): MERGE[k]=root
rows=list(csv.DictReader(open('../data/indus_decipher/data/indus_website_real_corpus.csv')))
def build(drop_damaged, merge):
    seen=set(); T=[]
    for r in rows:
        if drop_damaged and r['damaged']=='True': continue
        t=[s for s in r['sign_sequence'].split() if s in tags][::-1]
        if merge: t=[MERGE.get(s,s) for s in t]
        k=tuple(t)
        if t and k not in seen: seen.add(k); T.append(t)
    return T
LONG={s for s in VAL if VAL[s][0]=='long'}; SHORT={s for s in VAL if VAL[s][0]!='long' and s!='G2'}
J=lambda s: MERGE.get(s,s)
def stats(T):
    fin=np.mean([t[-1]==J('G740') for t in T if J('G740') in t])
    op=[t for t in T if len(t)>1 and t[0] in ('G861','G817','G820')]; g2=np.mean([t[1]=='G2' for t in op])
    multi=np.mean([sum(1 for a,b in zip(t,t[1:]) if a in VAL and a!='G2' and b not in VAL)>=2 for t in T])
    FS={J('G390'),J('G405'),J('G407')}; fish={J(s) for s,r in tags.items() if r['family']=='fish'}
    sf=sum(1 for t in T for a,b in zip(t,t[1:]) if a in SHORT and b in FS); lf=sum(1 for t in T for a,b in zip(t,t[1:]) if a in LONG and b in FS)
    sfi=sum(1 for t in T for a,b in zip(t,t[1:]) if a in SHORT and b in fish); lfi=sum(1 for t in T for a,b in zip(t,t[1:]) if a in LONG and b in fish)
    # near-duplicates: texts equal to another text except one sign
    S=set(map(tuple,T)); keys=collections.Counter()
    for t in S:
        for i in range(len(t)): keys[(t[:i],t[i+1:],len(t))]+=1
    near=np.mean([any(keys[(t[:i],t[i+1:],len(t))]>1 for i in range(len(t))) for t in S if len(t)>=3])
    return dict(n=len(T),jar_final=f'{fin:.0%}',opener_then_G2=f'{g2:.0%}',multi_entry=f'{multi:.1%}',
                forked_short_vs_long=f'{sf}:{lf}',fish_short_vs_long=f'{sfi}:{lfi}',near_duplicate_texts=f'{near:.0%}')
for name,dd,mm in (('as recorded',False,False),('drop damaged',True,False),('merge variants',False,True),('both',True,True)):
    print(f'{name:15s}',stats(build(dd,mm)))
print('variant groups merged:',len(set(MERGE.values())),'signs involved:',len(MERGE))
