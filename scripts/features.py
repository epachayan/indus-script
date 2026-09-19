import json, numpy as np
from PIL import Image, ImageDraw, ImageFont
from skimage.feature import hog
from skimage.measure import label, regionprops, euler_number
from skimage.morphology import skeletonize
m=json.load(open('meta.json')); cp={int(k):v for k,v in m['cp'].items()}
freq={int(k):v for k,v in m['freq'].items()}
font=ImageFont.truetype('../data/indus-website/src/assets/fonts/sk_indus_script-webfont.ttf',160)
S=64; ids=[]; imgs=[]; feats=[]; tags={}
for gid,c in sorted(cp.items()):
    im=Image.new('L',(260,260),0); ImageDraw.Draw(im).text((40,20),chr(c),font=font,fill=255)
    a=np.array(im)>128
    if a.sum()<20: continue
    ys,xs=np.where(a); a=a[ys.min():ys.max()+1,xs.min():xs.max()+1]
    h,w=a.shape; side=max(h,w); pad=np.zeros((side,side),bool)
    pad[(side-h)//2:(side-h)//2+h,(side-w)//2:(side-w)//2+w]=a
    small=np.array(Image.fromarray((pad*255).astype(np.uint8)).resize((S,S),Image.LANCZOS))/255.
    b=small>0.5
    lab=label(b,connectivity=2); allr=regionprops(lab)
    dots=[r for r in allr if max(r.bbox[2]-r.bbox[0],r.bbox[3]-r.bbox[1])<=4]
    for r in dots: b[lab==r.label]=False
    regs=[r for r in allr if r not in dots]; dotted=len(dots)>=4
    ncomp=len(regs); bg=label(~b,connectivity=1); border=set(bg[0,:])|set(bg[-1,:])|set(bg[:,0])|set(bg[:,-1])
    holes=sum(1 for r in regionprops(bg) if r.label not in border and r.area>=15)
    bars=sum(1 for r in regs if (r.bbox[2]-r.bbox[0])>=2.5*max(1,r.bbox[3]-r.bbox[1]) and r.extent>0.6)
    symLR=1-np.abs(b^b[:,::-1]).mean()/max(b.mean(),1e-3)/2
    symUD=1-np.abs(b^b[::-1,:]).mean()/max(b.mean(),1e-3)/2
    t=[]
    if dotted: t.append('numeral-marked')
    if ncomp==1 and bars==1: t.append('single-stroke')
    if dotted or (ncomp>=2 and bars==ncomp): t.append('stroke-numeral')
    elif bars>=2: t.append('has-strokes')
    if holes>=1: t.append('enclosed')
    if symLR>0.85: t.append('symmetric-LR')
    if symUD>0.85: t.append('symmetric-UD')
    if ncomp>=3 and 'stroke-numeral' not in t: t.append('multi-part')
    ar=w/h
    t.append('wide' if ar>1.6 else 'tall' if ar<0.6 else 'squarish')
    hf=hog(small,orientations=9,pixels_per_cell=(8,8),cells_per_block=(2,2))
    ids.append(gid); imgs.append(small.astype(np.float32)); feats.append(hf)
    tags[gid]=dict(tags=t,ncomp=ncomp,holes=int(holes),bars=bars,ink=float(b.mean()),freq=freq.get(gid,0),
                   symLR=round(float(symLR),2),aspect=round(ar,2))
np.save('imgs.npy',np.array(imgs)); np.save('hog.npy',np.array(feats)); json.dump(dict(ids=ids,tags=tags),open('tags.json','w'))
print(len(ids),'rendered')
