# Is the missing periodicity in the Indus decay curve a real difference, or just an
# artefact of short texts? Truncate the comparison corpora to the Indus length
# distribution and re-measure the decay.
import csv, re, collections, math, random, numpy as np
random.seed(67)
def H(s):
    c=collections.Counter(s); n=sum(c.values())
    return -sum(v/n*math.log2(v/n) for v in c.values())
def mi(p): return H([a for a,_ in p])+H([b for _,b in p])-H(p)
def excess_at(seqs,d,draws=12,reps=25,n=1200):
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
LENS=[len(t) for t in IND]
print(f'Indus length distribution: median {int(np.median(LENS))}, mean {np.mean(LENS):.1f}, '
      f'90th pct {int(np.percentile(LENS,90))}, max {max(LENS)}')
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
def truncate(seqs):
    # cut each sequence to a length drawn from the Indus distribution, keeping the start
    out=[]
    for s in seqs:
        L=random.choice(LENS)
        if len(s)>=3: out.append(s[:max(3,min(L,len(s)))])
    return out
print('\nexcess MI by distance; "truncated" = same corpus cut to Indus-like lengths')
print(f'{"corpus":34s}' + ''.join(f'  d={d}  ' for d in range(1,6)))
res=[]
for name,S in (('Indus (all sites)',IND),
               ('Linear B words (Greek)',LBw),('Linear B words, truncated',truncate(LBw)),
               ('Sumerian words (signs)',SUMw),('Sumerian words, truncated',truncate(SUMw)),
               ('Sumerian lines (words)',SUMl),('Sumerian lines, truncated',truncate(SUMl))):
    v=[excess_at(S,d) for d in range(1,6)]
    print(f'{name:34s}' + ''.join(('   -   ' if x is None else f' {x:5.1%}') for x in v))
    res.append(dict(corpus=name,**{f'd{d}':('' if x is None else round(x,4)) for d,x in zip(range(1,6),v)}))
with open('../outputs/length_control.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['corpus']+[f'd{d}' for d in range(1,6)]); w.writeheader(); w.writerows(res)
print('\nIf the d=4/d=5 rise survives truncation, the Indus difference is real;')
print('if truncation flattens the comparison corpora too, our reading was a length artefact.')
