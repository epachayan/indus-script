# Deciphered Mesopotamian seal legends (CDLI) vs Indus seal texts: same structural metrics.
import re, collections, math, csv, numpy as np
txt=open('../data/cdliatf_unblocked.atf',encoding='utf8',errors='replace').read()
legends=[]; langs=collections.Counter()
for b in re.split(r'\n(?=&P\d+)',txt):
    lm=re.search(r'#atf:\s*lang\s*(\w+)',b); lang=lm.group(1) if lm else '?'
    if lang not in('sux','akk'): continue
    cur=None
    for l in b.split('\n'):
        if l.startswith('@seal'): cur=[]; legends.append((lang,cur)); continue
        if l.startswith('@') and not l.startswith('@column'): cur=None; continue
        m=re.match(r"^\d+'?\.\s*(.*)",l)
        if cur is not None and m: cur.append(m.group(1))
def clean(line):
    line=re.sub(r'[\[\]#?!<>⸢⸣]','',line); line=re.sub(r'\.\.\.|\bx\b','',line)
    return [w for w in line.split() if w]
def signs(w): return [s for s in re.split(r'[-.]|(?=\{)|(?<=\})',w) if s]
seen=set(); L=[]
for lang,ls in legends:
    words=[clean(x) for x in ls]; flat=[w for line in words for w in line]
    if len(flat)<2 or any('[' in x for x in ls if x.count('[')>2): continue
    key=' / '.join(' '.join(x) for x in words)
    if key in seen: continue
    seen.add(key); L.append((lang,words))
print(f'seal sections found {len(legends)}; distinct usable legends {len(L)}',collections.Counter(l for l,_ in L))
# line-role tagging (Ur III / Akkadian seal conventions)
TITLES={'dub-sar','dumu','arad2','ir3','ir11','sanga','ensi2','sukkal','nu-banda3','ugula','kurusda','szabra','sagi','muhaldim','aszgab','dam-gar3','nar','gudu4','ensi','lugal','kal-ga','dam','sza3-tam','sipa','lu2-kin-gi4-a'}
def role(line):
    j=' '.join(line)
    if not line: return None
    if re.search(r'\b(arad2|ir3|ir11|ARAD|IR)',j): return 'SERVANT'
    if re.match(r'dumu\b|DUMU\b|mar',j): return 'FILIATION'
    if re.search(r'\blugal\b|\bszar\b|kal-ga|dannu',j): return 'ROYAL'
    if line[0].startswith('{d}') and len(line)<=2: return 'DEITY'
    if len(line)<=3 and any(w in TITLES for w in line): return 'TITLE'
    if len(line)<=2 and re.fullmatch(r'[a-z0-9\-]+',j) and '-' in j and len(j)<=10 and cnt_title[j]>=15: return 'TITLE'
    return 'NAME'
cnt_title=collections.Counter(' '.join(l) for _,ws in L for l in ws if len(l)<=2)
tmpl=collections.Counter(); ends=collections.Counter(); starts=collections.Counter()
for _,ws in L:
    r=[role(l) for l in ws if l]; r2=[x for i,x in enumerate(r) if i==0 or x!=r[i-1]]
    tmpl[' > '.join(r2)]+=1; starts[r2[0]]+=1; ends[r2[-1]]+=1
