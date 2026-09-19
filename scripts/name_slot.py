# Exp 1-2: locate a "name" slot in Indus texts and test whether it behaves like Mesopotamian names.
import csv, collections, re, numpy as np
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('../scripts/seal_legends.py').read().split('# ---- common structural metrics')[0])
# ---- Mesopotamian slots: whole line strings by role ----
meso=collections.defaultdict(list)
for _,ws in L:
    for l in ws:
        if l: meso[role(l)].append(tuple(s for w in l for s in signs(w)))
# ---- Indus slots from the template ----
OPEN={'G861','G817','G820','G692'}; MARK={'G2','G60','G1','G741'}; END={'G740','G400','G90','G151','G520'}
rows=list(csv.DictReader(open('../outputs/inscriptions_ml.csv')))
T=[r['signs_reading_order'].split() for r in rows if r['first_occurrence']=='True' and r['object_type']=='SEAL' and int(r['n_signs'])>=3]
ind=collections.defaultdict(list)
for t in T:
    i=0
    if t[0] in OPEN:
        j=2 if len(t)>1 and t[1] in MARK else 1; ind['OPENER unit'].append(tuple(t[:j])); i=j
    k=len(t)
    while k>i and t[k-1] in END: k-=1
    if k<len(t): ind['ENDING unit'].append(tuple(t[k:]))
    if k>i: ind['CORE (middle)'].append(tuple(t[i:k]))
def profile(vals):
    c=collections.Counter(vals); n=len(vals)
    once=sum(1 for v in c.values() if v==1)/len(c)
    top=c.most_common(1)[0][1]/n
    pieces=collections.Counter(p for v in c for p in set(v))
    reuse=np.mean([all(pieces[p]>=3 for p in v) for v in c])
    return n,len(c),once,top,np.mean([len(v) for v in vals]),reuse
print(f'{"slot":34s}{"uses":>6s}{"types":>7s}{"unique%":>9s}{"top%":>7s}{"len":>6s}{"built-from-common-pieces":>26s}')
for name,d in (('Mesopotamian',meso),('Indus seals',ind)):
    for k,v in sorted(d.items(),key=lambda x:-len(x[1])):
        if len(v)<100: continue
        n,ty,once,top,ln,reuse=profile(v)
        print(f'{name+" "+k:34s}{n:6d}{ty:7d}{once:9.0%}{top:7.0%}{ln:6.1f}{reuse:26.0%}')
# core frequency spectrum vs names: share of types seen once, twice, 3+
for lab,v in (('Meso NAME',meso['NAME']),('Indus CORE',ind['CORE (middle)'])):
    c=collections.Counter(collections.Counter(v).values()); tot=sum(c.values())
    print(f'{lab:11s} types seen 1x {c[1]/tot:.0%}, 2x {c[2]/tot:.0%}, 3+x {sum(x for k,x in c.items() if k>=3)/tot:.0%}')
# how often the core contains a numeral
NUM={'G1','G3','G4','G5','G7','G16','G17','G18','G19','G31','G32','G33','G35'}
print(f'Indus cores containing a count sign: {np.mean([any(s in NUM for s in v) for v in ind["CORE (middle)"]]):.0%}')
