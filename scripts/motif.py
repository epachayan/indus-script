import csv,collections,numpy as np,json
from scipy.stats import fisher_exact, chi2_contingency
from statsmodels.stats.multitest import multipletests
fam={r['sign']:r['family'] for r in csv.DictReader(open('../outputs/indus_sign_tags.csv'))}
def grp(m):
    if m.startswith('Bull1'): return 'unicorn'
    return {'Gaur':'gaur','Elep':'elephant','Bult':'humped bull','Zebu':'humped bull','Rhin':'rhino','Gavi':'rhino',
            'Buff':'buffalo','Tigr':'tiger','Htgr':'tiger','Fish':'fish','Tri4':'fish','Phyt':'tree','Pipal':'tree','Anth':'anthropomorph'}.get(m)
rs=[r for r in csv.DictReader(open('../data/indus_decipher/data/indus_website_real_corpus.csv')) if grp(r['motif'])]
M=[grp(r['motif']) for r in rs]; S=[[s for s in r['sign_sequence'].split() if s in fam] for r in rs]
print('inscriptions',len(rs),collections.Counter(M))
# overall association: family tokens x motif
motifs=sorted(set(M)); fams=sorted(set(fam.values()))
def table(Mv):
    T=np.zeros((len(motifs),len(fams)))
    for m,seq in zip(Mv,S):
        for s in seq: T[motifs.index(m),fams.index(fam[s])]+=1
    return T
def cramer(T):
    T=T[:,T.sum(0)>0]; c=chi2_contingency(T)[0]; return np.sqrt(c/T.sum()/(min(T.shape)-1))
obs=cramer(table(M)); rng=np.random.default_rng(1)
null=[cramer(table(list(rng.permutation(M)))) for _ in range(300)]
print(f'Cramer V family x motif = {obs:.3f}; shuffled {np.mean(null):.3f}±{np.std(null):.3f}; p<{(1+sum(n>=obs for n in null))/301:.3f}')
# presence-based sign-level enrichment (per inscription)
res=[]
sigs=collections.Counter(s for seq in S for s in set(seq))
for m in motifs:
    inm=[i for i,x in enumerate(M) if x==m]
    for s,n in sigs.items():
        if n<8: continue
        a=sum(s in S[i] for i in inm); b=len(inm)-a; c=n-a; d=len(rs)-len(inm)-c
        if a<3: continue
        OR,p=fisher_exact([[a,b],[c,d]],alternative='greater')
        res.append((m,s,fam[s],a,len(inm),round(a/len(inm)/(n/len(rs)),1),p))
q=multipletests([r[-1] for r in res],method='fdr_bh')[1]
hits=[r+(qq,) for r,qq in zip(res,q) if qq<0.05]
for m in motifs:
    h=sorted([x for x in hits if x[0]==m],key=lambda x:x[-1])[:6]
    if h: print(m,'|',', '.join(f'{x[1]}({x[2]}) x{x[5]} [{x[3]}/{x[4]}]' for x in h))
json.dump(hits,open('motif_hits.json','w'))
