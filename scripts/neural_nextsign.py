# Small neural (MLP) next-sign model vs bigram, with near-duplicate-aware (grouped) vs random splits.
import csv, collections, numpy as np, warnings
from scipy.sparse import lil_matrix
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GroupKFold, KFold
warnings.filterwarnings('ignore')
rows=list(csv.DictReader(open('../outputs/inscriptions_ml.csv')))
tags={r['sign']:r for r in csv.DictReader(open('../outputs/indus_sign_tags.csv'))}
T=[r['signs_reading_order'].split() for r in rows if r['first_occurrence']=='True' and int(r['n_signs'])>=2]
# groups: union texts that differ by one substitution / insertion / deletion
par=list(range(len(T)))
def f(x):
    while par[x]!=x: par[x]=par[par[x]]; x=par[x]
    return x
keys=collections.defaultdict(list)
for i,t in enumerate(T):
    for j in range(len(t)): keys[('sub',tuple(t[:j]),tuple(t[j+1:]),len(t))].append(i)
    keys[('del',tuple(t))].append(i)
    for j in range(len(t)): keys[('del',tuple(t[:j]+t[j+1:]))].append(i)
for v in keys.values():
    for i in v[1:]: par[f(i)]=f(v[0])
groups=np.array([f(i) for i in range(len(T))])
print(f'texts {len(T)}, near-duplicate groups {len(set(groups))} (largest {collections.Counter(groups).most_common(1)[0][1]})')
V=sorted({s for t in T for s in t}); vi={s:i for i,s in enumerate(V)}
fam=sorted({tags[s]['family'] for s in V}); fi={x:i for i,x in enumerate(fam)}
beh=sorted({tags[s]['behaviour_class'] or 'rare' for s in V}); bi={x:i for i,x in enumerate(beh)}
top=[s for s,_ in collections.Counter(s for t in T for s in t+['</s>'] if True).most_common(150)]
ti={s:i for i,s in enumerate(top)}
D=2*len(V)+2*len(fam)+2*len(beh)+6+2
samples=[]
for k,t in enumerate(T):
    p=['<s>','<s>']+t
    for i in range(2,len(p)+1):
        y=p[i] if i<len(p) else '</s>'
        samples.append((k,p[i-2],p[i-1],i-2,len(t),y))
def featurize(idx):
    X=lil_matrix((len(idx),D),dtype=np.float32)
    for r,j in enumerate(idx):
        _,a,b,pos,L,_=samples[j]; o=0
        for s in (a,b):
            if s in vi: X[r,o+vi[s]]=1; X[r,2*len(V)+(o>0)*len(fam)+fi[tags[s]['family']]]=1; X[r,2*len(V)+2*len(fam)+(o>0)*len(beh)+bi[tags[s]['behaviour_class'] or 'rare']]=1
            else: X[r,D-2+(o>0)]=1
            o=len(V)
        X[r,2*len(V)+2*len(fam)+2*len(beh)+min(pos,5)]=1
    return X.tocsr()
y=np.array([ti.get(s[5],-1) for s in samples]); ok=np.where(y>=0)[0]
tg=np.array([groups[s[0]] for s in samples])
def bigram_acc(tr,te):
    c=collections.defaultdict(collections.Counter)
    for j in tr: c[samples[j][2]][samples[j][5]]+=1
    glob=collections.Counter(samples[j][5] for j in tr)
    hit=[]
    for j in te:
        cand=c[samples[j][2]] or glob
        hit.append(cand.most_common(1)[0][0]==samples[j][5])
    return np.mean(hit)
for name,split in (('random split',KFold(5,shuffle=True,random_state=0).split(ok)),('grouped split',GroupKFold(5).split(ok,groups=tg[ok]))):
    a_mlp=[];a_bg=[]
    for k,(tr,te) in enumerate(split):
        if k>=3: break
        tr,te=ok[tr],ok[te]
        m=MLPClassifier(hidden_layer_sizes=(128,),max_iter=60,early_stopping=True,random_state=0)
        m.fit(featurize(tr),y[tr]); a_mlp.append(m.score(featurize(te),y[te])); a_bg.append(bigram_acc(tr,te))
    print(f'{name:14s}: MLP top-1 {np.mean(a_mlp):.1%}   bigram top-1 {np.mean(a_bg):.1%}')
