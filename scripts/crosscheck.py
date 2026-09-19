import json, csv, collections, numpy as np
from sklearn.metrics import adjusted_mutual_info_score as ami
f=json.load(open('func.json')); V=f['V']; lab=f['lab']; fr=f['freq']
tags={r['sign']:r for r in csv.DictReader(open('../outputs/indus_sign_tags.csv'))}
vis=[tags[s]['family'] for s in V]
obs=ami(vis,lab); rng=np.random.default_rng(0)
null=[ami(vis,list(rng.permutation(lab))) for _ in range(500)]
print(f'visual family vs behaviour class AMI={obs:.3f} null={np.mean(null):.3f}±{np.std(null):.3f} p={(1+sum(n>=obs for n in null))/501:.3f}')
m=json.load(open('meta.json')); fl=dict(zip(V,lab))
pairs=[(f'G{a}',f'G{b}') for a,b in m['sim'] if f'G{a}' in fl and f'G{b}' in fl]
print('known variant pairs with both frequent:',len(pairs),'same behaviour class:',sum(fl[a]==fl[b] for a,b in pairs), pairs)
# families spread across classes
for fam in ['jar/U-vessel','fish','human figure','human with side loops','oval with infill','grid/multi-bar']:
    c=collections.Counter(fl[s] for s in V if tags[s]['family']==fam)
    print(f'{fam:22s}', dict(c))
