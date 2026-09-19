# Writing-system typology: same structural metrics across Indus and 9 known/undeciphered corpora.
import re, json, csv, collections, math, numpy as np
rng=np.random.default_rng(0)
AEG_NUM=lambda ch: 0x10107<=ord(ch)<=0x10133 or 0x10140<=ord(ch)<=0x1018F
AEG_SKIP=set('\n \t[]')|{'\U00010101','\U00010100','\U00010102'}
def load_map(path):
    s=open(path,encoding='utf8').read()
    i=s.index('new Map(')+8
    try: j=s.index(']);',i)+1
    except ValueError: j=s.index('\n);',i)
    body=re.sub(r',(\s*[\]}])',r'\1',s[i:j]); body=re.sub(r'\\u(?![0-9a-fA-F]{4})',r'\\\\u',body)
    return json.loads(body,strict=False)
def aegean(path,field,kind):
    d=load_map(path); out=collections.defaultdict(list)
    for name,v in d:
        t=[('#' if AEG_NUM(ch) else ch) for ch in v.get(field,'') if ch not in AEG_SKIP and ord(ch)>0x10000]
        t=[x for i_,x in enumerate(t) if not (x=='#' and i_ and t[i_-1]=='#')]      # a run of numeral signs = one number
        if len(t)>=2: out[kind(v)].append(t)
    return out
LA=aegean('../data/lineara.xyz/LinearAInscriptions.js','parsedInscription',
          lambda v:'sealing' if v.get('support','') in('Nodule','Roundel') else 'other')
LB=aegean('../data/linearb.xyz/LinearBInscriptions.js','transcription',lambda v:'all')
txt=open('../data/cdliatf_unblocked.atf',encoding='utf8',errors='replace').read()
blocks=re.split(r'\n(?=&P\d+)',txt)
def atf_tokens(b,signsplit):
    t=[]
    for l in b.split('\n'):
        m=re.match(r"^\d+'?\.\s*(.*)",l)
        if not m: continue
        for w in re.sub(r'[\[\]#?!,]',' ',m.group(1)).split():
            if w in('...','x','X'): continue
            if re.match(r'^\d+(/\d+)?\(',w):
                if not t or t[-1]!='#': t.append('#')
            else: t.extend(signsplit(w))
    return t
cun_split=lambda w:[s for s in re.split(r'[-.]|(?=\{)|(?<=\})',w) if s]
pc_split=lambda w:[s for s in re.split(r'[|+.]',w) if s]
PE=[]; PC=[]; SUXADM=[]
lang=lambda b:(re.search(r'#atf:\s*lang\s*(\w+)',b) or [0,'?'])[1]
adm=[b for b in blocks if lang(b)=='sux' and '@seal' not in b]
for b in blocks:
    if lang(b)!='qpc': continue
    t=atf_tokens(b,pc_split)
    if len(t)<2: continue
    (PE if len(re.findall(r'\bM\d{3}',b))>=2 else PC).append(t)
for b in [adm[i] for i in rng.choice(len(adm),4000,replace=False)]:
    t=atf_tokens(b,cun_split)
    if len(t)>=2: SUXADM.append(t)
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('../scripts/seal_legends.py').read().split('# ---- common structural metrics')[0])
SUXSEAL=[[s for l in ws for w in l for s in signs(w)] for lg,ws in L if lg=='sux']
SUXSEALW=[[w for l in ws for w in l] for lg,ws in L if lg=='sux']
NUMG={'G1','G3','G4','G5','G7','G16','G17','G18','G19','G31','G32','G33','G35'}
rows=list(csv.DictReader(open('../outputs/inscriptions_ml.csv')))
IND=[['#' if s in NUMG else s for s in r['signs_reading_order'].split()] for r in rows if r['first_occurrence']=='True' and int(r['n_signs'])>=2]
LBW=[]
for name,v in load_map('../data/linearb.xyz/LinearBInscriptions.js'):
    w=[x for x in v.get('transliteratedWords',[]) if re.fullmatch(r'[a-z0-9\-]+',x) and '-' in x]
    if len(w)>=2: LBW.append(w)
corpora={'Indus (signs)':IND,'Linear A sealings':LA['sealing'],'Linear A other':LA['other'],'Linear B (signs)':LB['all'],
 'Linear B (words)':LBW,'Proto-cuneiform':PC,'Proto-Elamite':PE,'Sumerian admin (signs)':SUXADM,
 'Sumerian seals (signs)':SUXSEAL,'Sumerian seals (words)':SUXSEALW}
def dedup(T): 
    s=set(); o=[]
    for t in T:
        k=tuple(t)
        if k not in s: s.add(k); o.append(t)
    return o
