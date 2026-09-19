import csv, collections, numpy as np, re
exec(open('../scripts/numerals.py').read().split('cnt=collections.Counter')[0])
exec(open('../scripts/objtype.py').read().split("exec(open('../scripts/motif_dedup.py')")[0])
def kind(r):
    o,_=bycisi.get(r['cisi_number'],([],'?')); return 'TAB' if 'TAB' in o else 'SEAL' if 'SEAL' in o else 'TAG' if 'TAG' in o else '?'
rows=list(csv.DictReader(open('../data/indus_decipher/data/indus_website_real_corpus.csv')))
LONG={s for s in VAL if VAL[s][0]!='short'}   # counting-like series (G2 excluded as marker)
# --- stock-book predictions ---
dup=collections.Counter(r['sign_sequence'] for r in rows)
print('texts with an exact duplicate elsewhere: %.0f%%'%(100*np.mean([dup[r['sign_sequence']]>1 for r in rows])))
by=collections.defaultdict(list)
for r in rows:
    t=[s for s in r['sign_sequence'].split() if s in tags][::-1]
    by[kind(r)].append(t)
for k,ts in by.items():
    if len(ts)<30: continue
    num=[any(s in LONG for s in t) for t in ts]
    npair=[sum(1 for a,b in zip(t,t[1:]) if a in LONG and b not in VAL) for t in ts]
    print(f'{k:5s} n={len(ts):4d} mean len {np.mean([len(t) for t in ts]):.1f} | has count-numeral {np.mean(num):.0%} | texts with 2+ number-item entries {np.mean([p>=2 for p in npair]):.1%}')
vals=[VAL[s][1] for t in T for s in t if s in LONG]
print('largest count value seen:',max(vals),'| share of counts <=3: %.0f%%'%(100*np.mean(np.array(vals)<=3)))
# --- track 1: short vs long contexts ---
def follow(series):
    c=collections.Counter()
    for t in T:
        for i,s in enumerate(t[:-1]):
            if s in VAL and VAL[s][0]==series and s!='G2': c[t[i+1]]+=1
    return c
def jsd(a,b):
    keys=set(a)|set(b); p=np.array([a[k] for k in keys],float); q=np.array([b[k] for k in keys],float)
    p/=p.sum(); q/=q.sum(); m=(p+q)/2
    f=lambda x,y: np.sum(x[x>0]*np.log2(x[x>0]/y[x>0])); return (f(p,m)+f(q,m))/2
fs,fl=follow('short'),follow('long'); obs=jsd(fs,fl)
# null: split long-series occurrences randomly in two
occ=[t[i+1] for t in T for i,s in enumerate(t[:-1]) if s in VAL and VAL[s][0] in('short','long') and s!='G2']
rng=np.random.default_rng(0); ns=sum(fs.values()); null=[]
for _ in range(300):
    p=rng.permutation(occ); null.append(jsd(collections.Counter(p[:ns]),collections.Counter(p[ns:])))
print(f'\n[T1] short(no G2) vs long follower divergence {obs:.3f}; shuffled {np.mean(null):.3f}; p={(1+sum(n>=obs for n in null))/301:.3f}')
print('   short followed by:',fs.most_common(5)); print('   long  followed by:',fl.most_common(5))
# --- track 2: forked-stem unit by object type and motif ---
FS={'G390','G405','G407'}
for k,ts in by.items():
    if len(ts)<30: continue
    print(f'[T2] {k:5s} number+forked-stem in {np.mean([any(a in VAL and b in FS for a,b in zip(t,t[1:])) for t in ts]):.1%} of texts')
mot=collections.Counter(); tot=collections.Counter()
for r in rows:
    t=r['sign_sequence'].split()[::-1]; m='unicorn' if r['motif'].startswith('Bull1') else r['motif']
    tot[m]+=1; mot[m]+=any(a in VAL and b in FS for a,b in zip(t,t[1:]))
print('   by motif:',{m:f'{mot[m]}/{tot[m]}' for m,_ in tot.most_common(8)})
# --- track 3: numbered fish ---
fish=[s for s,r in tags.items() if r['family']=='fish']
nf=collections.defaultdict(collections.Counter)
for t in T:
    for a,b in zip(t,t[1:]):
        if a in VAL and b in fish: nf[b][VAL[a][1]]+=1
print('\n[T3] numbers before fish variants:')
for s,c in sorted(nf.items(),key=lambda x:-sum(x[1].values())): print('   ',s,dict(sorted(c.items())))
