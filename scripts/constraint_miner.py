# Mine falsifiable constraints from the Mohenjo-daro texts and validate them on a held-out
# half. Six kinds: positional, forbidden adjacency, obligatory adjacency, precedence,
# co-occurrence exclusion, cardinality. Nulls keep each text's sign multiset and shuffle
# order (for order rules) or keep text lengths and resample signs (for co-occurrence).
import csv, collections, itertools, random, numpy as np
random.seed(11)
rows=[r for r in csv.DictReader(open('../outputs/inscriptions_ml.csv'))
      if r['site']=='Mohenjo-daro' and r['first_occurrence']=='True' and r['signs_reading_order']]
T=[r['signs_reading_order'].split() for r in rows]
T=[t for t in T if len(t)>=2]
random.shuffle(T); half=len(T)//2
TRAIN,TEST=T[:half],T[half:]
print(f'Mohenjo-daro texts: {len(T)} (train {len(TRAIN)}, test {len(TEST)})')
def counts(texts):
    c=collections.Counter(s for t in texts for s in t); return c
cnt=counts(TRAIN); N=sum(cnt.values())
FREQ=[s for s,n in cnt.items() if n>=15]
print(f'signs with 15+ tokens in train: {len(FREQ)}')

def check(texts,pred):           # returns (violations, applicable)
    v=a=0
    for t in texts:
        ok,app=pred(t)
        a+=app; v+=(app and not ok)
    return v,a

print('\n--- 1. POSITIONAL (never initial / never final / only final ...) ---')
pos=[]
for s in FREQ:
    ini=sum(t[0]==s for t in TRAIN); fin=sum(t[-1]==s for t in TRAIN)
    tot=sum(s in t for t in TRAIN)
    mid=sum(s in t[1:-1] for t in TRAIN)
    for lab,hits in (('never initial',ini),('never final',fin),('never medial',mid)):
        if hits==0 and tot>=15: pos.append((s,lab,tot))
for s,lab,tot in sorted(pos,key=lambda x:-x[2])[:12]:
    if lab=='never initial': p=lambda t,s=s:(t[0]!=s, s in t)
    elif lab=='never final': p=lambda t,s=s:(t[-1]!=s, s in t)
    else: p=lambda t,s=s:(s not in t[1:-1], s in t)
    v,a=check(TEST,p)
    print(f'  {s:6s} {lab:14s} train n={tot:4d} | held-out: {v} violations in {a} texts')

print('\n--- 2. FORBIDDEN ADJACENCY (expected >=5, observed 0) ---')
big=collections.Counter((t[i],t[i+1]) for t in TRAIN for i in range(len(t)-1))
Nb=sum(big.values())
forb=[]
for x,y in itertools.permutations(FREQ,2):
    exp=cnt[x]*cnt[y]/N*Nb/N*2   # rough expectation under order shuffling
    if big[(x,y)]==0 and exp>=5: forb.append((x,y,exp))
print(f'  candidate forbidden pairs: {len(forb)}')
for x,y,exp in sorted(forb,key=lambda z:-z[2])[:10]:
    v,a=check(TEST,lambda t,x=x,y=y:(all((t[i],t[i+1])!=(x,y) for i in range(len(t)-1)), x in t and y in t))
    print(f'  {x:6s} never directly before {y:6s} (expected ~{exp:.0f}) | held-out: {v} violations in {a} texts with both')

print('\n--- 3. OBLIGATORY ADJACENCY (X occurs => Y immediately follows) ---')
ob=[]
for x in FREQ:
    occ=[(t,i) for t in TRAIN for i,s in enumerate(t) if s==x]
    if len(occ)<15: continue
    nxt=collections.Counter(t[i+1] if i+1<len(t) else '<END>' for t,i in occ)
    y,n=nxt.most_common(1)[0]
    if n/len(occ)>=0.85: ob.append((x,y,n/len(occ),len(occ)))
for x,y,r,n in sorted(ob,key=lambda z:-z[3])[:10]:
    if y=='<END>': p=lambda t,x=x:(all(i==len(t)-1 for i,s in enumerate(t) if s==x), x in t)
    else: p=lambda t,x=x,y=y:(all(i+1<len(t) and t[i+1]==y for i,s in enumerate(t) if s==x), x in t)
    v,a=check(TEST,p)
    print(f'  {x:6s} -> {y:7s} in {r:.0%} of {n} train occurrences | held-out: {v} violations in {a} texts')