n=len(L)
print('\nLine-role templates (top 8):'); [print(f'  {c/n:5.1%}  {t}') for t,c in tmpl.most_common(8)]
print('first role:',{k:f'{v/n:.0%}' for k,v in starts.most_common(4)},'| last role:',{k:f'{v/n:.0%}' for k,v in ends.most_common(4)})
# ---- common structural metrics at SIGN level ----
def metrics(T,name):
    T=[t for t in T if len(t)>=2]
    uni=collections.Counter(s for t in T for s in t); N=sum(uni.values())
    big=collections.Counter((a,b) for t in T for a,b in zip(t,t[1:])); NB=sum(big.values())
    pmi=lambda a,b: math.log2((big[(a,b)]/NB)/((uni[a]/N)*(uni[b]/N)))
    strong={p for p,c in big.items() if c>=5 and pmi(*p)>=3}
    inblk=sum(1 for t in T for i,s in enumerate(t) if (i and (t[i-1],s) in strong) or (i<len(t)-1 and (s,t[i+1]) in strong))/N
    st=collections.Counter(t[0] for t in T); en=collections.Counter(t[-1] for t in T)
    H=lambda c:-sum(v/sum(c.values())*math.log2(v/sum(c.values())) for v in c.values())
    mid=collections.Counter(s for t in T for s in t[1:-1])
    num=np.mean([any(re.match(r'\d+\(',s) or re.fullmatch(r'G(3[1235]|[1345]|7|1[6-9])',s) for s in t) for t in T])
    # held-out bigram perplexity ratio (bigram/unigram), 2-fold
    rng=np.random.default_rng(0); idx=rng.permutation(len(T)); ratio=[]
    for a,b_ in ((idx[::2],idx[1::2]),(idx[1::2],idx[::2])):
        tr=[T[i] for i in a]; te=[T[i] for i in b_]
        u=collections.Counter(s for t in tr for s in t+['</s>']); V=len(u)+1; Nu=sum(u.values())
        bg=collections.defaultdict(collections.Counter)
        for t in tr:
            for x,y in zip(['<s>']+t,t+['</s>']): bg[x][y]+=1
        lu=lb=k=0
        for t in te:
            for x,y in zip(['<s>']+t,t+['</s>']):
                pu=(u[y]+1)/(Nu+V); c=bg[x]; Nc=sum(c.values()); Tc=len(c)
                pb=(Nc/(Nc+Tc))*c[y]/Nc+(Tc/(Nc+Tc))*pu if Nc else pu
                lu+=math.log(pu); lb+=math.log(pb); k+=1
        ratio.append(math.exp(-lb/k)/math.exp(-lu/k))
    toks=[s for t in rng.permutation(np.array(T,dtype=object)) for s in t][:5000]
    v5k=len(set(toks))
    return dict(corpus=name,vocab_at_5k=v5k,texts=len(T),mean_len=round(np.mean([len(t) for t in T]),1),vocab=len(uni),
        top3_openers=f'{sum(c for _,c in st.most_common(3))/len(T):.0%}',top_closer=f'{en.most_common(1)[0][1]/len(T):.0%}',
        H_start=round(H(st),1),H_mid=round(H(mid),1),H_end=round(H(en),1),in_blocks=f'{inblk:.0%}',
        bigram_vs_unigram_ppl=round(np.mean(ratio),2),has_number=f'{num:.0%}')
res=[]
for lang in('sux','akk'):
    res.append(metrics([[s for w in (x for l in ws for x in l) for s in signs(w)] for lg,ws in L if lg==lang],f'{lang} seal legends (signs)'))
    res.append(metrics([[w for l in ws for w in l] for lg,ws in L if lg==lang],f'{lang} seal legends (words)'))
rows=list(csv.DictReader(open('../outputs/inscriptions_ml.csv')))
res.append(metrics([r['signs_reading_order'].split() for r in rows if r['first_occurrence']=='True' and r['object_type']=='SEAL'],'Indus seals'))
res.append(metrics([r['signs_reading_order'].split() for r in rows if r['first_occurrence']=='True'],'Indus all texts'))
print()
keys=list(res[0].keys())[1:]
print(f'{"":30s}'+''.join(f'{k[:11]:>12s}' for k in keys))
for r in res: print(f'{r["corpus"]:30s}'+''.join(f'{str(r[k]):>12s}' for k in keys))
with open('../outputs/seal_legend_comparison.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=res[0].keys()); w.writeheader(); w.writerows(res)
# what closes Mesopotamian legends, for reference
en=collections.Counter(ws[-1][-1] for _,ws in L if ws and ws[-1]); print('\nmost common final words:',en.most_common(6))
