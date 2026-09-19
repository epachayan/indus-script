# Sign concordance G (indus-website) <-> Parpola P (CISI digitisation) via shared CISI IDs,
# plus an estimate of how often the two corpora read signs differently.
import csv, re, collections, numpy as np
D='../data/indus_decipher/data/'
g={re.sub(r'\s+','',r['cisi_number']).upper():r['sign_sequence'].split() for r in csv.DictReader(open(D+'indus_website_real_corpus.csv'))}
c=[(r['inscription_id'],r['sign_sequence'].split()) for r in csv.DictReader(open(D+'cisi_real_corpus.csv'))]
pairs=[]
for cid,p in c:
    k=re.sub(r'\s+','',cid).upper(); k=k if k in g else k[:-1]
    if k in g: pairs.append((cid,p,g[k]))
print('matched seals',len(pairs))
def purity(orient):
    co=collections.defaultdict(collections.Counter)
    for _,p,gs in pairs:
        if len(p)!=len(gs): continue
        q=p if orient=='same' else p[::-1]
        for a,b in zip(q,gs): co[a][b]+=1
    tot=sum(sum(v.values()) for v in co.values()); top=sum(v.most_common(1)[0][1] for v in co.values())
    return top/tot, co
for o in ('same','reversed'): print(o,'orientation: position-wise agreement with best mapping %.0f%%'%(100*purity(o)[0]))
orient=max(('same','reversed'),key=lambda o:purity(o)[0])
# global alignment (Needleman-Wunsch) using the learned mapping, all pairs incl. unequal length
_,co=purity(orient)
best={a:v.most_common(1)[0][0] for a,v in co.items() if sum(v.values())>=2}
def nw(a,b):
    n,m=len(a),len(b); S=np.zeros((n+1,m+1)); S[:,0]=-np.arange(n+1); S[0,:]=-np.arange(m+1); B={}
    for i in range(1,n+1):
        for j in range(1,m+1):
            s=1 if best.get(a[i-1])==b[j-1] else -0.5
            S[i,j],B[i,j]=max((S[i-1,j-1]+s,'d'),(S[i-1,j]-1,'u'),(S[i,j-1]-1,'l'))
    i,j,al=n,m,[]
    while i>0 and j>0:
        t=B[i,j]
        if t=='d': al.append((a[i-1],b[j-1])); i-=1; j-=1
        elif t=='u': al.append((a[i-1],None)); i-=1
        else: al.append((None,b[j-1])); j-=1
    return al[::-1]
conc=collections.defaultdict(collections.Counter); agree=dis=gap=0; eq=0
for _,p,gs in pairs:
    q=p if orient=='same' else p[::-1]
    eq+=len(q)==len(gs)
    for a,b in nw(q,gs):
        if a is None or b is None: gap+=1; continue
        conc[a][b]+=1
        if best.get(a)==b: agree+=1
        else: dis+=1
print(f'orientation used: {orient}; same length in {eq}/{len(pairs)} seals')
print(f'aligned sign pairs: {agree+dis}; agree with dominant mapping {agree/(agree+dis):.0%}; unmatched (sign present in only one corpus) {gap}')
rows=[]
for a,v in sorted(conc.items()):
    n=sum(v.values()); b,k=v.most_common(1)[0]
    rows.append(dict(parpola=a,g_sign=b,n=n,consistency=round(k/n,2),alternatives=' '.join(f'{x}:{y}' for x,y in v.most_common()[1:4])))
with open('../outputs/concordance_parpola_G.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
many=collections.defaultdict(set)
for r in rows: many[r['g_sign']].add(r['parpola'])
print(f'concordance rows: {len(rows)}; fully consistent (n>=3): {sum(r["consistency"]==1 and r["n"]>=3 for r in rows)}/{sum(r["n"]>=3 for r in rows)}')
print('G signs split across several Parpola signs (sign-list granularity differences):',sum(len(v)>1 for v in many.values()))
for r in sorted(rows,key=lambda r:-r['n'])[:8]: print('  ',r)
