# Infer a Mahadevan (MSg) -> G sign mapping from distributional behaviour only (no shared IDs),
# anchored on the jar; validate by how many converted M77 texts appear verbatim in the G corpus.
import csv, collections, numpy as np
from scipy.optimize import linear_sum_assignment
D='../data/indus_decipher/data/'
G=[r['sign_sequence'].split() for r in csv.DictReader(open(D+'indus_website_real_corpus.csv'))]
M=[r['sign_sequence'].split() for r in csv.DictReader(open(D+'m77_indusscript_real_corpus.csv'))]
M=[t for t in M if 'MSg0' not in t]
# orientation: jar at start in G storage, at end in M storage -> reverse M to G storage order
M=[t[::-1] for t in M]
Gset=set(map(tuple,G)); fg=collections.Counter(s for t in G for s in t); fm=collections.Counter(s for t in M for s in t)
def prof(texts,s2k,keys):
    idx={k:i for i,k in enumerate(keys)}; F=collections.defaultdict(lambda:np.zeros(2*len(keys)+4))
    for t in texts:
        for i,s in enumerate(t):
            v=F[s]
            if i==0: v[-4]+=1
            if i==len(t)-1: v[-3]+=1
            if len(t)==1: v[-2]+=1
            v[-1]+=1
            if i>0 and t[i-1] in s2k: v[idx[s2k[t[i-1]]]]+=1
            if i<len(t)-1 and t[i+1] in s2k: v[len(keys)+idx[s2k[t[i+1]]]]+=1
    return F
def norm(v): v=v.copy(); n=v[-1]; v[:-1]/=max(n,1); v[-1]=0; return v/ (np.linalg.norm(v)+1e-9)
mapping={'MSg342':'G740'}
def overlap(mp):
    conv=[tuple(mp.get(s,'?') for s in t) for t in M]
    return sum(c in Gset for c in conv if '?' not in c)
for rnd in range(12):
    keys=sorted(set(mapping.values()))
    s2k_g={v:v for v in keys}; s2k_m=dict(mapping)
    Fg=prof(G,s2k_g,keys); Fm=prof(M,s2k_m,keys)
    candm=[s for s,_ in fm.most_common() if s not in mapping and fm[s]>=8][:120]
    candg=[s for s,_ in fg.most_common() if s not in mapping.values() and fg[s]>=5][:160]
    C=np.zeros((len(candm),len(candg)))
    for i,a in enumerate(candm):
        va=norm(Fm[a])
        for j,b in enumerate(candg):
            C[i,j]=-(va@norm(Fg[b])) + 0.15*abs(np.log(fm[a]/len(M))-np.log(fg[b]/len(G)))
    r,c=linear_sum_assignment(C)
    order=sorted(zip(r,c),key=lambda x:C[x])
    k=max(3,int(len(order)*0.15))          # accept the most confident 15% each round
    for i,j in order[:k]: mapping[candm[i]]=candg[j]
    print(f'round {rnd+1}: mapped {len(mapping)} signs, token coverage {sum(fm[s] for s in mapping)/sum(fm.values()):.0%}, M77 texts found verbatim in G: {overlap(mapping)}')
# null: same number of mapped signs, but frequency-rank mapping only
rank_m=[s for s,_ in fm.most_common()]; rank_g=[s for s,_ in fg.most_common()]
null=dict(zip(rank_m[:len(mapping)],rank_g[:len(mapping)]))
print('baseline (map by frequency rank only), verbatim texts:',overlap(null))
with open('../outputs/concordance_m77_G_inferred.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['m77_sign','g_sign_inferred','m77_freq','g_freq'])
    for a,b in sorted(mapping.items(),key=lambda x:-fm[x[0]]): w.writerow([a,b,fm[a],fg[b]])
print('first mappings:',list(mapping.items())[:12])

# ---- refinement: self-training on near-identical texts (<=1 mismatch, same length >=3) ----
gidx=collections.defaultdict(list)
for t in set(map(tuple,G)):
    if len(t)>=3:
        for i in range(len(t)): gidx[(len(t),i,t[:i]+t[i+1:])].append(t)
def long_verbatim(mp,L=4):
    return sum(1 for t in M if len(t)>=L and tuple(mp.get(s,'?') for s in t) in Gset)
for it in range(8):
    co=collections.defaultdict(collections.Counter); used=0
    for t in M:
        if len(t)<3: continue
        conv=tuple(mapping.get(s,'?') for s in t)
        if conv.count('?')>1: continue
        hits=set()
        for i in range(len(t)):
            for g_ in gidx.get((len(t),i,conv[:i]+conv[i+1:]),[]): hits.add(g_)
        if len(hits)!=1: continue
        g_=hits.pop(); used+=1
        for a,b in zip(t,g_): co[a][b]+=1
    new=dict(mapping)
    for a,v in co.items():
        b,k=v.most_common(1)[0]
        if k>=2 and k/sum(v.values())>=0.6: new[a]=b
    changed=sum(new.get(a)!=mapping.get(a) for a in new)
    mapping=new
    print(f'refine {it+1}: {used} near-matched texts, {changed} mappings changed/added, total {len(mapping)}, coverage {sum(fm[s] for s in mapping)/sum(fm.values()):.0%}, verbatim (len>=4) {long_verbatim(mapping)}')
    if changed==0: break
print('baseline verbatim (len>=4):',long_verbatim(null))
chk={k:mapping.get(k) for k in ('MSg342','MSg99','MSg267','MSg391','MSg150','MSg1','MSg176','MSg123')}
print('checks:',chk)
conv=[tuple(mapping.get(s,'?') for s in t) for t in M]
print(f'M77 texts (len>=4) matching a G text verbatim: {sum(1 for c in conv if len(c)>=4 and c in Gset)}/{sum(1 for c in conv if len(c)>=4)}')
with open('../outputs/concordance_m77_G_inferred.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['m77_sign','g_sign_inferred','m77_freq','g_freq'])
    for a,b in sorted(mapping.items(),key=lambda x:-fm[x[0]]): w.writerow([a,b,fm[a],fg[b]])
