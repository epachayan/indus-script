import json,numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import AgglomerativeClustering
from PIL import Image, ImageDraw
H=np.load('hog.npy'); im=np.load('imgs.npy'); d=json.load(open('tags.json')); ids=d['ids']; t=d['tags']
X=PCA(60,random_state=0).fit_transform(H)
K=36
lab=AgglomerativeClustering(K,linkage='ward').fit_predict(X)
m=json.load(open('meta.json')); idx={g:i for i,g in enumerate(ids)}
pairs=[(a,b) for a,b in m['sim'] if a in idx and b in idx]
same=sum(lab[idx[a]]==lab[idx[b]] for a,b in pairs)
rng=np.random.default_rng(0); base=np.mean([lab[i]==lab[j] for i,j in rng.integers(0,len(ids),(5000,2))])
print(f'similar-pairs in same cluster: {same}/{len(pairs)}  random baseline {base:.3f}')
np.save('labels.npy',lab)
for k in range(K):
    mem=sorted([i for i in range(len(ids)) if lab[i]==k],key=lambda i:-t[str(ids[i])]['freq'])[:30]
    sh=Image.new('L',(10*60,3*60),255); dr=ImageDraw.Draw(sh)
    for n,i in enumerate(mem):
        sh.paste(Image.fromarray(255-(im[i]*255).astype(np.uint8)).resize((46,46)),(n%10*60+7,n//10*60+2))
        dr.text((n%10*60+8,n//10*60+48),f'{ids[i]}',fill=0)
    sh.save(f'c{k:02d}.png')
print(np.bincount(lab))