print('\n--- 4. PRECEDENCE (X before Y whenever both occur) ---')
prec=[]
for x,y in itertools.permutations(FREQ,2):
    both=[t for t in TRAIN if x in t and y in t]
    if len(both)<10: continue
    ok=sum(t.index(x)<t.index(y) for t in both)
    if ok==len(both): prec.append((x,y,len(both)))
for x,y,n in sorted(prec,key=lambda z:-z[2])[:10]:
    v,a=check(TEST,lambda t,x=x,y=y:(t.index(x)<t.index(y) if (x in t and y in t) else True, x in t and y in t))
    print(f'  {x:6s} always before {y:6s} ({n} train texts) | held-out: {v} violations in {a} texts')

print('\n--- 5. CO-OCCURRENCE EXCLUSION (never in the same text) ---')
exc=[]
for x,y in itertools.combinations(FREQ,2):
    nx=sum(x in t for t in TRAIN); ny=sum(y in t for t in TRAIN)
    exp=nx*ny/len(TRAIN)
    if exp>=5 and not any(x in t and y in t for t in TRAIN): exc.append((x,y,exp))
for x,y,exp in sorted(exc,key=lambda z:-z[2])[:10]:
    v,a=check(TEST,lambda t,x=x,y=y:(not(x in t and y in t), x in t or y in t))
    print(f'  {x:6s} and {y:6s} never co-occur (expected ~{exp:.0f}) | held-out: {v} violations in {a} texts with either')

print('\n--- 6. CARDINALITY (at most one per text) ---')
card=[s for s in FREQ if max(t.count(s) for t in TRAIN)==1 and sum(s in t for t in TRAIN)>=30]
for s in sorted(card,key=lambda s:-cnt[s])[:8]:
    v,a=check(TEST,lambda t,s=s:(t.count(s)<=1, s in t))
    print(f'  {s:6s} at most once per text ({cnt[s]} train tokens) | held-out: {v} violations in {a} texts')

# ---- write every candidate rule with its held-out score ----
RULES=[]
def add(kind,a,b,support,pred):
    v,n=check(TEST,pred); RULES.append(dict(kind=kind,sign_a=a,sign_b=b,train_support=support,
        heldout_applicable=n,heldout_violations=v))
for s,lab,tot in pos:
    if lab=='never initial': p=lambda t,s=s:(t[0]!=s, s in t)
    elif lab=='never final': p=lambda t,s=s:(t[-1]!=s, s in t)
    else: p=lambda t,s=s:(s not in t[1:-1], s in t)
    add(lab,s,'',tot,p)
for x,y,exp in forb:
    add('never directly before',x,y,round(exp),
        lambda t,x=x,y=y:(all((t[i],t[i+1])!=(x,y) for i in range(len(t)-1)), x in t and y in t))
for x,y,r,n in ob:
    if y=='<END>': p=lambda t,x=x:(all(i==len(t)-1 for i,s in enumerate(t) if s==x), x in t)
    else: p=lambda t,x=x,y=y:(all(i+1<len(t) and t[i+1]==y for i,s in enumerate(t) if s==x), x in t)
    add('always immediately followed by',x,y,n,p)
for x,y,n in prec:
    add('always before',x,y,n,lambda t,x=x,y=y:(t.index(x)<t.index(y) if (x in t and y in t) else True, x in t and y in t))
for x,y,exp in exc:
    add('never co-occurs with',x,y,round(exp),lambda t,x=x,y=y:(not(x in t and y in t), x in t or y in t))
for s in card:
    add('at most once per text',s,'',cnt[s],lambda t,s=s:(t.count(s)<=1, s in t))
with open('../outputs/constraints.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['kind','sign_a','sign_b','train_support','heldout_applicable','heldout_violations'])
    w.writeheader(); w.writerows(sorted(RULES,key=lambda r:(r['kind'],-r['train_support'])))
tot_app=sum(r['heldout_applicable'] for r in RULES); tot_v=sum(r['heldout_violations'] for r in RULES)
clean=sum(1 for r in RULES if r['heldout_violations']==0 and r['heldout_applicable']>=10)
print(f'\n--- SUMMARY ---')
print(f'rules mined: {len(RULES)}; held-out applications {tot_app}, violations {tot_v} ({tot_v/max(tot_app,1):.2%})')
print(f'rules with 10+ held-out applications and zero violations: {clean}')
print('written to outputs/constraints.csv')
