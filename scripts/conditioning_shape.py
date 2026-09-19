# Three probes of the conditioning found in FINDINGS 31:
#  1. DECAY: excess MI at distances 1..5, Indus vs comparison corpora and controls.
#  2. FREQUENCY CLASSES: do frequent and rare signs condition their neighbours alike?
#  3. DIRECTION: is predicting forward easier than backward, and how do known systems sit?
import csv, re, collections, math, random, numpy as np
random.seed(53)
def H(s):
    c=collections.Counter(s); n=sum(c.values())
    return -sum(v/n*math.log2(v/n) for v in c.values())
def mi(p): return H([a for a,_ in p])+H([b for _,b in p])-H(p)
def excess_at(seqs,d,n=1000,draws=12,reps=25):
    S=[s for s in seqs if len(s)>=d+1]
    if len(S)<200: return None
    vals=[]
    for _ in range(draws):
        X=random.sample(S,min(n,len(S)))
        p=[(s[i],s[i+d]) for s in X for i in range(len(s)-d)]
        if len(p)<200: return None
        o=mi(p); hl=H([b for _,b in p]); nl=[]
        for _ in range(reps):
            b=[y for _,y in p]; random.shuffle(b); nl.append(mi(list(zip([x for x,_ in p],b))))
        vals.append((o-np.mean(nl))/hl)
    return float(np.mean(vals))
rows=[r for r in csv.DictReader(open('../outputs/inscriptions_ml.csv')) if r['signs_reading_order']]
IND=[r['signs_reading_order'].split() for r in rows]
MJ=[r['signs_reading_order'].split() for r in rows if r['site']=='Mohenjo-daro']
txt=open('../data/linearb.xyz/LinearBInscriptions.js',encoding='utf8',errors='replace').read()
LBw=[]
for m in re.findall(r'"parsedInscription"\s*:\s*"((?:[^"\\]|\\.)*)"',txt):
    for line in m.split('\\n'):
        for w in re.split(r'[\s,]+',line):
            w=re.sub(r'[\[\]\(\)<>%*?!\u2026\.]','',w).strip('-')
            if '-' in w and re.match(r'^[a-z0-9\-]+$',w): LBw.append(w.split('-'))
txt2=open('../data/cdliatf_unblocked.atf',encoding='utf8',errors='replace').read()
SUMl,SUMw=[],[]
for line in txt2.split('\n'):
    if not line.startswith(tuple('123456789')): continue
    ws=[re.sub(r'[\[\]<>#?!\(\)]','',w) for w in line.split()[1:]]
    ws=[w for w in ws if w and re.match(r'^[a-zA-Z0-9\-\.]+$',w)]
    if len(ws)>=3: SUMl.append(ws)
    for w in ws:
        if '-' in w: SUMw.append(w.split('-'))
    if len(SUMl)>25000: break
big=collections.defaultdict(collections.Counter); start=collections.Counter()
for t in IND:
    start[t[0]]+=1
    for a,b in zip(t,t[1:]): big[a][b]+=1
def gen(L):
    s=[random.choices(list(start),weights=start.values())[0]]
    while len(s)<L and big.get(s[-1]):
        nx=big[s[-1]]; s.append(random.choices(list(nx),weights=nx.values())[0])
    return s
CORP=[('Indus (all sites)',IND),('Linear B words (Greek)',LBw),('Sumerian words (signs)',SUMw),
      ('Sumerian lines (words)',SUMl),('Indus bigram-generated',[gen(len(t)) for t in IND]),
      ('Indus shuffled (null)',[random.sample(t,len(t)) for t in IND])]
print('--- 1. DECAY of conditioning with distance (excess MI over each corpus null) ---')
print(f'{"corpus":30s}' + ''.join(f'  d={d}   ' for d in range(1,6)))
res=[]
for name,S in CORP:
    vals=[excess_at(S,d) for d in range(1,6)]
    print(f'{name:30s}' + ''.join(('   -    ' if v is None else f' {v:5.1%} ') for v in vals))
    res.append(dict(corpus=name,**{f'd{d}':('' if v is None else round(v,4)) for d,v in zip(range(1,6),vals)}))
with open('../outputs/conditioning_decay.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['corpus']+[f'd{d}' for d in range(1,6)]); w.writeheader(); w.writerows(res)

print('\n--- 2. Do frequent and rare signs condition alike? (Mohenjo-daro) ---')
cnt=collections.Counter(s for t in MJ for s in t)
def band(s):
    n=cnt[s]
    return 'frequent (50+)' if n>=50 else ('mid (10-49)' if n>=10 else 'rare (<10)')
pairs=[(t[i],t[i+1]) for t in MJ for i in range(len(t)-1)]
for b in ('frequent (50+)','mid (10-49)','rare (<10)'):
    P=[p for p in pairs if band(p[0])==b]
    if len(P)<200: continue
    o=mi(P); hl=H([y for _,y in P]); nl=[]
    for _ in range(40):
        y=[q for _,q in P]; random.shuffle(y); nl.append(mi(list(zip([x for x,_ in P],y))))
    print(f'  first sign {b:16s} n={len(P):5d}  excess {(o-np.mean(nl))/hl:5.1%}  '
          f'(how much the NEXT sign is pinned down by a {b.split()[0]} sign)')

print('\n--- 3. DIRECTION: forward vs backward predictability ---')
def dirs(name,S):
    S=[s for s in S if len(s)>=3]
    if len(S)<300: return
    X=random.sample(S,min(1500,len(S)))
    fwd=[(s[i],s[i+1]) for s in X for i in range(len(s)-1)]
    Hf=H([b for _,b in fwd])-(mi(fwd))          # H(next | prev)
    Hb=H([a for a,_ in fwd])-(mi(fwd))          # H(prev | next)
    print(f'  {name:28s} H(next|prev)={Hf:5.2f}  H(prev|next)={Hb:5.2f}  '
          f'{"forward easier" if Hf<Hb else "backward easier"} by {abs(Hf-Hb):.2f} bits')
for name,S in (('Indus (all sites)',IND),('Linear B words (Greek)',LBw),
               ('Sumerian words (signs)',SUMw),('Sumerian lines (words)',SUMl)):
    dirs(name,S)
print('  (Indus is stored right-to-left as the script runs; Greek and Sumerian left-to-right)')
