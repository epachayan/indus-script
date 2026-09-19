import csv, collections, json, numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize
from sklearn.cluster import AgglomerativeClustering
tags={r['sign']:r for r in csv.DictReader(open('../outputs/indus_sign_tags.csv'))}
rows=list(csv.DictReader(open('../data/indus_decipher/data/indus_website_real_corpus.csv')))
seen=set(); texts=[]
for r in rows:
    if r['sign_sequence'] in seen: continue
    seen.add(r['sign_sequence'])
    seq=[s for s in r['sign_sequence'].split() if s in tags][::-1]   # reading order (right to left)
    if seq: texts.append(seq)
freq=collections.Counter(s for t in texts for s in t)
V=[s for s,n in freq.items() if n>=10]; vi={s:i for i,s in enumerate(V)}
print('unique texts',len(texts),'signs with >=10 uses',len(V),'covering %.0f%% of tokens'%(100*sum(freq[s] for s in V)/sum(freq.values())))
# position profile
P=np.zeros((len(V),4))  # initial, medial, final, solo
L=np.zeros((len(V),len(V)+1)); R=np.zeros((len(V),len(V)+1))
for t in texts:
    for i,s in enumerate(t):
        if s not in vi: continue
        k=3 if len(t)==1 else 0 if i==0 else 2 if i==len(t)-1 else 1
        P[vi[s],k]+=1
        l=t[i-1] if i>0 else None; r_=t[i+1] if i<len(t)-1 else None
        L[vi[s],vi.get(l,len(V))]+=1; R[vi[s],vi.get(r_,len(V))]+=1
Pn=P/P.sum(1,keepdims=True)
def ppmi(M):
    tot=M.sum(); pr=M.sum(1,keepdims=True)/tot; pc=M.sum(0,keepdims=True)/tot
    with np.errstate(divide='ignore',invalid='ignore'):
        x=np.log((M/tot)/(pr*pc)); x[~np.isfinite(x)]=0
    return np.maximum(x,0)
C=np.hstack([ppmi(L),ppmi(R)])
E=TruncatedSVD(20,random_state=0).fit_transform(C); E=normalize(E)
X=np.hstack([E, 2.0*Pn])
K=10
lab=AgglomerativeClustering(K,linkage='ward').fit_predict(X)
out={}
for k in range(K):
    m=[i for i in range(len(V)) if lab[i]==k]; p=P[m].sum(0)/P[m].sum()
    top=sorted(m,key=lambda i:-freq[V[i]])[:10]
    fams=collections.Counter(tags[V[i]]['family'] for i in m).most_common(3)
    print(f'\nC{k} n={len(m)} tokens={sum(freq[V[i]] for i in m)} init={p[0]:.0%} med={p[1]:.0%} fin={p[2]:.0%} solo={p[3]:.0%}')
    print('  ',' '.join(V[i] for i in top)); print('  ',fams)
    out[k]=[V[i] for i in m]
json.dump(dict(V=V,lab=lab.tolist(),P=P.tolist(),freq=freq,texts=texts),open('func.json','w'))
