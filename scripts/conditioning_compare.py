# How strong is the Indus pairwise conditioning compared with real writing systems?
# Measure: mutual information between the penultimate and final element of a sequence,
# normalised by the entropy of the final element (the share of the ending's uncertainty
# that its neighbour removes), with a shuffled null for each corpus.
import csv, re, collections, math, random, numpy as np
random.seed(41)
def H(s):
    c=collections.Counter(s); n=sum(c.values())
    return -sum(v/n*math.log2(v/n) for v in c.values())
def mi(p): return H([a for a,_ in p])+H([b for _,b in p])-H(p)
def profile(name,seqs,reps=200):
    seqs=[s for s in seqs if len(s)>=3]
    if len(seqs)<200: print(f'{name:30s} only {len(seqs)} sequences'); return None
    p=[(s[-2],s[-1]) for s in seqs]
    o=mi(p); hl=H([b for _,b in p]); nl=[]
    for _ in range(reps):
        b=[y for _,y in p]; random.shuffle(b); nl.append(mi(list(zip([x for x,_ in p],b))))
    z=(o-np.mean(nl))/np.std(nl)
    print(f'{name:30s} n={len(seqs):6d}  MI={o:5.2f}  H(end)={hl:5.2f}  MI/H={o/hl:5.1%}  '
          f'shuffled {np.mean(nl):5.2f} ({np.mean(nl)/hl:4.0%})  z={z:+6.1f}')
    return dict(corpus=name,n=len(seqs),mi=round(o,3),h_end=round(hl,3),
                mi_over_h=round(o/hl,4),shuffled=round(float(np.mean(nl)),3),z=round(float(z),1))
out=[]
rows=[r for r in csv.DictReader(open('../outputs/inscriptions_ml.csv')) if r['signs_reading_order']]
for site in ('Mohenjo-daro','Harappa'):
    out.append(profile(f'Indus {site} (signs)',[r['signs_reading_order'].split() for r in rows if r['site']==site]))
# Linear B: Mycenaean Greek, phrase level (words) and word level (syllabograms)
txt=open('../data/linearb.xyz/LinearBInscriptions.js',encoding='utf8',errors='replace').read()
phr,wd=[],[]
for m in re.findall(r'"parsedInscription"\s*:\s*"((?:[^"\\]|\\.)*)"',txt):
    for line in m.split('\\n'):
        ws=[re.sub(r'[\[\]\(\)<>%*?!\u2026\.]','',w).strip('-') for w in re.split(r'[\s,]+',line)]
        ws=[w for w in ws if w and re.match(r'^[a-z0-9\-]+$',w)]
        if len(ws)>=3: phr.append(ws)
        for w in ws:
            if '-' in w: wd.append(w.split('-'))
out.append(profile('Linear B phrases (Greek)',phr)); out.append(profile('Linear B words (Greek)',wd))
# Sumerian administrative lines (words) and words (signs)
txt=open('../data/cdliatf_unblocked.atf',encoding='utf8',errors='replace').read()
lines,words=[],[]
for line in txt.split('\n'):
    if not line.startswith(tuple('123456789')): continue
    ws=[re.sub(r'[\[\]<>#?!\(\)]','',w) for w in line.split()[1:]]
    ws=[w for w in ws if w and re.match(r'^[a-zA-Z0-9\-\.]+$',w)]
    if len(ws)>=3: lines.append(ws)
    for w in ws:
        if '-' in w: words.append(w.split('-'))
    if len(lines)>30000: break
out.append(profile('Sumerian lines (words)',lines)); out.append(profile('Sumerian words (signs)',words))
# controls
ind=[r['signs_reading_order'].split() for r in rows]
out.append(profile('Indus, signs shuffled in text',[random.sample(t,len(t)) for t in ind if len(t)>=3]))
# bigram-generated control: same bigram statistics, no higher structure
big=collections.defaultdict(collections.Counter)
start=collections.Counter()
for t in ind:
    start[t[0]]+=1
    for a,b in zip(t,t[1:]): big[a][b]+=1
def gen(L):
    s=[random.choices(list(start),weights=start.values())[0]]
    while len(s)<L:
        nxt=big.get(s[-1])
        if not nxt: break
        s.append(random.choices(list(nxt),weights=nxt.values())[0])
    return s
out.append(profile('Indus bigram-generated',[gen(len(t)) for t in ind if len(t)>=3]))
with open('../outputs/conditioning_profile.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['corpus','n','mi','h_end','mi_over_h','excess_bits','shuffled','z']); w.writeheader()
    w.writerows([r for r in out if r])

# Matched-size comparison. MI is upward-biased in small samples, so (a) subsample every
# corpus to the same number of sequences and (b) report the EXCESS over that corpus's own
# shuffled null, as a share of the ending's entropy.
print('\nMatched at n=1000 sequences, 20 draws each; excess = (MI - shuffled) / H(end)')
def excess(name,seqs,n=1000,draws=20):
    seqs=[s for s in seqs if len(s)>=3]
    if len(seqs)<n: return None
    vals=[]; bits=[]
    for _ in range(draws):
        S=random.sample(seqs,n); p=[(s[-2],s[-1]) for s in S]
        o=mi(p); hl=H([b for _,b in p])
        nl=[]
        for _ in range(30):
            b=[y for _,y in p]; random.shuffle(b); nl.append(mi(list(zip([x for x,_ in p],b))))
        vals.append((o-np.mean(nl))/hl); bits.append(o-np.mean(nl))
    print(f'  {name:30s} excess {np.mean(vals):5.1%}  (sd {np.std(vals):.1%})  '
          f'raw {np.mean(bits):5.2f} bits  (sd {np.std(bits):.2f})')
    return dict(corpus=name+' [n=1000]',n=n,mi='',h_end='',mi_over_h=round(float(np.mean(vals)),4),
                excess_bits=round(float(np.mean(bits)),3),shuffled='',z='')
ex=[]
ex.append(excess('Indus Mohenjo-daro (signs)',[r['signs_reading_order'].split() for r in rows if r['site']=='Mohenjo-daro']))
ex.append(excess('Linear B phrases (Greek)',phr))
ex.append(excess('Linear B words (Greek)',wd))
ex.append(excess('Sumerian lines (words)',lines))
ex.append(excess('Sumerian words (signs)',words))
ex.append(excess('Indus shuffled (null)',[random.sample(t,len(t)) for t in ind if len(t)>=3]))
ex.append(excess('Indus bigram-generated',[gen(len(t)) for t in ind if len(t)>=3]))
with open('../outputs/conditioning_profile.csv','a',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['corpus','n','mi','h_end','mi_over_h','excess_bits','shuffled','z'])
    w.writerows([r for r in ex if r])