def metrics(T):
    T=dedup(T)
    if len(T)>1500: T=[T[i] for i in rng.choice(len(T),1500,replace=False)]
    toks=[s for t in T for s in t]; nontok=[s for s in toks if s!='#']
    sample=[s for t in rng.permutation(np.array(T,dtype=object)) for s in t if s!='#'][:4000]
    uni=collections.Counter(toks); N=len(toks)
    big=collections.Counter((a,b) for t in T for a,b in zip(t,t[1:])); NB=sum(big.values())
    strong={p for p,c in big.items() if c>=4 and math.log2((c/NB)/((uni[p[0]]/N)*(uni[p[1]]/N)))>=3 and '#' not in p}
    inblk=sum(1 for t in T for i,s in enumerate(t) if s!='#' and ((i and (t[i-1],s) in strong) or (i<len(t)-1 and (s,t[i+1]) in strong)))/max(len(nontok),1)
    idx=rng.permutation(len(T)); rat=[]
    for a,b_ in ((idx[::2],idx[1::2]),(idx[1::2],idx[::2])):
        u=collections.Counter(s for i in a for s in T[i]+['</s>']); V=len(u)+1; Nu=sum(u.values()); bg=collections.defaultdict(collections.Counter)
        for i in a:
            for x,y in zip(['<s>']+T[i],T[i]+['</s>']): bg[x][y]+=1
        lu=lb=k=0
        for i in b_:
            for x,y in zip(['<s>']+T[i],T[i]+['</s>']):
                pu=(u[y]+1)/(Nu+V); c=bg[x]; Nc=sum(c.values()); Tc=len(c)
                pb=(Nc/(Nc+Tc))*c[y]/Nc+(Tc/(Nc+Tc))*pu if Nc else pu
                lu+=math.log(pu); lb+=math.log(pb); k+=1
        rat.append(math.exp(-lb/k)/math.exp(-lu/k))
    H=lambda c:-sum(v/sum(c.values())*math.log2(v/sum(c.values())) for v in c.values())
    en=collections.Counter(t[-1] for t in T); st=collections.Counter(t[0] for t in T)
    sing=sum(1 for v in collections.Counter(sample).values() if v==1)/max(len(set(sample)),1)
    return dict(texts=len(T),mean_len=np.mean([len(t) for t in T]),vocab_4k=len(set(sample)),singleton_share=sing,
                num_share=toks.count('#')/N,bigram_gain=np.mean(rat),in_blocks=inblk,
                H_start=H(st)/math.log2(max(len(st),2)),H_end=H(en)/math.log2(max(len(en),2)))
res={k:metrics(v) for k,v in corpora.items() if len(v)>=50}
keys=['texts','mean_len','vocab_4k','singleton_share','num_share','bigram_gain','in_blocks','H_start','H_end']
print(f'{"corpus":25s}'+''.join(f'{k[:10]:>11s}' for k in keys))
for n,r in res.items(): print(f'{n:25s}'+''.join(f'{r[k]:11.2f}' if isinstance(r[k],float) else f'{r[k]:11d}' for k in keys))
# nearest neighbours of Indus on structure (length excluded: genre-driven)
F=['vocab_4k','singleton_share','num_share','bigram_gain','in_blocks','H_start','H_end']
X=np.array([[res[n][f] for f in F] for n in res]); Z=(X-X.mean(0))/X.std(0); names=list(res)
d=np.linalg.norm(Z-Z[names.index('Indus (signs)')],axis=1)
print('\nstructural distance from Indus (standardised, length excluded):')
for i in np.argsort(d)[1:]: print(f'  {d[i]:.2f}  {names[i]}')
with open('../outputs/typology_metrics.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['corpus']+keys+['distance_to_indus'])
    for i,n in enumerate(names): w.writerow([n]+[round(res[n][k],3) if isinstance(res[n][k],float) else res[n][k] for k in keys]+[round(d[i],2)])
# robustness: nearest neighbour when each feature is left out (Linear A sealings excluded: only 63 texts)
keep=[n for n in names if n!='Linear A sealings']
print('\nnearest to Indus, leaving one feature out:')
for f in F:
    FF=[x for x in F if x!=f]
    X=np.array([[res[n][x] for x in FF] for n in keep]); Z=(X-X.mean(0))/X.std(0)
    d=np.linalg.norm(Z-Z[keep.index('Indus (signs)')],axis=1); o=[keep[i] for i in np.argsort(d)[1:3]]
    print(f'  without {f:16s}: {o[0]}, then {o[1]}')
