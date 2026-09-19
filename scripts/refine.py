import json, numpy as np
from skimage.morphology import skeletonize
from scipy.ndimage import convolve
from skimage.measure import label, regionprops
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from PIL import Image, ImageDraw
im=np.load('imgs.npy'); H=np.load('hog.npy'); lab=np.load('labels.npy'); d=json.load(open('tags.json')); ids=d['ids']; t=d['tags']
def struct(a):
    b=a>0.5; sk=skeletonize(b); nb=convolve(sk.astype(int),np.ones((3,3)),mode='constant')-sk
    ends=int(((nb==1)&sk).sum()); junc=int(((nb>=3)&sk).sum())
    bg=label(~b,connectivity=1); border=set(bg[0])|set(bg[-1])|set(bg[:,0])|set(bg[:,-1])
    holes=[r.area for r in regionprops(bg) if r.label not in border and r.area>=6]
    small_holes=sum(1 for h in holes if h<40)          # hatching / grids
    rows=b.any(1); cols=b.any(0)
    return [ends,junc,len(holes),small_holes,sk.sum()/max(b.sum(),1),b.mean(),rows.sum()/max(cols.sum(),1),
            b[:32].mean()-b[32:].mean(), b[:,:32].mean()-b[:,32:].mean()]
S=np.array([struct(a) for a in im])
np.save('struct.npy',S)
MIXED={1:'comb/frame + quadruped',5:'small marked + misc',24:'mixed line groups/birds',34:'zoomorph/hatched',14:'bracketed composite'}
newname={}
sheets=[]
for c,nm in MIXED.items():
    idx=np.where(lab==c)[0]
    X=np.hstack([StandardScaler().fit_transform(S[idx])*1.5, PCA(8,random_state=0).fit_transform(H[idx])])
    best=max(range(2,5),key=lambda k:silhouette_score(X,AgglomerativeClustering(k,linkage='ward').fit_predict(X)))
    sub=AgglomerativeClustering(best,linkage='ward').fit_predict(X)
    for k in range(best):
        mem=sorted(idx[sub==k],key=lambda i:-t[str(ids[i])]['freq'])
        sh=Image.new('L',(10*56,56*((len(mem[:20])+9)//10)+14),255); dr=ImageDraw.Draw(sh); dr.text((2,1),f'cluster {c}.{k}  n={len(mem)}',fill=0)
        for n_,i in enumerate(mem[:20]):
            sh.paste(Image.fromarray(255-(im[i]*255).astype(np.uint8)).resize((42,42)),(n_%10*56+6,n_//10*56+14))
        sheets.append(sh)
        for i in mem: newname[ids[i]]=(c,k)
h=sum(s.size[1] for s in sheets); out=Image.new('L',(560,h),255); y=0
for s in sheets: out.paste(s,(0,y)); y+=s.size[1]
out.save('refine.png'); json.dump({str(k):v for k,v in newname.items()},open('refine.json','w')); print(out.size)
