# Follow-ups to FINDINGS 29:
#  1. Are the frequent ending signs a functional class, or the general inventory?
#  2. Is the penultimate->ending link a few stock pairs, or a broad dependency?
#  3. Does the profile replicate at Harappa?
import csv, collections, math, random, numpy as np
random.seed(31)
def H(seq):
    c=collections.Counter(seq); n=sum(c.values())
    return -sum(v/n*math.log2(v/n) for v in c.values())
def mi(pairs):
    return H([a for a,_ in pairs])+H([b for _,b in pairs])-H(pairs)
def cover(seq,frac=0.9):
    c=collections.Counter(seq); n=sum(c.values()); run=0
    for i,(_,v) in enumerate(c.most_common(),1):
        run+=v
        if run>=frac*n: return i
    return len(c)
rows=[r for r in csv.DictReader(open('../outputs/inscriptions_ml.csv')) if r['signs_reading_order']]
SITES={s:[r['signs_reading_order'].split() for r in rows if r['site']==s] for s in ('Mohenjo-daro','Harappa')}
for k in SITES: SITES[k]=[t for t in SITES[k] if len(t)>=3]

print('--- 1. Are the frequent ending signs a distinct class? ---')
T=SITES['Mohenjo-daro']
last=[t[-1] for t in T]; nonlast=[s for t in T for s in t[:-1]]
c_last=collections.Counter(last); c_non=collections.Counter(nonlast)
topend=[s for s,_ in c_last.most_common(cover(last))]
print(f'  {len(topend)} signs cover 90% of endings. How do they behave elsewhere?')
excl=[s for s in topend if c_non[s]==0]
rare=[s for s in topend if c_non[s]>0 and c_last[s]/(c_last[s]+c_non[s])>=0.7]
mixed=[s for s in topend if c_non[s]>0 and c_last[s]/(c_last[s]+c_non[s])<0.7]
print(f'    never occur elsewhere (true terminators): {len(excl)}  {excl[:8]}')
print(f'    occur elsewhere but are 70%+ final:       {len(rare)}  {rare[:8]}')
print(f'    occur freely elsewhere:                   {len(mixed)}  {mixed[:8]}')
share=sum(c_last[s] for s in excl+rare)/len(last)
print(f'    share of all endings taken by the final-preferring signs: {share:.0%}')

print('\n--- 2. Is the penultimate->ending link a few stock pairs? ---')
pairs=[(t[-2],t[-1]) for t in T]
obs=mi(pairs)
cnt=collections.Counter(pairs)
def mi_without(drop):
    keep=[p for p in pairs if p not in drop]
    return mi(keep),len(keep)
for k in (5,10,20):
    drop=set(p for p,_ in cnt.most_common(k))
    m,n=mi_without(drop)
    print(f'  dropping the {k:2d} commonest pairs ({sum(cnt[p] for p in drop)/len(pairs):.0%} of texts): '
          f'MI {obs:.2f} -> {m:.2f} bits on the remaining {n} texts')
null=[]
for _ in range(300):
    b=[y for _,y in pairs]; random.shuffle(b)
    null.append(mi(list(zip([x for x,_ in pairs],b))))
drop=set(p for p,_ in cnt.most_common(20)); m,n=mi_without(drop)
null2=[]
keep=[p for p in pairs if p not in drop]
for _ in range(300):
    b=[y for _,y in keep]; random.shuffle(b)
    null2.append(mi(list(zip([x for x,_ in keep],b))))
print(f'  after dropping the top 20 pairs: MI {m:.2f} vs shuffled {np.mean(null2):.2f} '
      f'(z={(m-np.mean(null2))/np.std(null2):+.1f}) - the dependency is broad, not just stock phrases'
      if (m-np.mean(null2))/np.std(null2)>3 else
      f'  after dropping the top 20 pairs the dependency largely disappears (z={(m-np.mean(null2))/np.std(null2):+.1f})')

print('\n--- 3. Does it replicate at Harappa? ---')
for site,X in SITES.items():
    if len(X)<200: print(f'  {site}: only {len(X)} texts'); continue
    f=[t[0] for t in X]; l=[t[-1] for t in X]
    p2=[(t[-2],t[-1]) for t in X]
    o=mi(p2); nl=[]
    for _ in range(200):
        b=[y for _,y in p2]; random.shuffle(b); nl.append(mi(list(zip([x for x,_ in p2],b))))
    print(f'  {site:14s} n={len(X):5d}  H(first)={H(f):5.2f}  H(last)={H(l):5.2f}  diff={H(l)-H(f):+5.2f}  '
          f'commonest last {collections.Counter(l).most_common(1)[0][1]/len(l):4.0%}  '
          f'90% of endings in {cover(l):3d} signs  penult->end MI z={(o-np.mean(nl))/np.std(nl):+5.1f}')
